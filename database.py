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