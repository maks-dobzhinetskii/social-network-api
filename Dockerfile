FROM python:3.9.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip3 install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]
