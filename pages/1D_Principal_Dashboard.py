import streamlit as st
from auth.auth_manager import is_authenticated, has_role
from db.principal import class_strength, attendance_overview, fee_overview, teacher_load
from components.sidebar import show_sidebar

show_sidebar()

# -------------------------
# ACCESS CONTROL
# -------------------------
if not is_authenticated():
    st.error("Login required")
    st.stop()

if not has_role("principal", "admin"):
    st.error("Access denied")
    st.stop()

# -------------------------
# HEADER
# -------------------------
st.title("Principal Dashboard")
st.caption("School-wide analytics and performance overview.")

# -------------------------
# FEE OVERVIEW
# -------------------------
st.subheader("Fee Overview")

fees = fee_overview()

col1, col2, col3 = st.columns(3)
col1.metric("Total Fees", f"₹{fees['total_fees']}")
col2.metric("Collected", f"₹{fees['paid']}")
col3.metric("Pending", f"₹{fees['due']}")

st.markdown("---")

# -------------------------
# CLASS STRENGTH
# -------------------------
st.subheader("Class Strength")

strength = class_strength()

for cls, sec, count in strength:
    st.write(f"Class **{cls}-{sec}** → {count} students")

st.markdown("---")

# -------------------------
# ATTENDANCE OVERVIEW
# -------------------------
st.subheader("Attendance Overview")

attendance = attendance_overview()

for cls, present, absent in attendance:
    total = present + absent
    percent = round((present / total * 100), 2) if total else 0
    st.write(f"Class **{cls}** → {percent}% attendance")

st.markdown("---")

# -------------------------
# TEACHER LOAD
# -------------------------
st.subheader("Teacher Workload")

load = teacher_load()

for teacher, count in load:
    st.write(f"**{teacher}** → {count} assigned classes")
