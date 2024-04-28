import concurrent.futures
import colorama
from hcap_solver import Hcaptcha

colorama.init()

def solve_captcha():
    return Hcaptcha(
        site_key='4c672d35-0701-42b2-88c3-78380b0db560',
        host='https://discord.com/', 
        proxy="eo5lyn59sw99xcb:w8081b0cy1g9321@rp.proxyscrape.com:6060"
    ).solve()


def main():
 print(solve_captcha())

if __name__ == "__main__":
    solve_captcha()
