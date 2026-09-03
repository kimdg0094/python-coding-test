## L3. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 레슨은 Ch3에서 배운 DFS를 한 장으로 묶고, 문제를 만났을 때 바로 꺼내 쓸 수 있는 뼈대와 판단 기준을 정리한다. 새 개념은 없다.

**개념 지도**

Ch3의 도구는 전부 "재귀 + `visited`" 하나에서 갈라져 나온다. 무대(인접리스트·격자·트리)와 목적(방문·복원)이 바뀔 뿐 뼈대는 같다.

```text
            DFS = go deep, come back on return
                             |
   +-----------------+-------+---------+----------------+
   v                 v                 v                v
   adjacency list    2-D grid          tree             backtracking
   visited[v]        visited[r][c]     parent arg       mark / unmark
   |                 |                 |                |
   v                 v                 v                v
   reachability      flood fill        depth on entry   all simple
   components        area, label       size on return   paths, counts
   |                 |
   v                 v
   2-coloring        8 offsets
   3-color cycle     explicit stack
```

- 왼쪽 두 갈래(인접리스트·격자)는 "빠짐없이 한 번씩 방문"이 목적이라 `visited`를 **끝까지 켜 둔다.**
- 오른쪽 끝(백트래킹)만 `visited`를 **되돌린다.** 목적이 "한 경로"가 아니라 "모든 경로"이기 때문이다. 이 한 줄 차이가 두 세계를 가른다.
- 트리는 사이클이 없으므로 `visited` 없이 `parent` 인자 하나로 역주행만 막으면 된다.

**뼈대 코드**

```python
# (1) 그래프 DFS — 재귀판과 반복(명시적 스택)판
import sys
sys.setrecursionlimit(10 ** 6)

def dfs(cur):
    visited[cur] = True              # 들어오자마자 표시 (규칙 1)
    # 여기서 방문 순서 기록·카운트 등    # ← 문제마다 바뀜
    for nxt in graph[cur]:
        if not visited[nxt]:
            dfs(nxt)

def dfs_iter(start):                 # 깊이가 수십만을 넘길 위험이 있으면 이쪽
    stack = [start]
    visited[start] = True            # push 시점에 표시 (중복 push 방지)
    while stack:
        cur = stack.pop()
        for nxt in graph[cur]:
            if not visited[nxt]:
                visited[nxt] = True
                stack.append(nxt)
```

```python
# (2) 격자 DFS — 이동 조건만 갈아 끼우면 대부분의 격자 문제가 된다
dr = (-1, 1, 0, 0)
dc = (0, 0, -1, 1)                   # 8방향이면 여기에 4개 추가 # ← 문제마다 바뀜

def dfs_grid(r, c):
    visited[r][c] = True
    for d in range(4):
        nr, nc = r + dr[d], c + dc[d]
        if not (0 <= nr < N and 0 <= nc < M):   # 범위 검사가 항상 먼저
            continue
        if visited[nr][nc]:
            continue
        if grid[nr][nc] != 1:        # 이동 가능 조건 # ← 문제마다 바뀜
            continue
        dfs_grid(nr, nc)
```

```python
# (3) 연결 요소 세기 / 각 요소의 크기
count = 0
best = 0
for i in range(N):
    for j in range(M):
        if grid[i][j] == 1 and not visited[i][j]:   # 새 덩어리의 첫 칸
            count += 1
            area = flood(i, j)       # 방문한 칸 수를 돌려주게 만든다
            best = max(best, area)
# 그래프판: for s in range(1, V + 1): if not visited[s]: count += 1; dfs(s)
```

```python
# (4) 백트래킹 DFS — 모든 경로/조합을 세거나 나열할 때만
def dfs_path(cur):
    if cur == goal:                  # 종료 조건 # ← 문제마다 바뀜
        record()
        return
    for nxt in adj[cur]:
        if not visited[nxt]:
            visited[nxt] = True
            path.append(nxt)
            dfs_path(nxt)
            path.pop()
            visited[nxt] = False     # 되돌리기 — 이 줄이 (1)과의 유일한 차이
```

```python
# (5) 사이클 판정 — 방향 그래프는 3색, 무방향은 부모 비교
def dfs_directed(cur):               # 0=미방문, 1=현재 경로 위, 2=완료
    state[cur] = 1
    for nxt in graph[cur]:
        if state[nxt] == 1:
            return True              # 현재 경로로 되돌아감 = 사이클
        if state[nxt] == 0 and dfs_directed(nxt):
            return True
    state[cur] = 2
    return False

def dfs_undirected(cur, parent):
    visited[cur] = True
    for nxt in adj[cur]:
        if not visited[nxt]:
            if dfs_undirected(nxt, cur):
                return True
        elif nxt != parent:          # 부모가 아닌 방문 정점 = 사이클
            return True
    return False
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 도달 가능한가 / 연결되어 있는가 | DFS(재귀 또는 스택) | 방문만 하면 되고 순서는 답에 영향이 없다 | O(V+E) |
| 덩어리 개수·크기 | 미방문 시작점마다 DFS | 시작 횟수 = 요소 수, 방문 칸 수 = 크기 | O(V+E) |
| 격자 영역 칠하기·번호 매기기 | 격자 DFS(플러드 필) | 이동 조건만 갈아 끼우면 같은 뼈대 | O(N·M) |
| 재귀 깊이가 수만 이상일 위험 | 명시적 스택 DFS | 콜스택 한도·OS 스택과 무관해진다 | O(V+E) |
| 모든 경로 나열·경로 개수 | 백트래킹 DFS(표시 복원) | 다른 경로가 같은 정점을 다시 써야 한다 | 경로 수에 비례(지수) |
| 방향 그래프 사이클 판정 | 3색 DFS | "현재 경로 위"와 "완료"를 구분해야 오판이 없다 | O(V+E) |
| 무방향 그래프 사이클 판정 | 부모 비교 DFS | 부모로 되짚는 간선만 예외 처리하면 된다 | O(V+E) |
| 선후 관계를 만족하는 순서 | 후위 기록 + 역순(위상 정렬) | 자식을 다 마친 뒤 기록하므로 앞→뒤가 보장된다 | O(V+E) |
| 서브트리 값 누적 | 반환값 있는 후위 DFS | 자식 결과를 받아 자기 값을 확정한다 | O(V) |
| **간선 비용이 같은 최단 거리** | **BFS (Ch4)** | DFS의 "처음 도달"은 최단이 아니다 | O(V+E) |
| 좌표에 상태가 붙는 최단 | 상태 BFS (Ch4) | 층 구조가 있어야 최단이 보장된다 | O(V × 상태 수) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: DFS의 "되돌아오기"가 코드의 어느 부분에서 일어나는지(= `return`과 콜스택).
- [ ] 설명할 수 있다: 방문 표시를 함수 진입 즉시 해야 하는 이유와, 미루면 무엇이 터지는지.
- [ ] 설명할 수 있다: 재귀 DFS와 명시적 스택 DFS가 같은 순회를 하는데도 방문 순서가 달라질 수 있는 이유.
- [ ] 설명할 수 있다: 시간복잡도가 O(V+E)인 근거를 "호출 V번 + 인접리스트 총 순회 2E"로 세는 과정.
- [ ] 설명할 수 있다: 연결 요소 개수가 왜 "DFS 시작 횟수"와 같은지.
- [ ] 설명할 수 있다: 격자 DFS에서 범위 검사를 값 읽기보다 먼저 해야 하는 이유(음수 인덱스는 예외가 아니라 오답을 만든다).
- [ ] 설명할 수 있다: 순회용 DFS는 `visited`를 켜 두고, 백트래킹 DFS는 되돌리는 이유.
- [ ] 설명할 수 있다: 방향 그래프 사이클 판정에 왜 2색이 아니라 3색이 필요한지.
- [ ] 설명할 수 있다: 무방향 그래프에서 부모를 예외로 두지 않으면 어떤 그래프가 오판되는지.
- [ ] 설명할 수 있다: 위상 정렬에서 "후위 기록의 역순"이 왜 모든 간선의 방향을 지키는지.
- [ ] 설명할 수 있다: 트리 DFS에서 `visited` 대신 `parent`만으로 충분한 이유.
- [ ] 설명할 수 있다: DFS로 최단거리를 구하려면 왜 모든 경로를 봐야 하고, 그래서 왜 BFS를 쓰는지.
- [ ] 설명할 수 있다: 재귀 깊이가 최악에 V가 되는 입력의 모양과, 그때 무엇으로 바꿔야 하는지.

**⚠️ 자주 하는 실수**

1. **방문 표시를 안 하거나 늦게 한다**

   ```python
   # ❌ 틀린 코드
   def dfs(cur):
       for nxt in graph[cur]:
           if not visited[nxt]:
               visited[nxt] = True   # 표시가 '다음 노드'에만 찍힌다
               dfs(nxt)
   dfs(start)                        # 시작 노드는 끝내 표시되지 않는다
   ```

   왜: 시작 노드가 미표시라 이웃이 다시 시작 노드로 들어오고, 무방향 그래프에서는 그대로 무한 재귀가 된다. 표시 위치가 두 군데로 흩어지면 어디를 빠뜨렸는지도 보이지 않는다.

   ```python
   # ✅ 고친 코드
   def dfs(cur):
       visited[cur] = True           # 들어오자마자, 한 곳에서만
       for nxt in graph[cur]:
           if not visited[nxt]:
               dfs(nxt)
   dfs(start)                        # 시작 노드도 진입하며 자동 표시된다
   ```

2. **재귀 한도를 안 올리거나, 올려도 부족하다**

   ```python
   # ❌ 틀린 코드
   def dfs(r, c):
       visited[r][c] = True
       ...
   dfs(0, 0)      # 1000x1000 뱀 모양 격자 -> 깊이 10^6 -> RecursionError
   ```

   왜: 파이썬 기본 재귀 한도는 약 1000이라 정점이 몇천만 되어도 죽는다. `setrecursionlimit`으로 올려도 OS가 주는 실제 스택이 먼저 바닥나면 프로세스가 통째로 죽는다.

   ```python
   # ✅ 고친 코드
   import sys
   sys.setrecursionlimit(10 ** 6)    # 깊이 수천~수만이면 이걸로 충분

   stack = [(0, 0)]                  # 깊이가 수십만을 넘길 수 있으면 반복으로
   visited[0][0] = True
   while stack:
       r, c = stack.pop()
       # 이웃을 검사해 push (push 시점에 방문 표시)
   ```

3. **격자에서 범위 검사를 빠뜨린다**

   ```python
   # ❌ 틀린 코드
   nr, nc = r + dr[d], c + dc[d]
   if grid[nr][nc] == 1 and not visited[nr][nc]:
       dfs(nr, nc)
   ```

   왜: `nr`이 `-1`이면 파이썬은 오류를 내지 않고 **맨 아래 줄**을 읽는다. 예외가 안 나므로 디버깅이 어렵고, 격자가 위아래로 이어진 것처럼 동작해 조용히 틀린 답이 나온다.

   ```python
   # ✅ 고친 코드
   nr, nc = r + dr[d], c + dc[d]
   if 0 <= nr < N and 0 <= nc < M and not visited[nr][nc] and grid[nr][nc] == 1:
       dfs(nr, nc)                   # 범위 -> 방문 -> 값 순서로 검사
   ```

4. **모든 경로를 세는데 방문 표시를 되돌리지 않는다**

   ```python
   # ❌ 틀린 코드
   def dfs(cur):
       global count
       if cur == N:
           count += 1
           return
       for nxt in adj[cur]:
           if not visited[nxt]:
               visited[nxt] = True
               dfs(nxt)              # 복원이 없다
   ```

   왜: 첫 경로가 쓴 정점이 영원히 막혀, 그 정점을 지나는 다른 경로가 전부 사라진다. 네 갈래가 있어도 답이 `1`로 나온다.

   ```python
   # ✅ 고친 코드
           if not visited[nxt]:
               visited[nxt] = True
               dfs(nxt)
               visited[nxt] = False  # 이 경로를 벗어나면 다시 쓸 수 있게
   ```

5. **시작점 하나만 보고 끝낸다**

   ```python
   # ❌ 틀린 코드
   count = 1
   dfs(1)                            # 정점 1이 속한 덩어리만 방문된다
   print(count)
   ```

   왜: 그래프가 여러 덩어리로 끊어져 있을 수 있다. 격자도 마찬가지라 섬 하나만 세고 끝난다. 예제가 우연히 연결 그래프면 통과해 버려서 더 위험하다.

   ```python
   # ✅ 고친 코드
   count = 0
   for s in range(1, V + 1):
       if not visited[s]:
           count += 1                # 미방문 시작점마다 새 덩어리
           dfs(s)
   print(count)
   ```

6. **무방향 그래프 사이클 판정에서 부모를 빼지 않는다**

   ```python
   # ❌ 틀린 코드
   def dfs(cur):
       visited[cur] = True
       for nxt in adj[cur]:
           if not visited[nxt]:
               dfs(nxt)
           else:
               found = True          # 방금 온 부모도 '방문됨'이다
   ```

   왜: 간선이 `1-2` 하나뿐인 그래프에서도 `2`가 부모 `1`을 보고 사이클이라 답한다. 무방향 간선은 양쪽 인접리스트에 모두 들어 있기 때문이다.

   ```python
   # ✅ 고친 코드
   def dfs(cur, parent):
       visited[cur] = True
       for nxt in adj[cur]:
           if not visited[nxt]:
               dfs(nxt, cur)
           elif nxt != parent:       # 부모로 되짚는 간선만 예외
               found = True
   ```

7. **DFS의 첫 도달 거리를 최단이라고 믿는다**

   ```python
   # ❌ 틀린 코드
   def dfs(r, c, d):
       if visited[r][c]:
           return
       visited[r][c] = True
       dist[r][c] = d                # 처음 닿은 거리를 최단으로 기록
       for k in range(4):
           dfs(r + dr[k], c + dc[k], d + 1)
   ```

   왜: DFS는 한 방향으로 끝까지 파고들므로, 최단이 3인 칸에 길이 11짜리 경로로 먼저 닿을 수 있다. 첫 도달 거리는 "탐색 순서가 우연히 만든 경로의 길이"일 뿐이다.

   ```python
   # ✅ 고친 코드
   from collections import deque
   q = deque([(sr, sc)])
   dist[sr][sc] = 0                  # BFS: 층 단위로 퍼지므로
   while q:                          # 처음 적힌 값이 곧 최단
       r, c = q.popleft()
       # 이웃에 dist[r][c] + 1을 적으며 push
   ```

**다음 챕터로**

- Ch4의 BFS는 이 챕터의 뼈대에서 자료구조 하나만 바꾼다: 스택(재귀) → 큐(`deque`). 방문 배열·4방향 오프셋·범위 검사는 그대로 쓴다.
- 바뀌는 것은 **보장**이다. 층 단위로 퍼지므로 "처음 도달한 거리 = 최단거리"가 되고, 이 챕터에서 DFS로는 못 하던 최단거리 문제가 열린다.
- 여기서 익힌 "연결 요소 = 시작 횟수", "상태를 방문 키에 넣는다"는 감각은 Ch4의 다중 시작점 BFS·상태 BFS로 그대로 이어진다.
