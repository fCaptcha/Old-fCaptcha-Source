from concurrent.futures import ThreadPoolExecutor
from hcap_solver.motiondata import *
from hcap_solver.logger import log
from tls_client import Session
from datetime import datetime
from json import dumps
from re import findall
from time import time
import requests
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
            "accept-language": 'sv-SE;q=0.9'
        }

        self.proxy = proxy
        self.session.proxies = {'http': f'http://{self.proxy}', 'https': f'http://{self.proxy}'} if proxy else None
        self.api_js = self.session.get('https://hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaOnLoad').text
        self.version = findall(r'v1\/([A-Za-z0-9]+)\/static', self.api_js)[1]
        self.sitekey = sitekey
        self.host = host
        self.motion = MotionData(self.session.headers["user-agent"], f"https://{host}")
        self.motiondata = self.motion.get_captcha()
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
        log.info(f"Got Site Config / ({siteconfig.status_code})", s, time())
        return siteconfig.json()

    def get_captcha1(self) -> dict:
        s = time()
        getcaptcha = self.session.post(f"https://hcaptcha.com/getcaptcha/{self.sitekey}", data={
            'v': self.version,
            'sitekey': self.sitekey,
            'host': self.host,
            'hl': 'sv',
            'motionData': dumps(self.motiondata),
            'pdc':  {"s": round(datetime.now().timestamp() * 1000), "n":0, "p":0, "gcs":10},
            'n': self.hsw(self.siteconfig['c']['req']),
            'c': dumps(self.siteconfig['c']),
            'pst': False
        })
        log.info(f"Got Captcha Number 1 / ({getcaptcha.status_code})", s, time())
        return getcaptcha.json()
    
    def get_captcha2(self) -> dict:
        s = time()
        getcaptcha2 = self.session.post(f"https://hcaptcha.com/getcaptcha/{self.sitekey}", data={
            'v': self.version,
            'sitekey': self.sitekey,
            'host': self.host,
            'hl': 'sv',
            'a11y_tfe': 'true',
            'action': 'challenge-refresh',
            'old_ekey'  : self.captcha1['key'],
            'extraData': self.captcha1,
            'motionData': dumps(self.motiondata),
            'pdc':  {"s": round(datetime.now().timestamp() * 1000), "n":0, "p":0, "gcs":10},
            'n': self.hsw(self.captcha1['c']['req']),
            'c': dumps(self.captcha1['c']),
            'pst': False
        })
        log.info(f"Got Captcha Number 2 / ({getcaptcha2.status_code})", s, time())
        return getcaptcha2.json()

    def hsw(self, req: str) -> str:
        r = requests.post(f"http://localhost:6969/hsw", json={"req": req})
        return r.text

    def text(self, task: dict):
        s = time()
        q = task["datapoint_text"]["sv"]
        response = g4f.ChatCompletion.create(
            model=g4f.models.llama2_70b,
            messages=[{"role": "user", "content": f"srictly respond to the following question with only and only one single word, number, or phrase :  Question: {q} Response options: ja, nej"}],
        )
        if response:
            response = response.replace('.', '')
            log.captcha(f"Solved Question -> {q} -> {response}", s, time())
            with open('scraped.txt', 'a', encoding='utf-8') as f:
                f.write(f"{q}>>{response}\n")
            return task['task_key'], {'text': response}
        return None
    
    def solve(self) -> str:
        s = time()
        try:
            cap = self.captcha2
            with ThreadPoolExecutor() as e:
                results = list(e.map(self.text, cap['tasklist']))

            answers = {key: value for key, value in results}
            motiondata = self.motion.check_captcha(answers, 'text_free_entry')
            #submit = self.session.post(
            #    f"https://api.hcaptcha.com/checkcaptcha/{self.sitekey}/{cap['key']}",
            #    json={
            #        'answers': answers,
            #        'c': dumps(cap['c']),
            #        'job_mode': 'text_free_entry',
            #        'motionData': json.dumps(self.motiondata),
            #        'n': self.hsw(cap['c']['req']),
            #        'serverdomain': self.host,
            #        'sitekey': self.sitekey,
            #        'v': self.version,
            #    })
            #
            #if 'UUID' in submit.text:
            #    log.captcha(f"Solved hCaptcha {submit.json()['generated_pass_UUID'][:70]}", s, time())
            #    return submit.json()['generated_pass_UUID']
            #
            #log.failure(f"Failed To Solve hCaptcha", s, time(), level="hCaptcha")
            return "None"
        except Exception as e:
            log.failure(e)