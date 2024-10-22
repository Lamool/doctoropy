from src.web.app import *
from src.web.service.vote_city_service import *

@app.route("/vote/record_first", methods = ["POST"])
def first_record():
    contentType = request.content_type
    args = None

    if contentType == "application/x-www-form-urlencoded":
        args : dict = request.form

    elif contentType == "application/json":
        args : dict = request.json

    else :
        print("not supported content-type")


    data = list(args.get("list"))
    print(data)
    vote_record_list_first(data)

    return jsonify({"status" : "success", "received" : []})


@app.route("/vote/record_second", methods = ["POST"])
def second_record():
    contentType = request.content_type
    args = None

    if contentType == "application/x-www-form-urlencoded":
        args : dict = request.form

    elif contentType == "application/json":
        args : dict = request.json

    else :
        print("not supported content-type")


    data = list(args.get("list"))
    print(data)
    vote_record_list_second(data)

    return jsonify({"status" : "success", "received" : []})


@app.route("/vote/record_third", methods = ["POST"])
def third_record():
    contentType = request.content_type
    args = None

    if contentType == "application/x-www-form-urlencoded":
        args : dict = request.form

    elif contentType == "application/json":
        args : dict = request.json

    else :
        print("not supported content-type")


    data = list(args.get("list"))
    print(data)
    vote_record_list_third(data)

    return jsonify({"status" : "success", "received" : []})