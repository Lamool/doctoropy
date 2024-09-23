import pandas as pd
import re

df = pd.read_csv('poke_each_skill_data.csv')

# 각 셀에서 숫자가 있는지 확인하고, 하나라도 숫자가 있는 행만 살리기
# print(df["위력"])
data_poke_skill_name = df["스킬이름"]
data_poke_type_name = df["타입"]
data_poke_name = df["포켓몬"]
result = []
for i, d in enumerate(df["위력"]):
    if re.match(r"^\d+$", d):
        skill_list = [data_poke_skill_name.iloc[i], data_poke_type_name.iloc[i], d, data_poke_name.iloc[i]]
        result.append(skill_list)

data = pd.DataFrame(result, columns=("스킬이름", "타입", "위력", "포켓몬"))
data.index = data.index + 1
print(data)

data.to_csv("new_poke_each_skill_data.csv", index=True)
