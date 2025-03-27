@echo off
cd /d %~dp0
python -m streamlit run app.py --server.port 8501 --server.address localhost --browser.serverAddress localhost --browser.serverPort 8501 