FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y nginx && pip install gunicorn flask
RUN pip3 install -r requirements.txt

COPY . .
COPY wsgi.py /app/

#ENV FLASK_APP=app.py
EXPOSE 80

CMD ["sh", "-c", "service nginx start && gunicorn --bind 0.0.0.0:8080 wsgi:app"]
