FROM python:3.10-slim

COPY ./requirements.txt /data/requirements.txt
COPY ./main.py /data/main.py
COPY ./config.json /data/config.json

WORKDIR /data

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt --progress-bar off

CMD ["python", "-u", "main.py"]