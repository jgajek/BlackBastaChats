# Black Basta Chat Log Analysis

This repository contains tools and data for analyzing the leaked Black Basta ransomware gang chat logs that were published on Telegram in February 2025. This project includes parsing scripts, translation tools, and a SQLite database of the processed communications.

⚠️ **IMPORTANT**: This data is provided for research and educational purposes only. The contents may include sensitive information related to cybercrime activities.

## Repository Contents

- `blackbasta_chats.txt` - Raw chat logs from the Black Basta Telegram leak
- `blackbasta_chats.db` - SQLite3 database containing parsed and processed chat messages
- `parse_bb.py` - Python script for parsing the raw chat logs into structured data
- `translate_bb.py` - Python script for translating non-English messages using AWS Translate
- `oversized.log` - Error log containing messages that exceeded AWS Translate size limits

## Database Schema

The SQLite3 database (`blackbasta_chats.db`) contains the following structure:

```sql
CREATE TABLE messages (
    timestamp TEXT,
    chat_id TEXT,
    sender_alias TEXT,
    message TEXT,
    translated_aws TEXT
);
```

## Notes

- Messages that exceed AWS Translate's size limits are logged in `oversized.log`
- The database includes both original and translated content where available
- Some messages may contain sensitive information or indicators of compromise (IOCs)
