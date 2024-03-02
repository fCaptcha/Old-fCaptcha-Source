import json

import httpx
from redis import Redis
import hashlib
from math import ceil
from random import choice
from string import ascii_letters
from time import strftime, localtime, time


def mint(resource, bits=2, now=None, ext='', salt_chars=8):
    timestamp = strftime("%Y-%M-%d", localtime(now))
    challenge = f"1:{bits}:{timestamp}:{resource}:{ext}:{_get_salt(salt_chars)}"
    return challenge + _mint_stamp(challenge, bits)


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


database_fps = Redis(
    "80.75.212.79",
    6379,
    240,
    "k7rCJ59itoIjwaAFF930WVe99T8aagAtLc4b3CAdO7sXCAQ27ef4j9UJpBv0dObmw3QeK9XwZeh2alLmxR8Xl50etyTR74teQRXys6dfe7n5TvO3OK7pvc2WieIgqokHxlHTSQeFQBDq0vEYxEYAzV8NKWb77TtTXUSAY"
)
client = httpx.Client()


def decrypt(data):
    return client.post("http://83.143.112.20:8080/decrypt", headers={
        "key": "nigger321993021"
    }, json={
        "data": data
    }, timeout=93824).json().get("data")


def encrypt(data):
    return client.post("http://83.143.112.20:8080/encrypt", headers={
        "key": "nigger321993021"
    }, json={
        "data": data
    }, timeout=93824).json().get("data")


def pull(hc_diff: int, hc_data: str, ardata: str):
    if data := database_fps.get(database_fps.randomkey()):
        data = json.loads(data)
        data["stamp"] = mint(hc_data, hc_diff)
        for x in data["events"]:
            match x[0]:
                case 308248000:
                    new = json.loads(x[1])
                    new[0][0][0] = f"https://newassets.hcaptcha.com/captcha/v1/fadb9c6/hcaptcha.js#i={ardata}"
                    x[1] = new
        data["ardata"] = ardata
        data["proof_spec"]["data"] = hc_data
        return encrypt(json.dumps(data))
    return None