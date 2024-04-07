import concurrent.futures

from hcap_solver import HCaptcha
from hcap_solver.logger import *
import requests
import time


def solve_captcha():
    while True:
        start = time.time()
        if key := HCaptcha(
            '4c672d35-0701-42b2-88c3-78380b0db560',
            'discord.com',
            "22ujtl8x9pqc9jg-odds-5+100:3cc232m47zd7ftr@rp.proxyscrape.com:6060"
        ).solve():
            end = time.time()
            log.captcha(key[-30:], start, end)


with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    for _ in range(100):
        executor.submit(solve_captcha)
