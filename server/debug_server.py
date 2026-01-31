try:
    from flask import Flask
    from flask_cors import CORS
    import sys
    print("Imports successful", flush=True)
except ImportError as e:
    print(f"ImportError: {e}", flush=True)
    import sys
    sys.exit(1)

print("Starting simple server test...", flush=True)
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return "Hello"

if __name__ == "__main__":
    print("About to run app...", flush=True)
    try:
        app.run(port=5001)
    except Exception as e:
        print(f"Error running app: {e}", flush=True)
