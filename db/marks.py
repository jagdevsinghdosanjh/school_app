from typing import List, Dict
from .base import get_connection


def save_marks(entries: List[Dict]):
    """
    entries: list of dicts like:
    {
        "student_id": int,
        "subject": str,
        "exam": str,
        "marks_obtained": int,
        "max_marks": int,
        "teacher_id": int
    }
    """
    conn = get_connection()
    cur = conn.cursor()

    for e in entries:
        cur.execute(
            """
            INSERT INTO marks (student_id, subject, exam, marks_obtained, max_marks, teacher_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                marks_obtained = VALUES(marks_obtained),
                max_marks = VALUES(max_marks),
                teacher_id = VALUES(teacher_id)
        """,
            (
                e["student_id"],
                e["subject"],
                e["exam"],
                e["marks_obtained"],
                e.get("max_marks", 100),
                e["teacher_id"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()


def get_marks_for_student(student_id: int, exam: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT subject, marks_obtained, max_marks
        FROM marks
        WHERE student_id = %s AND exam = %s
        ORDER BY subject
    """,
        (student_id, exam),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_marks_for_class_exam(class_name: str, exam: str, subject: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s.full_name, s.roll_no, m.marks_obtained, m.max_marks
        FROM marks m
        JOIN students s ON m.student_id = s.id
        WHERE s.class = %s AND m.exam = %s AND m.subject = %s
        ORDER BY s.roll_no
    """,
        (class_name, exam, subject),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
