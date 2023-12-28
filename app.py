import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

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
@app.route('/log')
def log():
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
        location = request.form.get("location")

        # Do some validation
        if date and ftmade and ftattempted and location:
            if ftattempted > ftmade:
                conn = get_db_connection()
                conn.execute("INSERT INTO freethrowlog (sessionDate, ftMade, ftAttempted, locationName) VALUES (?, ?, ?, ?)",
                    (date, ftmade, ftattempted, location)
                    )
                conn.commit()
                conn.close()
                return redirect(url_for("log"))
            else:
                return redirect(url_for('error'))
        else:
            return redirect(url_for('error'))
    if request.method == "GET":
        return render_template('add.html')

# Edit a FT session data -> Handle the GET
@app.route("/edit/<string:id>",methods=['POST','GET'])
def edit(id):
    if request.method == 'POST':

        date = str(request.form.get("date"))
        ftmade = int(request.form.get("ftmade"))
        ftattempted = int(request.form.get("ftattempted"))
        location = request.form.get("location")

        if date and ftmade and ftattempted:
            if ftattempted > ftmade:
                conn = get_db_connection()
                conn.execute("UPDATE freethrowlog SET sessionDate=?,ftmade=?,ftattempted=?,locationName=? WHERE id=?",(date,ftmade,ftattempted, location, id))
                conn.commit()
                conn.close()
                return redirect(url_for("log"))
            else:
                return redirect(url_for('error'))
        else:
            return redirect(url_for('error'))
        

    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM freethrowlog WHERE ID=?", (id,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        date = str(data[0]['sessionDate'])
        return render_template("edit.html", data=data, date=date)


# Delete the FT session data
@app.route("/delete.<string:id>", methods=['GET', 'POST'])
def delete(id):
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM freethrowlog WHERE ID=?", (id,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("delete.html", data=data)


    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute("DELETE FROM freethrowlog WHERE ID=?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('log'))

# For when you have gotten a error in the app
@app.route("/error")
def error():
    return render_template('error.html')

# Run the application
if __name__ == '__main__':  
   app.run(debug=True)