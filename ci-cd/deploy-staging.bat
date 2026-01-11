@echo off 
echo === STAGING DEPLOYMENT START === 
pip install -r requirements.txt 
echo Starting Flask app in staging... 
start /B python src\app\main.py 
echo === STAGING DEPLOYMENT SUCCESS === 
timeout /t 3 
