from hcap_solver.logger import *
import base64, httpx

class AI_Solver:
    def __init__(self, type: str, captcha: dict, sitekey: str, host: str) -> None:
        self.type = type
        self.captcha = captcha
        self.sitekey = sitekey
        self.host = host
        self.headers = {
            "Content-type": "application/json",
            "apikey": "bobfa77-fc12e347-77f3-980a-066d-f7ff03209f51",
        }

    def encode_img(self, url: str) -> str:
        return base64.b64encode(httpx.get(url).content).decode()

    def solve(self) -> dict:
        solvers = {
            'image_label_binary': self.label_binary,
            'image_label_area_select': self.area_select
        }
        try:
            return solvers[self.type]()
        except KeyError:
            log.failure(f"Unsupported Captcha Type -> {self.type}", level="hCaptcha")

    def label_binary(self) -> dict:
        example = self.captcha.get("requester_question_example", [None])[0]
        data = {
            "images": {
                str(i): self.encode_img(self.captcha['tasklist'][i]["datapoint_uri"]) for i in range(9)
            },
            "target": self.captcha["requester_question"]["en"],
            "method": "hcaptcha_base64",
            "sitekey": self.sitekey,
            "site": self.host,
            "ln": "en",
            "softid": "UserScript3.7.0"
        }
        if example is not None: data["examples"] = [self.encode_img(example)]
        response = httpx.post("https://pro.nocaptchaai.com/solve", headers=self.headers, json=data,timeout=100000).json()
        return {self.captcha['tasklist'][i]["task_key"]: str(i in response["solution"]).lower() for i in range(9)}

    def area_select(self) -> dict:
        tasklist = self.captcha['tasklist']
        try:
            image = {str(i): base64.b64encode(httpx.get(str(img["datapoint_uri"])).content).decode('utf-8') for i, img in enumerate(tasklist)}
            task = httpx.post(
                'https://pro.nocaptchaai.com/solve',
                headers=self.headers,
                json={
                    'images': image,
                    'target': self.captcha["requester_question"]["en"],
                    'type': 'bbox',
                    'method': 'hcaptcha_base64',
                    "sitekey": self.sitekey,
                    "site": self.host,
                },
                timeout=100000
            )
            poses = task.json()['answers']
            return {
                tasklist[0]["task_key"]: [
                    {
                        "entity_name": 0,
                        "entity_type": "label",
                        "entity_coords": poses[0]
                    }
                ],
                tasklist[1]["task_key"]: [
                    {
                        "entity_name": 0,
                        "entity_type": "label",
                        "entity_coords": poses[1]
                    }
                ]
            }
        except:
            pass
