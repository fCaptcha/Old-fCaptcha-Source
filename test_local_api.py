import concurrent.futures
import colorama
from hcap_solver import Hcaptcha

colorama.init()

def solve_captcha():
    return Hcaptcha(
        site_key='4c672d35-0701-42b2-88c3-78380b0db560',
        host='https://discord.com/', 
        proxy="brd-customer-hl_6ef0caa2-zone-datacenter_proxy1:6p6xamh0a871@brd.superproxy.io:22225"
    ).solve()


def main():
 print(solve_captcha())

if __name__ == "__main__":
    main()
