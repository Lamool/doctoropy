import random

import pandas as pd
import json
from src.web.app import *
from flask import request

from fontTools.misc.cython import returns
from joblib.parallel import method
#
# df = pd.read_csv("datapokemon.csv", encoding="utf-8")
# df2 = df[['한글이름','아이디','영어이름','이미지']] #랭킹 전체출력
#
# df3 = df[["한글이름"]] #토너먼트 이름용
# df3_list = df3.values.tolist() #이차원리스트 일차원리스트로 변경
#################################################################################

@app.route("/tnmt", methods=["GET"])
def start_tournament() :
    data = request.args["set_size"]
    result = tournament(int(data))
    return json.loads(result)


@app.route("/rank")
def index():
    df = pd.read_csv("./service/datapokemon.csv", encoding="utf-8")
    df2 = df[['한글이름', '아이디', '영어이름', '이미지']]  # 랭킹 전체출력
    jsonData = df2.to_json(orient='records', force_ascii=False)
    result = json.loads(jsonData)
    return result


def tournament(set_size) :
    df = pd.read_csv("./service/datapokemon.csv", encoding="utf-8")
    df3 = df[["한글이름","이미지","아이디"]]  # 토너먼트 이름용
    df3_list = df3.values.tolist()  # 이차원리스트 일차원리스트로 변경
    select_pokemon = random.sample(df3_list, set_size)
    # print(type(select_pokemon))
    select_pokemon2 = [select_pokemon]
    select_pokemon3 = pd.DataFrame(select_pokemon2)
    jsondata = select_pokemon3.to_json(orient='records', force_ascii=False)
    print(jsondata)
    print(json.loads(jsondata))
    result = json.loads(jsondata)
    return jsondata
    # print(select_pokemon)
