import re, os, colr, time, json, base64, random, ctypes, logging, requests, threading, websocket, tls_client

from colorama       import Fore
from datetime       import datetime
from pygments       import highlight, lexers, formatters
from os.path        import isfile, join
from flask          import Flask, request, json

class _global:
    port:str=9999
    unlocked:int=0
    locked:int=0
    upm:int=0
    sl:int=0
    errors:int=0
    elapsed:str=""
    result: str=None

    all_pfps = [f for f in os.listdir("data/avatars/") if isfile(join("data/avatars/", f))]
    all_bios = open("data/bios.txt","r", encoding="utf8").read().splitlines()

class information:
    def rate(thing,total):
        try:
            return str(round(thing/total*100,4))
        except:
            return 0

    def calc_upm():
        while True:
            try:
                before=_global.unlocked
                time.sleep(15)
                after=_global.unlocked
                _global.upm = (after-before)*4
            except:
                _global.upm=0

    def title():
        second=0;minute=0;hours=0;days=0

        while True:
            second+=1
            if second == 60: second = 0; minute+=1
            if minute == 60: minute = 0; hours+=1
            if hours == 24:  hours = 0; days+=1

            _global.elapsed=f"{str(days).zfill(2)}:{str(hours).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}"

            ctypes.windll.kernel32.SetConsoleTitleW(f"account creator | unlocked: {str(_global.unlocked)} | locked: {str(_global.locked)} | upm: {str(_global.upm)} | uph: {str(_global.upm*60)} | errors: {str(_global.errors)} | sl: {str(_global.sl)} | unlock rate: {str(information.rate(_global.unlocked,_global.unlocked+_global.locked))} | elapsed: {_global.elapsed}")
            time.sleep(1)

class logger:
    colors_table = {
        "green":"#65fb07",
        "red":"#Fb0707",
        "yellow":"#c4bc18",
        "magenta":"#b207f5",
        "blue":"#001aff",
        "cyan":"#07baf5",
        "grey":"#3a3d40",
        "white":"#ffffff",
        "pink":"#c203fc"
    }

    def convert(color: str):
        if not color.__contains__("#"):
            return logger.colors_table[color]
        else:
            return color

    def color(c: str, obj: str):
        return colr.Colr().hex(logger.convert(c), obj)
    
    def printk(message: str):
        clock=datetime.now().strftime(f"%H:%M:%S")
        print(
            f'{Fore.CYAN}[{clock}]{Fore.RESET} {message}{Fore.RESET}',
            flush=True)
        
    def visualize(objects: list):
        final=[]

        for object in objects:
            before=time.time()
            _function=object["func"]
            _text=object["text"].upper()

            threading.Thread(target=_function).start()

            p_current=time.time()
            dot_speed=2
            current_dot=1

            while not _global.result:
                dots=""

                for i in range(dot_speed*4):
                    if not _global.result:
                        if 1 < time.time()-p_current:
                            print(logger.color(c='white', obj=f"[{_text}]:"), (f"{dots}{' '*(3-len(dots))}"), logger.color(c='white', obj=f"-> {round(time.time()-p_current,3)}s"), end="\r")
                        
                        else:
                            print(logger.color(c='white', obj=f"[{_text}]:"), (f"{dots}{' '*(3-len(dots))}"), end="\r")

                        if dot_speed==current_dot:
                            dots+="."
                            current_dot=1

                        else:
                            current_dot+=1

                        time.sleep(0.1)

            after=time.time()
            print(
                logger.color(c='white', obj=f"[{_text}]:"),
                logger.color(c='green',obj=f"SUCCESS"),
                logger.color(c='magenta',obj=f'(in {str(round(after-before,3))[0:4]}s)'),
                logger.color(c='yellow',obj=f"result: {str(_global.result)}"),
                
                end="\n"
            )

            final.append({
                _text.replace(" ","_"): _global.result
            })

            _global.result=None

        return final

class application:

    @staticmethod
    def native_build() -> int:
        _global.result=int(requests.get(
            "https://updates.discord.com/distributions/app/manifests/latest",
            params={
                "install_id":'0',
                "channel":"stable",
                "platform":"win",
                "arch":"x86"
            },
            headers={
                "user-agent": "Discord-Updater/1",
                "accept-encoding": "gzip"
        }).json()["metadata_version"])

    @staticmethod
    def client_build() -> int:
        page = requests.get("https://discord.com/app").text.split("app-mount")[1]
        assets = re.findall(r'src="/assets/([^"]+)"', page)[::-1]

        for asset in assets:
            js=requests.get(f"https://discord.com/assets/{asset}").text
            
            if "buildNumber:" in js:
                _global.result= int(js.split('buildNumber:"')[1].split('"')[0])
                break

    @staticmethod
    def main_version() -> str:
        app=requests.get(
            "https://discord.com/api/downloads/distributions/app/installers/latest",
            params={
                "channel":"stable",
                "platform":"win",
                "arch":"x86"
            },
            allow_redirects=False
        ).text

        _global.result= re.search(r'x86/(.*?)/', app).group(1)

class discord:
    def __init__(self):
        os.system("cls")
        os.system("title initializing")
        result=logger.visualize(objects=
            [
                {
                    "text": "native build",
                    "func": application.native_build,
                },
                {
                    "text": "main version",
                    "func": application.main_version,
                }, 
                {
                    "text": "client build",
                    "func": application.client_build,
                },
            ],  
        )

        self.native_build=result[0]["NATIVE_BUILD"]
        self.main_version=result[1]["MAIN_VERSION"]
        self.client_build=result[2]["CLIENT_BUILD"]

        self.chrome="108.0.5359.215"
        self.electron="22.3.26"
        self.safari="537.36"
        self.os_version="10.0.19045"

        time.sleep(1.5)

    def xprops(self):
        return base64.b64encode(json.dumps({
            "os":"Windows",
            "browser":"Discord Client",
            "release_channel":"stable",
            "client_version":self.main_version,
            "os_version":self.os_version,
            "os_arch":"x64",
            "app_arch":"ia32",
            "system_locale":"en",
            "browser_user_agent":self.useragent,
            "browser_version":self.electron,
            "client_build_number":self.client_build,
            "native_build_number":self.native_build,
            "client_event_source":None,
            "design_id":0
        }).encode()).decode()

    def get_session(self, proxy):
        session=tls_client.Session(
            client_identifier=f"chrome_108",
            random_tls_extension_order=True
        )

        session.proxies=f"http://{proxy}"
        session.timeout_seconds=60

        self.useragent=f"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/{self.safari} (KHTML, like Gecko) discord/{self.main_version} Chrome/{self.chrome} Electron/{self.electron} Safari/{self.safari}"

        session.headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en,en-US;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.useragent,
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'Europe/Stockholm',
            'x-super-properties': self.xprops()
        }

        session.cookies=session.get("https://discord.com").cookies
        
        return session

class generator:
    def __init__(self, capkey, proxy):
        self.proxy=proxy
        self.capkey=capkey

    def make_pronoune(self):
        pronounces=["her","him","he","it","was","them","his","hers","they","herself","himself","she","themself","myself","were","are","is"]
            
        return '/'.join(random.choice(pronounces) 
            for _ in range(random.randint(2,3))
        )

    def random_pronoune(self):
        try:
            success=self.session.patch(
                "https://discord.com/api/v9/users/%40me/profile",
                json = {
                    "pronouns": self.make_pronoune()
                }
            ).status_code

            if success==200:
                self.added.append("pronounces")

        except:
            pass
        
    def set_online(self):
        try:
            success=self.session.patch(
                "https://discord.com/api/v9/users/@me/settings",
                json = {
                    "status": "online"
                }
            ).status_code

            if success==200:
                self.added.append("online")
        except:
            pass

    def add_pfp(self):
        try:
            with open(f'data/avatars/{random.choice(_global.all_pfps)}', "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            
            success=self.session.patch(
                'https://discord.com/api/v9/users/@me',
                json = {
                    'avatar': f"data:image/png;base64,{(encoded_string.decode('utf-8'))}",
                }
            ).status_code

            if success==200:
                self.added.append("pfp")

        except:
            pass

    def setup_profile(self):
        try:
            banner_color = random.randrange(0, 16**6)

            success=self.session.patch("https://discord.com/api/v9/users/%40me/profile",
                json= {
                    "bio": random.choice(_global.all_bios),
                    "accent_color": banner_color
                }
            ).status_code

            if success==200:
                self.added.append("profile")

        except:
            pass

    def set_birth(self):
        try:
            birth = f"{str(random.randint(1970,2000))}-{str(random.randint(1,12)).zfill(2)}-{str(random.randint(1,23)).zfill(2)}"

            success=self.session.patch("https://discord.com/api/v9/users/@me",
                json= {
                    "date_of_birth": birth
                }
            ).status_code

            if success==200:
                self.added.append("birth")

        except:
            pass

    def hypesquad(self):
        try:
            success=self.session.post("https://discord.com/api/v9/hypesquad/online",
                json= {
                    "house_id": random.randint(1,3)
                }
            ).status_code

            if success==204:
                self.added.append("hypesquad")

        except:
            pass

    def enable_dev(self):
        try:
            success=self.session.patch(
                "https://discord.com/api/v9/users/@me/settings",
                json = {
                    "developer_mode": True
                }
            ).status_code

            if success==200:
                self.added.append("dev")

        except:
            pass

    def check(self, token:str, printl:bool=True):
        req = self.session.get("https://discord.com/api/v9/users/@me/settings")

        t_slice=token.split(".")
        hidden_token=f"{t_slice[0][:-5]}{'¤'*5}.{t_slice[1][:-1]}¤.{t_slice[2][:-5]}{'¤'*5}"

        if req.status_code == 200:
            if printl:
                logger.printk(f"{logger.color('green',obj=f'UNLOCKED {hidden_token}')} ")
                _global.unlocked+=1

            return "unlocked"
        
        if req.status_code == 403:
            if printl:
                logger.printk(f"{logger.color('yellow',obj=f'LOCKED {token}')} ")
                _global.locked+=1

            return "locked"

        elif req.status_code==401:
            if printl:
                logger.printk(f"{logger.color('red',obj=f'INVALID {token}')} ")
                
            return "invalid"

    def Register(self):
        return self.session.post(
            "https://discord.com/api/v9/auth/register",
            json={
                "consent": True,
                "fingerprint": self.fingerprint,
                "gift_code_sku_id": None,
                "captcha_key": self.capkey,
                "global_name": self.username,
                "unique_username_registration": True
            }).json()

    def Online(self):
        ws = websocket.WebSocket()
        
        proxy = self.proxy.split("@")
        username, password, host, port = proxy[0].split(":")[0], proxy[0].split(":")[1], proxy[1].split(":")[0], proxy[1].split(":")[1]

        ws.connect("wss://gateway.discord.gg/?v=9&encoding=json",
            http_proxy_host=host,
            http_proxy_port=str(port),
            proxy_type="http",
            http_proxy_auth=(username,password),
            timeout=10000
        )

        time.sleep(2)

        ws.send(json.dumps({"op":2,"d":{"token":self.token,"properties":{"$os":"Discord iOS","$browser":"Discord iOS","$device":"Discord iOS"}},"s":None,"t":None}))
        payload = json.dumps({"op": 3,"d": {"since": 0,"activities": [],"status": "online","afk": False}})
        ws.send(payload)

        if not ws.connected:
            return self.Online()

        return ws

    def Make_token(self): 
        self.session=self_discord.get_session(self.proxy)
        self.fingerprint=self.session.get("https://discord.com/api/v9/experiments").json()["fingerprint"]
        self.username=random.choice(open("data/usernames.txt",encoding = "utf-8").read().splitlines())

        self.session.headers.update({
            "X-Fingerprint": self.fingerprint
        })

        logger.printk(f"{logger.color('blue',obj='Fingerprint:')} {logger.color('magenta',obj=self.fingerprint)}")

        ###self.session.headers.update({"x-captcha-key":self.capkey})
        register_result=self.Register()
        #del self.session.headers["x-captcha-key"]
        
        if register_result.get("token"):
            self.token=register_result["token"]

            del self.session.headers["X-Fingerprint"]
            self.session.headers.update({
                "authorization": self.token
            })

            self.added=list()

            if self.check(self.token)=="unlocked":
                ws=self.Online()

                self.set_birth()
                self.add_pfp()
                self.set_online()
                self.setup_profile()
                self.hypesquad()
                self.enable_dev()
                self.random_pronoune()

                d = json.dumps({"added":self.added})
                logger.printk(highlight(d, lexers.JsonLexer(), formatters.TerminalFormatter())[:-1])

                time.sleep(10)
                if self.check(self.token,printl=False) =="unlocked":
                    with open("unclaimed.txt","a+") as file:
                        file.write(self.token+"\n")

                else:
                    logger.printk(logger.color('blue',obj=f"SILENT LOCK {self.token}"))
                    _global.sl+=1

                ws.close()

        else:
            _global.errors+=1

self_discord=discord()

def setup():
    os.system("cls")
    threading.Thread(target=information.calc_upm).start()

    app = Flask(__name__)

    @app.route('/make_token', methods = ["POST"])
    def make():
        j = request.get_json()

        function=generator(j["captcha_key"], j["proxy"]).Make_token
        threading.Thread(target=function).start()

        return "ok"

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=_global.port, debug=False, use_reloader=False)).start()

    time.sleep(0.5)
    os.system("cls")
    
    print(f"""
{Fore.LIGHTWHITE_EX}{' '*3}    ___                      
{Fore.LIGHTWHITE_EX}{' '*3}   / _ \___ ____ ___ ___ ____    [NATIVE]: {logger.color('blue',obj=str(self_discord.native_build))}
{Fore.LIGHTWHITE_EX}{' '*3}  / // / _ `/_ // -_) -_) __/    [CLIENT]: {logger.color('blue',obj=str(self_discord.client_build))}
{Fore.LIGHTWHITE_EX}{' '*3} /____/\_,_//__/\__/\__/_/       [MAIN V]: {logger.color('blue',obj=str(self_discord.main_version))}
"""+Fore.RESET)

    threading.Thread(target=information.title).start()
    print()

if __name__=="__main__":
    setup()