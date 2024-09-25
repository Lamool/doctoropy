
from src.web.app import *
from flask import request

from src.web.service.proposal import *


#가져오기
@app.route('/model/get', methods=["GET"])
def fetch_data() :
    java_url = 'http://localhost:8080/pro/get'
    response = request.get(java_url) #JAVA controller api 호출
    data = response.json() #json 데이터형식으로 파싱
    result = modeling(data)
    return jsonify(data)

#내보내기