import os

#клдасс конфигурации проекта
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'paraplan'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # Подключение к базе данных SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключение предупреждений о модификациях
