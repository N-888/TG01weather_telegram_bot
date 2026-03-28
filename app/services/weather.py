# Импортируем Any, чтобы типизировать словарь результата.
from typing import Any
# Импортируем aiohttp, чтобы отправлять асинхронный HTTP-запрос к погодному API.
import aiohttp

# Импортируем настройки с координатами города и часовым поясом.
from app.config import settings

# Создаем словарь расшифровки кодов погоды Open-Meteo в понятный русский текст.
WEATHER_CODE_MAP = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Туман с инеем",
    51: "Слабая морось",
    53: "Умеренная морось",
    55: "Сильная морось",
    56: "Слабая ледяная морось",
    57: "Сильная ледяная морось",
    61: "Слабый дождь",
    63: "Умеренный дождь",
    65: "Сильный дождь",
    66: "Слабый ледяной дождь",
    67: "Сильный ледяной дождь",
    71: "Слабый снег",
    73: "Умеренный снег",
    75: "Сильный снег",
    77: "Снежные зерна",
    80: "Слабые ливни",
    81: "Умеренные ливни",
    82: "Сильные ливни",
    85: "Слабые снегопады",
    86: "Сильные снегопады",
    95: "Гроза",
    96: "Гроза со слабым градом",
    99: "Гроза с сильным градом",
}


# Создаем асинхронную функцию, которая получает погоду по координатам выбранного города.
async def get_weather() -> dict[str, Any]:
    # Сохраняем адрес погодного API.
    url = "https://api.open-meteo.com/v1/forecast"

    # Собираем параметры запроса.
    params = {
        "latitude": settings.latitude,
        "longitude": settings.longitude,
        "current": "temperature_2m,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": settings.timezone,
        "forecast_days": 1,
    }

    # Ограничиваем общее время ожидания запроса, чтобы бот не зависал слишком долго.
    timeout = aiohttp.ClientTimeout(total=15)

    # Открываем асинхронную HTTP-сессию.
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Отправляем GET-запрос к API с нашими параметрами.
        async with session.get(url=url, params=params) as response:
            # Проверяем, что сервер вернул успешный ответ без ошибки.
            response.raise_for_status()
            # Превращаем JSON-ответ сервера в обычный словарь Python.
            data = await response.json()

    # Достаем блок с текущей погодой.
    current = data["current"]
    # Достаем блок с дневным прогнозом.
    daily = data["daily"]

    # Возвращаем уже готовый и удобный для бота словарь.
    return {
        "city": settings.city_name,
        "temperature_now": current["temperature_2m"],
        "weather_text": WEATHER_CODE_MAP.get(current["weather_code"], "Состояние погоды не определено"),
        "wind_speed": current["wind_speed_10m"],
        "temperature_max": daily["temperature_2m_max"][0],
        "temperature_min": daily["temperature_2m_min"][0],
    }