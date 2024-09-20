from src.web.app import *
from src.web.service.base_stats_service import *

# 포켓몬 종족값 목록 - 기본 : 아이디(번호) 기준 정렬
@app.route("/base/stats/print/all", methods=["POST"])
def base_stats_all_print() :
    data = request.json  # JSON 형식으로 데이터 받기
    print(data)  # 서버 콘솔에 출력

    result = base_stats_print_all(data)
    # print(result)
    return result



