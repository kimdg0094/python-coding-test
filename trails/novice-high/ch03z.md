## L12. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

**개념 지도**

```text
                               sorting
                                  |
                +-----------------+-----------------+
         comparison based                     non-comparison
                |                                   |
         +------+------------+               radix (LSD)
   O(n^2) family     O(n log n) family       bucket by digit
   bubble : swap     merge : split + merge   stable = correctness
   select : pick min quick : partition       O(d * n), space O(n)
   insert : shift    heap  : tree in array   # 키가 고정폭 정수일 때만
   space O(1)        merge stable + O(n)
   n <= 3000         quick, heap : in-place
                |                                   |
                +-----------------+-----------------+
                                  |
   lower bound : n! leaves -> height >= log2(n!) = Omega(n log n)
   Timsort (python sorted / list.sort) = merge + insertion, stable
```

이 챕터의 갈림길은 두 번 열린다.

- 첫 갈림길은 **"값을 서로 비교할 것인가"**다. 비교하는 순간 결정 트리 논증에 걸려 최악 비교 횟수가 n log n 아래로 못 내려간다. 기수 정렬만 이 문을 피해 가는데, 대신 "키가 자릿수를 가진 고정폭"이어야 한다는 값을 치른다.
- 두 번째 갈림길은 비교 정렬 안에서 **"한 번에 얼마나 멀리 보내는가"**다. 인접한 것만 바꾸면(거품·삽입) 한 번에 역위 하나를 지워 O(n²)이 되고, 반씩 쪼개거나(병합·퀵) 트리 높이만큼 뛰면(힙) 한 번에 여러 개를 정리해 O(n log n)이 된다.
- 그 아래에서 실전 선택을 가르는 축은 셋뿐이다 — **안정성**(동점 순서를 지키나), **공간**(임시 배열을 쓰나), **최악 보장**(퀵만 O(n²)로 무너질 수 있다).
- 파이썬의 `sorted`/`list.sort`는 병합 정렬과 삽입 정렬을 합친 Timsort라 이 세 축에서 안정 · O(n) 공간 · O(n log n) 보장을 준다. 그래서 실전 정답은 대개 "직접 짜지 말고 내장 정렬을 쓴다"이고, 직접 짜는 것은 원리를 묻거나 정렬 과정 자체가 답일 때다.

**뼈대 코드**

```python
# 1) O(n^2) 3형제 — 최소 골격
def bubble(a):
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):      # 뒤쪽 i 개는 확정 -> 범위를 줄인다
            if a[j] > a[j + 1]:         # ← '>' 만. '>=' 면 안정성이 깨짐
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:                 # 이번 패스에 교환 0 -> 이미 정렬됨
            break
    return a

def selection(a):
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if a[j] < a[m]:             # ← 인덱스만 갱신, 교환은 밖에서 한 번
                m = j
        a[i], a[m] = a[m], a[i]
    return a

def insertion(a):
    for i in range(1, len(a)):
        key = a[i]                      # 먼저 꺼내 둬야 덮어써도 안 잃는다
        j = i - 1
        while j >= 0 and a[j] > key:    # ← j >= 0 을 앞에 둬야 음수 인덱스 회피
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a
```

```python
# 2) 병합 정렬 — 항상 O(n log n), 안정, 공간 O(n)
def merge_sort(a):
    if len(a) <= 1:
        return a
    m = len(a) // 2
    left, right = merge_sort(a[:m]), merge_sort(a[m:])
    res, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:         # ← '<=' 왼쪽 우선이라 안정
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
            # inv += len(left) - i       # ← 역순쌍 개수를 셀 때만 추가
    res += left[i:]
    res += right[j:]                    # 남은 꼬리를 통째로 (빠뜨리기 쉬움)
    return res
```

```python
# 3) 퀵 정렬 — 이해용 3분할과 실전용 제자리 분할
def quick_simple(a):                    # 읽기 쉬움, 추가 공간 O(n)
    if len(a) <= 1:
        return a
    p = a[len(a) // 2]                  # ← 문제마다 바뀜(피벗 고르는 규칙)
    lo = [x for x in a if x < p]
    eq = [x for x in a if x == p]       # 같은 값을 따로 -> 중복 많아도 안전
    hi = [x for x in a if x > p]
    return quick_simple(lo) + eq + quick_simple(hi)

def partition(a, lo, hi):               # 제자리 분할(Lomuto), 피벗 = a[hi]
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]   # ← i 가 아니라 i+1 (대표적 off-by-one)
    return i + 1

def quick_inplace(a, lo, hi):
    if lo < hi:
        p = partition(a, lo, hi)
        quick_inplace(a, lo, p - 1)     # 피벗 자리는 확정이라 제외
        quick_inplace(a, p + 1, hi)
```

```python
# 4) 힙 — 전체 정렬보다 '극값 반복 추출'에 쓴다
import heapq

def heap_sort(a):
    h = list(a)
    heapq.heapify(h)                    # O(n) 에 힙 구성
    return [heapq.heappop(h) for _ in range(len(h))]

def top_k(a, k):                        # 상위 k 개를 O(n log k) 에
    h = []
    for x in a:
        heapq.heappush(h, x)            # ← 최대 힙이 필요하면 -x 로 넣는다
        if len(h) > k:
            heapq.heappop(h)            # 가장 작은 것을 버려 크기를 k 로 유지
    return sorted(h, reverse=True)
```

```python
# 5) 실전 — sort(key=) 패턴 모음
rows = [("kim", 90, 3), ("lee", 85, 1), ("park", 90, 2)]

rows.sort(key=lambda r: r[1])                  # 제자리 정렬, 반환값은 None
best = sorted(rows, key=lambda r: -r[1])       # 새 리스트, 점수 내림차순

# 다중 기준: 튜플에 순위대로 나열 (숫자는 부호로 방향을 뒤집는다)
sorted(rows, key=lambda r: (-r[1], r[0]))      # ← 문제마다 바뀜(정렬 규칙)

# 방향이 뒤섞여 튜플로 못 쓸 때: 낮은 순위부터 여러 번 안정 정렬
tmp = sorted(rows, key=lambda r: r[0])         # 2순위: 이름 오름차순
res = sorted(tmp, key=lambda r: -r[1])         # 1순위: 점수 내림차순

sorted(rows, key=lambda r: r[1], reverse=True) # 동점의 입력 순서는 유지된다
sorted(set(x for x in [3, 1, 3]))              # 중복 제거 후 정렬
```

**언제 무엇을 쓰나**

정렬 알고리즘 비교표 (n = 원소 수, d = 자릿수)

| 알고리즘 | 평균 | 최악 | 최선 | 추가 공간 | 안정성 | 언제 쓰나 |
|---|---|---|---|---|---|---|
| 거품 | O(n²) | O(n²) | O(n) | O(1) | 안정 | 학습용. 조기 종료가 있어 거의 정렬된 입력에만 |
| 선택 | O(n²) | O(n²) | O(n²) | O(1) | 불안정 | 교환·쓰기 비용이 비교보다 훨씬 비쌀 때(교환 ≤ n-1) |
| 삽입 | O(n²) | O(n²) | O(n) | O(1) | 안정 | n이 작거나 거의 정렬됨. 원소가 하나씩 도착하는 온라인 정렬 |
| 병합 | O(n log n) | O(n log n) | O(n log n) | O(n) | 안정 | 최악까지 보장 필요, 안정성 필요, 역순쌍 세기 |
| 퀵 | O(n log n) | O(n²) | O(n log n) | O(log n) | 불안정 | 평균이 가장 빠름. k번째 값만 필요하면 quickselect |
| 힙 | O(n log n) | O(n log n) | O(n log n) | O(1) | 불안정 | 최악 보장 + 제자리. 상위 k개, 우선순위 처리 |
| 기수 | O(d·n) | O(d·n) | O(d·n) | O(n) | 안정 | 키가 좁은 범위의 고정폭 정수·문자열 |
| Timsort | O(n log n) | O(n log n) | O(n) | O(n) | 안정 | 파이썬 실전 기본값. 특별한 이유가 없으면 이것 |

상황별 선택 기준

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 그냥 정렬해야 한다 | `sorted` / `list.sort` | 안정 + 최악 보장 + 가장 빠른 실측 | O(n log n) |
| 동점 순서를 입력대로 지켜야 한다 | 안정 정렬(병합·삽입·기수·Timsort) | 불안정 정렬은 동점 순서를 보장 못 함 | O(n log n) |
| 기준이 여러 개고 방향이 뒤섞임 | 낮은 순위부터 여러 번 `sorted` | 안정성이 이전 순서를 남겨 줌 | O(k·n log n) |
| 정렬 과정 자체를 출력해야 한다 | 그 알고리즘을 직접 구현 | 패스별 스냅샷은 내장 정렬로 못 뽑음 | 알고리즘에 따름 |
| n ≤ 수천이고 거의 정렬돼 있다 | 삽입 정렬 | 역위가 적어 실측이 O(n)에 근접 | 최선 O(n) |
| 교환 비용이 압도적으로 크다 | 선택 정렬 | 교환이 최대 n-1번뿐 | 비교 O(n²), 교환 O(n) |
| 최악에도 시간이 보장돼야 한다 | 병합 또는 힙 | 퀵은 피벗이 치우치면 O(n²) | O(n log n) |
| 메모리가 빠듯하다 | 힙 또는 제자리 퀵 | 병합은 O(n) 임시 배열이 필요 | 공간 O(1)~O(log n) |
| 전체가 아니라 상위 k개만 필요 | 크기 k 최소 힙 | 정렬 전체를 만들 필요가 없음 | O(n log k) |
| k번째 값 하나만 필요 | quickselect | 한쪽 구간만 재귀 | 평균 O(n) |
| 키가 0~999999 같은 정수 | 기수 정렬 | 비교를 아예 안 해 하한을 우회 | O(d·n) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 거품·선택·삽입이 왜 O(n²)인가 — (n-1)+(n-2)+…+1의 합으로 유도할 수 있다.
- [ ] 설명할 수 있다: 거품 정렬 안쪽 범위가 왜 `n-1-i`인가.
- [ ] 설명할 수 있다: 선택 정렬만 최선도 O(n²)인 이유(조기 종료가 불가능한 이유).
- [ ] 설명할 수 있다: 삽입 정렬의 이동 횟수가 왜 역위(inversion) 개수와 같은가.
- [ ] 설명할 수 있다: 안정 정렬이 무엇이고, 왜 다단 정렬을 여러 번의 단일 정렬로 쪼갤 수 있게 해 주는가.
- [ ] 설명할 수 있다: 선택·퀵·힙이 왜 불안정한가 — 각각 최소 반례를 하나씩 들 수 있다.
- [ ] 설명할 수 있다: 병합 정렬이 왜 O(n log n)인가 — 레벨당 O(n) × log n 레벨로 유도할 수 있다.
- [ ] 설명할 수 있다: 병합에서 `<=`와 `<`의 차이가 안정성에 미치는 영향.
- [ ] 설명할 수 있다: 퀵 정렬의 최악 O(n²)이 어떤 입력·피벗 조합에서 나오고, 어떻게 피하는가.
- [ ] 설명할 수 있다: 힙이 완전 이진 트리를 배열 하나로 표현하는 방식(부모·자식 인덱스 공식).
- [ ] 설명할 수 있다: 힙 배열이 왜 "정렬된 리스트"가 아닌가.
- [ ] 설명할 수 있다: 기수 정렬에서 안정성이 왜 성능이 아니라 정확성의 문제인가.
- [ ] 설명할 수 있다: 비교 기반 정렬의 하한이 왜 Ω(n log n)인가 — 결정 트리의 잎이 n!개라는 논증으로.
- [ ] 설명할 수 있다: 기수 정렬이 그 하한을 어떻게 피해 가고, 대신 무엇을 전제하는가.
- [ ] 설명할 수 있다: `sorted`와 `list.sort`의 차이(반환값·원본 변경·제자리 여부).

**⚠️ 자주 하는 실수**

**1) 거품 정렬의 안쪽 루프 범위를 잘못 잡는다**

```python
# ❌ 틀린 코드
for i in range(n - 1):
    for j in range(n):
        if a[j] > a[j + 1]:      # j 가 n-1 일 때 a[n] 을 읽는다 -> IndexError
            a[j], a[j + 1] = a[j + 1], a[j]
```

왜: 안쪽 루프는 `a[j]`와 `a[j+1]` 두 칸을 보므로 `j`의 상한이 `n-2`여야 한다. 게다가 패스 `i`가 끝나면 뒤쪽 `i`개는 이미 확정이라 다시 볼 필요도 없다.

```python
# ✅ 고친 코드
for i in range(n - 1):
    for j in range(n - 1 - i):   # -1 은 a[j+1] 때문에, -i 는 확정 구간 때문에
        if a[j] > a[j + 1]:
            a[j], a[j + 1] = a[j + 1], a[j]
```

**2) `sort()`의 반환값을 정렬 결과로 착각한다**

```python
# ❌ 틀린 코드
a = [3, 1, 2]
a = a.sort()                     # list.sort() 는 None 을 반환한다
print(a[0])                      # TypeError: 'NoneType' object is not subscriptable
```

왜: `list.sort()`는 원본을 제자리에서 고치고 `None`을 돌려준다. 새 리스트를 원하면 `sorted`를, 원본을 고치려면 반환값을 받지 말아야 한다.

```python
# ✅ 고친 코드
a = [3, 1, 2]
a.sort()                         # 원본을 제자리 정렬 (반환값을 받지 않는다)
b = sorted(a)                    # 또는 새 리스트가 필요하면 sorted
```

**3) 순회하면서 그 리스트의 길이를 바꾼다**

```python
# ❌ 틀린 코드
for x in a:
    if x < 0:
        a.remove(x)              # 순회 중 길이가 줄어 인덱스가 밀린다
```

왜: `for`는 내부적으로 인덱스를 하나씩 올리는데, 원소를 지우면 뒤가 앞으로 당겨져 다음 원소를 건너뛴다. `[-1, -2, 3]`에서 `-2`가 살아남는다.

```python
# ✅ 고친 코드
a = [x for x in a if x >= 0]     # 새 리스트를 만들거나
a[:] = [x for x in a if x >= 0]  # 원본 객체를 유지해야 하면 슬라이스 대입
```

**4) 제자리 분할에서 피벗 인덱스를 하나 잘못 쓴다**

```python
# ❌ 틀린 코드
def partition(a, lo, hi):
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i], a[hi] = a[hi], a[i]    # i 는 '피벗 이하 구간의 마지막'이다
    return i
```

왜: 루프가 끝난 시점에 `a[lo..i]`는 피벗 이하, `a[i+1..hi-1]`은 피벗 초과다. 피벗이 들어갈 경계 자리는 `i`가 아니라 `i+1`이다. `i`와 바꾸면 피벗보다 작은 값이 오른쪽 구간으로 넘어가 분할이 깨진다.

```python
# ✅ 고친 코드
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1
```

**5) 피벗과 같은 값을 어느 쪽에도 확정하지 않아 재귀가 멈추지 않는다**

```python
# ❌ 틀린 코드
def quick(a):
    if len(a) <= 1:
        return a
    p = a[0]
    lo = [x for x in a if x <= p]    # 피벗 자신도 lo 에 들어간다
    hi = [x for x in a if x > p]
    return quick(lo) + quick(hi)     # a 가 전부 같은 값이면 lo == a -> 무한 재귀
```

왜: `[5, 5, 5]`에서 `lo`가 다시 `[5, 5, 5]`가 되어 구간이 줄지 않는다. 재귀가 같은 크기로 반복되어 `RecursionError`가 난다.

```python
# ✅ 고친 코드
def quick(a):
    if len(a) <= 1:
        return a
    p = a[len(a) // 2]
    lo = [x for x in a if x < p]
    eq = [x for x in a if x == p]    # 같은 값은 여기서 확정하고 재귀하지 않는다
    hi = [x for x in a if x > p]
    return quick(lo) + eq + quick(hi)
```

**6) 비교에 등호를 넣어 안정성을 깬다**

```python
# ❌ 틀린 코드
while j >= 0 and a[j] >= key:    # 같은 값도 넘어가 버린다
    a[j + 1] = a[j]
    j -= 1
```

왜: `key`와 값이 같은 원소까지 밀어내면 `key`가 그 앞으로 가서 동점 원소의 입력 순서가 뒤집힌다. 다단 정렬의 전제가 무너져, 2순위 기준으로 맞춰 둔 순서가 사라진다.

```python
# ✅ 고친 코드
while j >= 0 and a[j] > key:     # 같은 값을 만나면 멈춰 뒤에 놓는다
    a[j + 1] = a[j]
    j -= 1
```

**7) 리스트를 통째로 뒤집어 내림차순을 만든다**

```python
# ❌ 틀린 코드
res = sorted(rows, key=lambda r: r[1])[::-1]   # 동점의 순서까지 뒤집힌다
```

왜: `[::-1]`은 정렬 결과 전체를 뒤집으므로 값이 같은 원소들의 상대 순서도 함께 뒤집힌다. "점수 내림차순, 동점이면 입력 순서"라는 요구를 만족하지 못한다.

```python
# ✅ 고친 코드
res = sorted(rows, key=lambda r: r[1], reverse=True)  # 동점 순서는 유지된다
res = sorted(rows, key=lambda r: -r[1])               # 숫자면 부호 반전도 가능
```

**8) 힙 배열을 정렬된 리스트로 착각한다**

```python
# ❌ 틀린 코드
import heapq
h = [5, 3, 8, 1]
heapq.heapify(h)
print(h)                         # [1, 3, 8, 5] — 정렬돼 있지 않다
```

왜: 힙이 보장하는 것은 "부모 ≤ 자식"뿐이고, 형제끼리의 대소는 아무 규칙이 없다. 루트만 최솟값이다.

```python
# ✅ 고친 코드
import heapq
h = [5, 3, 8, 1]
heapq.heapify(h)
out = [heapq.heappop(h) for _ in range(len(h))]   # 하나씩 꺼내야 정렬 순서
print(out)                       # [1, 3, 5, 8]
```

**다음 챕터로**

- 힙에서 잠깐 만난 "완전 이진 트리 + 배열 인덱스"는 다음 챕터의 트리·힙에서 본격적으로 다룬다. `sift-up`/`sift-down`을 직접 구현하면 이번의 `heapq`가 무엇을 대신해 줬는지 보인다.
- 분할 정복(병합·퀵)의 사고 틀은 이분 탐색과 재귀 문제로 이어진다. "절반씩 줄인다 → log n"이라는 감각이 그대로 재사용된다.
- 정렬은 그 자체보다 전처리로 더 자주 쓰인다. 정렬해 두면 이분 탐색, 투 포인터, 그리디의 교환 논증이 모두 가능해진다는 것이 이 챕터의 실전 결론이다.
