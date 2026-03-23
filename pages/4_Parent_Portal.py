import streamlit as st
from auth.auth_manager import is_authenticated, has_role
from db.parents import get_parent_by_user_id, get_children_for_parent
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

if not has_role("parent"):
    st.error("Access denied")
    st.stop()

# -------------------------
# LOAD PARENT + CHILDREN
# -------------------------
parent = get_parent_by_user_id(st.session_state["user"]["id"])
children = get_children_for_parent(parent["id"])

child_names = {c["full_name"]: c["id"] for c in children}

selected_child = st.selectbox("Select Child", list(child_names.keys()))
selected_child_id = child_names[selected_child]

# -------------------------
# FEES SECTION
# -------------------------
status = get_fee_status(selected_child_id)
history = get_payment_history(selected_child_id)

st.subheader("Fee Status")
st.write(status)

st.subheader("Payment History")
for h in history:
    st.write(h)


# -------------------------
# HOMEWORK SECTION
# -------------------------

st.subheader("Homework")

child = get_student_by_id(selected_child_id)

hw_list = get_homework_for_class(child["class"], child["section"])

if not hw_list:
    st.info("No homework assigned.")
else:
    for hw in hw_list:
        with st.expander(f"{hw['subject']} — {hw['title']}"):
            st.write(hw["description"])
            st.write(f"**Due Date:** {hw['due_date']}")
            st.caption(f"Posted on {hw['created_at']}")


# from db.parents import get_parent_by_user_id, get_children_for_parent
# from db.fees import get_fee_status, get_payment_history
# import streamlit as st
# from auth.auth_manager import is_authenticated, has_role

# if not is_authenticated():
#     st.error("Login required")
#     st.stop()

# if not has_role("parent"):
#     st.error("Access denied")
#     st.stop()


# parent = get_parent_by_user_id(st.session_state["user"]["id"])
# children = get_children_for_parent(parent["id"])

# child_names = {c["full_name"]: c["id"] for c in children}

# selected_child = st.selectbox("Select Child", list(child_names.keys()))
# selected_child_id = child_names[selected_child]

# status = get_fee_status(selected_child_id)
# history = get_payment_history(selected_child_id)

# st.write("### Fee Status")
# st.write(status)

# st.write("### Payment History")
# for h in history:
#     st.write(h)


# # from db.fees import get_fee_status, get_payment_history
# # from db.parents import get_children_for_parent  # coming next

# # with tab4:
# #     st.subheader("Fees Status")

# #     student_id = selected_child_id  # from parent-child mapping

# #     status = get_fee_status(student_id)
# #     if status:
# #         st.write(f"Total Fees: ₹{status['total_fees']}")
# #         st.write(f"Paid: ₹{status['paid']}")
# #         st.write(f"Due: ₹{status['due']}")
# #         st.write(f"Last Payment: {status['last_payment_date']}")

# #         st.markdown("### Payment History")
# #         history = get_payment_history(student_id)
# #         for h in history:
# #             st.write(f"₹{h[0]} via {h[1]} on {h[2]}")
# #     else:
# #         st.info("No fee record found.")
