from gevent import monkey
monkey.patch_all()

from playwright.sync_api import sync_playwright
from colorama import Fore, Style
from flask import Flask, request
from tls_client import Session
from datetime import datetime
from re import findall
import threading
import requests
import asyncio
import logging
import ctypes
import time

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)
session = Session(client_identifier='chrome_118', random_tls_extension_order=True)
heads = {
    "host": 'hcaptcha.com',
    "connection": 'keep-alive',
    "accept": 'application/json',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    "sec-ch-ua": '"Chromium";v="118", "Not A(Brand";v="24", "Google Chrome";v="118"',
    "sec-ch-ua-mobile": '?0',
    "sec-ch-ua-platform": '"Windows"',
    "origin": 'https://newassets.hcaptcha.com',
    "referer": 'https://newassets.hcaptcha.com/',
    "sec-fetch-site": 'same-site',
    "sec-fetch-mode": 'cors',
    "sec-fetch-dest": 'empty',
    "accept-encoding": 'gzip, deflate, br',
    "accept-language": 'en-US,en-SE;q=0.9,sv-SE;q=0.6'
}
session.headers = heads

class Stuff:
    amount = 0
    instance = None

ctypes.windll.kernel32.SetConsoleTitleW(f"Dexv-Solver HSW Server | Solved HSW: {Stuff.amount}")
dolphin_key = "Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiYWM5YzM5MzgyNjhhY2IyMTdhZThlYzUwYzA5NWYzMmVlMWY4YjljN2IyMTZiNTQ4YzUzODg3MDMzZjVhMDYxNTg2ODA5ZWI2NGY0OWVmY2IiLCJpYXQiOjE3MDg1NDI3NTYuMzA4NjQyLCJuYmYiOjE3MDg1NDI3NTYuMzA4NjQ1LCJleHAiOjE3NDAwNzg3NTYuMjk0MzA2LCJzdWIiOiIzMTI3NzA1Iiwic2NvcGVzIjpbXX0.ZbCwHf3kOYM6Nvii9-P8rjs05Wllfc0kiu4CUO_fNJy5aKsaZw4opV6t31z11zzakC4nhExqT9IWTadkwwsiZz57CBQsvvy30I0PJNWFRrdt-EltAHULEA8iJxIDmE5ohirKqszJGx0MIo0kjXS2D3_GPFpsv3VDlbH8vr8vkImu9iexpJXIUzELiX4nl_ZX0hKDkFes7H43PfhbXwV25vCZqu26A3oYqrNpuw9_ScBtGdCr-zIrblKjGOegT5NMhAsY9OEQ_TBkjyaRlgmkUjcD0N04MOxmrlkWAu_155HOQNHI8UfmckZXs3AgwyTl_VkKH8b2f9TKiW7yQQEGjESuFd9QwLcIm63waVfPTuovAOAkXHN6O_Pg-fs80HcRjhqOFEtx-Ap1WZ5i62mDtF-9WCRd_vFIodLdX5bUHTNVY1mIUQ2HC_GwVMymdqtHoH6eFlPikWTHmIfJJrFeA2EORO1lk0yVMa39EnVoZHyiM3gPI5ELan364hGPRJ2LxUyvrORtiYQzBsWdsiPH9nEBmjRz8UPl6nKY3td88hcR4MK439lPudINEjbQmy-QWird8h-Ybt4hSYPQF5YCQRr7wp3zLghkpTS5_GLiJH_ifQFRfPhzd64xECoksm-_-RcH7a6KUxJWHGPbZuKCrEThZW3TWo0KcZjTTb8wXT0"
            
class HSW:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.loop = asyncio.new_event_loop()

    def run(self, brow: str):
        Stuff.instance = self
        self.task(brow)
        self.discord()
        self.get_iframe()

        while True:
            time.sleep(60)
            self.page.evaluate("hcaptcha.execute()")

    @app.route('/hsw', methods = ["POST"])
    def get_hsw():
        s = time.time()
        req = request.get_json()["req"]
        with Stuff.instance.lock:
            hsw = Stuff.instance.frame.evaluate(f"hsw('{req}')")
            rn = datetime.now().strftime("%X")
            print(f"{Style.BRIGHT}{Fore.LIGHTBLACK_EX}{rn} {Fore.MAGENTA}/ {Fore.LIGHTGREEN_EX}Successfully Got HSW {Fore.MAGENTA}/ {Fore.LIGHTBLACK_EX}{hsw[:80]} {Fore.MAGENTA}/ {Fore.LIGHTGREEN_EX}Length: {len(hsw)} {Fore.MAGENTA}/ {Fore.LIGHTGREEN_EX}Time: {str(time.time() - s)[:5]}{Fore.RESET}")
        
        Stuff.amount += 1
        ctypes.windll.kernel32.SetConsoleTitleW(f"Dexv-Solver HSW Server | Solved HSW: {Stuff.amount}")
        return hsw

    def task(self, brow: str) -> None:
        self.playwright = sync_playwright().start()
        if brow == "undet":
            browser_id = list(requests.get("http://127.0.0.1:25325/list").json()["data"])[0]
            link = requests.get(f"http://127.0.0.1:25325/profile/start/{browser_id}", timeout=20.0).json()["data"]["websocket_link"]
        if brow == "anty":
            automation = requests.get(f"http://localhost:3001/v1.0/browser_profiles/284793315/start?automation=1", timeout=10.0, headers={"Authorization": dolphin_key}).json()
            link = f"ws://127.0.0.1:{automation['automation']['port']}{automation['automation']['wsEndpoint']}"

        self.browser = self.playwright.chromium.connect_over_cdp(link).contexts[0]
        self.page = self.browser.pages[0]
        html = open('./hcap_solver/hsw.html', 'r').read()
        self.page.set_content(html, wait_until="domcontentloaded")
        self.page.route("https://discord.com/", lambda r: r.fulfill(status=200, body=html.encode('utf-8'), content_type="text/html",))

    def discord(self) -> None:
        self.page.goto("https://discord.com/")
        self.page.wait_for_load_state('domcontentloaded')

    def get_iframe(self) -> None:
        s = time.time()
        found = False
        iframe = self.page.wait_for_selector("xpath=/html/body/center/div[1]/iframe")
        iframe = iframe.content_frame()
        button = iframe.wait_for_selector("xpath=/html/body/div/div[1]/div[1]/div/div/div[1]")
        button.click()

        r = get_req()

        while not found:
            self.page.wait_for_timeout(1000)
            for frame in self.page.frames:
                try:
                    frame.evaluate(f"hsw('{r}')")
                    found = True
                    self.frame = frame
                except:
                    pass

        rn = datetime.now().strftime("%X")            
        print(f"{Style.BRIGHT}{Fore.LIGHTBLACK_EX}{rn} {Fore.MAGENTA}/ {Fore.LIGHTGREEN_EX}Successfully Opened hCaptcha Embed {Fore.MAGENTA}/ {Fore.LIGHTGREEN_EX}{str(time.time() - s)[:5]}")

def get_version():
    js = requests.get('https://hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaOnLoad').text
    return findall(r'v1\/([A-Za-z0-9]+)\/static', js)[1]

def get_req():
    return session.post('https://hcaptcha.com/checksiteconfig', params={
        'v': get_version(),
        'host': 'discord.com',
        'sitekey': "4c672d35-0701-42b2-88c3-78380b0db560",
        'sc': '1',
        'swa': '1',}
    ).json()['c']["req"]

threading.Thread(target=lambda: app.run(host='0.0.0.0', port="6969", debug=False, use_reloader=False)).start()
HSW().run("undet")