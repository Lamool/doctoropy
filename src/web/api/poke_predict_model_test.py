import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, f1_score, recall_score, roc_auc_score

data = pd.read_csv("poke_rate_predict_record.csv", encoding="utf-8", index_col=0)

x = data[["점수", "승률", "포켓몬_번호", "사용한_기술의_위력"]]

y = data["결과"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

LR_model = LogisticRegression()

LR_model.fit(x_train, y_train)

predict_result = LR_model.predict_proba(x_test)

y_predict = LR_model.predict(x_test)

print(predict_result[0][0]) # 0.999589474721849
print(predict_result[0][1]) # 0.00041052527815103185

# 1. 오차 행렬
print(confusion_matrix(y_test, y_predict))
"""
[[2 0]
 [0 3]]
"""

# 2. 예측 정확도
print(accuracy_score(y_test, y_predict))

# 2. 정밀도
print(precision_score(y_test, y_predict))  # 0.75  -> 수치가 높을수록 정밀하다고 할 수 있다.

# 3. 재현율
print(recall_score(y_test, y_predict))     # 0.5   -> 수치가 높을수록 재현을 잘 하고 있다고 볼 수 있다.

# 4. F1 스코어
print(f1_score(y_test, y_predict))         # 0.6   -> 수치가 높을수록 정밀도와 재현율의 균형이 잘 맞춰져 있다.

# 5. FPR
print(roc_auc_score(y_test, y_predict))    # 0.625 -> 수치가 1에 가까울수록 좋은 성능이라고 평가를 내릴수 있다.
