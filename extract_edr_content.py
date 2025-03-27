import os
from google import genai
from pathlib import Path
from datetime import datetime

# Configure the Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY environment variable")

client = genai.Client(api_key=GOOGLE_API_KEY)

def extract_edr_content(chat_content, date_str):
    prompt = """
    Please analyze this chat log from a cybercrime group and extract ONLY content related to:
    - EDR (Endpoint Detection and Response) evasion techniques
    - Antivirus bypasses
    - EDR killer tools or methods
    
    If any such content exists, provide a detailed description of the techniques, tools, or methods discussed.
    If no such content exists, respond with "NO_EDR_CONTENT".
    
    Chat log:
    {content}
    """.format(content=chat_content)

    # Generate response using Gemini 2.0 Flash
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text

def analyze_daily_files():
    daily_chats_dir = Path("daily_chats")
    edr_output_file = Path("edr_bypass_content.txt")
    
    if not daily_chats_dir.exists():
        print("Error: daily_chats directory not found")
        return

    # Process each daily chat file
    for chat_file in sorted(daily_chats_dir.glob("chat_*.txt")):
        try:
            # Extract date from filename (assuming format chat_YYYY-MM-DD.txt)
            date_str = chat_file.name[5:-4]  # Removes "chat_" prefix and ".txt" suffix
            
            # Read the chat content
            with open(chat_file, 'r', encoding='utf-8') as f:
                chat_content = f.read()

            # Extract EDR-related content
            edr_content = extract_edr_content(chat_content, date_str)
            
            # Only append to the output file if EDR content was found
            if edr_content.strip() != "NO_EDR_CONTENT":
                with open(edr_output_file, 'a', encoding='utf-8') as out_file:
                    out_file.write(f"\n----------\n[{date_str}]\n----------\n")
                    out_file.write(edr_content)
                    out_file.write("\n")
                
                print(f"EDR content found in {chat_file.name} and added to output file")
            else:
                print(f"No EDR content found in {chat_file.name}")
            
        except Exception as e:
            print(f"Error processing {chat_file.name}: {str(e)}")

if __name__ == "__main__":
    analyze_daily_files() 
