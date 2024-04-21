from typing import Any

from hcap_solver.motiondata import *
from hcap_solver.nocap_ai import *
from hcap_solver.logger import *
from tls_client import Session
from datetime import datetime
from hcap_solver.hsw import *
import requests
import base64
import httpx
import time
import json
import re

js = requests.get("https://js.hcaptcha.com/1/api.js").text
version = re.search(r'v1/(.*?)/', js).group(1)

hswwww = {
  "proof_spec": {
    "difficulty": 16,
    "fingerprint_type": 0,
    "_type": "w",
    "data": "0B/+p0Vj9+Do93iyd/rbJSB4oDGXF4WdYHrs926ZOjTPsYpWXkMdRZz8qpA6j7PRZ6LsnncQzeSxjhGBWm026B644uani4GYX7E1SP7zliA2VFEqT5uzNq74rxV0xMbKdePjjU+/fTCFgLOyNbkk8sAROEng3CcZQs1q6scTl/bgI0YBcGp5GFdLMSgN17FnysNhCTHKhqJDHYioSouQ1v6AXMRSsk/UGHuHpVG+xrpNoP0B9Q==t8fuSBSiq2eB2ZEn",
    "_location": "https://newassets.hcaptcha.com/c/e78a38c",
    "timeout_value": 1000
  },
  "rand": [
    0.955140763884003,
    0.7979516244959086
  ],
  "components": {
    "navigator": {
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
      "language": "en-AU",
      "languages": [
        "en-AU",
        "fa",
        "en-US",
        "en",
        "sv"
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
    "notification_api_permission": "Denied",
    "chrome": True,
    "to_string_length": 33,
    "err_firefox": None,
    "r_bot_score": 0,
    "r_bot_score_suspicious_keys": [],
    "r_bot_score_2": 0,
    "audio_hash": "-1",
    "extensions": [
      False
    ],
    "parent_win_hash": "5683397452819783432",
    "webrtc_hash": "-1",
    "performance_hash": "5480068218625584110",
    "unique_keys": "1,onSuccess,hcaptcha,0,CMExtension,onExpire,grecaptcha",
    "inv_unique_keys": "hsw,__wdata,exportsInstance,image_label_binary,image_label_area_select,_sharedLibs",
    "common_keys_hash": 2005040245,
    "common_keys_tail": "stop,structuredClone,webkitCancelAnimationFrame,webkitRequestAnimationFrame,chrome,fence,caches,cookieStore,ondevicemotion,ondeviceorientation,ondeviceorientationabsolute,launchQueue,documentPictureInPicture,getScreenDetails,queryLocalFonts,showDirectoryPicker,showOpenFilePicker,showSaveFilePicker,originAgentCluster,onpagereveal,credentialless,speechSynthesis,onscrollend,webkitRequestFileSystem,webkitResolveLocalFileSystemURL,define,ethereum,ClownfishModuleInit,CF_Settings,createScriptProcessorHooked,StackTrace,cetus,Raven",
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
      3741287486,
      "[2147483647,2147483647,4294967294]"
    ],
    [
      1578500414,
      "16153807394097295248"
    ],
    [
      3635805594,
      "[\"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\",\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\",8,4,\"en-AU\",[\"en-AU\",\"fa\",\"en-US\",\"en\",\"sv\"],\"Win32\",null,[\"Google Chrome 123\",\"Not:A-Brand 8\",\"Chromium 123\"],false,\"Windows\",2,5,true,false,50,false,false,true,\"[object Keyboard]\",false,false]"
    ],
    [
      422388259,
      "[[[\"https://newassets.hcaptcha.com/captcha/v1/b1c589a/hcaptcha.js\",0,5]],[[\"*\",84,9],[null,92,1],[null,92,1],[null,92,1],[null,92,1],[null,92,1],[null,92,1],[null,92,1],[null,92,1],[null,92,1]]]"
    ],
    [
      1192669439,
      "13177607191192652685"
    ],
    [
      1438921646,
      "[[\"css:imgs3.hcaptcha.com\",0,34.299999952316284],[\"img:imgs3.hcaptcha.com\",0,122.64999997615814],[\"navigation:newassets.hcaptcha.com\",101,137.80000007152557],[\"script:newassets.hcaptcha.com\",4,16.849999964237213],[\"xmlhttprequest:api.hcaptcha.com\",0,305.10000002384186],[\"xmlhttprequest:api2.hcaptcha.com\",0,205.70000004768372]]"
    ],
    [
      1116177314,
      "855.7999999523163"
    ],
    [
      40999691,
      "[\"5ETO4UdOyKTO2idN\",\"1a\",\"8\",\"XHAVSCJDILKDL\"]"
    ],
    [
      1833974975,
      "11162887117610606218"
    ],
    [
      1933294324,
      "[16,4095,30,16,16380,120,12,120,[23,127,127]]"
    ],
    [
      2638668498,
      "[24,24,65536,212988,200704]"
    ],
    [
      3737842855,
      "1134"
    ],
    [
      689964981,
      "57"
    ],
    [
      157020890,
      "12027682292028963860"
    ],
    [
      2338842265,
      "3313549113868922289"
    ],
    [
      202322096,
      "2337666753322697468"
    ],
    [
      980782277,
      "[32767,32767,16384,8,8,8]"
    ],
    [
      4174694926,
      "[[\"loadTimes\",\"csi\",\"app\"],35,34,null,false,false,true,37,true,true,true,true,true,[\"define\",\"ethereum\",\"ClownfishModuleInit\",\"CF_Settings\",\"createScriptProcessorHooked\",\"StackTrace\",\"cetus\",\"Raven\",\"_sharedLibs\",\"hsw\",\"exportsInstance\",\"__wdata\",\"image_label_binary\",\"image_label_area_select\",\"web3\"],[[\"getElementsByClassName\",[]],[\"getElementById\",[]],[\"querySelector\",[]],[\"querySelectorAll\",[]]],[],true]"
    ],
    [
      3298983941,
      "9345374751420407194"
    ],
    [
      2883186606,
      "[[\"xmLWiTJQHheWvNBOCvRS1KuklcMyuIu3\",\"9\",\"11\",\"UIHCDNVBOZKWC\"],[\"VMxAJMlGcMzBdMWATMBhJMPAJMlEJN1AdMyuIQpNFMyuIQ6FkathneWiTjjFFrZrkVWiTjOkuuElFrwNkMlAJMlYVScDkwZNTwxETKWiTjR52X18FMdjTjWiTjx52X18FMWiTjZrwb6h3bzk\",\"15\",\"32\",\"OIPDJCGGWUDRD\"]]"
    ],
    [
      1578658063,
      "[1,2,3,4]"
    ],
    [
      1392191255,
      "[\"fmyUP2ZKvGDGJTJIlGZYP3DK\",\"f\",\"15\",\"WYPVHCFSKPDVN\"]"
    ],
    [
      645217632,
      "[1,1024,1,1,4]"
    ],
    [
      364527618,
      "[21]"
    ],
    [
      781302243,
      "35257"
    ],
    [
      4286617223,
      "[1920,1080,1920,1040,24,24,false,0,1,1920,1040,true,true,true,false]"
    ],
    [
      3961532981,
      "[-6.172840118408203,-20.710678100585938,120.71067810058594,-20.710678100585938,141.42135620117188,120.71067810058594,-20.710678100585938,141.42135620117188,-20.710678100585938,-20.710678100585938,0,0,400,600,false]"
    ],
    [
      355545911,
      "165624761953926771"
    ],
    [
      1845702994,
      "15307345790125003576"
    ],
    [
      1885396794,
      "[16384,32,16384,2048,2,2048]"
    ],
    [
      1340556786,
      "true"
    ],
    [
      702607242,
      "1713551954614.5"
    ],
    [
      3369879498,
      "18207788058829391080"
    ],
    [
      2258007971,
      "4932383211497360507"
    ],
    [
      1476007714,
      "[[true,\"en-US\",true,\"Microsoft David - English (United States)\",\"Microsoft David - English (United States)\"],[false,\"en-GB\",true,\"Microsoft Hazel - English (United Kingdom)\",\"Microsoft Hazel - English (United Kingdom)\"],[false,\"en-GB\",true,\"Microsoft Susan - English (United Kingdom)\",\"Microsoft Susan - English (United Kingdom)\"]]"
    ],
    [
      3157273169,
      "4.5"
    ],
    [
      2571423665,
      "94.29999995231628"
    ],
    [
      2264178394,
      "\"Europe/Stockholm\""
    ],
    [
      1767811539,
      "7245447288404687584"
    ],
    [
      612273951,
      "[\"Europe/Stockholm\",-60,-60,-3203646808000,\"Central European Standard Time\",\"en-US\"]"
    ],
    [
      2946108189,
      "[0,10465,10465]"
    ],
    [
      3504714987,
      "[1,4,5,7,9,12,20,21,24,25,29,31]"
    ],
    [
      3260504850,
      "[[196,[196,196,196,255,196,196,196,255,196,196,196,255,196,196,196,255]],[[11,0,0,95.96875,15,4,96.765625],[[12,0,-1,113.125,17,4,113],[11,0,0,111,12,4,111],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[12,0,0,109.640625,14,3,110.1953125]]],[0,2,4,5,6,8,9,12,13,15,17,18,19,21,22,23,28,29,30,31,33,34,35,37,39,42,47,48,49,66,67,69,71,72,75,76,77,78,79,81,82],[0,0,0,0,14,3,0]]"
    ],
    [
      1930240485,
      "[299624919858,299624919858,null,null,4294705152,true,true,true,null]"
    ],
    [
      2731828028,
      "1526195183414568207"
    ],
    [
      3672350690,
      "125.80000007152557"
    ],
    [
      3652805059,
      "[4,120,4]"
    ],
    [
      3646847539,
      "[2147483647,2147483647,2147483647,2147483647]"
    ],
    [
      1196101075,
      "[16,1024,4096,7,12,120,[23,127,127]]"
    ],
    [
      3444878050,
      "[[277114314453,277114314460,277114314451,357114314456,277114314452,554228628898,57114314443,717114314371391,554228628897,277114314456,1108457257863,277114314450,554228628919,277114314460,277114314451],false]"
    ],
    [
      206443282,
      "3616525.100000024"
    ],
    [
      3004217393,
      "631"
    ],
    [
      2122633777,
      "10709114373335899612"
    ],
    [
      956283155,
      "[\"Windows\",\"10.0.0\",null,\"64\",\"x86\",\"123.0.6312.122\"]"
    ],
    [
      106767486,
      "[\"Google Inc. (NVIDIA)\",\"ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 (0x00001F82) Direct3D11 vs_5_0 ps_5_0, D3D11)\"]"
    ]
  ],
  "suspicious_events": [],
  "messages": [
    [
      "https://newassets.hcaptcha.com",
      [
        "{\"target\":\"metamask-contentscrip",
        "{\"target\":\"metamask-inpage\",\"dat",
        "{\"target\":\"metamask-inpage\",\"dat",
        "{\"target\":\"metamask-inpage\",\"dat",
        "{\"target\":\"metamask-contentscrip",
        "{\"target\":\"metamask-inpage\",\"dat"
      ]
    ]
  ],
  "stack_data": [
    "r.sendSiteMetadata (<anonymous>)\ne (<anonymous>)",
    "new Promise (<anonymous>)"
  ],
  "stamp": "1:16:2024-04-19:0B/+p0Vj9+Do93iyd/rbJSB4oDGXF4WdYHrs926ZOjTPsYpWXkMdRZz8qpA6j7PRZ6LsnncQzeSxjhGBWm026B644uani4GYX7E1SP7zliA2VFEqT5uzNq74rxV0xMbKdePjjU+/fTCFgLOyNbkk8sAROEng3CcZQs1q6scTl/bgI0YBcGp5GFdLMSgN17FnysNhCTHKhqJDHYioSouQ1v6AXMRSsk/UGHuHpVG+xrpNoP0B9Q==t8fuSBSiq2eB2ZEn::A5OfBhXt:89b9",
  "href": "https://accounts.hcaptcha.com/demo",
  "ardata": None,
  "errs": {
    "list": []
  },
  "perf": [
    [
      1,
      20
    ],
    [
      2,
      868
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
        #self.session = Session(client_identifier='chrome_123', random_tls_extension_order=True)
        self.session = httpx.Client()
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
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
