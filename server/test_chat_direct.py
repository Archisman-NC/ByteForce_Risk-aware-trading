from chat_bot import chat
import sys

print("Invoking chat...", flush=True)
try:
    response = chat("What is the verdict for TCS?")
    print("Response received:", flush=True)
    print(response, flush=True)
except Exception as e:
    print(f"Error invoking chat: {e}", flush=True)
