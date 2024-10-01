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

@app.route('/pokeinfos', methods=["GET"])
def pokeinfos() :
    # number = request.args["number"]
    df = pd.read_csv("./service/datapokemon.csv", encoding="utf-8")
    df3 = df[["한글이름","한글정보","한글정보2","아이디"]]
    # print(df3)
    jsonData = df3.to_json(orient='records', force_ascii=False)
    result = json.loads(jsonData)
    return result