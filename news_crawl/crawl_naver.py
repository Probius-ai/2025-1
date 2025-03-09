import requests
from bs4 import BeautifulSoup
import csv
import schedule
import time

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

    # CSV 파일로 저장
    with open("news.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["번호", "제목", "링크"])  # 헤더 추가

        for idx, title in enumerate(titles, 1):
            news_title = title.text.strip()
            news_link = title.find_parent("a")["href"]
            writer.writerow([idx, news_title, news_link])

    print(f"✅ 뉴스 크롤링 완료! ({len(titles)}개 뉴스 저장됨)")
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 뉴스 크롤링 완료!\n")

# 💡 10분마다 실행되도록 설정
schedule.every(10).minutes.do(crawl_news)

# 무한 루프 실행 (계속 동작)
print("⏳ 자동 크롤링 시작! (Ctrl + C로 종료 가능)")
while True:
    schedule.run_pending()
    
    time.sleep(1)