#weather_service.py

import pandas as pd
from datetime import datetime, timedelta
import json
#[1] 5년치 데이터 준비과정

#데이터 읽기
df_2024=pd.read_csv('../api/weather_forecast/2024incheon.csv',encoding='cp949')
df_2023=pd.read_csv('../api/weather_forecast/2023incheon.csv',encoding='cp949')
df_2022=pd.read_csv('../api/weather_forecast/2022incheon.csv',encoding='cp949')
df_2021=pd.read_csv('../api/weather_forecast/2021incheon.csv',encoding='cp949')
df_2020=pd.read_csv('../api/weather_forecast/2020incheon.csv',encoding='cp949')
df_2019=pd.read_csv('../api/weather_forecast/2019incheon.csv',encoding='cp949')
df_2018=pd.read_csv('../api/weather_forecast/2018incheon.csv',encoding='cp949')
df_2017=pd.read_csv('../api/weather_forecast/2017incheon.csv',encoding='cp949')
df_2016=pd.read_csv('../api/weather_forecast/2016incheon.csv',encoding='cp949')
df_2015=pd.read_csv('../api/weather_forecast/2015incheon.csv',encoding='cp949')
# print(df_2024)
# print(df_2023)
# print(df_2019)

# 10년치 데이터 합치기
weather=pd.concat([df_2024,df_2023,df_2022,df_2021,df_2020,df_2019,df_2018,df_2017,df_2016,df_2015])
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
# print(weather.info)
# print(weather.describe())
#합친 데이터프레임 ---> csv 파일로 저장
weather.to_csv('weather.csv',index=False)

#===============================================[준비끝]======================================================#
#모델 훈련 시작
df = pd.read_csv('weather.csv')

# 열 이름 확인
# print(df.columns.tolist())
df.fillna(0, inplace=True)
# print(df)


# print(df.columns)
df.columns = df.columns.str.strip() #강수량 Nan 값을 0으로 변환
#데이터 통계 분석 #기온,강수량에 따른 현재 날씨 예측 모델 만들기
# 독립 변수 지정
# '일시'를 datetime 객체로 변환
df['일시'] = pd.to_datetime(df['일시'])

# print(df.head())
# 연, 월, 일, 시, 분 정보 추출
df['년'] = df['일시'].dt.year
df['월'] = df['일시'].dt.month
df['일'] = df['일시'].dt.day
df['시'] = df['일시'].dt.hour
df['분'] = df['일시'].dt.minute
# print(df.head())

x = df[['년', '월', '일', '시', '분']]
# print(x)
#종속변수
y=df[['기온(°C)','강수량(mm)']]
# print(y)

#다중 회귀 모델 구현

# 다중 출력 회귀 모델 정의
from sklearn.linear_model import  LinearRegression
#훈련용, 테스트용 나누기
from sklearn.model_selection import  train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(x,y,test_size=0.3, random_state=0)
X_test.reset_index(drop=True, inplace=True)



X_test = pd.DataFrame(X_test, columns=X_train.columns)
print(X_test)

#모델 피팅 #선형 회귀 분석 : 모델 생성
lr=LinearRegression()
lr.fit(X_train,Y_train)


#예측
Y_predict = lr.predict(X_test.to_numpy())
print(Y_predict)


#정확도
import  numpy as np
from sklearn.metrics import mean_squared_error, r2_score
mse=mean_squared_error(Y_test, Y_predict)
print(mse)
rmse=np.sqrt(mse)
print(rmse)

#실제 날씨 예측해보기
mpg_predict=lr.predict([[2024, 10, 21, 16, 49]])
print(mpg_predict)