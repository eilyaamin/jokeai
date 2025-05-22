FROM python:3.12

WORKDIR /app

COPY * ./

RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY . .

CMD ["python", "main.py", "--reload"]
