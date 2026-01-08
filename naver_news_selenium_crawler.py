from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import time

def setup_driver():
    """
    Selenium WebDriver 설정
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 백그라운드 실행
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"WebDriver 초기화 오류: {e}")
        print("ChromeDriver가 설치되어 있지 않을 수 있습니다. 설치를 진행합니다...")
        return None

def crawl_naver_news_selenium(keyword, num_articles=10):
    """
    Selenium을 사용하여 네이버 뉴스 크롤링
    """
    articles = []

    driver = setup_driver()
    if not driver:
        return articles

    try:
        # 네이버 뉴스 검색 URL (최신순 정렬: sort=1)
        url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sort=1"

        print(f"네이버 뉴스 페이지 로딩 중: {url}")
        driver.get(url)

        # 페이지 로딩 대기
        time.sleep(3)

        # 스크롤하여 더 많은 기사 로드
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scrolls = 5  # 최대 스크롤 횟수

        while scroll_attempts < max_scrolls and len(articles) < num_articles:
            # 현재 보이는 모든 뉴스 아이템 찾기
            try:
                news_items = driver.find_elements(By.CSS_SELECTOR, 'div.news_area')

                if not news_items:
                    # 대체 셀렉터 시도
                    news_items = driver.find_elements(By.CSS_SELECTOR, 'div.group_news ul.list_news > li')

                print(f"현재 페이지에서 {len(news_items)}개의 뉴스 아이템 발견")

                for item in news_items:
                    if len(articles) >= num_articles:
                        break

                    try:
                        # 제목과 링크
                        title_elem = item.find_element(By.CSS_SELECTOR, 'a.news_tit')
                        title = title_elem.get_attribute('title') if title_elem.get_attribute('title') else title_elem.text
                        link = title_elem.get_attribute('href')

                        # 이미 수집한 기사는 스킵
                        if any(article['링크'] == link for article in articles):
                            continue

                        # 언론사
                        try:
                            press_elem = item.find_element(By.CSS_SELECTOR, 'a.info.press')
                            press = press_elem.text.strip()
                        except:
                            press = ''

                        # 날짜
                        try:
                            date_elem = item.find_element(By.CSS_SELECTOR, 'span.info')
                            date_text = date_elem.text.strip()
                        except:
                            date_text = ''

                        # 요약 내용
                        try:
                            content_elem = item.find_element(By.CSS_SELECTOR, 'div.news_dsc')
                            content = content_elem.text.strip()
                        except:
                            try:
                                content_elem = item.find_element(By.CSS_SELECTOR, 'div.dsc_wrap')
                                content = content_elem.text.strip()
                            except:
                                content = ''

                        articles.append({
                            '제목': title,
                            '언론사': press,
                            '날짜': date_text,
                            '요약': content,
                            '링크': link,
                            '수집일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })

                        print(f"수집 완료 ({len(articles)}/{num_articles}): {title[:50]}...")

                    except Exception as e:
                        # print(f"기사 파싱 오류: {e}")
                        continue

                # 목표 개수에 도달하면 종료
                if len(articles) >= num_articles:
                    break

                # 페이지 스크롤
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                # 새로운 높이 확인
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    # 더 이상 로드할 내용이 없으면 종료
                    break
                last_height = new_height
                scroll_attempts += 1

            except Exception as e:
                print(f"크롤링 중 오류: {e}")
                break

    except Exception as e:
        print(f"전체 크롤링 오류: {e}")

    finally:
        driver.quit()

    return articles

def save_to_csv(articles, filename='naver_news_data_analyst_jobs.csv'):
    """
    수집한 기사를 CSV 파일로 저장
    """
    if not articles:
        print("저장할 기사가 없습니다.")
        return None

    df = pd.DataFrame(articles)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n총 {len(articles)}개 기사가 '{filename}' 파일로 저장되었습니다.")
    print(f"\n저장된 컬럼: {list(df.columns)}")
    return df

if __name__ == "__main__":
    keyword = "데이터 분석가 취업"
    num_articles = 10

    print(f"네이버 뉴스에서 '{keyword}' 관련 기사 {num_articles}개 수집 시작...\n")

    articles = crawl_naver_news_selenium(keyword, num_articles)

    if articles:
        df = save_to_csv(articles)
        print("\n=== 수집된 기사 미리보기 ===")
        print(df[['제목', '언론사', '날짜']].to_string())
    else:
        print("수집된 기사가 없습니다.")
        print("\n대체 방법을 시도합니다...")
