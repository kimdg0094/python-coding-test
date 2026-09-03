## L11. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 레슨은 Ch08(동적계획법) 전체를 한 장으로 묶는다. L1~L3에서 배운 "DP란 무엇이고 어떻게 구현하는가"와, L4~L8의 기본 유형 다섯 가지, 그리고 L9의 그리디가 사실은 **같은 질문("마지막 선택을 무엇으로 쪼갤 것인가")에 대한 서로 다른 답**이라는 것을 확인한다. 새 개념은 없고, 지도·뼈대·판단 기준·체크리스트만 남긴다.

**개념 지도**

- DP는 "쓸 수 있는가(조건) → 어떻게 구현하는가(방식) → 어떤 모양인가(유형)"의 3층 구조다. 문제를 만나면 항상 이 순서로 내려간다.

```text
  Ch08 : dynamic programming

  STEP 1  can I use DP ?
     optimal substructure   big answer is built from small answers
     overlapping subproblem the same small answer is needed again
     (both hold)  -> DP     (only the first) -> divide and conquer

  STEP 2  design  (always these four lines, in this order)
     state       dp[...] = "..."          # 한 문장으로 못 박는다
     recurrence  split by the LAST choice # 마지막 한 걸음으로 쪼갠다
     base        smallest case by hand    # 점화식이 안 통하는 칸
     order       small ones first         # 읽는 칸이 먼저 채워지게

  STEP 3  how to fill it       (same states, same answer)
     MEMOIZATION top-down       TABULATION bottom-up
     recursion + memo table     loops + table
     only the states you need   every state
     call stack = depth         no recursion, rolling is easy
```

- 유형 다섯 가지는 결국 **dp 표의 모양과 "어느 칸을 읽는가"**로 갈린다. ● 는 지금 채우는 칸, ▲ ◀ ↘ 는 그 칸이 읽는 자리다.

```text
  five shapes of a dp table      * = the cell being filled

  1) merge        dp[i]     <- dp[i-1], dp[i-2] ...
     +--+--+--+--+--+
     |  |  | ^| ^| *|               # 왼쪽 몇 칸만 읽는다
     +--+--+--+--+--+

  2) grid         dp[r][c]  <- dp[r-1][c], dp[r][c-1]
     +--+--+    3) cond.  dp[i][s] <- dp[i-1][s'] if allowed
     |  | ^|       s=0 +--+--+
     +--+--+           | ^| *|
     | <| *|       s=1 +--+--+      # 층이 곧 '직전 선택'
     +--+--+           | ^|  |
                       +--+--+

  4) knapsack     dp[c]     <- dp[c-w] + v
     +--+--+--+--+--+--+
     |  | ^|  |  | *|  |            # w 칸 뒤를 읽는다
     +--+--+--+--+--+--+

  5) two words    dp[i][j]  <- diag / up / left
     +--+--+
     | \| ^|
     +--+--+
     | <| *|                        # 세 칸 중 하나 또는 전부
     +--+--+
```

- L9의 그리디는 DP의 반대말이 아니라 **DP를 안 써도 되는 특수한 경우**다. 갈림길은 하나뿐이다.

```text
  greedy or dp ?

  does a locally best pick always stay in some optimal answer ?
       |                                   |
      yes                                 no / not sure
       |                                   |
   sort + one pass                     build the whole table
   O(n log n)                          O(states x transitions)
   proof needed (exchange argument)    always safe
```

**뼈대 코드**

- (1) 같은 문제, 두 가지 구현. 상태·점화식·기저는 완전히 같고 채우는 방향만 다르다.

```python
import sys
from functools import lru_cache
sys.setrecursionlimit(300000)

# 하향식: 재귀 그대로 두고 진입부에서 캐시 조회
@lru_cache(maxsize=None)
def f(i):                            # ← 상태: dp[i] = i번째 칸까지의 답
    if i <= 1:
        return 1                     # ← 기저: 문제마다 바뀜
    return f(i - 1) + f(i - 2)       # ← 점화식: 문제마다 바뀜

# 상향식: 같은 식을 작은 것부터 채운다
def g(n):
    dp = [0] * (n + 1)               # 칸 수는 n+1 (0..n 전부 쓴다)
    dp[0] = dp[1] = 1                # ← 기저
    for i in range(2, n + 1):        # 읽는 칸이 먼저 채워지는 순서
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

- (2) 유형 1 — 부분문제를 그대로 합치기. 개수 세기는 합, 최적값은 min/max다.

```python
MOD = 1_000_000_007                  # ← 문제마다 바뀜 (10007 등)
STEPS = (1, 2, 3)                    # ← 한 번에 갈 수 있는 걸음들

cnt = [0] * (n + 1)
cnt[0] = 1                           # 빈 선택도 한 가지 방법
for i in range(1, n + 1):
    for s in STEPS:                  # 마지막 한 걸음이 무엇이었나로 나눈다
        if i - s >= 0:
            cnt[i] = (cnt[i] + cnt[i - s]) % MOD   # 덧셈마다 나머지
# ← 최적값 문제면 cnt를 INF로 채우고 '+' 자리를 min(...) + cost[i] 로 바꾼다
```

- (3) 유형 2 — 격자 한 칸 전진. 첫 행·첫 열을 따로 쓰지 말고 "없으면 0/INF"로 처리하면 코드가 짧아진다.

```python
R, C = len(grid), len(grid[0])
dp = [[0] * C for _ in range(R)]     # 행마다 새 리스트로 만들 것

for r in range(R):
    for c in range(C):
        if grid[r][c] == BLOCK:      # ← 장애물 표시는 문제마다 바뀜
            dp[r][c] = 0             # 경로 수면 0, 최소비용이면 INF
            continue
        if r == 0 and c == 0:
            dp[r][c] = 1             # ← 시작 칸: 경로 수 1 / 비용 grid[0][0]
            continue
        up = dp[r - 1][c] if r > 0 else 0
        left = dp[r][c - 1] if c > 0 else 0
        dp[r][c] = up + left         # ← 결합: 개수면 +, 비용이면 min + 값
print(dp[R - 1][C - 1])
```

- (4) 유형 3 — 조건에 맞게 선택적으로 전진. "직전에 무엇을 골랐나"를 상태 축으로 올린다.

```python
S = 2                                # ← 상태 개수: 문제마다 바뀜
NEG = float('-inf')
dp = [[NEG] * S for _ in range(n)]
dp[0][0], dp[0][1] = 0, a[0]         # ← 0=안 고름, 1=고름

for i in range(1, n):
    dp[i][0] = max(dp[i - 1][0], dp[i - 1][1])   # 안 고름: 직전은 자유
    dp[i][1] = dp[i - 1][0] + a[i]               # 고름: 직전은 반드시 0
print(max(dp[n - 1]))                # ← 답의 위치: 마지막 칸의 유효 상태들
```

- (5) 유형 4 — 배낭. 루프 방향 한 글자가 "한 번만"과 "여러 번"을 가른다.

```python
# 0/1 배낭: 각 아이템 최대 1개  ->  용량 역순
dp = [0] * (W + 1)
for w, v in items:
    for c in range(W, w - 1, -1):    # 역순! 정순이면 같은 물건을 또 쓴다
        dp[c] = max(dp[c], dp[c - w] + v)

# 무한 배낭: 각 아이템 무제한  ->  용량 정순
dp2 = [0] * (W + 1)
for w, v in items:
    for c in range(w, W + 1):        # 정순! 방금 넣은 것을 또 쓴다
        dp2[c] = max(dp2[c], dp2[c - w] + v)
```

- (6) 유형 5 — 두 문자열. 끝 글자가 같은지로 갈라진다.

```python
n, m = len(A), len(B)
dp = [[0] * (m + 1) for _ in range(n + 1)]

for i in range(1, n + 1):
    for j in range(1, m + 1):
        if A[i - 1] == B[j - 1]:               # dp는 1-based, 문자열은 0-based
            dp[i][j] = dp[i - 1][j - 1] + 1    # ← 부분수열이면 대각선 +1
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
            # ← 연속 부분문자열이면 여기가 0 (이어짐이 끊기므로 리셋)
print(dp[n][m])
```

- (7) L9 그리디 — 정렬 기준 하나가 알고리즘 전부다.

```python
items.sort(key=lambda x: x[1])       # ← 정렬 기준: 여기가 문제의 본체
picked, last = 0, -INF_START         # ← 직전에 확정한 값
for s, e in items:
    if s >= last:                    # ← 채택 조건: 문제마다 바뀜
        picked += 1
        last = e                     # 한 번 고른 선택은 되돌리지 않는다
```

**언제 무엇을 쓰나**

- 먼저 지문의 말을 상태 정의로 옮긴다. DP에서 가장 자주 막히는 곳은 코드가 아니라 이 한 줄이다.

| 지문에 이런 말이 보이면 | 이렇게 상태를 잡는다 | 결합 연산 |
|---|---|---|
| "몇 가지 방법", "경우의 수" | `dp[i]` = i까지 오는 방법의 수 | `+` (와 `% MOD`) |
| "최소 비용", "최솟값" | `dp[i]` = i까지의 최소 비용 | `min` (초기값 INF) |
| "최대 이익", "가장 긴" | `dp[i]` = i를 끝으로 하는 최댓값 | `max` (초기값 -inf) |
| "오른쪽/아래로만 이동" | `dp[r][c]` = (r,c)에 도달했을 때의 답 | 위·왼쪽 결합 |
| "직전에 고른 것에 영향을 받는다" | `dp[i][s]` — s에 직전 선택을 넣는다 | 허용 전이만 결합 |
| "각 물건을 한 번씩만" | `dp[c]` = 용량 c일 때 최댓값, 역순 루프 | `max` |
| "얼마든지 여러 번 쓸 수 있다" | `dp[c]`, 정순 루프 | `max` 또는 `min` |
| "두 문자열의 공통", "몇 번 고쳐야" | `dp[i][j]` = A 앞 i글자, B 앞 j글자 | 대각·위·왼쪽 |
| "연속된"(구간이 끊기면 안 됨) | `dp[i]` = i를 **반드시 포함**하는 답 | 이어붙이기 vs 새로 시작 |
| "1,000,000,007로 나눈 나머지" | 상태는 그대로, 연산마다 `% MOD` | `+`, `*` 후 `% MOD` |

- 상태를 정했으면 도구를 고른다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 같은 부분문제가 다시 나온다 | DP(표에 저장) | 부분문제 개수만큼만 계산한다 | O(상태 × 전이) |
| 부분문제가 한 번씩만 쓰인다 | 그냥 분할정복 | 저장해도 재사용이 없어 이득이 없다 | 저장 불필요 |
| 상태 공간이 넓고 닿는 건 일부 | 메모이제이션 | 필요한 상태만 방문한다 | O(방문 상태) |
| 상태를 거의 다 쓰고 깊이가 깊다 | 타뷸레이션 | 재귀 스택이 없어 안전하고 상수배 빠름 | O(전체 상태) |
| 직전 1~2칸만 읽는다 | rolling(변수 2개 또는 행 2개) | 표 전체를 남길 이유가 없다 | 공간 O(1)/O(m) |
| 이동 방향이 오른쪽·아래로 제한 | 유형 2(격자) | 각 칸이 정해진 두세 칸에서만 온다 | O(R × C) |
| "인접 금지", "연속 k번까지" | 유형 3(상태 추가) | i만으로는 다음 선택 가능 여부를 모른다 | O(n × 상태 수) |
| 용량 한도 안에서 고르기 | 유형 4(배낭) | 완전탐색 2^n을 용량 축으로 압축 | O(n × W) |
| 국소 최적이 항상 전체 최적에 남는다 | 그리디 | 표를 만들 필요 없이 한 번 훑으면 끝 | O(n log n) |
| 그 증명이 안 되거나 반례가 보인다 | DP | 안전한 쪽이 항상 옳다 | O(상태 × 전이) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 최적 부분 구조와 중복 부분 문제가 **둘 다** 필요한 이유와, 하나만 있을 때 무엇이 되는지.
- [ ] 설명할 수 있다: 나이브 재귀 피보나치가 지수 시간인 이유를 호출 트리의 노드 수로.
- [ ] 설명할 수 있다: 점화식을 만드는 절차(상태 → 마지막 선택으로 쪼개기 → 식 → 기저 → 계산 순서 → 답의 위치).
- [ ] 설명할 수 있다: DP의 복잡도가 왜 "상태 개수 × 한 칸 채우는 비용"인지.
- [ ] 설명할 수 있다: 메모이제이션과 타뷸레이션이 같은 답을 내는 이유와, 무엇을 보고 둘 중 하나를 고르는지.
- [ ] 설명할 수 있다: 타뷸레이션에서 "계산 순서"를 정하는 유일한 근거(읽는 칸이 먼저 채워져야 한다).
- [ ] 설명할 수 있다: 경우의 수 DP에서 케이스가 **상호 배타적**이어야 그냥 더할 수 있는 이유.
- [ ] 설명할 수 있다: 격자 DP에서 첫 행·첫 열이 왜 따로 다뤄지고, 장애물을 어떤 값으로 막는지.
- [ ] 설명할 수 있다: `dp[i]`에 상태 축을 하나 더 붙여야 한다는 신호가 무엇인지.
- [ ] 설명할 수 있다: 0/1 배낭이 역순, 무한 배낭이 정순인 이유를 "무엇을 읽고 있는가"로.
- [ ] 설명할 수 있다: LCS 점화식에서 끝 글자가 같을 때 대각선을 쓰는 이유와, 부분수열과 부분문자열의 차이.
- [ ] 설명할 수 있다: 도달 불가 상태를 0이 아니라 INF / -inf로 두어야 하는 이유.
- [ ] 설명할 수 있다: 그리디가 성립하기 위한 두 성질과, 동전 문제에서 그리디가 깨지는 예.

**⚠️ 자주 하는 실수**

**1) 0/1 배낭의 용량 루프를 정순으로 돈다**

```python
# ❌ 틀린 코드
dp = [0] * (W + 1)
for w, v in items:
    for c in range(w, W + 1):        # 정순: 무한 배낭의 루프다
        dp[c] = max(dp[c], dp[c - w] + v)
```

왜: `dp[c - w]`는 **이번 아이템을 이미 반영한 뒤의 값**이다. 무게 3짜리 물건 하나로 `dp[3]`이 갱신되면, 곧이어 `dp[6]`이 그 `dp[3]`을 읽어 같은 물건을 두 번 담아 버린다. 한 개뿐인 물건이 무한개가 되어 답이 조용히 커진다. 예제에서는 통과하고 큰 입력에서만 틀리는 전형적인 유형이다.

```python
# ✅ 고친 코드
dp = [0] * (W + 1)
for w, v in items:
    for c in range(W, w - 1, -1):    # 역순: dp[c-w]는 '이번 아이템 이전' 값
        dp[c] = max(dp[c], dp[c - w] + v)
```

**2) 메모의 초기값과 "아직 계산 안 됨"을 구분하지 못한다**

```python
# ❌ 틀린 코드
memo = [0] * (n + 1)                 # 0으로 채워 두고
def f(i):
    if memo[i]:                      # 0이면 '미계산'으로 간주
        return memo[i]
    memo[i] = compute(i)
    return memo[i]
```

왜: 답이 진짜로 `0`인 상태를 저장해도 `if memo[i]`가 거짓이라 매번 다시 계산한다. 캐시가 통째로 무력화돼 지수 시간으로 되돌아가고, 부작용이 있는 함수라면 답까지 틀린다.

```python
# ✅ 고친 코드
memo = [None] * (n + 1)              # '미계산'을 답과 겹치지 않는 값으로
def f(i):
    if memo[i] is not None:          # 값 자체가 아니라 '있는지'를 묻는다
        return memo[i]
    memo[i] = compute(i)
    return memo[i]
```

**3) 도달 불가 칸을 0으로 둬서 최솟값이 0이 된다**

```python
# ❌ 틀린 코드
dp = [0] * (n + 1)                   # 최소 비용인데 전부 0으로 시작
for i in range(1, n + 1):
    dp[i] = min(dp[i - 1], dp[i - 2]) + cost[i]
```

왜: `min` DP에서 0은 "공짜로 갈 수 있다"는 뜻이다. 아직 아무것도 계산되지 않은 칸이 항상 최솟값으로 뽑혀 결과가 0 근처로 눌린다. 최댓값 DP에서 `0`으로 두면 반대로 "도달 못 하는 칸"이 유효한 후보가 된다.

```python
# ✅ 고친 코드
INF = float('inf')
dp = [INF] * (n + 1)                 # 도달 불가를 명시적으로 표시
dp[0] = 0                            # 진짜 출발점만 0
for i in range(1, n + 1):
    cand = dp[i - 1]
    if i >= 2:
        cand = min(cand, dp[i - 2])
    if cand != INF:                  # 도달 가능할 때만 갱신
        dp[i] = cand + cost[i]
```

**4) 경우의 수 DP의 기저를 0으로 둔다**

```python
# ❌ 틀린 코드
dp = [0] * (n + 1)                   # dp[0]도 0
for i in range(1, n + 1):
    for s in (1, 2, 3):
        if i - s >= 0:
            dp[i] += dp[i - s]
print(dp[n])                         # 항상 0이 나온다
```

왜: `dp[0]`은 "아무것도 안 쓰고 목표에 서 있는 방법"이라 **1가지**다. 이 값이 0이면 표 전체가 0의 합이라 답이 0으로 고정된다. 개수 세기 DP에서 "빈 선택도 하나의 방법"이라는 점을 놓치는 것이 이 실수의 정체다.

```python
# ✅ 고친 코드
dp = [0] * (n + 1)
dp[0] = 1                            # 빈 선택 = 방법 1가지
for i in range(1, n + 1):
    for s in (1, 2, 3):
        if i - s >= 0:
            dp[i] += dp[i - s]
```

**5) 모듈러를 마지막에 한 번만 취한다**

```python
# ❌ 틀린 코드
for i in range(2, n + 1):
    dp[i] = dp[i - 1] + dp[i - 2]    # 자릿수가 계속 늘어난다
print(dp[n] % MOD)
```

왜: 파이썬은 큰 정수를 지원하므로 값 자체는 맞지만, 자릿수가 수천 자리로 커지면 덧셈 한 번이 더 이상 O(1)이 아니다. n이 커질수록 눈에 띄게 느려져 시간 초과가 난다(다른 언어라면 아예 오버플로로 오답이 된다).

```python
# ✅ 고친 코드
MOD = 1_000_000_007
for i in range(2, n + 1):
    dp[i] = (dp[i - 1] + dp[i - 2]) % MOD   # 연산마다 취해 값을 묶어 둔다
print(dp[n] % MOD)
```

**6) 표 크기를 n으로 잡고 음수 인덱스를 방치한다**

```python
# ❌ 틀린 코드
dp = [0] * n                         # 0..n 을 쓸 계획인데 칸이 n개뿐
dp[0] = 1
for i in range(1, n + 1):
    dp[i] = dp[i - 1] + dp[i - 2]    # i == n 에서 IndexError
```

왜: `dp[0]`부터 `dp[n]`까지 쓰려면 칸이 `n + 1`개 필요하다. 게다가 `i = 1`일 때 `dp[-1]`은 파이썬에서 오류가 아니라 **맨 뒤 칸**을 읽으므로, 크기를 고쳐도 음수 인덱스 검사를 빼면 예외 없이 조용히 엉뚱한 값이 섞인다.

```python
# ✅ 고친 코드
dp = [0] * (n + 1)                   # 0..n 을 다 담는다
dp[0] = 1
for i in range(1, n + 1):
    dp[i] = dp[i - 1]
    if i >= 2:                       # 음수 인덱스를 막는다
        dp[i] += dp[i - 2]
```

**7) 그리디로 되는지 확인하지 않고 그리디를 쓴다**

```python
# ❌ 틀린 코드
def min_coins(coins, target):
    coins.sort(reverse=True)
    cnt, rest = 0, target
    for c in coins:                  # 큰 동전부터 최대한 집는다
        cnt += rest // c
        rest %= c
    return cnt                       # coins=[1,4,5], target=8 -> 4 (실제 답 2)
```

왜: 그리디는 "국소 최적이 항상 어떤 전체 최적해 안에 남는다"가 증명될 때만 옳다. `[1, 4, 5]`로 8을 만들 때 5를 먼저 집으면 5+1+1+1로 4개가 되지만, 4+4면 2개다. 큰 동전이 나머지를 나누어떨어뜨린다는 보장이 없으면 그리디가 깨진다.

```python
# ✅ 고친 코드
INF = float('inf')
def min_coins(coins, target):
    dp = [INF] * (target + 1)
    dp[0] = 0
    for c in coins:                  # 무한 배낭 = 정순 루프
        for x in range(c, target + 1):
            if dp[x - c] != INF:
                dp[x] = min(dp[x], dp[x - c] + 1)
    return dp[target] if dp[target] != INF else -1
```

**다음 챕터로**

- 여기서 잡은 "상태 한 문장 → 마지막 선택으로 쪼개기 → 기저 → 순서" 절차는 다음 단계의 DP에서도 그대로 쓰인다. 달라지는 것은 상태의 개수와 축의 종류뿐이다.
- 유형 3(조건부 전진)에서 붙였던 상태 축 `s`는 이후 "직전 선택 의존형·모드 전환형" DP로 확장되고, 유형 4(배낭)는 개수 제한·경우의 수·정확히 채우기 변형으로, 유형 5(두 문자열)는 편집 거리와 부분수열 개수 세기로 이어진다.
