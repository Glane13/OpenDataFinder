# This file is derived from this source:  https://github.com/bhavaniravi/rasa-site-bot
# The original file is licensed under "the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or any later version."
# Hence this file is also licensed under GNU GPL version 3
# All other files within this repo (https://github.com/Glane13/OpenDataFinder) except appy.py and bind.js are governed by an MIT licence
from flask import Flask
from flask import render_template,jsonify,request
import requests
import random
import sys
import sys

app = Flask(__name__)
app.secret_key = '12345'

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/chat',methods=["POST"])
def chat():
    user_message = request.form["text"]
    response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": "Graham","message":user_message})
    response = response.json()[0]['text']
    if not response:
        response = "error: no response"
    return jsonify({"status":"success","response": response}) 

app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8080)