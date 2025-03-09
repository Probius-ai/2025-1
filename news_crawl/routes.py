from flask import render_template, redirect, url_for, flash, request
from news_crawl.models import db, User, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from news_crawl.app import app  # Flask 앱 가져오기

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("회원가입이 완료되었습니다! 로그인해주세요.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("로그인 성공!", "success")
            return redirect(url_for("home"))
        else:
            flash("로그인 실패. 이메일과 비밀번호를 확인하세요.", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("로그아웃 되었습니다.", "info")
    return redirect(url_for("login"))
