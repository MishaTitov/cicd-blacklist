from flask import Blueprint
from flask import jsonify
# from data.data_json_handler import load_data
from data.mongodb_handler import load_data

get_list_bp = Blueprint('get_list', __name__)
    
@get_list_bp.route('/api/get_list', methods=['GET'])
def get_blacklist():
    blacklist = load_data()
    return jsonify(blacklist)