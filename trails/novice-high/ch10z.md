## L7. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

Ch10의 다섯 알고리즘은 각각 다른 질문에 답한다. 그 질문이 무엇인지 한 장으로 정리하고, 뼈대와 함정을 모아 둔다.

**개념 지도**

```text
                    weighted / directed graph
                              │
        ┌─────────────────────┼─────────────────────┐
   shortest path        spanning tree            ordering
        │                     │                      │
   ┌────┴─────┐          ┌────┴────┐          topological sort
   │          │          │         │          (Kahn, in-degree)
 dijkstra   floyd     kruskal    prim                │
 1 source   all pair  edge sort  vertex grow    cycle if len < N
 w >= 0     w may<0   + union    + heap
 heap       no neg    -find
 E log V    cycle     E log E    E log V
            O(N^3)
```

가중치가 없으면 Ch9의 BFS로 끝난다. 가중치가 생기는 순간 "무엇을 최소로 하려는가"에 따라 길이 갈린다. **시작점에서의 거리**를 최소로 하면 최단 경로(Dijkstra·Floyd), **채택한 간선의 총합**을 최소로 하면 최소 신장 트리(Kruskal·Prim)다. 최소화가 아니라 순서만 필요하면 위상 정렬이다.

Kruskal 밑에 깔린 Union-Find는 그 자체로 독립된 도구다.

```text
  union-find (disjoint set)
    find(x)    : follow parent up to the root     # 도중에 경로 압축
    union(a,b) : hang one root under the other
    find(a) == find(b)  <=>  already connected
                        <=>  adding edge a-b makes a cycle
```

**뼈대 코드**

(1) Dijkstra — `heapq` + 경로 복원

```python
import heapq
INF = float('inf')

def dijkstra(n, graph, start):        # graph[u] = [(v, w), ...]
    dist = [INF] * (n + 1)            # ← 0-based면 [INF] * n
    par = [-1] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:               # 낡은 항목은 버린다 (지연 삭제)
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                par[v] = u            # 경로가 필요할 때만
                heapq.heappush(pq, (nd, v))
    return dist, par

def restore(par, goal):               # goal 에서 거꾸로 따라 올라간다
    path, cur = [], goal
    while cur != -1:
        path.append(cur)
        cur = par[cur]
    path.reverse()
    return path
```

(2) Floyd-Warshall — 모든 쌍

```python
INF = float('inf')

def floyd(n, edges):                  # edges = [(u, v, w), ...]
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0                # 자기 자신은 0 (빠뜨리기 쉬움)
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)   # ← 중복 간선 대비
        dist[v][u] = min(dist[v][u], w)   # ← 방향 그래프면 이 줄 삭제
    for k in range(1, n + 1):         # k 가 반드시 가장 바깥
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

(3) Union-Find — 경로 압축

```python
def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]     # 경로 압축(절반씩 끌어올림)
        x = parent[x]
    return x

def union(parent, a, b):
    ra, rb = find(parent, a), find(parent, b)
    if ra == rb:
        return False                      # 이미 같은 집합 = 사이클
    parent[ra] = rb
    return True
```

(4) Kruskal — MST

```python
def kruskal(n, edges):                # edges = [(w, u, v), ...]
    parent = list(range(n + 1))
    edges.sort()                      # 가중치 오름차순 (w 가 맨 앞)
    total, cnt = 0, 0
    for w, u, v in edges:
        if union(parent, u, v):       # 사이클이 아니면 채택
            total += w
            cnt += 1
            if cnt == n - 1:          # 간선 V-1 개면 완성
                break
    return total if cnt == n - 1 else -1   # ← 연결 아님 처리는 문제마다
```

(5) Prim — MST

```python
import heapq

def prim(n, graph, start=1):          # graph[u] = [(v, w), ...], 무방향
    visited = [False] * (n + 1)
    pq = [(0, start)]
    total, cnt = 0, 0
    while pq and cnt < n:
        w, u = heapq.heappop(pq)
        if visited[u]:                # 낡은 항목 (지연 삭제)
            continue
        visited[u] = True
        total += w                    # 누적 거리가 아니라 간선 가중치
        cnt += 1
        for v, wv in graph[u]:
            if not visited[v]:
                heapq.heappush(pq, (wv, v))   # dist+w 가 아니라 w
    return total if cnt == n else -1
```

(6) 위상 정렬 — Kahn

```python
from collections import deque

def topo(n, graph, indeg):            # graph[u] = [v, ...] 방향 간선만
    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    # 사전순 답이 필요하면 deque 대신 heapq 를 쓴다   # ← 문제마다 바뀜
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []    # [] 이면 사이클
```

(7) 0-1 BFS — 가중치가 0 또는 1일 때

```python
from collections import deque

def zero_one_bfs(n, graph, start):    # graph[u] = [(v, w), ...], w in {0,1}
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[start] = 0
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0:
                    dq.appendleft(v)  # 비용 0 이면 앞에
                else:
                    dq.append(v)      # 비용 1 이면 뒤에
    return dist
```

**언제 무엇을 쓰나**

최단 경로 알고리즘 선택표부터 못 박는다. 이 표가 Ch9~Ch10의 갈림길 전부다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 간선 가중치가 없다(또는 전부 같다), 시작점 하나 | BFS (Ch9) | 처음 도달이 곧 최단, 힙이 필요 없다 | `O(V+E)` |
| 간선 가중치가 0 또는 1뿐, 시작점 하나 | 0-1 BFS | 덱 앞/뒤로 나눠 넣으면 힙 없이 정렬 유지 | `O(V+E)` |
| 간선 가중치가 모두 0 이상, 시작점 하나 | Dijkstra | 최소 거리를 꺼내면 그 값이 확정된다 | `O((V+E) log V)` |
| 모든 정점 쌍, 정점이 적다(대략 `N ≤ 400`) | Floyd-Warshall | 삼중 루프 한 방, 구현이 가장 짧다 | `O(N^3)` |
| 모든 정점 쌍인데 정점이 많고 간선은 희소 | Dijkstra를 `V`번 | `V·E log V`가 `N^3`보다 작다 | `O(V·E log V)` |
| 음수 간선이 있다 | Dijkstra 금지 | 확정 논증이 "비용 ≥ 0"에 기대고 있다 | — |

나머지 도구의 갈림길이다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 모든 정점을 최소 비용으로 연결, 간선 목록이 주어짐 | Kruskal | 정렬 한 번 + 사이클 검사만 | `O(E log E)` |
| 모든 정점을 최소 비용으로 연결, 인접 리스트이거나 밀집 | Prim | 트리 경계 간선만 힙으로 관리 | `O(E log V)` |
| "이미 연결됐나"를 여러 번 물어본다 | Union-Find | `find` 두 번이면 끝 | 사실상 `O(1)` |
| 선후 관계·의존성 순서를 정한다 | 위상 정렬(Kahn) | 진입차수 0을 하나씩 떼어내면 된다 | `O(V+E)` |
| 방향 그래프에 사이클이 있는지 본다 | 위상 정렬 후 길이 확인 | 사이클 정점은 진입차수가 0이 못 된다 | `O(V+E)` |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: Dijkstra가 "가장 가까운 정점을 꺼내면 그 값이 확정"이라고 말할 수 있는 근거.
- [ ] 설명할 수 있다: 음수 간선이 하나만 있어도 Dijkstra가 왜 틀리는지, 반례를 직접 그리며.
- [ ] 설명할 수 있다: Dijkstra의 복잡도 `O((V+E) log V)`에서 `log V`와 `V+E`가 각각 어디서 나왔는지.
- [ ] 설명할 수 있다: 지연 삭제(`if d > dist[u]: continue`)가 왜 필요하고, 빼면 무슨 일이 생기는지.
- [ ] 설명할 수 있다: Floyd-Warshall의 상태 정의와 점화식이 "마지막 선택"을 무엇으로 쪼갠 결과인지.
- [ ] 설명할 수 있다: 삼중 루프에서 `k`가 왜 반드시 가장 바깥이어야 하는지.
- [ ] 설명할 수 있다: 배열 하나를 제자리에서 덮어써도 되는 이유.
- [ ] 설명할 수 있다: 컷 성질이 무엇이고, 그것이 왜 Kruskal과 Prim을 동시에 정당화하는지.
- [ ] 설명할 수 있다: Kruskal이 간선을 버리는 순간이 정확히 어떤 상황인지.
- [ ] 설명할 수 있다: Union-Find의 경로 압축이 트리 모양을 어떻게 바꾸는지, 왜 빨라지는지.
- [ ] 설명할 수 있다: Prim과 Dijkstra의 코드가 닮았는데도 결과가 다른 이유(`w` vs `dist[u]+w`).
- [ ] 설명할 수 있다: MST의 간선 수가 왜 정확히 `V-1`개인지.
- [ ] 설명할 수 있다: Kahn 알고리즘이 사이클을 어떻게 감지하는지.
- [ ] 설명할 수 있다: 위상 정렬의 답이 여러 개일 수 있는 이유와, 사전순 최소를 얻는 방법.
- [ ] 설명할 수 있다: 최단 경로 선택표의 네 갈래(BFS / 0-1 BFS / Dijkstra / Floyd)를 상황만 보고 고르는 기준.

**⚠️ 자주 하는 실수**

(1) Dijkstra에서 이미 확정된 정점을 다시 처리한다

```python
# ❌ 틀린 코드
while pq:
    d, u = heapq.heappop(pq)
    for v, w in graph[u]:         # 낡은 (d, u) 도 그대로 전개한다
        if d + w < dist[v]:
            dist[v] = d + w
            heapq.heappush(pq, (dist[v], v))
```

왜: 거리를 갱신할 때마다 힙에 새 항목을 넣으므로, 같은 정점의 낡은 항목이 힙에 여러 개 남는다. 그것까지 전부 전개하면 정점 하나를 여러 번 완화하게 되어, 조밀한 그래프에서 시간 초과로 이어진다.

```python
# ✅ 고친 코드
while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]:               # 낡은 항목이면 버린다
        continue
    for v, w in graph[u]:
        if d + w < dist[v]:
            dist[v] = d + w
            heapq.heappush(pq, (dist[v], v))
```

(2) Floyd의 루프 순서를 뒤집는다

```python
# ❌ 틀린 코드
for i in range(1, n + 1):
    for j in range(1, n + 1):
        for k in range(1, n + 1):     # k 가 가장 안쪽
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
```

왜: `k` 루프 한 바퀴는 "경유 가능한 정점 집합을 `1..k`로 넓히는 한 단계"다. `i`를 바깥에 두면 `dist[i][k]`나 `dist[k][j]`가 아직 완성되지 않은 상태에서 참조된다. `1→3→4→2` 사슬에서 `dist[1][2]`는 INF로 남는다.

```python
# ✅ 고친 코드
for k in range(1, n + 1):             # k 가 반드시 가장 바깥
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
```

(3) 정수 INF를 쓰고 그대로 더한다

```python
# ❌ 틀린 코드
INF = 10 ** 9
...
if dist[i][k] + dist[k][j] < dist[i][j]:      # 10**9 + 10**9 = 2*10**9
    dist[i][j] = dist[i][k] + dist[k][j]      # 도달 불가인데 값이 들어간다
```

왜: 두 INF를 더한 값이 다른 큰 값과 비교되면서, 실제로는 이어지지 않은 경로에 유한한 거리가 기록될 수 있다. `k`가 커질수록 그 값이 다시 전파되어 표 전체가 오염된다.

```python
# ✅ 고친 코드
INF = float('inf')                # inf + 유한값 = inf 라 안전
# 정수 INF 를 꼭 써야 한다면 경유 가능 여부를 먼저 확인한다
if dist[i][k] != INF and dist[k][j] != INF:
    if dist[i][k] + dist[k][j] < dist[i][j]:
        dist[i][j] = dist[i][k] + dist[k][j]
```

(4) 자기 자신까지의 거리를 0으로 두지 않는다

```python
# ❌ 틀린 코드
dist = [[INF] * (n + 1) for _ in range(n + 1)]
for u, v, w in edges:
    dist[u][v] = w                # dist[i][i] 가 INF 로 남아 있다
```

왜: `dist[i][i]`가 INF면 `i`를 경유지로 쓰는 계산이 전부 막히고, "자기 자신까지의 거리"를 묻는 출력에서도 INF가 나온다. 자기 간선이 있는 경우가 아니라면 `dist[i][i] = 0`이 정의상 맞다.

```python
# ✅ 고친 코드
dist = [[INF] * (n + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    dist[i][i] = 0                # 먼저 대각선을 0으로
for u, v, w in edges:
    dist[u][v] = min(dist[u][v], w)
```

(5) 무방향 그래프인데 간선을 한 방향만 넣는다

```python
# ❌ 틀린 코드
for _ in range(m):
    u, v, w = map(int, input().split())
    graph[u].append((v, w))       # Prim/Dijkstra 가 반쪽 그래프를 본다
```

왜: 무방향 간선은 양쪽 인접 리스트에 모두 들어가야 한다. 한쪽만 넣으면 Prim은 트리를 다 못 키워 `-1`을 뱉고, Dijkstra는 실제보다 큰 거리(혹은 INF)를 답으로 낸다.

```python
# ✅ 고친 코드
for _ in range(m):
    u, v, w = map(int, input().split())
    graph[u].append((v, w))
    graph[v].append((u, w))       # 방향 그래프면 이 줄만 지운다
```

(6) Prim의 힙에 누적 거리를 넣는다

```python
# ❌ 틀린 코드
for v, wv in graph[u]:
    if not visited[v]:
        heapq.heappush(pq, (total + wv, v))   # 누적값을 넣었다
```

왜: MST가 최소로 만들려는 것은 시작점에서의 거리가 아니라 "채택한 간선 가중치의 합"이다. 누적값을 넣으면 시작점에서 먼 정점의 간선이 실제보다 비싸 보여, 최소 신장 트리가 아니라 최단 경로 트리가 만들어진다.

```python
# ✅ 고친 코드
for v, wv in graph[u]:
    if not visited[v]:
        heapq.heappush(pq, (wv, v))           # 간선 하나의 가중치만
```

(7) 위상 정렬에서 사이클 판정을 빼먹는다

```python
# ❌ 틀린 코드
while q:
    u = q.popleft()
    order.append(u)
    for v in graph[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
return order                      # 사이클이면 짧은 리스트를 그냥 돌려준다
```

왜: 사이클 위의 정점은 진입차수가 0이 되지 못해 큐에 들어가지 못한다. 그래서 `order`에는 사이클 밖 정점만 담기고, 검사를 안 하면 "부분 답"을 정답처럼 출력하게 된다.

```python
# ✅ 고친 코드
return order if len(order) == n else []       # 길이가 N 미만이면 사이클
```

(8) 진입차수를 반대 방향으로 센다

```python
# ❌ 틀린 코드
for _ in range(m):
    u, v = map(int, input().split())   # u 를 먼저 해야 한다는 뜻
    graph[u].append(v)
    indeg[u] += 1                      # 출발지를 올렸다
```

왜: 진입차수는 "그 정점으로 들어오는 간선 수"이므로 도착지 `v`만 올려야 한다. 출발지를 올리면 선행 조건이 없는 정점의 차수가 0이 아니게 되어 큐가 처음부터 비고, 멀쩡한 DAG를 사이클로 오판한다.

```python
# ✅ 고친 코드
for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    indeg[v] += 1                      # 도착지만 올린다
```

**다음 챕터로**

- Ch9의 BFS와 Ch10의 Dijkstra는 같은 뼈대(거리 배열 + 자료구조에서 하나 꺼내 이웃 완화)를 공유한다. 다른 것은 "무엇을 꺼내는 통이냐"뿐이다 — 큐냐, 우선순위 큐냐, 덱이냐.
- Union-Find는 MST뿐 아니라 "같은 그룹인가"를 묻는 모든 문제에서 다시 등장한다. 이 챕터에서 손에 익혀 두면 이후 그래프·집합 문제의 절반이 짧아진다.
- 위상 정렬은 "순서가 정해진 상태 공간"이라는 점에서 이후의 DP와 이어진다. DAG 위에서는 위상 순서대로 훑는 것이 곧 올바른 계산 순서다.
