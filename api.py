from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
import time
import threading
import requests
from fcaptcha import Hcaptcha, logger
import random
import string
import json
import hashlib
import hmac

start_time = time.time()
import logging
app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

client = MongoClient("mongodb+srv://dexv:#tkKM..FZeKx8$n@cluster0.xa88iyg.mongodb.net")
db = client['fcaptcha']
collection = db['users']

task_status = {}

admin_key = "DEXYSEXYFRFR^()69"
webhook = "https://discord.com/api/webhooks/1236679645873573970/n7sXyWyw-WjyIEmupNv7UBQQcWDVx6qBKxFxDOTylDt6P7ZWG1Sc9L4lFUhyTJD2zqGI"

def format_uptime(uptime_seconds):
    minutes, seconds = divmod(uptime_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    uptime_format = "{:02}w:{:02} / d:{:02} / h:{:02} / m:{:02}s".format(weeks, days, hours, minutes, seconds)
    return uptime_format

def send_error(api_key, sitekey, host, proxy, error):
   data = {
     "content": None,
     "embeds": [
      {
        "title": "Solve Error!",
        "description": f"API Key: {api_key}\nSite Key: {sitekey}\nHost: https://{host}/\nProxy: {proxy}\n---------------------------------------------------------------\n**Error:**\n```\ne{error}\n```",
        "color": 16385285
     }
    ],
    "attachments": []
   }
   r = requests.post(webhook, json=data)
   if r.status_code == 200:
     print("Sent Error to Logs")
   else:
     print("Failed to log error :(")
   
def generate_api_key() -> str:
    return f"fCap-{'-'.join([''.join(random.choices(string.ascii_lowercase + string.digits, k=4)) for _ in range(3)])}"

def clear_task_status(task_id: str) -> None:
    if task_id in task_status:
        del task_status[task_id]
        logger.log.success(f"Deleted task -> {task_id}")

def solve_captcha_task(api_key: str, task_id: str, sitekey: str, host: str, proxy: str, rqdata: str = None, useragent: str = None) -> None:
    start = time.time()
    if sitekey == "4c672d35-0701-42b2-88c3-78380b0db560":
        cost = 0.0005
    else:
        cost = 0.00025

    captcha_key = Hcaptcha(
        site_key=sitekey,
        host=host,
        proxy=proxy,
        rq_data=rqdata,
        user_agent=useragent
    ).solve()
    if captcha_key is None:
        task_status[task_id] = {
            "error": True,
            "task": {
                "captcha_key": captcha_key,
                "time": time.time() - start,
                "state": "error",
            },
        }
    #    send_error(api_key, sitekey, host, proxy, 'error_message')
    else:
        task_status[task_id] = {
            "error": False,
            "task": {
                "captcha_key": captcha_key,
                "time": time.time() - start,
                "state": "completed",
            },
        }
        collection.find_one_and_update(
            {"api_key": api_key},
            {"$inc": {"balance": -cost}}
        )
    threading.Timer(20, clear_task_status, args=(task_id,)).start()

# ADMIN Routes
@app.route('/admin/create', methods=['POST'])
def create_api_key():
    api_key = request.headers.get('authorization')
    if not api_key:
        return jsonify({"error": True, "message": "API key is missing"}), 401
    user = admin_key
    if not user:
        return jsonify({"error": True, "message": "Invalid API key"}), 401

    data = request.json
    apikey = data.get("api_key", generate_api_key())
    if data["balance"] <= 0:
        return jsonify({
            'message': 'bro, 0 bal api key? fuck off'
        }), 400
    Insert = {
        "api_key": apikey,
        "balance": data["balance"],
        "permissions": 0
    }
    collection.insert_one(Insert)
    return jsonify({
        'message': 'Successfully Created a New User!',
        'api_key': apikey
    }), 201
 
@app.route('/admin/delete', methods=['DELETE'])
def remove_api_key():
    api_key = request.headers.get('authorization')
    if not api_key:
        return jsonify({"error": True, "message": "API key is missing"}), 401
    user = admin_key
    if not user:
        return jsonify({"error": True, "message": "Invalid API key"}), 401
    data = request.json
    result = collection.delete_one({
        'api_key': data["api_key"]
    })
    if result.deleted_count == 0:
        return jsonify({
            'message': 'API key not found'
        }), 404
    return jsonify({
        'message': 'Deleted'
    })

@app.route('/admin/update_key', methods=['POST'])
def update_api_key_balance():
    api_key = request.headers.get('authorization')
    if not api_key:
        return jsonify({"error": True, "message": "API key is missing"}), 401
    user = admin_key
    if not user:
        return jsonify({"error": True, "message": "Invalid API key"}), 401

    data = request.json
    if "balance" not in data or data["balance"] <= 0:
        return jsonify({
            'message': 'Invalid balance'
        }), 400

    result = collection.update_one(
        {'api_key': api_key},
        {'$set': {'balance': data["balance"]}}
    )

    if result.matched_count == 0:
        return jsonify({
            'message': 'API key not found'
        }), 404

    return jsonify({
        'message': 'Balance updated successfully'
    }), 200

# Solving
@app.route("/api/createTask", methods=["POST"])
def solve_captcha_route():
    api_key = request.headers.get('authorization')
    if not api_key:
        return jsonify({"error": True, "message": "API key is missing"}), 401

    user = collection.find_one({"api_key": api_key})
    if not user:
        return jsonify({"error": True, "message": "Invalid API key"}), 401

    data = request.get_json()
    ip_address = request.headers.get('CF-Connecting-IP', request.remote_addr)

    if not data or "sitekey" not in data or "host" not in data or "proxy" not in data:
        return jsonify({"error": "Invalid JSON"}), 400

    sitekey = data["sitekey"]
    host = data["host"]
    proxy = data["proxy"]
    rq_data = data.get("rqdata")
    user_agent = data.get("user_agent")

    task_id = f"{''.join(str(random.randint(0, 9)) for _ in range(5))}-{''.join(str(random.randint(0, 9)) for _ in range(6))}-{''.join(str(random.randint(0, 9)) for _ in range(6))}"

    if task_id in task_status and task_status[task_id]["task"]["state"] == "processing":
        return jsonify({"error": False, "task": {"state": "processing"}})

    task_status[task_id] = {"error": False, "task": {"state": "processing"}}

    logger.log.info(f"New Task Created: {task_id} From IP: {ip_address}")

    rq_data = rq_data if rq_data != "" else None
    user_agent = user_agent if user_agent != "" else None

    threading.Thread(
        target=solve_captcha_task, args=(api_key, task_id, sitekey, host, proxy, rq_data, user_agent)
    ).start()

    return jsonify({"error": False, "task": {"task_id": task_id, "state": "Created"}}), 200

@app.route("/api/getTaskData", methods=["GET", "POST"])
def get_status():
    api_key = request.headers.get('authorization')
    if not api_key:
        return jsonify({"error": True, "message": "API key is missing"}), 401

    data = request.get_json()
    task_id = data["task_id"]
    user = collection.find_one({"api_key": api_key})
    if not user:
        return jsonify({"error": True, "message": "Invalid API key"}), 401

    if task_id not in task_status:
        return jsonify({"error": True, "message": "Task not found"}), 404

    return jsonify(task_status[task_id]), 200

@app.route('/get_balance/<api_key>', methods=['GET'])
def get_api_key_balance(api_key):
    if not api_key:
        return jsonify({"error": True, "message": "API key is missing"}), 401
    user = admin_key
    if not user:
        return jsonify({"error": True, "message": "Invalid API key"}), 401

    result = collection.find_one({'api_key': api_key})

    if not result:
        return jsonify({
            'message': 'API key not found'
        }), 404

    return jsonify({
        'message': 'Balance retrieved successfully',
        'balance': result['balance']
    }), 200
    
@app.route('/sellix/complete_purchase', methods=['POST'])
def sellix_complete():
    Sig = request.headers.get("X-Sellix-Signature")
    if not Sig:
        return jsonify({"error": True, "message": "X-Sellix-Signature Is Missing"}), 401
    
    payload = request.get_data()
    secret = b'kEn3nTemMlVhIzUZWBnesX8cu1ntHZ2K'  # replace with your webhook secret
    header_signature = Sig

    computed_signature = hmac.new(secret, payload, hashlib.sha512).hexdigest()
    
    if hmac.compare_digest(computed_signature, header_signature):
        data = request.get_json()
        if data and "data" in data and "uniqid" in data["data"]:
            uniqid = data["data"]["uniqid"]
            print("Valid Signature Recived!")
            print(f"Received uniqid: {uniqid}")
            bal = data["data"]["total"]
            apikey = generate_api_key()
            Insert = {
             "api_key": apikey,
             "balance": bal,
             "permissions": 0
            }
            collection.insert_one(Insert)
            print(f"${bal} Api key proccessed VIA Sellix storefront ")
            #print("new invoice processed")
            return f'${bal} - {apikey}', 200
        else:
            return jsonify({'message': 'Invalid data format!'}), 400
    else:
        return jsonify({'message': 'Invalid SIG!'}), 401
    
    
@app.route('/', methods=['GET'])
def home():
    uptime = time.time() - start_time
    response = {
        "message": "Welcome to fCaptcha API",
        "version": "1.1.1",
        "uptime": format_uptime(uptime),
        "docs": "https://docs.fcaptcha.lol",
        "discord": "https://discord.gg/fcaptcha",
        "authors": {
            "dexv & dort": "Solver",
            "denzelxrt": "API"
        },
        "github": "https://github.com/DXVVAY",
        "status": "Up And Working",
        "hcaptcha": {
            "hsw-version": "122e1a7",
            "discord_status": {
                "Register": "Phone Locked",
                "Join": "Works",
                "Friend Request": "Works"
            },
            "epicgames_status": {
                "Register": "Works"
            }
        }
    }

    return Response(json.dumps(response, sort_keys=False, indent=4), mimetype='application/json'), 200

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port='80',
        debug=True
    )