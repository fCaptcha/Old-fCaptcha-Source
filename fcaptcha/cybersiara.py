# ill fix it later

from tasks import base_task
from javascript import require, globalThis
import random
import re
import requests

class Cybersiara(base_task.BaseTask):

    def encode(self, data):
        return require("../../data/cybersiara.js").encodedData(data)

    def __init__(self) -> None:
        super().__init__("cybersiara")
        self.session = requests.Session()

    def get_fingerprint(self):

        navigator_info = {
            "mimeTypes": {"length": random.randint(2, 99)},
            "appCodeName": "Mozilla",
            "appName": "Netscape",
            "appVersion": self.app_version,
            "cookieEnabled": True,
            "deviceMemory": 8,
            "language": "pl-PL",
            "languages": ['pl-PL', 'de-PL', 'de', 'pl', 'en-US', 'en'],
            "onLine": True,
            "platform": "Win32",
            "product": "Gecko",
            "productSub": "20030107",
            "userAgent": self.user_agent,
            "vendor": "Google Inc.",
            "plugins": {"length": random.randint(5, 92)}
        }

        screen_info = {
            "availWidth": 1920,
            "availHeight": 1032,
            "width": 1920,
            "height": 1080,
            "colorDepth": 24,
            "pixelDepth": random.randint(21, 98),
            "isExtended": False,
            "orientation": {
                "angle": 0,
                "type": "landscape-primary"
            }
        }

        return self.encode((
            str(navigator_info["mimeTypes"]["length"])
            + re.sub(r"\D+", "", navigator_info["userAgent"])
            + str(navigator_info["plugins"]["length"])
            + str(screen_info["height"] or "")
            + str(screen_info["width"] or "")
            + str(screen_info["pixelDepth"] or "")
        ))

    def get_captcha(self):
        self.visitor_id = random.randint(10**(6-1), 10**6 - 1)
        self.request_id = random.randint(10**(7-1), 10**7- 1)

        payload = {
            "MasterUrlId" : self.sitekey,
            "DeviceName" : self.user_agent,
            "RequestUrl" : self.url,
            "BrowserIdentity": self.fingerprint,
            "PluginNo" : 0,
            "VisiterId": self.visitor_id,
            "LanguageId" : 1,
            "RequestID" : self.request_id,
            "LangChange" : 0,
            "ClickSecond" : random.randint(22, 46),
            "Iscookie" : 1,
            "DeviceHeight" : 1080,
            "DeviceWidth" : 1920
        }


        r = self.session.post("https://embed.mycybersiara.com/api/CyberSiara/GetCyberSiara", headers=self.headers, data=payload)
        return r.json()

    def verify_captcha(self, captcha):
        if captcha["HttpStatusCode"] == 400: return False
        payload = {
            "RequestID" : self.request_id,
            "FPID" : self.fingerprint,
            "VisiterId" : self.visitor_id
        }
        
        r = self.session.post("https://embed.mycybersiara.com/api/v2/verification/fp", headers=self.headers, data=payload)

        return r.json()

    def solve(self, task):
        self.url = task["website"]
        self.sitekey = task["sitekey"]
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        self.app_version = self.user_agent.split("/")
        self.app_version.pop(0)
        self.app_version = "/".join(self.app_version)
        self.fingerprint = self.get_fingerprint()
        self.headers = {
             "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.url,
            "Referer": self.url,
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": self.user_agent
        }

        captcha = self.get_captcha()
        captcha = self.verify_captcha(captcha)
        if not captcha:
            return "failed"
        payload = {
            'MasterUrl': self.sitekey,
            'DeviceName': self.user_agent,
            'BrowserIdentity': self.fingerprint,
            'Protocol': 'https:',
            'VisiterId': self.visitor_id,
            'second': random.randint(2, 3),
            'RequestID': self.request_id
        }

        r = self.session.post("https://embed.mycybersiara.com/api/v2/SubmitCaptcha/VerifiedSubmit", headers=self.headers, data=payload)
        if "data" in r.json() and isinstance(r.json()["data"], str):
            return r.json()["data"]     
        return "failed"