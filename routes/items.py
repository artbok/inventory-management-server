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
        item =  createItem(None, itemType.type, data["quantity"])
        createReport(f"{data["username"]} создал предмет {itemType.name} с описанием {itemType.description}, в количестве {item.quantity}шт.")
    return jsonify({'status': status})
    


@items_bp.route('/editItem', methods=['POST'])
def edit_item():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status == 'ok':
        item: Item = Item.get_by_id(data["itemId"])
        type = getItemType(item.type)
        editItem(data["itemId"], data["newName"], data["newDescription"], data["newQuantity"])
        createReport(f"{data["username"]} отредактировал предмет {type.name}({type.description}, {item.quantity}шт.) на {data["newName"]} ({data["newDescription"]}, {data["newQuantity"]}шт.)")
    return jsonify({'status': status})


@items_bp.route('/deleteItem', methods=['POST'])
def delete_item():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status == 'ok':
        deleteItem(data["itemId"], data["quantity"])
        item: Item = Item.get_by_id(data["itemId"])
        type = getItemType(item.type)
        createReport(f"{data["username"]} удалил предмет {type.name} с описанием {type.description}, в количестве {data["quantity"]}шт.")
    return jsonify({'status': status})


@items_bp.route('/changeItemStatus', methods=['POST'])
def change_item_status():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status == 'ok':
        changeStatus(data["itemId"], data["quantity"], data["status"], data["username"])
        item: Item = Item.get_by_id(data["itemId"])
        type = getItemType(item.type)
        createReport(f"{data["username"]} установил статус {data["status"]} предмету {type.name}({type.description}, {data["quantity"]}шт.)")
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
        item: Item = Item.get_by_id(data["itemId"])
        type = getItemType(item.type)
        createReport(f"{data["username"]} выдал предмет {type.name}, пользователю {data["user"]} в количестве {data["quantity"]}шт., с описанием {type.description}")
        return jsonify({'status': "ok"})
    return jsonify({'status': "authError"})