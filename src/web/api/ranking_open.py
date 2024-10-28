from idlelib.iomenu import encoding

import pandas as pd

from src.web.app import *

@app.route('/rank/allcrolling',methods=['POST'])
def all_crolling():
    contentType = request.content_type
    args = None

    if contentType == "application/x-www-form-urlencoded":
        args: dict = request.form

    elif contentType == "application/json":
        args: dict = request.json

    else:
        print("not supported content-type")

    data = list(args.get("data"))
    # print(data)
    # print(data[0]['pno'])
    # print(data[0]['click'])
    # print(data[0]['win'])
    fillter_data = [
        {'pno' : item['pno'], 'click' : item['click'], 'win': item['win']}
        for item in data
        if item['ko_name'] is None and item['en_name'] is None and item['img'] is None
    ]
    # print(fillter_data)

    df = pd.read_csv("./service/datapokemon.csv", encoding="utf-8")
    # print(df)
    df2 = df[['한글이름']]
    # print(df2)

    df_data = pd.DataFrame(fillter_data)
    # print(df_data)

    df2.index = range(1, len(df2) +1)
    # print(df2)

    merged_df = pd.merge(df_data, df2, left_on='pno', right_index=True)
    print(merged_df)
    merged_df.to_csv('merged_data.csv',index=False)
    print("파일 변환 완료")

    return jsonify(fillter_data)