# rate_pred_controller.py

from src.web.app import *
from src.web.service.rate_pred_service import *

@app.route("/rate_pred/take", methods=["POST"])
def list_take() :
    # data = request.get_json()
    #received_list = data.get('my_list', []) # 쿼리스트링 받아오기
    #print(f"Received list: {received_list}")
    #poke_list_take(data)

    contentType = request.content_type # 또는 contentType = request.headers.get('Content-Type')
    args = None
    # form
    if contentType == "application/x-www-form-urlencoded":
        args: dict = request.form
    # json
    elif contentType == "application/json":
        args: dict = request.json
    else:
        print("not supported content-type")

    data = list( args.get('list') )
    print( data )
    poke_list_take(data)
    return jsonify({"status": "success", "received": []})

@app.route("/rate_pred/update", methods=["GET"])
def model_update():
    poke_rate_predict_model()
    return "승률 예측 모델 최신화 성공"

@app.route("/rate_pred/predict", methods=["GET"])
def poke_real_predict():
    poke_index = request.args["poke_index"]
    rskillpower = request.args["rskillpower"]

    poke_info_list = poke_score_cal(poke_index, rskillpower)
    new_poke_rate_predict = poke_rate_predict_result(poke_info_list)

    return new_poke_rate_predict


###