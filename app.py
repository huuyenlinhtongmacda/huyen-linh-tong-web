
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os


app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "dev-secret-key"
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "users.db")


def get_conn():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_conn()

    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            TenTaiKhoan TEXT UNIQUE,
            MatKhau TEXT,
            Phone TEXT,
            is_deleted INTEGER DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            location TEXT,
            content TEXT
        )
    """)

    conn.commit()

    conn.close()


init_db()


@app.route("/")
def index():

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        username = request.form["username"].strip()

        password = request.form["password"].strip()

        if username == "huyenlinhtong" and password == "thiendat":

            return redirect(url_for("admin"))

        conn = get_conn()

        c = conn.cursor()

        c.execute("""
            SELECT *
            FROM users
            WHERE TenTaiKhoan = ?
            AND MatKhau = ?
            AND is_deleted = 0
        """, (username, password))

        user = c.fetchone()

        conn.close()

        if user:

            session["username"] = user["TenTaiKhoan"]

            return redirect(url_for("home"))

        else:

            error = "Sai tài khoản hoặc mật khẩu"

    return render_template(
        "login.html",
        error=error
    )


@app.route("/register", methods=["GET", "POST"])
def register():

    msg = ""

    if request.method == "POST":

        username = request.form["username"].strip()

        password = request.form["password"].strip()

        confirm_password = request.form["confirm_password"].strip()

        phone = request.form["phone"].strip()

        if username == "" or password == "" or phone == "":

            msg = "Vui lòng nhập đầy đủ thông tin"

            return render_template(
                "register.html",
                msg=msg
            )

        if password != confirm_password:

            msg = "Mật khẩu xác nhận không khớp"

            return render_template(
                "register.html",
                msg=msg
            )

        conn = get_conn()

        c = conn.cursor()

        c.execute("""
            SELECT *
            FROM users
            WHERE TenTaiKhoan = ?
        """, (username,))

        exists = c.fetchone()

        if exists:

            conn.close()

            msg = "Tài khoản đã tồn tại"

            return render_template(
                "register.html",
                msg=msg
            )

        c.execute("""
            INSERT INTO users
            (TenTaiKhoan, MatKhau, Phone)
            VALUES (?, ?, ?)
        """, (username, password, phone))

        conn.commit()

        conn.close()

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        msg=msg
    )


@app.route("/admin")
def admin():

    conn = get_conn()

    c = conn.cursor()

    c.execute("""
        SELECT *
        FROM users
        WHERE is_deleted = 0
    """)

    users = c.fetchall()

    c.execute("""
        SELECT *
        FROM users
        WHERE is_deleted = 1
    """)

    deleted = c.fetchall()

    c.execute("""
        SELECT *
        FROM reports
        ORDER BY id DESC
    """)

    reports = c.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        users=users,
        deleted=deleted,
        reports=reports
    )


@app.route("/delete_user", methods=["POST"])
def delete_user():

    username = request.form["username"]

    conn = get_conn()

    c = conn.cursor()

    c.execute("""
        UPDATE users
        SET is_deleted = 1
        WHERE TenTaiKhoan = ?
    """, (username,))

    conn.commit()

    conn.close()

    return redirect(url_for("admin"))


@app.route("/restore_user", methods=["POST"])
def restore_user():

    username = request.form["username"]

    conn = get_conn()

    c = conn.cursor()

    c.execute("""
        UPDATE users
        SET is_deleted = 0
        WHERE TenTaiKhoan = ?
    """, (username,))

    conn.commit()

    conn.close()

    return redirect(url_for("admin"))


@app.route("/delete_report", methods=["POST"])
def delete_report():

    report_id = request.form["id"]

    conn = get_conn()

    c = conn.cursor()

    c.execute("""
        DELETE FROM reports
        WHERE id = ?
    """, (report_id,))

    conn.commit()

    conn.close()

    return redirect(url_for("admin"))


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

    msg = ""

    password = ""

    if request.method == "POST":

        username = request.form["username"].strip()

        phone = request.form["phone"].strip()

        conn = get_conn()

        c = conn.cursor()

        c.execute("""
            SELECT *
            FROM users
            WHERE TenTaiKhoan = ?
            AND Phone = ?
        """, (username, phone))

        user = c.fetchone()

        conn.close()

        if user:

            password = user["MatKhau"]

        else:

            msg = "Không tìm thấy tài khoản"

    return render_template(
        "forgot_password.html",
        msg=msg,
        password=password
    )


@app.route("/home")
def home():

    return render_template("home.html")


@app.route("/service")
def service():

    return render_template("service.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]

        role = request.form["role"]

        location = request.form["location"]

        content = request.form["content"]

        conn = get_conn()

        c = conn.cursor()

        c.execute("""
            INSERT INTO reports
            (name, role, location, content)
            VALUES (?, ?, ?, ?)
        """, (name, role, location, content))

        conn.commit()

        conn.close()

    return render_template("contact.html")


@app.route("/username")
def profile():

    if "username" not in session:

        return redirect(url_for("login"))

    username = session["username"]

    conn = get_conn()

    c = conn.cursor()

    c.execute("""
        SELECT *
        FROM users
        WHERE TenTaiKhoan = ?
    """, (username,))

    user = c.fetchone()

    conn.close()

    return render_template(
        "username.html",
        username=user["TenTaiKhoan"],
        phone=user["Phone"]
    )


@app.route("/mission")
def mission():

    return render_template("mission.html")


@app.route("/library")
def library():

    return render_template("library.html")


@app.route("/member")
def member():

    conn = get_conn()

    c = conn.cursor()

    c.execute("""
        SELECT *
        FROM users
        WHERE is_deleted = 0
    """)

    users = c.fetchall()

    conn.close()

    return render_template(
        "member.html",
        users=users
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )

