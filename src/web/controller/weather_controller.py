
# from flask import Flask, request, jsonify
# from src.web.service.weather_service import *
from src.web.app import *
# CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})  # 모든 출처 허용
@app.route('/updateTime',methods=['get'])
def update_time():
   # java_url = 'http://localhost:8080/weather/'
   # response = requests.get(java_url)  # JAVA controller api 호출
   # print(response)

   year=request.args.get('year'),
   month=request.args.get('month'),
   day=request.args.get('day'),
   hours=request.args.get('hours'),
   minutes=request.args.get('minutes')
   print(f'현재 시간: {year}-{month}-{day} {hours}:{minutes}')

   return jsonify({'status': 'success', 'message': '시간이 업데이트되었습니다.'})
