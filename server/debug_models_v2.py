import os
import google.genai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("No API key found")
    exit(1)

print(f"Key found: {api_key[:5]}...", flush=True)

try:
    from google.generativeai import configure, list_models
    configure(api_key=api_key)
    print("Listing models...", flush=True)
    for m in list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except ImportError:
    # Try the new SDK if old one isn't present
    print("Using google-genai SDK...", flush=True)
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        # Verify how to list models in new SDK or just try a standard one
        print("SDK initialized. Trying to interact...")
        # Just try a simple generation with 1.5-flash
        response = client.models.generate_content(
            model="gemini-1.5-flash", contents="Hello"
        )
        print("1.5-flash works: ", response.text)
    except Exception as e:
        print(f"Error: {e}")
