FROM python:3.13-slim
EXPOSE 8000
WORKDIR /server_wanderbook
ADD . '/server_wanderbook/'
RUN pip install -r requirements.txt
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
CMD ["python", "server.py"]