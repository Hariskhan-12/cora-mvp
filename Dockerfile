FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir torch==2.7.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html 2>/dev/null || \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

RUN python -m scripts.ingest

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
