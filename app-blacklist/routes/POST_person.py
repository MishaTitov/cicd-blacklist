from flask import Blueprint
from flask import request
from flask import jsonify
from data.mongodb_handler import connect_to_mongodb

post_person_bp = Blueprint('post_person', __name__)

@post_person_bp.route('/api/add', methods=['POST'])
def post_person():
    """
    Add a new person to the blacklist.
    """
    name = request.form.get('name')
    reason = request.form.get('reason')

    if not name or not reason:
        return jsonify({"error": "Name and reason are required"}), 400  # Return an error if fields are missing

    new_person = {'name': name, 'reason': reason}
    collection = connect_to_mongodb()
    collection.insert_one(new_person)  # Insert the new person into the MongoDB collection

    return jsonify({"message": "Person added successfully"}), 201  # Return a success message