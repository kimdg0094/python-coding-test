## L8. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

**개념 지도**

```text
                        sequence container
                                 │
              ┌──────────────────┴───────────────────┐
         contiguous                            linked nodes
              │                                      │
    ┌─────────┴─────────┐            ┌───────────────┼───────────────┐
  array           dynamic array    singly         doubly         circular
  fixed size      grow x 2         val + next     prev + next    tail.next
  a[i] O(1)       append O(1)*     push_front     erase(node)    = head
  insert O(n)     * amortized      search O(n)    sentinels      rotate
  shift back      size vs cap      dummy head     deque          josephus
              │                                      │
              └──────────────────┬───────────────────┘
                                 │
                            Iterator
              __iter__ / __next__ / StopIteration / yield
              # 내부 구조를 숨기고 for 문 하나로 순회한다
```

이 챕터는 하나의 질문에서 갈라진다 — **"원소들을 붙여 놓을 것인가, 화살표로 이을 것인가."**

- 붙여 놓으면(배열) 주소 계산으로 어디든 O(1)에 가지만, 가운데를 건드릴 때마다 뒤를 전부 밀어야 한다.
- 화살표로 이으면(연결 리스트) 링크 한두 개만 고쳐 O(1)에 끼우고 뺄 수 있지만, `i`번째를 찾으려면 처음부터 걸어가야 한다.
- 동적 배열은 배열 쪽 가지에서 "크기 고정"이라는 제약만 없앤 것이고(2배 확장 + 분할상환), 이중·원형 리스트는 연결 리스트 쪽 가지에서 "뒤로 못 간다·끝이 있다"는 제약을 없앤 것이다.
- Iterator는 두 갈래 위에 얹는 공통 껍데기다. 내부가 배열이든 사슬이든 `for v in obj:` 한 줄로 같게 보이게 만든다.

**뼈대 코드**

```python
# 1) 단일 연결 리스트 — 노드 / 삽입 / 삭제 / 순회 골격
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

def build(vals):                       # 뒤에 이어 붙이며 만들기
    dummy = Node(None)
    tail = dummy
    for v in vals:
        tail.next = Node(v)
        tail = tail.next
    return dummy.next

def insert_after(cur, x):              # cur 바로 뒤에 삽입 O(1)
    node = Node(x)
    node.next = cur.next               # ← 순서 고정: 새 노드부터
    cur.next = node

def remove_all(head, target):          # 값이 target 인 노드 모두 삭제
    dummy = Node(None); dummy.next = head
    cur = dummy
    while cur.next:
        if cur.next.val == target:     # ← 문제마다 바뀜(삭제 조건)
            cur.next = cur.next.next   # 삭제 시 cur 를 전진시키지 않는다
        else:
            cur = cur.next
    return dummy.next

def walk(head):                        # 순회 O(n)
    cur = head
    while cur:
        yield cur.val
        cur = cur.next
```

```python
# 2) 이중 연결 리스트 — 센티넬 두 개로 경계 분기를 없앤다
class DNode:
    def __init__(self, val=None):
        self.val = val
        self.prev = None
        self.next = None

H, T = DNode(), DNode()                # head / tail 센티넬
H.next, T.prev = T, H

def insert_after_d(a, x):              # a 뒤에 x 삽입 — 링크 4개
    b = a.next
    node = DNode(x)
    node.prev, node.next = a, b        # (1)(2) 새 노드 쪽 먼저
    a.next, b.prev = node, node        # (3)(4) 이웃을 새 노드로
    return node

def erase_d(node):                     # 노드 자체를 O(1)에 삭제 — 링크 2개
    node.prev.next = node.next
    node.next.prev = node.prev

def dump(H, T):                        # 센티넬 사이만 훑는다
    out, cur = [], H.next
    while cur is not T:
        out.append(cur.val)
        cur = cur.next
    return out
```

```python
# 3) 원형 — 직접 구현 골격과 deque 실전 골격
def walk_circular(start):              # 종료 조건은 None 이 아니라 '복귀'
    cur = start
    while True:
        yield cur.val
        cur = cur.next
        if cur is start:               # ← 이 줄이 없으면 무한 루프
            break

from collections import deque
def rotate_pick(vals, k):              # k 번째마다 하나씩 빼는 골격
    dq = deque(vals)
    order = []
    while dq:
        dq.rotate(-(k - 1))            # ← 문제마다 바뀜(간격 규칙)
        order.append(dq.popleft())
    return order
```

```python
# 4) 동적 배열·반복자 실전 패턴
buf = []                               # 뒤에서만 쓰면 상환 O(1)
buf.append(1); buf.pop()               # 앞을 다루려면 deque 로 바꾼다

from collections import deque
dq = deque([1, 2, 3])
dq.appendleft(0); dq.popleft()         # 양끝 O(1)

class MyList:                          # 내부 구조를 숨긴 순회 제공
    def __init__(self, head):
        self.head = head
    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.val              # ← 문제마다 바뀜(내보낼 값)
            cur = cur.next

nums = (i * i for i in range(10 ** 9))  # 지연 평가: 필요한 만큼만 만든다
first5 = [next(nums) for _ in range(5)]
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 인덱스로 자주 읽고 크기가 거의 안 변함 | 배열(`list`) | 주소 계산으로 바로 점프 | 접근 O(1) |
| 개수를 모른 채 뒤로만 계속 쌓음 | 동적 배열(`list.append`) | 2배 확장으로 상환 O(1) | append 상환 O(1) |
| 앞에서 넣고 빼기가 잦음 | `deque` | 양끝이 모두 상수 시간 | 양끝 O(1) |
| 중간 삽입·삭제가 잦고 위치를 이미 쥐고 있음 | 단일 연결 리스트 | 링크 재배선만 하면 됨 | 삽입·삭제 O(1) |
| 노드 참조 하나로 그 자리를 즉시 삭제 | 이중 연결 리스트 | `prev`가 있어 직전 노드를 안 찾아도 됨 | 삭제 O(1) |
| 최근 사용 순서 유지 + 임의 키 접근 | 이중 리스트 + `dict` | 순서는 링크가, 탐색은 해시가 담당 | 갱신 O(1) |
| 돌면서 N번째마다 처리 | 원형 리스트 / `deque.rotate` | 끝이 없어 감기 처리가 필요 없음 | 회전 O(min(r, n-r)) |
| 큰(또는 무한) 수열을 흘려보냄 | 제너레이터 | 만들지 않은 값에는 비용을 안 냄 | 메모리 O(1) |
| 값을 인덱스로 자주 찾아야 함 | 연결 리스트 대신 배열·dict | 사슬은 임의 접근이 O(n) | 탐색 O(n) vs O(1) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 배열의 임의 접근이 왜 O(1)인가(주소 = base + i × 원소크기).
- [ ] 설명할 수 있다: 배열 중간 삽입이 왜 O(n)이고, 밀기를 왜 뒤에서부터 해야 하는가.
- [ ] 설명할 수 있다: size와 capacity의 차이, 그리고 둘이 같아지는 순간 무슨 일이 벌어지는가.
- [ ] 설명할 수 있다: 동적 배열 append가 왜 평균 O(1)인가(복사 총량 1+2+4+… < 2n).
- [ ] 설명할 수 있다: 확장 배수를 2배가 아니라 +1로 하면 왜 O(n²)이 되는가.
- [ ] 설명할 수 있다: 연결 리스트의 임의 접근이 왜 O(n)이고 삽입이 왜 O(1)인가.
- [ ] 설명할 수 있다: 삽입 시 `new.next`를 먼저 세팅해야 하는 이유와, 순서를 바꾸면 무엇이 사라지는가.
- [ ] 설명할 수 있다: 더미(센티넬) 헤드가 없애 주는 분기가 정확히 무엇인가.
- [ ] 설명할 수 있다: 단일 리스트에서 노드 하나를 지우려면 왜 직전 노드가 필요한가.
- [ ] 설명할 수 있다: 이중 리스트 삽입에서 바꿔야 할 링크 4개를 순서대로 댈 수 있다.
- [ ] 설명할 수 있다: LRU 캐시가 왜 `dict` 하나로도, 리스트 하나로도 안 되고 둘 다 필요한가.
- [ ] 설명할 수 있다: 원형 리스트의 순회 종료 조건이 왜 `None`이 아닌가.
- [ ] 설명할 수 있다: `__iter__`, `__next__`, `StopIteration`이 `for` 문 안에서 각각 언제 불리는가.
- [ ] 설명할 수 있다: 제너레이터가 한 번 소비되면 왜 다시 못 쓰는가.

**⚠️ 자주 하는 실수**

**1) 링크를 바꾸는 순서를 뒤집어 노드를 통째로 잃는다**

```python
# ❌ 틀린 코드
def insert_after(cur, x):
    node = Node(x)
    cur.next = node            # 여기서 B 로 가는 마지막 참조가 사라진다
    node.next = cur.next       # cur.next 는 이미 node -> node.next = node
```

왜: `cur.next = node`를 먼저 하면 원래 뒤에 있던 노드를 가리키는 참조가 하나도 남지 않는다. 두 번째 줄의 `cur.next`는 이미 `node`라 자기 자신을 가리키는 순환이 생기고, 뒤쪽 리스트가 통째로 유실된다.

```python
# ✅ 고친 코드
def insert_after(cur, x):
    node = Node(x)
    node.next = cur.next       # 새 노드가 먼저 뒤를 붙잡고
    cur.next = node            # 그다음 앞을 갈아 끼운다
```

**2) 순회 중 삭제하면서 커서를 전진시킨다**

```python
# ❌ 틀린 코드
cur = dummy
while cur.next:
    if cur.next.val == x:
        cur.next = cur.next.next
    cur = cur.next             # 삭제한 뒤에도 전진 -> 연속된 x 를 건너뜀
```

왜: 삭제하면 `cur.next`가 이미 다음 후보로 바뀌어 있다. 여기서 또 전진하면 그 후보를 검사도 못 하고 지나친다. `[1, 2, 2, 3]`에서 2를 지우면 `[1, 2, 3]`이 남는다.

```python
# ✅ 고친 코드
cur = dummy
while cur.next:
    if cur.next.val == x:
        cur.next = cur.next.next   # 삭제했으면 제자리에서 다시 검사
    else:
        cur = cur.next             # 안 지웠을 때만 전진
```

**3) 이중 리스트에서 한 방향 링크만 고친다**

```python
# ❌ 틀린 코드
def erase(node):
    node.prev.next = node.next     # next 방향만 이었다
```

왜: 정방향 순회는 멀쩡해 보이지만 `node.next.prev`가 여전히 삭제된 노드를 가리킨다. 역방향으로 훑는 순간 지운 값이 되살아나거나, 그 자리에서 순회가 끊긴다.

```python
# ✅ 고친 코드
def erase(node):
    node.prev.next = node.next
    node.next.prev = node.prev     # 두 방향을 반드시 함께
```

**4) 앞에서 빼는 연산을 `list`로 반복한다**

```python
# ❌ 틀린 코드
queue = [1, 2, 3, 4, 5]
while queue:
    x = queue.pop(0)               # 뺄 때마다 뒤 전체를 앞으로 당김 O(n)
```

왜: `list.pop(0)`은 O(n)이라 n번 반복하면 O(n²)이 된다. n이 10만이면 100억 번 이동으로 시간 초과가 난다.

```python
# ✅ 고친 코드
from collections import deque
queue = deque([1, 2, 3, 4, 5])
while queue:
    x = queue.popleft()            # 양끝 O(1)
```

**5) 원형 리스트를 `None` 기준으로 순회한다**

```python
# ❌ 틀린 코드
cur = head
while cur:                         # 원형에는 None 이 없다 -> 영원히 돈다
    print(cur.val)
    cur = cur.next
```

왜: 원형 리스트에서 마지막 노드의 `next`는 `None`이 아니라 다시 head다. 종료 조건이 절대 참이 되지 않아 무한 루프에 빠진다.

```python
# ✅ 고친 코드
cur = head
while True:
    print(cur.val)
    cur = cur.next
    if cur is head:                # 시작 노드로 돌아오면 한 바퀴 끝
        break
```

**6) 맨 앞 노드를 지우는 경우를 빠뜨린다**

```python
# ❌ 틀린 코드
cur = head
while cur.next:
    if cur.next.val == x:
        cur.next = cur.next.next
    else:
        cur = cur.next
# head 자체가 x 면 영영 지워지지 않는다. head 가 None 이면 AttributeError
```

왜: 이 코드는 "직전 노드가 존재하는 노드"만 지울 수 있다. head에는 직전 노드가 없어 예외 처리가 따로 필요하고, 그 분기를 잊으면 조용히 틀린 답이 나온다.

```python
# ✅ 고친 코드
dummy = Node(None); dummy.next = head    # head 앞에 가짜 노드를 하나
cur = dummy
while cur.next:
    if cur.next.val == x:
        cur.next = cur.next.next
    else:
        cur = cur.next
head = dummy.next                        # 새 head 를 다시 받아 온다
```

**7) 소진된 반복자를 다시 순회한다**

```python
# ❌ 틀린 코드
it = (x * 2 for x in [1, 2, 3])
total = sum(it)                    # 6 -> 12, 여기서 it 은 모두 소비됨
biggest = max(it)                  # ValueError: max() arg is an empty sequence
```

왜: 제너레이터는 "현재 위치" 하나만 들고 앞으로만 간다. 되감기 기능이 없어 한 번 끝까지 소비하면 두 번째 순회에서는 아무 값도 나오지 않는다.

```python
# ✅ 고친 코드
vals = [x * 2 for x in [1, 2, 3]]  # 두 번 쓸 거면 리스트로 재료를 남긴다
total = sum(vals)
biggest = max(vals)
```

**다음 챕터로**

- 다음 챕터의 정렬은 "배열 위에서 자리를 바꾸는 일"이다. 이 챕터에서 익힌 인덱스 밀기(삽입 정렬)와 교환(선택·거품 정렬)이 그대로 재료가 된다.
- 병합 정렬의 병합 단계는 L3에서 만든 "두 정렬 리스트 합치기"와 완전히 같은 투 포인터다. 연결 리스트로 짜면 추가 공간 없이도 합칠 수 있다.
- 힙 정렬에서 다시 만날 "완전 이진 트리를 배열 인덱스로 표현하기"는, 이 챕터의 "연속 메모리 + 인덱스 산술"이라는 발상의 연장이다.
