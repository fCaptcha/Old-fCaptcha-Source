import json
import random
import string
import base64
import requests
import secrets
import tls_client
import bodystuff
import colorama
import time

colorama.init()

r = requests.get("https://raw.githubusercontent.com/qoft/discord-api/main/fetch")
build_numbers_client = r.json()["build_numbers"]["client"]
build_numbers_main = r.json()["build_numbers"]["main"]
build_numbers_native = r.json()["build_numbers"]["native"]


class DiscordGen:
    def __init__(self):
        self.session = tls_client.Session(
            client_identifier="chrome_120", random_tls_extension_order=True
        )

        with open("data/proxies.txt", "r", encoding="utf-8") as f:
            proxies = f.read().splitlines()
            self.proxy = random.choice(proxies)

        self.session.proxies = f"http://{self.proxy}"

    def generate(self):
        self.session.get("https://discord.com")
        username = self.get_username()
        email = f"{secrets.token_hex(16)}@outlook.com"
        password = self.get_password()
        fingerprint = self.get_fingerprint()
        cookies = self.session.get("https://discord.com").cookies
        xtrack = self.get_xtrack()
        captcha = self.Solve()

        bodystuff.logger.info("creating account", username=username, password=password)
        self.session.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ar-kw,fa-ir;q=0.6,fa;q=0.7,en-us;q=0.7,en;q=0.6,ar;q=0.8",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Cookie": "; ".join(
                [f"{cookie.name}={cookie.value}" for cookie in cookies]
            ),
            "origin": "https://discord.com",
            "referer": "https://discord.com",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": f"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/{build_numbers_client} Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36",
            "x-discord-locale": "en-US",
            "X-Fingerprint": fingerprint,
            "X-Super-Properties": xtrack,
        }
        r = self.session.post(
            "https://discord.com/api/v9/auth/register",
            json={
                "captcha_key": captcha,
                "fingerprint": fingerprint,
                "email": f"{email}",
                "username": username,
                "global_name": username,
                "password": password,
                "invite": "",
                "consent": True,
                "date_of_birth": "2001-11-02",
                "gift_code_sku_id": None,
                "promotional_email_opt_in": False,
            },
        )
        if "token" in r.json():
            token = r.json()["token"]
            bodystuff.logger.success("Account Created!", username=username)
            self.session.headers["Authorization"] = token
            r = self.session.get("https://discord.com/api/v9/users/@me")
            flags = r.json()["flags"]
            if r.status_code == 200:
                bodystuff.logger.success(
                    "Account Not Locked!",
                    username=username,
                    token=token,
                    flags=flags,
                )
                with open("./output/unlocked.txt", "a") as f:
                   f.write(f"{email}:{password}:{token}" + "\n")
            else:
                if "40002" in r.json():
                    bodystuff.logger.error("Account Locked!")
                else:
                    bodystuff.logger.error("Account Locked!")
                    print(r.json())
        else:
            bodystuff.logger.error("failed to create account", response=r.json())

    def get_fingerprint(self):
        return self.session.get("https://discord.com/api/v9/experiments").json()["fingerprint"]

    def get_username(self):
        return secrets.token_hex(16)

    def get_password(self):
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(25)
        )

    def Solve(self):
        bodystuff.logger.info("Solving Captcha")
        start = time.time()
        payload = {
            "api_key": '',
            "url": 'discord.com',
            "sitekey": '4c672d35-0701-42b2-88c3-78380b0db560',
            "proxy": self.proxy,
            "user_agent": f"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/{build_numbers_client} Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36"
        }
        result = requests.post("", json=payload)
        data = result.json()
        if data.get("success"):
            bodystuff.logger.success(f"Solved Captcha {data['message'][:70]}  In {str(time.time() - start)[:5]} Seconds")
            return data['message']
        else:
            bodystuff.logger.error(f"Failed To Solve Captcha", error={data.get('message')})

    def get_xtrack(self):
        return base64.b64encode(
            json.dumps(
                {
                    "os": "Windows",
                    "browser": "Discord Client",
                    "release_channel": "stable",
                    "client_version": build_numbers_client,
                    "os_version": "10.0.19045",
                    "os_arch": "x64",
                    "app_arch": "ia32",
                    "system_locale": "en-US",
                    "browser_user_agent": f"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/{build_numbers_client} Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36",
                    "browser_version": "28.2.10",
                    "client_build_number": build_numbers_client,
                    "native_build_number": build_numbers_native,
                    "client_event_source": None,
                }
            ).encode()
        ).decode()


def genn():
   Sigma = DiscordGen()
   Sigma.generate()


genn()