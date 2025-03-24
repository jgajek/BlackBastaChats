import sqlite3
import boto3

def translate_and_store(db_file="chat_logs.db", table_name="messages", region_name="eu-west-1"):  # Replace with your AWS region
    """
    Translates Russian messages in an SQLite table to English using Amazon Translate
    and stores the translations in a new column.
    """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Select messages from the table.
        cursor.execute(f"SELECT rowid, message FROM {table_name}")
        rows = cursor.fetchall()

        translate = boto3.client(service_name='translate', region_name=region_name, use_ssl=True)

        for rowid, message in rows:
            try:
                # Translate the message.
                result = translate.translate_text(Text=message, SourceLanguageCode="ru", TargetLanguageCode="en")
                translated_text = result['TranslatedText']

                # Update the table with the translated message.
                cursor.execute(f"UPDATE {table_name} SET translated_aws = ? WHERE rowid = ?", (translated_text, rowid))

            except Exception as e:
                print(f"Error translating or updating row {rowid}: {e}")
                continue #continue to next row if error occurs.

        conn.commit()
        conn.close()
        print("Translation and database update complete.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage:
translate_and_store() #Make sure you have your AWS credentials configured.
