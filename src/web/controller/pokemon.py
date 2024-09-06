import json
from operator import index

import requests
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
#
list = []
for id in range(898,900) :
    url = f"https://pokeapi.co/api/v2/pokemon-species/{id}/"
    responses = requests.get(url)
    if responses.status_code == 200 :
        # print(">>> 통신 성공")
        data  = responses.json()
        # print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")  # 구분선
        ko_name = data.get('names')[2]["name"] #이름 한글
        # print("===========================================")  # 구분선
        # for genera in data.get('genera'):
        if data.get('genera')[1]["language"]['name'] == "ko" : #정보 한글
            ko_info = data.get('genera')[1]['genus']
        elif data.get('genera')[1]["language"]['name'] != 'ko' :
             ko_info = data.get('genera')[5]['genus']
        # print("===========================================") #구분선

        # ko_info2 = []
        # for entry  in data.get('flavor_text_entries')[0:2] :
        #     if entry['language']['name'] == 'ko' :
        #         ko_info2.append(entry['flavor_text'].replace("\n", " "))
        #     elif entry['language']['name'] != 'ko' :
        #         ko_info2 = ["null", "null"]


        if data.get('flavor_text_entries')[1]['language']['name'] == 'ko' :
            ko_info2 = data.get('flavor_text_entries')[1]["flavor_text"].replace("\n", " ")  # 상세정보 1
        elif data.get('flavor_text_entries')[23]['language']['name'] == 'ko' :
            ko_info2 = data.get('flavor_text_entries')[23]["flavor_text"].replace("\n", " ") # 상세정보 1
        else :
            ko_info2 = 'null'
        # print("===========================================") #구분선
        if data.get('flavor_text_entries')[11]['language']['name'] == 'ko' :
            ko_info3 = data.get('flavor_text_entries')[11]["flavor_text"].replace("\n", " ")  # 상세정보 2
        elif data.get('flavor_text_entries')[31]['language']['name'] == 'ko' :
            ko_info3 = data.get('flavor_text_entries')[31]["flavor_text"].replace("\n", " ") # 상세정보 2
        else :
            ko_info3 = 'null'
        # print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")  # 구분선
        url2 = f'https://pokeapi.co/api/v2/pokemon/{id}/'
        responses2 = requests.get(url2)
        if responses2.status_code == 200:
            data2 = responses2.json()
            id = data2['id']
            print(data2['id'])
            img = data2['sprites']['front_default'] #이미지
            hp = data2['stats'][0]['base_stat'] #hp
            attack = data2['stats'][1]['base_stat'] #attack
            defense = data2['stats'][2]['base_stat'] #defense
            special_attack = data2['stats'][3]['base_stat'] #special-attack
            special_defense = data2['stats'][4]['base_stat'] #special-defense
            speed = data2['stats'][5]['base_stat'] #speed
            type = data2['types'][0]['type']['name'] #type

            pokedata = [ko_name , ko_info , ko_info2, ko_info3 , id, img,hp,attack,defense,special_attack,special_defense,speed,type]
            list.append(pokedata)


data = pd.DataFrame(list , columns = ('이름','정보','정보2', '정보3', '아이디','이미지','체력','공격','방어','특수공격','특수방어','스피드','타입'))
data.index = data.index+1
print(data)
data.to_csv("datapokemon.csv", index=True)

skilllist = []
for skill in range(1,10) :
    url = f'https://pokeapi.co/api/v2/move/{skill}/'
    responses = requests.get(url)
    if responses.status_code == 200 :
        data = responses.json()
        for entries in data.get('effect_entries') :
            if entries['language']['name'] == 'ko' :
                skillname = entries['flavor_text'].replace("\n" , " ")

        skilltype = data['type']['name']