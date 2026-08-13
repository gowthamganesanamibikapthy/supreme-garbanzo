import hashlib
import datetime

class AuthenticationService:
    def __init__(self, db_manager):
        self.db = db_manager

    def hash_credentials(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def process_registration(self, username: str, password_raw: str) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                return False  # Account baseline profile duplicate mismatch
            
            now = datetime.datetime.now().isoformat()
            p_hash = self.hash_credentials(password_raw)
            cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, p_hash, now))
            cursor.execute("INSERT INTO configurations VALUES (?, 'CYBER_HUD')", (username,))
            conn.commit()
            return True

    def verify_login(self, username: str, password_raw: str) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row and row[0] == self.hash_credentials(password_raw):
                return True
            return False
