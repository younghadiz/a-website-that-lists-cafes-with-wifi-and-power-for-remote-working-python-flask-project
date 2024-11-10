from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('webappcafe.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cafes = conn.execute('SELECT * FROM cafes').fetchall()
    conn.close()
    return render_template('index.html', cafes=cafes)

@app.route('/add', methods=('GET', 'POST'))
def add_cafe():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        wifi_strength = request.form['wifi_strength']
        power_availability = request.form.get('power_availability') == 'on'

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO cafes (name, location, wifi_strength, power_availability) VALUES (?, ?, ?, ?)',
            (name, location, wifi_strength, power_availability)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_cafe.html')

if __name__ == '__main__':
    app.run(debug=True)
