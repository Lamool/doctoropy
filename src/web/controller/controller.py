from src.web.app import app

@app.route("/", methods = ['GET'])
def index() :
    return [1,2,3]
