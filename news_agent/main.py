"""
뉴스 클리핑 에이전트

야후 파이낸스, 네이버 뉴스에서 금융/IT/국제/경제 뉴스를 수집하여
카카오톡으로 전송합니다.

사용법:
    python main.py           # 즉시 실행
    python main.py --test    # 스크래핑만 테스트 (카카오톡 전송 안함)
    python main.py --schedule # 매일 오전 8시에 자동 실행
"""
import sys
import json
import io
import webbrowser
import os
from datetime import datetime

# Windows 콘솔 UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from scrapers import NaverNewsScraper, YahooFinanceScraper
from kakao_sender import KakaoSender, get_new_token_guide


def collect_news() -> dict:
    """모든 소스에서 뉴스 수집"""
    print("\n" + "=" * 50)
    print(f"📰 뉴스 수집 시작 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    all_news = {}

    # 네이버 뉴스 수집
    try:
        naver_scraper = NaverNewsScraper()
        naver_news = naver_scraper.scrape_all()
        all_news.update(naver_news)
    except Exception as e:
        print(f"[오류] 네이버 뉴스 수집 실패: {e}")

    # 야후 파이낸스 수집
    try:
        yahoo_scraper = YahooFinanceScraper()
        yahoo_news = yahoo_scraper.scrape_all()
        all_news.update(yahoo_news)
    except Exception as e:
        print(f"[오류] 야후 파이낸스 수집 실패: {e}")

    return all_news


def display_news(all_news: dict):
    """수집된 뉴스 출력"""
    print("\n" + "=" * 50)
    print("📋 수집된 뉴스 목록")
    print("=" * 50)

    total = 0
    for category, articles in all_news.items():
        print(f"\n【{category}】 ({len(articles)}개)")
        print("-" * 40)
        for i, article in enumerate(articles, 1):
            title = article["title"][:50] + "..." if len(article["title"]) > 50 else article["title"]
            print(f"  {i}. {title}")
        total += len(articles)

    print(f"\n총 {total}개의 뉴스가 수집되었습니다.")


def save_to_json(all_news: dict, filename: str = None):
    """뉴스를 JSON 파일로 저장"""
    if filename is None:
        filename = f"news_{datetime.now().strftime('%Y%m%d_%H%M')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)

    print(f"\n💾 {filename}에 저장되었습니다.")


def save_to_html(all_news: dict, filename: str = None) -> str:
    """뉴스를 HTML 파일로 저장하고 경로 반환"""
    if filename is None:
        filename = f"news_{datetime.now().strftime('%Y%m%d_%H%M')}.html"

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>오늘의 뉴스 클리핑 - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .category {{
            background: white;
            border-radius: 15px;
            margin-bottom: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .category-header {{
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 15px 20px;
            font-size: 1.3em;
            font-weight: bold;
        }}
        .article {{
            padding: 15px 20px;
            border-bottom: 1px solid #eee;
            transition: background 0.3s;
        }}
        .article:hover {{ background: #f8f9fa; }}
        .article:last-child {{ border-bottom: none; }}
        .article a {{
            color: #333;
            text-decoration: none;
            font-size: 1.1em;
            display: block;
        }}
        .article a:hover {{ color: #4facfe; }}
        .article-source {{
            color: #888;
            font-size: 0.85em;
            margin-top: 5px;
        }}
        .timestamp {{
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-top: 20px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📰 오늘의 뉴스 클리핑</h1>
"""

    for category, articles in all_news.items():
        if articles:
            html_content += f"""
        <div class="category">
            <div class="category-header">📁 {category} ({len(articles)}개)</div>
"""
            for article in articles:
                title = article.get("title", "제목 없음")
                link = article.get("link", "#")
                source = article.get("source", "")
                html_content += f"""
            <div class="article">
                <a href="{link}" target="_blank">{title}</a>
                <div class="article-source">{source}</div>
            </div>
"""
            html_content += """        </div>
"""

    html_content += f"""
        <p class="timestamp">생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"📄 {filename}에 HTML 저장 완료!")
    return os.path.abspath(filename)


def open_html_in_browser(filepath: str):
    """HTML 파일을 브라우저에서 열기"""
    try:
        webbrowser.open(f"file:///{filepath}")
        print(f"🌐 브라우저에서 뉴스 페이지를 열었습니다!")
    except Exception as e:
        print(f"브라우저 열기 실패: {e}")


def send_to_kakao(all_news: dict) -> bool:
    """카카오톡으로 전송"""
    print("\n" + "=" * 50)
    print("📱 카카오톡 전송 중...")
    print("=" * 50)

    try:
        sender = KakaoSender()
        return sender.send_news_summary(all_news)
    except ValueError as e:
        print(f"\n⚠️  {e}")
        get_new_token_guide()
        return False
    except Exception as e:
        print(f"\n❌ 전송 실패: {e}")
        return False


def run_scheduled():
    """스케줄러로 정기 실행"""
    import schedule
    import time

    def job():
        all_news = collect_news()
        if all_news:
            display_news(all_news)
            save_to_json(all_news)
            send_to_kakao(all_news)

    # 매일 오전 8시 실행
    schedule.every().day.at("08:00").do(job)

    print("\n⏰ 스케줄러 시작 - 매일 오전 8시에 뉴스를 전송합니다.")
    print("   (종료하려면 Ctrl+C)")

    # 즉시 한 번 실행
    job()

    while True:
        schedule.run_pending()
        time.sleep(60)


def main():
    # 명령행 인자 처리
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    # 뉴스 수집
    all_news = collect_news()

    if not all_news:
        print("수집된 뉴스가 없습니다.")
        return

    # 결과 출력
    display_news(all_news)

    # JSON 저장
    save_to_json(all_news)

    # HTML 저장 및 브라우저 열기
    html_path = save_to_html(all_news)

    # 테스트 모드 확인
    if "--test" in args:
        print("\n✅ 테스트 모드 - 카카오톡 전송을 건너뜁니다.")
        open_html_in_browser(html_path)
        return

    # 스케줄 모드
    if "--schedule" in args:
        run_scheduled()
        return

    # 카카오톡 전송
    send_to_kakao(all_news)

    # 브라우저에서 전체 뉴스 보기
    open_html_in_browser(html_path)


if __name__ == "__main__":
    main()
