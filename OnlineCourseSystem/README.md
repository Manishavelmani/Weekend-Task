# 📚 Online Course Management System

A modern Online Course Management System developed using **Flask** and **SQLite**. The application allows users to register, log in, browse available courses, enroll in courses, track enrolled courses, and manage their profile through a responsive web interface.

---

# 🚀 Features

### 👤 User Features

- User Registration
- Secure Login & Logout
- Session Management
- View Available Courses
- Enroll in Courses
- View Enrolled Courses
- User Dashboard
- Profile Management

### 💻 System Features

- SQLite Database
- Responsive Bootstrap UI
- Modular Flask Structure
- Course Enrollment System
- Database CRUD Operations

---

# 🛠 Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- Jinja2

---

# 📂 Project Structure

```text
OnlineCourseSystem/
│
├── app.py                      # Main Flask application
├── create_db.py                # Creates the database
├── insert_courses.py           # Inserts sample course data
├── onlinecourse.db             # SQLite database
├── README.md                   # Project documentation
│
├── database/
│   ├── user_db.py              # User database operations
│   ├── course_db.py            # Course database operations
│   └── enrollment_db.py        # Enrollment database operations
│
├── static/
│   ├── css/
│   │   ├── style.css           # Common styles
│   │   ├── home.css            # Home page styles
│   │   └── dashboard.css       # Dashboard styles
│   │
│   └── images/                 # Images
│
├── templates/
│   ├── includes/
│   │   ├── navbar.html
│   │   └── footer.html
│   │
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── courses.html
│   ├── mycourses.html
│   └── profile.html
│
└── .venv/                      # Virtual Environment
```

---

# ⚙ Installation Steps

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Navigate to the project folder

```bash
cd OnlineCourseSystem
```

### 3. Create a virtual environment (Optional)

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 5. Install Flask

```bash
pip install flask
```

### 6. Create the database

```bash
python create_db.py
```

### 7. Insert sample course data

```bash
python insert_courses.py
```

### 8. Run the application

```bash
python app.py
```

### 9. Open the browser

```
http://127.0.0.1:5000
```

---

# 🎯 Project Outcomes

- Developed a complete Online Course Management System using Flask.
- Implemented secure user authentication and session management.
- Designed a responsive user interface using Bootstrap.
- Performed database operations using SQLite.
- Built a course enrollment system.
- Implemented profile management functionality.

---

# 🚀 Future Enhancements

- Admin Dashboard
- Certificate Generation
- Online Video Lessons
- Quiz & Assessment Module
- Payment Gateway Integration
- Course Progress Analytics
- Email Notifications

---

# 📌 Conclusion

The Online Course Management System provides an efficient platform for users to register, explore courses, enroll in learning programs, and manage their learning journey. The project demonstrates practical implementation of Flask web development, SQLite database management, authentication, session handling, and responsive web design.