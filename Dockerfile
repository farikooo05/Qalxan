FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Retrain inside the image so the model matches the installed scikit-learn exactly.
RUN python scripts/train.py

ENV PORT=7860
EXPOSE 7860
CMD ["sh", "-c", "uvicorn qalxan.api:app --host 0.0.0.0 --port ${PORT}"]
