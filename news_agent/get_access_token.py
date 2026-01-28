"""
카카오 Access Token 발급 스크립트

사용법:
1. https://developers.kakao.com 에서 앱 생성
2. REST API 키 복사
3. 이 스크립트 실행 후 안내에 따라 진행
"""
import requests
import webbrowser
from urllib.parse import urlencode


def get_access_token():
    print("=" * 60)
    print("카카오 Access Token 발급")
    print("=" * 60)

    # Step 1: REST API Key 입력
    rest_api_key = input("\n1. REST API 키를 입력하세요: ").strip()
    if not rest_api_key:
        print("REST API 키가 필요합니다.")
        return

    # Redirect URI (카카오 개발자 콘솔에서 등록 필요)
    redirect_uri = "https://localhost.com"

    # Step 2: 인증 URL 생성 및 열기
    auth_url = (
        f"https://kauth.kakao.com/oauth/authorize?"
        f"client_id={rest_api_key}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code"
    )

    print(f"\n2. 브라우저에서 카카오 로그인을 진행하세요.")
    print(f"   (자동으로 열리지 않으면 아래 URL을 복사하여 접속)")
    print(f"\n   {auth_url}\n")

    try:
        webbrowser.open(auth_url)
    except:
        pass

    # Step 3: 인증 코드 입력
    print("3. 로그인 후 리다이렉트된 URL에서 'code=' 뒤의 값을 복사하세요.")
    print("   예: https://example.com/oauth?code=XXXXXX")
    auth_code = input("\n   인증 코드 입력: ").strip()

    if not auth_code:
        print("인증 코드가 필요합니다.")
        return

    # Step 4: Access Token 발급
    print("\n4. Access Token 발급 중...")

    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": rest_api_key,
        "redirect_uri": redirect_uri,
        "code": auth_code,
    }

    try:
        response = requests.post(token_url, data=data)
        result = response.json()

        if "access_token" in result:
            access_token = result["access_token"]
            refresh_token = result.get("refresh_token", "")

            print("\n" + "=" * 60)
            print("✅ 토큰 발급 성공!")
            print("=" * 60)
            print(f"\nACCESS_TOKEN:\n{access_token}")
            print(f"\nREFRESH_TOKEN:\n{refresh_token}")
            print("\n" + "=" * 60)
            print("위 토큰을 .env 파일에 저장하세요:")
            print("=" * 60)
            print(f'KAKAO_REST_API_KEY="{rest_api_key}"')
            print(f'KAKAO_ACCESS_TOKEN="{access_token}"')

            # .env 파일에 자동 저장 옵션
            save = input("\n.env 파일에 자동으로 저장할까요? (y/n): ").strip().lower()
            if save == "y":
                with open(".env", "w", encoding="utf-8") as f:
                    f.write(f'KAKAO_REST_API_KEY="{rest_api_key}"\n')
                    f.write(f'KAKAO_ACCESS_TOKEN="{access_token}"\n')
                print("✅ .env 파일에 저장되었습니다!")

        else:
            print(f"\n❌ 토큰 발급 실패: {result}")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")


if __name__ == "__main__":
    get_access_token()
