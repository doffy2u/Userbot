import sqlite3
import time

DB_NAME = "yapper.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
    
        message_id INTEGER PRIMARY KEY,
    
        chat_id INTEGER,
    
        sender_id INTEGER,
        sender_name TEXT,
        username TEXT,
    
        message_type TEXT,
    
        text TEXT,
    
        file_id TEXT,
    
        sent_time INTEGER
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
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ai_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        memory_key TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()
def save_message(
    message_id,
    chat_id,
    sender_id,
    sender_name,
    username,
    message_type,
    text="",
    file_id=""
):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO messages
        (
            message_id,
            chat_id,
            sender_id,
            sender_name,
            username,
            message_type,
            text,
            file_id,
            sent_time
        )
        VALUES (?,?,?,?,?,?,?,?,?)
        """,
        (
            message_id,
            chat_id,
            sender_id,
            sender_name,
            username,
            message_type,
            text,
            file_id,
            int(time.time())
        )
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

    cutoff = int(time.time()) - (5 * 24 * 60 * 60)

    cur.execute(
        """
        DELETE FROM messages
        WHERE sent_time < ?
        """,
        (cutoff,)
    )

    cur.execute("""
        DELETE FROM events
        WHERE timestamp < datetime('now', '-5 days')
    """)

    conn.commit()
    conn.close()

    # Run AFTER closing the first connection
    cleanup_ai_memory()
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

def set_afk(chat_id, user_id, name, reason):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO afk
        (chat_id,user_id,name,reason,start_time)
        VALUES(?,?,?,?,?)
        """,
        (
            chat_id,
            user_id,
            name,
            reason,
            int(time.time())
        )
    )

    conn.commit()
    conn.close()


def remove_afk(chat_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM afk
        WHERE chat_id=? AND user_id=?
        """,
        (chat_id, user_id)
    )

    conn.commit()
    conn.close()


def get_afk(chat_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM afk
        WHERE chat_id=? AND user_id=?
        """,
        (chat_id, user_id)
    )

    row = cur.fetchone()

    conn.close()

    return row
def get_all_afk(chat_id):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM afk
        WHERE chat_id=?
        """,
        (chat_id,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows
def save_ai_message(memory_key, role, content):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO ai_memory
        (memory_key, role, content, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (
            memory_key,
            role,
            content,
            int(time.time())
        )
    )

    conn.commit()
    conn.close()


def get_ai_history(memory_key, limit=20):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT role, content
        FROM ai_memory
        WHERE memory_key=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (memory_key, limit)
    )

    rows = cur.fetchall()

    conn.close()

    return rows[::-1]


def cleanup_ai_memory():
    cutoff = int(time.time()) - (5 * 24 * 60 * 60)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM ai_memory
        WHERE timestamp < ?
        """,
        (cutoff,)
    )

    conn.commit()
    conn.close()

