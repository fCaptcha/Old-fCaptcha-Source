import base64
import json
import time
import httpx
import tls_client
from redis import Redis
import random
import hashlib
from math import ceil
from string import ascii_letters
from random import randint as r
from time import strftime, localtime

client = tls_client.Session("chrome_104", random_tls_extension_order=True)
database_fps = Redis("45.45.238.213", 42081, 313, "ACCA5B570561DCFA5ACB1417C69F2900DAFF8A4FD39A2E66C36DF2BD796F0BE1CFEA8AF2DB18153874215E08BFDEC4A89A397EC53E52DAC33A1E9D0B17A52D43")


class HSW:
    def __init__(self):
        self.key = database_fps.randomkey()

    @staticmethod
    def decrypt(data: str) -> str:
        url = "http://solver.dexv.lol:1500/decrypt"
        json = {"data": data, "key": "realassssffrfr10384"}
        return client.post(url, json=json).text

    @staticmethod
    def encrypt(data: str) -> str:
        url = "http://solver.dexv.lol:1500/encrypt"
        json = {"data": data, "key": "realassssffrfr10384"}
        return client.post(url, json=json).text

    def random_float(self) -> float:
        return random.uniform(0.0000000000000001, 0.9999999999999999)

    def pull(self, jwt: str, host: str, user_agent: str) -> str:
        s = jwt.split(".")[1].encode()
        s += b'=' * (-len(s) % 4)
        parsed = json.loads(base64.b64decode(s, validate=False).decode())
        hc_diff = parsed['s']
        hc_data = parsed['d']
        if data := json.load(open("hsw_types/discord.json", "r")):
            data["stamp"] = self.mint(hc_data, hc_diff)
            data["components"]["navigator"]["user_agent"] = user_agent
            data["components"]["canvas_hash"] = str(random.randint(1000000000000000000,9999999999999999999))
            data["components"]["parent_win_hash"] = str(random.randint(10000000000000000000,99999999999999999999))
            data["components"]["performance_hash"] = str(random.randint(10000000000000000000, 99999999999999999999))
            data["components"]["common_keys_hash"] = random.randint(1000000000,9999999999)
            unique_keys = "__localeData__,DiscordNative,regeneratorRuntime,2,0,__BILLING_STANDALONE__,webpackChunkdiscord_app,platform,__SECRET_EMOTION__,__SENTRY__,hcaptcha,__SENTRY_IPC__,hcaptchaOnLoad,__timingFunction,DiscordErrors,clearImmediate,__OVERLAY__,grecaptcha,DiscordSentry,GLOBAL_ENV,setImmediate,1,IntlPolyfill,createDiscordStream,popupBridge,__DISCORD_WINDOW_ID".split(',')
            random.shuffle(unique_keys)
            data["components"]["unique_keys"] = ",".join(unique_keys)
            data["components"]["inv_unique_keys"] = "__wdata,sessionStorage,localStorage,hsw,_sharedLibs"
            data["components"]["common_keys_tail"] = "chrome,caches,cookieStore,ondevicemotion,ondeviceorientation,ondeviceorientationabsolute,launchQueue,documentPictureInPicture,onbeforematch,getScreenDetails,openDatabase,queryLocalFonts,showDirectoryPicker,showOpenFilePicker,showSaveFilePicker,originAgentCluster,credentialless,speechSynthesis,oncontentvisibilityautostatechange,onscrollend,webkitRequestFileSystem,webkitResolveLocalFileSystemURL,Raven"
            data["rand"] = [self.random_float(), self.random_float()]
            data["href"] = f"https://{host}"
            data["proof_spec"]["data"] = hc_data
            data["proof_spec"]["difficulty"] = hc_diff
            data["stack_data"] = ["new Promise (<anonymous>)"]
            random.shuffle(data["events"])
            for event in data["events"]:
                match event[0]:
                    case 702607242:
                        event[1] = str(round(time.time() * 1000, 1))
                    case 3260504850:
                        event[1] = f"[[69,[69,69,69,255,69,69,69,255,69,69,69,255,69,69,69,255]],[[11,0,1,105.015625,13,5,105.6171875],[[12,0,-1,113.125,17,4,113],[11,0,0,111,12,4,111],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[11,0,1,105.015625,13,5,105.6171875],[12,0,0,109.640625,14,3,110.1953125]]],[0,2,4,5,6,8,9,{str(r(10,12))},13,15,{str(r(16,17))},18,19,{str(r(20,21))},22,23,{str(r(26,28))},29,30,31,{str(r(32,33))},34,35,{str(r(36,37))},39,{str(r(40,45))},47,48,{str(r(49,65))},66,67,69,71,72,{str(r(73,75))},76,77,78,79,81,82],[0,0,0,0,{str(r(10,20))},{str(r(1,17))},0]]"
                    case 3635805594:
                        event[1] = f"[\"{user_agent.split('Mozilla/', 1)[-1]}\",\"{user_agent}\",8,4,\"en-US\",[\"en-US\",\"en-SE\",\"en-GB\",\"fa\",\"sv-SE\"],\"Win32\",null,[\"Not_A Brand 8\",\"Chromium 120\"],false,\"Windows\",2,5,true,false,150,false,false,false,\"[object Keyboard]\",false,false]"
            hsw_str = self.encrypt(json.dumps(data, separators=(",", ":")))
            return hsw_str
        return None

    def mint(self, resource: str, bits: int = 2, ext: str = '', salt_chars: int = 8) -> str:
        timestamp = strftime("%Y-%m-%d", localtime(time.time()))
        challenge = f"1:{bits}:{timestamp}:{resource}:{ext}:{self.get_salt(salt_chars)}"
        return f"{challenge}{self.mint_stamp(challenge, bits)}"

    def get_salt(self, data_in: int) -> str:
        charset = ascii_letters + "+/="
        return ''.join([random.choice(charset) for _ in [None] * data_in])

    def mint_stamp(self, challenge: str, bits: int) -> str:
        counter = 0
        hex_digits = int(ceil(bits / 4.0))
        zeros = '0' * hex_digits
        while 1:
            digest = hashlib.sha1((challenge + hex(counter)[2:]).encode()).hexdigest()
            if digest[:hex_digits] == zeros:
                return hex(counter)[2:]
            counter += 1