import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ContextTypes,
    ExtBot,
    TypeHandler,
)

from app.core.config import settings
from app.schemas.message import MessageBase

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    """
    Пользовательский класс CallbackContext, который делает
    user_data доступным для обновлений типа `WebhookUpdate`.
    """

    @classmethod
    def from_update(
        cls,
        update: object,
        app: Application,
    ) -> "CustomContext":
        if isinstance(update, MessageBase):
            return cls(application=app)
        return super().from_update(update, app)


async def start(update: Update) -> None:
    text = f"Ok!"
    await update.message.reply_html(text=text)


async def webhook_update(update: MessageBase, context: CustomContext) -> None:
    await context.bot.send_message(
        chat_id=update.user,
        text=update.message,
        parse_mode=ParseMode.HTML,
    )


context_types = ContextTypes(context=CustomContext)
application = (
    Application.builder()
    .token(settings.telegram_token)
    .updater(None)
    .context_types(context_types)
    .build()
)

application.add_handler(CommandHandler("start", start))
application.add_handler(TypeHandler(type=MessageBase, callback=webhook_update))


async def send_message(
    message: str,
):
    await application.update_queue.put(
        MessageBase(user=settings.admin_chat_id, message=message)
    )


async def start_telegram():
    await application.initialize()
    await application.bot.set_webhook(
        url=f"{settings.service_url}{settings.webhook_path}"
    )
    await application.start()


async def stop_telegram():
    await application.stop()
    await application.shutdown()
