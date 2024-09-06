from src.web.app import app

# 김민석 112233


@app.route("/", methods = ['GET'])
def index() :
    return [1,2,3]
