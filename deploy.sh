#!/bin/sh
# 미리보기 이미지와 공유 페이지를 다시 만들고 push 합니다. GitHub Pages 반영까지 1~2분 걸립니다
set -e
cd "$(dirname "$0")"
python3 build.py
git add -A
git commit -q -m "${1:-deploy $(date '+%Y-%m-%d %H:%M')}" || true
git push -q origin main
echo "pushed: https://77hdumat.github.io/dev-archetype/"
