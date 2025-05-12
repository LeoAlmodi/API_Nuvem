FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app .
# CMD ["tail", "-f", "/dev/null"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
