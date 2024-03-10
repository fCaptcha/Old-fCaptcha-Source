import concurrent.futures
from hcap_solver import Hcaptcha 

def fire():
    while True:
        Hcaptcha(
                    sitekey='4c672d35-0701-42b2-88c3-78380b0db560',
                    host='discord.com', 
                    proxy="dh43s5s47s88z7j:q62urbozsi7ifd9@rp.proxyscrape.com:6060"
                ).solve()
    
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    for i in range(100):
        executor.submit(fire)