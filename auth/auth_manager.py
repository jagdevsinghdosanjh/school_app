import bcrypt
import streamlit as st
from .db_manager import get_user_by_username, get_roles_for_user


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def login_form():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = get_user_by_username(username)
        if not user or not user["is_active"]:
            st.error("Invalid username or inactive account.")
            return
        if not verify_password(password, user["password_hash"]):
            st.error("Incorrect password.")
            return

        roles = get_roles_for_user(user["id"])
        if not roles:
            st.error("No roles assigned. Contact admin.")
            return

        st.session_state["authenticated"] = True
        st.session_state["user"] = {
            "id": user["id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user["email"],
            "roles": roles,
        }
        st.rerun()


def logout():
    for key in ["authenticated", "user"]:
        st.session_state.pop(key, None)
    st.rerun()


def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)


def has_role(*required_roles) -> bool:
    if not is_authenticated():
        return False
    user_roles = st.session_state["user"]["roles"]
    return any(r in user_roles for r in required_roles)
