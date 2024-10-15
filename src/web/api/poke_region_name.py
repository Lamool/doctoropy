import urllib.parse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

name_list = ["관동지방", "성도지방", "호연지방", "신오지방", "하나지방", "칼로스지방", "알로라지방", "가라르지방", "팔데아지방"]
result = []
# Quote the region name for the URL
for i in name_list:
    print(i)
    parse_name_list = urllib.parse.quote(i)
    url = f"https://namu.wiki/w/{parse_name_list}"

    # Create a request object with a User-Agent header
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})

    # Open the URL and read the response
    resp = urlopen(req)
    htmlData = resp.read()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(htmlData, "html.parser")

    # Print the formatted HTML
    # print(soup.prettify())
    first = True

    table = soup.select(".cQN0KU5Q")[4]
    # print(table)
    tbody = table.select_one("tbody")
    # print( tbody )
    for tr in tbody:
        # print(td)
        if first:
            first = False  # 첫 번째 항목 이후로는 실행됨
            continue  # 첫 번째 항목을 건너뜁니다.
        img_tag = tr.find('img', class_ = "z9pP1osj")
        city_info_list = []
        for td in tr:
            # print(td.text)
            city_info_list.append(td.text)
            if img_tag:
                # Extract the 'src' attribute from the 'img' tag
                img_src = img_tag.get('data-src')
                # print(img_src)
                city_info_list[0] = img_src
            else:
                print("")


        print(city_info_list)
        # city_info_list = [img_src, td.text[0]]
        result.append(city_info_list)

print(result)