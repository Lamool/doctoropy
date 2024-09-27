import requests
from socks import method

from src.web.app import *
from flask import request

from src.web.service.proposal import *
from flask import jsonify
from src.web.app import *

#가져오기
@app.route('/model', methods=["POST"])
def fetch_data() :
    java_url = 'http://localhost:8080/pro/get'

    user = request.get_json()

    gender = user.get('gender')
    ubirth = user.get('ubirth')

    response = requests.get(java_url) #JAVA controller api 호출
    data = response.json() #json 데이터형식으로 파싱
    # print(data)
    result = modeling(data, gender, ubirth)
    post_data(result)
    return result

@app.route('/promodel', methods=["GET"])
def post_data(result) :
    print(result)
    return result
