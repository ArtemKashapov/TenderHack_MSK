FROM amd64/python:3.9-buster

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install catboost
RUN pip install openpyxl
RUN pip install xlrd
RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]