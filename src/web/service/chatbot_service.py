#2_마니챗봇
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import  Embedding , LSTM, Dense, Bidirectional, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint
from sklearn.linear_model import LinearRegression

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import  pad_sequences

from konlpy.tag import  Okt
import  re

from src.web.service.info_service import *
from src.web.service.service import *

from src.web.service.weather_service import *
from flask import Flask, request

from src.web.service.board_service import *



def poke_info_search(*kwargs):
    poke_data = pd.read_csv("datapokemon.csv", encoding="utf-8", index_col=0)
    kr_name = poke_data["한글이름"]
    en_name = poke_data["영어이름"]  # en_name을 초기화합니다.
    search_en_name = ""

    # kwargs[0]을 문자열로 강제 변환해 비교에 사용합니다.
    search_name = str(kwargs[0]).split(" ")  # 첫 번째 인자를 문자열로 변환합니다.
    print(search_name)
    for search in search_name:
        for i, name in enumerate(kr_name):
            if name == search:
                search_en_name = en_name.iloc[i]
                print(search_en_name)

    result = poke_detail_info_print(search_en_name)

    return result

def poke_each_skills(*kwargs):
    result = []
    poke_data = pd.read_csv("datapokemon.csv", encoding="utf-8", index_col=0)
    kr_name = poke_data["한글이름"]

    search_name = str(kwargs[0]).split(" ")  # 첫 번째 인자를 문자열로 변환합니다.
    print(search_name)

    for search in search_name:
        for name in kr_name:
            if name == search:
                result = poke_new_skill_info(search)

    return result

# 날씨 함수
def weather_predict(*kwargs):
    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    date = now.day
    hours = now.hour
    minutes = now.minute
    result = predict_weather(year,month,date,hours,minutes)

    return f'인천 날씨는 { result } 입니다.'

# 게시판 인기 키워드 함수
# def popular_board(*kwargs):
#
#     result=count(data)
#     return f'포켓몬 자유게시판의 최근 인기 키워드는 { result } 입니다.'


response_functions = {
    0 : poke_info_search,
    1 : poke_each_skills,
    5 : weather_predict,
    # 6: popular_board

}

#데이터 수집 #
data = [
    {"user" : "피카츄 정보 알려줘", "bot" : "포켓몬 정보를 알려드리겠습니다."},
    {"user" : "피카츄 기술 알려줘", "bot" : "포켓몬이 가질 수 있는 기술을 알려드리겠습니다."},
    {"user" : "가장 강한 포켓몬은 뭔가요?", "bot" : "지우입니다."},
    {"user" : "챗봇 이름은 뭐야?", "bot" :"오박사입니다."},
    {"user" : "넌 뭘 할수있어?", "bot" :"불가능한거빼고모두가능합니다."},
    {"user" : "오늘 날씨 알려줘" ,"bot" : "날씨를 알려드릴게요."},
    {"user" : "게시물 인기 키워드는 뭐야?" ,"bot" : "포켓몬 자유게시판의 현재 인기 키워드를 알려드릴게요."},
    {"user" : "여기는 무슨 사이트야?", "bot" : "포켓몬에관한모든정보를제공해주는웹사이트입니다."},
    {"user" : "고마워요", "bot": "천만에요! 더 필요한 것이 있으면 말씀해주세요."},
    {"user" : "관리자 아이디 알려줘","bot" : "개인정보는알려드릴수없습니다."},
    {"user" : "다른 유저 개인정보 알려줘", "bot" : "불가능합니다."},
    {"user" : "이름이 뭐야?", "bot" : "제이름은오박사입니다."},
    {"user" : "가장 무거운 포켓몬은 뭐야?", "bot" : "가장무거운포켓몬은지우입니다."},
    {"user" : "따끔한 말해줘", "bot" : "질문할시간에운동을하세요."},
    {"user" : "너무해", "bot" : "유감입니다."},
    {"user" : "너무해", "bot" : "네전무입니다.오전무라고불러주세요."},
    {"user" : "오박사님", "bot" : "네?"},
    {"user" : "가장 쓸모없는 기술은 뭐야?", "bot" : "잉어킹의튀어오르기입니다."},
    {"user" : "피카츄 어떻게 생각해?", "bot" : "귀엽다고생각합니다."},
    {"user" : "피카츄 라이츄", "bot" : "파이리꼬부기버터플야도란피죤투또가스~"},
    {"user" : "피", "bot" : "카츄카츄"},
    {"user" : "아...", "bot" : "르세우스"},
    {"user" : "끝말잇기하자", "bot" : "싫습니다저못합니다."},
    {"user" : "포켓몬 정보는?", "bot" : "정보페이지에서확인해주세요~"},
    {"user" : "점메추 해줘", "bot" : "오늘은돈까스가먹고싶네요."},
    {"user" : "팝업스토어 위치 알려줘", "bot" : "현재진행중인팝업스토어는수원에있습니다."},
    {"user" : "만화", "bot" : "현재방영중인애니메이션은포켓몬스터테라스탈입니다."},
    {"user" : "애니","bot" : "현재방영중인애니메이션은포켓몬스터테라스탈입니다."},
    {"user" : "자기소개", "bot" : "안녕하세요오박사입니다."},
    {"user" : "오늘 뭐해?", "bot" : "오늘은잠만보와잠을잘겁니다."},
    {"user" : "오늘은 뭐해?", "bot" : "오늘은잉어킹낚시를할겁니다."},
    {"user" : "리자몽", "bot" : "리자몽은놀랍게도드래곤이아닙니다."},
    {"user" : "귀여워", "bot" : "제가좀귀엽습니다감사합니다."},
    {"user" : "아이템", "bot ": "어떤아이템이궁금하신가요?"},
    {"user" : "나1등했어", "bot" : "대단하시네요."},
{"user": "가장 강한 포켓몬은 뭔가요?", "bot" : "아르세우스 입니다."},
{"user": "가장 강한 포켓몬은?", "bot" : "아르세우스 입니다."},
{"user": "강한 포켓몬은 뭔가요?", "bot" : "아르세우스 입니다."},
{"user": "강한 포켓몬은?", "bot" : "아르세우스 입니다."},
{"user": "1등 포켓몬은 뭔가요?", "bot" : "아르세우스 입니다."},
{"user" : "챗봇 이름은 뭐야?", "bot" :"로토무 입니다."},
{"user" : "이름은 뭐야?", "bot" :"로토무 입니다."},
{"user" : "너의 이름은 뭐야?", "bot" :"로토무 입니다."},
{"user" : "너 이름은 뭐야?", "bot" :"로토무 입니다."},
{"user" : "로봇 이름은 뭐야?", "bot" :"로토무 입니다."},
{"user" : "이름이 뭐야?", "bot" : "제 이름은 로토무 입니다."},
{"user" : "넌 뭘 할 수 있어?", "bot" :"불가능한 것 빼고 모두 가능합니다."},
{"user" : "로토무는 뭘 할 수 있어?", "bot" :"불가능한 것 빼고 모두 가능합니다."},
{"user" : "로토무 뭘 할 수 있어?", "bot" :"불가능한 것 빼고 모두 가능합니다."},
{"user" : "넌 뭘 할 수 있어?", "bot" :"불가능한 것 빼고 모두 가능합니다."},
{"user" : "뭘 할 수 있어?", "bot" :"불가능한 것 빼고 모두 가능합니다."},
{"user" : "여기는 무슨 사이트야?", "bot" : "포켓몬에 관한 모든 정보를 제공 해주는 웹 사이트입니다."},
{"user" : "무슨 사이트야?", "bot" : "포켓몬에 관한 모든 정보를 제공 해주는 웹 사이트입니다."},
{"user" : "이곳은 무슨 사이트야?", "bot" : "포켓몬에 관한 모든 정보를 제공 해주는 웹 사이트입니다."},
{"user" : "여기는 무슨 사이트?", "bot" : "포켓몬에 관한 모든 정보를 제공 해주는 웹 사이트입니다."},
{"user" : "뭔 사이트?", "bot" : "포켓몬에 관한 모든 정보를 제공 해주는 웹 사이트입니다."},
{"user" : "뭔 사이트야?", "bot" : "포켓몬에 관한 모든 정보를 제공 해주는 웹 사이트입니다."},
{"user" : "관리자 아이디 알려줘","bot" : "개인정보는 알려드릴 수 없습니다."},
{"user" : "관리자 아이디","bot" : "개인정보는 알려드릴 수 없습니다."},
{"user" : "관리자 아이디 보여줘","bot" : "개인정보는 알려드릴 수 없습니다."},
{"user" : "관리자 아이디 가르쳐줘","bot" : "개인정보는 알려드릴 수 없습니다."},
{"user" : "관리자 아이디 뭐야?","bot" : "개인정보는 알려드릴 수 없습니다."},
{"user" : "다른 유저 개인정보 알려줘", "bot" : "불가능 합니다."},
{"user" : "다른 유저 정보 알려줘", "bot" : "불가능 합니다."},
{"user" : "다른 유저 개인정보 보여줘", "bot" : "불가능 합니다."},
{"user" : "다른 유저 정보 보여줘", "bot" : "불가능 합니다."},
{"user" : "다른 유저 개인정보 가르쳐줘", "bot" : "불가능 합니다."},
{"user" : "다른 유저 정보 가르쳐줘", "bot" : "불가능 합니다."},
{"user" : "다른 유저 개인정보", "bot" : "불가능 합니다."},
{"user" : "다른 유저 정보", "bot" : "불가능 합니다."},
{"user" : "가장 무거운 포켓몬은 뭐야?", "bot" : "가장 무거운 포켓몬은 지우입니다."},
{"user" : "가장 무거운 뭐야?", "bot" : "가장 무거운 포켓몬은 지우입니다."},
{"user" : "가장 무거운 포켓몬은?", "bot" : "가장 무거운 포켓몬은 지우입니다."},
{"user" : "가장 무거운 포켓몬?", "bot" : "가장 무거운 포켓몬은 지우입니다."},
{"user" : "따끔한 말해줘", "bot" : "질문할 시간에 운동을 하세요."},
{"user" : "따끔한 말", "bot" : "질문할 시간에 운동을 하세요."},
{"user" : "따끔하게 말해줘", "bot" : "질문할 시간에 운동을 하세요."},
{"user" : "진짜 너무해", "bot" : "유감입니다."},
{"user" : "너 진짜 너무해", "bot" : "유감입니다."},
{"user" : "정말 너무해", "bot" : "유감입니다."},
{"user" : "너무해", "bot" : "유감입니다."},
{"user" : "너 너무해", "bot" : "네 전무입니다. 로전무 라고 불러주세요."},
{"user" : "너 완전 너무해", "bot" : "네 전무입니다. 로전무 라고 불러주세요."},
{"user" : "넌 너무해", "bot" : "네 전무입니다. 로전무 라고 불러주세요."},
{"user" : "넌 완전 너무해", "bot" : "네 전무입니다. 로전무 라고 불러주세요."},
{"user" : "로토무", "bot" : "네?"},
{"user" : "야 로토무", "bot" : "네?"},
{"user" : "이봐 로토무", "bot" : "네?"},
{"user" : "어이 로토무", "bot" : "네?"},
{"user" : "야 로봇", "bot" : "네?"},
{"user" : "어이 로봇", "bot" : "네?"},
{"user" : "가장 쓸모없는 기술은 뭐야?", "bot" : "잉어킹의 튀어오르기 입니다."},
{"user" : "가장 쓸모없는 기술은?", "bot" : "잉어킹의 튀어오르기 입니다."},
{"user" : "쓸모없는 기술은 뭐야?", "bot" : "잉어킹의 튀어오르기 입니다."},
{"user" : "쓸모없는 기술은?", "bot" : "잉어킹의 튀어오르기 입니다."},
{"user" : "피카츄 어떻게 생각해?", "bot" : "귀엽다고 생각합니다."},
{"user" : "피카츄 귀엽다고 생각해?", "bot" : "귀엽다고 생각합니다."},
{"user" : "피카츄 멋지다고 생각해?", "bot" : "귀엽다고 생각합니다."},
{"user" : "피카츄 어때?", "bot" : "귀엽다고 생각합니다."},
{"user" : "피카츄 어떤 거 같아?", "bot" : "귀엽다고 생각합니다."},
{"user" : "피카츄 멋진 거 같아?", "bot" : "귀엽다고 생각합니다."},
{"user" : "피카츄 귀여운 거 같아?", "bot" : "귀엽다고 생각합니다."},
{"user" : "피카츄 라이츄", "bot" : "파이리 꼬부기 버터플 야도란 피죤투 또가스~"},
{"user" : "끝말잇기 하자", "bot" : "싫습니다 전 못합니다."},
{"user" : "끝말잇기", "bot" : "싫습니다 전 못합니다."},
{"user" : "끝말잇기 할래?", "bot" : "싫습니다 전 못합니다."},
{"user" : "끝말잇기 어때?", "bot" : "싫습니다 전 못합니다."},
{"user" : "끝말잇기 하고싶어", "bot" : "싫습니다 전 못합니다."},
{"user" : "끝말잇기 할까?", "bot" : "싫습니다 전 못합니다."},
{"user" : "포켓몬 정보는?", "bot" : "정보 페이지에서 확인해주세요"},
{"user" : "포켓몬 정보", "bot" : "정보 페이지에서 확인해주세요"},
{"user" : "포켓몬 정보 알려줘", "bot" : "정보 페이지에서 확인해주세요"},
{"user" : "포켓몬 정보 가르쳐줘", "bot" : "정보 페이지에서 확인해주세요"},
{"user" : "포켓몬 정보 확인", "bot" : "정보 페이지에서 확인해주세요"},
{"user" : "포켓몬 정보 출력", "bot" : "정보 페이지에서 확인해주세요"},
{"user" : "점심 메뉴 추천 해줘", "bot" : "오늘은 돈까스가 먹고싶네요."},
{"user" : "점심 메뉴 추천", "bot" : "오늘은 돈까스가 먹고싶네요."},
{"user" : "점심 메뉴", "bot" : "오늘은 돈까스가 먹고싶네요."},
{"user" : "점심 뭐 먹을까?", "bot" : "오늘은 돈까스가 먹고싶네요."},
{"user" : "점심 뭐 먹지?", "bot" : "오늘은 돈까스가 먹고싶네요."},
{"user" : "점심 먹어?", "bot" : "오늘은 돈까스가 먹고싶네요."},
{"user" : "팝업스토어 위치 알려줘", "bot" : "현재 진행 중인 팝업스토어는 수원에 있습니다."},
{"user" : "팝업스토어 위치", "bot" : "현재 진행 중인 팝업스토어는 수원에 있습니다."},
{"user" : "팝업스토어 위치는?", "bot" : "현재 진행 중인 팝업스토어는 수원에 있습니다."},
{"user" : "진행중인 팝업스토어 위치 알려줘", "bot" : "현재 진행 중인 팝업스토어는 수원에 있습니다."},
{"user" : "진행중인 팝업스토어", "bot" : "현재 진행 중인 팝업스토어는 수원에 있습니다."},
{"user" : "진행중인 팝업스토어 위치", "bot" : "현재 진행 중인 팝업스토어는 수원에 있습니다."},
{"user" : "현재 진행중인 팝업스토어", "bot" : "현재 진행 중인 팝업스토어는 수원에 있습니다."},
{"user" : "현재 진행중인 팝업스토어 위치", "bot" : "현재 진행 중인 팝업스토어는 수원에 있습니다."},
{"user" : "현재 진행중인 팝업스토어 알려줘", "bot" : "현재 진행 중인 팝업스토어는 수원에 있습니다."},
{"user" : "현재 진행중인 팝업스토어 가르쳐줘", "bot" : "현재 진행 중인 팝업스토어는 수원에 있습니다."},
{"user" : "진행중인 팝업스토어 알려줘", "bot" : "현재 진행 중인 팝업스토어는 수원에 있습니다."},
{"user" : "진행중인 팝업스토어 가르쳐줘", "bot" : "현재 진행 중인 팝업스토어는 수원에 있습니다."},
{"user" : "자기소개", "bot" : "안녕하세요 로토무 입니다."},
{"user" : "자기소개 해봐", "bot" : "안녕하세요 로토무 입니다."},
{"user" : "자기소개 해줘", "bot" : "안녕하세요 로토무 입니다."},
{"user" : "자기소개 해", "bot" : "안녕하세요 로토무 입니다."},
{"user" : "자기소개 해라", "bot" : "안녕하세요 로토무 입니다."},
{"user" : "자기소개 어때?", "bot" : "안녕하세요 로토무 입니다."},
{"user" : "자기소개 시작", "bot" : "안녕하세요 로토무 입니다."},
{"user" : "오늘 뭐해?", "bot" : "오늘은 잠만보와 잠을 잘겁니다."},
{"user" : "오늘은 뭐해?", "bot" : "오늘은 잠만보와 잠을 잘겁니다."},
{"user" : "오늘 뭐 할 거야?", "bot" : "오늘은 잠만보와 잠을 잘겁니다."},
{"user" : "오늘은 뭐 할 거야?", "bot" : "오늘은 잠만보와 잠을 잘겁니다."},
{"user" : "오늘 뭐 할래?", "bot" : "오늘은 잠만보와 잠을 잘겁니다."},
{"user" : "오늘은 뭐 할 거 있어?", "bot" : "오늘은 잠만보와 잠을 잘겁니다."},
{"user" : "오늘 할 거 있어?", "bot" : "오늘은 잠만보와 잠을 잘겁니다."},
{"user" : "오늘 일정 있어?", "bot" : "오늘은 잠만보와 잠을 잘겁니다."},
{"user" : "오늘은 일정 있어?", "bot" : "오늘은 잠만보와 잠을 잘겁니다."},
{"user" : "리자몽 정보", "bot" : "리자몽은 놀랍게도 드래곤이 타입이 아닙니다."},
{"user" : "리자몽 비밀 정보", "bot" : "리자몽은 놀랍게도 드래곤이 타입이 아닙니다."},
{"user" : "리자몽 상세 정보", "bot" : "리자몽은 놀랍게도 드래곤이 타입이 아닙니다."},
{"user" : "리자몽 비밀", "bot" : "리자몽은 놀랍게도 드래곤이 타입이 아닙니다."},
{"user" : "리자몽의 정보", "bot" : "리자몽은 놀랍게도 드래곤이 타입이 아닙니다."},
{"user" : "리자몽의 비밀", "bot" : "리자몽은 놀랍게도 드래곤이 타입이 아닙니다."},
{"user" : "리자몽의 상세 정보", "bot" : "리자몽은 놀랍게도 드래곤이 타입이 아닙니다."},
{"user" : "리자몽의 비밀 정보", "bot" : "리자몽은 놀랍게도 드래곤이 타입이 아닙니다."},
{"user" : "너 귀여워", "bot" : "제가 좀 귀엽습니다 감사합니다."},
{"user" : "너 진짜 귀여워", "bot" : "제가 좀 귀엽습니다 감사합니다."},
{"user" : "너 귀엽다", "bot" : "제가 좀 귀엽습니다 감사합니다."},
{"user" : "너 정말 귀여워", "bot" : "제가 좀 귀엽습니다 감사합니다."},
{"user" : "너 진짜 귀엽다", "bot" : "제가 좀 귀엽습니다 감사합니다."},
{"user" : "너 정말 귀엽다", "bot" : "제가 좀 귀엽습니다 감사합니다."},
{"user" : "너 귀엽구나?", "bot" : "제가 좀 귀엽습니다 감사합니다."},
{"user" : "너 진짜 귀엽구나?", "bot" : "제가 좀 귀엽습니다 감사합니다."},
{"user" : "너 정말 귀엽구나?", "bot" : "제가 좀 귀엽습니다 감사합니다."},
{"user" : "너 완전 귀엽구나?", "bot" : "제가 좀 귀엽습니다 감사합니다."},
{"user" : "너 완전 귀엽다?", "bot" : "제가 좀 귀엽습니다 감사합니다."},
{"user" : "아이템 정보", "bot" : "어떤 아이템이 궁금하신가요?"},
{"user" : "아이템 목록", "bot" : "어떤 아이템이 궁금하신가요?"},
{"user" : "나 1등 했어", "bot" : "대단하시네요."},
{"user" : "나 1위 했어", "bot" : "대단하시네요."},
{"user" : "나 1등 했다", "bot" : "대단하시네요."},
{"user" : "나 1위 했다", "bot" : "대단하시네요."},
{"user" : "나 1등 처음 했어", "bot" : "대단하시네요."},
{"user" : "나 1등 두번 했어", "bot" : "대단하시네요."},
{"user" : "나 1등 세번 했어", "bot" : "대단하시네요."},
{"user" : "나 1위 처음 했어", "bot" : "대단하시네요."},
{"user" : "나 1위 두번 했어", "bot" : "대단하시네요."},
{"user" : "나 1위 세번 했어", "bot" : "대단하시네요."},
{"user" : "나 일등 했어", "bot" : "대단하시네요."},
{"user" : "나 일위 했어", "bot" : "대단하시네요."},
{"user" : "나 일등 했다", "bot" : "대단하시네요."},
{"user" : "나 일위 했다", "bot" : "대단하시네요."},
{"user" : "나 일등 처음 했어", "bot" : "대단하시네요."},
{"user" : "나 일등 두번 했어", "bot" : "대단하시네요."},
{"user" : "나 일등 세번 했어", "bot" : "대단하시네요."},
{"user" : "나 일위 처음 했어", "bot" : "대단하시네요."},
{"user" : "나 일위 두번 했어", "bot" : "대단하시네요."},
{"user" : "나 일위 세번 했어", "bot" : "대단하시네요."},
{"user" : "나 2등 했어", "bot" : "멋지네요."},
{"user" : "나 2위 했어", "bot" : "멋지네요."},
{"user" : "나 2등 했다", "bot" : "멋지네요."},
{"user" : "나 2위 했다", "bot" : "멋지네요."},
{"user" : "나 2등 처음 했어", "bot" : "멋지네요."},
{"user" : "나 2등 두번 했어", "bot" : "멋지네요."},
{"user" : "나 2등 세번 했어", "bot" : "멋지네요."},
{"user" : "나 2위 처음 했어", "bot" : "멋지네요."},
{"user" : "나 2위 두번 했어", "bot" : "멋지네요."},
{"user" : "나 2위 세번 했어", "bot" : "멋지네요."},
{"user" : "나 이등 했어", "bot" : "멋지네요."},
{"user" : "나 이위 했어", "bot" : "멋지네요."},
{"user" : "나 이등 했다", "bot" : "멋지네요."},
{"user" : "나 이위 했다", "bot" : "멋지네요."},
{"user" : "나 이등 처음 했어", "bot" : "멋지네요."},
{"user" : "나 이등 두번 했어", "bot" : "멋지네요."},
{"user" : "나 이등 세번 했어", "bot" : "멋지네요."},
{"user" : "나 이위 처음 했어", "bot" : "멋지네요."},
{"user" : "나 이위 두번 했어", "bot" : "멋지네요."},
{"user" : "나 이위 세번 했어", "bot" : "멋지네요."},
{"user" : "나 3등 했어", "bot" : "근사하네요."},
{"user" : "나 3위 했어", "bot" : "근사하네요."},
{"user" : "나 3등 했다", "bot" : "근사하네요."},
{"user" : "나 3위 했다", "bot" : "근사하네요."},
{"user" : "나 3등 처음 했어", "bot" : "근사하네요."},
{"user" : "나 3등 두번 했어", "bot" : "근사하네요."},
{"user" : "나 3등 세번 했어", "bot" : "근사하네요."},
{"user" : "나 3위 처음 했어", "bot" : "근사하네요."},
{"user" : "나 3위 두번 했어", "bot" : "근사하네요."},
{"user" : "나 3위 세번 했어", "bot" : "근사하네요."},
{"user" : "나 삼등 했어", "bot" : "근사하네요."},
{"user" : "나 삼위 했어", "bot" : "근사하네요."},
{"user" : "나 삼등 했다", "bot" : "근사하네요."},
{"user" : "나 삼위 했다", "bot" : "근사하네요."},
{"user" : "나 삼등 처음 했어", "bot" : "근사하네요."},
{"user" : "나 삼등 두번 했어", "bot" : "근사하네요."},
{"user" : "나 삼등 세번 했어", "bot" : "근사하네요."},
{"user" : "나 삼위 처음 했어", "bot" : "근사하네요."},
{"user" : "나 삼위 두번 했어", "bot" : "근사하네요."},
{"user" : "나 삼위 세번 했어", "bot" : "근사하네요."},
{"user" : "가장 좋아하는 마을은 뭐야?","bot" : "태초마을 입니다."},
{"user" : "가장 마음에 드는 마을은 뭐야?","bot" : "태초마을 입니다."},
{"user" : "가장 호감인 마을은 뭐야?","bot" : "태초마을 입니다."},
{"user" : "가장 좋아하는 마을은?","bot" : "태초마을 입니다."},
{"user" : "가장 마음에 드는 마을은?","bot" : "태초마을 입니다."},
{"user" : "가장 호감인 마을은?","bot" : "태초마을 입니다."},
{"user" : "좋아하는 마을은?","bot" : "태초마을 입니다."},
{"user" : "마음에 드는 마을은?","bot" : "태초마을 입니다."},
{"user" : "호감인 마을은?","bot" : "태초마을 입니다."},
{"user" : "가장 싫어하는 마을은 뭐야?","bot" : "보라시티 입니다."},
{"user" : "가장 마음에 안 드는 마을은 뭐야?","bot" : "보라시티 입니다."},
{"user" : "가장 비호감인 마을은 뭐야?","bot" : "보라시티 입니다."},
{"user" : "가장 안 좋아하는 마을은?","bot" : "보라시티 입니다."},
{"user" : "가장 마음에 안 드는 마을은?","bot" : "보라시티 입니다."},
{"user" : "가장 비호감인 마을은?","bot" : "보라시티 입니다."},
{"user" : "안 좋아하는 마을은?","bot" : "보라시티 입니다."},
{"user" : "마음에 안 드는 마을은?","bot" : "보라시티 입니다."},
{"user" : "비호감인 마을은?","bot" : "보라시티 입니다."},
{"user" : "사용 방법 알려줘","bot" : "대부분 저에게 맡기시면 됩니다."},
{"user" : "너 사용 방법 알려줘","bot" : "대부분 저에게 맡기시면 됩니다."},
{"user" : "로토무 사용 방법 알려줘","bot" : "대부분 저에게 맡기시면 됩니다."},
{"user" : "사이트 사용 방법 알려줘","bot" : "대부분 저에게 맡기시면 됩니다."},
{"user" : "여기서 뭘 할 수 있어?","bot" : "포켓몬에 관한 것 들을 할수 있습니다."},
{"user" : "이 사이트는 뭘 할 수 있어?","bot" : "포켓몬에 관한 것 들을 할수 있습니다."},
{"user" : "이 사이트 에서 뭘 할 수 있어?","bot" : "포켓몬에 관한 것 들을 할수 있습니다."},
{"user" : "너는 무슨 포켓몬이야?" ,"bot" : "저는 No.0479 포켓몬 로토무입니다."},
{"user" : "로토무는 무슨 포켓몬이야?" ,"bot" : "저는 No.0479 포켓몬 로토무입니다."},
{"user" : "가장 강한 포켓몬 기술은 뭐야?" ,"bot" : "제 생각은 '아르세우스' 가 사용하는 심판의 뭉치 라고 생각합니다."},
{"user" : "너가 생각한 가장 강한 포켓몬 기술은 뭐야?" ,"bot" : "제 생각은 '아르세우스' 가 사용하는 심판의 뭉치 라고 생각합니다."},
{"user" : "너가 생각한 가장 강한 기술은 뭐야?" ,"bot" : "제 생각은 '아르세우스' 가 사용하는 심판의 뭉치 라고 생각합니다."},
{"user" : "피카츄 기술은 뭐가 있어?" ,"bot" : "대표적으로 백만볼트가 있습니다."},
{"user" : "피카츄 기술 뭐가 있어?" ,"bot" : "대표적으로 백만볼트가 있습니다."},
{"user" : "피카츄 기술" ,"bot" : "대표적으로 백만볼트가 있습니다."},
{"user" : "피카츄 기술에는 뭐가 있어?" ,"bot" : "대표적으로 백만볼트가 있습니다."},
{"user" : "막치기는 뭐야?" ,"bot" : "긴 꼬리나 손 등을 사용하여 상대를 때려서 공격하는 기술로 위력은 40 명중률은 100 사용횟수는 35회 입니다."},
{"user" : "막치기가 뭐야?" ,"bot" : "긴 꼬리나 손 등을 사용하여 상대를 때려서 공격하는 기술로 위력은 40 명중률은 100 사용횟수는 35회 입니다."},
{"user" : "막치기 정보" ,"bot" : "긴 꼬리나 손 등을 사용하여 상대를 때려서 공격하는 기술로 위력은 40 명중률은 100 사용횟수는 35회 입니다."},
{"user" : "막치기" ,"bot" : "긴 꼬리나 손 등을 사용하여 상대를 때려서 공격하는 기술로 위력은 40 명중률은 100 사용횟수는 35회 입니다."},
{"user" : "태권당수는 뭐야?" ,"bot" : "날카로운 당수로 상대를 때려서 공격한다. 급소에 맞을 확률이 높은 기술입니다. 위력50 명중률 100 사용횟수는 25회 입니다."},
{"user" : "태권당수가 뭐야?" ,"bot" : "날카로운 당수로 상대를 때려서 공격한다. 급소에 맞을 확률이 높은 기술입니다. 위력50 명중률 100 사용횟수는 25회 입니다."},
{"user" : "태권당수 정보" ,"bot" : "날카로운 당수로 상대를 때려서 공격한다. 급소에 맞을 확률이 높은 기술입니다. 위력50 명중률 100 사용횟수는 25회 입니다."},
{"user" : "태권당수" ,"bot" : "날카로운 당수로 상대를 때려서 공격한다. 급소에 맞을 확률이 높은 기술입니다. 위력50 명중률 100 사용횟수는 25회 입니다."},
{"user" : "연속뺨치기는 뭐야?" ,"bot" : "연속 뺨치기로 상대를 때려서 공격한다. 2-5회 동안 연속으로 사용하는 기술입니다. 위력15 명중률 85 사용횟수는 10회 입니다."},
{"user" : "연속뺨치기가 뭐야?" ,"bot" : "연속 뺨치기로 상대를 때려서 공격한다. 2-5회 동안 연속으로 사용하는 기술입니다. 위력15 명중률 85 사용횟수는 10회 입니다."},
{"user" : "연속뺨치기 뭐야?" ,"bot" : "연속 뺨치기로 상대를 때려서 공격한다. 2-5회 동안 연속으로 사용하는 기술입니다. 위력15 명중률 85 사용횟수는 10회 입니다."},
{"user" : "연속뺨치기 정보" ,"bot" : "연속 뺨치기로 상대를 때려서 공격한다. 2-5회 동안 연속으로 사용하는 기술입니다. 위력15 명중률 85 사용횟수는 10회 입니다."},
{"user" : "연속뺨치기" ,"bot" : "연속 뺨치기로 상대를 때려서 공격한다. 2-5회 동안 연속으로 사용하는 기술입니다. 위력15 명중률 85 사용횟수는 10회 입니다."},
{"user" : "연속펀치는 뭐야?" ,"bot" : "노도 같은 펀치로 상대를 세게 때려서 공격한다. 2-5회 동안 연속으로 사용하는 기술입니다. 위력18 명중률 85 사용횟수는 15회 입니다."},
{"user" : "연속펀치가 뭐야?" ,"bot" : "노도 같은 펀치로 상대를 세게 때려서 공격한다. 2-5회 동안 연속으로 사용하는 기술입니다. 위력18 명중률 85 사용횟수는 15회 입니다."},
{"user" : "연속펀치 뭐야?" ,"bot" : "노도 같은 펀치로 상대를 세게 때려서 공격한다. 2-5회 동안 연속으로 사용하는 기술입니다. 위력18 명중률 85 사용횟수는 15회 입니다."},
{"user" : "연속펀치 정보" ,"bot" : "노도 같은 펀치로 상대를 세게 때려서 공격한다. 2-5회 동안 연속으로 사용하는 기술입니다. 위력18 명중률 85 사용횟수는 15회 입니다."},
{"user" : "연속펀치" ,"bot" : "노도 같은 펀치로 상대를 세게 때려서 공격한다. 2-5회 동안 연속으로 사용하는 기술입니다. 위력18 명중률 85 사용횟수는 15회 입니다."},
{"user" : "메가톤펀치는 뭐야?" ,"bot" : "힘을 담은 펀치로 상대를 공격하는 기술입니다. 위력80 명중률 85 사용횟수는 20회 입니다."},
{"user" : "메가톤펀치가 뭐야?" ,"bot" : "힘을 담은 펀치로 상대를 공격하는 기술입니다. 위력80 명중률 85 사용횟수는 20회 입니다."},
{"user" : "메가톤펀치 뭐야?" ,"bot" : "힘을 담은 펀치로 상대를 공격하는 기술입니다. 위력80 명중률 85 사용횟수는 20회 입니다."},
{"user" : "메가톤펀치 정보" ,"bot" : "힘을 담은 펀치로 상대를 공격하는 기술입니다. 위력80 명중률 85 사용횟수는 20회 입니다."},
{"user" : "메가톤펀치" ,"bot" : "힘을 담은 펀치로 상대를 공격하는 기술입니다. 위력80 명중률 85 사용횟수는 20회 입니다."},
{"user" : "고양이돈받기는 뭐야?" ,"bot" : "상대의 몸에 금화를 던져서 공격한다. 전투 후에 돈을 얻는 기술입니다. 위력40 명중률 100 사용횟수는 20회 입니다."},
{"user" : "고양이돈받기가 뭐야?" ,"bot" : "상대의 몸에 금화를 던져서 공격한다. 전투 후에 돈을 얻는 기술입니다. 위력40 명중률 100 사용횟수는 20회 입니다."},
{"user" : "고양이돈받기 뭐야?" ,"bot" : "상대의 몸에 금화를 던져서 공격한다. 전투 후에 돈을 얻는 기술입니다. 위력40 명중률 100 사용횟수는 20회 입니다."},
{"user" : "고양이돈받기 정보" ,"bot" : "상대의 몸에 금화를 던져서 공격한다. 전투 후에 돈을 얻는 기술입니다. 위력40 명중률 100 사용횟수는 20회 입니다."},
{"user" : "고양이돈받기" ,"bot" : "상대의 몸에 금화를 던져서 공격한다. 전투 후에 돈을 얻는 기술입니다. 위력40 명중률 100 사용횟수는 20회 입니다."},
{"user" : "불꽃펀치는 뭐야?" ,"bot" : "불꽃을 담은 펀치로 상대를 공격한다. 화상 상태가 되는 경우가 있는 기술입니다. 위력75 명중률 100 사용횟수는 15회 입니다."},
{"user" : "불꽃펀치가 뭐야?" ,"bot" : "불꽃을 담은 펀치로 상대를 공격한다. 화상 상태가 되는 경우가 있는 기술입니다. 위력75 명중률 100 사용횟수는 15회 입니다."},
{"user" : "불꽃펀치 뭐야?" ,"bot" : "불꽃을 담은 펀치로 상대를 공격한다. 화상 상태가 되는 경우가 있는 기술입니다. 위력75 명중률 100 사용횟수는 15회 입니다."},
{"user" : "불꽃펀치 정보" ,"bot" : "불꽃을 담은 펀치로 상대를 공격한다. 화상 상태가 되는 경우가 있는 기술입니다. 위력75 명중률 100 사용횟수는 15회 입니다."},
{"user" : "불꽃펀치" ,"bot" : "불꽃을 담은 펀치로 상대를 공격한다. 화상 상태가 되는 경우가 있는 기술입니다. 위력75 명중률 100 사용횟수는 15회 입니다."},
{"user" : "냉동펀치는 뭐야?" ,"bot" : "냉기를 담은 펀치로 상대를 공격한다. 얼음 상태가 되는 경우가 있는 기술입니다. 위력75 명중률 100 사용횟수는 15회 입니다."},
{"user" : "냉동펀치가 뭐야?" ,"bot" : "냉기를 담은 펀치로 상대를 공격한다. 얼음 상태가 되는 경우가 있는 기술입니다. 위력75 명중률 100 사용횟수는 15회 입니다."},
{"user" : "냉동펀치 뭐야?" ,"bot" : "냉기를 담은 펀치로 상대를 공격한다. 얼음 상태가 되는 경우가 있는 기술입니다. 위력75 명중률 100 사용횟수는 15회 입니다."},
{"user" : "냉동펀치 정보", "bot" : "냉기를 담은 펀치로 상대를 공격한다. 얼음 상태가 되는 경우가 있는 기술입니다. 위력75 명중률 100 사용횟수는 15회 입니다."},
{"user" : "냉동펀치" ,"bot" : "냉기를 담은 펀치로 상대를 공격한다. 얼음 상태가 되는 경우가 있는 기술입니다. 위력75 명중률 100 사용횟수는 15회 입니다."},
{"user" : "대전에서 이기려면 어떻게 해야 해?" ,"bot" : "확률을 사용해서 분석을 하는걸 추천합니다."},
{"user" : "대전에서 이기려면?" ,"bot" : "확률을 사용해서 분석을 하는걸 추천합니다."},
{"user" : "대전에서 이기는 방법?" ,"bot" : "확률을 사용해서 분석을 하는걸 추천합니다."},
{"user" : "대전에서 이기는 방법" ,"bot" : "확률을 사용해서 분석을 하는걸 추천합니다."},
{"user" : "대전에서 필승 방법" ,"bot" : "확률을 사용해서 분석을 하는걸 추천합니다."},
{"user" : "대전에서 필승 방법?" ,"bot" : "확률을 사용해서 분석을 하는걸 추천합니다."},
{"user" : "대전에서 필승 방법 알려줘" ,"bot" : "확률을 사용해서 분석을 하는걸 추천합니다."},
{"user" : "대전에서 이기는 방법 알려줘" ,"bot" : "확률을 사용해서 분석을 하는걸 추천합니다."},
{"user" : "기술 하나만 추천해줘" ,"bot" : "튀어오르기 어떠세요?"},
{"user" : "기술 하나만 추천해" ,"bot" : "튀어오르기 어떠세요?"},
{"user" : "기술 하나만 추천" ,"bot" : "튀어오르기 어떠세요?"},
{"user" : "기술 추천해줘" ,"bot" : "튀어오르기 어떠세요?"},
{"user" : "기술 추천해" ,"bot" : "튀어오르기 어떠세요?"},
{"user" : "기술 추천" ,"bot" : "튀어오르기 어떠세요?"},
{"user" : "가장 비싼 아이템은 뭐야?" ,"bot" : "금구슬 입니다."},
{"user" : "제일 비싼 아이템은 뭐야?" ,"bot" : "금구슬 입니다."},
{"user" : "가장 비싼 아이템은?" ,"bot" : "금구슬 입니다."},
{"user" : "제일 비싼 아이템은?" ,"bot" : "금구슬 입니다."},
{"user" : "가장 비싼 아이템은 뭘까?" ,"bot" : "금구슬 입니다."},
{"user" : "가장 비싼 아이템은 뭐지?" ,"bot" : "금구슬 입니다."},
{"user" : "제일 비싼 아이템은 뭐지?" ,"bot" : "금구슬 입니다."},
{"user" : "제일 값이 많이 나가는 아이템은 뭘까?" ,"bot" : "금구슬 입니다."},
{"user" : "제일 값이 많이 나가는 아이템은 뭐야?" ,"bot" : "금구슬 입니다."},
{"user" : "제일 값이 많이 나가는 아이템은 뭐지?" ,"bot" : "금구슬 입니다."},
{"user" : "두번째로 비싼 아이템은 뭐야?" ,"bot" : "맛있는꼬리 입니다."},
{"user" : "두번째로 비싼 아이템은?" ,"bot" : "맛있는꼬리 입니다."},
{"user" : "두번째로 비싼 아이템은 뭘까?" ,"bot" : "맛있는꼬리 입니다."},
{"user" : "두번째로 비싼 아이템은 뭐지?" ,"bot" : "맛있는꼬리 입니다."},
{"user" : "두번째로 비싼 아이템은 뭐?" ,"bot" : "맛있는꼬리 입니다."},
{"user" : "세번째로 비싼 아이템은 뭐야?" ,"bot" : "별의모래 입니다."},
{"user" : "세번째로 비싼 아이템은 뭘까?" ,"bot" : "별의모래 입니다."},
{"user" : "세번째로 비싼 아이템은 뭐지?" ,"bot" : "별의모래 입니다."},
{"user" : "세번째로 비싼 아이템은 뭐?" ,"bot" : "별의모래 입니다."},
{"user" : "세번째로 비싼 아이템은?" ,"bot" : "별의모래 입니다."},
{"user" : "네번째로 비싼 아이템은 뭐야?" ,"bot" : "별의조각 입니다."},
{"user" : "네번째로 비싼 아이템은 뭐지?" ,"bot" : "별의조각 입니다."},
{"user" : "네번째로 비싼 아이템은 뭘까?" ,"bot" : "별의조각 입니다."},
{"user" : "네번째로 비싼 아이템은 무엇?" ,"bot" : "별의조각 입니다."},
{"user" : "네번째로 비싼 아이템은?" ,"bot" : "별의조각 입니다."},
{"user" : "다섯번째로 비싼 아이템은 뭐야?" ,"bot" : "잘 모르겠습니다."},
{"user" : "다섯번째로 비싼 아이템은 뭐지?" ,"bot" : "잘 모르겠습니다."},
{"user" : "다섯번째로 비싼 아이템은 무엇?" ,"bot" : "잘 모르겠습니다."},
{"user" : "다섯번째로 비싼 아이템은 뭘까?" ,"bot" : "잘 모르겠습니다."},
{"user" : "다섯번째로 비싼 아이템은?" ,"bot" : "잘 모르겠습니다."},
{"user" : "가장 싼 아이템은 뭐야?" ,"bot" : "큰 죽순 입니다."},
{"user" : "가장 싼 아이템은 뭐지?" ,"bot" : "큰 죽순 입니다."},
{"user" : "가장 싼 아이템은 뭘까?" ,"bot" : "큰 죽순 입니다."},
{"user" : "가장 싼 아이템은 무엇?" ,"bot" : "큰 죽순 입니다."},
{"user" : "가장 싼 아이템은?" ,"bot" : "큰 죽순 입니다."},
{"user" : "두번째로 싼 아이템은 뭐야?" ,"bot" : "작은 죽순 입니다."},
{"user" : "두번째로 싼 아이템은 뭐지?" ,"bot" : "작은 죽순 입니다."},
{"user" : "두번째로 싼 아이템은 뭘까?" ,"bot" : "작은 죽순 입니다."},
{"user" : "두번째로 싼 아이템은?" ,"bot" : "작은 죽순 입니다."},
{"user" : "세번째로 싼 아이템은 뭐야?" ,"bot" : "잘모르겠네요"},
{"user" : "세번째로 싼 아이템은 뭐지?" ,"bot" : "잘모르겠네요"},
{"user" : "세번째로 싼 아이템은 뭘까?" ,"bot" : "잘모르겠네요"},
{"user" : "세번째로 싼 아이템은?" ,"bot" : "잘모르겠네요"},
{"user" : "가장 좋은 카드는 뭐야?" ,"bot" : "현재 가장 좋은 카드는 날뛰는우레ex 카드입니다."},
{"user" : "가장 좋은 카드는 뭐지?" ,"bot" : "현재 가장 좋은 카드는 날뛰는우레ex 카드입니다."},
{"user" : "가장 좋은 카드는 뭘까?" ,"bot" : "현재 가장 좋은 카드는 날뛰는우레ex 카드입니다."},
{"user" : "가장 좋은 카드는?" ,"bot" : "현재 가장 좋은 카드는 날뛰는우레ex 카드입니다."},
{"user" : "현재 가장 좋은 카드는 뭐야?" ,"bot" : "현재 가장 좋은 카드는 날뛰는우레ex 카드입니다."},
{"user" : "현재 가장 좋은 카드는 뭐지?" ,"bot" : "현재 가장 좋은 카드는 날뛰는우레ex 카드입니다."},
{"user" : "일순위 카드는 뭐야?" ,"bot" : "현재 가장 좋은 카드는 날뛰는우레ex 카드입니다."},
{"user" : "첫번째 좋은 카드는 뭐야?","bot"  : "현재 가장 좋은 카드는 날뛰는우레ex 카드입니다."},
{"user" : "1순위 카드는 뭐야?" ,"bot" : "현재 가장 좋은 카드는 날뛰는우레ex 카드입니다."},
{"user" : "두번째 좋은 카드는 뭐야?" ,"bot" : "리자몽ex 카드입니다."},
{"user" : "2순위 카드는 뭐야?" ,"bot" : "리자몽ex 카드입니다."},
{"user" : "이순위 카드는 뭐야?" ,"bot" : "리자몽ex 카드입니다."},
{"user" : "세번째 좋은 카드는 뭐야?" ,"bot" : "드래펄트ex 카드입니다."},
{"user" : "3순위 카드는 뭐야?","bot"  : "드래펄트ex 카드입니다."},
{"user" : "삼순위 카드는 뭐야?" ,"bot" : "드래펄트ex 카드입니다."},
{"user" : "네번째 좋은 카드는 뭐야?" ,"bot" : "분석중이라 알려드릴수가 없네요."},
{"user" : "4순위 카드는 뭐야?" ,"bot" : "분석중이라 알려드릴수가 없네요."},
{"user" : "사순위 카드는 뭐야?" ,"bot" : "분석중이라 알려드릴수가 없네요."},
{"user" : "가장 귀여운 포켓몬은?" ,"bot" : "제 생각은 파밀리쥐 입니다."},
{"user" : "가장 귀여운 포켓몬은 뭐야?" ,"bot" : "제 생각은 파밀리쥐 입니다."},
{"user" : "가장 귀여운 포켓몬은 뭐라고 생각해?" ,"bot" : "제 생각은 파밀리쥐 입니다."},
{"user" : "귀여운 포켓몬은?" ,"bot" : "제 생각은 파밀리쥐 입니다."},
{"user" : "네 생각에 가장 귀여운 포켓몬은?" ,"bot" : "제 생각은 파밀리쥐 입니다."},
{"user" : "너는 가장 귀여운 포켓몬이 뭐라고 생각해?" ,"bot" : "제 생각은 파밀리쥐 입니다."},
{"user" : "너가 생각한 가장 귀여운 포켓몬은?" ,"bot" : "제 생각은 파밀리쥐 입니다."},
{"user" : "너가 생각한 가장 멋진 포켓몬은?" ,"bot" : "제 생각은 거북왕 입니다."},
{"user" : "가장 멋진 포켓몬은?" ,"bot" : "제 생각은 거북왕 입니다."},
{"user" : "네 기준 가장 멋진 포켓몬은?" ,"bot" : "제 생각은 거북왕 입니다."},
{"user" : "네가 생각한 가장 멋진 포켓몬은?" ,"bot" : "제 생각은 거북왕 입니다."},
{"user" : "멋진 포켓몬은?" ,"bot" : "제 생각은 거북왕 입니다."},
{"user" : "가장 아름다운 포켓몬은?" ,"bot" : "제 생각은 밀로틱 입니다."},
{"user" : "너가 생각한 가장 아름다운 포켓몬은?" ,"bot" : "제 생각은 밀로틱 입니다."},
{"user" : "네가 생각한 가장 아름다운 포켓몬은?" ,"bot" : "제 생각은 밀로틱 입니다."},
{"user" : "아름다운 포켓몬은?" ,"bot" : "제 생각은 밀로틱 입니다."},
{"user" : "가장 아름다운 포켓몬은 뭐야?" ,"bot" : "제 생각은 밀로틱 입니다."},
{"user" : "가장 아름다운 포켓몬은 무엇일까?" ,"bot" : "제 생각은 밀로틱 입니다."},
{"user" : "가장 강한 타입은?" ,"bot" : "저는 풀타입 이라고 생각합니다."},
{"user" : "네가 생각한 가장 강한 타입은?" ,"bot" : "저는 풀타입 이라고 생각합니다."},
{"user" : "너가 생각한 가장 강한 타입은?" ,"bot" : "저는 풀타입 이라고 생각합니다."},
{"user" : "네 기준 가장 강한 타입은?" ,"bot" : "저는 풀타입 이라고 생각합니다."},
{"user" : "너 기준 가장 강한 타입은?" ,"bot" : "저는 풀타입 이라고 생각합니다."},
{"user" : "니 기준 가장 강한 타입은?" ,"bot" : "저는 풀타입 이라고 생각합니다."},
{"user" : "너의 기준 가장 강한 타입은?" ,"bot" : "저는 풀타입 이라고 생각합니다."},
{"user" : "가장 강한 타입은 뭘까?" ,"bot" : "저는 풀타입 이라고 생각합니다."},
{"user" : "가장 강한 타입은 뭐야?" ,"bot" : "저는 풀타입 이라고 생각합니다."},
{"user" : "가장 강한 타입은 뭐라고 생각해?" ,"bot" : "저는 풀타입 이라고 생각합니다."},
{"user" : "약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "네가 생각한 약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "너가 생각한 약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "니가 생각한 약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "너의 기준 약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "네 기준 약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "니 기준 약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "너 기준 약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "가장약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "네가 생각한 가장약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "너가 생각한 가장약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "니가 생각한 가장약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "너의 기준 가장약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "네 기준 가장약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "니 기준 가장약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "너 기준 가장약한 타입은 뭐야?" ,"bot" : "저는 비행타입 이라고 생각합니다."},
{"user" : "가장 좋은 몬스터볼은 뭐야?" ,"bot" : "마스터볼입니다."},
{"user" : "네가 생각한 가장 좋은 몬스터볼은 뭐야?" ,"bot" : "마스터볼입니다."},
{"user" : "너가 생각한 가장 좋은 몬스터볼은 뭐야?" ,"bot" : "마스터볼입니다."},
{"user" : "니가 생각한 가장 좋은 몬스터볼은 뭐야?" ,"bot" : "마스터볼입니다."},
{"user" : "가장 좋은 몬스터볼은 뭐지?" ,"bot" : "마스터볼입니다."},
{"user" : "가장 좋은 몬스터볼은 뭘까?" ,"bot" : "마스터볼입니다."},
{"user" : "좋은 몬스터볼은?" ,"bot" : "마스터볼입니다."},
{"user" : "가장 인기있는 포켓몬" ,"bot" : "해당 포켓몬 입니다."},
{"user" : "인기있는 포켓몬" ,"bot" : "해당 포켓몬 입니다."},
{"user" : "가장 못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."},
{"user" : "못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."},
{"user" : "제일 못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."},
{"user" : "네 생각에 가장 못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."},
{"user" : "네 생각에 못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."},
{"user" : "네 생각에 제일 못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."},
{"user" : "너 생각에 가장 못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."},
{"user" : "너 생각에 못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."},
{"user" : "너 생각에 제일 못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."},
{"user" : "니 생각에 가장 못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."},
{"user" : "니 생각에 못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."},
{"user" : "니 생각에 제일 못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."}



]

data= pd.DataFrame(data) #데이터프레임 변환
print(data)

#2.데이터 전처리
inputs=list(data['user']) #질문
outputs=list(data['bot']) #응답

okt=Okt()


def preprocess(text):
    #1.한글과 띄어쓰기(\s)를 제외한 문자제거
    result=re.sub(r'[^가-힣0-9\s]', '', text) #정규표현식 #일반적인 문자열 정규표현식
    #2. 형태소 분석
    result=okt.pos(result) ; print(result)
    #3. 명사와 동사와 형용사 외 제거 #형태소 분석기가 각 형태소들을 명칭하는 단어들 (pos)변수 존재한다.
    result=[word for word, pos in result if pos in ['Noun','Verb','Adjective']]
    #불용어 생략
    #반환
    return " ".join(result).strip() #strop() 아뒤 공백 제거 함수

#전처리 실행
processed_inpus=[ preprocess(질문) for 질문 in inputs]
print(processed_inpus)

#3. 토크나이저

tokenizer=Tokenizer(filters="", lower=False, oov_token="<OOV>")
tokenizer.fit_on_texts(processed_inpus) #전처리된 단어 목록을 단어사전 생성

#패딩
input_sequences=tokenizer.texts_to_sequences(processed_inpus) #벡터화
print(input_sequences)

max_sequence_length=max(len(문장) for 문장 in input_sequences )  #가장 긴 길이의 문장개수
print(max_sequence_length)

input_sequences=pad_sequences(input_sequences, maxlen=max_sequence_length) #패딩화 #가장 길이가 긴 문장 기준으로 0으로 채우기
print(input_sequences)


#종속변수 #데이터프레임 --> 일반 배열 반환
output_sequences=np.array(range(len(outputs)))
print(output_sequences)




#1. 모델
model= Sequential()
    #input_dim : 입력받을 단어의 총 개수
    #output_dim : 밀집 벡터로 변환된 벡터 차원수
model.add(Embedding(input_dim=len(tokenizer.word_index), output_dim=50, input_length=max_sequence_length))
model.add(Bidirectional(LSTM(256, recurrent_dropout=0.2, dropout=0.2))) #,256 128,64,32
model.add(Dense(32, activation="relu"))
model.add(Dense(16, activation="relu"))
model.add(Dense(len(outputs),activation='softmax')) #종속변수 값 개수는 응답 개수

checkpoint_path = "best_performed_model.ckpt"
checkpoint = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True, save_best_only=True, verbose = 1)

early_stop = tf.keras.callbacks.EarlyStopping(monitor = "loss", patience = 2)


#2. 컴파일
model.compile(optimizer=tf.optimizers.Adam(learning_rate=0.001),loss='sparse_categorical_crossentropy',metrics=['accuracy'])

NUM_EPOCHS = 20

#예측하기
def response(message):
    text=preprocess(message)
    print(text)
    #2. 예측할 값도 토큰과 패딩 #학습된 모델과 데이터 동일
    text=tokenizer.texts_to_sequences([text])
    text=pad_sequences(text,maxlen=max_sequence_length)
    # 예측하기
    result=model.predict(text)
    #결과 #가장 높은 확률의 인덱스 찾기
    max_index=np.argmax(result)
    msg = outputs[max_index]

    if max_index in response_functions :
        msg += f"\n{response_functions[max_index](message)}" # 함수 호출 시에는 () 붙여야 함

    return msg

for epoch in range(NUM_EPOCHS):
    #3. 학습
    model.fit(input_sequences, output_sequences, callbacks=[early_stop, checkpoint] ,epochs=10)


    for idx in data["user"]:
        question_inputs = idx
        results = response(question_inputs)


# print(response(('안녕하세요'))) #질문이 '안녕하세요', 학습된 질문 목록중에 가장 높은 예측비율이 높은 질문의 응답을 출력한다.

# 서비스 제공한다. #플라스크

import time

#챗봇의 답변이 타자치는 것처럼 출력 함수
def print_with_delay(text, delay=0.1):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # 마지막에 줄 바꿈

while True:
    text = input('사용자: ')  # 챗봇에게 전달할 내용 입력받기
    result = response(text)  # 입력받은 내용을 함수에 넣어 응답 예측을 한다

    # 챗봇의 응답을 한 글자씩 출력
    print_with_delay(f'챗봇: {result}')  # 챗봇의 응답 출력










