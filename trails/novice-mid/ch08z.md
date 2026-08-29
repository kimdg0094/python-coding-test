## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 챕터의 질문은 하나다. **"나는 지금 무엇을 하나씩 바꿔가며 보고 있는가?"** 그 축이 잘못되면 완전탐색은 느려지고, 축을 바꾸면 같은 답을 훨씬 적은 경우로 센다.
- L1은 **축을 새로 만든다**(정하면 나머지가 줄줄이 결정되는 미지수 하나를 가정). L2는 **축을 갈아끼운다**(쌍·조합 대신 값·기준점·시각을 훑는다).

**개념 지도**

```text
                     brute force is too slow
                               |
                   "which axis am I looping over?"
                               |
           +-------------------+-------------------+
           |                                       |
     ASSUME  (L1)                            RE-AXIS  (L2)
     fix ONE unknown, derive the rest        swap the loop axis
           |                                       |
     for x in range(lo, hi+1):               pair (i, j)    O(n^2)
         build the rest by the rule                | replace with
         contradiction? -> drop                    v
         survived?      -> candidate         sorted ends    O(n log n)
           |                                 threshold val  O(n log n)
           v                                 pivot index    O(n) x O(1)
     O(V * n)                                time event     O(n log n)
           |                                       |
           +-------------------+-------------------+
                               |
                    keep the best / count survivors
```

- 두 갈래의 공통 원리: **자유도(free variable)를 1개로 줄인다.** 자유도가 2개면 후보가 V²개로 늘어난다.
- 축을 잘 고르는 것이 그대로 복잡도 개선이다. `O(n²) → O(n log n)`은 대개 정렬·이벤트 스캔으로 축을 바꾼 결과다.

**뼈대 코드**

가정 하나 고정 → 규칙 전개 → 검증 골격.

```python
n, d, H = 4, 2, 10                # ← 문제마다 바뀜(입력)

cnt = 0
best = None
for x in range(1, H + 1):         # ← 문제마다 바뀜(가정할 값의 범위)
    ok = True                     # 가정마다 반드시 새로 초기화
    cur = x
    for i in range(1, n):
        cur = cur + d             # ← 문제마다 바뀜(전개 규칙)
        if cur < 1 or cur > H:    # ← 문제마다 바뀜(모순 조건)
            ok = False
            break
    if ok:                        # 끝까지 살아남은 가정만 후보
        cnt += 1
        if best is None or x > best:
            best = x
print(cnt, best)
```

단조 수열이면 양 끝만 검사한다 — 위 골격의 안쪽 루프를 O(1)로 줄인 형태.

```python
n, d, H = 4, 2, 10

cnt = 0
for x in range(1, H + 1):
    lo = x                        # d >= 0 이므로 맨 앞이 최솟값
    hi = x + d * (n - 1)          # 맨 뒤가 최댓값
    if lo >= 1 and hi <= H:       # 양 끝이 범위 안 → 중간은 자동
        cnt += 1
print(cnt)
```

기준점 하나를 고정하고 나머지를 훑는 골격.

```python
n = 5
a = [3, 1, 4, 1, 5]

best = None
for i in range(n):                # i를 기준점으로 고정
    for j in range(n):            # ← 문제에 따라 O(1) 계산으로 대체 가능
        if j == i:
            continue
        v = a[i] - a[j]           # ← 문제마다 바뀜(평가식)
        if best is None or v > best:
            best = v
print(best)
```

쌍을 정확히 한 번씩 보는 골격 — 순서가 무의미하면 `i < j`.

```python
n = 4
a = [3, 1, 4, 2]

best = None
for i in range(n):
    for j in range(i + 1, n):     # (i, j)를 한 번만, 총 n(n-1)/2회
        v = a[i] * a[j]           # ← 문제마다 바뀜
        if best is None or v > best:
            best = v
print(best)
```

시각(이벤트)을 축으로 스캔하는 골격 — 구간 겹침 개수를 셀 때의 정석.

```python
segs = [(1, 4), (2, 5), (6, 8)]   # ← 문제마다 바뀜(반열린 구간 [s, e))

events = []
for s, e in segs:
    events.append((s, 1))         # 시작: +1
    events.append((e, -1))        # 끝: -1
events.sort(key=lambda x: (x[0], x[1]))   # 동시각이면 -1이 먼저

cur = 0
best = 0
for _, delta in events:
    cur += delta
    if cur > best:
        best = cur
print(best)
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 규칙은 명확한데 시작값·기준값 하나가 안 정해짐 | 그 값을 가정하고 전개(L1) | 하나만 정하면 나머지가 도미노처럼 결정 | O(V · n) |
| 가정 위에서 만들어지는 수열이 단조 | 양 끝값만 검사 | 최솟값·최댓값이 범위 안이면 중간은 자동 | O(V) |
| 두 수를 골라 최대/최소를 구함 | 정렬 후 양 끝 상수 개만 비교 | 극단값에서만 답이 나옴 | O(n log n) |
| "정확히 k명이 넘는 문턱" 류 | 값(문턱)을 축으로 | 후보 값이 입력에 등장하는 수뿐 | O(n log n) |
| 모든 쌍을 봐야만 하는 작은 n | 이중 for `i < j` | 중복 없이 n(n-1)/2회 | O(n²) |
| 구간이 동시에 몇 개 겹치는지 | 시작 +1 / 끝 −1 이벤트 스캔 | 축을 "쌍"에서 "시각"으로 | O(n log n) |
| 가정할 미지수가 둘 이상으로 보임 | 하나를 다른 하나로 표현해 1개로 줄임 | V² → V | O(V · n) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: "무엇을 가정할지" 고를 때 왜 "정하면 나머지가 결정되는 값"이 좋은 후보인지.
- [ ] 설명할 수 있다: 가정을 두 개 겹치면 복잡도가 왜 O(V·n)에서 O(V²·n)로 커지는지.
- [ ] 설명할 수 있다: 가정한 값이 만드는 수열이 단조일 때, 왜 양 끝값만 검사해도 되는지.
- [ ] 설명할 수 있다: 가정마다 `ok` 같은 상태 변수를 다시 초기화해야 하는 이유.
- [ ] 설명할 수 있다: "축을 갈아끼운다"는 말이 구체적으로 무엇을 무엇으로 바꾸는 것인지 예를 들어.
- [ ] 설명할 수 있다: n개 중 2개를 고를 때 `i < j`로 두면 중복이 왜 사라지고 개수가 왜 n(n-1)/2인지.
- [ ] 설명할 수 있다: 두 수의 곱을 최대로 만들 때 왜 "가장 작은 두 수"도 후보여야 하는지.
- [ ] 설명할 수 있다: 문턱(합격선) 문제에서 후보 값이 왜 입력에 등장하는 수 근처뿐인지.
- [ ] 설명할 수 있다: 동점이 있으면 "정확히 k명"이 왜 불가능해질 수 있는지.
- [ ] 설명할 수 있다: 구간 겹침 최대 개수를 시작 +1 / 끝 −1 이벤트로 세는 원리.
- [ ] 설명할 수 있다: 반열린 구간 `[s, e)`에서 같은 시각의 끝을 시작보다 먼저 처리해야 하는 이유.
- [ ] 설명할 수 있다: 답이 없을 수 있는 문제에서 `best = 0`이 아니라 `best = None`으로 시작해야 하는 이유.

**⚠️ 자주 하는 실수**

**1) 가정마다 상태 변수를 초기화하지 않기**

```python
# ❌ 틀린 코드
res = []
ok = True                         # 반복 바깥에서 한 번만 초기화
for x in range(1, H + 1):
    for i in range(1, n):
        if x + d * i > H:
            ok = False
    if ok:
        res.append(x)
```

왜: 한 번이라도 `ok`가 False가 되면 그 뒤의 모든 가정이 무조건 실패로 처리된다. 앞쪽 가정이 통과하는 입력에서는 답이 맞아 보여서 더 위험하다.

```python
# ✅ 고친 코드
res = []
for x in range(1, H + 1):
    ok = True                     # 가정 하나마다 새로 초기화
    for i in range(1, n):
        if x + d * i > H:
            ok = False
            break
    if ok:
        res.append(x)
```

**2) 같은 쌍을 두 번 세기(`i < j` 누락)**

```python
# ❌ 틀린 코드
cnt = 0
for i in range(n):
    for j in range(n):
        if i != j and a[i] + a[j] == target:
            cnt += 1
```

왜: `(i, j)`와 `(j, i)`가 각각 세어져 답이 정확히 2배가 된다. `i != j`는 "같은 원소를 두 번 고르는 것"만 막을 뿐 순서 중복은 못 막는다.

```python
# ✅ 고친 코드
cnt = 0
for i in range(n):
    for j in range(i + 1, n):     # 항상 i < j → n(n-1)/2회, 중복 없음
        if a[i] + a[j] == target:
            cnt += 1
```

**3) 정렬 후 "큰 쪽 끝"만 후보로 보기**

```python
# ❌ 틀린 코드
arr.sort()
print(arr[-1] * arr[-2])          # 가장 큰 두 수의 곱만 본다
```

왜: 음수 두 개의 곱은 양수라 더 클 수 있다. `[-10, -9, 1, 2]`에서 정답은 90인데 이 코드는 2를 출력한다. 극단값을 볼 때는 **양쪽 끝**을 모두 후보로 둬야 한다.

```python
# ✅ 고친 코드
arr.sort()
print(max(arr[-1] * arr[-2], arr[0] * arr[1]))
```

**4) 이벤트 정렬에서 동시각 처리 순서를 지정하지 않기**

```python
# ❌ 틀린 코드
events = []
for s, e in segs:
    events.append((s, 1))
    events.append((e, -1))
events.sort(key=lambda x: x[0])   # 같은 시각의 순서를 정하지 않았다
```

왜: 반열린 구간 `[s, e)`에서는 `e` 시점에 이미 끝난 것으로 본다. 같은 시각에 시작(+1)이 먼저 처리되면 `[1,2)`와 `[2,5)`를 겹친 것으로 세어 답이 1 커진다.

```python
# ✅ 고친 코드
events.sort(key=lambda x: (x[0], x[1]))   # -1 < +1 이므로 끝이 먼저
```

**5) 최댓값 변수를 0으로 초기화**

```python
# ❌ 틀린 코드
best = 0
for i in range(n):
    for j in range(i + 1, n):
        p = a[i] * a[j]
        if p > best:
            best = p
print(best)
```

왜: 모든 곱이 음수인 입력(예: `[-3, 2]` → 정답 −6)에서는 한 번도 갱신되지 않아 0이 출력된다. 0은 실제 후보가 아닌데 답이 되어 버린다.

```python
# ✅ 고친 코드
best = None
for i in range(n):
    for j in range(i + 1, n):
        p = a[i] * a[j]
        if best is None or p > best:
            best = p
print(best)
```

**6) "불가능"과 "답이 0"을 구별하지 않기**

```python
# ❌ 틀린 코드
ans = 0                           # 조건을 만족하는 x가 없어도 0을 출력
for x in range(0, C + 1):
    if x - k * (n - 1) >= 0 and x <= C:
        ans = x
print(ans)
```

왜: 어떤 가정도 통과하지 못하는 입력에서 `-1`을 내야 하는데, 초기값 0이 그대로 출력되어 "가능하고 답은 0"으로 오해된다.

```python
# ✅ 고친 코드
ans = -1                          # 한 번도 갱신 안 되면 불가능
for x in range(0, C + 1):
    if x - k * (n - 1) >= 0 and x <= C:
        ans = x
print(ans)
```

**7) 가정을 두 개 겹쳐서 훑기**

```python
# ❌ 틀린 코드
for x in range(0, V + 1):
    for y in range(0, V + 1):     # y는 x가 정해지면 이미 결정되는데도 훑는다
        if ok(x, y):
            best = pick(best, x, y)
```

왜: `y`가 규칙으로 `x`에서 계산되는 값이라면 두 번째 반복은 전부 낭비다. `O(V·n)`이면 되는 것이 `O(V²·n)`이 되어 시간 초과가 난다.

```python
# ✅ 고친 코드
for x in range(0, V + 1):
    y = derive(x)                 # 규칙으로 바로 계산 → 자유도 1개
    if ok(x, y):
        best = pick(best, x, y)
```

**다음 챕터로**

- 다음 챕터는 "탐색"보다 **"분류"** 에 초점이 있다. 하나의 문제를 서로 겹치지 않고 빠짐없는 케이스로 쪼개는 법을 배운다.
- 이번 챕터의 이벤트 스캔·구간 겹침은 다음 챕터의 "구간 겹침 정리·포함-배제"로 곧장 이어진다. 경계에서 `<`를 쓸지 `<=`를 쓸지 정하는 습관을 그대로 가져가면 된다.
