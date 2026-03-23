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
