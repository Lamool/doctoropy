import json

from src.web.app import app

from src.web.service.service import *
from src.web.app import *
# 김민석 112233
#

@app.route("/rate/cal", methods = ['GET'])
def rate_cal() :
    n1 = request.args["n1"]
    m1 = request.args["m1"]
    n2 = request.args["n2"]
    m2 = request.args["m2"]
    rate_dict = poke(int(n1), int(m1), int(n2), int(m2))
    return rate_dict


@app.route("/rate/data_info", methods = ["GET"])
def rate_data_info() :
    n = request.args["n"]
    poke_data_info = poke_rate_data_info(int(n))
    return poke_data_info

@app.route("/rate/skill_info", methods = ["GET"])
def rate_skill_info() :
    n = request.args["n"]
    poke_data_info = poke_rate_skill_info(int(n))
    return poke_data_info

@app.route("/rate/all_info", methods=["GET"])
def rate_data_all() :
    poke_data_json_loads = poke_info_num()
    return poke_data_json_loads

@app.route("/rate/all_skill", methods=["GET"])
def rate_skill_all() :
    poke_data_json_loads = poke_skill_num()
    return poke_data_json_loads

@app.route("/rate/each_skill_info", methods=["GET"])
def each_skill_info():
    kr_name = request.args["kr_name"]
    poke_skill_each_data_list = poke_new_skill_info(kr_name)
    return poke_skill_each_data_list