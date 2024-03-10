import random, string, json, base64, requests, re, hashlib, math
from time import time
from bs4 import BeautifulSoup
from random import randint as r

class HSW:
    def __init__(self) -> None:
        self.ardata=self.get_ardata()
        self.time=str(int(time()))
        self.canvas_hash=str(random.randint(1000000000000000000,9999999999999999999))
        self.parent_win_hash=str(random.randint(10000000000000000000,99999999999999999999))
        self.common_keys_hash=random.randint(1000000000,9999999999)
        self.thing=f"[0,2,4,5,6,8,9,{str(r(10,12))},13,15,{str(r(16,17))},18,19,{str(r(20,21))},22,23,{str(r(26,28))},29,30,31,{str(r(32,33))},34,35,{str(r(36,37))},39,{str(r(40,45))},47,48,{str(r(49,65))},66,67,69,71,72,{str(r(73,75))},76,77,78,79,81,82],[0,0,0,0,{str(r(10,20))},{str(r(1,17))},0]]"

    def make_stamp(self, resource, bits=2, now=None, ext='', salt_chars=8) -> str:
        timestamp = "2024-03-09"
        challenge = f"1:{bits}:{timestamp}:{resource}:{ext}:{self._get_salt(salt_chars)}:"
        return challenge + self._mint_stamp(challenge, bits)

    def _get_salt(self, data_in) -> str:
        charset = string.ascii_letters + "+/="
        return ''.join([random.choice(charset) for _ in [None] * data_in])

    def _mint_stamp(self, challenge, bits) -> str:
        counter = 0
        hex_digits = int(math.ceil(bits / 4.0))
        zeros = '0' * hex_digits
        while 1:
            digest = hashlib.sha1((challenge + hex(counter)[2:]).encode()).hexdigest()
            if digest[:hex_digits] == zeros:
                return hex(counter)[2:]
            counter += 1

    def decrypt(self, data) -> str:
        return requests.post("http://solver.dexv.lol:1500/decrypt", json={
            "data": data,
            "key": "realasffrfr10384"
        }).text

    def encrypt(self, data) -> str:
        return requests.post("http://solver.dexv.lol:1500/encrypt", json={
            "data": data,
            "key": "realasffrfr10384"
        }).text

    def random_string(self, length:int) -> str:
        return ''.join(random.sample((string.ascii_letters+string.digits)*10, length))

    def random_float(self) -> float:
        return random.uniform(0.0000000000000001,0.9999999999999999)

    def randomize_list(self, things:list) -> str:
        random.shuffle(things)
        return ",".join(things)

    def get_ardata(self) -> str:
        r = requests.get("https://newassets.hcaptcha.com/captcha/v1/fadb9c6/static/hcaptcha.html?_v=n2igxf14d2i")
        soup = BeautifulSoup(r.text, 'html.parser')
        tag = soup.find('script', {'src': re.compile(r'hcaptcha\.js#i=')})
        ardata = tag['src'].split('#i=')[1]
        return ardata

    def decode_req_token(self, req:str) -> str:
        _,part,_ = req.split(".")

        return json.loads(base64.b64decode((part+"==").encode()).decode())

    def random13(self):
        return ''.join(random.sample(string.ascii_uppercase,13))

    def make_get_hsw(self, req:str) -> str:
        data=self.decode_req_token(req)
        events=[[1499802123,"[\"Windows\",\"10.0.0\",null,\"64\",\"x86\",\"122.0.6261.95\"]"],[4122073669,"57"],[3011284755,"1779.2999999523163"],[1370757769,"85.69999998807907"],[561957708,"[\"Europe/Stockholm\",-60,-60,-3203646808000,\"centraleuropeisk normaltid\",\"sv\"]"],[2611063157,"true"],[2098392812,"[3440,1440,3440,1400,24,24,false,0,1,1705,856,true,true,true,false]"],[3427494050,"3313549113868922289"],[553071129,"8808183120261983913"],[1301092348,"[4,120,4]"],[2952842224,"17974846415965634345"],[284488784,f"[[57,[57,57,57,255,57,57,57,255,57,57,57,255,57,57,57,255]],[[11,0,0,95.96875,15,4,96.765625],[[12,0,-1,113.125,17,4,113],[11,0,0,111,12,4,111],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[12,0,0,109.640625,14,3,110.1953125]]],{self.thing}"],[3277268589,"[0,10465,10465]"],[3642958270,"4932383211497360507"],[403765066,"[\"Google Inc. (NVIDIA)\",\"ANGLE (NVIDIA, NVIDIA GeForce RTX 3070 (0x00002484) Direct3D11 vs_5_0 ps_5_0, D3D11)\"]"],[767375397,"13177607191192652685"],[1526063983,"[16,4095,30,16,16380,120,12,120,[23,127,127]]"],[4106644958,"16153807394097295248"],[1993690389,"[\"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36\",\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36\",8,16,\"sv-SE\",[\"sv-SE\",\"sv\",\"en-US\",\"en\"],\"Win32\",null,[\"Chromium 122\",\"Not(A:Brand 24\",\"Google Chrome 122\"],false,\"Windows\",2,5,true,false,100,false,false,true,\"[object Keyboard]\",false,false]"],[2596966448,"\"Europe/Stockholm\""],[1304795084,self.time],[224944468,"[1,1024,1,1,4]"],[1699873298,"16981507572126021743"],[1216692676,"31.299999952316284"],[3082807950,"[\"bXZGjtjtR3BJTGAvxwBFVncv\",\"1a\",\"5\",\"SQOOSAWBTKEJQ\"]"],[603870060,"15307345790125003576"],[4035552665,"[[\"CVRS1KUklcMYUiU3xmLwITJqHhEwVnBO\",\"9\",\"1\",\"HQECOOBZYEKYD\"],[\"V0VFZNJHDWitJdTewthFuWitJom0SYnFwqnkmlajmla1qwFeVtnzuxetKWitJlh2X18FmdJtJWitJrh2X18FmWitJth3Z0JXAzmVmxajmlgCmTbdmWajm0gdnPajmlmdm3admyuyRJ1emyuI\",\"f\",\"5f\",\"MAENWIPQUBETD\"]]"],[576381132,"[32767,32767,16384,8,8,8]"],[506504373,"4631229088072584217"],[1928955012,"[1,4,5,7,9,12,20,21,23,25,29,32]"],[1881216048,"[2147483647,2147483647,4294967294]"],[2670975532,"[[true,\"sv-SE\",true,\"Microsoft Bengt - Swedish\",\"Microsoft Bengt - Swedish\"],[false,\"de-DE\",false,\"Google Deutsch\",\"Google Deutsch\"],[false,\"en-US\",false,\"Google US English\",\"Google US English\"]]"],[943669038,"[[277114314453,277114314460,277114314451,357114314456,277114314452,554228628898,57114314443,717114314371391,554228628897,277114314456,1108457257862,277114314450,554228628919,277114314460,277114314451],false]"],[1213335269,"[[\"navigation:newassets.hcaptcha.com\",80.70000004768372,111],[\"script:newassets.hcaptcha.com\",28.69999998807907,52.099999994039536],[\"xmlhttprequest:api2.hcaptcha.com\",0,199.39999997615814]]"],[308248000,f"[[[\"https://newassets.hcaptcha.com/captcha/v1/fadb9c6/hcaptcha.js#i={self.ardata}\",0,5],[[\"*\",84,9]]]"],[4257244769,"[16,1024,4096,7,12,120,[23,127,127]]"],[2578092907,"2337666753322697468"],[1019165209,"9912002456075893955"],[3837470343,"[1,2,3,4]"],[1329850757,"[-6.172840118408203,-20.710678100585938,120.71067810058594,-20.710678100585938,141.42135620117188,120.71067810058594,-20.710678100585938,141.42135620117188,-20.710678100585938,-20.710678100585938,0,0,300,150,false]"],[3182929905,"1121"],[3571348344,"629"],[1825909650,"[[\"loadTimes\",\"csi\",\"app\"],35,34,null,false,false,true,37,true,true,true,true,true,[\"Raven\",\"_sharedLibs\",\"hsw\",\"__wdata\"],[[\"getElementsByClassName\",[]],[\"getElementById\",[]],[\"querySelector\",[]],[\"querySelectorAll\",[]]],[],true]"],[1059429151,"[2147483647,2147483647,2147483647,2147483647]"],[586079477,"22.100000023841858"],[2143466793,"[614106279936,614106279936,null,null,4294705152,true,true,true,null]"],[2454601770,"[24,24,65536,212988,200704]"],[2779210117,"9345374751420407194"],[434050150,"[\"jn2eDnxAjnYctO5m\",\"b\",\"e\",\"SNZYTEKMUPMYE\"]"],[2117410547,"[16]"],[2079951407,"[16384,32,16384,2048,2,2048]"],[2762634007,"7585258433303263092"]]
        random.shuffle(events)
        unique_keys=self.randomize_list(["objectFitPolyfill","Optanon","regeneratorRuntime","OptanonActiveGroups","2","OneTrustStub","onYTReady","0","pageUsesReact","scriptUrl","platform","OnetrustActiveGroups","initDownloadButton","tram","hcaptcha","hcaptchaOnLoad","initLogInOrOpenDiscordButton","gaGlobal","_","WebFont","OneTrust","core","__skippedLocalizeInit","YT","$","webpackChunkdiscord_marketing","clearImmediate","initSignUpOrOpenButtons","grecaptcha","dataLayer","Webflow","GLOBAL_ENV","setImmediate","otStubData","1","ttPolicy","IntlPolyfill","onYouTubeIframeAPIReady","YTConfig","google_tag_manager","jQuery","google_tag_data","_babelPolyfill","Localize"])
        inv_unique_keys=self.randomize_list(["__wdata","sessionStorage","localStorage","hsw","_sharedLibs"])
        stamp=self.make_stamp(data['d'], data['s'])

        return self.encrypt(str(json.dumps({"proof_spec":{"difficulty":2,"fingerprint_type":0,"_type":"w","data":data["d"],"_location":data["l"],"timeout_value":1000.0},"rand":[self.random_float(),self.random_float()],"components":{"navigator":{"user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36","language":"sv-SE","languages":["sv-SE","sv","en-US","en"],"platform":"Win32","max_touch_points":0,"webdriver":False,"notification_query_permission":None,"plugins_undefined":False},"screen":{"color_depth":24,"pixel_depth":24,"width":3440,"height":1440,"avail_width":3440,"avail_height":1400},"device_pixel_ratio":1.0,"has_session_storage":True,"has_local_storage":True,"has_indexed_db":True,"web_gl_hash":"-1","canvas_hash":self.canvas_hash,"has_touch":False,"notification_api_permission":"Denied","chrome":True,"to_string_length":33,"err_firefox":None,"r_bot_score":0,"r_bot_score_suspicious_keys":[],"r_bot_score_2":0,"audio_hash":"-1","extensions":[False],"parent_win_hash":self.parent_win_hash,"webrtc_hash":"-1","performance_hash":str(random.randint(10000000000000000000,99999999999999999999)),"unique_keys":unique_keys,"inv_unique_keys":inv_unique_keys,"common_keys_hash":self.common_keys_hash,"common_keys_tail":"webkitCancelAnimationFrame,webkitRequestAnimationFrame,chrome,caches,cookieStore,ondevicemotion,ondeviceorientation,ondeviceorientationabsolute,launchQueue,documentPictureInPicture,getScreenDetails,queryLocalFonts,showDirectoryPicker,showOpenFilePicker,showSaveFilePicker,originAgentCluster,credentialless,speechSynthesis,onscrollend,webkitRequestFileSystem,webkitResolveLocalFileSystemURL,Raven","features":{"performance_entries":True,"web_audio":True,"web_rtc":False,"canvas_2d":True,"fetch":True}},"events":events,"suspicious_events":[],"messages":None,"stack_data":None,"stamp":stamp,"href":"https://discord.com/","ardata":self.ardata,"errs":{"list":[]},"perf":[[1,4.0],[2,25.0],[3,0.0]]})))

    def make_post_hsw(self, req:str) -> str:
        data=self.decode_req_token(req)
        events=[[2143466793,"[614106279936,614106279936,null,null,4294705152,true,true,true,null]"],[2117410547,"[16]"],[586079477,"26.799999952316284"],[1928955012,"[1,4,5,7,9,12,20,21,23,25,29,32]"],[4035552665,"[[\"LCmYUSSuNMlWItJH92bnXwZO4kvJRUSB\",\"1a\",\"9\",\"VLOGEMEYTAWAX\"],[\"etZRvWRnkmlAjmleFRXJUvUnDvxetKwitJMl2X18FmDJtJwitJsl2X18FmwitJUlha1nNazqvmxAjmlgCmuBDmwAjm0gDnPAjmlmDm3ADmyUCSK5emyUyv1ZvZonXdwitJexUWUlvUwitJoq\",\"10\",\"7a\",\"MTMQPNIIVNEHQ\"]]"],[1301092348,"[4,120,4]"],[1499802123,"[\"Windows\",\"10.0.0\",null,\"64\",\"x86\",\"122.0.6261.95\"]"],[767375397,"13177607191192652685"],[943669038,"[[277114314453,277114314460,277114314451,357114314456,277114314452,554228628898,57114314443,717114314371391,554228628897,277114314456,1108457257862,277114314450,554228628919,277114314460,277114314451],false]"],[1881216048,"[2147483647,2147483647,4294967294]"],[2454601770,"[24,24,65536,212988,200704]"],[4106644958,"16153807394097295248"],[2611063157,"true"],[1304795084,self.time],[2596966448,"\"Europe/Stockholm\""],[1993690389,"[\"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36\",\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36\",8,16,\"sv-SE\",[\"sv-SE\",\"sv\",\"en-US\",\"en\"],\"Win32\",null,[\"Chromium 122\",\"Not(A:Brand 24\",\"Google Chrome 122\"],false,\"Windows\",2,5,true,false,100,false,false,true,\"[object Keyboard]\",false,false]"],[3182929905,"1121"],[1216692676,"28.69999998807907"],[603870060,"15307345790125003576"],[3082807950,"[\"y9GCIHXDynhAGJtJWDNCm52A\",\"3\",\"14\",\"NAFBTCPDCNHEB\"]"],[576381132,"[32767,32767,16384,8,8,8]"],[2762634007,"7585258433303263092"],[1825909650,"[[\"loadTimes\",\"csi\",\"app\"],35,34,null,false,false,true,37,true,true,true,true,true,[\"Raven\",\"_sharedLibs\",\"hsw\",\"__wdata\",\"image_label_area_select\"],[[\"getElementsByClassName\",[]],[\"getElementById\",[]],[\"querySelector\",[]],[\"querySelectorAll\",[]]],[],true]"],[3642958270,"4932383211497360507"],[224944468,"[1,1024,1,1,4]"],[2098392812,"[3440,1440,3440,1400,24,24,false,0,1,1705,856,true,true,true,false]"],[553071129,"8808183120261983913"],[4257244769,"[16,1024,4096,7,12,120,[23,127,127]]"],[2779210117,"9345374751420407194"],[403765066,"[\"Google Inc. (NVIDIA)\",\"ANGLE (NVIDIA, NVIDIA GeForce RTX 3070 (0x00002484) Direct3D11 vs_5_0 ps_5_0, D3D11)\"]"],[308248000,f"[[[\"https://newassets.hcaptcha.com/captcha/v1/fadb9c6/hcaptcha.js#i={self.ardata}\",0,5],[[\"*\",84,9]]]"],[506504373,"4631229088072584217"],[3277268589,"[1504.3428571428572,13233,13163]"],[2952842224,"17974846415965634345"],[1019165209,"1571873144550830076"],[2079951407,"[16384,32,16384,2048,2,2048]"],[1329850757,"[-6.172840118408203,-20.710678100585938,120.71067810058594,-20.710678100585938,141.42135620117188,120.71067810058594,-20.710678100585938,141.42135620117188,-20.710678100585938,-20.710678100585938,0,0,520,580,true]"],[3011284755,"13291.899999976158"],[1213335269,"[[\"img:imgs.hcaptcha.com\",0,99.34999999403954],[\"navigation:newassets.hcaptcha.com\",80.70000004768372,111],[\"script:newassets.hcaptcha.com\",26.100000023841858,43.80000001192093],[\"xmlhttprequest:api.hcaptcha.com\",0,356],[\"xmlhttprequest:api2.hcaptcha.com\",0,199.39999997615814]]"],[1370757769,"85.69999998807907"],[561957708,"[\"Europe/Stockholm\",-60,-60,-3203646808000,\"centraleuropeisk normaltid\",\"sv\"]"],[3837470343,"[1,2,3,4]"],[4122073669,"57"],[2670975532,"[[true,\"sv-SE\",true,\"Microsoft Bengt - Swedish\",\"Microsoft Bengt - Swedish\"],[false,\"de-DE\",false,\"Google Deutsch\",\"Google Deutsch\"],[false,\"en-US\",false,\"Google US English\",\"Google US English\"]]"],[3427494050,"3313549113868922289"],[1526063983,"[16,4095,30,16,16380,120,12,120,[23,127,127]]"],[1059429151,"[2147483647,2147483647,2147483647,2147483647]"],[284488784,f"[[203,[203,203,203,255,203,203,203,255,203,203,203,255,203,203,203,255]],[[11,0,0,95.96875,15,4,96.765625],[[12,0,-1,113.125,17,4,113],[11,0,0,111,12,4,111],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[11,0,0,95.96875,15,4,96.765625],[12,0,0,109.640625,14,3,110.1953125]]],{self.thing}"],[1699873298,"16981507572126021743"],[434050150,"[\"JNycTO5MJN2EDNXA\",\"a\",\"6\",\"SXVJIBKRGHJGL\"]"],[2578092907,"2337666753322697468"],[3571348344,"629"]]
        random.shuffle(events)
        unique_keys=self.randomize_list(["otStubData","dataLayer","initDownloadButton","ttPolicy","tram","GLOBAL_ENV","Localize","initSignUpOrOpenButtons","0","_","Webflow","OptanonActiveGroups","WebFont","hcaptcha","gaGlobal","google_tag_data","IntlPolyfill","OnetrustActiveGroups","onYouTubeIframeAPIReady","webpackChunkdiscord_marketing","grecaptcha","2","OneTrust","__skippedLocalizeInit","google_tag_manager","1","hcaptchaOnLoad","clearImmediate","setImmediate","_babelPolyfill","initLogInOrOpenDiscordButton","YTConfig","Optanon","$","onYTReady","pageUsesReact","scriptUrl","objectFitPolyfill","OneTrustStub","regeneratorRuntime","jQuery","platform","YT","core"])
        inv_unique_keys=self.randomize_list(["image_label_area_select","sessionStorage","hsw","__wdata","_sharedLibs","localStorage"])
        stamp=self.make_stamp(data['d'], data['s'])

        return self.encrypt(str(json.dumps({"proof_spec":{"difficulty":2,"fingerprint_type":0,"_type":"w","data":data["d"],"_location":data["l"],"timeout_value":1000.0},"rand":[self.random_float(),self.random_float()],"components":{"navigator":{"user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36","language":"sv-SE","languages":["sv-SE","sv","en-US","en"],"platform":"Win32","max_touch_points":0,"webdriver":False,"notification_query_permission":None,"plugins_undefined":False},"screen":{"color_depth":24,"pixel_depth":24,"width":3440,"height":1440,"avail_width":3440,"avail_height":1400},"device_pixel_ratio":1.0,"has_session_storage":True,"has_local_storage":True,"has_indexed_db":True,"web_gl_hash":"-1","canvas_hash":self.canvas_hash,"has_touch":False,"notification_api_permission":"Denied","chrome":True,"to_string_length":33,"err_firefox":None,"r_bot_score":0,"r_bot_score_suspicious_keys":[],"r_bot_score_2":0,"audio_hash":"-1","extensions":[False],"parent_win_hash":self.parent_win_hash,"webrtc_hash":"-1","performance_hash":str(random.randint(1000000000000000000,9999999999999999999)),"unique_keys":unique_keys,"inv_unique_keys":inv_unique_keys,"common_keys_hash":self.common_keys_hash,"common_keys_tail":"webkitCancelAnimationFrame,webkitRequestAnimationFrame,chrome,caches,cookieStore,ondevicemotion,ondeviceorientation,ondeviceorientationabsolute,launchQueue,documentPictureInPicture,getScreenDetails,queryLocalFonts,showDirectoryPicker,showOpenFilePicker,showSaveFilePicker,originAgentCluster,credentialless,speechSynthesis,onscrollend,webkitRequestFileSystem,webkitResolveLocalFileSystemURL,Raven","features":{"performance_entries":True,"web_audio":True,"web_rtc":False,"canvas_2d":True,"fetch":True}},"events":events,"suspicious_events":[],"messages":None,"stack_data":["new Promise (<anonymous>)"],"stamp":stamp,"href":"https://discord.com/","ardata":self.ardata,"errs":{"list":[]},"perf":[[1,5.0],[2,30.0],[3,0.0]]})))
    
