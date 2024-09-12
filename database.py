import sqlite3

# 데이터베이스 초기화 함수
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL
        )
    """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            school TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


# 데이터베이스에서 모든 토픽을 가져오는 함수
def get_topics():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id, title, body FROM topics")
    topics = [{"id": row[0], "title": row[1], "body": row[2]} for row in c.fetchall()]
    conn.close()
    return topics


# 데이터베이스에 새로운 토픽을 추가하는 함수
def add_topic(title, body):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO topics (title, body) VALUES (?, ?)", (title, body))
    conn.commit()
    conn.close()


# 데이터베이스에서 특정 토픽을 업데이트하는 함수
def update_topic(id, title, body):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE topics SET title = ?, body = ? WHERE id = ?", (title, body, id))
    conn.commit()
    conn.close()


# 데이터베이스에서 특정 토픽을 삭제하는 함수
def delete_topic(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM topics WHERE id = ?", (id,))
    conn.commit()
    conn.close()


# 검색 기능을 위한 함수 추가
def search_topics(keyword):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT id, title, body FROM topics WHERE title LIKE ? OR body LIKE ?', ('%' + keyword + '%', '%' + keyword + '%'))
    topics = [{'id': row[0], 'title': row[1], 'body': row[2]} for row in c.fetchall()]
    conn.close()
    return topics

# 사용자 관리 기능을 위한 함수 추가
def add_user(user_id, username, password, school):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (user_id, username, password, school) VALUES (?, ?, ?, ?)', (user_id, username, password, school))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT user_id, username, password, school FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def update_userInfo(user_id, username, password, school):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE users SET username = ?, password = ?, school = ? WHERE user_id = ?', (username, password, school, user_id))
    conn.commit()
    conn.close()

def login(user_id, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT user_id, username, password, school FROM users WHERE user_id = ? AND password = ?', (user_id, password))
    user = c.fetchone()
    conn.close()
    return user