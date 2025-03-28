# Black Basta Chat Log Analysis

This repository contains tools and data for analyzing the leaked Black Basta ransomware gang chat logs that were published on Telegram in February 2025. This project includes parsing scripts, translation tools, and a SQLite database of the processed communications.

⚠️ **IMPORTANT**: This data is provided for research and educational purposes only. The contents may include sensitive information related to cybercrime activities.

## Repository Contents

- `blackbasta_chats.txt` - Raw chat logs from the Black Basta Telegram leak
- `blackbasta_chats.db` - SQLite3 database containing parsed and processed chat messages
- `parse_bb.py` - Python script for parsing the raw chat logs into structured data
- `translate_bb.py` - Python script for translating non-English messages using AWS Translate
- `oversized.log` - Error log containing messages that exceeded AWS Translate size limits
- `daily_chats/` - Directory containing daily chat log files (format: chat_YYYY-MM-DD.txt)
- `daily_summaries/` - Directory containing AI-generated summaries of daily chat contents
- `analyze_daily_chats.py` - Script that processes daily chat files and generates summaries using Gemini AI
- `extract_edr_content.py` - Script that analyzes daily chats for EDR/AV evasion content and saves findings to edr_bypass_content.txt
- `edr_bypass_content.txt` - Consolidated file containing EDR/AV evasion related content extracted from daily chats
- `generate_edr_article.py` - Script that generates a comprehensive article analyzing EDR evasion tools and techniques using Gemini AI
- `edr_bypass_article.txt` - Generated article analyzing EDR evasion content from the chat logs

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
