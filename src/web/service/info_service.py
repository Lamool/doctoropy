
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
            i_poke_data_dict = {"이미지": i_poke_data["이미지"],
                                "한글이름": i_poke_data["한글이름"],
                                "영어이름": i_poke_data["영어이름"]}
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
            i_poke_data_dict = {"이미지" : i_poke_data["이미지"],
                                "한글이름" : i_poke_data["한글이름"],
                                "영어이름" : i_poke_data["영어이름"]}
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
"""
> 타입 분류 기능
   타입 이름이 담긴 리스트를 for문을 돌려서 순회
-> 인풋으로 받은 타입 이름과 겹치는 것이 있다면 
-> 그 때의 인덱스를 리스트에 append
-> 인덱스를 담은 리스트를 for문을 돌려서 순회
-> 그 인덱스에 따른 이름과 이미지를 리스트에 append
-> json 타입으로 변경 후 내보내기 
"""
# type_eng = input("타입 입력")
# index_list = []
# poke_type_info_list = []
# poke_data = pd.read_csv("datapokemon.csv", encoding="utf-8", index_col=0)
#
# poke_type = poke_data.loc[:, "타입"]
# # print(poke_type)
# for i, t in enumerate(poke_type) :
#     if t == type_eng:
#         index_list.append(i)
# # print(index_list)
# # print(len(index_list))
# for i in index_list:
#     poke_data_index = poke_data.iloc[i]
#     poke_data_index_dict = {"이미지": poke_data_index["이미지"], "한글이름": poke_data_index["한글이름"], "영어이름": poke_data_index["영어이름"]}
#     poke_type_info_list.append(poke_data_index_dict)
# print(poke_type_info_list)
# type_eng = input("타입 입력: ")
# page_number = int(input("페이지 번호 입력: "))  # 예를 들어 1페이지, 2페이지 등

def get_paged_data(index_list, page_size, page_number):
    # print(index_list)
    # print(page_size)
    # print(page_number)
    start_index = page_size * (page_number - 1)
    end_index = start_index + page_size

# 범위를 초과하지 않도록 end_index 조정
    if end_index > len(index_list):
        end_index = len(index_list)
    return index_list[start_index:end_index]
def type_poke_info(type_eng, page_number) :
    # 사용자 입력 받기
    # 데이터 읽기
    # print(page_number)
    print(type_eng)
    poke_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)
    # print(poke_data)
    # 타입 정보 추출
    poke_type = poke_data.loc[:, "타입"]
    index_list = [i for i, t in enumerate(poke_type) if t == type_eng]
    # print(index_list)
    # 페이지 크기와 페이지 번호 설정
    page_size = 100


    # 페이지에 해당하는 인덱스 리스트 추출
    paged_index_list = get_paged_data(index_list, page_size, page_number)
    # print(paged_index_list)
    ##
    # 페이지에 해당하는 데이터 처리
    poke_type_info_list = []
    for i in paged_index_list:
        poke_data_index = poke_data.iloc[i]
        poke_data_index_dict = {
            "이미지": poke_data_index["이미지"],
            "한글이름": poke_data_index["한글이름"],
            "영어이름": poke_data_index["영어이름"]
        }
        poke_type_info_list.append(poke_data_index_dict)
    print(poke_type_info_list)
    return poke_type_info_list
    # 결과 출력
    # for info in poke_type_info_list:
    #     print(info)

# type_poke_info(type_eng, page_number)

"""
> 검색 기능
    for 문을 돌려서 한글이름 or 영어이름 하나씩 순회
-> 순회할 때마다 이름을 자연어 처리로 하나씩 쪼개서 리스트에 저장 
-> 인풋으로 받아온 값과 비교하는데 받아온 값의 길이가 2 이상인 경우 받아온 값도 쪼개서 리스트에 저장 후 안에 포함되는 지 확인
-> 만약 비교해서 맞는 값이 있다면 그 때의 인덱스 값에 해당하는 이름과 이미지를 리스트에 append
-> json 타입으로 변경 후 내보내기
-> 이름 검색 시 원래 이름보다 길 경우는 찾지 않는다는 조건이 추가되어야 함
"""
# input_kr_name = input("한글 이름 입력 : ")
# input_kr_name_list = list(input_kr_name)
# poke_data = pd.read_csv("datapokemon.csv", encoding="utf-8", index_col=0)
# poke_data_kr_name = poke_data.loc[:, "한글이름"]
# for i, kr_name in enumerate(poke_data_kr_name) :
#     for kr_name_split in list(kr_name) :
#         if len(list(kr_name)) == len(input_kr_name_list) :
#             if kr_name == input_kr_name :
#                 print(kr_name)
#                 print(i)
#                 break
#         if len(list(kr_name)) > len(input_kr_name_list) :
#             if kr_name_split in input_kr_name_list :
#                 print(kr_name)
#                 print(i)
#                 break
#         if len(list(kr_name)) < len(input_kr_name_list) :
#             break

# def split_name(name):
#     """이름을 한 글자씩 쪼개서 리스트로 반환합니다."""
#     return list(name)

# 사용자로부터 입력을 받음
def poke_kr_search(input_kr_name, page_number):
    print(input_kr_name)
    print(page_number)
    # 페이지 당 항목 수
    items_per_page = 100

    # Pokémon 데이터 로드
    poke_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)

    # '한글이름' 열과 '이미지' 열을 문자열로 변환하고 결측치를 빈 문자열로 처리
    poke_data['한글이름'] = poke_data['한글이름'].fillna('').astype(str)
    poke_data['이미지'] = poke_data['이미지'].fillna('').astype(str)

    poke_data_kr_name = poke_data['한글이름']
    poke_data_images = poke_data['이미지']
    poke_data_en_name = poke_data["영어이름"]

    results = []

    for i, kr_name in enumerate(poke_data_kr_name):
        if pd.isna(kr_name):
            continue  # 결측치인 경우 건너뜁니다.

        if input_kr_name in kr_name:
            results.append({"한글이름": kr_name,
                            "이미지": poke_data_images.iloc[i],
                            "영어이름": poke_data_en_name.iloc[i]})

    # 페이지 범위 계산
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    poke_search_results = results[start_index:end_index]
    print(poke_search_results)
    return poke_search_results

def poke_en_search(input_en_name, page_number):
    print(input_en_name)
    print(page_number)
    # 페이지 당 항목 수
    items_per_page = 100

    # Pokémon 데이터 로드
    poke_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)

    # '한글이름' 열과 '이미지' 열을 문자열로 변환하고 결측치를 빈 문자열로 처리
    poke_data['한글이름'] = poke_data['한글이름'].fillna('').astype(str)
    poke_data['이미지'] = poke_data['이미지'].fillna('').astype(str)

    poke_data_kr_name = poke_data['한글이름']
    poke_data_images = poke_data['이미지']
    poke_data_en_name = poke_data["영어이름"]

    results = []

    for i, en_name in enumerate(poke_data_en_name):
        if pd.isna(en_name):
            continue  # 결측치인 경우 건너뜁니다.

        if input_en_name in en_name:
            results.append({"영어이름": en_name,
                            "이미지": poke_data_images.iloc[i],
                            "한글이름": poke_data_kr_name.iloc[i]})

    # 페이지 범위 계산
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    poke_search_results = results[start_index:end_index]
    print(poke_search_results)
    return poke_search_results

"""
>   타입 분류와 검색 기능 합치기
   먼저 타입 이름이 담긴 리스트를 for문을 돌려서 순회
-> 인풋으로 받은 타입 이름과 겹치는 것이 있다면
-> 그 때의 인덱스를 리스트에 append
-> 인덱스를 담은 리스트를 for문을 돌려서 순회
-> 이때 인덱스값에 해당하는 이름을 가져와서 
-> 인풋으로 받아온 이름과 비교 (비교 방법은 1과 동일)
-> 겹치는 이름이 있을 경우에만 그 때의 인덱스값을 통해서
-> 이름과 이미지를 리스트에 append
-> 그 후 json 타입으로 변경 후 내보내기
"""
# type_eng = input("타입 입력 : ")
# input_kr_name = input("찾고 싶은 포켓몬 : ")
# page_number = int(input("페이지 번호 : "))

def poke_type_kr_search(input_kr_name, type_eng, page_number):
    # 페이지 당 항목 수
    items_per_page = 100
    poke_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)

    poke_type = poke_data.loc[:, "타입"]
    index_list = [i for i, t in enumerate(poke_type) if t == type_eng]

    poke_data['한글이름'] = poke_data['한글이름'].fillna('').astype(str)
    poke_data['이미지'] = poke_data['이미지'].fillna('').astype(str)
    poke_data_kr_name = poke_data['한글이름']

    find_type_kr_name = []

    for i in index_list :
        # print(i)
        # print(poke_data_kr_name.iloc[i])
        find_type_kr_name.append(poke_data_kr_name.iloc[i])
    # print(find_type_kr_name)

    poke_data_images = poke_data['이미지']
    poke_data_en_name = poke_data["영어이름"]

    results = []

    for i, kr_name in enumerate(find_type_kr_name):
        if pd.isna(kr_name):
            continue  # 결측치인 경우 건너뜁니다.

        if input_kr_name in kr_name:
            results.append({"한글이름": kr_name,
                            "이미지": poke_data_images.iloc[index_list[i]],
                            "영어이름": poke_data_en_name.iloc[index_list[i]]})

    # print(results)
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    poke_search_results = results[start_index:end_index]
    print(poke_search_results)
    return poke_search_results

# poke_type_kr_search(input_kr_name, type_eng, page_number)

# type_eng = input("타입 입력 : ")
# input_en_name = input("찾고 싶은 포켓몬 : ")
# page_number = int(input("페이지 번호 : "))
def poke_type_en_search(input_en_name, type_eng, page_number):
    # 페이지 당 항목 수
    items_per_page = 100
    poke_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)

    poke_type = poke_data.loc[:, "타입"]
    index_list = [i for i, t in enumerate(poke_type) if t == type_eng]

    poke_data['한글이름'] = poke_data['한글이름'].fillna('').astype(str)
    poke_data['이미지'] = poke_data['이미지'].fillna('').astype(str)
    poke_data_en_name = poke_data["영어이름"]

    find_type_en_name = []

    for i in index_list :
        # print(i)
        # print(poke_data_kr_name.iloc[i])
        find_type_en_name.append(poke_data_en_name.iloc[i])
    # print(find_type_kr_name)

    poke_data_images = poke_data['이미지']
    poke_data_kr_name = poke_data['한글이름']

    results = []

    for i, en_name in enumerate(find_type_en_name):
        if pd.isna(en_name):
            continue  # 결측치인 경우 건너뜁니다.

        if input_en_name in en_name:
            results.append({"영어이름": en_name,
                            "이미지": poke_data_images.iloc[index_list[i]],
                            "한글이름": poke_data_kr_name.iloc[index_list[i]]})

    # print(results)
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    poke_search_results = results[start_index:end_index]
    print(poke_search_results)
    return poke_search_results

# poke_type_en_search(input_en_name, type_eng, page_number)
