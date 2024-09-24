from src.web.app import *
from src.web.service.event_crawling_service import *

# 포켓몬 스토어 온라인 - 이벤트 페이지 일부 항목 크롤링
@app.route("/event/crawling", methods=["GET"])
def event_pokemon() :
    result = pokemon_event()
    return result

