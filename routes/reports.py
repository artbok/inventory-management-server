from flask import Blueprint, request, jsonify
from services.report_service import *
from services.user_service import isAdmin

report_bp = Blueprint("report", __name__)
   


@report_bp.route('/getReports', methods=['POST'])
def get_reports():
    data = request.json
    if isAdmin(data['username'], data['password']):
        items = getReports(data['page'])
        return jsonify({'status': 'ok', 'data': items})
    return jsonify({'status': "authError"}) 
