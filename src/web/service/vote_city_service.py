import pandas as pd
import numpy as np

from src.web.service.rankservice import index


def vote_record_list_first(data):
    result = []
    for r in data:
        record_list = [r["poll_city_info_no"], r["gender"], r["first_count"], r["ubirth"]]

        result.append(record_list)

    record = pd.DataFrame(result, columns=("도시_번호", "성별", "선택_수", "생일"))
    record.index = record.index + 1
    print(record)

    record.to_csv("./service/vote_record_first_list.csv", index = True)


def vote_record_list_second(data):
    result = []
    for r in data:
        record_list = [r["poll_city_info_no"], r["gender"], r["second_count"], r["ubirth"]]

        result.append(record_list)

    record = pd.DataFrame(result, columns=("도시_번호", "성별", "선택_수", "생일"))
    record.index = record.index + 1
    print(record)

    record.to_csv("./service/vote_record_second_list.csv", index = True)


def vote_record_list_third(data):
    result = []
    for r in data:
        record_list = [r["poll_city_info_no"], r["gender"], r["third_count"], r["ubirth"]]

        result.append(record_list)

    record = pd.DataFrame(result, columns=("도시_번호", "성별", "선택_수", "생일"))
    record.index = record.index + 1
    print(record)

    record.to_csv("./service/vote_record_third_list.csv", index = True)