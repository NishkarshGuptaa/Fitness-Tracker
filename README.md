# Fitness Tracker Web App

This is a lightweight fitness tracking web application built using **Flask** and **SQLite**. It allows users to register, log in securely, and record their daily fitness data—such as steps taken, calories burned, and workout minutes. The app features a clean dashboard that displays logs, calculates averages, and provides personalized fitness feedback.

---

## Features

- Secure user registration and login (hashed passwords via Werkzeug)
- Track daily fitness metrics: steps, calories, and workout duration
- Auto-generated averages and fitness level classification
- Smart suggestions based on user activity
- Responsive and modern UI using Bootstrap 5 and custom CSS
- Session-based authentication using Flask's session management
- Simple and maintainable file structure for easy learning or extension

---

## Technologies Used

- **Backend:** Python (Flask)
- **Frontend:** HTML, Bootstrap 5, CSS, Jinja2 templating
- **Database:** SQLite
- **Authentication:** Werkzeug (password hashing)

---

## Getting Started


1. #Clone the Repositery#
```bash
git clone https://github.com/your-username/fitness-tracker.git
cd fitness-tracker

2. #Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate  # Windows

3. #Install Dependencies#
pip install flask werkzeug

4. #Run the App#
python app.py

**Open in Browser**
http://127.0.0.1:5000/


fitness-tracker/
│
├── static/
│   └── style.css               # Custom styles
│
├── templates/
│   ├── base.html               # Common layout
│   ├── index.html              # Landing page
│   ├── login.html              # User login
│   ├── register.html           # New user registration
│   └── dashboard.html          # Fitness dashboard
│
├── app.py                      # Main Flask application
├── database.db                 # SQLite database file (auto-created)
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation



