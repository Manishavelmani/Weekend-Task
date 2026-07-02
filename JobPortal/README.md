# 💼 Job Portal Web Application

The **Job Portal Web Application** is a modern recruitment platform developed using **Python Flask** and **SQLite**. The application is designed to bridge the gap between employers and job seekers by providing a centralized platform for recruitment and job searching. It enables employers to publish job openings, manage applications, and review candidates, while allowing job seekers to search for jobs, apply with resumes, track application status, and maintain professional profiles.

The project follows a modular Flask architecture with a responsive Bootstrap 5 interface, secure session management, and SQLite database integration, providing a smooth and user-friendly experience for both employers and candidates.

---

# 🚀 Features

## 👤 Candidate Features

- Candidate Registration
- Secure Login & Logout
- Browse Available Jobs
- Search Jobs by Title, Experience, and Location
- View Complete Job Details
- Apply for Jobs with Resume Upload
- Save Favorite Jobs
- Track Application Status
- Candidate Dashboard
- Profile & Resume Management

---

## 🏢 Employer Features

- Employer Registration
- Secure Login & Logout
- Post New Job Openings
- Edit Existing Jobs
- Delete Job Listings
- View Applicants
- Preview Candidate Resumes
- Download Candidate Resumes
- Accept or Reject Applications
- Employer Dashboard
- Company Profile Management

---

## 💼 Job Management

The **Job Management** module serves as the core functionality of the application, enabling employers to efficiently create, update, and manage job postings through an intuitive interface. Employers can publish new job opportunities, edit existing job details, and remove inactive job listings whenever required.

Candidates can browse all available job openings, perform advanced searches using filters such as **Job Title**, **Experience**, and **Location**, view detailed job descriptions, save preferred jobs for future reference, and apply directly by uploading their resumes. The application also validates job applications to prevent duplicate submissions, ensuring a smooth and efficient recruitment process for both employers and job seekers.

---

## 💻 System Features

- Role-Based Authentication
- Session Management
- SQLite Database Integration
- Bootstrap 5 Responsive Design
- Secure Resume Upload
- Flash Notifications
- Modular Flask Architecture
- Dynamic Jinja2 Templates

---

# 🛠 Technologies Used

### Backend

- Python
- Flask
- SQLite
- Werkzeug

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- Jinja2

### Development Tools

- PyCharm
- Git
- GitHub

---

# 📂 Project Structure

```text
JobPortal/
│
├── app.py                          # Main Flask application
├── create_db.py                    # Creates database and tables
├── README.md                       # Project documentation
│
├── database/
│   ├── database.db                 # SQLite database
│   ├── user_db.py                  # User authentication & profile operations
│   ├── job_db.py                   # Job management operations
│   └── application_db.py           # Job application operations
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── home.css
│   │   ├── dashboard.css
│   │   ├── profile.css
│   │   ├── job.css
│   │   └── login.css
│   │
│   ├── icons/
│   ├── images/
│   │
│   └── uploads/
│       ├── profile/
│       └── resumes/
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── jobs.html
│   ├── job_details.html
│   ├── candidate_login.html
│   ├── candidate_register.html
│   ├── employer_login.html
│   ├── employer_register.html
│   ├── dashboard_candidate.html
│   ├── dashboard_employer.html
│   ├── profile.html
│   ├── edit_profile.html
│   ├── post_job.html
│   ├── edit_job.html
│   ├── applicants.html
│   ├── saved_jobs.html
│   └── view_resume.html
│
└── .venv/                          # Virtual Environment
```

---

# ⚙ Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Navigate to the Project Folder

```bash
cd JobPortal
```

### 3. Create a Virtual Environment (Optional)

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 5. Install Required Dependencies

```bash
pip install Flask Werkzeug
```

### 6. Create the Database

```bash
python create_db.py
```

### 7. Run the Application

```bash
python app.py
```

### 8. Open the Application

```
http://127.0.0.1:5000
```

---

# 🎯 Project Outcomes

- Developed a complete Job Portal Web Application using Flask.
- Implemented secure role-based authentication for Candidates and Employers.
- Designed responsive user interfaces using Bootstrap 5.
- Performed database operations using SQLite.
- Built a complete job posting and application workflow.
- Implemented secure profile image and resume upload functionality.
- Developed candidate and employer dashboards with application statistics.
- Integrated job search, filtering, saved jobs, and profile management.
- Implemented resume preview and download functionality.

---

# 🚀 Future Enhancements

- Admin Dashboard
- Email Notifications
- Password Hashing with Flask-Bcrypt
- Forgot Password Functionality
- Company Logo Upload
- Pagination for Job Listings
- Interview Scheduling
- AI-Based Resume Parsing
- Job Recommendation System
- Real-Time Notifications

---

# 📌 Conclusion

The **Job Portal Web Application** provides a comprehensive recruitment platform that simplifies the hiring process for employers while helping job seekers discover suitable career opportunities. By combining Flask, SQLite, Bootstrap 5, and Jinja2, the project demonstrates practical implementation of full-stack web development concepts including authentication, database management, file handling, session management, responsive user interface design, and modular application architecture. The project serves as a strong foundation for building scalable recruitment systems and can be further extended with advanced features to meet real-world industry requirements.