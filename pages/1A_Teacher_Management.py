import streamlit as st
import bcrypt
from auth.auth_manager import is_authenticated, has_role
from db.base import get_connection

# -------------------------
# ACCESS CONTROL
# -------------------------
if not is_authenticated():
    st.error("Login required")
    st.stop()

if not has_role("admin"):
    st.error("Access denied")
    st.stop()

st.title("Teacher Management")
st.caption("Create teachers, assign roles, and manage teacher accounts.")


# -------------------------
# DB HELPERS
# -------------------------
def create_teacher_user(username, password, full_name, email):
    conn = get_connection()
    cur = conn.cursor()

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # Create user
    cur.execute(
        """
        INSERT INTO users (username, password_hash, full_name, email, is_active)
        VALUES (%s, %s, %s, %s, 1)
    """,
        (username, hashed, full_name, email),
    )
    user_id = cur.lastrowid

    # Assign teacher role
    cur.execute(
        """
        INSERT INTO user_roles (user_id, role_id)
        VALUES (%s, (SELECT id FROM roles WHERE name='teacher'))
    """,
        (user_id,),
    )

    conn.commit()
    cur.close()
    conn.close()
    return user_id


def get_all_teachers():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT u.id, u.username, u.full_name, u.email, u.is_active
        FROM users u
        JOIN user_roles ur ON ur.user_id = u.id
        JOIN roles r ON r.id = ur.role_id
        WHERE r.name = 'teacher'
        ORDER BY u.id
    """
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def set_active_status(user_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_active=%s WHERE id=%s", (status, user_id))
    conn.commit()
    cur.close()
    conn.close()


# -------------------------
# CREATE TEACHER FORM
# -------------------------
st.subheader("Create New Teacher")

with st.form("create_teacher_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")

    submitted = st.form_submit_button("Create Teacher")

    if submitted:
        if not username or not password:
            st.error("Username and password are required.")
        else:
            try:
                teacher_id = create_teacher_user(username, password, full_name, email)
                st.success(
                    f"Teacher '{username}' created successfully (ID: {teacher_id})."
                )
            except Exception as e:
                st.error(f"Error creating teacher: {e}")

st.markdown("---")

# -------------------------
# TEACHER LIST
# -------------------------
st.subheader("All Teachers")

teachers = get_all_teachers()

for t in teachers:
    with st.expander(f"{t['username']} — {t['full_name']}"):
        st.write(f"**Email:** {t['email']}")
        st.write(f"**Active:** {'Yes' if t['is_active'] else 'No'}")

        if t["is_active"]:
            if st.button("Deactivate", key=f"deact_{t['id']}"):
                set_active_status(t["id"], 0)
                st.warning("Teacher deactivated.")
                st.experimental_rerun()
        else:
            if st.button("Activate", key=f"act_{t['id']}"):
                set_active_status(t["id"], 1)
                st.success("Teacher activated.")
                st.experimental_rerun()
