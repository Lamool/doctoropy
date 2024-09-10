import pandas as pd
import json

df = pd.read_csv("datapokemon.csv", encoding="utf-8")
df2 = df[['한글이름','아이디','영어이름','이미지']]
print(df2)

from flask import Flask
app = Flask(__name__)

from flask_cors import CORS
CORS(app)

@app.route("/rank")
def index():
    jsonData = df2.to_json(orient='records', force_ascii=False)
    result = json.loads(jsonData)
    return result

if __name__ == "__main__" :
    app.run()