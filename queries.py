def create_query(type, my_number, start=None, end=None):
    if type == 'range':
        return range_query(my_number, start, end)
    else:
        return default_query(my_number)

def default_query(my_number):
    query = f"""
    SELECT
        datetime(message.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
        message.text,
        CASE message.is_from_me
            WHEN 0 THEN '{my_number}'
            WHEN 1 THEN chat.chat_identifier
            ELSE 'Unknown'
        END as sms_from,
        CASE message.is_from_me
            WHEN 0 THEN chat.chat_identifier
            WHEN 1 THEN '{my_number}'
            ELSE 'Unknown'
        END as sms_to,
        CASE message.is_emote
            WHEN 0 THEN 'iMessage'
            WHEN 1 THEN 'SMS'
            ELSE 'Unknown'
        END as message_type
    FROM
        chat
        JOIN chat_message_join ON chat."ROWID" = chat_message_join.chat_id
        JOIN message ON chat_message_join.message_id = message."ROWID"
    ORDER BY
        message_date DESC;
    """
    return query

def range_query(my_number, start, end):
    query = f"""
    SELECT
        datetime(message.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
        message.text,
        CASE message.is_from_me
            WHEN 0 THEN '{my_number}'
            WHEN 1 THEN chat.chat_identifier
            ELSE 'Unknown'
        END as sms_from,
        CASE message.is_from_me
            WHEN 0 THEN chat.chat_identifier
            WHEN 1 THEN '{my_number}'
            ELSE 'Unknown'
        END as sms_to,
        CASE message.is_emote
            WHEN 0 THEN 'iMessage'
            WHEN 1 THEN 'SMS'
            ELSE 'Unknown'
        END as message_type
    FROM
        chat
        JOIN chat_message_join ON chat."ROWID" = chat_message_join.chat_id
        JOIN message ON chat_message_join.message_id = message."ROWID"
    WHERE 
        datetime(message.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") BETWEEN '{start}' AND '{end}'
    ORDER BY
        message_date DESC;
    """
    return query

def startup_script():
    script = """#!/bin/bash

cwdir() {
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    cd $DIR
}

check_env() {
    if [ ! -f .env ]; then
        echo "Error: .env does not exist. Please copy .env.example and create .env file."
        exit 1
    fi
    source .env
}

create_venv() {
    if [ ! -d "$VENV_NAME" ]; then
        python3 -m venv $VENV_NAME || { echo "Error: Couldn't create virtual environment. Try running the script as sudo."; exit 1; }
    fi
    source $VENV_NAME/bin/activate || { echo "Error: Couldn't activate virtual environment."; exit 1; }
}

check_requirements() {
    if [ ! -f requirements.txt ]; then
        cat > requirements.txt <<EOL
blinker==1.6.2
click==8.1.3
Flask==2.3.2
Flask-SSLify==0.1.5
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.3
python-dotenv==1.0.0
Werkzeug==2.3.6
EOL
    fi
    pip install -r requirements.txt
}

run_server() {
    python3 server.py
}

cwdir
check_env
create_venv
check_requirements
run_server
"""
    return script