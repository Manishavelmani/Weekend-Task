import sqlite3

# Database Connection
conn = sqlite3.connect("database/database.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# ===================================
# USERS TABLE for
#Candidate and Employer Details
# ===================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mobile TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,

    work_status TEXT,
    company_name TEXT,
    company_type TEXT,

    skills TEXT,
    experience TEXT,
    profile_image TEXT
)
""")

# ===================================
# JOBS TABLE 
# ===================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs(
    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employer_id INTEGER,
    company_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    location TEXT NOT NULL,
    experience TEXT,
    salary TEXT,
    skills TEXT,
    description TEXT,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(employer_id) REFERENCES users(user_id)
)
""")

# ===================================
# APPLICATIONS TABLE
# ===================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS applications(
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    resume_file TEXT,
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'Pending',

    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(job_id) REFERENCES jobs(job_id),

    UNIQUE(user_id, job_id)   -- ✅ Prevent duplicates at DB level
)
""")

# ===================================
# SAVED JOBS TABLE
# ===================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS saved_jobs(
    save_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    job_id INTEGER,

    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(job_id) REFERENCES jobs(job_id)
)
""")

conn.commit()
conn.close()

print("Database Created Successfully 🚀")