import streamlit as st
from auth.auth_manager import is_authenticated, has_role
from db.students import get_student_by_id
from db.attendance import get_attendance_for_student, get_attendance_summary
from db.marks import get_marks_for_student
from db.fees import get_fee_status, get_payment_history
from db.homework import get_homework_for_class
from components.sidebar import show_sidebar

show_sidebar()


# -------------------------
# ACCESS CONTROL
# -------------------------
if not is_authenticated():
    st.error("Login required")
    st.stop()

if not has_role("student"):
    st.error("Access denied")
    st.stop()

# -------------------------
# LOAD STUDENT DATA
# -------------------------
student_id = st.session_state["user"].get("student_id")

if not student_id:
    st.error("Student account not linked to a student record.")
    st.stop()

student = get_student_by_id(student_id)

st.title("Student Portal")
st.caption(f"Welcome, {student['full_name']}")

# -------------------------
# TABS
# -------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Profile", "Attendance", "Marks", "Homework", "Fees"]
)

# -------------------------
# PROFILE TAB
# -------------------------
with tab1:
    st.subheader("My Profile")
    st.write(f"**Full Name:** {student['full_name']}")
    st.write(f"**Roll No:** {student['roll_no']}")
    st.write(f"**Class:** {student['class']}")
    st.write(f"**Section:** {student['section']}")
    st.write("---")

# -------------------------
# ATTENDANCE TAB
# -------------------------
with tab2:
    st.subheader("My Attendance")

    summary = get_attendance_summary(student_id)
    st.write(f"**Total Days:** {summary['total']}")
    st.write(f"**Present:** {summary['present']}")
    st.write(f"**Absent:** {summary['absent']}")
    st.write(f"**Attendance %:** {summary['percent']}%")

    st.markdown("### Recent Attendance")
    records = get_attendance_for_student(student_id)

    for date, status in records[:20]:
        st.write(f"{date} — **{status.capitalize()}**")

# -------------------------
# MARKS TAB
# -------------------------
with tab3:
    st.subheader("My Marks")

    exam = st.selectbox(
        "Select Exam", ["Unit Test 1", "Unit Test 2", "Half Yearly", "Final"]
    )

    marks = get_marks_for_student(student_id, exam)

    if marks:
        for subject, obtained, max_marks in marks:
            st.write(f"**{subject}:** {obtained}/{max_marks}")
    else:
        st.info("No marks found for this exam.")

# -------------------------
# HOMEWORK TAB
# -------------------------

with tab4:
    st.subheader("Homework")

    hw_list = get_homework_for_class(student["class"], student["section"])

    if not hw_list:
        st.info("No homework assigned yet.")
    else:
        for hw in hw_list:
            with st.expander(f"{hw['subject']} — {hw['title']}"):
                st.write(hw["description"])
                st.write(f"**Due Date:** {hw['due_date']}")
                st.caption(f"Posted on {hw['created_at']}")

# with tab4:
#     st.subheader("Homework")
#     st.info("Homework module coming soon.")

# -------------------------
# FEES TAB
# -------------------------
with tab5:
    st.subheader("My Fees")

    status = get_fee_status(student_id)

    if status:
        st.write(f"**Total Fees:** ₹{status['total_fees']}")
        st.write(f"**Paid:** ₹{status['paid']}")
        st.write(f"**Due:** ₹{status['due']}")
        st.write(f"**Last Payment:** {status['last_payment_date']}")

        st.markdown("### Payment History")
        history = get_payment_history(student_id)

        for h in history:
            st.write(f"₹{h[0]} via {h[1]} on {h[2]}")
    else:
        st.info("No fee record found.")


# # import streamlit as st
# # from auth.auth_manager import is_authenticated, has_role, logout
# from db.fees import get_fee_status, get_payment_history
# import streamlit as st
# from auth.auth_manager import is_authenticated, has_role
# from db.fees import get_fee_status, get_payment_history

# # -------------------------
# # ACCESS CONTROL
# # -------------------------
# if not is_authenticated():
#     st.error("Login required")
#     st.stop()

# if not has_role("student"):
#     st.error("Access denied")
#     st.stop()

# # -------------------------
# # TABS FOR STUDENT PORTAL
# # -------------------------
# tab1, tab2, tab3, tab4, tab5 = st.tabs(
#     ["Profile", "Attendance", "Marks", "Homework", "Fees"]
# )

# with tab5:
#     st.subheader("My Fees")

#     student_id = user["student_id"]  # from login mapping

#     status = get_fee_status(student_id)
#     st.write(status)

#     history = get_payment_history(student_id)
#     st.write("Payment History:", history)
