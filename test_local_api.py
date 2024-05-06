import requests
from hcap_solver import Hcaptcha

def solve_captcha():
    return Hcaptcha(
        site_key='4c672d35-0701-42b2-88c3-78380b0db560',
        host='https://discord.com/', 
        proxy="5ki63yn1tpy0qvc:2zd5osm1wn9ssf1@rp.proxyscrape.com:6060"
    ).solve()


if __name__ == "__main__":
    g = solve_captcha()
    if g:
        requests.post("http://localhost:9999/make_token", json={"captcha_key": g, "proxy": "5ki63yn1tpy0qvc:2zd5osm1wn9ssf1@rp.proxyscrape.com:6060"})
