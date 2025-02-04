from flask import Blueprint

health_bp = Blueprint('health', __name__)
    
@health_bp.route('/health', methods=['GET'])
def health():
    try:
        return "OK", 200
    except:
        return "Failure", 500