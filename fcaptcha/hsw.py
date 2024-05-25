import json
import base64
import hashlib
import json
import random
import secrets
import time
from io import BytesIO
from math import ceil
from string import ascii_letters
from time import strftime, localtime
from urllib.parse import quote
from zlib import crc32

import numpy
import tls_client
import xxhash
from redis import Redis

client = tls_client.Session("chrome_104", random_tls_extension_order=True)
database_fps = Redis("45.45.238.213", 42081, 313, "ACCA5B570561DCFA5ACB1417C69F2900DAFF8A4FD39A2E66C36DF2BD796F0BE1CFEA8AF2DB18153874215E08BFDEC4A89A397EC53E52DAC33A1E9D0B17A52D43")
hash_json = lambda x: str(xxhash.xxh64_intdigest(json.dumps(x, separators=(",", ":")), seed=5575352424011909552))


class HSW:
    def __init__(self):
        self.key = database_fps.randomkey()

    @staticmethod
    def encode(input_str: str) -> list:
        h_a, in_arr = 'abcdefghijklmnopqrstuvwxyz', ''.join(chr(random.randint(65, 90)) for _ in range(13))
        rand_a = random.randint(1, 26)
        result = []

        for char in input_str[::-1]:
            if char.isalpha():
                shifted_char = h_a[(h_a.index(char.lower()) + rand_a) % 26]
                result.append(shifted_char.upper() if char.isupper() else shifted_char)
            else:
                result.append(char)

        result = ''.join(result)[::-1]
        b64 = base64.b64encode(quote(result).encode()).decode()[::-1]
        b64rand = random.randint(1, len(b64) - 1)
        b64 = b64[b64rand:] + b64[:b64rand]

        output = [char.lower() if char.isupper() else char.upper() if char in in_arr or char in in_arr.lower() else char
                  for char in b64]

        return [''.join(output), f"{rand_a:x}", f"{b64rand:x}", in_arr]

    @staticmethod
    def decrypt(data: str) -> str:
        url = "http://solver.dexv.lol:1500/decrypt"
        json = {"data": data, "key": "88de30e1c0d0e89d"}
        return client.post(url, json=json).text

    @staticmethod
    def encrypt(data: str) -> str:
        url = "http://solver.dexv.lol:1500/encrypt"
        json = {"data": data, "key": "88de30e1c0d0e89d"}
        return client.post(url, json=json).text

    @staticmethod
    def random_float() -> float:
        return random.uniform(0.0000000000000001, 0.9999999999999999)

    def pull(self, jwt: str, host: str, user_agent: str) -> str | None:
        s = jwt.split(".")[1].encode()
        s += b'=' * (-len(s) % 4)
        parsed = json.loads(base64.b64decode(s, validate=False).decode())
        hc_diff = parsed['s']
        hc_data = parsed['d']
        if data := json.load(open("hsw_types/discord.json", "r")):
            data["stamp"] = self.mint(hc_data, hc_diff)
            data["rand"] = [self.random_float()]
            data["href"] = f"https://{host}"
            data["proof_spec"]["data"] = hc_data
            data["proof_spec"]["difficulty"] = hc_diff
            data["stack_data"] = ["new Promise (<anonymous>)"]
            random.shuffle(data["events"])
            rand = random.randint(1, 254)
            r = [rand, [rand, rand, rand, 255, rand, rand, rand, 255, rand, rand, rand, 255, rand, rand, rand, 255]]
            events = {x: y for x, y in data["events"]}
            gpu_event = json.loads(events.get(1004633796))
            rand_event = json.loads(events.get(3569888996))[0]
            timezone_event = json.loads(events.get(2444897354))
            for event_id, event_value in events.items():
                match event_id:
                    case 2809130260:
                        event_value = json.dumps(self.encode(timezone_event), separators=(",", ":"))
                    case 382530556:
                        event_value = json.dumps(self.encode(str(rand_event)), separators=(",", ":"))
                    case 1303333220:
                        event_value = json.dumps([self.encode(gpu_event[0]), self.encode(gpu_event[1])], separators=(",", ":"))
                    case 1204159645:
                        var0 = json.loads(event_value)
                        var0[0] = r
                        event_value = json.dumps(var0, separators=(",", ":"))
                    case 1022788021:
                        event_value = str(round(time.time() * 1000, 1))
                    case 527778036:
                        event_value = hash_json([
                            [
                                gpu_event[0], gpu_event[1]
                            ],
                            [
                                "EXT_clip_control", "EXT_color_buffer_float", "EXT_color_buffer_half_float",
                                "EXT_conservative_depth", "EXT_depth_clamp", "EXT_disjoint_timer_query_webgl2",
                                "EXT_float_blend", "EXT_polygon_offset_clamp", "EXT_texture_compression_bptc",
                                "EXT_texture_compression_rgtc", "EXT_texture_filter_anisotropic",
                                "EXT_texture_mirror_clamp_to_edge", "EXT_texture_norm16", "KHR_parallel_shader_compile",
                                "NV_shader_noperspective_interpolation", "OES_draw_buffers_indexed",
                                "OES_texture_float_linear", "OVR_multiview2", "WEBGL_blend_func_extended",
                                "WEBGL_clip_cull_distance", "WEBGL_compressed_texture_s3tc",
                                "WEBGL_compressed_texture_s3tc_srgb", "WEBGL_debug_renderer_info",
                                "WEBGL_debug_shaders",
                                "WEBGL_lose_context", "WEBGL_multi_draw", "WEBGL_polygon_mode",
                                "WEBGL_provoking_vertex",
                                "WEBGL_stencil_texturing"
                            ],
                            [
                                [1, 1024],
                                [1, 1],
                                2147483647, 2147483647, 2147483647, 2147483647, 16384, [32767, 32767],
                                4, 16, 4095, 30, 32, 16, 16, 1024,
                                "WebGL GLSL ES 3.00 (OpenGL ES GLSL ES 3.0 Chromium)",
                                "WebKit", "WebKit WebGL", "WebGL 2.0 (OpenGL ES 3.0 Chromium)", 16384, 16384, 2048,
                                2147483647, 2147483647, 2, 8, 4096, 16380, 2048, 7, 120, 4, 120, 4, 8, 8, 12, 12, 24,
                                24,
                                65536, 212988, 200704, 120, 120, 4294967294,
                                [[23, 127, 127], [23, 127, 127], [23, 127, 127], [0, 30, 31]],
                                [[23, 127, 127], [23, 127, 127], [23, 127, 127], [0, 30, 31]], 16, None, True]
                        ])
                events.update({
                    event_id: event_value
                })
            data["events"] = [[x, y] for x, y in events.items()]
            hsw_str = self.encrypt(json.dumps(data, separators=(",", ":")))
            data["rand"].append(numpy.uint32(crc32(hsw_str.encode())) * 2.3283064365386963e-10)
            hsw_str = self.encrypt(json.dumps(data, separators=(",", ":")))
            return hsw_str
        return None

    def mint(self, resource: str, bits: int = 2, ext: str = '', salt_chars: int = 8) -> str:
        timestamp = strftime("%Y-%m-%d", localtime(time.time()))
        challenge = f"1:{bits}:{timestamp}:{resource}:{ext}:{self.get_salt(salt_chars)}:"
        return f"{challenge}{self.mint_stamp(challenge, bits)}"

    @staticmethod
    def get_salt(salt_length: int) -> str:
        charset = ascii_letters + "+/="
        return ''.join([random.choice(charset) for _ in range(salt_length)])

    @staticmethod
    def mint_stamp(challenge: str, bits: int) -> str:
        counter = 0
        hex_digits = int(ceil(bits / 4.0))
        zeros = '0' * hex_digits
        while 1:
            digest = hashlib.sha1((challenge + hex(counter)[2:]).encode()).hexdigest()
            if digest[:hex_digits] == zeros:
                return hex(counter)[2:]
            counter += 1