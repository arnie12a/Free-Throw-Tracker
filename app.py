import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os
import seaborn as sns


def get_df():
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT * FROM freethrowlog ORDER BY sessionDate ASC", conn)
    return df

# Creates Percentage column
def createPercentage(df):
    percentages = []
    for index, row in df.iterrows():
        percentages.append(round(row['ftMade']/row['ftAttempted'], 3)*100)
    df['percent'] = percentages
    return df

def averagePercentagePlot():
    # Manipulating Data
    df = get_df()
    made = df['ftMade'].sum()
    attempted = df['ftAttempted'].sum()
    labels = ['Free Throws Made', 'Free Throws Missed']
    values = [made, attempted - made]

    # Set Seaborn style
    sns.set_theme()

    # Plot the pie chart using Matplotlib
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("Free Throws Made vs. Missed")

    plt.savefig("static/averagePercentagePlot.png",format="png")
    return 

def locationPlot():

    # Manipulating data
    df = get_df()
    location_df = df.groupby('locationName').agg({'ftMade': 'sum', 'ftAttempted': 'sum'}).reset_index()
    location_df = createPercentage(location_df)
    location_df
    
    # Plotting 
    sns.set_theme()

    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a bar plot using Seaborn
    sns.barplot(x='locationName', y='percent', data=location_df, ax=ax)
    sns.color_palette("Set2")
    ax.set_title("Location vs. Year")
    ax.set_xlabel('Location')
    ax.set_ylabel('Percentage')
    ax.set_ylim(65, 95)

    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    plt.tight_layout()  # Adjust layout for better display

    fig.savefig("static/locationPlot.png",format="png")
    return

# Free Throw Percentage per year
def yearPlot():

    # Manipulating data
    df = get_df()
    date_list = df['sessionDate'].tolist()

    extract_year = lambda date_str: datetime.strptime(date_str, '%Y-%m-%d').year
    year_list = list(map(extract_year, date_list))
    df['Year'] = year_list
    d = {}
    for year in year_list:
        if year in d:
            d[year] += 1
        else:
            d[year] = 1
    year_df = df.groupby('Year').agg({'ftMade': 'sum', 'ftAttempted': 'sum'}).reset_index()
    year_df = createPercentage(year_df)
    year_df['numSessions'] = list(d.values())

    # Plotting
    sns.set_theme()
    sns.color_palette("Set2")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a bar plot using Seaborn
    sns.barplot(x='Year', y='percent', data=year_df, ax=ax)

    ax.set_title("Location vs. Year")
    ax.set_xlabel('Location')
    ax.set_ylabel('Percentage')
    ax.set_ylim(60, 90)

    plt.tight_layout()  # Adjust layout for better display

    fig.savefig("static/yearPlot.png",format="png")
    return

def calculateAveragePercentage(table):
    totalFTmade = 0
    totalFTattempted = 0
    for i in range(len(table)):
        totalFTmade += table[i]['ftmade']
        totalFTattempted += table[i]['ftattempted']
    return round((totalFTmade/totalFTattempted)*100, 2)


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
    logs = conn.execute('SELECT * FROM freethrowlog ORDER BY sessionDate ASC').fetchall()
    conn.close()
    return render_template('log.html', logs=logs, vals=len(logs))

# Page for statistics and has dashboard
@app.route('/statistics')
def statistics():
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM freethrowlog ORDER BY sessionDate ASC').fetchall()
    conn.close()

    # Calculate the average shooting percentage from the ft line
    percentage = calculateAveragePercentage(logs)
    if not os.path.exists("static"):
        os.makedirs("static")
    yearPlot()
    averagePercentagePlot()
    locationPlot()
    return render_template('stats.html', percentage=percentage)

# Add free throw session to the database
@app.route('/add', methods = ["GET", "POST"])
def add():
    if request.method == "POST":

        date = str(request.form.get("date"))
        ftmade = int(request.form.get("ftmade"))
        ftattempted = int(request.form.get("ftattempted"))
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
                print("not greater")
                return redirect(url_for('error'))
        else:
            print("not all filled")
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