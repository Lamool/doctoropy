import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, f1_score, recall_score, roc_auc_score
from sklearn.preprocessing import StandardScaler

data = pd.read_csv("poke_rate_predict_record.csv", encoding="utf-8", index_col=0)

x = data[["체력", "공격", "방어", "스피드", "특수공격", "특수방어", "점수", "승률", "사용한_기술의_위력"]]
print(x)

scaler = StandardScaler()
x_scaled_data = scaler.fit_transform(x)
print(x_scaled_data)

y = data["결과"]
print(y)

x_train, x_test, y_train, y_test = train_test_split(x_scaled_data, y, test_size=0.3, random_state=0)

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
scaled_new_data = scaler.fit_transform(new_data)
new_predict = LR_model.predict_proba(scaled_new_data)
print(f"예측값이 승리 쪽에 속할 확률 : {new_predict[0][1]}")


