from dotenv import load_dotenv
import os

# файл запуска проекта
load_dotenv()  # Загружает переменные окружения из файла .env

from app import app

if __name__ == '__main__':
    app.run()
