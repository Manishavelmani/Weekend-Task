import sqlite3


# Create database connection
# Used by all user functions

def connect_db():

    conn = sqlite3.connect("onlinecourse.db")

    conn.row_factory = sqlite3.Row

    return conn


# Register a new user account
# Check email uniqueness before insertion

def register_user(name, email, phone, password):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email=?
    """, (email,))

    user = cursor.fetchone()

    if user:

        conn.close()

        return False

    cursor.execute("""
        INSERT INTO users(
            name,
            email,
            phone,
            password
        )
        VALUES (?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        password
    ))

    conn.commit()

    conn.close()

    return True


# Verify user login credentials
# Return user details after login

def login_user(email, password):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email=? AND password=?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    return user


# Get user information
# Used in profile and dashboard

def get_user(user_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE user_id=?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return user


# Update user profile details
# Modify name, email and phone

def update_profile(user_id, name, email, phone):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET name=?,
            email=?,
            phone=?
        WHERE user_id=?
    """, (name, email, phone, user_id))

    conn.commit()

    conn.close()