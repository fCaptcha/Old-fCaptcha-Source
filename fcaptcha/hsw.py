import json
import base64
import hashlib
import json
import random
import time
from math import ceil
from string import ascii_letters
from time import strftime, localtime
from urllib.parse import quote

import tls_client
import xxhash
from redis import Redis

client = tls_client.Session("chrome_104", random_tls_extension_order=True)
database_fps = Redis("45.45.238.213", 42081, 313,
                     "ACCA5B570561DCFA5ACB1417C69F2900DAFF8A4FD39A2E66C36DF2BD796F0BE1CFEA8AF2DB18153874215E08BFDEC4A89A397EC53E52DAC33A1E9D0B17A52D43")

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

    def random_float(self) -> float:
        return random.uniform(0.0000000000000001, 0.9999999999999999)

    def pull(self, jwt: str, host: str, user_agent: str) -> str | None:
        s = jwt.split(".")[1].encode()
        s += b'=' * (-len(s) % 4)
        parsed = json.loads(base64.b64decode(s, validate=False).decode())
        hc_diff = parsed['s']
        hc_data = parsed['d']
        if data := json.load(open("hsw_types/discord.json")):
            data["stamp"] = self.mint(hc_data, hc_diff)
            data["rand"] = [self.random_float(), self.random_float()]
            data["href"] = f"https://{host}"
            data["proof_spec"]["data"] = hc_data
            data["proof_spec"]["difficulty"] = hc_diff
            data["stack_data"] = ["new Promise (<anonymous>)"]
            random.shuffle(data["events"])
            rand = random.randint(1, 254)
            unhashed_143592240 = [rand,
                                  [rand + 1, rand, rand, 255, rand + 1, rand + 1, rand, 255, rand + 1, rand, rand, 255,
                                   rand + 1, rand, rand + 1, 255]]
            hashed_143592240 = hash_json(unhashed_143592240)
            events = {x: y for x, y in data["events"]}
            gpu_event = json.loads(events.get(669213918))
            for event in data["events"]:
                match event[0]:
                    case 3916977893:
                        event[1] = json.dumps([self.encode(gpu_event[0]), self.encode(gpu_event[1])])
                    case 669213918:
                        event[1] = json.dumps(gpu_event)
                    case 443486963:
                        event[1] = hashed_143592240
                    case 143592240:
                        var0 = json.loads(event[1])
                        var0[0] = unhashed_143592240
                        event[1] = json.dumps(var0, separators=(",", ":"))
                    case 1587180961:
                        event[1] = str(int(time.time() * 1000))
            hsw_str = self.encrypt(json.dumps(data, separators=(",", ":")))
            return hsw_str
        return None

    def mint(self, resource: str, bits: int = 2, ext: str = '', salt_chars: int = 8) -> str:
        timestamp = strftime("%Y-%m-%d", localtime(time.time()))
        challenge = f"1:{bits}:{timestamp}:{resource}:{ext}:{self.get_salt(salt_chars)}:"
        return f"{challenge}{self.mint_stamp(challenge, bits)}"

    @staticmethod
    def get_salt(data_in: int) -> str:
        charset = ascii_letters + "+/="
        return ''.join([random.choice(charset) for _ in [None] * data_in])

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
