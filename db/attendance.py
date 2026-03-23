from typing import Dict, List
from datetime import date
from .base import get_connection


def save_attendance(
    class_name: str, att_date: date, teacher_id: int, status_map: Dict[int, str]
):
    """
    status_map: {student_id: 'present' or 'absent'}
    """
    conn = get_connection()
    cur = conn.cursor()

    for student_id, status in status_map.items():
        cur.execute(
            """
            INSERT INTO attendance (student_id, class, date, status, teacher_id)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE status = VALUES(status), teacher_id = VALUES(teacher_id)
        """,
            (student_id, class_name, att_date, status, teacher_id),
        )

    conn.commit()
    cur.close()
    conn.close()


def get_attendance_for_student(student_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT date, status
        FROM attendance
        WHERE student_id = %s
        ORDER BY date DESC
    """,
        (student_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_attendance_summary(student_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) AS present_days,
            SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) AS absent_days
        FROM attendance
        WHERE student_id = %s
    """,
        (student_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    present = row[0] or 0
    absent = row[1] or 0
    total = present + absent
    percent = (present / total * 100) if total > 0 else 0
    return {
        "present": present,
        "absent": absent,
        "total": total,
        "percent": round(percent, 2),
    }


def get_attendance_for_class_date(class_name: str, att_date: date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s.full_name, s.roll_no, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE a.class = %s AND a.date = %s
        ORDER BY s.roll_no
    """,
        (class_name, att_date),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
