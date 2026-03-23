import streamlit as st
from auth.auth_manager import is_authenticated, has_role
from db.base import get_connection

# -------------------------
# ACCESS CONTROL
# -------------------------
if not is_authenticated():
    st.error("Login required")
    st.stop()

if not has_role("admin", "principal", "dba"):
    st.error("Access denied")
    st.stop()

st.title("System Meta Dashboard")
st.caption("Complete meta-state of the school_mgmt database.")


# -------------------------
# HELPER FUNCTIONS
# -------------------------
def get_table_list():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    tables = [t[0] for t in cur.fetchall()]
    cur.close()
    conn.close()
    return tables


def get_row_count(table):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return int(count)


def get_table_size(table):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT 
            ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb
        FROM information_schema.TABLES
        WHERE table_schema = 'school_mgmt' AND table_name = %s
        """,
        (table,),
    )
    size = cur.fetchone()[0]
    cur.close()
    conn.close()
    return float(size) if size is not None else 0.0


# def get_table_size(table):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """
#         SELECT
#             ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb
#         FROM information_schema.TABLES
#         WHERE table_schema = 'school_mgmt' AND table_name = %s
#     """,
#         (table,),
#     )
#     size = cur.fetchone()[0]
#     cur.close()
#     conn.close()
#     return size


def get_last_update(table):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT UPDATE_TIME 
        FROM information_schema.tables 
        WHERE TABLE_SCHEMA='school_mgmt' AND TABLE_NAME=%s
        """,
        (table,),
    )
    ts = cur.fetchone()[0]
    cur.close()
    conn.close()

    # Convert datetime → string for Streamlit metric
    return ts.strftime("%Y-%m-%d %H:%M:%S") if ts else "—"


# def get_last_update(table):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """
#         SELECT UPDATE_TIME
#         FROM information_schema.tables
#         WHERE TABLE_SCHEMA='school_mgmt' AND TABLE_NAME=%s
#     """,
#         (table,),
#     )
#     ts = cur.fetchone()[0]
#     cur.close()
#     conn.close()
#     return ts or "—"


def get_fk_relations():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT 
            TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA='school_mgmt' AND REFERENCED_TABLE_NAME IS NOT NULL
    """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def run_consistency_checks():
    conn = get_connection()
    cur = conn.cursor()

    checks = {}

    # Students without parents
    cur.execute(
        """
        SELECT s.id, s.full_name 
        FROM students s
        LEFT JOIN parent_child pc ON pc.student_id = s.id
        WHERE pc.student_id IS NULL
    """
    )
    checks["students_without_parents"] = cur.fetchall()

    # Parents without children
    cur.execute(
        """
        SELECT p.id, p.full_name 
        FROM parents p
        LEFT JOIN parent_child pc ON pc.parent_user_id = p.id
        WHERE pc.parent_user_id IS NULL
    """
    )
    checks["parents_without_children"] = cur.fetchall()

    # Teachers without class assignments
    cur.execute(
        """
        SELECT u.id, u.full_name
        FROM users u
        JOIN user_roles ur ON ur.user_id = u.id
        JOIN roles r ON r.id = ur.role_id
        LEFT JOIN teacher_classes tc ON tc.teacher_id = u.id
        WHERE r.name='teacher' AND tc.id IS NULL
    """
    )
    checks["teachers_without_classes"] = cur.fetchall()

    # Students without fee records
    cur.execute(
        """
        SELECT s.id, s.full_name
        FROM students s
        LEFT JOIN fee_payments f ON f.student_id = s.id
        WHERE f.student_id IS NULL
    """
    )
    checks["students_without_fee_records"] = cur.fetchall()

    cur.close()
    conn.close()
    return checks


# -------------------------
# TABLE META OVERVIEW
# -------------------------
st.header("📊 Database Tables Overview")

tables = get_table_list()

for table in tables:
    with st.expander(f"Table: {table}"):
        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", get_row_count(table))
        col2.metric("Size (MB)", get_table_size(table))
        col3.metric("Last Updated", get_last_update(table))

st.markdown("---")

# -------------------------
# FOREIGN KEY RELATIONSHIPS
# -------------------------
st.header("🔗 Foreign Key Relationships")

relations = get_fk_relations()

for r in relations:
    st.write(f"**{r[0]}.{r[1]} → {r[2]}.{r[3]}**")

st.markdown("---")

# -------------------------
# CONSISTENCY CHECKS
# -------------------------
st.header("🧪 Data Consistency Checks")

checks = run_consistency_checks()

for key, rows in checks.items():
    st.subheader(key.replace("_", " ").title())
    if not rows:
        st.success("No issues found.")
    else:
        for r in rows:
            st.error(f"{r[0]} — {r[1]}")
