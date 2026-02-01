import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import BOT_TOKEN, LOG_LEVEL
from scheduler import setup_scheduler

async def main():
    # Налаштування логування
    logging.basicConfig(
        level=LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logging.info("🤖 Запуск Telegram-бота для графіків відключень...")
    
    # Ініціалізація бота
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    
    # Встановлення меню команд
    commands = [
        BotCommand(command="start", description="Інформація про бота"),
    ]
    await bot.set_my_commands(commands)
    
    # Запуск планувальника
    setup_scheduler(bot)
    
    logging.info("✅ Бот запущено і готовий до роботи!")
    
    # Простий polling (без обробки команд, т.к. бот тільки публікує)
    try:
        await asyncio.sleep(10**10)  # Бесконечне очікування
    except KeyboardInterrupt:
        logging.info("⛔ Бот зупинено")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Програма переривана користувачем")