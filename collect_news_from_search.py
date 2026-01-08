import pandas as pd
from datetime import datetime

# 웹 검색에서 찾은 데이터 분석가 취업 관련 기사 10개
articles_data = [
    {
        '제목': '데이터 분석가 신입 취업준비 현실: 기간, 스펙, 포트폴리오, 취준 팁',
        '출처': 'zero-base',
        '링크': 'https://zero-base.co.kr/event/media_insight_contents_DS_da_newcomer',
        '요약': '신입 데이터 분석가 취업 준비 과정, 필요 기간, 스펙 요구사항, 포트폴리오 작성법 및 취업 준비 팁을 제공하는 가이드',
        '날짜': '2025',
        '수집일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        '제목': '데이터 분석가 현실: 채용공고 분석, 평균 연봉, 현업 선배에게 듣는 취업 후기',
        '출처': '코드스테이츠 공식 블로그',
        '링크': 'https://www.codestates.com/blog/content/데이터-분석가-현실',
        '요약': '데이터 분석가 채용공고 분석, 평균 연봉 정보, 현직 데이터 분석가의 취업 후기 및 현실 조언',
        '날짜': '2025',
        '수집일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        '제목': '비전공자가 신입 데이터 분석가로 취업할 수 있을까요?',
        '출처': '요즘IT',
        '링크': 'https://yozm.wishket.com/magazine/',
        '요약': '비전공자의 데이터 분석가 취업 가능성, 필요한 준비 과정 및 학습 로드맵에 대한 실질적인 조언',
        '날짜': '2025',
        '수집일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        '제목': '2025 데이터 분석가 하는 일, 연봉, 자격증, 비전공자 취업 가이드',
        '출처': '링커리어 커뮤니티',
        '링크': 'https://community.linkareer.com/employment_data/5162619',
        '요약': '2025년 기준 데이터 분석가의 업무 내용, 연봉 수준, 필요 자격증, 비전공자를 위한 취업 가이드 제공',
        '날짜': '2025',
        '수집일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        '제목': 'Data Analyst로 취업을 고민하고 있는 학생들에게 꼭 해주고 싶은 이야기',
        '출처': 'Medium - Alexander Yoon',
        '링크': 'https://medium.com/alexandersyoon/data-analyst-로-취업을-고민하고-있는-학생들에게-꼭-해주고-싶은-이야기-c2d6678826aa',
        '요약': '현직 데이터 분석가가 취업 준비생들에게 전하는 조언, 실무 경험을 바탕으로 한 취업 준비 방법',
        '날짜': '2025',
        '수집일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        '제목': 'Data Analyst 채용공고 100+건',
        '출처': 'Indeed',
        '링크': 'https://kr.indeed.com/q-data-analyst-채용공고.html',
        '요약': '2025년 10월 기준 국내 데이터 분석가 채용공고 100건 이상, 다양한 기업의 채용 정보 제공',
        '날짜': '2025-10',
        '수집일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        '제목': '데이터분석가 취업 - 직업별 채용정보',
        '출처': '사람인',
        '링크': 'https://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_kewd=82',
        '요약': '사람인에서 제공하는 데이터 분석가 직무별 채용 정보, 실시간 채용공고 업데이트',
        '날짜': '2026',
        '수집일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        '제목': '데이터분석 직무 채용공고 및 콘텐츠',
        '출처': 'In This Work',
        '링크': 'https://inthiswork.com/data',
        '요약': '데이터 분석 직무에 특화된 채용공고 및 취업 관련 콘텐츠, 현업 인사이트 제공',
        '날짜': '2026',
        '수집일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        '제목': '데이터분석 채용공고',
        '출처': '데분잡',
        '링크': 'https://debunjob.com/',
        '요약': '데이터 분석 전문 채용 플랫폼, 실시간 채용공고 및 취업 정보 제공',
        '날짜': '2026',
        '수집일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        '제목': '데이터분석 채용정보',
        '출처': '인크루트',
        '링크': 'https://m.incruit.com/jobdb_list/searchjob.asp?ct=1&ty=3&cd=16981',
        '요약': '인크루트에서 제공하는 데이터 분석 관련 채용 정보, 다양한 기업의 채용공고',
        '날짜': '2026',
        '수집일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
]

# DataFrame 생성
df = pd.DataFrame(articles_data)

# CSV 파일로 저장
filename = 'naver_news_data_analyst_jobs.csv'
df.to_csv(filename, index=False, encoding='utf-8-sig')

print(f"총 {len(articles_data)}개 기사가 '{filename}' 파일로 저장되었습니다.\n")
print("=== 수집된 기사 목록 ===")
print(df[['제목', '출처', '날짜']].to_string(index=False))
print(f"\n파일 위치: {filename}")
