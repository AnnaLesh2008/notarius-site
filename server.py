from flask import Flask, request, render_template
import sqlite3
import datetime

app = Flask(__name__)

# Создаем базу данных
def init_db():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS appointments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  service TEXT NOT NULL,
                  date TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Добавляем запись в БД
def add_appointment(name, phone, service):
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("INSERT INTO appointments (name, phone, service, date) VALUES (?, ?, ?, ?)",
              (name, phone, service, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

@app.route('/')
def form():
    return render_template('form.html', success=False)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    service = request.form['service']
    
    add_appointment(name, phone, service)
    
    return render_template('form.html', success=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)