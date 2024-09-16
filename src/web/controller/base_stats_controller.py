from src.web.app import *
from src.web.service.base_stats_service import *

# 포켓몬 종족값 목록 -> 아이디(번호)를 기준으로 출력 [오름차순]
@app.route("/base/stats/print", methods=["GET"])
def base_stats_all_print() :
    result = base_stats_print_all()
    print(result)
    return result

# 포켓몬 종족값 목록 -> 아이디(번호)를 기준으로 출력 [내림차순]
@app.route("/base/stats/print/pokeno", methods=["GET"])
def base_stats_pokeno_print() :
    result = base_stats_print_pokeno()
    # print(result)
    return result
