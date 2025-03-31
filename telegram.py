import re
import asyncio
import aiohttp
import inspect

from database import Database
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from logger import setup_logger

"""
TELEGRAM BOT
"""

logger = setup_logger("telegram_bot")

URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
OFFSET = 0


"""
MESSAGE LISTENER
"""
async def listen_telegram():
    global OFFSET
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                logger.info("Listening for new messages...")
                async with session.get(f"{URL}/getUpdates", params={"offset": OFFSET, "timeout": 30}) as response:
                    data = await response.json()
                    
                    if data["ok"] and data["result"]:
                        for update in data["result"]:
                            OFFSET = update["update_id"] + 1
                            message = update.get("edited_message", update.get("message"))
                            if message:
                                chat_id = message["chat"]["id"]
                                text = message.get("text", "")
                                logger.info(f"Received message from {chat_id}: {text}")
                                await process_message(chat_id, text)
            except aiohttp.ClientError as e:
                logger.error(f"Error getting updates: {e}", exc_info=True)

            await asyncio.sleep(2)

# Process the message
async def process_message(chat_id, text):
    db = Database()
    text = text.split()[0] if text else ""
    response = db.get_tele_response(text, chat_id)

    if response:
        if response.get("receiver") and response["receiver"] != chat_id:
            return

        trigger_type = response["trigger_type"]
        trigger_text = response["trigger_text"]

        if trigger_type == "case-sensitive":
            matched = text == trigger_text
        elif trigger_type == "case-insensitive":
            matched = text.lower() == trigger_text.lower()
        elif trigger_type == "regex":
            matched = re.match(r"^" + re.escape(trigger_text) + r"\b", text) is not None
        else:
            matched = False
        
        if not matched:
            return

        if response["response_type"] == "text":
            await send_telegram_message(response["response_text"], chat_id)
        elif response["response_type"] == "func":
            func_name = response["response_func"]
            if func_name in globals():
                func = globals()[func_name]
                await call_function_safely(func, chat_id, text)
            else:
                logger.warning(f"Function {func_name} not found.")
                await send_telegram_message("Function not found.", chat_id)

# Utils
async def call_function_safely(func, chat_id, text):
    sig = inspect.signature(func)
    param_count = len(sig.parameters)

    if param_count == 2:
        return await func(chat_id, text)
    elif param_count == 1:
        return await func(chat_id)
    elif param_count == 0:
        return await func()
    else:
        return "Invalid function signature."

# Example function
async def show_tele_id(chat_id, text):
    await send_telegram_message(f"{chat_id}", chat_id)

"""
MESSAGE SENDER
"""
async def send_telegram_message(text, chat_id=None):
    chat_id = chat_id or TELEGRAM_CHAT_ID
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{URL}/sendMessage", data=data) as response:
                await response.json()
                logger.info(f"Message sent to {chat_id}: {text}")
        except aiohttp.ClientError as e:
            logger.error(f"Telegram Error: {e}", exc_info=True)

async def heartbeat():
    """Send 'Bot is alive' every 4 hours."""
    while True:
        await send_telegram_message("Bot is alive")
        await asyncio.sleep(14400) # 4 hours