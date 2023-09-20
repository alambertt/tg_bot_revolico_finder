from telegram import ForceReply, Update
from telegram.ext import ContextTypes

from web_scrap import scraper

from .constants import TEXT_EMPTY
from .helpers import error_handler
from .tg_logger import send_log, send_exception_log


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        await update.message.reply_html(
            rf"HOLA {user.mention_html()}! Para consultar el funcionamiento de este bot envíe el comando /help",
            # reply_markup=ForceReply(selective=True),
        )
        await send_log(
            f"Session started by {user.mention_html()}. ID: {user['id']}", context
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
    try:
        long_text = 40
        user = update.effective_user
        text_msg = update.message.text
        query = text_msg.split("/search")[1]
        await send_log(
            message=f"Query <pre>{query}</pre> executed by {user.mention_html()}",
            context=context,
        )
        await update.message.reply_text("Buscando...")
        items = scraper.find(search_text=query)
        msg = "\n\n".join(
            f'{i+1}. <a href="{item["link"]}">{item["text"][:long_text]+"..." if len(item["text"]) > long_text else item["text"]}</a>. Publicado <i>{item["date"]}</i> en {item["location"]}'
            for i, item in enumerate(items)
        )
        await update.message.reply_html(msg)
        return
    except IndexError as e:
        await update.message.reply_html(TEXT_EMPTY)
        return
    except Exception as e:
        await send_exception_log("Search Command error: " + str(e), context)
        return
