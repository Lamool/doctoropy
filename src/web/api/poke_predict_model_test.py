import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, f1_score, recall_score, roc_auc_score, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
# from sklearn.preprocessing import StandardScaler


data = pd.read_csv("poke_rate_predict_record.csv", encoding="utf-8", index_col=0)
# print(data.head())
# print(data.shape)

x = data[["체력", "공격", "방어", "스피드", "특수공격", "특수방어", "점수", "승률", "사용한_기술의_위력"]]
print(x)
y = data["결과"]
print(y)
# scaler = StandardScaler()
# x_scaled_data = scaler.fit_transform(x)
# print(x_scaled_data)



x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

LR_model = LogisticRegression()

LR_model.fit(x_train, y_train)

predict_result = LR_model.predict_proba(x_test)

y_predict = LR_model.predict(x_test)

print(predict_result[0][0]) # 0.999589474721849
print(predict_result[0][1]) # 0.00041052527815103185

# 1. 오차 행렬
print(f" 오차 행렬 : \n {confusion_matrix(y_test, y_predict)}")
"""
[[2 0]
 [0 3]]
"""

# 2. 예측 정확도
print(f" 예측 정확도 : {accuracy_score(y_test, y_predict)}")

# 2. 정밀도
print(f" 정밀도 : {precision_score(y_test, y_predict)}")  # 0.75  -> 수치가 높을수록 정밀하다고 할 수 있다.

# 3. 재현율
print(f" 재현율 : {recall_score(y_test, y_predict)}")     # 0.5   -> 수치가 높을수록 재현을 잘 하고 있다고 볼 수 있다.

# 4. F1 스코어
print(f" f1 스코어 : {f1_score(y_test, y_predict)}")         # 0.6   -> 수치가 높을수록 정밀도와 재현율의 균형이 잘 맞춰져 있다.

# 5. FPR
print(f" FPR : {roc_auc_score(y_test, y_predict)}")    # 0.625 -> 수치가 1에 가까울수록 좋은 성능이라고 평가를 내릴수 있다.


new_data = [[50, 40, 30, 45, 55, 20, 55, 58, 40]]
new_data2 = [[10, 10, 20, 15, 10, 10, 20, 10, 20]]
new_data3 = [[100, 100, 100, 100, 100, 100, 100, 90, 100]]
new_data4 = [[75, 85, 200, 30, 55, 65, 93, 72.66, 60]]

# scaled_new_data = scaler.fit_transform(new_data)
# scaled_new_data2 = scaler.fit_transform(new_data2)
# scaled_new_data3 = scaler.fit_transform(new_data3)
#
# new_predict = LR_model.predict_proba(new_data)
# print(new_predict[0][1])
# scaled_new_data = scaler.fit_transform(new_data)
# new_predict = LR_model.predict_proba(scaled_new_data)
# print(f"예측값이 승리 쪽에 속할 확률 : {new_predict[0][1]}")

new_predict2 = LR_model.predict_proba(new_data2)
print(new_predict2[0][1])

new_predict3 = LR_model.predict_proba(new_data3)
print(new_predict3[0][1])
print(new_predict3[0][0])


new_predict4 = LR_model.predict_proba(new_data4)
print(new_predict3[0][1])




x1 = data[["체력", "공격", "방어", "스피드", "특수공격", "특수방어", "점수", "사용한_기술의_위력"]]
print(x1.head())

y1 = data["승률"]
print(y1.head())

x_train1, x_test1, y_train1, y_test1 = train_test_split(x1, y1, test_size=0.3, random_state=0)

lr_model = LinearRegression()

lr_model.fit(x_train1, y_train1)

y_predict1 = lr_model.predict(x_test1)
print(y_predict1)

MSE = mean_squared_error(y_test1, y_predict1)
RMSE = np.sqrt(MSE)
R2_SCORE = r2_score(y_test1, y_predict1)
print(f" MSE = {MSE}")
print(f" RMSE = {RMSE}")
print(f" R2_SCORE = {R2_SCORE}")
print(f" Y절편 = {np.round(lr_model.intercept_, 2)}")
print(f" 회귀계수값 = {np.round(lr_model.coef_, 2)}")

coef = pd.Series(data=np.round(lr_model.coef_, 2), index=x1.columns)
coef.sort_values(ascending=False)
print(coef)
"""
(샘플 3만개) 0.5841816544889874 
-> (샘플 4만개) 0.6454431074843747 
-> (샘플 5.2만개) 0.6981852340438781
-> (샘플 7.1만개) 0.7520755004786792
-> (샘플 9만개) 0.7812564658737996
"""

new_data5 = [[75, 85, 200, 30, 55, 65, 93, 60]]
new_data6 = [[70, 80, 65, 85, 90, 65, 64, 35]]

new_predict5 = lr_model.predict(new_data5)
print(new_predict5)

new_predict6 = lr_model.predict(new_data6)
print(new_predict6)     # 27.34

new_data7 = [[40, 50, 45, 70, 70, 45, 55, 35]]

new_predict7 = lr_model.predict(new_data7)
print(new_predict7)

fig, axs = plt.subplots(figsize = (20, 20), ncols=3, nrows= 3)

x_features = ["체력", "공격", "방어", "스피드", "특수공격", "특수방어", "점수", "사용한_기술의_위력"]
plot_color = ["r", "b", "y", "g", "r", "b", "y", "g"]

# 폰트 설정
import matplotlib
from matplotlib import font_manager

font_path = "c:/windows/fonts/malgunsl.ttf"
    # (2) 폰트 설정 객체를 이용한 폰트 설정
font_kor = font_manager.FontProperties(fname = font_path).get_name()
    # (3) 차트에 적용
plt.rc("font", family = font_kor)


for i, feature in enumerate(x_features) :
    row = int(i / 3)
    col = i % 3
    sns.regplot(x = feature, y = "승률", data = data, ax = axs[row][col] , scatter_kws={'s': 2 , 'color' : plot_color[i] })

plt.show()

###