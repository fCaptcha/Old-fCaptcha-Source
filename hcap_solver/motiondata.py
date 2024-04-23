import numpy as np
from scipy import interpolate
import random
import math
import time
import string

class util:
    @staticmethod
    def randint(a: int, b: int) -> int:
        return random.randint(min(a, b), max(a, b))

    @staticmethod
    def get_ms():
        return int(time.time() * 1000)

    @staticmethod
    def get_mm(start: tuple, goal: tuple, screen_size: tuple, max_points: int, random_amount: int, polling_rate: int) -> list:
        cp = util.randint(3, 5)
        x, y = np.linspace(start[0], goal[0], num=cp, dtype='int'), np.linspace(start[1], goal[1], num=cp, dtype='int')
        r = [util.randint(-random_amount, random_amount) for _ in range(cp)]
        x += np.clip(r, 0, screen_size[0])
        y += np.clip(r, 0, screen_size[1])
        tck, _ = interpolate.splprep((x, y), k=3 if cp > 3 else cp - 1)
        u = np.linspace(0, 1, num=min(
            2 + int(math.sqrt((goal[0] - start[0]) ** 2 + (goal[1] - start[1]) ** 2) / polling_rate), max_points))
        points = interpolate.splev(u, tck)
        return [[int(x), int(y), util.get_ms()] for x, y in zip(*(i.astype(int) for i in points)) if
                time.sleep(1 / util.randint(80, 240)) is None]

    @staticmethod
    def periods(timestamps: list) -> float:
        periods = [timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]
        return sum(periods) / len(periods) if periods else 0

    @staticmethod
    def distance(a: tuple, b: tuple) -> float:
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    @staticmethod
    def get_random_point(bbox: tuple) -> tuple:
        return util.randint(bbox[0][0], bbox[1][0]), util.randint(bbox[0][1], bbox[1][1])

    @staticmethod
    def get_center(bbox: tuple) -> tuple:
        x1, y1 = bbox[0]
        x2, y2 = bbox[1]

        return int(x1 + (x2 - x1) / 2), int(y1 + (y2 - y1) / 2)

    @staticmethod
    def convert_answers(answers: dict) -> dict:
        answers = list(answers.values()) if isinstance(answers, dict) else answers
        result = {}
        for i, answer in enumerate(answers):
            result[i] = answer.lower() == 'true' if isinstance(answer, str) else answer
        return result

class rectangle:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def get_dimensions(self) -> tuple:
        return self.width, self.height

    def get_box(self, rel_x: int, rel_y: int) -> tuple:
        return (rel_x, rel_y), (rel_x + self.width, rel_y + self.height)

    def get_corners(self, rel_x: int = 0, rel_y: int = 0) -> list:
        return [(rel_x, rel_y), (rel_x + self.width, rel_y), (rel_x, rel_y + self.height),
                (rel_x + self.width, rel_y + self.height)]

class widget_check:
    def __init__(self, rel_position: tuple) -> None:
        self.widget = rectangle(300, 75)
        self.check_box = rectangle(28, 28)
        self.rel_position = rel_position

    def get_check(self) -> tuple:
        return self.check_box.get_box(16 + self.rel_position[0], 23 + self.rel_position[1])

    def get_closest(self, position: tuple) -> tuple:
        corners = self.widget.get_corners(self.rel_position[0], self.rel_position[1])
        sorted_corners = sorted(corners, key=lambda c: util.distance(position, c))
        return sorted_corners[0], sorted_corners[1]

class binary_challenge:
    def __init__(self, box_centre: tuple, screen_size: tuple) -> None:
        x = min(screen_size[0] / 2 - 200, box_centre[0] + 25)
        y = max(10, min(screen_size[1] - 610, box_centre[1] - 300))

        self.widget_position = x, y
        self.widget = rectangle(400, 600)
        self.button = rectangle(80, 35)
        self.image = rectangle(120, 120)
        self.images = {str(i): ((i % 3) * 130 + 10, (i // 3) * 130 + 130) for i in range(9)}

    def get_image_box(self, index: int) -> tuple:
        index = index % 9
        x, y = self.images.get(str(index))
        return self.image.get_box(x, y)

    def get_button_box(self) -> tuple:
        return self.button.get_box(310, 555)

    def get_closest(self, position: tuple) -> tuple:
        corners = self.widget.get_corners(*self.widget_position)
        sorted_corners = sorted(corners, key=lambda c: util.distance(position, c))
        return sorted_corners[0], sorted_corners[1]

COMMON_SCREEN_SIZES = [
    (1024, 768),
    (1280, 720),
    (1280, 800),
    (1280, 960),
    (1280, 1024),
    (1366, 768),
    (1440, 900),
    (1600, 900),
    (1600, 1200),
    (1680, 1050),
    (1920, 1080),
    (1920, 1200),
    (2048, 1152),
    (2560, 1440),
    (2560, 1600)
]
COMMON_CORE_COUNTS = [
    2,
    4,
    6,
    8,
    12,
    16,
    32
]
COMMON_MEMORY_SIZES = [
    8,
    16,
    32,
    64
]

class get_cap:
    def __init__(self, user_agent: str, href: str) -> None:
        self.user_agent = user_agent
        self.href = href
        screen_size = random.choice(COMMON_SCREEN_SIZES)
        self.screen_size = screen_size
        widget_id = '0' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        random_point = util.get_random_point(((0, 0), (screen_size[0] - 150, screen_size[1] - 38)))
        self.widget = widget_check(random_point)
        self.position = util.get_random_point(((0, 0), screen_size))
        goal = util.get_random_point(self.widget.get_check())
        self.mouse_movement = util.get_mm(self.position, goal, self.screen_size, 20, 3, 10)

        self.data = {
            "v": 1,
            "topLevel": {
                "st": util.get_ms(),
                "sc": {
                    "availWidth": self.screen_size[0],
                    "availHeight": self.screen_size[1] - 40,
                    "width": self.screen_size[0],
                    "height": self.screen_size[1],
                    "colorDepth": 24,
                    "pixelDepth": 24,
                    "availLeft": 0,
                    "availTop": 0,
                    "onchange": None,
                    "isExtended": True
                },
                "nv": {
                    "vendorSub": "",
                    "productSub": "20030107",
                    "vendor": "Google Inc.",
                    "maxTouchPoints": 0,
                    "scheduling": {},
                    "userActivation": {},
                    "doNotTrack": None,
                    "geolocation": {},
                    "connection": {},
                    "pdfViewerEnabled": True,
                    "webkitTemporaryStorage": {},
                    "windowControlsOverlay": {},
                    "hardwareConcurrency": random.choice(COMMON_CORE_COUNTS),
                    "cookieEnabled": True,
                    "appCodeName": "Mozilla",
                    "appName": "Netscape",
                    "appVersion": self.user_agent.split('Mozilla/', 1)[-1],
                    "platform": "Win32",
                    "product": "Gecko",
                    "userAgent": self.user_agent,
                    "language": "en-US",
                    "languages": [
                        "en-US",
                        "en",
                        "sv-SE",
                        "sv"
                    ],
                    "onLine": True,
                    "webdriver": False,
                    "deprecatedRunAdAuctionEnforcesKAnonymity": False,
                    "bluetooth": {},
                    "clipboard": {},
                    "credentials": {},
                    "keyboard": {},
                    "managed": {},
                    "mediaDevices": {},
                    "storage": {},
                    "serviceWorker": {},
                    "virtualKeyboard": {},
                    "wakeLock": {},
                    "deviceMemory": random.choice(COMMON_MEMORY_SIZES),
                    "userAgentData": {
                        "brands": [
                            {
                                "brand": "Not A(Brand",
                                "version": "99"
                            },
                            {
                                "brand": "Google Chrome",
                                "version": "121"
                            },
                            {
                                "brand": "Chromium",
                                "version": "121"
                            }
                        ],
                        "mobile": False,
                        "platform": "Windows"
                    },
                    "login": {},
                    "ink": {},
                    "mediaCapabilities": {},
                    "hid": {},
                    "locks": {},
                    "gpu": {},
                    "mediaSession": {},
                    "permissions": {},
                    "presentation": {},
                    "usb": {},
                    "xr": {},
                    "serial": {},
                    "plugins": [
                        "internal-pdf-viewer",
                        "internal-pdf-viewer",
                        "internal-pdf-viewer",
                        "internal-pdf-viewer",
                        "internal-pdf-viewer"
                    ]
                },
                "dr": href,
                "inv": False,
                "exec": False,
                'wn': [self.screen_size[0], self.screen_size[1], 1, util.get_ms()],
                "wn-mp": 0,
                "xy": [[0, 0, 1, util.get_ms() + 2]],
                "xy-mp": 0,
                "mm": [[x - random_point[0], y - random_point[1], t] for x, y, t in self.mouse_movement],
                "mm-mp": util.periods([x[-1] for x in self.mouse_movement])
            },
            "session": [],
            "widgetList": [widget_id],
            "widgetId": widget_id,
            "href": href,
            "prev": {
                "escaped": False,
                "passed": False,
                "expiredChallenge": False,
                "expiredResponse": False
            }
        }

class check_cap:
    def __init__(self, old_motion_data: get_cap, answers: dict) -> None:
        self.old_motion_data = old_motion_data
        screen_size = old_motion_data.screen_size
        self.screen_size = screen_size
        widget_center = util.get_center(old_motion_data.widget.get_check())
        self.position = util.get_random_point(((0, 0), screen_size))
        self.widget = binary_challenge(widget_center, screen_size)

        self.data = {
            "st": util.get_ms(),
            "dct": util.get_ms(),
            "mm": [],
            "mm-mp": 0,
            "md": [],
            "md-mp": 0,
            "mu": [],
            "mu-mp": 0,
            "topLevel": self.old_motion_data.data["topLevel"],
            "v": 1
        }

        for answer_key, is_correct in util.convert_answers(answers).items():
            if is_correct:
                goal = util.get_random_point(self.widget.get_image_box(int(answer_key)))
                mouse_movements = util.get_mm(self.position, goal, self.screen_size, 25, 3, 17)
                self.data["mm"].extend(mouse_movements)
                self.data["md"].append(mouse_movements[-1][:2] + [util.get_ms()])
                time.sleep(0.1)
                self.data["mu"].append(mouse_movements[-1][:2] + [util.get_ms()])

        self.data["mm-mp"] = util.periods([x[-1] for x in self.data["mm"]])
        self.data["md-mp"] = util.periods([x[-1] for x in self.data["md"]])
        self.data["mu-mp"] = util.periods([x[-1] for x in self.data["mu"]])

class MotionData:
    def __init__(self, user_agent: str, url: str) -> None:
        self.user_agent = user_agent
        self.url = url
        self.get_captcha_motion_data = get_cap(self.user_agent, self.url)

    def get_captcha(self) -> dict:
        return self.get_captcha_motion_data.data

    def check_captcha(self, answers) -> dict:
        return check_cap(self.get_captcha_motion_data, answers).data
