import streamlit as st
from auth.auth_manager import is_authenticated, has_role, logout

st.set_page_config(page_title="DBA Logout", layout="centered")

# ------------------ ACCESS CONTROL ------------------
if not is_authenticated() or not has_role("dba"):
    st.error("Access denied. Only DBA can access this page.")
    st.stop()

# ------------------ UI ------------------
st.title("DBA Logout")
st.caption("You are logged in as Database Administrator.")

st.markdown("### Are you sure you want to log out?")

if st.button("Logout Now"):
    logout()
    st.success("You have been logged out successfully.")
