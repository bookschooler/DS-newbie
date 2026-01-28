"""
카카오톡 메시지 전송 모듈
"나에게 보내기" 기능 사용
"""
import requests
import json
from typing import List, Dict
from config import KAKAO_ACCESS_TOKEN


class KakaoSender:
    """카카오톡으로 메시지를 전송하는 클래스"""

    SEND_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    def __init__(self, access_token: str = None):
        self.access_token = access_token or KAKAO_ACCESS_TOKEN
        if not self.access_token:
            raise ValueError("카카오 Access Token이 필요합니다. .env 파일을 확인하세요.")

    def _make_text_message(self, text: str, link_url: str = None) -> dict:
        """텍스트 메시지 템플릿 생성"""
        template = {
            "object_type": "text",
            "text": text,
            "link": {
                "web_url": link_url or "https://news.naver.com",
                "mobile_web_url": link_url or "https://news.naver.com"
            },
            "button_title": "뉴스 더보기"
        }
        return template

    def _make_list_message(self, title: str, articles: List[Dict]) -> dict:
        """리스트 메시지 템플릿 생성 (최대 3개 아이템)"""
        contents = []
        for article in articles[:3]:  # 리스트형은 최대 3개
            contents.append({
                "title": article["title"][:40],  # 제목 길이 제한
                "description": article.get("source", ""),
                "image_url": "",
                "image_width": 50,
                "image_height": 50,
                "link": {
                    "web_url": article["link"],
                    "mobile_web_url": article["link"]
                }
            })

        template = {
            "object_type": "list",
            "header_title": title,
            "header_link": {
                "web_url": "https://news.naver.com",
                "mobile_web_url": "https://news.naver.com"
            },
            "contents": contents,
            "buttons": [
                {
                    "title": "뉴스 더보기",
                    "link": {
                        "web_url": "https://news.naver.com",
                        "mobile_web_url": "https://news.naver.com"
                    }
                }
            ]
        }
        return template

    def send_text(self, text: str, link_url: str = None) -> bool:
        """텍스트 메시지 전송"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        template = self._make_text_message(text, link_url)
        data = {"template_object": json.dumps(template)}

        try:
            response = requests.post(self.SEND_URL, headers=headers, data=data)
            if response.status_code == 200:
                print("✓ 메시지 전송 성공!")
                return True
            else:
                print(f"✗ 전송 실패: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ 전송 오류: {e}")
            return False

    def send_news_summary(self, all_news: Dict[str, List[Dict]]) -> bool:
        """뉴스 요약을 텍스트로 전송 (전체 기사 + 링크 포함)"""
        message_parts = ["[오늘의 뉴스 클리핑]\n"]

        for category, articles in all_news.items():
            if articles:
                message_parts.append(f"\n\n===== {category} =====")
                for i, article in enumerate(articles, 1):  # 전체 기사 포함
                    title = article["title"]
                    link = article.get("link", "")
                    message_parts.append(f"\n{i}. {title}")
                    message_parts.append(f"    {link}")

        full_message = "\n".join(message_parts)

        return self.send_text(full_message)


def get_new_token_guide():
    """토큰 발급 가이드 출력"""
    guide = """
    ╔════════════════════════════════════════════════════════════╗
    ║          카카오 API 토큰 발급 가이드                          ║
    ╠════════════════════════════════════════════════════════════╣
    ║                                                            ║
    ║  1. https://developers.kakao.com 접속                      ║
    ║                                                            ║
    ║  2. 로그인 후 [내 애플리케이션] → [애플리케이션 추가]           ║
    ║                                                            ║
    ║  3. 앱 생성 후 [앱 키] 에서 REST API 키 복사                 ║
    ║                                                            ║
    ║  4. [카카오 로그인] 메뉴 → 활성화 설정: ON                    ║
    ║                                                            ║
    ║  5. [동의항목] → "카카오톡 메시지 전송" 동의 설정               ║
    ║                                                            ║
    ║  6. 아래 URL로 접속하여 인증 (REST_API_KEY 교체):             ║
    ║     https://kauth.kakao.com/oauth/authorize                ║
    ║     ?client_id={REST_API_KEY}                              ║
    ║     &redirect_uri=https://example.com/oauth                ║
    ║     &response_type=code                                    ║
    ║                                                            ║
    ║  7. 리다이렉트된 URL에서 code= 값 복사                        ║
    ║                                                            ║
    ║  8. get_access_token.py 실행하여 토큰 발급                   ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(guide)


if __name__ == "__main__":
    get_new_token_guide()
