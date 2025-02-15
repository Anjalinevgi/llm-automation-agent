FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN pip install flask requests

CMD ["python", "main.py"]