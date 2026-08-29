## L5. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 레슨은 Ch06(완전탐색 I) 전체를 한 장으로 묶는 정리다. 세 레슨은 "후보가 무엇이냐"만 다를 뿐, **후보를 빠짐없이 나열하고 조건을 검사한다**는 뼈대가 완전히 같다. 그리고 그 앞에는 항상 "다 세도 되는가"를 계산하는 단계가 있다.

**개념 지도**

- 완전탐색의 갈래는 "무엇 하나를 후보로 볼 것인가"로 나뉜다. 후보가 정해지면 개수를 세는 공식도 함께 정해지고, 그 개수가 코드를 짤지 말지를 결정한다.

```text
                     Ch06 : brute force I
                              |
        +---------------------+---------------------+
        |                     |                     |
   ONE NUMBER            ONE RANGE            ONE ARRANGEMENT
   candidate = n         candidate = (i, j)   candidate = (s1..sn)
        |                     |                     |
   L1 digit scan         L2 subarray scan     L3 slot by slot
   for n in a..b         for i , for j        nested for / product
   str(n) or % 10        running sum s        product(V, repeat=n)
        |                     |                     |
   count = b - a + 1     count = n(n+1)/2     count = m ** n
        |                     |                     |
        +---------------------+---------------------+
                              |
              step 0 : count first, then write code
```

- "다 세도 되는가"를 판단하는 자는 하나뿐이다. **후보 수 × 후보 하나당 검사 비용**을 곱해 보고, 파이썬 기준 1초에 약 10^7 단계라는 예산과 비교한다.

```text
  budget : about 10^7 simple steps per second

  candidates      x  cost   =  total          verdict
  ----------------------------------------------------------
  10^5 (a..b)        7         7 * 10^5       fine
  2000^2 / 2         1         2 * 10^6       fine       # O(n^2), n=2000
  3^10               10        6 * 10^5       fine
  9^7                7         3 * 10^7       tight
  10^8               1         10^8           risky
  10^5 ^ 2           1         5 * 10^9       impossible # O(n^2), n=10^5
```

- 자리마다 값을 정하는 탐색은 트리로 그리면 개수가 눈에 보인다. 잎 하나가 후보 하나이고, 가지 수가 `m`, 깊이가 `n`이면 잎은 `m^n`개다.

```text
  n = 3 slots, values = {1, 2}   ->   2^3 = 8 leaves

                 root
            /            \
          1                2         slot 1
        /   \            /   \
       1     2          1     2      slot 2
      / \   / \        / \   / \
     1   2 1   2      1   2 1   2    slot 3
```

**뼈대 코드**

- (1) 자리 수 단위: 범위 안의 정수를 하나씩 후보로 본다.

```python
a, b = map(int, input().split())
cnt = 0
for n in range(a, b + 1):           # ← "이상/이하"를 그대로 옮긴다(+1 주의)
    s = str(n)                      # 자릿수를 봐야 하면 문자열이 가장 짧다
    value = sum(int(ch) for ch in s)        # ← 문제마다 바뀜: 계산할 값
    if value % k == 0:                      # ← 문제마다 바뀜: 조건
        cnt += 1
print(cnt)
```

- (2) 구간 단위: 모든 `(i, j)`를 훑되 합은 누적으로 굴린다.

```python
best = None                         # 음수 대비: 0으로 두지 않는다
cnt = 0
for i in range(n):                  # 구간 시작
    s = 0                           # ← 반드시 바깥 루프 안에서 초기화
    mn = mx = arr[i]
    for j in range(i, n):           # 구간 끝을 한 칸씩 늘린다
        s += arr[j]                 # arr[i..j] 의 합을 O(1) 로 유지
        if arr[j] < mn: mn = arr[j]
        if arr[j] > mx: mx = arr[j]
        if s == target:             # ← 문제마다 바뀜: 조건
            cnt += 1
        # 조기 종료는 조건이 단조일 때만!
        # if mx - mn > d: break
```

- (3) 자리마다 값 정하기: 자리 수가 고정이면 중첩 for, 변수면 `product`.

```python
from itertools import product

# 자리 수가 코드에 박혀 있을 때 (2자리)
for x in range(1, d + 1):
    for y in range(1, d + 1):
        combo = (x, y)              # ← 여기서 조건 검사

# 자리 수 n 이 입력으로 올 때 — 위와 완전히 같은 것을 만든다
for combo in product(range(1, d + 1), repeat=n):
    ok = True
    for i in range(n - 1):          # ← 문제마다 바뀜: 조건
        if combo[i] == combo[i + 1]:
            ok = False
            break
    if ok:
        cnt += 1
```

- (4) 경우의 수 계산: 코드를 짜기 전에 이 표를 먼저 채운다.

```python
# 후보 수 세는 공식 (검산용 — 코드는 완전탐색으로 짜도 된다)
#   범위 정수         : b - a + 1
#   모든 연속 구간    : n * (n + 1) // 2
#   길이 L 고정 구간  : n - L + 1
#   자리 n, 값 m 가지 : m ** n
#   첫 자리만 0 금지  : (m - 1) * m ** (n - 1)
#   이웃 자리 상이    : d * (d - 1) ** (n - 1)
#   n칸 중 k칸만 'A'  : C(n, k) * 2 ** (n - k)

total = m ** n                      # ← 문제마다 바뀜
print(total, "candidates")          # 10^7 을 넘으면 다른 방법을 찾는다
```

- (5) 세기·최선값 고르기의 공통 마무리.

```python
cnt = 0
best = None                         # 최댓값 초기값을 0으로 두지 않는다
for cand in candidates:             # ← 위 세 골격 중 하나
    if not passes(cand):            # ← 문제마다 바뀜: 조건
        continue
    cnt += 1
    v = score(cand)                 # ← 문제마다 바뀜: 평가값
    if best is None or v > best:
        best = v
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| a 이상 b 이하의 수를 검사 | `range(a, b+1)` 순회 | 후보가 정수 하나씩이라 가장 단순 | O(b−a) |
| 자릿수 합·포함·회문 판정 | `str(n)`으로 한 글자씩 | 0과 음수 처리가 자연스럽고 짧다 | 후보당 O(자리 수) |
| k진 자릿수 값이 필요 | `% k`, `// k` 반복 | 문자 변환 없이 값 자체를 얻음 | 후보당 O(log n) |
| 모든 연속 구간을 봐야 함 | 이중 for + 누적 합 | 구간마다 원소 하나만 더하면 됨 | O(n²) |
| 길이가 정확히 L인 구간 | 시작점만 이동(슬라이딩) | 끝점이 시작점에 종속 | O(n) |
| 구간 폭이 단조로 커짐 | 조건 위반 시 `break` | 더 늘려도 회복 불가 | 평균이 크게 줄어듦 |
| 자리 수가 코드에 고정(2~3) | for 중첩 | 읽기 쉽고 인덱스 실수가 적음 | O(mⁿ) |
| 자리 수가 입력 변수 | `product(V, repeat=n)` | 중첩 개수를 코드로 못 바꿈 | O(mⁿ) |
| 자리마다 후보 집합이 다름 | `product(V1, V2, ...)` | 자리별 제약을 집합에 반영 | 곱만큼 |
| 후보 수가 10^7을 넘음 | 완전탐색 포기 | 1초 예산 초과 | — |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 완전탐색의 두 단계("후보를 빠짐없이 나열" + "조건 검사")와, 그 앞에 경우의 수 계산이 오는 이유.
- [ ] 설명할 수 있다: a 이상 b 이하의 정수가 `b - a + 1`개인 이유와, 그것이 `range(a, b+1)`과 맞아떨어지는 이유.
- [ ] 설명할 수 있다: 길이 n 배열의 연속 구간이 `n(n+1)/2`개인 것을 시작점별로 세어 유도할 수 있다.
- [ ] 설명할 수 있다: 안쪽 루프에서 누적 변수를 쓰면 왜 O(n³)이 O(n²)로 줄어드는지.
- [ ] 설명할 수 있다: 자리 n개·값 m가지의 경우의 수가 `mⁿ`인 이유를 곱의 법칙과 트리 잎 개수로 각각.
- [ ] 설명할 수 있다: "이웃한 자리가 달라야 한다"는 제약이 붙으면 왜 `d·(d-1)^(n-1)`이 되는지.
- [ ] 설명할 수 있다: `product(V, repeat=n)`이 for 중첩과 같은 것을 만든다는 사실과, 그럼에도 `product`가 필요한 상황.
- [ ] 설명할 수 있다: 후보 수와 검사 비용을 곱해 1초 안에 되는지 판단하는 기준(약 10^7 단계).
- [ ] 설명할 수 있다: `n`을 1 늘리는 것이 `m`을 1 늘리는 것보다 훨씬 위험한 이유.
- [ ] 설명할 수 있다: 문제의 제약이 유난히 작을 때(`n ≤ 7` 등) 그것이 무엇을 뜻하는 신호인지.
- [ ] 설명할 수 있다: 조기 종료(`break`)가 정당한 조건과, 음수가 섞였을 때 위험한 이유.
- [ ] 설명할 수 있다: "정확히 k개"와 "k개 이상"을 코드에서 어떻게 구분하는지.
- [ ] 설명할 수 있다: 최댓값 변수의 초기값을 0으로 두면 안 되는 경우와 그 대안.
- [ ] 설명할 수 있다: 완전탐색으로 얻은 답을 닫힌 식(`nCr` 등)으로 검산하는 방법.

**⚠️ 자주 하는 실수**

**1) 범위의 끝이 하나 빠진다**

```python
# ❌ 틀린 코드
for n in range(a, b):        # b 자신을 검사하지 않는다
    if ok(n):
        cnt += 1
```

왜: 문장이 "a 이상 b 이하"인데 `range(a, b)`는 `b-1`에서 멈춘다. 답이 딱 1 모자라게 나오는 전형적인 오답이라, 예제가 우연히 맞으면 끝까지 못 찾는다.

```python
# ✅ 고친 코드
for n in range(a, b + 1):    # "이하"는 b + 1
    if ok(n):
        cnt += 1
```

**2) 누적 변수를 바깥에서 한 번만 초기화한다**

```python
# ❌ 틀린 코드
s = 0
for i in range(n):           # 시작점이 바뀌어도 s 가 이어진다
    for j in range(i, n):
        s += arr[j]
        if s == target:
            cnt += 1
```

왜: `s`는 "현재 시작점 `i`에서 시작한 구간의 합"이어야 한다. 바깥에 두면 이전 시작점의 합이 그대로 남아, 두 번째 `i`부터는 존재하지 않는 구간의 합을 검사한다.

```python
# ✅ 고친 코드
for i in range(n):
    s = 0                    # 시작점이 바뀔 때마다 리셋
    for j in range(i, n):
        s += arr[j]
        if s == target:
            cnt += 1
```

**3) 슬라이스 끝에서 `j`를 포함시키지 않는다**

```python
# ❌ 틀린 코드
for i in range(n):
    for j in range(i, n):
        if sum(arr[i:j]) == target:   # arr[j] 가 빠진 구간을 본다
            cnt += 1
```

왜: 인덱스 `j`는 "구간의 끝 원소"인데 슬라이스 `arr[i:j]`는 `j`를 포함하지 않는다. 길이가 하나씩 짧은 구간만 검사하게 되고, `i == j`인 길이 1 구간은 빈 구간이 되어 아예 사라진다. 게다가 매번 다시 더하므로 O(n³)이다.

```python
# ✅ 고친 코드
for i in range(n):
    s = 0
    for j in range(i, n):
        s += arr[j]                   # 누적으로 arr[i..j] 유지 (O(n^2))
        if s == target:
            cnt += 1
```

**4) 최댓값 초기값을 0으로 둔다**

```python
# ❌ 틀린 코드
best = 0
for i in range(n - L + 1):
    s = sum(arr[i:i + L])
    if s > best:
        best = s                      # 모든 구간 합이 음수면 0이 남는다
```

왜: 값에 음수가 섞이면 "존재하지 않는 답 0"이 실제 최댓값을 이긴다. 초기값은 **후보 중 하나**여야지, 임의의 상수여서는 안 된다.

```python
# ✅ 고친 코드
best = sum(arr[:L])                   # 첫 후보로 초기화
for i in range(1, n - L + 1):
    s = sum(arr[i:i + L])
    if s > best:
        best = s
```

**5) 단조가 아닌 조건에 조기 종료를 건다**

```python
# ❌ 틀린 코드
for i in range(n):
    s = 0
    for j in range(i, n):
        s += arr[j]
        if s > target:
            break                     # 음수가 있으면 뒤에서 다시 줄어든다
        if s == target:
            cnt += 1
```

왜: `break`가 정당하려면 "더 진행해도 조건이 회복되지 않는다"가 참이어야 한다. 원소가 모두 양수면 합은 커지기만 하니 옳지만, 음수가 섞이면 합이 다시 내려와 `target`이 될 수 있어 답을 놓친다.

```python
# ✅ 고친 코드
for i in range(n):
    s = 0
    for j in range(i, n):
        s += arr[j]
        if s == target:
            cnt += 1                  # 음수 가능성이 있으면 끝까지 본다
```

**6) 자리 수가 변수인데 for 중첩으로 버틴다**

```python
# ❌ 틀린 코드
for x in range(1, d + 1):             # n 이 3일 때만 맞는 코드
    for y in range(1, d + 1):
        for z in range(1, d + 1):
            check((x, y, z))
```

왜: 중첩 개수는 코드를 쓸 때 정해지므로 입력으로 들어오는 `n`에 맞출 수 없다. `n`이 2나 5로 오는 순간 통째로 틀린다. 이럴 때 쓰라고 있는 도구가 `product`의 `repeat`이다.

```python
# ✅ 고친 코드
from itertools import product
for combo in product(range(1, d + 1), repeat=n):   # 자리 수를 변수로
    check(combo)
```

**7) "정확히 k개"를 "k개 이상"으로 센다**

```python
# ❌ 틀린 코드
if combo.count('A') >= k:             # 정확히 k 개를 물었는데 이상으로 셌다
    cnt += 1
```

왜: `>=`는 A가 `k+1`개, `k+2`개인 경우까지 포함한다. "정확히"는 하나의 값과의 일치이므로 `==`여야 한다. 반대로 "적어도"라고 적힌 문장에 `==`를 쓰면 답이 모자란다 — 문장의 낱말을 그대로 연산자로 옮기는 습관이 필요하다.

```python
# ✅ 고친 코드
if combo.count('A') == k:             # 정확히 k 개
    cnt += 1
```

**다음 챕터로**

- 완전탐색은 "정직하게 다 본다"는 가장 안전한 무기이자, 이후 모든 최적화의 **기준선**이다. 더 빠른 풀이를 떠올렸을 때 작은 입력에서 완전탐색 결과와 비교하면 그 풀이가 맞는지 검증할 수 있다.
- 앞으로는 이 뼈대에 "이미 틀린 가지는 더 내려가지 않는다"(가지치기)와 "같은 계산을 두 번 하지 않는다"(기억하기)가 붙는다. 지금 경우의 수를 세는 습관을 들여 두면, 그 최적화가 왜 필요한지도 숫자로 보인다.
