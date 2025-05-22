FROM python:3.12

WORKDIR /app

COPY * ./

RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
