
from src.web.app import *
import json


from src.web.service.board_service import *

@app.route('/board/wordCount', methods=['POST'])
def count_word():
    data = request.get_json()  # JSON 형식으로 요청 본문 파싱
    # print(data)  # 받은 데이터 출력
    result = count(data)
    return result













