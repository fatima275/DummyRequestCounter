from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

# Redis configuration
redis_host = os.getenv('REDIS_HOST', 'redis-service')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route('/')
def home():
    return 'Welcome to Requests Counter App! Use /count to see request counts.'

@app.route('/count')
def count_requests():
    try:
        # Increment counter for each request
        count = redis_client.incr('request_count')
        client_ip = request.remote_addr

        # Log the request
        print(f"Request #{count} from IP: {client_ip}")

        return jsonify({
            'request_count': count,
            'client_ip': client_ip
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)