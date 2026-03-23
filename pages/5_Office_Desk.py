from db.fees import record_fee_payment, get_fee_status, get_payment_history
from db.students import get_student_by_roll  # we will create this next

# --- Fees Management ---
with tab2:
    st.subheader("Record Fee Payment")

    roll_no = st.text_input("Student Roll No")
    amount = st.number_input("Amount Paid", min_value=0, step=100)
    mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Card", "Bank Transfer"])

    if st.button("Record Payment"):
        student = get_student_by_roll(roll_no)
        if student:
            record_fee_payment(student["id"], amount, mode)
            st.success("Payment recorded successfully.")
        else:
            st.error("Student not found.")

    st.markdown("---")
    st.subheader("Check Fees Status")

    roll_search = st.text_input("Search Roll No", key="fees_search_roll")

    if st.button("Fetch Fees Status"):
        student = get_student_by_roll(roll_search)
        if student:
            status = get_fee_status(student["id"])
            st.write(status)
            history = get_payment_history(student["id"])
            st.write("Payment History:", history)
        else:
            st.error("Student not found.")


# import streamlit as st
# from auth.auth_manager import is_authenticated, has_role, logout

# st.set_page_config(page_title="Office Desk", layout="wide")

# # --- Access control ---
# if not is_authenticated():
#     st.error("You must be logged in to view this page.")
#     st.stop()

# if not has_role("office", "admin"):
#     st.error("You do not have permission to view this page.")
#     st.stop()

# st.title("Office Desk")
# st.caption("Manage admissions, fees, and certificates.")

# tab1, tab2, tab3 = st.tabs(["Admissions", "Fees Management", "Certificates"])

# # --- Admissions ---
# with tab1:
#     st.subheader("New Admission")
#     name = st.text_input("Student Name")
#     cls = st.text_input("Class")
#     section = st.text_input("Section")
#     contact = st.text_input("Parent Contact")
#     address = st.text_area("Address")

#     if st.button("Register Student"):
#         # TODO: insert into students table
#         st.success("Student registered (placeholder).")

# # --- Fees Management ---
# with tab2:
#     st.subheader("Fees Management")

#     roll_no = st.text_input("Student Roll No")
#     cls_fees = st.text_input("Class")
#     amount = st.number_input("Amount Paid", min_value=0, step=100)
#     mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Card", "Bank Transfer"])

#     if st.button("Record Payment"):
#         # TODO: insert into fees_payments table
#         st.success("Payment recorded (placeholder).")

#     st.markdown("---")
#     st.subheader("Check Fees Status")
#     roll_search = st.text_input("Search by Roll No", key="fees_search_roll")
#     if st.button("Fetch Fees Status"):
#         # TODO: query fees summary
#         st.info("Fees status for this student (placeholder).")

# # --- Certificates ---
# with tab3:
#     st.subheader("Certificates")
#     cert_type = st.selectbox("Certificate Type", ["Bonafide", "Character", "Transfer"])
#     cert_roll = st.text_input("Student Roll No", key="cert_roll")

#     if st.button("Generate Certificate"):
#         # TODO: generate certificate record / PDF
#         st.success(f"{cert_type} certificate generated (placeholder).")

# st.markdown("---")

# if st.button("Logout"):
#     logout()
