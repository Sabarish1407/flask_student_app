from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)

# ---------- Database Path ----------
DB_PATH = os.path.join(os.path.dirname(__file__), "students.db")

# ---------- Initialize Database ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT NOT NULL,
            dept TEXT NOT NULL,
            year TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ---------- Routes ----------
@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        dept = request.form['dept']
        year = request.form['year']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, roll, dept, year) VALUES (?, ?, ?, ?)",
            (name, roll, dept, year)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('view_students'))

    return render_template('register.html')

@app.route('/view')
def view_students():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('view.html', students=students)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
