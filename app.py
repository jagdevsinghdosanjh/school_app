import streamlit as st
from auth.auth_manager import login_form, logout, is_authenticated, has_role

st.set_page_config(page_title="School Management System")

# if is_authenticated() and has_role("dba"):
#     st.sidebar.page_link("pages/0_DBA_Logout.py", label="DBA Logout")


def show_nav():
    st.sidebar.title("Navigation")

    if is_authenticated():
        st.sidebar.write(f"Welcome, {st.session_state['user']['full_name']}")

        if has_role("admin"):
            st.sidebar.page_link("pages/1_Admin.py", label="Admin Dashboard")
        if has_role("teacher"):
            st.sidebar.page_link("pages/2_Teacher_Panel.py", label="Teacher Panel")
        if has_role("student"):
            st.sidebar.page_link("pages/3_Student_Portal.py", label="Student Portal")

        if st.sidebar.button("Logout"):
            logout()
    else:
        st.sidebar.info("Please log in")


def main():
    if not is_authenticated():
        login_form()
        return

    show_nav()
    st.title("School Management System")


main()
