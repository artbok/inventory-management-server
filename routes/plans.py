from flask import Blueprint, request, jsonify
from models.user import * 
from models.item import *
from models.plan import *
from math import ceil


plans_bp = Blueprint("plans", __name__)


@plans_bp.route('/getPlans', methods=['POST'])
def plans():
    data = request.json
    if isUser(data["username"], data["password"]): 
        totalPages = ceil(Plan.select().count() / 10)
        items = getStorageItemsOnPage(int(data["page"]))
        users = getUsers()
        return jsonify({'status': 'ok', "totalPages": totalPages, 'data': items, 'users': users})
    return jsonify({'status': "authError"})
