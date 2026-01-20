#!/bin/bash

# OpenJDK 17 설치 및 환경변수 설정 스크립트

set -e

echo "=== OpenJDK 17 설치 시작 ==="

# 패키지 업데이트 및 OpenJDK 설치
echo "[1/3] 패키지 업데이트 및 OpenJDK 17 설치 중..."
sudo apt update
sudo apt install -y openjdk-17-jdk

# 환경변수 설정
echo "[2/3] 환경변수 설정 중..."
JAVA_HOME_LINE='export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64'
PATH_LINE='export PATH=$JAVA_HOME/bin:$PATH'

# 이미 설정되어 있는지 확인 후 추가
if ! grep -q "JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" ~/.bashrc; then
    echo "$JAVA_HOME_LINE" >> ~/.bashrc
    echo "$PATH_LINE" >> ~/.bashrc
    echo "환경변수가 ~/.bashrc에 추가되었습니다."
else
    echo "환경변수가 이미 설정되어 있습니다."
fi

# 현재 세션에 적용
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# 설치 확인
echo "[3/3] 설치 확인..."
echo "---"
java -version
echo "---"
javac -version
echo "---"
echo "JAVA_HOME: $JAVA_HOME"

echo ""
echo "=== OpenJDK 17 설치 완료 ==="
echo "새 터미널에서 환경변수가 자동 적용됩니다."
