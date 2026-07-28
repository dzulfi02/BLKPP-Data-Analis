import sqlite3
import pandas as pd

DATABASE_NAME = "database/history.db"


def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            evaluation_type TEXT NOT NULL,
            overall_score TEXT,
            result TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_result(input_text, evaluation_type, overall_score, result):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO evaluations (
            input_text,
            evaluation_type,
            overall_score,
            result
        )
        VALUES (?, ?, ?, ?)
    """, (
        input_text,
        evaluation_type,
        overall_score,
        result
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            evaluation_type,
            overall_score,
            created_at
        FROM evaluations
        ORDER BY created_at DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data

def get_history():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            evaluation_type,
            overall_score,
            created_at
        FROM evaluations
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
def export_history():

    conn = sqlite3.connect(DATABASE_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM evaluations",
        conn
    )

    conn.close()

    return df