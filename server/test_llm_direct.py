from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
print("Initialized.", flush=True)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7
)

print("Invoking LLM...", flush=True)
try:
    response = llm.invoke("Say hello")
    print("Response received:", flush=True)
    print(response.content, flush=True)
except Exception as e:
    print(f"Error invoking LLM: {e}", flush=True)
