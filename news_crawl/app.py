from flask import Flask, render_template
import os
import csv
import time

# 현재 파일(app.py)이 있는 폴더의 절대 경로 찾기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Flask 앱 설정 - 템플릿 폴더 경로 절대 경로로 설정
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))

# 뉴스 데이터 폴더 절대 경로 설정
NEWS_DIR = os.path.join(BASE_DIR, "news_data")

# 최신 뉴스 파일 찾기
def get_latest_news_file():
    files = [f for f in os.listdir(NEWS_DIR) if f.startswith("news_") and f.endswith(".csv")]
    files.sort(reverse=True)  # 최신 파일이 첫 번째가 되도록 정렬
    return os.path.join(NEWS_DIR, files[0]) if files else None

# 뉴스 데이터 읽기
def read_news():
    latest_file = get_latest_news_file()
    news_list = []

    if latest_file:
        with open(latest_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 건너뛰기
            for row in reader:
                news_list.append({"number": row[0], "title": row[1], "link": row[2]})

    print(f"📊 불러온 뉴스 개수: {len(news_list)}")  # 뉴스 개수 출력
    return news_list

# 웹 페이지 라우트
@app.route("/")
def home():
    news = read_news()
    return render_template("index.html", news=news)

# Flask 실행
if __name__ == "__main__":
    app.run(debug=True)