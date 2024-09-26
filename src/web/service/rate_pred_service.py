# rate_pred_service.py
import pandas as pd


def poke_list_take(data) :
    result = []
    for d in data:
        record_list = [d["rhp"], d["ratk"], d["rdef"], d["rspd"], d["rspatk"], d["rspdef"],d["rscore"], d["rrate"], d["rpokeindex"], d["rskillpower"], d["rresult"]]
        result.append(record_list)

    record = pd.DataFrame(result, columns=("체력", "공격", "방어", "스피드", "특수공격", "특수방어", "점수", "승률", "포켓몬_번호", "사용한_기술의_위력", "결과"))
    record.index = record.index + 1
    print(record)

    record.to_csv("./service/poke_rate_predict_record.csv", index=True)

