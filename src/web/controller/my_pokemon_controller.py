from src.web.app import *
from src.web.service.my_pokemon_service import *

# 내 포켓몬 이름, 이미지 찾기
@app.route("/mypoke/info", methods=["GET"])
def my_pokemon_info() :
    # 쿼리 스트링으로 보내온 데이터 포켓몬 번호를 가져오기 # 데이터가 문자열이기 때문에 int형으로 변환해줌
    pokeno = int(request.args.get('pokeno'))
    # print(pokeno)
    # print(type(pokeno))

    result = info_my_pokemon(pokeno)
    # print(result)
    return result

# 내 포켓몬 진화하기
@app.route("/mypoke/evolve", methods=["GET"])
def my_pokemon_evolve() :
    # 쿼리 스트링으로 보내온 데이터 포켓몬 번호를 가져오기 # 데이터가 문자열이기 때문에 int형으로 변환해줌
    stage = int(request.args.get('stage'))
    # print(stage)
    # print(type(stage))

    result = evolve_my_pokemon(stage)
    # print(result)
    return result

