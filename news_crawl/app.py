from news_crawl import create_app, db
from flask_login import LoginManager

app = create_app()
login_manager = LoginManager()
login_manager.login_view = "routes.login"  # 로그인 페이지 설정

# 데이터베이스 테이블 생성 (Flask 앱 컨텍스트에서 실행)
with app.app_context():
    db.create_all()

# 🚀 사용자 로드 함수 추가
from news_crawl.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)
