from typing import Any

from hcap_solver.motiondata import *
from hcap_solver.nocap_ai import *
from hcap_solver.logger import *
from tls_client import Session
from datetime import datetime
from hcap_solver.hsw import *
import requests
import base64
import time
import json
import re

js = requests.get("https://js.hcaptcha.com/1/api.js").text
version = re.search(r'v1/(.*?)/', js).group(1)

hswwww = {
  "proof_spec": {
    "difficulty": 2,
    "fingerprint_type": 0,
    "_type": "w",
    "data": "KaGNA2b9ZmazONDC6sEAzWwWTFO2ZKQvxepbBnXLAuIyyyGBo9Zk03ESc0+0DQzo8JgoQjMxYyFibv6AmwSvC5YBuZHdcuj9GRv2TY+xTip7nbp9C4rUgZxL+srwnU2/fgBF4SlVDBSYcLdr+0RtFq0ejbA0JSc+gKpLiewa9A1/Qn5EdfAPkFDw99Q7WgeUCOmvoBtsYsoieBTFSG8TK05UWFiLM+9aTITKtsdkprg1NjVDxVWnOVbLGXfWiinV",
    "_location": "https://newassets.hcaptcha.com/c/e78a38c",
    "timeout_value": 1000
  },
  "rand": [
    0.5787595025663348,
    0.02666437067091465
  ],
  "components": {
    "navigator": {
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.221 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36",
      "language": "en-US",
      "languages": [
        "en-US",
        "en-SE",
        "en-GB",
        "fa",
        "sv-SE"
      ],
      "platform": "Win32",
      "max_touch_points": 0,
      "webdriver": False,
      "notification_query_permission": None,
      "plugins_undefined": False
    },
    "screen": {
      "color_depth": 24,
      "pixel_depth": 24,
      "width": 1920,
      "height": 1080,
      "avail_width": 1920,
      "avail_height": 1040
    },
    "device_pixel_ratio": 1,
    "has_session_storage": True,
    "has_local_storage": True,
    "has_indexed_db": True,
    "web_gl_hash": "-1",
    "canvas_hash": "3290922276056775431",
    "has_touch": False,
    "notification_api_permission": "Granted",
    "chrome": False,
    "to_string_length": 33,
    "err_firefox": None,
    "r_bot_score": 0,
    "r_bot_score_suspicious_keys": [],
    "r_bot_score_2": 0,
    "audio_hash": "-1",
    "extensions": [
      False
    ],
    "parent_win_hash": "18230616880885635051",
    "webrtc_hash": "-1",
    "performance_hash": "4140103483592612201",
    "unique_keys": "__localeData__,DiscordNative,regeneratorRuntime,2,0,__BILLING_STANDALONE__,webpackChunkdiscord_app,platform,__SECRET_EMOTION__,__SENTRY__,hcaptcha,__SENTRY_IPC__,hcaptchaOnLoad,__timingFunction,DiscordErrors,clearImmediate,__OVERLAY__,grecaptcha,DiscordSentry,GLOBAL_ENV,setImmediate,1,IntlPolyfill,createDiscordStream,_ws,popupBridge,__DISCORD_WINDOW_ID",
    "inv_unique_keys": "__wdata,sessionStorage,localStorage,hsw,_sharedLibs",
    "common_keys_hash": 276567530,
    "common_keys_tail": "chrome,caches,cookieStore,ondevicemotion,ondeviceorientation,ondeviceorientationabsolute,launchQueue,documentPictureInPicture,onbeforematch,getScreenDetails,openDatabase,queryLocalFonts,showDirectoryPicker,showOpenFilePicker,showSaveFilePicker,originAgentCluster,credentialless,speechSynthesis,oncontentvisibilityautostatechange,onscrollend,webkitRequestFileSystem,webkitResolveLocalFileSystemURL,Raven",
    "features": {
      "performance_entries": True,
      "web_audio": True,
      "web_rtc": True,
      "canvas_2d": True,
      "fetch": True
    }
  },
  "events": [
    [
      1340556786,
      "true"
    ],
    [
      2258007971,
      "4932383211497360507"
    ],
    [
      4286617223,
      "[1920,1080,1920,1040,24,24,false,0,1,1920,1040,true,true,true,false]"
    ],
    [
      3737842855,
      "1117"
    ],
    [
      2571423665,
      "86.60000002384186"
    ],
    [
      1578658063,
      "[1,2,3,4]"
    ],
    [
      157020890,
      "17002384262467705698"
    ],
    [
      364527618,
      "[19]"
    ],
    [
      3369879498,
      "11038406483972230190"
    ],
    [
      1845702994,
      "15307345790125003576"
    ],
    [
      645217632,
      "[1,1024,1,1,4]"
    ],
    [
      1885396794,
      "[16384,32,16384,2048,2,2048]"
    ],
    [
      1767811539,
      "4226317358175830201"
    ],
    [
      422388259,
      "[[[\"https://newassets.hcaptcha.com/captcha/v1/b1c589a/hcaptcha.js\",0,5]],[[\"*\",84,9]]]"
    ],
    [
      3652805059,
      "[4,120,4]"
    ],
    [
      3444878050,
      "[[277114314453,277114314460,277114314451,357114314456,277114314452,554228628898,57114314443,717114314371391,554228628897,277114314456,1108457257862,277114314450,554228628919,277114314460,277114314451],false]"
    ],
    [
      702607242,
      "1713548957202"
    ],
    [
      3260504850,
      "[[193,[193,193,193,255,193,193,193,255,193,193,193,255,193,193,193,255]],[[11,0,1,105.015625,13,5,105.6171875],[[12,0,-1,113.125,17,4,113],[11,0,0,111,12,4,111],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[12,0,0,109.640625,14,3,110.1953125]]],[0,2,4,5,6,8,9,12,13,15,17,18,19,21,22,23,28,29,30,31,33,34,35,37,39,42,47,48,49,66,67,69,71,72,75,76,77,78,79,81,82],[0,0,0,0,14,3,0]]"
    ],
    [
      1930240485,
      "[26046259200,26046259200,null,null,1098907648,true,true,true,null]"
    ],
    [
      1392191255,
      "[\"TGbeRxCU9GzGJtJSNnbiP2zU\",\"19\",\"15\",\"PCZEALPHTWULX\"]"
    ],
    [
      1192669439,
      "13177607191192652685"
    ],
    [
      1476007714,
      "[[true,\"en-US\",true,\"Microsoft David - English (United States)\",\"Microsoft David - English (United States)\"],[false,\"en-GB\",true,\"Microsoft Hazel - English (United Kingdom)\",\"Microsoft Hazel - English (United Kingdom)\"],[false,\"en-GB\",true,\"Microsoft Susan - English (United Kingdom)\",\"Microsoft Susan - English (United Kingdom)\"]]"
    ],
    [
      980782277,
      "[32767,32767,16384,8,8,8]"
    ],
    [
      355545911,
      "14882824317255702596"
    ],
    [
      206443282,
      "3080.7000000476837"
    ],
    [
      3635805594,
      "[\"5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.221 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36\",\"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.221 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36\",8,4,\"en-US\",[\"en-US\",\"en-SE\",\"en-GB\",\"fa\",\"sv-SE\"],\"Win32\",null,[\"Not_A Brand 8\",\"Chromium 120\"],false,\"Windows\",2,5,true,false,50,false,false,false,\"[object Keyboard]\",false,false]"
    ],
    [
      1196101075,
      "[16,1024,4096,7,12,120,[23,127,127]]"
    ],
    [
      3741287486,
      "[2147483647,2147483647,4294967294]"
    ],
    [
      40999691,
      "[\"NWQJNyUtOyADM=IJ\",\"11\",\"3\",\"CZKRKJCGGTWWW\"]"
    ],
    [
      2264178394,
      "\"Europe/Stockholm\""
    ],
    [
      1578500414,
      "16153807394097295248"
    ],
    [
      3961532981,
      "[-6.172840118408203,-20.710678100585938,120.71067810058594,-20.710678100585938,141.42135620117188,120.71067810058594,-20.710678100585938,141.42135620117188,-20.710678100585938,-20.710678100585938,0,0,300,150,false]"
    ],
    [
      956283155,
      "[\"Windows\",\"10.0.0\",null,\"64\",\"x86\",\"120.0.6099.291\"]"
    ],
    [
      4174694926,
      "[[],35,34,null,false,false,true,37,true,true,true,true,true,[\"Raven\",\"_sharedLibs\",\"hsw\",\"__wdata\"],[[\"getElementsByClassName\",[]],[\"getElementById\",[]],[\"querySelector\",[]],[\"querySelectorAll\",[]]],[],true]"
    ],
    [
      3157273169,
      "56.799999952316284"
    ],
    [
      689964981,
      "57"
    ],
    [
      2946108189,
      "[0,18407,18407]"
    ],
    [
      1438921646,
      "[[\"navigation:newassets.hcaptcha.com\",56.799999952316284,75.10000002384186],[\"script:newassets.hcaptcha.com\",36.35000002384186,229.69999998807907],[\"xmlhttprequest:api.hcaptcha.com\",0,182]]"
    ],
    [
      3298983941,
      "9345374751420407194"
    ],
    [
      2883186606,
      "[[\"lQUlCmYUiQNZNLwITjahga6VgeOc0TCD\",\"13\",\"6\",\"MMSDYPGJKXNDO\"],[\"zRMZwITJPDLSfpKqwITJo80VkVKSCNKmLajmLI0TI1KRfNTRxETkwITJxR3X18fmdJTJwITJ3R3X18fmwITJfp2cMRWDzuumxajmLGCm5bdmwaTmhHjmpajmLEjN1admyuCSVLfmyuCSMDEc\",\"1\",\"64\",\"DAMHMQFBLBGUK\"]]"
    ],
    [
      612273951,
      "[\"Europe/Stockholm\",-60,-60,-3203646808000,\"Central European Standard Time\",\"en-US\"]"
    ],
    [
      202322096,
      "2337666753322697468"
    ],
    [
      106767486,
      "[\"Google Inc. (NVIDIA)\",\"ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 (0x00001F82) Direct3D11 vs_5_0 ps_5_0, D3D11)\"]"
    ],
    [
      3646847539,
      "[2147483647,2147483647,2147483647,2147483647]"
    ],
    [
      1933294324,
      "[16,4095,30,16,16380,120,12,120,[23,127,127]]"
    ],
    [
      3004217393,
      "627"
    ],
    [
      2638668498,
      "[24,24,65536,212988,200704]"
    ],
    [
      2122633777,
      "12073207331849695208"
    ],
    [
      2338842265,
      "3313549113868922289"
    ],
    [
      1833974975,
      "16290568259171983358"
    ],
    [
      3672350690,
      "137.75"
    ],
    [
      2731828028,
      "4631229088072584217"
    ],
    [
      3504714987,
      "[1,4,5,7,9,12,20,21,24,25,29,31]"
    ]
  ],
  "suspicious_events": [],
  "messages": None,
  "stack_data": None,
  "stamp": "1:2:2024-04-19:KaGNA2b9ZmazONDC6sEAzWwWTFO2ZKQvxepbBnXLAuIyyyGBo9Zk03ESc0+0DQzo8JgoQjMxYyFibv6AmwSvC5YBuZHdcuj9GRv2TY+xTip7nbp9C4rUgZxL+srwnU2/fgBF4SlVDBSYcLdr+0RtFq0ejbA0JSc+gKpLiewa9A1/Qn5EdfAPkFDw99Q7WgeUCOmvoBtsYsoieBTFSG8TK05UWFiLM+9aTITKtsdkprg1NjVDxVWnOVbLGXfWiinV::ph4uKgxE:5",
  "href": "https://canary.discord.com/register?redirect_to=%2Fchannels%2F%40me%2F1230637003364630639",
  "ardata": None,
  "errs": {
    "list": []
  },
  "perf": [
    [
      1,
      25
    ],
    [
      2,
      98
    ],
    [
      3,
      0
    ]
  ]
}

class Hcaptcha:
    def __init__(self, site_key: str, host: str, proxy: str = None, rq_data: str = None) -> None:
        #self.hsw_key = database_fps.randomkey()
        self.hsw_key = hswwww
        self.job = None
        self.key = None
        self.c2 = None
        self.session = Session(client_identifier='chrome_118', random_tls_extension_order=True)
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
        self.session.proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        self.site_key = site_key
        self.host = host.split("//")[-1].split("/")[0]
        self.rq_data = rq_data
        self.motion = MotionData(self.session.headers["user-agent"], f"https://{self.host}")
        self.motion_data = self.motion.get_captcha()

    def hsw(self, req: str) -> str:
        s = req.split(".")[1].encode()
        s += b'=' * (-len(s) % 4)
        data = json.loads(base64.b64decode(s, validate=False).decode())
        return pull(self.hsw_key, data['s'], data['d'], self.host)

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
        captcha_type = captcha["request_type"]
        self.c2 = captcha['c']
        self.key = captcha['key']
        log.captcha(f"Solving Captcha -> {captcha_type}...")
        self.job = captcha_type
        return AI_Solver(captcha_type, captcha, self.site_key, self.host).solve()

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
