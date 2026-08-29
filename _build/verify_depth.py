# -*- coding: utf-8 -*-
"""
「이론서 수준」 보완 작업 검증기 (DEPTH_SPEC.md 짝)

사용법
  python _build/verify_depth.py trails/<trail>/chNNz.md [...]   # z 파일 구조 검사
  python _build/verify_depth.py --diff                          # 기존 파일이 '추가만' 되었는지 git으로 검사
  python _build/verify_depth.py --diagrams                      # 전체 md의 ```text 도식 규칙 검사
"""
import sys, os, re, subprocess

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HANGUL = re.compile(r"[가-힣ㄱ-ㆎ]")
MAX_DIAGRAM_WIDTH = 80

Z_SECTIONS = ["**개념 지도**", "**뼈대 코드**", "**언제 무엇을 쓰나**",
              "**✅ 마스터 체크리스트**", "**⚠️ 자주 하는 실수**"]


def fences(lines):
    """(시작줄, 끝줄, 언어) 목록. 끝줄은 닫는 ``` 의 인덱스."""
    out, i = [], 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("```"):
            lang = s[3:].strip()
            j = i + 1
            while j < len(lines) and lines[j].strip() != "```":
                j += 1
            out.append((i, j, lang))
            i = j + 1
        else:
            i += 1
    return out


def check_diagrams(path, lines, errors, warns):
    """```text 도식: 한글 금지(정렬 깨짐), 80자 초과 금지."""
    n = 0
    for a, b, lang in fences(lines):
        if lang not in ("text", "diagram"):
            continue
        n += 1
        for k in range(a + 1, min(b, len(lines))):
            ln = lines[k]
            m = HANGUL.search(ln)
            if m:
                # 줄 끝 '#' 주석 안의 한글은 정렬에 영향이 없으므로 허용
                hash_at = ln.find("#")
                if not (hash_at != -1 and hash_at < m.start()):
                    errors.append(
                        f"line {k+1}: 도식(```text) 정렬 칸에 한글 — 폰트 폴백으로 어긋납니다. "
                        f"'#' 주석으로 옮기거나 도식 밖 캡션으로 → {ln.strip()[:50]!r}")
            if len(ln.rstrip()) > MAX_DIAGRAM_WIDTH:
                warns.append(f"line {k+1}: 도식 줄이 {len(ln.rstrip())}자 (권장 {MAX_DIAGRAM_WIDTH}자 이하)")
    return n


def check_z(path):
    """챕터 마무리 레슨(z 파일) 구조 검사."""
    errors, warns = [], []
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")

    heads = [l for l in lines if l.startswith("## ")]
    if not heads:
        errors.append("'## L{K}. ...' 레슨 제목이 없음")
    elif not re.match(r"^## L\d+\.\s+\S", heads[0]):
        errors.append(f"레슨 제목 형식 오류 → {heads[0]!r}")
    if len(heads) > 1:
        errors.append(f"레슨이 {len(heads)}개 — z 파일은 정확히 1개여야 함")
    if not text.lstrip().startswith("## L"):
        errors.append("파일이 '## L'로 시작하지 않음")

    if "**개념**" not in text:
        errors.append("'**개념**' 라벨이 없음")
    if "**문제**" in text:
        errors.append("'**문제**' 절이 있음 — z 파일은 문제를 넣지 않음")
    if "```runner" in text:
        errors.append("runner 블록이 있음 — z 파일은 문제를 넣지 않음")

    for sec in Z_SECTIONS:
        if sec not in text:
            errors.append(f"필수 절 없음: {sec}")

    # 체크리스트 항목
    checks = re.findall(r"^\s*-\s*\[ \]", text, re.M)
    if len(checks) < 8:
        errors.append(f"마스터 체크리스트 항목 {len(checks)}개 (최소 8개)")

    # 자주 하는 실수: 틀린/고친 코드 쌍
    bad = text.count("❌")
    good = text.count("✅ 고친") + text.count("✅ 올바른")
    mistakes_idx = text.find("**⚠️ 자주 하는 실수**")
    if mistakes_idx >= 0:
        tail = text[mistakes_idx:]
        if tail.count("❌") < 5:
            errors.append(f"자주 하는 실수 {tail.count('❌')}개 (최소 5개, ❌ 표시 기준)")
        if tail.count("```python") < 5:
            errors.append("자주 하는 실수에 코드 예시가 부족 (틀린/고친 코드 쌍 필요)")

    ndia = check_diagrams(path, lines, errors, warns)
    if ndia == 0:
        errors.append("개념 지도 도식(```text)이 없음")

    # 뼈대 코드
    skel_idx = text.find("**뼈대 코드**")
    if skel_idx >= 0:
        seg = text[skel_idx: text.find("**언제 무엇을 쓰나**") if "**언제 무엇을 쓰나**" in text else len(text)]
        if seg.count("```python") < 2:
            errors.append(f"뼈대 코드 템플릿 {seg.count('```python')}개 (최소 2개)")

    if re.search(r"#include|std::|\bcout\b|\bcin\b|C\+\+", text):
        errors.append("다른 언어(C++) 언급 금지")

    nlines = len([l for l in lines if l.strip()])
    if nlines < 60:
        warns.append(f"내용이 짧음 ({nlines}줄) — 권장 120~250줄")

    return errors, warns, {"diagrams": ndia, "checks": len(checks), "lines": len(lines)}


def git(args):
    return subprocess.run(["git"] + args, cwd=BASE, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def problem_tail(text):
    """각 레슨의 '**문제**' 이후 구간을 모두 이어붙인 것 — 절대 바뀌면 안 되는 영역."""
    out = []
    for block in re.split(r"^## ", text, flags=re.M):
        i = block.find("**문제**")
        if i >= 0:
            out.append(block[i:])
    return "\n<<<LESSON>>>\n".join(out)


def is_subsequence(old_lines, new_lines):
    """old의 모든 줄이 순서대로 new 안에 있는가(= 추가만 했는가)."""
    i = 0
    for ln in new_lines:
        if i < len(old_lines) and ln == old_lines[i]:
            i += 1
    return i == len(old_lines), i


def check_diff():
    """기존 추적 파일이 '추가만' 되었는지, 문제 영역이 그대로인지 git으로 검사."""
    r = git(["diff", "--name-only", "HEAD", "--", "trails", "ch01-basics.md", "ch02-io.md",
             "ch03-conditionals-1.md", "ch04-loops-1.md", "ch05-conditionals-2.md",
             "ch06-array-1d.md", "ch07-string.md", "ch08-loops-2.md",
             "ch09-nested-loops.md", "ch10-array-2d.md"])
    if r.returncode != 0:
        print("git diff 실패:", r.stderr.strip()[:200]); return 1
    files = [f.strip() for f in r.stdout.split("\n") if f.strip().endswith(".md")]
    if not files:
        print("변경된 기존 md 없음 (Part A 미실행 또는 이미 커밋됨)")
        return 0

    bad = 0
    print(f"변경된 기존 파일 {len(files)}개 검사\n")
    for f in files:
        old = git(["show", f"HEAD:{f}"])
        if old.returncode != 0:
            print(f"  [신규] {f} — HEAD에 없음(새 파일이면 정상)"); continue
        old_text = old.stdout
        new_text = open(os.path.join(BASE, f.replace("/", os.sep)), encoding="utf-8").read()

        errs = []
        ok, upto = is_subsequence(old_text.split("\n"), new_text.split("\n"))
        if not ok:
            errs.append(f"기존 줄이 수정/삭제됨 (원본 {upto}번째 줄 이후 불일치) — 추가만 허용")
        if problem_tail(old_text) != problem_tail(new_text):
            errs.append("'**문제**' 이후 구간이 변경됨 — 절대 금지")

        lines = new_text.split("\n")
        dia_err, dia_warn = [], []
        check_diagrams(f, lines, dia_err, dia_warn)
        errs += dia_err

        added = len(lines) - len(old_text.split("\n"))
        if errs:
            bad += 1
            print(f"  [실패] {f}  (+{added}줄)")
            for e in errs:
                print(f"          ERROR: {e}")
        else:
            print(f"  OK     {f}  (+{added}줄)")
    print(f"\n=> {'실패 ' + str(bad) + '건' if bad else '전부 OK (추가만, 문제 영역 무변경)'}")
    return 1 if bad else 0


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return 2
    if args[0] == "--diff":
        return check_diff()
    if args[0] == "--diagrams":
        import glob
        bad = 0
        pats = [os.path.join(BASE, "ch*.md"), os.path.join(BASE, "trails", "*", "ch*.md")]
        for path in sorted(sum((glob.glob(p) for p in pats), [])):
            lines = open(path, encoding="utf-8").read().split("\n")
            e, w = [], []
            n = check_diagrams(path, lines, e, w)
            if e or w:
                rel = os.path.relpath(path, BASE)
                print(f"[{rel}] 도식 {n}개")
                for x in e: print("  ERROR:", x); bad += 1
                for x in w: print("  WARN :", x)
        print("=> 도식 오류", bad, "건")
        return 1 if bad else 0

    bad = 0
    for path in args:
        if not os.path.exists(path):
            print(f"[{path}] 파일 없음"); bad += 1; continue
        errors, warns, st = check_z(path)
        rel = os.path.relpath(path, BASE)
        print(f"[{rel}] 도식 {st['diagrams']}개 · 체크리스트 {st['checks']}개 · {st['lines']}줄")
        for w in warns: print("  WARN :", w)
        for e in errors: print("  ERROR:", e)
        print("  =>", "OK" if not errors else f"실패 {len(errors)}건")
        if errors: bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
