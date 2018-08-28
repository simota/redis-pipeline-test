FROM python:3.7.0-alpine

RUN mkdir /app
COPY ./app/requirements.txt /requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r /requirements.txt
CMD ["python", "/app/main.py"]
