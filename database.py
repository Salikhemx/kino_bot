import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movies(
    code TEXT PRIMARY KEY,
    file_id TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings(
    id INTEGER PRIMARY KEY,
    channel TEXT
)
""")

conn.commit()


def add_movie(code, file_id):
    cursor.execute(
        "INSERT OR REPLACE INTO movies(code, file_id) VALUES(?, ?)",
        (code, file_id)
    )
    conn.commit()


def get_movie(code):
    cursor.execute(
        "SELECT file_id FROM movies WHERE code=?",
        (code,)
    )
    result = cursor.fetchone()

    if result:
        return result[0]

    return None


def set_channel(channel):
    cursor.execute(
        "INSERT OR REPLACE INTO settings(id, channel) VALUES(1, ?)",
        (channel,)
    )
    conn.commit()


def get_channel():
    cursor.execute("SELECT channel FROM settings WHERE id=1")
    result = cursor.fetchone()

    if result:
        return result[0]

    return None