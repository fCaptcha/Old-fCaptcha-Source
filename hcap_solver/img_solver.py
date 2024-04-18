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
      "data": "Lq+UDc7qtn3nT5M8p/MrGhy5mAXzDd/O1ozKji1EJXmLKRNn46fmvKukB0V7hwhlWiF9nKD1CSoVdtpGLUpIQBaTdyxkCJWOUphK/xQwIcdJUMo/e9xaTxpst4Hz/K/vsmOhC19vDeRPiFvjHve4PjDgO2J/kR0m7mvg98/AqAFQGhNBVVfZ0iZS8HMRNJH6U/w0gNJMOQVuFQCi3qwaiVtmd0XWAi+Y11eWxLzpKlxvF36vUXLOueC4LeRT6NzX",
      "_location": "https://newassets.hcaptcha.com/c/e78a38c",
      "timeout_value": 1000
    },
    "rand": [
      0.42094430598666466,
      0.7744985257741064
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
      "parent_win_hash": "1099413536459394834",
      "webrtc_hash": "-1",
      "performance_hash": "11097854906383886648",
      "unique_keys": "regeneratorRuntime,1,GLOBAL_ENV,__BILLING_STANDALONE__,webpackChunkdiscord_app,__localeData__,createDiscordStream,popupBridge,hcaptcha,__SENTRY_IPC__,0,__OVERLAY__,DiscordErrors,clearImmediate,grecaptcha,DiscordSentry,__timingFunction,hcaptchaOnLoad,IntlPolyfill,__SENTRY__,__DISCORD_WINDOW_ID,setImmediate,__SECRET_EMOTION__,2,platform,DiscordNative",
      "inv_unique_keys": "localStorage,_sharedLibs,hsw,__wdata,sessionStorage",
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
        157020890,
        "17002384262467705698"
      ],
      [
        1578658063,
        "[1,2,3,4]"
      ],
      [
        1438921646,
        "[[\"navigation:newassets.hcaptcha.com\",75.59999996423721,367],[\"script:newassets.hcaptcha.com\",107.5,385.60000002384186],[\"xmlhttprequest:api2.hcaptcha.com\",0,212.69999998807907]]"
      ],
      [
        2731828028,
        "4631229088072584217"
      ],
      [
        3298983941,
        "9345374751420407194"
      ],
      [
        3157273169,
        "92"
      ],
      [
        422388259,
        "[[[\"https://newassets.hcaptcha.com/captcha/v1/b1c589a/hcaptcha.js\",0,5]],[[\"*\",84,9]]]"
      ],
      [
        3961532981,
        "[-6.172840118408203,-20.710678100585938,120.71067810058594,-20.710678100585938,141.42135620117188,120.71067810058594,-20.710678100585938,141.42135620117188,-20.710678100585938,-20.710678100585938,0,0,300,150,false]"
      ],
      [
        1885396794,
        "[16384,32,16384,2048,2,2048]"
      ],
      [
        2338842265,
        "3313549113868922289"
      ],
      [
        3652805059,
        "[4,120,4]"
      ],
      [
        3741287486,
        "[2147483647,2147483647,4294967294]"
      ],
      [
        3444878050,
        "[[277114314453,277114314460,277114314451,357114314456,277114314452,554228628898,57114314443,717114314371391,554228628897,277114314456,1108457257862,277114314450,554228628919,277114314460,277114314451],false]"
      ],
      [
        645217632,
        "[1,1024,1,1,4]"
      ],
      [
        202322096,
        "2337666753322697468"
      ],
      [
        3369879498,
        "11038406483972230190"
      ],
      [
        1196101075,
        "[16,1024,4096,7,12,120,[23,127,127]]"
      ],
      [
        1845702994,
        "15307345790125003576"
      ],
      [
        612273951,
        "[\"Europe/Stockholm\",-60,-60,-3203646808000,\"Central European Standard Time\",\"en-US\"]"
      ],
      [
        4286617223,
        "[1920,1080,1920,1040,24,24,false,0,1,1280,720,true,true,true,false]"
      ],
      [
        1930240485,
        "[26417430528,26417430528,null,null,1098907648,true,true,true,null]"
      ],
      [
        1340556786,
        "true"
      ],
      [
        1933294324,
        "[16,4095,30,16,16380,120,12,120,[23,127,127]]"
      ],
      [
        2264178394,
        "\"Europe/Stockholm\""
      ],
      [
        3672350690,
        "289.84999999403954"
      ],
      [
        3004217393,
        "627"
      ],
      [
        2122633777,
        "12073207331849695208"
      ],
      [
        1578500414,
        "16153807394097295248"
      ],
      [
        106767486,
        "[\"Google Inc. (NVIDIA)\",\"ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 (0x00001F82) Direct3D11 vs_5_0 ps_5_0, D3D11)\"]"
      ],
      [
        3635805594,
        "[\"5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.221 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36\",\"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.221 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36\",8,4,\"en-US\",[\"en-US\",\"en-SE\",\"en-GB\",\"fa\",\"sv-SE\"],\"Win32\",null,[\"Not_A Brand 8\",\"Chromium 120\"],false,\"Windows\",2,5,true,false,350,false,false,false,\"[object Keyboard]\",false,false]"
      ],
      [
        206443282,
        "3878"
      ],
      [
        364527618,
        "[23]"
      ],
      [
        3504714987,
        "[1,4,5,7,9,12,20,21,24,25,29,31]"
      ],
      [
        3260504850,
        "[[223,[223,223,223,255,223,223,223,255,223,223,223,255,223,223,223,255]],[[11,0,1,105.015625,13,5,105.6171875],[[12,0,-1,113.125,17,4,113],[11,0,0,111,12,4,111],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[12,0,0,109.640625,14,3,110.1953125]]],[0,2,4,5,6,8,9,12,13,15,17,18,19,21,22,23,28,29,30,31,33,34,35,37,39,42,47,48,49,66,67,69,71,72,75,76,77,78,79,81,82],[0,0,0,0,14,3,0]]"
      ],
      [
        1833974975,
        "16290568259171983358"
      ],
      [
        1192669439,
        "13177607191192652685"
      ],
      [
        40999691,
        "[\"eZN0MDM1iDO=iJN0\",\"3\",\"5\",\"JWHEUEQTXJZIV\"]"
      ],
      [
        2638668498,
        "[24,24,65536,212988,200704]"
      ],
      [
        2571423665,
        "118.10000002384186"
      ],
      [
        355545911,
        "14882824317255702596"
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
        1392191255,
        "[\"bzBxcJlndzrxAGJTJxh3cn9G\",\"4\",\"13\",\"OOKYXQFKXVARY\"]"
      ],
      [
        980782277,
        "[32767,32767,16384,8,8,8]"
      ],
      [
        3737842855,
        "1117"
      ],
      [
        1476007714,
        "[[true,\"en-US\",true,\"Microsoft David - English (United States)\",\"Microsoft David - English (United States)\"],[false,\"en-GB\",true,\"Microsoft Hazel - English (United Kingdom)\",\"Microsoft Hazel - English (United Kingdom)\"],[false,\"en-GB\",true,\"Microsoft Susan - English (United Kingdom)\",\"Microsoft Susan - English (United Kingdom)\"]]"
      ],
      [
        1767811539,
        "4226317358175830201"
      ],
      [
        702607242,
        "1713477023100.3"
      ],
      [
        4174694926,
        "[[],35,34,null,false,false,true,37,true,true,true,true,true,[\"Raven\",\"_sharedLibs\",\"hsw\",\"__wdata\"],[[\"getElementsByClassName\",[]],[\"getElementById\",[]],[\"querySelector\",[]],[\"querySelectorAll\",[]]],[],true]"
      ],
      [
        956283155,
        "[\"Windows\",\"10.0.0\",null,\"64\",\"x86\",\"120.0.6099.291\"]"
      ],
      [
        2883186606,
        "[[\"vrMLwItJIBHcO1MzO80VkVKSClCmyuiS\",\"1\",\"10\",\"URRPNMKNZTOGR\"],[\"uumXajmlgCm5BDmWatmhHjmPajmlejN1aDmyuCsVlFmyuCsMdeczRMZWitJpdlsFPkQWitJO80VKVksCNkmlajmli0ti1kRFNtRXetKWitJXR3x18FmDJtJWitJ3R3x18FmWitJFP2cMRwdz\",\"1\",\"31\",\"HWPEOTAITMXSU\"]]"
      ],
      [
        689964981,
        "57"
      ],
      [
        3646847539,
        "[2147483647,2147483647,2147483647,2147483647]"
      ]
    ],
    "suspicious_events": [],
    "messages": None,
    "stack_data": None,
    "stamp": "1:2:2024-04-18:Lq+UDc7qtn3nT5M8p/MrGhy5mAXzDd/O1ozKji1EJXmLKRNn46fmvKukB0V7hwhlWiF9nKD1CSoVdtpGLUpIQBaTdyxkCJWOUphK/xQwIcdJUMo/e9xaTxpst4Hz/K/vsmOhC19vDeRPiFvjHve4PjDgO2J/kR0m7mvg98/AqAFQGhNBVVfZ0iZS8HMRNJH6U/w0gNJMOQVuFQCi3qwaiVtmd0XWAi+Y11eWxLzpKlxvF36vUXLOueC4LeRT6NzX::LubYurU0:9",
    "href": "https://canary.discord.com/register",
    "ardata": None,
    "errs": {
      "list": []
    },
    "perf": [
      [
        1,
        11
      ],
      [
        2,
        124
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
        self.session = Session(client_identifier='chrome_120', random_tls_extension_order=True)
        self.before = time.time()
        self.session.headers = {
            'authority': 'hcaptcha.com',
            'accept': 'application/json',
            'accept-language': 'en-US',
            'content-type': 'text/plain',
            'origin': 'https://newassets.hcaptcha.com',
            'referer': 'https://newassets.hcaptcha.com/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.221 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36',
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
        target = captcha["requester_question"]["en"]
        captcha_type = captcha["request_type"]
    
        self.c2 = captcha['c']
        self.key = captcha['key']
        log.captcha(f"Solving Captcha -> {captcha_type}...")
        
        if captcha_type == "image_label_binary":
            images = {f"image{i+1}": captcha['tasklist'][i]["datapoint_uri"] for i in range(9)}
            solution = solve_grid(target, images, self.site_key, self.host)["solution"]
            self.job = "image_label_binary"
            return {captcha['tasklist'][i]["task_key"]: str(i in solution).lower() for i in range(9)}
    
        elif captcha_type == "image_label_area_select":
            self.job = "image_label_area_select"
            return solve_area_select(target, captcha['tasklist'], self.site_key, self.host)
    
        else:
            log.failure(f"Unsupported Captcha Type -> {captcha_type}", level="hCaptcha")

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
