FROM python:slim-buster

# FROM debian:latest

# RUN apt-get update && \ 
# 		apt-get install -y python3 python3-pip

RUN mkdir -p /app/service
WORKDIR /app

COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY . ./service

CMD ["uvicorn", "service.__main__:app", "--host=0.0.0.0", "--port=80"]
