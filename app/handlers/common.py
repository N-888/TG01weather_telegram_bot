# Импортируем F, чтобы удобно фильтровать текстовые сообщения.
from aiogram import F
# Импортируем Router, чтобы сгруппировать все обработчики в одном месте.
from aiogram import Router
# Импортируем фильтр команды /help.
from aiogram.filters import Command
# Импортируем фильтр команды /start.
from aiogram.filters import CommandStart
# Импортируем тип Message, чтобы правильно работать с входящими сообщениями.
from aiogram.types import Message

# Импортируем клавиатуру главного меню.
from app.keyboards.main_menu import main_menu_keyboard
# Импортируем функцию получения погоды.
from app.services.weather import get_weather

# Создаем роутер для команд и обычных сообщений.
router = Router()


# Обрабатываем команду /start.
@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    # Отправляем красивое приветствие и сразу показываем клавиатуру.
    await message.answer(
        "<b>Привет! 👋</b>\n\n"
        "Я современный Telegram-бот с прогнозом погоды.\n"
        "Нажми кнопку <b>🌤 Погода</b> или используй команду <b>/weather</b>, "
        "чтобы получить прогноз для выбранного города.\n\n"
        "Если захочешь посмотреть все возможности, нажми <b>ℹ️ Помощь</b> или введи <b>/help</b>.",
        reply_markup=main_menu_keyboard,
    )


# Обрабатываем команду /help.
@router.message(Command("help"))
# Обрабатываем нажатие кнопки помощи.
@router.message(F.text == "ℹ️ Помощь")
async def cmd_help(message: Message) -> None:
    # Отправляем понятную справку по всем возможностям бота.
    await message.answer(
        "<b>Список команд 📚</b>\n\n"
        "🔹 <b>/start</b> — запустить бота и открыть меню\n"
        "🔹 <b>/help</b> — показать подсказку по командам\n"
        "🔹 <b>/weather</b> — показать прогноз погоды\n\n"
        "Также ты можешь просто нажимать кнопки на клавиатуре под полем ввода.",
        reply_markup=main_menu_keyboard,
    )


# Обрабатываем команду /weather.
@router.message(Command("weather"))
# Обрабатываем нажатие кнопки погоды.
@router.message(F.text == "🌤 Погода")
async def cmd_weather(message: Message) -> None:
    # Пытаемся получить свежие данные о погоде.
    try:
        # Запрашиваем прогноз у погодного сервиса.
        weather = await get_weather()

        # Формируем красивое сообщение с погодой.
        text = (
            f"<b>Погода для города {weather['city']} 🌍</b>\n\n"
            f"🌡 Сейчас: <b>{weather['temperature_now']:.1f}°C</b>\n"
            f"☁️ Состояние: <b>{weather['weather_text']}</b>\n"
            f"💨 Ветер: <b>{weather['wind_speed']:.1f} км/ч</b>\n"
            f"📈 Максимум сегодня: <b>{weather['temperature_max']:.1f}°C</b>\n"
            f"📉 Минимум сегодня: <b>{weather['temperature_min']:.1f}°C</b>"
        )

        # Отправляем пользователю готовый прогноз.
        await message.answer(text, reply_markup=main_menu_keyboard)

    # Ловим любую ошибку, чтобы бот не падал и дал человеку понятный ответ.
    except Exception:
        # Сообщаем, что сейчас не удалось получить прогноз.
        await message.answer(
            "⚠️ Не удалось получить прогноз погоды.\n"
            "Проверь интернет, настройки проекта и попробуй еще раз чуть позже.",
            reply_markup=main_menu_keyboard,
        )


# Обрабатываем все остальные сообщения, которые бот пока специально не понимает.
@router.message()
async def cmd_unknown(message: Message) -> None:
    # Подсказываем пользователю, какие команды уже реализованы.
    await message.answer(
        "Я пока понимаю только команды <b>/start</b>, <b>/help</b> и <b>/weather</b>.\n"
        "Нажми кнопку на клавиатуре ниже 👇",
        reply_markup=main_menu_keyboard,
    )