FROM python:3.13-slim

WORKDIR /app

COPY ./pyproject.toml ./

RUN pip install .

COPY ./src ./src
COPY ./.env ./

CMD ["python3", "src/main.py"]