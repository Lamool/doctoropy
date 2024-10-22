import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, f1_score, recall_score, roc_auc_score, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

df1 = pd.read_csv("vote_record_first_list.csv", encoding="utf-8", index_col=0)

cal_age1 = []
for i in df1["생일"]:
    i = i[:4]
    age = 2024 - int(i)
    cal_age1.append(int(age))

df1["생일"] = cal_age1

num_gen1 = []
for i in df1["성별"]:
    if i == "M":
        i = 0
    elif i == "F":
        i = 1
    num_gen1.append(int(i))

df1["성별"] = num_gen1

# print(df1)
x1 = df1[["성별", "선택_수", "생일"]]
y1 = df1["도시_번호"]

x_train1, x_test1, y_train1, y_test1 = train_test_split(x1, y1, test_size=0.3, random_state=0)

model1 = LinearRegression()

model1.fit(x_train1, y_train1)

y_predict1 = model1.predict(x_test1)
print(y_predict1)

MSE = mean_squared_error(y_test1, y_predict1)
RMSE = np.sqrt(MSE)
R2_SCORE = r2_score(y_test1, y_predict1)
print(f" MSE = {MSE}")
print(f" RMSE = {RMSE}")
print(f" R2_SCORE = {R2_SCORE}")
print(f" Y절편 = {np.round(model1.intercept_, 2)}")
print(f" 회귀계수값 = {np.round(model1.coef_, 2)}")

coef = pd.Series(data=np.round(model1.coef_, 2), index=x1.columns)
coef.sort_values(ascending=False)
print(coef)

new_data1 = [[1, 1, 10]]

new_predict1 = model1.predict(new_data1)
print(new_predict1) # 나이 30 : [64.16455888] 20 : [62.63297075] 10 : [61.10138262]

df2 = pd.read_csv("vote_record_second_list.csv", encoding="utf-8", index_col=0)

cal_age2 = []
for i in df2["생일"]:
    i = i[:4]
    age = 2024 - int(i)
    cal_age2.append(int(age))

df2["생일"] = cal_age2

num_gen2 = []
for i in df2["성별"]:
    if i == "M":
        i = 0
    elif i == "F":
        i = 1
    num_gen2.append(int(i))

df2["성별"] = num_gen2

# print(df2)
x2 = df2[["성별", "선택_수", "생일"]]
y2 = df2["도시_번호"]

x_train2, x_test2, y_train2, y_test2 = train_test_split(x2, y2, test_size=0.3, random_state=0)

model2 = LinearRegression()

model2.fit(x_train2, y_train2)

y_predict2 = model2.predict(x_test2)
print(y_predict2)

MSE = mean_squared_error(y_test2, y_predict2)
RMSE = np.sqrt(MSE)
R2_SCORE = r2_score(y_test2, y_predict2)
print(f" MSE = {MSE}")
print(f" RMSE = {RMSE}")
print(f" R2_SCORE = {R2_SCORE}")
print(f" Y절편 = {np.round(model2.intercept_, 2)}")
print(f" 회귀계수값 = {np.round(model2.coef_, 2)}")

coef = pd.Series(data=np.round(model2.coef_, 2), index=x2.columns)
coef.sort_values(ascending=False)
print(coef)

new_data2 = [[0, 4, 25]]

new_predict2 = model2.predict(new_data2)
print(new_predict2) # 나이 30 : [64.16455888] 20 : [62.63297075] 10 : [60.85017428]
"""
new_data2 = [[0, 4, 25]] -> [52.30682331]
"""


df3 = pd.read_csv("vote_record_third_list.csv", encoding="utf-8", index_col=0)

cal_age3 = []
for i in df3["생일"]:
    i = i[:4]
    age = 2024 - int(i)
    cal_age3.append(int(age))

df3["생일"] = cal_age3

num_gen3 = []
for i in df3["성별"]:
    if i == "M":
        i = 0
    elif i == "F":
        i = 1
    num_gen3.append(int(i))

df3["성별"] = num_gen3

# print(df3)
x3 = df3[["성별", "선택_수", "생일"]]
y3 = df3["도시_번호"]

x_train3, x_test3, y_train3, y_test3 = train_test_split(x3, y3, test_size=0.3, random_state=0)

model3 = LinearRegression()

model3.fit(x_train3, y_train3)

y_predict3 = model3.predict(x_test3)
print(y_predict3)

MSE = mean_squared_error(y_test3, y_predict3)
RMSE = np.sqrt(MSE)
R2_SCORE = r2_score(y_test3, y_predict3)
print(f" MSE = {MSE}")
print(f" RMSE = {RMSE}")
print(f" R2_SCORE = {R2_SCORE}")
print(f" Y절편 = {np.round(model3.intercept_, 2)}")
print(f" 회귀계수값 = {np.round(model3.coef_, 2)}")

coef = pd.Series(data=np.round(model3.coef_, 2), index=x3.columns)
coef.sort_values(ascending=False)
print(coef)

new_data3 = [[0, 4, 25]]

new_predict3 = model3.predict(new_data3)
print(new_predict3) # 나이 30 : [64.16455888] 20 : [62.63297075] 10 : [57.8156578]

"""
new_data3 = [[0, 4, 25]] -> [52.30682331]
"""