FROM python:3.8-slim

COPY ./requirements.txt /data/requirements.txt
COPY ./main.py /data/main.py
COPY ./config.json /data/config.json

WORKDIR /data

# RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

CMD ["python", "-u", "main.py"]