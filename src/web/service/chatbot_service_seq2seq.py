import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import  Embedding, LSTM, Dense, Bidirectional, Dropout, Attention
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import  pad_sequences

import warnings

from konlpy.tag import  Okt
import  re

from src.web.service.info_service import *
from src.web.service.service import *



def poke_info_search(*kwargs):
    poke_data = pd.read_csv("datapokemon.csv", encoding="utf-8", index_col=0)
    kr_name = poke_data["한글이름"]
    result = ""

    # kwargs[0]을 문자열로 강제 변환해 비교에 사용합니다.
    search_name = str(kwargs[0]).split(" ")  # 첫 번째 인자를 문자열로 변환합니다.
    print(search_name)
    for search in search_name:
        for i, name in enumerate(kr_name):
            if name == search:
                result += f"이름은 {poke_data['한글이름'].iloc[i]}, {poke_data['한글정보'].iloc[i]}입니다. {poke_data['타입'].iloc[i]} 타입입니다.\n"
                result += f"체력 : {poke_data['체력'].iloc[i]}, 공격 : {poke_data['공격'].iloc[i]}, 방어 : {poke_data['방어'].iloc[i]}\n"
                result += f"특수공격 : {poke_data['특수공격'].iloc[i]}, 특수방어 : {poke_data['특수방어'].iloc[i]}, 스피드 : {poke_data['스피드'].iloc[i]}\n"
                result += f"{poke_data['한글정보2'].iloc[i]}\n"
                result += f"{poke_data['한글정보3'].iloc[i]}"

    return result

def poke_each_skills(*kwargs):
    result = ""

    skill_data = pd.read_csv("new_poke_each_skill_data.csv", encoding="utf-8", index_col=0)
    kr_name = skill_data["포켓몬"]

    search_name = str(kwargs[0]).split(" ")  # 첫 번째 인자를 문자열로 변환합니다.
    print(search_name)

    for search in search_name:
        for i, name in enumerate(kr_name):
            if name == search:
                result += f"{skill_data['스킬이름'].iloc[i]} : {skill_data['타입'].iloc[i]} 타입, 위력 {skill_data['위력'].iloc[i]}의 기술입니다.\n"

    return result

def link_collection(*kwargs):
    result = ""

    search_name = str(kwargs[0]).split(" ")

    for search in search_name:
        if search == "게시판":
            result += "localhost:8080/board/bprint"

        elif search == "종족값":
            result += "localhost:8080/base/stats/print"

        elif search == "채팅":
            result += "localhost:8080/chat"

        elif search == "쇼핑":
            result += "localhost:8080/product"

        elif search == "투표":
            result += "localhost:8080/rank/enter"

        elif search == "포인트":
            result += "localhost:8080/point/charge"

        elif search == "장바구니":
            result += "localhost:8080/cart"

        elif search == "승률":
            result += "localhost:8080/rate"

    return result

def poke_click(*kwargs):
    result = ""

    click_data = pd.read_csv("merged_data.csv", encoding="utf-8", index_col=0)
    kr_name = click_data["한글이름"]

    search_name = str(kwargs[0]).split(" ")
    print(search_name)

    for search in search_name :
        for i , name in enumerate(kr_name) :
            if name == search:
                result += f"{kr_name.iloc[i]}의 클릭 수는 {click_data['click'].iloc[i]} "

def poke_win(*kwargs):
    result = ""

    win_data = pd.read_csv("merged_data.csv", encoding="utf-8", index_col=0)
    kr_name = win_data["한글이름"]

    search_name = str(kwargs[0]).split(" ")
    print(search_name)

    for search in search_name:
        for i, name in enumerate(kr_name):
            if name == search:
                result += f"{kr_name.iloc[i]}의 클릭 수는 {win_data['win'].iloc[i]} "

response_functions = {
    0 : poke_info_search,
    1 : poke_each_skills,
    2 : poke_click,
    3 : poke_win,
    4 : link_collection
}

#데이터 수집 #
data = [
    {"user" : "피카츄 정보 알려줘", "bot" : "포켓몬 정보를 알려드리겠습니다."},
    {"user" : "피카츄 기술 알려줘", "bot" : "포켓몬이 가질 수 있는 기술을 알려드리겠습니다."},
    {"user" : "가장 강한 포켓몬은 뭔가요?", "bot" : "지우입니다."},
    {"user" : "챗봇 이름은 뭐야?", "bot" :"오박사입니다."},
    {"user" : "넌 뭘 할수있어?", "bot" :"불가능한거빼고모두가능합니다."},
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
    {"user" : "이 사이트는 뭘 할 수 있어?","bot" : "포켓몬에 관한 것 들을 할 수 있습니다."},
    {"user" : "이 사이트 에서 뭘 할 수 있어?","bot" : "포켓몬에 관한 것 들을 할 수 있습니다."},
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
    {"user" : "니 생각에 제일 못생긴 포켓몬" ,"bot" : "저는 질뻐기 라고 생각합니다."},
    {"user" : "이상해씨 클릭 횟수" ,"bot" : "이상해씨 클릭 횟수는 15회 입니다."},
    {"user" : "이상해씨 클릭 횟수 알려줘" ,"bot" : "이상해씨 클릭 횟수는 15회 입니다."},
    {"user" : "이상해씨 클릭 횟수 출력해줘" ,"bot" : "이상해씨 클릭 횟수는 15회 입니다."},
    {"user" : "이상해씨 클릭 수" ,"bot" : "이상해씨 클릭 횟수는 15회 입니다."},
    {"user" : "이상해씨 클릭 수 알려줘", "bot": "이상해씨 클릭 횟수는 15회 입니다."},
    {"user" : "팬텀 우승 횟수" ,"bot" : "팬텀 우승 횟수는 10회 입니다."},
    {"user" : "꼬부기 우승 횟수 알려줘", "bot": "꼬부기 우승 횟수는 10회 입니다."},
    {"user" : "야도란 우승 횟수 가르쳐줘", "bot": "야도란 우승 횟수는 10회 입니다."},
    {"user" : "또가스 우승 횟수 출력해줘", "bot": "또가스 우승 횟수는 10회 입니다."},
    {"user" : "리자몽 우승 수", "bot": "리자몽 우승 횟수는 10회 입니다."},
    {"user" : "거북왕 우승 수 알려줘", "bot": "거북왕 우승 횟수는 10회 입니다."},
    {"user" : "팬텀 우승 수 가르쳐줘", "bot": "팬텀 우승 횟수는 10회 입니다."},
    {"user": "피카츄 클릭 횟수", "bot": "피카츄 클릭 횟수는 15회 입니다."},
    {"user": "이상해꽃 클릭 횟수 알려줘", "bot": "이상해꽃 클릭 횟수는 15회 입니다."},
    {"user": "아보크 클릭 횟수 출력해줘", "bot": "아보크 클릭 횟수는 15회 입니다."},
    {"user": "냐옹 클릭 수", "bot": "냐옹 클릭 횟수는 15회 입니다."},
    {"user": "파이리 클릭 수 알려줘", "bot": "파이리 클릭 횟수는 15회 입니다."},
    {"user": "가랴도스 우승 횟수", "bot": "가랴도스 우승 횟수는 10회 입니다."},
    {"user": "고라파덕 우승 횟수 알려줘", "bot": "고라파덕 우승 횟수는 10회 입니다."},
    {"user": "펄기아 우승 횟수 가르쳐줘", "bot": "펄기아 우승 횟수는 10회 입니다."},
    {"user": "디아루가 우승 횟수 출력해줘", "bot": "디아루가 우승 횟수는 10회 입니다."},
    {"user": "라이츄 우승 수", "bot": "라이츄 우승 횟수는 10회 입니다."},
    {"user": "피죤투 우승 수 알려줘", "bot": "피죤투 우승 횟수는 10회 입니다."},
    {"user": "야돈 우승 수 가르쳐줘", "bot": "야돈 우승 횟수는 10회 입니다."},
    {"user": "피츄 클릭 횟수", "bot": "피츄 클릭 횟수는 15회 입니다."},
    {"user": "이브이 클릭 횟수 알려줘", "bot": "이브이 클릭 횟수는 15회 입니다."},
    {"user": "에브이 클릭 횟수 출력해줘", "bot": "에브이 클릭 횟수는 15회 입니다."},
    {"user": "나옹 클릭 수", "bot": "나옹 클릭 횟수는 15회 입니다."},
    {"user": "골덕 클릭 수 알려줘", "bot": "골덕 클릭 횟수는 15회 입니다."},
    {"user": "고오스 우승 횟수", "bot": "고오스 우승 횟수는 10회 입니다."},
    {"user": "마자용 우승 횟수 알려줘", "bot": "마자용 우승 횟수는 10회 입니다."},
    {"user": "아르세우스 우승 횟수 가르쳐줘", "bot": "아르세우스 우승 횟수는 10회 입니다."},
    {"user": "기라티나 우승 횟수 출력해줘", "bot": "기라티나 우승 횟수는 10회 입니다."},
    {"user": "다크라이 우승 수", "bot": "다크라이 우승 횟수는 10회 입니다."},
    {"user": "라이코 우승 수 알려줘", "bot": "라이코 우승 횟수는 10회 입니다."},
    {"user": "칠색조 우승 수 가르쳐줘", "bot": "칠색조 우승 횟수는 10회 입니다."}



]

data= pd.DataFrame(data) #데이터프레임 변환

texts = list(data["user"])   # 질문 리스트
pairs = list(data["bot"])  # 답변 리스트


def clean_sentence(sentence):
    # 한글 숫자 제외한 모든 문자 제거
    sentence = re.sub(r"[^가-힣ㄱ-ㅎㅏ-ㅣ0-9\s]", r'', str(sentence))

    return sentence

okt = Okt()

def process_morph(sentence):

    return " ".join(okt.morphs(sentence))   # 형태소 분석 결과를 하나의 문자열로 합치기

def clean_and_morph(sentence, is_question = True):  # 매개변수명 = 초기값, 매개변수명에 초기값 넣기
    # 한글 문장 전처리
    sentence = clean_sentence(sentence)

    # 형태소 변환
    sentence = process_morph(sentence)

    # Question 인 경우, Answer 인 경우를 분기하여 처리
    if is_question:

        return sentence

    else :

        # Start 토큰은 decoder input 에, End 토큰은 decoder output 에 추가
        return (f"<START> {sentence}", f"{sentence} <END>")

def preprocess(texts, pairs):
    # 인코더에 입력할 질문 전체 리스트
    questions = []
    # 디코더에 입력할 데이터셋(답변의 시작), <START> 토큰을 문장 처음에 추가
    answer_in = []
    # 디코더에 입력할 데이터셋(답변의 끝), <END> 토큰을 문장 마지막에 추가
    answer_out = []

    # 질의에 대한 전처리
    for text in texts:
        # 전처리와 morphs 진행
        question = clean_and_morph(text, is_question=True)
        questions.append(question)

    # 답변에 대한 전처리
    for pair in pairs:
        in_, out_ = clean_and_morph(pair, is_question=False)
        answer_in.append(in_)
        answer_out.append(out_)

    return questions, answer_in, answer_out


questions, answer_in, answer_out = preprocess(texts, pairs)

all_sentences = questions + answer_in + answer_out

tokenizer = Tokenizer(filters="", lower=False, oov_token="<OOV>")
tokenizer.fit_on_texts(all_sentences)

# for word, idx in tokenizer.word_index.items():
#     print(f"{word}\t -> \t{idx}")
#     if idx > 10 :
#         break

question_sequence = tokenizer.texts_to_sequences(questions)
answer_in_sequence = tokenizer.texts_to_sequences(answer_in)
answer_out_sequence = tokenizer.texts_to_sequences(answer_out)


# 패딩 (문장 길이 맞춰서 학습 데이터들의 차원을 일치화함으로써 모델 성능 향상)
MAX_LENGTH = 30 # 문장 내 최대 길이를 임의로 30, "post" -> 빈 칸을 뒤에 0으로 채우기
question_padded = pad_sequences(question_sequence, maxlen=MAX_LENGTH, truncating= "post", padding="post")
answer_in_padded = pad_sequences(answer_in_sequence, maxlen=MAX_LENGTH, truncating= "post", padding="post")
answer_out_padded = pad_sequences(answer_out_sequence, maxlen=MAX_LENGTH, truncating= "post", padding="post")


class Encoder(tf.keras.Model):
    # units : LSTM 에서 사용할 유닛 / 노드 / 뉴런 수
    # "안녕하세요, 오늘 날씨 어때요?" 라는 문장이라고 가정
    # vocab_size : 임베딩 레이어의 입력으로 들어가는 크기
    # "안녕하세요", "오늘", "날씨", "어때요" -> 4
    # embedding_dim : 임베딩 레이어의 각 단어 크기를 나타내는 벡터 차원
    # 밀집 행렬을 처리할 때 한 단어를 표현할 차원의 수, "안녕하세요"를 몇 차원으로 구성할 지 결정
    # timp_steps : 임베딩 레이어의 입력으로 sequence 의 길이
    # 한번에 몇 개의 단어를 모델이 학습하고 기억할 지 단위를 정함 -> 단위 2라면 "안녕하세요", "오늘"
    def __init__(self, units, vocab_size, embedding_dim, time_steps):
        # 상속받은 super 클래스의 생성자를 호출
        super(Encoder, self).__init__()

        # 임베딩 레이어
        self.embedding = Embedding(vocab_size, embedding_dim, input_length=time_steps)

        # 드롭아웃 레이어
        self.dropout = Dropout(0.2)

        # LSTM 레이어
        self.lstm = LSTM(units, return_state=True, return_sequences=True)


    # 실행 함수, call
    def call(self, inputs):
        x = self.embedding(inputs)  # 임베딩 레이어에 따른 밀집행렬 생성
        x = self.dropout(x)  # 드롭 아웃 레이어에 따른 무작위 노드 제외
        # x : LSTM 레이어에서 특정 단어들을 통해 도출해낸 특징(정보 / 패턴)
        # 문장 : "오늘 무엇을 먹을까?" -> 현재 문장의 분석 결과를 알려주는 출력값
        # hidden_state : LSTM 레이어가 현재 시점에서 기록한 특징(정보 / 패턴) -> 최종 은닉 상태
        # L(Long) S(Short) T(Term) M(Memory) : 앞 전 문장을 잊지 않고 지속하는 문장을 기록하는 메모리
        # cell_state : LSTM 레이어가 전체 단어들에서 기록한 중요한 특징(정보 / 패턴) -> 셀 상태
        # 앞 전 전체 분석된 문장들 중에서 중요한 단어들을 기억하는 메모리
        # 특징 / 패턴 분석
        # CNN : 이미지 분석, 곡선, 색감, 사이즈, 비율, 질감(텍스쳐) 등등, 컴퓨터는 0 ~ 255 사이의 숫자들로 RGB를 판단
        # RNN : 텍스트 분석, 빈도, 삼정, 형태소(동사, 형용사 등등), 단어의 의미, 컴퓨터는 텍스트 대신 벡터로 판단
        x, hidden_state, cell_state = self.lstm(x)  # LSTM 레이어에 따른 학습 실행

        # Dense 레이어가 없는 이유는 현재 클래스(인코더)의 목적이 입력 과정을 하기 위해서 -> 디코더에 전달
        return x, [hidden_state, cell_state]  #


# 디코더, 텐서플로의 Model 클래스로부터 상속받아서 디코더 클래스 정의
class Decoder(tf.keras.Model):
    def __init__(self, units, vocab_size, embedding_dim, time_steps):
        super(Decoder, self).__init__()
        self.embedding = Embedding(vocab_size, embedding_dim, input_length=time_steps)

        self.dropout = Dropout(0.2)
        self.lstm = LSTM(units, return_state=True, return_sequences=True)

        self.attention = Attention()

        self.dense = Dense(vocab_size, activation="softmax")

    def call(self, inputs, initial_state):
        encoder_inputs, decoder_inputs = inputs

        x = self.embedding(decoder_inputs)
        x = self.dropout(x)
        x, hidden_state, cell_state = self.lstm(x, initial_state=initial_state)


            # (Attention) key_value, attention_matrix 추가
            # (Attention) 이전 hidden_state의 값을 concat 으로 만들어 vector 를 생성
        key_value = tf.concat([initial_state[0][:, tf.newaxis, :], x[:, :-1, :]], axis = 1)

            # (Attention) 이전 hidden_state 의 값을 concat 으로 만든 vector 와 encoder에서 나온 출력값들로 attention 을 구함
        attention_matrix = self.attention([key_value, encoder_inputs])

            # (Attention) 위에서 구한 attention_matrix 와 decoder 의 출력값을 합침(concat)
        x = tf.concat([x, attention_matrix], axis = -1)
        x = self.dense(x)
        return x, hidden_state, cell_state


# 모델 결합
class Seq2Seq(tf.keras.Model):
    def __init__(self, units, vocab_size, embedding_dim, time_steps, start_token, end_token):
        super(Seq2Seq, self).__init__()
        self.start_token = start_token
        self.end_token = end_token
        self.time_steps = time_steps

        self.encoder = Encoder(units, vocab_size, embedding_dim, time_steps)
        self.decoder = Decoder(units, vocab_size, embedding_dim, time_steps)

    def call(self, inputs, training=True):
        if training:
            encoder_inputs, decoder_inputs = inputs
            encoder_outputs, context_vector = self.encoder(encoder_inputs)
            decoder_outputs, _, _ = self.decoder((encoder_outputs, decoder_inputs), initial_state=context_vector)

            return decoder_outputs
        else:

            x = inputs

            # (Attention) encoder 출력 값 수정
            encoder_outputs, context_vector = self.encoder(x)

            target_seq = tf.constant([[self.start_token]], dtype=tf.float32)
            results = tf.TensorArray(tf.int32, self.time_steps)

            for i in tf.range(self.time_steps):
                decoder_output, decoder_hidden, decoder_cell = self.decoder((encoder_outputs, target_seq), initial_state=context_vector)

                decoder_output = tf.cast(tf.argmax(decoder_output, axis=-1), dtype=tf.int32)

                decoder_output = tf.reshape(decoder_output, shape=(1, 1))

                results = results.write(i, decoder_output)

                if decoder_output == self.end_token:
                    break

                target_seq = decoder_output
                context_vector = [decoder_hidden, decoder_cell]

            return tf.reshape(results.stack(), shape=(1, self.time_steps))


VOCAB_SIZE = len(tokenizer.word_index) + 1


def convert_to_one_hot(padded):
    # 원 핫 인코딩 초기화
    one_hot_vector = np.zeros((len(answer_out_padded), MAX_LENGTH, VOCAB_SIZE))

    # 디코더 목표를 원 핫 인코딩으로 변환
    # 학습 시 입력은 인덱스 이지만 출력은 원 핫 인코딩 형식임
    for i, sequence in enumerate(answer_out_padded):
        for j, index in enumerate(sequence):
            one_hot_vector[i, j, index] = 1

    return one_hot_vector


answer_in_one_hot = convert_to_one_hot(answer_in_padded)
answer_out_one_hot = convert_to_one_hot(answer_out_padded)


# print(answer_in_one_hot[0].shape)   # (30, 2303)
# print(answer_out_one_hot[0].shape)  # (30, 2303)

def convert_index_to_text(indexs, end_token):
    sentence = ""

    # 모든 문장에 대해서 반복
    for index in indexs:
        if index == end_token:
            # 끝 단어이므로 예측 준비
            break

        # 사전에 존재하는 단어의 경우 단어 추가
        if index > 0 and tokenizer.index_word[index] is not None:
            # print(index)
            sentence += tokenizer.index_word[index]

        else:
            # 사전에 없는 인덱스면 빈 문자열 추가
            sentence += " "

        # 빈 칸 추가
        sentence += " "

    return sentence


# 훈련 시 필요한 파라미터 값 정의
BUFFER_SIZE = 1000
BATCH_SIZE = 16
EMBEDDING_DIM = 100
TIME_STEPS = MAX_LENGTH
START_TOKEN = tokenizer.word_index["<START>"]
END_TOKEN = tokenizer.word_index["<END>"]

UNITS = 128

VOCAB_SIZE = len(tokenizer.word_index) + 1
DATA_LENGTH = len(questions)
SAMPLE_SIZE = 3
NUM_EPOCHS = 20

# 모델 저장할 수 있도록 체크포인트 생성
checkpoint_path = "model/seq2seq-chatbot-checkpoint.ckpt"
checkpoint = ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, monitor="loss", verbose=1)

# seq2seq
seq2seq = Seq2Seq(UNITS, VOCAB_SIZE, EMBEDDING_DIM, TIME_STEPS, START_TOKEN, END_TOKEN)
seq2seq.compile(optimizer=tf.optimizers.Adam(learning_rate=0.001), loss="categorical_crossentropy", metrics=["acc"])


def make_prediction(model, question_inputs):
    results = model(inputs=question_inputs, training=False)
    # 변환된 인덱스를 문장으로 변환
    results = np.asarray(results).reshape(-1)

    return results


for epoch in range(NUM_EPOCHS):
    print(f"processing epoch: {epoch * 10 + 1}...")
    seq2seq.fit([question_padded, answer_in_padded], answer_out_one_hot, epochs=10, batch_size=BATCH_SIZE,
                callbacks=[checkpoint])

    # 랜덤한 샘플 번호 추출
    samples = np.random.randint(DATA_LENGTH, size=SAMPLE_SIZE)

    # 예측 성능 테스트
    for idx in samples:
        question_inputs = question_padded[idx]

        # 문장 예측
        results = make_prediction(seq2seq, np.expand_dims(question_inputs, 0))

        # 변환된 인덱스를 문장으로 변환
        results = convert_index_to_text(results, END_TOKEN)

        # print(f"Q : {questions[idx]}")
        # print(f"A : {results}\n")
        # print()

def make_question(sentence):
    sentence = clean_and_morph(sentence)
    question_sequence = tokenizer.texts_to_sequences([sentence])
    question_padded = pad_sequences(question_sequence, maxlen=MAX_LENGTH, truncating="post", padding="post")

    return question_padded

def run_chatbot(question):
    #응답
    question_inputs = make_question(question)
    results = make_prediction(seq2seq, question_inputs)
    results = convert_index_to_text(results, END_TOKEN)

    # 질문에 따른 인덱스 ( 유사 ) 인덱스 찾기
    question_preprocess = clean_and_morph(question, True)
    print(question_preprocess)

    if "정보" in question_preprocess :
        results += f"\n{response_functions[0](question_preprocess)}"

    if "기술" in question_preprocess :
        results += f"\n{response_functions[1](question_preprocess)}"

    if "클릭" in question_preprocess :
        results += f"\n{response_functions[2](question_preprocess)}"

    if "우승" in question_preprocess :
        results += f"\n{response_functions[3](question_preprocess)}"

    if "싶어" or "링크" or "싶다" in question_preprocess:
        results += f"\n{response_functions[4](question_preprocess)}"
    return results

while True:
    user_input = input("<<말을 걸어 보세요!\n")
    if user_input == "q":
        break
    print(f">> 챗봇 응답 : {run_chatbot(user_input)}")
