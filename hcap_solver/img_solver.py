from typing import Any

from hcap_solver.motiondata import *
from hcap_solver.nocap_ai import *
from hcap_solver.logger import *
from datetime import datetime
from hcap_solver.hsw import *
import requests
import base64
import time
import json
import re

js = requests.get("https://js.hcaptcha.com/1/api.js").text
version = re.search(r'v1/(.*?)/', js).group(1)


class HCaptcha:
    def __init__(self, site_key: str, host: str, proxy: str = None, rq_data: str = None) -> None:
        self.hsw_key = database_fps.randomkey()
        self.job = None
        self.key = None
        self.c2 = None
        self.session = requests.Session()
        self.proxy = proxy
        self.before = time.time()
        self.session.headers = {
            'authority': 'hcaptcha.com',
            'accept': 'application/json',
            'accept-language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'text/plain',
            'origin': 'https://newassets.hcaptcha.com',
            'referer': 'https://newassets.hcaptcha.com/',
            'sec-ch-ua': '"Chromium";v="120", "Google Chrome";v="120", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        self.proxy = proxy
        self.session.proxies = {'http': f'http://{self.proxy}', 'https': f'http://{self.proxy}'} if proxy else None
        self.site_key = site_key
        self.host = host.split("//")[-1].split("/")[0]
        self.rq_data = rq_data
        self.motion = MotionData(self.session.headers["user-agent"], f"https://{self.host}")
        self.motion_data = self.motion.get_captcha()

    def hsw(self, req: str) -> str:
        s = req.split(".")[1].encode()
        s += b'=' * (-len(s) % 4)
        data = json.loads(base64.b64decode(s, validate=False).decode())
        return pull(self.hsw_key, data['s'], data['d'])

    def solve(self) -> str:
        try:
            captcha = self.siteconfig()
            hsw = self.hsw(captcha["req"])
            got_captcha = self.getcaptcha(hsw, captcha)
            answers = self.get_answers(got_captcha)
            if answers:
                solve_time1 = round(time.time() - self.before, 2)
                sleep_total = 3.9 - solve_time1
                if sleep_total >= 0:
                    time.sleep(sleep_total)
                hsw2 = self.hsw(self.c2["req"])
                response = self.submit_captcha(answers, hsw2)
                if response:
                    try:
                        capkey = response["generated_pass_UUID"]
                        log.captcha(f"Solved hCaptcha {capkey[:70]}", self.before, time.time())
                        return capkey
                    except Exception:
                        log.failure(f"Failed To Solve hCaptcha", self.before, time.time(), level="hCaptcha")
        except Exception as e:
            log.failure(f"Failed To Solve hCaptcha -> {e}", self.before, time.time(), level="hCaptcha")
            # traceback.print_exc()

    def submit_captcha(self, answers: dict, hsw2: str) -> Any | None:
        self.session.headers.update({'content-type': 'application/json;charset=UTF-8'})
        motion = self.motion.check_captcha(answers, "image_label_binary")
        try:
            return self.session.post(
                f'https://hcaptcha.com/checkcaptcha/{self.site_key}/{self.key}',
                json={
                    'v': version,
                    'job_mode': self.job,
                    'answers': answers,
                    'serverdomain': self.host,
                    'sitekey': self.site_key,
                    'motionData': json.dumps(motion),
                    'n': hsw2,
                    'c': json.dumps(self.c2),
                },
            ).json()
        except Exception:
            return None

    def get_answers(self, captcha: dict) -> dict:
        target = captcha["requester_question"]["en"]
        captcha_type = captcha["request_type"]

        self.c2 = captcha['c']
        self.key = captcha['key']
        log.captcha(f"Solving Captcha -> {captcha_type}...")
        if captcha_type == "image_label_binary":
            images = {
                "image1": captcha['tasklist'][0]["datapoint_uri"],
                "image2": captcha['tasklist'][1]["datapoint_uri"],
                "image3": captcha['tasklist'][2]["datapoint_uri"],
                "image4": captcha['tasklist'][3]["datapoint_uri"],
                "image5": captcha['tasklist'][4]["datapoint_uri"],
                "image6": captcha['tasklist'][5]["datapoint_uri"],
                "image7": captcha['tasklist'][6]["datapoint_uri"],
                "image8": captcha['tasklist'][7]["datapoint_uri"],
                "image9": captcha['tasklist'][8]["datapoint_uri"]
            }
            solution = solve_grid(target, images, self.site_key, self.host)["solution"]
            self.job = "image_label_binary"
            return {
                captcha['tasklist'][0]["task_key"]: str(0 in solution).lower(),
                captcha['tasklist'][1]["task_key"]: str(1 in solution).lower(),
                captcha['tasklist'][2]["task_key"]: str(2 in solution).lower(),
                captcha['tasklist'][3]["task_key"]: str(3 in solution).lower(),
                captcha['tasklist'][4]["task_key"]: str(4 in solution).lower(),
                captcha['tasklist'][5]["task_key"]: str(5 in solution).lower(),
                captcha['tasklist'][6]["task_key"]: str(6 in solution).lower(),
                captcha['tasklist'][7]["task_key"]: str(7 in solution).lower(),
                captcha['tasklist'][8]["task_key"]: str(8 in solution).lower()
            }

        elif captcha_type == "image_label_area_select":
            self.job = "image_label_area_select"
            return solve_area_select(target, captcha['tasklist'], self.site_key, self.host)

        else:
            log.failure(f"Unsupported Captcha Type -> {captcha_type}", level="hCaptcha")

    def getcaptcha(self, hsw: str, c: dict) -> dict:
        self.session.headers.update({'content-type': 'application/x-www-form-urlencoded'})
        data = {
            'v': version,
            'sitekey': self.site_key,
            'host': self.host,
            'hl': 'sv',
            'motionData': json.dumps(self.motion_data),
            'pdc': {"s": round(datetime.now().timestamp() * 1000), "n": 0, "p": 1, "gcs": 32},
            'n': hsw,
            'c': json.dumps(c),
            'pst': 'false'
        }
        if self.rq_data is not None: data['rqdata'] = self.rq_data
        return self.session.post(f'https://hcaptcha.com/getcaptcha/{self.site_key}', data=data).json()

    def siteconfig(self) -> dict:
        return self.session.post("https://hcaptcha.com/checksiteconfig", params={
            'v': version,
            'host': self.host,
            'sitekey': self.site_key,
            'sc': '1',
            'swa': '1',
            'spst': '1',
        }).json()["c"]
