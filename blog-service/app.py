from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
DATABASE = 'blogs.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS blogs (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')

@app.route('/blogs/', methods=['POST'])
def create_blog():
    data = request.get_json()
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("INSERT INTO blogs (title, content) VALUES (?, ?)", (data['title'], data['content']))
    return jsonify({'message': 'Blog created successfully'}), 201

@app.route('/blogs/', methods=['GET'])
def list_blogs():
    with sqlite3.connect(DATABASE) as conn:
        blogs = conn.execute("SELECT * FROM blogs").fetchall()
    return jsonify([{'id': blog[0], 'title': blog[1], 'content': blog[2]} for blog in blogs]), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)
