from flask import Blueprint, request, jsonify
from models.user import * 
from models.replacement_request import *
from math import ceil


replacement_requests_bp = Blueprint("replacement_requests", __name__)


@replacement_requests_bp.route('/newReplacementRequest', methods=['POST'])
def newReplacementRequest():
    data = request.json
    if isUser(data['username'], data['password']): 
        createReplacementRequest(data["owner"], data["itemId"], data["quantity"])
        return jsonify({'status': 'ok'})
    return jsonify({'status': "authError"})


@replacement_requests_bp.route('/getReplacementsRequests', methods=['POST'])
def replacementsRequests():
    data = request.json
    if isUser(data['username'], data['password']):
        items = getReplacementsRequests(data['owner'])
        return jsonify({'status': 'ok', 'data': items})
    return jsonify({'status': "authError"})


