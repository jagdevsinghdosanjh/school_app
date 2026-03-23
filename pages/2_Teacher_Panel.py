import streamlit as st
from datetime import date

from auth.auth_manager import is_authenticated, has_role, logout
from db.students import get_students_by_class
from db.attendance import save_attendance
from db.marks import save_marks
from db.teacher_classes import get_classes_for_teacher
from components.sidebar import show_sidebar

show_sidebar()


# -------------------------
# ACCESS CONTROL
# -------------------------
if not is_authenticated():
    st.error("You must be logged in to view this page.")
    st.stop()

if not has_role("teacher", "admin"):
    st.error("You do not have permission to view this page.")
    st.stop()

teacher_id = st.session_state["user"]["id"]

# -------------------------
# HEADER
# -------------------------
st.title("Teacher Panel")
st.caption("Manage your classes, attendance, and student performance.")

# -------------------------
# LOAD TEACHER CLASSES
# -------------------------
assigned_classes = get_classes_for_teacher(teacher_id)

if not assigned_classes:
    st.warning("No classes assigned to you yet. Contact Admin.")
    st.stop()

# Display assigned classes
st.subheader("My Classes")
for c in assigned_classes:
    st.write(f"• Class {c['class']}-{c['section']} — {c['subject']}")

st.markdown("---")

# -------------------------
# ATTENDANCE SECTION
# -------------------------
st.subheader("Attendance")

# Build dropdowns from assigned classes
class_options = [
    f"{c['class']}-{c['section']} ({c['subject']})" for c in assigned_classes
]
selected = st.selectbox("Select Class", class_options)

# Extract class + section + subject
selected_class, rest = selected.split("-", 1)
selected_section = rest.split(" ")[0]

students = get_students_by_class(selected_class, selected_section)

if not students:
    st.info("No students found for this class.")
    st.stop()

att_date = st.date_input("Date", value=date.today())
st.write(f"Attendance for Class {selected_class}-{selected_section}")

status_map = {}

for s in students:
    status = st.radio(
        f"{s['roll_no']} - {s['full_name']}",
        ["present", "absent"],
        horizontal=True,
        key=f"att_{s['id']}",
    )
    status_map[s["id"]] = status

if st.button("Save Attendance"):
    save_attendance(
        class_name=f"{selected_class}-{selected_section}",
        att_date=att_date,
        teacher_id=teacher_id,
        status_map=status_map,
    )
    st.success("Attendance saved successfully.")

st.markdown("---")

# -------------------------
# MARKS ENTRY SECTION
# -------------------------
st.subheader("Marks Entry")

exam_type = st.selectbox("Exam", ["Unit Test 1", "Unit Test 2", "Half Yearly", "Final"])

# Subject comes from assigned class
subject = selected.split("(")[1].replace(")", "")

st.write(
    f"Enter marks for **Class {selected_class}-{selected_section}**, "
    f"**{subject}**, **{exam_type}**"
)

marks_entries = []

for s in students:
    m = st.number_input(
        f"{s['roll_no']} - {s['full_name']}",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
        key=f"mark_{s['id']}",
    )

    marks_entries.append(
        {
            "student_id": s["id"],
            "subject": subject,
            "exam": exam_type,
            "marks_obtained": m,
            "max_marks": 100,
            "teacher_id": teacher_id,
        }
    )

if st.button("Save Marks"):
    save_marks(marks_entries)
    st.success("Marks saved successfully.")

st.markdown("---")

# -------------------------
# HOMEWORK SECTION
# -------------------------
st.subheader("Post Homework")

hw_title = st.text_input("Homework Title")
hw_desc = st.text_area("Description")
hw_due = st.date_input("Due Date")

if st.button("Post Homework"):
    from db.homework import add_homework

    add_homework(
        teacher_id=teacher_id,
        cls=selected_class,
        section=selected_section,
        subject=subject,
        title=hw_title,
        description=hw_desc,
        due_date=hw_due,
    )
    st.success("Homework posted successfully!")


# -------------------------
# LOGOUT
# -------------------------
if st.button("Logout"):
    logout()


# import streamlit as st
# from datetime import date

# from auth.auth_manager import is_authenticated, has_role, logout
# from db.students import get_students_by_class
# from db.attendance import save_attendance
# from db.marks import save_marks

# st.set_page_config(page_title="Teacher Panel", layout="wide")

# # ---------------------------------------------------------
# # ACCESS CONTROL
# # ---------------------------------------------------------
# if not is_authenticated():
#     st.error("You must be logged in to view this page.")
#     st.stop()

# if not has_role("teacher", "admin"):
#     st.error("You do not have permission to view this page.")
#     st.stop()

# teacher_id = st.session_state["user"]["id"]

# # ---------------------------------------------------------
# # HEADER
# # ---------------------------------------------------------
# st.title("Teacher Panel")
# st.caption("Manage your classes, attendance, and student performance.")

# col1, col2 = st.columns([2, 1])
# with col1:
#     st.subheader("My Classes")
#     st.write("• Class 10-A – Mathematics")
#     st.write("• Class 9-B – Science")

# with col2:
#     st.subheader("Quick Actions")
#     st.button("Take Attendance")
#     st.button("Enter Marks")
#     st.button("Post Homework")

# st.markdown("---")

# # ---------------------------------------------------------
# # ATTENDANCE SECTION
# # ---------------------------------------------------------
# st.subheader("Attendance")

# selected_class = st.selectbox("Select Class", ["10", "9", "8", "7", "6"])
# selected_section = st.selectbox("Section", ["A", "B", "C"])

# students = get_students_by_class(selected_class, selected_section)

# if not students:
#     st.info("No students found for this class.")
#     st.stop()

# att_date = st.date_input("Date", value=date.today())

# st.write(f"Attendance for Class {selected_class}-{selected_section}")

# status_map = {}

# for s in students:
#     status = st.radio(
#         f"{s['roll_no']} - {s['full_name']}",
#         ["present", "absent"],
#         horizontal=True,
#         key=f"att_{s['id']}",
#     )
#     status_map[s["id"]] = status

# if st.button("Save Attendance"):
#     save_attendance(
#         class_name=f"{selected_class}-{selected_section}",
#         att_date=att_date,
#         teacher_id=teacher_id,
#         status_map=status_map,
#     )
#     st.success("Attendance saved successfully.")

# st.markdown("---")

# # ---------------------------------------------------------
# # MARKS ENTRY SECTION
# # ---------------------------------------------------------
# st.subheader("Marks Entry")

# exam_type = st.selectbox("Exam", ["Unit Test 1", "Unit Test 2", "Half Yearly", "Final"])
# subject = st.selectbox("Subject", ["Mathematics", "Science", "English"])

# st.write(
#     f"Enter marks for **Class {selected_class}-{selected_section}**, **{subject}**, **{exam_type}**"
# )

# marks_entries = []

# for s in students:
#     m = st.number_input(
#         f"{s['roll_no']} - {s['full_name']}",
#         min_value=0,
#         max_value=100,
#         value=0,
#         step=1,
#         key=f"mark_{s['id']}",
#     )

#     marks_entries.append(
#         {
#             "student_id": s["id"],
#             "subject": subject,
#             "exam": exam_type,
#             "marks_obtained": m,
#             "max_marks": 100,
#             "teacher_id": teacher_id,
#         }
#     )

# if st.button("Save Marks"):
#     save_marks(marks_entries)
#     st.success("Marks saved successfully.")

# st.markdown("---")

# # ---------------------------------------------------------
# # LOGOUT
# # ---------------------------------------------------------
# if st.button("Logout"):
#     logout()
