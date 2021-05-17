#!/usr/bin/env python3

from flask import Flask, render_template, redirect, request
import requests
from typing import List
import os

app = Flask(__name__)

HTTP_ENDPOINT = os.getenv('HTTP_ENDPOINT')
ESCAPE_HTML = os.getenv('ESCAPE_HTML')
if not HTTP_ENDPOINT:
    print("ERROR: HTTP_ENDPOINT not set")
    exit(1)

ESCAPE_HTML = ESCAPE_HTML and ESCAPE_HTML == "True"

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "GET":
            captcha_id, captcha_png = captcha_get(ttl=600)
            return render_template("index.html", captcha_id = captcha_id, captcha_png = captcha_png)
        elif request.method == "POST":
            captcha_id = request.form.get('captcha-id')
            captcha_solution = request.form.get('captcha-solution')
            success, trials_left = captcha_validate(captcha_id, captcha_solution)
            if not success:
                return render_template('message.html', message = "Failed captcha", attempts_left = trials_left)
            message = request.form.get('message')
            if ESCAPE_HTML:
                message = message.replace("<", "&lt;").replace(">", "&gt;")
            if message != "":
                requests.post(HTTP_ENDPOINT, data={'subject': 'New Simple Contact message', 'message': message})
            return render_template('message.html', message = "Your message was sent successfully")
        else:
            raise TypeError("Invalid method")
    except Exception as e:
        print(e)
        return render_template('message.html', message="Error occurred")

def captcha_get(max_tries: int = 3, ttl: int = 120, difficulty: str = "medium") -> List[str]:
    """ Creates a captcha and returns [id, base64 encoded png] """
    response = requests.post(f"http://rust-captcha:8000/new/{difficulty}/{max_tries}/{ttl}", headers={'X-Client-ID': 'Simple Contact'}).json()
    if response["error_code"] != 0:
        raise Exception(response)
    return [response["result"]["id"], response["result"]["png"]]

def captcha_validate(captcha_id: str, captcha_solution: str) -> List:
    """ Validates a captcha and returns [success, trials_left] """
    if len(captcha_id) > 100 or len(captcha_solution) > 10:
        return [False, 0]
    response = requests.post(f"http://rust-captcha:8000/solution/{captcha_id}/{captcha_solution}", headers={'X-Client-ID': 'Simple Contact'}).json()
    if response["error_code"] != 0:
        print(f"http://rust-captcha:8000/solution/{captcha_id}/{captcha_solution}")
        raise Exception(response)
    if response["result"]["solution"] == "accepted":
        return [True, 0]
    return [False, response["result"]["trials_left"]]

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8888)