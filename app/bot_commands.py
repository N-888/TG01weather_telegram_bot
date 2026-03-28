# Импортируем Bot, чтобы работать с уже созданным объектом Telegram-бота.
from aiogram import Bot
# Импортируем BotCommand, чтобы описать список команд, видимых в меню бота.
from aiogram.types import BotCommand


# Создаем асинхронную функцию регистрации команд бота.
async def set_main_menu(bot: Bot) -> None:
    # Собираем список команд, которые будут показаны в интерфейсе Telegram.
    commands = [
        # Добавляем команду запуска бота.
        BotCommand(command="start", description="Запустить бота и открыть меню"),
        # Добавляем команду справки.
        BotCommand(command="help", description="Показать список команд"),
        # Добавляем команду погоды.
        BotCommand(command="weather", description="Показать прогноз погоды"),
    ]

    # Отправляем список команд в Telegram, чтобы они появились у пользователя в меню.
    await bot.set_my_commands(commands)