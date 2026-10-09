"""Telegram bot: a subscriber forwards a suspicious SMS and gets a verdict in their language.

Runs inside the API process (long polling) so every report also shows up live on the dashboard.
"""
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

log = logging.getLogger("qalxan.bot")

WELCOME = (
    "🛡 Qalxan\n\n"
    "AZ: Şübhəli SMS-i mənə göndərin və ya yönləndirin, fırıldaq olub-olmadığını deyim.\n"
    "RU: Перешлите мне подозрительное SMS, и я скажу, мошенничество ли это.\n"
    "EN: Forward me a suspicious SMS and I'll tell you if it's a scam."
)
ICON = {"scam": "🚨", "suspicious": "⚠️", "safe": "✅"}
FOOTER = {"az": "Operatorun fırıldaq şöbəsinə ötürüldü.", "ru": "Передано в антифрод-отдел оператора.",
          "en": "Forwarded to the operator's anti-fraud team."}


def pick_lang(result: dict, user_lang: str | None) -> str:
    if user_lang and user_lang[:2] in ("az", "ru", "en"):
        return user_lang[:2]
    return result.get("lang") or "en"


def format_reply(result: dict, lang: str) -> str:
    text = f"{ICON[result['verdict']]} {result['explanation'][lang]}"
    if result["verdict"] != "safe":
        text += f"\n\n{FOOTER[lang]}"
    return text


async def run_bot(process):
    """`process(text, sender)` is the API's coroutine that analyzes and broadcasts a report."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        log.info("TELEGRAM_BOT_TOKEN not set, bot disabled")
        return
    bot = Bot(token=token)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(WELCOME)

    @dp.message()
    async def check(message: Message):
        text = message.text or message.caption
        if not text:
            await message.answer("Send the SMS as text, please / Mətni göndərin / Пришлите текст сообщения.")
            return
        user = message.from_user
        result = await process(text, f"Telegram @{user.username}" if user and user.username else "Telegram")
        lang = pick_lang(result, user.language_code if user else None)
        await message.answer(format_reply(result, lang))

    try:
        await dp.start_polling(bot, handle_signals=False)
    except Exception as e:
        log.error(f"bot stopped: {e}")
