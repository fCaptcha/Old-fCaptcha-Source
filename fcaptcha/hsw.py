import json
import base64
import hashlib
import json
import random
import time
from io import BytesIO
from math import ceil
from string import ascii_letters
from time import strftime, localtime
from urllib.parse import quote
from zlib import crc32

import numpy
import tls_client
import xxhash
from redis import Redis

client = tls_client.Session("chrome_104", random_tls_extension_order=True)
database_fps = Redis("45.45.238.213", 42081, 313, "ACCA5B570561DCFA5ACB1417C69F2900DAFF8A4FD39A2E66C36DF2BD796F0BE1CFEA8AF2DB18153874215E08BFDEC4A89A397EC53E52DAC33A1E9D0B17A52D43")
hash_json = lambda x: str(xxhash.xxh64(json.dumps(x, separators=(",", ":")), seed=5575352424011909552).intdigest())


class HSW:
    def __init__(self):
        self.key = database_fps.randomkey()

    @staticmethod
    def encode(input_str: str) -> list:
        h_a, in_arr = 'abcdefghijklmnopqrstuvwxyz', ''.join(chr(random.randint(65, 90)) for _ in range(13))
        rand_a = random.randint(1, 26)
        result = []

        for char in input_str[::-1]:
            if char.isalpha():
                shifted_char = h_a[(h_a.index(char.lower()) + rand_a) % 26]
                result.append(shifted_char.upper() if char.isupper() else shifted_char)
            else:
                result.append(char)

        result = ''.join(result)[::-1]
        b64 = base64.b64encode(quote(result).encode()).decode()[::-1]
        b64rand = random.randint(1, len(b64) - 1)
        b64 = b64[b64rand:] + b64[:b64rand]

        output = [char.lower() if char.isupper() else char.upper() if char in in_arr or char in in_arr.lower() else char
                  for char in b64]

        return [''.join(output), f"{rand_a:x}", f"{b64rand:x}", in_arr]

    @staticmethod
    def decrypt(data: str) -> str:
        url = "http://solver.dexv.lol:1500/decrypt"
        json = {"data": data, "key": "88de30e1c0d0e89d"}
        return client.post(url, json=json).text

    @staticmethod
    def encrypt(data: str) -> str:
        url = "http://solver.dexv.lol:1500/encrypt"
        json = {"data": data, "key": "88de30e1c0d0e89d"}
        return client.post(url, json=json).text

    @staticmethod
    def random_float() -> float:
        return random.uniform(0.0000000000000001, 0.9999999999999999)

    def pull(self, jwt: str, host: str, user_agent: str) -> str | None:
        s = jwt.split(".")[1].encode()
        s += b'=' * (-len(s) % 4)
        parsed = json.loads(base64.b64decode(s, validate=False).decode())
        hc_diff = parsed['s']
        hc_data = parsed['d']
        if data := json.loads(client.get(f"https://hcap.capbypass.com/api/fetchhsw?jwt={jwt}").content):
            data["stamp"] = self.mint(hc_data, hc_diff)
            data["rand"] = [self.random_float()]
            data["href"] = f"https://{host}"
            data["proof_spec"]["data"] = hc_data
            data["proof_spec"]["difficulty"] = hc_diff
            data["stack_data"] = ["new Promise (<anonymous>)"]
            random.shuffle(data["events"])
            rand = random.randint(1, 254)
            r = [rand, [rand, rand, rand, 255, rand, rand, rand, 255, rand, rand, rand, 255, rand, rand, rand, 255]]
            hashed_3485632643 = hash_json(r[1])
            events = {x: y for x, y in data["events"]}
            gpu_event = json.loads(events.get(405066441))
            rand_event = json.loads(events.get(1491932711))[0]
            timezone_event = json.loads(events.get(2679091159))
            for event_id, event_value in events.items():
                match event_id:
                    case 3349438585:
                        event_value = json.dumps(self.encode(timezone_event), separators=(",", ":"))
                    case 2979183504:
                        event_value = json.dumps(self.encode(str(rand_event)), separators=(",", ":"))
                    case 3503035011:
                        event_value = json.dumps([self.encode(gpu_event[0]), self.encode(gpu_event[1])], separators=(",", ":"))
                    case 214505624:
                        event_value = hashed_3485632643
                    case 3485632643:
                        var0 = json.loads(event_value)
                        var0[0] = r
                        event_value = json.dumps(var0, separators=(",", ":"))
                    case 4148757807:
                        event_value = str(round(time.time() * 1000, 1))
                events.update({
                    event_id: event_value
                })
            data["events"] = [[x, y] for x, y in events.items()]
            hsw_str = self.encrypt(json.dumps(data, separators=(",", ":")))
            data["rand"].append(numpy.uint32(crc32(hsw_str.encode())) * 2.3283064365386963e-10)
            hsw_str = self.encrypt(json.dumps(data, separators=(",", ":")))
            return hsw_str
        return None

    def mint(self, resource: str, bits: int = 2, ext: str = '', salt_chars: int = 8) -> str:
        timestamp = strftime("%Y-%m-%d", localtime(time.time()))
        challenge = f"1:{bits}:{timestamp}:{resource}:{ext}:{self.get_salt(salt_chars)}:"
        return f"{challenge}{self.mint_stamp(challenge, bits)}"

    @staticmethod
    def get_salt(salt_length: int) -> str:
        charset = ascii_letters + "+/="
        return ''.join([random.choice(charset) for _ in range(salt_length)])

    @staticmethod
    def mint_stamp(challenge: str, bits: int) -> str:
        counter = 0
        hex_digits = int(ceil(bits / 4.0))
        zeros = '0' * hex_digits
        while 1:
            digest = hashlib.sha1((challenge + hex(counter)[2:]).encode()).hexdigest()
            if digest[:hex_digits] == zeros:
                return hex(counter)[2:]
            counter += 1