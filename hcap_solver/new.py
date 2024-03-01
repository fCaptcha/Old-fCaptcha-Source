import datetime
import requests
import json
import pyppeteer
import base64
import asyncio
import random
import string
import os
import platform
import time
from hcap_solver.motiondata import MotionData
from bs4 import BeautifulSoup
from json import dumps
import re
from tls_client import Session
from re import findall

class Solver:
    def __init__(self, sitekey: str, host: str, proxy: str = None):
        self.sitekey = sitekey
        self.href = host
        self.host = host.split("//")[-1].split("/")[0]
        self.session = Session(client_identifier='chrome_118', random_tls_extension_order=True)
        self.proxy = proxy
        self.session.proxies = {'http': f'http://{self.proxy}', 'https': f'http://{self.proxy}'} if proxy else None
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.141 Whale/3.15.136.29 Safari/537.36"
        self.motion = MotionData(self.user_agent, self.host)
        self.motiondata = self.motion.get_captcha()
        self.nocaptchaai = {"apikey": "bobfa77-63ccda61-339a-c87a-0104-eb9e931f60f6", "solver": "https://pro.nocaptchaai.com/solve"}
        self.api_js = self.session.get('https://hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaOnLoad').text
        self.version = findall(r'v1\/([A-Za-z0-9]+)\/static', self.api_js)[1]
    
    def ardata(self):
        r = self.session.get("https://newassets.hcaptcha.com/captcha/v1/fadb9c6/static/hcaptcha.html?_v=n2igxf14d2i")
        soup = BeautifulSoup(r.text, 'html.parser')
        tag = soup.find('script', {'src': re.compile(r'hcaptcha\.js#i=')})
        ardata = tag['src'].split('#i=')[1]
        return ardata
    
    def hsw(self, req: str) -> str:
        ardata = self.ardata()
        r = requests.get(f"http://70.29.98.18:23280/proof/hsw?jwt={req}&auth=4043eb1&ardata={ardata}").json()
        return r["proof"]

    def get_captcha(self):
        siteconfig = self.session.post(f"https://hcaptcha.com/checksiteconfig", params={
            'v': self.version,
            'sitekey': self.sitekey,
            'host': self.host,
            'sc': '1', 
            'swa': '1', 
            'spst': '1'
        }).json()

        print(siteconfig)
        payload = {
            "v": self.version,
            "sitekey": self.sitekey,
            "host": self.host,
            "hl": "en",
            "motionData": dumps(self.motiondata),
            "n": self.hsw(siteconfig["c"]["req"]),
            "c": dumps(siteconfig['c'])
        }
        captcha = self.session.post(f"https://api.hcaptcha.com/getcaptcha/{self.sitekey}", 
            headers={
                "accept": "application/json",
                "accept-language": "en-US,en;q=0.9",
                "content-type": "application/x-www-form-urlencoded",
                "origin": "https://newassets.hcaptcha.com",
                "referer": "https://newassets.hcaptcha.com/",
                "user-agent": self.user_agent,
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site"
            }, data=payload).json()
        print(captcha)
        return captcha

    def solve(self):
        time_start = time.time()
        solve_time = 8
        headers = {
            "Authority": "hcaptcha.com",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://newassets.hcaptcha.com/",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "User-Agent": self.user_agent,
        }

        captcha = self.get_captcha()
        k, t = captcha["key"], captcha["tasklist"]
        i, t_, z = {}, {}, 0
        request_type = captcha["request_type"]
        if request_type == "image_label_binary":
            captcha_type = "grid"
            choices = []
        elif request_type == "image_label_area_select":
            captcha_type = "bbox"
            choices = []
            print("bbox captcha detected")

        for u in t:
            img_base64 = base64.b64encode(requests.get(str(u["datapoint_uri"]), headers=headers).content)
            img_base64_decoded = img_base64.decode('utf-8') 
            url, task_key =img_base64_decoded , str(u["task_key"])
            i[z], t_[url] = url, task_key
            z += 1
        g = captcha["requester_question"]["en"]
        print(f"Target is ==> {g}")
        task_data = {
            "images": i,
            "target": g,
            "method": "hcaptcha_base64",
            "site": self.href,
            "sitekey": self.sitekey
        }
        if captcha_type == "bbox":
            task_data['choices'] = []
            task_data['type'] = 'bbox'
        else:
            task_data['choices'] = []

        with open("task_data.json", "w") as f:
            json.dump(task_data, f)
        task_result = requests.post(self.nocaptchaai["solver"], json=task_data, headers={
            "Content-type": "application/json",
            "apikey": self.nocaptchaai["apikey"]
        }).json()
        print(task_result)
        status = 'new'
        if task_result['status'] == 'new':
            url, p2, z, answer = task_result["url"], None, 0, {}
            time.sleep(2.5)
            while True:
                p2 = requests.get(url).text
                if "solved" in p2:
                    p2 = json.loads(p2)
                    status = 'solved'
                    break
                elif not "queue" in p2:
                    return False
                if z >= 5:
                    print(p2)
                    return False
                z += 1
            for d in i:
                if captcha_type == "grid":
                    if str(d) in p2["solution"]:
                        answer[t_[i[d]]] = "true"
                    else:
                        answer[t_[i[d]]] = "false"
                elif captcha_type == "bbox":
                    if len(i) != len(p2["answers"]):
                        return False
                    for d in i:
                        item = [{"entity_name": 0,"entity_type": "label","entity_coords": p2["answers"][d]}]
                        answer[t_[i[d]]] = item
        elif task_result['status'] == 'solved':
            answer = {}
            status = 'solved'
            if captcha_type == "grid":
                for d in i:
                    if d in task_result["solution"]:
                        answer[t_[i[d]]] = "true"
                    else:
                        answer[t_[i[d]]] = "false"
            elif captcha_type == "bbox":
                if len(i) != len(task_result["answers"]):
                    return False
                for d in i:
                    item = [{"entity_name": 0,"entity_type": "label","entity_coords": task_result["answers"][d]}]
                    answer[t_[i[d]]] = item

        if (time_start + solve_time) > time.time():
            time.sleep(time_start + solve_time - time.time())
        if status == 'solved':
            h = self.hsw(captcha["c"]["req"])
            motiondata = self.motion.check_captcha(answer, 'text_free_entry')
            s = {
                "v": self.version,
                "job_mode": "image_label_binary",
                "answers": answer,
                "serverdomain": self.host,
                "sitekey": self.sitekey,
                "motionData": motiondata,
                "n": h,
                "c": "{\"type\":\"" + captcha["c"]["type"] + "\",\"req\":\"" + captcha["c"]["req"] + "\"}"
            }
            checkcaptcha = self.session.post(f"https://hcaptcha.com/checkcaptcha/{self.sitekey}/{k}", json=s, headers={
                "Authority": "hcaptcha.com",
                "content-type": "application/json",
                "accept-language": "en-US,en;q=0.9",
                "content-length": str(len(s)),
                "accept": "*/*",
                "origin": "https://newassets.hcaptcha.com",
                "referer": "https://newassets.hcaptcha.com/",
                "user-agent": self.user_agent,
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site"
            })
            if "generated_pass_UUID" in checkcaptcha.json():
                return checkcaptcha.json()["generated_pass_UUID"]
            else:
                return False
        else:
            return "Something wrong"

def main():
    solver = Solver("a5f74b19-9e45-40e0-b45d-47ff91b7a6c2", "https://accounts.hcaptcha.com/demo", "vmOP5Ks2DeIn:ijWtcsMd9YWP@att.proxies.fo:5000")
    result = solver.solve()
    if result == False:
        print("Failed to get token")
    else:
        print("Got token")
        print(result)

if __name__ == '__main__':
    main()
