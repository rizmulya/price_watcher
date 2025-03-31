import asyncio
from telegram import listen_telegram, heartbeat
from binance.watch import watch_binance
from logger import setup_logger

logger = setup_logger("main")

async def main():
    logger.info("Bot started...")
    await asyncio.gather(
        listen_telegram(),
        heartbeat(),
        watch_binance(),
    )

if __name__ == "__main__":
    asyncio.run(main())