from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

# SQLite database file
DATABASE = 'users.db'

# Initialize the database
def init_db():
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )''')
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")

# Helper function to connect to the database
def get_db_connection():
    try:
        return sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Register a new user
@app.route('/register/', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400

    hashed_password = generate_password_hash(data['password'])
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                         (data['username'], hashed_password))
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'User already exists'}), 400
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# User login
@app.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400

    try:
        with get_db_connection() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", 
                                (data['username'],)).fetchone()
        if user and check_password_hash(user[2], data['password']):
            return jsonify({'message': 'Login successful'}), 200
        return jsonify({'message': 'Invalid credentials'}), 401
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
