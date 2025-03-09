from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# Flask 앱 설정
app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"  # CSRF 보호를 위한 키 설정
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"  # SQLite 데이터베이스 사용
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# DB, 암호화, 로그인 관리 초기화
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# 사용자 테이블 모델 생성
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# 데이터베이스 생성
with app.app_context():
    db.create_all()