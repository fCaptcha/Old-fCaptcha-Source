import bodystuff
import time
import colorama
import requests
from hcap import HCaptchaEnterpriseChallenge, DATABASE

colorama.init()

def solve_captcha():
    bodystuff.logger.info("Solving Captcha")
    start = time.time()
    payload = {
            "api_key": 'DEXV-ADMIN-71BczP-nssbPD-eR61cH',
            "url": 'discord.com',
            "sitekey": '4c672d35-0701-42b2-88c3-78380b0db560',
            "proxy": 'mr34501PeoH:MJm1949SGk@ultra.marsproxies.com:44443',
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
        }
    result = requests.post("http://solver.dexv.lol:1000/api/solve_hcap", json=payload)
    data = result.json()
    if data.get("success"):
            bodystuff.logger.success(f"Solved Captcha {data['message'][:70]}  In {str(time.time() - start)[:5]} Seconds")
            return data['message']
    else:
        bodystuff.logger.error(f"Failed To Solve Captcha -> {data.get('message')}")


def main():
  while True:
    c = solve_captcha()
    r = requests.post("http://localhost:9999/make_token", json={
      "captcha_key": c,
      "proxy": "mr34501PeoH:MJm1949SGk@ultra.marsproxies.com:44443"
      })
    print(r.text)
        
if __name__ == "__main__":
    main()
