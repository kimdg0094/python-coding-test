# -*- coding: utf-8 -*-
# 모든 md의 ```runner 블록에서 정답코드+테스트를 뽑아 실제로 실행해 채점 검증.
import os, re, sys, subprocess, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\pqow0\OneDrive\0_Projects\coding_test\codetree-101-analysis"

def parse_runner(content_lines):
    sol, expl, tests = [], [], []
    cur_in, cur_out, io_mode, mode = [], [], None, None
    def flush():
        if cur_in or cur_out:
            tests.append({"in": "\n".join(cur_in), "out": "\n".join(cur_out)})
        return [], []
    for l in content_lines:
        s = l.strip()
        if s == "@@SOLUTION": mode="sol"; continue
        if s == "@@TESTS": mode="tests"; io_mode=None; continue
        if s == "@@EXPL": cur_in, cur_out = flush(); mode="expl"; continue
        if mode=="sol": sol.append(l)
        elif mode=="tests":
            if s=="--IN": cur_in, cur_out = flush(); io_mode="in"; continue
            if s=="--OUT": io_mode="out"; continue
            if io_mode=="in": cur_in.append(l)
            elif io_mode=="out": cur_out.append(l)
        elif mode=="expl": expl.append(l)
    if mode=="tests": cur_in, cur_out = flush()
    code = "\n".join(sol).strip("\n")
    code = re.sub(r"^```[a-zA-Z0-9]*\n","",code); code = re.sub(r"\n```\s*$","",code)
    tests = [{"in": t["in"].strip("\n"), "out": t["out"].strip("\n")} for t in tests]
    return code, tests, "\n".join(expl).strip()

def find_runners(text):
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        if lines[i].strip().startswith("```runner"):
            j = i+1
            while j < len(lines) and lines[j].strip() != "```": j += 1
            out.append(lines[i+1:j]); i = j+1
        else: i += 1
    return out

def norm(s): return re.sub(r"[ \t]+(?=\n)","", (s or "")).rstrip()

def run(code, stdin):
    try:
        p = subprocess.run([sys.executable, "-c", code], input=stdin, capture_output=True, text=True, timeout=10, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1"))
        if p.returncode != 0: return None, (p.stderr or "").strip().splitlines()[-1:] and (p.stderr.strip().splitlines()[-1]) or "runtime error"
        return p.stdout, None
    except subprocess.TimeoutExpired: return None, "TIMEOUT"
    except Exception as e: return None, str(e)

files = glob.glob(os.path.join(BASE,"ch*.md")) + glob.glob(os.path.join(BASE,"trails","*","ch*.md"))
total=passed=failed=noblock=0
fails=[]
for f in sorted(files):
    with open(f, encoding="utf-8") as fh: text = fh.read()
    for block in find_runners(text):
        total += 1
        code, tests, _ = parse_runner(block)
        if not code or not tests:
            noblock += 1; continue
        ok = True; detail = ""
        for k,t in enumerate(tests):
            out, err = run(code, t["in"])
            if err is not None: ok=False; detail=f"err@{k+1}:{err}"; break
            if norm(out) != norm(t["out"]): ok=False; detail=f"mismatch@{k+1}: got {norm(out)!r} exp {norm(t['out'])!r}"; break
        if ok: passed += 1
        else:
            failed += 1
            fails.append(f"FAIL {os.path.relpath(f,BASE)} :: {detail}")
print(f"runner blocks: {total} | passed: {passed} | FAILED: {failed} | empty: {noblock}")
for x in fails[:60]: print(x)
