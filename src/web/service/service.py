# service
import json

import pandas as pd
from pandas import read_csv

from src.web.model.rate_class import *

# poke_data = pd.read_csv("datapokemon.csv", encoding="utf-8", index_col=0)
# poke_skill_data = pd.read_csv("skilldata.csv", encoding="utf-8",index_col=0)
# # print(poke_data)f
# new_poke_skill_data = poke_skill_data.fillna(0)
# # print(new_poke_skill_data)
# # print(poke_data.iloc[1000])
type_value_a = 0
type_value_b = 0

rate_dict = {}

# n1 = int(input("A포켓몬 번호 입력"))
# m1 = int(input("A포켓몬 사용 스킬 번호 입력"))
#
# n2 = int(input("B포켓몬 번호 입력"))
# m2 = int(input("B포켓몬 사용 스킬 번호 입력"))

def poke_info_num() :
    poke_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)
    poke_data_all_info = poke_data[["한글이름","영어이름"]]
    poke_data_json_loads = poke_data_all_info.to_json(orient='records', force_ascii=False)
    poke_data_result = json.loads(poke_data_json_loads)
    return poke_data_result

def poke_skill_num() :
    poke_skill_data = pd.read_csv("./service/skilldata.csv", encoding="utf-8", index_col=0)
    new_poke_skill_data = poke_skill_data.fillna(0)
    poke_skill_data_info = new_poke_skill_data[["스킬이름","타입"]]
    poke_skill_json_loads = poke_skill_data_info.to_json(orient='records', force_ascii=False)
    poke_skill_result = json.loads(poke_skill_json_loads)
    return poke_skill_result

def poke_new_skill_info(kr_name) :
    result = []
    poke_each_skill_data = pd.read_csv("./service/new_poke_each_skill_data.csv", encoding="utf-8", index_col=0)
    poke_each_skill_data_poke_name = poke_each_skill_data["포켓몬"]
    poke_each_skill_data_dam = poke_each_skill_data["위력"]
    poke_each_skill_data_skill_name = poke_each_skill_data["스킬이름"]
    poke_each_skill_data_type_name = poke_each_skill_data["타입"]
    for i, poke_name in enumerate(poke_each_skill_data_poke_name):
        if kr_name == poke_name:
            result.append({"인덱스": i,
                           "기술이름": poke_each_skill_data_skill_name.iloc[i],
                           "타입": poke_each_skill_data_type_name.iloc[i],
                           "위력": int(poke_each_skill_data_dam.iloc[i]),
                           "포켓몬": poke_name})
    return result

def poke_rate_data_info(n) :
    poke_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)
    poke_data_one = poke_data.iloc[n]
    print( poke_data_one  )
    poke_info_dict = {"한글이름" : poke_data_one["한글이름"], "영어이름" : poke_data_one["영어이름"], "체력": int( poke_data_one["체력"] ) , "공격" : int(poke_data_one["공격"]), "방어" : int(poke_data_one["방어"]), "특수공격" : int(poke_data_one["특수공격"]), "특수방어" : int(poke_data_one["특수방어"]), "스피드" : int(poke_data_one["스피드"]), "타입" : poke_data_one["타입"], "이미지" : poke_data_one["이미지"]}
    print( poke_info_dict )

    return poke_info_dict


def poke_rate_skill_info(n) :
    poke_skill_data = pd.read_csv("./service/skilldata.csv", encoding="utf-8", index_col=0)
    new_poke_skill_data = poke_skill_data.fillna(0)
    poke_skill_data_one = new_poke_skill_data.iloc[n]
    poke_skill_info_dict = {"스킬_이름" : poke_skill_data_one["스킬이름"], "타입" : poke_skill_data_one["타입"]}

    return poke_skill_info_dict

def poke(n1, m1, n2, m2):
    poke_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)
    print(poke_data)

    # print(poke_data.iloc[1000])
    poke_data_one = poke_data.iloc[n1]
    print(m1)
    poke_data_two = poke_data.iloc[n2]
    print(m2)
    a_pokemon = rate_poke_mon_A(poke_data_one["체력"], poke_data_one["공격"], poke_data_one["방어"], poke_data_one["특수공격"], poke_data_one["특수방어"], poke_data_one["스피드"], poke_data_one["타입"], int(m1))
    b_pokemon = rate_poke_mon_A(poke_data_two["체력"], poke_data_two["공격"], poke_data_two["방어"], poke_data_two["특수공격"], poke_data_two["특수방어"], poke_data_two["스피드"], poke_data_two["타입"], int(m2))
    rate_dict = rate_cal(a_pokemon, b_pokemon)

    return rate_dict

def rate_cal (a_pokemon, b_pokemon) :
    type_value_a = type_cal_a(a_pokemon.type, b_pokemon.type)
    type_value_b = type_cal_b(a_pokemon.type, b_pokemon.type)
    print(type_value_a)
    print(type_value_b)
    total_score_a = (a_pokemon.hp * 0.15) + (a_pokemon.atk * 0.2 * type_value_a) + (a_pokemon.spe_atk * 0.2 * (type_value_a * 0.5)) + (a_pokemon._def * 0.15) + (a_pokemon.spe_def * 0.15) + (a_pokemon.speed * 0.15) + (a_pokemon.sk_dam * 0.25)
    total_score_b = (b_pokemon.hp * 0.15) + (b_pokemon.atk * 0.2 * type_value_b) + (b_pokemon.spe_atk * 0.2 * (type_value_b * 0.5)) + (b_pokemon._def * 0.15) + (b_pokemon.spe_def * 0.15) + (b_pokemon.speed * 0.15) + (b_pokemon.sk_dam * 0.25)
    print(total_score_a)
    print(total_score_b)
    if total_score_a > total_score_b :
        print("A 스코어가 더 큼")
        ratio_a = (total_score_a / total_score_b)
        rate_a = round(50 * ratio_a, 2)
        if ratio_a >= 2 :
            rate_a = 100
        rate_b = 100 - rate_a
        rate_dict["A_포켓몬_점수"] = round(total_score_a, 2)
        rate_dict["B_포켓몬_점수"] = round(total_score_b, 2)
        rate_dict["A_포켓몬_승률"] = round(rate_a, 2)
        rate_dict["B_포켓몬_승률"] = round(rate_b, 2)
        print(rate_a)
        print(rate_b)
    elif total_score_b > total_score_a:
        print("B 스코어가 더 큼")
        ratio_b = (total_score_b / total_score_a)
        rate_b = round(50 * ratio_b, 2)
        if ratio_b >= 2 :
            rate_b = 100
        rate_a = 100 - rate_b
        rate_dict["A_포켓몬_점수"] = round(total_score_a, 2)
        rate_dict["B_포켓몬_점수"] = round(total_score_b, 2)
        rate_dict["A_포켓몬_승률"] = round(rate_a, 2)
        rate_dict["B_포켓몬_승률"] = round(rate_b, 2)
        print(rate_a)
        print(rate_b)
    elif total_score_a == total_score_b :
        rate_dict["A_포켓몬_점수"] = round(total_score_a, 2)
        rate_dict["B_포켓몬_점수"] = round(total_score_b, 2)
        rate_dict["A_포켓몬_승률"] = 50
        rate_dict["B_포켓몬_승률"] = 50

    return rate_dict


def type_cal_a(type_a, type_b) :
    # 0. 노말은 바위(12)와 강철(16)에게 0.5배의 데미지, 고스트(13)에게 0배의 데미지
    global type_value_a
    if type_a == "normal" :
        if type_b == "rock" or type_b == "steel" :
            type_value_a = 0.5
        elif type_b == "ghost" :
            type_value_a = 0
        else:
            type_value_a = 1
    # 1. 불꽃은 풀(4), 얼음(5), 벌레(11), 강철(16)에게 2배의 데미지, 불꽃(1), 물(2), 바위(12), 드래곤(14)에게 0.5배의 데미지
    elif type_a == "fire" :
        if type_b == "grass" or type_b == "ice" or type_b == "bug" or type_b == "steel" :
            type_value_a = 2
        elif type_b == "fire" or type_b == "water" or type_b == "rock" or type_b == "dragon" :
            type_value_a = 0.5
        else:
            type_value_a = 1
    # 2. 물은 불꽃(1), 땅(8), 바위(12)에게 2배의 데미지, 물(2), 풀(4), 드래곤(14)에게 0.5배의 데미지
    elif type_a == "water" :
        if type_b == "fire" or type_a == "ground" or type_b == "rock" :
            type_value_a = 2
        elif type_b == "water" or type_b == "grass" or type_b == "dragon" :
            type_value_a = 0.5
        else :
            type_value_a = 1
    # 3. 전기는 물(2), 비행(9)에게 2배의 데미지, 전기(3), 풀(4), 드래곤(14)에게 0.5배의 데미지, 땅(8)에게 0배의 데미지
    elif type_a == "electric" :
        if type_b == "water" or type_b == "flying" :
            type_value_a = 2
        elif type_b == "electric" or type_b == "grass" or type_b == "dragon" :
            type_value_a = 0.5
        elif type_b == "ground" :
            type_value_a = 0
        else :
            type_value_a = 1
    # 4. 풀은 물(2), 땅(8), 바위(12)에게 2배의 데미지, 불꽃(1), 풀(4), 독(7), 비행(9), 벌레(11), 드래곤(14), 강철(16)에게 0.5배의 데미지
    elif type_a == "grass" :
        if type_b == "water" or type_b == "ground" or type_b == "rock" :
            type_value_a = 2
        elif type_b == "fire" or type_b == "grass" or type_b == "flying" or type_b == "bug" or type_b == "dragon" or type_b == "steel" :
            type_value_a = 0.5
        else :
            type_value_a = 1
    # 5. 얼음은 풀(4), 땅(8), 비행(9), 드래곤(14)에게 2배의 데미지, 불꽃(1), 물(2), 얼음(5), 강철(16)에게 0.5배의 데미지
    elif type_a == "ice" :
        if type_b == "grass" or type_b == "ground" or type_b == "flying" or type_b == "dragon" :
            type_value_a = 2
        elif type_b == "fire" or type_b == "water" or type_b == "ice" or type_b == "steel" :
            type_value_a = 0.5
        else :
            type_value_a = 1
    # 6. 격투는 노말(0), 얼음(5), 바위(12), 악(15), 강철(16)에게 2배의 데미지, 독(7), 비행(9), 에스퍼(10), 벌레(11), 페어리(17)에게 0.5배의 데미지, 고스트(13)에게 0배의 데미지
    elif type_a == "fighting" :
        if type_b == "normal" or type_b == "ice" or type_b == "rock" or type_b == "dark" or type_b == "steel" :
            type_value_a = 2
        elif type_b == "poison" or type_b == "flying" or type_b == "psychic" or type_b == "bug" or type_b == "fairy" :
            type_value_a = 0.5
        elif type_b == "ghost" :
            type_value_a = 0
        else :
            type_value_a = 1
    # 7. 독은 풀(4), 페어리(17)에게 2배의 데미지, 독(7), 땅(8), 바위(12), 고스트(13)에게 0.5배의 데미지, 강철(16)에게 0배의 데미지
    elif type_a == "poison" :
        if type_b == "grass" or type_b == "fairy" :
            type_value_a = 2
        elif type_b == "poison" or type_b == "ground" or type_b == "rock" or type_b == "ghost" :
            type_value_a = 0.5
        elif type_b == "steel" :
            type_value_a = 0
        else:
            type_value_a = 1
    # 8. 땅은 불꽃(1), 전기(3), 독(7), 바위(12), 강철(16)에게 2배의 데미지, 풀(4), 벌레(11)에게 0.5배의 데미지, 비행(9)에게 0배의 데미지
    elif type_a == "ground" :
        if type_b == "fire" or type_b == "electric" or type_b == "poison" or type_b == "rock" :
            type_value_a = 2
        elif type_b == "grass" or type_b == "bug" :
            type_value_a = 0.5
        elif type_b == "flying" :
            type_value_a = 0
        else :
            type_value_a = 1
    # 9. 비행은 풀(4), 격투(6), 벌레(9)에게 2배의 데미지, 전기(3), 바위(12), 강철(16)에게 0.5배의 데미지
    elif type_a == "flying" :
        if type_b == "grass" or type_b == "fighting" or type_b == "bug" :
            type_value_a = 2
        elif type_b == "electric" or type_b == "rock" or type_b == "steel" :
            type_value_a = 0.5
        else :
            type_value_a = 1
    # 10. 에스퍼는 격투(6), 독(7)에게 2배의 데미지, 에스퍼(10), 강철(16)에게 0.5배의 데미지, 악(15)에게 0배의 데미지
    elif type_a == "psychic" :
        if type_b == "fighting" or type_b == "poison" :
            type_value_a = 2
        elif type_b == "psychic" or type_b == "steel" :
            type_value_a = 0.5
        elif type_b == "dark" :
            type_value_a = 0
        else :
            type_value_a = 1
    # 11. 벌레는 풀(4), 에스퍼(10), 악(15)에게 2배의 데미지, 불꽃(1), 격투(6), 땅(8), 비행(9), 고스트(13), 강철(16), 페어리(17)에게 0.5배의 데미지
    elif type_a == "bug" :
        if type_b == "grass" or type_b == "psychic" or type_b == "dark" :
            type_value_a = 2
        elif type_b == "fire" or type_b == "fighting" or type_b == "ground" or type_b == "flying" or type_b == "ghost" or type_b == "steel" or type_b == "fairy" :
            type_value_a = 0.5
        else :
            type_value_a = 1
    # 12. 바위는 불꽃(1), 얼음(5), 비행(9), 벌레(11)에게 2배의 데미지, 격투(6), 땅(8), 강철(16)에게 0.5배의 데미지
    elif type_a == "rock" :
        if type_b == "fire" or type_b == "ice" or type_b == "flying" or type_b == "bug" :
            type_value_a = 2
        elif type_b == "fighting" or type_b == "ground" or type_b == "steel" :
            type_value_a = 0.5
        else :
            type_value_a = 1
    # 13. 고스트는 에스퍼(10), 고스트(13)에게 2배의 데미지, 악(15)에게 0.5배의 데미지, 노말에게 0배의 데미지
    elif type_a == "ghost" :
        if type_b == "psychic" or type_b == "ghost" :
            type_value_a = 2
        elif type_b == "dark" :
            type_value_a = 0.5
        elif type_b == "normal" :
            type_value_a = 0
        else :
            type_value_a = 1
    # 14. 드래곤은 드래곤(14)에게 2배의 데미지, 강철(16)에게 0.5배의 데미지, 페어리(17)에게 0배의 데미지
    elif type_a == "dragon" :
        if type_b == "dragon" :
            type_value_a = 2
        elif type_b == "steel" :
            type_value_a = 0.5
        elif type_b == "fairy" :
            type_value_a = 0
        else :
            type_value_a = 1
    # 15. 악은 에스퍼(10), 고스트(13)에게 2배의 데미지, 악(15), 페어리(17)에게 0.5배의 데미지
    elif type_a == "dark" :
        if type_b == "psychic" or type_b == "ghost" :
            type_value_a = 2
        elif type_b == "dark" or type_b == "fairy" :
            type_value_a = 0.5
        else:
            type_value_a = 1
    # 16. 강철은 얼음(5), 바위(12), 페어리(17)에게 2배의 데미지, 불꽃(1), 물(2), 전기(3), 강철(16)에게 0.5배의 데미지
    elif type_a == "steel" :
        if type_b == "ice" or type_b == "rock" or type_b == "fairy" :
            type_value_a = 2
        elif type_b == "fire" or type_b == "ice" or type_b == "electric" or type_b == "steel" :
            type_value_a = 0.5
        else :
            type_value_a = 1
    # 17. 페어리는 격투(6), 드래곤(14), 악(15)에게 2배의 데미지, 불꽃(1), 독(7), 강철(16)에게 0.5배의 데미지
    elif type_a == "fairy" :
        if type_b == "fighting" or type_b == "dragon" or type_b == "dark" :
            type_value_a = 2
        elif type_b == "fire" or type_b == "poison" or type_b == "steel" :
            type_value_a = 0.5
        else :
            type_value_a = 1

    return type_value_a

"""
=====================================================================================================

"""

def type_cal_b(type_a, type_b) :
    # 0. 노말은 바위(12)와 강철(16)에게 0.5배의 데미지, 고스트(13)에게 0배의 데미지
    global type_value_b
    if type_b == "normal" :
        if type_a == "rock" or type_a == "steel" :
            type_value_b = 0.5
        elif type_a == "ghost" :
            type_value_b = 0
        else:
            type_value_b = 1
    # 1. 불꽃은 풀(4), 얼음(5), 벌레(11), 강철(16)에게 2배의 데미지, 불꽃(1), 물(2), 바위(12), 드래곤(14)에게 0.5배의 데미지
    elif type_b == "fire" :
        if type_a == "grass" or type_a == "ice" or type_a == "bug" or type_a == "steel" :
            type_value_b = 2
        elif type_a == "fire" or type_a == "water" or type_a == "rock" or type_a == "dragon" :
            type_value_b = 0.5
        else:
            type_value_b = 1
    # 2. 물은 불꽃(1), 땅(8), 바위(12)에게 2배의 데미지, 물(2), 풀(4), 드래곤(14)에게 0.5배의 데미지
    elif type_b == "water" :
        if type_a == "fire" or type_a == "ground" or type_a == "rock" :
            type_value_b = 2
        elif type_a == "water" or type_a == "grass" or type_a == "dragon" :
            type_value_b = 0.5
        else :
            type_value_b = 1
    # 3. 전기는 물(2), 비행(9)에게 2배의 데미지, 전기(3), 풀(4), 드래곤(14)에게 0.5배의 데미지, 땅(8)에게 0배의 데미지
    elif type_b == "electric" :
        if type_a == "water" or type_a == "flying" :
            type_value_b = 2
        elif type_a == "electric" or type_a == "grass" or type_a == "dragon" :
            type_value_b = 0.5
        elif type_a == "ground" :
            type_value_b = 0
        else :
            type_value_b = 1
    # 4. 풀은 물(2), 땅(8), 바위(12)에게 2배의 데미지, 불꽃(1), 풀(4), 독(7), 비행(9), 벌레(11), 드래곤(14), 강철(16)에게 0.5배의 데미지
    elif type_b == "grass" :
        if type_a == "water" or type_a == "ground" or type_a == "rock" :
            type_value_b = 2
        elif type_a == "fire" or type_a == "grass" or type_a == "flying" or type_a == "bug" or type_a == "dragon" or type_a == "steel" :
            type_value_b = 0.5
        else :
            type_value_b = 1
    # 5. 얼음은 풀(4), 땅(8), 비행(9), 드래곤(14)에게 2배의 데미지, 불꽃(1), 물(2), 얼음(5), 강철(16)에게 0.5배의 데미지
    elif type_b == "ice" :
        if type_a == "grass" or type_a == "ground" or type_a == "flying" or type_a == "dragon" :
            type_value_b = 2
        elif type_a == "fire" or type_a == "water" or type_a == "ice" or type_a == "steel" :
            type_value_b = 0.5
        else :
            type_value_b = 1
    # 6. 격투는 노말(0), 얼음(5), 바위(12), 악(15), 강철(16)에게 2배의 데미지, 독(7), 비행(9), 에스퍼(10), 벌레(11), 페어리(17)에게 0.5배의 데미지, 고스트(13)에게 0배의 데미지
    elif type_b == "fighting" :
        if type_a == "normal" or type_a == "ice" or type_a == "rock" or type_a == "dark" or type_a == "steel" :
            type_value_b = 2
        elif type_a == "poison" or type_a == "flying" or type_a == "psychic" or type_a == "bug" or type_a == "fairy" :
            type_value_b = 0.5
        elif type_a == "ghost" :
            type_value_b = 0
        else :
            type_value_b = 1
    # 7. 독은 풀(4), 페어리(17)에게 2배의 데미지, 독(7), 땅(8), 바위(12), 고스트(13)에게 0.5배의 데미지, 강철(16)에게 0배의 데미지
    elif type_b == "poison" :
        if type_a == "grass" or type_a == "fairy" :
            type_value_b = 2
        elif type_a == "poison" or type_a == "ground" or type_a == "rock" or type_a == "ghost" :
            type_value_b = 0.5
        elif type_a == "steel" :
            type_value_b = 0
        else:
            type_value_b = 1
    # 8. 땅은 불꽃(1), 전기(3), 독(7), 바위(12), 강철(16)에게 2배의 데미지, 풀(4), 벌레(11)에게 0.5배의 데미지, 비행(9)에게 0배의 데미지
    elif type_b == "ground" :
        if type_a == "fire" or type_a == "electric" or type_a == "poison" or type_a == "rock" :
            type_value_b = 2
        elif type_a == "grass" or type_a == "bug" :
            type_value_b = 0.5
        elif type_a == "flying" :
            type_value_b = 0
        else :
            type_value_b = 1
    # 9. 비행은 풀(4), 격투(6), 벌레(9)에게 2배의 데미지, 전기(3), 바위(12), 강철(16)에게 0.5배의 데미지
    elif type_b == "flying" :
        if type_a == "grass" or type_a == "fighting" or type_a == "bug" :
            type_value_b = 2
        elif type_a == "electric" or type_a == "rock" or type_a == "steel" :
            type_value_b = 0.5
        else :
            type_value_b = 1
    # 10. 에스퍼는 격투(6), 독(7)에게 2배의 데미지, 에스퍼(10), 강철(16)에게 0.5배의 데미지, 악(15)에게 0배의 데미지
    elif type_b == "psychic" :
        if type_a == "fighting" or type_a == "poison" :
            type_value_b = 2
        elif type_a == "psychic" or type_a == "steel" :
            type_value_b = 0.5
        elif type_a == "dark" :
            type_value_b = 0
        else :
            type_value_b = 1
    # 11. 벌레는 풀(4), 에스퍼(10), 악(15)에게 2배의 데미지, 불꽃(1), 격투(6), 땅(8), 비행(9), 고스트(13), 강철(16), 페어리(17)에게 0.5배의 데미지
    elif type_b == "bug" :
        if type_a == "grass" or type_a == "psychic" or type_a == "dark" :
            type_value_b = 2
        elif type_a == "fire" or type_a == "fighting" or type_a == "ground" or type_a == "flying" or type_a == "ghost" or type_a == "steel" or type_a == "fairy" :
            type_value_b = 0.5
        else :
            type_value_b = 1
    # 12. 바위는 불꽃(1), 얼음(5), 비행(9), 벌레(11)에게 2배의 데미지, 격투(6), 땅(8), 강철(16)에게 0.5배의 데미지
    elif type_b == "rock" :
        if type_a == "fire" or type_a == "ice" or type_a == "flying" or type_a == "bug" :
            type_value_b = 2
        elif type_a == "fighting" or type_a == "ground" or type_a == "steel" :
            type_value_b = 0.5
        else :
            type_value_b = 1
    # 13. 고스트는 에스퍼(10), 고스트(13)에게 2배의 데미지, 악(15)에게 0.5배의 데미지, 노말에게 0배의 데미지
    elif type_b == "ghost" :
        if type_a == "psychic" or type_a == "ghost" :
            type_value_b = 2
        elif type_a == "dark" :
            type_value_b = 0.5
        elif type_a == "normal" :
            type_value_b = 0
        else :
            type_value_b = 1
    # 14. 드래곤은 드래곤(14)에게 2배의 데미지, 강철(16)에게 0.5배의 데미지, 페어리(17)에게 0배의 데미지
    elif type_b == "dragon" :
        if type_a == "dragon" :
            type_value_b = 2
        elif type_a == "steel" :
            type_value_b = 0.5
        elif type_a == "fairy" :
            type_value_b = 0
        else :
            type_value_b = 1
    # 15. 악은 에스퍼(10), 고스트(13)에게 2배의 데미지, 악(15), 페어리(17)에게 0.5배의 데미지
    elif type_b == "dark" :
        if type_b == "psychic" or type_a == "ghost" :
            type_value_b = 2
        elif type_a == "dark" or type_a == "fairy" :
            type_value_b = 0.5
        else:
            type_value_b = 1
    # 16. 강철은 얼음(5), 바위(12), 페어리(17)에게 2배의 데미지, 불꽃(1), 물(2), 전기(3), 강철(16)에게 0.5배의 데미지
    elif type_b == "steel" :
        if type_a == "ice" or type_a == "rock" or type_a == "fairy" :
            type_value_b = 2
        elif type_a == "fire" or type_a == "ice" or type_a == "electric" or type_a == "steel" :
            type_value_b = 0.5
        else :
            type_value_b = 1
    # 17. 페어리는 격투(6), 드래곤(14), 악(15)에게 2배의 데미지, 불꽃(1), 독(7), 강철(16)에게 0.5배의 데미지
    elif type_b == "fairy" :
        if type_a == "fighting" or type_a == "dragon" or type_a == "dark" :
            type_value_b = 2
        elif type_a == "fire" or type_a == "poison" or type_a == "steel" :
            type_value_b = 0.5
        else :
            type_value_b = 1

    return type_value_b

