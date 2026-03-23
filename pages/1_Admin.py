import streamlit as st
from auth.auth_manager import is_authenticated, has_role
from db.students import get_students_by_class
from db.fees import get_fee_status
from db.attendance import get_attendance_summary
from db.marks import get_marks_for_student

# -------------------------
# ACCESS CONTROL
# -------------------------
if not is_authenticated():
    st.error("Login required")
    st.stop()

if not has_role("admin"):
    st.error("Access denied")
    st.stop()

# -------------------------
# PAGE HEADER
# -------------------------
st.title("Admin Dashboard")
st.caption("Manage users, roles, teachers, parents, and system operations.")

# -------------------------
# DASHBOARD CARDS
# -------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Students", "—")
with col2:
    st.metric("Total Teachers", "—")
with col3:
    st.metric("Parents Registered", "—")
with col4:
    st.metric("Office Staff", "—")

st.markdown("---")

# -------------------------
# MANAGEMENT SECTIONS
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["User Management", "Teacher Management", "Parent Management", "System Tools"]
)

# -------------------------
# USER MANAGEMENT TAB
# -------------------------
with tab1:
    st.subheader("User Management")
    st.write("Create users, assign roles, activate/deactivate accounts.")
    st.page_link("pages/1_Admin_Panel.py", label="Open User & Role Manager")

# -------------------------
# TEACHER MANAGEMENT TAB
# -------------------------
with tab2:
    st.subheader("Teacher Management")
    st.write("Create teacher accounts and assign them classes.")
    st.info("Teacher creation module coming next.")

# -------------------------
# PARENT MANAGEMENT TAB
# -------------------------
with tab3:
    st.subheader("Parent Management")
    st.write("Register parents and map them to their children.")
    st.info("Parent registration & mapping module coming next.")

# -------------------------
# SYSTEM TOOLS TAB
# -------------------------
with tab4:
    st.subheader("System Tools")
    st.write("Database admin, backups, logs, and maintenance.")
    st.page_link("pages/@_DBA_Panels.py", label="Open DBA Panel")


# import streamlit as st
# from auth.auth_manager import is_authenticated, has_role

# if not is_authenticated():
#     st.error("Login required")
#     st.stop()

# if not has_role("admin"):
#     st.error("Access denied")
#     st.stop()

# st.title("Admin Dashboard")
