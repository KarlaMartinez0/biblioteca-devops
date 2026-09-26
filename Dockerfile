FROM python:3.10-slim

WORKDIR /app

COPY app/requerimientos.txt ./
RUN pip install --no-cache-dir -r requerimientos.txt

COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]