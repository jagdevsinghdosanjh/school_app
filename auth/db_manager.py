import mysql.connector
from typing import Optional, Dict, List
import streamlit as st


def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
    )


def get_user_by_username(username: str) -> Optional[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, username, password_hash, full_name, email, is_active
        FROM users
        WHERE username = %s
    """,
        (username,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {
            "id": row[0],
            "username": row[1],
            "password_hash": row[2],
            "full_name": row[3],
            "email": row[4],
            "is_active": bool(row[5]),
        }
    return None


def get_roles_for_user(user_id: int) -> List[str]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT r.name
        FROM roles r
        JOIN user_roles ur ON r.id = ur.role_id
        WHERE ur.user_id = %s
    """,
        (user_id,),
    )
    roles = [r[0] for r in cur.fetchall()]
    cur.close()
    conn.close()
    return roles
