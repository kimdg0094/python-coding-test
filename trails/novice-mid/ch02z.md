## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

**개념 지도**

재귀는 문법이 아니라 **구조**다. 아래 한 장에 이 챕터의 전부가 들어 있다 — 반드시 필요한 세 부분, 값을 돌려주느냐 마느냐, 그리고 한 번에 얼마나 줄이느냐.

```text
                    +---------------------+
                    |      recursion      |
                    +----------+----------+
             +-----------------+-----------------+
             |                                   |
       3 required parts                    2 return shapes
             |                                   |
   1. base case : stop here            void  : print / update
   2. shrink    : get closer           value : return + combine
   3. combine   : build the answer     both  : same 3 parts
             |                                   |
             +-----------------+-----------------+
                               |
              +----------------+----------------+
              |                |                |
        shrink by 1      shrink by half    two branches
        depth n          depth log n       depth n, 2^n calls
        n-1, n//10       b//2, (lo+hi)//2  f(n-1) + f(n-2)
        O(n)             O(log n)          O(2^n) without memo
```

세 부분 중 하나라도 빠지면 재귀는 성립하지 않는다. 그리고 "한 번에 얼마나 줄이는가"가 곧 복잡도와 재귀 깊이를 결정한다. 값을 돌려주는 재귀는 언제나 아래 두 방향 운동으로 읽는다.

```text
   unfold  f(4) -> f(3) -> f(2) -> f(1)          # shrink each step
                                     |
                                     v base case
   fold    24  <-   6  <-   2  <-   1            # combine on the way back
```

**뼈대 코드**

재귀 문제를 만나면 아래 골격 중 하나를 고른 뒤, 종료 조건·축소·결합 세 자리만 채운다.

```python
# 1) 값을 반환하지 않는 재귀 — 출력·상태 변경이 목적
def rec(cur, n):
    if cur > n:                    # ← 문제마다 바뀜: 종료 조건
        return
    print(cur)                     # ← 재귀 '앞'에 두면 정방향(작은 것부터)
    rec(cur + 1, n)                # ← 문제마다 바뀜: 축소 규칙
    # print(cur)                   # ← 여기로 옮기면 역방향(큰 것부터)
```

```python
# 2) 값을 반환하는 재귀(한 갈래) — 부분 답 하나를 받아 조합
def rec(n):
    if n <= 1:                     # ← 문제마다 바뀜: 가장 작은 경우
        return 1                   # ← 그 경우의 정확한 답(여기가 틀리면 전부 틀림)
    sub = rec(n - 1)               # ← 문제마다 바뀜: 축소
    return n * sub                 # ← 문제마다 바뀜: 결합 연산
```

```python
# 3) 두 갈래 재귀 — 부분 답 둘을 합친다
def ways(n):
    if n < 0:
        return 0                   # ← 범위를 벗어난 갈래는 0으로 막는다
    if n == 0:
        return 1                   # ← 도착 한 가지
    return ways(n - 1) + ways(n - 3)   # ← 결합: 더하기·최댓값·논리합 등
```

```python
# 4) 절반 축소(분할 정복) — 깊이가 log n이라 안전하다
def solve(arr, lo, hi):
    if lo == hi:                   # ← 원소 하나면 답이 명백
        return arr[lo]
    mid = (lo + hi) // 2
    left = solve(arr, lo, mid)     # 구간을 [lo, mid], [mid+1, hi]로 나눔
    right = solve(arr, mid + 1, hi)
    return left if left > right else right   # ← 문제마다 바뀜: 결합 연산
```

```python
# 5) 문자열·자릿수 축소 — 한 조각을 떼고 나머지를 맡긴다
def rev(s):
    if len(s) <= 1:                # ← 종료 조건
        return s
    return rev(s[1:]) + s[0]       # ← 축소 + 결합

def digit_sum(n):
    if n < 10:                     # ← 한 자리만 남으면 그것이 답
        return n
    return n % 10 + digit_sum(n // 10)
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 출력·전역 갱신만 하면 된다 | 반환 없는 재귀 | 위로 올릴 값이 없다 | 시간 O(호출 수), 공간 O(깊이) |
| 작은 것부터 처리·출력 | 일 처리를 재귀 호출 **앞**에 | 펼치며 처리된다 | O(n) |
| 큰 것부터 처리·출력 | 일 처리를 재귀 호출 **뒤**에 | 접히며 처리된다 | O(n) |
| 부분 답을 모아 답을 만든다 | 반환 있는 재귀 | 결합 연산으로 조립 | O(호출 수) |
| 한 걸음씩 줄어든다 | `n-1`, `n//10`, `s[1:]` | 자연스러운 축소 | O(n), 깊이 n |
| 절반씩 줄어든다 | `b//2`, `(lo+hi)//2` | 깊이가 log n으로 얕다 | O(log n) 또는 O(n) 방문 |
| 갈래가 둘이고 겹친다 | 재귀만으로는 위험 | 같은 부분 문제를 반복 계산 | O(2^n) — 이후 메모이제이션 필요 |
| 축소 인자가 배열의 일부다 | 리스트가 아니라 `lo`, `hi` 인덱스 | 슬라이싱은 매번 복사한다 | 인덱스 O(1) vs 슬라이스 O(n) |
| 깊이가 1000을 넘을 것 같다 | 반복문 또는 절반 축소 | 파이썬 재귀 깊이 한계 | — |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 재귀의 세 요소(종료 조건·문제 축소·결합)와, 각각을 빼면 무엇이 깨지는지.
- [ ] 설명할 수 있다: 종료 조건이 없으면 왜 멈추는 게 아니라 `RecursionError`가 나는지.
- [ ] 설명할 수 있다: 종료 조건이 있어도 축소가 없으면 왜 여전히 무한 재귀인지.
- [ ] 설명할 수 있다: 호출이 쌓이는 펼침과 값이 되돌아오는 접힘을 그림으로.
- [ ] 설명할 수 있다: 일 처리를 재귀 호출 앞에 두느냐 뒤에 두느냐로 출력 순서가 뒤집히는 이유.
- [ ] 설명할 수 있다: 재귀 호출 앞에 `return`을 빠뜨리면 왜 `None`이 새어 나오는지.
- [ ] 설명할 수 있다: 종료 조건의 반환값이 틀리면 왜 최종 답 전체가 무너지는지.
- [ ] 설명할 수 있다: "부분 답을 이미 안다고 가정한다"는 사고가 수학적 귀납법과 같은 구조라는 것.
- [ ] 설명할 수 있다: `fact(4)`를 (깊이, 인자, 반환값) 표로 끝까지 손으로 추적하는 과정.
- [ ] 설명할 수 있다: 한 갈래 재귀가 O(n)이고 두 갈래 재귀가 왜 O(2^n)에 가까워지는지.
- [ ] 설명할 수 있다: 매번 절반으로 줄이면 왜 호출 횟수가 O(log n)이 되는지.
- [ ] 설명할 수 있다: 재귀가 반복문보다 O(깊이)만큼 추가 공간을 쓰는 이유.
- [ ] 설명할 수 있다: 배열을 슬라이스로 넘기지 않고 인덱스 `lo`, `hi`로 넘기는 이유.

**⚠️ 자주 하는 실수**

**1) 종료 조건을 아예 빠뜨린다**

```python
# ❌ 틀린 코드
def count_up(cur, n):
    print(cur)
    count_up(cur + 1, n)     # 멈출 조건이 없다
```

왜: 호출마다 스택 프레임이 쌓이는데 되돌아올 지점이 없다. 파이썬은 깊이가 약 1000을 넘는 순간 `RecursionError`를 던지며 프로그램을 끝낸다.

```python
# ✅ 고친 코드
def count_up(cur, n):
    if cur > n:              # 종료 조건 먼저
        return
    print(cur)
    count_up(cur + 1, n)
```

**2) 종료 조건은 있는데 인자가 줄지 않는다**

```python
# ❌ 틀린 코드
def s(n):
    if n == 1:
        return 1
    return n + s(n)          # 같은 n을 다시 넘긴다 → 종료 조건에 영영 못 닿음
```

왜: 종료 조건과 축소는 짝이다. 매 호출이 종료 조건 쪽으로 한 걸음이라도 다가가지 않으면, 조건이 있어도 그 자리를 지나칠 수 없다.

```python
# ✅ 고친 코드
def s(n):
    if n == 1:
        return 1
    return n + s(n - 1)      # 매 호출마다 1씩 작아진다
```

**3) 재귀 호출 앞에 `return`을 빠뜨린다**

```python
# ❌ 틀린 코드
def fact(n):
    if n <= 1:
        return 1
    n * fact(n - 1)          # 계산만 하고 돌려주지 않는다

print(fact(5))               # None
```

왜: `return`이 없는 갈래는 `None`을 돌려준다. 곱셈 결과는 계산되자마자 버려지고, 호출자는 `None`을 받는다. 재귀에서는 **모든 갈래가 값을 반환**해야 한다.

```python
# ✅ 고친 코드
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)
```

**4) 종료 조건의 반환값이 틀렸다**

```python
# ❌ 틀린 코드
def fact(n):
    if n <= 1:
        return 0             # 0! = 1인데 0을 돌려준다
    return n * fact(n - 1)

print(fact(4))               # 0
```

왜: 최종 답은 종료 조건의 값 위에 연산을 쌓아 만든 것이다. `4 * 3 * 2 * 0`은 무조건 0이 된다. 가장 작은 사례를 손으로 검산하는 이유가 이것이다.

```python
# ✅ 고친 코드
def fact(n):
    if n <= 1:
        return 1             # 0! = 1! = 1
    return n * fact(n - 1)
```

**5) 역방향 출력인데 일 처리를 재귀 앞에 둔다**

```python
# ❌ 틀린 코드
def stars(cur, n):
    if cur > n:
        return
    print("*" * cur)         # 재귀보다 먼저 출력 → 1개짜리 줄이 맨 위
    stars(cur + 1, n)
```

왜: 재귀 앞의 코드는 펼치며(작은 인자부터) 실행되고, 뒤의 코드는 접히며(큰 인자부터) 실행된다. 출력 순서를 뒤집고 싶으면 코드의 위치를 바꾸면 된다.

```python
# ✅ 고친 코드
def stars(cur, n):
    if cur > n:
        return
    stars(cur + 1, n)        # 끝까지 내려간 뒤
    print("*" * cur)         # 돌아오면서 출력 → n개짜리 줄이 맨 위
```

**6) 절반 축소인데 같은 재귀를 두 번 부른다**

```python
# ❌ 틀린 코드
def power(a, b):
    if b == 0:
        return 1
    if b % 2 == 0:
        return power(a, b // 2) * power(a, b // 2)   # 같은 값을 두 번 계산
    return a * power(a, b - 1)
```

왜: 호출이 매 단계 두 갈래로 갈라지므로 절반으로 줄인 이득이 사라진다. 호출 트리의 노드 수가 다시 b에 비례해 O(b)가 된다.

```python
# ✅ 고친 코드
def power(a, b):
    if b == 0:
        return 1
    if b % 2 == 0:
        half = power(a, b // 2)      # 한 번만 계산해 변수에 담는다
        return half * half
    return a * power(a, b - 1)
```

**7) 배열을 슬라이스로 잘라 넘긴다**

```python
# ❌ 틀린 코드
def find_max(arr):
    if len(arr) == 1:
        return arr[0]
    mid = len(arr) // 2
    left = find_max(arr[:mid])       # 매 호출마다 리스트를 통째로 복사
    right = find_max(arr[mid:])
    return left if left > right else right
```

왜: 슬라이싱은 새 리스트를 만든다. 각 단계에서 원소 n개를 복사하고 단계가 log n개이므로, 비교 자체는 O(n)인데 복사 때문에 O(n log n) 시간·공간이 추가로 든다.

```python
# ✅ 고친 코드
def find_max(arr, lo, hi):
    if lo == hi:
        return arr[lo]
    mid = (lo + hi) // 2
    left = find_max(arr, lo, mid)    # 복사 없이 인덱스만 넘긴다
    right = find_max(arr, mid + 1, hi)
    return left if left > right else right
```

**다음 챕터로**

- Ch3의 정렬은 "절반으로 나눠 각각 풀고 합친다"는 이 챕터의 분할 정복 골격 위에 서 있다. 파이썬 정렬이 O(N log N)인 이유도 "절반씩 log N번 나눈다"는 같은 셈에서 나온다.
- 값을 반환하는 재귀에서 "부분 답을 어떤 연산으로 합칠지" 정하던 감각은, 정렬에서 "무엇을 기준으로 비교할지(`key`)"를 정하는 감각으로 이어진다.
