# rate_pred_service.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from src.web.model.rate_class import *

type_value_a = 0

def poke_list_take(data) :
    result = []
    for d in data:
        record_list = [d["rhp"], d["ratk"], d["rdef"], d["rspd"], d["rspatk"], d["rspdef"],d["rscore"], d["rrate"], d["rpokeindex"], d["rskillpower"], d["rresult"]]
        result.append(record_list)

    record = pd.DataFrame(result, columns=("체력", "공격", "방어", "스피드", "특수공격", "특수방어", "점수", "승률", "포켓몬_번호", "사용한_기술의_위력", "결과"))
    record.index = record.index + 1
    print(record)

    record.to_csv("./service/poke_rate_predict_record.csv", index=True)


def poke_rate_predict_model():
    data = pd.read_csv("./service/poke_rate_predict_record.csv", encoding="utf-8", index_col=0)
    x1 = data[["체력", "공격", "방어", "스피드", "특수공격", "특수방어", "점수", "사용한_기술의_위력"]]

    y1 = data["승률"]

    x_train1, x_test1, y_train1, y_test1 = train_test_split(x1, y1, test_size=0.3, random_state=0)

    lr_model = LinearRegression()

    lr_model.fit(x_train1, y_train1)

    y_predict1 = lr_model.predict(x_test1)
    print(y_predict1)

    MSE = mean_squared_error(y_test1, y_predict1)
    RMSE = np.sqrt(MSE)
    R2_SCORE = r2_score(y_test1, y_predict1)
    print(f" MSE = {MSE}")  # MSE = 349.8993110412591
    print(f" RMSE = {RMSE}")  # RMSE = 18.70559571468546
    print(f" R2_SCORE = {R2_SCORE}")  # R2_SCORE = 0.5841816544889874

    return lr_model

def poke_rate_predict_result(poke_info_list):
    print(poke_info_list)
    lr_model = poke_rate_predict_model()
    print(lr_model)

    x_pred = [poke_info_list]
    new_poke_rate_predict = lr_model.predict(x_pred)

    return new_poke_rate_predict


def poke_score_cal(n1, m1):
    poke_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)
    print(poke_data)

    poke_data_one = poke_data.iloc[n1]
    print(m1)

    a_pokemon = rate_poke_mon_A(poke_data_one["체력"], poke_data_one["공격"], poke_data_one["방어"], poke_data_one["특수공격"], poke_data_one["특수방어"], poke_data_one["스피드"], poke_data_one["타입"], int(m1))
    poke_score = poke_rate_cal(a_pokemon)

    poke_info_list = [poke_data_one["체력"], poke_data_one["공격"], poke_data_one["방어"], poke_data_one["스피드"], poke_data_one["특수공격"], poke_data_one["특수방어"], poke_score, m1]

    return poke_info_list

def poke_rate_cal(a_pokemon) :
    type_value_a = type_cal(a_pokemon.type)
    total_score_a = (a_pokemon.hp * 0.15) + (a_pokemon.atk * 0.2 * type_value_a) + (a_pokemon.spe_atk * 0.2 * (type_value_a * 0.5)) + (a_pokemon._def * 0.15) + (a_pokemon.spe_def * 0.15) + (a_pokemon.speed * 0.15) + (a_pokemon.sk_dam * 0.25)

    return round(total_score_a, 2)


def type_cal(type_a) :
    # 0. 노말은 바위(12)와 강철(16)에게 0.5배의 데미지, 고스트(13)에게 0배의 데미지
    global type_value_a
    if type_a == "normal" :
        type_value_a = 0.8889
    # 1. 불꽃은 풀(4), 얼음(5), 벌레(11), 강철(16)에게 2배의 데미지, 불꽃(1), 물(2), 바위(12), 드래곤(14)에게 0.5배의 데미지
    elif type_a == "fire" :
        type_value_a = 1.1111
    # 2. 물은 불꽃(1), 땅(8), 바위(12)에게 2배의 데미지, 물(2), 풀(4), 드래곤(14)에게 0.5배의 데미지
    elif type_a == "water" :
        type_value_a = 1.0833
    # 3. 전기는 물(2), 비행(9)에게 2배의 데미지, 전기(3), 풀(4), 드래곤(14)에게 0.5배의 데미지, 땅(8)에게 0배의 데미지
    elif type_a == "electric" :
        type_value_a = 0.9722
    # 4. 풀은 물(2), 땅(8), 바위(12)에게 2배의 데미지, 불꽃(1), 풀(4), 독(7), 비행(9), 벌레(11), 드래곤(14), 강철(16)에게 0.5배의 데미지
    elif type_a == "grass" :
        type_value_a = 1
    # 5. 얼음은 풀(4), 땅(8), 비행(9), 드래곤(14)에게 2배의 데미지, 불꽃(1), 물(2), 얼음(5), 강철(16)에게 0.5배의 데미지
    elif type_a == "ice" :
        type_value_a = 1.1111
    # 6. 격투는 노말(0), 얼음(5), 바위(12), 악(15), 강철(16)에게 2배의 데미지, 독(7), 비행(9), 에스퍼(10), 벌레(11), 페어리(17)에게 0.5배의 데미지, 고스트(13)에게 0배의 데미지
    elif type_a == "fighting" :
        type_value_a = 1.0833
    # 7. 독은 풀(4), 페어리(17)에게 2배의 데미지, 독(7), 땅(8), 바위(12), 고스트(13)에게 0.5배의 데미지, 강철(16)에게 0배의 데미지
    elif type_a == "poison" :
        type_value_a = 0.9444
    # 8. 땅은 불꽃(1), 전기(3), 독(7), 바위(12), 강철(16)에게 2배의 데미지, 풀(4), 벌레(11)에게 0.5배의 데미지, 비행(9)에게 0배의 데미지
    elif type_a == "ground" :
        type_value_a = 1.1111
    # 9. 비행은 풀(4), 격투(6), 벌레(9)에게 2배의 데미지, 전기(3), 바위(12), 강철(16)에게 0.5배의 데미지
    elif type_a == "flying" :
        type_value_a = 1.0833
    # 10. 에스퍼는 격투(6), 독(7)에게 2배의 데미지, 에스퍼(10), 강철(16)에게 0.5배의 데미지, 악(15)에게 0배의 데미지
    elif type_a == "psychic" :
        type_value_a = 1
    # 11. 벌레는 풀(4), 에스퍼(10), 악(15)에게 2배의 데미지, 불꽃(1), 격투(6), 땅(8), 비행(9), 고스트(13), 강철(16), 페어리(17)에게 0.5배의 데미지
    elif type_a == "bug" :
        type_value_a = 0.9722
    # 12. 바위는 불꽃(1), 얼음(5), 비행(9), 벌레(11)에게 2배의 데미지, 격투(6), 땅(8), 강철(16)에게 0.5배의 데미지
    elif type_a == "rock" :
        type_value_a = 1.1388
    # 13. 고스트는 에스퍼(10), 고스트(13)에게 2배의 데미지, 악(15)에게 0.5배의 데미지, 노말에게 0배의 데미지
    elif type_a == "ghost" :
        type_value_a = 1.0277
    # 14. 드래곤은 드래곤(14)에게 2배의 데미지, 강철(16)에게 0.5배의 데미지, 페어리(17)에게 0배의 데미지
    elif type_a == "dragon" :
        type_value_a = 0.9722
    # 15. 악은 에스퍼(10), 고스트(13)에게 2배의 데미지, 악(15), 페어리(17)에게 0.5배의 데미지
    elif type_a == "dark" :
        type_value_a = 1.0555
    # 16. 강철은 얼음(5), 바위(12), 페어리(17)에게 2배의 데미지, 불꽃(1), 물(2), 전기(3), 강철(16)에게 0.5배의 데미지
    elif type_a == "steel" :
        type_value_a = 1.0555
    # 17. 페어리는 격투(6), 드래곤(14), 악(15)에게 2배의 데미지, 불꽃(1), 독(7), 강철(16)에게 0.5배의 데미지
    elif type_a == "fairy" :
        type_value_a = 1.0833

    return type_value_a
###