import mysql.connector
from database import Database

class BinanceDatabase(Database):
    def get_ticker(self, symbol):
        """Get the latest ticker data for a given symbol."""
        self.cursor.execute(
            "SELECT * FROM bnc_ticker_24 WHERE symbol = %s ORDER BY timestamp DESC LIMIT 1",
            (symbol,),
        )
        return self.cursor.fetchone()

    def insert_or_update_ticker(self, symbol, price_change_percent, last_price, high_price, low_price, volume):
        """Insert or update ticker data in the database."""
        self.cursor.execute(
            """
            INSERT INTO bnc_ticker_24 (symbol, priceChangePercent, lastPrice, highPrice, LowPrice, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            priceChangePercent = VALUES(priceChangePercent),
            lastPrice = VALUES(lastPrice),
            highPrice = VALUES(highPrice),
            lowPrice = VALUES(lowPrice),
            volume = VALUES(volume)
            """,
            (symbol, price_change_percent, last_price, high_price, low_price, volume),
        )
        self.conn.commit()

    def get_alert(self, symbol):
        """Retrieve price alert data for a given symbol."""
        # self.conn.commit()
        self.cursor.execute("SELECT * FROM bnc_alerts WHERE symbol = %s LIMIT 1", (symbol,))
        return self.cursor.fetchone()
