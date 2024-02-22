import numpy as np
from scipy import interpolate
import random
import math
import time
import string

# Code by body, modified by dort
# i got consent by body to use this.

class Helpers:
    # shitty randint fix
    @staticmethod
    def randint(a, b):
        if a < b:
            return random.randint(a, b)
        else:
            return random.randint(b, a)

    @staticmethod
    def get_milliseconds_as_int():
        return int(time.time() * 1000)

    @staticmethod
    def simulate_cursor_movement(start, goal, screen_size, max_points, random_amount, polling_rate):
        cp = Helpers.randint(3, 5)

        x1, y1 = start
        x2, y2 = goal

        x = np.linspace(x1, x2, num=cp, dtype='int')
        y = np.linspace(y1, y2, num=cp, dtype='int')

        xr = [Helpers.randint(-random_amount, random_amount) for _ in range(cp)]
        yr = [Helpers.randint(-random_amount, random_amount) for _ in range(cp)]
        xr[0] = yr[0] = xr[-1] = yr[-1] = 0
        x += xr
        y += yr

        x = np.clip(x, 0, screen_size[0])
        y = np.clip(y, 0, screen_size[1])

        degree = 3 if cp > 3 else cp - 1
        tck, u = interpolate.splprep((x, y), k=degree)

        num_points = min(2 + int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / polling_rate), max_points)
        u = np.linspace(0, 1, num=num_points)

        points = interpolate.splev(u, tck)

        return [
            [int(x), int(y), Helpers.get_milliseconds_as_int()] for x, y in list(
                zip(*(i.astype(int) for i in points))
            ) if time.sleep(1 / Helpers.randint(80, 240)) is None
        ]

    @staticmethod
    def mean_period(timestamps):
        if len(timestamps) < 2:
            return 0

        periods = [timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]

        return sum(periods) / len(periods)

    @staticmethod
    def distance(a, b):
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    @staticmethod
    def get_random_point(bounding_box):
        return Helpers.randint(bounding_box[0][0], bounding_box[1][0]), Helpers.randint(bounding_box[0][1],
                                                                                        bounding_box[1][1])

    @staticmethod
    def get_center(bounding_box):
        x1, y1 = bounding_box[0]
        x2, y2 = bounding_box[1]

        return int(x1 + (x2 - x1) / 2), int(y1 + (y2 - y1) / 2)

    @staticmethod
    def convert_answers(answers, as_dict=True):
        if isinstance(answers, dict):
            answers = list(answers.values())
        else:
            answers = answers
        if as_dict:
            answer_dict = {}
            i = 0
            for answer in answers:
                if isinstance(answer, str):
                    answer_dict[i] = answer.lower() == 'true'
                else:
                    answer_dict[i] = answer
                i += 1
            return answer_dict
        else:
            answer_list = []
            for answer in answers:
                if isinstance(answer, str):
                    answer_list.append(answer.lower() == 'true')
                else:
                    answer_list.append(answer)
            return answer_list


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_dimensions(self):
        return self.width, self.height

    def get_bounding_box(self, relative_x, relative_y):
        return (relative_x, relative_y), (relative_x + self.width, relative_y + self.height)

    def get_corners(self, relative_x=0, relative_y=0):
        return [(relative_x, relative_y), (relative_x + self.width, relative_y), (relative_x, relative_y + self.height),
                (relative_x + self.width, relative_y + self.height)]


class WidgetCheckBox:
    def __init__(self, relative_position):
        self.widget = Rectangle(300, 75)
        self.check_box = Rectangle(28, 28)
        self.relative_position = relative_position

    def get_check_box_bounding_box(self):
        return self.check_box.get_bounding_box(16 + self.relative_position[0], 23 + self.relative_position[1])

    def get_closest_face(self, position):
        corners = self.widget.get_corners(self.relative_position[0], self.relative_position[1])
        sorted_corners = sorted(corners, key=lambda c: Helpers.distance(position, c))
        return sorted_corners[0], sorted_corners[1]


# TODO: widget inheritence
# TODO: retry option

class WidgetChallengeText:
    def __init__(self, check_box_centre_position, screen_size):

        x: int
        y: int

        if check_box_centre_position[0] > screen_size[0] - 380:
            x = screen_size[0] / 2 - 185
        else:
            x = check_box_centre_position[0] + 25

        if check_box_centre_position[1] <= 160:
            y = 10
        elif check_box_centre_position[1] >= screen_size[1] - 160:
            y = screen_size[1] - 310
        else:
            y = check_box_centre_position[1] - 150

        widget_position = (x, y)
        self.widget_position = widget_position
        self.widget = Rectangle(370, 300)
        self.text_box = Rectangle(314, 40)
        self.button = Rectangle(80, 35)

    def get_text_bounding_box(self):
        return self.text_box.get_bounding_box(28, 165)

    def get_button_bounding_box(self):
        return self.button.get_bounding_box(280, 255)

    def get_closest_face(self, position):
        corners = self.widget.get_corners(self.widget_position[0], self.widget_position[1])
        sorted_corners = sorted(corners, key=lambda c: Helpers.distance(position, c))
        return sorted_corners[0], sorted_corners[1]


class WidgetChallengeBinary:
    def __init__(self, check_box_centre_position, screen_size):

        x: int
        y: int

        if check_box_centre_position[0] > screen_size[0] - 410:
            x = screen_size[0] / 2 - 200
        else:
            x = check_box_centre_position[0] + 25

        if check_box_centre_position[1] <= 310:
            y = 10
        elif check_box_centre_position[1] >= screen_size[1] - 310:
            y = screen_size[1] - 610
        else:
            y = check_box_centre_position[1] - 300
        widget_position = x, y
        self.widget_position = widget_position

        self.widget = Rectangle(400, 600)

        self.button = Rectangle(80, 35)

        self.image = Rectangle(120, 120)

        i = 0
        self.images = {}
        iy = 0
        for _ in range(3):
            ix = 10
            iy += 130
            for __ in range(3):
                self.images[str(i)] = (ix, iy)
                ix += 130
                i += 1

    def get_image_bounding_box(self, index):
        if index > 8:
            index -= 8
        x, y = self.images.get(str(index))
        return self.image.get_bounding_box(x, y)

    def get_button_bounding_box(self):
        return self.button.get_bounding_box(310, 555)

    def get_closest_face(self, position):
        corners = self.widget.get_corners(self.widget_position[0], self.widget_position[1])
        sorted_corners = sorted(corners, key=lambda c: Helpers.distance(position, c))
        return sorted_corners[0], sorted_corners[1]


class WidgetChallengeMultipleChoice:
    class Size:
        class DEFAULT:
            WIDTH = 500
            HEIGHT = 520
            BUTTON_HEIGHT = 80
            BUTTON_WIDTH = 200

        WIDTH = 400
        HEIGHT = 600

    def __init__(self, check_box_centre_position, screen_size):
        x: int
        y: int
        if check_box_centre_position[0] > screen_size[0] - 510:
            x = screen_size[0] / 2 - 250
        else:
            x = check_box_centre_position[0] + 25
        if check_box_centre_position[1] <= 270:
            y = 10
        elif check_box_centre_position[1] >= screen_size[1] - 310:
            y = screen_size[1] - 530
        else:
            y = check_box_centre_position[1] - 260
        widget_position = x, y
        self.widget_position = widget_position

        self.widget = Rectangle(500, 520)

        self.button = Rectangle(80, 35)

        self.answer_box = Rectangle(200, 80)
        i = 0
        self.answer = {}
        ay = 10
        for _ in range(4):
            ay += 80
            self.answer[str(i)] = (290, ay)
            i += 1

    def get_answer_bounding_box(self, index):
        x, y = self.answer.get(str(index))
        return self.answer_box.get_bounding_box(x, y)

    def get_button_bounding_box(self):
        return self.button.get_bounding_box(410, 475)

    def get_closest_face(self, position):
        corners = self.widget.get_corners(self.widget_position[0], self.widget_position[1])
        sorted_corners = sorted(corners, key=lambda c: Helpers.distance(position, c))
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


##
# might implement windowed mode later; for now we assume that the frame takes 100% of the screen space
##
class _GetCaptchaMotionData:
    global COMMON_SCREEN_SIZES, COMMON_CORE_COUNTS

    def __init__(self, user_agent, href, screen_size=None, widget_id=None):
        self.user_agent = user_agent

        if screen_size is None:
            screen_size = random.choice(COMMON_SCREEN_SIZES)

        self.screen_size = screen_size

        if widget_id is None:
            widget_id = '0' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

        random_point = Helpers.get_random_point(((0, 0), (screen_size[0] - 150, screen_size[1] - 38)))

        self.widget = WidgetCheckBox(random_point)

        self.position = Helpers.get_random_point(((0, 0), screen_size))

        data = {
            'st': Helpers.get_milliseconds_as_int(),
            'mm': [],
            'mm-mp': 0,
            'md': [],
            'md-mp': 0,
            'mu': [],
            'mu-mp': 0,
            'v': 1,
            'topLevel': self.top_level(),
            'session': [],
            'widgetList': [widget_id],
            'widgetId': widget_id,
            'href': href,
            'prev': {  # previous data
                'escaped': False,
                'passed': False,
                'expiredChallenge': False,
                'expiredResponse': False
            }
        }

        goal = Helpers.get_random_point(self.widget.get_check_box_bounding_box())

        self.mouse_movement = Helpers.simulate_cursor_movement(
            self.position,
            goal,
            self.screen_size,
            20,
            3,
            10
        )

        data['mm'] = [[x - random_point[0], y - random_point[1], t] for x, y, t in self.mouse_movement]
        data['mm-mp'] = Helpers.mean_period([x[-1] for x in self.mouse_movement])

        data['md'].append(data['mm'][-1][:-1] + [Helpers.get_milliseconds_as_int()])

        time.sleep(1 / Helpers.randint(3, 7))

        data['mu'].append(data['mm'][-1][:-1] + [Helpers.get_milliseconds_as_int()])

        self.data = data

    def top_level(self):
        data = {
            'inv': False,
            'st': Helpers.get_milliseconds_as_int(),
            'sc': {
                'availWidth': self.screen_size[0],
                'availHeight': self.screen_size[1],
                'width': self.screen_size[0],
                'height': self.screen_size[1],
                'colorDepth': 24,
                'pixelDepth': 24,
                'top': 0,
                'left': 0,
                'availTop': 0,
                'availLeft': 0,
                'mozOrientation': 'landscape-primary',
                'onmozorientationchange': None
            },
            'nv': {  # (window.navigator) removed alot of depricated items
                'permissions': {},
                'pdfViewerEnabled': True,
                'doNotTrack': 'unspecified',
                'maxTouchPoints': 0,
                'mediaCapabilities': {},
                'vendor': '',
                'vendorSub': '',
                'cookieEnabled': True,
                'mediaDevices': {},
                'serviceWorker': {},
                'credentials': {},
                'clipboard': {},
                'mediaSession': {},
                'webdriver': False,
                'hardwareConcurrency': random.choice(COMMON_CORE_COUNTS),
                'geolocation': {},
                'userAgent': self.user_agent,
                'language': 'en-US',
                'languages': ['en-US', 'en'],
                'locks': {},
                'onLine': True,
                'storage': {},
                'plugins': [  # internal-pdf-viewer
                    'internal-pdf-viewer',
                    'internal-pdf-viewer',
                    'internal-pdf-viewer',
                    'internal-pdf-viewer',
                    'internal-pdf-viewer'
                ]
            },
            'dr': '',
            'exec': False,
            'wn': [  # assume the screen is not resized
                [
                    self.screen_size[0],
                    self.screen_size[1],
                    1,  # screen DPR
                    Helpers.get_milliseconds_as_int()
                ]
            ],
            'wn-mp': 0,
            'xy': [
                [
                    0,  # scroll X
                    0,  # scroll Y
                    1,  # document.documentElement.clientWidth / tt.Browser.width()
                    Helpers.get_milliseconds_as_int()
                ]
            ],
            'xy-mp': 0,
            'mm': [],
            'mm-mp': 0
        }

        goal = Helpers.get_random_point(self.widget.get_closest_face(self.position))

        mouse_movement = Helpers.simulate_cursor_movement(
            self.position,
            goal,
            self.screen_size,
            75,
            3,
            15
        )

        self.position = goal

        data['mm'] = mouse_movement
        data['mm-mp'] = Helpers.mean_period([x[-1] for x in mouse_movement])

        return data


class _CheckCaptchaMotionData:
    global COMMON_SCREEN_SIZES, COMMON_CORE_COUNTS

    def __init__(self, previous_motion_data, answers, captcha_type):
        self.position: list = []
        self.previous_motion_data = previous_motion_data

        screen_size = previous_motion_data.screen_size
        self.screen_size = screen_size

        widget = {
            'image_label_binary': WidgetChallengeBinary,
            'text_free_entry': WidgetChallengeText,
            'image_label_multiple_choice': WidgetChallengeMultipleChoice
        }.get(captcha_type)(
            Helpers.get_center(previous_motion_data.widget.get_check_box_bounding_box()),
            screen_size
        )

        self.widget = widget

        data = {
            'st': Helpers.get_milliseconds_as_int(),  # start time
            'dct': Helpers.get_milliseconds_as_int(),  # same as start time
            'mm': [],  # mouse movement (inside the widget)
            'mm-mp': 0,  # mouse movement mean period (inside the widget)
            'md': [],  # mouse down
            'md-mp': 0,  # mouse down mean period (assume that there is only one click; the mean period is 0)
            'mu': [],  # mouse up
            'mu-mp': 0,  # mouse up mean period (assume that there is only one click; the mean period is 0)
            'v': 1,  # some constant, probably motion data version
            'topLevel': self.top_level()  # top level (tracking for outside of the widget)
        }

        relative_position = (self.position[0] - widget.widget_position[0], self.position[1] - widget.widget_position[1])
        if captcha_type == 'image_label_binary':
            for index, answer in Helpers.convert_answers(answers).items():
                if answer:
                    goal = Helpers.get_random_point(widget.get_image_bounding_box(index))
                    data['mm'] += Helpers.simulate_cursor_movement(
                        relative_position,
                        goal,
                        screen_size,
                        25,
                        3,
                        17
                    )

                    data['md'].append(list(goal) + [Helpers.get_milliseconds_as_int()])
                    time.sleep(1 / Helpers.randint(4, 9))
                    data['mu'].append(list(goal) + [Helpers.get_milliseconds_as_int()])

                    relative_position = goal

                if (index + 1) % 9:
                    goal = Helpers.get_random_point(widget.get_button_bounding_box())
                    data['mm'] += Helpers.simulate_cursor_movement(
                        relative_position,
                        goal,
                        screen_size,
                        25,
                        3,
                        16
                    )

                    data['md'].append(list(goal) + [Helpers.get_milliseconds_as_int()])
                    time.sleep(1 / Helpers.randint(4, 9))
                    data['mu'].append(list(goal) + [Helpers.get_milliseconds_as_int()])

                    relative_position = goal
                time.sleep(1 / Helpers.randint(4, 9))

        elif captcha_type == 'text_free_entry':
            for _ in range(3):
                goal = Helpers.get_random_point(widget.get_text_bounding_box())
                if Helpers.randint(0, 10) > 6:
                    data['mm'] += Helpers.simulate_cursor_movement(
                        relative_position,
                        goal,
                        screen_size,
                        15,
                        3,
                        17
                    )
                    relative_position = goal
                    data['md'].append(list(goal) + [Helpers.get_milliseconds_as_int()])
                    time.sleep(1 / Helpers.randint(4, 9))
                    data['mu'].append(list(goal) + [Helpers.get_milliseconds_as_int()])
                time.sleep(10 / Helpers.randint(8, 15))
                goal = Helpers.get_random_point(widget.get_button_bounding_box())
                data['mm'] += Helpers.simulate_cursor_movement(
                    relative_position,
                    goal,
                    screen_size,
                    30,
                    3,
                    17
                )
                relative_position = goal
                data['md'].append(list(goal) + [Helpers.get_milliseconds_as_int()])
                time.sleep(1 / Helpers.randint(7, 9))
                data['mu'].append(list(goal) + [Helpers.get_milliseconds_as_int()])

        elif captcha_type == 'image_label_multiple_choice':
            for _ in range(3):
                goal = Helpers.get_random_point(widget.get_answer_bounding_box(Helpers.randint(0, 3)))
                data['mm'] += Helpers.simulate_cursor_movement(
                    relative_position,
                    goal,
                    screen_size,
                    40,
                    3,
                    17
                )
                relative_position = goal
                data['md'].append(list(goal) + [Helpers.get_milliseconds_as_int()])
                time.sleep(1 / Helpers.randint(4, 9))
                data['mu'].append(list(goal) + [Helpers.get_milliseconds_as_int()])
                goal = Helpers.get_random_point(widget.get_button_bounding_box())
                data['mm'] += Helpers.simulate_cursor_movement(
                    relative_position,
                    goal,
                    screen_size,
                    40,
                    3,
                    17
                )
                relative_position = goal
                data['md'].append(list(goal) + [Helpers.get_milliseconds_as_int()])
                time.sleep(1 / Helpers.randint(7, 15))
                data['mu'].append(list(goal) + [Helpers.get_milliseconds_as_int()])
        for x in ['m', 'd', 'u']:
            data[f'm{x}-mp'] = Helpers.mean_period([x[-1] for x in data['m' + x]])

        self.data = data

    def top_level(self):

        data = self.previous_motion_data.data['topLevel']

        data['mm'] += self.previous_motion_data.mouse_movement

        position = tuple(data['mm'][-1][:-1])
        data['mm'] += Helpers.simulate_cursor_movement(
            position,
            Helpers.get_random_point(self.widget.get_closest_face(position)),
            self.screen_size,
            60,
            3,
            16
        )

        data['mm-mp'] = Helpers.mean_period([x[-1] for x in data['mm']])

        self.position = tuple(data['mm'][-1][:-1])

        return data


class MotionData:
    def __init__(self, user_agent, url):
        self.user_agent = user_agent
        self.url = url
        self.get_captcha_motion_data = _GetCaptchaMotionData(self.user_agent, self.url)

    def get_captcha(self):
        return self.get_captcha_motion_data.data

    def check_captcha(self, answers, captcha_type):
        return _CheckCaptchaMotionData(self.get_captcha_motion_data, answers, captcha_type).data
