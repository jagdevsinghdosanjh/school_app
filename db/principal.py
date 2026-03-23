from .base import get_connection


def class_strength():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT class, section, COUNT(*)
        FROM students
        GROUP BY class, section
        ORDER BY class, section
    """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def attendance_overview():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT class, 
               SUM(CASE WHEN status='present' THEN 1 ELSE 0 END),
               SUM(CASE WHEN status='absent' THEN 1 ELSE 0 END)
        FROM attendance
        GROUP BY class
        ORDER BY class
    """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def fee_overview():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT SUM(total_fees), SUM(paid), SUM(due)
        FROM fees
    """
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return {
        "total_fees": row[0] or 0,
        "paid": row[1] or 0,
        "due": row[2] or 0,
    }


def teacher_load():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT u.full_name, COUNT(tc.id)
        FROM users u
        JOIN user_roles ur ON ur.user_id = u.id
        JOIN roles r ON r.id = ur.role_id
        LEFT JOIN teacher_classes tc ON tc.teacher_id = u.id
        WHERE r.name='teacher'
        GROUP BY u.id
        ORDER BY u.full_name
    """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
