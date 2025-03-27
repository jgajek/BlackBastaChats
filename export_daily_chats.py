import sqlite3
from datetime import datetime
import os

def create_daily_logs():
    # Create output directory if it doesn't exist
    output_dir = "daily_chats"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Connect to the database
    conn = sqlite3.connect('blackbasta_chats.db')
    cursor = conn.cursor()

    # Get all unique dates from the database
    cursor.execute("""
        SELECT DISTINCT date(timestamp) 
        FROM messages 
        ORDER BY date(timestamp)
    """)
    dates = cursor.fetchall()

    # For each date, create a file with that day's messages
    for (date,) in dates:
        filename = os.path.join(output_dir, f"chat_{date}.txt")
        
        # Get all messages for this date
        cursor.execute("""
            SELECT timestamp, sender_alias, message 
            FROM messages 
            WHERE date(timestamp) = ? 
            ORDER BY timestamp
        """, (date,))
        
        messages = cursor.fetchall()
        
        # Write messages to file
        with open(filename, 'w', encoding='utf-8') as f:
            for timestamp, sender, message in messages:
                f.write(f"[{timestamp}] {sender}: {message}\n")
                f.write("-" * 20 + "\n")

    conn.close()

if __name__ == "__main__":
    create_daily_logs() 