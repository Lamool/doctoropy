
from src.web.app import *
from flask import request

from src.web.service.proposal import *


#가져오기
@app.route('/model/get', methods=["GET"])
def fetch_data() :
    java_url = 'http://localhost:8080/pro/get'
    uno_url = ('http://localhost:8080/user/my/info')

    response = request.get(java_url) #JAVA controller api 호출
    response2 = request.get(uno_url)

    data = response.json() #json 데이터형식으로 파싱
    users = response2.json()

    result = modeling(data, users)

    print(result)
    return result
