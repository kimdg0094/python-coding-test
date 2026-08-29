## L6. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터의 네 도구는 전부 같은 질문에 대한 서로 다른 대답이다. **"지금까지 무엇을 썼는지"를 기억하려면 상태가 `2^n`으로 폭발한다 — 그것을 어떻게 줄일 것인가.** 정렬로 단조성을 얻어 기억할 필요를 없애면 Bitonic, 답이 경계 하나에서 갈라지면 구간 DP, 집합을 끝내 기억해야 하면 비트마스크, 집합이 아니라 합만 중요하면 값 DP다. 그래서 유형 선택의 첫 단서는 언제나 **입력 크기**다.

**개념 지도**

```text
  Ch05 map : shrink the state until the table fits

  a DP whose naive state is "which ones did I already use ?"
   |
   +-- sorting gives monotonicity      ->  Bitonic
   |     x-sorted, both chains only move right
   |     the visited set is forced to be {0..j} -> two ends suffice
   |     dp[i][j] , O(n^2) instead of O(2^n)
   |
   +-- the answer splits at a boundary ->  interval DP
   |     dp[i][j] = best over k of dp[i][k] + dp[k+1][j] + cost(i,j)
   |     fill by span length, shortest first , O(n^3)
   |
   +-- the set itself must be kept     ->  bitmask
   |     element i is in the set  <->  bit i is 1
   |     one integer = one subset , 2^n of them
   |     |
   |     +-- order does not matter   dp[mask]       O(2^n * n)
   |     +-- "where am I now"        dp[mask][u]    O(2^n * n^2)
   |     +-- split into two groups   subset walk    O(3^n)
   |
   +-- only the total value matters    ->  DP over values
         dp[w] = can we reach sum w , O(n * S) , fine even at n = 1e5
```

지문보다 먼저 **제한**을 읽는다. n의 상한이 유형을 거의 다 정해 준다.

```text
  read the bound on n first, then pick the shape

  n <= 16     2^n * n^2   bitmask DP with a position    ~1.7e7
  n <= 16     3^n         every subset of every mask    ~4.3e7
  n <= 20     2^n * n     one pass over all subsets     ~2.1e7
  n <= 300    n^3         interval DP                   ~2.7e7
  n <= 500    n^3         interval DP, already tight    ~1.2e8
  n <= 5000   n^2         two-way LIS by plain DP       ~2.5e7
  n <= 1e5    n log n     two-way LIS by bisect         ~1.7e6
  S <= 1e5    n * S       subset sum over values
  # n = 1e5 with a "choose a subset" story is never bitmask
  # n = 15 with a vague statement is almost always bitmask
```

네 유형이 공유하는 진짜 뼈대는 점화식이 아니라 **채우는 순서**다.

```text
  every DP here fills cells in an order where the sources are done

  bitonic     frontier j ascending    dp[i][j] reads dp[*][j-1]
  interval    span length ascending   dp[i][j] reads shorter spans only
  bitmask     mask value ascending    dp[m | b] is written from dp[m]
  subset sum  weight descending       keeps each item usable only once
  # break the order and you read a cell that still holds its init value
```

**뼈대 코드**

1) 비트 연산 관용구 — 집합 하나가 정수 하나

```python
if (mask >> i) & 1:                  # 원소 i 포함 여부 (괄호는 가독성용)
    ...
mask | (1 << i)                      # 원소 i 추가
mask & ~(1 << i)                     # 원소 i 제거
mask ^ (1 << i)                      # 원소 i 토글
mask & (mask - 1)                    # 최하위 1비트 하나 끄기
low = mask & (-mask)                 # 최하위 1비트만 남기기
idx = low.bit_length() - 1           # 그 비트가 가리키는 원소 번호
bin(mask).count("1")                 # 켜진 비트 수 (3.10+ 는 mask.bit_count())
FULL = (1 << n) - 1                  # 전체 집합 = 비트 n개가 전부 1
rest = FULL ^ mask                   # 여집합
if mask & other == 0:                # 서로소인가 — & 가 == 보다 먼저 묶인다
    ...

for mask in range(1 << n):           # 모든 마스크. 끝값은 1 << n 이다
    ...                              # ← 마스크마다 할 일은 문제마다 바뀜

sub = mask                           # mask의 모든 부분집합을 한 번씩
while True:
    ...                              # ← sub 를 쓰는 자리 (빈 집합도 여기 들어온다)
    if sub == 0:
        break                        # 검사·탈출이 갱신보다 뒤에 와야 한다
    sub = (sub - 1) & mask
```

2) 비트마스크 DP — TSP형 `dp[mask][i]`와 배정형 `dp[mask]`

```python
INF = 10 ** 18
FULL = (1 << n) - 1
dp = [[INF] * n for _ in range(1 << n)]      # 행 수는 1 << n (마스크 개수)
dp[1][0] = 0                                 # 초기 상태 — 이 한 줄이 빠지면 전부 INF
for mask in range(1 << n):                   # 오름차순 순회가 그대로 위상 순서
    row = dp[mask]
    for u in range(n):
        cur = row[u]
        if cur == INF or not (mask >> u) & 1:
            continue                         # 도달 못 했거나 u에 있을 수 없는 상태
        for v in range(n):
            if (mask >> v) & 1:              # 이미 방문한 곳으로는 안 간다
                continue
            nm = mask | (1 << v)
            if cur + dist[u][v] < dp[nm][v]:
                dp[nm][v] = cur + dist[u][v]
ans = min(dp[FULL][u] + dist[u][0] for u in range(1, n))   # ← 복귀가 없으면 min(dp[FULL])

# 배정형: '지금 몇 번째 사람 차례인가'가 popcount로 정해져 1차원이면 충분
dp = [INF] * (1 << n)
dp[0] = 0
for mask in range(1 << n):
    if dp[mask] == INF:
        continue
    i = bin(mask).count("1")                 # 이미 배정된 수 = 지금 배정할 사람
    if i == n:
        continue
    for j in range(n):
        if not (mask >> j) & 1:
            nm = mask | (1 << j)
            if dp[mask] + cost[i][j] < dp[nm]:
                dp[nm] = dp[mask] + cost[i][j]   # ← 비용표는 문제마다 바뀜
ans = dp[FULL]
```

3) 구간 DP — 바깥 루프는 반드시 구간 길이

```python
INF = 10 ** 18
pre = [0] * (n + 1)
for i in range(n):
    pre[i + 1] = pre[i] + a[i]               # 구간 합을 O(1)로

dp = [[0] * n for _ in range(n)]             # 길이 1 구간은 0 — base case
for length in range(2, n + 1):               # 짧은 구간부터 바깥으로
    for i in range(0, n - length + 1):
        j = i + length - 1
        cost = pre[j + 1] - pre[i]           # ← 합칠 때 드는 비용은 문제마다 바뀜
        best = INF
        for k in range(i, j):                # 마지막에 합쳐지는 경계 k
            v = dp[i][k] + dp[k + 1][j]      # 둘 다 길이가 더 짧아 이미 완성됨
            if v < best:
                best = v
        dp[i][j] = best + cost
ans = dp[0][n - 1]

# 변형: 분할점 없이 '양끝만 비교'하는 형태(회문 계열)는 안쪽 칸 하나만 읽는다
for length in range(2, n + 1):
    for i in range(0, n - length + 1):
        j = i + length - 1
        if s[i] == s[j]:
            dp[i][j] = dp[i + 1][j - 1]                    # ← 양끝이 같으면 그대로
        else:
            dp[i][j] = min(dp[i + 1][j], dp[i][j - 1]) + 1
```

4) Bitonic — 양방향 LIS를 따로 채워 꼭대기에서 붙인다

```python
inc = [1] * n                                # i에서 '끝나는' 증가 최대 길이
for i in range(n):
    for j in range(i):                       # 왼쪽 -> 오른쪽
        if a[j] < a[i] and inc[j] + 1 > inc[i]:
            inc[i] = inc[j] + 1

dec = [1] * n                                # i에서 '시작하는' 감소 최대 길이
for i in range(n - 1, -1, -1):               # 반드시 오른쪽 끝부터
    for j in range(i + 1, n):
        if a[j] < a[i] and dec[j] + 1 > dec[i]:
            dec[i] = dec[j] + 1

ans = max(inc[i] + dec[i] - 1 for i in range(n))   # 꼭대기가 두 번 세어지므로 -1
# ← 길이가 아니라 '합'을 최대화하는 문제면 초기값을 a[i]로 두고 마지막에 - a[i]
# ← 양쪽이 모두 비어 있으면 안 되는 문제면 inc[i] > 1 and dec[i] > 1 조건을 추가
```

5) 부분집합 합 — 마스크별 합과 값 기반 DP

```python
# (A) 모든 마스크의 원소 합을 O(2^n)에. 마스크마다 다시 더하면 O(2^n * n)이 된다
ssum = [0] * (1 << n)
for mask in range(1, 1 << n):
    low = mask & (-mask)                     # 최하위 원소 하나를 떼어내고
    ssum[mask] = ssum[mask ^ low] + a[low.bit_length() - 1]   # 나머지는 이미 계산됨

# (B) n이 커도 값의 합이 작으면 '집합'이 아니라 '값'을 상태로 잡는다
S = sum(a)
dp = [False] * (S + 1)                       # dp[w] = 합이 정확히 w인 부분집합이 있나
dp[0] = True
for x in a:                                  # ← 원소를 한 번씩만 쓰려면
    for w in range(S, x - 1, -1):            #    반드시 내림차순 (오름차순이면 중복 사용)
        if dp[w - x]:
            dp[w] = True
best = min(abs(S - 2 * w) for w in range(S + 1) if dp[w])   # ← 목적식은 문제마다 바뀜
```

**언제 무엇을 쓰나**

| 지문 신호 | 상태 정의 | 복잡도 | n 상한 |
| --- | --- | --- | --- |
| "왼쪽 끝에서 오른쪽 끝까지 갔다가 되돌아온다", 좌표로 정렬하면 단조 | `dp[i][j]` = 두 체인의 끝점이 i, j | O(n²) | n ≤ 2,000 |
| "증가하다가 감소하는" 산 모양 부분수열 | `inc[i]`, `dec[i]` 두 배열을 따로 | O(n²) | n ≤ 5,000 |
| 같은 산 모양인데 n이 10만 | `inc`, `dec`를 이분 탐색 LIS로 | O(n log n) | n ≤ 10⁵ |
| "인접한 두 더미를 합친다", "괄호를 어디에 치나" | `dp[i][j]` = 구간을 하나로 만드는 최적값 | O(n³) | n ≤ 300~500 |
| "양끝을 동시에 본다"(회문 삽입·분할) | `dp[i][j]`, 분할점 없이 안쪽 한 칸 | O(n²) | n ≤ 3,000 |
| "마지막에 터뜨리는/제거하는 것 하나를 고른다" | `dp[i][j]` + 분할점 k | O(n³) | n ≤ 300 |
| "N개를 켜고 끄는 모든 경우를 본다" | 마스크 정수 하나 | O(2ⁿ × n) | n ≤ 20~22 |
| "모든 도시를 한 번씩, 어디서 왔는지가 비용을 바꾼다" | `dp[mask][u]` | O(2ⁿ × n²) | n ≤ 16 |
| "사람 i를 자리 j에 배정", 순서는 비용과 무관 | `dp[mask]`, 사람 번호 = `popcount(mask)` | O(2ⁿ × n) | n ≤ 20 |
| "집합을 그룹 k개로 쪼갠다" | `dp[mask]` + 부분집합 순회 | O(3ⁿ) | n ≤ 16 |
| 마스크마다 원소 합·유효성이 필요 | `ssum[mask] = ssum[mask^low] + a[idx]` | O(2ⁿ) | n ≤ 22 |
| "부분집합의 합이 목표에 닿나", n은 큰데 값이 작다 | `dp[w]` — 집합이 아니라 값이 상태 | O(n × S) | n ≤ 10⁵ |
| 격자 위 "지점 k곳을 다 들르는 최단 이동" | BFS 거리표 + `dp[mask][i]` | O(격자 + 2ᵏ × k²) | k ≤ 12 |
| 원소가 20개를 훌쩍 넘는데 "부분집합" 이야기 | 비트마스크가 아니다 — 정렬·그리디·값 DP를 다시 본다 | — | — |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: n의 상한만 보고 비트마스크·구간 DP·양방향 LIS 중 무엇인지 좁히는 근거를.
- [ ] 설명할 수 있다: 비트마스크의 한계가 왜 대략 `n ≤ 20`인지를 `2ⁿ × n` 계산으로.
- [ ] 설명할 수 있다: 구간 DP가 왜 `n ≤ 300~500`에서 막히는지를 `n³` 계산으로.
- [ ] 설명할 수 있다: 왜 구간 DP의 바깥 루프가 반드시 "구간 길이"여야 하는지.
- [ ] 설명할 수 있다: 구간 DP의 base case(길이 1)가 왜 0 또는 참인지.
- [ ] 설명할 수 있다: 비트마스크 DP에서 마스크를 오름차순으로 도는 것이 왜 위상 정렬과 같은지.
- [ ] 설명할 수 있다: `dp[mask][u]`에서 왜 지나온 순서를 통째로 기억하지 않아도 되는지.
- [ ] 설명할 수 있다: 배정형이 왜 `dp[mask]` 1차원으로 줄어들고 TSP는 왜 안 줄어드는지.
- [ ] 설명할 수 있다: `sub = (sub - 1) & mask`가 왜 모든 부분집합을 정확히 한 번씩 도는지.
- [ ] 설명할 수 있다: "모든 마스크의 모든 부분집합"이 왜 `2ⁿ`도 `4ⁿ`도 아닌 `3ⁿ`인지.
- [ ] 설명할 수 있다: `mask & (mask - 1)`과 `mask & (-mask)`가 각각 무엇을 남기는지, 비트로.
- [ ] 설명할 수 있다: Bitonic에서 상태가 왜 "두 끝점"만으로 충분한지(방문 집합이 자동으로 결정되는 이유).
- [ ] 설명할 수 있다: 양방향 LIS를 합칠 때 왜 꼭대기 값을 한 번 빼야 하는지.
- [ ] 설명할 수 있다: `dec` 배열을 왜 오른쪽 끝부터 채워야 하는지.
- [ ] 설명할 수 있다: 0/1 부분집합 합 DP에서 무게 루프를 왜 내림차순으로 도는지.
- [ ] 설명할 수 있다: 같은 "부분집합 고르기" 문제를 마스크로 풀지 값으로 풀지 무엇을 보고 정하는지.

**⚠️ 자주 하는 실수**

**1) 비트 연산과 산술의 우선순위를 착각한다**

```python
# ❌ 틀린 코드
FULL = 1 << n - 1                # '전체 집합'을 만들 생각이었다
for mask in range(1 << n - 1):   # '모든 마스크'를 돌 생각이었다
    ...
if mask & 1 + 1:                 # '0번 비트와 1을 AND' 할 생각이었다
    ...
```

왜: 파이썬에서 `+`, `-`는 `<<`, `>>`보다 **먼저** 묶이고, `<<`는 `&`보다 먼저 묶인다. 그래서 `1 << n - 1`은 `(1 << n) - 1`이 아니라 `1 << (n-1)`이다. `n = 4`면 15가 아니라 8이 나오고, `range(8)`은 마스크 16개 중 절반만 돈다. `mask & 1 + 1`도 `(mask & 1) + 1`이 아니라 `mask & 2`다. 절반만 도는 루프는 예외를 내지 않고 그냥 답이 작게 나오므로 발견이 가장 늦다.

한편 흔히 반대로 알려진 `mask & 1 == 0`은 파이썬에서 `(mask & 1) == 0`으로 **의도대로** 묶인다(비교가 `&`보다 우선순위가 낮다). 진짜 위험한 것은 비교가 아니라 위의 산술 쪽이다.

```python
# ✅ 고친 코드
FULL = (1 << n) - 1              # 괄호로 "먼저 2^n, 그다음 -1"을 못 박는다
for mask in range(1 << n):       # 마스크 개수는 2^n, 끝값은 1 << n
    ...
if mask & (1 + 1):               # 의도가 무엇이든 괄호로 적어 둔다
    ...
# 규칙: 시프트와 산술이 한 줄에 같이 나오면 무조건 괄호를 친다
```

**2) 구간 DP를 왼쪽 인덱스 오름차순으로 돈다**

```python
# ❌ 틀린 코드
for i in range(n):               # i 오름차순
    for j in range(i + 1, n):
        for k in range(i, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + cost(i, j))
```

왜: `dp[i][j]`는 `dp[k+1][j]`를 읽는데 `k+1 > i`라 **행 번호가 더 큰 칸**이다. `i` 오름차순이면 그 행은 아직 손도 대지 않은 초기값(0이나 INF)이다. INF로 초기화했다면 답이 INF로 남아 눈에 띄지만, 0으로 초기화했다면 비용을 빼먹은 채 조용히 작은 값이 나온다. 길이 2, 3짜리 작은 예제는 우연히 맞아 통과하기도 한다.

```python
# ✅ 고친 코드
for length in range(2, n + 1):   # 짧은 구간부터 = 읽는 칸이 항상 먼저 완성됨
    for i in range(0, n - length + 1):
        j = i + length - 1
        for k in range(i, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + cost(i, j))
# i를 내림차순(for i in range(n-1, -1, -1))으로 돌아도 같은 순서가 만들어진다
```

**3) 비트마스크 DP의 초기 상태를 빼먹는다**

```python
# ❌ 틀린 코드
dp = [[INF] * n for _ in range(1 << n)]
for mask in range(1 << n):       # dp[1][0] = 0 을 안 썼다
    for u in range(n):
        if dp[mask][u] == INF:
            continue
        ...
print(min(dp[FULL]))             # INF 출력
```

왜: 전이는 "이미 값이 있는 칸에서 다음 칸으로" 퍼뜨리는 구조라, 시작점이 하나도 없으면 아무 칸도 채워지지 않는다. 표 전체가 INF인 채 끝나고 답도 INF다. 반대로 `dp = [[0] * n ...]`으로 초기화하면 도달 불가능한 상태가 전부 "비용 0"으로 보여 답이 0으로 나온다. **두 증상 모두 "점화식이 틀렸나"를 먼저 의심하게 만들어 시간을 잡아먹는다.**

```python
# ✅ 고친 코드
dp = [[INF] * n for _ in range(1 << n)]
dp[1][0] = 0                     # 0만 방문했고 0에 있음, 비용 0
# 배정형이면 dp = [INF] * (1 << n) 에 dp[0] = 0
# 도달 가능성을 INF로 구분하므로 초기값은 반드시 INF, 시작 칸만 0
```

**4) 전체 마스크 `(1 << n) - 1`과 순회 끝값 `1 << n`을 뒤바꾼다**

```python
# ❌ 틀린 코드
FULL = 1 << n                    # 전체 집합이라고 쓴 값
for mask in range((1 << n) - 1): # 모든 마스크라고 쓴 루프
    ...
print(dp[FULL])                  # IndexError, 또는 엉뚱한 칸
```

왜: 원소가 `n`개면 마스크는 `0`부터 `2^n - 1`까지 `2^n`개다. 그래서 **전체 집합**은 비트가 전부 1인 `(1 << n) - 1`이고, **순회 끝값**은 그보다 하나 큰 `1 << n`이다. 두 값을 맞바꾸면 배열 밖을 읽거나(`dp[1 << n]`), 마지막 마스크 하나를 빠뜨린다. 빠지는 그 하나가 하필 "전부 방문한" 상태, 즉 정답이 사는 칸이다.

```python
# ✅ 고친 코드
FULL = (1 << n) - 1              # 비트가 전부 1 = 전체 집합
dp = [INF] * (1 << n)            # 길이는 마스크 개수 = 2^n
for mask in range(1 << n):       # 0 .. 2^n - 1 을 전부 돈다
    ...
print(dp[FULL])
```

**5) 부분집합 순회에서 빈 집합을 빠뜨린다**

```python
# ❌ 틀린 코드
sub = mask
while sub:                       # sub == 0 이면 들어가지도 않는다
    dp[mask] = min(dp[mask], cost[sub] + dp[mask ^ sub])
    sub = (sub - 1) & mask
```

왜: `while sub:`는 `sub`가 0이 되는 순간 본문을 건너뛰고 끝난다. "한 그룹을 통째로 비우는" 분할이 후보에서 빠지는데, 그것이 유효한 선택인 문제에서는 답이 어긋난다. 반대로 빈 집합을 넣으면 `mask ^ sub`가 `mask` 자신이 되어 `dp[mask]`가 자기 값을 읽는 순환 참조가 생긴다 — 대개는 값이 그대로라 무해하지만 "그룹은 비어 있을 수 없다" 같은 제약이 붙은 문제에서는 잘못된 값이 굳는다. **빈 집합을 넣을지 말지는 문제를 보고 정하고, 그 판단이 코드 형태에 드러나야 한다.**

```python
# ✅ 고친 코드
sub = mask                       # 빈 집합까지 포함해 한 번씩 도는 형태
while True:
    ...                          # sub 를 쓰는 자리
    if sub == 0:
        break                    # 사용 -> 검사 -> 갱신 순서
    sub = (sub - 1) & mask

sub = (mask - 1) & mask          # 진부분집합만 필요할 때(자기 자신 제외)
while sub:
    ...
    sub = (sub - 1) & mask
```

**6) n이 큰데 비트마스크를 적용한다**

```python
# ❌ 틀린 코드
# 제한: 1 <= n <= 100000, 부분집합의 합을 목표 S에 맞춘다
for mask in range(1 << n):       # 2^100000 개의 마스크
    if ssum(mask) == S:
        ...
```

왜: "부분집합"이라는 단어만 보고 마스크를 떠올린 것이다. `n = 100000`이면 마스크가 `2^100000`개라 루프가 끝나지 않는다(파이썬은 정수 크기 제한이 없어 `range(1 << n)` 자체는 에러 없이 만들어져 더 헷갈린다). **`2ⁿ`을 쓸 수 있는 것은 n이 20 안팎일 때뿐이고, 그 이상이면 상태를 집합이 아닌 다른 것으로 잡아야 한다.**

```python
# ✅ 고친 코드
# 합의 상한 S가 작다면 '값'을 상태로 잡는다 -> O(n * S)
dp = [False] * (S + 1)
dp[0] = True
for x in a:
    for w in range(S, x - 1, -1):
        if dp[w - x]:
            dp[w] = True
print(dp[S])
# n <= 20 이면 비트마스크, n이 크고 S가 작으면 값 DP, 둘 다 크면 다른 성질을 찾는다
```

**7) 0/1 부분집합 합 DP의 무게 루프를 오름차순으로 돈다**

```python
# ❌ 틀린 코드
for x in a:
    for w in range(x, S + 1):    # 오름차순
        if dp[w - x]:
            dp[w] = True
```

왜: 오름차순이면 이번 라운드에서 방금 `x`를 써서 True가 된 `dp[w-x]`를 같은 라운드의 더 큰 `w`에서 다시 읽는다. 결과적으로 원소 `x`를 두 번, 세 번 쓴 합까지 True가 되어 "각 원소를 최대 한 번"이라는 조건이 무너진다. `a = [3]`, `S = 6`일 때 `dp[6]`이 True로 나오는지 확인하면 바로 드러난다.

```python
# ✅ 고친 코드
for x in a:
    for w in range(S, x - 1, -1):    # 내림차순 = dp[w-x]는 항상 이전 라운드 값
        if dp[w - x]:
            dp[w] = True
# 원소를 여러 번 써도 되는 문제(무한 개수)라면 그때는 오름차순이 정답이다
```

**8) 양방향 LIS를 합치며 꼭대기를 두 번 센다**

```python
# ❌ 틀린 코드
dec = [1] * n
for i in range(n):               # 왼쪽부터 채운다
    for j in range(i + 1, n):
        if a[j] < a[i]:
            dec[i] = max(dec[i], dec[j] + 1)   # dec[j]가 아직 1이다
ans = max(inc[i] + dec[i] for i in range(n))   # 꼭대기가 두 번 더해진다
```

왜: 두 가지가 동시에 틀렸다. 첫째, `dec[i]`는 오른쪽 값들을 읽으므로 **오른쪽 끝부터** 채워야 하는데 왼쪽부터 돌면 `dec[j]`가 아직 초기값 1이라 감소 구간이 언제나 길이 2로 끊긴다. 둘째, `inc[i]`와 `dec[i]`는 둘 다 자기 자신 `a[i]`를 포함하므로 그냥 더하면 꼭대기가 중복된다. 길이 문제에서는 답이 정확히 1만큼 커져서, 예제 하나로는 오프바이원인지 구조 오류인지 구분이 안 된다.

```python
# ✅ 고친 코드
dec = [1] * n
for i in range(n - 1, -1, -1):   # 오른쪽 끝부터 = 읽는 dec[j]가 이미 완성됨
    for j in range(i + 1, n):
        if a[j] < a[i] and dec[j] + 1 > dec[i]:
            dec[i] = dec[j] + 1
ans = max(inc[i] + dec[i] - 1 for i in range(n))   # 꼭대기 중복 1 제거
# 합을 구하는 문제라면 - 1 대신 - a[i]
```

**다음 챕터로**

- 이 챕터에서 익힌 "상태를 정수 하나로 압축한다"는 감각은 다른 유형에서 **BFS의 방문 표시**로 그대로 넘어간다. 격자 위에서 열쇠 몇 개를 모아야 문을 여는 문제는 `visited[r][c][keymask]`처럼 좌표 뒤에 마스크 한 칸을 붙이는 것으로 끝난다. 상태 설계의 문법이 같다.
- "채우는 순서가 곧 정확성"이라는 이 챕터의 교훈은 앞으로 만나는 모든 DP의 첫 점검 항목이다. 답이 이상하면 점화식보다 **읽는 칸이 이미 완성돼 있는지**를 먼저 확인하는 습관을 들이면 디버깅 시간이 크게 줄어든다.
