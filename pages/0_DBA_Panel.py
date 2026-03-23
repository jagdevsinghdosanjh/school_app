import streamlit as st
import mysql.connector
import bcrypt

from auth.auth_manager import is_authenticated, has_role

st.set_page_config(page_title="DBA Panel", layout="centered")


def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
    )


def create_admin_user(username: str, password: str, full_name: str, email: str):
    conn = get_connection()
    cur = conn.cursor()

    # hash password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # create user
    cur.execute(
        """
        INSERT INTO users (username, password_hash, full_name, email, is_active)
        VALUES (%s, %s, %s, %s, 1)
        """,
        (username, hashed, full_name, email),
    )
    user_id = cur.lastrowid

    # assign admin role
    cur.execute(
        """
        INSERT INTO user_roles (user_id, role_id)
        VALUES (%s, (SELECT id FROM roles WHERE name='admin'))
        """,
        (user_id,),
    )

    conn.commit()
    cur.close()
    conn.close()
    return user_id


# ------------------ ACCESS CONTROL ------------------
if not is_authenticated() or not has_role("dba"):
    st.error("Access denied. Only Database Administrator (DBA) can access this page.")
    st.stop()

# ------------------ UI ------------------
st.title("Database Administrator Panel")
st.caption("Only DBA can create school_app admin accounts.")

st.subheader("Create New Admin User")

with st.form("create_admin_form"):
    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")

    submitted = st.form_submit_button("Create Admin")

    if submitted:
        if not username or not password:
            st.error("Username and password are required.")
        else:
            try:
                user_id = create_admin_user(username, password, full_name, email)
                st.success(
                    f"Admin user '{username}' created successfully (ID: {user_id})."
                )
            except Exception as e:
                st.error(f"Error creating admin: {e}")
