# -*- coding: utf-8 -*-
# build_html.py / cpp_build.py 의 CSS 블록을 theme.make_css() 호출로 교체하고 JS에 JS_UI를 연결.
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BD = os.path.dirname(os.path.abspath(__file__))

HEADER = (
    "import sys as _sys, os as _os\n"
    "_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))\n"
    "from theme import make_css, JS_UI\n"
)

for fname, lang in (("build_html.py", "python"), ("cpp_build.py", "cpp")):
    p = os.path.join(BD, fname)
    src = open(p, encoding="utf-8").read()
    if "from theme import" in src:
        print(f"{fname}: 이미 적용됨 — 건너뜀")
        continue
    # CSS 블록 교체 (내부에 삼중따옴표 없음을 전제로 non-greedy 매칭)
    n1 = len(re.findall(r'CSS = """.*?"""', src, flags=re.S))
    if n1 != 1:
        print(f"{fname}: CSS 블록 매칭 {n1}개 — 중단"); continue
    src = re.sub(r'CSS = """.*?"""', HEADER + f'CSS = make_css("{lang}")', src, count=1, flags=re.S)
    # JS 정의 끝에 JS_UI 연결
    n2 = len(re.findall(r'JS = """.*?"""', src, flags=re.S))
    if n2 != 1:
        print(f"{fname}: JS 블록 매칭 {n2}개 — 중단"); continue
    src = re.sub(r'(JS = """.*?""")', r'\1\nJS = JS + JS_UI', src, count=1, flags=re.S)
    open(p, "w", encoding="utf-8").write(src)
    print(f"{fname}: 테마 적용 완료 (lang={lang})")
