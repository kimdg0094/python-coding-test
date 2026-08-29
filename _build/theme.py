# -*- coding: utf-8 -*-
"""공통 디자인 시스템 — python_learning.html / cpp_learning.html 동일 구조.
make_css(lang): lang in {"python","cpp"} — 액센트 색만 다르고 나머지 동일.
JS_UI: 읽기 진행바 + 레슨 TOC + 코드 하이라이팅 (기능 JS와 독립).
"""

ACCENTS = {
    "python": {
        "accent": "#0d8577", "deep": "#085e54", "soft": "#e2f4f0", "softb": "#c6e8e1",
        "dsoft": "#0e2f2a", "dsoftb": "#1b4a42", "glow": "13,133,119",
    },
    "cpp": {
        "accent": "#0f6bb8", "deep": "#0a4d88", "soft": "#e3eef9", "softb": "#c8dff2",
        "dsoft": "#0d2438", "dsoftb": "#1a4062", "glow": "15,107,184",
    },
}


def make_css(lang):
    a = ACCENTS[lang]
    return """
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,600;1,500&display=swap');

:root{
  --accent:""" + a["accent"] + """; --accent-d:""" + a["deep"] + """; --accent-l:""" + a["soft"] + """;
  --accent-lb:""" + a["softb"] + """; --glow:""" + a["glow"] + """;
  --ink:#1c232b; --muted:#65707c; --line:#e6e3db; --bg:#f7f5f0; --card:#ffffff;
  --code-bg:#0d1420; --code-ink:#dbe4f0; --warn-bg:#fdf3e4; --warn-line:#eab566;
  --shadow:0 1px 2px rgba(28,35,43,.05),0 6px 24px -12px rgba(28,35,43,.14);
  --shadow-lift:0 2px 4px rgba(28,35,43,.06),0 14px 34px -14px rgba(var(--glow),.28);
  --sans:'Pretendard Variable',Pretendard,'Malgun Gothic',system-ui,sans-serif;
  --mono:'JetBrains Mono','D2Coding',Consolas,monospace;
}
@media (prefers-color-scheme: dark){
  :root{
    --accent-l:""" + a["dsoft"] + """; --accent-lb:""" + a["dsoftb"] + """;
    --ink:#e4e9ef; --muted:#94a0ac; --line:#2a313b; --bg:#10141a; --card:#181e26;
    --warn-bg:#2b2113; --warn-line:#8a6a2f;
    --shadow:0 1px 2px rgba(0,0,0,.35),0 8px 26px -12px rgba(0,0,0,.5);
    --shadow-lift:0 2px 4px rgba(0,0,0,.4),0 14px 34px -12px rgba(var(--glow),.25);
  }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
html,body{margin:0;padding:0}
body{font-family:var(--sans);color:var(--ink);background:var(--bg);line-height:1.75;font-size:15.5px;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:var(--accent-d)}
::selection{background:var(--accent-l);color:var(--accent-d)}
h3{scroll-margin-top:calc(var(--stick2,100px) + 62px)}
::-webkit-scrollbar{width:11px;height:11px}
::-webkit-scrollbar-thumb{background:var(--line);border-radius:8px;border:3px solid var(--bg)}
::-webkit-scrollbar-track{background:transparent}

#readbar{position:fixed;top:0;left:0;height:3px;width:0;z-index:99;
  background:linear-gradient(90deg,var(--accent),var(--accent-d));transition:width .1s linear}

.wrap{max-width:980px;margin:0 auto;padding:0 20px 90px}

/* ── 마스트헤드 ─────────────────────────── */
.masthead{position:relative;overflow:hidden;color:#f2f6f4;
  background:
    radial-gradient(1px 1px at 22px 24px, rgba(255,255,255,.16) 1px, transparent 0),
    linear-gradient(128deg,var(--accent-d) 0%,#131a22 130%);
  background-size:44px 44px,cover;
  padding:38px 0 30px;border-bottom:1px solid rgba(255,255,255,.07)}
.masthead::after{content:'';position:absolute;right:-140px;top:-140px;width:420px;height:420px;border-radius:50%;
  background:radial-gradient(circle,rgba(var(--glow),.45),transparent 65%);filter:blur(6px);pointer-events:none}
.masthead .inner{max-width:980px;margin:0 auto;padding:0 20px;position:relative}
.masthead h1{margin:0 0 8px;font-size:clamp(26px,4vw,36px);font-weight:800;letter-spacing:-.045em;line-height:1.2}
.masthead p{margin:0;opacity:.86;font-size:14.5px;max-width:640px}
.masthead p b{color:#fff}
.masthead .stat{display:inline-flex;gap:8px;margin-top:16px;flex-wrap:wrap}
.masthead .stat span{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);
  backdrop-filter:blur(4px);padding:4px 12px;border-radius:20px;font-size:12.5px;font-weight:600;letter-spacing:-.01em}

/* ── 상단 코스 탭 ─────────────────────────── */
.topbar{position:sticky;top:0;z-index:30;background:color-mix(in srgb,var(--card) 88%,transparent);
  backdrop-filter:blur(12px);border-bottom:1px solid var(--line);overflow-x:auto;scrollbar-width:none}
.topbar::-webkit-scrollbar{display:none}
.topbar .inner{max-width:980px;margin:0 auto;padding:9px 20px;display:flex;gap:6px;min-width:max-content}
.topbar .tab{font-family:var(--sans);font-size:14px;font-weight:700;letter-spacing:-.02em;
  padding:8px 15px;border:1px solid transparent;border-radius:20px;background:none;cursor:pointer;
  color:var(--muted);white-space:nowrap;transition:all .15s}
.topbar .tab.active{background:var(--accent);border-color:var(--accent);color:#fff;
  box-shadow:0 3px 10px -3px rgba(var(--glow),.5)}
.topbar .tab:hover:not(.active){color:var(--accent-d);border-color:var(--accent-lb);background:var(--accent-l)}

/* ── Learn/Test 모드 토글 ─────────────────── */
.modebar{position:sticky;top:var(--stick1,50px);z-index:26;display:flex;gap:7px;
  margin:0 0 2px;padding:12px 0 10px;background:color-mix(in srgb,var(--bg) 92%,transparent);
  backdrop-filter:blur(10px)}
.modebar .tab{font-family:var(--sans);font-size:13.5px;font-weight:700;padding:7px 20px;
  border:1px solid var(--line);border-radius:20px;background:var(--card);cursor:pointer;
  color:var(--muted);transition:all .16s}
.modebar .tab.active{background:var(--accent);border-color:var(--accent);color:#fff;
  box-shadow:0 3px 10px -3px rgba(var(--glow),.5)}
.modebar .tab:hover:not(.active){border-color:var(--accent);color:var(--accent-d)}

/* ── 챕터 필 탭 ──────────────────────────── */
.chapters{position:sticky;top:var(--stick2,100px);z-index:25;background:color-mix(in srgb,var(--bg) 92%,transparent);
  backdrop-filter:blur(10px);padding:13px 0 11px;display:flex;gap:7px;flex-wrap:wrap;
  border-bottom:1px solid var(--line);margin-bottom:22px}
.chapters .tab{font-family:var(--sans);font-size:12.8px;font-weight:600;letter-spacing:-.01em;
  padding:6px 13px;border:1px solid var(--line);background:var(--card);border-radius:20px;
  cursor:pointer;color:var(--muted);white-space:nowrap;transition:all .16s}
.chapters .tab.active{background:var(--accent);border-color:var(--accent);color:#fff;
  box-shadow:0 3px 10px -3px rgba(var(--glow),.5)}
.chapters .tab:hover:not(.active){border-color:var(--accent);color:var(--accent-d);transform:translateY(-1px)}

/* ── 페인 전환 ──────────────────────────── */
.pane{display:none}
.pane.active{display:block}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.pane.active>*:nth-child(-n+8){animation:rise .4s cubic-bezier(.2,.7,.3,1) backwards}
.pane.active>*:nth-child(1){animation-delay:.03s}
.pane.active>*:nth-child(2){animation-delay:.07s}
.pane.active>*:nth-child(3){animation-delay:.11s}
.pane.active>*:nth-child(4){animation-delay:.15s}
.pane.active>*:nth-child(5){animation-delay:.19s}

/* ── 챕터 헤더·칩 ────────────────────────── */
.ch-head{margin:6px 0 20px;padding-bottom:14px;border-bottom:2px solid var(--line)}
.ch-head h1{font-size:24px;font-weight:800;letter-spacing:-.035em;margin:0 0 9px}
.chips{display:flex;gap:7px;flex-wrap:wrap}
.chip{background:var(--accent-l);color:var(--accent-d);border:1px solid var(--accent-lb);
  font-size:12px;padding:3px 11px;border-radius:14px;font-weight:700;letter-spacing:-.01em}
.test-note{color:var(--muted);font-size:13.5px;margin-top:6px}
.trail-banner{background:var(--accent-l);border:1px solid var(--accent-lb);color:var(--accent-d);
  border-radius:14px;padding:13px 18px;margin:20px 0 2px;font-size:14px;line-height:1.65}
.tr-intro{background:var(--accent-l);border:1px solid var(--accent-lb);border-radius:14px;
  padding:13px 18px;margin-bottom:20px;color:var(--accent-d);font-size:14.3px}

/* ── 섹션 카드 (101 Learn) ────────────────── */
.sec{background:var(--card);border:1px solid var(--line);border-radius:16px;
  padding:8px 26px 20px;margin-bottom:22px;box-shadow:var(--shadow)}
.sec h2{font-size:18.5px;font-weight:800;letter-spacing:-.03em;margin:18px 0 8px;
  padding-bottom:10px;border-bottom:1px dashed var(--line)}
.sec h3{font-size:15.8px;font-weight:700;margin:22px 0 7px;color:var(--accent-d);letter-spacing:-.02em}
.sec-mistakes{background:var(--warn-bg);border-color:var(--warn-line)}
.sec-checklist ul{list-style:none;padding-left:2px}
.sec-checklist li.task{margin:6px 0}
.sec-checklist input{margin-right:9px;transform:translateY(1px);accent-color:var(--accent)}
.sec p{margin:9px 0}
.sec ul,.sec ol{margin:9px 0;padding-left:23px}
.sec li{margin:4px 0}
.sec strong{color:var(--ink)}
.sec-problems{background:none;border:none;padding:0;box-shadow:none}

/* ── 레슨 카드 (트레일) ───────────────────── */
.lesson{background:var(--card);border:1px solid var(--line);border-radius:16px;
  padding:10px 26px 20px;margin-bottom:26px;box-shadow:var(--shadow)}
.lesson-title{font-size:19.5px;font-weight:800;letter-spacing:-.03em;margin:14px 0 10px;
  padding-bottom:10px;border-bottom:2px solid var(--accent-l)}
.lsub{font-weight:800;color:var(--accent-d);margin:18px 0 7px;font-size:14.5px;letter-spacing:-.01em}
.lsub .pc{background:var(--accent);color:#fff;border-radius:10px;padding:1px 9px;font-size:11.5px;margin-left:3px}
.lconcept ul,.lconcept ol{margin:9px 0;padding-left:23px}
.lconcept li{margin:5px 0}
.lconcept p{margin:9px 0}
.lesson-p{margin-bottom:26px}
.lesson-p .lesson-title{margin-bottom:10px}

/* ── 표 ─────────────────────────────────── */
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14px}
th,td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
th{background:var(--accent-l);color:var(--accent-d);font-weight:700}
tr:nth-child(even) td{background:color-mix(in srgb,var(--accent-l) 22%,var(--card))}

/* ── 코드 ────────────────────────────────── */
code,pre,pre code,.runner .code,.sol-code,.run-result{
  font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0}
code{background:color-mix(in srgb,var(--accent-l) 55%,var(--card));color:var(--accent-d);
  padding:1.5px 6px;border-radius:6px;font-size:13px;font-family:var(--mono);font-weight:500}
pre{background:var(--code-bg);color:var(--code-ink);padding:15px 18px;border-radius:12px;
  overflow:auto;margin:13px 0;border:1px solid rgba(255,255,255,.06);box-shadow:var(--shadow)}
pre code{background:none;color:inherit;padding:0;font-size:13px;line-height:1.68;font-weight:400}
pre code.hljs{background:transparent;padding:0}

/* ── 문제 카드 ───────────────────────────── */
.problem{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);
  border-radius:14px;padding:14px 20px 16px;margin:16px 0;box-shadow:var(--shadow);
  transition:box-shadow .2s,transform .2s}
.problem:hover{box-shadow:var(--shadow-lift);transform:translateY(-1px)}
.phead{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px}
.pnum{background:var(--accent-l);color:var(--accent-d);border-radius:9px;padding:2px 9px;
  font-weight:800;font-size:13.5px;font-family:var(--mono)}
.pname{font-weight:800;font-size:16.5px;letter-spacing:-.025em}
.badges{display:flex;gap:6px;flex-wrap:wrap;margin-left:auto}
.badge{background:var(--accent-l);color:var(--accent-d);border:1px solid var(--accent-lb);
  font-size:11.5px;padding:2px 10px;border-radius:12px;font-weight:700;margin-left:auto}
.phead .badge{margin-left:auto}
.problem ul{list-style:none;padding-left:0}
.problem li{margin:6px 0;padding-left:2px}
.problem .lead{color:var(--muted)}

/* ── 코드 러너 ───────────────────────────── */
.runner{margin:14px 0 2px;border-top:1px dashed var(--line);padding-top:14px}
.runner .code{width:100%;min-height:135px;font-family:var(--mono);font-size:13px;
  border:1px solid #2b3648;border-radius:12px;padding:12px 14px;resize:vertical;
  background:var(--code-bg);color:var(--code-ink);line-height:1.6;tab-size:4;transition:border .15s,box-shadow .15s}
.runner .code:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(var(--glow),.22)}
.runctl{display:flex;gap:9px;margin-top:10px;flex-wrap:wrap}
.run-btn{background:var(--accent);color:#fff;border:none;padding:9px 18px;border-radius:10px;
  cursor:pointer;font-weight:700;font-size:13.5px;font-family:var(--sans);
  box-shadow:0 4px 12px -4px rgba(var(--glow),.55);transition:all .16s}
.run-btn:hover{background:var(--accent-d);transform:translateY(-1px)}
.reveal-btn{background:var(--card);color:var(--accent-d);border:1.5px solid var(--accent-lb);
  padding:9px 18px;border-radius:10px;cursor:pointer;font-weight:700;font-size:13.5px;
  font-family:var(--sans);transition:all .16s}
.reveal-btn:hover{background:var(--accent-l);border-color:var(--accent)}
.run-result{margin-top:10px;font-size:13px;white-space:pre-wrap;font-family:var(--mono);line-height:1.55}
.run-result.pass{color:var(--accent-d);font-weight:700}
.run-result.fail{color:#d64545;font-weight:700}
.solution{margin-top:12px;border:1px solid var(--accent-lb);border-radius:14px;
  padding:8px 18px 16px;background:color-mix(in srgb,var(--accent-l) 45%,var(--card))}
.sol-h{font-weight:800;color:var(--accent-d);margin:13px 0 7px;font-size:14.5px}
.sol-code{margin:0}
.sol-expl{font-size:14.2px}
.sol-expl ul,.sol-expl ol{margin:9px 0;padding-left:23px}
.sol-expl ul{list-style:disc}
.sol-expl ol{list-style:decimal}
.sol-expl li{margin:5px 0;padding-left:0}
.sol-expl p{margin:9px 0}

/* ── 기타 ────────────────────────────────── */
.test-jump{margin:16px 0 8px;padding:15px 19px;background:var(--accent-l);
  border:1px solid var(--accent-lb);border-radius:14px;font-size:14px}
.goto-test{background:var(--accent);color:#fff;border:none;padding:8px 15px;border-radius:9px;
  cursor:pointer;font-size:13.5px;font-weight:700;font-family:var(--sans);margin-left:7px;transition:all .15s}
.goto-test:hover{background:var(--accent-d)}
.bulk-done{background:var(--card);color:var(--accent-d);border:1.5px solid var(--accent-lb);
  padding:7px 14px;border-radius:9px;cursor:pointer;font-size:13.5px;font-weight:700;
  font-family:var(--sans);margin-left:7px;transition:all .15s}
.bulk-done:hover{background:var(--accent-l);border-color:var(--accent)}
footer{color:var(--muted);font-size:12.5px;text-align:center;margin:34px auto 0;padding:20px 20px 26px;
  border-top:1px solid var(--line);max-width:980px;line-height:1.7}


/* ── 레슨 완료 토글 ───────────────────────── */
.done-toggle{float:right;margin:2px 0 0 12px;font-family:var(--sans);font-size:11px;font-weight:700;
  color:var(--muted);background:none;border:1.5px solid var(--line);border-radius:12px;
  padding:4px 11px;cursor:pointer;transition:all .15s;letter-spacing:-.01em}
.done-toggle:hover{border-color:var(--accent);color:var(--accent-d)}
.done-toggle.on{background:var(--accent);border-color:var(--accent);color:#fff}
h3.done-h{color:var(--muted)}

/* ── 이어서 학습 ─────────────────────────── */
#resumepill{position:fixed;right:18px;bottom:18px;z-index:60;background:var(--accent);color:#fff;
  border:none;border-radius:24px;padding:12px 19px;font-family:var(--sans);font-size:13.5px;
  font-weight:800;cursor:pointer;box-shadow:0 10px 26px -6px rgba(var(--glow),.6);
  animation:rise .45s cubic-bezier(.2,.7,.3,1)}
#resumepill:hover{background:var(--accent-d)}

/* ── 진행 뱃지 ───────────────────────────── */
.tab .prog{display:inline-block;margin-left:7px;font-size:10.5px;font-weight:800;line-height:1;
  background:var(--accent-l);color:var(--accent-d);border:1px solid var(--accent-lb);
  border-radius:9px;padding:2.5px 7px;vertical-align:1px}
.tab .prog.full{background:var(--accent);border-color:var(--accent);color:#fff}
.chapters .tab.active .prog,.topbar .tab.active .prog{background:rgba(255,255,255,.22);border-color:transparent;color:#fff}

/* ── 마감 디테일 ─────────────────────────── */
button:focus-visible,a:focus-visible,.tab:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:8px}
pre{position:relative}
.copybtn{position:absolute;top:8px;right:8px;font-family:var(--sans);font-size:11px;font-weight:700;
  background:rgba(255,255,255,.1);color:#c6d2df;border:1px solid rgba(255,255,255,.18);
  border-radius:7px;padding:4px 10px;cursor:pointer;opacity:0;transition:all .15s}
pre:hover .copybtn{opacity:1}
.copybtn.ok{background:var(--accent);border-color:var(--accent);color:#fff;opacity:1}
#totop{position:fixed;right:18px;bottom:18px;z-index:55;width:44px;height:44px;border-radius:50%;
  border:1px solid var(--line);background:var(--card);color:var(--accent-d);font-size:17px;
  font-weight:800;cursor:pointer;box-shadow:var(--shadow-lift);display:none}
#totop.show{display:block}
#totop:hover{background:var(--accent-l)}
"""


JS_UI = """
/* ===== 공통 UI: 진행바 · TOC · 완료체크 · 이어서학습 · 하이라이팅 ===== */
(function(){
  var SITE=(location.pathname.split('/').pop()||'learn').replace(/[^A-Za-z0-9_-]/g,'_');

  /* 읽기 진행바 */
  var pb=document.createElement('div');pb.id='readbar';document.body.appendChild(pb);
  addEventListener('scroll',function(){var h=document.documentElement;
    var m=h.scrollHeight-h.clientHeight;pb.style.width=(m>0?(h.scrollTop/m*100):0)+'%';},{passive:true});

  /* sticky 3층(코스탭·모드바·챕터탭) 높이 실측 정렬 */
  function stick(){
    var tb=document.querySelector('.topbar');
    var mb=document.querySelector('.modebar');
    var h1=tb?tb.offsetHeight:50, h2=(mb&&mb.offsetHeight)||48;
    var r=document.documentElement.style;
    r.setProperty('--stick1',h1+'px');
    r.setProperty('--stick2',(h1+h2)+'px');
  }
  stick();addEventListener('resize',stick);
  setTimeout(stick,400);setTimeout(stick,1600);
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){setTimeout(stick,50);});

  /* 레슨 완료 저장소 */
  var DKEY=SITE+':done', done={};
  try{done=JSON.parse(localStorage.getItem(DKEY)||'{}')||{};}catch(e){done={};}
  function dsave(){try{localStorage.setItem(DKEY,JSON.stringify(done));}catch(e){}}
  function keyOf(h){var p=h.closest('.pane');
    return (p?p.id:'x')+'::'+((h.dataset.t||h.textContent).trim().slice(0,60));}

  /* 레슨 TOC 제거됨 — buildToc는 다른 호출부 호환용 no-op */
  function buildToc(){}

  /* 레슨 완료 토글 + 진행률 집계 */
  var HEADS=[];
  Array.prototype.slice.call(document.querySelectorAll('.lesson > .lesson-title, .sec h3')).forEach(function(h){
    h.dataset.t=h.textContent.trim();
    var chp=h.closest('.pane'), cop=h.closest('[id^="pane-"]');
    var e={k:keyOf(h), ch:chp?chp.id:'', co:cop?cop.id:''};
    HEADS.push(e);
    var b=document.createElement('button');b.type='button';b.className='done-toggle';
    function paint(){var on=!!done[e.k];b.classList.toggle('on',on);
      b.textContent=on?'✓ 완료':'완료 표시';h.classList.toggle('done-h',on);}
    b.addEventListener('click',function(){
      if(done[e.k])delete done[e.k];else done[e.k]=1;dsave();paint();buildToc();paintProgress();});
    paint();h.appendChild(b);
    e.paint=paint;
  });

  /* 챕터 전체 완료 버튼 (Learn 챕터 하단 test-jump 안) */
  var BULK={};
  (function(){
    var byCh={};
    HEADS.forEach(function(e){(byCh[e.ch]=byCh[e.ch]||[]).push(e);});
    Object.keys(byCh).forEach(function(id){
      var pane=document.getElementById(id);if(!pane)return;
      var tj=pane.querySelector('.test-jump');if(!tj)return;
      var b=document.createElement('button');b.type='button';b.className='bulk-done';
      b.textContent='✓ 레슨 전부 완료';
      b.addEventListener('click',function(){
        var hs=byCh[id],all=hs.every(function(e){return !!done[e.k];});
        hs.forEach(function(e){if(all)delete done[e.k];else done[e.k]=1;e.paint();});
        dsave();buildToc();paintProgress();
      });
      tj.appendChild(b);
      BULK[id]={btn:b};
    });
  })();
  function setBadge(tab,txt,full){
    if(!tab)return;
    var s=tab.querySelector('.prog');
    if(!txt){if(s)s.remove();return;}
    if(!s){s=document.createElement('span');s.className='prog';tab.appendChild(s);}
    s.textContent=txt;s.classList.toggle('full',!!full);
  }
  function paintProgress(){
    var ch={},co={},allD=0;
    HEADS.forEach(function(e){
      (ch[e.ch]=ch[e.ch]||{d:0,t:0}).t++;(co[e.co]=co[e.co]||{d:0,t:0}).t++;
      if(done[e.k]){ch[e.ch].d++;co[e.co].d++;allD++;}
    });
    Object.keys(ch).forEach(function(id){
      var c=ch[id],full=c.d===c.t,txt=c.d?(full?'✓':c.d+'/'+c.t):'';
      setBadge(document.querySelector('.chapters .tab[data-target="'+id+'"]'),txt,full);
      var tid=id.indexOf('-c-ch')>-1?id.replace('-c-ch','-p-ch'):id.replace(/^tut-ch/,'test-ch');
      if(tid!==id)setBadge(document.querySelector('.chapters .tab[data-target="'+tid+'"]'),txt,full);
    });
    Object.keys(co).forEach(function(id){
      var c=co[id],p=Math.round(c.d/c.t*100);
      setBadge(document.querySelector('.topbar .tab[data-target="'+id+'"]'),c.d?p+'%':'',p===100);
    });
    Object.keys(BULK).forEach(function(id){
      var c=ch[id]||{d:0,t:0};
      BULK[id].btn.textContent=(c.t>0&&c.d===c.t)?'↺ 완료 모두 해제':'✓ 레슨 전부 완료';
    });
    var st=document.querySelector('.masthead .stat');
    if(st){
      var s=document.getElementById('overallprog');
      if(!s){s=document.createElement('span');s.id='overallprog';st.appendChild(s);}
      s.textContent='📈 내 진행률 '+Math.round(allD/(HEADS.length||1)*100)+'% ('+allD+'/'+HEADS.length+' 레슨)';
    }
  }
  paintProgress();
  setTimeout(buildToc,120);

  /* 이어서 학습 (마지막 위치 기억·복원) */
  var PKEY=SITE+':pos';
  function chain(){
    var top=document.querySelector('.topbar .tab.active');if(!top)return null;
    var c=top.dataset.target,pane=document.getElementById(c);if(!pane)return null;
    var mt=pane.querySelector('.modebar .tab.active');
    var chts=Array.prototype.slice.call(pane.querySelectorAll('.chapters .tab.active'));
    var vis=chts.filter(function(t){return t.offsetParent!==null;});
    var cht=vis[0]||chts[0];
    return {c:c,m:mt?mt.dataset.target:null,t:cht?cht.dataset.target:null};
  }
  document.addEventListener('click',function(e){
    if(e.target.closest('.tab')||e.target.closest('.jump-nav'))
      setTimeout(function(){var s=chain();if(s&&s.t)try{localStorage.setItem(PKEY,JSON.stringify(s));}catch(_){}} ,90);
  });
  var pos=null;try{pos=JSON.parse(localStorage.getItem(PKEY)||'null');}catch(e){}
  if(pos&&pos.t&&document.querySelector('.chapters .tab[data-target="'+pos.t+'"]')){
    var pill=document.createElement('button');pill.id='resumepill';pill.type='button';
    pill.textContent='▶ 이어서 학습';
    pill.addEventListener('click',function(){
      var ct=document.querySelector('.topbar .tab[data-target="'+pos.c+'"]');if(ct)ct.click();
      if(pos.m){var mt=document.querySelector('#'+pos.c+' .modebar .tab[data-target="'+pos.m+'"]');if(mt)mt.click();}
      var t=document.querySelector('.chapters .tab[data-target="'+pos.t+'"]');if(t)t.click();
      pill.remove();
    });
    document.addEventListener('click',function(e){
      if(e.target!==pill&&e.target.closest('.tab')&&pill.parentNode)pill.remove();});
    document.body.appendChild(pill);
  }

  /* 코드 복사 버튼 */
  Array.prototype.slice.call(document.querySelectorAll('pre')).forEach(function(p){
    var c=p.querySelector('code');if(!c)return;
    var b=document.createElement('button');b.type='button';b.className='copybtn';b.textContent='복사';
    b.addEventListener('click',function(){
      var txt=c.innerText;
      function ok(){b.textContent='✓ 복사됨';b.classList.add('ok');
        setTimeout(function(){b.textContent='복사';b.classList.remove('ok');},1400);}
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(ok,ok);}
      else{var ta=document.createElement('textarea');ta.value=txt;document.body.appendChild(ta);
        ta.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(ta);ok();}
    });
    p.appendChild(b);
  });

  /* 맨 위로 버튼 */
  var up=document.createElement('button');up.id='totop';up.type='button';up.textContent='↑';
  up.title='맨 위로';document.body.appendChild(up);
  up.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
  addEventListener('scroll',function(){
    var show=(document.documentElement.scrollTop||0)>600;
    up.classList.toggle('show',show);
    var rp=document.getElementById('resumepill');
    if(rp)rp.style.bottom=show?'74px':'18px';
  },{passive:true});

  /* 코드 입력칸: Tab=4칸 · Enter=자동 들여쓰기(':' 뒤 한 단계 추가) · Backspace=4칸 단위 해제 */
  document.addEventListener('keydown',function(e){
    var t=e.target;
    if(!(t&&t.tagName==='TEXTAREA'&&t.classList&&t.classList.contains('code')))return;
    var s=t.selectionStart,en=t.selectionEnd;
    if(e.key==='Tab'){
      e.preventDefault();
      t.value=t.value.slice(0,s)+'    '+t.value.slice(en);
      t.selectionStart=t.selectionEnd=s+4;
    }else if(e.key==='Enter'){
      e.preventDefault();
      var before=t.value.slice(0,s);
      var ls=before.lastIndexOf('\\n')+1;
      var line=before.slice(ls);
      var ind=(line.match(/^[ \\t]*/)||[''])[0];
      if(/:\\s*$/.test(line))ind+='    ';
      var ins='\\n'+ind;
      t.value=before+ins+t.value.slice(en);
      t.selectionStart=t.selectionEnd=s+ins.length;
    }else if(e.key==='Backspace'&&s===en&&s>0){
      var b4=t.value.slice(0,s);
      var ls2=b4.lastIndexOf('\\n')+1;
      var seg=b4.slice(ls2);
      if(seg.length>0&&/^ +$/.test(seg)){
        e.preventDefault();
        var rm=(seg.length%4)||4;
        t.value=t.value.slice(0,s-rm)+t.value.slice(en);
        t.selectionStart=t.selectionEnd=s-rm;
      }
    }
  });

  /* 코드 하이라이팅 */
  var l=document.createElement('link');l.rel='stylesheet';
  l.href='https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css';
  document.head.appendChild(l);
  var s=document.createElement('script');
  s.src='https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js';
  s.onload=function(){
    var blocks=Array.prototype.slice.call(document.querySelectorAll('pre code'));
    var i=0;
    function chunk(){
      var end=Math.min(i+150,blocks.length);
      for(;i<end;i++){try{hljs.highlightElement(blocks[i]);}catch(e){}}
      if(i<blocks.length)(window.requestIdleCallback||setTimeout)(chunk,1);
    }
    (window.requestIdleCallback||setTimeout)(chunk,1);
  };
  s.onerror=function(){};
  document.head.appendChild(s);
})();
"""
