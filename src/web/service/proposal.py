import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression #모델 객체 생성
from sklearn.model_selection import train_test_split # 모델 훈련용,테스트용 분류
from sklearn.metrics import mean_squared_error,r2_score #MSE, R² 값 분석

#X ,Y 분할
# Y = data_df[''] #타겟
# X = data_df[''] #피처

X_train , X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
#비율 7:3 설정

#선형회귀분석 모델 생성
lr = LinearRegression
#모델 피팅 (훈련)
lr.fit(X_train, Y_train)
#선형 회귀 분석 예측 값 생성
Y_predict = lr.predict(X_test)

MSE = mean_squared_error(Y_test, Y_predict)
print(MSE)
RMSE = np.sqrt(MSE)
print(RMSE)
r2 = r2_score(Y_test, Y_predict)
print(r2)

print("Y 절편 값 :", np.round(lr.intercept_, 2))
print("회귀 계수 값 :", np.round(lr.coef_, 2))

# coef = pd.Series(data = np.round(lr.coef_,2), index=X.columns) #Series 자료형 생성
# coef.sort_values(ascending=False) #내림 차순

# 생성중 접근 금지

# @app.route("/pro")
# def proposal():
#