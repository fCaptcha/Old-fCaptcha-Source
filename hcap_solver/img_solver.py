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
    "data": "WK2aL9dtcAKKBF3RReLPOfdfpZtfF/uaRzVVEQ63IPEaFYydJz0R7ogmAzU5aFmE9riopKXoSEr3dU52ojf5ZzQaX7bnEZ6c9DmbZKpS6mY9d0Ii+tJr1nfHLhqme7SRktYV4UnFFMV9sb3yKTvDZIGZYWvovi2QRQ0PBQoqsvP2EXXidALY2kExoD+bSmNierAz/k6FjaYwVBikUPbhTN7YBDr2zmX3MI9sDA8f1kI1Soe8Oh50qT7ZxI3maqZ2",
    "_location": "https://newassets.hcaptcha.com/c/e78a38c",
    "timeout_value": 1000.0
  },
  "rand": [
    0.692674159538677,
    0.31257969001308084
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
    "device_pixel_ratio": 1.0,
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
    "extensions": [False],
    "parent_win_hash": "12176117950321074744",
    "webrtc_hash": "-1",
    "performance_hash": "4140103483592612201",
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
    [3635805594, "[\"5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9041 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36\",\"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9041 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36\",8,4,\"en-US\",[\"en-US\",\"en-SE\",\"en-GB\",\"fa\",\"sv-SE\"],\"Win32\",null,[\"Not_A Brand 8\",\"Chromium 120\"],false,\"Windows\",2,5,true,false,50,false,false,false,\"[object Keyboard]\",false,false]"]
  ],
  "href": "https://discord.com/",
  "stamp": "1:2:2024-04-21:WK2aL9dtcAKKBF3RReLPOfdfpZtfF/uaRzVVEQ63IPEaFYydJz0R7ogmAzU5aFmE9riopKXoSEr3dU52ojf5ZzQaX7bnEZ6c9DmbZKpS6mY9d0Ii+tJr1nfHLhqme7SRktYV4UnFFMV9sb3yKTvDZIGZYWvovi2QRQ0PBQoqsvP2EXXidALY2kExoD+bSmNierAz/k6FjaYwVBikUPbhTN7YBDr2zmX3MI9sDA8f1kI1Soe8Oh50qT7ZxI3maqZ2::VDufKz9i:2"
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
