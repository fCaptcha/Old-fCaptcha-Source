import concurrent.futures
from hcap_solver.logger import *
import requests
import time

class Captcha:
    def __init__(self, api_key: str, url: str, sitekey: str, proxy: str, rqdata: str = None) -> None:
        self.api_key = api_key
        self.url = url
        self.sitekey = sitekey
        self.proxy = proxy
        self.rqdata = rqdata

    def solve(self) -> str:
        #log.info("Solving Captcha...")
        start = time.time()

        payload = {"api_key": self.api_key, "url": self.url, "sitekey": self.sitekey, "proxy": self.proxy}
        if self.rqdata: payload["rqdata"] = self.rqdata

        while True:
            try:
                result = requests.post("http://solver.dexv.lol:1000/api/solve_hcap", json=payload)
                data = result.json()
                if data.get("success"):
                    log.captcha(f"Solved Captcha / {data['message'][:70]} / In {str(time.time() - start)[:5]} Seconds")
                    return data['message']
                #log.failure(f"Failed To Solve Captcha -> {data.get('message')}")
                break
            except Exception as e:
                pass
                #log.failure(f"Failed To Solve Captcha -> {e}")

def solve_captcha():
    while True:
        Captcha(
            api_key="DEXV-ADMIN-71BczP-nssbPD-eR61cH",
            sitekey='4c672d35-0701-42b2-88c3-78380b0db560',
            url='discord.com', 
            proxy="22ujtl8x9pqc9jg-odds-5+100:3cc232m47zd7ftr@rp.proxyscrape.com:6060"
        ).solve()

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    for _ in range(100):
        executor.submit(solve_captcha)