## L6. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

백트래킹은 "모든 경우를 만든다"가 아니라 **"부분 선택을 하나 늘렸다가, 돌아올 때 원래대로
되돌린다"**는 한 문장이다. 이 챕터의 네 유형은 전부 같은 재귀 골격 위에 있고, 다른 것은
단 두 가지 — **후보를 어떻게 나열하는가**와 **어떤 상태를 되돌려야 하는가**뿐이다.

**개념 지도**

```text
                     rec(depth, state)
                     |  base : depth == N  -> record answer
                     |  loop : for each candidate
                     |    choose -> rec(depth+1) -> undo
                     v
   +-----------------+------------------+------------------+
   |                 |                  |                  |
  L1 repeated       L2 + pruning       L3 combination     L4 permutation
  for c in range(K) same loop, but     for i in           for i in range(N)
  no restriction    'if bad: continue' range(start, N)    'if used[i]: skip'
  K^N cases         cuts K^(N-d) at    rec(i+1, cnt+1)    used[i]=True ... False
                    one stroke         C(N,M) cases       P(N,M) cases
```

가장 왼쪽 L1이 뼈대이고, 오른쪽으로 갈수록 "무엇을 금지하는가"가 하나씩 붙는다.
L2는 값에 조건을 걸고, L3은 인덱스에 순서를 강제하고, L4는 사용 여부를 기억한다.

```text
 which template?
   same value may repeat, order matters   -> L1  K^N
   ... plus a rule that forbids some picks -> L2  prune before recursing
   order does NOT matter, no repeats       -> L3  start index, C(N,M)
   order matters, no repeats               -> L4  used[], P(N,M)
   pick or skip each element               -> subset, 2^N
```

**뼈대 코드**

(1) 중복 순열 — K개 중 하나를 N번 (L1)

```python
K, N = 3, 2
picked = [0] * N
res = []

def rec(depth):
    if depth == N:
        res.append(picked[:])          # 반드시 복사본
        return
    for c in range(K):                 # ← 문제마다 바뀜(후보 집합)
        picked[depth] = c
        rec(depth + 1)
        # 인덱스 덮어쓰기 방식이라 별도 복원이 필요 없다
rec(0)
```

(2) 조합 nCr — 순서 없이 M개 (L3)

```python
arr = [1, 2, 3, 4]
N, M = len(arr), 2
chosen, res = [], []

def rec(start, cnt):
    if cnt == M:
        res.append(chosen[:])
        return
    if N - start < M - cnt:            # 개수 가지치기: 남은 원소로 못 채움
        return
    for i in range(start, N):          # start 부터 → 인덱스 증가만 허용
        chosen.append(arr[i])
        rec(i + 1, cnt + 1)            # i+1: 자기 다음 원소부터
        chosen.pop()                   # 복원
rec(0, 0)
```

(3) 순열 — 방문 배열로 사용한 원소를 기억 (L4)

```python
arr = [1, 2, 3]
N, M = len(arr), 3
used = [False] * N
perm = [0] * M
res = []

def rec(depth):
    if depth == M:
        res.append(perm[:])
        return
    for i in range(N):
        if used[i]:
            continue
        used[i] = True                 # 켜기
        perm[depth] = arr[i]
        rec(depth + 1)
        used[i] = False                # 되돌리기(핵심)
rec(0)
```

(4) 부분집합 — 각 원소를 고르거나 건너뛰거나

```python
arr = [1, 2, 3]
N = len(arr)
cur, res = [], []

def rec(idx):
    if idx == N:
        res.append(cur[:])             # 2^N 개
        return
    rec(idx + 1)                       # idx번째를 건너뛴다
    cur.append(arr[idx])               # idx번째를 고른다
    rec(idx + 1)
    cur.pop()                          # 복원
rec(0)
```

(5) 격자 경로 탐색 — 방문 표시를 켜고 되돌리는 위치가 핵심

```python
DR = [-1, 1, 0, 0]
DC = [0, 0, -1, 1]

def dfs(r, c, depth, g, R, C, visited):
    if depth == LIMIT:                 # ← 문제마다 바뀜(길이/목적지/조건)
        record(r, c)
        return
    for d in range(4):
        nr, nc = r + DR[d], c + DC[d]
        if not (0 <= nr < R and 0 <= nc < C):
            continue
        if visited[nr][nc]:
            continue
        if g[nr][nc] == BLOCK:         # ← 문제마다 바뀜(통과 조건)
            continue
        visited[nr][nc] = True         # 내려가기 직전에 켠다
        dfs(nr, nc, depth + 1, g, R, C, visited)
        visited[nr][nc] = False        # 올라오면서 끈다
```

시작 칸은 재귀 진입 전에 `visited[sr][sc] = True`로 켜 두어야 한다. 루프 안에서만
켜면 출발점이 표시되지 않아 자기 자리로 되돌아가는 경로가 생긴다.

(6) 가지치기(bound)를 넣는 자리 — 최적화 문제의 표준 위치

```python
best = [10 ** 18]

def rec(depth, cur_cost, cur_sum):
    if cur_cost >= best[0]:            # (a) 진입하자마자: 이미 최선보다 나쁨
        return
    if depth == N:
        best[0] = min(best[0], cur_cost)
        return
    if cur_sum + remain_max(depth) < TARGET:   # (b) 남은 걸 다 써도 목표 미달
        return
    for c in candidates(depth):        # ← 문제마다 바뀜
        if not ok(c, depth):           # (c) 후보 단위 필터
            continue
        rec(depth + 1, cur_cost + cost(c), cur_sum + c)
```

`(a)`는 경로 단위 컷, `(c)`는 후보 단위 필터다. 둘 다 **재귀로 내려가기 전**에 있어야
이득이 있다. 종료 조건 뒤에 두면 이미 그 가지를 다 만든 뒤라 아무것도 아끼지 못한다.

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 같은 값을 여러 번 골라도 되고 순서가 다르면 다른 경우 | 중복 순열 틀 (L1) | 제약이 없어 각 칸이 독립적으로 K갈래 | O(K^N) |
| "직전과 같으면 안 된다 / 합이 S 이하" 같은 단서가 붙음 | 가지치기 틀 (L2) | 위반 가지를 진입 전에 잘라낸다 | 최악 O(K^N), 실측은 훨씬 적음 |
| "N개 중 M개를 뽑는다", 순서 무관 | 조합 틀 `start` (L3) | 인덱스 증가만 허용해 중복 대표를 제거 | O(C(N,M)·M) |
| "각 원소를 넣거나 뺀다", 부분집합 전체 | 이분 재귀 (pick/skip) | 원소마다 두 갈래가 곧 2^N | O(2^N·N) |
| "줄을 세운다 / 방문 순서 / 이어붙인 수" | 순열 틀 `used[]` (L4) | 순서가 결과를 바꾸고 재사용은 금지 | O(P(N,M)·M) |
| 격자 위를 이동하며 경로를 만든다 | DFS + `visited` 켜고 끄기 | 같은 칸을 한 경로에서 두 번 밟지 않게 | O(4^L) |
| 최소/최대를 찾는 최적화 | bound 가지치기 추가 | 이미 최선보다 나쁜 가지는 볼 필요가 없다 | 최악은 같지만 실측 급감 |
| N ≥ 20이고 상태가 "어떤 것들을 썼는가"뿐 | 비트마스크 + 메모이제이션 | 같은 집합이 여러 순서로 반복 계산됨 | O(2^N·N) |
| 나열이 아니라 개수만 필요 | 점화식/DP로 전환 | 경우를 만들 필요 자체가 없다 | 문제마다 다름 |
| 중복 원소가 있는데 같은 결과를 한 번만 | 정렬 후 "앞 형제 미사용이면 skip" | 같은 값의 형제 중 하나만 대표로 | 중복 제거된 개수 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 백트래킹의 세 단계(선택 → 재귀 → 되돌리기)가 각각 무엇을 하는지, 그리고 왜 세 번째가 이름값인지.
- [ ] 설명할 수 있다: `depth`가 "지금까지 몇 칸을 채웠는가"라는 뜻이고, 종료 조건이 왜 `depth == N`인지.
- [ ] 설명할 수 있다: 중복 순열의 경우의 수가 K^N인 이유를 곱의 법칙으로.
- [ ] 설명할 수 있다: 백트래킹의 시간복잡도를 "가지 수^깊이 × 한 경우 처리 비용"으로 어림하는 방법.
- [ ] 설명할 수 있다: 깊이 d에서 가지 하나를 자르면 정확히 몇 개의 잎이 사라지는지.
- [ ] 설명할 수 있다: 가지치기가 최악 복잡도는 못 낮추는데도 실전에서 통과를 만드는 이유.
- [ ] 설명할 수 있다: 조합에서 `start`를 넘기면 왜 `{1,3}`과 `{3,1}`의 중복이 사라지는지.
- [ ] 설명할 수 있다: 조합의 다음 재귀가 `rec(i+1)`이어야 하고 `rec(start+1)`이면 안 되는 이유.
- [ ] 설명할 수 있다: 순열이 `start` 대신 `used[]`를 쓰는 이유, 즉 "인덱스 순서 제약"과 "재사용 금지"의 차이.
- [ ] 설명할 수 있다: `used[i] = False`를 빠뜨리면 결과 개수가 어떻게 줄어드는지 작은 예로.
- [ ] 설명할 수 있다: `res.append(path)`와 `res.append(path[:])`의 차이가 왜 "나중에 답이 전부 같아지는" 현상을 만드는지.
- [ ] 설명할 수 있다: 인덱스 덮어쓰기 방식(`picked[depth] = c`)에서는 왜 명시적 복원이 필요 없는지.
- [ ] 설명할 수 있다: 격자 DFS에서 `visited`를 켜고 끄는 위치가 BFS의 방문 표시와 어떻게 다른지.
- [ ] 설명할 수 있다: N!과 2^N과 C(N,M)이 각각 N이 얼마쯤에서 감당 못 할 크기가 되는지.

**⚠️ 자주 하는 실수**

(1) 정답 리스트에 참조를 넣어 나중에 전부 바뀐다

```python
# ❌ 틀린 코드
res = []
def rec(depth):
    if depth == N:
        res.append(picked)      # 리스트 '그 자체'를 넣는다
        return
    ...
# 끝나고 보면 res 안의 모든 원소가 똑같다
```

왜: `picked`는 재귀 내내 하나뿐인 리스트다. 참조를 넣으면 `res`의 모든 항목이 같은
객체를 가리키고, 이후 재귀가 그 리스트를 계속 덮어쓴다.

```python
# ✅ 고친 코드
res.append(picked[:])           # 그 시점의 복사본을 넣는다
# 또는 res.append(list(picked)) / res.append(tuple(picked))
```

(2) 되돌리기 누락 — `used[i] = False`를 안 쓴다

```python
# ❌ 틀린 코드
for i in range(N):
    if used[i]:
        continue
    used[i] = True
    perm[depth] = arr[i]
    rec(depth + 1)
    # used[i] = False 가 없다
```

왜: `used`는 "이 경로에서 썼는가"라는 경로 지역 정보인데, 끄지 않으면 전역 정보가
된다. N=3이면 `[1,2,3]` 하나만 나오고 나머지 5개 순열은 후보가 모두 소진돼 사라진다.

```python
# ✅ 고친 코드
    used[i] = True
    perm[depth] = arr[i]
    rec(depth + 1)
    used[i] = False             # 위로 올라오면서 반드시 되돌린다
```

(3) 조합에서 `rec(start + 1)`로 내려간다

```python
# ❌ 틀린 코드
for i in range(start, N):
    chosen.append(arr[i])
    rec(start + 1, cnt + 1)     # i 가 아니라 start
    chosen.pop()
```

왜: 다음 단계의 시작 위치가 `i`와 무관해져 같은 원소를 다시 고를 수 있고, 오름차순
보장이 깨져 `{1,3}`과 `{3,1}`이 둘 다 나온다.

```python
# ✅ 고친 코드
for i in range(start, N):
    chosen.append(arr[i])
    rec(i + 1, cnt + 1)         # 방금 고른 i의 '다음'부터
    chosen.pop()
```

(4) `pop()` 복원 누락 — 경로가 계속 길어진다

```python
# ❌ 틀린 코드
for i in range(start, N):
    chosen.append(arr[i])
    rec(i + 1, cnt + 1)
    # chosen.pop() 없음
```

왜: 형제 가지로 넘어갈 때 앞 가지에서 넣은 원소가 그대로 남아 `cnt`와 `len(chosen)`이
어긋난다. 결과 길이가 M을 넘거나 IndexError가 난다.

```python
# ✅ 고친 코드
for i in range(start, N):
    chosen.append(arr[i])
    rec(i + 1, cnt + 1)
    chosen.pop()                # append와 짝을 맞춘다
```

(5) 가지치기를 종료 조건 뒤에 둔다

```python
# ❌ 틀린 코드
def rec(depth, cur_sum):
    if depth == N:
        if cur_sum == S:
            cnt[0] += 1
        return
    for c in range(1, K + 1):
        rec(depth + 1, cur_sum + c)
        if cur_sum > S:         # 다 내려갔다 온 뒤에 검사
            return
```

왜: 이미 그 가지의 모든 잎을 다 만든 뒤에 자르는 것이라 아낀 게 없다. 가지치기의 이득은
"깊이 d에서 자르면 K^(N-d)개가 한 번에 사라진다"에서 온다.

```python
# ✅ 고친 코드
def rec(depth, cur_sum):
    if cur_sum > S:             # 함수 진입 즉시 컷
        return
    if depth == N:
        if cur_sum == S:
            cnt[0] += 1
        return
    for c in range(1, K + 1):
        rec(depth + 1, cur_sum + c)
```

(6) 격자 DFS에서 방문 표시를 되돌리는 위치가 틀렸다

```python
# ❌ 틀린 코드
def dfs(r, c, depth):
    visited[r][c] = True
    if depth == LIMIT:
        record()
        return                  # 켜 놓은 채로 빠져나간다
    for d in range(4):
        ...
        dfs(nr, nc, depth + 1)
    visited[r][c] = False
```

왜: 종료 지점의 `return`이 `visited[r][c] = False`를 건너뛴다. 그 칸이 켜진 채로 남아
이후의 모든 경로가 그 칸을 피하고, 답이 실제보다 적게 나온다.

```python
# ✅ 고친 코드
def dfs(r, c, depth):
    if depth == LIMIT:
        record()
        return                  # 여기서는 아직 켜지 않았다
    for d in range(4):
        ...
        visited[nr][nc] = True  # 켜기와 끄기를 재귀 호출 양옆에 짝으로
        dfs(nr, nc, depth + 1)
        visited[nr][nc] = False
```

(7) 종료 조건에서 `return`을 빠뜨린다

```python
# ❌ 틀린 코드
def rec(depth):
    if depth == N:
        res.append(picked[:])   # return 이 없다
    for c in range(K):
        picked[depth] = c       # depth == N 이면 IndexError
        rec(depth + 1)
```

왜: 기저 조건에서 멈추지 않으면 `depth`가 N을 넘어 계속 내려가고, 배열 범위를 벗어나거나
재귀가 끝나지 않는다.

```python
# ✅ 고친 코드
def rec(depth):
    if depth == N:
        res.append(picked[:])
        return                  # 반드시 멈춘다
    for c in range(K):
        picked[depth] = c
        rec(depth + 1)
```

(8) 재귀 깊이 한계를 잊는다

```python
# ❌ 틀린 코드
def dfs(x):
    if x == 0:
        return 0
    return 1 + dfs(x - 1)
print(dfs(5000))                # RecursionError: maximum recursion depth exceeded
```

왜: 파이썬 기본 재귀 한도는 1000 근처다. 깊이가 그보다 깊어지는 경로 탐색은 예외로
끝난다. 백트래킹의 깊이는 보통 N이니, N이 큰 문제에서 특히 위험하다.

```python
# ✅ 고친 코드
import sys
sys.setrecursionlimit(10 ** 6)  # 깊이 상한을 올린다
def dfs(x):
    if x == 0:
        return 0
    return 1 + dfs(x - 1)
print(dfs(5000))
# 깊이가 수만을 넘으면 재귀 대신 스택 자료구조로 바꾸는 것이 안전하다
```

**다음 챕터로**

이 챕터의 "선택 → 재귀 → 되돌리기"는 그대로 격자 위 경로 탐색(DFS)과 이어진다.
또 가지치기에서 "이미 계산한 상태를 또 계산하고 있다"는 낭비가 보이기 시작하면,
그 다음 단계가 메모이제이션과 동적 계획법이다. 순열 전수 나열이 막히는 지점
(N이 10을 넘는 순간)이 곧 비트마스크 DP로 넘어가라는 신호다.
