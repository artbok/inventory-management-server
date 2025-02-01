from flask import Blueprint, request, jsonify
from models.user import * 
from models.item import *
from models.item_owner import *
from math import ceil


items_bp = Blueprint("items", __name__)


@items_bp.route('/newItem', methods=['POST'])
def newItem():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status == 'ok':
        createItem(data["name"], data["description"], data["quantity"])
    return jsonify({'status': status})


@items_bp.route('/editItem', methods=['POST'])
def edit_item():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status == 'ok':
        editItem(data["itemId"], data["newName"], data["newQuantity"], data["newDescription"])
    return jsonify({'status': status})


@items_bp.route('/changeItemStatus', methods=['POST'])
def changeItemStatus():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status == 'ok':
        changeStatus(data["itemId"], data["quantity"], data["status"])
    return jsonify({'status': status})


@items_bp.route('/getItems', methods=['POST'])
def items():
    data = request.json
    if isUser(data["username"], data["password"]): 
        totalPages = ceil(Item.select().count() / 10)
        items = getStorageItemsOnPage(int(data["page"]))
        users = getUsers()
        return jsonify({'status': 'ok', "totalPages": totalPages, 'data': items, 'users': users})
    return jsonify({'status': "authError"})


@items_bp.route('/getUsersItems', methods=['POST'])
def usersItems():
    data = request.json
    if isUser(data["username"], data["password"]): 
        totalPages = ceil(ItemOwner.select().where(ItemOwner.owner == data["username"]).count() / 10)
        items = getUsersItems(data["username"], data["page"])
        return jsonify({'status': 'ok', "totalPages": totalPages, 'data': items})
    return jsonify({'status': "authError"})


@items_bp.route('/giveItem', methods=['POST'])
def giveItem():
    data = request.json
    if isUser(data["username"], data["password"]): 
        addOwnerForItem(data["user"], data["itemId"], data["quantity"])
        return jsonify({'status': "ok"})
    return jsonify({'status': "authError"})