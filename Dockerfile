FROM python:3.9-slim-buster as python

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/* /

EXPOSE 8000
CMD gunicorn wm:app