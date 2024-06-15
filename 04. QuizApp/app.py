from flask import Flask, render_template, request
import subprocess
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Execute Python script
        result_py = subprocess.check_output(['python', 'script.py'], universal_newlines=True).strip()
        
        # Execute SQL query
        conn = sqlite3.connect('your_database.db')  # Make sure your database exists
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM results WHERE id = 1")  # Adjust your SQL query as needed
        result_sql = cursor.fetchone()[0]  # Fetch the result
        conn.close()

        # Render template with results
        return render_template('index.html', py_result=result_py, sql_result=result_sql)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
