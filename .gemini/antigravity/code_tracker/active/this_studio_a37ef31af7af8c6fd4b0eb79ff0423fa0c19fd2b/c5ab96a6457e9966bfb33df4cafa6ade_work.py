�import requests
import pandas as pd
import time
from xml.etree import ElementTree

# [설정] 본인의 정보로 수정
SERVICE_KEY = '13daacd9c6761fa276b9a264c8025e93892500fbe0bddc1811ee8130d476292c' 
# CSV_FILE_PATH = 'rd.csv' 
CSV_FILE_PATH = '/teamspace/studios/this_studio/tp/rd.csv' 
REGION_COL_NAME = '법정동코드'

# 202501, 202502 ... 202512 리스트 자동 생성
target_months = [f"2025{str(m).zfill(2)}" for m in range(1, 13)]

def collect():
    try:
        # CSV 읽기
        df = pd.read_csv(CSV_FILE_PATH)
        # 지역코드 컬럼에서 중복 제거 후 리스트화
        codes = df[REGION_COL_NAME].unique().tolist()
        print(f"데이터 수집 시작: 총 {len(codes)}개 지역, 12개월분")
    except Exception as e:
        print(f"파일 읽기 에러: {e}")
        return

    url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev"
    all_data = []

    for code in codes:
        # 지역코드를 5자리 문자열로 변환 (예: 11110)
        clean_code = str(code).strip().zfill(5)[:5]
        
        for ymd in target_months:
            params = {
                'serviceKey': SERVICE_KEY,
                'LAWD_CD': clean_code,
                'DEAL_YMD': ymd,
                'numOfRows': '999'
            }
            
            print(f"수집 중... 지역: {clean_code} | 월: {ymd}", end="\r")
            
            try:
                res = requests.get(url, params=params)
                if res.status_code == 200:
                    root = ElementTree.fromstring(res.text)
                    items = root.findall('.//item')
                    for item in items:
                        all_data.append({child.tag: child.text for child in item})
                
                # API 서버 부하 방지를 위해 0.5초 대기
                time.sleep(0.5)
                
            except Exception as e:
                print(f"\n에러 발생 ({clean_code}, {ymd}): {e}")

    if all_data:
        # 결과를 CSV로 저장 (한글 깨짐 방지를 위해 utf-8-sig 사용)
        pd.DataFrame(all_data).to_csv("apt_result_2025.csv", index=False, encoding='utf-8-sig')
        print(f"\n수집 완료! 총 {len(all_data)}건 저장됨.")
    else:
        print("\n수집된 데이터가 없습니다. 인증키와 파라미터를 다시 확인하세요.")

if __name__ == "__main__":
    collect()�"(a37ef31af7af8c6fd4b0eb79ff0423fa0c19fd2b20file:///teamspace/studios/this_studio/tp/work.py:%file:///teamspace/studios/this_studio