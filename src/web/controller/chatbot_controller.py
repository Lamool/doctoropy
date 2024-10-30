# from src.web.service.chatbot_service import *
from src.web.service.chatbot_service_seq2seq import run_chatbot
from src.web.app import app ,request

# @app.route("/chatbot/bot", methods=["GET"])
# def chat_bot() :
#     text = request.args.get("text")
#     print(text)
#     result = response(text)
#     print(result)
#     return result

@app.route("/chatbot/seq2seq", methods = ["GET"])
def chat_bot_seq2seq():
    text = request.args.get("text")
    result = run_chatbot(text)
    print(result)

    return result