import sqlite3

DATABASE_NAME = 'database.db'

def crear_tabla():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                camera_id INTEGER,
                image_url TEXT
            )
        ''')
        conn.commit()

def agregar_mensaje(date, camera_id, image_url):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (date, camera_id, image_url) VALUES (?, ?, ?)", (date, camera_id, image_url))
        conn.commit()



