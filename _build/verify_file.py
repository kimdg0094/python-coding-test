# -*- coding: utf-8 -*-
# 사용법: python _build/verify_file.py trails/<trail>/chNNx.md [다른 파일...]
# 지정한 md 파일의 구조(문제 카드·러너 블록)와 정답 코드 실행 결과를 검증한다.
import sys, re, os, subprocess, time
sys.stdout.reconfigure(encoding="utf-8")

DIFFS = {"Easy", "Medium", "Hard"}
PROB = re.compile(r"^\*\*(\d+)\)\s*(.+?)\*\*\s*·\s*(\S+)\s*$")
FIELDS = ("요구사항", "입력", "출력", "예제", "셀프체크")

def parse_runner(content_lines):
    sol, expl, tests = [], [], []
    cur_in, cur_out, io_mode, mode = [], [], None, None
    seen = {"sol": 0, "tests": 0, "expl": 0}
    def flush():
        if cur_in or cur_out:
            tests.append({"in": "\n".join(cur_in), "out": "\n".join(cur_out)})
        return [], []
    for l in content_lines:
        s = l.strip()
        if s == "@@SOLUTION": mode = "sol"; seen["sol"] += 1; continue
        if s == "@@TESTS": mode = "tests"; io_mode = None; seen["tests"] += 1; continue
        if s == "@@EXPL": cur_in, cur_out = flush(); mode = "expl"; seen["expl"] += 1; continue
        if mode == "sol": sol.append(l)
        elif mode == "tests":
            if s == "--IN": cur_in, cur_out = flush(); io_mode = "in"; continue
            if s == "--OUT": io_mode = "out"; continue
            if io_mode == "in": cur_in.append(l)
            elif io_mode == "out": cur_out.append(l)
        elif mode == "expl": expl.append(l)
    if mode == "tests": cur_in, cur_out = flush()
    code = "\n".join(sol).strip("\n")
    code = re.sub(r"^```[a-zA-Z0-9]*\n", "", code); code = re.sub(r"\n```\s*$", "", code)
    tests = [{"in": t["in"].strip("\n"), "out": t["out"].strip("\n")} for t in tests]
    return code, tests, "\n".join(expl).strip(), seen

def norm(s): return re.sub(r"[ \t]+(?=\n)", "", (s or "")).rstrip()

def run(code, stdin):
    try:
        t0 = time.time()
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
        p = subprocess.run([sys.executable, "-c", code], input=stdin, capture_output=True,
                           text=True, timeout=10, encoding="utf-8", env=env)
        dt = time.time() - t0
        if p.returncode != 0:
            tail = (p.stderr or "").strip().splitlines()
            return None, (tail[-1] if tail else "runtime error"), dt
        return p.stdout, None, dt
    except subprocess.TimeoutExpired: return None, "TIMEOUT(10s)", 10.0
    except Exception as e: return None, str(e), 0.0

def check_file(path):
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    errors, warns = [], []
    heads = [(i, l) for i, l in enumerate(lines) if l.startswith("## ")]
    if not heads: errors.append("'## L..' 레슨 제목이 없음")
    for i, l in heads:
        if not re.match(r"^## L\d+\.\s+\S", l): errors.append(f"line {i+1}: 레슨 제목 형식 오류 → {l!r} (예: '## L11. 추가 연습 — ...')")
    if "**문제**" not in text: errors.append("'**문제**' 구분선이 없음")
    problems, cur, expected = [], None, 1
    i = 0
    while i < len(lines):
        l = lines[i]; s = l.strip()
        if s.startswith("## "): expected = 1
        m = PROB.match(s)
        if m:
            num, name, diff = int(m.group(1)), m.group(2), m.group(3)
            if num != expected: errors.append(f"line {i+1}: 문제 번호 {num} (기대 {expected})")
            expected = num + 1
            if diff not in DIFFS: errors.append(f"line {i+1}: 난이도 '{diff}' (Easy/Medium/Hard만 허용)")
            if cur and cur["runner"] is None: errors.append(f"문제 {cur['num']} '{cur['name']}': runner 블록 없음")
            cur = {"num": num, "name": name, "diff": diff, "runner": None, "line": i + 1, "body": []}
            problems.append(cur); i += 1; continue
        if s.startswith("```runner"):
            if cur is None: errors.append(f"line {i+1}: 문제 카드 밖의 runner")
            j = i + 1
            while j < len(lines) and lines[j].strip() != "```":
                if lines[j].strip().startswith("```"): errors.append(f"line {j+1}: runner 안에 중첩 펜스(```) 금지")
                j += 1
            if j >= len(lines): errors.append(f"line {i+1}: runner 블록이 닫히지 않음"); break
            if cur is not None:
                if cur["runner"] is not None: errors.append(f"문제 {cur['num']}: runner 블록 중복")
                cur["runner"] = lines[i + 1:j]
            i = j + 1; continue
        if cur is not None and cur["runner"] is None: cur["body"].append(l)
        i += 1
    if cur and cur["runner"] is None: errors.append(f"문제 {cur['num']} '{cur['name']}': runner 블록 없음")
    if not problems: errors.append("문제 카드(**N) 제목** · 난이도)가 하나도 없음")
    slow = 0
    for p in problems:
        body = "\n".join(p["body"])
        for key in FIELDS:
            if f"**{key}**" not in body: errors.append(f"문제 {p['num']} '{p['name']}': **{key}** 항목 없음")
        if p["runner"] is None: continue
        code, tests, expl, seen = parse_runner(p["runner"])
        if seen["sol"] != 1 or seen["tests"] != 1 or seen["expl"] != 1:
            errors.append(f"문제 {p['num']}: @@SOLUTION/@@TESTS/@@EXPL 각각 정확히 1번 필요 (현재 {seen})")
        if not code: errors.append(f"문제 {p['num']}: 정답 코드가 비어 있음"); continue
        # 입력이 없는 문제(출력 전용)는 두 번째 테스트가 첫 번째의 완전한 중복이라 1개를 허용
        input_free = all(not t["in"].strip() for t in tests)
        if not tests:
            errors.append(f"문제 {p['num']} '{p['name']}': 테스트가 없음")
        elif not input_free and len(tests) < 2:
            errors.append(f"문제 {p['num']} '{p['name']}': 테스트 {len(tests)}개 (입력 있는 문제는 최소 2개)")
        if len(expl) < 80: errors.append(f"문제 {p['num']}: @@EXPL 풀이가 너무 짧음/없음")
        if re.search(r"^\s*(import|from)\s+(numpy|pandas|scipy|requests|sympy)", code, re.M):
            errors.append(f"문제 {p['num']}: 외부 패키지 사용 금지")
        if "setrecursionlimit" in code: warns.append(f"문제 {p['num']}: setrecursionlimit 사용 — 테스트 입력을 작게(깊이 수천 이하) 유지할 것")
        for k, t in enumerate(tests):
            out, err, dt = run(code, t["in"])
            if dt > 1.5: slow += 1; warns.append(f"문제 {p['num']} 테스트 {k+1}: {dt:.1f}s 소요 (브라우저 실행 고려, 1초 이하 권장)")
            if err: errors.append(f"문제 {p['num']} '{p['name']}' 테스트 {k+1}: 실행 오류 → {err}"); break
            if norm(out) != norm(t["out"]):
                errors.append(f"문제 {p['num']} '{p['name']}' 테스트 {k+1}: 출력 불일치\n      실제: {norm(out)!r}\n      기대: {norm(t['out'])!r}"); break
    for i, l in enumerate(lines):
        if re.search(r"#include|std::|\bcout\b|\bcin\b|C\+\+|\bcpp\b", l): errors.append(f"line {i+1}: C++ 관련 언급 금지 → {l.strip()[:60]!r}")
    dist = {d: sum(1 for p in problems if p["diff"] == d) for d in ("Easy", "Medium", "Hard")}
    return problems, dist, errors, warns

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python verify_file.py <file.md> [...]"); sys.exit(2)
    bad = 0
    for path in sys.argv[1:]:
        if not os.path.exists(path): print(f"[{path}] 파일 없음"); bad += 1; continue
        problems, dist, errors, warns = check_file(path)
        print(f"[{os.path.relpath(path)}] 문제 {len(problems)}개 · Easy {dist['Easy']} / Medium {dist['Medium']} / Hard {dist['Hard']}")
        for w in warns: print("  WARN:", w)
        for e in errors: print("  ERROR:", e)
        print("  =>", "OK" if not errors else f"실패 {len(errors)}건")
        if errors: bad += 1
    sys.exit(1 if bad else 0)
