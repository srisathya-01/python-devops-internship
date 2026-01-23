import os 
from flask import Flask 
from dotenv import load_dotenv 
 
load_dotenv() 
app = Flask(__name__) 
 
@app.route('/') 
def home(): 
    env = os.getenv('ENV', 'development') 
    return f"Python DevOps Demo - ENV: {env}"

@app.route('/health', methods=['GET'])
def health_check():
    return {
        "status": "ok",
        "message": "Service is running"
    }, 200

if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0', port=5000) 
@app.route("/metrics")
def metrics():
    return "ok", 200
