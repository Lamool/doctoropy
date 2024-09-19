
import pandas as pd
import random


poke_data = pd.read_csv("datapokemon.csv", encoding="utf-8", index_col=0)

# select_tournament_num = int(input("1 : 64강, 2 : 32강, 3 : 16강, 4 : 8강, 5 : 4강"))

def select_tournament(select_tournament_num) :
    if select_tournament_num == 1 :
        num_list = []
        duplicate_search = set()
        for i in range(0, 64) :
            random_num = random.randint(0, 1026)
            num_list.append(random_num)
            for j in range(len(num_list)) :
                if num_list[j] == duplicate_search :
                    num_list[j] = random.randint(0, 1026)
        tournament_64_info_list = []
        for i in num_list :
            tournament_64 = poke_data.iloc[i]
            tournament_64_dict = {"이미지" : tournament_64["이미지"], "한글이름" : tournament_64["한글이름"], "영어이름" : tournament_64["영어이름"]}
            tournament_64_info_list.append(tournament_64_dict)
        print(tournament_64_info_list)
        tournament_64_action(tournament_64_info_list)

    elif select_tournament_num == 2 :
        num_list = []
        duplicate_search = set()
        for i in range(0, 32) :
            random_num = random.randint(0, 1026)
            num_list.append(random_num)
            for j in range(len(num_list)) :
                if num_list[j] == duplicate_search :
                    num_list[j] = random.randint(0, 1026)
        tournament_32_info_list = []
        for i in num_list :
            tournament_32 = poke_data.iloc[i]
            tournament_32_dict = {"이미지" : tournament_32["이미지"], "한글이름" : tournament_32["한글이름"], "영어이름" : tournament_32["영어이름"]}
            tournament_32_info_list.append(tournament_32_dict)
        print(tournament_32_info_list)
        tournament_32_action(tournament_32_info_list)

    elif select_tournament_num == 3 :
        num_list = []
        duplicate_search = set()
        for i in range(0, 16) :
            random_num = random.randint(0, 1026)
            num_list.append(random_num)
            for j in range(len(num_list)) :
                if num_list[j] == duplicate_search :
                    num_list[j] = random.randint(0, 1026)
        tournament_16_info_list = []
        for i in num_list :
            tournament_16 = poke_data.iloc[i]
            tournament_16_dict = {"이미지" : tournament_16["이미지"], "한글이름" : tournament_16["한글이름"], "영어이름" : tournament_16["영어이름"]}
            tournament_16_info_list.append(tournament_16_dict)
        print(tournament_16_info_list)
        tournament_16_action(tournament_16_info_list)

    elif select_tournament_num == 4 :
        num_list = []
        duplicate_search = set()
        for i in range(0, 8) :
            random_num = random.randint(0, 1026)
            num_list.append(random_num)
            for j in range(len(num_list)) :
                if num_list[j] == duplicate_search :
                    num_list[j] = random.randint(0, 1026)
        tournament_8_info_list = []
        for i in num_list :
            tournament_8 = poke_data.iloc[i]
            tournament_8_dict = {"이미지" : tournament_8["이미지"], "한글이름" : tournament_8["한글이름"], "영어이름" : tournament_8["영어이름"]}
            tournament_8_info_list.append(tournament_8_dict)
        print(tournament_8_info_list)
        tournament_8_action(tournament_8_info_list)

    elif select_tournament_num == 5 :
        num_list = []
        duplicate_search = set()
        for i in range(0, 4) :
            random_num = random.randint(0, 1026)
            num_list.append(random_num)
            for j in range(len(num_list)) :
                if num_list[j] == duplicate_search :
                    num_list[j] = random.randint(0, 1026)
        tournament_4_info_list = []
        for i in num_list :
            tournament_4 = poke_data.iloc[i]
            tournament_4_dict = {"이미지" : tournament_4["이미지"], "한글이름" : tournament_4["한글이름"], "영어이름" : tournament_4["영어이름"]}
            tournament_4_info_list.append(tournament_4_dict)
        print(tournament_4_info_list)
        tournament_4_action(tournament_4_info_list)

def tournament_64_action(list) :
    print(list)
    n = 0
    m = 1
    for i in range(0, 32) :
        select_win = int(input("0 : 왼쪽 선택, 1 : 오른쪽 선택"))
        if select_win == 0 :
            list.pop(m)
            n += 2
            m += 2
        elif select_win == 1 :
            list.pop(n)
            n += 2
            m += 2
    print(list)
    print(len(list))
    tournament_32_action(list)

def tournament_32_action(list) :
    print(list)
    n = 0
    m = 1
    for i in range(0, 16) :
        select_win = int(input("0 : 왼쪽 선택, 1 : 오른쪽 선택"))
        if select_win == 0 :
            list.pop(m)
            n += 2
            m += 2
        elif select_win == 1 :
            list.pop(n)
            n += 2
            m += 2
    print(list)
    print(len(list))
    tournament_16_action(list)

def tournament_16_action(list) :
    print(list)
    n = 0
    m = 1
    for i in range(0, 8) :
        select_win = int(input("0 : 왼쪽 선택, 1 : 오른쪽 선택"))
        if select_win == 0 :
            list.pop(m)
            n += 2
            m += 2
        elif select_win == 1 :
            list.pop(n)
            n += 2
            m += 2
    print(list)
    print(len(list))
    tournament_8_action(list)

def tournament_8_action(list) :
    print(list)
    n = 0
    m = 1
    for i in range(0, 4) :
        select_win = int(input("0 : 왼쪽 선택, 1 : 오른쪽 선택"))
        if select_win == 0 :
            list.pop(m)
            n += 2
            m += 2
        elif select_win == 1 :
            list.pop(n)
            n += 2
            m += 2
    print(list)
    print(len(list))
    tournament_4_action(list)

def tournament_4_action(list) :
    print(list)
    n = 0
    m = 1
    for i in range(0, 2) :
        select_win = int(input("0 : 왼쪽 선택, 1 : 오른쪽 선택"))
        if select_win == 0 :
            list.pop(m)
            n += 2
            m += 2
        elif select_win == 1 :
            list.pop(n)
            n += 2
            m += 2
    print(list)
    print(len(list))
    tournament_final_action(list)

def tournament_final_action(list) :
    print(list)
    n = 0
    m = 1
    select_win = int(input("0 : 왼쪽 선택, 1 : 오른쪽 선택"))
    if select_win == 0 :
        list.pop(m)
    elif select_win == 1 :
        list.pop(n)

    print(list)
    print(len(list))
    print(f"우승 포켓몬은 {list[0]}입니다.")

# if __name__ == "__main__" :
#     select_tournament_num = int(input("1 : 64강, 2 : 32강, 3 : 16강, 4 : 8강, 5 : 4강"))
#     select_tournament(select_tournament_num)
