from hcap_solver.motiondata import *
from hcap_solver.nocap_ai import *
from hcap_solver.logger import *
from datetime import datetime
from bs4 import BeautifulSoup
from hcap_solver.hsw import *
import requests
import base64
import time
import json
import re

js = requests.get("https://js.hcaptcha.com/1/api.js").text
version = re.search(r'v1/(.*?)/', js).group(1)

class Hcaptcha:
    def __init__(self, sitekey: str, host: str, proxy: str = None, rqdata: str = None) -> None:
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
        self.sitekey = sitekey
        self.host = host.split("//")[-1].split("/")[0]
        self.rqdata = rqdata
        self.motion = MotionData(self.session.headers["user-agent"], f"https://{self.host}")
        self.motiondata = self.motion.get_captcha()

    def solve(self) -> None:
        captcha = self.siteconfig()

        if captcha:
            hsw = self.get_hsw(captcha["req"])
            got_captcha = self.getcaptcha(hsw, captcha)
            
            if captcha:
                answers = self.get_answers(got_captcha)

                if answers:
                    solve_time1 = round(time.time()-self.before,2)
                    sleep_total = 3.9 - solve_time1
                    
                    if sleep_total >= 0:
                        time.sleep(sleep_total)
                        
                    hsw2 = self.get_hsw(self.c2["req"])
                    response = self.submit_captcha(answers, hsw2)

                    if response:
                        try:
                            capkey = response["generated_pass_UUID"]
                            log.captcha(f"Solved hCaptcha {capkey[:70]}", self.before, time.time())
                            return capkey
                        except Exception:
                            log.failure(f"Failed To Solve hCaptcha", self.before, time.time(), level="hCaptcha")
        
    def submit_captcha(self, answers: dict, hsw2: str) -> dict:
        self.session.headers.update({'content-type': 'application/json;charset=UTF-8'})
        try:
            return self.session.post(
                f'https://hcaptcha.com/checkcaptcha/{self.sitekey}/{self.key}',
                json={
                    'v': version,
                    'job_mode': self.job,
                    'answers': answers,
                    'serverdomain': self.host,
                    'sitekey': self.sitekey,
                    'motionData': json.dumps(self.motiondata),
                    'n': hsw2,
                    'c': json.dumps(self.c2),
                },
            ).json()
        except Exception:
            return None
        
    def get_answers(self, captcha: dict) -> dict:
        target = captcha["requester_question"]["en"]
        captcha_type = captcha["request_type"]

        self.c2  = captcha['c']
        self.key = captcha['key']
        log.captcha(f"Solving Captcha -> {captcha_type}...")
        if captcha_type == "image_label_binary":
            images = {f"image{i+1}": captcha['tasklist'][i]["datapoint_uri"] for i in range(9)}
            solution = solve_grid(target, images, self.sitekey, self.host)["solution"]
            self.job = "image_label_binary"
            return {captcha['tasklist'][i]["task_key"]: str(i in solution).lower() for i in range(9)}

        elif captcha_type == "image_label_area_select":
            self.job = "image_label_area_select"
            return solve_area_select(target, captcha['tasklist'], self.sitekey, self.host)

        else:
            log.failure(f"Unsupported Captcha Type -> {captcha_type}", level="hCaptcha")

    def ardata(self):
        r = self.session.get("https://newassets.hcaptcha.com/captcha/v1/fadb9c6/static/hcaptcha.html?_v=n2igxf14d2i")
        soup = BeautifulSoup(r.text, 'html.parser')
        tag = soup.find('script', {'src': re.compile(r'hcaptcha\.js#i=')})
        ardata = tag['src'].split('#i=')[1]
        return ardata

    def get_hsw(self, req: str) -> str:
        ardata = self.ardata()
        s = req.split(".")[1].encode()
        s += b'=' * (-len(s) % 4)
        data = json.loads(base64.b64decode(s, validate=False).decode())
        return pull(data['s'], data['d'], ardata)

    def getcaptcha(self, hsw:str, c:dict) -> dict:
        self.session.headers.update({'content-type': 'application/x-www-form-urlencoded'})
        data = {
            'v': version,
            'sitekey': self.sitekey,
            'host':self.host,
            'hl': 'sv',
            'motionData': json.dumps(self.motiondata),
            'pdc': {"s": round(datetime.now().timestamp() * 1000), "n":0, "p":1, "gcs":32},
            'n':hsw,
            'c':json.dumps(c),
            'pst':'false'
        }
        if self.rqdata is not None: data['rqdata'] = self.rqdata
        return self.session.post(f'https://hcaptcha.com/getcaptcha/{self.sitekey}', data=data).json()

    def siteconfig(self) -> dict:
        return self.session.post("https://hcaptcha.com/checksiteconfig", params = {
            'v': version,
            'host': self.host,
            'sitekey': self.sitekey,
            'sc': '1',
            'swa': '1',
            'spst': '1',
        }).json()["c"]
