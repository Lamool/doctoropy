# service
import json

import pandas as pd
from pandas import read_csv

poke_data = pd.read_csv("datapokemon.csv", encoding="utf-8", index_col=0)
poke_skill_data = pd.read_csv("skilldata.csv", encoding="utf-8",index_col=0)
# print(poke_data)

# print(poke_data.iloc[1000])
n = int(input("포켓몬 번호 입력"))
m = int(input("스킬 번호 입력"))


def poke(n):
    poke_data_one = poke_data.iloc[n]
    poke_skill_data_one = poke_skill_data.iloc[m]
    print(poke_data_one["체력"])
    print(poke_skill_data_one["데미지"])

poke(n)