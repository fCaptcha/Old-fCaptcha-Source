from hcap_solver.motiondata import *
from hcap_solver.logger import *
from tls_client import Session
from datetime import datetime
from hcap_solver.hsw import *
from typing import Any
import traceback
import requests
import random
import time
import json
import re

from matplotlib import pyplot
import matplotlib.image as mpimg

def show(mouse_data):
    img = mpimg.imread('fcap.png')
    dpi = 100
    fig_width = img.shape[1] / dpi
    fig_height = img.shape[0] / dpi
    fig, ax = pyplot.subplots(figsize=(fig_width, fig_height), dpi=dpi)
    ax.imshow(img, extent=[0, img.shape[1], 0, img.shape[0]])

    x_data = [data[0] for data in mouse_data]
    y_data = [data[1] for data in mouse_data]

    x = [(data - min(x_data)) * img.shape[1] / (max(x_data) - min(x_data)) for data in x_data]
    y = [(data - min(y_data)) * img.shape[0] / (max(y_data) - min(y_data)) for data in y_data]

    ax.plot(x, y, color='red')
    pyplot.xlabel('X position')
    pyplot.ylabel('Y position')
    pyplot.title('Motiondata')
    pyplot.show()

js = requests.get("https://js.hcaptcha.com/1/api.js").text
version = re.search(r'v1/(.*?)/', js).group(1)

class Hcaptcha:
    def __init__(self, site_key: str, host: str, proxy: str, user_agent: str = None,  rq_data: str = None) -> None:
        self.hsw = HSW()
        self.job = None
        self.key = None
        self.c2 = None
        self.session = Session("chrome_120", random_tls_extension_order=True)
        self.before = time.time()
        self.user_agent = user_agent if user_agent else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        self.session.headers = {
            'accept': '*/*',
            'accept-language': 'en-AU,en;q=0.9,fa;q=0.8,en-US;q=0.7,sv;q=0.6',
            'content-type': 'application/json;charset=UTF-8',
            'dnt': "1",
            'origin': 'https://newassets.hcaptcha.com',
            'referer': 'https://newassets.hcaptcha.com/',
            'sec-ch-ua': '"Google Chrome";v="120", "Not:A-Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': self.user_agent,
        }
        proxy = proxy.split('://', 1)[-1]
        self.session.proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        self.site_key = site_key
        self.host = host.split("//")[-1].split("/")[0]
        self.rq_data = rq_data
        self.motion = MotionData(self.user_agent, f"https://{self.host}")
        self.motion_data = self.motion.get_captcha()

    def solve(self) -> str:
        try:
            captcha = self.siteconfig()
            hsw = self.hsw.pull(captcha["req"], self.host, self.user_agent)
            got_captcha = self.getcaptcha(hsw, captcha)
            answers = self.get_answers(got_captcha)
            if answers:
                #solve_time1 = round(time.time() - self.before, 2)
                #sleep_total = 3.9 - solve_time1
                #if sleep_total >= 0:
                #    time.sleep(sleep_total)
                hsw2 = self.hsw.pull(self.c2["req"], self.host, self.user_agent)
                response = self.submit_captcha(answers, hsw2)
                if response:
                    try:
                        capkey = response["generated_pass_UUID"]
                        log.captcha(f"Solved hCaptcha {capkey[:50]}", self.before, time.time())
                        return capkey
                    except Exception:
                        log.failure(f"Failed To Solve hCaptcha", self.before, time.time(), level="hCaptcha")
        except Exception as e:
            log.failure(f"Failed To Solve hCaptcha -> {e}", self.before, time.time(), level="hCaptcha")
            traceback.print_exc()

    def submit_captcha(self, answers: dict, hsw2: str) -> Any | None:
        self.session.headers.update({'content-type': 'application/json;charset=UTF-8'})
        motion = self.motion.check_captcha(answers)
        #show(motion["mm"])
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
        captcha_type = captcha["request_type"]
        self.c2 = captcha['c']
        self.key = captcha['key']
        log.captcha(f"Solving Captcha -> {captcha_type}...")
        self.job = captcha_type
        json = {
            "captcha_type": captcha_type,
            "captcha_json": captcha,
            "sitekey": self.site_key,
            "host": self.host,
            "key": "6643617074636861206f6e20746f7021"
        }
        return httpx.post("http://solver.dexv.lol:1000/solve_ai", json=json, timeout=1000).json()

    def getcaptcha(self, hsw: str, c: dict) -> dict:
        self.session.headers.update({'content-type': 'application/x-www-form-urlencoded'})
        data = {
            'v': version,
            'sitekey': self.site_key,
            'host': self.host,
            'hl': 'sv',
            'motionData': json.dumps(self.motion_data),
            'pdc': {"s": round(datetime.now().timestamp() * 1000), "n": 0, "p": random.randint(0, 2), "gcs": random.randint(30, 658)},
            'pem': {"csc":random.uniform(100, 2500)},
            'n': hsw,
            'c': json.dumps(c),
            'pst': 'false'
        }
        if self.rq_data is not None: data['rqdata'] = self.rq_data
        return self.session.post(f'https://hcaptcha.com/getcaptcha/{self.site_key}', data=data).json()

    def siteconfig(self) -> dict:
        return self.session.post("https://api.hcaptcha.com/checksiteconfig", params={
            'v': version,
            'host': self.host,
            'sitekey': self.site_key,
            'sc': '1',
            'swa': '1',
            'spst': '1',
        }).json()["c"]
