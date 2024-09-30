# 1. 플라스크 모듈 가져오기
from flask import Flask, request, jsonify

# 2. 플라스크 객체 생성
app = Flask(__name__)

# 3. CORS허용
from flask_cors import CORS
CORS(app)

# 모듈 가져오기
from controller.controller import *
from src.web.service.rankservice import *
from src.web.controller.info_controller import *
from src.web.controller.base_stats_controller import *
from src.web.controller.event_crawling_controller import *
from src.web.controller.rate_pred_controller import *
from src.web.controller.board_controller import  *
from src.web.controller.proposal import *
from src.web.controller.my_pokemon_controller import *

# 3. 플라스크 웹 실행
if __name__ == "__main__":
    app.run(host='0.0.0.0' , debug=True)

