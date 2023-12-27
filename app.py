import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Connecting to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# The root
@app.route('/')
def index():
    return render_template('index.html')

# Page that has the log where you can edit and delete data in database
@app.route('/freethrowlog')
def freethrowlog():
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM freethrowlog').fetchall()
    conn.close()
    return render_template('log.html', logs=logs)

# Page for statistics and has dashboard
@app.route('/statistics')
def statistics():
    return render_template('stats.html')

# Add free throw session to the database
@app.route('/add', methods = ["GET", "POST"])
def add():
    if request.method == "POST":

        date = str(request.form.get("date"))
        ftmade = request.form.get("ftmade")
        ftattempted = request.form.get("ftattempted")

        # Do some validation
        if date and ftmade and ftattempted:
            if ftattempted > ftmade:
                conn = get_db_connection()
                conn.execute("INSERT INTO freethrowlog (sessionDate, ftMade, ftAttempted) VALUES (?, ?, ?)",
                    (date, ftmade, ftattempted)
                    )
                conn.commit()
                conn.close()
                return redirect(url_for("freethrowlog"))
    if request.method == "GET":
        return render_template('add.html')

# Edit a FT session data
@app.route("/edit/<string:id>",methods=['POST','GET'])
def edit(id):
    pass

# Run the application
if __name__ == '__main__':  
   app.run(debug=True)