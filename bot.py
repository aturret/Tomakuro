"""Tomakuro - A minimalist Telegram pomodoro timer bot."""

import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from constants import BTN_SETTINGS, BTN_START_CLOCK, BTN_STATUS, BTN_STOP
from handlers import (
    cb_add_time_pressed,
    cb_add_time_selected,
    cb_break_duration_selected,
    cb_cancel_timer,
    cb_duration_selected,
    cmd_start,
    handle_settings,
    handle_start_clock,
    handle_status,
    handle_stop,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("Set TELEGRAM_BOT_TOKEN environment variable.")
        return

    application = Application.builder().token(token).build()

    # /start command
    application.add_handler(CommandHandler("start", cmd_start))

    # Bottom keyboard text handlers
    application.add_handler(
        MessageHandler(filters.Text([BTN_START_CLOCK]), handle_start_clock)
    )
    application.add_handler(MessageHandler(filters.Text([BTN_STATUS]), handle_status))
    application.add_handler(MessageHandler(filters.Text([BTN_STOP]), handle_stop))
    application.add_handler(
        MessageHandler(filters.Text([BTN_SETTINGS]), handle_settings)
    )

    # Inline callback handlers
    application.add_handler(
        CallbackQueryHandler(cb_duration_selected, pattern=r"^(dur|sec)_\d+$")
    )
    application.add_handler(
        CallbackQueryHandler(cb_add_time_pressed, pattern="^add_time$")
    )
    application.add_handler(
        CallbackQueryHandler(cb_add_time_selected, pattern=r"^addtime_\d+$")
    )
    application.add_handler(
        CallbackQueryHandler(cb_cancel_timer, pattern="^cancel_timer$")
    )
    application.add_handler(
        CallbackQueryHandler(cb_break_duration_selected, pattern=r"^break_\d+$")
    )

    logger.info("Bot started.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
