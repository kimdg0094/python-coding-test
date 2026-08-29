## L8. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 레슨은 Ch1(시간·공간복잡도) 전체를 하나의 판단 절차로 접는다. 이 챕터의 도구는 결국 **하나의 질문에 답하기 위한 것**이다 — "내가 지금 떠올린 방법이 주어진 입력 크기에서 제한 시간 안에 끝나는가?"

- 그 질문에 답하는 순서는 항상 같다. **수도코드로 설계하고 → 줄별 실행 횟수를 세어 `T(n)`을 만들고 → 지배항만 남겨 Big-O로 줄이고 → 입력 크기와 대조한다.** 아래 지도가 그 흐름 전체다.

**개념 지도**

```text
 how to price an algorithm
 -------------------------------------------------------------
   problem  ->  pseudocode  ->  count  ->  T(n)  ->  O( . )
                    L1           L3        L3        L2
                                  |
                +-----------------+-----------------+
                |                                   |
             LOOPS   (L4)                     RECURSION  (L5)
                |                                   |
      nesting   -> multiply             T(n) = a T(n/b) + f(n)
      sequence  -> add                  unroll , or sum levels
      i += 1    -> n steps              -1 shrink -> depth n
      i *= 2    -> log n steps          /2 shrink -> depth log n
                |                                   |
                +-----------------+-----------------+
                                  |
                        drop constants and
                        keep the top term
                                  |
                +-----------------+-----------------+
             TIME                                SPACE  (L6)
       compare with the limit            extra containers
       ops per second ~ 1e8              + max stack depth
 -------------------------------------------------------------
 one call tree , two prices : nodes = time , height = space
```

- 지도의 마지막 줄이 이 챕터에서 가장 자주 놓치는 지점이다. **같은 재귀 트리를 놓고 시간은 "노드 수"로, 공간은 "높이"로 읽는다.** 나이브 피보나치가 시간 `O(2ⁿ)`인데 공간은 `O(n)`인 이유가 여기 있다.

- 등급 판정이 막히면 **배율 테스트**로 돌아온다. `n`을 2배로 했을 때 비용이 `×1`이면 `O(1)`, `+1`이면 `O(log n)`, `×2`면 `O(n)`, `×2.2`면 `O(n log n)`, `×4`면 `O(n²)`, 제곱이 되면 `O(2ⁿ)`이다.

```text
 max n for a 1-second budget  ( about 1e8 simple ops )
 -------------------------------------------------------------
 n                1e8   1e6   1e5   1e4  2000   100    20    10
 O(1)              ok    ok    ok    ok    ok    ok    ok    ok
 O(log n)          ok    ok    ok    ok    ok    ok    ok    ok
 O(n)              ok    ok    ok    ok    ok    ok    ok    ok
 O(n log n)        --    ok    ok    ok    ok    ok    ok    ok
 O(n^2)            --    --    --    ok    ok    ok    ok    ok
 O(n^3)            --    --    --    --    --    ok    ok    ok
 O(2^n)            --    --    --    --    --    --    ok    ok
 O(n!)             --    --    --    --    --    --    --    ok
 -------------------------------------------------------------
 read it backwards : the given n tells you which line to aim at
```

- 이 표를 **거꾸로 읽는 것**이 실전 사용법이다. 지문에서 `n ≤ 10⁵`를 보면 `O(n²)` 줄이 이미 막혀 있으므로, 설계를 시작하기도 전에 "`O(n log n)` 이하로 짜야 한다"는 목표가 정해진다.

**뼈대 코드**

```python
# 뼈대 1(before) — 리스트 멤버십 : 한 줄처럼 보이지만 O(n)
seen = []
for x in a:                  # n번
    if x not in seen:        # 리스트 스캔 O(n)  ->  전체 O(n^2)
        seen.append(x)
```

```python
# 뼈대 1(after) — 집합으로 바꾸면 검사 한 번이 평균 O(1)
seen = set()
out = []
for x in a:                  # n번
    if x not in seen:        # 해시 조회 평균 O(1)  ->  전체 O(n)
        seen.add(x)
        out.append(x)        # ← 순서 보존이 필요할 때만
```

```python
# 뼈대 2(before) — 문자열 이어붙이기 : 문자열은 불변이라 매번 복사
s = ""
for w in words:              # n번
    s += w                   # 길이만큼 복사 O(len(s))  ->  전체 O(n^2)
```

```python
# 뼈대 2(after) — 조각을 모았다가 마지막에 한 번만 합친다
parts = []
for w in words:              # n번
    parts.append(w)          # 끝에 붙이기 평균 O(1)
s = "".join(parts)           # 한 번에 이어붙이기 O(전체 길이)  ->  O(n)
```

```python
# 뼈대 3(before) — 구간 합을 매번 다시 계산
for lo, hi in queries:       # q개의 질의
    print(sum(a[lo:hi + 1])) # 슬라이싱 복사 + 합 O(n)  ->  전체 O(q*n)
```

```python
# 뼈대 3(after) — 누적합을 한 번 만들어 두고 뺄셈으로 답한다
pre = [0] * (len(a) + 1)
for i, x in enumerate(a):    # 전처리 O(n)
    pre[i + 1] = pre[i] + x  # pre[k] = a[0] + ... + a[k-1]
for lo, hi in queries:
    print(pre[hi + 1] - pre[lo])   # 질의당 O(1)  ->  전체 O(n + q)
```

```python
# 뼈대 4(before) — 리스트 앞에서 빼기 : 뒤 원소를 전부 한 칸씩 민다
queue = [start]
while queue:
    cur = queue.pop(0)       # O(n)  ->  전체 O(n^2)
    queue.append(nxt)        # ← 문제마다 바뀜
```

```python
# 뼈대 4(after) — 양끝 큐를 쓰면 앞에서 빼기도 O(1)
from collections import deque
queue = deque([start])       # deque : 양쪽 끝 삽입·삭제가 O(1)
while queue:
    cur = queue.popleft()    # O(1)  ->  전체 O(n)
    queue.append(nxt)        # ← 문제마다 바뀜
```

```python
# 뼈대 5(before) — 재귀 : 깊이가 n에 비례하면 공간 O(n) + 한도 위험
def rec_sum(a, i=0):
    if i == len(a):
        return 0
    return a[i] + rec_sum(a, i + 1)   # 깊이 n  ->  n이 크면 실행 불가
```

```python
# 뼈대 5(after) — 꼬리가 단순한 재귀는 반복문으로 바꿔 공간 O(1)
def iter_sum(a):
    s = 0
    for x in a:              # 시간은 그대로 O(n)
        s += x
    return s                 # 공간 O(1), 재귀 한도와 무관
```

**언제 무엇을 쓰나**

**(1) 입력 크기 `n`이 알려주는 목표 복잡도** — 지문의 제한을 보고 설계 방향을 먼저 정한다.

| 입력 크기 `n` | 노려야 할 복잡도 | 대표 알고리즘·기법 | 대략 연산 수 |
|---|---|---|---|
| `n ≤ 10` | `O(n!)`, `O(2ⁿ·n)` | 순열 전부 나열, 완전탐색, 비트마스크 | ~10⁷ |
| `n ≤ 20` | `O(2ⁿ)` | 부분집합 전부, 비트마스크 DP | ~10⁶ |
| `n ≤ 100` | `O(n³)` | 3중 반복, 모든 쌍의 최단거리 표 | ~10⁶ |
| `n ≤ 2 000` | `O(n²)` | 2중 반복, 2차원 DP, 모든 쌍 비교 | ~4·10⁶ |
| `n ≤ 10⁵` | `O(n log n)` | 정렬, 이분 탐색, 우선순위 큐, 분할정복 | ~1.7·10⁶ |
| `n ≤ 10⁶` | `O(n)` / `O(n log n)` | 한 번 훑기, 누적합, 투 포인터, 해시 | ~10⁷ |
| `n ≤ 10⁸` | `O(n)` | 단순 순회만(입출력 자체가 병목) | ~10⁸ |
| `n`이 10⁹ 이상 | `O(log n)` / `O(1)` | 이분 탐색, 수식·닫힌 식, 거듭제곱 분할 | ~30 |

- 기준선은 **1초에 대략 10⁸번의 단순 연산**이다. 파이썬은 이보다 느리므로(대략 10⁷ 수준) **한 칸 더 보수적으로** 잡는 것이 안전하다. 즉 `n = 10⁵`에서 `O(n²)`는 애초에 후보가 아니다.
- 반대 방향으로도 쓴다. `n ≤ 20`처럼 유난히 작으면 그것은 **"지수 시간을 써도 된다"는 신호**다. 억지로 다항식 해법을 찾느라 시간을 버릴 필요가 없다.

**(2) 복잡도를 한 칸 낮추는 정석 치환** — 코드에서 바로 갈아 끼우는 판단표다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 반복 안에서 `x in lst` | `set` / `dict`로 교체 | 리스트는 선형 스캔, 해시는 즉시 조회 | `O(n²)` → `O(n)` |
| 반복 안에서 문자열 `+=` | 리스트에 모아 `"".join()` | 문자열은 불변이라 매번 전체 복사 | `O(n²)` → `O(n)` |
| 같은 구간 합을 여러 번 | 누적합 배열 전처리 | 뺄셈 한 번으로 임의 구간 합을 얻음 | `O(qn)` → `O(n+q)` |
| 앞에서 빼는 큐 | `collections.deque` | 리스트의 `pop(0)`는 뒤를 전부 밀어야 함 | `O(n²)` → `O(n)` |
| 재귀에 잘라 넘기기 `a[:m]` | 인덱스 `lo, hi`를 넘김 | 슬라이싱은 새 리스트 복사(시간·공간) | `O(n log n)` → `O(log n)` 공간 |
| 같은 부분문제를 반복 계산 | 메모이제이션·DP | 비용 = 상태 수 × 전이 비용 | `O(2ⁿ)` → `O(n)` |
| 정렬된 배열에서 값 찾기 | 이분 탐색 | 매번 후보가 절반으로 줄어듦 | `O(n)` → `O(log n)` |
| 개수 세기를 `lst.count(x)`로 | `Counter` / `dict` 누적 | `count`는 호출마다 전체를 훑음 | `O(n²)` → `O(n)` |
| 깊이가 `n`인 재귀 | 반복문 또는 명시적 스택 | 스택 한도(약 1000)와 공간 `O(n)`을 피함 | 공간 `O(n)` → `O(1)` |
| 메모리 제한이 병목 | 롤링 배열·제자리 갱신 | 이전 한두 줄만 있으면 되는 DP가 많음 | 공간 `O(n²)` → `O(n)` |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: Big-O의 정의를 `c`와 `n₀`를 써서, 그리고 왜 그 정의가 상수·저차항을 버리게 만드는지를.
- [ ] 설명할 수 있다: 실행 시간(초)이 아니라 연산 횟수를 세는 이유와, 그 모델이 파이썬에서 깨지는 자리들을.
- [ ] 설명할 수 있다: `O`·`Ω`·`Θ`의 차이와, `O(n)`인 코드를 `O(n²)`이라 말해도 거짓은 아니지만 쓸모없는 이유를.
- [ ] 설명할 수 있다: `n`을 2배로 했을 때의 배율만 보고 복잡도 등급을 역산하는 법을.
- [ ] 설명할 수 있다: `1+2+…+n = n(n+1)/2`를 가우스 짝짓기로 유도하고, 왜 그것이 `O(n²)`인지를.
- [ ] 설명할 수 있다: 절반씩 줄이면 `log₂n`번인 이유를 `2^k = n`에서 시작해서.
- [ ] 설명할 수 있다: 중첩 반복이 곱, 순차 반복이 합이 되는 이유를.
- [ ] 설명할 수 있다: 이중 반복인데도 `O(n²)`이 아닌 경우(안쪽이 `log n`번, 또는 조화급수)를 예와 함께.
- [ ] 설명할 수 있다: 점화식을 세우는 세 요소(분기 수·크기 감소·호출 밖 비용)와 반복 대입법으로 푸는 절차를.
- [ ] 설명할 수 있다: 네 가지 대표 점화식의 결과를 유도까지 곁들여서.
- [ ] 설명할 수 있다: 레벨 합이 평평할 때·위로 기울 때·아래로 기울 때 결과가 어떻게 달라지는지를.
- [ ] 설명할 수 있다: 나이브 피보나치가 시간 `O(2ⁿ)`인데 공간은 `O(n)`인 이유를(노드 수 대 높이).
- [ ] 설명할 수 있다: 재귀 호출에서 형제 프레임이 공간에 더해지지 않는 이유를.
- [ ] 설명할 수 있다: 메모이제이션의 비용이 "상태 수 × 전이 비용"인 이유를.
- [ ] 설명할 수 있다: 주어진 `n`만 보고 노려야 할 복잡도 등급을 즉시 말할 수 있다.

**⚠️ 자주 하는 실수**

**1) 리스트의 `in`을 `O(1)`로 착각한다**

```python
# ❌ 틀린 코드
seen = []
for x in a:                  # n번
    if x not in seen:        # 리스트를 앞에서부터 전부 비교 → O(n)
        seen.append(x)
# "한 번 훑었으니 O(n)"이라고 분석한다
```

왜: 파이썬 리스트의 `in`은 앞에서부터 하나씩 비교하는 **선형 탐색**이다. 원소가 모두 유일하면 비교가 `0+1+2+…+(n-1) = n(n-1)/2`번 일어나 실제로는 **`O(n²)`**이다. `n = 10⁵`이면 50억 번이라 시간 초과다.

```python
# ✅ 고친 코드
seen = set()                 # 해시 기반 → 멤버십 검사 평균 O(1)
for x in a:
    if x not in seen:
        seen.add(x)
# 전체 O(n)
```

**2) 반복문 안에서 문자열을 `+=`로 이어 붙인다**

```python
# ❌ 틀린 코드
s = ""
for i in range(n):
    s += str(i) + " "        # 매번 새 문자열을 통째로 만든다
print(s)
```

왜: 파이썬 문자열은 **불변(immutable)**이라 `s += t`는 "기존 `s`를 복사해 새 문자열을 만드는" 연산이다. 비용이 `1 + 2 + … + n`으로 누적되어 전체가 **`O(n²)`**이 된다. 겉보기에는 반복이 한 겹이라 속기 쉽다.

```python
# ✅ 고친 코드
parts = []
for i in range(n):
    parts.append(str(i))     # 끝에 붙이기만 하므로 평균 O(1)
print(" ".join(parts))       # 마지막에 한 번만 이어붙임 → 전체 O(n)
```

**3) 슬라이싱이 공짜라고 생각한다**

```python
# ❌ 틀린 코드
def bsearch(a, x):
    if not a:
        return False
    mid = len(a) // 2
    if a[mid] == x:
        return True
    if a[mid] < x:
        return bsearch(a[mid + 1:], x)   # 새 리스트를 복사해서 넘긴다
    return bsearch(a[:mid], x)
```

왜: `a[mid+1:]`은 원소를 **복사한 새 리스트**를 만든다. 즉 각 단계마다 `O(n)`의 시간과 공간이 추가되어, `T(n) = T(n/2) + O(n)`이 되고 전체가 `O(log n)`이 아니라 **`O(n)`**으로 나빠진다. 공간도 `O(n)`을 먹는다.

```python
# ✅ 고친 코드
def bsearch(a, x, lo, hi):
    if lo > hi:
        return False
    mid = (lo + hi) // 2      # 자르지 말고 '범위'만 넘긴다
    if a[mid] == x:
        return True
    if a[mid] < x:
        return bsearch(a, x, mid + 1, hi)
    return bsearch(a, x, lo, mid - 1)
# 시간 O(log n), 추가 공간은 스택 O(log n)뿐
```

**4) 리스트의 앞에서 원소를 빼거나 넣는다**

```python
# ❌ 틀린 코드
queue = [0]
while queue:
    cur = queue.pop(0)        # 앞 원소를 빼면 뒤 전부를 한 칸씩 당긴다
    for nxt in graph[cur]:
        queue.append(nxt)
# 또는 order.insert(0, x) 로 앞에 계속 끼워 넣기
```

왜: 리스트는 원소가 메모리에 나란히 놓인 구조라, **앞에서 빼면 뒤의 모든 원소를 한 칸씩 이동**해야 한다. `pop(0)`과 `insert(0, x)`는 각각 `O(n)`이므로 `n`번 반복하면 `O(n²)`이 된다.

```python
# ✅ 고친 코드
from collections import deque
queue = deque([0])            # 양쪽 끝 연산이 모두 O(1)
while queue:
    cur = queue.popleft()     # O(1)
    for nxt in graph[cur]:
        queue.append(nxt)
# 앞에 쌓는 것이 목적이라면 append 후 마지막에 reverse() 해도 된다
```

**5) 같은 구간 합을 질의마다 다시 계산한다**

```python
# ❌ 틀린 코드
for lo, hi in queries:        # q개
    total = 0
    for i in range(lo, hi + 1):   # 구간 길이만큼 → 최악 O(n)
        total += a[i]
    print(total)
# 전체 O(q * n)
```

왜: 질의가 `q`개이고 각 질의가 최악 `n`개를 더하므로 `O(qn)`이다. `n = q = 10⁵`이면 100억 번이다. 구간 합은 **미리 한 번 계산해 두면 질의마다 뺄셈 한 번**으로 끝난다.

```python
# ✅ 고친 코드
pre = [0] * (len(a) + 1)
for i, x in enumerate(a):          # 전처리 O(n)
    pre[i + 1] = pre[i] + x
for lo, hi in queries:
    print(pre[hi + 1] - pre[lo])   # 질의당 O(1) → 전체 O(n + q)
```

**6) 반복문 안에 숨은 반복(내장 함수)을 넣는다**

```python
# ❌ 틀린 코드
result = []
for x in a:                   # n번
    result.append(a.count(x)) # count는 매번 리스트 전체를 훑는다 → O(n)
# 반복이 한 겹처럼 보이지만 실제로는 O(n^2)
```

왜: `a.count(x)`, `min(a)`, `sum(a)`, `sorted(a)`는 **그 자체가 반복**이다. 반복문 안에 넣는 순간 중첩이 되어 등급이 한 칸 올라간다. `sorted`라면 `O(n² log n)`까지 간다.

```python
# ✅ 고친 코드
from collections import Counter
cnt = Counter(a)              # 전체를 한 번만 훑어 개수를 집계 → O(n)
result = [cnt[x] for x in a]  # 조회는 평균 O(1) → 전체 O(n)
```

**7) 깊이가 `n`인 재귀를 그대로 제출한다**

```python
# ❌ 틀린 코드
def rec_sum(a, i=0):
    if i == len(a):
        return 0
    return a[i] + rec_sum(a, i + 1)

print(rec_sum(list(range(100000))))   # RecursionError
```

왜: 파이썬은 재귀 깊이를 약 1000으로 제한한다(스택 영역을 넘어서는 사고를 막는 안전장치). 깊이가 입력 크기에 비례하는 재귀는 `n`이 조금만 커져도 **복잡도 이전에 실행 자체가 실패**한다. 공간도 `O(n)`을 쓴다.

```python
# ✅ 고친 코드
def iter_sum(a):
    s = 0
    for x in a:               # 시간 O(n), 공간 O(1), 깊이 항상 1
        s += x
    return s

print(iter_sum(list(range(100000))))
```

**8) 등급이 아니라 상수만 최적화한다**

```python
# ❌ 틀린 코드  ( n = 100000 )
best = 0
for i in range(n):
    for j in range(i + 1, n):        # 삼각형이라 절반이지만 여전히 O(n^2)
        if a[i] + a[j] == target:
            best += 1
# "range(i+1, n)으로 절반 줄였으니 괜찮겠지"
```

왜: 절반으로 줄여도 `n(n-1)/2 ≈ 5·10⁹`번이라 등급은 `O(n²)` 그대로다. **계수 `1/2`는 Big-O가 흡수한다.** 필요한 것은 상수 개선이 아니라 **등급을 한 칸 낮추는 구조 변경**이다.

```python
# ✅ 고친 코드
from collections import Counter
cnt = Counter()
best = 0
for x in a:                          # 한 번만 훑는다
    best += cnt[target - x]          # 짝이 왼쪽에 몇 개 있었나 → 평균 O(1)
    cnt[x] += 1
# 전체 O(n)
```

**다음 챕터로**

- 이 챕터의 결론은 하나다. **알고리즘 선택은 지문의 `n`을 읽는 순간 이미 절반이 끝난다.** 앞으로 어떤 문제를 만나든 "이 `n`에서 허용되는 등급은 무엇인가"를 먼저 적고 설계를 시작하면, 잘못된 방향으로 구현을 끝까지 밀고 가는 사고를 막을 수 있다.

- 이어지는 챕터들의 자료구조·알고리즘은 사실상 **"복잡도를 한 칸 낮추는 도구 상자"**다. 정렬과 이분 탐색은 `O(n)`을 `O(log n)`으로, 해시는 탐색을 `O(1)`로, 누적합·투 포인터는 반복 계산을 한 번 훑기로, DP는 지수를 다항식으로 끌어내린다. 이 챕터에서 만든 "상태 수 × 전이 비용" 공식이 그중 DP의 계산을 그대로 담당한다.

- 공간복잡도 감각도 계속 쓰인다. 2차원 DP 표를 `n = 10⁵`에 잡으려다 메모리가 먼저 터지는 일, 재귀 깊이가 한도를 넘어 실행이 실패하는 일은 모두 이 챕터에서 배운 이유로 일어난다.
