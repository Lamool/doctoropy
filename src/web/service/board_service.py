# #board_service.py
# from idlelib.iomenu import encoding
# import pandas as pd
# from nltk.corpus import stopwords
# from konlpy.tag import Okt
# from collections import  Counter
# import matplotlib.pyplot as plt
# from matplotlib import  font_manager, rc
# from wordcloud import WordCloud
# import json
#
#
# #1-2 분석할 내용 추출
# #1. 내용이 어떤 타입인지 혹인 후 뽑아내기
# # JSON 문자열로 변환
# # json_string = json.dumps(posts, ensure_ascii=False)
# # JSON 출력
# # print(json_string)
# # jsonData = json.loads(json_string)
# # print(jsonData)
# import  re
#
# btitle = ''
# bcontent = ''
#
# for item in jsonData:
#     # 요소 내 'btitle'과 'bcontent' 키가 존재하면
#     if 'btitle' in item and 'bcontent' in item:
#         btitle = item['btitle']
#         bcontent = item['bcontent']
#         # print(f"{btitle}, {bcontent}")
#
#         #전처리(정규표현식)
#         #분석할 문장내 정규표현식을 이용한 특수문자 제거하고 공백으로 치환,
#         combined_text = ''  # btitle과 bcontent를 결합할 변수
#
#         for item in jsonData:
#             if 'btitle' in item and 'bcontent' in item:
#                 # btitle과 bcontent에서 특수문자를 제거하고 결합
#                 cleaned_title = re.sub(r'[^\w]', '', item['btitle'])
#                 cleaned_content = re.sub(r'[^\w]', '', item['bcontent'])
#                 combined_text += f"{cleaned_title} {cleaned_content} "  # 공백으로 구분하여 결합
#
# # 결과 출력
# # print(combined_text.strip())  # 마지막 공백 제거
#
# #품사 태깅 : 명사 추출
# from konlpy.tag import Okt
# okt=Okt() #품사 태깅할 객체 생성
# words=okt.nouns(combined_text)
# # print(words)
#
# #################################준비끝########################################
# #2. 데이터 분석
# #2-1 단어 빈도 분석
# from collections import Counter
# wordCount=Counter(words)
# # print(wordCount) # 빈도 개수
# #2-2 단어 빈도 딕셔너리 화
# word_count= {}
# for word, count in wordCount.most_common(10):
#     if len(word) >1:
#         word_count[word]=count
# print(word_count)
#
#
#
