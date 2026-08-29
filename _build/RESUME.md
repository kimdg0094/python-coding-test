# 프로젝트 상태 (최종 갱신: 2026-08-29 — GitHub Pages 배포)

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
