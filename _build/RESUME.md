# 프로젝트 상태 (최종 갱신: 2026-08-29 — 이론서 수준 보완 완료)

## 산출물
- **python_learning.html**: Python 학습 사이트. 7코스·733문제·733러너(브라우저 Pyodide 실행·채점 + 숨김 정답·풀이).
- **cpp_learning.html**: C++ 학습 사이트. 동일 구조, option C(코드 실행기 없이 정답·풀이 공개만).

## 완료된 검토·업그레이드 (A/B/C단계 전부 완료)
- A: 모범답안 검증 — Python 733/733(로컬+브라우저 이중), C++ 733/733(g++ 16.1.0 컴파일·실행). 안전망으로 정리 후 전체 재검증도 실행함.
- B: 교차 언어 오염 정리 — Python쪽 C++ 언급 0건, C++쪽 Python 언급 0건(예외: novice-low/ch09b의 문제 예제 데이터 "Python 3" 3건은 콘텐츠라 유지).
- C: frontend-design 업그레이드 — 공통 디자인 시스템 `_build/theme.py`(Pretendard+JetBrains Mono, 라이트/다크 자동, 읽기 진행바, 우측 레슨 TOC(1440px+), highlight.js 코드 하이라이팅, 정제된 카드·탭·러너 UI). 두 빌드가 같은 모듈을 import — 구조 동일, 액센트만 Python=틸(#0d8577)/C++=블루(#0f6bb8). 기능(탭·채점·reveal) 회귀 검증 통과.

## 빌드·검증 도구 (_build/)
- `build_html.py` → python_learning.html / `cpp_build.py` → cpp_learning.html (둘 다 `theme.py` import)
- `verify_runners.py`(Python 정답 실행 검증) / `verify_cpp.py [scope]`(C++ g++ 검증; scope: 101|trails|<trail명>|all)
- `lang_purity_check.py`(교차언어 오염 스캔) / `qa_check.py`·`fence_check.py`(md 무결성; BASE가 Python쪽 기준 — cpp 점검 시 BASE 수정)
- g++: WinGet WinLibs POSIX UCRT 16.1.0 (verify_cpp.py에 경로 하드코딩됨)

## 콘텐츠 소스
- Python: 루트 ch*.md(=Tutorial 코스) + trails/<코스>/ch*.md
- C++: cpp/ 하위 동일 구조 (러너 형식: ```runner @@SOLUTION/@@TESTS/@@EXPL)
- 문제/러너 1:1(각 733), ```runner 블록 안 중첩 펜스 금지

## 순차 학습 기능 (2026-07-03 추가, 두 사이트 공통)
- Learn 하단 "Test에서 문제 풀기 →" / Test 하단 "다음 챕터 Learn →" (레벨 마지막→다음 레벨, 최종→완주 메시지) — 빌드 스크립트의 jump_btn/next_course_of 헬퍼가 생성, JS .jump-nav 위임 핸들러가 이동 처리
- 레슨 완료 토글(제목 우측, 256개) + TOC ✓ 표시 — localStorage '<파일명>:done'
- 이어서 학습 pill(우하단) — 마지막 코스/모드/챕터 localStorage '<파일명>:pos', 탭 클릭 시 자동 저장
- 진행률 뱃지 — 챕터 탭 n/m·완료✓(Learn/Test 미러), 코스 탭 %, 마스트헤드 전체 진행률 칩(paintProgress, theme.py)
- 마감 기능(2026-07-03) — 사이트 간 전환 링크(.langswap, 마스트헤드 우상단), 코드블록 복사 버튼(hover), 맨 위로 버튼(#totop), 러너 입력칸 Tab=4칸 들여쓰기, 풀이 불릿 마커 복원, :focus-visible 접근성. 순차 검토 v2로 미배운 문법 선행 설명 73건(py 39/cpp 34) 추가 완료.

## 재개가 필요할 때
- md 수정 후: 해당 빌드 스크립트 재실행 → 필요 시 verify 재실행
- 디자인 수정: theme.py만 고치고 두 빌드 재실행(두 사이트 동일 유지)


## 2026-08-28 업그레이드 (Python 전용 — 이후 cpp는 동결)
- **정책**: 사용자 결정으로 이후 업그레이드는 `python_learning.html`만. `cpp/`·`cpp_build.py`·`cpp_learning.html`은 손대지 않는다.
- **추가 연습 레슨**: 상위 트레일 45개 챕터마다 `trails/<trail>/ch{NN}x.md`(접미사 x → 병합 순서 마지막)에 `## L{K}. 추가 연습 — 핵심 반복 × 유형 확장` 레슨 1개씩. 총 **496문제**(novice-low 112 / novice-mid 100 / novice-high 114 / int-low 68 / int-mid 54 / int-high 48). 사이트 전체 733 → **1,229문제**, 레슨 256 → 301.
  - 구성: 반복 훈련 50~60% + 유형 확장 40~50%(백준 단계별·solved.ac CLASS·프로그래머스 Kit·이코테·NeetCode 150·삼성 기출 스타일, 전부 창작). 레슨 첫머리에 문제 구성표.
  - 규격 문서: `_build/EXTRA_SPEC.md`. 문법 수준은 챕터 기존 정답 범위 준수(선행 문법은 풀이 첫 줄에 설명).
- **📚 자료 탭**: `_build/resources.py`(RES_MD·RES_CSS·resources_pane) — 레벨 매핑표, 추천 문제집 링크, 학습 루틴, 파이썬 치트시트. `build_html.py`가 import해 최상위 탭 `pane-resources`로 렌더링(레슨 없음 → 진행률 집계 대상 아님).
- **빌드 스크립트 변경**: `build_html.py`에 resources import, 마스트헤드 칩 `✨ 추가 연습 N문제`(ch??x.md 자동 집계), 안내문·푸터 문구. 백업 `build_html.py.bak`.
- **검증 도구**: 신규 `_build/verify_file.py <md...>` — 단일 파일 구조(5항목·번호·난이도·중첩 펜스·C++ 언급) + 정답 실행 대조 + 실행 시간 WARN. `verify_runners.py`/`verify_file.py` 모두 자식 프로세스에 `PYTHONIOENCODING=utf-8, PYTHONUTF8=1`을 넘기도록 수정(Windows cp949 파이프에서 한글 출력 문제가 오판정되던 것 해결).
- **검증 결과**: 신규 45파일 496문제 verify_file 전부 OK(ERROR 0/WARN 0). 전체 verify_runners 재실행 결과는 아래 「재개」 항목 참고.
- **환경 주의**: 이 세션의 Bash 도구는 heredoc 안의 이중 백슬래시를 하나로 접고, `python - <<EOF` stdin은 cp949로 읽힌다 → 패치 스크립트는 파일로 저장 후 `PYTHONUTF8=1 python file.py`.

## 재개가 필요할 때 (2026-08-28 이후)
- 문제 추가: 해당 챕터의 `ch{NN}x.md`에 문제 카드 이어 붙이기(번호 연속) → `python _build/verify_file.py <파일>` → `PYTHONUTF8=1 python _build/build_html.py`.
- 새 레슨/챕터 유형이 필요하면 `EXTRA_SPEC.md` 규격을 그대로 따른다.

## 2026-08-29 GitHub Pages 배포
- **공개 주소**: https://kimdg0094.github.io/python-coding-test/ — 저장소 `kimdg0094/python-coding-test` (public, `main` 브랜치 `/` 루트)
- **사용자 선택**: 저작권 주의(README의 "무단 배포 금지", Tutorial 탭 69문제가 © Codetree)를 안내했고, 사용자가 "전체 배포 + 검색엔진 차단"을 선택함. Tutorial 포함 1,229문제 전부 배포.
- **색인 차단 2중**: `robots.txt`(User-agent: * Disallow: / + GPTBot·ClaudeBot·Google-Extended·CCBot·PerplexityBot·Bytespider) / `<meta name='robots' content='noindex, nofollow, noarchive, nosnippet'>` — 메타는 `build_html.py`의 viewport 줄 다음에 삽입되어 재빌드해도 유지됨.
- **추가 파일**: `index.html`(python_learning.html로 리다이렉트, 테마 맞춤), `.nojekyll`(`_build/` 등 언더스코어 폴더가 Jekyll에 무시되지 않게), `.gitignore`(cpp·로그·venv·pycache 제외), `robots.txt`
- **커밋 범위**: 124파일 9.4MB. `cpp/`·`cpp_learning.html`은 동결이라 제외 — 다시 포함하려면 `.gitignore`에서 두 줄 삭제.
- **검증**: 루트/학습페이지 200 OK, gzip 전송 1.17MB, robots.txt 서빙 확인, noindex 메타 확인, 실제 브라우저에서 Hard 문제(장르별 인기곡 플레이리스트) Pyodide 채점 ✅ 통과.
- **갱신 절차**: md 수정 → `python _build/build_html.py` → `git add -A && git commit && git push` → 1~2분 후 반영.

## 2026-08-29 이론서 수준 보완 (45/45 챕터 완료)
- **동기**: 사이트 평가 "입문은 개념·실수·체크리스트가 있어 페이지만으로 되지만, 이후는 교과서가 아니라 코테 요약. 그림 없음. 이론서 대체는 아님."
- **진단(데이터)**: 트레일에 체크리스트 1개 파일·자주 하는 실수 0개, 도식 0건(mermaid 0/SVG 0/박스드로잉 1). 구조가 `개념→접근 전략→문제` 3단이라 유도·추적·템플릿 자리가 없었음.
- **Part A(기존 48개 파일에 추가만)**: 각 레슨 개념부에 `**그림으로 보기**`/`**손으로 따라가기**`/`**왜 이렇게 되는가**` 삽입. 45/45 챕터 완료.
- **Part B(신규 45개 `ch{NN}z.md`)**: `## L{K}. 정리 —` 레슨. 개념 지도·뼈대 코드·언제 무엇을 쓰나·마스터 체크리스트·자주 하는 실수(❌→왜→✅ 3단). 병합 순서가 `'' < a < b < c < x < z`라 챕터 맨 끝에 온다.
- **결과**: 레슨 301→346, 도식 573개, 체크박스 705개, 표 290개, dlabel 852개. HTML 5.5MB→7.2MB.
- **빌드 변경**: `build_html.py`의 `md2html`이 심화 라벨을 `<h4 class="dlabel dl-*">`로 승격하고 `<table>`을 `.tablewrap`으로 감쌈. 스타일은 `resources.py`의 `RES_CSS`(python 전용, theme.py는 cpp 공용이라 미변경).
- **도식 규칙(중요)**: `--mono`가 `JetBrains Mono → D2Coding → Consolas`인데 JetBrains Mono에 한글 글리프가 없어 도식 안 한글은 폰트 폴백으로 정렬이 깨진다. **정렬 칸은 ASCII만, 한글은 줄 끝 `#` 주석만 허용** — `verify_depth.py --diagrams`가 강제.
- **안전장치**: `verify_depth.py --diff`가 git으로 (1) 기존 줄이 새 파일의 부분수열인지(=추가만) (2) 각 레슨 `**문제**` 이후 구간이 바이트 동일한지 검사. 20개 에이전트 동시 작업에도 러너 1229/1229 유지.
- **함께 수정**: 초안 자기 정정 문구 노출 5건(ch06 15→20, ch07 NO→YES, ch10 9→7, novice-mid/ch04 시각 2건, int-high/ch02 2→3), 오타 2곳, `verify_file.py` 입력 없는 문제 테스트 1개 허용.
- **정정 기록**: 오케스트레이터가 에이전트에 "파이썬에서 `mask & 1 == 0`이 잘못 묶인다"고 잘못 지시했으나 에이전트가 실측으로 반박(파이썬은 `&`가 비교보다 우선순위가 높아 올바르게 묶임 — C 계열 함정의 오전파). 실제 함정인 `1 << n - 1`로 교체됨.

## 2026-09-08 ✨ Extra 모드 신설 (추가 연습을 Test에서 분리)
- **변경**: 각 트레일 코스의 모드바가 `📖 Learn · 🧩 Test · ✨ Extra` 3개. `ch{NN}x.md`(추가 연습)는 Learn/Test 병합에서 제외하고 Extra 모드에 챕터별 패널(`{alias}-x-ch{N}`)로 렌더링 — 레슨 머리(반복 개념·출제 맵·구성표) 카드 + 문제 러너. Tutorial(codetree-101)은 x 파일이 없어 Extra 없음.
- **빌드 스크립트**: `build_html.py` — `split_trail_text`/`_lesson_parts` 헬퍼 분리, `render_extra_chapter` 추가, 트레일 루프에서 접미사 x 조각을 따로 읽음. 마스트헤드 칩 `✨ Extra N문제`는 루프에서 누적(EXTRA_P). 순차 내비: Learn 하단 `[Test 풀기][Extra]`, Test 하단 `[Extra][다음 Learn]`, Extra 하단 `[다음 Learn]`.
- **진행률**: Extra 레슨 제목에도 완료 토글(챕터당 1개) → Extra 챕터 탭 ✓ 뱃지, 코스 %에 포함. 예전에 Learn에서 완료 표시한 「추가 연습」 키(`*-c-chN::L9. 추가 연습…`)는 페이지 로드 시 `*-x-chN::…`으로 자동 이관(build_html.py JS 첫 블록). Extra 패널의 `.bulk-done`은 CSS로 숨김(`resources.py` RES_CSS).
- **수치**: 러너 1229 유지(Learn/Test 733 + Extra 496), 레슨 346 유지(Learn 301 + Extra 45). Learn 레슨 번호는 md 그대로라 x 번호(예: L9)가 Learn에서는 비고 Extra에 있음.
- **미반영 항목**: Learn 챕터 헤더 칩 `레슨 n·문제 m`은 이제 x 제외 수치. `EXTRA_SPEC.md`의 md 규격은 변경 없음(파일 위치·형식 동일).
- **검증**: 브라우저(localhost)에서 모드 전환·jump-nav(Test→Extra→다음 Learn)·완료 토글·뱃지·키 이관·Pyodide 채점(Extra 1번 정답 ✅) 확인. 배포는 `git push` 필요.

## 2026-09-08 예제 표기 정비 (가로줄 현상 + `/` 줄바꿈 표기 통일)
- **현상 1 — 예제 출력에 가로줄(`---`)이 그어짐**: 원인은 `- **예제**:` 목록 항목 아래에 2칸 들여쓴 ```` ``` ```` 펜스. Python-Markdown의 `fenced_code`는 펜스가 줄 맨 앞에 있어야만 인식하므로 내용이 일반 마크다운으로 해석돼 `***` 줄이 `<hr>`, `**`가 강조로 바뀜(별 사각형·`*hi*` 문제 등). 레슨 구분용으로 남은 단독 `---`도 `<hr>`가 되어 카드 끝에 줄이 보였음.
  - 수정: `build_html.py`에 `_IndentedFenceExt`(들여쓴 펜스를 htmlStash 자리표시자로 치환하는 Preprocessor, 우선순위 26)와 `_strip_hr`(펜스 밖 `---`/`***`/`___` 단독 줄 제거) 추가. `md2html`이 둘을 사용. 백업 `_build/tmp/build_html.py.before_fence`. 결과 `python_learning.html`의 `<hr />` 14 → 0.
- **현상 2 — 입력은 `/`로 줄바꿈을 표시하는데 출력은 표시하지 않고 쭉 씀**: 규칙을 하나로 통일 — **코드 상자 안의 ` / ` = 줄바꿈, 케이스 사이 ` · ` = 다른 예제**. 문제 카드 위 안내문(Test·트레일·Extra 3곳)에 범례 `EX_LEGEND`(`.ex-legend`, theme.py) 표시.
  - **도구**: 신규 `_build/verify_examples.py` — 예제 줄을 파싱해 `@@SOLUTION`을 실제 실행한 결과와 대조. `--fix`(안전한 자동 정정: `a` `b`처럼 붙어 있던 것을 실행 결과 줄 수에 맞춰 `a / b`로), `--normalize`(표기 통일: `` `a` / `b` `` → `` `a / b` ``, 케이스 구분 ` / `·`,`·`;` → ` · `), `--show MISMATCH,NORM,all`. 두 번 실행하면 변경 0(멱등). 판정: OK / OK-MARKED / FIX-* / NORM-* / MISMATCH / RUNERR(추상 표기 `n=5, ops=[...]`류) / PROSE / SKIP.
  - **자동 정정**: FIX 43곳, NORM-OUT 166 / NORM-IN 223 / NORM-SEP 277곳(58파일).
  - **수동 정정(값 자체가 틀렸던 예제 17건, 러너 정답 기준)**: int-high/ch05 행렬곱 26000→14000 · int-low/ch01 `*10/12*`→`*21/12*`, `.B.W.B`→`.BW.B`, 튕기는 공 `2 0`→`0 0` · int-low/ch02 점프 `2`→2가지 · int-mid/ch01 두 수 합 둘째 예제 교체, LRU 출력 · novice-high/ch03a 버블 패스(N 3→5), 안정성 예제, 기수 정렬 · novice-high/ch05 `2`→`3` · ch08a 20→25 · ch08b 45/35→25(검산 인용문 재작성) · ch10 두 번째 최단 2→4(정점 재방문 허용 명시) · novice-mid/ch01 자릿수 합 1→2, 팰린드롬 소수 4→5 · ch06 13→19 · ch09 신호등 4→-1. 이 예제들에 붙어 있던 "예제의 함정" 류 문구는 모두 제거(예제는 정답과 일치해야 함).
  - **표기만 정정**: `\n` 표기(novice-mid/ch02), `입력`/`출력` 라벨 분리형(novice-high/ch10), `S=…, P=…` 추상형(int-high/ch04), 리스트 표기(int-low/ch05 DP 전부 stdin 형식으로), 첫 줄 N 누락(novice-high/ch02·ch05 스택/덱), `,` 로 나뉜 다중 줄 입력(novice-high/ch06). 스크립트 `_build/tmp/manual_fixes.py`, `manual_fixes2.py`.
  - **남은 MISMATCH 6건은 의도적**: `…`/`...` 생략(로또·구구단), 분수 출력 `5/6`(줄바꿈 아님을 예제에 명시), 빈 줄 출력(소인수분해 1), 검산 주석의 `{4,2,5}`. → 2차 정비(아래)에서 분수 1건만 남기고 해소.
- **검증**: `verify_runners.py` 1229/1229, 브라우저(localhost)에서 별 사각형 코드 상자·범례 렌더링 확인. 배포는 `git push` 필요.
- **다음에 예제를 추가/수정할 때**: `PYTHONUTF8=1 python _build/verify_examples.py --normalize <md>`로 확인 → 표기 통일이 필요하면 `--fix --normalize`.

## 2026-09-08 예제 표기 정비 2차 — 모든 예제의 줄바꿈을 눈에 보이게
- **요청**: "`slow 5 SHOW … → slow fast …`처럼 쓰면 입력·출력의 줄바꿈을 알 수 없다. 모든 예제를 `slow / 5 / SHOW / …` → `slow / fast / …` 식으로." → 예제 span 안의 ```` ``` ```` 상자·추상 표기·산문 표기를 전부 인라인 ` / ` 표기로 통일.
- **규칙(확정)**: 코드 상자 안 ` / ` = 줄바꿈, ` · ` = 다른 예제, `(입력 없음)`/`(출력 없음)`, `(빈 줄)` = 빈 줄 한 개(코드 상자 안에서도 사용 가능: `` `1 2 3 / (빈 줄) / 4 5 6` ``). 인라인으로 표현하면 뜻이 깨지는 출력(앞뒤 공백·연속 공백 — 인라인 `<code>`는 공백을 접음 —, `/`·백틱 포함, `(출력 앞부분)` 부분 출력)만 여러 줄 상자를 유지. 범례 `EX_LEGEND`에 `(빈 줄)`·상자 설명 추가.
- **자동 변환** `_build/tmp/convert_fenced.py`: 예제 span 안 펜스 109개 → 인라인, 42개 유지(별 도형·우측정렬 표·`|`/`----+` 표·빈 줄 포함 격자·부분 출력). 로그 `_build/tmp/convert_log.txt`. 후처리로 `` `c` → `d` `` 연속줄을 ` · `로 병합.
- **수동 변환** `manual_fixes3.py`(59곳)·`manual_fixes4.py`(4곳)·`manual_fixes5.py`(6곳): `n=5, ops=[...]`·`S=…` 추상 표기 → 러너 입력 형식(int-high/ch02 9문제·ch03·ch04·ch05, int-low/ch01·ch04·ch06, int-mid/ch04·ch05, novice-high/ch03a·ch03b·ch06·ch06x·ch08a·ch09·ch10, novice-mid/ch02·ch05, novice-low/ch05c·ch05x·ch09a, ch04-loops-1(LeebrosCode 6줄)·ch07·ch09·ch10). 로또 7줄·`(출력 앞부분)` 대신 전체 출력 기입. `sep_pass.py`: 예제 줄에서 백틱·괄호 밖의 ` / `(케이스 구분으로 쓰인 것) 24곳 → ` · `.
- **값 정정(러너 정답 기준, 검산 메모도 함께 고침)**: int-low/ch06 `4`→`5`, `84`→`96` · novice-high/ch10:944 둘째 값 `2`→`1` · novice-high/ch03b `5 / 5 4 3 2 1`→`0 2` · int-mid/ch04 동전 뒤집기 `4 / THTH` `-1`→`2`(검산 2가 THTH→HHTH로 잘못 뒤집음; 실제 i=0→HTTH, i=1→HHHH) + `3 / TTT`→`-1` 추가 · int-low/ch03 미로 `YES 8`→`YES 9`(셀프체크의 8칸 목록에 도착 (0,3) 누락) · int-mid/ch04 동전 예제 `2 30 / 1 7`→`6` 채움 · novice-high/ch03a 선택 정렬 예제 값 채움. 예제에 붙어 있던 "직접 손으로 전개해 답을 확정할 것" 류 문구 제거.
- **검증기 변경** `_build/verify_examples.py`: 괄호 토큰 1단계 중첩 허용, `(빈 줄…)` 단독 = 출력 없음, `split_lines`가 `(빈 줄)`→빈 문자열, `(검산 …)` 메모 줄은 파싱 제외(위치 보존). **git 미추적 상태였음 → `git add _build/verify_examples.py` 필요.**
- **novice-high/ch01(시간복잡도 개념 챕터) 17문제** `manual_fixes6.py`: 손 분석 과제는 요구사항에 그대로 두고 입력/출력/예제를 러너의 stdin/stdout 형식으로 재작성(출력 끝에 "(손 분석 과제: …)"로 원래 과제 유지). 예: `5 2 9 / 5` → `1 best`, `a 4` → `16 O(n^2)`, `97` → `prime 8`, `1000000` → `iter O(1) / rec O(log n) 20 / time O(log n)`.
- **초안 흔적 제거**: novice-high/ch09 최소 이동 횟수 예제(`(M실제=3) ...` — 아래 정확 버전 참고 / 예제(정확) ×2 → 한 줄로), int-mid/ch02 `(인덱스 1..3의 1+3+1? 실은 …)`, novice-high/ch09x 검산 `` `4` / `3 2 1 1` `` → `` `4 / 3 2 1 1` ``, ch01-basics "출력 `T`" → "(입력 없음) → `T`".
- **최종 판정** `_build/tmp/ex_after6.txt`: OK 2492 / RUNERR 0 / PROSE 0 / MISMATCH 2(novice-mid/ch01 분수 `5/6` — 줄바꿈이 아님을 예제에 명시, 의도적) / SKIP 2(ch04a·ch04x `(출력 없음)` 별도 줄 — 파서 오탐, 값은 정확). 러너 1229/1229. 브라우저(localhost)에서 slow/fast 예제·범례·별 피라미드 상자 렌더링 확인.
- **재개**: 예제를 새로 쓸 때는 위 규칙대로 인라인 ` / ` 표기 → `PYTHONUTF8=1 python _build/verify_examples.py --show MISMATCH,RUNERR,PROSE <md>`(전체 실행은 2분 이상 → timeout 600000).
