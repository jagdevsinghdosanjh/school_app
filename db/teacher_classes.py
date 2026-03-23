from typing import List, Dict
from .base import get_connection


def assign_class(teacher_id: int, cls: str, section: str, subject: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO teacher_classes (teacher_id, class, section, subject)
        VALUES (%s, %s, %s, %s)
    """,
        (teacher_id, cls, section, subject),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_classes_for_teacher(teacher_id: int) -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT class, section, subject
        FROM teacher_classes
        WHERE teacher_id = %s
        ORDER BY class, section
    """,
        (teacher_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [{"class": r[0], "section": r[1], "subject": r[2]} for r in rows]


def get_all_assignments() -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT tc.id, u.full_name, tc.class, tc.section, tc.subject
        FROM teacher_classes tc
        JOIN users u ON tc.teacher_id = u.id
        ORDER BY tc.class, tc.section
    """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "teacher": r[1],
            "class": r[2],
            "section": r[3],
            "subject": r[4],
        }
        for r in rows
    ]


def delete_assignment(assign_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM teacher_classes WHERE id=%s", (assign_id,))
    conn.commit()
    cur.close()
    conn.close()
