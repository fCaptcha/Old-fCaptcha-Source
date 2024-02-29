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
        print("Solving Captcha...")
        start = time.time()

        payload = {"api_key": self.api_key, "url": self.url, "sitekey": self.sitekey, "proxy": self.proxy}
        if self.rqdata: payload["rqdata"] = self.rqdata

        while True:
            try:
                result = requests.post("http://solver.dexv.lol:1000/api/solve_hcap", json=payload)
                data = result.json()
                if data.get("success"):
                    print(f"Solved Captcha / {data['message'][:70]} / In {str(time.time() - start)[:5]} Seconds")
                    return data['message']
                print(f"Failed To Solve Captcha -> {data.get('message')}")
                break
            except Exception as e:
                print(f"Failed To Solve Captcha -> {e}")

Captcha(
    api_key="DEXV-ADMIN-D1IWNf-ZBMl8m-TutuyP",
    sitekey='4c672d35-0701-42b2-88c3-78380b0db560',
    url='discord.com', 
    proxy="g5hltixerdytvio:g7w9oxoov0b8jsz@rp.proxyscrape.com:6060"
).solve()