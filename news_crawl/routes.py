from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from news_crawl import db, bcrypt
from news_crawl.models import User
import os
import csv

# 블루프린트 생성
routes = Blueprint("routes", __name__)

# 뉴스 데이터 폴더 경로
NEWS_DIR = "news_crawl/news_data"

def get_latest_news_file():
    files = [f for f in os.listdir(NEWS_DIR) if f.startswith("news_") and f.endswith(".csv")]
    files.sort(reverse=True)  # 최신 파일이 첫 번째가 되도록 정렬
    return os.path.join(NEWS_DIR, files[0]) if files else None

def read_news():
    latest_file = get_latest_news_file()
    news_list = []

    if latest_file:
        with open(latest_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 건너뛰기
            for row in reader:
                news_list.append({"number": row[0], "title": row[1], "link": row[2]})

    return news_list

@routes.route("/")
def home():
    if current_user.is_authenticated:
        news = read_news()
        return render_template("index.html", news=news)  # 로그인 상태면 뉴스 페이지로 이동
    return redirect(url_for("routes.login"))  # 비로그인 상태면 로그인 페이지로 이동

@routes.route("/register", methods=["GET", "POST"])
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
        return redirect(url_for("routes.login"))

    return render_template("register.html")

@routes.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes.home"))  # 이미 로그인한 경우 홈으로 이동

    next_page = request.args.get("next")  # 🔥 사용자가 원래 가려던 URL 저장

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("로그인 성공!", "success")
            return redirect(next_page) if next_page else redirect(url_for("routes.home"))  # ✅ 원래 가려던 페이지로 이동
        else:
            flash("로그인 실패. 이메일과 비밀번호를 확인하세요.", "danger")

    return render_template("login.html")

@routes.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("로그아웃 되었습니다.", "info")
    return redirect(url_for("routes.login"))