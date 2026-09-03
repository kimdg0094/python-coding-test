## L8. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터의 여섯 레슨은 서로 다른 자료구조를 배운 것처럼 보이지만, 실제로 던진 질문은 하나다. **"이 문제는 컬렉션에게 무엇을 요구하는가?"** 존재 여부만 물으면 해시로 충분하고, 정렬 순서를 계속 물으면 비교 기반 구조가 필요하며, 극단값 하나만 반복해서 꺼낸다면 전체를 정렬할 이유가 없다. 아래에서 그 갈림길을 한 장으로 잇고, 바로 꺼내 쓸 뼈대와 자주 넘어지는 지점을 모은다.

**개념 지도**

챕터 전체는 "컬렉션에 무엇을 요구하는가"라는 한 질문에서 다섯 갈래로 갈라진다. 맨 아랫줄의 복잡도가 곧 그 선택의 가격표다.

```text
                    Ch01 : mid-level containers
                                |
         what does the problem need from the collection ?
                                |
 +-----------+-------------+-------------+-------------+
 |           |             |             |             |
 membership  order kept    one extreme   both ends     neighbors
 frequency   at all times  over and over only          of a node
 |           |             |             |             |
 dict / set  sorted list   heapq         deque         prv / nxt
 L1 , L3     + bisect      L5            (see L6)      L6
             L2 , L4
 |           |             |             |             |
 O(1) avg    O(log n)      O(log n)      O(1) ends     O(1) if the
 unordered   per query     top only      O(n) middle   node is held
```

같은 원소 다섯 개를 세 구조에 담아 보면 차이가 한눈에 보인다. **유지하는 순서가 많을수록 삽입이 비싸진다** — 이 한 문장이 위 지도의 가격표를 설명한다.

```text
  how much order does each structure actually keep ?

  dict / set : none          slot = hash(x) % size
      +----+----+----+----+----+
      |  7 |  1 |  9 |  3 |  5 |
      +----+----+----+----+----+

  heap : only "parent <= child"
              1                    root is the minimum
            /   \                  siblings have no order at all
           3     5                 the maximum is somewhere in a leaf
          / \
         7   9

  sorted list : total order
      +----+----+----+----+----+
      |  1 |  3 |  5 |  7 |  9 |   bisect can search here
      +----+----+----+----+----+

  more order kept   ->   more work per insert
  dict O(1)    <    heap O(log n)    <    sorted list O(n) to shift
```

힙에는 "가운데 원소 하나만 지우기"가 없다. 그 구멍을 메우는 표준 우회가 지연 삭제이고, 이 챕터의 어려운 문제 대부분이 이 패턴 위에 서 있다.

```text
  a heap cannot delete an element in the middle -> lazy deletion

  push (value, id)   and keep   alive = { ids that still count }

  delete id 2                        alive = { 1, 3, 4 }
      heap  [ (3,2) , (5,1) , (9,4) ]
              ^ top is a ghost : id 2 is no longer in alive

  peek : pop while the top id is missing from alive
      heap  [ (5,1) , (9,4) ]
              ^ real top = 5

  every element is pushed once and popped at most once
  -> the cleanup costs O(log n) amortized per operation
```

**뼈대 코드**

1) `heapq` 5종 — 최소/최대, 튜플 우선순위, 상위 K 유지.

```python
import heapq

h = []
heapq.heappush(h, x)                  # 최소 힙: 항상 h[0]이 최솟값 (O(1) peek)
smallest = heapq.heappop(h)
h2 = arr[:]; heapq.heapify(h2)        # 배열이 이미 다 있으면 O(n)에 힙화

maxh = []
heapq.heappush(maxh, -x)              # 최대 힙은 부호를 뒤집어 흉내낸다
largest = -heapq.heappop(maxh)        # 꺼낼 때 반드시 되돌린다

seq += 1
heapq.heappush(h, (pri, seq, obj))    # ← 문제마다 바뀜: 우선순위 키
#                       ^^^ 타이브레이커. obj끼리 비교되는 사고를 막는다

if len(topk) < K:                     # 상위 K개 유지: top이 K개 중 최솟값
    heapq.heappush(topk, x)
elif x > topk[0]:
    heapq.heapreplace(topk, x)        # pop + push를 한 번에
```

2) 두 힙으로 중앙값 — 작은 절반과 큰 절반의 경계 두 개를 O(1)에 본다.

```python
lo, hi = [], []                       # lo: 작은 절반(최대 힙), hi: 큰 절반(최소 힙)

def add(x):
    heapq.heappush(lo, -x)
    heapq.heappush(hi, -heapq.heappop(lo))    # lo의 최대를 hi로 넘겨 경계를 맞춤
    if len(hi) > len(lo):                     # 불변식: len(lo) == len(hi) 또는 +1
        heapq.heappush(lo, -heapq.heappop(hi))

def median():
    if len(lo) > len(hi):
        return -lo[0]
    return (-lo[0] + hi[0]) / 2       # ← 문제마다 바뀜: 짝수 개일 때의 규칙
```

3) `bisect` 4종 — 정렬 배열 위의 모든 경계 질의는 이 두 함수로 만든다.

```python
import bisect
# a는 항상 정렬 상태여야 한다
i = bisect.bisect_left(a, x)          # x 미만 개수 == x 이상인 첫 위치
j = bisect.bisect_right(a, x)         # x 이하 개수 == x 초과인 첫 위치

cnt_x  = j - i                                   # x의 등장 횟수
cnt_LR = bisect.bisect_right(a, R) - bisect.bisect_left(a, L)   # [L, R] 개수
ge     = a[i]   if i < len(a) else None          # x 이상 최솟값 (successor 계열)
le     = a[j-1] if j > 0      else None          # x 이하 최댓값 (predecessor 계열)
```

4) 정렬 리스트로 TreeSet 흉내 — 삽입이 O(n)이라는 대가를 알고 쓴다.

```python
a = []

def add(v):                           # 집합이므로 중복은 넣지 않는다
    i = bisect.bisect_left(a, v)
    if i == len(a) or a[i] != v:
        a.insert(i, v)                # 위치 찾기 O(log n) + 밀기 O(n)

def remove(v):
    i = bisect.bisect_left(a, v)
    if i < len(a) and a[i] == v:
        a.pop(i)                      # 역시 O(n)

kth = a[k-1] if k <= len(a) else None # ← k번째로 작은 값은 인덱스 하나
```

5) `deque` — 양끝만 쓴다면 직접 만들지 않는다.

```python
from collections import deque

dq = deque()
dq.append(x);   dq.appendleft(x)      # 양끝 삽입 O(1)
r = dq.pop();   l = dq.popleft()      # 양끝 삭제 O(1)
window = deque(maxlen=W)              # ← 문제마다 바뀜: 고정 크기 창
# dq[0], dq[-1]은 O(1)이지만 dq[i]는 O(n) — 인덱스 접근이 잦으면 list
```

6) 센티넬 이중 연결 리스트 — 삽입·삭제·복원의 세 줄짜리 정석.

```python
H, T = 0, n + 1                       # 양끝 센티넬 두 칸(경계 분기를 없앤다)
nxt = [i + 1 for i in range(n + 2)]
prv = [i - 1 for i in range(n + 2)]

def link(p, x, q):                    # p와 q 사이에 x를 끼운다 (링크 네 개)
    nxt[p], prv[x] = x, p
    nxt[x], prv[q] = q, x

def unlink(x):                        # x를 뗀다 (링크 두 개, 짝으로 고친다)
    nxt[prv[x]] = nxt[x]
    prv[nxt[x]] = prv[x]              # x의 prv/nxt는 지우지 않고 남겨 둔다

def restore(x):                       # 뗀 것을 제자리로 — 반드시 뗀 역순으로
    nxt[prv[x]] = x
    prv[nxt[x]] = x
```

**언제 무엇을 쓰나**

문제 문장을 "무엇을 묻는가"로 번역하면 자료구조는 거의 자동으로 정해진다. 아래 표의 왼쪽 열을 문제에서 찾는 것이 실제로 하는 일의 전부다.

| 무엇을 묻는 문제인가 | 고르는 것 | 이유 | 주요 연산 복잡도 |
|---|---|---|---|
| "이 값이 있는가"를 수없이 물음 | `set` | 해시가 칸을 계산해 주므로 비교 한 번이면 끝 | `in`·`add`·`discard` 평균 O(1) |
| 중복을 없애고 개수만 세기 | `set` | 같은 값은 같은 칸이라 자동 흡수 | 생성 O(n), `len` O(1) |
| "몇 번 나왔는가"(빈도) | `Counter` | 세기 전용이고 `most_common`까지 딸려 온다 | 생성 O(n), 조회 O(1) |
| "키마다 목록을 모은다"(그룹핑) | `defaultdict(list)` | 없는 키의 초기화가 자동이라 KeyError가 없다 | 접근·추가 평균 O(1) |
| "키 → 값 대응을 읽고 고친다" | `dict` | 저장 위치를 해시로 계산 | 조회·삽입·삭제 평균 O(1) |
| 인덱스로 접근하고 순서대로 훑기만 함 | `list` | 연속 메모리라 `a[i]`가 주소 계산 한 번 | `a[i]` O(1), `in` O(n), 중간 삽입 O(n) |
| "가장 작은 것을 반복해서 꺼낸다" | `heapq` | 뿌리만 최소로 유지하므로 갱신이 높이만큼 | push·pop O(log n), `h[0]` O(1) |
| "가장 큰 것을 반복해서 꺼낸다" | `heapq` + 부호 반전 | 최소 힙만 있으므로 `-x`로 대소를 뒤집음 | push·pop O(log n) |
| "상위 K개만 계속 유지" | 크기 K 최소 힙 | top이 K개 중 최솟값 = 다음 탈락 후보 | 원소당 O(log K) |
| "K번째로 작은 값" | 크기 K 최대 힙 | 작은 K개의 최댓값이 곧 답 | 원소당 O(log K), 조회 O(1) |
| "지금까지의 중앙값" | 최대 힙 + 최소 힙 | 절반씩 나누면 경계의 두 top이 중앙 | 삽입 O(log n), 조회 O(1) |
| "최댓값과 최솟값을 둘 다 지운다" | 두 힙 + 지연 삭제 | 힙 하나로는 반대쪽 극단을 볼 수 없다 | 연산당 분할상환 O(log n) |
| "양끝에서 넣고 뺀다" | `deque` | 양끝 블록만 건드려 원소 이동이 없다 | 양끝 O(1), 중간 O(n) |
| 리스트 앞에서 계속 꺼냄(큐) | `deque.popleft` | `list.pop(0)`은 뒤를 전부 당긴다 | O(1) 대 O(n) |
| "정렬 순서로 k번째 값" | 정렬 리스트 + 인덱스 | 정렬이 유지되면 `a[k-1]`이 그대로 답 | 조회 O(1), 삽입 O(n) |
| "x 이하 최댓값 / x 이상 최솟값" | 정렬 리스트 + `bisect` | 이분탐색이 경계 위치를 직접 준다 | 조회 O(log n), 삽입 O(n) |
| "[L, R] 안에 몇 개인가" | 정렬 리스트 + `bisect` | `right(R) - left(L)`이 곧 개수 | 조회 O(log n) |
| 삽입·삭제가 정렬 질의와 대량으로 섞임 | `SortedList` 또는 좌표압축+BIT | 정렬 리스트의 O(n) 이동이 병목이 된다 | 연산당 O(log n) |
| "삽입 순서를 그대로 유지" | `dict` (3.7+) | dict는 삽입 순서를 보존, `set`은 보장 없음 | 순회 O(n) |
| "어떤 노드의 바로 앞/뒤에 넣고 뺀다" | 이중 연결 리스트(`prv`/`nxt`) | 이웃 링크 몇 개만 고치면 끝 | 삽입·삭제 O(1)(참조 보유 시) |
| "값으로 노드를 찾아 즉시 옮긴다"(LRU) | `dict` + 이중 연결 리스트 | 찾기와 잇기가 둘 다 O(1)이라야 전체가 O(1) | 접근·이동 O(1) |

헷갈리기 쉬운 짝들은 갈림 기준을 한 줄로 못 박아 둔다.

| 헷갈리는 짝 | 갈림 기준 | 결론 |
|---|---|---|
| `set` vs `dict` | 값이 딸려 오는가 | 존재만이면 set, 값이 붙으면 dict |
| `d.get(k, 0)` vs `defaultdict` | 없는 키를 읽기만 하는가 | 읽기만이면 get, 누적·append면 defaultdict |
| `Counter` vs `defaultdict(int)` | `most_common`·뺄셈이 필요한가 | 필요하면 Counter, 단순 카운팅은 어느 쪽이든 |
| 힙 vs 정렬 | 전부 필요한가, 극단만 반복인가 | 전부면 `sort()`, 반복 추출이면 힙 |
| 힙 vs 정렬 리스트 | 중간 순위 질의가 있는가 | k번째·구간 개수가 있으면 정렬 리스트+bisect |
| `deque` vs 이중 연결 리스트 | 중간을 건드리는가 | 양끝만이면 deque, 중간이면 직접 구현 |
| `remove` vs `discard` | 없는 값이 들어올 수 있는가 | 들어올 수 있으면 discard(KeyError 없음) |
| `bisect_left` vs `bisect_right` | 경계에 같은 값을 포함하는가 | "이상(≥)"은 left, "초과(>)"는 right |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: dict·set의 평균 O(1)이 "적재율을 상수로 유지하는 재배치" 위에 서 있다는 것과, 최악이 O(n)이 되는 조건.
- [ ] 설명할 수 있다: 리스트가 dict 키나 set 원소가 될 수 없는 이유를 "저장 위치가 해시로 정해진다"에서 출발해 유도하기.
- [ ] 설명할 수 있다: dict는 삽입 순서를 보존하지만 set은 아무 순서도 보장하지 않는 이유.
- [ ] 설명할 수 있다: `d[k]`·`d.get(k, 0)`·`defaultdict(int)`·`Counter`가 없는 키에 각각 어떻게 반응하는지.
- [ ] 설명할 수 있다: `bisect_left`가 "x 미만 개수", `bisect_right`가 "x 이하 개수"라는 정의 하나에서 pred·succ·구간 개수 공식을 전부 다시 만들어 내기.
- [ ] 설명할 수 있다: 정렬 리스트가 "위치 찾기 O(log n) + 자리 만들기 O(n)"이라 삽입이 O(n)인 이유와, 그럼에도 써도 되는 상황.
- [ ] 설명할 수 있다: 힙이 완전이진트리라 높이가 log n이고, 그래서 push·pop이 O(log n)이 되는 과정.
- [ ] 설명할 수 있다: `heapify`가 O(n)인데 하나씩 push하면 O(n log n)인 이유.
- [ ] 설명할 수 있다: 최소 힙에서 최댓값을 O(1)에 볼 수 없는 이유(형제 사이에 순서가 없다).
- [ ] 설명할 수 있다: "K번째로 작은 값"은 최대 힙, "상위 K개의 합"은 최소 힙이라는 방향을 그림 없이 말로 설명하기.
- [ ] 설명할 수 있다: 힙 튜플에 타이브레이커를 끼우는 이유와, 그것이 없을 때 정확히 어느 시점에 TypeError가 나는지.
- [ ] 설명할 수 있다: 힙에서 임의 원소를 지울 수 없는 이유와, 지연 삭제가 왜 분할상환 O(log n)인지.
- [ ] 설명할 수 있다: 이중 연결 리스트의 삭제가 O(1)이려면 "노드를 이미 손에 쥐고 있어야 한다"는 전제와, LRU가 dict를 곁들이는 이유.
- [ ] 설명할 수 있다: 센티넬 노드가 없애 주는 경계 분기가 정확히 어떤 코드였는지.
- [ ] 설명할 수 있다: `deque`와 직접 만든 이중 연결 리스트 중 무엇을 고를지 한 문장으로.

**⚠️ 자주 하는 실수**

**1) `heapq`로 최대 힙을 쓴다고 생각한다**

```python
# ❌ 틀린 코드
import heapq
h = []
for x in arr:
    heapq.heappush(h, x)
biggest = heapq.heappop(h)      # arr = [3, 9, 1] 이면 9가 아니라 1이 나온다
```

왜: 파이썬 `heapq`에는 최대 힙이 없다. `heappop`은 언제나 최솟값을 준다. 최댓값은 잎 어딘가에 있지만 힙 조건("부모 ≤ 자식")은 형제 사이의 순서를 아무것도 보장하지 않아서, 뿌리만 보고는 찾을 수 없다.

```python
# ✅ 고친 코드 — 부호를 뒤집어 대소를 반전시킨다
for x in arr:
    heapq.heappush(h, -x)       # 넣을 때 뒤집고
biggest = -heapq.heappop(h)     # 꺼낼 때 되돌린다 (한쪽만 하면 값이 음수로 나온다)
```

**2) 힙 튜플의 두 번째 원소가 비교 불가능한 타입이다**

```python
# ❌ 틀린 코드
h = []
heapq.heappush(h, (2, {"id": 1}))
heapq.heappush(h, (2, {"id": 2}))   # 우선순위 2가 동점 → dict끼리 비교
# TypeError: '<' not supported between instances of 'dict' and 'dict'
```

왜: 튜플 비교는 앞 원소가 같을 때 **다음 원소로 넘어간다**. 우선순위가 한 번도 겹치지 않는 입력에서는 멀쩡히 돌다가, 동점이 처음 나오는 순간 뒤 원소가 비교되면서 터진다. 그래서 로컬 테스트는 통과하고 채점에서만 죽는 전형적인 실수다.

```python
# ✅ 고친 코드 — 항상 비교 가능한 타이브레이커를 사이에 끼운다
seq = 0
for pri, obj in items:
    seq += 1
    heapq.heappush(h, (pri, seq, obj))   # seq가 서로 달라 obj까지 갈 일이 없다
```

**3) 정렬 리스트에 삽입을 반복해 O(n²)를 만든다**

```python
# ❌ 틀린 코드
import bisect
a = []
for x in arr:                # N = 200000
    bisect.insort(a, x)      # 위치 찾기는 O(log n)이지만 밀기가 O(n)
print(a[k-1])
```

왜: `insort`가 빠르다는 착각은 "이분탐색으로 자리를 찾는다"만 보고 생긴다. 실제로 자리를 만들려면 뒤쪽 원소를 **전부** 한 칸씩 밀어야 하므로 한 번이 O(n)이고, N번 반복하면 O(N²)다. N=20만이면 200억 번이다.

```python
# ✅ 고친 코드 — 삽입이 다 끝난 뒤 조회만 한다면 한 번만 정렬한다
a = sorted(arr)              # O(N log N)
print(a[k-1])
# 삽입·삭제가 조회와 계속 섞여야 한다면 sortedcontainers.SortedList,
# 또는 좌표압축 + 펜윅 트리로 갈아탄다.
```

**4) 없는 키를 `d[k]`로 읽는다**

```python
# ❌ 틀린 코드
cnt = {}
for x in arr:
    cnt[x] += 1              # 처음 보는 x에서 KeyError
```

왜: `cnt[x] += 1`은 "읽고 → 더하고 → 쓴다"인데, 첫 단계인 읽기에서 키가 없어 터진다. 반대로 `defaultdict`는 **읽기만 해도 키를 만들어 넣기 때문에**, 그 성질을 모르고 존재 확인에 쓰면 dict가 조용히 부풀어 오른다. 존재만 볼 때는 `in`을 쓰거나 `get`을 쓴다.

```python
# ✅ 고친 코드
from collections import Counter, defaultdict

cnt = Counter(arr)                  # 빈도 세기는 이 한 줄
group = defaultdict(list)           # 누적·append에는 defaultdict
for k, v in data:
    group[k].append(v)
print(cnt.get(9, 0))                # 없는 키를 "읽기만" 할 때는 get (키가 안 생긴다)
```

**5) 리스트를 dict 키나 set 원소로 넣는다**

```python
# ❌ 틀린 코드
seen = set()
seen.add([r, c])             # TypeError: unhashable type: 'list'
best = {}
best[[r, c]] = 0             # 같은 이유로 실패
```

왜: 저장 위치가 `hash(key)`로 정해지는데, 리스트는 내용이 바뀌면 해시도 바뀐다. 넣을 때의 칸과 찾을 때의 칸이 달라져 "분명 넣었는데 없다"가 되므로, 파이썬은 가변 객체의 해시를 아예 금지한다. 좌표를 키로 쓰는 격자 문제에서 가장 자주 만난다.

```python
# ✅ 고친 코드
seen.add((r, c))             # 튜플은 불변이라 해시 가능
best[(r, c)] = 0
seen.add(frozenset(group))   # 집합 자체를 원소로 넣어야 하면 frozenset
```

**6) `set`의 순회 순서를 믿는다**

```python
# ❌ 틀린 코드
s = set()
for x in arr:
    s.add(x)
print(" ".join(map(str, s)))     # "중복만 제거된 입력 순서"가 아니다
```

왜: set 원소의 위치는 삽입 순서가 아니라 해시값으로 정해진다. 순회는 "칸 번호 순"이라 사람이 예상하는 순서와 무관하고, 원소 구성이 조금만 달라져도 통째로 바뀐다. 작은 예제에서 우연히 맞아 보이는 것이 이 버그를 오래 살려 둔다.

```python
# ✅ 고친 코드 — 원하는 순서를 코드에 명시한다
print(" ".join(map(str, sorted(s))))              # 정렬 순서가 필요하면 sorted
print(" ".join(map(str, dict.fromkeys(arr))))     # 입력 순서 유지 중복 제거는 dict
```

**7) 힙에서 가운데 원소를 지우려 한다**

```python
# ❌ 틀린 코드
h.remove(v)          # 리스트의 remove: 탐색 O(n) + 힙 성질이 깨질 수 있다
heapq.heapify(h)     # 그래서 매번 다시 힙화 → 삭제 한 번에 O(n)
```

왜: 힙은 "뿌리가 최소"만 보장할 뿐 특정 값이 어디 있는지 모른다. 찾는 데 O(n)이 들고, 지운 자리를 메우느라 구조가 깨져 `heapify`를 다시 불러야 한다. 삭제가 Q번이면 O(NQ)라 힙을 쓴 의미가 사라진다.

```python
# ✅ 고친 코드 — 지연 삭제: 지웠다고 표시만 하고, 꺼낼 때 걷어낸다
alive = set()                     # 살아 있는 고유번호만 담는다
def kill(sid):
    alive.discard(sid)            # 힙은 건드리지 않는다 (O(1))
def top():
    while h and h[0][1] not in alive:
        heapq.heappop(h)          # 유령은 top에 올라온 순간에만 치운다
    return h[0] if h else None
```

**8) 이중 연결 리스트에서 링크를 한쪽만 고친다**

```python
# ❌ 틀린 코드
def unlink(x):
    nxt[prv[x]] = nxt[x]          # 앞 → 뒤 방향만 이어 붙였다
```

왜: 뒤에서 앞으로 가는 길은 여전히 x를 가리킨다. 앞에서부터 순회하면 멀쩡해 보이다가, 역방향 순회나 `prv[nxt[x]]`를 쓰는 순간 이미 지운 x로 되돌아간다. **삭제는 링크 두 개, 삽입은 네 개**를 반드시 짝으로 고쳐야 한다.

```python
# ✅ 고친 코드
def unlink(x):
    p, q = prv[x], nxt[x]
    nxt[p] = q
    prv[q] = p                    # x의 prv/nxt는 남겨 둔다 → restore(x)로 복원 가능
```

**다음 챕터로**

- 이 챕터의 도구들은 다음 챕터(Shorten time Technique)에서 **전처리의 재료**로 다시 나온다. 좌표 압축의 `sorted(set(...))`은 여기서 배운 set과 정렬 리스트 그대로이고, "값 → 순위" 변환은 dict의 전형적인 쓰임이다.
- `bisect`는 특히 그대로 이어진다. 압축된 좌표에서 `[L, R]` 구간을 찾을 때, 누적합 위에서 조건을 만족하는 경계를 찾을 때 다시 등장하며, 그 다음 챕터의 이진탐색에서는 `bisect`가 하던 일을 직접 손으로 구현하게 된다.
- 반대로 "질의와 갱신이 번갈아 오는" 상황에서 정렬 리스트의 O(n) 이동이 병목이 된다는 이 챕터의 결론은, 펜윅 트리·세그먼트 트리라는 다음 단계로 가는 정확한 이유가 된다.
