import concurrent.futures
from hcap_solver import Hcaptcha 

def solve_captcha():
    while True:
        Hcaptcha(
            site_key='4c672d35-0701-42b2-88c3-78380b0db560',
            host='discord.com', 
            proxy="qapnxywtcwnmbmn38052:bmvgavatiz@prem_resi.turboproxy.in:16666"
        ).solve()

with concurrent.futures.ThreadPoolExecutor() as executor:
    for _ in range(20):
        executor.submit(solve_captcha)