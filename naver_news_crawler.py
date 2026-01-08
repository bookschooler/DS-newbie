import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import urllib.parse

def crawl_naver_news(keyword, num_articles=10):
    """
    네이버 뉴스에서 키워드로 검색하여 기사 수집
    """
    articles = []
    encoded_keyword = urllib.parse.quote(keyword)

    # 네이버 뉴스 검색 URL (최신순 정렬)
    base_url = f"https://search.naver.com/search.naver?where=news&query={encoded_keyword}&sort=1"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        page = 1
        start = 1

        while len(articles) < num_articles:
            # 페이지 번호에 따른 start 값 계산 (1, 11, 21, ...)
            url = f"{base_url}&start={start}"

            print(f"크롤링 중: {url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 디버깅: HTML 구조 확인 (첫 페이지만)
            if page == 1:
                # HTML 파일로 저장하여 구조 확인
                with open('naver_news_debug.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("HTML 구조 확인을 위해 'naver_news_debug.html' 파일로 저장했습니다.")

            # 뉴스 기사 항목 찾기 - 여러 셀렉터 시도
            news_items = soup.select('div.news_area')

            if not news_items:
                news_items = soup.select('li.bx')

            if not news_items:
                news_items = soup.select('div.group_news > ul.list_news > li')

            if not news_items:
                print("더 이상 기사를 찾을 수 없습니다.")
                print(f"시도한 셀렉터로 항목을 찾지 못했습니다.")
                # 대체 방법: a 태그 중 news_tit 클래스를 직접 찾기
                news_links = soup.select('a.news_tit')
                if news_links:
                    print(f"news_tit 링크 {len(news_links)}개 발견")
                    # news_links를 사용하여 기사 수집
                    for link_elem in news_links:
                        if len(articles) >= num_articles:
                            break

                        try:
                            title = link_elem.get('title', '').strip()
                            link = link_elem.get('href', '')

                            # 부모 요소에서 추가 정보 찾기
                            parent = link_elem.find_parent('div', class_='news_wrap')
                            if not parent:
                                parent = link_elem.find_parent()

                            press = ''
                            date_text = ''
                            content = ''

                            if parent:
                                press_elem = parent.select_one('a.info.press')
                                if press_elem:
                                    press = press_elem.text.strip()

                                date_elem = parent.select_one('span.info')
                                if date_elem:
                                    date_text = date_elem.text.strip()

                                content_elem = parent.select_one('div.news_dsc')
                                if not content_elem:
                                    content_elem = parent.select_one('div.dsc_wrap')
                                if content_elem:
                                    content = content_elem.text.strip()

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
                            print(f"기사 파싱 오류: {e}")
                            continue

                    if len(articles) >= num_articles:
                        break

                    # 다음 페이지로
                    start += 10
                    page += 1
                    time.sleep(1)
                    continue
                else:
                    break

            for item in news_items:
                if len(articles) >= num_articles:
                    break

                try:
                    # 제목과 링크
                    title_elem = item.select_one('a.news_tit')
                    if not title_elem:
                        continue

                    title = title_elem.get('title', '').strip()
                    link = title_elem.get('href', '')

                    # 언론사
                    press_elem = item.select_one('a.info.press')
                    press = press_elem.text.strip() if press_elem else ''

                    # 날짜
                    date_elem = item.select_one('span.info')
                    date_text = date_elem.text.strip() if date_elem else ''

                    # 요약 내용
                    content_elem = item.select_one('div.news_dsc')
                    content = content_elem.text.strip() if content_elem else ''

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
                    print(f"기사 파싱 오류: {e}")
                    continue

            # 다음 페이지로
            start += 10
            page += 1
            time.sleep(1)  # 서버 부하 방지

            # 최대 10페이지까지만 검색
            if page > 10:
                break

    except Exception as e:
        print(f"크롤링 오류: {e}")

    return articles

def save_to_csv(articles, filename='naver_news_data_analyst_jobs.csv'):
    """
    수집한 기사를 CSV 파일로 저장
    """
    if not articles:
        print("저장할 기사가 없습니다.")
        return

    df = pd.DataFrame(articles)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n총 {len(articles)}개 기사가 '{filename}' 파일로 저장되었습니다.")
    print(f"\n저장된 컬럼: {list(df.columns)}")
    return df

if __name__ == "__main__":
    keyword = "데이터 분석가 취업"
    num_articles = 10

    print(f"네이버 뉴스에서 '{keyword}' 관련 기사 {num_articles}개 수집 시작...\n")

    articles = crawl_naver_news(keyword, num_articles)

    if articles:
        df = save_to_csv(articles)
        print("\n=== 수집된 기사 미리보기 ===")
        print(df[['제목', '언론사', '날짜']].to_string())
    else:
        print("수집된 기사가 없습니다.")
