import concurrent.futures
from hcap_solver import Hcaptcha 

def solve_captcha():
    while True:
        Hcaptcha(
            sitekey='4c672d35-0701-42b2-88c3-78380b0db560',
            host='discord.com', 
            proxy="g5hltixerdytvio:g7w9oxoov0b8jsz@rp.proxyscrape.com:6060"
        ).solve()

with concurrent.futures.ThreadPoolExecutor() as executor:
    for _ in range(100):
        executor.submit(solve_captcha)