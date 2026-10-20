# 결과별 공유 페이지(r/*.html)와 미리보기 이미지(og/*.png)를 만듭니다
# index.html 의 COMBOS 를 읽어서 만들기 때문에 조합 이름을 바꾸면 다시 실행하면 됩니다
import html
import pathlib
import re
import subprocess

SITE = 'https://77hdumat.github.io/dev-archetype/'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
ROOT = pathlib.Path(__file__).parent
NAMES = {'P': '프로토타이퍼', 'B': '빌더', 'S': '스위퍼', 'G': '그로워', 'M': '메인테이너'}

src = (ROOT / 'index.html').read_text()
combos = re.findall(r"^\s+([PBSGM]{2}): \['([^']+)', '([^']+)'", src, re.M)
assert len(combos) == 10, combos

PAGE = '''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="canonical" href="{site}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="개발자 아키타입 테스트">
<meta property="og:locale" content="ko_KR">
<meta property="og:url" content="{site}r/{key}.html">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}og/{key}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}og/{key}.png">
<script>location.replace('../' + location.search);</script>
</head>
<body><a href="../">개발자 아키타입 테스트로 가기</a></body>
</html>
'''

(ROOT / 'r').mkdir(exist_ok=True)
(ROOT / 'og').mkdir(exist_ok=True)


def shot(key):
    subprocess.run([
        CHROME, '--headless=new', '--hide-scrollbars', '--force-device-scale-factor=1',
        '--window-size=1200,630', '--virtual-time-budget=5000',
        f'--screenshot={ROOT / "og" / (key + ".png")}',
        f'{(ROOT / "index.html").as_uri()}?og={key}',
    ], check=True, capture_output=True)


singles = [(t, f'{n} 중심형', f'{n} 성향이 다른 역할보다 뚜렷하게 앞섭니다.') for t, n in NAMES.items()]
for key, name, desc in combos + singles:
    code = '+'.join(key)
    roles = ' + '.join(NAMES[t] for t in key) if len(key) == 2 else '주 역할 ' + NAMES[key]
    (ROOT / 'r' / f'{key}.html').write_text(PAGE.format(
        site=SITE, key=key,
        title=html.escape(f'나의 개발자 아키타입은 {code}, {name}'),
        desc=html.escape(f'{roles}. {desc} 40문항으로 나의 역할도 알아보세요.'),
    ))
    shot(key)
shot('main')
print('ok', len(combos) + len(singles), 'pages')
