import random
import os
from datetime import datetime, timedelta

def generate_dummy_log(file_path='server.log', num_lines=25000000):
    """
    테스트를 위한 대용량 더미 로그 파일을 생성합니다.
    기본값인 25,000,000줄 설정 시 약 1GB 이상의 파일이 생성됩니다.
    
    Args:
        file_path (str): 생성할 로그 파일의 경로
        num_lines (int): 생성할 로그 줄 수 (기본 25,000,000줄 -> 약 1.1~1.2GB)
    """
    levels = ['INFO', 'DEBUG', 'WARNING', 'ERROR']
    messages = [
        "User logged in",
        "Database connection established",
        "API request received",
        "Cache miss for key: user_123",
        "Invalid password attempt",
        "Disk space low",
        "Unexpected token in request",
        "Job queue processed successfully",
        "Connection timeout from upstream"
    ]
    
    start_time = datetime.now()
    
    print(f"[{file_path}] 생성 시작... (총 {num_lines:,}줄, 예상 크기: {num_lines * 45 / 1024 / 1024 / 1024:.2f} GB)")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        # 대량 쓰기 성능을 위해 버퍼링을 고려하면 좋을 수 있지만, 
        # 한 줄씩 써도 파이썬 내부 버퍼링이 잘 작동합니다.
        for i in range(num_lines):
            timestamp = (start_time + timedelta(seconds=i)).strftime('%Y-%m-%d %H:%M:%S')
            level = random.choices(levels, weights=[70, 15, 10, 5])[0]
            msg = random.choice(messages)
            
            f.write(f"[{timestamp}] {level}: {msg}\n")
            
            # 진행률 출력 (10% 단위로 변경하여 출력량 감소)
            if (i + 1) % (num_lines // 10) == 0:
                percent = (i + 1) / num_lines * 100
                elapsed = (datetime.now() - start_time).seconds
                print(f"진행률: {percent:.0f}% 완료 ({i + 1:,}줄, 소요 시간: {elapsed}초)")

    print(f"생성 완료: {os.path.abspath(file_path)}")

if __name__ == "__main__":
    # 스크립트로 직접 실행 시 기본값으로 생성
    generate_dummy_log()
