import mysql.connector
import streamlit as st
from datetime import date


def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
    )


# ---------------------------------------------------------
# Initialize fees record for a new student
# ---------------------------------------------------------
def initialize_fee_record(student_id: int, total_fees: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO fees (student_id, total_fees, paid, last_payment_date)
        VALUES (%s, %s, 0, NULL)
    """,
        (student_id, total_fees),
    )

    conn.commit()
    cur.close()
    conn.close()


# ---------------------------------------------------------
# Record a fee payment
# ---------------------------------------------------------
def record_fee_payment(student_id: int, amount: int, mode: str):
    conn = get_connection()
    cur = conn.cursor()

    # Insert into fee_payments table
    cur.execute(
        """
        INSERT INTO fee_payments (student_id, amount, mode)
        VALUES (%s, %s, %s)
    """,
        (student_id, amount, mode),
    )

    # Update fees table
    cur.execute(
        """
        UPDATE fees
        SET paid = paid + %s,
            last_payment_date = CURRENT_TIMESTAMP
        WHERE student_id = %s
    """,
        (amount, student_id),
    )

    conn.commit()
    cur.close()
    conn.close()


# ---------------------------------------------------------
# Get fee status for a student
# ---------------------------------------------------------
def get_fee_status(student_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT total_fees, paid, due, last_payment_date
        FROM fees
        WHERE student_id = %s
    """,
        (student_id,),
    )

    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return {
            "total_fees": row[0],
            "paid": row[1],
            "due": row[2],
            "last_payment_date": row[3],
        }
    return None


# ---------------------------------------------------------
# Get payment history
# ---------------------------------------------------------
def get_payment_history(student_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT amount, mode, payment_date
        FROM fee_payments
        WHERE student_id = %s
        ORDER BY payment_date DESC
    """,
        (student_id,),
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return rows
