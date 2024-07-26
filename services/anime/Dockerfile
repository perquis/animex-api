FROM alpine:3.12

RUN apk add --no-cache \
  python3 \
  py3-pip

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
  poetry config virtualenvs.create false && \
  poetry install --no-dev

COPY . .

RUN ./.venv/Scripts/activate

CMD ["fastapi", "run", "main.py"]