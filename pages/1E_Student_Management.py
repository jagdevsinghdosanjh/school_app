import streamlit as st
from auth.auth_manager import is_authenticated, has_role
from db.student_admin import register_student, get_all_students, promote_student
from components.sidebar import show_sidebar

show_sidebar()


# -------------------------
# ACCESS CONTROL
# -------------------------
if not is_authenticated():
    st.error("Login required")
    st.stop()

if not has_role("admin"):
    st.error("Access denied")
    st.stop()

st.title("Student Management")
st.caption("Register new students and promote existing students.")

# -------------------------
# REGISTER NEW STUDENT
# -------------------------
st.subheader("Register New Student")

with st.form("register_student_form"):
    full_name = st.text_input("Full Name")
    roll_no = st.text_input("Roll Number")
    cls = st.selectbox("Class", ["6", "7", "8", "9", "10"])
    section = st.selectbox("Section", ["A", "B", "C"])

    submitted = st.form_submit_button("Register Student")

    if submitted:
        if not full_name or not roll_no:
            st.error("Full name and roll number are required.")
        else:
            register_student(full_name, roll_no, cls, section)
            st.success(f"Student '{full_name}' registered successfully.")

st.markdown("---")

# -------------------------
# PROMOTE STUDENTS
# -------------------------
st.subheader("Promote Students")

students = get_all_students()

for s in students:
    with st.expander(f"{s['full_name']} — Class {s['class']}{s['section']}"):
        new_class = st.selectbox(
            "New Class",
            ["6", "7", "8", "9", "10"],
            index=["6", "7", "8", "9", "10"].index(s["class"]),
            key=f"class_{s['id']}",
        )
        new_section = st.selectbox(
            "New Section",
            ["A", "B", "C"],
            index=["A", "B", "C"].index(s["section"]),
            key=f"section_{s['id']}",
        )

        if st.button("Promote", key=f"promote_{s['id']}"):
            promote_student(s["id"], new_class, new_section)
            st.success(f"{s['full_name']} promoted to Class {new_class}{new_section}.")
            st.experimental_rerun()
