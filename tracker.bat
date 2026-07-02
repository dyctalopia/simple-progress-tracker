@echo off
REM Progress Tracker — launch script
REM Starts Flask server at port 5050 and opens browser.

cd /d "%~dp0"

python server.py %*
