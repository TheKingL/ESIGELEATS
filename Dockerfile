FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY controllers/ controllers/
COPY models/ models/
COPY routes/ routes/
COPY utils/ utils/
COPY sql/ sql/
COPY sql.py .
COPY templates/ templates/
COPY static/ static/
COPY utils/ utils/
COPY app.py .

EXPOSE 5050

CMD ["python", "app.py"]