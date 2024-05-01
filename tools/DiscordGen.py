import json
import multiprocessing
import random
import string
import base64
import threading
import traceback

import requests
import secrets
import tls_client
import bodystuff
import colorama
import concurrent.futures
from hcap_solver import DATABASE, HCaptchaEnterpriseChallenge
from kopeechka import MailActivations

colorama.init()

# Dont Abuse cus only has like $1 on this 😭
api = MailActivations(api_token="f8f4546f2d204d2a4b486b25dc7ce433")

r = requests.get("https://raw.githubusercontent.com/qoft/discord-api/main/fetch")
build_numbers_client = r.json()["build_numbers"]["client"]
build_numbers_main = r.json()["build_numbers"]["main"]
build_numbers_native = r.json()["build_numbers"]["native"]


class DiscordGen:
    def __init__(self):
        self.session = tls_client.Session(
            client_identifier="chrome_108", random_tls_extension_order=True
        )

        with open("proxies.txt", "r", encoding="utf-8") as f:
            proxies = f.read().splitlines()
            self.proxy = random.choice(proxies)

        self.session.proxies = f"http://{self.proxy}"

    def generate(self):
        self.session.get("https://discord.com")
        username = self.get_username()
        # email = api.mailbox_get_email("discord.com", "outlook")
        email = f"{secrets.token_hex(16)}@outlook.com"
        password = self.get_password()
        fingerprint = self.get_fingerprint()
        xtrack = self.get_xtrack()
        while True:
            try:
                if captcha := HCaptchaEnterpriseChallenge(
                        site_key="4c672d35-0701-42b2-88c3-78380b0db560",
                        site_url="https://discord.com",
                        proxy=f"http://{self.proxy}",
                        database=DATABASE
                ).solve(True):
                    break
            except Exception:
                pass
        bodystuff.logger.info("creating account", username=username, password=password)
        self.session.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "DNT": "1",
            "Host": "discord.com",
            "Origin": "https://discord.com",
            "Referer": 'https://discord.com/register',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "TE": "trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            "X-Debug-Options": "bugReporterEnabled",
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": "Asia/Calcutta",
            "X-Track": xtrack,
        }
        retard_req = self.session.post(
            "https://discord.com/api/v9/auth/register",
            json={
                "captcha_key": captcha,
                "fingerprint": fingerprint,
                "global_name": username,
                "invite": "sRAW4yzy",
                "consent": True
            }
        )
        if "token" in retard_req.json():
            token = retard_req.json()["token"]
            bodystuff.logger.success("Account Created!", username=username)
            self.session.headers["Authorization"] = token
            retard_req = self.session.get("https://discord.com/api/v9/users/@me")
            flags = retard_req.json()["flags"]
            if retard_req.status_code == 200:
                bodystuff.logger.success(
                    "Account Not Locked!", username=username, token=token[:40], flags=flags
                )
                # e_token = self.GetVerifylink(email)
                # e_solve = Hcaptcha(
                #     site_key="f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34",
                #     host="discord.com",
                #     proxy=self.proxy,
                # ).solve()
                # verify = self.session.post(
                #     "https://discord.com/api/v9/auth/verify",
                #     headers={
                #         "Authorization": token,
                #         "X-Captcha-Key": e_solve,
                #     },
                #     json={"token": e_token},
                # )
                # if verify.status_code == 200:
                #     bodystuff.logger.success(f"Successfully Verified", Token=token[:40])#
                #     token = verify.json()["token"]
                #     with open("tokens.txt", "a") as f:
                #         f.write(f"{email.mail}:{password}:{token}" + "\n")
            else:
                if "40002" in retard_req.json():
                    bodystuff.logger.error("Account Locked!")
                else:
                    bodystuff.logger.error("Account Locked!")
                    print(retard_req.json())
        else:
            bodystuff.logger.error("failed to create account", response=retard_req.json())

    def get_fingerprint(self):
        return self.session.get("https://discord.com/api/v9/experiments").json()[
            "fingerprint"
        ]

    def get_username(self):
        return secrets.token_hex(16)

    def get_password(self):
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(25)
        )

    def GetVerifylink(self, email):
        bodystuff.logger.info("Waiting for verification link...")
        while True:
            ans_3 = self.session.get(
                f"https://api.kopeechka.store/mailbox-get-message?id={email.id}&token=f8f4546f2d204d2a4b486b25dc7ce433&full=&type=json&api=2.0"
            )
            while ans_3.json()["status"] == "OK":
                link = ans_3.json()["value"]
                if link == "" or "click.discord.com" not in link:
                    bodystuff.logger.error(f"Failed to Get Verification Token :(")
                    return None
                r = self.session.get(link, allow_redirects=False)
                link = r.headers["Location"]
                token = link.split("=")[-1]
                bodystuff.logger.success(f"Retrieved Token", Token=token[:40])
                return token

    def get_xtrack(self):
        return base64.b64encode(
            json.dumps(
                {
                    "os": "Windows",
                    "browser": "Discord Client",
                    "release_channel": "canary",
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
                }
            ).encode()
        ).decode()


def genn():
    while 1:
        try:
            i = DiscordGen()
            i.generate()
        except Exception:
            pass


def proc():
    for i in range(101):
        threading.Thread(target=genn).start()
