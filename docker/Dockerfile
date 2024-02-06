FROM python:3.9.18-alpine3.19

RUN pip install -U Flask
RUN pip install waitress

WORKDIR /app
COPY ./src /app

EXPOSE 8080
CMD ["python3", "main.py"]
