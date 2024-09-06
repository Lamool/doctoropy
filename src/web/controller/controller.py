from src.web.app import app

@app.route("/", methods = ['GET'])
def index() :
    return 'main'
