from typing import List, Dict
from .base import get_connection


def add_homework(
    teacher_id: int,
    cls: str,
    section: str,
    subject: str,
    title: str,
    description: str,
    due_date,
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO homework (teacher_id, class, section, subject, title, description, due_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
        (teacher_id, cls, section, subject, title, description, due_date),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_homework_for_class(cls: str, section: str) -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT subject, title, description, due_date, created_at
        FROM homework
        WHERE class=%s AND section=%s
        ORDER BY created_at DESC
    """,
        (cls, section),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "subject": r[0],
            "title": r[1],
            "description": r[2],
            "due_date": r[3],
            "created_at": r[4],
        }
        for r in rows
    ]
