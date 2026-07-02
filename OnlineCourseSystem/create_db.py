import sqlite3

conn = sqlite3.connect("onlinecourse.db")

cursor = conn.cursor()

# Store user account information
# Used for registration and login

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Store available course details
# Used in courses page

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses(
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    category TEXT,
    duration TEXT,
    description TEXT
)
""")

# Store enrolled courses and progress
# Connects users and courses

cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments(
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    course_id INTEGER,
    progress INTEGER DEFAULT 0,
    enrollment_date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")