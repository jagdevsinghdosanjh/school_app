from datetime import date
from .base import get_connection


def generate_receipt_no(student_id: int) -> str:
    return f"RCPT-{student_id}-{date.today().strftime('%Y%m%d')}"


def get_daily_collection(target_date: date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT SUM(amount)
        FROM fee_payments
        WHERE DATE(payment_date) = %s
    """,
        (target_date,),
    )
    total = cur.fetchone()[0] or 0
    cur.close()
    conn.close()
    return total


def get_monthly_collection(year: int, month: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT SUM(amount)
        FROM fee_payments
        WHERE YEAR(payment_date) = %s AND MONTH(payment_date) = %s
    """,
        (year, month),
    )
    total = cur.fetchone()[0] or 0
    cur.close()
    conn.close()
    return total


def get_all_payments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT student_id, amount, mode, payment_date, receipt_no
        FROM fee_payments
        ORDER BY payment_date DESC
    """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
