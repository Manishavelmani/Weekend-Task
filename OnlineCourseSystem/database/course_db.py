import sqlite3
#sqlite connection
# Create database connection
# Used by all course functions

def connect_db():
    conn = sqlite3.connect("onlinecourse.db")
    conn.row_factory = sqlite3.Row
    return conn

#courses details
# Get all available courses
# Display courses in courses page
def get_courses():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM courses""")

    courses = cursor.fetchall()

    conn.close()

    return courses

#search course
# Search courses by name
# Used in course search feature
def search_courses(keyword):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM courses WHERE course_name LIKE ?""", ('%' + keyword + '%',))

    courses = cursor.fetchall()

    conn.close()

    return courses


# Get single course details
# Find course using course id

def get_course(course_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM courses WHERE course_id=?""", (course_id,))

    course = cursor.fetchone()

    conn.close()

    return course