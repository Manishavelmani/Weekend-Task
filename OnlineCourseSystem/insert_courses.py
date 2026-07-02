import sqlite3

conn = sqlite3.connect("onlinecourse.db")

cursor = conn.cursor()
# Sample courses for the application
# Used to display courses in the courses page
courses = [

    ("Python Programming",
     "Programming",
     "30 Hours",
     "Learn Python from beginner to advanced."),

    ("Flask Development",
     "Web Development",
     "20 Hours",
     "Build web applications using Flask."),

    ("SQL Database",
     "Database",
     "15 Hours",
     "Learn SQL queries and database concepts."),

    ("HTML and CSS",
     "Frontend",
     "18 Hours",
     "Create responsive web pages."),

    ("JavaScript",
     "Frontend",
     "25 Hours",
     "Learn modern JavaScript."),

    ("React JS",
     "Frontend",
     "35 Hours",
     "Build applications using React."),

    ("Node JS",
     "Backend",
     "28 Hours",
     "Server-side programming with Node.js."),

    ("Data Structures",
     "Programming",
     "40 Hours",
     "Learn DSA concepts and problem solving."),

    ("Machine Learning",
     "AI",
     "50 Hours",
     "Introduction to machine learning."),

    ("Bootstrap",
     "Frontend",
     "10 Hours",
     "Responsive website design using Bootstrap."),

    ("Git and GitHub",
     "Tools",
     "12 Hours",
     "Version control using Git and GitHub."),

    ("Python OOP",
     "Programming",
     "20 Hours",
     "Object-oriented programming concepts."),

    ("Advanced Flask",
     "Web Development",
     "25 Hours",
     "Develop advanced Flask applications."),

    ("REST API Development",
     "Backend",
     "22 Hours",
     "Create REST APIs using Flask."),

    ("MongoDB",
     "Database",
     "18 Hours",
     "Learn NoSQL database concepts."),

    ("Django Framework",
     "Web Development",
     "35 Hours",
     "Build web applications using Django."),

    ("Linux Basics",
     "Operating System",
     "15 Hours",
     "Learn Linux commands and administration."),

    ("Docker",
     "DevOps",
     "20 Hours",
     "Containerization using Docker."),

    ("AWS Cloud",
     "Cloud Computing",
     "30 Hours",
     "Introduction to AWS services."),

    ("Cyber Security",
     "Security",
     "25 Hours",
     "Learn security concepts and practices."),

    ("Data Science",
     "AI",
     "40 Hours",
     "Data analysis and visualization."),

    ("Pandas and NumPy",
     "Python",
     "18 Hours",
     "Data analysis using Python libraries."),

    ("Power BI",
     "Analytics",
     "20 Hours",
     "Create business intelligence dashboards."),

    ("C Programming",
     "Programming",
     "22 Hours",
     "Programming fundamentals using C."),

    ("Java Programming",
     "Programming",
     "30 Hours",
     "Object-oriented programming with Java."),

    ("C++ Programming",
     "Programming",
     "28 Hours",
     "Learn C++ and OOP concepts."),

    ("PHP Development",
     "Backend",
     "20 Hours",
     "Build dynamic web applications with PHP."),

    ("Angular",
     "Frontend",
     "30 Hours",
     "Develop modern applications using Angular."),

    ("Artificial Intelligence",
     "AI",
     "45 Hours",
     "Introduction to AI concepts and tools."),

    ("DevOps Fundamentals",
     "DevOps",
     "24 Hours",
     "Learn CI/CD and DevOps practices.")
]

cursor.executemany("""
INSERT INTO courses(
    course_name,
    category,
    duration,
    description
)
VALUES (?, ?, ?, ?)
""", courses)

conn.commit()
conn.close()

print("Courses Added Successfully")