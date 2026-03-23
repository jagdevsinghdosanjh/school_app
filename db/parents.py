from typing import List, Dict
from .base import get_connection


def get_parent_by_user_id(user_id: int) -> Dict:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, full_name, email, phone
        FROM parents
        WHERE user_id = %s
    """,
        (user_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return {
            "id": row[0],
            "full_name": row[1],
            "email": row[2],
            "phone": row[3],
        }
    return None


def get_children_for_parent(parent_id: int) -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s.id, s.full_name, s.roll_no, s.class, s.section
        FROM parent_children pc
        JOIN students s ON pc.student_id = s.id
        WHERE pc.parent_id = %s
        ORDER BY s.class, s.roll_no
    """,
        (parent_id,),
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
