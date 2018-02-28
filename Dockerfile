FROM python:alpine

RUN pip install requests

RUN mkdir /data

COPY entrypoint.py /

ENTRYPOINT ["python", "/entrypoint.py"]