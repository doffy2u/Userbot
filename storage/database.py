import sqlite3

DB_NAME = "yapper.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        sender TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        event_type TEXT,
        user TEXT,
        details TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS briefings (
        chat_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        last_checked DATETIME,
        PRIMARY KEY(chat_id, user_id)
    )
    """)

    conn.commit()
    conn.close()


def save_message(chat_id, sender, message):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO messages(chat_id, sender, message)
        VALUES (?, ?, ?)
        """,
        (chat_id, sender, message)
    )

    conn.commit()
    conn.close()
    cleanup_old_messages()
def save_event(chat_id, event_type, user="", details=""):
    
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
    
        cur.execute(
            """
            INSERT INTO events(chat_id,event_type,user,details)
            VALUES(?,?,?,?)
            """,
            (
                chat_id,
                event_type,
                user,
                details
            )
        )
    
        conn.commit()
        conn.close()
def get_last_briefing(chat_id, user_id):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT last_checked
        FROM briefings
        WHERE chat_id = ?
        AND user_id = ?
        """,
        (chat_id, user_id)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


def update_last_briefing(chat_id, user_id):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO briefings(chat_id,user_id,last_checked)
        VALUES(?,?,CURRENT_TIMESTAMP)

        ON CONFLICT(chat_id,user_id)

        DO UPDATE SET
        last_checked=CURRENT_TIMESTAMP
        """,
        (chat_id, user_id)
    )

    conn.commit()
    conn.close()
def cleanup_old_messages():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM messages
        WHERE timestamp < datetime('now', '-5 days')
    """)

    cur.execute("""
        DELETE FROM events
        WHERE timestamp < datetime('now', '-5 days')
    """)
    

    conn.commit()
    conn.close()
def get_recent_events(chat_id, since):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM events
        WHERE chat_id=?
        AND timestamp > ?
        ORDER BY timestamp DESC
        """,
        (
            chat_id,
            since
        )
    )

    rows = cur.fetchall()

    conn.close()

    return rows
