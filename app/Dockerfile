FROM python:3.9-slim

RUN apt-get update && apt-get install gcc -y
RUN pip install --upgrade pip
RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

COPY . .
CMD [ "python3", "-u", "app.py"]