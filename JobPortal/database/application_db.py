import sqlite3


# ==========================
# Database Connection
# ==========================
def connect_db():
    conn = sqlite3.connect("database/database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ==========================
# Apply Job
# ==========================
def apply_job(user_id,
              job_id,
              resume_file,
              applied_date):

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO applications(
                user_id,
                job_id,
                resume_file,
                applied_date
            )
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            job_id,
            resume_file,
            applied_date
        ))

        conn.commit()
        return True

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        conn.close()


# ==========================
# Candidate Applications
# ==========================
def get_user_applications(user_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT applications.*,
               jobs.job_title,
               jobs.company_name
        FROM applications

        JOIN jobs
        ON applications.job_id = jobs.job_id

        WHERE applications.user_id = ?

        ORDER BY application_id DESC
    """, (user_id,))

    applications = cursor.fetchall()

    conn.close()

    return applications


# ==========================
# Employer View Applicants
# ==========================
def get_job_applications(job_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT applications.*,
               users.name,
               users.email,
               users.mobile

        FROM applications

        JOIN users
        ON applications.user_id = users.user_id

        WHERE applications.job_id = ?

        ORDER BY application_id DESC
    """, (job_id,))

    applications = cursor.fetchall()

    conn.close()

    return applications

# ==========================
# Check Already Applied
# ==========================
def already_applied(user_id, job_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                SELECT * FROM applications
                WHERE user_id = ? AND job_id = ?
            """, (user_id, job_id))

    result = cursor.fetchone()
    conn.close()

    return result is not None

# ==========================
# Update Status
# ==========================

def update_status(application_id,
                  status):

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE applications
            SET status = ?
            WHERE application_id = ?
        """, (
            status,
            application_id
        ))

        conn.commit()
        return True

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        conn.close()


# ==========================
# Delete Application
# ==========================
def delete_application(application_id):

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM applications
            WHERE application_id = ?
        """, (application_id,))

        conn.commit()
        return True

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        conn.close()


