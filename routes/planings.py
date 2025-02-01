from flask import Blueprint, request, jsonify
from models.user import * 
from models.plan import *
from math import ceil


planings_bp = Blueprint("planings", __name__)


@planings_bp.route('/newPlaning', methods=['POST'])
def newPlaning():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status =='ok':
        createPlaning(data["itemName"], data["itemDescription"], data["itemQuantity"], data["supplier"], data["price"])
    return jsonify({'status': status})

@planings_bp.route('/changePlanningStatus', methods=['POST'])
def setPlanningStatus():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status =='ok':
        changePlanningStatus(data["id"], data["completed"])
    return jsonify({'status': status})


@planings_bp.route('/getPlanings', methods=['POST'])
def planings():
    data = request.json
    status = isAdmin(data["username"], data["password"])
    if status =='ok':
        completedPlannings, uncompletedPlannings = getPlanings()
        return jsonify({'status': 'ok', 'completedPlannings': completedPlannings, 'uncompletedPlannings': uncompletedPlannings})
    return jsonify({'status': status})

