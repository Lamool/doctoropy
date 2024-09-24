import pandas as pd
import json

# 포켓몬 종족값 목록 - 기본 : 아이디(번호) 기준 정렬
def base_stats_print_all(data) :
    # 판다스를 이용한 csv를 데이터프레임으로 가져오기
    pokemon_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)
    # print(pokemon_data)

    pokemon_data_df = pokemon_data[["한글이름", "영어이름", "아이디", "이미지", "체력", "공격", "방어", "특수공격", "특수방어", "스피드", "타입"]]
    # print(pokemon_data_df)

    # "체력", "공격", "방어", "특수공격", "특수방어", "스피드"의 합계를 구한 새로운 컬럼 '총합' 추가
    pokemon_data_df['총합'] = pokemon_data_df[["체력", "공격", "방어", "특수공격", "특수방어", "스피드"]].sum(axis=1)

    print(data)
    print(data['sort'])
    print(data['name'])
    if data['sort'] == '내림차순' :     # 내림차순으로 정렬 # 값이 같다면 아이디(번호) 기준 오름차순 정렬 # (ascending=True : 기본값, 오름차순 정렬)
        pokemon_data_df = pokemon_data_df.sort_values(by=[data['name'], '아이디'], ascending=[False, True])   # data['name'] 속성을 내림차순 하겠다
        print(pokemon_data_df)
    else :          # 오름차순으로 정렬
        pokemon_data_df = pokemon_data_df.sort_values(by=[data['name'], '아이디'])  # data['name'] 속성을 오름차순 하겠다
        print(pokemon_data_df)

    # 데이터프레임 객체를 JSON으로 가져오기
    json_pokemon_data = pokemon_data_df.to_json(orient='records', force_ascii=False)
        # to_json() : 데이터프레임 객체 내 데이터를 JSON 변환함수
            # oreint='records' : 각 행마다 하나의 JSON 객체로 구성
            # force_ascii=False : 아스키 문자 사용 여부 : True(아스키), False(아스키 대신 유니코드 utf-8)
    # print(json_pokemon_data)

    # JSON 형식 (문자열 타입)의 py타입(객체타입-리스트/딕셔너리)으로 변환
    result = json.loads(json_pokemon_data)  # import json 모듈 호출
    # print(result)
    return result

def type_trans(type) :
    if type == "normal" :
        kr_type = "노말"
    elif type == "fire" :
        kr_type = "불"
    elif type == "water" :
        kr_type = "물"
    elif type == "electric" :
        kr_type = "전기"
    elif type == "grass" :
        kr_type = "풀"
    elif type == "ice" :
        kr_type = "얼음"
    elif type == "fighting" :
        kr_type = "격투"
    elif type == "poison" :
        kr_type = "독"
    elif type == "ground" :
        kr_type = "땅"
    elif type == "flying" :
        kr_type = "비행"
    elif type == "psychic" :
        kr_type = "에스퍼"
    elif type == "bug" :
        kr_type = "벌레"
    elif type == "rock" :
        kr_type = "바위"
    elif type == "ghost" :
        kr_type = "고스트"
    elif type == "dragon" :
        kr_type = "드래곤"
    elif type == "dark" :
        kr_type = "악"
    elif type == "steel" :
        kr_type = "강철"
    elif type == "fairy" :
        kr_type = "페어리"
    return kr_type
