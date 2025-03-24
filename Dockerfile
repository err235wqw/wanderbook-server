FROM python:3.13-slim
EXPOSE 8000
WORKDIR /server_wanderbook
ADD . '/server_wanderbook/'
RUN pip install -r requirements.txt
CMD ["python", "server.py"]