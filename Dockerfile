FROM arm32v6/python:3-alpine3.7
COPY qemu-arm-static /usr/bin/

COPY . .

RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies

ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["python3", "solar_tracker.py"]

