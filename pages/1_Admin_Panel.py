import streamlit as st
import mysql.connector

from auth.auth_manager import is_authenticated, has_role
from components.sidebar import show_sidebar

show_sidebar()


st.set_page_config(page_title="Admin Panel", layout="wide")


# ------------------ DB CONNECTION ------------------
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
    )


# ------------------ DB HELPERS ------------------
def get_all_users():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT id, username, full_name, email, is_active FROM users ORDER BY id"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_roles(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT r.name 
        FROM roles r 
        JOIN user_roles ur ON ur.role_id = r.id
        WHERE ur.user_id = %s
    """,
        (user_id,),
    )
    roles = [r[0] for r in cur.fetchall()]
    cur.close()
    conn.close()
    return roles


def assign_role(user_id, role_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO user_roles (user_id, role_id)
        VALUES (%s, (SELECT id FROM roles WHERE name=%s))
        ON DUPLICATE KEY UPDATE role_id = role_id
    """,
        (user_id, role_name),
    )

    conn.commit()
    cur.close()
    conn.close()


def remove_role(user_id, role_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM user_roles 
        WHERE user_id=%s AND role_id=(SELECT id FROM roles WHERE name=%s)
    """,
        (user_id, role_name),
    )

    conn.commit()
    cur.close()
    conn.close()


def set_active_status(user_id, status):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE users SET is_active=%s WHERE id=%s", (status, user_id))

    conn.commit()
    cur.close()
    conn.close()


# ------------------ ACCESS CONTROL ------------------
if not is_authenticated() or not has_role("admin"):
    st.error("Access denied. Only Admin can access this page.")
    st.stop()


# ------------------ UI ------------------
st.title("Admin Panel")
st.caption("Manage user roles, permissions, and account status.")

users = get_all_users()

st.subheader("All Users")

for user in users:
    with st.expander(f"{user['username']} — {user['full_name']}"):
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Active:** {'Yes' if user['is_active'] else 'No'}")

        current_roles = get_roles(user["id"])
        st.write(f"**Roles:** {', '.join(current_roles) if current_roles else 'None'}")

        st.markdown("---")

        # Assign new role
        st.write("### Assign Role")
        role_to_assign = st.selectbox(
            f"Assign role to {user['username']}",
            ["teacher", "office", "parent", "student"],
            key=f"assign_{user['id']}",
        )

        if st.button(f"Assign {role_to_assign}", key=f"btn_assign_{user['id']}"):
            assign_role(user["id"], role_to_assign)
            st.success(f"Role '{role_to_assign}' assigned to {user['username']}.")
            st.experimental_rerun()

        # Remove role
        st.write("### Remove Role")
        if current_roles:
            role_to_remove = st.selectbox(
                f"Remove role from {user['username']}",
                current_roles,
                key=f"remove_{user['id']}",
            )

            if st.button(f"Remove {role_to_remove}", key=f"btn_remove_{user['id']}"):
                remove_role(user["id"], role_to_remove)
                st.warning(f"Role '{role_to_remove}' removed from {user['username']}.")
                st.experimental_rerun()

        st.markdown("---")

        # Activate / Deactivate
        st.write("### Account Status")
        if user["is_active"]:
            if st.button("Deactivate Account", key=f"deact_{user['id']}"):
                set_active_status(user["id"], 0)
                st.warning(f"{user['username']} deactivated.")
                st.experimental_rerun()
        else:
            if st.button("Activate Account", key=f"act_{user['id']}"):
                set_active_status(user["id"], 1)
                st.success(f"{user['username']} activated.")
                st.experimental_rerun()
