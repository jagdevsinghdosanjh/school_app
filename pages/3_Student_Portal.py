# import streamlit as st
# from auth.auth_manager import is_authenticated, has_role, logout
from db.fees import get_fee_status, get_payment_history

with tab5:
    st.subheader("My Fees")

    student_id = user["student_id"]  # from login mapping

    status = get_fee_status(student_id)
    st.write(status)

    history = get_payment_history(student_id)
    st.write("Payment History:", history)

# st.set_page_config(page_title="Student Portal", layout="wide")

# # --- Access control ---
# if not is_authenticated():
#     st.error("You must be logged in to view this page.")
#     st.stop()

# if not has_role("student", "admin"):
#     st.error("You do not have permission to view this page.")
#     st.stop()

# user = st.session_state["user"]

# # --- Header ---
# st.title("Student Portal")
# st.caption(f"Welcome, {user['full_name']}")

# tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Attendance", "Marks", "Homework"])

# with tab1:
#     st.subheader("Overview")
#     st.write("• Class: (placeholder)")
#     st.write("• Roll No: (placeholder)")
#     st.write("• Section: (placeholder)")
#     st.write("• Class Teacher: (placeholder)")

# with tab2:
#     st.subheader("Attendance Summary")
#     # TODO: fetch from attendance table filtered by student_id
#     st.write("Present: 120 days (placeholder)")
#     st.write("Absent: 5 days (placeholder)")
#     st.write("Attendance %: 96% (placeholder)")

# with tab3:
#     st.subheader("Marks")
#     exam = st.selectbox(
#         "Select Exam", ["Unit Test 1", "Unit Test 2", "Half Yearly", "Final"]
#     )
#     # TODO: fetch marks from DB
#     st.write(f"Marks for **{exam}** (placeholder):")
#     st.write("- Mathematics: 88")
#     st.write("- Science: 92")
#     st.write("- English: 85")

# with tab4:
#     st.subheader("Homework / Assignments")
#     # TODO: fetch homework from DB
#     st.write("• Mathematics – Chapter 5 Exercises (Due: 2026-03-25)")
#     st.write("• Science – Lab Report (Due: 2026-03-27)")

# st.markdown("---")

# if st.button("Logout"):
#     logout()
