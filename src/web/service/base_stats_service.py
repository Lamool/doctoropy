import pandas as pd

# 포켓몬 종족값 목록 출력
def base_stats_print_all() :
    pokemon_data = pd.read_csv("./service/datapokemon.csv", encoding="utf-8", index_col=0)
    pokemon_data_df = pokemon_data[["한글이름","영어이름", "아이디", "이미지", "체력", "공격", "방어", "특수공격", "특수방어", "스피드", "타입"]]
    print(pokemon_data)
    print(pokemon_data_df)

