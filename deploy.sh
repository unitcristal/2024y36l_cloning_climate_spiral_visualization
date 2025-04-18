#!/bin/bash

set -e  # 에러 발생 시 즉시 종료

# y-l 날짜 포맷 (Python 스크립트 활용)
yl=$(python3 __scripts/yl_date.py)

# 1. 데이터 변환 (Docker에서 convert_csv.py 직접 실행)
echo "🚀 [1/6] CSV 변환 실행 중..."
docker run --rm -v "$PWD":/workspace climate_spiral python scripts/convert_csv.py

# 2. 데이터 테스트 (Docker에서 test_convert.py 실행)
echo "🔍 [2/6] 변환된 CSV 테스트 중..."
docker run --rm -v "$PWD":/workspace climate_spiral python scripts/test_convert.py

# 3. 배포 디렉토리 구성
DIST_DIR="dist"
echo "📁 [3/6] 배포 디렉토리 정리: $DIST_DIR"
rm -rf $DIST_DIR
mkdir $DIST_DIR

# 필요한 파일 복사
echo "📄 index.html, sketch.js, glb_temp.csv 복사 중..."
cp index/index.html index/sketch.js data/glb_temp.csv $DIST_DIR/

# 4. main 브랜치 커밋 (루트)
echo "📦 [4/6] main 브랜치 변경사항 커밋 중..."
git add .
git commit -m "updated and deployed on $yl" || echo "⚠️ main 브랜치에 커밋할 변경사항 없음"
git push origin main

# 5. gh-pages 브랜치 초기화 및 커밋
cd $DIST_DIR
git init > /dev/null
git checkout -b gh-pages > /dev/null

echo "🚀 [5/6] gh-pages 브랜치 커밋 준비 중..."
git add .
git commit -m "deployed on $yl"

# 6. 원격 저장소에 강제 푸시
REPO_URL="https://github.com/unitcristal/2024y36l_cloning_climate_spiral_visualization"

echo "🚀 [6/6] gh-pages 브랜치에 푸시 중..."
git remote add origin "$REPO_URL" 2>/dev/null || true
git push --force origin gh-pages

cd ..
echo "✅ 배포 완료: $yl"