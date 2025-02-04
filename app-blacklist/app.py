from flask import Flask
from routes import register_routes
from prometheus_flask_exporter import PrometheusMetrics
# from data.data_json_handler import load_data
import os


app = Flask(__name__)
metrics = PrometheusMetrics(app)

register_routes(app)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/") 

if __name__=="__main__":
    app.logger.info(MONGO_URI)
    app.run(host='0.0.0.0', port=5000)