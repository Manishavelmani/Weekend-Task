# ==========================================
# Import Required Libraries
# ==========================================
# Imports Flask modules and required Python libraries.
# Used throughout the application.
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    send_from_directory
)

from datetime import date
from werkzeug.utils import secure_filename

# ==========================================
# User Database Functions
# ==========================================
# Imports functions related to user registration,
# login, and profile management.
from database.user_db import (
    register_user,
    login_user,
    get_user,
    update_profile,
    update_employer_profile
)

# ==========================================
# Job Database Functions
# ==========================================
# Imports functions for creating, updating,
# searching, and managing job postings.
from database.job_db import (
    add_job,
    get_all_jobs,
    get_job_by_id,
    get_employer_jobs,
    update_job,
    delete_job,
    search_jobs,
    get_saved_jobs,
    connect_db
)
# ==========================================
# Application Database Functions
# ==========================================
# Imports functions related to job applications
# and application status management.
from database.application_db import (
    apply_job,
    get_user_applications,
    get_job_applications,
    update_status,
    already_applied
)

# ==========================================
# Flask Application Configuration
# ==========================================
# Creates the Flask application and
# sets the secret key for session management.
app = Flask(__name__)
app.secret_key = "jobportal"


# ==========================================
# Home Page Routes
# ==========================================
# Displays the home page with available jobs.
# Loads job data from the database.
@app.route("/")
def home():
    jobs = get_all_jobs()
    return render_template("home.html", jobs=jobs)

# ==========================================
# Logout Route
# ==========================================
# Clears the current user session
# and redirects to the home page.
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ==========================================
# Job Search Routes
# ==========================================
# Searches jobs using keyword,
# experience, and location filters.
@app.route("/jobs")
def jobs():

    keyword    = request.args.get("keyword", "").strip()
    experience = request.args.get("experience", "").strip()
    location   = request.args.get("location", "").strip()

    # Empty search prevent
    if request.args and not (keyword or experience or location):
        flash("Please enter at least one search field!")
        return redirect("/jobs")

    jobs = search_jobs(keyword, experience, location)

    return render_template(
        "jobs.html",
        jobs=jobs,
        keyword=keyword,
        experience=experience,
        location=location
    )

# ==========================================
# Home Search Redirect
# ==========================================
# Redirects the search request
# from the home page to the jobs page.
@app.route("/search")
def search():

    keyword = request.args.get("keyword", "").strip()

    if not keyword:
        flash("Please enter a keyword to search!")
        return redirect("/")

    return redirect(f"/jobs?keyword={keyword}")

# ==========================================
# Job Details Route
# ==========================================
# Displays complete information
# about a selected job.
@app.route("/job/<int:job_id>")
def job_details(job_id):

    job = get_job_by_id(job_id)

    is_applied = False
    if "user_id" in session and session.get("role") == "Candidate":
        is_applied = already_applied(session["user_id"], job_id)

    return render_template(
        "job_details.html",
        job=job,
        is_applied=is_applied
    )

# ==========================================
# Employer Dashboard
# ==========================================
# Displays jobs posted by the employer
# along with application statistics.

@app.route("/employer_dashboard")
def employer_dashboard():

    if "user_id" not in session:
        return redirect("/employer_login")

    if session["role"] != "Employer":
        return redirect("/")

    jobs = get_employer_jobs(session["user_id"])

    total_applications = 0
    for job in jobs:
        apps = get_job_applications(job["job_id"])
        total_applications += len(apps)

    return render_template(
        "dashboard_employer.html",
        jobs=jobs,
        total_applications=total_applications
    )

# ==========================================
# Candidate Dashboard
# ==========================================
# Displays candidate applications
# and application status summary.
@app.route("/candidate_dashboard")
def candidate_dashboard():

    if "user_id" not in session:
        return redirect("/candidate_login")

    if session["role"] != "Candidate":
        return redirect("/")

    applications = get_user_applications(session["user_id"])

    applied_count  = len(applications)
    pending_count  = len([a for a in applications if a["status"] == "Pending"])
    accepted_count = len([a for a in applications if a["status"] == "Accepted"])
    rejected_count = len([a for a in applications if a["status"] == "Rejected"])

    user = get_user(session["user_id"])

    return render_template(
        "dashboard_candidate.html",
        user=user,
        applications=applications,
        applied_count=applied_count,
        pending_count=pending_count,
        accepted_count=accepted_count,
        rejected_count=rejected_count
    )

# ==========================================
# Add New Job
# ==========================================
# Allows employers
# to create and publish a new job.
@app.route("/add_job", methods=["GET", "POST"])
def add_new_job():

    if "user_id" not in session:
        return redirect("/employer_login")

    if session["role"] != "Employer":
        return redirect("/")

    # ✅ Get employer from DB
    employer = get_user(session["user_id"])

    if request.method == "POST":

        add_job(
            session["user_id"],
            employer["company_name"],  # ✅ DB from auto
            request.form["job_title"],
            request.form["location"],
            request.form["experience"],
            request.form["salary"],
            request.form["skills"],
            request.form["description"],
            str(date.today())
        )

        flash("Job Posted Successfully ✅")
        return redirect("/employer_dashboard")

    return render_template(
        "post_job.html",
        employer=employer
    )

# ==========================================
# Edit Existing Job
# ==========================================
# Allows employers
# to update job information.

@app.route("/edit_job/<int:job_id>", methods=["GET", "POST"])
def edit_job(job_id):

    if "user_id" not in session:
        return redirect("/employer_login")

    if session["role"] != "Employer":
        return redirect("/")

    job      = get_job_by_id(job_id)
    employer = get_user(session["user_id"])

    if request.method == "POST":

        update_job(
            job_id,
            employer["company_name"],  # ✅ DB from auto
            request.form["job_title"],
            request.form["location"],
            request.form["experience"],
            request.form["salary"],
            request.form["skills"],
            request.form["description"]
        )

        flash("Job Updated Successfully ✅")
        return redirect("/employer_dashboard")

    return render_template(
        "edit_job.html",
        job=job
    )


# ==========================
# Delete Job
# ==========================
@app.route("/delete_job/<int:job_id>")
def remove_job(job_id):

    if "user_id" not in session:
        return redirect("/employer_login")

    if session["role"] != "Employer":
        return redirect("/")

    delete_job(job_id)
    flash("Job Deleted ✅")
    return redirect("/employer_dashboard")


# ==========================
# Apply Job
# ==========================
@app.route("/apply/<int:job_id>", methods=["POST"])
def apply(job_id):

    if "user_id" not in session:
        return redirect("/candidate_login")

    if session["role"] != "Candidate":
        return redirect("/")

    # Duplicate check
    if already_applied(session["user_id"], job_id):
        flash("You have already applied for this job!")
        return redirect(f"/job/{job_id}")

    # Resume validation
    resume = request.files.get("resume")

    if not resume or resume.filename == "":
        flash("Please upload your resume!")
        return redirect(f"/job/{job_id}")

    filename = secure_filename(resume.filename)
    resume.save("static/uploads/resumes/" + filename)

    apply_job(
        session["user_id"],
        job_id,
        filename,
        str(date.today())
    )

    flash("Application Submitted Successfully ✅")
    return redirect("/candidate_dashboard")


# ==========================
# Applicants
# ==========================
@app.route("/applicants/<int:job_id>")
def applicants(job_id):

    if "user_id" not in session:
        return redirect("/employer_login")

    if session["role"] != "Employer":
        return redirect("/")

    applications = get_job_applications(job_id)

    return render_template(
        "applicants.html",
        applications=applications
    )


# ==========================
# Update Status
# ==========================
@app.route("/update_status/<int:application_id>/<status>")
def change_status(application_id, status):

    if "user_id" not in session:
        return redirect("/employer_login")

    if session["role"] != "Employer":
        return redirect("/")

    update_status(application_id, status)
    flash(f"Status Updated to {status} ✅")
    return redirect(request.referrer or "/employer_dashboard")


# ==========================
# Save Job
# ==========================
@app.route("/save_job/<int:job_id>")
def save_job(job_id):

    if "user_id" not in session:
        return redirect("/candidate_login")

    if session["role"] != "Candidate":
        return redirect("/")

    conn   = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM saved_jobs
        WHERE user_id = ? AND job_id = ?
    """, (session["user_id"], job_id))

    existing = cursor.fetchone()

    if existing:
        flash("Job Already Saved!")
    else:
        cursor.execute("""
            INSERT INTO saved_jobs (user_id, job_id)
            VALUES (?, ?)
        """, (session["user_id"], job_id))
        conn.commit()
        flash("Job Saved Successfully ✅")

    conn.close()
    return redirect("/saved_jobs")


# ==========================
# Saved Jobs Page
#Displays all jobs saved by the candidate.
# ==========================
@app.route("/saved_jobs")
def saved_jobs():

    if "user_id" not in session:
        return redirect("/candidate_login")

    if session["role"] != "Candidate":
        return redirect("/")

    jobs = get_saved_jobs(session["user_id"])

    return render_template("saved_jobs.html", jobs=jobs)


# ==========================
# View Resume (No Blink)
# ==========================
@app.route("/resume/<filename>")
def view_resume(filename):

    return send_from_directory(
        "static/uploads/resumes",
        filename,
        mimetype="application/pdf"
    )


# ==========================
# 2. Show Resume Viewer Page
#view the resume in the same page
# ==========================
@app.route("/view_resume_page/<filename>")
def view_resume_page(filename):
    if "user_id" not in session:
        return redirect("/")

    return render_template("view_resume.html", filename=filename)

# ==========================
# Profile
# Displays user profile information along with related statistics.
# ==========================
@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/")

    user = get_user(session["user_id"])

    applied_count      = 0
    saved_count        = 0
    accepted_count     = 0
    total_jobs         = 0
    total_applications = 0
    latest_resume      = None

    if user["role"] == "Candidate":

        applications   = get_user_applications(session["user_id"])
        applied_count  = len(applications)
        accepted_count = len(
            [a for a in applications if a["status"] == "Accepted"]
        )

        saved       = get_saved_jobs(session["user_id"])
        saved_count = len(saved)

        # Resume - profile first, then application
        if user["resume_file"]:
            latest_resume = user["resume_file"]
        elif applications:
            latest_resume = applications[0]["resume_file"]

    else:

        jobs       = get_employer_jobs(session["user_id"])
        total_jobs = len(jobs)

        for job in jobs:
            apps = get_job_applications(job["job_id"])
            total_applications += len(apps)

    return render_template(
        "profile.html",
        user=user,
        applied_count=applied_count,
        saved_count=saved_count,
        accepted_count=accepted_count,
        total_jobs=total_jobs,
        total_applications=total_applications,
        latest_resume=latest_resume
    )


# ==========================
# Edit Profile
# Allows users to update their profile and resume.
# ==========================
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:
        return redirect("/")

    user = get_user(session["user_id"])

    # Latest resume
    latest_resume = None

    if user["role"] == "Candidate":
        if user["resume_file"]:
            latest_resume = user["resume_file"]
        else:
            applications = get_user_applications(session["user_id"])
            if applications:
                latest_resume = applications[0]["resume_file"]

    if request.method == "POST":

        # Profile Image
        filename = user["profile_image"]

        if "profile" in request.files:
            image = request.files["profile"]
            if image.filename != "":
                filename = secure_filename(image.filename)
                image.save("static/uploads/profile/" + filename)

        # Candidate Update
        if user["role"] == "Candidate":

            resume_filename = None

            if "resume" in request.files:
                resume = request.files["resume"]
                if resume.filename != "":
                    resume_filename = secure_filename(resume.filename)
                    resume.save(
                        "static/uploads/resumes/" + resume_filename
                    )

            update_profile(
                session["user_id"],
                request.form["name"],
                request.form["mobile"],
                request.form.get("skills", ""),
                request.form.get("experience", ""),
                filename,
                resume_filename
            )

        # Employer Update
        else:

            update_employer_profile(
                session["user_id"],
                request.form["name"],
                request.form["mobile"],
                request.form.get("company_name", ""),
                request.form.get("company_type", ""),
                request.form.get("about_company", ""),
                filename
            )

        flash("Profile Updated Successfully ✅")
        return redirect("/profile")

    return render_template(
        "edit_profile.html",
        user=user,
        latest_resume=latest_resume
    )


# ==========================
# Candidate Register
# Registers a new candidate in the system.
# ==========================
@app.route("/candidate_register", methods=["GET", "POST"])
def candidate_register():

    if request.method == "POST":

        register_user(
            request.form["name"],
            request.form["email"],
            request.form["mobile"],
            request.form["password"],
            "Candidate",
            request.form["work_status"]
        )

        flash("Registered Successfully ✅")
        return redirect("/candidate_login")

    return render_template("candidate_register.html")


# ==========================
# Employer Register
# Registers a new employer in the system.
# ==========================
@app.route("/employer_register", methods=["GET", "POST"])
def employer_register():

    if request.method == "POST":

        register_user(
            request.form["name"],
            request.form["email"],
            request.form["mobile"],
            request.form["password"],
            "Employer",
            "",
            request.form["company_name"],
            request.form["company_type"]
        )

        flash("Registered Successfully ✅")
        return redirect("/employer_login")

    return render_template("employer_register.html")


# ==========================
# Candidate Login
# Authenticates candidate credentials
# and creates a user session.
# ==========================
@app.route("/candidate_login", methods=["GET", "POST"])
def candidate_login():

    if request.method == "POST":

        user = login_user(
            request.form["email"],
            request.form["password"]
        )

        if user and user["role"] == "Candidate":

            session["user_id"]       = user["user_id"]
            session["name"]          = user["name"]
            session["role"]          = user["role"]
            session["profile_image"] = user["profile_image"]

            flash("Login Successful ✅")
            return redirect("/candidate_dashboard")

        flash("Invalid Login Credentials!")

    return render_template("candidate_login.html")


# ==========================
# Employer Login
# Authenticates employer credentials
# and creates a user session.
# ==========================
@app.route("/employer_login", methods=["GET", "POST"])
def employer_login():

    if request.method == "POST":

        user = login_user(
            request.form["email"],
            request.form["password"]
        )

        if user and user["role"] == "Employer":

            session["user_id"] = user["user_id"]
            session["name"]    = user["name"]
            session["role"]    = user["role"]

            flash("Login Successful ✅")
            return redirect("/employer_dashboard")

        flash("Invalid Login Credentials!")

    return render_template("employer_login.html")


# ==========================
# Run App
# Starts the Flask development server
# in debug mode.
# ==========================
if __name__ == "__main__":
    app.run(debug=True)