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
def newUser():
    data = request.json
    if getUser(data["username"]):
        return jsonify({'status': 'userAlreadyExists'})
    createUser(data["username"], data["password"], data["rightsLevel"])
    return jsonify({'status': 'ok'})


@app.route('/authUser', methods=['POST'])
def authUser():
    data = request.json 
    if not isUser(data["username"], data["password"]):
        return jsonify({'status': 'invalidLogin'})
    user: User = getUser(data["username"])
    return jsonify({'status': 'ok', 'rightsLevel': user.rightsLevel})


@app.route('/newItem', methods=['POST'])
def newItem():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    createItem(data["name"], data["description"], int(data["quantity"]))
    return jsonify({'status': status})


@app.route('/getItems', methods=['POST'])
def items():
    data = request.json
    if isUser(data["username"], data["password"]): 
        totalPages = ceil(Items.select().count() / 10)
        items = getStorageItemsOnPage(int(data["page"]))
        return jsonify({'status': 'ok', "totalPages": totalPages, 'data': items, 'users': getUsers()})
    return jsonify({'status': "authError"})


@app.route('/getUsersItems', methods=['POST'])
def usersItems():
    data = request.json
    if isUser(data["username"], data["password"]): 
        totalPages = ceil(ItemOwners.select().where(ItemOwners.owner == data["owner"]).count() / 10)
        items = getUsersItems(data["owner"], int(data["page"]))
        return jsonify({'status': 'ok', "totalPages": totalPages, 'data': items})
    return jsonify({'status': "authError"})


@app.route('/giveItem', methods=['POST'])
def giveItem():
    data = request.json
    if isUser(data["username"], data["password"]): 
        addOwnerForItem(data["user"], data["itemName"], data["description"], data["quantity"])
        return jsonify({'status': "ok"})
    return jsonify({'status': "authError"})


@app.route('/newItemRequest', methods=['POST'])
def newItemRequest():
    data = request.json
    if isUser(data["username"], data["password"]):
        createItemRequest(data["isCustom"], data["itemName"], data["quantity"], data["owner"])
        return jsonify({'status': 'ok'})
    return jsonify({'status': "authError"})  


@app.route('/getItemsRequests', methods=['POST'])
def itemsRequests():
    data = request.json
    if isUser(data['username'], data['password']):
        items = getItemsRequests(data['owner'])
        return jsonify({'status': 'ok', 'data': items})
    return jsonify({'status': "authError"}) 


@app.route('/newReplacementRequest', methods=['POST'])
def newReplacementRequest():
    data = request.json
    if isUser(data['username'], data['password']): 
        createReplacementRequest(data["owner"], data["itemName"], data["quantity"])
        return jsonify({'status': 'ok'})
    return jsonify({'status': "authError"})


@app.route('/getReplacementsRequests', methods=['POST'])
def replacementsRequests():
    data = request.json
    if isUser(data['username'], data['password']):
        items = getReplacementsRequests(data['owner'])
        return jsonify({'status': 'ok', 'data': items})
    return jsonify({'status': "authError"})


app.run()