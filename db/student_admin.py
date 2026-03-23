from typing import List, Dict
from .base import get_connection


def register_student(full_name: str, roll_no: str, cls: str, section: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO students (full_name, roll_no, class, section)
        VALUES (%s, %s, %s, %s)
    """,
        (full_name, roll_no, cls, section),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_all_students() -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, full_name, roll_no, class, section
        FROM students
        ORDER BY class, section, roll_no
    """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "full_name": r[1],
            "roll_no": r[2],
            "class": r[3],
            "section": r[4],
        }
        for r in rows
    ]


def promote_student(student_id: int, new_class: str, new_section: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE students
        SET class=%s, section=%s
        WHERE id=%s
    """,
        (new_class, new_section, student_id),
    )
    conn.commit()
    cur.close()
    conn.close()
