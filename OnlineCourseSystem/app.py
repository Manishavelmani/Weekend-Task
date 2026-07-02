from flask import ( Flask, render_template, request, redirect, session, flash)

from datetime import datetime

from database.user_db import ( register_user, login_user,  get_user,  update_profile)

from database.course_db import (  get_courses, search_courses)

from database.enrollment_db import ( enroll_course, get_my_courses, update_progress,get_enrolled_course_ids)

app = Flask(__name__)

app.secret_key = "online_course_secret"


# ======================
# Home Page
# ======================

@app.route("/")
def home():
    return render_template("home.html")


# ======================
# Authentication Routes
# Register, Login and Logout
# ======================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        phone = request.form["phone"]

        password = request.form["password"]

        result = register_user(
            name,
            email,
            phone,
            password
        )

        if result:

            flash(
                "Registration successful.",
                "success"
            )

            return redirect("/login")

        else:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect("/register")

    return render_template("register.html")


# ======================
# Login
# ======================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        user = login_user(email, password)

        if user:

            session["user_id"] = user["user_id"]

            session["name"] = user["name"]

            return redirect("/dashboard")

        else:

            return render_template("login.html", error="Invalid Email or Password")

    return render_template("login.html")


# ======================
# Logout
# ======================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ======================
# Courses
# Get all courses and enrolled course ids
# Used to show "Enrolled" button status
# ======================

@app.route("/courses")
def courses():

    keyword = request.args.get("keyword")

    if keyword:
        all_courses = search_courses(keyword)
    else:
        all_courses = get_courses()

    enrolled_courses = []

    if "user_id" in session:

        user_id = session["user_id"]

        data = get_enrolled_course_ids(user_id)

        for row in data:
            enrolled_courses.append(row["course_id"])

    return render_template(
        "courses.html",
        courses=all_courses,
        enrolled_courses=enrolled_courses
    )

# ======================
# Enroll Course
# Enroll the logged-in user into a course
# Redirect to my courses after enrollment
# ======================

'''@app.route("/enroll/<int:course_id>")
def enroll(course_id):

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    date = datetime.now().strftime("%d-%m-%Y")

    result = enroll_course( user_id,  course_id, date )

    return redirect("/mycourses")'''
@app.route("/enroll/<int:course_id>")
def enroll(course_id):

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    date = datetime.now().strftime("%d-%m-%Y")

    enroll_course(
        user_id,
        course_id,
        date
    )

    flash(
        "Course enrolled successfully.",
        "success"
    )

    return redirect("/mycourses")


# ======================
# My Courses
# ======================

@app.route("/mycourses")
def mycourses():

    if "user_id" not in session:

        return redirect("/login")

    user_id = session["user_id"]

    courses = get_my_courses(user_id)

    return render_template(
        "mycourses.html",
        courses=courses
    )


# ======================
# Update Progress
# ======================

@app.route( "/progress/<int:enrollment_id>", methods=["POST"])
def progress(enrollment_id):

    progress = request.form["progress"]

    update_progress( enrollment_id, progress )

    return redirect("/mycourses")


# ======================
# Dashboard
# Calculate course statistics
# Used for dashboard cards and progress report
# ======================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect("/login")

    user_id = session["user_id"]

    user = get_user(user_id)

    courses = get_my_courses(user_id)

    total_courses = len(courses)

    completed = 0

    in_progress = 0

    total_progress = 0

    for course in courses:

        total_progress += course["progress"]

        if course["progress"] == 100:

            completed += 1

        elif course["progress"] > 0:

            in_progress += 1

    if total_courses > 0:

        completion_rate = int( total_progress / total_courses )

    else:

        completion_rate = 0

    return render_template("dashboard.html",
        user=user,
        courses=courses,
        total_courses=total_courses,
        completed=completed,
        in_progress=in_progress,
        completion_rate=completion_rate
    )


# ======================
# Profile
# View and update user profile
# Display completed course count
# ======================

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        update_profile( user_id,name,email, phone)

        return redirect("/profile")

    user = get_user(user_id)

    courses = get_my_courses(user_id)

    total_courses = len(courses)

    completed = 0

    for course in courses:
        if course["progress"] == 100:
            completed += 1

    return render_template(
        "profile.html",
        user=user,
        total_courses=total_courses,
        completed=completed
    )
# Update course progress percentage
# Show success message after update
@app.route("/update_progress/<int:enrollment_id>",
           methods=["POST"])
def update_course_progress(enrollment_id):

    if "user_id" not in session:
        return redirect("/login")

    progress = request.form["progress"]

    update_progress( enrollment_id, progress)

    flash(
        "Progress updated successfully.",
        "success"
    )

    return redirect("/mycourses")



# ======================
# Run Flask
# ======================

if __name__ == "__main__":

    app.run(debug=True)