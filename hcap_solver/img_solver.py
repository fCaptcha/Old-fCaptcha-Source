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
    "data": "k2kqshsTRKsw6Y3ilgyIwTaSTdQdqwh3/Jv6CvPX4PGeQ828UU/DQEhRypicZ7GtAd4OmrGd2EBxQXl+1jgdhoTS+uA+j4jGl7FKHZcRT1hHwrBi+3GmJsVi5x30gi7U/5yEltmI9cUYSp8DwK1onkK8dYk/jbciX2gH5rhYX1LmJ7Eh+60QiHXfsBl8ZmgG5nRlt1mhlAjHNoz00nHK5JJVV6lufQ1zITJvLtSpqWpdjG39m6FeF/ntNUn00cnf",
    "_location": "https://newassets.hcaptcha.com/c/e78a38c",
    "timeout_value": 1000
  },
  "rand": [
    0.765966403188455,
    0.15956021286547184
  ],
  "components": {
    "navigator": {
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9041 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36",
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
    "parent_win_hash": "12176117950321074744",
    "webrtc_hash": "-1",
    "performance_hash": "11097854906383886648",
    "unique_keys": "__localeData__,PermissionStore,ReadStateStore,useEffect,SnowflakeUtils,DiscordNative,canonicalizeReplace,SearchableSelect,findByCode,ScrollerThin,MaskedLink,MessageStore,zustandPersist,useToken,Button,ModalImageClasses,SelectedGuildStore,TextArea,regeneratorRuntime,UserProfileStore,2,__isReactDndBackendSetUp,0,__BILLING_STANDALONE__,findExportedComponent,shortcutList,InviteActions,useCallback,webpackChunkdiscord_app,platform,wpex,React,UserSettingsActionCreators,Paginator,__SECRET_EMOTION__,ComponentTypes,Dialog,GuildMemberStore,__SENTRY__,reload,IconUtils,lodash,fakeRender,Parser,UserProfileActions,findByProps,hcaptcha,SettingsRouter,Card,__SENTRY_IPC__,useRef,hcaptchaOnLoad,MessageActions,moment,zustandCreate,Vencord,Flex,PluginsApi,wp,RelationshipStore,restart,wpsearch,Switch,OAuth2AuthorizeModal,Slider,WindowStore,UserUtils,useMemo,ButtonWrapperClasses,__timingFunction,wpexs,findComponentByCode,UploadHandler,SelectedChannelStore,ContextMenuApi,useReducer,TextAndImagesSettingsStores,findAll,canonicalizeReplacement,findStore,Api,DiscordErrors,GuildChannelStore,ReactDOM,RestAPI,Tooltip,Flux,findAllByProps,VencordNative,plugins,clearImmediate,Alerts,Select,Clickable,VencordStyles,__OVERLAY__,showToast,findAllComponentsByCode,DraftStore,Timestamp,grecaptcha,Popout,Avatar,findAllByCode,GuildStore,ButtonLooks,FluxDispatcher,GLOBAL_ENV,canonicalizeMatch,setImmediate,useStateFromStores,Settings,1,Toasts,EmojiStore,IntlPolyfill,NavigationRouter,useState,ComponentDispatch,PresenceStore,Forms,wpc,TabBar,UserStore,hljs,DraftType,ApplicationAssetUtils,createDiscordStream,TextInput,MenuTypes,Menu,_ws,UtilTypes,popupBridge,PermissionsBits,i18n,FocusLock,StatusSettingsStores,ChannelStore,wreq,__DISCORD_WINDOW_ID,PrivateChannelsStore",
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
      1196101075,
      "[32,4096,16384,7,14,128,[23,127,127]]"
    ],
    [
      422388259,
      "[[[\"https://newassets.hcaptcha.com/captcha/v1/b1c589a/hcaptcha.js\",0,5]],[[\"*\",84,9]]]"
    ],
    [
      2883186606,
      "[[\"UYrSfmlwiTjf1WbLp2yoUUbtvmAJLcMY\",\"18\",\"d\",\"AJVYIVSLDCQRF\"],[\"JMleVdnrmcrzwEiNGcWItjOAJdWADMWeeMCNUKPMkMlAJMlgSUZPHEJbxBPAJMlI0Y0dwYJbJMlgSU1dGzyFlz5j2YWbJMleJLZ4CMWItjUNnaPlHBWItjOUUBTVmaJNkMlAJMlkFtFP0Qib3z0NGcPA\",\"18\",\"a\",\"ZJXPOPORTWEOB\"]]"
    ],
    [
      1767811539,
      "4226317358175830201"
    ],
    [
      40999691,
      "[\"KjN3EDo1KjM=iTN3\",\"7\",\"5\",\"OXLISFPFFPVKW\"]"
    ],
    [
      1578658063,
      "[1,2,3,4]"
    ],
    [
      3444878050,
      "[[277114314453,277114314460,277114314451,357114314456,277114314452,554228628898,57114314443,717114314371391,554228628897,277114314456,1108457257862,277114314450,554228628919,277114314460,277114314451],false]"
    ],
    [
      3635805594,
      "[\"5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9041 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36\",\"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9041 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36\",8,4,\"en-US\",[\"en-US\",\"en-SE\",\"en-GB\",\"fa\",\"sv-SE\"],\"Win32\",null,[\"Not_A Brand 8\",\"Chromium 120\"],false,\"Windows\",2,5,true,false,50,false,false,false,\"[object Keyboard]\",false,false]"
    ],
    [
      3652805059,
      "[4,128,4]"
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
      1845702994,
      "15307345790125003576"
    ],
    [
      3004217393,
      "627"
    ],
    [
      3504714987,
      "[1,4,5,7,9,12,20,21,24,25,29,31]"
    ],
    [
      1192669439,
      "13051680398954254262"
    ],
    [
      1578500414,
      "16153807394097295248"
    ],
    [
      2338842265,
      "3313549113868922289"
    ],
    [
      106767486,
      "[\"Google Inc. (Google)\",\"ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)\"]"
    ],
    [
      645217632,
      "[1,1023,1,1,4]"
    ],
    [
      1340556786,
      "false"
    ],
    [
      4174694926,
      "[[],35,34,null,false,false,true,37,true,true,true,true,true,[\"Raven\",\"_sharedLibs\",\"hsw\",\"__wdata\"],[[\"getElementsByClassName\",[]],[\"getElementById\",[]],[\"querySelector\",[]],[\"querySelectorAll\",[]]],[],true]"
    ],
    [
      1930240485,
      "[25796718592,25796718592,null,null,1098907648,true,true,true,null]"
    ],
    [
      3369879498,
      "11038406483972230190"
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
      157020890,
      "17002384262467705698"
    ],
    [
      355545911,
      "1825316679185413516"
    ],
    [
      3672350690,
      "46.19999998807907"
    ],
    [
      2731828028,
      "4631229088072584217"
    ],
    [
      1438921646,
      "[[\"navigation:newassets.hcaptcha.com\",7.399999976158142,24.100000023841858],[\"script:newassets.hcaptcha.com\",18.55000001192093,46.19999998807907],[\"xmlhttprequest:api2.hcaptcha.com\",0,127.10000002384186]]"
    ],
    [
      1392191255,
      "[\"X2Z1NmenRWZx1mAnH2DGjTjL\",\"12\",\"d\",\"HUDKSQSAXJOYF\"]"
    ],
    [
      702607242,
      "1713733748341.7"
    ],
    [
      612273951,
      "[\"Europe/Stockholm\",-60,-60,-3203646808000,\"Central European Standard Time\",\"en-US\"]"
    ],
    [
      2264178394,
      "\"Europe/Stockholm\""
    ],
    [
      956283155,
      "[\"Windows\",\"10.0.0\",null,\"64\",\"x86\",\"120.0.6099.291\"]"
    ],
    [
      3260504850,
      "[[5,[5,5,5,255,5,5,5,255,5,5,5,255,5,5,5,255]],[[11,0,1,105.015625,13,5,105.6171875],[[12,0,-1,113.125,17,4,113],[11,0,0,111,12,4,111],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[12,0,0,109.640625,14,3,110.1953125]]],[0,2,4,5,6,8,9,12,13,15,17,18,19,21,22,23,28,29,30,31,33,34,35,37,39,42,47,48,49,66,67,69,71,72,75,76,77,78,79,81,82],[0,0,0,0,14,3,0]]"
    ],
    [
      202322096,
      "2337666753322697468"
    ],
    [
      2258007971,
      "4932383211497360507"
    ],
    [
      2122633777,
      "12073207331849695208"
    ],
    [
      2638668498,
      "[60,72,65536,245760,245760]"
    ],
    [
      3961532981,
      "[-6.172840118408203,-20.710678100585938,120.71067810058594,-20.710678100585938,141.42135620117188,120.71067810058594,-20.710678100585938,141.42135620117188,-20.710678100585938,-20.710678100585938,0,0,300,150,false]"
    ],
    [
      4286617223,
      "[1920,1080,1920,1040,24,24,false,0,1,1920,1040,true,true,true,false]"
    ],
    [
      1933294324,
      "[16,4096,31,32,16384,124,14,128,[23,127,127]]"
    ],
    [
      980782277,
      "[8192,8192,8192,8,8,4]"
    ],
    [
      1885396794,
      "[8192,64,16384,2048,15,2048]"
    ],
    [
      1833974975,
      "16290568259171983358"
    ],
    [
      206443282,
      "1516.5"
    ],
    [
      3646847539,
      "[2147483647,2147483647,2147483647,2147483647]"
    ],
    [
      3157273169,
      "14.5"
    ],
    [
      3298983941,
      "9345374751420407194"
    ],
    [
      2571423665,
      "81.19999992847443"
    ],
    [
      3741287486,
      "[2147483647,2147483647,4294967294]"
    ],
    [
      364527618,
      "[23]"
    ]
  ],
  "suspicious_events": [],
  "messages": None,
  "stack_data": None,
  "stamp": "1:2:2024-04-21:k2kqshsTRKsw6Y3ilgyIwTaSTdQdqwh3/Jv6CvPX4PGeQ828UU/DQEhRypicZ7GtAd4OmrGd2EBxQXl+1jgdhoTS+uA+j4jGl7FKHZcRT1hHwrBi+3GmJsVi5x30gi7U/5yEltmI9cUYSp8DwK1onkK8dYk/jbciX2gH5rhYX1LmJ7Eh+60QiHXfsBl8ZmgG5nRlt1mhlAjHNoz00nHK5JJVV6lufQ1zITJvLtSpqWpdjG39m6FeF/ntNUn00cnf::qcnPUW4k:25",
  "href": "https://discord.com/register?email=dex&redirect_to=%2Fchannels%2F%40me%2F1222616146981945456",
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
      90
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
