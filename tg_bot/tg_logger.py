from telegram.ext import ContextTypes
from .constants import CHANNEL_LOGS_ID
from telegram.constants import ParseMode


async def send_exception_log(msg, context):
    await send_log(context=context, message=f"An error ocurred: \n\n <pre>{msg}</pre>")


async def send_log(message: str, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHANNEL_LOGS_ID, text=message, parse_mode=ParseMode.HTML
    )
