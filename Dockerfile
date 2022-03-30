FROM python:3.9-slim-buster as python

RUN apt-get update && apt-get install -y --no-install-recommends nginx

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /wm

EXPOSE 80
CMD ["/wm/scripts/launch.sh"]
