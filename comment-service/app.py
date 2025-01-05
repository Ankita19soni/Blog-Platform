from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
DATABASE = 'comments.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, post_id INTEGER, content TEXT)''')

@app.route('/comments/', methods=['POST'])
def add_comment():
    data = request.get_json()
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("INSERT INTO comments (post_id, content) VALUES (?, ?)", (data['post_id'], data['content']))
    return jsonify({'message': 'Comment added successfully'}), 201

@app.route('/comments/', methods=['GET'])
def list_comments():
    post_id = request.args.get('post_id')
    with sqlite3.connect(DATABASE) as conn:
        comments = conn.execute("SELECT * FROM comments WHERE post_id = ?", (post_id,)).fetchall()
    return jsonify([{'id': comment[0], 'post_id': comment[1], 'content': comment[2]} for comment in comments]), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002)
