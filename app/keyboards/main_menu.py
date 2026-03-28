# Импортируем KeyboardButton, чтобы создать обычные кнопки под полем ввода.
from aiogram.types import KeyboardButton
# Импортируем ReplyKeyboardMarkup, чтобы собрать клавиатуру из кнопок.
from aiogram.types import ReplyKeyboardMarkup

# Создаем главное меню бота с большими и удобными кнопками.
main_menu_keyboard = ReplyKeyboardMarkup(
    # Передаем список строк клавиатуры.
    keyboard=[
        # Создаем первую строку с кнопкой погоды.
        [KeyboardButton(text="🌤 Погода")],
        # Создаем вторую строку с кнопкой помощи.
        [KeyboardButton(text="ℹ️ Помощь")],
    ],
    # Просим Telegram уменьшить клавиатуру под экран устройства.
    resize_keyboard=True,
    # Добавляем подсказку внутри поля ввода.
    input_field_placeholder="Выберите действие ниже 👇",
)