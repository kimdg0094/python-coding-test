## L7. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

Ch9에서 배운 것을 한 장으로 묶고, 문제를 만나면 바로 꺼내 쓸 수 있는 뼈대와 함정 목록으로 정리한다.

**개념 지도**

```text
                    graph = (V, E)
                          │
              ┌───────────┴───────────┐
        adjacency matrix        adjacency list
        O(V^2) space            O(V+E) space
        edge query O(1)         neighbor scan O(deg)
              └───────────┬───────────┘
                          │  traversal
              ┌───────────┴───────────┐
        DFS (stack/recursion)     BFS (queue)
        go deep, backtrack        expand layer by layer
              │                       │
    components, path, cycle     shortest dist (unweighted)
              │                       │
              └───────────┬───────────┘
                          │
              grid : cell is a vertex, 4-dir is an edge
                          │
              ┌───────────┴───────────┐
        multi-source BFS         all weights = w
        (push every source)      dist x w  -> Ch10 dijkstra
```

한 줄로 요약하면 이렇다. **저장 방식(행렬/리스트)을 고르고 → 탐색 방식(DFS/BFS)을 고른다.** 거리가 필요 없으면 DFS, 필요하면 BFS다. 격자는 그래프를 따로 만들지 않고 좌표 그대로 쓰는 특수 케이스이고, 간선 가중치가 서로 달라지는 순간 BFS를 버리고 Ch10으로 넘어간다.

**뼈대 코드**

(1) 입력 → 인접 리스트

```python
import sys
input = sys.stdin.readline

N, M = map(int, input().split())
adj = [[] for _ in range(N + 1)]      # ← 0-based면 range(N)
for _ in range(M):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)                  # ← 방향 그래프면 이 줄을 지운다
# for i in range(N + 1): adj[i].sort()   # ← 이웃을 번호순으로 볼 때만
```

(2) DFS — 재귀와 명시적 스택

```python
import sys
sys.setrecursionlimit(300000)         # ← 정점이 1만을 넘으면 필수

visited = [False] * (N + 1)

def dfs(u):                           # 재귀 버전
    visited[u] = True
    for v in adj[u]:                  # ← 여기에 문제별 처리를 넣는다
        if not visited[v]:
            dfs(v)

def dfs_stack(s):                     # 스택 버전 (깊이 제한 없음)
    st = [s]
    visited[s] = True
    while st:
        u = st.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True     # push 하는 순간 표시
                st.append(v)
```

(3) BFS — 거리와 경로 복원

```python
from collections import deque

def bfs(start, goal):
    dist = [-1] * (N + 1)
    par = [-1] * (N + 1)              # 경로 복원용 부모
    dist[start] = 0
    q = deque([start])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:         # 미방문 = 아직 거리 없음
                dist[v] = dist[u] + 1
                par[v] = u
                q.append(v)
    if dist[goal] == -1:
        return -1, []
    path, cur = [], goal              # goal 에서 거꾸로 따라 올라간다
    while cur != -1:
        path.append(cur)
        cur = par[cur]
    path.reverse()
    return dist[goal], path
```

(4) 격자 BFS

```python
from collections import deque

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))   # ← 8방향이면 대각선 4개 추가

def grid_bfs(grid, H, W, sr, sc):
    dist = [[-1] * W for _ in range(H)]
    dist[sr][sc] = 0
    q = deque([(sr, sc)])
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < H and 0 <= nc < W):
                continue              # 경계 밖
            if dist[nr][nc] != -1:
                continue              # 이미 방문
            if grid[nr][nc] == '0':   # ← 벽 판정은 문제마다 바뀜
                continue
            dist[nr][nc] = dist[r][c] + 1
            q.append((nr, nc))
    return dist
```

(5) 연결 요소 세기 · 다중 시작 BFS

```python
from collections import deque

count = 0                             # 연결 요소 개수
visited = [False] * (N + 1)
for s in range(1, N + 1):             # ← 0-based면 range(N)
    if not visited[s]:
        count += 1
        visited[s] = True
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append(v)

# 다중 시작 BFS: 시작점을 전부 dist 0 으로 두고 한꺼번에 큐에 넣는다
q = deque()
for v in sources:                     # ← 시작점 목록은 문제마다 바뀜
    dist[v] = 0
    q.append(v)
# 이후 while 루프는 일반 BFS와 완전히 같다
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 정점이 적고(대략 `V ≤ 2000`) "두 점이 이어졌나"를 자주 묻는다 | 인접행렬 | 칸 하나만 보면 끝 | 공간 `O(V^2)`, 질의 `O(1)` |
| 간선이 정점 수의 몇 배 수준(희소)이고 탐색을 돌린다 | 인접리스트 | 실제 있는 간선만 저장 | 공간 `O(V+E)`, 탐색 `O(V+E)` |
| 연결 요소 개수, 경로 존재 여부, 사이클 유무 | DFS | 거리는 필요 없고 도달만 보면 된다 | `O(V+E)` |
| 최소 이동 횟수, 최단 간선 수, 층별 처리 | BFS | 처음 도달한 순간이 곧 최단 | `O(V+E)` |
| 격자에서 최단 이동 | 격자 BFS | 칸=정점, 한 칸 이동=비용 1 | `O(H*W)` |
| 여러 출발점에서 동시에 번진다 | 다중 시작 BFS | 시작점을 한꺼번에 큐에 넣으면 끝 | `O(V+E)` |
| 간선 가중치가 전부 같은 상수 `w` | BFS 후 `× w` | 간선 수 최소 = 비용 최소 | `O(V+E)` |
| 정점이 수만 개이고 깊이가 깊어질 수 있다 | 스택 DFS 또는 BFS | 재귀 한도를 아예 피한다 | `O(V+E)` |
| 간선 가중치가 서로 다르다 | Ch10 Dijkstra | BFS의 층 논증이 깨진다 | `O(E log V)` |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 정점·간선·차수·경로·사이클·연결 요소가 각각 무엇인지.
- [ ] 설명할 수 있다: 무방향 그래프에서 차수의 합이 왜 간선 수의 두 배인지.
- [ ] 설명할 수 있다: 인접행렬과 인접리스트의 공간·질의·순회 복잡도가 왜 그렇게 되는지.
- [ ] 설명할 수 있다: 어떤 상황에서 인접행렬이 인접리스트보다 유리한지, 그 기준이 무엇인지.
- [ ] 설명할 수 있다: DFS가 "깊이 들어갔다 되돌아온다"는 것이 스택에서 어떤 모양으로 나타나는지.
- [ ] 설명할 수 있다: DFS를 재귀로 짤 때와 명시적 스택으로 짤 때의 장단점.
- [ ] 설명할 수 있다: BFS가 왜 가중치 없는 그래프의 최단 거리를 주는지(큐 안의 거리가 두 종류뿐이라는 층 논증).
- [ ] 설명할 수 있다: 같은 그래프를 DFS와 BFS로 훑었을 때 방문 순서가 왜 달라지는지.
- [ ] 설명할 수 있다: 방문 표시를 큐에 넣을 때 해야 하는 이유와, 꺼낼 때 하면 무엇이 깨지는지.
- [ ] 설명할 수 있다: 탐색의 복잡도 `O(V + E)`에서 `V`와 `E`가 각각 어디서 나온 항인지.
- [ ] 설명할 수 있다: 격자 문제를 그래프로 바꾸는 관점(칸=정점, 상하좌우 인접=간선).
- [ ] 설명할 수 있다: 다중 시작 BFS가 시작점마다 따로 돌리는 것보다 왜 빠른지.
- [ ] 설명할 수 있다: 간선 가중치가 모두 같을 때 BFS로 충분한 이유와, 달라지는 순간 왜 틀리는지.
- [ ] 설명할 수 있다: BFS로 거리뿐 아니라 실제 경로를 복원하는 방법(부모 배열).

**⚠️ 자주 하는 실수**

(1) 무방향 그래프인데 한 방향만 넣는다

```python
# ❌ 틀린 코드
for _ in range(M):
    u, v = map(int, input().split())
    adj[u].append(v)          # v -> u 가 없다
```

왜: 무방향 간선 하나는 "양쪽으로 갈 수 있다"는 뜻이라 두 리스트에 모두 들어가야 한다. 한쪽만 넣으면 `v`에서 출발한 탐색이 `u`를 영원히 못 찾아, 연결 요소가 실제보다 많이 세어지거나 거리가 `-1`로 남는다.

```python
# ✅ 고친 코드
for _ in range(M):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)
```

(2) 방문 표시를 큐에서 꺼낼 때 한다

```python
# ❌ 틀린 코드
q = deque([start])
while q:
    u = q.popleft()
    visited[u] = True         # 꺼낼 때 표시
    for v in adj[u]:
        if not visited[v]:
            q.append(v)       # 같은 정점이 여러 번 들어간다
```

왜: `u`를 꺼내 이웃 `v`를 넣은 뒤, 아직 큐에 남아 있던 다른 정점도 같은 `v`를 넣는다. `v`가 큐에 중복으로 쌓여 큐 길이가 최악 `O(E)`까지 부풀고, 두 번째로 꺼낸 `v`가 거리를 더 큰 값으로 덮어써 최단성이 깨진다.

```python
# ✅ 고친 코드
q = deque([start])
visited[start] = True
while q:
    u = q.popleft()
    for v in adj[u]:
        if not visited[v]:
            visited[v] = True     # push 하는 순간 표시
            q.append(v)
```

(3) 재귀 DFS가 깊이 제한에 걸린다

```python
# ❌ 틀린 코드
def dfs(u):                   # N = 100000, 그래프가 한 줄 사슬이면
    visited[u] = True         # 재귀 깊이가 100000 까지 간다
    for v in adj[u]:
        if not visited[v]:
            dfs(v)            # RecursionError
```

왜: 파이썬의 기본 재귀 한도는 약 1000이다. 사슬 모양 그래프에서는 재귀 깊이가 정점 수만큼 깊어져 `N`이 1만만 넘어도 바로 터진다.

```python
# ✅ 고친 코드
import sys
sys.setrecursionlimit(300000)     # 한도를 올리거나
st = [s]                          # 아예 명시적 스택으로 바꾼다
visited[s] = True
while st:
    u = st.pop()
    for v in adj[u]:
        if not visited[v]:
            visited[v] = True
            st.append(v)
```

(4) 큐를 리스트로 만들고 앞에서 꺼낸다

```python
# ❌ 틀린 코드
q = [start]
while q:
    u = q.pop(0)              # 리스트 앞에서 빼기 = O(N)
```

왜: 리스트의 `pop(0)`은 뒤의 원소를 전부 한 칸씩 당기므로 한 번에 `O(N)`이다. 정점이 10만 개면 BFS 전체가 `O(V^2)`가 되어 시간 초과가 난다.

```python
# ✅ 고친 코드
from collections import deque
q = deque([start])
while q:
    u = q.popleft()           # 양끝 연산이 O(1)
```

(5) 격자에서 경계 검사를 빠뜨린다

```python
# ❌ 틀린 코드
nr, nc = r + dr, c + dc
if grid[nr][nc] == '1':       # nr 이 -1 이면 마지막 행을 읽는다
    ...
```

왜: 파이썬의 음수 인덱스는 예외가 아니라 "뒤에서부터"로 해석된다. `nr = -1`이면 맨 아랫줄을 읽어, 위쪽 벽 너머와 아래쪽 끝이 이어진 것처럼 탐색이 새어 나간다. 오른쪽·아래쪽으로 넘칠 때만 `IndexError`가 나서 더 찾기 어렵다.

```python
# ✅ 고친 코드
nr, nc = r + dr, c + dc
if 0 <= nr < H and 0 <= nc < W and grid[nr][nc] == '1':
    ...
```

(6) 인접행렬을 곱셈으로 만든다

```python
# ❌ 틀린 코드
adj = [[0] * N] * N           # 같은 리스트 하나를 N번 참조
adj[0][1] = 1                 # 모든 행의 1번 칸이 1이 된다
```

왜: `[x] * N`은 `x`를 `N`번 복사하는 게 아니라 같은 객체를 `N`번 가리킨다. 바깥쪽에 쓰면 행이 전부 같은 리스트가 되어, 한 칸만 고쳐도 모든 행이 동시에 바뀐다.

```python
# ✅ 고친 코드
adj = [[0] * N for _ in range(N)]   # 행마다 새 리스트를 만든다
adj[0][1] = 1
```

(7) 시작점의 거리를 초기화하지 않는다

```python
# ❌ 틀린 코드
dist = [-1] * N
q = deque([start])            # dist[start] 가 -1 로 남아 있다
while q:
    u = q.popleft()
    for v in adj[u]:
        if dist[v] == -1:
            dist[v] = dist[u] + 1   # -1 + 1 = 0 부터 시작한다
```

왜: `dist[start]`가 `-1`이면 "미방문"으로 취급돼 시작점이 다시 큐에 들어갈 수 있고, 거리 계산도 한 칸씩 밀린다. `-1`은 미방문 표시와 거리 저장을 겸하고 있으므로 시작점만은 반드시 `0`으로 못 박아야 한다.

```python
# ✅ 고친 코드
dist = [-1] * N
dist[start] = 0               # 미방문 표시와 거리를 겸하는 배열
q = deque([start])
```

**다음 챕터로**

- Ch9에서는 간선의 비용이 전부 같다고 보고 "간선 수"만 셌다. Ch10은 간선마다 비용이 다른 세계로 넘어가, 큐 대신 **우선순위 큐**로 "지금 가장 가까운 정점"을 꺼내는 Dijkstra를 배운다.
- BFS의 층 논증이 왜 무너지는지를 이해했다면, Dijkstra가 왜 "확정" 개념을 따로 두는지, 그리고 왜 음수 간선에서 깨지는지가 자연스럽게 이어진다.
- 여기서 익힌 인접 리스트·`visited`·`dist` 배열은 Ch10의 모든 알고리즘에서 그대로 재사용된다.
