#weather_service.py

import pandas as pd
import json
#[1] 5년치 데이터 준비과정

#데이터 읽기
df_2024=pd.read_csv('../api/weather_forecast/2024incheon.csv',encoding='cp949')
df_2023=pd.read_csv('../api/weather_forecast/2023incheon.csv',encoding='cp949')
df_2022=pd.read_csv('../api/weather_forecast/2022incheon.csv',encoding='cp949')
df_2021=pd.read_csv('../api/weather_forecast/2021incheon.csv',encoding='cp949')
df_2020=pd.read_csv('../api/weather_forecast/2020incheon.csv',encoding='cp949')

# print(df_2024)
# print(df_2023)

# 5년치 데이터 합치기
weather=pd.concat([df_2024,df_2023,df_2022,df_2021,df_2020])
# print(weather.shape)
# print(weather)
'''
       지점 지점명                일시  ...  중하층운량(10분위)  운형(운형약어)  최저운고(100m )
0     112  인천  2024-01-01 01:00  ...          0.0       NaN          NaN
1     112  인천  2024-01-01 02:00  ...          3.0       NaN         13.0
2     112  인천  2024-01-01 03:00  ...          8.0        Sc          9.0
3     112  인천  2024-01-01 04:00  ...          1.0        Sc         10.0
4     112  인천  2024-01-01 05:00  ...          8.0        Sc          7.0

'''
#데이터프레임의 기본정보 출력
print(weather.info)
print(weather.describe())
#합친 데이터프레임 ---> csv 파일로 저장
weather.to_csv('weather.csv',index=False)

#============================[준비끝]============================#






