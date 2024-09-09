# 1. 플라스크 모듈 가져오기
from flask import Flask

# 2. 플라스크 객체 생성
app = Flask(__name__)

# 3. CORS허용
from flask_cors import CORS
CORS(app)

# 김민석 커밋
from controller.controller import *

# 3. 플라스크 웹 실행
if __name__ == "__main__":
    app.run(host='0.0.0.0' , debug=True)

