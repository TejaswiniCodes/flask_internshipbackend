from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)
DATABASE=todo.db

#database config
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

#create_table
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


create_table()

#home
@app.route("/")
def home():
    return jsonify({"message": "To-Do API is Running"})


# CREATE TASK
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks(title, description) VALUES(%s, %s)",
        (title, description)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Task Added Successfully"}), 201


# GET TASKS
@app.route("/tasks", methods=["GET"])
def get_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    tasks = []

    for row in rows:
        tasks.append(dict(row))

    conn.close()

    return jsonify(tasks)




# UPDATE TASK
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):

    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    status = data.get("status")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title=?,
            description=?,
            status=?,
            updated_at=CURRENT_TIMESTAMP
        WHERE id=?
    """, (title, description, status, id))

    conn.commit()
    conn.close()

    return jsonify({"message": "Task Updated Successfully"})


# DELETE TASK
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Task Deleted Successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
