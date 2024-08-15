FROM python:3.9-slim

WORKDIR /app


COPY best_model /app/best_model
COPY Dr-Tom.py /app/Dr-Tom.py
COPY requirements.txt /app/requirements.txt
COPY static /app/static

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "Dr-Tom:app", "--host", "0.0.0.0", "--port", "8000"]
