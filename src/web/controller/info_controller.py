# info_controller.py


from src.web.app import *
from src.web.service.info_service import *

@app.route("/info/print", methods=["GET"])
def poke_info_all_print() :
    page = request.args["page"]
    print(page)
    df_list_all_result = poke_all_info_print(int(page))
    return df_list_all_result

@app.route("/info/detail", methods=["GET"])
def poke_info_detail_print() :
    name = request.args["name"]
    df_poke_detail_info_result = poke_detail_info_print(name)
    return df_poke_detail_info_result

@app.route("/info/type", methods=["GET"])
def poke_info_type_print():
    ##
    type = request.args["type"]
    page = request.args["page"]
    df_poke_type_list_all_result = type_poke_info(type, int(page))
    return df_poke_type_list_all_result
