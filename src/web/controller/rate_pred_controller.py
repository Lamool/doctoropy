# rate_pred_controller.py

from src.web.app import *
from src.web.service.rate_pred_service import *

@app.route("/rate_pred/take", methods=["GET"])
def list_take() :
    list = request.args["list"]
    poke_list_take(list)
