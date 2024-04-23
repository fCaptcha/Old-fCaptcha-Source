from time import strftime, localtime
from string import ascii_letters
from random import randint as r
from redis import Redis
from math import ceil
import hashlib
import random
import base64
import httpx
import json
import time


class HSW:
    def __init__(self) -> None:
        self.database_fps = Redis("80.75.212.79", 6379, 240, "k7rCJ59itoIjwaAFF930WVe99T8aagAtLc4b3CAdO7sXCAQ27ef4j9UJpBv0dObmw3QeK9XwZeh2alLmxR8Xl50etyTR74teQRXys6dfe7n5TvO3OK7pvc2WieIgqokHxlHTSQeFQBDq0vEYxEYAzV8NKWb77TtTXUSAY")
        self.client = httpx.Client()

    def that_thing(self) -> list:
        thing = []
        thing.append(random.randint(50, 200))
        thing.append([random.randint(50, 200) for _ in range(8)])
        thing.append([[random.randint(10, 20), 0, random.choice([-1, 0, 1]), random.uniform(100, 120), random.randint(10, 20), random.randint(3, 6), random.uniform(100, 120)] for _ in range(10)])
        thing.append([random.randint(0, 100) for _ in range(40)])
        thing.append([0, 0, 0, 0, random.randint(10, 20), random.randint(1, 20), 0])
        return thing
    
    def decrypt(self, data: str) -> str:
        url = "http://solver.dexv.lol:1500/decrypt"
        json = {"data": data, "key": "realassssffrfr10384"}
        return self.client.post(url, json=json).text

    def encrypt(self, data: str) -> str:
        url = "http://solver.dexv.lol:1500/encrypt"
        json = {"data": data, "key": "realassssffrfr10384"}
        return self.client.post(url, json=json).text

    def random_float(self) -> float:
        return random.uniform(0.0000000000000001,0.9999999999999999)
    
    def pull(self, req: str, host: str, user_agent: str) -> str:
        s = req.split(".")[1].encode()
        s += b'=' * (-len(s) % 4)
        parsed = json.loads(base64.b64decode(s, validate=False).decode())
        hc_diff = parsed['s']
        hc_data = parsed['d']
        if data := json.load(open("n.json", "r")):
            data["stamp"] = self.mint(hc_data, hc_diff)
            data["components"]["navigator"]["user_agent"] = user_agent
            data["components"]["canvas_hash"] = str(random.randint(1000000000000000000,9999999999999999999))
            data["components"]["parent_win_hash"] = str(random.randint(10000000000000000000,99999999999999999999))
            data["components"]["performance_hash"] = str(random.randint(10000000000000000000, 99999999999999999999))
            data["components"]["common_keys_hash"] = random.randint(1000000000,9999999999)
            data["components"]["unique_keys"] = "__localeData__,DiscordNative,regeneratorRuntime,2,0,__BILLING_STANDALONE__,webpackChunkdiscord_app,platform,__SECRET_EMOTION__,__SENTRY__,hcaptcha,__SENTRY_IPC__,hcaptchaOnLoad,__timingFunction,DiscordErrors,clearImmediate,__OVERLAY__,grecaptcha,DiscordSentry,GLOBAL_ENV,setImmediate,1,IntlPolyfill,createDiscordStream,_ws,popupBridge,__DISCORD_WINDOW_ID"
            data["components"]["inv_unique_keys"] = "__wdata,sessionStorage,localStorage,hsw,_sharedLibs"
            data["components"]["common_keys_tail"] = "chrome,caches,cookieStore,ondevicemotion,ondeviceorientation,ondeviceorientationabsolute,launchQueue,documentPictureInPicture,onbeforematch,getScreenDetails,openDatabase,queryLocalFonts,showDirectoryPicker,showOpenFilePicker,showSaveFilePicker,originAgentCluster,credentialless,speechSynthesis,oncontentvisibilityautostatechange,onscrollend,webkitRequestFileSystem,webkitResolveLocalFileSystemURL,Raven"
            data["rand"] = [self.random_float(), self.random_float()]
            data["href"] = f"https://{host}"
            data["proof_spec"]["data"] = hc_data
            data["proof_spec"]["difficulty"] = hc_diff
            data["stack_data"] = ["new Promise (<anonymous>)"]
            for event in data["events"]:
                match event[0]:
                    case 702607242:
                        event[1] = str(round(time.time() * 1000, 1))
                    case 3260504850:
                        event[1] = str(self.that_thing())
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