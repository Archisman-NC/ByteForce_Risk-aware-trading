import os
import pprint
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print("Attempting to list models...", flush=True)

# Try google-generativeai (the standard one)
try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    print("\n--- google.generativeai ---")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Name: {m.name}")
except ImportError:
    print("google.generativeai not installed")
except Exception as e:
    print(f"google.generativeai error: {e}")

# Try google.genai (the new one)
try:
    from google import genai
    client = genai.Client(api_key=api_key)
    print("\n--- google.genai ---")
    # This might fail if the method is different, but let's try
    # The new SDK documentation is sparse but client.models.list() is a good guess
    # or client.list_models()
    try:
        pager = client.models.list()
        for model in pager:
            print(f"Name: {model.name}")
    except Exception as e:
        print(f"google.genai list error: {e}")
        
except ImportError:
    print("google.genai not installed")
except Exception as e:
    print(f"google.genai client error: {e}")
