import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# =========================
# Kinolar
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS movies(
    code TEXT PRIMARY KEY,
    file_id TEXT
)
""")

# =========================
# Kanal
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings(
    id INTEGER PRIMARY KEY,
    channel TEXT
)
""")

# =========================
# Foydalanuvchilar
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY
)
""")

conn.commit()


# =========================
# KINOLAR
# =========================

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


def get_movies_count():
    cursor.execute(
        "SELECT COUNT(*) FROM movies"
    )
    return cursor.fetchone()[0]


# =========================
# KANAL
# =========================

def set_channel(channel):
    cursor.execute(
        "INSERT OR REPLACE INTO settings(id, channel) VALUES(1, ?)",
        (channel,)
    )
    conn.commit()


def get_channel():
    cursor.execute(
        "SELECT channel FROM settings WHERE id=1"
    )
    result = cursor.fetchone()

    if result:
        return result[0]

    return None


# =========================
# FOYDALANUVCHILAR
# =========================

def add_user(user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO users(user_id) VALUES(?)",
        (user_id,)
    )
    conn.commit()


def get_users_count():
    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )
    return cursor.fetchone()[0]


def get_all_users():
    cursor.execute(
        "SELECT user_id FROM users"
    )
    return cursor.fetchall()