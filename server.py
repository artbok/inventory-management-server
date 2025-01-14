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
    if not isUser(data["username"], data["password"]):
        return jsonify({'status': 'invalidLogin'})
    user: User = getUser(data["username"])
    return jsonify({'status': 'ok', 'rightsLevel': user.rightsLevel})


@app.route('/newItem', methods=['POST'])
def newItem():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    createItem(data["name"], data["description"], int(data["amount"]))
    return jsonify({'status': status})


@app.route('/getItems', method=['POST'])
def getUsersItems():
    data = request.json
    if data["owner"]:
        totalPages = ceil(Items.select().where(Items.owner == data["owner"]).count() / 10)
        items = getItemsOnPage(int(data["page"]), data['username'])
    else:
        totalPages = ceil(Items.select().count() / 10)
        items = getItemsOnPage(int(data["page"]))
    if not isUser(data["username"], data["password"]):
        return jsonify({'status': "authError"})
    return jsonify({'status': 'ok', "totalPages": totalPages, 'data': items})
app.run()