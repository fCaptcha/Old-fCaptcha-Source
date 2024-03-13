import base64

import httpx
import time

headers = {
    "Content-type": "application/json",
    "apikey": "bobfa77-fc12e347-77f3-980a-066d-f7ff03209f51",
}

def encode_img(url):
    return base64.b64encode(httpx.get(url).content).decode()

def solve_grid(target, images, sitekey, host):
    response = httpx.post("https://pro.nocaptchaai.com/solve", headers=headers, json={
        "images": {
            "0": encode_img(images["image1"]),
            "1": encode_img(images["image2"]),
            "2": encode_img(images["image3"]),
            "3": encode_img(images["image4"]),
            "4": encode_img(images["image5"]),
            "5": encode_img(images["image6"]),
            "6": encode_img(images["image7"]),
            "7": encode_img(images["image8"]),
            "8": encode_img(images["image9"])
        },
        "target": target,
        "method": "hcaptcha_base64",
        "sitekey": sitekey,
        "site": host,
        "ln": "en",
        "softid": "UserScript3.7.0"
        },timeout=100000).json()
    return response

def solve_area_select(target, tasklist, sitekey, host):
    try:
        imgB64 = {str(i): base64.b64encode(httpx.get(str(img["datapoint_uri"])).content).decode('utf-8') for i, img in enumerate(tasklist)}

        task = httpx.post(
            'https://pro.nocaptchaai.com/solve',
            headers=headers,
            json={
                'images': imgB64,
                'target': target,
                'type': 'bbox',
                'method': 'hcaptcha_base64',
                "sitekey": sitekey,
                "site": host,
            },
            timeout=100000
        )
        time.sleep(2)
        # result__ = httpx.get(
        #     task.json()['url'],
        #     headers=headers
        # )
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
    