from routes.GET_list import get_list_bp
from routes.GET_by_name import get_by_name_bp
from routes.POST_person import post_person_bp
from routes.DELETE_person import delete_person_bp
from routes.health import health_bp
# from routes.metrics import metrics_bp

blueprints = [
    get_list_bp,
    get_by_name_bp,
    post_person_bp,
    delete_person_bp,
    health_bp,
    # metrics_bp
]

def register_routes(app):
    """
    Register all routes of app
    """
    for bp in blueprints:
        app.register_blueprint(bp)