from src.web.app import *
from src.web.service.base_stats_service import *

# 포켓몬 종족값 목록 출력
@app.route("/base/stats/print", methods=["GET"])
def base_stats_all_print() :
    result = base_stats_print_all()
    print(result)
    return "a"


