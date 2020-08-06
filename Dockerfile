FROM python:3.8-slim-buster

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

ADD . /app

RUN chmod +x /app/entrypoint.sh
RUN chmod -R 755 /app

CMD [ "/app/entrypoint.sh" ]
