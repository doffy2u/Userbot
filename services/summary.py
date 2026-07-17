import sqlite3
from storage.database import get_last_briefing

DB_NAME = "yapper.db"


def get_summary(chat_id, user_id):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    last = get_last_briefing(chat_id, user_id)

    if last:

        cur.execute(
            """
            SELECT sender, message
            FROM messages
            WHERE chat_id = ?
            AND timestamp > ?
            ORDER BY id ASC
            """,
            (chat_id, last)
        )

    else:

        cur.execute(
            """
            SELECT sender, message
            FROM messages
            WHERE chat_id = ?
            ORDER BY id DESC
            LIMIT 100
            """,
            (chat_id,)
        )

    rows = cur.fetchall()

    conn.close()

    return rows
