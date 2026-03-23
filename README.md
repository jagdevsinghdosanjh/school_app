# School Management System (Streamlit + Python + MySQL)

A modular, secure, and scalable **School Management System** built with:

- **Streamlit** (UI + routing)
- **Python** (backend logic)
- **MySQL 8 (WAMP)** (local database)
- **Role-Based Access Control (RBAC)** for Admin, Teacher, Student, Parent, Office Staff

This project is designed to be clean, modular, and ready for future cloud deployment.

---

## 🚀 Features

### 🔐 Authentication System
- Secure login with hashed passwords (bcrypt)
- Session-based authentication
- MySQL-backed user storage

### 🛡️ Role-Based Access Control (RBAC)
- Admin
- Principal
- Teacher
- Student
- Parent
- Office Staff

Each role sees different pages and has different permissions.

### 📦 Modular Architecture
school_app/
│
├── app.py
├── auth/
│   ├── auth_manager.py
│   ├── db_manager.py
│   └── init.py
├── pages/
│   ├── 1_Admin_Dashboard.py
│   ├── 2_Teacher_Panel.py
│   ├── 3_Student_Portal.py
│   ├── 4_Parent_Portal.py
│   └── 5_Office_Desk.py
└── .streamlit/
└── secrets.toml

---

## 🗄️ Database Setup (MySQL 8 on WAMP)

Run this in phpMyAdmin:

```sql
CREATE DATABASE IF NOT EXISTS school_mgmt
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE school_mgmt;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100),
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE user_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

INSERT INTO roles (name) VALUES
('admin'), ('principal'), ('teacher'), ('student'), ('parent'), ('office');


🔧 Configuration
Create:

Code
.streamlit/secrets.toml
Add:

toml
[mysql]
host = "localhost"
port = 3306
user = "root"
password = "YOUR_WAMP_PASSWORD"
database = "school_mgmt"
▶️ Running the App
Install dependencies:

bash
pip install -r requirements.txt
Run Streamlit:

bash
streamlit run app.py
🌐 Future Cloud Deployment
This project is designed to migrate easily to:

AWS RDS

PlanetScale

Azure MySQL

Google Cloud SQL

Only the secrets.toml needs to change.

📄 License
MIT License

👨‍💻 Author
Built by Jagdev Singh Dosanjh  
Modular architect • Quant educator • Ed‑tech builder

Code

---

# 🎁 Want me to generate the **full folder structure** with empty files?

I can produce:

- All folders  
- All Python files with boilerplate  
- Admin UI starter  
- User creation script  
- Role assignment script  

Just say **“Generate full project skeleton”** and I’ll build it.
