import websocket, threading, json, tls_client, random, string, time
from decimal import Decimal

messages_recived=[]

class get_ws_messages(websocket.WebSocketApp):
    def __init__(self, token):
        self.packets_recv = 0
        self.message: dict = {}
        self.token = token
        self.open = False
        self.create_id = None

        self.socket_headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9013 Chrome/108.0.5359.215 Electron/22.3.2 Safari/537.36"
        }
        super().__init__(
            "wss://gateway.discord.gg/?encoding=json&v=9",
            header=self.socket_headers,
            on_open=lambda ws: self.sock_open(ws),
            on_message=lambda ws, msg: self.sock_message(ws, msg)
        )
        
    def run(self) -> dict:
        self.run_forever()
        
    def sock_open(self, ws):
self.send(
            '{"op":2,"d":{"token":"'
            + self.token
            + '","capabilities":125,"properties":{"os":"Windows","browser":"Firefox","device":"","system_locale":"sv-SE","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0","browser_version":"94.0","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":103981,"client_event_source":null},"presence":{"status":"online","since":0,"activities":[],"afk":false},"compress":false,"client_state":{"guild_hashes":{},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1}}}'
        )

    def sock_message(self, ws, message):
        decoded = json.loads(message)
        messages_recived.append(decoded)
        
    def sock_close(self, ws, close_code, close_msg):
        pass

class Pandez():
    def __init__(self, token, msg_link) -> None:
        self.token=token
        self.bot_id="967155551211491438"

        self.t = get_ws_messages(self.token)
        self.thread = threading.Thread(target=self.t.run)
        self.thread.start()

        _,_,_,_, self.guild_id, self.channel_id, self.message_id = msg_link.split("/")

        self.session=tls_client.Session(
            client_identifier="chrome_114",
            random_tls_extension_order=True
        )

        self.session.headers = {
            'authorization': token,
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InN2LVNFIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE1LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjIxODYwNCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
        }

        self.session_id=self.Random_string(32)

    def Random_string(self, length:int) -> str:
        return ''.join(random.sample(string.ascii_letters+string.digits,length))

    def Nonce(self) -> str:
        return str(round(Decimal(time.time()*1000-1420070400000)*4194304))

    def bypass(self) -> None:
        self.click(msg_id=self.message_id, button="verify")
        print("clicked verify")

        for message in messages_recived:
            if "message_reference" in str(message):
                msg_id2=message["d"]["id"]

        self.click(msg_id=msg_id2, button="turnOffDMContinue", flags=64)
        print("clicked turnOffDMContinue")

        for message in messages_recived:
            print(message)
            if "agree to the server rules" in str(message):
                msg_id3=message["d"]["id"]

        self.click(msg_id=msg_id3, button="readRulesContinue",flags=64)
        print("clicked readRulesContinue")

        for message in messages_recived:
            print(message)
            if "enter the green numbers" in str(message).lower():
                msg_id4=message["d"]["id"]
                captcha_url=message["d"]["embeds"][0]["image"]["url"]

        print(captcha_url)
        answer=input("answer: ")

        print("entering answer")
        for number in answer:
            self.click(msg_id=msg_id4,button=number,flags=64)  

        self.t.close()
        self.thread.join()

        print("done")

    def click(self, msg_id:str, button:str, flags:int=0) -> None:
        result=self.session.post("https://discord.com/api/v9/interactions",json={
            "type": 3,
            "nonce": self.Nonce(),
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_flags": flags,
            "message_id": msg_id,
            "application_id": self.bot_id,
            "session_id": self.session_id,
            "data": {
                "component_type": 2,
                "custom_id": button
            }
        })

        if not result.status_code==204:
            print(result.text)

        time.sleep(4)

Pandez(
    token="MTA4NTczNTk2MzA2MzQ5MjYyOA.GeDRNH.GBStJWBr-kf74oBM9ncVLhdlcbEsL0k_LwTFtw",
    msg_link="https://discord.com/channels/1171140028135641198/1218592244353859676/1218592247004532898"
).bypass()