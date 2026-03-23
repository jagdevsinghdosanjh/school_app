import streamlit as st
from datetime import date
from auth.auth_manager import is_authenticated, has_role
from db.students import get_student_by_roll
from db.fees import record_fee_payment, get_fee_status, get_payment_history
from db.office import (
    generate_receipt_no,
    get_daily_collection,
    get_monthly_collection,
    get_all_payments,
)

# -------------------------
# ACCESS CONTROL
# -------------------------
if not is_authenticated():
    st.error("Login required")
    st.stop()

if not has_role("office", "admin"):
    st.error("Access denied")
    st.stop()

st.title("Office Desk")
st.caption("Manage fee payments, receipts, and financial reports.")

# -------------------------
# TABS
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["Record Payment", "Fee Status", "Daily Summary", "Monthly Summary"]
)

# -------------------------
# TAB 1 — RECORD PAYMENT
# -------------------------
with tab1:
    st.subheader("Record Fee Payment")

    roll_no = st.text_input("Student Roll No")
    amount = st.number_input("Amount Paid", min_value=0, step=100)
    mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Card", "Bank Transfer"])

    if st.button("Record Payment"):
        student = get_student_by_roll(roll_no)
        if student:
            receipt_no = generate_receipt_no(student["id"])
            record_fee_payment(student["id"], amount, mode)
            st.success(f"Payment recorded. Receipt No: {receipt_no}")
        else:
            st.error("Student not found.")

# -------------------------
# TAB 2 — FEE STATUS
# -------------------------
with tab2:
    st.subheader("Check Fee Status")

    roll_search = st.text_input("Search Roll No", key="fees_search_roll")

    if st.button("Fetch Status"):
        student = get_student_by_roll(roll_search)
        if student:
            status = get_fee_status(student["id"])
            history = get_payment_history(student["id"])

            st.write("### Fee Status")
            st.write(status)

            st.write("### Payment History")
            for h in history:
                st.write(f"₹{h[0]} via {h[1]} on {h[2]}")
        else:
            st.error("Student not found.")

# -------------------------
# TAB 3 — DAILY SUMMARY
# -------------------------
with tab3:
    st.subheader("Daily Collection Summary")

    target_date = st.date_input("Select Date", value=date.today())
    total = get_daily_collection(target_date)

    st.metric(f"Total Collection on {target_date}", f"₹{total}")

# -------------------------
# TAB 4 — MONTHLY SUMMARY
# -------------------------
with tab4:
    st.subheader("Monthly Collection Summary")

    year = st.number_input(
        "Year", min_value=2020, max_value=2030, value=date.today().year
    )
    month = st.number_input(
        "Month", min_value=1, max_value=12, value=date.today().month
    )

    total = get_monthly_collection(year, month)

    st.metric(f"Total Collection ({month}/{year})", f"₹{total}")
