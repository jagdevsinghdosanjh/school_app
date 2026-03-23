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


# import streamlit as st
# from auth.auth_manager import is_authenticated, has_role, logout

# st.set_page_config(page_title="Parent Portal", layout="wide")

# # --- Access control ---
# if not is_authenticated():
#     st.error("You must be logged in to view this page.")
#     st.stop()

# if not has_role("parent", "admin"):
#     st.error("You do not have permission to view this page.")
#     st.stop()

# user = st.session_state["user"]

# # --- Header ---
# st.title("Parent Portal")
# st.caption(f"Welcome, {user['full_name']}")

# # Placeholder: later fetch children list from DB (parent_child table)
# children = ["Child 1 – Aman (Class 10-A)", "Child 2 – Simran (Class 6-B)"]
# selected_child = st.selectbox("Select Child", children)

# tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Attendance", "Marks", "Fees"])

# with tab1:
#     st.subheader("Child Overview")
#     st.write(f"Details for: {selected_child} (placeholder)")
#     st.write("• Class Teacher: (placeholder)")
#     st.write("• Contact: (placeholder)")

# with tab2:
#     st.subheader("Attendance")
#     # TODO: fetch attendance summary for selected child
#     st.write("Present: 118 days (placeholder)")
#     st.write("Absent: 7 days (placeholder)")
#     st.write("Attendance %: 94% (placeholder)")

# with tab3:
#     st.subheader("Marks")
#     exam = st.selectbox(
#         "Exam",
#         ["Unit Test 1", "Unit Test 2", "Half Yearly", "Final"],
#         key="parent_exam",
#     )
#     # TODO: fetch marks for selected child
#     st.write(f"Marks for **{exam}** (placeholder):")
#     st.write("- Mathematics: 85")
#     st.write("- Science: 90")
#     st.write("- English: 88")

# with tab4:
#     st.subheader("Fees")
#     # TODO: fetch fees status from DB
#     st.write("• Total Fees: ₹40,000 (placeholder)")
#     st.write("• Paid: ₹30,000 (placeholder)")
#     st.write("• Due: ₹10,000 (placeholder)")
#     st.write("• Last Payment Date: 2026-02-15 (placeholder)")

# st.markdown("---")

# if st.button("Logout"):
#     logout()
