import concurrent.futures
from hcap_solver import Hcaptcha 

print(Hcaptcha(
            sitekey='4c672d35-0701-42b2-88c3-78380b0db560',
            host='discord.com', 
            proxy="dh43s5s47s88z7j:q62urbozsi7ifd9@rp.proxyscrape.com:6060"
        ).solve())