import json

import requests
from socks import method

from src.web.app import *
from flask import request

from src.web.service.proposal import *
from flask import jsonify
from src.web.app import *

#가져오기
@app.route('/model', methods=["GET"])
def fetch_data() :
    java_url = 'http://localhost:8080/pro/get'

    # print(java_url)
    # print(uno_url)

    response = requests.get(java_url) #JAVA controller api 호출
    # print(response)

    data = response.json() #json 데이터형식으로 파싱

    result = modeling(data)
    print(result)

    return str(result)

@app.route('/ubirth', method=["GET"])
def unoubirth() :
    ubirth = request.args["ubirth"]
    result = modeling(int(ubirth))
    return json.loads(result)

@app.route('/gender', method=["GET"])
def gender() :
    gender = request.args["gender"]
    result = modeling(int(gender))
    return json.loads(result)