import concurrent.futures
import colorama
from hcap_solver import Hcaptcha

colorama.init()

def solve_captcha():
    return Hcaptcha(
        site_key='4c672d35-0701-42b2-88c3-78380b0db560',
        site_url='https://discord.com/', 
        proxy="http://brd-customer-hl_6ef0caa2-zone-datacenter_proxy1:6p6xamh0a871@brd.superproxy.io:22225"
    ).solve()


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(solve_captcha) for _ in range(20)]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except:
                pass

if __name__ == "__main__":
    main()
