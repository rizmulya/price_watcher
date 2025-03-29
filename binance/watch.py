import time
import aiohttp
import asyncio
import random

from binance.database import BinanceDatabase
from telegram import send_telegram_message
from config import USER_AGENT
from logger import setup_logger

"""
BNC PRICE WATCHER
"""

logger = setup_logger("binance_watcher")

async def watch_binance():
    """Binance Price Watcher (Async)"""
    url = "https://api.binance.com/api/v3/ticker/24hr"
    db = BinanceDatabase()
    
    price_change_threshold = db.get_option("bnc_price_change_perc_treshold") or 20.0

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                logger.info("Watching binance market price...")
                headers = {"User-Agent": USER_AGENT}
                async with session.get(url, headers=headers) as response:
                    if response.status == 429:
                        raise Exception("Rate limit hit. Try again later.")

                    data = await response.json()

                    for ticker in data:
                        symbol = ticker["symbol"]
                        price_change_percent = float(ticker["priceChangePercent"])
                        last_price = float(ticker["lastPrice"])
                        high_price = float(ticker["highPrice"])
                        low_price = float(ticker["lowPrice"])
                        volume = float(ticker["volume"])

                        # CHECK PRICE MOVEMENT
                        prev_data = db.get_ticker(symbol)

                        if price_change_percent > price_change_threshold:
                            if not prev_data or time.time() - prev_data["timestamp"].timestamp() > 86400:
                                message = (
                                    f"🚀 *ALERT: {symbol} is Pumping!* 🚀\n"
                                    f"📈 Price Change: {price_change_percent:.2f}%\n"
                                    f"💰 Last Price: {last_price}\n"
                                    f"📊 High: {high_price}\n"
                                    f"📉 Low: {low_price}\n"
                                    f"🔄 Volume: {volume}\n"
                                    f"{time.strftime('%Y-%m-%d %H:%M:%S')}"
                                )
                                await send_telegram_message(message)
                                db.insert_or_update_ticker(symbol, price_change_percent, last_price, high_price, low_price, volume)

                        # PRICE ALERTS
                        alert = db.get_alert(symbol)
                        if alert:
                            if last_price >= alert["higher"]:
                                await send_telegram_message(f"🚀 *ALERT: {symbol} hit HIGHER {alert['higher']}!* 🚀\n📈 Current Price: {last_price}")
                            elif last_price <= alert["lower"]:
                                await send_telegram_message(f"🔻 *ALERT: {symbol} dropped to LOWER {alert['lower']}!* 🔻\n📉 Current Price: {last_price}")
            except Exception as e:
                logger.error(f"Binance ERROR: {e}", exc_info=True)

            await asyncio.sleep(random.randint(60, 120))