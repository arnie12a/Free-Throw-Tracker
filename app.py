import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM freethrowlog').fetchall()
    print(logs)
    conn.close()
    return render_template('index.html', logs=logs)

if __name__ == '__main__':  
   app.run(debug=True)