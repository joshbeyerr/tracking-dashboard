import sqlite3

DB_FILE = 'tokens.db'


def table_exists(table_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def create_table():
    if not table_exists('ups_tokens'):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ups_tokens (
                id INTEGER PRIMARY KEY,
                access_token TEXT NOT NULL,
                issued_at INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()


def save_ups_tokens(access_token, issued_at):

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO ups_tokens (access_token, issued_at)
        VALUES (?, ?)
    ''', (access_token, issued_at))

    conn.commit()
    conn.close()


def get_ups_tokens():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ups_tokens ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'access_token': row[1],
            'issued_at': row[2]
        }
    return None


def delete_ups_tokens():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ups_tokens')
    conn.commit()
    conn.close()
