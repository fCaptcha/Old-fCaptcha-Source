
from datetime import datetime
import tls_client
import secrets
import json
import base64
from hcap_solver import Hcaptcha 

def x_super():
    return base64.b64encode(
        json.dumps(
            {
                "os": "Android",
                "browser": "Discord Android",
                "device": "ASUS_I003DD",
                "system_locale": "en-US",
                "client_version": "216.14 - rn",
                "release_channel": "googleRelease",
                "device_vendor_id": "6bfb5c3c-411e-4c1f-87fb-326a9da50260",
                "browser_user_agent": "",
                "browser_version": "",
                "os_version": "28",
                "client_build_number": 216014,
                "client_event_source": None,
            }
        ).encode()
    ).decode()

X_TRACK = x_super()


class DiscordGen:
    def __init__(self):
        self.proxy = "g5hltixerdytvio:g7w9oxoov0b8jsz@rp.proxyscrape.com:6060"
        self.session = tls_client.Session(
            client_identifier="chrome_120",
            force_http1=True,
        )
        self.user_agent = "Discord-Android/216014;RNA"
        self.session.headers.pop("Accept-Encoding")
        self.session.proxies = {'http': f'http://{self.proxy}', 'https': f'http://{self.proxy}'}

        self.session.headers = {
            "Accept-Language": "en-US",
            "Content-Type": "application/json",
            "Connection": "Keep-Alive",
            "Host": "discord.com",
            "User-Agent": self.user_agent,
            "x-context-properties": "eyJsb2NhdGlvbiI6Ii8ifQ==",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": X_TRACK,
        }
        self.session.get("https://discord.com")

    def getCookies(self):
        return self.session.get("https://discord.com/").cookies

    def getFingerprint(self):
        return (
            self.session.get(
                "https://discord.com/api/v9/experiments",
                params={
                    "with_guild_experiments": "true",
                },
            )
            .json()
            .get("fingerprint")
        )


    def gen(self):
        cookies = self.getCookies()
        self.session.cookies = cookies
        fingerprint = self.getFingerprint()
        print(f"Got Fingerprint {fingerprint}")
        self.session.headers["X-Fingerprint"] = fingerprint
        captcha_key = Hcaptcha(sitekey='4c672d35-0701-42b2-88c3-78380b0db560', host='discord.com',  proxy="g5hltixerdytvio:g7w9oxoov0b8jsz@rp.proxyscrape.com:6060").solve()
        self.session.headers["x-captcha-key"] = captcha_key
        print(f"Solved Captcha {captcha_key[:30]}")
        response = self.session.post(
            "https://discord.com/api/v9/auth/register",
            json={
                "fingerprint": fingerprint,
                "email": secrets.token_hex(6) + "@hotmail.com",
                "username": secrets.token_hex(6),
                "global_name": "SlotthWasHere",
                "password": secrets.token_hex(12) + "!",
                "invite": None,
                "consent": True,
                "date_of_birth": "1997-02-21",
                "gift_code_sku_id": None,
            },
        )
        print(response.text)


DiscordGen().gen()
