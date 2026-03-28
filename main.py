# Импортируем asyncio, чтобы корректно запускать асинхронную функцию main.
import asyncio
# Импортируем logging, чтобы видеть служебные сообщения и проще искать ошибки.
import logging

# Импортируем класс Bot для создания объекта Telegram-бота.
from aiogram import Bot
# Импортируем класс Dispatcher для регистрации и обработки входящих событий.
from aiogram import Dispatcher
# Импортируем класс DefaultBotProperties, чтобы задать общие настройки для всех сообщений бота.
from aiogram.client.default import DefaultBotProperties
# Импортируем ParseMode, чтобы включить HTML-разметку в сообщениях.
from aiogram.enums import ParseMode

# Импортируем функцию, которая зарегистрирует команды бота в Telegram.
from app.bot_commands import set_main_menu
# Импортируем настройки из файла конфигурации.
from app.config import settings
# Импортируем роутер с обработчиками команд и сообщений.
from app.handlers.common import router as common_router


# Создаем асинхронную функцию main, которая будет точкой входа в приложение.
async def main() -> None:
    # Настраиваем красивый и понятный вывод логов в терминал.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    # Создаем объект бота и сразу включаем HTML-разметку по умолчанию.
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Создаем диспетчер, который будет принимать и распределять все обновления.
    dp = Dispatcher()

    # Подключаем роутер с нашими командами и текстовыми обработчиками.
    dp.include_router(common_router)

    # Сбрасываем возможный webhook и очищаем старые накопившиеся обновления перед polling-режимом.
    await bot.delete_webhook(drop_pending_updates=True)

    # Регистрируем список команд, чтобы они отображались в меню Telegram.
    await set_main_menu(bot)

    # Запускаем бота в режиме polling и начинаем слушать новые сообщения.
    await dp.start_polling(bot)


# Проверяем, что файл запущен напрямую, а не импортирован как модуль.
if __name__ == "__main__":
    # Пытаемся аккуратно запустить бота.
    try:
        # Запускаем асинхронную функцию main через встроенный цикл событий.
        asyncio.run(main())
    # Перехватываем ручную остановку из терминала сочетанием Ctrl + C.
    except KeyboardInterrupt:
        # Печатаем понятное сообщение об остановке.
        print("Бот остановлен вручную.")