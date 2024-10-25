from src.web.service.chatbot_service import *
from src.web.app import *

@app.route("/chatbot/bot", methods=["GET"])
def chat_bot() :
    text = request.args.get("text")
    print(text)
    result = response(text)
    print(result)
    return result