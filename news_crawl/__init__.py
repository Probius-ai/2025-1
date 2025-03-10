from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# SQLAlchemy 인스턴스 생성
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "login"

def create_app():
    app = Flask(__name__)

    # Flask 설정
    app.config["SECRET_KEY"] = "supersecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 확장 기능 초기화
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # 블루프린트 등록
    from news_crawl.routes import routes
    app.register_blueprint(routes)

    return app

# 🚀 사용자 로드 함수 추가
from news_crawl.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))