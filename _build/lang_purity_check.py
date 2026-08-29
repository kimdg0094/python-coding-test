# -*- coding: utf-8 -*-
# 교차 언어 오염 스캔:
#  - Python 콘텐츠(루트 ch*.md, trails/)에 C++ 언급이 있는지
#  - C++ 콘텐츠(cpp/)에 Python/파이썬 언급이 있는지
import os, glob, re, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\pqow0\OneDrive\0_Projects\coding_test\codetree-101-analysis"

def scan(files, pattern, label):
    rx = re.compile(pattern)
    total = 0
    hits = {}
    for f in sorted(files):
        rel = os.path.relpath(f, BASE)
        lines = open(f, encoding="utf-8").read().split("\n")
        fh = []
        for i, l in enumerate(lines):
            if rx.search(l):
                fh.append((i + 1, l.strip()[:110]))
        if fh:
            hits[rel] = fh
            total += len(fh)
    print(f"### {label}: {total}건, {len(hits)}개 파일")
    for rel, fh in hits.items():
        print(f"[{rel}] {len(fh)}건")
        for ln, txt in fh[:6]:
            print(f"   L{ln}: {txt}")
        if len(fh) > 6:
            print(f"   ... 외 {len(fh)-6}건")
    print()

py_files = glob.glob(os.path.join(BASE, "ch*.md")) + glob.glob(os.path.join(BASE, "trails", "*", "ch*.md"))
cpp_files = glob.glob(os.path.join(BASE, "cpp", "ch*.md")) + glob.glob(os.path.join(BASE, "cpp", "trails", "*", "ch*.md"))

# Python 콘텐츠에서 C++ 흔적 (단어 경계 고려: 'C++', 'cpp')
scan(py_files, r"C\+\+|(?<![A-Za-z])cpp(?![A-Za-z])", "PYTHON 콘텐츠 내 C++ 언급")
# C++ 콘텐츠에서 Python 흔적
scan(cpp_files, r"[Pp]ython|파이썬|[Pp]yodide", "C++ 콘텐츠 내 Python 언급")
