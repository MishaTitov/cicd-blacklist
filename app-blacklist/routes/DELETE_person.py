from flask import Blueprint
from flask import jsonify
from flask import request
# from data.data_json_handler import delete_entry
from data.mongodb_handler import connect_to_mongodb

delete_person_bp = Blueprint('delete_person', __name__)

@delete_person_bp.route('/api/delete', methods=['DELETE'])
def delete_person():
    """
    Delete a person from the blacklist by name.
    """
    name = request.form.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400  # Return an error if no name is provided

    collection = connect_to_mongodb()
    result = collection.delete_one({"name": name})  # Delete the person by name

    if result.deleted_count == 0:
        return jsonify({"error": "Person not found"}), 404  # Return an error if the person was not found

    return jsonify({"message": "Person deleted successfully"}), 200  # Return a success message