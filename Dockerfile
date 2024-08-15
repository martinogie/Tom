FROM python:3.9-slim

WORKDIR /


COPY best_model /
COPY Dr-Tom.py /
COPY requirements.txt /
COPY static /
COPY buildspec.yml /

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "Dr-Tom:app", "--host", "0.0.0.0", "--port", "8000"]

docker build -t doctortom-app .
