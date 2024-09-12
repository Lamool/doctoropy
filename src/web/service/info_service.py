
import json

import pandas as pd

poke_data = pd.read_csv("datapokemon.csv", encoding="utf-8", index_col=0)

# print(poke_data)
#
# print(poke_data.loc[[0:20], ["영어이름"], ["이미지"]])
# print(poke_data.loc[0:20,"영어이름"])
# print(poke_data.loc[0:20,"이미지"])