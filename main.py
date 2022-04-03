#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import flask
import requests

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/webhook/<env>', methods=['POST'])
def receive_message(env):
    prometheus_data = json.loads(flask.request.data)
    print(prometheus_data)

    summary = prometheus_data['commonAnnotations']['summary']
    description = prometheus_data['commonAnnotations']['description']
    severity = prometheus_data['alerts'][0]['labels']['severity']
    start_time = prometheus_data['alerts'][0]['startsAt']
    message = str('alert: %s' %summary + 'description: %s' %description + 'start_time: %s' %start_time)

    print(message)
    send_message(message, env)
    return "OK", 200

def send_message(message, env):
    url="http://localhost:9191"
    if env == "prod":
        url = "http://localhost:9192"

    params = {"key1": "value1", "key2": "value2", "text": "message"}

    response = requests.post(url, params=params)
    print(response)

if __name__ == '__main__':
    app.run(debug = False, host = 'localhost', port = 7000)