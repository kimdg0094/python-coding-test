## L6. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 챕터의 한 문장 요약은 **"하나의 문제를 케이스로 쪼개되, 빠짐없이(Exhaustive) 겹치지 않게(Exclusive) 쪼갠다"** 이다. 이 두 조건을 합쳐 MECE라고 부른다.
- 겹치면 같은 상황을 두 번 세고, 빠지면 어떤 입력에서 아무 분기에도 안 걸린다. 둘 다 **특정 입력에서만 틀리는 버그**라 대표 예제로는 잘 안 잡힌다.

**개념 지도**

```text
                one problem  ->  split into CASES
                              |
              MECE : no overlap  +  no gap
                              |
    +-------------+-----------+-----------+-------------+
    |             |                       |             |
 OVERLAP       REVERSE                  PRUNE       ENUMERATE
  (L1)          (L2)                    (L3)          (L4)
    |             |                       |             |
 |A U B| =     observed -> cause     drop dominated  list all by
 |A|+|B|                                 options     one clean axis
  -|A & B|     list candidates,       keep frontier       |
    |          filter by each              |         set size 1/2/3
 sort + sweep  observation            exchange       sign + / 0 / -
 for segments       |                 argument       a<b / a=b / a>b
    |               |                     |               |
    v               v                     v               v
 +-------------------------------------------------------------+
 |        combine per-case results -> sum / max / YES-NO        |
 +-------------------------------------------------------------+
```

- L1은 "겹침을 어떻게 한 번만 셀까", L2는 "결과에서 원인을 어떻게 되짚을까", L3은 "볼 필요 없는 후보를 어떻게 버릴까", L4는 "어떤 축으로 케이스를 가를까"를 다룬다.
- 네 갈래 모두 마지막 단계는 같다. **케이스별 답을 하나로 합친다.**

**뼈대 코드**

포함-배제 골격 — 두 조건이 겹칠 때.

```python
N = 20
a, b = 3, 5                       # ← 문제마다 바뀜(두 조건)

import math
lcm = a * b // math.gcd(a, b)     # 두 조건을 동시에 만족하는 것의 주기
cnt = N // a + N // b - N // lcm  # |A| + |B| - |A & B|
print(cnt)
```

두 구간의 겹침 판정과 교집합·합집합 길이 골격.

```python
a1, a2 = 0, 5                     # 구간 A = [a1, a2)
b1, b2 = 3, 8                     # 구간 B = [b1, b2)

L = max(a1, b1)                   # 겹침 후보의 왼쪽 끝
R = min(a2, b2)                   # 겹침 후보의 오른쪽 끝
if L < R:                         # 반열린 구간이면 '<' (닫힌 구간이면 '<=')
    inter = R - L
else:
    inter = 0
union = (a2 - a1) + (b2 - b1) - inter
print(inter, union)
```

구간 여러 개의 합집합 길이 — 정렬 후 스위핑 골격.

```python
segs = [(1, 4), (2, 6), (8, 10)]  # ← 문제마다 바뀜

segs.sort()                       # 왼쪽 끝 기준 정렬이 전제 조건
total = 0
cover_end = -1                    # 지금까지 덮은 오른쪽 끝
for L, R in segs:
    if R <= cover_end:            # 이미 통째로 덮인 구간 → 기여 0
        continue
    start = L if L > cover_end else cover_end
    total += R - start            # 새로 덮이는 부분만 더한다
    cover_end = R
print(total)
```

MECE 케이스 분기 골격 — 축을 하나 정하고 `else`로 닫는다.

```python
a, b, c = 3, 3, 6                 # ← 문제마다 바뀜

kinds = len({a, b, c})            # ← 문제마다 바뀜(케이스를 가르는 축)
if kinds == 1:                    # 케이스 1: 모두 같음
    ans = 10000 + a * 1000        # ← 문제마다 바뀜
elif kinds == 2:                  # 케이스 2: 정확히 둘만 같음
    same = a if [a, b, c].count(a) == 2 else (b if [a, b, c].count(b) == 2 else c)
    ans = 1000 + same * 100       # ← 문제마다 바뀜
else:                             # 케이스 3: 모두 다름 (else로 빠짐 방지)
    ans = max(a, b, c) * 100      # ← 문제마다 바뀜
print(ans)
```

역추론 골격 — 후보를 세우고 관찰로 걸러낸다.

```python
lo, hi = 0, 100                   # ← 문제마다 바뀜(원인의 후보 범위)
obs = [(4, 0), (6, 2)]            # ← 문제마다 바뀜(관찰들)

cands = []
for x in range(lo, hi + 1):
    ok = True
    for t, w in obs:
        if forward(x, t) != w:    # ← 문제마다 바뀜(정방향 규칙)
            ok = False
            break
    if ok:
        cands.append(x)

if len(cands) == 0:
    print(-1)                     # 불가능
elif len(cands) == 1:
    print(cands[0])               # 유일하게 복원됨
else:
    print(*cands)                 # 여러 개 — 문제가 요구하는 형식으로
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 조건 두세 개가 동시에 참일 수 있음 | 포함-배제 | 겹친 부분을 정확히 한 번만 뺌 | 조건 k개면 O(2^k) |
| 구간이 겹칠 때 "덮인 총 길이" | 정렬 + 스위핑(cover_end) | 좌표가 커도 메모리 안 씀 | O(M log M) |
| 좌표 범위가 작고 구간이 많음 | 칠하기 배열(누적) | 구현이 훨씬 단순 | O(범위 + M) |
| 두 구간이 겹치는지 한 번 판정 | `max(a1,b1) < min(a2,b2)` | 여섯 배치를 부등식 하나로 | O(1) |
| 결과만 주고 원인을 물음 | 역추론(방정식 또는 후보 검증) | 정방향 규칙을 뒤집음 | O(1) ~ O(후보 수) |
| 후보 전략이 많지만 대부분 손해 | 지배 제거(파레토 프론티어) | 모든 축에서 나쁜 선택은 볼 필요 없음 | O(n log n) |
| 정렬 순서만 정하면 답이 나옴 | 그리디 + 교환 논증으로 정당화 | 바꿔치기해도 나빠지지 않음을 보임 | O(n log n) |
| 상황이 몇 가지 굵직한 유형으로 갈림 | MECE 케이스 분기 | 각 케이스 안에서 문제가 단순해짐 | O(케이스 수 × 처리) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: MECE의 두 조건이 각각 무엇을 막아 주는지(중복 계산 / 처리 누락).
- [ ] 설명할 수 있다: `|A ∪ B| = |A| + |B| − |A ∩ B|`에서 왜 교집합을 정확히 한 번만 빼는지.
- [ ] 설명할 수 있다: 두 구간의 상대 배치가 왜 여섯 가지뿐인지, 그중 겹치는 것이 어느 넷인지.
- [ ] 설명할 수 있다: 겹침 판정이 왜 `max(a1,b1) < min(a2,b2)` 하나로 끝나는지(부정으로 뒤집어 유도).
- [ ] 설명할 수 있다: 반열린 구간 `[s, e)`와 닫힌 구간 `[s, e]`에서 경계 부호가 `<`와 `<=`로 갈리는 이유.
- [ ] 설명할 수 있다: 교집합 길이가 왜 `max(0, min(a2,b2) − max(a1,b1))`인지.
- [ ] 설명할 수 있다: 구간 합집합 스위핑에서 정렬이 왜 반드시 선행되어야 하는지.
- [ ] 설명할 수 있다: 완전히 덮인 구간을 `continue`로 넘기지 않으면 무슨 일이 생기는지.
- [ ] 설명할 수 있다: 역추론에서 후보가 0개일 때와 2개 이상일 때 각각 무엇을 답해야 하는지.
- [ ] 설명할 수 있다: 어떤 선택이 "지배당한다"는 말의 정의와, 지배당한 후보를 버려도 되는 이유.
- [ ] 설명할 수 있다: 회의실 문제에서 왜 "끝나는 시각"으로 정렬하는지를 교환 논증으로.
- [ ] 설명할 수 있다: `if / elif / else` 사슬이 중복은 자동으로 막지만 빠짐은 막지 못하는 이유.
- [ ] 설명할 수 있다: 케이스 분류가 옳은지 검사하는 방법(케이스별 개수의 합 = 전체 개수).

**⚠️ 자주 하는 실수**

**1) 겹침 판정의 경계 부호를 잘못 고르기**

```python
# ❌ 틀린 코드
if max(a1, b1) <= min(a2, b2):    # 반열린 구간 [s, e)인데 등호를 허용
    print("overlap")
```

왜: `[0,5)`와 `[5,9)`는 실제로 만나지 않는데 `max = 5`, `min = 5`라 `5 <= 5`가 참이 되어 겹쳤다고 판정한다. 겹친 길이가 0인 경우를 겹침으로 세는 것이다.

```python
# ✅ 고친 코드
if max(a1, b1) < min(a2, b2):     # 겹친 길이가 0보다 클 때만 겹침
    print("overlap")
```

닫힌 구간 `[s, e]`끼리 "점 하나만 닿아도 겹침"이라고 정의한 문제라면 `<=`가 맞다. **먼저 구간의 정의를 못박고 부호를 고른다.**

**2) 포함-배제에서 교집합을 빼지 않기**

```python
# ❌ 틀린 코드
print(N // 3 + N // 5)            # 3의 배수 개수 + 5의 배수 개수
```

왜: 15의 배수는 3의 배수이면서 5의 배수라 두 항에 모두 들어가 두 번 세어진다. `N = 15`면 5 + 3 = 8이 나오지만 실제 개수는 7이다.

```python
# ✅ 고친 코드
print(N // 3 + N // 5 - N // 15)  # 겹친 15의 배수를 정확히 한 번 뺀다
```

**3) 정렬 없이 스위핑하고, 덮인 구간을 걸러내지 않기**

```python
# ❌ 틀린 코드
total = 0
cover_end = -1
for L, R in segs:                 # 정렬하지 않았다
    total += R - max(L, cover_end)
    cover_end = R
```

왜: 정렬하지 않으면 앞 구간에 통째로 포함되는 구간이 뒤에 올 수 있다. 그때 `R - max(L, cover_end)`가 음수가 되어 총합이 깎이고, `cover_end`도 뒤로 후퇴한다.

```python
# ✅ 고친 코드
segs.sort()
total = 0
cover_end = -1
for L, R in segs:
    if R <= cover_end:            # 이미 다 덮임 → 기여 0
        continue
    total += R - max(L, cover_end)
    cover_end = R
```

**4) 경계 케이스가 통째로 빠짐(gap)**

```python
# ❌ 틀린 코드
if d2 > s:
    print(0)                      # 서로 밖에 떨어짐
elif d2 < diff:
    print(-1)                     # 한 원이 다른 원 안에 있음
else:
    print(2)                      # 두 점에서 만남
```

왜: 접하는 두 경계(`d2 == s`인 외접, `d2 == diff`인 내접)가 `else`에 묻혀 전부 `2`로 나온다. 접하는 입력을 넣기 전까지는 멀쩡해 보인다.

```python
# ✅ 고친 코드
if d2 > s:
    print(0)
elif d2 == s:
    print(1)                      # 외접
elif d2 < diff:
    print(-1)
elif d2 == diff:
    print(1)                      # 내접
else:
    print(2)
```

**5) 케이스가 서로 겹쳐서 이중 계산(MECE 위반)**

```python
# ❌ 틀린 코드
less = 0
greater = 0
for x in arr:
    if x <= p:
        less += 1
    if x >= p:
        greater += 1              # x == p 가 양쪽에 모두 들어간다
print(less + greater)             # 합이 n을 넘는다
```

왜: `x <= p`와 `x >= p`는 `x == p`에서 겹친다. 빠짐은 없지만 중복이 있어 MECE가 아니고, 케이스별 개수의 합이 전체 개수와 어긋난다.

```python
# ✅ 고친 코드
less = 0
equal = 0
greater = 0
for x in arr:
    if x < p:
        less += 1
    elif x == p:
        equal += 1
    else:
        greater += 1
print(less + equal + greater)     # 항상 정확히 n
```

**6) 등호를 잘못 넣어 조건 하나가 뒤집힘**

```python
# ❌ 틀린 코드
x, y, z = sorted((a, b, c))
if x + y >= z:                    # 삼각형 판정
    print("YES")
else:
    print("NO")
```

왜: `x + y == z`이면 세 점이 한 직선 위에 놓여 넓이가 0이다. `3 4 5`처럼 명백한 예제는 통과하지만 `1 2 3`에서만 틀린다.

```python
# ✅ 고친 코드
x, y, z = sorted((a, b, c))
if x + y > z:                     # 등호는 일직선이므로 제외
    print("YES")
else:
    print("NO")
```

**7) 최솟값 변수를 0으로 초기화**

```python
# ❌ 틀린 코드
best = 0                          # 두 그룹 차이의 최솟값을 담을 변수
for mask in range(1 << n):
    h = 0
    for i in range(n):
        if mask & (1 << i):
            h += w[i]
    d = abs(S - 2 * h)
    if d < best:
        best = d
print(best)
```

왜: 차이 `d`는 항상 0 이상이라 `d < 0`이 결코 참이 되지 않는다. 한 번도 갱신되지 않고 언제나 0이 출력된다. "최댓값을 0으로 초기화해 음수 답을 놓치는" 실수의 정확히 반대편이다.

```python
# ✅ 고친 코드
best = None                       # 또는 최댓값이 될 수 있는 값(예: S)으로
for mask in range(1 << n):
    h = 0
    for i in range(n):
        if mask & (1 << i):
            h += w[i]
    d = abs(S - 2 * h)
    if best is None or d < best:
        best = d
print(best)
```

**다음 챕터로**

- 케이스를 MECE로 가르는 습관은 이후 모든 챕터의 기본기가 된다. 구현·시뮬레이션에서는 "규칙이 갈리는 지점"이, 그래프·DP에서는 "마지막 선택을 무엇으로 쪼갤 것인가"가 곧 케이스 분류다.
- 구간 겹침 판정과 정렬 후 스위핑은 이후 좌표 압축·이벤트 처리 문제에서 그대로 재등장한다. 여섯 가지 배치 그림과 `max(a1,b1) < min(a2,b2)` 하나는 반드시 외워 두자.
