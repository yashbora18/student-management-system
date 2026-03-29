from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

DB_PATH = "students.db"

# Connect DB
def get_db():
    return sqlite3.connect(DB_PATH)

# Create table
def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll TEXT,
            class TEXT
        )
    """)
    conn.commit()
    conn.close()

# 🔥 IMPORTANT: create table when app starts (for Render)
create_table()

# Home page
@app.route('/')
def home():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html", students=students)

# Add student
@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        clas = request.form['class']

        conn = get_db()
        conn.execute(
            "INSERT INTO students (name, roll, class) VALUES (?, ?, ?)",
            (name, roll, clas)
        )
        conn.commit()
        conn.close()

        flash("Student added successfully!")
        return redirect('/')

    return render_template("add.html")

# Delete student
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Edit student
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    conn = get_db()

    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        clas = request.form['class']

        conn.execute(
            "UPDATE students SET name=?, roll=?, class=? WHERE id=?",
            (name, roll, clas, id)
        )
        conn.commit()
        conn.close()
        return redirect('/')

    student = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", student=student)

# Search
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    conn = get_db()
    students = conn.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%' + keyword + '%',)
    ).fetchall()
    conn.close()
    return render_template("index.html", students=students)

# Run locally
if __name__ == '__main__':
    app.run(debug=True)