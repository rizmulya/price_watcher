import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

"""
GLOBAL DATABASE
"""

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def get_option(self, name):
        """Get Settings"""
        self.cursor.execute("SELECT value FROM options WHERE name = %s LIMIT 1", (name,))
        result = self.cursor.fetchone()
        return float(result["value"]) if result else None

    def get_tele_response(self, text, chat_id):
        """Get telegram auto response based on received text and user chat_id"""
        self.cursor.execute("""
            SELECT trigger_type, trigger_text, response_type, response_text, response_func 
            FROM tele_responses 
            WHERE (receiver IS NULL OR receiver = %s) AND trigger_text = %s
            LIMIT 1
        """, (chat_id, text))
        return self.cursor.fetchone()

    def __del__(self):
        """Tutup koneksi database saat objek dihapus"""
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
