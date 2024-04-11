FROM python:3.10
COPY . /app

WORKDIR /app
RUN apt-get update
RUN pip3 install -r requirements.txt

CMD ["python3", "/app/app.py", "/conf/input.txt"]