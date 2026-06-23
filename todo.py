from flask import Flask, request, jsonify
import psycopg2
app = Flask(__name__)
# Database config
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "my_password"

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# CREATE TABLE
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(20) DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
create_table()

# HOME
@app.route("/")
def home():
    return jsonify({"message": "To-Do API is Running"})

# ADD TASK
@app.route("/tasks", methods=["POST"])
def add_task():
    title = request.json["title"]
    description = request.json["description"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, description) VALUES (%s, %s)",
        (title, description)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Task added successfully"}), 201

# GET TASK
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    Data = cur.fetchall()
    cur.close()
    conn.close()
    tasks = []
    for row in Data:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "created_at": str(row[4]),
            "updated_at": str(row[5])
        })
    return jsonify(tasks), 200

#UPDATE TASK 
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    title = request.json["title"]
    status = request.json["status"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE tasks
        SET title = %s,
            status = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
    """, (title, status, id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Task updated successfully"}), 200

#  DELETE TASK
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
