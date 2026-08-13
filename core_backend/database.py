import sqlite3

class CloudDatabase:
    def __init__(self, db_path="aura_production.db"):
        self.db_path = db_path
        self.init_schema()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_schema(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # User Database Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            # Multitenant Task Management Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    task_text TEXT NOT NULL,
                    status TEXT DEFAULT 'ACTIVE',
                    created_at TEXT NOT NULL
                )
            """)
            # Configuration Management State Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS configurations (
                    username TEXT PRIMARY KEY,
                    active_skin TEXT DEFAULT 'CYBER_HUD'
                )
            """)
            conn.commit()
    