## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 챕터는 완전탐색의 **축(axis)** 을 두 갈래로 갈라서 배웠다. 하나는 "무엇을 고를까"(부분집합)를 훑는 것이고, 다른 하나는 "정답이 될 값이 얼마일까"를 훑는 것이다.
- 두 갈래는 서로 배타적이지 않다. 같은 문제를 양쪽으로 다 풀 수 있는 경우도 있으니, **후보 개수가 더 작은 축**을 고르면 된다.

**개념 지도**

```text
                      exhaustive search
                              |
          +-------------------+-------------------+
          |                                       |
    axis = CHOICE                           axis = VALUE
    "what do I pick?"                       "what is the answer?"
          |                                       |
    subset of n items                       candidate v in [lo, hi]
    r = 0..n, combinations(a, r)            for v in range(lo, hi+1)
          |                                       |
    evaluate(chosen) : sum / count          check(v) : one O(n) scan
          |                                       |
    O(2^n * n),  n <= 20                    O(V * n),  V = hi-lo+1
          |                                       |
    +-----+------+                          is check monotone?
    |            |                          O O O X X X  -> yes
  pick/skip    split in two                       |
  (knapsack)   (two teams)                  binary search on answer
                                            (a later chapter)
```

- 왼쪽 갈래는 **답이 "조합"** 일 때, 오른쪽 갈래는 **답이 "하나의 수"** 일 때 쓴다.
- 두 갈래가 만나는 자리가 "두 그룹으로 나누기"다. 한쪽을 고르면 반대쪽이 자동으로 결정되므로 부분집합 하나 = 배정 하나가 된다.

**뼈대 코드**

부분집합 완전탐색 — combinations 골격.

```python
from itertools import combinations

n = 4
w = [3, 7, 4, 9]                  # ← 문제마다 바뀜(물체의 속성)
C = 13                            # ← 문제마다 바뀜(제약)

best = 0                          # ← 답이 음수일 수 있으면 None으로
for r in range(n + 1):            # 고르는 개수 0 .. n → 합쳐서 2^n가지
    for chosen in combinations(w, r):
        total = sum(chosen)
        cnt = r                   # 고른 개수는 r 그 자체
        if total <= C:            # ← 문제마다 바뀜(제약 통과 조건)
            if total > best:      # ← 문제마다 바뀜(최대/최소/개수)
                best = total
print(best)
```

물체의 속성이 둘 이상이면(무게와 가치 등) 값이 아니라 **번호**를 고른다.

```python
from itertools import combinations

n = 3
w = [3, 4, 5]
v = [4, 5, 6]

for r in range(n + 1):
    for pick in combinations(range(n), r):   # 번호 묶음 (0, 2) 같은 꼴
        tw = sum(w[i] for i in pick)
        tv = sum(v[i] for i in pick)
```

부분집합 완전탐색 — 재귀 골격(도중에 가지치기를 넣고 싶을 때 같은 일을 한다).

```python
n = 3
a = [5, 2, 8]
best = 0

def go(i, total):                 # i번째 물체까지 결정했고, 현재 합은 total
    global best
    if i == n:                    # 끝까지 결정 → 여기서 평가
        if total > best:          # ← 문제마다 바뀜
            best = total
        return
    go(i + 1, total + a[i])       # i번을 고른다
    go(i + 1, total)              # i번을 고르지 않는다

go(0, 0)
print(best)
```

두 그룹으로 나누기 골격 — 한쪽만 고르면 반대쪽은 자동이다.

```python
from itertools import combinations

n = 4
a = [1, 6, 11, 5]
total = sum(a)

best = None
for r in range(1, n):                 # 0명과 n명 제외 → 두 그룹 모두 최소 1개
    for chosen in combinations(a, r):
        s = sum(chosen)
        d = abs(s - (total - s))      # ← 문제마다 바뀜(평가식)
        if best is None or d < best:
            best = d
print(best)
```

값 기준 완전탐색 골격 — 후보 값을 하나씩 대입해 판정한다.

```python
a = [20, 15, 10, 17]
M = 7                             # ← 문제마다 바뀜(목표치)

lo, hi = 0, max(a)                # ← 문제마다 바뀜(후보 값의 범위)
ans = -1                          # 한 번도 만족 못 하면 그대로 -1
for v in range(lo, hi + 1):       # hi 자신도 후보이므로 +1 필수
    got = 0
    for x in a:
        if x > v:                 # ← 문제마다 바뀜(판정용 계산)
            got += x - v
    if got >= M:                  # ← 문제마다 바뀜(조건)
        ans = v                   # "만족하는 v 중 최대" → 계속 덮어쓰기
print(ans)
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| "몇 개를 골라서 …", 각 물체가 독립적으로 포함/제외 | 부분집합(`combinations`, r = 0..n) | 탐색의 축이 물체 그 자체 | O(2^n · n), n ≤ 20 |
| "두 팀/두 그룹으로 남김없이 나눠라" | 부분집합 + 나머지는 자동 | 한쪽을 정하면 반대편이 결정됨 | O(2^n · n) |
| 고르는 개수가 **정확히 k개**로 정해져 있다 | `combinations(a, k)` 한 줄 | r을 훑을 필요 없이 그 크기만 | O(C(n,k) · k) |
| 뽑는 **순서가 뜻을 가진다**(줄 세우기·암호 배치) | `permutations` | `combinations`는 순서를 무시함 | O(n! / (n-k)!) |
| 같은 것을 **여러 번 골라도 된다**(K종류를 N번) | `product(a, repeat=n)` | 중복 선택은 조합이 아님 | O(K^n) |
| 도중에 가지치기해 가망 없는 가지를 끊고 싶다 | 재귀(포함/제외) | 부분 상태를 인자로 들고 다닐 수 있음 | O(2^n) 노드 |
| "조건을 만족하는 가장 큰/작은 값 X를 구하라" | 값 기준 완전탐색 | 답 자체가 하나의 수 | O(V · n) |
| 값 범위 V가 매우 크고 check가 단조 | (다음 단계) 답에 대한 이분탐색 | 참/거짓 경계가 딱 한 곳 | O(n log V) |
| 물체 n개 중 **정확히 2개**만 고른다 | 이중 for `i < j` | 순서가 무의미해 절반만 보면 됨 | O(n²) |
| n이 20을 넘는데 답이 조합 | 부분집합 포기 → DP·그리디 재검토 | 2^n이 폭발함 | — |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 부분집합의 개수가 왜 정확히 2^n인지(각 물체마다 두 갈래 × n번 → 곱의 법칙).
- [ ] 설명할 수 있다: 크기별로 나눠 세면 왜 중복도 누락도 없는지(C(n,0) + … + C(n,n) = 2^n).
- [ ] 설명할 수 있다: `combinations`가 왜 `(3, 7)`과 `(7, 3)`을 따로 내지 않는지.
- [ ] 설명할 수 있다: `range(n + 1)`에서 `+ 1`을 빼면 어떤 경우가 통째로 빠지는지.
- [ ] 설명할 수 있다: 배열이 둘 이상일 때 왜 `combinations(range(n), r)`로 번호를 고르는지.
- [ ] 설명할 수 있다: `combinations`·`permutations`·`product`를 각각 언제 쓰는지.
- [ ] 설명할 수 있다: "두 그룹으로 나누기"가 왜 부분집합 하나를 고르는 문제와 같은지.
- [ ] 설명할 수 있다: 두 그룹이 모두 비지 않아야 할 때 r 범위를 `1 .. n-1`로 두는 이유.
- [ ] 설명할 수 있다: 부분집합 완전탐색이 O(2^n · n)이고, 그래서 n ≤ 20이 실전 기준선인 이유.
- [ ] 설명할 수 있다: "값 기준 완전탐색"이 조합 대신 무엇을 훑는지, 언제 그 발상이 가능한지.
- [ ] 설명할 수 있다: 후보 값의 범위 [lo, hi]를 어떻게 정하고, 왜 `range(lo, hi + 1)`이어야 하는지.
- [ ] 설명할 수 있다: 판정 함수 check(v)가 단조라는 말이 무슨 뜻이고, 그게 왜 나중에 이분탐색으로 이어지는지.
- [ ] 설명할 수 있다: 최댓값을 담는 변수를 0으로 초기화하면 어떤 입력에서 틀리는지.
- [ ] 설명할 수 있다: n개 중 2개를 고를 때 `i < j`로 두면 왜 중복이 사라지고 개수가 n(n-1)/2가 되는지.

**⚠️ 자주 하는 실수**

**1) 고르는 개수 범위에서 `+ 1`을 빠뜨리기**

```python
# ❌ 틀린 코드
n = 4
for r in range(n):                # 0, 1, 2, 3 — n개를 전부 고르는 경우가 없다
    for chosen in combinations(a, r):
        pass
```

왜: `range(n)`은 `n - 1`에서 멈춘다. "전부 고르기"가 정답인 입력(예: 한도가 넉넉해 다 담는 게 최선)에서만 틀리는데, 작은 예제는 대개 그 경우가 아니라 잘 안 잡힌다.

```python
# ✅ 고친 코드
n = 4
for r in range(n + 1):            # 0 .. n, 공집합과 전체집합 모두 포함
    for chosen in combinations(a, r):
        pass
```

**2) 배열이 둘인데 값을 골라 짝이 어긋나기**

```python
# ❌ 틀린 코드
for r in range(n + 1):
    for chosen in combinations(w, r):    # 무게 "값"만 골랐다
        tw = sum(chosen)
        tv = sum(v[:r])                  # 가치는 어느 상품 것인지 알 수 없다
```

왜: `combinations(w, r)`이 내어 주는 것은 무게 값뿐이라, 그 무게가 **몇 번 상품의 것인지**가 사라진다. 짝이 되는 가치를 되찾을 방법이 없고, 무게가 같은 상품이 둘 이상이면 더욱 그렇다.

```python
# ✅ 고친 코드
for r in range(n + 1):
    for pick in combinations(range(n), r):   # "번호"를 고른다
        tw = sum(w[i] for i in pick)
        tv = sum(v[i] for i in pick)
```

**3) 최댓값 변수를 0으로 초기화**

```python
# ❌ 틀린 코드
best = 0
for r in range(n + 1):
    for chosen in combinations(v, r):
        s = sum(chosen)
        if s > best:
            best = s
```

왜: "반드시 1개 이상 골라야 한다"인데 모든 가치가 음수라면 정답도 음수다. 그런데 `best = 0`은 한 번도 갱신되지 않아 0이 출력된다.

```python
# ✅ 고친 코드
best = None
for r in range(1, n + 1):         # 최소 1개는 고른다 → r = 0 제외
    for chosen in combinations(v, r):
        s = sum(chosen)
        if best is None or s > best:
            best = s
```

**4) 같은 쌍을 두 번 세기(`i < j` 누락)**

```python
# ❌ 틀린 코드
cnt = 0
for i in range(n):
    for j in range(n):
        if i != j and a[i] + a[j] == target:
            cnt += 1
```

왜: `(i, j)`와 `(j, i)`가 서로 다른 반복에서 각각 세어져 답이 정확히 2배가 된다. `i != j`는 "같은 원소 두 번"만 막을 뿐 순서 중복은 못 막는다.

```python
# ✅ 고친 코드
cnt = 0
for i in range(n):
    for j in range(i + 1, n):     # 항상 i < j → 각 쌍을 정확히 한 번
        if a[i] + a[j] == target:
            cnt += 1
```

**5) 값 후보의 상한을 빠뜨리기**

```python
# ❌ 틀린 코드
ans = -1
for v in range(lo, hi):           # hi 자신은 한 번도 검사되지 않는다
    if check(v):
        ans = v
```

왜: `range(lo, hi)`는 `hi - 1`에서 멈춘다. 정답이 딱 `hi`인 입력(예: 가장 높은 나무 높이가 그대로 답)에서만 틀려, 예제로는 잘 안 잡힌다.

```python
# ✅ 고친 코드
ans = -1
for v in range(lo, hi + 1):       # 상한 포함
    if check(v):
        ans = v
```

**6) 판정 계산에서 음수 기여를 막지 않기**

```python
# ❌ 틀린 코드
got = 0
for x in h:
    got += x - H                  # H보다 낮은 나무가 총합을 깎는다
```

왜: 절단기 높이 `H` 이하인 나무의 기여는 0이어야 하는데, `x - H`가 음수로 더해져 얻는 양이 실제보다 작게 계산된다.

```python
# ✅ 고친 코드
got = 0
for x in h:
    if x > H:
        got += x - H              # 또는 got += max(0, x - H)
```

**7) 두 그룹으로 나눌 때 빈 그룹을 허용**

```python
# ❌ 틀린 코드
for r in range(n + 1):            # r = 0 이면 한 그룹이 텅 빈다
    for chosen in combinations(a, r):
        s = sum(chosen)
```

왜: "두 팀 모두 최소 1명"이라는 조건이 있으면 고르는 인원이 `0`명(한 팀이 빔)이거나 `n`명(반대 팀이 빔)인 경우는 유효한 분할이 아니다. 그대로 두면 항상 "전부 한 팀"이 최적으로 뽑힌다.

```python
# ✅ 고친 코드
for r in range(1, n):             # 양 끝(0명, n명)을 자연스럽게 배제
    for chosen in combinations(a, r):
        s = sum(chosen)
```

**다음 챕터로**

- 다음 챕터는 "고를 대상"이 뚜렷하지 않은 문제를 다룬다. **미지수 하나를 가정**하고 나머지를 규칙대로 전개하거나, 아예 **탐색의 축을 다른 것으로 갈아끼워** 경우의 수를 줄인다.
- 여기서 익힌 "탐색의 축을 의식한다"는 습관이 그대로 이어진다. 지금은 축이 물체/값 두 가지였다면, 다음에는 가정·기준점·시각 같은 축이 추가된다.
