import streamlit as st
from auth.auth_manager import is_authenticated, has_role
from db.teacher_classes import assign_class, get_all_assignments, delete_assignment
from db.base import get_connection

# -------------------------
# ACCESS CONTROL
# -------------------------
if not is_authenticated():
    st.error("Login required")
    st.stop()

if not has_role("admin"):
    st.error("Access denied")
    st.stop()

st.title("Class Assignment Manager")
st.caption("Assign teachers to classes, sections, and subjects.")


# -------------------------
# GET TEACHERS
# -------------------------
def get_teachers():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT u.id, u.full_name
        FROM users u
        JOIN user_roles ur ON ur.user_id = u.id
        JOIN roles r ON r.id = ur.role_id
        WHERE r.name = 'teacher'
        ORDER BY u.full_name
    """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


teachers = get_teachers()

# -------------------------
# ASSIGN CLASS FORM
# -------------------------
st.subheader("Assign Class to Teacher")

with st.form("assign_form"):
    teacher = st.selectbox(
        "Select Teacher", teachers, format_func=lambda x: x["full_name"]
    )
    cls = st.selectbox("Class", ["6", "7", "8", "9", "10"])
    section = st.selectbox("Section", ["A", "B", "C"])
    subject = st.selectbox(
        "Subject",
        [
            "Math",
            "Science",
            "English",
            "Punjabi",
            "Hindi",
            "Social Studies",
            "Computer Science",
            "HPE",
            "Drawing",
        ],
    )

    submitted = st.form_submit_button("Assign")

    if submitted:
        assign_class(teacher["id"], cls, section, subject)
        st.success("Class assigned successfully.")
        st.experimental_rerun()

st.markdown("---")

# -------------------------
# VIEW ALL ASSIGNMENTS
# -------------------------
st.subheader("All Class Assignments")

assignments = get_all_assignments()

for a in assignments:
    with st.expander(
        f"{a['teacher']} — Class {a['class']}{a['section']} ({a['subject']})"
    ):
        if st.button("Delete Assignment", key=f"del_{a['id']}"):
            delete_assignment(a["id"])
            st.warning("Assignment deleted.")
            st.experimental_rerun()
