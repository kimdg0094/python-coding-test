# -*- coding: utf-8 -*-
"""문제 카드의 `- **예제**:` 표기 검증/정정 도구.

표기 규칙: 백틱 안에서 ` / `는 줄바꿈, 케이스 사이는 ` · `.
    - **예제**: `3 / 1 2 3` → `6` · `2 / 5 5` → `10`

검사 내용
  - 예제의 입력을 실제로 정답 코드에 넣어 돌린 뒤, 출력 표기가 실제 출력의 "줄 구조"를 담고 있는지 본다.
  - 여러 줄 출력을 `1 2 3`처럼 공백으로 이어 쓰거나 `1` `2` `3`처럼 백틱을 나열한 경우 → FIX 대상.
  - 입력도 같은 방식(백틱 나열 `5` `3` `0`, 또는 여러 줄 입력을 한 줄로)이면 FIX 대상.
  - 표기와 실제 출력이 아예 다른 경우는 MISMATCH로 보고만 한다(수동 확인).
  - 펜스(```)로 쓴 예제와 산문형 예제(PROSE)는 건너뛴다.

사용법
  python _build/verify_examples.py                 # 보고만 (FIX/MISMATCH/RUNERR)
  python _build/verify_examples.py --show all      # 전체 판정 출력
  python _build/verify_examples.py --fix           # 자동 정정 가능한 항목을 md에 반영
  python _build/verify_examples.py --fix trails/novice-low/ch05c.md   # 특정 파일만
  python _build/verify_examples.py --fix --normalize   # 표기 통일까지: `a` / `b` → `a / b`, 케이스 사이 ` / ` → ` · `
"""
import os, re, sys, glob, subprocess, argparse, collections
sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROB_HEAD = re.compile(r"^\*\*(\d+\))\s*(.*?)\*\*\s*(?:·\s*(.+?))?\s*$")
JOIN_WORDS = {"그리고", "및", "(줄바꿈)"}   # 출력 줄 사이에 끼어 있어도 지워도 되는 낱말/표시

# ---------- 문제/러너 추출 ----------
def problems(lines):
    heads = [i for i, l in enumerate(lines)
             if PROB_HEAD.match(l.strip()) or l.startswith("### ")]
    for k, i in enumerate(heads):
        j = heads[k + 1] if k + 1 < len(heads) else len(lines)
        yield i, lines[i].strip(), i + 1, j

def parse_runner(body):
    sol, tests, mode, io, cur, inr = [], [], None, None, None, False
    for l in body:
        s = l.strip()
        if not inr:
            if s.startswith("```runner"): inr = True
            continue
        if s == "```": break
        if s == "@@SOLUTION": mode = "s"; continue
        if s == "@@TESTS": mode = "t"; continue
        if s == "@@EXPL": mode = None; continue
        if mode == "s": sol.append(l)
        elif mode == "t":
            if s == "--IN": cur = {"in": [], "out": []}; tests.append(cur); io = "in"; continue
            if s == "--OUT": io = "out"; continue
            if cur is not None and io: cur[io].append(l)
    code = "\n".join(sol).strip("\n")
    code = re.sub(r"^```[a-zA-Z0-9]*\n", "", code); code = re.sub(r"\n```\s*$", "", code)
    tests = [{"in": "\n".join(t["in"]).strip("\n"), "out": "\n".join(t["out"]).strip("\n")} for t in tests]
    return code, tests

def example_span(lines, b, e):
    """예제 불릿(여러 개 가능)과 그 연속 줄의 [시작, 끝) 줄 범위. 없으면 None."""
    start = end = None
    for i in range(b, e):
        s = lines[i].strip()
        if s.startswith("```runner"): break
        if s.startswith("- **예제**"):
            if start is None: start = i
            end = i + 1; continue
        if start is not None:
            if re.match(r"^- \*\*", s): break
            if s: end = i + 1
    return (start, end) if start is not None else None

# ---------- 토큰화 ----------
TOK = re.compile(r"(?P<code>`[^`\n]*`)|(?P<paren>\((?:[^()\n]|\([^()\n]*\))*\))|(?P<arrow>→)|(?P<slash>/)"
                 r"|(?P<sep>·|,|\||;)|(?P<nl>\n)|(?P<ws>[ \t]+)|(?P<text>[^`()→/·,|;\n \t]+)")

def tokenize(text, base):
    toks = []
    for m in TOK.finditer(text):
        kind, val = m.lastgroup, m.group(0)
        if kind == "ws": continue
        if kind == "paren":
            if "입력 없음" in val: kind = "noin"
            elif "출력 없음" in val or re.match(r"^\(빈 줄[^()]*\)$", val): kind = "noout"
            elif re.match(r"^\(줄\s*\d+\)$", val): kind = "lineno"
            else: kind = "text"
        if kind == "code" and val[1:-1] in ("입력", "출력"): kind = "text"   # `입력`: … → `출력`: … 라벨
        toks.append({"k": kind, "v": val, "s": base + m.start(), "e": base + m.end()})
    return toks

def split_lines(code_text):
    parts = re.split(r"\s*/\s*", code_text) if code_text != "" else [""]
    return ["" if pt == "(빈 줄)" else pt for pt in parts]   # 코드 상자 안의 (빈 줄) = 빈 줄

def sep_kind(between):
    ks = {t["k"] for t in between}
    if "sep" in ks: return "sep"
    if "lineno" in ks: return "lineno"
    if "slash" in ks: return "slash"
    if "text" in ks or "noin" in ks or "noout" in ks: return "text"
    if "nl" in ks: return "nl"
    return "adj"

# ---------- 케이스 파싱 ----------
def parse_cases(toks, run):
    """화살표로 나눈 그룹 → 케이스 목록.
    case = {in: [(tok, between)], out: [(tok, between)], noin, noout, prose, lineno_in}"""
    groups, items, between, marks = [], [], [], []
    for t in toks:
        if t["k"] == "code":
            items.append((t, between)); between = []
        elif t["k"] == "arrow":
            groups.append({"items": items, "marks": marks, "tail": between}); items, between, marks = [], [], []
        else:
            between.append(t); marks.append(t)
    groups.append({"items": items, "marks": marks, "tail": between})
    if len(groups) < 2: return []
    n_cases = len(groups) - 1
    cases = [{"in": [], "out": [], "noin": False, "noout": False, "prose": False, "lineno_in": False, "sep_toks": []}
             for _ in range(n_cases)]
    # 그룹 0 = 케이스 0 입력
    g0 = groups[0]
    cases[0]["in"] = g0["items"]
    cases[0]["noin"] = any(m["k"] == "noin" for m in g0["marks"])
    cases[0]["lineno_in"] = any(m["k"] == "lineno" for m in g0["marks"])
    for g in range(1, len(groups)):
        items = groups[g]["items"]; marks = groups[g]["marks"]
        prev = cases[g - 1]
        if g == len(groups) - 1:                       # 마지막 그룹은 전부 출력
            prev["out"] = items
            prev["noout"] = any(m["k"] == "noout" for m in marks)
            break
        nxt = cases[g]
        cut = None
        for j in range(len(items) - 1, 0, -1):         # 명시 구분(· , | ;)
            if sep_kind(items[j][1]) == "sep": cut = j; break
        if cut is None:                                # 실제 출력과 대조
            prev["out"] = items
            actual = run_case(prev, run)
            if actual is not None:
                for j in range(0, len(items) + 1):
                    if displayed_lines(items[:j]) == actual: cut = j; break
        if cut is None:
            for j in range(len(items) - 1, 0, -1):
                if sep_kind(items[j][1]) == "nl": cut = j; break
        if cut is None:
            for j in range(len(items) - 1, 0, -1):
                if sep_kind(items[j][1]) == "slash": cut = j; break
        if cut is None or cut == 0 and len(items) == 0:
            prev["prose"] = True; nxt["prose"] = True
            prev["out"] = items; continue
        prev["out"] = items[:cut]
        if cut < len(items): nxt["sep_toks"] = items[cut][1]      # 케이스 사이 구분 토큰(` / ` → ` · ` 통일용)
        nxt["in"] = [(t, [] if n == 0 else b) for n, (t, b) in enumerate(items[cut:])]
        head_marks = []
        for t, b in items[:cut]: head_marks.extend(b)
        tail_marks = []
        for t, b in items[cut:]: tail_marks.extend(b)
        tail_marks.extend(groups[g]["tail"])
        prev["noout"] = any(m["k"] == "noout" for m in head_marks + (groups[g]["tail"] if cut == len(items) else []))
        nxt["noin"] = any(m["k"] == "noin" for m in tail_marks)
        nxt["lineno_in"] = any(m["k"] == "lineno" for m in tail_marks)
    return cases

def in_lines_of(case):
    if case["noin"]: return []
    lines = []
    for t, _ in case["in"]:
        lines.extend(split_lines(t["v"][1:-1]))
    return lines

def displayed_lines(items):
    lines = []
    for t, _ in items:
        lines.extend(split_lines(t["v"][1:-1]))
    return lines

_cache = {}
def run_case(case, run):
    key = tuple(in_lines_of(case))
    if key not in _cache:
        _cache[key] = run("\n".join(key) + ("\n" if key else ""))
    return _cache[key]

def make_runner(code):
    def run(stdin):
        try:
            p = subprocess.run([sys.executable, "-c", code], input=stdin, capture_output=True, text=True,
                               timeout=10, encoding="utf-8",
                               env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1"))
            if p.returncode != 0: return None
            lines = [l.rstrip() for l in p.stdout.replace("\r\n", "\n").split("\n")]
            while lines and lines[-1] == "": lines.pop()
            return lines
        except Exception:
            return None
    return run

# ---------- 판정 ----------
def mergeable(items):
    """items[1:]의 between 토큰이 줄바꿈/공백/슬래시/허용 낱말뿐이면 하나의 백틱으로 합쳐도 안전"""
    for _, b in items[1:]:
        for t in b:
            if t["k"] in ("nl", "slash"): continue
            if t["k"] in ("text", "paren") and t["v"] in JOIN_WORDS: continue
            return False
    return True

def judge(case, run, tests, normalize=False):
    """→ (verdict, actual, fixes) fixes = [(start, end, replacement)]
    normalize=True면 이미 맞는 표기도 정식 표기로 통일한다(`a` / `b` → `a / b`, 입력 `3`/`red` → `3 / red`)."""
    if case["prose"]: return "PROSE", None, []
    if not case["in"] and not case["noin"]: return "SKIP", None, []
    if not case["out"] and not case["noout"]: return "SKIP", None, []
    fixes = []
    actual = run_case(case, run)
    in_fix = None
    if actual is None and len(case["in"]) == 1 and not case["noin"]:
        # 여러 줄 입력을 한 줄로 이어 쓴 경우: 러너 테스트 입력과 대조
        span = case["in"][0][0]["v"][1:-1]
        for t in tests:
            tl = t["in"].split("\n")
            if len(tl) > 1 and " ".join(tl) == span:
                cand = run("\n".join(tl) + "\n")
                if cand is not None:
                    actual = cand; in_fix = tl; break
    if actual is None: return "RUNERR", None, []
    ot = case["out"]
    disp = [] if case["noout"] else displayed_lines(ot)
    seps = [sep_kind(b) for _, b in ot[1:]]
    if disp == actual:
        if len(actual) > 1 and any(s in ("adj", "nl", "text") for s in seps):
            verdict = "FIX-OUT-ADJ"
        elif len(actual) > 1 and len(ot) > 1:
            verdict = "OK-MARKED"                       # `a` / `b` 또는 `a`(줄1) `b`(줄2)
            if normalize and mergeable(ot):
                fixes.append((ot[0][0]["s"], ot[-1][0]["e"], "`" + " / ".join(actual) + "`"))
                verdict = "NORM-OUT"
        else:
            verdict = "OK"
    elif len(ot) == 1 and len(actual) > 1 and ot[0][0]["v"][1:-1] == " ".join(actual):
        verdict = "FIX-OUT-SPACE"
    elif len(ot) == 1 and len(actual) > 1 and \
            ot[0][0]["v"][1:-1].replace(" ", "") == "/".join(actual).replace(" ", ""):
        verdict = "OK"
    else:
        verdict = "MISMATCH"
    if verdict.startswith("FIX-OUT"):
        if mergeable(ot):
            fixes.append((ot[0][0]["s"], ot[-1][0]["e"], "`" + " / ".join(actual) + "`"))
        else:
            verdict += "(manual)"
    it = case["in"]
    if verdict.startswith(("OK", "FIX-OUT", "NORM")) and not case["noin"]:
        if in_fix:
            fixes.append((it[0][0]["s"], it[0][0]["e"], "`" + " / ".join(in_fix) + "`"))
            verdict += "+FIX-IN-SPACE"
        elif len(it) > 1 and not case["lineno_in"]:
            iseps = [sep_kind(b) for _, b in it[1:]]
            if any(s in ("adj", "nl", "text") for s in iseps) or (normalize and "slash" in iseps):
                if mergeable(it):
                    fixes.append((it[0][0]["s"], it[-1][0]["e"], "`" + " / ".join(in_lines_of(case)) + "`"))
                    verdict += "+FIX-IN-ADJ" if any(s in ("adj", "nl", "text") for s in iseps) else "+NORM-IN"
                else:
                    verdict += "+FIX-IN-ADJ(manual)"
    return verdict, actual, fixes

# ---------- 메인 ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--normalize", action="store_true", help="맞는 표기도 정식 표기로 통일(--fix와 함께)")
    ap.add_argument("--show", default="FIX,MISMATCH,RUNERR,OK+FIX",
                    help="출력할 판정 종류(쉼표 구분, 접두어 일치; all=전부)")
    args = ap.parse_args()
    files = args.files or (sorted(glob.glob(os.path.join(BASE, "ch*.md")))
                           + sorted(glob.glob(os.path.join(BASE, "trails", "*", "ch*.md"))))
    show = tuple(x for x in args.show.split(",") if x)
    stats = collections.Counter(); changed = 0
    for f in files:
        f = os.path.abspath(f)
        text = open(f, encoding="utf-8").read()
        lines = text.split("\n")
        offs = [0]
        for l in lines: offs.append(offs[-1] + len(l) + 1)
        file_fixes = []
        for hi, head, b, e in problems(lines):
            sp = example_span(lines, b, e)
            if sp is None: stats["no-example"] += 1; continue
            s0, e0 = sp
            ex = "\n".join(lines[s0:e0])
            if "```" in ex: stats["fenced"] += 1; continue
            code, tests = parse_runner(lines[b:e])
            if not code: stats["no-runner"] += 1; continue
            run = make_runner(code)
            _cache.clear()
            ex = re.sub(r"- \*\*예제\*\*:?", lambda m: " " * len(m.group(0)), ex)  # 위치 보존
            ex = "\n".join(" " * len(l) if re.match(r"^\s*(?:-\s*)?\(?검산", l) else l
                           for l in ex.split("\n"))                                 # 검산 메모 줄은 제외(위치 보존)
            toks = tokenize(ex, offs[s0])
            cases = parse_cases(toks, run)
            if not cases: stats["no-arrow"] += 1
            for ci, c in enumerate(cases):
                verdict, actual, fixes = judge(c, run, tests, args.normalize)
                key = verdict.replace("(manual)", "")
                stats[key] += 1
                # 실행으로 확인된 케이스 뒤에 오는 ` / ` 구분자는 ` · `로 통일
                if args.normalize and verdict.startswith(("OK", "FIX", "NORM")) and ci + 1 < len(cases):
                    st = cases[ci + 1]["sep_toks"]
                    sl = [t for t in st if t["k"] in ("slash", "sep") and t["v"] != "·"]
                    if len(sl) == 1 and all(t["k"] in ("slash", "sep", "nl") for t in st):
                        t0 = sl[0]
                        rep = "·" if text[t0["s"] - 1] == " " else " ·"
                        fixes.append((t0["s"], t0["e"], rep)); verdict += "+NORM-SEP"; stats["NORM-SEP"] += 1
                if "all" in show or verdict.startswith(show) or ("+FIX" in verdict and "OK+FIX" in show)                         or ("NORM" in verdict and "NORM" in show):
                    rel = os.path.relpath(f, BASE)
                    disp = None if c["prose"] else displayed_lines(c["out"])
                    print(f"{verdict:22} {rel}:{s0+1} {head[:34]!r}\n"
                          f"    in={in_lines_of(c) if not c['prose'] else '?'}  shown={disp}  actual={actual}")
                file_fixes.extend(fixes)
        if args.fix and file_fixes:
            file_fixes.sort(key=lambda x: x[0], reverse=True)
            for s, e, rep in file_fixes:
                text = text[:s] + rep + text[e:]
            open(f, "w", encoding="utf-8", newline="\n").write(text)
            changed += 1
            print(f"== fixed {len(file_fixes)} span(s) in {os.path.relpath(f, BASE)}")
    print("\n" + ", ".join(f"{k}:{v}" for k, v in sorted(stats.items())))
    if args.fix: print(f"files changed: {changed}")

if __name__ == "__main__":
    main()
