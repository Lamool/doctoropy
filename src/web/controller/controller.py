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
