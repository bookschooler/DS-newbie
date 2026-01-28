"""
네이버 뉴스 스크래퍼
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from config import NAVER_CATEGORIES, NEWS_COUNT_PER_CATEGORY


class NaverNewsScraper:
    """네이버 뉴스에서 카테고리별 뉴스를 스크래핑"""

    BASE_URL = "https://news.naver.com/section/"
    SEARCH_URL = "https://search.naver.com/search.naver"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def scrape_category(self, category_name: str, category_id: int) -> List[Dict]:
        """특정 카테고리의 뉴스를 스크래핑"""
        url = f"{self.BASE_URL}{category_id}"
        articles = []

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # 헤드라인 뉴스 가져오기
            news_items = soup.select("a.sa_text_title")[:NEWS_COUNT_PER_CATEGORY]

            for item in news_items:
                title = item.get_text(strip=True)
                link = item.get("href", "")

                if title and link:
                    articles.append({
                        "title": title,
                        "link": link,
                        "source": "네이버뉴스",
                        "category": category_name
                    })

        except requests.RequestException as e:
            print(f"[네이버] {category_name} 스크래핑 오류: {e}")

        return articles

    def scrape_search(self, query: str, count: int = 10) -> List[Dict]:
        """네이버 뉴스 검색으로 특정 키워드 뉴스 수집 (최신순)"""
        # sort=1은 최신순 정렬
        params = {
            "where": "news",
            "query": query,
            "sort": "1",  # 최신순
            "sm": "tab_opt",
            "nso": "so:dd,p:all,a:all"  # 최신순 정렬 옵션
        }
        articles = []

        try:
            response = self.session.get(self.SEARCH_URL, params=params, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # 뉴스 검색 결과에서 기사 추출
            news_items = soup.select("div.news_area")[:count]

            for item in news_items:
                title_elem = item.select_one("a.news_tit")
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get("href", "")

                    if title and link:
                        articles.append({
                            "title": title,
                            "link": link,
                            "source": "네이버뉴스",
                            "category": f"{query}"
                        })

        except requests.RequestException as e:
            print(f"[네이버] {query} 검색 스크래핑 오류: {e}")

        return articles

    def scrape_all(self) -> Dict[str, List[Dict]]:
        """모든 카테고리의 뉴스를 스크래핑"""
        all_news = {}

        for category_name, category_id in NAVER_CATEGORIES.items():
            print(f"[네이버] {category_name} 뉴스 수집 중...")
            articles = self.scrape_category(category_name, category_id)
            all_news[f"네이버_{category_name}"] = articles
            print(f"[네이버] {category_name}: {len(articles)}개 수집 완료")

        # AI 뉴스 검색 추가
        print(f"[네이버] AI 뉴스 수집 중...")
        ai_articles = self.scrape_search("AI 인공지능", count=10)
        all_news["네이버_AI"] = ai_articles
        print(f"[네이버] AI: {len(ai_articles)}개 수집 완료")

        return all_news


if __name__ == "__main__":
    scraper = NaverNewsScraper()
    news = scraper.scrape_all()

    for category, articles in news.items():
        print(f"\n=== {category} ===")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article['title']}")
