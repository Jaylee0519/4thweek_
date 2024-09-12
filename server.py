from flask import Flask, request, redirect, session
from database import *

app = Flask(__name__)

app.secret_key = "SECRET_KEY"


init_db()


def template(contents, content, id=None):
    contextUI = ""
    userSession = ""
    if id != None:
        contextUI = f"""
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
        """
    # 로그인 상태에 따라 버튼 표시
    if "user_id" in session:
        userSession = """
            <li><a href="/logout/">logout</a></li>
            <li><a href="/my_page/">my page</a></li>
        """
    else:
        userSession = """
            <li><a href="/login/">login</a></li>
            <li><a href="/sign_in/">sign_in</a></li>
        """

    return f"""<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <form action="/search/" method="POST">
                <p><input type="text" name="keyword" placeholder="search"></p>
                <p><input type="submit" value="search"></p>
            </form>
            <ul>
                {userSession}
            </ul>
            <h2>Contents</h2>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    """


def getContents():
    topics = get_topics()
    liTags = ""
    for topic in topics:
        liTags = (
            liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
        )
    return liTags


@app.route("/")
def index():
    return template(getContents(), "<h2>Welcome</h2>Hello, WEB")


@app.route("/read/<int:id>/")
def read(id):
    topics = get_topics()
    title = ""
    body = ""
    for topic in topics:
        if id == topic["id"]:
            title = topic["title"]
            body = topic["body"]
            break
    return template(getContents(), f"<h2>{title}</h2>{body}", id)


@app.route("/create/", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        content = """
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        """
        return template(getContents(), content)
    elif request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        add_topic(title, body)
        topics = get_topics()
        new_topic = topics[-1]
        url = "/read/" + str(new_topic["id"]) + "/"
        return redirect(url)


@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    if request.method == "GET":
        topics = get_topics()
        title = ""
        body = ""
        for topic in topics:
            if id == topic["id"]:
                title = topic["title"]
                body = topic["body"]
                break
        content = f"""
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" placeholder="title" value="{title}"></p>
                <p><textarea name="body" placeholder="body">{body}</textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        """
        return template(getContents(), content)
    elif request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        update_topic(id, title, body)
        url = "/read/" + str(id) + "/"
        return redirect(url)


@app.route("/delete/<int:id>/", methods=["POST"])
def delete(id):
    delete_topic(id)
    return redirect("/")


@app.route("/search/", methods=["POST"])
def search():
    keyword = request.form["keyword"]
    topics = search_topics(keyword)
    liTags = ""
    for topic in topics:
        liTags = (
            liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
        )
    return template(liTags, f"<h2>Search results for '{keyword}'</h2>")


@app.route("/sign_in/", methods=["GET", "POST"])
def sign_in():
    if request.method == "GET":
        content = """
            <form action="/sign_in/" method="POST">
                <p><input type="text" name="user_id" placeholder="id"></p>
                <p><input type="text" name="username" placeholder="username"></p>
                <p><input type="password" name="password" placeholder="password"></p>
                <p><input type="text" name="school" placeholder="school"></p>
                <p><input type="submit" value="sign in"></p>
            </form>
        """
        return template(getContents(), content)
    elif request.method == "POST":
        user_id = request.form["user_id"]
        username = request.form["username"]
        password = request.form["password"]
        school = request.form["school"]
        add_user(user_id, username, password, school)
        return redirect("/")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        content = """
            <form action="/login/" method="POST">
                <p><input type="text" name="user_id" placeholder="user_id"></p>
                <p><input type="password" name="password" placeholder="password"></p>
                <p><input type="submit" value="login"></p>
            </form>
        """
        return template(getContents(), content)
    elif request.method == "POST":
        user_id = request.form["user_id"]
        password = request.form["password"]
        user = get_user(user_id)
        if user != None and user[2] == password:
            session["user_id"] = user[0]
        return redirect("/")


@app.route("/logout/")
def logout():
    session.pop("user_id", None)
    return redirect("/")


@app.route("/my_page/")
def my_page():
    if "user_id" in session:
        user = get_user(session["user_id"])
        # 사용자 정보를 출력 및 수정할 수 있는 페이지
        content = f"""
            <h2>My page</h2>
            <p>user_id: {user[0]}</p>
            <p>username: {user[1]}</p>
            <p>password: {user[2]}</p>
            <p>school: {user[3]}</p>
            <a href="/update_user/">update</a>
        """
        return template(getContents(), content)
    else:
        return redirect("/login/")


@app.route("/update_user/", methods=["GET", "POST"])
def update_user():
    if request.method == "GET":
        user = get_user(session["user_id"])
        content = f"""
            <form action="/update_user/" method="POST">
                <p><input type="text" name="username" placeholder="username" value="{user[1]}"></p>
                <p><input type="password" name="password" placeholder="password" value="{user[2]}"></p>
                <p><input type="text" name="school" placeholder="school" value="{user[3]}"></p>
                <p><input type="submit" value="update"></p>
            </form>
        """
        return template(getContents(), content)
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        school = request.form["school"]
        update_userInfo(session["user_id"], username, password, school)
        return redirect("/my_page/")


app.run(debug=True)
