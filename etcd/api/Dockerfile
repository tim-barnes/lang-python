FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY src/ .

ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "--port", "5000", "main:app" ]
