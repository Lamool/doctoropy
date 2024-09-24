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
