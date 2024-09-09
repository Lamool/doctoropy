import json
from operator import index

import requests
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
#
list = []
for id in range(1,1026) :
    url = f"https://pokeapi.co/api/v2/pokemon-species/{id}/"
    responses = requests.get(url)
    if responses.status_code == 200 :
        # print(">>> 통신 성공")
        data  = responses.json()
        # print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")  # 구분선
        ko_name = "null"
        for names in data.get('names') :
            if names['language']['name'] == 'ko' :
                ko_name = names["name"] #이름 한글
                # print('>>>> name 성공')
                break

        en_name = "null"
        for names in data.get('names') :
            if names['language']['name'] == 'en' :
                en_name = names["name"] #이름 영어
                break

        # print("===========================================")  # 구분선
        ko_info = "null"
        for genera in data.get('genera'):
            if genera["language"]['name'] == "ko" : #정보 한글
                ko_info = genera['genus']
                break

        en_info = "null"
        for genera in data.get('genera'):
            if genera["language"]['name'] == "en" : #정보 영어
                en_info = genera['genus']
                break

        # print("===========================================") #구분선
        ko_info2 = "null"
        for entry in data.get('flavor_text_entries') :
            if entry['language']['name'] == 'ko' :
                ko_info2 = entry['flavor_text'].replace("\n"," ") #상세1 한글
                break

        en_info2 = "null"
        for entry in data.get('flavor_text_entries') :
            if entry['language']['name'] == 'en' :
                en_info2 = entry['flavor_text'].replace("\n"," ") #상세1 영어
                break


        ko_info3 = "null"
        for entry in data.get('flavor_text_entries') :
            if entry['language']['name'] == 'ko' :
                ko_info3 = entry['flavor_text'].replace("\n"," ") #상세2 한글

        en_info3 = "null"
        for entry in data.get('flavor_text_entries') :
            if entry['language']['name'] == 'en' :
                en_info3 = entry['flavor_text'].replace("\n"," ") #상세2 영어

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


            pokedata = [ko_name ,en_name ,ko_info ,en_info, ko_info2,en_info2, ko_info3,en_info3, id, img,hp,attack,defense,special_attack,special_defense,speed,type]
            list.append(pokedata)


data = pd.DataFrame(list , columns = ('한글이름','영어이름','한글정보','영어정보','한글정보2','영어정보2','한글정보3','영어정보3','아이디','이미지','체력','공격','방어','특수공격','특수방어','스피드','타입'))
data.index = data.index+1
print(data)
data.to_csv("datapokemon.csv", index=True)