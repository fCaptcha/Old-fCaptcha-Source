from flask import Flask, request
from hcap_solver import Hcaptcha 
import logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

@app.route('/solve_captcha', methods=['POST'])
def solve_captcha():
    data = request.get_json()
    sitekey = data.get('sitekey')
    host = data.get('host')

    result = Hcaptcha(
        sitekey=sitekey,
        host=host, 
    ).solve()

    return {'result': result}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port="1000", debug=False)