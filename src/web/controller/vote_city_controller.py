from src.web.app import *
from src.web.service.vote_city_service import *
from src.web.service.vote_city_model_service import *

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

@app.route("/vote/first_pred", methods = ["GET"])
def first_pred():
    gen = request.args["gen"]
    age = request.args["age"]
    print(gen)
    print(age)

    result = first_city_pred(gen, age)
    print(result)

    return result


@app.route("/vote/second_pred", methods=["GET"])
def second_pred():
    gen = request.args["gen"]
    age = request.args["age"]
    print(gen)
    print(age)

    result = second_city_pred(gen, age)
    print(result)

    return result


@app.route("/vote/third_pred", methods=["GET"])
def third_pred():
    gen = request.args["gen"]
    age = request.args["age"]
    print(gen)
    print(age)

    result = third_city_pred(gen, age)
    print(result)

    return result

