from flask import Blueprint
from flask import request
from flask import jsonify
# from data.data_json_handler import load_data
from data.mongodb_handler import connect_to_mongodb

get_by_name_bp = Blueprint('get_by_name', __name__)

@get_by_name_bp.route('/api/search', methods=['GET'])
def get_by_name():
    """
    GET by name
    """
    name = request.args.get('name')
    if name:
        collection = connect_to_mongodb()
        # Perform a case-insensitive search for names containing the query string
        query = {"name": {"$regex": name, "$options": "i"}}
        filtered_bl = list(collection.find(query, {'_id': 0}))  # Exclude MongoDB's _id field
        return jsonify(filtered_bl)  # Return filtered results as JSON
    return jsonify([])  # Return an empty list if no name is provided