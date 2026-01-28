import os
from dotenv import load_dotenv

load_dotenv()

# 카카오 API 설정
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY", "")
KAKAO_ACCESS_TOKEN = os.getenv("KAKAO_ACCESS_TOKEN", "")

# 스크래핑 설정
NEWS_COUNT_PER_CATEGORY = 10

# 뉴스 카테고리 설정
NAVER_CATEGORIES = {
    "경제": 101,
    "IT": 105,
    "세계": 104,
}

YAHOO_CATEGORIES = {
    "finance": "https://finance.yahoo.com/topic/stock-market-news/",
    "economy": "https://finance.yahoo.com/topic/economic-news/",
    "tech": "https://finance.yahoo.com/topic/tech/",
}
