import os
import google.generativeai as genai
from pathlib import Path

# Configure the Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY environment variable")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def get_chat_summary(chat_content):
    prompt = """
    Please analyze this chat log from a cybercrime group and provide a concise summary of:
    1. Main topics discussed
    2. Key decisions or actions planned
    3. Notable interactions between participants
    
    Chat log:
    {content}
    """.format(content=chat_content)

    # Generate response
    response = model.generate_content(prompt)
    return response.text

def analyze_daily_files():
    daily_chats_dir = Path("daily_chats")
    
    if not daily_chats_dir.exists():
        print("Error: daily_chats directory not found")
        return

    # Process each daily chat file
    for chat_file in sorted(daily_chats_dir.glob("chat_*.txt")):
        print(f"\n{'='*80}")
        print(f"Analyzing {chat_file.name}")
        print(f"{'='*80}\n")

        try:
            # Read the chat content
            with open(chat_file, 'r', encoding='utf-8') as f:
                chat_content = f.read()

            # Get and print the summary
            summary = get_chat_summary(chat_content)
            print("SUMMARY:")
            print(summary)
            
        except Exception as e:
            print(f"Error processing {chat_file.name}: {str(e)}")

if __name__ == "__main__":
    analyze_daily_files() 
