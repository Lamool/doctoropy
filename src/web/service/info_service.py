
import json

import pandas as pd



# print(poke_data)
#
# print(poke_data.loc[])
# print(poke_data.loc[0:20,"영어이름"])
# print(poke_data.loc[0:20,"이미지"])


def poke_all_info_print(page) :
    list = []
    list_all = []

    poke_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)
    n = 0
    m = 100
    if page >= 1000 :
        for i1 in range(1000, 1025):
            i_poke_data = poke_data.iloc[i1]
            i_poke_data_dict = {"이미지": i_poke_data["이미지"], "한글이름": i_poke_data["한글이름"], "영어이름": i_poke_data["영어이름"]}
            list.append(i_poke_data_dict)
            # print(f"시작 번호 : {n}, 끝 번호 : {m}")
            # print(i_poke_data_dict)
        list_all = [list]
        # print(list)
        # print(list_all)
        df_list_all = pd.DataFrame(list_all)
        df_list_all_json = df_list_all.to_json(orient="records", force_ascii=False)
        df_list_all_result = json.loads(df_list_all_json)
        return df_list_all_result
    else :
        for i1 in range(n + page , m + page) :  #  0+0  , 100+0  , 0+100 , 100+100
            i_poke_data = poke_data.iloc[i1]
            i_poke_data_dict = {"이미지" : i_poke_data["이미지"], "한글이름" : i_poke_data["한글이름"], "영어이름" : i_poke_data["영어이름"]}
            list.append(i_poke_data_dict)
            # print(f"시작 번호 : {n}, 끝 번호 : {m}")
            # print(i_poke_data_dict)
        list_all = [list]
        # print(list)
        # print(list_all)
        df_list_all = pd.DataFrame(list_all)
        df_list_all_json = df_list_all.to_json(orient="records", force_ascii=False)
        df_list_all_result = json.loads(df_list_all_json)
        return df_list_all_result


def poke_detail_info_print(name) :
    poke_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)
    name_poke_data = poke_data.loc[:, "영어이름"]

    for i, n in enumerate(name_poke_data) :
        if n == name :
            poke_detail_info_dict = [poke_data.iloc[i]]
            print(poke_detail_info_dict)
            df_poke_detail_info_list = pd.DataFrame(poke_detail_info_dict)
            df_poke_detail_info_json = df_poke_detail_info_list.to_json(orient="records", force_ascii=False)
            df_poke_detail_info_result = json.loads(df_poke_detail_info_json)
            print(df_poke_detail_info_result)
            return df_poke_detail_info_result

