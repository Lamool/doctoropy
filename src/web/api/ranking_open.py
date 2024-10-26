from src.web.app import *

@app.route('/rank/allcrolling',methods=['POST'])
def all_crolling():
    contentType = request.content_type
    args = None

    if contentType == "application/x-www-form-urlencoded":
        args: dict = request.form

    elif contentType == "application/json":
        args: dict = request.json

    else:
        print("not supported content-type")

    data = list(args.get("data"))
    print(data)
    return data