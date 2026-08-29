## L6. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch9(그래프 탐색)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. 새 문법은 없다. 인접리스트·`visited`·DFS(재귀/스택)·BFS(`deque`)·격자 4방향 탐색만으로 12문제를 푼다.

- **반복 훈련 개념**
- 인접리스트 구성: 무방향은 양쪽, 방향은 한쪽만 — `adj[u].append(v); adj[v].append(u)`
- DFS(재귀/스택) + 방문 표시: 진입 즉시 마킹, 이웃은 정렬해 번호 순으로 — `for v in adj[u]: if not visited[v]: dfs(v)`
- BFS + 거리 배열: 큐에 넣는 순간 거리 확정 — `dist[v] = dist[u] + 1; q.append(v)`
- 연결 요소: 미방문 정점을 만날 때마다 탐색을 새로 시작하고 개수·크기를 센다 — `for s in range(N): if not visited[s]: ...`
- 격자 탐색: 칸=정점, 4방향(또는 8방향)=간선, 경계 검사 필수 — `0 <= nx < H and 0 <= ny < W`

- **코딩테스트 출제 맵**: 이 챕터의 유형은 백준 「단계별로 풀어보기」의 'DFS와 BFS' 단계(연결 요소·미로 탐색·이분 그래프·불 번짐·벽 부수기 류), 프로그래머스 「코딩테스트 고득점 Kit」의 'DFS/BFS', NeetCode 150의 'Graphs'(Number of Islands·Max Area of Island·Rotting Oranges 류), 삼성 SW 역량테스트의 '시뮬레이션·BFS' 유형에 그대로 등장한다. 이 레슨의 유형 확장 문제는 그 대표 유형을 소재·수치·조건을 새로 만들어 재구성한 것이다.

- **문제 구성표**

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 친구 목록 정리 | Easy | 인접리스트 구성 + 정렬 | 반복 훈련 |
| 2 | 일방통행 노선도 순회 | Easy | 재귀 DFS 방문 순서 + 미도달 수 | 반복 훈련 |
| 3 | 감염 단계별 인원 | Easy | BFS 거리 배열 → 거리별 집계 | 반복 훈련 |
| 4 | 동아리 그룹 크기 | Medium | 연결 요소 크기 + 스택 DFS | 반복 훈련 |
| 5 | 창고 로봇 최단 이동 | Medium | 격자 BFS + 장애물 + 시작/도착 문자 | 반복 훈련 |
| 6 | 배선 고리 검사 | Medium | DFS + 부모 추적 사이클 판정 | 유형 확장 (백준 'DFS와 BFS' 단계 스타일) |
| 7 | 두 팀으로 나누기 | Medium | BFS 2색 칠하기(이분 그래프) | 유형 확장 (백준 'DFS와 BFS' 단계 스타일) |
| 8 | 섬 개수와 가장 큰 섬 | Medium | 격자 8방향 DFS + 크기 최댓값 | 반복 훈련 |
| 9 | 최단 경로 복원 | Medium | BFS 부모 배열 + 역추적 | 유형 확장 (프로그래머스 Kit 'DFS/BFS' 스타일) |
| 10 | 불 번지는 창고 탈출 | Hard | 다중 시작 BFS + 시간 비교 BFS | 유형 확장 (백준 'DFS와 BFS' 단계 · 삼성 SW 'BFS' 스타일) |
| 11 | 벽 하나 부수고 탈출 | Hard | 상태 1비트 BFS `(x, y, 부순 여부)` | 유형 확장 (백준 'DFS와 BFS' 단계 스타일) |
| 12 | 안전 지대 최대 개수 | Hard | 임계값 반복 × 격자 연결 요소 | 반복 훈련 |

**문제**

**1) 친구 목록 정리** · Easy

- **요구사항**: `N`명의 사람(1번~`N`번)과 `M`쌍의 친구 관계(무방향)가 주어진다. 인접리스트를 만들어 각 사람의 친구 목록을 정리하라. 사람 `i`의 줄에는 `친구 수`를 먼저 쓰고, 이어서 친구 번호를 **오름차순**으로 공백 구분해 출력한다(친구가 없으면 `0`만).
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 100`, `0 ≤ M ≤ 500`). 이어 `M`개 줄에 `u v` (1-based, `u ≠ v`, 같은 쌍은 최대 한 번).
- **출력**: `N`개 줄. `i`번째 줄에 `i`번의 친구 수와 친구 번호들.
- **예제**: `4 3 / 1 2 / 1 3 / 2 3` → `2 2 3 / 2 1 3 / 2 1 2 / 0` · `3 0` → `0 / 0 / 0`
- **셀프체크**: 1-based라 배열 크기를 `N+1`로 잡았는가? 무방향이므로 `u`의 목록에 `v`, `v`의 목록에 `u`를 **둘 다** 넣었는가? 친구 수 `0`인 사람도 빠뜨리지 않고 한 줄을 출력했는가?

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
idx = 0
N = int(data[idx]); idx += 1
M = int(data[idx]); idx += 1
adj = [[] for _ in range(N + 1)]
for _ in range(M):
    u = int(data[idx]); idx += 1
    v = int(data[idx]); idx += 1
    adj[u].append(v)
    adj[v].append(u)
out = []
for i in range(1, N + 1):
    adj[i].sort()
    out.append(' '.join(map(str, [len(adj[i])] + adj[i])))
print('\n'.join(out))
@@TESTS
--IN
4 3
1 2
1 3
2 3
--OUT
2 2 3
2 1 3
2 1 2
0
--IN
3 0
--OUT
0
0
0
--IN
5 4
5 1
4 1
3 1
2 1
--OUT
4 2 3 4 5
1 1
1 1
1 1
1 1
@@EXPL
(1) 접근·핵심 아이디어

- "각 정점의 이웃 목록"이 곧 인접리스트다. 간선을 읽으면서 양쪽 리스트에 서로를 넣기만 하면 자료구조가 완성된다.
- 출력은 오름차순이어야 하므로 리스트마다 `sort()` 한 번. 간선이 들어온 순서는 제멋대로일 수 있으니 정렬 없이 출력하면 정답이 유일하지 않다.
- 복잡도: 간선 저장 `O(M)`, 정렬은 리스트 길이 합이 `2M`이라 `O(M log M)` 이내.

(2) 코드 단계별

- 1-based 번호를 그대로 쓰기 위해 `adj = [[] for _ in range(N + 1)]`로 `N+1`칸을 만든다(0번은 비워 둠).
- 간선 `u v`마다 `adj[u].append(v)`, `adj[v].append(u)` — 무방향이라 양쪽.
- `1..N` 순서로 각 리스트를 정렬하고 `[len(adj[i])] + adj[i]`를 공백으로 이어 한 줄씩 모은 뒤 줄바꿈으로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "N+1 크기 인접리스트" → "간선마다 양쪽 append" → "각 리스트 정렬" → "친구 수 + 목록 출력". 경계값은 `M = 0`(전부 `0` 한 줄씩)과 한 사람에게 친구가 몰린 경우(예제 3)다.
```

**2) 일방통행 노선도 순회** · Easy

- **요구사항**: 역 `0`~`N-1`이 **일방통행** 노선(방향 간선)으로 이어져 있다. 출발역 `s`에서 재귀 DFS로 방문하는 순서를 출력하되, 갈 수 있는 이웃 역 중 **번호가 작은 역부터** 들어간다. 이어 둘째 줄에 `s`에서 **도달하지 못한 역의 개수**를 출력한다.
- **입력**: 첫 줄 `N M s` (`1 ≤ N ≤ 100`, `0 ≤ M ≤ 500`, `0 ≤ s < N`). 이어 `M`개 줄에 방향 간선 `u v` (u→v).
- **출력**: 첫 줄 방문 순서(공백 구분), 둘째 줄 미도달 역 수.
- **예제**: `5 5 0 / 0 2 / 0 1 / 1 3 / 2 3 / 4 0` → `0 1 3 2 / 1` · `3 2 2 / 0 1 / 1 2` → `2 / 2`
- **셀프체크**: 방향 간선이므로 `adj[u]`에만 넣었는가(양쪽에 넣으면 4번 역이 방문돼 오답)? 인접리스트를 정렬해야 "작은 번호 먼저"가 보장된다. 미도달 수는 `N - len(방문 순서)`로 바로 구할 수 있다.

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
idx = 0
N = int(data[idx]); idx += 1
M = int(data[idx]); idx += 1
s = int(data[idx]); idx += 1
adj = [[] for _ in range(N)]
for _ in range(M):
    u = int(data[idx]); idx += 1
    v = int(data[idx]); idx += 1
    adj[u].append(v)
for i in range(N):
    adj[i].sort()
visited = [False] * N
order = []
def dfs(u):
    visited[u] = True
    order.append(u)
    for v in adj[u]:
        if not visited[v]:
            dfs(v)
dfs(s)
print(' '.join(map(str, order)))
print(N - len(order))
@@TESTS
--IN
5 5 0
0 2
0 1
1 3
2 3
4 0
--OUT
0 1 3 2
1
--IN
3 2 2
0 1
1 2
--OUT
2
2
--IN
4 4 0
0 1
1 2
2 3
3 0
--OUT
0 1 2 3
0
@@EXPL
(1) 접근·핵심 아이디어

- DFS는 "갈 수 있는 데까지 들어갔다가 막히면 되돌아오는" 순회다. 재귀 호출이 되돌아오기(backtrack)를 대신하므로, 진입 즉시 방문 표시 + 순서 기록만 하면 된다.
- 방향 그래프라 `u→v` 한쪽만 저장한다. 예제 1의 `4→0`은 4에서 0으로 가는 길일 뿐, 0에서 4로는 못 가므로 4는 미도달이다.
- `N ≤ 100`이라 재귀 깊이는 최대 100 — 파이썬 기본 한도(약 1000) 안이다. 복잡도 `O(N + M)`(+정렬).

(2) 코드 단계별

- 간선을 `adj[u].append(v)`로 한쪽만 저장하고 각 리스트를 정렬(작은 번호 먼저).
- `dfs(u)`: `visited[u] = True`, `order.append(u)` 후 정렬된 이웃을 보며 미방문이면 재귀.
- 예제 1 검산: 0 → 이웃 [1, 2] 중 1 → 1의 이웃 3 → 3은 이웃 없음, 복귀 → 0의 다음 이웃 2 → 2의 이웃 3은 방문됨. 순서 `0 1 3 2`, 미도달은 4 하나.
- 마지막에 `N - len(order)`가 도달 못한 역 수.

(3) 스스로 다시 짤 때 생각 순서

- "방향 인접리스트(한쪽만) + 정렬" → "visited/order 준비" → "s에서 재귀 DFS" → "순서 출력, N − 방문 수 출력". 예제 3처럼 사이클이 있어도 `visited` 덕분에 멈춘다.
```

**3) 감염 단계별 인원** · Easy

- **요구사항**: `N`명(0번~`N-1`번)이 무방향 접촉 관계로 이어져 있다. 0번이 0일차 최초 감염자이고, 매일 감염자와 접촉한 사람은 **다음 날** 감염된다. 0일차부터 마지막 감염일까지 **각 날 새로 감염된 인원 수**를 공백으로 구분해 출력하라(끝내 감염되지 않는 사람은 무시).
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 200`, `0 ≤ M ≤ 1000`). 이어 `M`개 줄 `u v` (0-based, 무방향).
- **출력**: 0일차, 1일차, … 순으로 감염 인원 수를 한 줄에.
- **예제**: `6 5 / 0 1 / 0 2 / 1 3 / 2 3 / 3 4` → `1 2 1 1` · `1 0` → `1`
- **셀프체크**: "d일차 감염자 = 0번으로부터 최단 거리 d인 사람"임을 이해했는가? 0일차는 항상 `1`(0번 자신)이다. 도달 못한 사람(`dist == -1`)을 집계에서 제외했는가? 거리별 개수 배열의 크기는 "최대 거리 + 1"이다.

```runner
@@SOLUTION
import sys
from collections import deque
data = sys.stdin.read().split()
idx = 0
N = int(data[idx]); idx += 1
M = int(data[idx]); idx += 1
adj = [[] for _ in range(N)]
for _ in range(M):
    u = int(data[idx]); idx += 1
    v = int(data[idx]); idx += 1
    adj[u].append(v)
    adj[v].append(u)
dist = [-1] * N
dist[0] = 0
q = deque([0])
while q:
    u = q.popleft()
    for v in adj[u]:
        if dist[v] == -1:
            dist[v] = dist[u] + 1
            q.append(v)
maxd = max(dist)
cnt = [0] * (maxd + 1)
for d in dist:
    if d != -1:
        cnt[d] += 1
print(' '.join(map(str, cnt)))
@@TESTS
--IN
6 5
0 1
0 2
1 3
2 3
3 4
--OUT
1 2 1 1
--IN
1 0
--OUT
1
--IN
4 3
0 1
0 2
0 3
--OUT
1 3
@@EXPL
(1) 접근·핵심 아이디어

- 매일 "아는 사람 전원이 동시에 이웃에게 전파"하는 구조는 BFS의 층(layer) 전개와 정확히 같다. 어떤 사람이 감염되는 날 = 0번으로부터의 최단 거리(간선 수).
- 따라서 BFS 한 번으로 `dist`를 구한 뒤, 같은 거리끼리 묶어 세면 답이다. 도달 못한 사람은 `-1`로 남으니 집계에서 뺀다.
- 복잡도 `O(N + M)`.

(2) 코드 단계별

- 무방향 간선을 양쪽에 저장하고 `dist`를 `-1`로 초기화, `dist[0] = 0`.
- BFS: 큐에서 꺼낸 `u`의 이웃 중 `dist == -1`인 사람만 `dist[u] + 1`로 확정하며 큐에 넣는다(처음 도달 = 최단).
- `max(dist)`가 마지막 감염일. 크기 `maxd + 1`의 `cnt` 배열을 만들어 `dist`가 `-1`이 아닌 값만 누적.
- 예제 1 검산: 거리 0 → {0}, 1 → {1, 2}, 2 → {3}, 3 → {4}, 5번은 미도달 → `1 2 1 1`.

(3) 스스로 다시 짤 때 생각 순서

- "0번에서 BFS로 dist" → "최대 거리 크기의 카운트 배열" → "-1 제외하고 집계" → "출력". 경계값: `N = 1`이면 `1`만 출력, 0번이 고립돼 있어도 0일차 `1`은 나온다.
```

**4) 동아리 그룹 크기** · Medium

- **요구사항**: `N`명(1번~`N`번)의 학생 사이에 `M`개의 "같은 동아리" 관계(무방향)가 있다. 직접·간접으로 이어진 학생들은 하나의 그룹이다. 그룹의 개수와, 각 그룹의 인원수를 **내림차순**으로 출력하라.
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 200`, `0 ≤ M ≤ 1000`). 이어 `M`개 줄 `u v` (1-based).
- **출력**: 첫 줄 그룹 수, 둘째 줄 각 그룹 인원수를 내림차순 공백 구분.
- **예제**: `7 4 / 1 2 / 2 3 / 4 5 / 3 1` → `4 / 3 2 1 1` · `3 0` → `3 / 1 1 1`
- **셀프체크**: 미방문 정점에서 탐색을 새로 시작할 때마다 "그룹 하나"가 생기고, 그 탐색에서 꺼낸 정점 수가 그룹 크기다. 간선 `3 1`처럼 이미 같은 그룹인 쌍이 다시 와도 크기가 중복 계산되지 않는가? 혼자인 학생도 크기 `1`인 그룹이다.

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
idx = 0
N = int(data[idx]); idx += 1
M = int(data[idx]); idx += 1
adj = [[] for _ in range(N + 1)]
for _ in range(M):
    u = int(data[idx]); idx += 1
    v = int(data[idx]); idx += 1
    adj[u].append(v)
    adj[v].append(u)
visited = [False] * (N + 1)
sizes = []
for s in range(1, N + 1):
    if visited[s]:
        continue
    visited[s] = True
    st = [s]
    size = 0
    while st:
        x = st.pop()
        size += 1
        for y in adj[x]:
            if not visited[y]:
                visited[y] = True
                st.append(y)
    sizes.append(size)
sizes.sort(reverse=True)
print(len(sizes))
print(' '.join(map(str, sizes)))
@@TESTS
--IN
7 4
1 2
2 3
4 5
3 1
--OUT
4
3 2 1 1
--IN
3 0
--OUT
3
1 1 1
--IN
5 4
1 2
2 3
3 4
4 5
--OUT
1
5
@@EXPL
(1) 접근·핵심 아이디어

- 그룹 = 연결 요소. `1..N`을 훑다가 미방문 정점을 만나면 그 자리에서 탐색을 시작해 덩어리 전체를 방문 표시하고, 그때 꺼낸 정점 수를 세면 그룹 크기다.
- 스택 DFS에서 "스택에 넣는 순간" 방문 표시를 해야 같은 정점이 두 번 들어가 크기가 부풀지 않는다(예제 1의 삼각형 1-2-3에서 중요).
- 복잡도 `O(N + M)` + 크기 정렬 `O(N log N)`.

(2) 코드 단계별

- 1-based라 `N+1` 크기 인접리스트·`visited`.
- 각 시작점 `s`에서 스택 DFS: `pop`할 때 `size += 1`, 미방문 이웃은 마킹하며 `push`.
- 탐색이 끝나면 `sizes`에 크기를 추가. 모든 정점 처리 후 내림차순 정렬해 개수와 목록을 출력.
- 예제 1 검산: {1,2,3} 크기 3, {4,5} 크기 2, {6}, {7} 각 1 → `4` / `3 2 1 1`.

(3) 스스로 다시 짤 때 생각 순서

- "visited 준비" → "정점 순회, 미방문이면 새 그룹" → "스택 DFS로 크기 세기" → "크기 내림차순 정렬 출력". 경계값: `M = 0`이면 그룹 `N`개가 전부 크기 1, 전부 이어져 있으면 그룹 1개에 크기 `N`.
```

**5) 창고 로봇 최단 이동** · Medium

- **요구사항**: `H×W` 창고 격자에 `.`(빈 바닥), `#`(선반), `S`(로봇 시작), `E`(목표 지점)이 있다. 로봇은 상하좌우로 한 칸씩 움직이며 선반은 지나갈 수 없다. `S`에서 `E`까지의 **최소 이동 횟수**를 출력하라. 도달 불가면 `-1`.
- **입력**: 첫 줄 `H W` (`1 ≤ H, W ≤ 30`). 이어 `H`개 줄, 각 줄 `W`개 문자(공백 없음). `S`와 `E`는 정확히 하나씩.
- **출력**: 최소 이동 횟수 또는 `-1`.
- **예제**: `3 4 / S..# / .#.. / ...E` → `5` · `2 3 / S#E / .#.` → `-1`
- **셀프체크**: 출력이 "지나는 칸 수"가 아니라 "이동 횟수"다(`S`와 `E`가 인접하면 `1`). `S`와 `E`의 위치를 격자에서 먼저 찾았는가? `E`도 `#`이 아니므로 통과 조건 `!= '#'`으로 걸러야 큐에 들어간다.

```runner
@@SOLUTION
import sys
from collections import deque
data = sys.stdin.read().split()
idx = 0
H = int(data[idx]); idx += 1
W = int(data[idx]); idx += 1
grid = []
for _ in range(H):
    grid.append(data[idx]); idx += 1
for i in range(H):
    for j in range(W):
        if grid[i][j] == 'S':
            sx, sy = i, j
        elif grid[i][j] == 'E':
            ex, ey = i, j
dist = [[-1] * W for _ in range(H)]
dist[sx][sy] = 0
q = deque([(sx, sy)])
while q:
    x, y = q.popleft()
    if x == ex and y == ey:
        break
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < H and 0 <= ny < W and dist[nx][ny] == -1 and grid[nx][ny] != '#':
            dist[nx][ny] = dist[x][y] + 1
            q.append((nx, ny))
print(dist[ex][ey])
@@TESTS
--IN
3 4
S..#
.#..
...E
--OUT
5
--IN
2 3
S#E
.#.
--OUT
-1
--IN
1 2
SE
--OUT
1
--IN
3 3
S..
###
..E
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- 한 칸 이동 = 비용 1이므로 격자 BFS가 곧 최단 경로다. 시작칸을 거리 0으로 두고 물결처럼 퍼뜨리면 `E`에 처음 닿는 순간의 거리가 최소 이동 횟수다.
- `dist`를 `-1`로 초기화해 "미방문"과 "도달 불가"를 한 배열로 표현한다. BFS가 끝난 뒤 `dist[E]`가 `-1`이면 그대로 `-1`을 출력하면 된다.
- 복잡도 `O(H·W)`.

(2) 코드 단계별

- 격자를 읽으며 `S`, `E`의 좌표를 찾는다.
- `dist[sx][sy] = 0`으로 시작, 큐에서 꺼낸 칸의 4방향 이웃 중 "경계 안 + 미방문 + 선반 아님"인 칸만 `dist + 1`로 확정하며 큐에 넣는다.
- `E`를 꺼내는 순간 더 볼 필요가 없어 `break`(없어도 정답은 같다).
- 예제 1 검산: (0,0)→(0,1)→(0,2)→(1,2)→(1,3)→(2,3) 5번 이동. 아래쪽으로 돌아가도 5번.

(3) 스스로 다시 짤 때 생각 순서

- "S/E 좌표 찾기" → "dist -1 초기화, S는 0" → "4방향 BFS(경계·미방문·`#` 아님)" → "dist[E] 출력". 경계값: `S`·`E`가 붙어 있으면 `1`, 선반이 한 줄을 완전히 막으면 `-1`(예제 4).
```

**6) 배선 고리 검사** · Medium

- **요구사항**: `N`개의 단자(0번~`N-1`번)를 `M`개의 케이블(무방향)로 연결했다. 어느 단자에서 출발해 서로 다른 케이블만 따라 다시 그 단자로 돌아오는 **고리(사이클)** 가 하나라도 있으면 `YES`, 없으면 `NO`를 출력하라. 배선이 여러 덩어리로 나뉘어 있을 수도 있다.
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 100`, `0 ≤ M ≤ 500`). 이어 `M`개 줄 `u v` (0-based, `u ≠ v`, 같은 쌍은 최대 한 번).
- **출력**: `YES` 또는 `NO`.
- **예제**: `4 4 / 0 1 / 1 2 / 2 0 / 2 3` → `YES` · `4 3 / 0 1 / 1 2 / 2 3` → `NO`
- **셀프체크**: 무방향 그래프에서 이웃이 "방금 온 부모"인 건 사이클이 아니다 — 부모를 제외하고 **이미 방문한 이웃**을 만났을 때만 사이클이다. 덩어리가 여러 개일 수 있으니 모든 미방문 정점에서 탐색을 시작했는가? 검산 팁: 사이클이 없는 그래프(숲)는 간선이 최대 `N-1`개다.

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
idx = 0
N = int(data[idx]); idx += 1
M = int(data[idx]); idx += 1
adj = [[] for _ in range(N)]
for _ in range(M):
    u = int(data[idx]); idx += 1
    v = int(data[idx]); idx += 1
    adj[u].append(v)
    adj[v].append(u)
visited = [False] * N
def dfs(u, parent):
    visited[u] = True
    for v in adj[u]:
        if not visited[v]:
            if dfs(v, u):
                return True
        elif v != parent:
            return True
    return False
found = False
for s in range(N):
    if not visited[s]:
        if dfs(s, -1):
            found = True
            break
print('YES' if found else 'NO')
@@TESTS
--IN
4 4
0 1
1 2
2 0
2 3
--OUT
YES
--IN
4 3
0 1
1 2
2 3
--OUT
NO
--IN
6 5
0 1
2 3
3 4
4 5
5 3
--OUT
YES
--IN
1 0
--OUT
NO
@@EXPL
(1) 접근·핵심 아이디어

- DFS로 내려가다가 "이미 방문한 정점"을 다시 만나면 어딘가로 되돌아오는 길이 있다는 뜻, 즉 사이클이다. 단, 무방향 그래프에서는 방금 지나온 부모도 이웃 목록에 있으므로 부모는 예외로 둬야 한다(이걸 빼먹으면 간선 하나만 있어도 `YES`가 나온다).
- 그래프가 여러 덩어리일 수 있어 미방문 정점마다 DFS를 새로 시작한다(예제 3은 두 번째 덩어리에 고리가 있다).
- `N ≤ 100`이라 재귀 깊이 걱정이 없다. 복잡도 `O(N + M)`.

(2) 코드 단계별

- 무방향 간선을 양쪽에 저장.
- `dfs(u, parent)`: `u`를 마킹하고 이웃 `v`를 본다. 미방문이면 `dfs(v, u)`를 재귀 호출해 그 안에서 사이클이 발견되면 즉시 `True` 전파. 이미 방문했는데 `v != parent`이면 사이클 → `True`.
- 모든 시작점에서 `False`가 나오면 `NO`.
- 예제 1 검산: 0→1→2에서 2의 이웃 0은 방문됨이고 2의 부모(1)가 아니다 → `YES`.

(3) 스스로 다시 짤 때 생각 순서

- "인접리스트" → "dfs(u, parent)로 방문·부모 추적" → "방문한 비부모 이웃 = 사이클" → "덩어리마다 시작". 경계값: 간선 0개·정점 1개(`NO`), 삼각형 하나만 있어도 `YES`. 같은 쌍의 중복 간선이 허용된다면 그것도 고리라 별도 처리가 필요하지만, 이 문제는 중복이 없다.
```

**7) 두 팀으로 나누기** · Medium

- **요구사항**: `N`명(0번~`N-1`번)과 "서로 같은 팀이 되기 싫은" `M`쌍이 주어진다. 모든 쌍을 서로 다른 팀(A/B)에 배정할 수 있으면 첫 줄에 `YES`, 둘째 줄에 각 사람의 팀을 0번부터 공백 구분해 출력하라. 배정 규칙은 "**각 덩어리(연결 요소)에서 번호가 가장 작은 사람이 A팀**"으로 고정한다. 불가능하면 `NO`만 출력.
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 200`, `0 ≤ M ≤ 1000`). 이어 `M`개 줄 `u v` (0-based, 무방향).
- **출력**: `YES` + 팀 배정 한 줄, 또는 `NO`.
- **예제**: `4 4 / 0 1 / 1 2 / 2 3 / 3 0` → `YES / A B A B` · `3 3 / 0 1 / 1 2 / 2 0` → `NO`
- **셀프체크**: 이웃끼리 항상 다른 색이어야 하는 "2색 칠하기(이분 그래프)" 문제다. 색을 칠하다 이웃이 **같은 색**이면 즉시 `NO`. 번호 0부터 순서대로 미방문 정점을 시작점 삼아 A로 두면 "덩어리의 최소 번호가 A"가 자동으로 만족된다. 아무와도 연결되지 않은 사람은 A인가?

```runner
@@SOLUTION
import sys
from collections import deque
data = sys.stdin.read().split()
idx = 0
N = int(data[idx]); idx += 1
M = int(data[idx]); idx += 1
adj = [[] for _ in range(N)]
for _ in range(M):
    u = int(data[idx]); idx += 1
    v = int(data[idx]); idx += 1
    adj[u].append(v)
    adj[v].append(u)
color = [-1] * N
ok = True
for s in range(N):
    if color[s] != -1:
        continue
    color[s] = 0
    q = deque([s])
    while q and ok:
        u = q.popleft()
        for v in adj[u]:
            if color[v] == -1:
                color[v] = 1 - color[u]
                q.append(v)
            elif color[v] == color[u]:
                ok = False
                break
    if not ok:
        break
if ok:
    print('YES')
    print(' '.join('A' if c == 0 else 'B' for c in color))
else:
    print('NO')
@@TESTS
--IN
4 4
0 1
1 2
2 3
3 0
--OUT
YES
A B A B
--IN
3 3
0 1
1 2
2 0
--OUT
NO
--IN
5 2
0 1
3 4
--OUT
YES
A B A A B
--IN
2 0
--OUT
YES
A A
@@EXPL
(1) 접근·핵심 아이디어

- "이웃끼리 다른 팀"은 그래프를 두 색으로 칠하는 문제(이분 그래프 판정)다. BFS로 시작점을 0(A)으로 두고 이웃은 반대 색으로 칠해 나가다가, 이미 칠해진 이웃이 **같은 색**이면 불가능하다.
- 한 덩어리의 2색 칠하기는 "시작 색을 고정하면 유일"하다. 그래서 "덩어리의 최소 번호 = A"라는 규칙을 두면 답이 하나로 정해진다. `0..N-1` 순서로 미방문 정점을 시작점으로 잡으면 그 정점이 자동으로 덩어리의 최소 번호다.
- 홀수 길이 사이클(예제 2의 삼각형)이 있으면 반드시 충돌한다. 복잡도 `O(N + M)`.

(2) 코드 단계별

- `color`를 `-1`(미칠함)로 초기화. 정점 `s`를 순서대로 보며 미칠함이면 `color[s] = 0`으로 두고 BFS 시작.
- 이웃 `v`가 미칠함이면 `1 - color[u]`로 칠하고 큐에 넣는다. 이미 칠해져 있고 `color[v] == color[u]`면 `ok = False`로 끝낸다.
- `ok`이면 `YES`와 함께 `0 → A`, `1 → B`로 바꿔 출력. 아니면 `NO`.
- 예제 3 검산: {0,1} → A B, 2는 혼자라 A, {3,4} → A B → `A B A A B`.

(3) 스스로 다시 짤 때 생각 순서

- "color 배열 -1" → "정점 순서대로 미칠함이면 A로 BFS 시작" → "이웃은 반대색, 같은 색 충돌이면 NO" → "YES + 배정 출력". 경계값: 간선 0개면 전부 A, 홀수 사이클 하나만 있어도 NO. 짝수 사이클(예제 1)은 문제없다.
```

**8) 섬 개수와 가장 큰 섬** · Medium

- **요구사항**: `0`(바다)과 `1`(땅)로 된 격자에서, 상하좌우뿐 아니라 **대각선까지 8방향**으로 이어진 땅을 하나의 섬으로 본다. 섬의 개수와 가장 큰 섬의 칸 수를 출력하라. 섬이 하나도 없으면 `0 0`.
- **입력**: 첫 줄 `H W` (`1 ≤ H, W ≤ 30`). 이어 `H`개 줄, 각 줄 `W`개의 0/1(공백 없음).
- **출력**: `섬 개수 가장 큰 섬 크기`를 공백으로 한 줄에.
- **예제**: `4 5 / 11000 / 01001 / 00010 / 10000` → `3 3` · `2 2 / 00 / 00` → `0 0`
- **셀프체크**: 8방향은 `dx, dy ∈ {-1, 0, 1}`의 조합 9개 중 `(0, 0)`을 뺀 8개다. 대각선으로만 붙은 땅(예제 1의 (1,4)와 (2,3))이 같은 섬으로 묶이는가? 크기는 "스택에서 꺼낸 횟수"로 세면 중복이 없다.

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
idx = 0
H = int(data[idx]); idx += 1
W = int(data[idx]); idx += 1
grid = []
for _ in range(H):
    grid.append(data[idx]); idx += 1
visited = [[False] * W for _ in range(H)]
count = 0
largest = 0
for i in range(H):
    for j in range(W):
        if grid[i][j] == '1' and not visited[i][j]:
            count += 1
            visited[i][j] = True
            st = [(i, j)]
            size = 0
            while st:
                x, y = st.pop()
                size += 1
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < H and 0 <= ny < W and not visited[nx][ny] and grid[nx][ny] == '1':
                            visited[nx][ny] = True
                            st.append((nx, ny))
            if size > largest:
                largest = size
print(count, largest)
@@TESTS
--IN
4 5
11000
01001
00010
10000
--OUT
3 3
--IN
2 2
00
00
--OUT
0 0
--IN
3 3
101
010
101
--OUT
1 5
@@EXPL
(1) 접근·핵심 아이디어

- 섬 = 격자 위의 연결 요소. 다른 점은 간선이 8방향이라는 것뿐이다. 방향 벡터를 `dx, dy`의 이중 루프로 만들되 `(0, 0)`만 건너뛰면 8개가 나온다.
- 각 섬을 탐색할 때 꺼낸 칸 수를 세면 크기가 되고, 그 최댓값을 따로 유지한다. 개수와 크기를 한 번의 순회로 동시에 얻는다.
- 복잡도 `O(H·W)`(칸마다 8이웃 확인).

(2) 코드 단계별

- 격자를 문자열로 읽고 `visited`를 준비.
- 모든 칸을 훑다 "땅 + 미방문"이면 `count += 1`, 스택 DFS 시작. 스택에 넣을 때 마킹.
- `pop`할 때 `size += 1`, 8방향 이웃 중 경계 안·미방문·땅만 push.
- 섬 하나가 끝나면 `largest = max(largest, size)`. 마지막에 `count largest` 출력.
- 예제 1 검산: (0,0)(0,1)(1,1) 크기 3, (1,4)(2,3) 대각선으로 붙어 크기 2, (3,0) 크기 1 → `3 3`. 예제 3은 X자 모양이 대각선으로 전부 이어져 한 섬 크기 5.

(3) 스스로 다시 짤 때 생각 순서

- "visited + 카운터 두 개" → "칸 순회" → "미방문 땅이면 count++ 후 8방향 DFS로 size 세기" → "largest 갱신" → "출력". 경계값: 땅이 없으면 `0 0`, 4방향이었다면 예제 3이 5개 섬이 되므로 방향 수를 꼭 확인.
```

**9) 최단 경로 복원** · Medium

- **요구사항**: 무방향 비가중 그래프에서 `s`에서 `t`까지의 **최단 경로**를 정점 나열로 출력하라. 최단 경로가 여러 개면 정점 번호 나열을 앞에서부터 비교했을 때 **사전순으로 가장 앞선** 것을 출력한다. 도달 불가면 `-1`.
- **입력**: 첫 줄 `N M s t` (`1 ≤ N ≤ 200`, `0 ≤ M ≤ 1000`, 0-based). 이어 `M`개 줄 `u v`.
- **출력**: 경로의 정점을 공백 구분 한 줄(`s == t`면 `s` 하나), 또는 `-1`.
- **예제**: `6 7 0 5 / 0 1 / 0 2 / 1 3 / 2 4 / 3 5 / 4 5 / 1 4` → `0 1 3 5` · `4 2 0 3 / 0 1 / 2 3` → `-1`
- **셀프체크**: BFS에서 정점을 **처음 발견한 순간** `parent[v] = u`를 기록하고, `t`에서 `parent`를 거슬러 올라가 뒤집으면 경로다. 인접리스트를 오름차순으로 정렬해 두면 처음 발견되는 부모가 사전순으로 가장 앞선 경로를 만든다. `s == t`일 때 경로가 `s` 하나로 나오는가?

```runner
@@SOLUTION
import sys
from collections import deque
data = sys.stdin.read().split()
idx = 0
N = int(data[idx]); idx += 1
M = int(data[idx]); idx += 1
s = int(data[idx]); idx += 1
t = int(data[idx]); idx += 1
adj = [[] for _ in range(N)]
for _ in range(M):
    u = int(data[idx]); idx += 1
    v = int(data[idx]); idx += 1
    adj[u].append(v)
    adj[v].append(u)
for i in range(N):
    adj[i].sort()
parent = [-1] * N
visited = [False] * N
visited[s] = True
q = deque([s])
while q:
    u = q.popleft()
    for v in adj[u]:
        if not visited[v]:
            visited[v] = True
            parent[v] = u
            q.append(v)
if not visited[t]:
    print(-1)
else:
    path = []
    cur = t
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    print(' '.join(map(str, path)))
@@TESTS
--IN
6 7 0 5
0 1
0 2
1 3
2 4
3 5
4 5
1 4
--OUT
0 1 3 5
--IN
4 2 0 3
0 1
2 3
--OUT
-1
--IN
3 1 1 1
0 1
--OUT
1
--IN
5 5 0 4
0 3
0 1
3 4
1 2
2 4
--OUT
0 3 4
@@EXPL
(1) 접근·핵심 아이디어

- BFS는 정점을 처음 발견할 때의 거리가 최단이므로, 그 순간의 "누가 나를 발견했는가"(`parent`)를 기록해 두면 `t`에서 거꾸로 따라가 최단 경로를 복원할 수 있다.
- 사전순 최소 보장: 인접리스트를 정렬하면 큐 안의 순서가 "각 정점까지의 사전순 최소 경로" 순서와 같아지고, 다음 층의 정점은 그중 가장 앞선 정점이 먼저 발견한다. 따라서 처음 기록된 부모가 곧 사전순 최소 경로의 직전 정점이다.
- 복잡도 `O(N + M)`(+정렬). 경로 복원은 경로 길이만큼 `O(N)`.

(2) 코드 단계별

- 무방향 간선을 양쪽 저장 후 각 리스트 정렬.
- `parent`를 `-1`로 초기화(시작점의 부모는 `-1`로 남아 역추적 종료 조건이 된다). `s`를 마킹하고 BFS.
- 이웃을 처음 발견하면 마킹 + `parent[v] = u` + 큐 push. 이미 방문한 정점의 부모는 덮어쓰지 않는다(덮어쓰면 최단성이 깨진다).
- `visited[t]`가 거짓이면 `-1`. 아니면 `t`에서 `parent`를 따라 `-1`이 나올 때까지 모아 뒤집어 출력.
- 예제 1 검산: 길이 3인 경로가 `0 1 3 5`, `0 1 4 5`, `0 2 4 5` 세 개. 사전순 최소는 `0 1 3 5`.

(3) 스스로 다시 짤 때 생각 순서

- "정렬된 인접리스트" → "BFS하며 처음 발견 시 parent 기록" → "t 미방문이면 -1" → "parent 역추적 후 reverse". 경계값: `s == t`(경로 `s` 하나), 도달 불가, 그리고 예제 4처럼 사전순으로는 `0 1 …`이 앞서 보여도 더 긴 경로면 안 된다는 점(최단이 우선).
```

**10) 불 번지는 창고 탈출** · Hard

- **요구사항**: `H×W` 격자에 `#`(벽), `.`(빈칸), `F`(불, 여러 곳 가능), `J`(사람, 정확히 하나)가 있다. 매 분마다 (1) 사람은 상하좌우로 한 칸 이동하고, (2) 불은 상하좌우의 벽이 아닌 모든 칸으로 번진다. 사람은 **그 시각에 불이 있거나 그 시각에 불이 도착하는 칸**으로는 이동할 수 없다. 사람이 격자 **바깥으로 나가는** 최소 시간(분)을 출력하라. 격자 가장자리 칸에서 한 번 더 이동하면 바깥이다. 탈출 불가면 `IMPOSSIBLE`.
- **입력**: 첫 줄 `H W` (`1 ≤ H, W ≤ 30`). 이어 `H`개 줄, 각 줄 `W`개 문자.
- **출력**: 최소 시간 또는 `IMPOSSIBLE`.
- **예제**: `3 5 / ##### / F..J. / #####` → `2` · `3 5 / ##### / #J.F. / #####` → `IMPOSSIBLE`
- **셀프체크**: 불은 시작점이 여러 개인 **다중 시작 BFS**로 각 칸의 도착 시각 `fire`를 먼저 구한다(닿지 않는 칸은 무한대). 사람 BFS에서 `d+1` 시각에 들어갈 칸은 `fire[nx][ny] > d+1`이어야 한다(같으면 불과 동시에 도착 → 불가). 격자 밖으로 나가는 이동을 "탈출 성공, 시각 `d+1`"로 처리했는가? 사람이 이미 가장자리에 있으면 답은 `1`이다.

```runner
@@SOLUTION
import sys
from collections import deque
data = sys.stdin.read().split()
idx = 0
H = int(data[idx]); idx += 1
W = int(data[idx]); idx += 1
grid = []
for _ in range(H):
    grid.append(data[idx]); idx += 1
INF = 10 ** 9
fire = [[INF] * W for _ in range(H)]
q = deque()
for i in range(H):
    for j in range(W):
        if grid[i][j] == 'F':
            fire[i][j] = 0
            q.append((i, j))
        elif grid[i][j] == 'J':
            sx, sy = i, j
dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
while q:
    x, y = q.popleft()
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < H and 0 <= ny < W and grid[nx][ny] != '#' and fire[nx][ny] == INF:
            fire[nx][ny] = fire[x][y] + 1
            q.append((nx, ny))
dist = [[-1] * W for _ in range(H)]
dist[sx][sy] = 0
q = deque([(sx, sy)])
ans = -1
while q and ans == -1:
    x, y = q.popleft()
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < H and 0 <= ny < W):
            ans = dist[x][y] + 1
            break
        if grid[nx][ny] != '#' and dist[nx][ny] == -1 and fire[nx][ny] > dist[x][y] + 1:
            dist[nx][ny] = dist[x][y] + 1
            q.append((nx, ny))
print(ans if ans != -1 else 'IMPOSSIBLE')
@@TESTS
--IN
3 5
#####
F..J.
#####
--OUT
2
--IN
3 5
#####
#J.F.
#####
--OUT
IMPOSSIBLE
--IN
5 5
#####
#..F#
#J#.#
#...#
##.##
--OUT
4
--IN
2 3
.J.
###
--OUT
1
@@EXPL
(1) 접근·핵심 아이디어

- 불과 사람이 동시에 움직이지만, 불은 사람의 영향을 받지 않는다. 그래서 먼저 불만 따로 BFS로 퍼뜨려 "각 칸에 불이 도착하는 시각"을 확정해 두면(여러 `F`를 처음부터 큐에 넣는 다중 시작 BFS), 사람 BFS는 그 표만 참조하면 된다.
- 사람이 시각 `d+1`에 어떤 칸에 들어가려면 그 칸의 불 도착 시각이 `d+1`보다 **엄격히** 커야 한다. 같은 시각이면 불에 닿는다.
- 탈출은 "격자 밖으로 나가는 이동"이므로 이웃 좌표가 범위를 벗어나는 순간 `d+1`이 답이다. BFS는 `d`가 작은 순으로 처리하니 처음 발견한 탈출이 최소다. 복잡도 `O(H·W)` 두 번.

(2) 코드 단계별

- 격자를 읽으며 모든 `F`를 `fire = 0`으로 큐에 넣고 `J` 좌표를 기억한다. 불 BFS로 벽이 아닌 칸의 `fire` 시각을 채운다(닿지 않는 칸은 `INF`).
- 사람 BFS: `dist[J] = 0`. 꺼낸 칸의 4방향을 보며 범위 밖이면 `ans = dist + 1`로 종료. 범위 안이면 "벽 아님 + 미방문 + `fire > dist + 1`"일 때만 큐에 넣는다.
- 큐가 비도록 탈출하지 못하면 `IMPOSSIBLE`.
- 예제 3 검산: 불(1,3)이 (3,2)에 3분, (4,2)에 4분에 도착. 사람 (2,1)→(3,1) 1분→(3,2) 2분(불 3 > 2)→(4,2) 3분(불 4 > 3)→바깥 4분. 위쪽 길은 (1,2)에 2분에 도착하려 하지만 불이 1분에 이미 와 있어 막힌다.

(3) 스스로 다시 짤 때 생각 순서

- "불 다중 시작 BFS로 fire 표" → "사람 BFS, 범위 밖 = 탈출" → "입장 조건 fire > d+1" → "못 나가면 IMPOSSIBLE". 경계값: 사람이 가장자리에서 시작하면 `1`(예제 4), 불이 사람 바로 옆이면 그 칸은 시각 1에 불이 와서 못 들어감(예제 2), 불이 없는 입력도 `INF` 덕분에 그대로 동작.
```

**11) 벽 하나 부수고 탈출** · Hard

- **요구사항**: `0`(길)과 `1`(벽)로 된 `H×W` 격자에서 `(0,0)`에서 `(H-1,W-1)`까지 상하좌우로 이동한다. 이동 중 **벽을 최대 한 번** 부수고 지나갈 수 있다(부순 벽 칸도 한 번 이동으로 지난다). 최소 이동 횟수를 출력하라. 불가능하면 `-1`. 시작·도착 칸은 항상 `0`이다.
- **입력**: 첫 줄 `H W` (`1 ≤ H, W ≤ 30`). 이어 `H`개 줄, 각 줄 `W`개의 0/1(공백 없음).
- **출력**: 최소 이동 횟수 또는 `-1`.
- **예제**: `5 3 / 000 / 110 / 000 / 011 / 000` → `6` · `3 3 / 010 / 111 / 010` → `-1`
- **셀프체크**: 방문 상태를 `(x, y)`만으로 두면 "벽을 아직 안 부순 채 도착"과 "이미 부수고 도착"을 구분 못 해 오답이 난다 — `dist[x][y][b]`처럼 **부순 여부 1비트**를 상태에 포함해야 한다. 벽 칸으로는 `b == 0`일 때만 들어가며 그때 `b`가 `1`로 바뀐다. 답은 두 상태 중 `-1`이 아닌 것의 최솟값. `1×1` 격자면 `0`이다.

```runner
@@SOLUTION
import sys
from collections import deque
data = sys.stdin.read().split()
idx = 0
H = int(data[idx]); idx += 1
W = int(data[idx]); idx += 1
grid = []
for _ in range(H):
    grid.append(data[idx]); idx += 1
dist = [[[-1] * 2 for _ in range(W)] for _ in range(H)]
dist[0][0][0] = 0
q = deque([(0, 0, 0)])
while q:
    x, y, b = q.popleft()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if not (0 <= nx < H and 0 <= ny < W):
            continue
        if grid[nx][ny] == '0':
            if dist[nx][ny][b] == -1:
                dist[nx][ny][b] = dist[x][y][b] + 1
                q.append((nx, ny, b))
        elif b == 0:
            if dist[nx][ny][1] == -1:
                dist[nx][ny][1] = dist[x][y][0] + 1
                q.append((nx, ny, 1))
d0 = dist[H - 1][W - 1][0]
d1 = dist[H - 1][W - 1][1]
cands = [d for d in (d0, d1) if d != -1]
print(min(cands) if cands else -1)
@@TESTS
--IN
5 3
000
110
000
011
000
--OUT
6
--IN
3 3
010
111
010
--OUT
-1
--IN
1 1
0
--OUT
0
--IN
2 2
01
10
--OUT
2
@@EXPL
(1) 접근·핵심 아이디어

- "벽을 한 번 부술 수 있다"는 조건은 이동의 **상태**를 바꾼다. 같은 칸이라도 "아직 부술 기회가 남은 채로 온 것"이 "이미 써 버린 채로 온 것"보다 가치가 높으므로, 정점을 `(x, y, b)`(`b` = 부순 여부 0/1)로 확장한 그래프에서 BFS를 한다.
- 모든 이동 비용이 1이라 확장 그래프에서도 BFS가 최단이다. 정점 수가 `2·H·W`로 두 배가 될 뿐 복잡도는 여전히 `O(H·W)`.
- 벽 칸으로는 `b == 0`인 상태에서만 들어갈 수 있고, 들어가면 `b = 1`이 된다. 부순 뒤에는 남은 벽을 모두 통과 불가로 취급한다.

(2) 코드 단계별

- `dist[x][y][b]`를 `-1`로 초기화하고 `dist[0][0][0] = 0`, 큐에 `(0, 0, 0)`.
- 꺼낸 상태의 4방향 이웃: 길(`'0'`)이면 같은 `b`로, 벽(`'1'`)이면 `b == 0`일 때만 `b = 1`로 전이. 각각 해당 상태가 미방문일 때만 갱신·push.
- 도착 칸의 두 상태 `dist[H-1][W-1][0]`, `[1]` 중 `-1`이 아닌 값들의 최솟값이 답. 둘 다 `-1`이면 `-1`.
- 예제 1 검산: 벽을 안 부수면 지그재그로 10번, `(1,0)` 하나를 부수면 아래로 쭉 내려가 6번(맨해튼 거리와 같아 더 줄일 수 없다).

(3) 스스로 다시 짤 때 생각 순서

- "상태 = (x, y, 부순 여부)" → "3차원 dist" → "길이면 b 유지, 벽이면 b==0일 때만 b=1로" → "도착 두 상태의 최솟값". 경계값: `1×1`(답 `0`), 벽을 두 번 부숴야만 통과 가능한 격자(예제 2, `-1`), 부수는 것이 유일한 길인 격자(예제 4).
```

**12) 안전 지대 최대 개수** · Hard

- **요구사항**: `H×W` 지역의 각 칸에 높이(정수)가 있다. 강수량이 `k`이면 높이가 `k` **이하**인 칸은 모두 물에 잠기고, 잠기지 않은 칸들이 상하좌우로 이어진 덩어리 하나가 "안전 지대"다. `k`를 `0`부터 격자의 최대 높이까지 모두 시도했을 때 안전 지대 개수의 **최댓값**과, 그 최댓값을 만드는 **가장 작은 `k`** 를 출력하라. (`k = 0`이면 아무 곳도 잠기지 않는다.)
- **입력**: 첫 줄 `H W` (`1 ≤ H, W ≤ 20`). 이어 `H`개 줄, 각 줄 `W`개 정수(공백 구분, `1 ≤ 높이 ≤ 30`).
- **출력**: `최대 안전 지대 수 그때의 최소 k`를 공백으로 한 줄에.
- **예제**: `3 3 / 3 1 3 / 1 1 1 / 3 1 3` → `4 1` · `2 2 / 1 1 / 1 1` → `1 0`
- **셀프체크**: `k`마다 `visited`를 **새로** 만들어 연결 요소를 다시 세야 한다(재사용하면 두 번째 `k`부터 0이 나온다). "높이 `> k`인 칸만 정점"이라는 조건을 탐색 시작과 이웃 확장 양쪽에 모두 걸었는가? 동률일 때 가장 작은 `k`를 남기려면 `>`로만 갱신해야 한다(`>=`면 큰 `k`로 덮인다). 모두 잠기면 안전 지대는 `0`개다.

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
idx = 0
H = int(data[idx]); idx += 1
W = int(data[idx]); idx += 1
grid = []
for i in range(H):
    row = []
    for j in range(W):
        row.append(int(data[idx])); idx += 1
    grid.append(row)
maxh = max(max(row) for row in grid)
best = -1
best_k = 0
for k in range(maxh + 1):
    visited = [[False] * W for _ in range(H)]
    cnt = 0
    for i in range(H):
        for j in range(W):
            if grid[i][j] > k and not visited[i][j]:
                cnt += 1
                visited[i][j] = True
                st = [(i, j)]
                while st:
                    x, y = st.pop()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < H and 0 <= ny < W and not visited[nx][ny] and grid[nx][ny] > k:
                            visited[nx][ny] = True
                            st.append((nx, ny))
    if cnt > best:
        best = cnt
        best_k = k
print(best, best_k)
@@TESTS
--IN
3 3
3 1 3
1 1 1
3 1 3
--OUT
4 1
--IN
2 2
1 1
1 1
--OUT
1 0
--IN
1 4
2 5 2 5
--OUT
2 2
--IN
3 4
5 5 1 5
5 1 1 5
5 5 5 5
--OUT
1 0
@@EXPL
(1) 접근·핵심 아이디어

- 강수량 `k`를 고정하면 "높이 `> k`인 칸"만 정점인 격자가 되고, 안전 지대 수는 그 격자의 연결 요소 수다. 즉 익숙한 "섬의 개수"를 `k`마다 반복해서 풀고 최댓값을 취하면 된다.
- `k`의 후보는 `0..최대 높이`면 충분하다(최대 높이 이상이면 전부 잠겨 0개). 격자가 `20×20`, 높이 `≤ 30`이라 최대 31번의 `O(H·W)` 탐색으로 넉넉하다.
- "최댓값이 같으면 가장 작은 `k`"이므로 갱신 조건을 `cnt > best`(엄격 초과)로 두고 `k`를 오름차순으로 돈다.

(2) 코드 단계별

- 격자를 정수 2차원 리스트로 읽고 `maxh`를 구한다. `best = -1`로 시작해 `k = 0`의 결과가 반드시 기록되게 한다.
- 각 `k`마다 `visited`를 새로 만들고, "높이 `> k` + 미방문"인 칸마다 `cnt += 1` 후 스택 DFS로 덩어리를 마킹(이웃도 높이 `> k`만).
- `cnt > best`일 때만 `best, best_k` 갱신. 마지막에 `best best_k` 출력.
- 예제 1 검산: `k=0` 전부 안 잠겨 1개, `k=1` 가운데 십자가 잠겨 네 귀퉁이가 각각 1칸씩 4개, `k=2`도 4개(동률이라 `k=1` 유지), `k=3` 0개 → `4 1`.

(3) 스스로 다시 짤 때 생각 순서

- "k를 0..maxh로 반복" → "k마다 visited 초기화" → "높이 > k인 칸의 연결 요소 세기" → "엄격 초과일 때만 best 갱신". 경계값: 전부 같은 높이면 `1 0`(예제 2), 잠긴 칸이 안쪽에만 있으면 덩어리가 나뉘지 않아 `1 0`(예제 4), 동률은 작은 `k`.
```
