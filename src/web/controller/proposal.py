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
    # uno_url = 'http://localhost:8080/my/info'

    gender = request.args["gender"]
    ubirth = request.args["ubirth"]

    print(ubirth)
    print(gender)

    # print(java_url)

    response = requests.get(java_url) #JAVA controller api 호출
    # response2 = requests.get(uno_url)
    # print(response)

    data = response.json() #json 데이터형식으로 파싱

    result = modeling(data,int(ubirth),int(gender))
    print(result)

    return str(result)

# @app.route('/ubirth', methods=["GET"])
# def unoubirth() :
#     ubirth = request.args["ubirth"]
#     # print(ubirth)
#     result = modeling(int(ubirth))
#     return json.loads(result)
#
# @app.route('/gender', methods=["GET"])
# def gender() :
#     gender = request.args["gender"]
#     # print(gender)
#     result = modeling(int(gender))
#     return json.loads(result)