## L5. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

**개념 지도**

Ch3은 "어떤 도구로 정렬하나"와 "무엇을 기준으로 정렬하나"라는 두 축으로 이루어져 있다. 도구는 두 개뿐이고, 기준은 `key`가 전부다.

```text
                   +---------------------+
                   |       sorting       |
                   +----------+----------+
            +-----------------+-----------------+
            |                                   |
      which tool                          which order
            |                                   |
   sorted(a) : returns a new list      key=f        : what to compare
   a.sort()  : in place, returns None  reverse=True : flip everything
            |                                   |
            +-----------------+-----------------+
                              |
             +----------------+----------------+
             |                |                |
       single value    object (tuple)    many criteria
       a[0], a[-1]     (name, score)     key=lambda x:
       a[k-1], a[n//2] fields stay glued   (-x[1], x[0])
             |                |                |
             +----------------+----------------+
                              |
                              v
                stable sort : ties keep input order
```

`key`를 어떻게 줄지는 "기준이 몇 개이고 방향이 무엇인가"만 물으면 정해진다.

```text
   how many criteria?
        |
        +-- one, ascending   --> sort()
        +-- one, descending  --> sort(reverse=True)
        +-- two or more      --> sort(key=lambda x: (k1, k2, ...))
                                 numbers : put '-' on descending keys
                                 input order ties : leave it to stability
```

**뼈대 코드**

```python
# 1) 기본 — 정렬해 두면 원하는 값이 인덱스에 고정된다
n = int(input())
a = list(map(int, input().split()))
a.sort()                              # 원본을 오름차순으로(반환값을 받지 않는다)
print(a[0], a[-1], a[n // 2])         # ← 문제마다 바뀜: 최소·최대·중앙값 등
print(*sorted(set(a)))                # 중복 제거가 필요하면 set 후 다시 정렬
```

```python
# 2) 객체(튜플) 다중 기준 정렬 — 실전 정렬 문제의 대부분
items = []
for _ in range(n):
    parts = input().split()
    items.append((parts[0], int(parts[1])))     # ← 문제마다 바뀜: 필드 구성

items.sort(key=lambda x: (-x[1], x[0]))         # ← 1순위 점수 내림, 2순위 이름 오름
for name, score in items:
    print(name, score)
```

```python
# 3) key 패턴 모음 — 규칙을 말로 적은 뒤 그대로 옮긴다
sorted(a, key=lambda x: x[1])                   # 한 필드 오름차순
sorted(a, key=lambda x: -x[1])                  # 한 필드 내림차순(숫자만 가능)
sorted(a, key=lambda x: (x[1], x[0]))           # 1순위 오름 → 2순위 오름
sorted(a, key=lambda x: (-x[1], x[0]))          # 1순위 내림 → 2순위 오름
sorted(a, key=lambda x: (x[0], -x[1], x[2]))    # 3순위까지 방향 섞기
sorted(w, key=lambda s: (len(s), s))            # 계산 키: 길이 먼저, 같으면 사전순
sorted(p, key=lambda q: q[0] ** 2 + q[1] ** 2)  # 계산 키: 원점에서의 거리
sorted(w, key=len)                              # 함수 이름만 넘기는 형태
```

```python
# 4) 정렬 후 인접 비교 — 이웃끼리만 보면 O(N)에 끝난다
a.sort()
best = a[1] - a[0]                    # ← 문제마다 바뀜: 초깃값
for i in range(len(a) - 1):           # i+1을 읽으므로 반드시 -1
    if a[i + 1] - a[i] < best:
        best = a[i + 1] - a[i]
print(best)
```

```python
# 5) 안정성에 맡기는 두 가지 패턴
items.sort(key=lambda x: -x[1])       # 동점은 입력 순서 그대로 → 키에 넣지 않는다

# 굳이 두 번 정렬해야 한다면 '2순위 먼저, 1순위 나중'
items.sort(key=lambda x: x[0])        # 2순위
items.sort(key=lambda x: -x[1])       # 1순위(안정성이 2순위 순서를 보존한다)
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 원본 순서를 나중에 또 쓴다 | `sorted(a)` | 새 리스트를 만들고 원본은 그대로 | O(N log N) + O(N) 공간 |
| 원본이 더 이상 필요 없다 | `a.sort()` | 추가 공간이 거의 없다 | O(N log N) |
| 기준이 하나고 방향을 뒤집는다 | `reverse=True` | 한 번에 통째로 뒤집힌다 | O(N log N) |
| 기준마다 방향이 다르다 | 튜플 `key` + 숫자에 `-` | `reverse`는 전부 뒤집는다 | O(N log N) |
| 문자열을 내림차순으로 | 그 기준이 유일할 때만 `reverse=True` | 문자열에는 `-`를 못 쓴다 | O(N log N) |
| 비교값을 계산해야 한다 | `key=lambda x: 계산식` | `key`는 원소당 한 번만 계산 | 계산 N회 + O(N log N) |
| 동점은 입력 순서 유지 | 키에 넣지 말고 안정성에 맡김 | 파이썬 정렬은 안정 정렬 | O(N log N) |
| k번째로 작은 값 | 정렬 후 `a[k-1]` | 자리가 고정된다 | O(N log N) + O(1) |
| 중복을 없앤 뒤 줄 세운다 | `sorted(set(a))` | `set`은 순서를 보장하지 않는다 | O(N log N) |
| 가장 가까운 두 값 | 정렬 후 인접 차이 최소 | 정렬하면 후보가 이웃뿐 | O(N log N) + O(N) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: `sorted(a)`와 `a.sort()`가 각각 무엇을 반환하고 무엇을 바꾸는지.
- [ ] 설명할 수 있다: `.sort()`가 왜 `None`을 돌려주도록 설계됐는지.
- [ ] 설명할 수 있다: 비교 기반 정렬이 왜 O(N log N)보다 빨라질 수 없는지.
- [ ] 설명할 수 있다: 정렬 뒤 `a[0]`, `a[-1]`, `a[k-1]`, `a[n//2]`가 각각 무엇이 되는지.
- [ ] 설명할 수 있다: `set`으로 중복을 없앤 뒤 왜 반드시 다시 정렬해야 하는지.
- [ ] 설명할 수 있다: `key`가 정렬 방식을 바꾸는 게 아니라 "비교값을 갈아 끼우는" 장치라는 것.
- [ ] 설명할 수 있다: `lambda x: x[1]`이 `def f(x): return x[1]`과 완전히 같은 뜻이라는 것.
- [ ] 설명할 수 있다: 튜플 키가 앞 원소부터 비교되고 같을 때만 다음 칸으로 넘어가는 규칙.
- [ ] 설명할 수 있다: `-값` 트릭이 왜 내림차순이 되는지를 부등호 뒤집기로.
- [ ] 설명할 수 있다: 기준마다 방향이 다를 때 `reverse=True` 하나로는 왜 안 되는지.
- [ ] 설명할 수 있다: 안정 정렬이 무엇이고, 그것이 "동점은 입력 순서"를 왜 공짜로 만들어 주는지.
- [ ] 설명할 수 있다: 안정성 덕분에 "2순위 먼저, 1순위 나중" 두 번 정렬이 튜플 키와 같은 결과를 내는 이유.
- [ ] 설명할 수 있다: `key` 함수가 원소당 한 번만 호출되어 복잡도를 해치지 않는다는 것.

**⚠️ 자주 하는 실수**

**1) `sort()`의 반환값을 받아 쓴다**

```python
# ❌ 틀린 코드
a = [5, 2, 9]
a = a.sort()                 # sort()는 None을 반환한다
print(a[0])                  # TypeError: NoneType은 인덱싱할 수 없다
```

왜: `.sort()`는 원본을 제자리에서 바꾸고 아무것도 돌려주지 않는다. 그 반환값을 다시 대입하면 정렬 결과가 아니라 `None`이 이름에 붙는다.

```python
# ✅ 고친 코드
a = [5, 2, 9]
a.sort()                     # 제자리 정렬은 대입하지 않는다
print(a[0])
# 또는 새 리스트가 필요하면
b = sorted(a)
```

**2) `set`으로 중복만 없애고 정렬을 잊는다**

```python
# ❌ 틀린 코드
a = [5, 3, 3, 1, 5, 2]
print(*set(a))               # 출력 순서가 오름차순이라는 보장이 없다
```

왜: `set`은 값을 해시로 흩어 담기 때문에 넣은 순서도 크기 순서도 유지하지 않는다. 중복 제거와 정렬은 별개의 작업이다.

```python
# ✅ 고친 코드
a = [5, 3, 3, 1, 5, 2]
print(*sorted(set(a)))       # 중복 제거 후 반드시 다시 정렬
```

**3) 방향이 다른 다중 기준을 `reverse=True`로 처리한다**

```python
# ❌ 틀린 코드
# 규칙: 점수 내림차순, 같으면 이름 오름차순
students.sort(key=lambda x: (x[1], x[0]), reverse=True)
# 점수뿐 아니라 이름까지 내림차순이 되어 버린다
```

왜: `reverse=True`는 완성된 순서를 통째로 뒤집는다. 1순위만 뒤집을 수 없으므로 2순위·3순위까지 함께 반대가 된다.

```python
# ✅ 고친 코드
students.sort(key=lambda x: (-x[1], x[0]))   # 숫자 기준에만 '-'를 붙여 개별 지정
```

**4) 다중 기준을 두 번 정렬하는데 순서가 거꾸로다**

```python
# ❌ 틀린 코드
items.sort(key=lambda x: -x[1])   # 1순위를 먼저 정렬하고
items.sort(key=lambda x: x[0])    # 2순위를 나중에 → 1순위가 무너진다
```

왜: 마지막 정렬이 전체 순서를 지배한다. 안정성을 이용해 두 번에 나누려면 "덜 중요한 기준을 먼저, 가장 중요한 기준을 마지막에" 해야 한다.

```python
# ✅ 고친 코드
items.sort(key=lambda x: (-x[1], x[0]))   # 한 번에 튜플 키로 끝내는 편이 안전하다
```

**5) k번째 값의 인덱스를 하나 어긋나게 잡는다**

```python
# ❌ 틀린 코드
a.sort()
print(a[k])                  # k번째로 작은 값을 원했는데 (k+1)번째가 나온다
```

왜: `k`는 1부터 세지만 리스트 인덱스는 0부터 센다. `k = 1`일 때 최솟값은 `a[0]`이다.

```python
# ✅ 고친 코드
a.sort()
print(a[k - 1])              # k=1 → a[0](최소), k=N → a[N-1](최대)
```

**6) 숫자를 문자열인 채로 정렬한다**

```python
# ❌ 틀린 코드
students = []
for _ in range(n):
    parts = input().split()
    students.append((parts[0], parts[1]))   # 점수가 문자열 그대로다
students.sort(key=lambda x: x[1])           # "100" < "9" 로 비교된다
```

왜: 문자열은 사전식으로 비교되므로 첫 글자가 먼저다. `"100"`은 `"9"`보다 앞이 되어 숫자 크기와 결과가 어긋난다.

```python
# ✅ 고친 코드
students.append((parts[0], int(parts[1])))  # 비교 전에 정수로 변환
students.sort(key=lambda x: x[1])
```

**7) `key`에 함수가 아니라 계산 결과를 넘긴다**

```python
# ❌ 틀린 코드
words = ["banana", "fig", "kiwi"]
words.sort(key=len(words))   # len(words)는 숫자 3이라 호출할 수 없다
```

왜: `key`에는 "원소 하나를 받아 비교값을 돌려주는 함수 자체"를 넘겨야 한다. 괄호를 붙이는 순간 함수가 아니라 이미 계산된 값이 되어 버린다.

```python
# ✅ 고친 코드
words.sort(key=len)                  # 함수 이름만(괄호 없이)
words.sort(key=lambda w: len(w))     # 같은 뜻을 lambda로
```

**다음 챕터로**

- 정렬은 그 자체가 답인 경우보다 "정렬해 두면 다음 단계가 쉬워지는" 전처리인 경우가 훨씬 많다. 앞으로 만날 이분 탐색, 구간 문제, 탐욕적 선택은 모두 "정렬된 상태"를 전제로 출발한다.
- 정렬 뒤 이웃끼리만 비교하면 O(N)에 끝나는 패턴은, 나중에 두 포인터·투 포인터류 기법으로 그대로 확장된다.
