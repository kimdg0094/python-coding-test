# -*- coding: utf-8 -*-
# 「📚 자료」 탭: 외부 코딩테스트 자료 가이드 + 사이트 레벨 매핑 + 파이썬 치트시트
# build_html.py 에서 import 해서 사용 (Python 사이트 전용)
import re

RES_MD = r"""
## 이 사이트 레벨 ↔ 외부 자료 매핑

각 레벨을 마친 뒤(또는 병행하며) 아래 외부 자료의 **같은 유형**을 2~3문제씩 추가로 풀면 개념이 오래 남습니다. 각 챕터 끝의 **「추가 연습」 레슨**은 이 매핑의 유형을 챕터 수준으로 재구성한 창작 문제입니다.

| 사이트 레벨 | 백준 「단계별로 풀어보기」 | solved.ac | 프로그래머스 고득점 Kit | 『이코테』 파트 | NeetCode 150 | 기타 |
|---|---|---|---|---|---|---|
| Tutorial · novice-low | 입출력과 사칙연산 · 조건문 · 반복문 · 1차원 배열 · 문자열 · 심화 1 · 2차원 배열 | CLASS 1 | — | — | — | 코드트리 「프로그래밍 시작/기초」 |
| novice-mid | 일반 수학 1 · 약수/배수와 소수 · 브루트 포스 · 정렬 · 재귀 | CLASS 2 | 정렬 · 완전탐색 | 구현 · 그리디 | — | 코드트리 「프로그래밍 연습」 |
| novice-high | 스택/큐/덱 · 집합과 맵 · 이분 탐색 · 우선순위 큐 · 트리 · DFS와 BFS · 동적 계획법 1 | CLASS 3 | 해시 · 스택/큐 · 힙 · 정렬 · DFS/BFS · 동적계획법 | 정렬 · 이진 탐색 · DFS/BFS · DP | Arrays & Hashing · Stack · Binary Search · Linked List · Trees · Heap | 코드트리 「자료구조 알고리즘」 |
| intermediate-low | 백트래킹 · DFS와 BFS · 동적 계획법 1~2 · 분할 정복 | CLASS 3~4 | 완전탐색 · DFS/BFS · 동적계획법 | DFS/BFS · DP | Backtracking · Graphs · 1-D DP · 2-D DP | **삼성 SW 역량테스트 기출**(시뮬레이션·BFS·백트래킹) |
| intermediate-mid | 누적 합 · 투 포인터 · 이분 탐색 · 그리디 · 최단 경로 · 우선순위 큐 | CLASS 4 | 탐욕법 · 이분탐색 · 그래프 · 힙 | 그리디 · 이진 탐색 · 최단 경로 | Two Pointers · Sliding Window · Greedy · Intervals · Advanced Graphs | 카카오 블라인드 기출(구현+자료구조) |
| intermediate-high | 트리 · 최소 신장 트리 · 위상 정렬 · 유니온 파인드 · 최소 공통 조상 · 문자열 알고리즘 · 동적 계획법 3 | CLASS 5 | 그래프 · 동적계획법 | 그래프 이론 · 기타 그래프 | Tries · 2-D DP · Bit Manipulation · Math & Geometry | Codeforces Div.2 C~D |

## 추천 외부 자료

#### 한국어 플랫폼 · 문제집

- **[백준 온라인 저지 — 단계별로 풀어보기](https://www.acmicpc.net/step)** · 입출력부터 세그먼트 트리까지 주제별 계단식 구성. 가장 표준적인 국내 연습 경로. **활용**: 위 표의 단계 이름으로 찾아 챕터를 끝낼 때마다 2~3문제.
- **[solved.ac CLASS](https://solved.ac/class)** · 백준 문제를 난이도·필수도로 큐레이션한 클래스(1~10). **활용**: CLASS 2 = 기초 완성, CLASS 4~5 = 대기업 코테 안정권 기준으로 진도 점검.
- **[프로그래머스 — 코딩테스트 고득점 Kit](https://school.programmers.co.kr/learn/challenges?tab=algorithm_practice_kit)** · 해시·스택/큐·힙·정렬·완전탐색·탐욕법·DP·DFS/BFS·이분탐색·그래프 10개 주제. 실제 기업 코테(함수 작성형)와 형식이 같다. **활용**: novice-high 이후 주제별로 전부 풀기.
- **[백준 문제집 — 삼성 SW 역량 테스트 기출](https://www.acmicpc.net/workbook/view/1152)** · 시뮬레이션·BFS·백트래킹 중심. **활용**: intermediate-low의 Simulation/Backtracking/BFS 챕터를 마친 뒤 도전.
- **[백준 문제집 — IT기업·대기업 코테와 비슷했던 문제들](https://www.acmicpc.net/workbook/view/8708)** · 실제 코테와 유사한 문제 모음(지속 갱신). **활용**: 모의고사용.
- **[tony9402/baekjoon — 코딩테스트 대비 유형별 문제집](https://github.com/tony9402/baekjoon)** · 자료구조·트리·수학·그리디·DP·투포인터·구현·그래프·브루트포스·시뮬레이션·이분탐색·백트래킹·분할정복·누적합·문자열·최단경로·위상정렬·분리집합·MST·트라이 등 23개 유형별 추천 문제. **활용**: 약한 유형만 골라 집중 훈련.
- **[코테 단골 유형 실버 문제집 (philgineer)](https://www.philgineer.com/2021/11/codingtest-selection.html)** · 문자열·수학·재귀·브루트포스·정렬·백트래킹·DP·그리디·큐/덱·분할정복·이분탐색·DFS/BFS·트리 13유형 대표 문제. **활용**: novice-high 마무리 점검용 미니 세트.
- **[코드트리 (Codetree)](https://www.codetree.ai/)** · 이 사이트 커리큘럼의 원본. 삼성 역량테스트 대비 트레일이 강점. **활용**: 원문 강의·채점이 필요할 때.
- **[SW Expert Academy](https://swexpertacademy.com/)** · 삼성 주관 문제 사이트. **활용**: 삼성 계열 코테 준비 시 모의 테스트.

#### 책 · 강의

- **[『이것이 취업을 위한 코딩테스트다 with 파이썬』 공식 소스코드](https://github.com/ndb796/python-for-coding-test)** · 그리디·구현·DFS/BFS·정렬·이진 탐색·DP·최단 경로·그래프 이론 순서의 대표 교재. **[유튜브 무료 강의](https://www.youtube.com/playlist?list=PLRx0vPvlEmdAghTr5mXQxGpHjWqSz0dgC)** 도 있다. **활용**: novice-high ~ intermediate-mid 구간의 이론 보강.
- **[Do it! 알고리즘 코딩테스트 with Python (인프런 무료 강의)](https://www.inflearn.com/course/%EB%91%90%EC%9E%87-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8-%ED%8C%8C%EC%9D%B4%EC%8D%AC)** · 백준 문제 기반 유형별 강의.

#### 영어 플랫폼

- **[NeetCode 150](https://neetcode.io/practice)** · LeetCode 문제 150개를 18개 패턴(Arrays & Hashing → Two Pointers → Sliding Window → Stack → Binary Search → Linked List → Trees → Heap → Backtracking → Tries → Graphs → DP → Greedy → Intervals → Math → Bit)으로 정리한 로드맵. 각 패턴의 첫 문제가 핵심 패턴을 가르치고 뒤로 갈수록 제약이 붙는다. **활용**: 해외 기업·영어 면접 대비, 또는 패턴별 반복 훈련.
- **[LeetCode](https://leetcode.com/problemset/)** · 함수 작성형 문제 3,000+. 태그·회사별 필터. **활용**: 특정 패턴(Sliding Window 등)만 골라 10문제씩.
- **[Codeforces](https://codeforces.com/)** · 실시간 대회. Div.2 A~B는 novice-high, C~D는 intermediate-high 수준. **활용**: 시간 압박 훈련.

## 학습 루틴 제안

1. **Learn**에서 레슨 개념을 읽고 예제 코드를 손으로 따라 친다.
2. **Test**에서 그 레슨 문제를 스스로 푼다 → 러너로 채점 → 틀리면 정답을 보지 말고 **셀프체크**로 먼저 점검.
3. 챕터 끝 **「추가 연습」 레슨**으로 같은 개념을 소재를 바꿔 반복하고, 코테 단골 유형으로 확장한다.
4. 위 매핑표에서 같은 유형의 외부 문제를 **2~3개** 더 푼다(백준·프로그래머스).
5. 틀린 문제는 풀이의 **「스스로 다시 짤 때 생각 순서」** 를 보며 **다음 날 백지에서 다시** 짠다. 3일 뒤 한 번 더.

## 파이썬 코딩테스트 치트시트

```python
# ── 빠른 입력 (입력이 수만 줄 이상이면 input() 대신) ──
import sys
input = sys.stdin.readline          # 끝의 '\n' 포함 → .rstrip() 또는 int() 로 처리
n = int(input())
arr = list(map(int, input().split()))
data = sys.stdin.read().split()      # 전체를 한 번에 토큰으로

# ── 재귀 한도 (DFS 깊이가 1000을 넘을 수 있으면) ──
sys.setrecursionlimit(10**6)

# ── 자주 쓰는 표준 라이브러리 ──
from collections import deque, Counter, defaultdict
q = deque([start]); q.popleft(); q.appendleft(x)      # BFS 큐 · 덱
cnt = Counter(arr); cnt.most_common(1)                 # 빈도
g = defaultdict(list); g[u].append(v)                  # 인접 리스트

import heapq
heapq.heappush(h, (dist, node)); d, u = heapq.heappop(h)   # 최소 힙 (최대 힙은 -값)

from bisect import bisect_left, bisect_right
lo = bisect_left(sorted_arr, x)      # x 이상 첫 위치 = lower_bound
hi = bisect_right(sorted_arr, x)     # x 초과 첫 위치 = upper_bound → 개수는 hi - lo

from itertools import permutations, combinations, product, accumulate
list(combinations(arr, 2)); list(permutations(arr)); list(accumulate(arr))  # 누적합

import math
math.gcd(a, b); math.lcm(a, b); math.isqrt(n); math.comb(n, r)

# ── 정렬 관용구 ──
arr.sort(key=lambda x: (-x[1], x[0]))       # 2차 기준: 값 내림차순, 같으면 이름 오름차순
INF = float('inf')

# ── 격자 4방향/8방향 ──
dx = [-1, 1, 0, 0]; dy = [0, 0, -1, 1]
for d in range(4):
    nx, ny = x + dx[d], y + dy[d]
    if 0 <= nx < n and 0 <= ny < m: ...

# ── 2차원 배열 생성 (얕은 복사 함정 피하기) ──
grid = [[0] * m for _ in range(n)]       # OK
# grid = [[0] * m] * n                    # 금지: 모든 행이 같은 객체

# ── 출력 모아서 한 번에 (print 수만 번은 느림) ──
out = []
out.append(str(ans))
print("\n".join(out))
```

**시간 감각**: 파이썬은 초당 대략 2~5천만 회 단순 연산. N=10⁵면 O(N log N)까지, N=10³이면 O(N²)까지, N=20이면 O(2ᴺ)까지 안전하다.
"""

def resources_pane(md2html):
    body = md2html(RES_MD.strip())
    body = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', body)
    head = ('<div class="ch-head"><h1>📚 코딩테스트 외부 자료 가이드</h1>'
            '<div class="chips"><span class="chip">레벨 매핑</span><span class="chip">추천 문제집</span>'
            '<span class="chip">학습 루틴</span><span class="chip">파이썬 치트시트</span></div></div>')
    return ('<div class="pane" id="pane-resources"><div class="wrap">'
            '<div class="trail-banner"><b>📚 자료</b> · 인터넷에서 찾은 코딩테스트 연습 자료를 이 사이트의 레벨과 연결했습니다. '
            '각 챕터 끝의 <b>「추가 연습」</b> 레슨은 이 자료들의 단골 유형을 챕터 수준으로 재구성한 창작 문제입니다.</div>'
            + head + '<div class="res-body">' + body + '</div></div></div>')

RES_CSS = """
/* ── 심화 보완(DEPTH_SPEC) 라벨: 그림/추적/유도/정리 ── */
.dlabel{display:flex;align-items:center;gap:8px;font-size:14.5px;font-weight:800;
  letter-spacing:-.02em;color:var(--accent-d);margin:26px 0 10px;padding:7px 13px;
  background:var(--accent-l);border-left:3px solid var(--accent);border-radius:0 9px 9px 0}
.dlabel::before{font-weight:400;font-size:15px;line-height:1;opacity:.95}
.dl-fig::before{content:"🖼"}
.dl-trace::before{content:"✍"}
.dl-why::before{content:"💡"}
.dl-map::before{content:"🗺"}
.dl-skel::before{content:"🧰"}
.dl-pick::before{content:"🧭"}
.dl-next::before{content:"➡"}
.dl-check{color:#0f7a4f;background:rgba(22,163,101,.10);border-left-color:#16a365}
.dl-warn{color:#9a5b00;background:rgba(217,138,10,.12);border-left-color:#d98a0a}
@media (prefers-color-scheme:dark){
  .dl-check{color:#5fd6a0;background:rgba(95,214,160,.12);border-left-color:#3fbc86}
  .dl-warn{color:#f0b95c;background:rgba(240,185,92,.12);border-left-color:#d99f3c}
}
.dlabel + p,.dlabel + ul,.dlabel + ol,.dlabel + pre,.dlabel + .tablewrap{margin-top:8px}
/* 도식(```text)은 줄바꿈 없이 그대로 — 넘치면 블록 안에서만 스크롤 */
pre>code.language-text,pre>code.language-diagram{white-space:pre}
/* 넓은 표는 페이지가 아니라 표 안에서 스크롤 */
.tablewrap{overflow-x:auto;margin:14px 0}
.tablewrap table{margin:0}

/* ── 예제 묶음: 빈 줄로 구분된 독립 예제를 각각의 박스로 ── */
.exset{margin:13px 0}
.exset pre{margin:0}
.exset pre + pre{margin-top:9px}
/* 같은 설명에 딸린 예제들임을 알 수 있게 왼쪽에 옅은 연결선 */
.exset{border-left:2px solid var(--accent-lb);padding-left:11px;border-radius:2px}

/* ── 코드 입력칸: 내용만큼 높이가 늘어나고 내부 스크롤 없음 ── */
.runner .code{overflow-y:hidden;resize:none;min-height:150px;
  height:auto;field-sizing:content}

.res-body h2{font-size:19px;font-weight:800;letter-spacing:-.03em;margin:30px 0 10px;color:var(--ink)}
.res-body h4{font-size:15px;font-weight:700;margin:20px 0 6px;color:var(--accent-d)}
.res-body p{margin:9px 0;line-height:1.7}
.res-body ul,.res-body ol{margin:9px 0;padding-left:23px}
.res-body li{margin:7px 0;line-height:1.65}
.res-body table{font-size:13px}
.res-body table th,.res-body table td{vertical-align:top}
.res-body table td:first-child{white-space:nowrap;font-weight:700}
.res-body .tablewrap{overflow-x:auto}
"""
