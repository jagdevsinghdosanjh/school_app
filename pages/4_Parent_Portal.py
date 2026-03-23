from db.fees import get_fee_status, get_payment_history
from db.parents import get_children_for_parent  # coming next

with tab4:
    st.subheader("Fees Status")

    student_id = selected_child_id  # from parent-child mapping

    status = get_fee_status(student_id)
    if status:
        st.write(f"Total Fees: ₹{status['total_fees']}")
        st.write(f"Paid: ₹{status['paid']}")
        st.write(f"Due: ₹{status['due']}")
        st.write(f"Last Payment: {status['last_payment_date']}")

        st.markdown("### Payment History")
        history = get_payment_history(student_id)
        for h in history:
            st.write(f"₹{h[0]} via {h[1]} on {h[2]}")
    else:
        st.info("No fee record found.")
