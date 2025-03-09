import os
import requests
from bs4 import BeautifulSoup
import csv
import schedule
import time

# 뉴스 파일 저장 폴더 설정
NEWS_DIR = "news_crawl/news_data"
if not os.path.exists(NEWS_DIR):
    os.makedirs(NEWS_DIR)

# 크롤링 함수 정의
def crawl_news():
    print("\n🚀 뉴스 크롤링 시작...")

    # 네이버 IT 뉴스 URL
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105"

    # HTTP 요청
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 뉴스 제목 가져오기
    titles = soup.select(".sa_text_strong")

    # 날짜와 시간별 파일명 생성 (시간 단위 포함)
    today = time.strftime('%Y-%m-%d_%H')
    filename = os.path.join(NEWS_DIR, f"news_{today}.csv")

    # CSV 파일로 저장
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["번호", "제목", "링크"])  # 헤더 추가

        for idx, title in enumerate(titles, 1):
            news_title = title.text.strip()
            news_link = title.find_parent("a")["href"]
            writer.writerow([idx, news_title, news_link])

    print(f"✅ 뉴스 크롤링 완료! ({len(titles)}개 뉴스 저장됨)")
    with open("news_crawl/log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 뉴스 크롤링 완료! 파일: {filename}\n")

# 💡 10분마다 실행되도록 설정
schedule.every(1).minutes.do(crawl_news)

# 무한 루프 실행 (계속 동작)
print("⏳ 자동 크롤링 시작! (Ctrl + C로 종료 가능)")
while True:
    schedule.run_pending()
    time.sleep(1)