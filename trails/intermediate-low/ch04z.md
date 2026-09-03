## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 레슨은 Ch4에서 배운 BFS를 한 장으로 묶고, 문제를 만났을 때 바로 꺼내 쓸 수 있는 뼈대와 판단 기준을 정리한다. 새 개념은 없다.

**개념 지도**

BFS는 "큐로 층을 하나씩 밀어낸다" 하나에서 갈라져 나온다. 정점이 무엇이냐(번호·좌표·상태)와 간선의 비용이 무엇이냐(1·0/1)만 바뀐다.

```text
         BFS = expand layer by layer with a queue
                             |
   +-----------------+-------+---------+----------------+
   v                 v                 v                v
   graph BFS         grid BFS          multi-source     state BFS
   dist[v]           dist[r][c]        all start at 0   dist[r][c][s]
   |                 |                 |                |
   v                 v                 v                v
   min edge count    shortest path     nearest source   key, wall break
   components        maze escape       spread time      direction, mod
   |                                                    |
   v                                                    v
   parent[] kept                                        0-1 BFS
   path restore                                         cost 0 -> front
```

- 네 갈래 모두 **큐 하나·`dist` 하나**로 돌아간다. 다른 것은 "정점을 무엇으로 부르느냐"뿐이다: 번호 `v`, 좌표 `(r, c)`, 좌표+상태 `(r, c, s)`.
- 다중 시작점은 "시작점이 여러 개인 같은 BFS"다. 처음 큐에 여럿을 넣는 것 말고는 코드가 똑같다.
- 0-1 BFS만 자료구조가 큐에서 **덱**으로 바뀐다. 비용 0 간선을 앞에 넣어 층 순서를 지키기 위해서다.

**뼈대 코드**

```python
# (1) 그래프 BFS — dist 하나로 방문 여부(-1)와 거리를 함께 관리
from collections import deque

def bfs(start, graph, V):
    dist = [-1] * (V + 1)            # -1 = 미방문
    dist[start] = 0
    q = deque([start])
    while q:
        cur = q.popleft()
        if cur == target:            # 조기 종료 (필요할 때만) # ← 문제마다 바뀜
            break
        for nxt in graph[cur]:
            if dist[nxt] == -1:      # 아직 값이 없을 때만
                dist[nxt] = dist[cur] + 1
                q.append(nxt)        # push하는 순간 방문 확정
    return dist
```

```python
# (2) 격자 BFS — 칸이 정점, 4방향 이동이 간선(비용 1)
from collections import deque

dr = (-1, 1, 0, 0)
dc = (0, 0, -1, 1)                   # 8방향이면 4개 추가 # ← 문제마다 바뀜

dist = [[-1] * M for _ in range(N)]
dist[sr][sc] = 0
q = deque([(sr, sc)])
while q:
    r, c = q.popleft()
    for d in range(4):
        nr, nc = r + dr[d], c + dc[d]
        if not (0 <= nr < N and 0 <= nc < M):   # 범위 검사가 항상 먼저
            continue
        if dist[nr][nc] != -1:
            continue
        if grid[nr][nc] == 1:        # 이동 가능 조건 # ← 문제마다 바뀜
            continue
        dist[nr][nc] = dist[r][c] + 1
        q.append((nr, nc))
```

```python
# (3) 다중 시작점 BFS — 시작점 전부를 거리 0으로 먼저 넣는다
from collections import deque

q = deque()
dist = [[-1] * M for _ in range(N)]
for r in range(N):
    for c in range(M):
        if grid[r][c] == SOURCE:     # 시작점의 정의 # ← 문제마다 바뀜
            dist[r][c] = 0
            q.append((r, c))
# 이후 루프는 (2)와 글자 하나 다르지 않다.
# 결과 dist[r][c] = "가장 가까운 시작점까지의 거리"
# 전체 확산 시간을 묻는다면 도달한 칸들의 dist 최댓값이 답
```

```python
# (4) 상태 BFS — 좌표에 상태를 붙이고 방문 배열의 차원을 늘린다
from collections import deque

S = K + 1                            # 상태 가짓수 # ← 문제마다 바뀜
dist = [[[-1] * S for _ in range(M)] for _ in range(N)]
dist[sr][sc][0] = 0
q = deque([(sr, sc, 0)])
while q:
    r, c, s = q.popleft()
    for d in range(4):
        nr, nc = r + dr[d], c + dc[d]
        if not (0 <= nr < N and 0 <= nc < M):
            continue
        ns = next_state(s, nr, nc)   # 상태 전이 규칙 # ← 문제마다 바뀜
        if ns is None:               # 그 상태로는 못 감(문·부수기 소진 등)
            continue
        if dist[nr][nc][ns] != -1:   # 같은 칸이라도 상태가 다르면 다른 정점
            continue
        dist[nr][nc][ns] = dist[r][c][s] + 1
        q.append((nr, nc, ns))
answer = min(d for d in dist[er][ec] if d != -1)   # 도착 칸의 모든 상태 중 최소
```

```python
# (5) 0-1 BFS — 비용이 0과 1 두 종류일 때. 덱의 앞/뒤를 쓴다
from collections import deque

INF = float('inf')
dist = [[INF] * M for _ in range(N)]
dist[sr][sc] = 0
dq = deque([(sr, sc)])
while dq:
    r, c = dq.popleft()
    for d in range(4):
        nr, nc = r + dr[d], c + dc[d]
        if not (0 <= nr < N and 0 <= nc < M):
            continue
        w = 1 if grid[nr][nc] == 1 else 0        # 간선 비용 # ← 문제마다 바뀜
        if dist[r][c] + w < dist[nr][nc]:        # 더 짧아질 때만 갱신
            dist[nr][nc] = dist[r][c] + w
            if w == 0:
                dq.appendleft((nr, nc))          # 같은 층 -> 앞
            else:
                dq.append((nr, nc))              # 다음 층 -> 뒤
```

```python
# (6) 경로 복원 — 처음 방문시킨 직전 정점을 남긴다
parent = [-1] * (V + 1)
# BFS 안에서: dist[nxt] = dist[cur] + 1; parent[nxt] = cur; q.append(nxt)

if dist[goal] == -1:
    print(-1)
else:
    path = []
    v = goal
    while v != -1:                   # 시작점의 parent가 -1이라 자연히 멈춘다
        path.append(v)
        v = parent[v]
    path.reverse()
    print(*path)
# 격자면 parent[r][c] = (r, c) 튜플로, 또는 "어느 방향에서 왔는가"만 저장
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 간선 비용이 모두 같은 최단 거리 | BFS | 층 단위로 퍼지므로 첫 도달이 곧 최단 | O(V+E) |
| 격자에서 최소 이동 횟수 | 격자 BFS(`dist` 배열) | 칸=정점, 4방향=간선, 비용 1 | O(N·M) |
| "가장 가까운 X까지"(X가 여럿) | 다중 시작점 BFS | 모든 X를 거리 0으로 함께 넣으면 한 번에 끝 | O(N·M) |
| 좌표에 조건이 붙는 최단(열쇠·부수기) | 상태 BFS(차원 추가) | 같은 칸이라도 상태가 다르면 다른 정점 | O(N·M·S) |
| 비용이 0과 1 두 종류 | 0-1 BFS(덱) | 0은 앞, 1은 뒤 → 우선순위 큐가 필요 없다 | O(V+E) |
| 비용이 제각각인 최단 | 다익스트라(이후 챕터) | 층 구조가 깨져 BFS·0-1 BFS 모두 틀린다 | O(E log V) |
| 거리뿐 아니라 경로 자체가 필요 | BFS + `parent` 기록 | 처음 방문시킨 정점만 남기면 역추적된다 | O(V+E) |
| "번지는 것"과 "움직이는 것"이 함께 | BFS 두 번(두 단계) | 번짐 시각은 이동과 무관하게 먼저 확정된다 | O(N·M) |
| 도달 가능성·연결 요소만 | DFS든 BFS든 무관 | 순서가 답에 영향을 주지 않는다 | O(V+E) |
| 모든 경로 나열·경로 개수 | DFS 백트래킹 (Ch3) | 표시를 되돌려야 하는데 큐로는 불가능하다 | 경로 수에 비례(지수) |
| 재귀 깊이가 위험한 큰 격자 | BFS(또는 반복 DFS) | 큐는 콜스택 한도와 무관하다 | O(N·M) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: BFS가 최단거리를 보장하는 이유를 "층 단위 확장 → 첫 도달이 최소"로 유도하는 과정.
- [ ] 설명할 수 있다: 큐 안에는 왜 항상 거리 `d`와 `d+1` 두 종류만 들어 있는지.
- [ ] 설명할 수 있다: 방문 표시를 pop이 아니라 **push 시점**에 해야 하는 이유와, 어기면 무엇이 터지는지.
- [ ] 설명할 수 있다: `dist` 배열 하나로 방문 여부와 거리를 동시에 관리하는 방법(`-1` = 미방문).
- [ ] 설명할 수 있다: 시간복잡도 O(V+E)를 "정점당 push·pop 1회 + 인접리스트 총 순회 2E"로 세는 과정.
- [ ] 설명할 수 있다: `list.pop(0)`이 왜 O(N)이고 전체가 왜 O(V²)가 되는지.
- [ ] 설명할 수 있다: 다중 시작점 BFS가 왜 한 번의 BFS로 "가장 가까운 시작점까지의 거리"를 주는지.
- [ ] 설명할 수 있다: 어떤 값을 방문 배열의 차원에 넣어야 하고 어떤 값은 넣으면 안 되는지, 그 판단 기준.
- [ ] 설명할 수 있다: 상태를 추가하면 복잡도가 어떻게 곱해지는지(`R·C·(K+1)`, `R·C·2^k`).
- [ ] 설명할 수 있다: 0-1 BFS가 다익스트라 없이도 되는 이유(덱의 불변식).
- [ ] 설명할 수 있다: 간선 비용이 서로 다르면 BFS가 왜 틀리는지, 그때 무엇으로 바꾸는지.
- [ ] 설명할 수 있다: "간선 수"와 "지나는 칸 수"의 차이(+1이 어디서 나오는지).
- [ ] 설명할 수 있다: `parent`를 남겨 최단 경로를 복원하는 절차와, 역추적이 멈추는 조건.
- [ ] 설명할 수 있다: 두 단계 BFS(번짐 시각 계산 → 그 위에서 이동)로 문제를 나누는 이유.

**⚠️ 자주 하는 실수**

1. **방문 표시를 pop 시점에 한다**

   ```python
   # ❌ 틀린 코드
   while q:
       cur = q.popleft()
       visited[cur] = True           # 꺼낼 때 표시
       for nxt in graph[cur]:
           if not visited[nxt]:
               q.append(nxt)         # 큐 안에 이미 있는 정점을 또 넣는다
   ```

   왜: 큐에서 대기 중인 정점은 아직 미표시라, 그 이웃들이 저마다 다시 넣는다. 격자에서는 한 칸이 최대 4번 들어가고 그 4개가 또 이웃을 넣어 큐가 눈덩이처럼 불어난다 → 시간·메모리 초과.

   ```python
   # ✅ 고친 코드
   while q:
       cur = q.popleft()
       for nxt in graph[cur]:
           if dist[nxt] == -1:
               dist[nxt] = dist[cur] + 1
               q.append(nxt)         # 넣는 순간 확정 -> 정점당 정확히 1회
   ```

2. **큐를 리스트로 만들고 `pop(0)`으로 꺼낸다**

   ```python
   # ❌ 틀린 코드
   q = [start]
   while q:
       cur = q.pop(0)                # 맨 앞을 빼면 뒤를 전부 한 칸씩 당긴다
   ```

   왜: 리스트는 값이 연속으로 놓인 배열이라 `pop(0)` 한 번이 O(len)이다. 정점 V개면 전체가 O(V²)가 되어, V가 10^5만 되어도 통과할 수 없다.

   ```python
   # ✅ 고친 코드
   from collections import deque
   q = deque([start])
   while q:
       cur = q.popleft()             # 양끝 연산이 O(1)
   ```

3. **상태를 방문 배열에 넣지 않는다**

   ```python
   # ❌ 틀린 코드
   dist = [[-1] * M for _ in range(N)]        # 차원이 2개뿐
   q = deque([(sr, sc, 0)])
   while q:
       r, c, key = q.popleft()
       ...
       if dist[nr][nc] == -1:                 # key를 무시하고 판단
           dist[nr][nc] = dist[r][c] + 1
           q.append((nr, nc, key))
   ```

   왜: 열쇠를 줍고 되돌아올 때 지나야 하는 칸이 "이미 방문됨"으로 막힌다. 정답 경로가 통째로 사라져 도달 가능한 문제에 `-1`이 나온다.

   ```python
   # ✅ 고친 코드
   dist = [[[-1] * 2 for _ in range(M)] for _ in range(N)]   # (r, c, key)
   ...
       if dist[nr][nc][nkey] == -1:           # 상태까지 포함해 판단
           dist[nr][nc][nkey] = dist[r][c][key] + 1
           q.append((nr, nc, nkey))
   ```

4. **시작점의 거리를 초기화하지 않는다**

   ```python
   # ❌ 틀린 코드
   dist = [[-1] * M for _ in range(N)]
   q = deque([(sr, sc)])             # 큐에는 넣었지만 dist는 여전히 -1
   while q:
       r, c = q.popleft()
       ...
       dist[nr][nc] = dist[r][c] + 1 # -1 + 1 = 0 -> 거리가 전부 밀린다
   ```

   왜: 시작 칸이 미방문으로 남아 있어 나중에 다시 큐에 들어갈 수도 있고, 거리 계산의 기준점이 `-1`이 되어 모든 값이 1씩 어긋난다.

   ```python
   # ✅ 고친 코드
   dist = [[-1] * M for _ in range(N)]
   dist[sr][sc] = 0                  # 큐에 넣는 것과 표시는 항상 한 쌍
   q = deque([(sr, sc)])
   ```

5. **시작점이 여럿인데 하나씩 BFS를 돌린다**

   ```python
   # ❌ 틀린 코드
   best = INF
   for (r, c) in sources:            # 시작점마다 격자 전체를 훑는다
       d = bfs(r, c)
       best = min(best, d[er][ec])
   ```

   왜: 시작점이 `S`개면 O(S·N·M)이 된다. 격자가 1000×1000이고 시작점이 수천 개면 그대로 시간 초과다.

   ```python
   # ✅ 고친 코드
   q = deque()
   for (r, c) in sources:
       dist[r][c] = 0                # 전부 거리 0으로 함께 넣고
       q.append((r, c))
   # 한 번만 퍼뜨린다 -> O(N·M)
   ```

6. **간선 비용이 다른데 BFS로 최단을 구한다**

   ```python
   # ❌ 틀린 코드
   for nxt, w in graph[cur]:         # w가 2, 5, 7 ... 제각각
       if dist[nxt] == -1:
           dist[nxt] = dist[cur] + w # 첫 도달이 최소라는 보장이 깨진다
           q.append(nxt)
   ```

   왜: BFS의 최단 보장은 "모든 간선의 비용이 같다"에서만 나온다. 비용이 다르면 큐에서 먼저 나온 정점이 더 가깝다는 근거가 없어져, 비용 큰 간선 하나로 먼저 닿은 값이 그대로 굳는다.

   ```python
   # ✅ 고친 코드
   import heapq                      # 비용이 제각각이면 다익스트라
   pq = [(0, start)]
   while pq:
       d, cur = heapq.heappop(pq)    # 항상 '가장 가까운 것'부터 확정
       if d > dist[cur]:
           continue
   # 비용이 0과 1 두 종류뿐이면 heapq 대신 0-1 BFS(덱)로 충분하다
   ```

7. **"간선 수"와 "지나는 칸 수"를 혼동한다**

   ```python
   # ❌ 틀린 코드
   print(dist[N-1][M-1])             # 이동 횟수를 그대로 출력
   ```

   왜: `dist`는 **간선 수**(이동 횟수)이고, 문제가 묻는 "지나는 칸의 개수"는 그보다 1 크다. 게다가 도달 불가(`-1`)일 때 `+1`을 해 버리면 `0`이라는 엉뚱한 값이 나간다.

   ```python
   # ✅ 고친 코드
   ans = dist[N-1][M-1]
   print(ans + 1 if ans != -1 else -1)   # 도달 불가는 별도로 처리
   # 또는 시작 칸의 dist를 1로 두고 시작해 처음부터 '칸 수'로 세도 된다
   ```

**다음 챕터로**

- 이 챕터의 BFS는 "모든 간선 비용이 같다"를 전제로 최단을 보장했다. 비용이 제각각이 되는 순간 그 보장이 깨지고, 우선순위 큐로 "가장 가까운 것부터 확정"하는 다익스트라가 필요해진다.
- 0-1 BFS는 그 중간 지점이다. 덱의 앞/뒤만으로 우선순위 큐 흉내를 내는 이 아이디어가, 이후 최단 경로 알고리즘을 배울 때 "왜 우선순위가 필요한가"를 이해하는 발판이 된다.
- 상태 BFS에서 익힌 "정점을 새로 정의한다"는 감각은 이후 상태 압축·비트마스크 탐색으로 그대로 이어진다.
