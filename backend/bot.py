"""
ScamCheck KZ - Telegram Bot Implementation
Run this script with TELEGRAM_BOT_TOKEN to launch the Telegram Bot.
Supports text messages, photos/screenshots, and language selection (RU/KZ).
"""

import os
import sys
import logging
from app.detector import detector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ScamCheckBot")

# Language preferences per user_id
user_langs = {}

def process_bot_message(user_id: int, text: str) -> str:
    """Core text message handler logic for Telegram Bot."""
    lang = user_langs.get(user_id, "ru")
    
    if text in ["/start", "/help"]:
        if lang == "kz":
            return (
                "🤖 *ScamCheck KZ Ботқа қош келдіңіз!*\n\n"
                "Маған мессенджерден кез келген күмәнді хабарламаны немесе скриншотты бағыттаңыз. "
                "Мен оны алаяқтыққа тексеріп беремін.\n\n"
                "Тілді ауыстыру үшін: /ru немесе /kz теріңіз."
            )
        else:
            return (
                "🤖 *Добро пожаловать в ScamCheck KZ Bot!*\n\n"
                "Перешлите мне любое подозрительное сообщение или скриншот из чата. "
                "Я мгновенно проверю его на признаки мошенничества и дам рекомендации.\n\n"
                "Для смены языка используйте: /ru или /kz."
            )

    if text == "/kz":
        user_langs[user_id] = "kz"
        return "✅ Тіл қазақшаға ауыстырылды."
    elif text == "/ru":
        user_langs[user_id] = "ru"
        return "✅ Язык переключён на русский."

    res = detector.analyze(text, lang=lang)
    score = res["score"]
    level = res["level"]
    scheme_name = res["scheme_name"]
    triggers = res["triggers"]
    recommendations = res["recommendations"]

    if lang == "kz":
        if level == "risk":
            status_hdr = f"🚨 *ЖОҒАРЫ АЛАЯҚТЫҚ ҚАУПІ ({score}% risk)*"
        elif level == "warn":
            status_hdr = f"⚠️ *КҮМӘНДІ ХАБАРЛАМА ({score}% risk)*"
        else:
            status_hdr = f"✅ *ҚАУІПСІЗ ХАБАРЛАМА ({score}% risk)*"

        msg = f"{status_hdr}\n\n"
        if scheme_name:
            msg += f"📌 *Схема:* {scheme_name}\n"
        if triggers:
            msg += f"🔍 *Анықталған белгілер:* {', '.join(triggers)}\n"

        msg += "\n💡 *Кеңес:* \n"
        for rec in recommendations:
            msg += f"• {rec}\n"

        return msg
    else:
        if level == "risk":
            status_hdr = f"🚨 *ВЫСОКИЙ РИСК МОШЕННИЧЕСТВА ({score}% risk)*"
        elif level == "warn":
            status_hdr = f"⚠️ *ПОДОЗРИТЕЛЬНОЕ СООБЩЕНИЕ ({score}% risk)*"
        else:
            status_hdr = f"✅ *БЕЗОПАСНОЕ СООБЩЕНИЕ ({score}% risk)*"

        msg = f"{status_hdr}\n\n"
        if scheme_name:
            msg += f"📌 *Схема:* {scheme_name}\n"
        if triggers:
            msg += f"🔍 *Обнаруженные маркеры:* {', '.join(triggers)}\n"

        msg += "\n💡 *Рекомендации:* \n"
        for rec in recommendations:
            msg += f"• {rec}\n"

        return msg


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.info("TELEGRAM_BOT_TOKEN environment variable not set.")
        logger.info("Running standalone bot handler self-test...")
        
        sample_msg = "Здравствуйте, это служба безопасности банка. На вас оформляют кредит, срочно переведите деньги на безопасный счёт!"
        response = process_bot_message(12345, sample_msg)
        print("--- Bot Sample Output ---")
        print(response)
        return

    try:
        from aiogram import Bot, Dispatcher, types
        from aiogram.enums import ParseMode
        import asyncio

        bot = Bot(token=token, parse_mode=ParseMode.MARKDOWN)
        dp = Dispatcher()

        @dp.message()
        async def handle_msg(message: types.Message):
            txt = message.text or message.caption or ""
            reply = process_bot_message(message.from_user.id, txt)
            await message.reply(reply)

        asyncio.run(dp.start_polling(bot))

    except ImportError:
        logger.error("aiogram is not installed. Install it with: pip install aiogram")


if __name__ == "__main__":
    main()
