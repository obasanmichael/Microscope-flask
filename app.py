from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("specimens.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS specimens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            microscope_size REAL,
            magnification REAL,
            actual_size REAL
        )
    ''')
    conn.commit()
    conn.close()

def fetch_all_data():
    conn = sqlite3.connect("specimens.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM specimens")
    rows = cursor.fetchall()
    conn.close()
    return rows

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    all_records = fetch_all_data()

    if request.method == "POST":
        username = request.form["username"]
        microscope_size = float(request.form["microscope_size"])
        magnification = float(request.form["magnification"])
        actual_size = microscope_size / magnification
        result = actual_size

        conn = sqlite3.connect("specimens.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO specimens (username, microscope_size, magnification, actual_size) VALUES (?, ?, ?, ?)",
                       (username, microscope_size, magnification, actual_size))
        conn.commit()
        conn.close()

        all_records = fetch_all_data()  # Refresh the table after insert

    return render_template("index.html", result=result, records=all_records)

if __name__ == "__main__":
    app.run(debug=True)
