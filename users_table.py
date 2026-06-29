from flask import Flask, request, jsonify
import psycopg2
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "2004"
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
def create_users_table():
    connection=get_db_connection()
    cur=connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL UNIQUE,
            phone_number VARCHAR(10) NOT NULL,
            college TEXT NOT NULL
        )
""")
conn.commit()
cur.close()
connection.close()
create_users_table()
@app.route("/signup", methods=["POST"])
def signup():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    phone_number = request.json["phone_number"]
    college = request.json["college"]
    if not username or not email or not password or not phone_number or not college:
        return jsonify({"error": "All fields are required"}), 400
    cursor.execute(
        "SELECT * FROM users WHERE username=%s OR email=%s",
        (username, email)
    )
    user = cursor.fetchone()
    if user:
        return jsonify({"message": "Username or Email already exists"}), 400
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    connection=get_db_connection()
    cur=connection.cursor()
    cursor.execute("""
    INSERT INTO users(username,email,password,phone_number,college)
    VALUES(%s,%s,%s,%s,%s)""",(username,email,hashed_password,phone_number,college))
    connection.commit()
    cur.close()
    connection.close()
    return jsonify({"message":"User Registered Successfully"})
@app.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    if not username or not email or not password:
        return jsonify({"message":"All fields are required"}),400
        connection=get_db_connection()
        cur=connection.cursor()
    cur.execute("""
    SELECT user_id,username,email,password,college
    FROM users
    WHERE username=%s AND email=%s
    """,(username,email))
    user = cur.fetchone()
    cur.close()
    connection.close()
    if not user:
        return jsonify({"error":"Invalid Username or Email"})
        user_id, username, hashed_password=user
    if not bcrypt.check_password_hash(hashed_password,password):
        return jsonify({"message":"Incorrect Password"}),401
    return jsonify({
        "message":"login successful",
        "user":{
            "user_id":user_id,
            "username":username,
            "email":email,
            "college":college
        }
    })
 
if __name__ == "__main__":
    app.run(debug=True)
