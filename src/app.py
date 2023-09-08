import os
import logging
from dotenv import load_dotenv

from telegram.ext import ApplicationBuilder, Application, CommandHandler, CallbackQueryHandler, MessageHandler
from telegram import Update

from src.handlers.command_handlers import main_handler, button, timestamp_handler
from src.config import notifications
from src.reminder import reminder

load_dotenv()
TOKEN = os.environ.get("TELEGRAM_TOKEN")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename="log")


def init_reminders(app: Application) -> None:
    j = app.job_queue
    for notification_time in notifications:
        j.run_daily(reminder, days=(0, 1, 2, 3, 4, 5, 6), time=notification_time)


def init_app() -> Application:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", main_handler))
    app.add_handler(CommandHandler("record", main_handler))
    app.add_handler(CommandHandler("timestamp", timestamp_handler))
    app.add_handler(CommandHandler("stats", stats_handler))
    app.add_handler(MessageHandler(None, main_handler))
    app.add_handler(CallbackQueryHandler(button))
    init_reminders(app)
    return app


if __name__ == '__main__':
    application = init_app()
    logging.info("Starting application")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
