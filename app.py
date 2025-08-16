from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'      # your mysql username
app.config['MYSQL_PASSWORD'] = ''      # your mysql password
app.config['MYSQL_DB'] = 'tododb'

mysql = MySQL(app)

# Home Page – Show Tasks
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=tasks)

# Add Task
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks(task) VALUES(%s)", (task,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

# Delete Task
@app.route('/delete/<int:id>')
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

# Update Task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        new_task = request.form['task']
        cur.execute("UPDATE tasks SET task=%s WHERE id=%s", (new_task, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    # If GET → Fetch existing task and show update.html
    cur.execute("SELECT * FROM tasks WHERE id=%s", (id,))
    task = cur.fetchone()
    cur.close()
    return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)