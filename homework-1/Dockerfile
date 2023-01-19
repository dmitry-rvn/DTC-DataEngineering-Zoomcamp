FROM python:3.9.1-buster

RUN apt-get update
RUN apt-get install wget -y
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python", "ingest_data.py"]