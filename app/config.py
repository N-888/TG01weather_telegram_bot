# Импортируем os, чтобы читать переменные окружения из .env.
import os
# Импортируем dataclass, чтобы удобно хранить настройки проекта в одном объекте.
from dataclasses import dataclass
# Импортируем Path, чтобы надежно строить путь к файлу .env.
from pathlib import Path
# Импортируем load_dotenv, чтобы загрузить переменные из файла .env.
from dotenv import load_dotenv

# Определяем корневую папку проекта.
BASE_DIR = Path(__file__).resolve().parent.parent
# Формируем путь до файла .env, который лежит в корне проекта.
ENV_PATH = BASE_DIR / ".env"
# Загружаем переменные из файла .env в окружение программы.
load_dotenv(ENV_PATH)


# Создаем dataclass со всеми настройками приложения.
@dataclass
class Settings:
    # Храним токен Telegram-бота.
    bot_token: str
    # Храним красивое имя города, которое будет показано пользователю.
    city_name: str
    # Храним широту выбранного города.
    latitude: float
    # Храним долготу выбранного города.
    longitude: float
    # Храним часовой пояс выбранного города.
    timezone: str


# Создаем функцию для безопасного чтения обязательных переменных окружения.
def get_env(name: str) -> str:
    # Получаем значение переменной по ее имени.
    value = os.getenv(name)
    # Проверяем, что переменная действительно найдена и не пустая.
    if not value:
        # Выбрасываем понятную ошибку, если пользователь забыл заполнить .env.
        raise ValueError(f"В файле .env не заполнена обязательная переменная: {name}")
    # Возвращаем найденное значение.
    return value


# Собираем все настройки в один объект settings.
settings = Settings(
    bot_token=get_env("BOT_TOKEN"),
    city_name=get_env("CITY_NAME"),
    latitude=float(get_env("LATITUDE")),
    longitude=float(get_env("LONGITUDE")),
    timezone=get_env("TIMEZONE"),
)