from flask import Flask, request, jsonify
from pymongo import MongoClient
import time
import threading
from hcap_solver import Hcaptcha, logger
import random
import string

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb+srv://dev:hwOhSJASFYGKx8sb@cluster0.dgh1m9c.mongodb.net/')
db = client['fcaptcha']
collection = db['users']

# keep this empty cus pro db shit
task_status = {}

admin_key = "fuckjews123"
def generate_api_key():
    apikey = 'fcap-' + '-'.join([''.join(random.choices(string.ascii_lowercase + string.digits, k=4)) for _ in range(3)])
    return apikey


def solve_captcha_task(api_key, task_id, sitekey, host, proxy, rqdata=None, useragent=None):
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
            "error": False,
            "task": {
                "captcha_key": captcha_key,
                "time": time.time() - start,
                "state": "error",
            },
        }
    else:
        task_status[task_id] = {
            "error": False,
            "task": {
                "captcha_key": captcha_key,
                "time": time.time() - start,
                "state": "completed",
            },
        }
        deduct = collection.find_one_and_update(
            {"api_key": api_key},
            {"$inc": {"balance": -cost}}
        )

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
    if data["balance"] <= 0:
        return jsonify({
            'message': 'bro, 0 bal api key? fuck off'
        }), 400
    apikey = generate_api_key()
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

# Solving
@app.route("/solve", methods=["POST"])
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

    if rq_data or user_agent is not None:
        threading.Thread(
            target=solve_captcha_task, args=(api_key, task_id, sitekey, host, proxy, rq_data, user_agent)
        ).start()
    else:
        threading.Thread(
            target=solve_captcha_task, args=(api_key, task_id, sitekey, host, proxy)
        ).start()

    return jsonify({"error": False, "task": {"task_id": task_id, "state": "processing"}})


@app.route("/getTaskData/<task_id>", methods=["GET"])
def get_status(task_id):
    api_key = request.headers.get('authorization')
    if not api_key:
        return jsonify({"error": True, "message": "API key is missing"}), 401

    user = collection.find_one({"api_key": api_key})
    if not user:
        return jsonify({"error": True, "message": "Invalid API key"}), 401

    if task_id not in task_status:
        return jsonify({"error": True, "message": "Task not found"}), 404

    return jsonify(task_status[task_id])


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port='1234',
        debug=True
    )
