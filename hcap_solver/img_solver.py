from typing import Any

from hcap_solver.motiondata import *
from hcap_solver.nocap_ai import *
from hcap_solver.logger import *
from tls_client import Session
from datetime import datetime
from hcap_solver.hsw import *
import requests
import random
import base64
import httpx
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
        "data": "iLFYiWil+qbfMw4e/8+ZRNKxvtLukIgX17Z6xI6O939ekb/khYEbiEFhP0Zc78t3ooYrMlaVzYqiOO1el67K5b4ezw74Lyvj8+hAyFpALJwdplf6Xz5etpQPba4cKRKk7SCneuGELFFgDHkH6D1Jpna7EGGdS14X6LPmXHlRgU/rrJ5amoWQMEC56WE/lSb+BZYdLaLaxplRENzhMDRb72a+KS7EUrD2oC58/AlbJWm0VKkrypQ/oU0fH5A6PpIR",
        "_location": "https://newassets.hcaptcha.com/c/e78a38c",
        "timeout_value": 1000
    },
    "rand": [
        0.0017065975023073943,
        0.5795185193419456
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
            1476007714,
            "[[true,\"en-US\",true,\"Microsoft David - English (United States)\",\"Microsoft David - English (United States)\"],[false,\"en-GB\",true,\"Microsoft Hazel - English (United Kingdom)\",\"Microsoft Hazel - English (United Kingdom)\"],[false,\"en-GB\",true,\"Microsoft Susan - English (United Kingdom)\",\"Microsoft Susan - English (United Kingdom)\"]]"
        ],
        [
            2264178394,
            "\"Europe/Stockholm\""
        ],
        [
            1438921646,
            "[[\"navigation:newassets.hcaptcha.com\",11.600000023841858,16],[\"script:newassets.hcaptcha.com\",31.80000001192093,55.799999952316284],[\"xmlhttprequest:api.hcaptcha.com\",0,58.90000009536743]]"
        ],
        [
            1192669439,
            "13177607191192652685"
        ],
        [
            3672350690,
            "38.30000001192093"
        ],
        [
            364527618,
            "[22]"
        ],
        [
            40999691,
            "[\"MJn2MDoyaDo=Itn4\",\"e\",\"5\",\"UTGNSJBCAEOHG\"]"
        ],
        [
            4286617223,
            "[1920,1080,1920,1040,24,24,false,0,1,1920,1040,true,true,true,false]"
        ],
        [
            202322096,
            "2337666753322697468"
        ],
        [
            1340556786,
            "true"
        ],
        [
            2731828028,
            "4631229088072584217"
        ],
        [
            1933294324,
            "[16,4095,30,16,16380,120,12,120,[23,127,127]]"
        ],
        [
            1392191255,
            "[\"1gA2RWYovmzY52AoLgegJtJM\",\"13\",\"d\",\"GVLUUQVIDTLAZ\"]"
        ],
        [
            2946108189,
            "[0,18407,18407]"
        ],
        [
            2258007971,
            "4932383211497360507"
        ],
        [
            422388259,
            "[[[\"https://newassets.hcaptcha.com/captcha/v1/b1c589a/hcaptcha.js\",0,5]],[[\"*\",84,9]]]"
        ],
        [
            2638668498,
            "[24,24,65536,212988,200704]"
        ],
        [
            2338842265,
            "3313549113868922289"
        ],
        [
            612273951,
            "[\"Europe/Stockholm\",-60,-60,-3203646808000,\"Central European Standard Time\",\"en-US\"]"
        ],
        [
            3635805594,
            "[\"5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.221 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36\",\"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.221 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36\",8,4,\"en-US\",[\"en-US\",\"en-SE\",\"en-GB\",\"fa\",\"sv-SE\"],\"Win32\",null,[\"Not_A Brand 8\",\"Chromium 120\"],false,\"Windows\",2,5,true,false,50,false,false,false,\"[object Keyboard]\",false,false]"
        ],
        [
            1578500414,
            "16153807394097295248"
        ],
        [
            3741287486,
            "[2147483647,2147483647,4294967294]"
        ],
        [
            3157273169,
            "11.600000023841858"
        ],
        [
            106767486,
            "[\"Google Inc. (NVIDIA)\",\"ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 (0x00001F82) Direct3D11 vs_5_0 ps_5_0, D3D11)\"]"
        ],
        [
            980782277,
            "[32767,32767,16384,8,8,8]"
        ],
        [
            1930240485,
            "[25836638208,25836638208,null,null,1098907648,true,true,true,null]"
        ],
        [
            3004217393,
            "627"
        ],
        [
            157020890,
            "17002384262467705698"
        ],
        [
            702607242,
            "1713732206359.6"
        ],
        [
            3369879498,
            "11038406483972230190"
        ],
        [
            3652805059,
            "[4,120,4]"
        ],
        [
            1845702994,
            "15307345790125003576"
        ],
        [
            1196101075,
            "[16,1024,4096,7,12,120,[23,127,127]]"
        ],
        [
            689964981,
            "57"
        ],
        [
            956283155,
            "[\"Windows\",\"10.0.0\",null,\"64\",\"x86\",\"120.0.6099.291\"]"
        ],
        [
            3504714987,
            "[1,4,5,7,9,12,20,21,24,25,29,31]"
        ],
        [
            645217632,
            "[1,1024,1,1,4]"
        ],
        [
            1578658063,
            "[1,2,3,4]"
        ],
        [
            3298983941,
            "9345374751420407194"
        ],
        [
            3961532981,
            "[-6.172840118408203,-20.710678100585938,120.71067810058594,-20.710678100585938,141.42135620117188,120.71067810058594,-20.710678100585938,141.42135620117188,-20.710678100585938,-20.710678100585938,0,0,300,150,false]"
        ],
        [
            4174694926,
            "[[],35,34,null,false,false,true,37,true,true,true,true,true,[\"Raven\",\"_sharedLibs\",\"hsw\",\"__wdata\"],[[\"getElementsByClassName\",[]],[\"getElementById\",[]],[\"querySelector\",[]],[\"querySelectorAll\",[]]],[],true]"
        ],
        [
            3444878050,
            "[[277114314453,277114314460,277114314451,357114314456,277114314452,554228628898,57114314443,717114314371391,554228628897,277114314456,1108457257862,277114314450,554228628919,277114314460,277114314451],false]"
        ],
        [
            1833974975,
            "16290568259171983358"
        ],
        [
            3260504850,
            "[[149,[149,149,149,255,149,149,149,255,149,149,149,255,149,149,149,255]],[[11,0,1,105.015625,13,5,105.6171875],[[12,0,-1,113.125,17,4,113],[11,0,0,111,12,4,111],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[12,0,0,109.640625,14,3,110.1953125]]],[0,2,4,5,6,8,9,12,13,15,17,18,19,21,22,23,28,29,30,31,33,34,35,37,39,42,47,48,49,66,67,69,71,72,75,76,77,78,79,81,82],[0,0,0,0,14,3,0]]"
        ],
        [
            2571423665,
            "72.80000007152557"
        ],
        [
            3737842855,
            "1117"
        ],
        [
            3646847539,
            "[2147483647,2147483647,2147483647,2147483647]"
        ],
        [
            2883186606,
            "[[\"wiTJF1WblP2yOwEvhJ0RZlCMYuYRSFmL\",\"18\",\"14\",\"YISHOSQOUVGPK\"],[\"BZVQtNkMlajMlMlrZr0VwNjVXEtKWItJoT2x18fMdJtJWItJuT2x18fMWItJwfmA3VHbzyVMXajMlGcMWBdMWatMyhjMpajMlEjN1adMYUSwMBfMYUSw3h1ZqV3DWItJg5UQwf0UWItJoykt\",\"12\",\"7c\",\"TDYYAXFWYWRCG\"]]"
        ],
        [
            206443282,
            "1002.7000000476837"
        ],
        [
            1767811539,
            "4226317358175830201"
        ],
        [
            1885396794,
            "[16384,32,16384,2048,2,2048]"
        ],
        [
            355545911,
            "14882824317255702596"
        ],
        [
            2122633777,
            "12073207331849695208"
        ]
    ],
    "suspicious_events": [],
    "messages": None,
    "stack_data": None,
    "stamp": "1:2:2024-04-21:iLFYiWil+qbfMw4e/8+ZRNKxvtLukIgX17Z6xI6O939ekb/khYEbiEFhP0Zc78t3ooYrMlaVzYqiOO1el67K5b4ezw74Lyvj8+hAyFpALJwdplf6Xz5etpQPba4cKRKk7SCneuGELFFgDHkH6D1Jpna7EGGdS14X6LPmXHlRgU/rrJ5amoWQMEC56WE/lSb+BZYdLaLaxplRENzhMDRb72a+KS7EUrD2oC58/AlbJWm0VKkrypQ/oU0fH5A6PpIR::JESuTQot:11",
    "href": "https://canary.discord.com/register",
    "ardata": None,
    "errs": {
        "list": []
    },
    "perf": [
        [
            1,
            12
        ],
        [
            2,
            79
        ],
        [
            3,
            0
        ]
    ]
}

class Hcaptcha:
    def __init__(self, site_key: str, host: str, proxy: str, rq_data: str = None) -> None:
        #self.hsw_key = database_fps.randomkey()
        self.hsw_key = hswwww
        self.job = None
        self.key = None
        self.c2 = None
        self.session = Session(client_identifier='chrome_120', random_tls_extension_order=True)
        self.before = time.time()
        self.session.headers = {
            'accept': '*/*',
            'accept-language': 'en-AU,en;q=0.9,fa;q=0.8,en-US;q=0.7,sv;q=0.6',
            'content-type': 'application/json;charset=UTF-8',
            'dnt': "1",
            'origin': 'https://newassets.hcaptcha.com',
            'referer': 'https://newassets.hcaptcha.com/',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9041 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36',
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
        return HSW().pull(self.hsw_key, data['s'], data['d'], self.host, self.session.headers["user-agent"])

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
        motion = self.motion.check_captcha(answers)
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
            'pdc': {"s": round(datetime.now().timestamp() * 1000), "n": 0, "p": random.randint(0, 2), "gcs": random.randint(30, 658)},
            'pem': {"csc":random.uniform(100, 2500)},
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
