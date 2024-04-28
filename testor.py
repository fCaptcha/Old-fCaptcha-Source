import requests

class fCaptcha:
    def __init__(self, api_key: str, sitekey: str, host: str, proxy: str, rqdata: str = None, user_agent: str = None) -> None:
        self.api_key = api_key
        self.sitekey = sitekey
        self.host = host
        self.proxy = proxy
        self.rqdata = rqdata
        self.user_agent = user_agent

    def solve(self) -> str:
        try:
            headers = {"authorization": self.api_key}
            payload = {}
            keys = ['sitekey', 'host', 'proxy', 'rqdata', 'user_agent']
            for key in keys:
                if getattr(self, key) is not None:
                    payload[key] = getattr(self, key)
                
            result = requests.post("https://api.fcaptcha.lol/api/createTask", headers=headers, json=payload)
            task_id = result.json()["task"]["task_id"]
            payload = {"task_id": task_id}
            while True:
                result = requests.get(f"https://api.fcaptcha.lol/api/getTaskData", headers=headers, json=payload)
                data = result.json()
                if data["task"]["state"] == "processing":
                    continue
                time = data["task"]["time"]
                capkey = data["task"]["captcha_key"]
                print(f"Solved Captcha / {capkey[:70]} / In {str(time)[:3]} Seconds")
                return capkey
        except Exception as e:
            print(f"Failed to solve -> {e}")

fCaptcha(
    api_key="DEXV-ADMIN-71BczP-nssbPD-eR61cH",
    sitekey='4c672d35-0701-42b2-88c3-78380b0db560',
    host='discord.com',
    proxy="6c78f8469c;any:bcbc8697ff@datacenter.sigmaproxies.com:9000"
).solve()