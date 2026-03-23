import streamlit as st
import bcrypt
from auth.auth_manager import is_authenticated, has_role
from db.base import get_connection
from db.parents import create_parent_record, map_parent_to_child
from db.students import get_student_by_roll
from components.sidebar import show_sidebar

show_sidebar()


# -------------------------
# ACCESS CONTROL
# -------------------------
if not is_authenticated():
    st.error("Login required")
    st.stop()

if not has_role("admin"):
    st.error("Access denied")
    st.stop()

st.title("Parent Management")
st.caption("Create parent accounts and map them to their children.")

# -------------------------
# CREATE PARENT ACCOUNT
# -------------------------
st.subheader("Create Parent Account")

with st.form("create_parent_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")

    submitted = st.form_submit_button("Create Parent")

    if submitted:
        if not username or not password:
            st.error("Username and password are required.")
        else:
            try:
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

                # Assign parent role
                cur.execute(
                    """
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES (%s, (SELECT id FROM roles WHERE name='parent'))
                """,
                    (user_id,),
                )

                conn.commit()
                cur.close()
                conn.close()

                # Create parent record
                create_parent_record(user_id, full_name, email, phone)

                st.success(f"Parent '{username}' created successfully.")

            except Exception as e:
                st.error(f"Error creating parent: {e}")

st.markdown("---")

# -------------------------
# MAP PARENT TO CHILD
# -------------------------
st.subheader("Map Parent to Child")

parent_user_id = st.number_input("Parent User ID", min_value=1, step=1)
child_roll = st.text_input("Child Roll Number")

if st.button("Map Parent to Child"):
    student = get_student_by_roll(child_roll)
    if not student:
        st.error("Student not found.")
    else:
        from db.parents import get_parent_by_user_id

        parent = get_parent_by_user_id(parent_user_id)

        if not parent:
            st.error("Parent record not found.")
        else:
            map_parent_to_child(parent["id"], student["id"])
            st.success(
                f"Mapped parent to child {student['full_name']} ({student['roll_no']})."
            )
