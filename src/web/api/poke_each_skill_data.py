
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

poke_data = pd.read_csv("datapokemon.csv", encoding="utf-8", index_col=0)
# poke_skill_data = pd.read_csv("skilldata.csv", encoding="utf-8", index_col=0)

poke_data_kr_name = poke_data["한글이름"]
# poke_skill_data_index = poke_skill_data["스킬이름"]
# print(len(poke_data_kr_name))
# 포켓몬 이름을 URL 인코딩 (이상해씨)
# print(poke_data_kr_name[1])
result = []

for poke_name in poke_data_kr_name:
    print(poke_name)

    # 첫 번째 URL 시도
    poke_url = urllib.parse.quote(poke_name)
    poke_url += "_("
    poke_url += urllib.parse.quote("포켓몬")
    poke_url += ")/9"
    poke_url += urllib.parse.quote("세대")
    poke_url += "_"
    poke_url += urllib.parse.quote("기술")

    url = f"https://pokemon.fandom.com/ko/wiki/{poke_url}"

    try:
        # URL 열기 및 HTML 데이터 가져오기
        resp = urllib.request.urlopen(url)
        htmlData = resp.read()

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"404 Error: {url}, trying /8 instead...")

            # 404 에러 발생 시 두 번째 URL 시도
            poke_url = urllib.parse.quote(poke_name)
            poke_url += "_("
            poke_url += urllib.parse.quote("포켓몬")
            poke_url += ")/8"
            poke_url += urllib.parse.quote("세대")
            poke_url += "_"
            poke_url += urllib.parse.quote("기술")

            url = f"https://pokemon.fandom.com/ko/wiki/{poke_url}"

            try:
                resp = urllib.request.urlopen(url)
                htmlData = resp.read()

            except urllib.error.HTTPError as e:
                if e.code == 404 :
                    print(f"404 Error: {url}, trying /7 instead...")

                    # 404 에러 발생 시 두 번째 URL 시도
                    poke_url = urllib.parse.quote(poke_name)
                    poke_url += "_("
                    poke_url += urllib.parse.quote("포켓몬")
                    poke_url += ")/7"
                    poke_url += urllib.parse.quote("세대")
                    poke_url += "_"
                    poke_url += urllib.parse.quote("기술")

                    url = f"https://pokemon.fandom.com/ko/wiki/{poke_url}"

                    try:
                        resp = urllib.request.urlopen(url)
                        htmlData = resp.read()
                    except urllib.error.HTTPError as e:
                        if e.code == 404:
                            print(f"404 Error: {url}, trying /6 instead...")

                            # 404 에러 발생 시 두 번째 URL 시도
                            poke_url = urllib.parse.quote(poke_name)
                            poke_url += "_("
                            poke_url += urllib.parse.quote("포켓몬")
                            poke_url += ")/6"
                            poke_url += urllib.parse.quote("세대")
                            poke_url += "_"
                            poke_url += urllib.parse.quote("기술")

                            url = f"https://pokemon.fandom.com/ko/wiki/{poke_url}"

                            try:
                                resp = urllib.request.urlopen(url)
                                htmlData = resp.read()
                            except urllib.error.HTTPError as e:
                                print(f"Error: {e}, skipping {poke_name}")
                                continue  # 다른 에러 발생 시 해당 포켓몬을 건너뛰고 다음으로 진행

        else:
            print(f"Error: {e}, skipping {poke_name}")
            continue  # 다른 에러 발생 시 해당 포켓몬을 건너뛰고 다음으로 진행

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(htmlData, "html.parser")

    # 기술 데이터 추출
    w_100 = soup.select_one(".w-100")
    if not w_100:
        print(f"No table found for {poke_name}, skipping...")
        continue  # 테이블이 없을 경우 건너뜀

    t_body = w_100.select_one("tbody")
    trs = t_body.findAll("tr", class_="bg-white")

    for tr in trs:
        tds = tr.text.split()

        if len(tds) > 5:  # 최소 길이 체크
            skill_name = tds[1]
            skill_type = tds[2]
            skill_dam = tds[4].replace("—", "0")  # — 대신 0으로 대체

            skill_list = [skill_name, skill_type, skill_dam]

            # 해당 포켓몬 이름 추가
            skill_list.append(poke_name)

            result.append(skill_list)

# 결과를 DataFrame으로 변환
data = pd.DataFrame(result, columns=("스킬이름", "타입", "위력", "포켓몬"))
data.index = data.index + 1
print(data)

# 결과를 CSV로 저장
data.to_csv("poke_each_skill_data.csv", index=True)
