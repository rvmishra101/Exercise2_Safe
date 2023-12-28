import sqlite3
from flask import Flask, render_template, request 

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('entries.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            profession TEXT,
            city TEXT,
            country TEXT,
            remarks TEXT,
            contact TEXT,
            volunteer INTEGER,
            volunteerLevel TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join_chain')
def join_chain():
    return render_template('joinchain.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/submit', methods=['POST','GET'])
def submit():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        prof = request.form['prof']
        city = request.form['city']
        country = request.form['country']
        remarks = request.form['remarks']
        contact = request.form['contact']
        vol = 'vol' in request.form
        volevel = request.form['volevel']


        # Create an entry in the database
        conn = sqlite3.connect('entries.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO entries (name, profession, city, country, remarks, contact, volunteer, volunteerLevel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, prof, city, country, remarks, contact, vol, volevel))
        conn.commit()
        conn.close()

    return render_template('success.html')

@app.route('/result')
def result():
    conn = sqlite3.connect('entries.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries')
    entries = cursor.fetchall()
    conn.close()
    return render_template('result.html', entries=entries)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
