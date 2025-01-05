from flask import Flask, request, jsonify
from dataRepository import *
from math import ceil


app = Flask("server")

@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route('/newUser', methods=['POST'])
def registerNewUser():
    data = request.json
    if getUser(data["username"]) != None:
        return jsonify({'status': 'userAlreadyExists'})
    User.create(username = data["username"], password = data["password"], rightsLevel = int(data["rightsLevel"])).save()
    return jsonify({'status': 'ok'})


@app.route('/authUser', methods=['POST'])
def userAuth():
    data = request.json 
    user: User = getUser(data["username"])
    if not user or user.password != data["password"]:
        return jsonify({'status': 'invalidLogin'})
    return jsonify({'status': 'ok'})


@app.route('/newItem', methods=['POST'])
def newItem():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    createItem(data["name"], data["description"], int(data["amount"]))
    return jsonify({'status': status})


@app.route('/getItems', methods=['POST'])
def getItems():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status != 'ok':
        return jsonify({'status': status})
    return jsonify({'status': status, 'totalPages': ceil(Items.select().count() / 10), 'data': getItemsOnPage(int(data["page"]))})
app.run()