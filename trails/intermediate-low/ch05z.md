## L6. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 레슨은 Ch5(DP I)의 네 유형을 **변형까지 포함해** 한 장으로 묶는다. L1~L4에서는 각 유형의 기본형을 배웠다. 실제 문제는 거의 항상 그 기본형에 조건 하나가 더 붙은 모습으로 나오므로, 여기서는 "무엇이 바뀌면 코드의 어디가 바뀌는가"를 축으로 정리한다. 특히 배낭 세 종류의 차이는 **루프 방향 한 줄**로 갈리므로 표로 못 박아 둔다.

**개념 지도**

- 배낭 계열은 "각 아이템을 몇 번 쓸 수 있는가" 하나만 물으면 코드가 결정된다.

```text
  knapsack : one question decides the code

              how many times may one item be used ?
                            |
      +---------------------+---------------------+
      |                     |                     |
   at most 1            unlimited             at most k
   0/1                  unbounded             bounded
      |                     |                     |
  for c in W..w        for c in w..W        split k into
  descending           ascending            1, 2, 4, ..., rest
      |                     |               then run 0/1 on each
  dp[c-w] is the       dp[c-w] already            |
  value BEFORE         includes this item    O(n W log k)
  this item                  |
      |                   O(n W)
   O(n W)
```

- 격자·조건부 전진은 "어느 칸에서 들어오는가"만 갈아끼우면 된다. 아래 네 축이 변형의 전부다.

```text
  grid / conditional dp : what changes from problem to problem

  1 incoming     right+down  -> dp[r][c] <- dp[r-1][c], dp[r][c-1]
                 three ways  -> dp[r][c] <- dp[r-1][c-1 .. c+1]
                 jump 1 or k -> dp[i]    <- dp[i-1], dp[i-k]
                 window k    -> dp[i]    <- min(dp[i-k .. i-1])

  2 direction    forward  for i in 1..n     # 앞에서부터 쌓는 문제
                 backward for i in n..1     # '지금 고르면 t 뒤로 점프'

  3 blocked      counting -> 0              # 경로가 없음
                 min cost -> INF            # 도달 불가

  4 space        only row r-1 is read -> keep two rows, O(C)
```

- 답이 커지는 경우의 수 문제는 모듈러가 따라온다. 나머지 연산은 덧셈·곱셈과 자유롭게 섞이지만, **뺄셈만 예외**다.

```text
  modular arithmetic

  (a + b) % m == ((a % m) + (b % m)) % m      ok
  (a * b) % m == ((a % m) * (b % m)) % m      ok
  (a - b) % m -> may go negative in theory    +m then % m
  (a / b) % m != (a % m) / (b % m)            never divide

  take the remainder at EVERY step, not once at the end
```

**뼈대 코드**

- (1) 0/1 배낭 — 각 아이템 최대 1개. 2차원으로 먼저 이해하고 1차원으로 압축한다.

```python
# 2차원: dp[i][c] = 앞 i개 아이템만 보고 용량 c를 쓸 때 최대 가치
dp = [[0] * (W + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    w, v = items[i - 1]                       # ← 아이템 표현은 문제마다 바뀜
    for c in range(W + 1):
        dp[i][c] = dp[i - 1][c]               # 안 담는다
        if c >= w:
            dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)   # 담는다

# 1차원 압축: 위 식이 '이전 행'만 읽으므로 한 줄로 줄인다
dp = [0] * (W + 1)
for w, v in items:
    for c in range(W, w - 1, -1):             # 역순이 '이전 행'을 흉내낸다
        dp[c] = max(dp[c], dp[c - w] + v)
print(dp[W])
```

- (2) 무한 배낭 — 각 아이템 무제한. 정순이면 "방금 담은 것"을 다시 읽는다.

```python
INF = float('inf')

# 최대 가치
dp = [0] * (W + 1)
for w, v in items:
    for c in range(w, W + 1):                 # 정순 = 재사용 허용
        dp[c] = max(dp[c], dp[c - w] + v)

# 최소 개수 변형: 초기값과 결합만 바꾼다
cnt = [INF] * (W + 1)
cnt[0] = 0                                    # ← 기저: 0을 만드는 데 0개
for w in weights:
    for c in range(w, W + 1):
        if cnt[c - w] != INF:                 # 도달 불가에서 +1 하지 않는다
            cnt[c] = min(cnt[c], cnt[c - w] + 1)
print(cnt[W] if cnt[W] != INF else -1)        # ← 불가능일 때 출력은 문제마다
```

- (3) 개수 제한 배낭 — 아이템 i를 최대 `k_i`개. 두 가지 방법이 있다.

```python
# 방법 A: 상태에 '몇 개 썼나'를 직접 넣는다. k가 작을 때 가장 안전하다.
dp = [0] * (W + 1)
for w, v, k in items:                         # ← (무게, 가치, 개수 한도)
    ndp = dp[:]                               # 이번 아이템 '이전' 값을 보존
    for c in range(W + 1):
        for t in range(1, k + 1):             # t개 쓰는 경우를 전부 시도
            if c < w * t:
                break
            ndp[c] = max(ndp[c], dp[c - w * t] + v * t)
    dp = ndp

# 방법 B: k를 1,2,4,... 로 쪼개 0/1 배낭으로 바꾼다. k가 클 때.
packs = []
for w, v, k in items:
    p = 1
    while p <= k:                             # 1+2+4+... 로 1..k를 모두 표현
        packs.append((w * p, v * p))
        k -= p
        p *= 2
    if k > 0:
        packs.append((w * k, v * k))          # 남은 나머지도 묶음 하나로
dp = [0] * (W + 1)
for w, v in packs:
    for c in range(W, w - 1, -1):             # 이제 그냥 0/1 배낭
        dp[c] = max(dp[c], dp[c - w] + v)
```

- (4) 경우의 수 배낭 — 루프 중첩 순서가 "조합"과 "순열"을 가른다.

```python
MOD = 1_000_000_007                           # ← 문제마다 바뀜

# 조합(고른 집합이 같으면 한 가지): 아이템이 바깥
comb = [0] * (W + 1)
comb[0] = 1                                   # ← 빈 선택 = 1가지
for w in weights:
    for c in range(w, W + 1):
        comb[c] = (comb[c] + comb[c - w]) % MOD

# 순열(고르는 순서가 다르면 다른 것): 용량이 바깥
perm = [0] * (W + 1)
perm[0] = 1
for c in range(1, W + 1):
    for w in weights:
        if c >= w:
            perm[c] = (perm[c] + perm[c - w]) % MOD
```

- (5) 격자 전진의 변형 — 들어오는 방향과 훑는 방향만 갈아끼운다.

```python
# 3방향(대각선 포함) + 장애물 + 두 줄만 유지
NEG = float('-inf')
prev = [NEG] * C
prev[0] = g[0][0]                             # ← 기저: 시작 칸
for r in range(1, R):
    cur = [NEG] * C
    for c in range(C):
        if g[r][c] == BLOCK:                  # ← 막힌 칸 표시는 문제마다
            continue                          # NEG 그대로 두어 차단
        best = NEG
        for d in (-1, 0, 1):                  # ← 들어오는 방향 목록
            pc = c + d
            if 0 <= pc < C and prev[pc] != NEG:
                best = max(best, prev[pc])
        if best != NEG:
            cur[c] = best + g[r][c]
    prev = cur
print(max(prev))
```

- (6) 조건부 전진의 변형 — 후보를 어떻게 거르느냐만 다르다.

```python
INF = float('inf')

# (a) 최근 k칸 중에서만 점프: dp[i] = cost[i] + min(dp[i-k .. i-1])
dp = [INF] * (n + 1)
dp[0] = 0
for i in range(1, n + 1):
    for j in range(max(0, i - k), i):         # ← 점프 폭 제한이 조건
        if dp[j] != INF:
            dp[i] = min(dp[i], dp[j] + cost[i])

# (b) 뒤에서 앞으로: "지금 고르면 t칸 뒤로 건너뛴다"
dp = [0] * (n + 2)
for i in range(n - 1, -1, -1):
    dp[i] = dp[i + 1]                         # 이번 것을 건너뛴다
    if i + t[i] <= n:                         # ← 기한 안에 끝나야 채택 가능
        dp[i] = max(dp[i], p[i] + dp[i + t[i]])
print(dp[0])
```

**언제 무엇을 쓰나**

- 먼저 배낭 세 종류를 구분한다. 지문에서 "각 물건을 몇 번 쓸 수 있는가"만 찾으면 된다.

| 유형 | 지문의 표현 | 용량 루프 | 점화식 | 복잡도 |
|---|---|---|---|---|
| 0/1 배낭 | "각각 하나씩", "한 번만" | `range(W, w-1, -1)` 역순 | `dp[c] = max(dp[c], dp[c-w]+v)` | O(n·W) |
| 무한 배낭 | "얼마든지", "제한 없이" | `range(w, W+1)` 정순 | 같은 식, 방향만 다름 | O(n·W) |
| 개수 제한 | "최대 k개까지" | 개수 축 추가 또는 이진 분할 | `dp[c-w·t] + v·t` | O(n·W·k) 또는 O(n·W·log k) |

- 그다음 "무엇을 묻는가"로 초기값과 결합 연산을 정한다.

| 지문에 이런 말이 보이면 | 상태·초기값 | 결합 |
|---|---|---|
| "최대 가치" (남아도 됨) | `dp = [0]*(W+1)` | `max` |
| "정확히 W를 채워서 최대" | `dp = [-inf]*(W+1)`, `dp[0]=0` | `max` |
| "만드는 데 필요한 최소 개수" | `dp = [INF]*(W+1)`, `dp[0]=0` | `min` |
| "만드는 방법의 수" | `dp = [0]*(W+1)`, `dp[0]=1` | `+` |
| "순서가 다르면 다른 방법" | 같은 배열, **용량 루프를 바깥**으로 | `+` |
| "…로 나눈 나머지" | 배열은 그대로 | 연산마다 `% MOD` |
| "만들 수 없으면 -1" | 도달 불가를 INF/-inf로 유지 | 마지막에 판별 |

- 유형 사이의 갈림길은 이 표로 끊는다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 마지막 한 걸음이 몇 가지로 배타적 | 유형 1(합치기) | 겹치지 않으니 그냥 더한다 | O(n × 걸음 수) |
| 격자에서 방향이 제한돼 있다 | 유형 2(격자) | 각 칸이 정해진 몇 칸에서만 온다 | O(R × C) |
| 격자 크기는 큰데 직전 행만 읽는다 | 두 행만 유지 | 나머지 행은 다시 안 쓴다 | 공간 O(C) |
| "이 원소 뒤에 이을 수 있나"를 따진다 | 유형 3(조건부 전진) | 조건을 만족하는 후보만 모아 최적 | O(n²) |
| 점프 폭이 최대 k로 제한 | 최근 k칸만 후보 | 나머지는 애초에 전이가 없다 | O(n·k) |
| "고르면 t칸 뒤로 건너뛴다" | 뒤에서 앞으로 채우기 | 미래 칸이 먼저 확정돼야 읽을 수 있다 | O(n) |
| 용량·예산 한도 안에서 고르기 | 유형 4(배낭) | 완전탐색 2^n을 용량 축으로 압축 | O(n·W) |
| 아이템 개수 한도 k가 아주 크다 | 이진 분할 후 0/1 | k를 통째로 도는 루프를 없앤다 | O(n·W·log k) |
| 용량이 10^9처럼 크고 아이템은 적다 | 배낭이 아니다 | 표를 만들 수 없으니 다른 접근 | — |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 0/1 배낭의 2차원 점화식이 어떻게 1차원 역순 루프로 압축되는지, 역순이 무엇을 흉내내는지.
- [ ] 설명할 수 있다: 무한 배낭의 정순 루프에서 `dp[c-w]`가 "이번 아이템을 이미 쓴 값"인 이유.
- [ ] 설명할 수 있다: 개수 제한 배낭을 1, 2, 4, … 로 쪼개면 왜 1부터 k까지 모든 개수를 만들 수 있는지.
- [ ] 설명할 수 있다: 경우의 수 배낭에서 아이템 루프를 바깥에 두면 조합, 용량 루프를 바깥에 두면 순열이 되는 이유.
- [ ] 설명할 수 있다: "정확히 채우기"와 "넘지 않게 채우기"의 초기값 차이(`-inf` vs `0`)와 그 이유.
- [ ] 설명할 수 있다: 최소 개수 DP에서 `INF`에 1을 더하면 왜 안 되는지.
- [ ] 설명할 수 있다: 격자 DP에서 첫 행·첫 열이 기저가 되는 이유와, 3방향 전이일 때 범위 검사가 필요한 이유.
- [ ] 설명할 수 있다: 장애물을 경우의 수 문제에서는 0, 최소 비용 문제에서는 INF로 막는 이유.
- [ ] 설명할 수 있다: 직전 행만 읽는 격자 DP를 두 행으로 줄일 수 있는 근거.
- [ ] 설명할 수 있다: "고르면 t칸 뒤로 점프"류를 왜 뒤에서 앞으로 채우는지.
- [ ] 설명할 수 있다: 매 연산마다 `% MOD`를 취해도 최종 답이 바뀌지 않는 이유와, 뺄셈만 예외인 이유.
- [ ] 설명할 수 있다: 배낭 DP의 복잡도가 O(n·W)인 근거와, W가 커지면 왜 이 접근이 무너지는지.

**⚠️ 자주 하는 실수**

**1) 0/1 배낭의 용량 루프를 정순으로 돈다**

```python
# ❌ 틀린 코드
dp = [0] * (W + 1)
for w, v in items:
    for c in range(w, W + 1):        # 정순
        dp[c] = max(dp[c], dp[c - w] + v)
```

왜: 1차원 압축의 전제는 "`dp[c - w]`가 **이번 아이템을 반영하기 전** 값"이라는 것이다. 정순이면 그 전제가 깨진다. 무게 2, 가치 3짜리 물건 하나, `W = 6`으로 손으로 돌려 보면 `dp[2] = 3`, `dp[4] = dp[2] + 3 = 6`, `dp[6] = dp[4] + 3 = 9`가 되어 한 개뿐인 물건이 세 번 담긴다. 정답은 3인데 9가 나온다.

```python
# ✅ 고친 코드
dp = [0] * (W + 1)
for w, v in items:
    for c in range(W, w - 1, -1):    # 역순: dp[c-w]는 아직 갱신 전
        dp[c] = max(dp[c], dp[c - w] + v)
```

**2) 무한 배낭을 역순으로 돌아 재사용을 막아 버린다**

```python
# ❌ 틀린 코드
# "동전을 얼마든지 쓸 수 있다"인데 0/1 루프를 그대로 복사했다
cnt = [INF] * (W + 1)
cnt[0] = 0
for w in coins:
    for c in range(W, w - 1, -1):    # 역순
        cnt[c] = min(cnt[c], cnt[c - w] + 1)
```

왜: 역순은 "같은 동전을 두 번 쓰지 마라"는 뜻이다. 동전마다 최대 한 번만 쓰이므로 `coins = [1, 5]`로 12를 만들 때 답이 나오지 않거나(`INF`) 엉뚱하게 커진다. 0/1과 무한은 **의도가 정반대**이므로 루프 방향을 복사하면 안 된다.

```python
# ✅ 고친 코드
cnt = [INF] * (W + 1)
cnt[0] = 0
for w in coins:
    for c in range(w, W + 1):        # 정순: 방금 쓴 동전을 또 쓴다
        if cnt[c - w] != INF:
            cnt[c] = min(cnt[c], cnt[c - w] + 1)
```

**3) 개수 제한이 있는데 무한 배낭으로 푼다**

```python
# ❌ 틀린 코드
# 각 아이템을 최대 k개까지만 쓸 수 있는데 k를 무시했다
dp = [0] * (W + 1)
for w, v, k in items:
    for c in range(w, W + 1):        # 정순 = 무제한
        dp[c] = max(dp[c], dp[c - w] + v)
```

왜: 정순 루프는 개수 제한을 전혀 모른다. 가장 가치 대비 무게가 좋은 아이템 하나만 용량이 허락하는 만큼 반복해서 담아 버려, 답이 항상 크게 나온다. 제한 `k`는 코드 어딘가에서 **세어져야** 한다.

```python
# ✅ 고친 코드
dp = [0] * (W + 1)
for w, v, k in items:
    ndp = dp[:]                      # 이번 아이템 이전 값을 따로 보존
    for c in range(W + 1):
        for t in range(1, k + 1):    # t개 쓰는 경우만 시도
            if c < w * t:
                break
            ndp[c] = max(ndp[c], dp[c - w * t] + v * t)
    dp = ndp
```

**4) 경우의 수 배낭에서 루프 중첩 순서를 뒤집는다**

```python
# ❌ 틀린 코드
# "동전 조합의 가짓수"인데 용량을 바깥 루프에 뒀다
dp = [0] * (W + 1)
dp[0] = 1
for c in range(1, W + 1):
    for w in coins:                  # 안쪽이 아이템
        if c >= w:
            dp[c] += dp[c - w]
```

왜: 이 순서는 "1 다음 2"와 "2 다음 1"을 다른 방법으로 센다. 즉 조합이 아니라 **순열**을 센다. `coins = [1, 2]`, `W = 3`이면 조합은 `{1,1,1}`, `{1,2}`로 2가지인데 이 코드는 3을 낸다. 두 코드는 겉보기 차이가 두 줄뿐이라 눈으로 잡기 어렵다.

```python
# ✅ 고친 코드
dp = [0] * (W + 1)
dp[0] = 1
for w in coins:                      # 아이템이 바깥 = 각 아이템을 한 번만 고려
    for c in range(w, W + 1):
        dp[c] += dp[c - w]
```

**5) "정확히 채우기"에서 도달 불가를 0으로 둔다**

```python
# ❌ 틀린 코드
# 용량을 정확히 W로 채웠을 때의 최대 가치
dp = [0] * (W + 1)                   # 전부 0 = 전부 '도달 가능'
for w, v in items:
    for c in range(W, w - 1, -1):
        dp[c] = max(dp[c], dp[c - w] + v)
print(dp[W])
```

왜: `0`은 "가치 0으로 정확히 채웠다"는 뜻이라, 실제로는 만들 수 없는 용량까지 유효한 출발점이 된다. 그 칸에서 이어진 값이 답으로 뽑혀 "만들 수 없는 조합"의 가치를 출력한다. 도달 가능/불가능은 값이 아니라 **표시**로 구분해야 한다.

```python
# ✅ 고친 코드
NEG = float('-inf')
dp = [NEG] * (W + 1)
dp[0] = 0                            # 오직 용량 0만 진짜 출발점
for w, v in items:
    for c in range(W, w - 1, -1):
        if dp[c - w] != NEG:         # 도달 가능한 칸에서만 잇는다
            dp[c] = max(dp[c], dp[c - w] + v)
print(dp[W] if dp[W] != NEG else -1)
```

**6) 뺄셈이 섞인 모듈러에서 음수를 그대로 둔다**

```python
# ❌ 틀린 코드
# "전체 - 금지된 경우"를 세는 계산
dp[i] = (total[i] - bad[i]) % MOD
print(dp[n])                         # 다른 값과 더할 때 음수가 섞인다
```

왜: `total[i]`와 `bad[i]`가 이미 `% MOD` 된 값이면 뺄셈 결과가 음수일 수 있다. 파이썬의 `%`는 항상 양수를 돌려주므로 이 한 줄만 보면 안전하지만, 뺀 값을 `% MOD` 없이 다른 계산에 넘기거나 최종 출력 전에 한 번 더 정규화하지 않으면 표에 음수가 남아 이후 비교·출력이 어긋난다.

```python
# ✅ 고친 코드
dp[i] = (total[i] - bad[i] + MOD) % MOD    # 먼저 MOD를 더해 양수로 만든다
```

**7) 역순 루프의 끝 값을 하나 놓친다**

```python
# ❌ 틀린 코드
for c in range(W, w, -1):            # w 에서 멈춘다 = dp[w]를 갱신 못 함
    dp[c] = max(dp[c], dp[c - w] + v)
```

왜: `range(W, w, -1)`은 `w + 1`까지만 돈다. 용량이 정확히 `w`인 칸, 즉 그 아이템 하나만 담는 경우가 통째로 빠진다. 아이템이 여러 개면 다른 경로로 덮여 답이 맞아 보이다가, 아이템이 하나뿐인 작은 입력에서만 틀린다.

```python
# ✅ 고친 코드
for c in range(W, w - 1, -1):        # w 까지 포함하려면 끝값은 w - 1
    dp[c] = max(dp[c], dp[c - w] + v)
```

**다음 챕터로**

- Ch5는 "상태가 무엇인지 이미 정해진" 문제들이었다. `dp[i]`, `dp[r][c]`, `dp[c]` 모두 지문이 축을 알려 준다.
- Ch6은 그 축을 **스스로 찾아야 하는** 문제로 넘어간다. "i까지 봤다"만으로는 다음 결정을 못 내릴 때 무엇을 상태로 승격할지, 그 감각이 다음 챕터의 전부다. 여기서 본 유형 3(조건부 전진)의 `dp[i][s]`가 그 출발점이다.
