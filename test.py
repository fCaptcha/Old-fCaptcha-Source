from hcap_solver import *

g =Hcaptcha(
    site_key="4c672d35-0701-42b2-88c3-78380b0db560",
    host="discord.com",
    proxy=f"user-10014101_25-country-US-session-636321:Mt0mdR7aLHOL5@geo.iproyal.vip:8888",
).solve()

print(g)