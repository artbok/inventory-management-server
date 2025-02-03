from flask import Blueprint, request, jsonify
from math import ceil
from services.user_service import *
from services.item_service import *
from services.item_type_service import *


items_bp = Blueprint("items", __name__)


@items_bp.route('/newItem', methods=['POST'])
def new_item():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status == 'ok':
        itemType = createItemType(data["name"], data["description"])
        createItem(None, itemType.type, data["quantity"])
    return jsonify({'status': status})


@items_bp.route('/editItem', methods=['POST'])
def edit_item():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status == 'ok':
        editItem(data["itemId"], data["newName"], data["newDescription"], data["newQuantity"])
    return jsonify({'status': status})


@items_bp.route('/deleteItem', methods=['POST'])
def delete_item():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status == 'ok':
        deleteItem(data["itemId"], data["quantity"])
    return jsonify({'status': status})


@items_bp.route('/changeItemStatus', methods=['POST'])
def change_item_status():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status == 'ok':
        changeStatus(data["itemId"], data["quantity"], data["status"])
    return jsonify({'status': status})


@items_bp.route('/getItems', methods=['POST'])
def get_items():
    data = request.json
    if isUser(data["username"], data["password"]): 
        totalPages = ceil(ItemType.select().count() / 10)
        items = getStorageItemsOnPage(int(data["page"]))
        users = getUsers()
        return jsonify({'status': 'ok', "totalPages": totalPages, 'data': items, 'users': users})
    return jsonify({'status': "authError"})


@items_bp.route('/getUserItems', methods=['POST'])
def get_user_Items():
    data = request.json
    if isUser(data["username"], data["password"]): 
        totalPages = ceil(Item.select().where(Item.owner == data["username"]).count() / 10)
        items = getUserItems(data["username"], data["page"])
        return jsonify({'status': 'ok', "totalPages": totalPages, 'data': items})
    return jsonify({'status': "authError"})


@items_bp.route('/giveItem', methods=['POST'])
def give_item():
    data = request.json
    if isUser(data["username"], data["password"]): 
        giveItem(data["itemId"], data["quantity"], data["user"])
        return jsonify({'status': "ok"})
    return jsonify({'status': "authError"})