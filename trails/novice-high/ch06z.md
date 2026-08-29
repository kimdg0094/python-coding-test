## L7. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터에서 배운 것은 결국 **하나의 모양(트리) 위에 서로 다른 규칙을 얹은 것**이다. 규칙이 "왼쪽 < 나 < 오른쪽"이면 BST, "부모 ≤ 자식"이면 힙, 아무 규칙도 없으면 그냥 트리다. 아래 지도로 전체를 한 번에 훑고, 뼈대 코드·선택 기준표·체크리스트로 정리한다.

**개념 지도**

```text
  Ch06 map : one shape, many rules

  tree  (N nodes, N-1 edges, no cycle, exactly one root)
   |
   +-- how the input arrives
   |    parent[v]            -> children[parent[v]].append(v)
   |    edge list u v        -> adj[u].append(v); adj[v].append(u)
   |    left[i], right[i]    -> binary tree, 0 means "no child"
   |
   +-- DFS on a tree
   |    going down : depth[c] = depth[v] + 1
   |    coming up  : size[v]  = 1 + sum(size[c])
   |
   +-- binary tree  (at most 2 children, left and right differ)
        |
        +-- traversal
        |    pre  : node left right    -> copy, serialize
        |    in   : left node right    -> sorted order in a BST
        |    post : left right node    -> subtree sum, delete
        |    BFS  : level by level     -> deque, nearest first
        |
        +-- complete tree -> array with no gap
        |    1-based : 2i, 2i+1, i//2
        |    0-based : 2i+1, 2i+2, (i-1)//2
        |    height = floor(log2 N)
        |
        +-- BST   left subtree < node < right subtree
        |    search / insert / delete : O(h)
        |    inorder = sorted
        |    skewed -> h = N-1 -> O(N)
        |
        +-- heap  parent <= child (min-heap)
             push / pop : O(log N),  peek : O(1)
             heapq is a min-heap,  push -x for a max-heap
```

문제를 만나면 아래 순서로 한 칸씩 좁힌다.

```text
  which tool ?

  visit every node once           -> DFS or BFS
  child answers needed first      -> postorder  (coming up)
  parent info carried downward    -> preorder   (going down)
  distance measured in levels     -> BFS with a deque
  sorted order or rank            -> BST inorder, or sort + bisect
  only the current min or max     -> heap (heapq)
  the k largest values            -> min-heap of size k
```

**뼈대 코드**

1) 부모 배열 입력 → 깊이·서브트리 크기 (재귀 없이)

```python
import sys
data = sys.stdin.read().split()
idx = 0
n = int(data[idx]); idx += 1
parent = [int(data[idx + i]) for i in range(n)]; idx += n   # ← 문제마다 바뀜

children = [[] for _ in range(n)]
root = -1
for v in range(n):
    if parent[v] == -1:            # ← 루트 표시 방법은 문제마다 바뀜
        root = v
    else:
        children[parent[v]].append(v)

order, stack = [], [root]
depth = [0] * n
while stack:                       # 스택 DFS: 방문 순서를 order에 기록
    v = stack.pop()
    order.append(v)
    for c in children[v]:
        depth[c] = depth[v] + 1    # 내려가며 계산
        stack.append(c)

size = [1] * n
for v in reversed(order):          # 역순 = 자식이 먼저 확정된 순서
    if parent[v] != -1:
        size[parent[v]] += size[v] # 올라오며 계산
```

2) 무방향 간선 목록 입력 → 인접 리스트 + BFS 깊이

```python
from collections import deque

adj = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u = int(data[idx]); v = int(data[idx + 1]); idx += 2
    adj[u].append(v)
    adj[v].append(u)               # 방향이 없으면 양쪽에 등록

dist = [-1] * (n + 1)
start = 1                          # ← 루트 번호는 문제마다 바뀜
dist[start] = 0
q = deque([start])
while q:
    v = q.popleft()
    for c in adj[v]:
        if dist[c] == -1:          # 미방문 검사 = 부모로 되돌아가지 않기
            dist[c] = dist[v] + 1
            q.append(c)
```

3) 순회 3종 — 재귀형과 반복형

```python
# 재귀형: 한 번의 DFS로 세 결과를 동시에 만든다
pre, ino, post = [], [], []

def dfs(v):
    if v == 0:                     # ← '자식 없음'을 뜻하는 값은 문제마다 바뀜
        return
    pre.append(v)
    dfs(left[v])
    ino.append(v)
    dfs(right[v])
    post.append(v)

# 반복형 전위: 오른쪽을 먼저 push해야 왼쪽이 먼저 pop된다
def preorder_iter(root):
    out, stack = [], [root]
    while stack:
        v = stack.pop()
        if v == 0:
            continue
        out.append(v)
        stack.append(right[v])
        stack.append(left[v])
    return out

# 반복형 중위: 왼쪽 끝까지 push → pop해서 기록 → 오른쪽으로
def inorder_iter(root):
    out, stack, cur = [], [], root
    while stack or cur != 0:
        while cur != 0:
            stack.append(cur)
            cur = left[cur]
        cur = stack.pop()
        out.append(cur)
        cur = right[cur]
    return out
```

4) heapq 실전 패턴 모음

```python
import heapq

h = []
heapq.heappush(h, 5)                # 삽입 O(log N)
peek = h[0]                         # 최솟값 조회 O(1), 제거하지 않음
smallest = heapq.heappop(h)         # 최솟값 제거 O(log N)
heapq.heapify(nums)                 # 리스트를 제자리에서 힙으로 O(N)

maxh = []                           # 최대 힙: 부호를 뒤집어 넣는다
for x in nums:
    heapq.heappush(maxh, -x)
biggest = -heapq.heappop(maxh)      # 꺼낸 뒤 부호를 되돌린다

pq, seq = [], 0                     # 우선순위 큐: (우선순위, 순번, 데이터)
for cost, item in tasks:            # ← 튜플 구성은 문제마다 바뀜
    seq += 1
    heapq.heappush(pq, (cost, seq, item))
                                    # seq는 동점일 때 비교가 멈추게 하는 안전핀

topk = []                           # 가장 큰 k개 유지 → 크기 k 최소 힙
for x in nums:
    if len(topk) < k:
        heapq.heappush(topk, x)
    elif x > topk[0]:
        heapq.heapreplace(topk, x)  # pop + push를 한 번에
kth_largest = topk[0]               # 상위 k개 중 가장 작은 값
```

5) BST 삽입·탐색

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def insert(node, val):
    if node is None:
        return Node(val)
    if val < node.val:
        node.left = insert(node.left, val)     # 반환값을 반드시 다시 대입
    elif val > node.val:
        node.right = insert(node.right, val)
    return node                                # ← 중복 규칙은 문제마다 바뀜

def search(node, val):
    while node is not None:                    # 반복문이면 재귀 한도와 무관
        if val == node.val:
            return True
        node = node.left if val < node.val else node.right
    return False
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 부모 배열만 주어졌고 깊이·크기를 묻는다 | 자식 리스트 + DFS | 위에서 아래로 훑을 경로가 있어야 한다 | O(N) |
| 간선이 방향 없이 주어진다 | 인접 리스트 + 방문 표시 | `adj[v]`에 부모도 들어 있어 되돌아감을 막아야 | O(N) |
| 자식들의 답을 모아 내 답을 만든다 | 후위 순회 | 내 차례에 자식이 전부 확정돼 있다 | O(N) |
| 부모에게서 물려받아 아래로 전달한다 | 전위 순회 | 내 차례에 부모 정보만 있으면 충분하다 | O(N) |
| 몇 번째 층인가, 층 단위로 처리 | BFS(`deque`) | 큐에 든 원소가 항상 같은 층이다 | O(N) |
| 입력이 완전 이진 트리다 | 배열 인덱싱 | 포인터 없이 계산만으로 자식·부모로 이동 | 이동 O(1) |
| 삽입·삭제가 섞이며 정렬 순서를 유지해야 한다 | BST | 중위 순회가 정렬, 하강이 한 방향뿐 | O(h) |
| 값이 고정이고 순위·범위만 물어본다 | `sorted()` + `bisect` | 균형 걱정 없이 항상 O(log N)이 보장된다 | O(log N) |
| 남은 것 중 최소/최대만 반복해서 꺼낸다 | 힙(`heapq`) | 전체 순서를 포기해 삽입·삭제를 싸게 만든다 | O(log N) |
| 상위 k개 또는 k번째 큰 값 | 크기 k 최소 힙 | 전체 정렬 O(N log N)보다 싸다 | O(N log k) |
| 한 번 정렬해 놓고 더 안 바뀐다 | `sorted()` | 갱신이 없으면 정렬이 가장 단순하고 빠르다 | O(N log N) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 노드가 N개인 트리의 간선이 왜 정확히 N-1개인지.
- [ ] 설명할 수 있다: 깊이와 높이의 차이, 그리고 각각이 왜 반대 방향으로 계산되는지.
- [ ] 설명할 수 있다: 부모 배열·간선 목록·자식 배열 중 어떤 입력이 와도 트리를 만드는 방법.
- [ ] 설명할 수 있다: 1-based `2i`/`2i+1`과 0-based `2i+1`/`2i+2`가 왜 같은 그림의 다른 번호인지.
- [ ] 설명할 수 있다: 완전 이진 트리의 높이가 왜 약 log2(N)인지.
- [ ] 설명할 수 있다: 전위·중위·후위가 왜 같은 코드에서 append 위치만 다른 것인지.
- [ ] 설명할 수 있다: 서브트리 크기·합 계산에 왜 후위 순회가 맞는지.
- [ ] 설명할 수 있다: 전위+중위로는 트리가 복원되는데 전위+후위로는 안 되는 이유.
- [ ] 설명할 수 있다: BST에서 중위 순회 결과가 왜 항상 오름차순인지.
- [ ] 설명할 수 있다: BST 연산이 O(log N)이 되는 조건과, O(N)으로 무너지는 입력.
- [ ] 설명할 수 있다: BST 삭제의 세 경우와, 자식이 둘일 때 오른쪽 최솟값을 쓰는 이유.
- [ ] 설명할 수 있다: 힙의 sift-up/sift-down이 왜 높이만큼만 움직이는지.
- [ ] 설명할 수 있다: `heapq`로 최대 힙을 만드는 방법과 그것이 성립하는 원리.
- [ ] 설명할 수 있다: 정렬·BST·힙 중 무엇을 언제 고를지, 그 판단 근거.

**⚠️ 자주 하는 실수**

**1) 깊은 트리에서 재귀가 먼저 터진다**

```python
# ❌ 틀린 코드
def size(v):
    return 1 + sum(size(c) for c in children[v])

print(size(root))          # 노드 10만 개짜리 사슬 트리 → RecursionError
```

왜: 파이썬의 기본 재귀 한도는 약 1000이다. 각 노드가 자식을 하나만 갖는 사슬 모양이면 깊이가 N-1이라, 알고리즘이 맞아도 호출 스택이 먼저 무너진다.

```python
# ✅ 고친 코드
import sys
sys.setrecursionlimit(300000)   # 재귀를 꼭 쓸 때

# 더 안전한 방법: 재귀를 아예 반복문으로 바꾼다
order, stack = [], [root]
while stack:
    v = stack.pop()
    order.append(v)
    stack.extend(children[v])
size = [1] * n
for v in reversed(order):
    if parent[v] != -1:
        size[parent[v]] += size[v]
```

**2) 0-based 리스트에 1-based 자식 공식을 쓴다**

```python
# ❌ 틀린 코드
h = [3, 1, 4, 1, 5]        # 0-based 파이썬 리스트
left = 2 * i               # L2에서 본 1-based 공식을 그대로 가져옴
right = 2 * i + 1
```

왜: 0-based에서 `i = 0`의 왼쪽 자식은 1인데 `2 * 0`은 0이라 자기 자신을 가리킨다. 루트에서 무한 루프가 돌거나, 인덱스가 한 칸씩 밀려 엉뚱한 노드끼리 비교된다.

```python
# ✅ 고친 코드
left = 2 * i + 1
right = 2 * i + 2
parent = (i - 1) // 2      # 0-based는 1-based보다 전부 1씩 밀린다
```

**3) 힙에 넣은 튜플의 두 번째 원소가 비교 불가 타입이다**

```python
# ❌ 틀린 코드
import heapq
pq = []
heapq.heappush(pq, (2, node_a))
heapq.heappush(pq, (2, node_b))   # TypeError: '<' not supported
```

왜: 첫 원소(우선순위)가 같으면 파이썬은 튜플의 다음 원소를 비교한다. 그 자리에 비교 연산이 정의되지 않은 객체가 있으면 그 순간 TypeError가 난다. 우선순위가 겹치지 않는 입력에서는 멀쩡히 통과하다가 특정 입력에서만 터져 원인 찾기가 어렵다.

```python
# ✅ 고친 코드
import heapq
pq, seq = [], 0
seq += 1
heapq.heappush(pq, (2, seq, node_a))   # 순번을 중간에 끼운다
seq += 1
heapq.heappush(pq, (2, seq, node_b))   # 동점이면 넣은 순서대로 나온다
```

**4) 무방향 간선에서 부모로 되돌아간다**

```python
# ❌ 틀린 코드
def dfs(v, d):
    depth[v] = d
    for c in adj[v]:
        dfs(c, d + 1)      # adj[v]에는 자식뿐 아니라 부모도 들어 있다
```

왜: 간선 `u v`를 `adj[u]`와 `adj[v]` 양쪽에 넣었으므로 `adj[v]`를 훑으면 부모도 나온다. 부모로 다시 내려가고 부모는 또 나에게 내려와 무한 재귀가 된다.

```python
# ✅ 고친 코드
def dfs(v, p, d):          # p = 나를 호출한 부모 번호
    depth[v] = d
    for c in adj[v]:
        if c != p:         # 부모 하나만 건너뛰면 된다
            dfs(c, v, d + 1)
```

**5) 힙에서 peek만 하고 pop을 안 한다**

```python
# ❌ 틀린 코드
while h:
    x = h[0]               # 최솟값을 보기만 했다
    total += x             # 힙 크기가 줄지 않아 while이 끝나지 않는다
```

왜: `h[0]`은 조회일 뿐 원소를 제거하지 않는다. 같은 값을 영원히 다시 읽으며 무한 루프에 빠진다.

```python
# ✅ 고친 코드
while h:
    x = heapq.heappop(h)   # 꺼내면서 제거한다
    total += x
```

**6) BST 재귀 삽입의 반환값을 부모에 다시 연결하지 않는다**

```python
# ❌ 틀린 코드
def insert(node, val):
    if node is None:
        return Node(val)
    if val < node.val:
        insert(node.left, val)     # 반환값을 그냥 버렸다
    else:
        insert(node.right, val)
    return node
```

왜: `node.left`가 `None`인 자리에서 새 노드를 만들어 돌려주지만 받는 쪽이 없어 그대로 사라진다. 루트만 남고 트리가 자라지 않아, 이후 탐색이 전부 `NO`가 된다.

```python
# ✅ 고친 코드
def insert(node, val):
    if node is None:
        return Node(val)
    if val < node.val:
        node.left = insert(node.left, val)     # 돌려받은 서브트리를 다시 매단다
    else:
        node.right = insert(node.right, val)
    return node
```

**7) 최대 힙에서 부호를 되돌리지 않는다**

```python
# ❌ 틀린 코드
maxh = []
for x in nums:
    heapq.heappush(maxh, -x)
print(heapq.heappop(maxh))     # -9 같은 음수가 그대로 출력된다
```

왜: 힙에 저장된 값은 `x`가 아니라 `-x`다. 넣을 때 뒤집은 부호는 꺼낼 때 반드시 되돌려야 원래 값이 된다.

```python
# ✅ 고친 코드
print(-heapq.heappop(maxh))    # 꺼낸 뒤 부호를 한 번 더 뒤집는다
```

**다음 챕터로**

- 여기서 만든 "인접 리스트 + 방문 표시 + DFS/BFS" 뼈대는 그래프 챕터에서 그대로 재사용된다. 트리는 사이클이 없는 특수한 그래프라, 달라지는 것은 "방문 표시를 반드시 해야 한다"는 조건 하나뿐이다.
- 힙은 최단 경로(다익스트라)에서 "다음에 확정할 가장 가까운 정점"을 고르는 도구로 다시 등장한다. `(거리, 정점)` 튜플을 넣는 우선순위 큐 패턴이 그 자리에서 그대로 쓰인다.
