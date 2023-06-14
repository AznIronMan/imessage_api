import contextlib, logging, os, sqlite3, sys

from datetime import datetime
from flask import Flask, request, jsonify
from flask_sslify import SSLify
from dotenv import load_dotenv

from queries import create_query
from utils import env_check, init_checks, ssl_check, start_sh_check

app = Flask(__name__)

if not init_checks():
    sys.exit(1)

if env_check():
    pass
else:
    print("Error loading .env file.")
    sys.exit(1)

if ssl_check():
    sslify = SSLify(app)

start_sh_check()

@app.route('/messages', methods=['GET'])
def get_messages():
    load_dotenv()
    conn = None
    try:
        type = request.args.get('type', 'all')
        start = request.args.get('start', '2001-01-01 00:00')
        end = request.args.get('end', datetime.now().strftime("%Y-%m-%d %H:%M"))

        # TO DO: Add header check for API key

        db_path = os.getenv('CHAT_DB_PATH')
        my_number = os.getenv('MY_NUMBER')

        conn = sqlite3.connect(str(db_path))
        c = conn.cursor()

        query = create_query(type, my_number, start, end)
        c.execute(query)
        rows = c.fetchall()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    load_dotenv()

    db_path = os.getenv('CHAT_DB_PATH')
    my_number = os.getenv('MY_NUMBER')

    if db_path is not None and os.path.exists(db_path):
        pass
    else:
        raise SystemExit('CHAT_DB_PATH is not accessible. Please go to Settings > Privacy > Full Disk Access and add Terminal to it. Then re-run this script with sudo.')

    port = int(os.getenv('LISTEN_PORT', '5000'))

    if os.getenv('DEBUG') is 'False':
        debug_mode = False
    elif os.getenv('DEBUG') is 'True':
        debug_mode = True
    else:
        debug_mode = False

    os.system('clear')

    print(f'Starting iMessages API server on {os.getenv("LISTEN_IP")}:{os.getenv("LISTEN_PORT")}')
    print()
    print('Press Ctrl+C to quit.')

    if debug_mode is False:
        with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
            app.run(debug=False, host=os.getenv('LISTEN_IP'), port=os.getenv('LISTEN_PORT'))
    else:
        app.run(debug=True, host=os.getenv('LISTEN_IP'), port=os.getenv('LISTEN_PORT'))