from flask import Flask, request
import subprocess
import sys
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

active_processes = {}

@app.route('/')
def home():
    return "Nuker Bot API is running!"

@app.route('/start', methods=['POST'])
def start_bot():
    data = request.json
    token = data.get('token')
    
    if not token:
        return {"error": "Token required"}, 400
    
    try:
        # Railway par subprocess spawn allowed hai
        process = subprocess.Popen(
            [sys.executable, "nuker_bot.py", token],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Process ko store karo
        active_processes[process.pid] = process
        
        return {"status": "started", "pid": process.pid}
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {"error": str(e)}, 500

@app.route('/list', methods=['GET'])
def list_processes():
    return {"active_pids": list(active_processes.keys())}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
