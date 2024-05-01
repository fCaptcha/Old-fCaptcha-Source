import json
import random
import typing
from hashlib import sha1
from io import BytesIO

import httpx
import imagehash
import tls_client
from PIL import Image
from redis.client import Redis

from hcap_solver import MotionData, HSW
from hcap_solver.nocap_ai import NoCapAIClient

CLIENT = httpx.Client()


def hostname_from_url(url):
    return url.split("://", 1)[1].split("/", 1)[0].lower()


DATABASE = Redis("45.45.238.213", 42081, 239,
                 "ACCA5B570561DCFA5ACB1417C69F2900DAFF8A4FD39A2E66C36DF2BD796F0BE1CFEA8AF2DB18153874215E08BFDEC4A89A397EC53E52DAC33A1E9D0B17A52D43")


class Tile(object):
    image_id: str
    image_index: int
    image_content: bytes

    def __init__(self, image_id: str, image_index: int, image_content: bytes):
        self.selected = False
        self.image_id = image_id
        self.image_content = image_content
        self.image_index = image_index


class HCaptchaEnterpriseChallenge(object):
    site_key: str
    site_url: str
    tiles: list[Tile]

    def __init__(self, site_key: str,
                 site_url: str,
                 extra_data: dict[str, str] = None,
                 proxy: str = None,
                 agent: str = None,
                 database: typing.Union[Redis, typing.Mapping] = DATABASE) -> None:
        if extra_data is None:
            extra_data = dict[str, str]()
        self.database = database
        self.hsw = HSW()
        self.answered = []
        self.tiles = list[Tile]()
        self.site_key = site_key
        self.site_url = hostname_from_url(site_url)
        self.extra_data = extra_data
        self.agent = agent if agent else "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9038 Chrome/120.0.6099.291 Electron/28.2.7 Safari/537.36"
        self.client = tls_client.Session("chrome_108", random_tls_extension_order=True)
        self.client.proxies = proxy
        resp = self.client.get("https://hcaptcha.com/1/api.js")
        data = resp.text
        start = data.find("https://newassets.hcaptcha.com/captcha/") + 42
        end = data[start:].find("/") + start
        self.version = data[start:end]
        self.motion_data = MotionData(self.agent, site_url)
        self.token = self._obtain_token()
        self.challenge = self._obtain_chl()
        if self.challenge.get("pass"):
            self.solved_token = self.challenge.get("generated_pass_UUID")
        else:
            self.solved_token = None
        self.proof_data = self.challenge.get("c")
        self.game_variant = self.challenge.get("requester_question").get("en")
        self.game_token = self.challenge.get("key")
        self.tiles = [
            Tile(info.get("task_key"), index, CLIENT.get(info.get("datapoint_uri"), headers={
                "Accept-Encoding": "gzip"
            }).content)
            for index, info in enumerate(self.challenge.get("tasklist"))
        ]

    def _obtain_token(self) -> dict:
        return self.client.get(f"https://hcaptcha.com/checksiteconfig?v={self.version}&host={self.site_url}"
                               f"&sitekey={self.site_key}&sc=1&swa=1",
                               headers={
                                   "accept": "application/json",
                                   "accept-encoding": "gzip, deflate, br",
                                   "accept-language": "en-US,en;q=0.9",
                                   "content-type": "application/x-www-form-urlencoded",
                                   "origin": "https://newassets.hcaptcha.com",
                                   "referer": "https://newassets.hcaptcha.com/",
                                   "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\""
                                                ";v=\"113\", \"Not-A.Brand\";v=\"24\"",
                                   "sec-ch-ua-mobile": "?0",
                                   "sec-ch-ua-platform": "\"Windows\"",
                                   "sec-fetch-dest": "empty",
                                   "sec-fetch-mode": "cors",
                                   "sec-fetch-site": "same-site",
                                   "user-agent": self.agent
                               }).json().get("c")

    def _obtain_chl(self) -> dict:
        return self.client.post(f"https://hcaptcha.com/getcaptcha/{self.site_key}", headers={
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://newassets.hcaptcha.com",
            "referer": "https://newassets.hcaptcha.com/",
            "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": self.agent
        }, data={
            "v": self.version,
            "sitekey": self.site_key,
            "host": self.site_url,
            "hl": "en",
            **self.extra_data,
            "motiondata": self.motion_data.get_captcha(),
            "n": self.hsw.pull(self.token.get("req"), self.site_url),
            "c": json.dumps(self.token)
        }).json()

    def solve(self, brute: bool) -> str | None:
        if self.solved_token:
            return self.solved_token
        question_hash = sha1(self.game_variant.encode()).hexdigest()
        for tile in self.tiles:
            image_hash = imagehash.phash(Image.open(BytesIO(tile.image_content)), 32)
            tile.custom_id = f"{question_hash}|{image_hash}"
            tile.score = int(self.database.get(tile.custom_id) or 0)
        if brute:
            self.tiles.sort(
                key=lambda _tile: _tile.score or random.uniform(0, 0.97),
                reverse=True)
            n_answers = max(3,
                            len(list(filter(lambda t: t.score >= 1, self.tiles))))
            for index in range(n_answers):
                tile = self.tiles[index]
                tile.selected = True
        else:
            if answers := NoCapAIClient("image_label_binary", self.challenge, self.site_key, self.site_url).solve():
                for idx in range(len(self.tiles)):
                    if bool(answers.get(self.tiles[idx].image_id)):
                        self.tiles[idx].selected = True
        token: dict = self._submit()
        if token.get("generated_pass_UUID"):
            for tile in self.tiles:
                if not tile.selected:
                    continue
                self.database.incrbyfloat(tile.custom_id, 1)
            return token.get("generated_pass_UUID")

    def _submit(self):
        answers: dict = {
            tile.image_id: "true" if tile.selected else "false" for tile in self.tiles
        }
        return self.client.post(f"https://hcaptcha.com/checkcaptcha/{self.site_key}/{self.game_token}", headers={
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "Content-type": "application/json;charset=UTF-8",
            "origin": "https://newassets.hcaptcha.com",
            "referer": "https://newassets.hcaptcha.com/",
            "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": self.agent
        }, json={
            "v": self.version,
            "job_mode": "image_label_binary",
            "answers": answers,
            "serverdomain": self.site_url,
            "sitekey": self.site_key,
            "motionData": json.dumps(self.motion_data.check_captcha(answers)),
            "n": self.hsw.pull(self.proof_data.get("req"), self.site_url),
            "c": json.dumps(self.proof_data)
        }).json()
