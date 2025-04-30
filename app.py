from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS fitness (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            steps INTEGER,
            calories INTEGER,
            workout INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.close()

init_db()

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('database.db')
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists!"
        finally:
            conn.close()
        return redirect('/login')
    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            return redirect('/dashboard')
        return "Invalid credentials"
    return render_template('login.html')

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')

    if request.method == 'POST':
        date = request.form['date']
        steps = int(request.form['steps'])
        calories = int(request.form['calories'])
        workout = int(request.form['workout'])

        conn.execute('''
            INSERT INTO fitness (user_id, date, steps, calories, workout)
            VALUES (?, ?, ?, ?, ?)
        ''', (session['user_id'], date, steps, calories, workout))
        conn.commit()

    # Fetch all logs
    data = conn.execute('''
        SELECT date, steps, calories, workout FROM fitness
        WHERE user_id = ?
        ORDER BY date DESC
    ''', (session['user_id'],)).fetchall()

    # Calculate averages
    stats = conn.execute('''
        SELECT AVG(steps), AVG(calories), AVG(workout)
        FROM fitness WHERE user_id = ?
    ''', (session['user_id'],)).fetchone()

    avg_steps = stats[0] or 0
    avg_calories = stats[1] or 0
    avg_workout = stats[2] or 0

    # Determine fitness level
    if avg_steps >= 8000 and avg_calories >= 300 and avg_workout >= 30:
        level = "Good"
        suggestion = "Keep up the good work!"
    elif avg_steps >= 5000 or avg_workout >= 20:
        level = "Average"
        suggestion = "Doing okay! Try to increase steps and workout time."
    else:
        level = "Needs Improvement"
        suggestion = "Start with small goals. Walk more and exercise at least 15–20 mins daily."

    conn.close()

    return render_template('dashboard.html', data=data, level=level, suggestion=suggestion,
                           avg_steps=int(avg_steps), avg_calories=int(avg_calories), avg_workout=int(avg_workout))

@app.route('/logout')
def logout():
    print("Logging out user")
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
