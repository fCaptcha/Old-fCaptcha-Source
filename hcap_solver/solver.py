from concurrent.futures import ThreadPoolExecutor
from hcap_solver.motiondata import *
from hcap_solver.logger import log
from redis.client import Redis
from tls_client import Session
from datetime import datetime
from bs4 import BeautifulSoup
from json import dumps
from re import findall
from time import time
import requests
import hashlib
import json
import g4f
import re

database = Redis("147.189.168.82", 6379, 0, "4wHQaoenQxqk4E@FC8")

class Hcaptcha:
    def __init__(self, sitekey: str, host: str, proxy: str = None) -> None:
        self.answers = {}
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
            "accept-language": 'nl-NL;q=0.9'
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
        self.captcha = self.get_captcha()

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
    
    def get_captcha(self) -> dict:
        s = time()
        getcaptcha = self.session.post(f"https://hcaptcha.com/getcaptcha/{self.sitekey}", data={
            'v': self.version,
            'sitekey': self.sitekey,
            'host': self.host,
            'hl': 'nl',
            'a11y_tfe': 'true',
            'action': 'challenge-refresh',
            'motionData': dumps(self.motiondata),
            'pdc':  {"s": round(datetime.now().timestamp() * 1000), "n":0, "p":0, "gcs":10},
            'n': self.hsw(self.siteconfig['c']['req']),
            'c': dumps(self.siteconfig['c']),
            'pst': False
        })
        #yyylog.info(f"Got Captcha / ({getcaptcha2.status_code})", s, time())
        return getcaptcha.json()

    def ardata(self):
        r = self.session.get("https://newassets.hcaptcha.com/captcha/v1/fadb9c6/static/hcaptcha.html?_v=n2igxf14d2i")
        soup = BeautifulSoup(r.text, 'html.parser')
        tag = soup.find('script', {'src': re.compile(r'hcaptcha\.js#i=')})
        ardata = tag['src'].split('#i=')[1]
        return ardata
    
    def hsw(self, req: str) -> str:
        ardata = self.ardata()
        r = requests.get(f"http://70.26.113.238:23280/proof/hsw?jwt={req}&ardata={ardata}").json()
        return r["proof"]

    def text(self, task: dict):
        s = time()
        q = task["datapoint_text"]["nl"]
        hashed_q = hashlib.sha1(q.encode()).hexdigest()
        if response := database.get(hashed_q):
            #log.captcha(f"Got question from database -> {q} -> {response.decode()}", s, time())
            return task['task_key'], {'text': response.decode()}
        
        response = g4f.ChatCompletion.create(
            model=g4f.models.llama2_70b,
            messages=[{"role": "user", "content": f"srictly respond to the following question with only and only one single word, number, or phrase :  Question: {q} Response options: ja, nee"}],
        )
        if response:
            response = response.replace('.', '')
            #log.captcha(f"Solved Question -> {q} -> {response}", s, time())
            self.answers[hashed_q] = response
            return task['task_key'], {'text': response}
        return None
    
    def solve(self) -> str:
        s = time()
        try:
            cap = self.captcha
            with ThreadPoolExecutor() as e:
                results = list(e.map(self.text, cap['tasklist']))

            answers = {key: value for key, value in results}
            motiondata = self.motion.check_captcha(answers, 'text_free_entry')
            submit = self.session.post(
                f"https://api.hcaptcha.com/checkcaptcha/{self.sitekey}/{cap['key']}",
                json={
                    'answers': answers,
                    'c': dumps(cap['c']),
                    'job_mode': 'text_free_entry',
                    'motionData': dumps(motiondata),
                    'n': self.hsw(cap['c']['req']),
                    'serverdomain': self.host,
                    'sitekey': self.sitekey,
                    'v': self.version,
                })
            
            if 'UUID' in submit.text:
                log.captcha(f"Solved hCaptcha {submit.json()['generated_pass_UUID'][:70]}", s, time())
                for q, r in self.answers.items():
                    database.set(q, r)
                # for x in answers:
                #     database.set(x, answers[x])
                return submit.json()['generated_pass_UUID']
            
            log.failure(f"Failed To Solve hCaptcha", s, time(), level="hCaptcha")
            return "None"
        except Exception as e:
            pass