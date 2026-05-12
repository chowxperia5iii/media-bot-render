FROM python:3.11-slim\nRUN apt-get update && apt-get install -y ffmpeg\nCOPY . .\nRUN pip install -r requirements.txt\nCMD streamlit run app.py --server.port 8080
