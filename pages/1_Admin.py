import streamlit as st
from auth.auth_manager import is_authenticated, has_role
from db.dashboard import (
    count_students,
    count_teachers,
    count_parents,
    count_office_staff,
    count_homework,
    count_attendance_entries,
    total_fee_collected,
)

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
st.caption("Live system statistics and administrative controls.")

# -------------------------
# METRICS ROW 1
# -------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Students", count_students())

with col2:
    st.metric("Total Teachers", count_teachers())

with col3:
    st.metric("Parents Registered", count_parents())

with col4:
    st.metric("Office Staff", count_office_staff())

st.markdown("---")

# -------------------------
# METRICS ROW 2
# -------------------------
col5, col6, col7 = st.columns(3)

with col5:
    st.metric("Homework Posted", count_homework())

with col6:
    st.metric("Attendance Entries", count_attendance_entries())

with col7:
    st.metric("Total Fees Collected (₹)", total_fee_collected())

st.markdown("---")

# -------------------------
# NAVIGATION LINKS
# -------------------------
st.subheader("Management Panels")

st.page_link("pages/1_Admin_Panel.py", label="User & Role Manager")
st.page_link("pages/1A_Teacher_Management.py", label="Teacher Management")
st.page_link("pages/1B_Class_Assignment.py", label="Class Assignment Manager")
st.page_link("pages/0_DBA_Panel.py", label="DBA Panel")
