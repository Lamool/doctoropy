import pandas as pd
import json
from flask import jsonify
import random

# 내 포켓몬 이름, 이미지 찾기
def info_my_pokemon(pokeno) :
    # 판다스를 이용한 csv를 데이터프레임으로 가져오기
    pokemon_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)
    # print(pokemon_data)

    # pokemon_data라는 데이터프레임에서 특정 열(이름, 이미지)만 추출하여 pokemon_data_df라는 새로운 데이터 프레임 만들기
    pokemon_data_df = pokemon_data[["한글이름", "이미지", "아이디"]]
    # print(pokemon_data_df)

    # 받아온 포켓몬 번호가 아이디(포켓몬 번호) 중 해당 하는 값이 있으면 행 추출
        # ex) pokeno = 1 # 아이디 열에 1이 있다면 그 행 추출
    my_pokemon_data = pokemon_data_df[pokemon_data_df["아이디"].isin([pokeno])]
    # print(my_pokemon_data)

    # 데이터프레임 객체를 JSON으로 가져오기
    json_pokemon_data = my_pokemon_data.to_json(orient='records', force_ascii=False)
        # to_json() : 데이터프레임 객체 내 데이터를 JSON 변환함수
            # oreint='records' : 각 행마다 하나의 JSON 객체로 구성
            # force_ascii=False : 아스키 문자 사용 여부 : True(아스키), False(아스키 대신 유니코드 utf-8)
    # print(json_pokemon_data)

    # JSON 형식 (문자열 타입)의 py타입(객체타입-리스트/딕셔너리)으로 변환
    result = json.loads(json_pokemon_data)  # import json 모듈 호출
    # print(result)
    return result

# 내 포켓몬 진화하기
def evolve_my_pokemon(stage) :
    # 판다스를 이용한 csv를 데이터프레임으로 가져오기
    pokemon_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)
    # print(pokemon_data)

    # pokemon_data라는 데이터프레임에서 특정 열만 추출하여 pokemon_data_df라는 새로운 데이터 프레임 만들기
    pokemon_data_df = pokemon_data[["한글이름", "아이디", "체력", "공격", "방어", "특수공격", "특수방어", "스피드"]]
    # print(pokemon_data_df)

    # "체력", "공격", "방어", "특수공격", "특수방어", "스피드"의 합계를 구한 새로운 컬럼 '총합' 추가
    pokemon_data_df['총합'] = pokemon_data_df[["체력", "공격", "방어", "특수공격", "특수방어", "스피드"]].sum(axis=1)

    new_pokeno = 0  # 새로운 포켓몬 번호를 담을 변수

    # 진화하고자 하는 단계에 맞는 포켓몬이 나올 때까지 난수 생성 무한반복
    while True :
        # 난수 생성 -> 포켓몬 번호
        random_num = random.randint(1, len(pokemon_data_df['총합']))
        print(random_num)

        # 난수(새 포켓몬 번호)의 총합 값 가져오기 ("총합" 열의 random_num 번째 값)
        random_num_total = int(pokemon_data_df.loc[random_num, '총합'])
        print(random_num_total)

        # 총합 -> 최소 : 175, 최대 : 720
        if stage >= 6 :     # 6단계 진화 시 # 총합이 601 ~ 800 사이인 포켓몬으로 진화 가능
            print('총합 : 601 ~ 800')
            if 601 <= random_num_total <= 800 :
                new_pokeno = random_num
                break
        elif stage >= 5 :     # 5단계 진화 시 # 총합이 501 ~ 600 사이인 포켓몬으로 진화 가능
            print('총합 : 501 ~ 600')
            if 501 <= random_num_total <= 600 :
                new_pokeno = random_num
                break
        elif stage >= 4 :     # 4단계 진화 시 # 총합이 401 ~ 500 사이인 포켓몬으로 진화 가능
            print('총합 : 401 ~ 500')
            if 401 <= random_num_total <= 500 :
                new_pokeno = random_num
                break
        elif stage >= 3 :     # 3단계 진화 시 # 총합이 301 ~ 400 사이인 포켓몬으로 진화 가능
            print('총합 : 301 ~ 400')
            if 301 <= random_num_total <= 400 :
                new_pokeno = random_num
                break
        elif stage >= 2 :     # 2단계 진화 시 # 총합이 201 ~ 300 사이인 포켓몬으로 진화 가능
            print('총합 : 201 ~ 300')
            if 201 <= random_num_total <= 300 :
                new_pokeno = random_num
                break
        elif stage >= 1 :     # 1단계 진화 시 # 총합이 101 ~ 200 사이인 포켓몬으로 진화 가능
            print('총합 : 101 ~ 200')
            if 101 <= random_num_total <= 200 :
                new_pokeno = random_num
                break

    result = jsonify({ 'new_pokeno': new_pokeno })
    return result

