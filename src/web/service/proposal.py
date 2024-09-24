import numpy as np
import pandas as pd
import json

import requests
from src.web.app import *

from sklearn.linear_model import LinearRegression #모델 객체 생성
from sklearn.model_selection import train_test_split # 모델 훈련용,테스트용 분류
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error  # MSE, R² 값 분석
from src.web.controller.proposal import *

def modeling(data):

    df = pd.DataFrame(data)
    df = df.drop(columns=['prono'])
    ages = []
    for i in df['ubirth'] :
        i = i[:4]
        age = 2024 - int(i)
        # print(age)
        ages.append(age)
    df['ubirth'] = ages
    df = df.replace({'M':1,'F':0})
    # print(df)

    # X ,Y 분할
    Y = df['pno']  # 타겟
    X = df[['gender','ubirth']]  # 피처
    # print(Y)
    # print(X)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
    # print(X_train)
    # print(X_test)
    # print(Y_train)
    # print(Y_test)
    model = LinearRegression()
    #모델 피팅
    model.fit(X_train, Y_train)

    #예측 값
    Y_predict = model.predict(X_test)
    # print(Y_predict)

    #성능평가
    #평균 절대 오차
    MAE = mean_absolute_error(Y_test, Y_predict)
    print(MAE)

    #평균 제곱 오차
    MSE = mean_squared_error(Y_test, Y_predict)
    print(MSE)

    #결정개수
    r2 = r2_score(Y_test, Y_predict)
    print(r2)

    #새로운 데이털 포켓몬 번호 예측
    newData = np.array([[0,26]])
    predict2 = model.predict(newData)
    print(f'포켓몬 번호 결과 확인 : {predict2[0]:0.0f}')