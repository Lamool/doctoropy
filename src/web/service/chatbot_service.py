#2_마니챗봇
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import  Embedding , LSTM, Dense, Bidirectional, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import  pad_sequences

from konlpy.tag import  Okt
import  re


#데이터 수집 #
data = [
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
    {"user" : "나1등했어", "bot" : "대단하시네요."}

]

data= pd.DataFrame(data) #데이터프레임 변환
print(data)

#2.데이터 전처리
inputs=list(data['user']) #질문
outputs=list(data['bot']) #응답

okt=Okt()


def preprocess(text):
    #1.한글과 띄어쓰기(\s)를 제외한 문자제거
    result=re.sub(r'[^가-힣\s]', '', text) #정규표현식 #일반적인 문자열 정규표현식
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

early_stop = tf.keras.callbacks.EarlyStopping(monitor = "val_loss", patience = 2)


#2. 컴파일
model.compile(optimizer=tf.optimizers.Adam(learning_rate=0.001),loss='sparse_categorical_crossentropy',metrics=['accuracy'])

NUM_EPOCHS = 1

#예측하기
def response(text):
    text=preprocess(text)
    print(text)
    #2. 예측할 값도 토큰과 패딩 #학습된 모델과 데이터 동일
    text=tokenizer.texts_to_sequences([text])
    text=pad_sequences(text,maxlen=max_sequence_length)
    # 예측하기
    result=model.predict(text)
    #결과 #가장 높은 확률의 인덱스 찾기
    max_index=np.argmax(result)
    print(outputs[max_index])
    return outputs[max_index]

for epoch in range(NUM_EPOCHS):
    #3. 학습
    model.fit(input_sequences, output_sequences, callbacks=[early_stop, checkpoint] ,epochs=10)


    for idx in data["user"]:
        question_inputs = idx
        results = response(question_inputs)

        print(f"Q : {question_inputs} ")
        print(f"A : {results} ")


# print(response(('안녕하세요'))) #질문이 '안녕하세요', 학습된 질문 목록중에 가장 높은 예측비율이 높은 질문의 응답을 출력한다.

#서비스 제공한다. #플라스크
# while True:
#     text=input('사용자:') #챗봇에게 전달할 내용 입력받기
#     result=response(text) #입력받은 내용을 함수에 넣어 응답 예측을 한다
#     print(f'챗봇:{result}') #예측한 응답 출력한다.







