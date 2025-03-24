import sqlite3

def parse_chat_logs(log_file, db_file="chat_logs.db", table_name="messages"):
    """
    Parses a chat log file and inserts the messages into an SQLite table.

    Args:
        log_file (str): The path to the chat log file.
        db_file (str): The path to the SQLite database file.
        table_name (str): The name of the table to insert data into.
    """

    messages = []
    with open(log_file, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line == '{':
            message_data = {}
            i += 1  # Move to the next line

            # Extract timestamp
            line = lines[i].strip()
            if line.startswith('timestamp:'):
                message_data['timestamp'] = line.split('timestamp:')[1].strip().rstrip(',')
                i += 1

            # Extract chat_id
            line = lines[i].strip()
            if line.startswith('chat_id:'):
                message_data['chat_id'] = line.split('chat_id:')[1].strip().rstrip(',')
                i += 1

            # Extract sender_alias
            line = lines[i].strip()
            if line.startswith('sender_alias:'):
                message_data['sender_alias'] = line.split('sender_alias:')[1].strip().rstrip(',')
                i += 1

            # Extract message
            message_lines = []
            line = lines[i].strip()
            if line.startswith('message:'):
                message_lines.append(line.split('message:')[1].strip())
                i += 1
                while i < len(lines) and not (lines[i].rstrip() == '}' and (i+1 == len(lines) or lines[i+1].rstrip() == '{')):
                    message_lines.append(lines[i].strip())
                    i += 1
            message_data['message'] = '\n'.join(message_lines)  # Join multi-lines

            messages.append(message_data)
            i += 1  # Move past the closing curly brace
        else:
            print(f"{i}: {line}")
            quit()
            i += 1  # Move to the next line

    # Insert messages into SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            timestamp TEXT,
            chat_id TEXT,
            sender_alias TEXT,
            message TEXT,
            translated_aws TEXT
        )
    """)

    # Insert messages
    for msg in messages:
        cursor.execute(f"""
            INSERT INTO {table_name} (timestamp, chat_id, sender_alias, message)
            VALUES (?, ?, ?, ?)
        """, (msg['timestamp'], msg['chat_id'], msg['sender_alias'], msg['message']))

    conn.commit()
    conn.close()

# Usage:
log_file = "blackbasta_chats.txt"  # Replace with the actual path
parse_chat_logs(log_file)
