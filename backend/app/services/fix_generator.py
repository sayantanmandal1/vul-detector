from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

def suggest_fix(code: str, description: str) -> str:
    try:
        prompt = f"""The following code has this vulnerability: {description}.
Suggest a secure code fix, and explain why it's better.

Code:
{code}
"""
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating fix: {e}"
