import json
import random
import string
import base64
import requests
import secrets
import tls_client
import bodystuff
from hcap_solver import Hcaptcha

r = requests.get("https://raw.githubusercontent.com/qoft/discord-api/main/fetch")
build_numbers_client = r.json()["build_numbers"]["client"]
build_numbers_main = r.json()["build_numbers"]["main"]
build_numbers_native = r.json()["build_numbers"]["native"]

class DiscordGen:
    def __init__(self):
        self.session = tls_client.Session(
            client_identifier="chrome_108",
            random_tls_extension_order=True
        )
        self.session.proxies = "http://qapnxywtcwnmbmn38052:bmvgavatiz@prem_resi.turboproxy.in:16666"

    def generate(self):
        cookies = self.session.get("https://discord.com").cookies
        username = self.get_username()
        password = self.get_password()
        fingerprint = self.get_fingerprint()
        xtrack = self.get_xtrack()
        captcha = Hcaptcha(
            site_key='4c672d35-0701-42b2-88c3-78380b0db560',
            host='discord.com', 
            proxy="qapnxywtcwnmbmn38052:bmvgavatiz@prem_resi.turboproxy.in:16666"
        ).solve()

        bodystuff.logger.info("creating account", username=username, password=password)
        self.session.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": 'ar-kw,fa-ir;q=0.6,fa;q=0.7,en-us;q=0.7,en;q=0.6,ar;q=0.8',
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Cookie": "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies]),
            "origin": "https://discord.com",
            "referer": "https://discord.com/register?redirect_to=%2Fchannels%2F%40me",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9038 Chrome/120.0.6099.291 Electron/28.2.7 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "X-Fingerprint": fingerprint,
            "X-Super-Properties": xtrack,
        }

        r = self.session.post("https://discord.com/api/v9/auth/register", json={
            "captcha_key": captcha,
            "fingerprint": fingerprint,
            "email": f"{username}{secrets.token_hex(1)}@outlook.com",
            "username": username,
            "global_name": username,
            "password": password,
            "invite": "qraid",
            "consent": True,
            "date_of_birth": "2001-02-10",
            "gift_code_sku_id": None,
            "promotional_email_opt_in": False,
        })

        if "token" in r.json():
            bodystuff.logger.success("account created", username=username, password=password, token=r.json()["token"])
            self.session.headers["Authorization"] = r.json()["token"]
            r = self.session.get("https://discord.com/api/v9/users/@me/guilds")
            if r.status_code == 200:
                bodystuff.logger.success("Account Not Locked!", username=username, password=password, token=r.json()["token"][:30])
                with open("tokens.txt", "a") as f:
                    f.write(r.json()["token"] + "\n")
            else:
                if '40002' in r.json():
                    bodystuff.logger.error("Account Locked!")
                else:
                    bodystuff.logger.error("Account Locked!")
                    print(r.json())
        else:
            bodystuff.logger.error("failed to create account", response=r.json())

    def get_fingerprint(self):
        return self.session.get("https://discord.com/api/v9/experiments").json()["fingerprint"]

    def get_username(self):
        while True:
            username = self.session.get("https://randomuser.me/api/").json()["results"][0]["login"]["username"]
            check = self.session.post(f"https://discord.com/api/v9/unique-username/username-attempt-unauthed",json={
                "username": username
            }).json()["taken"]
            if check:
                self.get_username()
            else:
                return username

    def get_password(self):
        return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(25))

    def get_xtrack(self):
        return base64.b64encode(json.dumps({
            "os": "Windows",
            "browser": "Discord Client",
            "release_channel": "stable",
            "client_version": build_numbers_client,
            "os_version": "10.0.19045",
            "os_arch": "x64",
            "app_arch": "ia32",
            "system_locale": "en-US",
            "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9038 Chrome/120.0.6099.291 Electron/28.2.7 Safari/537.36",
            "browser_version": "28.2.7",
            "client_build_number": build_numbers_client,
            "native_build_number": build_numbers_native,
            "client_event_source": None,
        }).encode()).decode()

def Gen():
    DiscordGen().generate()

#Gen()

# Uncomment to make run forever thing
import concurrent.futures
with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
    for _ in range(10):
        executor.submit(Gen)
