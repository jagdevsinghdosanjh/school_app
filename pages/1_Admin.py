import streamlit as st
from auth.auth_manager import is_authenticated, has_role

if not is_authenticated():
    st.error("Login required")
    st.stop()

if not has_role("admin"):
    st.error("Access denied")
    st.stop()

st.title("Admin Dashboard")
