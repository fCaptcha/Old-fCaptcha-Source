from concurrent.futures import ThreadPoolExecutor
from python_ghost_cursor import path
from subprocess import check_output
from hcap_solver.logger import log
from tls_client import Session
from datetime import datetime
from json import dumps
from re import findall
from time import time
import requests
import random
import ctypes
import json
import g4f

class Hcaptcha:
    def __init__(self, sitekey: str, host: str, proxy: str = None) -> None:
        self.session = Session(client_identifier='chrome_118', random_tls_extension_order=True)
        self.session.headers = {
            "host": 'hcaptcha.com',
            "connection": 'keep-alive',
            "accept": 'application/json',
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            "sec-ch-ua": '"Chromium";v="118", "Not A(Brand";v="24", "Google Chrome";v="118"',
            "sec-ch-ua-mobile": '?0',
            "sec-ch-ua-platform": '"Windows"',
            "origin": 'https://newassets.hcaptcha.com',
            "referer": 'https://newassets.hcaptcha.com/',
            "sec-fetch-site": 'same-site',
            "sec-fetch-mode": 'cors',
            "sec-fetch-dest": 'empty',
            "accept-encoding": 'gzip, deflate, br',
            "accept-language": 'en-US,en;q=0.9,sv-SE;q=0.8,sv;q=0.7'
        }

        self.proxy = proxy
        self.session.proxies = {'http': f'http://{self.proxy}', 'https': f'http://{self.proxy}'} if proxy else None
        self.api_js = self.session.get('https://hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaOnLoad').text
        self.version = findall(r'v1\/([A-Za-z0-9]+)\/static', self.api_js)[1]
        self.sitekey = sitekey
        self.host = host
        self.siteconfig = self.get_siteconfig()
        self.captcha1 = self.get_captcha1()
        self.captcha2 = self.get_captcha2()

    def get_siteconfig(self) -> dict:
        s = time()
        siteconfig = self.session.post(f"https://hcaptcha.com/checksiteconfig", params={
            'v': self.version,
            'sitekey': self.sitekey,
            'host': self.host,
            'sc': '1', 
            'swa': '1', 
            'spst': '1'
        })
        #log.info(f"Got Site Config / ({siteconfig.status_code})", s, time())
        return siteconfig.json()

    def get_captcha1(self) -> dict:
        s = time()
        getcaptcha = self.session.post(f"https://hcaptcha.com/getcaptcha/{self.sitekey}", data={
            'v': self.version,
            'sitekey': self.sitekey,
            'host': self.host,
            'hl': 'en',
            'motionData': dumps(self.motion_data()),
            'pdc':  {"s": round(datetime.now().timestamp() * 1000), "n":0, "p":0, "gcs":10},
            'n': self.hsw(self.siteconfig['c']['req']),
            'c': dumps(self.siteconfig['c']),
            'pst': False
        })
        #log.info(f"Got Captcha Number 1 / ({getcaptcha.status_code})", s, time())
        return getcaptcha.json()
    
    def get_captcha2(self) -> dict:
        s = time()
        getcaptcha2 = self.session.post(f"https://hcaptcha.com/getcaptcha/{self.sitekey}", data={
            'v': self.version,
            'sitekey': self.sitekey,
            'host': self.host,
            'hl': 'en',
            'a11y_tfe': 'true',
            'action': 'challenge-refresh',
            'old_ekey'  : self.captcha1['key'],
            'extraData': self.captcha1,
            'motionData': dumps(self.motion_data()),
            'pdc':  {"s": round(datetime.now().timestamp() * 1000), "n":0, "p":0, "gcs":10},
            'n': self.hsw(self.captcha1['c']['req']),
            'c': dumps(self.captcha1['c']),
            'pst': False
        })
        #log.info(f"Got Captcha Number 2 / ({getcaptcha2.status_code})", s, time())
        return getcaptcha2.json()

    def motion_data(self):
        start, end = {'x': 100, 'y': 100}, {'x': 600, 'y': 700}
        mm = [[int(p['x']), int(p['y']), int(time() * 1000) + round(random.random() * (5000 - 2000) + 2000)] for p in path(start, end)]
        timestamp = int((time() * 1000) + round(random.random() * (120 - 30) + 30))
        rand_times = lambda data, range=100: [[*x[:-1], x[-1] + random.randint(-range, range)] for x in data]
        md, mu = [[173,124,1662999327280],[251,178,1662999328537],[270,179,1662999330025],[275,178,1662999330990]], [[173,124,1662999327413],[251,178,1662999328655],[270,179,1662999330166],[275,178,1662999331088]]
        kd, ku = [[83,1662999327818],[65,1662999327841],[68,1662999327963],[68,1662999329203],[65,1662999329359],[68,1662999329572],[68,1662999330532],[65,1662999330621],[83,1662999330643]], [[83,1662999328019],[68,1662999328243],[68,1662999329449],[65,1662999329584],[83,1662999329605],[68,1662999329772],[68,1662999330823],[65,1662999330867]]
        top_level = {
            "st": time(),
            "sc": {"availWidth": 1920, "availHeight": 1050, "width": 1920, "height": 1080, "colorDepth": 24, "pixelDepth": 24, "top": 0, "left": 0, "availTop": 0, "availLeft": 0, "mozOrientation": "landscape-primary", "onmozorientationchange": None},
            "nv": {"permissions": {}, "pdfViewerEnabled": True, "doNotTrack": "1", "maxTouchPoints": 0, "mediaCapabilities": {}, "oscpu": "Windows NT 10.0; Win64; x64", "vendor": "", "vendorSub": "", "productSub": "20100101", "cookieEnabled": True, "buildID": "20181001000000", "mediaDevices": {}, "serviceWorker": {}, "credentials": {}, "clipboard": {}, "mediaSession": {}, "webdriver": False, "hardwareConcurrency": 12, "geolocation": {}, "appCodeName": "Mozilla", "appName": "Netscape", "appVersion": "5.0 (Windows)", "platform": "Win32", "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0", "product": "Gecko", "language": "en-US", "languages": ["en-US", "en"], "locks": {}, "onLine": True, "storage": {}, "plugins": ["internal-pdf-viewer"]*5},
            "dr": "", "inv": False, "exec": False, "wn": [], "wn-mp": 450.51612903225805, "xy": [], "xy-mp": 0, "mm": [[568, 779, 1662999326734], [517, 755, 1662999326760], [468, 720, 1662999326787], [428, 674, 1662999326813], [400, 627, 1662999326840], [385, 577, 1662999326864]], "mm-mp": 82.32692307692308
        }

        return {
            'st': timestamp, 
            'dct': timestamp, 
            'mm': mm, 
            'md': rand_times(md), 
            'mu': rand_times(mu), 
            'kd': rand_times(kd), 
            'ku': rand_times(ku), 
            'topLevel': top_level}

    def hsw(self, req: str) -> str:
        r = requests.post(f"http://localhost:6969/hsw", json={"req": req})
        return r.text

    def text(self, task: dict):
        s = time()
        q = task["datapoint_text"]["en"]
        response = g4f.ChatCompletion.create(
            model=g4f.models.llama2_70b,
            messages=[{"role": "user", "content": f"srictly respond to the following question with only and only one single word, number, or phrase : {q}"}],
        )
        if response:
            #log.captcha(f"Solved Question -> {q} -> {response}", s, time())
            return task['task_key'], {'text': response}
        return None

    def solve(self) -> str:
        s = time()
        try:
            cap = self.captcha2
            with ThreadPoolExecutor() as e:
                results = list(e.map(self.text, cap['tasklist']))

            answers = {key: value for key, value in results}
            submit = self.session.post(
                f"https://api.hcaptcha.com/checkcaptcha/{self.sitekey}/{cap['key']}",
                json={
                    'answers': answers,
                    'c': dumps(cap['c']),
                    'job_mode': 'text_free_entry',
                    'motionData': json.dumps(self.motion_data()),
                    'n': self.hsw(cap['c']['req']),
                    'serverdomain': self.host,
                    'sitekey': self.sitekey,
                    'v': self.version,
                })

            if 'UUID' in submit.text:
                log.captcha(f"Solved Captcha {submit.json()['generated_pass_UUID'][:70]}", s, time())
                return submit.json()['generated_pass_UUID']

            log.failure(f"Failed To Solve Captcha", s, time(), level="Captcha")
            return "None"
        except Exception as e:
            log.failure(e)