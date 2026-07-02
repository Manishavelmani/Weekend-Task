import sqlite3


# ==========================
# Database Connection
# ==========================
def connect_db():
    conn = sqlite3.connect("database/database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ==========================
# Register User
# ==========================
def register_user(
    name,
    email,
    mobile,
    password,
    role,
    work_status="",
    company_name="",
    company_type=""
):

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users(
                name,
                email,
                mobile,
                password,
                role,
                work_status,
                company_name,
                company_type,
                skills,
                experience,
                profile_image
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            mobile,
            password,
            role,
            work_status,
            company_name,
            company_type,
            "",
            "",
            "default.png"
        ))

        conn.commit()
        return True

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        conn.close()


# ==========================
# Login User
# ==========================
def login_user(email, password):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email = ?
        AND password = ?
    """, (email, password))

    user = cursor.fetchone()
    conn.close()

    return user


# ==========================
# Get User By ID
# ==========================
def get_user(user_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    user = cursor.fetchone()
    conn.close()

    return user


# ==========================
# Update Candidate Profile
# ==========================
def update_profile(
    user_id,
    name,
    mobile,
    skills,
    experience,
    profile_image,
    resume_file=None
):

    try:
        conn = connect_db()
        cursor = conn.cursor()

        if resume_file:

            cursor.execute("""
                UPDATE users
                SET name          = ?,
                    mobile        = ?,
                    skills        = ?,
                    experience    = ?,
                    profile_image = ?,
                    resume_file   = ?
                WHERE user_id = ?
            """, (
                name,
                mobile,
                skills,
                experience,
                profile_image,
                resume_file,
                user_id
            ))

        else:

            cursor.execute("""
                UPDATE users
                SET name          = ?,
                    mobile        = ?,
                    skills        = ?,
                    experience    = ?,
                    profile_image = ?
                WHERE user_id = ?
            """, (
                name,
                mobile,
                skills,
                experience,
                profile_image,
                user_id
            ))

        conn.commit()
        return True

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        conn.close()


# ==========================
# Update Employer Profile
# ==========================
def update_employer_profile(
    user_id,
    name,
    mobile,
    company_name,
    company_type,
    about_company,
    profile_image
):

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET name          = ?,
                mobile        = ?,
                company_name  = ?,
                company_type  = ?,
                about_company = ?,
                profile_image = ?
            WHERE user_id = ?
        """, (
            name,
            mobile,
            company_name,
            company_type,
            about_company,
            profile_image,
            user_id
        ))

        conn.commit()
        return True

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        conn.close()