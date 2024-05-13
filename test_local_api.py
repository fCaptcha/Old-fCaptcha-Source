import threading
import requests, httpx
from fcaptcha import Hcaptcha

def solve_captcha():
    return Hcaptcha(
        site_key='4c672d35-0701-42b2-88c3-78380b0db560',
        host='discord.com/register', 
        proxy="oxp76Hrr7o6IYbaR:X3r6ouTUsWATFRd0@geo.iproyal.com:12321",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9146 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36"
    ).solve()

def execute_thread():
    while True:
        try:
            g = solve_captcha()
            if g:
                httpx.post("http://localhost:9999/make_token", json={"captcha_key": g, "proxy": "oxp76Hrr7o6IYbaR:X3r6ouTUsWATFRd0@geo.iproyal.com:12321"})
        except Exception as e:
            print(e)

if __name__ == "__main__":
    threads = []
    for _ in range(30):
        thread = threading.Thread(target=execute_thread)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
