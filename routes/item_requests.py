from flask import Blueprint, request, jsonify
from services.item_request_service import *
from services.user_service import isUser

item_requests_bp = Blueprint("item_requests", __name__)


@item_requests_bp.route('/newItemRequest', methods=['POST'])
def new_itemRequest():
    data = request.json
    if isUser(data["username"], data["password"]):
        createItemRequest(data["id"], data["name"], data["description"], data["quantity"], data["username"])
        return jsonify({'status': 'ok'})
    return jsonify({'status': "authError"})  


@item_requests_bp.route('/getItemsRequests', methods=['POST'])
def items_requests():
    data = request.json
    if isUser(data['username'], data['password']):
        items = getItemsRequests(data['owner'])
        return jsonify({'status': 'ok', 'data': items})
    return jsonify({'status': "authError"}) 


@item_requests_bp.route('/acceptItemRequest', methods=['POST'])
def accept_item_request():
    data = request.json
    if isUser(data['username'], data['password']):
        status, required = acceptItemRequest(data["id"])
        return jsonify({'status': status, "required": required})
    return jsonify({'status': "authError"})


@item_requests_bp.route('/declineItemRequest', methods=['POST'])
def decline_item_request():
    data = request.json
    if isUser(data['username'], data['password']):
        declineItemRequest(data["id"])
        return jsonify({'status': 'ok'})
    return jsonify({'status': "authError"})
