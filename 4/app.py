rom flask import Flask, request, jsonify
from prometheus_client import Counter, generate_latest, REGISTRY, CollectorRegistry, CONTENT_TYPE_LATEST
import logging
import logging.handlers  # Import handlers explicitly
import os

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
EVENT_COUNT = Counter('event_count', 'Total number of events generated')

# Set up logging
log_directory = '/var/log/flask'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logger = logging.getLogger('event_logger')
logger.setLevel(logging.INFO)
logstash_handler = logging.handlers.SocketHandler('logstash', 5000)  # Adjust with your Logstash host and port
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logstash_handler.setFormatter(formatter)
logger.addHandler(logstash_handler)

@app.route('/')
def home():
    REQUEST_COUNT.inc()
    logger.info('Home endpoint was called')
    return 'Welcome to the Metrics API!'

@app.route('/generate_event', methods=['POST'])
def generate_event():
    REQUEST_COUNT.inc()
    EVENT_COUNT.inc()
    logger.info('Event generated')
    return jsonify({"status": "event generated"})

@app.route('/metrics')
def metrics():
    REQUEST_COUNT.inc()
    return generate_latest(REGISTRY), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)