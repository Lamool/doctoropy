from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import json

# 포켓몬 스토어 온라인 - 이벤트 페이지 일부 항목 크롤링
def pokemon_event() :
    # 브라우저 옵션 설정 (예: Headless 모드)
        # Selenium은 기본적으로 브라우저를 띄움
        # Headless 모드를 사용하면 브라우저를 띄우지 않고도 JavaScript를 실행하여 동적으로 로드된 데이터를 가져올 수 있음
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # webdriver 객체 생성
    wd = webdriver.Chrome(options=chrome_options)

    # 포켓몬 스토어 온라인 웹페이지 연결
    wd.get('https://pokemonstore.co.kr/pages/board/event.html?boardId=event-benefit&pageNumber=1&searchType=ALL&keyword=')
    # time.sleep(2)

    event = []  # 이벤트 정보를 담을 리스트

    # 필요한 요소 가져오기 (특정 ID로 요소 찾기)
    event_section = wd.find_element(By.ID, "boardArticles")

    # 이미지 태그를 모두 찾기
    event_section_img = event_section.find_elements(By.TAG_NAME, "img")

    # p 태그를 모두 찾기
    event_section_p = event_section.find_elements(By.TAG_NAME, "p")

    # 이미지의 src 속성값(이미지 URL)과 alt 속성값(제목) 가져오기
    for img in event_section_img :
        img_url = img.get_attribute("src")      # 이미지의 src 속성값(이미지 URL)
        title = img.get_attribute("alt")        # 이미지의 alt 속성값(제목)
        print(f"이미지 URL : {img_url}")
        print(f"제목 : {title}")
        result = [img_url, title]
        event.append(result)
    print(event)

    # event 리스트에 작성일 추가
    i = 0
    for p in event_section_p :
        print(f"p : {p.text}")
        event[i].append(p.text)
        i = i + 1
    print(event)

    # 판다스를 이용한 2차원 리스트를 데이터 프레임 객체로 생성
    event_df = pd.DataFrame(event, columns=['이미지', '제목', '작성일'])
    print(event_df)

    # 데이터 프레임 객체를 JSON으로 가져오기
    json_event_data = event_df.to_json(orient='records', force_ascii=False)
    print(json_event_data)

    # JSON 형식 (문자열 타입)의 py타입(객체타입-리스트/딕셔너리)으로 변환
    result = json.loads(json_event_data)
    print(result)

    return result

