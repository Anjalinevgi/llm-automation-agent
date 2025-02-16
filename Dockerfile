FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir \
    flask \
    requests \
    pandas \
    torch \
    tensorflow \
    pillow \
    pytesseract \
    transformers \
    beautifulsoup4 \
    markdown \
    speechrecognition 

CMD ["python", "main.py"]


