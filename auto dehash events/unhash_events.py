import xxhash, json, os
from colorama import Fore
os.system("cls")

from playwright.sync_api import sync_playwright
import requests, json

def decrypt(data:str) -> dict:
    return json.loads(requests.post(
        "http://solver.dexv.lol:1500/decrypt", json={
            "data": data,
            "key": "88de30e1c0d0e89d"
        }
    ).text)

with open("hsw.js") as file:
    hsw=file.read()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False).new_context(bypass_csp=True)
    page = browser.new_page()

    page.route("https://discord.com/", lambda route: route.fulfill(
        status=200,
        body=open("captcha.html","r+").read().replace("SITEKEYHERE","4c672d35-0701-42b2-88c3-78380b0db560"))
    )
    page.goto("https://discord.com/")
    page.add_script_tag(content="Object.defineProperty(navigator, \"webdriver\", {\"get\": () => false})")
    page.add_script_tag(content=hsw)
    response = page.evaluate(f"hsw(\"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmIjowLCJzIjoyLCJ0IjoidyIsImQiOiIxMWV0QytPYTNhVWdHd2M3TFF1Tms2aUgvWmQvMm1LeUFFdllZRDBKOGdUcE4yK2xEcXBNZmxuVFpnY2NBQUlaUW9GeVRpb3E3WmNyTkthc2xHOVhkKzFLK3FXVUp2eFFqUmVLeXhWSkZsd1NVOGJTSll0VkN2WnZaTlRmbURhbGliY2MzNUpIbEl0bE92d1ZZVkJTRzU4MFZrMG9CT254cHV3MFdGbWJtejRjam9IVlF0S05BZGpCOW9ieUFob1R6elE1enpDSmhnc042SWE5MDVobDZXWlN3WHRwSzFlOEVmd2ZzUnNpcXBIeEJQQ2MwOVo2Q2hBN1lOU1FoVFdlIiwibCI6Imh0dHBzOi8vbmV3YXNzZXRzLmhjYXB0Y2hhLmNvbS9jL2Y5MjJhNDEiLCJpIjoic2hhMjU2LVF0bWtBUnJEYXVTRDZPUExTN0t6Z3B1V3Z6WnJ2QndPS3JRTlRYM3Jra0E9IiwiZSI6MTcxNTYxNjY4MiwibiI6ImhzdyIsImMiOjEwMDB9.kO00qLSV_ogCVPzD5JnorvbSLyjU7gBHdtXhKgFdBuQ\")")
    
    raw_events=page.evaluate("get_events()")
    hashed_events=decrypt(response)["events"]
    

def hash(data:str) -> str:
    return str(xxhash.xxh64(json.dumps(data, separators=(",", ":")), seed=5575352424011909552).intdigest())

def hash_compare(data:str) -> any:
    for event in raw_events:
        if data==hash(event):
            return event

for event in hashed_events:
    try:
        int(event[1])
        if len(event[1])>5:
            print(Fore.YELLOW+"event: "+str(event))
            result=hash_compare(event[1])
            print(f"{Fore.LIGHTGREEN_EX}result: {str(result)[0:100]} .....")
            with open(f"{event[0]}.txt","w") as file:
                file.write(str(result))
    except:
        pass

with open("hashed events.txt","w") as file:
    file.write(str(json.dumps(hashed_events, indent=4)))
    
input()