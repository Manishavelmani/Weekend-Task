import sqlite3


def connect_db():
    conn = sqlite3.connect("database/database.db")
    conn.row_factory = sqlite3.Row
    return conn


def add_job(employer_id, company_name, job_title,
            location, experience, salary, skills,
            description, posted_date):

    conn   = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO jobs (
            employer_id, company_name, job_title,
            location, experience, salary, skills,
            description, posted_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        employer_id, company_name, job_title,
        location, experience, salary, skills,
        description, posted_date
    ))

    conn.commit()
    conn.close()


def get_all_jobs():

    conn   = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM jobs
        ORDER BY job_id DESC
    """)

    jobs = cursor.fetchall()
    conn.close()
    return jobs


def get_employer_jobs(employer_id):

    conn   = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM jobs
        WHERE employer_id = ?
        ORDER BY job_id DESC
    """, (employer_id,))

    jobs = cursor.fetchall()
    conn.close()
    return jobs


def get_job_by_id(job_id):

    conn   = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM jobs
        WHERE job_id = ?
    """, (job_id,))

    job = cursor.fetchone()
    conn.close()
    return job


def update_job(job_id, company_name, job_title,
               location, experience, salary,
               skills, description):

    conn   = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET company_name = ?,
            job_title    = ?,
            location     = ?,
            experience   = ?,
            salary       = ?,
            skills       = ?,
            description  = ?
        WHERE job_id = ?
    """, (
        company_name, job_title, location,
        experience, salary, skills,
        description, job_id
    ))

    conn.commit()
    conn.close()


def delete_job(job_id):

    conn   = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM jobs
        WHERE job_id = ?
    """, (job_id,))

    conn.commit()
    conn.close()


# ===================================
# Search Jobs (keyword + experience + location)
# ===================================
def search_jobs(keyword="", experience="", location=""):

    conn   = connect_db()
    cursor = conn.cursor()

    query  = "SELECT * FROM jobs WHERE 1=1"
    params = []

    if keyword:
        query += """
            AND (
                job_title    LIKE ? OR
                company_name LIKE ? OR
                skills       LIKE ?
            )
        """
        params.extend([
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ])

    if experience:
        query += " AND experience LIKE ?"
        params.append(f"%{experience}%")

    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")

    query += " ORDER BY job_id DESC"

    cursor.execute(query, params)

    jobs = cursor.fetchall()
    conn.close()
    return jobs


def get_saved_jobs(user_id):

    conn   = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT jobs.*
        FROM saved_jobs
        JOIN jobs ON saved_jobs.job_id = jobs.job_id
        WHERE saved_jobs.user_id = ?
        ORDER BY jobs.job_id DESC
    """, (user_id,))

    jobs = cursor.fetchall()
    conn.close()
    return jobs