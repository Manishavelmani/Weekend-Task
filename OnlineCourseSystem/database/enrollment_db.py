import sqlite3


# Create database connection
# Used by all enrollment functions

def connect_db():

    conn = sqlite3.connect("onlinecourse.db")

    conn.row_factory = sqlite3.Row

    return conn


# Enroll user into a course
# Prevent duplicate enrollments

def enroll_course(user_id, course_id, date):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM enrollments
        WHERE user_id=? AND course_id=?
    """, (user_id, course_id))

    existing = cursor.fetchone()

    if existing:

        conn.close()

        return False

    cursor.execute("""
        INSERT INTO enrollments(
            user_id,
            course_id,
            progress,
            enrollment_date
        )
        VALUES (?, ?, ?, ?)
    """, (user_id, course_id, 0, date))

    conn.commit()

    conn.close()

    return True


# Get enrolled courses of a user
# Used in My Courses page

def get_my_courses(user_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            enrollments.enrollment_id,
            courses.course_id,
            courses.course_name,
            courses.category,
            courses.duration,
            enrollments.progress,
            enrollments.enrollment_date

        FROM enrollments
        JOIN courses
        ON enrollments.course_id = courses.course_id

        WHERE enrollments.user_id=?
    """, (user_id,))

    courses = cursor.fetchall()

    conn.close()

    return courses


# Update course progress percentage
# Used in progress tracking

def update_progress(enrollment_id, progress):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE enrollments
        SET progress=?
        WHERE enrollment_id=?
    """, (progress, enrollment_id))

    conn.commit()

    conn.close()


# Count total enrolled courses
# Used in dashboard statistics

def get_total_courses(user_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM enrollments
        WHERE user_id=?
    """, (user_id,))

    total = cursor.fetchone()[0]

    conn.close()

    return total


# Count completed courses
# Progress value should be 100

def get_completed_courses(user_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM enrollments
        WHERE user_id=? AND progress=100
    """, (user_id,))

    completed = cursor.fetchone()[0]

    conn.close()

    return completed


# Count ongoing courses
# Progress value is less than 100

def get_in_progress_courses(user_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM enrollments
        WHERE user_id=? AND progress < 100
    """, (user_id,))

    progress = cursor.fetchone()[0]

    conn.close()

    return progress


# Get enrolled course ids
# Used to disable enroll button

def get_enrolled_course_ids(user_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT course_id
        FROM enrollments
        WHERE user_id=?
    """, (user_id,))

    courses = cursor.fetchall()

    conn.close()

    return courses