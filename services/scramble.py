import sqlite3

DB_NAME = "yapper.db"


def signature(word: str) -> str:
    return "".join(sorted(word.lower()))


def lookup(scrambled: str):

    sig = signature(scrambled)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT word
        FROM scramble_dictionary
        WHERE signature = ?
        """,
        (sig,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


def learn(scrambled: str, word: str):

    sig = signature(scrambled)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO scramble_dictionary
        (
            signature,
            word
        )
        VALUES (?,?)
        """,
        (
            sig,
            word.lower()
        )
    )

    conn.commit()
    conn.close()

    print(
        f"Saved: {sig} -> {word}"
    )
