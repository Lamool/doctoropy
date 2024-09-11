import random

import pandas as pd
import json

df = pd.read_csv("datapokemon.csv", encoding="utf-8")
df2 = df[['한글이름','아이디','영어이름','이미지']]
# print(df2)
df2_list = df2.values.tolist()
# print(df2_list)
# ////////////////////////////////////////////////////////////////
df3 = df[["한글이름"]]
print(len(df3))
df3_list = df3.values.tolist()

pokemon = []
for i in df3_list :
    pokemon += i
print(pokemon)

import random
set = int(input(" 4,8,16 선택"))
print(set)

pokemon1 = random.sample(pokemon, set)
print(pokemon1)
라운드 = 1  # 처음시작 라운드
라운드to대진 = {
    1: "32강",
    2: "16강",
    3: "8강",
    4: "2강",
    5: "결승전"
}

while len(pokemon1) > 1:  # 최종 우승자 1명이 나올때까지 반복
    print(f"\n=== {라운드to대진[라운드]} ===")
    승리포켓몬 = []  # 승자들만 추가하는 리스트
    random.shuffle(pokemon1)  # 참가자들 랜덤 셔플

    for i in range(0, len(pokemon1) - 1, 2):
        대결 = [pokemon1[i], pokemon1[i + 1]]  # 참가자들의 앞에서 두명씩 짝을지어 대결
        while True:
            print(f"누가 이길까요? {대결[0]} vs {대결[1]}")
            승자선택 = int(input("이기는 쪽을 선택하세요 (1 또는 2): "))  # 사용자 입력
            if 승자선택 == 1 or 승자선택 == 2:
                승자 = 대결[승자선택 - 1]  # -1 하는 이유 : 리스트는 0번째 부터
                승리포켓몬.append(승자)
                break
            else:  # 1,2 말고 다른것 입력한사람
                print("=" * 20)
                print("잘못된 입력입니다. 1 또는 2를 입력하세요.")

    print("남은 사람들", 승리포켓몬)
    pokemon1 = 승리포켓몬  # 참가자들중 이긴사람(절반)만 살아남고 다시 다음라운드 참가자로 진행
    라운드 += 1  # 다음 라운드 진행

print(f"\n최종 포켓몬 {pokemon1[0]} 입니다!")  # 최종 이상형 선정



from flask import Flask
app = Flask(__name__)

from flask_cors import CORS
CORS(app)

@app.route("/rank")
def index():
    jsonData = df2.to_json(orient='records', force_ascii=False)
    result = json.loads(jsonData)
    return result
#
# if __name__ == "__main__" :
#     app.run()