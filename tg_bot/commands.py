from tg_logger import *
from telegram.ext import (
    ContextTypes,
)
from telegram import ForceReply, Update


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )
        await send_log(
            f"Session started by {user.mention_html()}. ID: {user['id']+er}", context
        )
    except Exception as e:
        await send_exception_log(str(e), context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # await update.message.reply_text(update.message.text)
    await update.message.reply_text(
        "Send /search command to find a product on Revolico.com"
    )


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    query = update.message.text.split(' ')[1]
    if not query:
        await update.message.reply_text("Por favor, especifique una búsqueda")
        return
    await send_log(message=f'Query <pre>{query}</pre> executed by {user.mention_html()}',context=context)
    await update.message.reply_text('Buscando...')
    return
