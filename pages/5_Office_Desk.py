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
