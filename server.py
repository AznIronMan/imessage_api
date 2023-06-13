import os, sqlite3, sys

from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sslify import SSLify

from queries import create_query as get_messages
from utils import env_check, init_checks, ssl_check, start_sh_check

app = Flask(__name__)

if not init_checks():
    sys.exit(1)

if env_check():
    load_dotenv()
else:
    print("Error loading .env file.")
    sys.exit(1)

if ssl_check():
    sslify = SSLify(app)

start_sh_check()

@app.route('/messages', methods=['GET'])
def get_messages():
    try:
        type = request.args.get('type', 'all')
        start = request.args.get('start', '2001-01-01 00:00')
        end = request.args.get('end', datetime.now().strftime("%Y-%m-%d %H:%M"))

        db_path = os.getenv('DB_PATH')
        my_number = os.getenv('MY_NUMBER')

        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        query = get_messages(type, my_number, start, end)
        c.execute(query)
        rows = c.fetchall()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        try:
            conn.close()
        except:
            pass
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print(f'Starting iMessages API server on {os.getenv("listen_host")}:{os.getenv("listen_port")}')
    print('Press Ctrl+C to quit.')
    app.run(debug=True, host=os.getenv('listen_host'), port=os.getenv('listen_port'))