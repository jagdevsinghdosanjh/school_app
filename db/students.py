from typing import Optional, Dict, List
from .base import get_connection


def register_student(
    full_name: str, roll_no: str, cls: str, section: str = None, parent_id: int = None
) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO students (full_name, roll_no, class, section, parent_id)
        VALUES (%s, %s, %s, %s, %s)
    """,
        (full_name, roll_no, cls, section, parent_id),
    )
    conn.commit()
    student_id = cur.lastrowid
    cur.close()
    conn.close()
    return student_id


def get_student_by_roll(roll_no: str) -> Optional[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, full_name, roll_no, class, section, parent_id
        FROM students
        WHERE roll_no = %s
    """,
        (roll_no,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {
            "id": row[0],
            "full_name": row[1],
            "roll_no": row[2],
            "class": row[3],
            "section": row[4],
            "parent_id": row[5],
        }
    return None


def get_student_by_id(student_id: int) -> Optional[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, full_name, roll_no, class, section, parent_id
        FROM students
        WHERE id = %s
    """,
        (student_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {
            "id": row[0],
            "full_name": row[1],
            "roll_no": row[2],
            "class": row[3],
            "section": row[4],
            "parent_id": row[5],
        }
    return None


def get_students_by_class(cls: str, section: str = None) -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    if section:
        cur.execute(
            """
            SELECT id, full_name, roll_no, class, section
            FROM students
            WHERE class = %s AND section = %s
            ORDER BY roll_no
        """,
            (cls, section),
        )
    else:
        cur.execute(
            """
            SELECT id, full_name, roll_no, class, section
            FROM students
            WHERE class = %s
            ORDER BY roll_no
        """,
            (cls,),
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
