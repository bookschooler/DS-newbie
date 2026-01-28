"""
야후 파이낸스 뉴스 스크래퍼
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from config import YAHOO_CATEGORIES, NEWS_COUNT_PER_CATEGORY


class YahooFinanceScraper:
    """야후 파이낸스에서 카테고리별 뉴스를 스크래핑"""

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def scrape_category(self, category_name: str, url: str) -> List[Dict]:
        """특정 카테고리의 뉴스를 스크래핑"""
        articles = []

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # 뉴스 아이템 찾기 (야후 파이낸스 구조)
            news_items = soup.select("h3 a, li.stream-item a.subtle-link")[:NEWS_COUNT_PER_CATEGORY * 2]

            seen_titles = set()
            for item in news_items:
                title = item.get_text(strip=True)
                link = item.get("href", "")

                # 중복 제거 및 유효성 검사
                if not title or title in seen_titles or len(title) < 10:
                    continue

                # 상대 URL 처리
                if link.startswith("/"):
                    link = f"https://finance.yahoo.com{link}"

                if title and link:
                    seen_titles.add(title)
                    articles.append({
                        "title": title,
                        "link": link,
                        "source": "Yahoo Finance",
                        "category": category_name
                    })

                if len(articles) >= NEWS_COUNT_PER_CATEGORY:
                    break

        except requests.RequestException as e:
            print(f"[Yahoo] {category_name} 스크래핑 오류: {e}")

        return articles

    def scrape_all(self) -> Dict[str, List[Dict]]:
        """모든 카테고리의 뉴스를 스크래핑"""
        all_news = {}

        for category_name, url in YAHOO_CATEGORIES.items():
            print(f"[Yahoo] {category_name} 뉴스 수집 중...")
            articles = self.scrape_category(category_name, url)
            all_news[f"Yahoo_{category_name}"] = articles
            print(f"[Yahoo] {category_name}: {len(articles)}개 수집 완료")

        return all_news


if __name__ == "__main__":
    scraper = YahooFinanceScraper()
    news = scraper.scrape_all()

    for category, articles in news.items():
        print(f"\n=== {category} ===")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article['title']}")
