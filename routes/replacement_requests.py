from flask import Blueprint, request, jsonify
from models.user import * 
from models.replacement_request import *
from services.user_service import isUser
from services.replacement_request_service import *


replacement_requests_bp = Blueprint("replacement_requests", __name__)


@replacement_requests_bp.route('/newReplacementRequest', methods=['POST'])
def newReplacementRequest():
    data = request.json
    if isUser(data['username'], data['password']): 
        createReplacementRequest(data["owner"], data["itemId"], data["quantity"])
        return jsonify({'status': 'ok'})
    return jsonify({'status': "authError"})


@replacement_requests_bp.route('/getReplacementRequests', methods=['POST'])
def get_replacement_requests():
    data = request.json
    if isUser(data['username'], data['password']):
        items = getReplacementsRequests(data['owner'])
        return jsonify({'status': 'ok', 'data': items})
    return jsonify({'status': "authError"})


@replacement_requests_bp.route('/acceptReplacementRequest', methods=['POST'])
def accept_replacement_request():
    data = request.json
    if isUser(data['username'], data['password']):
        status = acceptReplacementRequest(data["id"])
        return jsonify({'status': status})
    return jsonify({'status': "authError"})


@replacement_requests_bp.route('/declineReplacementRequest', methods=['POST'])
def decline_replacement_request():
    data = request.json
    if isUser(data['username'], data['password']):
        declineReplacementRequest(data["id"])
        return jsonify({'status': 'ok'})
    return jsonify({'status': "authError"})