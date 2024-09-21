import pandas as pd

# poke_data = pd.read_csv("datapokemon.csv", encoding="utf-8", index_col=0)

# poke_data_kr_name = poke_data["한글이름"]

poke_each_skill_data = pd.read_csv("poke_each_skill_data.csv", encoding="utf-8", index_col=0)

poke_each_skill_data_kr_name = poke_each_skill_data["포켓몬"]

# poke_name = input("포켓몬 이름 입력 : ")
#
# for i, kr_name in enumerate(poke_each_skill_data_kr_name):
#     if poke_name == kr_name:
#         print(i)

print(poke_each_skill_data.iloc[19450]["위력"])