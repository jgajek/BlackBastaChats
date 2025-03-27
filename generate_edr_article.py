import os
from google import genai
from pathlib import Path

# Configure the Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY environment variable")

client = genai.Client(api_key=GOOGLE_API_KEY)

def generate_edr_article(edr_content):
    prompt = """
    Based on the following EDR/AV evasion content from a cybercrime group's chat logs, write a comprehensive article that analyzes and synthesizes the information. 
    Focus on the following aspects:
    1. EDR/AV products targeted by the group
    2. Specific bypass tools and EDR killers mentioned
    3. Evasion techniques and methods discussed
    4. Common problems or challenges encountered
    5. Interesting longer quotes by the gang members on the subject of EDR/AV evasion

    Format the article with clear sections and bullet points where appropriate. Include references to a specific date for all major points.  Make it professional and analytical in tone.

    Content to analyze:
    {content}
    """.format(content=edr_content)

    # Generate response using Gemini 2.0 Flash
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text

def main():
    # Read the EDR bypass content
    edr_content_file = Path("edr_bypass_content.txt")
    if not edr_content_file.exists():
        print("Error: edr_bypass_content.txt not found")
        return

    try:
        with open(edr_content_file, 'r', encoding='utf-8') as f:
            edr_content = f.read()

        # Generate the article
        article = generate_edr_article(edr_content)

        # Save the article
        output_file = Path("edr_bypass_article.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(article)

        print(f"Article has been generated and saved to {output_file}")

    except Exception as e:
        print(f"Error generating article: {str(e)}")

if __name__ == "__main__":
    main() 
