from flask import Flask, request, jsonify
from src.web.service.weather_service import *
from src.web.app import *
@app.route('/updateTime',methods=['get'])
def update_time():
   year = int(request.args.get('year'))
   month = int(request.args.get('month'))
   date = int(request.args.get('date'))
   hours = int(request.args.get('hours'))
   minutes = int(request.args.get('minutes'))
   print(year,month,date,hours,minutes)
   result= predict_weather(year,month,date,hours,minutes)

   return result