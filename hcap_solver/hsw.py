import json
import httpx
from redis import Redis
import hashlib
import time
from math import ceil
from random import choice
from string import ascii_letters
from time import strftime, localtime
import random


database_fps = Redis(
    "80.75.212.79",
    6379,
    240,
    "k7rCJ59itoIjwaAFF930WVe99T8aagAtLc4b3CAdO7sXCAQ27ef4j9UJpBv0dObmw3QeK9XwZeh2alLmxR8Xl50etyTR74teQRXys6dfe7n5TvO3OK7pvc2WieIgqokHxlHTSQeFQBDq0vEYxEYAzV8NKWb77TtTXUSAY"
)
client = httpx.Client()


def mint(resource, bits=2, ext='', salt_chars=8):
    timestamp = strftime("%Y-%m-%d", localtime(time.time()))
    challenge = f"1:{bits}:{timestamp}:{resource}:{ext}:{_get_salt(salt_chars)}"
    return f"{challenge}:{_mint_stamp(challenge, bits)}"


def _get_salt(data_in):
    charset = ascii_letters + "+/="
    return ''.join([choice(charset) for _ in [None] * data_in])


def _mint_stamp(challenge, bits):
    counter = 0
    hex_digits = int(ceil(bits / 4.0))
    zeros = '0' * hex_digits
    while 1:
        digest = hashlib.sha1((challenge + hex(counter)[2:]).encode()).hexdigest()
        if digest[:hex_digits] == zeros:
            return hex(counter)[2:]
        counter += 1

def decrypt(data):
    url = "http://solver.dexv.lol:1500/decrypt"
    json = {"data": data, "key": "realassssffrfr10384"}
    return client.post(url, json=json).text

def encrypt(data):
    url = "http://solver.dexv.lol:1500/encrypt"
    json = {"data": data, "key": "realassssffrfr10384"}
    return client.post(url, json=json).text


def pull(hc_diff: int, hc_data: str, ardata: str):
    if data := json.loads(database_fps.get(database_fps.randomkey())):
        data["stamp"] = mint(hc_data, hc_diff)
        data["rand"] = [random.random()]
        data["components"]["canvas_hash"] = str(random.randint(10000000000000000000, 99999999999999999999))
        data["components"]["performance_hash"] = str(random.randint(10000000000000000000, 99999999999999999999))
        data["components"]["unique_keys"] = "otStubData,dataLayer,initDownloadButton,ttPolicy,tram,GLOBAL_ENV,Localize,initSignUpOrOpenButtons,0,_,Webflow,OptanonActiveGroups,WebFont,hcaptcha,gaGlobal,google_tag_data,IntlPolyfill,OnetrustActiveGroups,onYouTubeIframeAPIReady,webpackChunkdiscord_marketing,grecaptcha,2,OneTrust,__skippedLocalizeInit,google_tag_manager,1,hcaptchaOnLoad,clearImmediate,setImmediate,_babelPolyfill,initLogInOrOpenDiscordButton,YTConfig,Optanon,$,onYTReady,pageUsesReact,scriptUrl,objectFitPolyfill,OneTrustStub,regeneratorRuntime,jQuery,platform,YT,core"
        data["components"]["inv_unique_keys"] = "sessionStorage,hsw,image_label_binary,__wdata,_sharedLibs,localStorage"
        data["components"]["common_keys_tail"] = "webkitCancelAnimationFrame,webkitRequestAnimationFrame,chrome,fence,caches,cookieStore,ondevicemotion,ondeviceorientation,ondeviceorientationabsolute,launchQueue,sharedStorage,documentPictureInPicture,getScreenDetails,queryLocalFonts,showDirectoryPicker,showOpenFilePicker,showSaveFilePicker,originAgentCluster,credentialless,speechSynthesis,onscrollend,webkitRequestFileSystem,webkitResolveLocalFileSystemURL,Raven"
        data["stack_data"] = ["new Promise (<anonymous>)"]
        data["ardata"] = None
        data["href"] = "https://discord.com/"
        data["proof_spec"]["data"] = hc_data
        data["proof_spec"]["difficulty"] = hc_diff
        for x in data["events"]:
            if x[0] == 284488784:
                x[1] = json.dumps([
                    [
                        57, [random.randint(17, 23), random.randint(17, 23), 57, 255, 57, 57, random.randint(17, 23), 255, 57, 57, 57, 255, 57, 57, 57, 255]
                    ],
                    [
                        [
                            random.randint(17, 23), 0, 0, 95.96875, 15, 4, 96.765625
                        ],
                        [
                            [
                                random.randint(17, 23), 0, -1, 113.125, 17, 4, 113
                            ],
                            [
                                random.randint(17, 23), 0, 0, 111, 12, 4, 111
                            ],
                            [
                                11, 0, 0, 95.96875, 15, 4, 96.765625
                            ],
                            [
                                11, 0, 0, 95.96875, 15, 4, 96.765625
                            ],
                            [
                                11, 0, 0, 95.96875, 15, 4, 96.765625
                            ],
                            [
                                11, 0, 0, 95.96875, 15, 4, 96.765625
                            ],
                            [
                                11, 0, 0, 95.96875, 15, 4, 96.765625
                            ],
                            [11, 0, 0, 95.96875, 15, 4, 96.765625
                             ],
                            [
                                12, 0, 0, 109.640625, 14, 3, 110.1953125
                            ]
                        ]
                    ],
                    [
                        0, random.randint(1, 7),
                        8, random.randint(10, 14),
                        15, random.randint(17, 23),
                        24, 26, 27, 28, 29, 30, 31, 32, 34, 37, 39, 40, 49, 69, 75, 76, 79,
                        random.randint(80, 1123)
                    ],
                    [
                        0, 0, 0, 0, random.randint(1, 23), random.randint(1, 23), 0
                    ]
                ], separators=(",", ":"))
            if x[0] == 1825909650:
                x[1] = "[[\"loadTimes\",\"csi\",\"app\"],35,34,null,false,false,true,37,true,true,true,true,true,[\"Raven\",\"_sharedLibs\",\"hsw\",\"__wdata\",\"image_label_binary\"],[[\"getElementsByClassName\",[]],[\"getElementById\",[]],[\"querySelector\",[]],[\"querySelectorAll\",[]]],[],true]"
            #if x[0] == 308248000:
            #    x[1] = f"[[[\"https://newassets.hcaptcha.com/captcha/v1/fadb9c6/hcaptcha.js#i={ardata}\",0,5]],[[\"*\",84,9]]]"
            if x[0] == 1213335269:
                x[1] = f"[[\"img:imgs.hcaptcha.com\",0,{random.random() * 100}],[\"img:imgs3.hcaptcha.com\",0,{random.random() * 100}],[\"navigation:newassets.hcaptcha.com\",{random.random() * 100},{random.random() * 100}],[\"script:newassets.hcaptcha.com\",{random.random() * 100},{random.random() * 100}],[\"xmlhttprequest:api.hcaptcha.com\",0,{random.random() * 100}]]"
            if x[0] == 1304795084:
                x[1] = str(round(time(), 1))
        data["perf"] = [
            [
                1,
                float(random.randint(1, 13))
            ],
            [
                2,
                float(random.randint(13, 200))
            ],
            [
                3,
                0.0
            ]
        ]
        return encrypt(json.dumps(data, separators=(",", ":")))
    return None
