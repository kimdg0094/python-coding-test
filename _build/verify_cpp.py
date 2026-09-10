# -*- coding: utf-8 -*-
# cpp/ 의 ```runner 블록에서 C++ 정답 코드+테스트를 뽑아 g++로 컴파일·실행해 채점 검증.
import os, re, sys, subprocess, glob, tempfile
sys.stdout.reconfigure(encoding='utf-8')

# g++ 위치: PATH 우선, 없으면 winget 설치 경로
GPP = None
from shutil import which
GPP = which("g++") or r"C:\Users\pqow0\AppData\Local\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\mingw64\bin\g++.exe"

BASE = r"C:\Users\pqow0\OneDrive\0_Projects\coding_test\codetree-101-analysis\cpp"

def parse_runner(content_lines):
    sol, expl, tests = [], [], []
    cur_in, cur_out, io_mode, mode = [], [], None, None
    def flush():
        if cur_in or cur_out:
            tests.append({"in": "\n".join(cur_in), "out": "\n".join(cur_out)})
        return [], []
    for l in content_lines:
        s = l.strip()
        if s == "@@SOLUTION": mode = "sol"; continue
        if s == "@@TESTS": mode = "tests"; io_mode = None; continue
        if s == "@@EXPL": cur_in, cur_out = flush(); mode = "expl"; continue
        if mode == "sol": sol.append(l)
        elif mode == "tests":
            if s == "--IN": cur_in, cur_out = flush(); io_mode = "in"; continue
            if s == "--OUT": io_mode = "out"; continue
            if io_mode == "in": cur_in.append(l)
            elif io_mode == "out": cur_out.append(l)
        elif mode == "expl": expl.append(l)
    if mode == "tests": cur_in, cur_out = flush()
    code = "\n".join(sol).strip("\n")
    code = re.sub(r"^```[a-zA-Z0-9+]*\n", "", code); code = re.sub(r"\n```\s*$", "", code)
    tests = [{"in": t["in"].strip("\n"), "out": t["out"].strip("\n")} for t in tests]
    return code, tests

def find_runners(text):
    lines = text.split("\n"); out=[]; i=0
    while i < len(lines):
        if lines[i].strip().startswith("```runner"):
            j=i+1
            while j<len(lines) and lines[j].strip()!="```": j+=1
            out.append(lines[i+1:j]); i=j+1
        else: i+=1
    return out

def norm(s): return re.sub(r"[ \t]+(?=\n)","", (s or "")).rstrip()

def main():
    args = sys.argv[1:] or ["all"]
    # 인자가 실제 md 파일 경로면 그 파일들만 검사한다.
    # (한 트레일을 여러 명이 나눠 작업할 때 남의 작업 중인 파일까지 잡히지 않게)
    paths = [a for a in args if a.lower().endswith(".md")]
    if paths:
        files = []
        for a in paths:
            p = a if os.path.isabs(a) else os.path.join(os.path.dirname(BASE), a)
            if not os.path.exists(p):
                p = os.path.join(BASE, a)
            if not os.path.exists(p):
                print(f"파일 없음: {a}"); return
            files.append(p)
    else:
        scope = args[0]
        if scope == "101":
            files = glob.glob(os.path.join(BASE, "ch*.md"))
        elif scope == "trails":
            files = glob.glob(os.path.join(BASE, "trails", "*", "ch*.md"))
        elif scope not in ("all",):
            files = glob.glob(os.path.join(BASE, "trails", scope, "ch*.md"))
        else:
            files = glob.glob(os.path.join(BASE, "ch*.md")) + glob.glob(os.path.join(BASE, "trails", "*", "ch*.md"))
    total=passed=failed=noblk=comped=0
    fails=[]
    tmp = tempfile.mkdtemp(prefix="cppv_")
    src = os.path.join(tmp,"s.cpp"); exe = os.path.join(tmp,"s.exe")
    for f in sorted(files):
        text = open(f, encoding="utf-8").read()
        for block in find_runners(text):
            total += 1
            code, tests = parse_runner(block)
            if not code or not tests: noblk += 1; continue
            open(src,"w",encoding="utf-8").write(code)
            cp = subprocess.run([GPP,"-O0","-std=c++17","-o",exe,src], capture_output=True, text=True, encoding="utf-8", errors="replace")
            if cp.returncode != 0:
                failed += 1; fails.append(f"COMPILE {os.path.relpath(f,BASE)} :: {(cp.stderr or '').strip().splitlines()[-1:] and cp.stderr.strip().splitlines()[-1][:80]}")
                continue
            ok=True; detail=""
            for k,t in enumerate(tests):
                try:
                    r = subprocess.run([exe], input=t["in"], capture_output=True, text=True, timeout=10, encoding="utf-8", errors="replace")
                except subprocess.TimeoutExpired:
                    ok=False; detail=f"TIMEOUT@{k+1}"; break
                if r.returncode != 0:
                    ok=False; detail=f"runtime@{k+1}"; break
                if norm(r.stdout) != norm(t["out"]):
                    ok=False; detail=f"mismatch@{k+1}: got {norm(r.stdout)[:40]!r} exp {norm(t['out'])[:40]!r}"; break
            if ok: passed += 1
            else: failed += 1; fails.append(f"FAIL {os.path.relpath(f,BASE)} :: {detail}")
    print(f"g++: {GPP}")
    print(f"runner blocks: {total} | passed: {passed} | FAILED: {failed} | empty: {noblk}")
    for x in fails[:80]: print(x)

main()
