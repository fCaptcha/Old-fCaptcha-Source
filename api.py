from flask import Flask, request, jsonify
from pymongo import MongoClient
import time
import threading
from hcap_solver import Hcaptcha, logger
import random
import string

app = Flask(__name__)

client = MongoClient('mongodb+srv://dev:hwOhSJASFYGKx8sb@cluster0.dgh1m9c.mongodb.net/')
db = client['fcaptcha']
collection = db['users']

task_status = {}

admin_key = "fuckjews123"
def generate_api_key() -> str:
    return f"fcap-{'-'.join([''.join(random.choices(string.ascii_lowercase + string.digits, k=4)) for _ in range(3)])}"

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

    rq_data = rq_data if rq_data != "" else None
    user_agent = user_agent if user_agent != "" else None

    threading.Thread(
        target=solve_captcha_task, args=(api_key, task_id, sitekey, host, proxy, rq_data, user_agent)
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

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port='1234',
        debug=True
    )
