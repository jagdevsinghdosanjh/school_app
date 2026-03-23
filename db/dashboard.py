from .base import get_connection


def count_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM students")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count


def count_teachers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COUNT(*)
        FROM users u
        JOIN user_roles ur ON ur.user_id = u.id
        JOIN roles r ON r.id = ur.role_id
        WHERE r.name = 'teacher'
    """
    )
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count


def count_parents():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COUNT(*)
        FROM users u
        JOIN user_roles ur ON ur.user_id = u.id
        JOIN roles r ON r.id = ur.role_id
        WHERE r.name = 'parent'
    """
    )
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count


def count_office_staff():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COUNT(*)
        FROM users u
        JOIN user_roles ur ON ur.user_id = u.id
        JOIN roles r ON r.id = ur.role_id
        WHERE r.name = 'office'
    """
    )
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count


def count_homework():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM homework")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count


def count_attendance_entries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM attendance")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count


def total_fee_collected():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM fee_payments")
    total = cur.fetchone()[0] or 0
    cur.close()
    conn.close()
    return total
