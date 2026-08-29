## L3. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터의 내용은 문장 하나로 압축된다 — **키를 계산해서 자리를 만들면, 찾는 일이 세는 일이 아니라 뛰어가는 일이 된다.** 리스트에서 `in`으로 훑던 O(n)이 `set`/`dict`에서 평균 O(1)로 바뀌는 이유가 전부 여기 있다. 아래 지도로 원리와 도구를 한 번에 정리한다.

**개념 지도**

```text
  Ch07 map : key -> number -> slot

  hash(key) % m  ->  bucket index    # 계산 한 번으로 자리가 정해진다
   |
   +-- collision : two keys, one slot
   |     chaining        : hang a list on that slot
   |     open addressing : probe the next free slot
   |
   +-- load factor  a = n / m
   |     a stays small  -> average O(1)
   |     a grows        -> rehash (bigger m, insert everything again)
   |     all in one slot -> worst O(n)
   |
   +-- python built-ins
   |     set         : membership only      x in s
   |     dict        : key -> value         d[k],  d.get(k, 0)
   |     Counter     : key -> count         Counter(arr)
   |     defaultdict : missing key is auto  defaultdict(list)
   |
   +-- key must be immutable
         ok  : int, str, tuple, frozenset
         no  : list, dict, set             # 내용이 바뀌면 자리도 바뀌므로
```

같은 질문을 자료구조만 바꿔 물으면 비용이 이렇게 달라진다.

```text
  same question, different cost

  "is x in here ?"     list    : scan every item        O(n)
                       set     : one hash jump          O(1) average

  "how many x ?"       list    : arr.count(x) each time O(n) each
                       Counter : cnt[x]                 O(1) average

  "what maps to x ?"   two lists + index()              O(n)
                       dict    : d[x]                   O(1) average

  "sorted order ?"     hash    : no order at all        # 해시는 순서를 버린다
                       sorted + bisect                  O(log n)
```

**뼈대 코드**

1) 존재 판정 — `set`으로 "확인 → 추가"

```python
import sys
data = sys.stdin.read().split()
n = int(data[0])
arr = [int(x) for x in data[1:1 + n]]     # ← 파싱은 문제마다 바뀜

seen = set()
for x in arr:
    if x in seen:            # 확인이 먼저
        print(x)             # ← 찾았을 때 할 일은 문제마다 바뀜
        break
    seen.add(x)              # 추가는 나중
else:
    print(-1)                # for가 break 없이 끝났을 때만 실행되는 절
```

2) 빈도 세기 — `Counter` 또는 `dict.get`

```python
from collections import Counter

cnt = Counter(arr)                    # 값 → 등장 횟수를 O(n)에 만든다
print(cnt['zzz'])                     # 없는 키도 0을 돌려준다(에러 없음)

d = {}                                # Counter 없이 직접 세는 형태
for x in arr:
    d[x] = d.get(x, 0) + 1            # 없으면 0에서 시작

best = min(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
                                      # ← 정렬 기준은 문제마다 바뀜
                                      # 빈도 내림차순, 동점이면 키 오름차순
print(best[0])
```

3) 그룹화 — `defaultdict(list)` + 정규화 키

```python
from collections import defaultdict

groups = defaultdict(list)            # 없는 키를 읽으면 빈 리스트가 자동 생성
for s in words:
    key = "".join(sorted(s))          # ← 정규화 키는 문제마다 바뀜
    groups[key].append(s)

print(len(groups))                    # 그룹 개수
for key in sorted(groups):            # 출력 순서가 필요하면 반드시 정렬
    print(key, sorted(groups[key]))
```

4) 매핑·명령 처리와 집합 연산

```python
book = {}                             # 키 → 값 저장소
book['apple'] = 'red'                 # 삽입과 수정이 같은 문법
if 'apple' in book:                   # 존재 확인
    del book['apple']                 # 없는 키를 지우면 KeyError
print(book.get('apple', 'none'))      # 없을 때 기본값

a = set(list_a)
b = set(list_b)
print(sorted(a & b))                  # 교집합 — 출력은 sorted로 순서 고정
print(sorted(a - b))                  # 차집합
print(len(a | b))                     # 합집합 크기
```

5) 튜플 키와 누적합 + `dict` 조합

```python
visited = set()                       # 좌표처럼 값 여러 개가 한 키일 때
x, y = 0, 0
visited.add((x, y))                   # 리스트는 키가 될 수 없어 튜플로 만든다

from collections import defaultdict   # 합이 K인 연속 구간의 개수
freq = defaultdict(int)
freq[0] = 1                           # 누적합 0을 한 번 본 것으로 시작
total, ans = 0, 0
for x in arr:
    total += x
    ans += freq[total - K]            # ← 찾을 값의 정의는 문제마다 바뀜
    freq[total] += 1
print(ans)
```

**언제 무엇을 쓰나**

| 무엇을 묻는 문제인가 | 무엇을 쓰나 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 순서가 의미를 갖고 인덱스로 접근한다 | `list` | 위치 정보를 가진 유일한 자료구조 | 인덱스 O(1) · `in` O(n) |
| "이 값이 있었나?"만 반복해서 묻는다 | `set` | 값에서 자리를 계산해 한 칸만 본다 | 평균 O(1) |
| 중복을 없애고 종류의 개수만 센다 | `set` + `len` | 같은 값은 한 번만 저장된다 | O(n) |
| 두 모음의 겹침·차이를 구한다 | `set` 연산 `&` `-` `\|` | 원소별 O(1) 조회를 n번 반복 | O(n + m) |
| "이 키에 딸린 값"이 필요하다 | `dict` | 키→값 한 방향 매핑이 정확히 그 일 | 평균 O(1) |
| 각 값이 몇 번 나왔는지 센다 | `Counter` | 없는 키도 0이라 초기화 코드가 사라진다 | O(n) |
| 최빈값·상위 k개 빈도를 뽑는다 | `Counter` + 정렬 키 | 빈도표를 만든 뒤 기준만 정하면 끝 | O(n log n) |
| 같은 기준의 원소들을 묶는다 | `defaultdict(list)` | 키가 없을 때 빈 리스트를 자동 생성 | O(n) |
| 키가 좌표처럼 값 여러 개의 조합이다 | `tuple` 키 + `set`/`dict` | 튜플은 불변이라 해시가 된다 | 평균 O(1) |
| 정렬 순서나 범위 질의(x 이상 y 이하) | 해시 말고 정렬 + `bisect` | 해시는 순서 정보를 아예 버린다 | O(log n) |
| 결과를 정해진 순서로 출력해야 한다 | `sorted(집합)` | `set`/`dict`의 순회 순서는 답이 아니다 | O(n log n) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 해시 함수가 키를 어떻게 버킷 번호로 바꾸는지, 그 계산이 왜 한 번이면 되는지.
- [ ] 설명할 수 있다: 충돌이 무엇이고, 체이닝과 개방 주소법이 각각 어떻게 처리하는지.
- [ ] 설명할 수 있다: 적재율 α가 무엇이고, 커지면 왜 느려지는지.
- [ ] 설명할 수 있다: 해시가 왜 평균 O(1)이고 최악 O(n)인지, 그 둘을 가르는 조건이 무엇인지.
- [ ] 설명할 수 있다: 리스트 `in`이 O(n)인데 `set` `in`이 평균 O(1)인 차이가 어디서 오는지.
- [ ] 설명할 수 있다: 왜 리스트는 키가 될 수 없고 튜플은 될 수 있는지.
- [ ] 설명할 수 있다: `d[k]`가 KeyError를 내는 이유와 `d.get`·`defaultdict`가 그 자리를 어떻게 대신하는지.
- [ ] 설명할 수 있다: `Counter` 뺄셈이 대칭이 아닌 이유와 그로 인한 함정.
- [ ] 설명할 수 있다: `set`이 순서를 보장하지 않는 이유와, 출력 시 무엇을 해야 하는지.
- [ ] 설명할 수 있다: 애너그램 묶기처럼 "정규화 키"를 만드는 발상이 왜 해시 문제의 핵심인지.
- [ ] 설명할 수 있다: 정렬·이진탐색이 필요한 문제와 해시로 충분한 문제를 어떻게 구분하는지.
- [ ] 설명할 수 있다: `list` / `set` / `dict` / `Counter` 중 무엇을 고를지, 문제 문장에서 어떤 단어를 보고 판단하는지.

**⚠️ 자주 하는 실수**

**1) 없는 키를 `d[k]`로 읽는다**

```python
# ❌ 틀린 코드
d = {}
for x in arr:
    d[x] = d[x] + 1        # 처음 보는 x에서 KeyError
```

왜: 해시 테이블은 "그 칸에 키가 없다"까지만 알려 준다. 없을 때 무엇을 돌려줄지는 자료구조가 정할 수 없어 파이썬은 예외를 던진다. 기본값이 필요하면 그 의도를 코드에 적어야 한다.

```python
# ✅ 고친 코드
d = {}
for x in arr:
    d[x] = d.get(x, 0) + 1         # 없으면 0에서 시작

from collections import defaultdict
d = defaultdict(int)               # 또는 없는 키를 0으로 자동 생성
for x in arr:
    d[x] += 1
```

**2) 리스트를 키로 쓴다**

```python
# ❌ 틀린 코드
groups = {}
key = sorted(s)                    # sorted()는 리스트를 돌려준다
groups[key] = 1                    # TypeError: unhashable type: 'list'
```

왜: 저장 자리가 `hash(key)`로 정해지는데, 리스트는 나중에 내용이 바뀔 수 있어 해시값을 고정할 수 없다. 자리가 바뀌면 넣어 둔 값을 영영 못 찾으므로 파이썬은 아예 해시를 거부한다.

```python
# ✅ 고친 코드
key = "".join(sorted(s))           # 문자열로 합치거나
key = tuple(sorted(s))             # 튜플로 바꾼다 — 둘 다 불변이라 해시 가능
groups[key] = 1
```

**3) `Counter` 뺄셈이 음수를 버린다는 걸 잊는다**

```python
# ❌ 틀린 코드
from collections import Counter
borrowed = Counter(['python', 'python', 'algo'])
returned = Counter(['python', 'algo', 'algo'])
print(returned - borrowed)         # Counter({'algo': 1}) — 방향이 반대다
```

왜: `Counter` 뺄셈은 개수가 0 이하가 되는 항목을 결과에서 아예 지운다. 그래서 `a - b`와 `b - a`가 대칭이 아니고, 방향을 잘못 쓰면 에러 없이 조용히 다른 답이 나온다.

```python
# ✅ 고친 코드
print(borrowed - returned)         # Counter({'python': 1}) — 빌린 쪽에서 뺀다
```

**4) `set`의 순회 순서를 답으로 쓴다**

```python
# ❌ 틀린 코드
s = set(['banana', 'apple', 'cherry'])
print(' '.join(s))                 # 순서가 보장되지 않는다
```

왜: `set`은 원소를 해시값이 정한 버킷에 흩어 담는다. "넣은 순서"도 "정렬 순서"도 아니다. 로컬에서 우연히 맞아 보여도 값이 조금만 달라지면 순서가 바뀐다.

```python
# ✅ 고친 코드
print(' '.join(sorted(s)))         # 출력 순서가 필요하면 반드시 정렬한다
```

**5) 리스트에 `in`을 반복해서 O(n^2)을 만든다**

```python
# ❌ 틀린 코드
seen = []
for x in arr:
    if x in seen:                  # 리스트 in은 앞에서부터 전부 비교 O(n)
        print(x); break
    seen.append(x)
```

왜: 이 `in` 한 번이 O(n)인데 루프가 n번 돈다. 전체가 O(n^2)이라 n이 10만이면 100억 번 비교로 시간 초과가 난다. 자료구조만 바꾸면 전체가 O(n)이 된다.

```python
# ✅ 고친 코드
seen = set()                       # append → add, 나머지 코드는 그대로
for x in arr:
    if x in seen:
        print(x); break
    seen.add(x)
```

**6) "추가 → 확인" 순서로 뒤집어 쓴다**

```python
# ❌ 틀린 코드
seen = set()
for x in arr:
    seen.add(x)                    # 먼저 넣어 버렸다
    if (T - x) in seen:            # T=8, x=4면 4 하나로 YES가 된다
        print("YES"); break
```

왜: 자기 자신을 짝으로 세게 된다. 배열에 4가 하나뿐인데 `T - 4 = 4`가 방금 넣은 자기 값과 맞아 떨어져 잘못된 YES가 나온다.

```python
# ✅ 고친 코드
seen = set()
for x in arr:
    if (T - x) in seen:            # 확인이 먼저 — 지나온 값들만 후보
        print("YES"); break
    seen.add(x)                    # 추가는 나중
```

**7) 순회 중에 `dict`/`set`의 크기를 바꾼다**

```python
# ❌ 틀린 코드
for k in d:
    if d[k] == 0:
        del d[k]        # RuntimeError: dictionary changed size during iteration
```

왜: 순회 도중 원소가 지워지면 내부 자리 배치가 흐트러져 어디까지 훑었는지 알 수 없게 된다. 파이썬은 조용히 틀리는 대신 즉시 에러를 낸다.

```python
# ✅ 고친 코드
for k in list(d):                  # 키 목록을 먼저 복사해 두고 돈다
    if d[k] == 0:
        del d[k]

d = {k: v for k, v in d.items() if v != 0}   # 또는 새 dict를 만든다
```

**다음 챕터로**

- 해시는 "값 → 자리"를 계산하는 도구라 순서 정보를 버린다. 그래서 정렬된 순서·범위 질의가 필요한 순간 정렬과 이진탐색이 다시 등장한다. 두 도구는 경쟁 관계가 아니라 묻는 질문이 다르다.
- 튜플 키 `set`으로 좌표 방문을 표시하는 패턴은 그래프·탐색 챕터에서 격자 방문 배열과 같은 역할을 한다. 좌표 범위가 아주 넓거나 음수까지 나오는 문제에서는 배열 대신 이 방식이 답이 된다.
