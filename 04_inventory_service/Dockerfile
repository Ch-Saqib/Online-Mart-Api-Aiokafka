FROM python:latest

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /inventory

COPY . /inventory/

RUN pip install poetry 

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-root

CMD [ "poetry","run","uvicorn","main:app","--host","0.0.0.0","--port","8084","--reload" ]