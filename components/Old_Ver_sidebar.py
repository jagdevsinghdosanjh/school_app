import streamlit as st


def show_sidebar():
    if "user" not in st.session_state:
        st.sidebar.info("Please log in.")
        return

    role = st.session_state["user"]["role"]

    st.sidebar.title("Navigation")

    # -------------------------
    # ADMIN MENU
    # -------------------------
    if role == "admin":
        st.sidebar.page_link("pages/1_Admin.py", label="Admin Dashboard")
        st.sidebar.page_link("pages/1_Admin_Panel.py", label="User & Role Manager")
        st.sidebar.page_link(
            "pages/1A_Teacher_Management.py", label="Teacher Management"
        )
        st.sidebar.page_link("pages/1B_Class_Assignment.py", label="Class Assignment")
        st.sidebar.page_link("pages/1C_Parent_Management.py", label="Parent Management")
        st.sidebar.page_link(
            "pages/1E_Student_Management.py", label="Student Management"
        )
        st.sidebar.page_link("pages/@_DBA_Panels.py", label="DBA Panel")

    # -------------------------
    # PRINCIPAL MENU
    # -------------------------
    elif role == "principal":
        st.sidebar.page_link(
            "pages/1D_Principal_Dashboard.py", label="Principal Dashboard"
        )

    # -------------------------
    # TEACHER MENU
    # -------------------------
    elif role == "teacher":
        st.sidebar.page_link("pages/2_Teacher_Panel.py", label="Teacher Panel")

    # -------------------------
    # STUDENT MENU
    # -------------------------
    elif role == "student":
        st.sidebar.page_link("pages/3_Student_Portal.py", label="Student Portal")

    # -------------------------
    # PARENT MENU
    # -------------------------
    elif role == "parent":
        st.sidebar.page_link("pages/4_Parent_Portal.py", label="Parent Portal")

    # -------------------------
    # OFFICE STAFF MENU
    # -------------------------
    elif role == "office":
        st.sidebar.page_link("pages/5_Office_Desk.py", label="Office Desk")

    # -------------------------
    # LOGOUT BUTTON
    # -------------------------
    from auth.auth_manager import logout

    if st.sidebar.button("Logout"):
        logout()
