from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
print("Initialized.", flush=True)

try:
    client = genai.Client(api_key=api_key)
    print("Invoking Client directly...", flush=True)
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents="Say hello"
    )
    print("Response received:", flush=True)
    print(response.text, flush=True)
except Exception as e:
    print(f"Error invoking Client: {e}", flush=True)
