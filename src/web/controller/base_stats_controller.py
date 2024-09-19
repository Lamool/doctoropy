from src.web.app import *
from src.web.service.base_stats_service import *

# 포켓몬 종족값 목록 -> 아이디(번호)를 기준으로 출력 [오름차순]
# @app.route("/base/stats/print", methods=["POST"])
# def base_stats_all_print() :
#     data = request.json  # JSON 형식으로 데이터 받기
#     print(data)  # 서버 콘솔에 출력
#     if data['data'] == 101010 :
#         print("aaaaa")
#     else :
#         print("bbbbb")
#     result = base_stats_print_all()
#     print(result)
#     return result
#
# # 포켓몬 종족값 목록 -> 아이디(번호)를 기준으로 출력 [내림차순]
# @app.route("/base/stats/print/pokeno", methods=["GET"])
# def base_stats_pokeno_print() :
#     result = base_stats_print_pokeno()
#     # print(result)
#     return result








# 포켓몬 종족값 목록 -> 아이디(번호)를 기준으로 출력 [오름차순]
@app.route("/base/stats/print", methods=["POST"])
def base_stats_all_print() :
    # data = request.json  # JSON 형식으로 데이터 받기
    # print(data)  # 서버 콘솔에 출력
    # if data['data'] == 101010 :
    #     print("aaaaa")
    # else :
    #     print("bbbbb")
    result = base_stats_print_all()
    print(result)
    return result

# 포켓몬 종족값 목록 -> 아이디(번호)를 기준으로 출력 [내림차순]
@app.route("/base/stats/print/pokeno", methods=["GET"])
def base_stats_pokeno_print() :
    result = base_stats_print_pokeno()
    # print(result)
    return result


# 포켓몬 종족값 목록 -> 포켓몬명을 기준으로 출력
@app.route("/base/stats/print/pokename", methods=["POST"])
def base_stats_pokename_print() :
    data = request.json  # JSON 형식으로 데이터 받기
    print(data)  # 서버 콘솔에 출력

    result = base_stats_print_pokename(data)
    # print(result)
    return result



