import json
import time
import httpx
from redis import Redis
import hashlib
from math import ceil
from random import choice
from string import ascii_letters
from time import strftime, localtime

database_fps = Redis(
    "80.75.212.79",
    6379,
    240,
    "k7rCJ59itoIjwaAFF930WVe99T8aagAtLc4b3CAdO7sXCAQ27ef4j9UJpBv0dObmw3QeK9XwZeh2alLmxR8Xl50etyTR74teQRXys6dfe7n5TvO3OK7pvc2WieIgqokHxlHTSQeFQBDq0vEYxEYAzV8NKWb77TtTXUSAY"
)
client = httpx.Client()

def decrypt(data):
    url = "http://solver.dexv.lol:1500/decrypt"
    json = {"data": data, "key": "realassssffrfr10384"}
    return client.post(url, json=json).text

def encrypt(data):
    url = "http://solver.dexv.lol:1500/encrypt"
    json = {"data": data, "key": "realassssffrfr10384"}
    return client.post(url, json=json).text

def pull(key: str, hc_diff: int, hc_data: str):
    if data := json.loads(database_fps.get(key)):
        data["stamp"] = mint(hc_data, hc_diff)
        data["href"] = "https://discord.com/"
        data["proof_spec"]["data"] = hc_data
        data["proof_spec"]["difficulty"] = hc_diff
        data["stack_data"] = [
            "new Promise (<anonymous>)"
        ]
        for event in data["events"]:
            match event[0]:
                case 2228825458:
                    event[1] = str(round(time.time() / 1000, 1))
        d = encrypt(json.dumps(data, separators=(",", ":")))
        return d
    return None


def mint(resource, bits=2, ext='', salt_chars=8):
    timestamp = strftime("%Y-%m-%d", localtime(time.time()))
    challenge = f"1:{bits}:{timestamp}:{resource}:{ext}:{_get_salt(salt_chars)}"
    return f"{challenge}{_mint_stamp(challenge, bits)}"


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