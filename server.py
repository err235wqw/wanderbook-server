import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import os
from dotenv import load_dotenv

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


class HTTPReqHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            connectionBD = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )

            with connectionBD:
                with connectionBD.cursor() as cursor:
                    cursor.execute(
                        "SELECT username FROM users WHERE username=%s", (data['username'],))
                    user = cursor.fetchone()

                    if user:
                        response = {"status": "success",
                                    "message": "Пользователь уже существует"}
                    else:
                        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                                       (data['username'], data['password']))
                        connectionBD.commit()
                        response = {"status": "success",
                                    "message": "Пользователь добавлен"}

                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            logging.error(f"Ошибка: {str(e)}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_GET(self):
        try:
            username = self.path.split('/')[-1]

            connectionBD = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )

            with connectionBD:
                with connectionBD.cursor() as cursor:
                    cursor.execute(
                        "SELECT password FROM users WHERE username=%s", (username,))
                    result = cursor.fetchone()

                    if result:
                        response = {"password": result[0]}
                        self.send_response(200)
                    else:
                        response = {"error": "Пользователь не найден"}
                        self.send_response(404)

                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            logging.error(f"Ошибка: {str(e)}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())


def run(server_class=HTTPServer, handler_class=HTTPReqHandler, port=8000):
    logging.basicConfig(level=logging.INFO,
                        filename="py_log.log", filemode="a")
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f'Сервер запущен на порту {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
