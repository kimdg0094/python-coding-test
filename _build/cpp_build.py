# -*- coding: utf-8 -*-
import re, html, os, json
import markdown

SRC = r"C:\Users\pqow0\OneDrive\0_Projects\coding_test\codetree-101-analysis\cpp"
OUT = os.path.join(os.path.dirname(SRC), "cpp_learning.html")

CHAPTERS = [
    (1, "기본", "ch01-basics.md"),
    (2, "입출력", "ch02-io.md"),
    (3, "조건문 1", "ch03-conditionals-1.md"),
    (4, "단순 반복문 1", "ch04-loops-1.md"),
    (5, "조건문 2", "ch05-conditionals-2.md"),
    (6, "1차원 배열", "ch06-array-1d.md"),
    (7, "문자열", "ch07-string.md"),
    (8, "단순 반복문 2", "ch08-loops-2.md"),
    (9, "다중 반복문", "ch09-nested-loops.md"),
    (10, "2차원 배열", "ch10-array-2d.md"),
]

# 상위 트레일(직접 창작). 각 트레일 폴더의 ch{NN}[part].md 조각을 챕터별로 병합해 렌더링.
TRAILS = [
    {"alias": "novice-low", "name": "프로그래밍 기초", "folder": "trails/novice-low",
     "chapters": ["출력", "입출력", "연산자", "조건문", "단순 반복문", "다중 반복문", "1차원 배열", "2차원 배열", "문자열"]},
    {"alias": "novice-mid", "name": "프로그래밍 연습", "folder": "trails/novice-mid",
     "chapters": ["함수", "재귀함수", "정렬", "시뮬레이션 I", "시뮬레이션 II", "완전탐색 I", "완전탐색 II", "완전탐색 III", "케이스별로 나누기", "Ad-Hoc"]},
    {"alias": "novice-high", "name": "자료구조 알고리즘", "folder": "trails/novice-high",
     "chapters": ["시간, 공간복잡도", "배열, 연결 리스트", "정렬", "이진탐색", "스택, 큐, 덱", "트리", "해싱", "DP", "그래프 탐색", "그래프 알고리즘"]},
    {"alias": "intermediate-low", "name": "알고리즘 입문", "folder": "trails/intermediate-low",
     "chapters": ["Simulation", "Backtracking", "DFS", "BFS", "DP I", "DP II"]},
    {"alias": "intermediate-mid", "name": "알고리즘 기본", "folder": "trails/intermediate-mid",
     "chapters": ["중급 자료구조", "Shorten time Technique", "Parametric Search", "Greedy", "Shortest Path"]},
    {"alias": "intermediate-high", "name": "알고리즘 실전", "folder": "trails/intermediate-high",
     "chapters": ["Tree", "MST", "위상정렬", "String", "Advanced DP"]},
]

# ── 순차 학습 내비게이션 헬퍼 ──
def _trail_chnums(t):
    folder = os.path.join(SRC, t["folder"])
    if not os.path.isdir(folder):
        return []
    nums = set()
    for f in os.listdir(folder):
        m = re.match(r"ch(\d\d)[a-z]?\.md$", f)
        if m: nums.add(int(m.group(1)))
    return sorted(nums)

TRAIL_CHNUMS = {t["alias"]: _trail_chnums(t) for t in TRAILS}
_COURSE_ORDER = ["codetree-101"] + [t["alias"] for t in TRAILS if TRAIL_CHNUMS.get(t["alias"])]

def next_course_of(alias):
    i = _COURSE_ORDER.index(alias)
    if i + 1 < len(_COURSE_ORDER):
        na = _COURSE_ORDER[i + 1]
        return na, TRAIL_CHNUMS[na][0]
    return None, None

def jump_btn(label, course_pane, mode_target, chtab_target):
    return (f'<button class="goto-test jump-nav" data-course="{course_pane}" '
            f'data-mode="{mode_target}" data-chtab="{chtab_target}">{label}</button>')

LIST_ITEM = re.compile(r"^\s*([-*+]\s+|\d+[.)]\s+)")
BOLD_LABEL = re.compile(r"^\*\*[^*].*?\*\*")

def fix_lists(text):
    out, in_fence = [], False
    for line in text.split("\n"):
        s = line.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = not in_fence
            out.append(line); continue
        if not in_fence and out and out[-1].strip() != "":
            prev = out[-1]
            if LIST_ITEM.match(line):
                if not LIST_ITEM.match(prev):
                    out.append("")
            elif BOLD_LABEL.match(line):
                out.append("")
        out.append(line)
    return "\n".join(out)

def md2html(text):
    h = markdown.markdown(text or "", extensions=["tables", "fenced_code", "sane_lists"])
    h = re.sub(r"<li>\s*\[ \]\s*", '<li class="task"><input type="checkbox" disabled> ', h)
    h = re.sub(r"<li>\s*\[[xX]\]\s*", '<li class="task done"><input type="checkbox" checked disabled> ', h)
    return h

# ============ 코드 실행 채점 러너 ============
# 문제 본문 안의 ```runner ... ``` 블록을 파싱한다.
#   @@SOLUTION  (그 파트에서 배운 내용으로 쓴 정답 코드, 펜스 없이 raw)
#   @@TESTS     (--IN / --OUT 쌍 반복; IN 비면 입력 없음)
#   @@EXPL      (풀이 설명, 마크다운)
RUNNER_STATS = {"with": 0, "problems": 0}

def extract_runner(body_lines):
    start = end = None
    for i, l in enumerate(body_lines):
        s = l.strip()
        if start is None and s.startswith("```runner"):
            start = i
        elif start is not None and s == "```":
            end = i; break
    if start is None or end is None:
        return body_lines, None
    content = body_lines[start + 1:end]
    visible = body_lines[:start] + body_lines[end + 1:]
    sol, expl = [], []
    tests = []
    mode = None
    cur_in, cur_out, io_mode = [], [], None
    def flush():
        if cur_in or cur_out:
            tests.append({"in": "\n".join(cur_in), "out": "\n".join(cur_out)})
        return [], []
    for l in content:
        s = l.strip()
        if s == "@@SOLUTION": mode = "sol"; continue
        if s == "@@TESTS": mode = "tests"; io_mode = None; continue
        if s == "@@EXPL":
            cur_in, cur_out = flush(); mode = "expl"; continue
        if mode == "sol":
            sol.append(l)
        elif mode == "tests":
            if s == "--IN": cur_in, cur_out = flush(); io_mode = "in"; continue
            if s == "--OUT": io_mode = "out"; continue
            if io_mode == "in": cur_in.append(l)
            elif io_mode == "out": cur_out.append(l)
        elif mode == "expl":
            expl.append(l)
    if mode == "tests":
        cur_in, cur_out = flush()
    sol_code = "\n".join(sol).strip("\n")
    sol_code = re.sub(r"^```[a-zA-Z0-9]*\n", "", sol_code)
    sol_code = re.sub(r"\n```\s*$", "", sol_code)
    tests = [{"in": t["in"].strip("\n"), "out": t["out"].strip("\n")} for t in tests]
    return visible, {"solution": sol_code, "tests": tests, "expl": "\n".join(expl).strip()}

def runner_html(data):
    # option C: 코드 실행기 없이 "정답·풀이 보기"만
    RUNNER_STATS["with"] += 1
    sol = html.escape(data.get("solution", ""))
    expl = md2html(data.get("expl", ""))
    return (
        '<div class="runner">'
        '<div class="runctl"><button class="reveal-btn">💡 정답·풀이 보기</button></div>'
        '<div class="solution" hidden>'
        '<div class="sol-h">✅ 정답 코드 (C++)</div><pre class="sol-code"><code class="language-cpp">' + sol + '</code></pre>'
        '<div class="sol-h">📝 풀이</div><div class="sol-expl">' + expl + '</div>'
        '</div></div>'
    )

# ============ codetree-101 (Tutorial/Test) ============
def parse(text):
    title, meta = "", ""
    sections, cur = [], None
    for line in text.split("\n"):
        if title == "" and line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip(); continue
        if line.startswith("## "):
            if cur: sections.append(cur)
            cur = [line[3:].strip(), []]; continue
        if cur is None:
            if meta == "" and line.lstrip().startswith(">"):
                meta = line.lstrip().lstrip(">").strip()
        else:
            cur[1].append(line)
    if cur: sections.append(cur)
    return title, meta, sections

def sec_kind(h):
    if "개요" in h: return "overview"
    if "개념" in h: return "concepts"
    if "문제" in h: return "problems"
    if "체크리스트" in h: return "checklist"
    if "실수" in h: return "mistakes"
    return "other"

TITLE_RE = re.compile(r"^\s*(\d+\))\s*(.*?)\s*(?:\((.*)\))?\s*$")

def render_problem_cards(body_lines):
    lead, blocks, cur = [], [], None
    for line in body_lines:
        if line.startswith("### "):
            if cur is not None: blocks.append(cur)
            cur = {"title": line[4:].strip(), "lines": []}
        else:
            (cur["lines"] if cur is not None else lead).append(line)
    if cur is not None: blocks.append(cur)
    out = []
    lead_txt = "\n".join(lead).strip()
    if lead_txt: out.append('<p class="lead">' + md2html(lead_txt) + "</p>")
    for b in blocks:
        m = TITLE_RE.match(b["title"])
        if m:
            num, name, meta = html.escape(m.group(1)), html.escape(m.group(2)), m.group(3)
            head = f'<span class="pnum">{num}</span> <span class="pname">{name}</span>'
            if meta:
                badges = "".join(f'<span class="badge">{html.escape(x.strip())}</span>'
                                 for x in re.split(r"[·|]", meta) if x.strip())
                head += f'<span class="badges">{badges}</span>'
        else:
            head = f'<span class="pname">{html.escape(b["title"])}</span>'
        RUNNER_STATS["problems"] += 1
        visible, rdata = extract_runner(b["lines"])
        body_html = md2html("\n".join(visible).strip())
        runner = runner_html(rdata) if rdata else ""
        out.append(f'<div class="problem"><div class="phead">{head}</div>{body_html}{runner}</div>')
    return "\n".join(out), len(blocks)

def chip_line(meta):
    if not meta: return ""
    chips = "".join(f'<span class="chip">{html.escape(c.strip())}</span>'
                    for c in re.split(r"[·|]", meta) if c.strip())
    return f'<div class="chips">{chips}</div>'

data = []
for n, name, fname in CHAPTERS:
    with open(os.path.join(SRC, fname), encoding="utf-8") as f:
        text = fix_lists(f.read())
    title, meta, sections = parse(text)
    title = re.sub(r"\s*[—-]\s*Codetree.*$", "", title).strip()
    data.append({"n": n, "name": name, "title": title, "meta": meta, "sections": sections})

tut_tabs, tut_panes, test_tabs, test_panes = [], [], [], []
for i, d in enumerate(data):
    n = d["n"]; label = f"Ch{n}. {html.escape(d['name'])}"; active = " active" if i == 0 else ""
    prob_count = 0
    parts = [f'<div class="ch-head"><h1>{html.escape(d["title"])}</h1>{chip_line(d["meta"])}</div>']
    for heading, body in d["sections"]:
        kind = sec_kind(heading)
        if kind == "problems":
            _, prob_count = render_problem_cards(body); continue
        parts.append(f'<section class="sec sec-{kind}"><h2>{html.escape(heading)}</h2>{md2html(chr(10).join(body).strip())}</section>')
    parts.append(f'<div class="test-jump">🧩 이 챕터에는 문제 <b>{prob_count}개</b>가 있습니다. '
                 + jump_btn("Test에서 문제 풀기 →", "pane-codetree-101", "c101-test", f"test-ch{n}") + '</div>')
    tut_tabs.append(f'<button class="tab{active}" data-target="tut-ch{n}">{label}</button>')
    tut_panes.append(f'<div class="pane{active}" id="tut-ch{n}">' + "\n".join(parts) + "</div>")
    prob_html, cnt = "", 0
    for heading, body in d["sections"]:
        if sec_kind(heading) == "problems":
            prob_html, cnt = render_problem_cards(body); break
    test_head = (f'<div class="ch-head"><h1>Ch{n}. {html.escape(d["name"])} — 문제</h1>'
                 f'<div class="test-note">문제 <b>{cnt}개</b> · 요구사항·입출력·예제만 보고 <b>스스로 풀어</b> 본 뒤 '
                 f'각 문제의 <b>셀프체크 포인트</b>로 채점하세요.</div></div>')
    test_tabs.append(f'<button class="tab{active}" data-target="test-ch{n}">{label}</button>')
    if n < len(CHAPTERS):
        _nav = ('<div class="test-jump">✅ 문제를 다 풀었다면 '
                + jump_btn(f"다음: Ch{n+1}. {CHAPTERS[n][1]} Learn →", "pane-codetree-101", "c101-tut", f"tut-ch{n+1}") + '</div>')
    else:
        _na, _nf = next_course_of("codetree-101")
        _nav = ('<div class="test-jump">✅ Tutorial 완료! '
                + jump_btn(f"다음 레벨: {_na} →", f"pane-{_na}", f"{_na}-tut", f"{_na}-c-ch{_nf}") + '</div>') if _na else ''
    test_panes.append(f'<div class="pane{active}" id="test-ch{n}">{test_head}'
                      f'<section class="sec sec-problems">{prob_html}</section>{_nav}</div>')

# ============ 상위 트레일 (레슨: 개념+문제) ============
PROB_HEAD = re.compile(r"^\*\*(\d+\))\s*(.*?)\*\*\s*(?:·\s*(.+?))?\s*$")

def render_trail_problems(lines):
    blocks, cur = [], None
    for line in lines:
        m = PROB_HEAD.match(line.strip())
        if m:
            if cur: blocks.append(cur)
            cur = {"num": m.group(1), "name": m.group(2), "diff": (m.group(3) or "").strip(), "lines": []}
        elif cur is not None:
            cur["lines"].append(line)
    if cur: blocks.append(cur)
    out = []
    for b in blocks:
        badge = f'<span class="badge">{html.escape(b["diff"])}</span>' if b["diff"] else ""
        RUNNER_STATS["problems"] += 1
        visible, rdata = extract_runner(b["lines"])
        body = md2html("\n".join(visible).strip())
        runner = runner_html(rdata) if rdata else ""
        out.append(f'<div class="problem"><div class="phead"><span class="pnum">{html.escape(b["num"])}</span> '
                   f'<span class="pname">{html.escape(b["name"])}</span>{badge}</div>{body}{runner}</div>')
    return "\n".join(out), len(blocks)

def render_trail_lesson_split(title, body_lines):
    prob_idx = None
    for i, line in enumerate(body_lines):
        if line.strip() == "**문제**":
            prob_idx = i; break
    if prob_idx is None:
        concept_lines, problem_lines = body_lines, []
    else:
        concept_lines, problem_lines = body_lines[:prob_idx], body_lines[prob_idx + 1:]
    concept_lines = [l for l in concept_lines if l.strip() != "**개념**"]
    concept_html = md2html("\n".join(concept_lines).strip())
    problems_html, pc = render_trail_problems(problem_lines)
    c = (f'<div class="lesson"><h3 class="lesson-title">{html.escape(title)}</h3>'
         f'<div class="lconcept">{concept_html}</div></div>')
    p = ""
    if pc:
        p = f'<div class="lesson-p"><h3 class="lesson-title">{html.escape(title)}</h3>{problems_html}</div>'
    return c, p, pc

def render_trail_chapter(text):
    text = fix_lists(text)
    intro, lessons, cur = "", [], None
    for line in text.split("\n"):
        if line.startswith("## "):
            if cur: lessons.append(cur)
            cur = [line[3:].strip(), []]; continue
        if cur is None:
            if line.strip().startswith(">"):
                t = re.sub(r"^개요\s*:\s*", "", line.strip().lstrip(">").strip())
                intro = (intro + " " + t).strip()
        else:
            cur[1].append(line)
    if cur: lessons.append(cur)
    c_parts, p_parts, total_p = [], [], 0
    intro_html = f'<div class="tr-intro">{html.escape(intro)}</div>' if intro else ""
    for title, blines in lessons:
        c, p, pc = render_trail_lesson_split(title, blines)
        c_parts.append(c)
        if p: p_parts.append(p)
        total_p += pc
    concept_body = intro_html + "\n".join(c_parts)
    problem_body = ('<div class="test-note">각 레슨의 문제를 요구사항·입출력·예제만 보고 스스로 푼 뒤 셀프체크로 채점하세요.</div>'
                    + "\n".join(p_parts)) if p_parts else "<p>문제 없음</p>"
    return concept_body, problem_body, len(lessons), total_p

trail_top_tabs, trail_panes = [], []
trail_stat = []
for trail in TRAILS:
    folder = os.path.join(SRC, trail["folder"])
    files = [f for f in os.listdir(folder) if re.match(r"ch\d\d[a-z]?\.md$", f)]
    if not files:
        continue
    groups = {}
    for f in files:
        m = re.match(r"ch(\d\d)([a-z]?)\.md$", f)
        groups.setdefault(int(m.group(1)), []).append((m.group(2), f))
    alias = trail["alias"]
    c_tabs, c_panes, p_tabs, p_panes = [], [], [], []
    t_lessons = t_probs = 0
    chlist = sorted(groups)
    for idx, cnum in enumerate(chlist):
        frags = sorted(groups[cnum], key=lambda x: x[0])
        text = "\n\n".join(open(os.path.join(folder, ff), encoding="utf-8").read() for _, ff in frags)
        cname = trail["chapters"][cnum - 1] if cnum - 1 < len(trail["chapters"]) else f"Ch{cnum}"
        cbody, pbody, nlessons, nprob = render_trail_chapter(text)
        t_lessons += nlessons; t_probs += nprob
        active = " active" if idx == 0 else ""
        cid, pid = f"{alias}-c-ch{cnum}", f"{alias}-p-ch{cnum}"
        chlabel = f"Ch{cnum}. {html.escape(cname)}"
        chead = (f'<div class="ch-head"><h1>Ch{cnum}. {html.escape(cname)}</h1>'
                 f'<div class="chips"><span class="chip">레슨 {nlessons}</span><span class="chip">문제 {nprob}</span></div></div>')
        c_tabs.append(f'<button class="tab{active}" data-target="{cid}">{chlabel}</button>')
        _ljump = (f'<div class="test-jump">🧩 이 챕터에는 문제 <b>{nprob}개</b>가 있습니다. '
                  + jump_btn("Test에서 문제 풀기 →", f"pane-{alias}", f"{alias}-test", f"{alias}-p-ch{cnum}") + '</div>')
        c_panes.append(f'<div class="pane{active}" id="{cid}">{chead}{cbody}{_ljump}</div>')
        p_tabs.append(f'<button class="tab{active}" data-target="{pid}">{chlabel}</button>')
        _pos = chlist.index(cnum)
        if _pos + 1 < len(chlist):
            _nn = chlist[_pos + 1]
            _nname = trail["chapters"][_nn - 1] if _nn - 1 < len(trail["chapters"]) else f"Ch{_nn}"
            _nav = ('<div class="test-jump">✅ 문제를 다 풀었다면 '
                    + jump_btn(f"다음: Ch{_nn}. {_nname} Learn →", f"pane-{alias}", f"{alias}-tut", f"{alias}-c-ch{_nn}") + '</div>')
        else:
            _na, _nf = next_course_of(alias)
            if _na:
                _nav = ('<div class="test-jump">✅ 이 레벨 완료! '
                        + jump_btn(f"다음 레벨: {_na} →", f"pane-{_na}", f"{_na}-tut", f"{_na}-c-ch{_nf}") + '</div>')
            else:
                _nav = '<div class="test-jump">🎉 모든 레벨을 완주했습니다! 수고하셨습니다.</div>'
        p_panes.append(f'<div class="pane{active}" id="{pid}">{chead}{pbody}{_nav}</div>')
    tut_id, test_id = f"{alias}-tut", f"{alias}-test"
    banner = (f'<div class="trail-banner"><b>{html.escape(alias)}</b> · {html.escape(trail["name"])} '
              f'&nbsp;—&nbsp; 레슨 {t_lessons} · 문제 {t_probs}. '
              f'<b>📖 Learn</b>에서 개념을 익히고 <b>🧩 Test</b>에서 문제를 스스로 푸세요.</div>')
    mode = ('<div class="tab-scope">'
            f'<div class="modebar tabbar"><button class="tab active" data-target="{tut_id}">📖 Learn</button>'
            f'<button class="tab" data-target="{test_id}">🧩 Test</button></div>'
            f'<div class="pane active" id="{tut_id}"><div class="tab-scope"><div class="chapters tabbar">'
            + "\n".join(c_tabs) + '</div>\n' + "\n".join(c_panes) + '</div></div>'
            f'<div class="pane" id="{test_id}"><div class="tab-scope"><div class="chapters tabbar">'
            + "\n".join(p_tabs) + '</div>\n' + "\n".join(p_panes) + '</div></div>'
            '</div>')
    pane_id = f"pane-{alias}"
    trail_top_tabs.append(f'<button class="tab" data-target="{pane_id}">{html.escape(alias)}</button>')
    trail_panes.append(f'<div class="pane" id="{pane_id}"><div class="wrap">{banner}{mode}</div></div>')
    trail_stat.append(f"{alias}({t_lessons}L/{t_probs}P)")

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from theme import make_css, JS_UI
CSS = make_css("cpp")

JS = """
document.querySelectorAll('.tabbar').forEach(function(bar){
  bar.addEventListener('click', function(e){
    var btn = e.target.closest('.tab'); if(!btn || !bar.contains(btn)) return;
    var scope = bar.closest('.tab-scope');
    bar.querySelectorAll(':scope > .tab').forEach(function(t){t.classList.remove('active');});
    btn.classList.add('active');
    scope.querySelectorAll(':scope > .pane').forEach(function(p){p.classList.remove('active');});
    var tgt = document.getElementById(btn.dataset.target);
    if(tgt) tgt.classList.add('active');
    window.scrollTo({top:0,behavior:'smooth'});
  });
});
document.addEventListener('click', function(e){
  var b = e.target.closest('.jump-nav'); if(!b) return;
  var ct = document.querySelector('.topbar .tab[data-target="'+b.dataset.course+'"]');
  if(ct && !ct.classList.contains('active')) ct.click();
  var mt = document.querySelector('#'+b.dataset.course+' .modebar .tab[data-target="'+b.dataset.mode+'"]');
  if(mt && !mt.classList.contains('active')) mt.click();
  var cht = document.querySelector('.chapters .tab[data-target="'+b.dataset.chtab+'"]');
  if(cht) cht.click();
});

/* ===== Python code runner (Pyodide) ===== */
var __pyReady = null;
function ensurePy(){
  if(!__pyReady){
    __pyReady = new Promise(function(resolve, reject){
      var s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js';
      s.onload = function(){ loadPyodide({indexURL:'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/'}).then(resolve, reject); };
      s.onerror = function(){ reject(new Error('Pyodide 로드 실패 — 코드 실행에는 인터넷 연결이 필요합니다.')); };
      document.head.appendChild(s);
    });
  }
  return __pyReady;
}
function normOut(s){ return (s==null?'':String(s)).replace(/[ \t]+(?=\\n)/g,'').replace(/\\s+$/,''); }
async function runOne(py, code, stdin){
  py.globals.set('__inp', stdin==null?'':stdin);
  py.globals.set('__code', code);
  await py.runPythonAsync(
    'import sys, io, traceback\\n' +
    '_bi,_bo = sys.stdin, sys.stdout\\n' +
    'class _SI(io.StringIO):\\n' +
    '    pass\\n' +
    '_si = _SI(__inp)\\n' +
    '_si.buffer = io.BytesIO(__inp.encode("utf-8"))\\n' +
    'sys.stdin = _si\\n' +
    'sys.stdout = io.StringIO()\\n' +
    '_err = ""\\n' +
    'try:\\n' +
    '    exec(compile(__code, "<user>", "exec"), {"__name__":"__main__"})\\n' +
    'except SystemExit:\\n' +
    '    pass\\n' +
    'except Exception:\\n' +
    '    _err = traceback.format_exc()\\n' +
    '_res = sys.stdout.getvalue()\\n' +
    'sys.stdin, sys.stdout = _bi, _bo\\n'
  );
  return { out: py.globals.get('_res'), err: py.globals.get('_err') };
}
async function judge(runner){
  var resultEl = runner.querySelector('.run-result');
  var code = runner.querySelector('.code').value;
  var tests = [];
  try{ tests = JSON.parse(runner.dataset.tests||'[]'); }catch(e){ tests=[]; }
  if(!code.trim()){ resultEl.className='run-result fail'; resultEl.textContent='코드를 입력하세요.'; return; }
  resultEl.className='run-result'; resultEl.textContent='실행 준비 중… (첫 실행은 파이썬 로딩에 몇 초 걸릴 수 있어요)';
  var py;
  try{ py = await ensurePy(); }catch(e){ resultEl.className='run-result fail'; resultEl.textContent='⚠️ '+e.message; return; }
  if(tests.length===0){
    var r0 = await runOne(py, code, '');
    resultEl.className='run-result'; resultEl.textContent = r0.err ? ('⚠️ 실행 오류:\\n'+r0.err) : ('실행 출력:\\n'+r0.out);
    return;
  }
  for(var i=0;i<tests.length;i++){
    var r = await runOne(py, code, tests[i]['in']);
    if(r.err){ resultEl.className='run-result fail'; resultEl.textContent='⚠️ 실행 오류 (예제 '+(i+1)+'):\\n'+r.err; return; }
    if(normOut(r.out) !== normOut(tests[i]['out'])){
      resultEl.className='run-result fail';
      resultEl.textContent='❌ 오답 — 예제 '+(i+1)+'에서 기대와 다른 출력입니다.\\n\\n[입력]\\n'+(tests[i]['in']||'(없음)')+'\\n\\n[내 코드 출력]\\n'+r.out;
      return;
    }
  }
  resultEl.className='run-result pass'; resultEl.textContent='✅ 정답! 예제 '+tests.length+'개를 모두 통과했습니다.';
}
document.addEventListener('click', function(e){
  var rv = e.target.closest('.reveal-btn');
  if(rv){ var sol = rv.closest('.runner').querySelector('.solution'); sol.hidden = !sol.hidden; rv.textContent = sol.hidden ? '💡 정답·풀이 보기' : '🙈 정답·풀이 숨기기'; }
});
"""
JS = JS + JS_UI

stat_chips = "<span>💠 C++</span><span>Tutorial (34L·69P)</span>" + \
             "".join(f"<span>{html.escape(s)}</span>" for s in trail_stat)

top_tabs_html = ("<button class='tab active' data-target='pane-codetree-101'>Tutorial</button>"
                 + "".join(trail_top_tabs))

c101_banner = ("<div class='trail-banner'><b>codetree-101</b> · 프로그래밍 시작 (C++) &nbsp;—&nbsp; "
               "10챕터 34레슨 · 개념 34 · 문제 69. <b>📖 Learn</b>에서 개념을 익히고 <b>🧩 Test</b>에서 문제를 스스로 푼 뒤 정답·풀이를 확인하세요.</div>")
c101_mode = ("<div class='tab-scope'>"
    "<div class='modebar tabbar'><button class='tab active' data-target='c101-tut'>📖 Learn</button>"
    "<button class='tab' data-target='c101-test'>🧩 Test</button></div>"
    "<div class='pane active' id='c101-tut'><div class='tab-scope'><div class='chapters tabbar'>"
    + "\n".join(tut_tabs) + "</div>\n" + "\n".join(tut_panes) + "</div></div>"
    "<div class='pane' id='c101-test'><div class='tab-scope'><div class='chapters tabbar'>"
    + "\n".join(test_tabs) + "</div>\n" + "\n".join(test_panes) + "</div></div>"
    "</div>")
c101_pane = "<div class='pane active' id='pane-codetree-101'><div class='wrap'>" + c101_banner + c101_mode + "</div></div>"

HTML = (
"<!doctype html>\n<html lang='ko'>\n<head>\n<meta charset='utf-8'>\n"
"<meta name='viewport' content='width=device-width, initial-scale=1'>\n"
"<title>C++ 학습 가이드</title>\n<style>" + CSS + "</style>\n</head>\n<body>\n"
"<div class='masthead'><div class='inner'>"
"<h1>💠 C++ 학습 가이드</h1>"
"<p>입문 코스 <b>Tutorial</b>부터 상위 트레일까지 C++로 순서대로 학습하세요. 각 문제는 스스로 풀어 본 뒤 <b>정답 코드·풀이</b>를 확인할 수 있습니다.</p>"
"<div class='stat'>" + stat_chips + "</div>"
"</div></div>\n"
"<div class='tab-scope'>\n"
"<div class='topbar'><div class='inner tabbar'>" + top_tabs_html + "</div></div>\n"
+ c101_pane + "\n"
+ "\n".join(trail_panes) +
"\n</div>\n"
"<footer><b>Tutorial</b> 코스는 © Branch &amp; Bound(Codetree) 원문을 개인 학습용으로 요약·분석한 자료입니다. "
"상위 트레일 탭(novice-low 등)은 공개된 레슨 제목·구조만 참고해 새로 창작한 원본 학습자료입니다.</footer>\n"
"<script>" + JS + "</script>\n</body>\n</html>"
)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)

print("WROTE", OUT)
print("size KB", round(len(HTML.encode("utf-8")) / 1024, 1))
print("trails:", ", ".join(trail_stat))
