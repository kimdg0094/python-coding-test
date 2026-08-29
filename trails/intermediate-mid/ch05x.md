## L3. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch05(Shortest Path)의 핵심 — 지연 삭제 Dijkstra와 **상태를 얹은 확장**(경로 복원·연료·열쇠), 그리고 모든 쌍을 구해 두고 **조각을 합쳐 읽는 Floyd-Warshall**(경유지·간선 수 제한·분기점) — 을 소재만 바꿔 **반복 훈련**하고, 코딩테스트 단골 유형(가장 먼 노드·격자 비용·파티(왕복)·합승 요금 류)으로 **확장**하는 연습 세트다.
- **반복 훈련 개념**:
  - Dijkstra 뼈대: `pq = [(0, s)]` → 꺼낼 때 `if d > dist[u]: continue`(지연 삭제) → 완화 `if d + w < dist[v]: dist[v] = d + w; heappush(pq, (d + w, v))`.
  - 경로 복원: 완화하는 순간 `parent[v] = u`, 끝에서 `while v != s: path.append(v); v = parent[v]` 후 뒤집기.
  - 상태 확장: 연료 잔량·열쇠 비트마스크처럼 가짓수가 작은 부가 상태를 차원으로 얹어 `dist[v][state]`, 힙에는 `(거리, 정점, 상태)`.
  - 역방향 그래프: "모든 정점 → X"의 최단은 간선을 뒤집은 그래프에서 X 출발 Dijkstra 한 번으로.
  - Floyd 뼈대: `for k: for i: for j: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`(k 최외곽). 모든 쌍을 구해 두면 경유지·분기점 질의는 `dist` 조각의 합으로 읽는다.
  - 격자 = 그래프: 칸이 정점, 4방향 이웃이 간선, 비용은 "들어가는 칸의 값".
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '최단 경로' 단계(최단경로·특정한 최단 경로·파티·플로이드 류), 프로그래머스 「코딩테스트 고득점 Kit」의 '그래프'(가장 먼 노드·합승 택시 요금 류), 『이것이 취업을 위한 코딩테스트다』의 '최단 경로' 파트(전보·미래 도시 류).
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 창고에서 각 매장까지 최단 배송 시간 | Easy | Dijkstra 기본 + INF 출력 | 반복 훈련 |
| 2 | 본사에서 가장 먼 지점 개수 | Easy | Dijkstra + 거리 최댓값 집계 | 유형 확장 (프로그래머스 Kit '그래프' 가장 먼 노드 스타일) |
| 3 | 최단 배송 경로 복원 | Medium | parent 기록 + 역추적 | 반복 훈련 |
| 4 | 격자 최소 통행료 | Medium | 격자 Dijkstra(칸 비용) | 유형 확장 (백준 '최단 경로' 단계 격자 스타일) |
| 5 | 충전소를 거치는 전기차 최단 경로 | Medium | 상태 확장(연료 잔량) | 반복 훈련 |
| 6 | 환승 K번 이내 모든 쌍 최소 요금 | Medium | Floyd 변형(min-plus 곱 K회) | 반복 훈련 |
| 7 | 본부로 갔다 돌아오는 최장 왕복 시간 | Medium | 정방향 + 역방향 Dijkstra | 유형 확장 (백준 '최단 경로' 단계 파티 스타일) |
| 8 | 필수 방문 지점 K개 최단 순회 | Hard | Floyd + 경유 순서 순열 | 반복 훈련 |
| 9 | 열쇠를 모아 잠긴 통로 열기 | Hard | 상태 확장(열쇠 비트마스크) | 반복 훈련 |
| 10 | 합배송 후 분기 최소 비용 | Hard | Floyd + 분기점 전수 | 유형 확장 (프로그래머스 Kit '그래프' 합승 택시 요금 스타일) |

**문제**

**1) 창고에서 각 매장까지 최단 배송 시간** · Easy

- **요구사항**: 도시 N곳과 일방통행 도로 M개(이동 시간 w ≥ 0)가 주어진다. 창고가 있는 도시 S에서 출발해 **각 도시 1..N까지의 최단 이동 시간**을 모두 구하라. 도달할 수 없는 도시는 `INF`.
- **입력**: 첫 줄 `N M S`(1 ≤ N ≤ 10^4, 0 ≤ M ≤ 10^5), 이후 M줄 `u v w`(u→v 일방통행, 0 ≤ w ≤ 10^4). 같은 쌍의 도로가 여러 개일 수 있다.
- **출력**: N줄. i번째 줄에 S→i 최단 시간(자기 자신은 0), 도달 불가면 `INF`.
- **예제**: `4 5 2 / 2 1 4 / 2 3 1 / 3 1 2 / 3 4 5 / 1 4 1` → `3 / 0 / 1 / 4` · `3 1 1 / 2 3 5` → `0 / INF / INF`
- **셀프체크**: 힙에 `(거리, 정점)`을 넣고, 꺼낸 거리가 `dist[u]`보다 크면 낡은 항목이므로 버린다(지연 삭제). 예제1: S=2 → 3(1) → 1(1+2=3, 직행 4보다 짧음) → 4(3+1=4, 3→4 직행 1+5=6보다 짧음). 일방통행이므로 간선을 한 방향만 넣는다(양방향으로 넣으면 예제1의 1→2가 생겨 틀림). `float('inf')`가 그대로 남은 정점을 `INF`로 바꿔 출력.

```runner
@@SOLUTION
import sys, heapq

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); s = int(data[idx + 2]); idx += 3
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        graph[u].append((v, w))       # 일방통행: 한 방향만
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:               # 지연 삭제
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    out = []
    for i in range(1, n + 1):
        out.append("INF" if dist[i] == INF else str(dist[i]))
    print("\n".join(out))

main()
@@TESTS
--IN
4 5 2
2 1 4
2 3 1
3 1 2
3 4 5
1 4 1
--OUT
3
0
1
4
--IN
3 1 1
2 3 5
--OUT
0
INF
INF
--IN
1 0 1
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 간선 가중치가 0 이상인 단일 출발 최단 거리 → Dijkstra. 힙에서 가장 작은 거리로 처음 꺼낸 정점의 값은 그 순간 확정된다(더 짧은 경로가 나중에 올 수 없음).
- 같은 정점이 여러 번 힙에 들어갈 수 있으므로, 꺼낼 때 `d > dist[u]`면 이미 더 좋은 값으로 처리된 낡은 항목이라 건너뛴다.

(2) 코드 단계별

- 인접 리스트 `graph[u] = [(v, w), ...]`를 일방통행 방향으로만 채운다.
- `dist[s] = 0`, 힙 `[(0, s)]`에서 시작해 pop → 낡은 항목 필터 → 이웃 완화·push.
- 끝나면 `dist`를 1..N 순서로 출력하되, `INF`로 남은 정점은 문자열 `INF`.

(3) 스스로 다시 짤 때 생각 순서

- "출발점 하나 + 가중치 ≥ 0" → Dijkstra 뼈대(힙·지연 삭제·완화) 세 줄을 먼저 쓴다.
- 방향성(일방통행)과 다중 간선(그대로 넣어도 완화가 알아서 처리)을 입력 단계에서 확인한다.
- 출력 규칙(도달 불가 표기, 자기 자신 0)을 마지막에 맞춘다. 복잡도 O((N+M) log N).
```

**2) 본사에서 가장 먼 지점 개수** · Easy

- **요구사항**: 양방향 도로로 연결된 지점 N개가 있다. 본사(지점 1)에서 **도달 가능한** 지점들 중, 최단 거리가 **가장 먼** 지점이 몇 개인지 구하라(본사 자신도 거리 0인 후보로 포함).
- **입력**: 첫 줄 `N M`(1 ≤ N ≤ 10^4, 0 ≤ M ≤ 10^5), 이후 M줄 `u v w`(양방향, 1 ≤ w ≤ 10^4).
- **출력**: `최대거리 개수`를 공백으로 한 줄에.
- **예제**: `6 6 / 1 2 3 / 1 3 1 / 3 2 1 / 2 4 4 / 3 5 6 / 4 6 1` → `7 2` · `3 1 / 2 3 4` → `0 1`
- **셀프체크**: 먼저 Dijkstra로 `dist`를 채운 뒤, `INF`가 아닌 값들의 최댓값과 그 값의 등장 횟수를 센다. 예제1: 1→3(1)→2(2)→4(6)→6(7), 3→5(6+1=7)이므로 거리 7이 두 개(5, 6). 도달 불가 정점을 최댓값 계산에 넣으면 `inf`가 답이 되니 반드시 걸러야 한다. 아무 도로도 없으면 본사만 남아 `0 1`(예제2).

```runner
@@SOLUTION
import sys, heapq

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); idx += 2
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        graph[u].append((v, w))
        graph[v].append((u, w))       # 양방향
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    far = 0
    cnt = 0
    for i in range(1, n + 1):
        if dist[i] == INF:            # 도달 불가는 후보에서 제외
            continue
        if dist[i] > far:
            far = dist[i]
            cnt = 1
        elif dist[i] == far:
            cnt += 1
    print(far, cnt)

main()
@@TESTS
--IN
6 6
1 2 3
1 3 1
3 2 1
2 4 4
3 5 6
4 6 1
--OUT
7 2
--IN
3 1
2 3 4
--OUT
0 1
--IN
4 3
1 2 1
1 3 1
1 4 1
--OUT
1 3
@@EXPL
(1) 접근·핵심 아이디어

- "가장 먼 지점"은 최단 거리 기준이므로 먼저 Dijkstra로 모든 정점의 최단 거리를 구하고, 그 결과를 한 번 훑어 최댓값과 개수를 센다.
- 도달 불가 정점(`INF`)은 "먼" 것이 아니라 "없는" 것이므로 집계에서 제외한다. 본사 자신은 거리 0으로 항상 도달 가능하므로 답의 개수는 최소 1이다.

(2) 코드 단계별

- 양방향 간선을 두 방향으로 넣고 정점 1에서 Dijkstra.
- `far=0, cnt=0`으로 시작해 1..N을 보며, `INF`는 건너뛰고 더 크면 `far` 갱신·`cnt=1`, 같으면 `cnt += 1`.
- `far cnt` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "최단 거리로 가장 먼 것" → Dijkstra 후 집계라는 두 단계로 나눈다.
- 집계에서 INF 제외, 본사 포함(거리 0) 규칙을 먼저 정한다.
- 경계: 도로가 없으면 `0 1`, 여러 정점이 같은 최대 거리(예제3).
```

**3) 최단 배송 경로 복원** · Medium

- **요구사항**: 일방통행 가중 그래프에서 S→T 최단 거리와 **그 경로(정점 나열)** 를 출력하라. 입력은 **S→T 최단 경로가 유일**하도록 주어진다. 도달할 수 없으면 `-1` 한 줄만.
- **입력**: 첫 줄 `N M S T`(1 ≤ N ≤ 10^4, 0 ≤ M ≤ 10^5), 이후 M줄 `u v w`(u→v, 1 ≤ w ≤ 10^4).
- **출력**: 첫 줄 최단 거리, 둘째 줄 S부터 T까지의 정점을 공백으로. S=T면 거리 0과 정점 하나.
- **예제**: `5 6 1 5 / 1 2 2 / 1 3 5 / 2 3 1 / 3 4 2 / 2 4 6 / 4 5 1` → `6 / 1 2 3 4 5` · `4 3 1 4 / 1 2 1 / 2 3 1 / 4 3 1` → `-1`
- **셀프체크**: 완화가 일어나는 순간(`nd < dist[v]`)에 `parent[v] = u`를 기록하면, 마지막에 남은 `parent`는 최단 경로 트리다. T에서 `parent`를 따라 S까지 거슬러 올라간 뒤 뒤집는다. 예제1: 1→2(2)→3(3)→4(5)→5(6). `dist[T]`가 INF면 경로 복원을 시도하지 말고 -1. S=T면 역추적 루프가 한 번도 돌지 않으므로 S 하나만 출력되는지 확인.

```runner
@@SOLUTION
import sys, heapq

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); s = int(data[idx + 2]); t = int(data[idx + 3]); idx += 4
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        graph[u].append((v, w))
    INF = float('inf')
    dist = [INF] * (n + 1)
    parent = [0] * (n + 1)
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u         # 완화 순간에 직전 정점 기록
                heapq.heappush(pq, (nd, v))
    if dist[t] == INF:
        print(-1)
        return
    path = []
    v = t
    while v != s:                     # T에서 거꾸로 따라감
        path.append(v)
        v = parent[v]
    path.append(s)
    path.reverse()
    print(dist[t])
    print(" ".join(map(str, path)))

main()
@@TESTS
--IN
5 6 1 5
1 2 2
1 3 5
2 3 1
3 4 2
2 4 6
4 5 1
--OUT
6
1 2 3 4 5
--IN
4 3 1 4
1 2 1
2 3 1
4 3 1
--OUT
-1
--IN
2 1 2 2
1 2 3
--OUT
0
2
@@EXPL
(1) 접근·핵심 아이디어

- Dijkstra가 `dist[v]`를 마지막으로 갱신했을 때의 `u`가 최단 경로에서 v의 직전 정점이다. 그래서 완화 시점에 `parent[v] = u`를 덮어쓰면, 종료 후 `parent`는 S를 뿌리로 하는 최단 경로 트리가 된다.
- T에서 `parent`를 따라 올라가면 S에 닿고, 그 순서를 뒤집으면 S→T 경로다. 최단 경로가 유일하다는 보장 덕분에 어떤 갱신 순서로 돌아도 같은 경로가 나온다.

(2) 코드 단계별

- 방향 간선을 담고 Dijkstra를 돌리되, `nd < dist[v]`로 갱신할 때마다 `parent[v] = u`.
- `dist[t]`가 INF면 -1 출력 후 종료.
- `v = t`에서 `v != s`인 동안 `path`에 담고 `v = parent[v]`, 마지막에 s를 붙이고 뒤집는다.
- 거리와 경로를 두 줄로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "경로도 출력"을 보면 `parent` 배열 한 줄 추가를 떠올린다(완화 안에서만 기록).
- 도달 불가 판정을 역추적보다 먼저 한다(INF면 parent가 0이라 무한 루프·오류).
- 경계: S=T(경로가 정점 하나), 유일성이 깨지면 정답이 여럿이 되므로 문제 조건을 확인한다.
```

**4) 격자 최소 통행료** · Medium

- **요구사항**: N×M 격자의 각 칸에 통행료(0~9)가 적혀 있다. 왼쪽 위 (0,0)에서 출발해 오른쪽 아래 (N-1,M-1)까지 **상하좌우 4방향**으로 이동한다. 지나는 모든 칸(출발 칸 포함)의 통행료 합을 최소화하라.
- **입력**: 첫 줄 `N M`(1 ≤ N, M ≤ 100), 이후 N줄에 M개의 정수(0~9).
- **출력**: 최소 통행료 합.
- **예제**: `3 4 / 2 8 3 1 / 1 1 9 1 / 6 1 1 1` → `7` · `5 3 / 1 1 1 / 9 9 1 / 1 1 1 / 1 9 9 / 1 1 1` → `11`
- **셀프체크**: 오른쪽·아래로만 간다면 DP지만, 4방향이면 위·왼쪽으로 되돌아가는 경로가 더 쌀 수 있어(예제2는 뱀처럼 왼쪽으로 돌아가야 11, 우·하만 쓰면 15) **격자를 그래프로 보고 Dijkstra**를 돌린다. 정점 = 칸, 간선 비용 = 들어가는 칸의 값, `dist[0][0] = grid[0][0]`으로 시작. 칸을 `(r, c)` 튜플이나 `r*M + c` 정수로 힙에 넣는다. 범위 검사를 빠뜨리면 인덱스 오류.

```runner
@@SOLUTION
import sys, heapq

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); idx += 2
    grid = []
    for r in range(n):
        grid.append([int(data[idx + c]) for c in range(m)])
        idx += m
    INF = float('inf')
    dist = [[INF] * m for _ in range(n)]
    dist[0][0] = grid[0][0]           # 출발 칸 비용 포함
    pq = [(grid[0][0], 0, 0)]
    dr = (1, -1, 0, 0)
    dc = (0, 0, 1, -1)
    while pq:
        d, r, c = heapq.heappop(pq)
        if d > dist[r][c]:
            continue
        if r == n - 1 and c == m - 1:
            break                     # 목표 칸이 확정되면 종료
        for k in range(4):
            nr, nc = r + dr[k], c + dc[k]
            if 0 <= nr < n and 0 <= nc < m:
                nd = d + grid[nr][nc]
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heapq.heappush(pq, (nd, nr, nc))
    print(dist[n - 1][m - 1])

main()
@@TESTS
--IN
3 4
2 8 3 1
1 1 9 1
6 1 1 1
--OUT
7
--IN
5 3
1 1 1
9 9 1
1 1 1
1 9 9
1 1 1
--OUT
11
--IN
1 1
7
--OUT
7
@@EXPL
(1) 접근·핵심 아이디어

- 4방향 이동은 "되돌아가기"를 허용하므로 행·열 순서 DP로는 풀 수 없다. 대신 각 칸을 정점, 인접 칸으로의 이동을 "들어가는 칸의 비용"을 가진 간선으로 보면 비용이 0 이상인 그래프의 단일 출발 최단 경로 → Dijkstra.
- 출발 칸의 비용도 포함해야 하므로 `dist[0][0] = grid[0][0]`에서 시작한다.

(2) 코드 단계별

- 격자를 2차원 리스트로 읽고 `dist`를 INF로 채운다.
- 힙에 `(비용, r, c)`를 넣고 pop → 지연 삭제 → 목표 칸이면 종료(그 순간 확정).
- 네 방향 이웃 중 범위 안인 칸을 `d + grid[nr][nc]`로 완화·push.
- `dist[n-1][m-1]` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "격자 + 칸마다 비용 + 4방향"을 보면 BFS(균일 비용)가 아니라 Dijkstra임을 떠올린다.
- 출발 칸 비용 포함 여부를 문제에서 확인해 초기값을 정한다.
- 경계: 1×1 격자(출발=도착), 되돌아가야 싼 뱀 모양 경로(예제2)로 DP 대비 검산.
```

**5) 충전소를 거치는 전기차 최단 경로** · Medium

- **요구사항**: 양방향 도로로 연결된 도시 N곳이 있다. 전기차는 배터리 용량이 C이고, 도로 하나를 지나면 길이 w만큼 배터리가 소모된다(남은 배터리가 w 미만이면 그 도로를 지날 수 없다). 일부 도시에는 충전소가 있어 도착하면 **즉시 C까지 완충**된다(비용 없음). 완충 상태로 도시 1에서 출발해 도시 N에 도착하는 **최소 총 이동 거리**를 구하라. 불가능하면 -1.
- **입력**: 첫 줄 `N M C K`(1 ≤ N ≤ 10^3, 0 ≤ M ≤ 10^4, 1 ≤ C ≤ 20, 1 ≤ K ≤ N), 둘째 줄 충전소 도시 번호 K개, 이후 M줄 `u v w`(양방향, 1 ≤ w ≤ C).
- **출력**: 최소 이동 거리 또는 -1.
- **예제**: `4 4 5 1 / 2 / 1 2 3 / 2 3 3 / 1 3 7 / 3 4 2` → `8` · `4 4 5 1 / 4 / 1 2 3 / 2 3 3 / 1 3 7 / 3 4 2` → `-1`
- **셀프체크**: 상태를 `(도시, 남은 배터리)`로 두고 `dist[u][f]`를 관리한다(C ≤ 20이라 상태 수가 작다). 간선 `w > f`면 이동 불가, 도착 도시가 충전소면 `f'=C`, 아니면 `f'=f-w`. 답은 `min(dist[N][*])`. 예제1: 1→3 직행(7)은 배터리 5로 불가, 1→2(충전)→3→4 = 8. 예제2: 충전소가 도착지뿐이라 3에 도달할 수 없어 -1. `visited`로 정점 재방문을 막으면 "같은 도시, 다른 배터리"를 놓치니 지연 삭제만 쓴다.

```runner
@@SOLUTION
import sys, heapq

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); cap = int(data[idx + 2]); k = int(data[idx + 3]); idx += 4
    station = [False] * (n + 1)
    for _ in range(k):
        station[int(data[idx])] = True; idx += 1
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        graph[u].append((v, w))
        graph[v].append((u, w))
    INF = float('inf')
    # dist[u][f]: 도시 u에 배터리 f 남기고 도달하는 최소 거리
    dist = [[INF] * (cap + 1) for _ in range(n + 1)]
    dist[1][cap] = 0
    pq = [(0, 1, cap)]
    while pq:
        d, u, f = heapq.heappop(pq)
        if d > dist[u][f]:
            continue
        for v, w in graph[u]:
            if w > f:                 # 배터리 부족 → 이 도로 불가
                continue
            nf = cap if station[v] else f - w    # 충전소면 완충
            nd = d + w
            if nd < dist[v][nf]:
                dist[v][nf] = nd
                heapq.heappush(pq, (nd, v, nf))
    ans = min(dist[n])
    print(-1 if ans == INF else ans)

main()
@@TESTS
--IN
4 4 5 1
2
1 2 3
2 3 3
1 3 7
3 4 2
--OUT
8
--IN
4 4 5 1
4
1 2 3
2 3 3
1 3 7
3 4 2
--OUT
-1
--IN
5 5 5 1
2
1 2 2
2 3 2
1 3 3
3 4 2
4 5 1
--OUT
7
--IN
1 0 3 1
1
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- "지금 배터리가 얼마 남았는가"에 따라 갈 수 있는 도로가 달라지므로 정점만으로는 상태가 부족하다. `(도시, 배터리)`를 노드로 보면 각 노드에서의 전이가 결정적이고 비용(거리)은 0 이상이므로 Dijkstra가 그대로 성립한다.
- 상태 전이 규칙 두 가지: 배터리가 부족한 도로는 건너뛰고, 충전소에 도착하면 배터리를 C로 되돌린다. 목표는 도시 N에 어떤 배터리로 도착하든 상관없으므로 `dist[N]`의 최솟값이 답이다.

(2) 코드 단계별

- 충전소 여부 배열과 양방향 인접 리스트를 만든다.
- `dist[1][cap] = 0`, 힙에 `(0, 1, cap)`.
- pop → 지연 삭제 → 각 간선에 대해 `w > f`면 continue, 아니면 `nf`를 계산해 `dist[v][nf]` 완화.
- `min(dist[n])`이 INF면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "이동 가능 여부가 잔량에 좌우"되면 잔량을 상태 차원으로 얹는다(가짓수 C+1이 작은지 확인).
- 전이에서 "불가 조건"과 "상태 리셋(충전)"을 정확히 적는다.
- 예제3처럼 거리만 보면 더 짧은 경로(1→3→4→5 = 6)가 배터리 때문에 막히고 우회(7)가 답이 되는 경우로 검산한다. 복잡도 O(C·M log(C·N)).
```

**6) 환승 K번 이내 모든 쌍 최소 요금** · Medium

- **요구사항**: 도시 N곳과 일방통행 노선 M개(요금 w)가 있다. **노선을 최대 K개까지만** 이용할 때(즉 간선을 K개 이하로 쓰는 경로만 허용) 도시 s에서 t로 가는 최소 요금을 여러 질의에 대해 답하라. 불가능하면 -1, s=t면 0.
- **입력**: 첫 줄 `N M K`(1 ≤ N ≤ 30, 0 ≤ M ≤ 500, 0 ≤ K ≤ 10), 이후 M줄 `u v w`(u→v, 1 ≤ w ≤ 10^4), 다음 줄 질의 수 Q(1 ≤ Q ≤ 100), 이후 Q줄 `s t`.
- **출력**: 질의마다 최소 요금 또는 -1을 한 줄씩.
- **예제**: `4 4 2 / 1 2 1 / 2 3 1 / 3 4 1 / 1 4 10 / 3 / 1 4 / 1 3 / 4 1` → `10 / 2 / -1` · `4 4 3 / 1 2 1 / 2 3 1 / 3 4 1 / 1 4 10 / 1 / 1 4` → `3`
- **셀프체크**: Floyd의 `min/plus` 연산을 행렬 곱처럼 보면, 인접 행렬 A(대각선 0, 간선 w, 없으면 INF)를 K번 "min-plus 곱"한 결과 `A^K[i][j]`가 **간선 K개 이하**로 가는 최소 비용이다(대각선 0이 "제자리"를 허용해 "정확히 K개"가 아니라 "K개 이하"가 된다). 예제1: K=2면 1→2→3→4(간선 3개)는 못 쓰고 직행 10, 예제2는 K=3이라 3. K=0이면 s=t만 0. 삼중 루프의 안쪽에서 INF를 만나면 건너뛰어 불필요한 연산을 줄인다.

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); k = int(data[idx + 2]); idx += 3
    INF = float('inf')
    adj = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        adj[i][i] = 0                 # "제자리" 허용 → 간선 K개 이하
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        if w < adj[u][v]:
            adj[u][v] = w

    def minplus(A, B):                # C[i][j] = min_t (A[i][t] + B[t][j])
        C = [[INF] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            Ai = A[i]; Ci = C[i]
            for t in range(1, n + 1):
                if Ai[t] == INF:
                    continue
                ait = Ai[t]; Bt = B[t]
                for j in range(1, n + 1):
                    if ait + Bt[j] < Ci[j]:
                        Ci[j] = ait + Bt[j]
        return C

    res = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        res[i][i] = 0                 # 간선 0개: 자기 자신만 도달
    for _ in range(k):
        res = minplus(res, adj)       # 허용 간선 수를 하나씩 늘림
    q = int(data[idx]); idx += 1
    out = []
    for _ in range(q):
        s = int(data[idx]); t = int(data[idx + 1]); idx += 2
        out.append("-1" if res[s][t] == INF else str(res[s][t]))
    print("\n".join(out))

main()
@@TESTS
--IN
4 4 2
1 2 1
2 3 1
3 4 1
1 4 10
3
1 4
1 3
4 1
--OUT
10
2
-1
--IN
4 4 3
1 2 1
2 3 1
3 4 1
1 4 10
1
1 4
--OUT
3
--IN
2 1 1
1 2 5
2
1 1
2 1
--OUT
0
-1
--IN
2 1 0
1 2 5
1
1 2
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- Floyd-Warshall의 완화식 `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`는 "곱셈을 덧셈으로, 덧셈을 min으로" 바꾼 행렬 곱(min-plus 곱)이다. 인접 행렬 A를 자기 자신과 min-plus 곱하면 "간선 2개로 가는 최소 비용", K번 곱하면 "간선 K개로 가는 최소 비용"이 된다.
- 대각선을 0으로 두면 "제자리에 머무는 간선"이 생겨, A^K가 "정확히 K개"가 아니라 **"K개 이하"** 로 가는 최소 비용을 뜻한다. 간선 수 제한이 붙은 순간 일반 Floyd(경유지 확장)로는 표현이 안 되므로 이 관점이 필요하다.

(2) 코드 단계별

- `adj`를 INF로 채우고 대각선 0, 간선은 min으로 초기화.
- `minplus(A, B)`: 삼중 루프로 `min_t A[i][t] + B[t][j]`. `A[i][t]`가 INF면 안쪽 루프를 건너뛴다.
- `res`를 단위 행렬(대각 0, 나머지 INF)로 두고 K번 `res = minplus(res, adj)`.
- 질의마다 `res[s][t]`를 읽어 INF면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "간선 K개 이하"라는 제한을 보면 Floyd의 경유지 루프 대신 "허용 간선 수를 하나씩 늘리는" 반복을 떠올린다.
- 대각선 0의 의미("이하"로 만들어 줌)를 확인하고, K=0(자기 자신만)을 경계로 검산한다.
- 복잡도 O(K·N^3)이므로 N·K가 작을 때만 쓴다.
```

**7) 본부로 갔다 돌아오는 최장 왕복 시간** · Medium

- **요구사항**: 일방통행 도로로 연결된 지점 N곳이 있다. 모든 지점의 직원이 본부 X에 갔다가 **각자 자기 지점으로 돌아온다**(갈 때·올 때 모두 최단 경로, 일방통행이라 두 경로가 다를 수 있다). 왕복 시간이 가장 긴 직원의 왕복 시간을 구하라. 모든 지점에서 왕복이 가능하도록 입력이 주어진다.
- **입력**: 첫 줄 `N M X`(1 ≤ N ≤ 10^3, 0 ≤ M ≤ 10^4), 이후 M줄 `u v w`(u→v, 1 ≤ w ≤ 10^3).
- **출력**: 최장 왕복 시간.
- **예제**: `4 6 1 / 1 2 3 / 2 1 5 / 1 3 1 / 3 4 2 / 4 1 4 / 2 4 1` → `8` · `3 4 3 / 1 3 2 / 3 1 2 / 2 3 1 / 3 2 9` → `10`
- **셀프체크**: "X → 모든 정점"은 X 출발 Dijkstra 한 번. "모든 정점 → X"를 정점마다 Dijkstra로 구하면 N번이라 느리다 — **간선을 뒤집은 그래프**에서 X 출발 Dijkstra 한 번이면 `rev_dist[i]` = i→X 최단이다. 답은 `max(dist[i] + rev_dist[i])`. 예제1: 2번 지점이 갈 때 5(2→1), 올 때 3(1→2)으로 8. 본부 자신은 0이다.

```runner
@@SOLUTION
import sys, heapq

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); x = int(data[idx + 2]); idx += 3
    graph = [[] for _ in range(n + 1)]
    rgraph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        graph[u].append((v, w))
        rgraph[v].append((u, w))      # 역방향 그래프

    def dijkstra(g, src):
        INF = float('inf')
        dist = [INF] * (n + 1)
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in g[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist

    go = dijkstra(rgraph, x)          # go[i] = i -> x 최단 (역방향에서 x 출발)
    back = dijkstra(graph, x)         # back[i] = x -> i 최단
    best = 0
    for i in range(1, n + 1):
        if go[i] + back[i] > best:
            best = go[i] + back[i]
    print(best)

main()
@@TESTS
--IN
4 6 1
1 2 3
2 1 5
1 3 1
3 4 2
4 1 4
2 4 1
--OUT
8
--IN
3 4 3
1 3 2
3 1 2
2 3 1
3 2 9
--OUT
10
--IN
1 0 1
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 왕복 시간 = (i→X 최단) + (X→i 최단). 뒤쪽은 X 출발 Dijkstra 한 번으로 전부 나온다.
- 앞쪽 "모든 i → X"는 모든 간선의 방향을 뒤집으면 "X → 모든 i"가 되므로, 역방향 그래프에서 X 출발 Dijkstra 한 번으로 전부 나온다. 정점마다 Dijkstra를 돌리는 O(N · M log N) 대신 O(M log N) 두 번.

(2) 코드 단계별

- 간선 `u→v`를 `graph[u]`에, 뒤집어 `rgraph[v]`에 담는다.
- `dijkstra(rgraph, x)`로 각 정점에서 X까지, `dijkstra(graph, x)`로 X에서 각 정점까지의 최단을 구한다.
- 두 배열의 합의 최댓값을 출력한다(왕복 보장이라 INF는 없다).

(3) 스스로 다시 짤 때 생각 순서

- "여러 출발점 → 한 도착점"을 보면 역방향 그래프 트릭을 떠올린다(일방통행일 때만 의미가 있다).
- 같은 Dijkstra 함수를 그래프 인자만 바꿔 두 번 호출하는 구조로 짠다.
- 경계: 본부 자신(0), 지점 하나뿐인 그래프(예제3).
```

**8) 필수 방문 지점 K개 최단 순회** · Hard

- **요구사항**: 양방향 가중 그래프에서 지점 1에서 출발해 지점 N에 도착하되, 지정된 **필수 지점 K개를 모두**(순서는 자유, 같은 지점·도로를 여러 번 지나도 됨) 거쳐야 한다. 최소 이동 거리를 구하라. 불가능하면 -1.
- **입력**: 첫 줄 `N M K`(2 ≤ N ≤ 50, 0 ≤ M ≤ 1000, 1 ≤ K ≤ 5), 둘째 줄 필수 지점 K개(서로 다름), 이후 M줄 `u v w`(양방향, 1 ≤ w ≤ 10^4).
- **출력**: 최소 이동 거리 또는 -1.
- **예제**: `5 6 2 / 2 4 / 1 2 1 / 2 3 1 / 3 4 1 / 4 5 1 / 1 4 3 / 2 5 6` → `4` · `4 4 2 / 3 2 / 1 2 1 / 2 3 1 / 3 4 1 / 1 3 5` → `3`
- **셀프체크**: 경로는 `1 → p1 → p2 → ... → pK → N` 조각으로 쪼개지고 각 조각은 최단 경로여도 된다(재방문 허용). Floyd로 모든 쌍 최단거리를 구한 뒤, 필수 지점의 **순서 K!가지**(`itertools.permutations`)를 전부 시도해 조각 합의 최솟값을 취한다. 예제2: 1→2→3→4 = 3이 1→3→2→4 = 5보다 짧다. 어떤 조각이라도 INF면 그 순서는 불가능, 모두 불가능하면 -1. K ≤ 5라 120가지 × K번 덧셈뿐이다.

```runner
@@SOLUTION
import sys
from itertools import permutations

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); k = int(data[idx + 2]); idx += 3
    must = [int(data[idx + i]) for i in range(k)]; idx += k
    INF = float('inf')
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        if w < dist[u][v]:
            dist[u][v] = w
            dist[v][u] = w
    for t in range(1, n + 1):         # Floyd: 경유지 t 최외곽
        dt = dist[t]
        for i in range(1, n + 1):
            dit = dist[i][t]
            if dit == INF:
                continue
            di = dist[i]
            for j in range(1, n + 1):
                if dit + dt[j] < di[j]:
                    di[j] = dit + dt[j]
    best = INF
    for order in permutations(must):  # 필수 지점 방문 순서 전수
        total = 0
        prev = 1
        for p in order:
            total += dist[prev][p]
            prev = p
        total += dist[prev][n]
        if total < best:
            best = total
    print(-1 if best == INF else best)

main()
@@TESTS
--IN
5 6 2
2 4
1 2 1
2 3 1
3 4 1
4 5 1
1 4 3
2 5 6
--OUT
4
--IN
4 4 2
3 2
1 2 1
2 3 1
3 4 1
1 3 5
--OUT
3
--IN
4 2 1
3
1 2 1
3 4 1
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- 필수 지점을 어떤 순서로 들를지만 정하면, 연속한 두 지점 사이는 최단 경로로 잇는 것이 최선이다(재방문이 허용되므로 조각별 최단이 전체 최적을 깨지 않는다). 즉 답 = `min over 순서 (dist[1][p1] + dist[p1][p2] + ... + dist[pK][N])`.
- 조각의 양 끝이 다양한 정점 쌍이므로 모든 쌍 최단거리가 필요하다 → N이 작으니 Floyd-Warshall 한 번. 순서는 K! ≤ 120가지라 전수 시도해도 된다.

(2) 코드 단계별

- `dist`를 INF/대각 0으로 초기화하고 양방향 간선을 대칭으로(중복은 min) 넣는다.
- 경유지 최외곽 삼중 루프로 모든 쌍 최단거리를 구한다.
- `permutations(must)`의 각 순서에 대해 1→…→N 조각 합을 계산해 최솟값 갱신. INF가 섞인 순서는 자연히 INF가 되어 탈락.
- 최솟값이 INF면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "반드시 지나야 하는 정점 여러 개 + 순서 자유"를 보면 Floyd + 순열 전수라는 결합을 떠올린다(L2의 경유지 하나 문제의 일반화).
- 조각 합이 정당한 이유(재방문 허용 + 부분 경로 최적성)를 한 줄로 확인한다.
- 경계: 필수 지점이 1 또는 N과 같아도 `dist[x][x] = 0`이라 자연히 처리, 일부 쌍이 단절되면 -1.
```

**9) 열쇠를 모아 잠긴 통로 열기** · Hard

- **요구사항**: 일방통행 통로로 연결된 방 N개가 있다. 일부 방에는 **열쇠**(색 1·2·3 중 하나, 방당 최대 하나)가 놓여 있어 그 방에 들어서는 순간 획득한다(여러 번 들어가도 상관없음). 일부 통로는 색 c의 **자물쇠**가 걸려 있어 같은 색 열쇠가 있어야 지날 수 있다. 방 1에서 출발해(방 1의 열쇠는 출발과 동시에 획득) 방 N에 도착하는 최소 이동 거리를 구하라. 불가능하면 -1.
- **입력**: 첫 줄 `N M`(2 ≤ N ≤ 10^3, 0 ≤ M ≤ 10^4), 둘째 줄 각 방의 열쇠 N개(0=없음, 1~3), 이후 M줄 `u v w c`(u→v, 1 ≤ w ≤ 10^4, c=0이면 자물쇠 없음, 1~3이면 그 색 자물쇠).
- **출력**: 최소 이동 거리 또는 -1.
- **예제**: `4 4 / 0 1 0 0 / 1 4 5 1 / 1 2 1 0 / 2 1 1 0 / 2 4 10 0` → `7` · `3 2 / 0 0 0 / 1 2 1 0 / 2 3 1 2` → `-1`
- **셀프체크**: 상태 = `(방, 가진 열쇠 비트마스크)`, 마스크는 0~7. 간선을 지날 때 `c != 0`이면 `mask`의 해당 비트를 검사하고, 도착 방에 열쇠가 있으면 마스크에 비트를 OR 한다. 답은 `min(dist[N][*])`. 예제1: 1→2(열쇠 1 획득)→1→4(자물쇠 1 열림) = 1+1+5 = 7이 2→4 직행 11보다 짧다 — 열쇠를 가지고 **같은 방으로 되돌아오는** 것이 새로운 상태이므로 `visited`로 막으면 안 된다. 열쇠가 없는 방(0)에서 `1 << (0-1)` 같은 실수를 하지 않도록 분기.

```runner
@@SOLUTION
import sys, heapq

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); idx += 2
    key = [0] * (n + 1)
    for i in range(1, n + 1):
        key[i] = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2]); c = int(data[idx + 3]); idx += 4
        graph[u].append((v, w, c))
    INF = float('inf')
    S = 8                             # 열쇠 3종 → 비트마스크 0..7
    dist = [[INF] * S for _ in range(n + 1)]
    start = (1 << (key[1] - 1)) if key[1] else 0
    dist[1][start] = 0
    pq = [(0, 1, start)]
    while pq:
        d, u, mask = heapq.heappop(pq)
        if d > dist[u][mask]:
            continue
        for v, w, c in graph[u]:
            if c and not (mask >> (c - 1)) & 1:   # 잠긴 통로인데 열쇠 없음
                continue
            nmask = (mask | (1 << (key[v] - 1))) if key[v] else mask
            nd = d + w
            if nd < dist[v][nmask]:
                dist[v][nmask] = nd
                heapq.heappush(pq, (nd, v, nmask))
    ans = min(dist[n])
    print(-1 if ans == INF else ans)

main()
@@TESTS
--IN
4 4
0 1 0 0
1 4 5 1
1 2 1 0
2 1 1 0
2 4 10 0
--OUT
7
--IN
3 2
0 0 0
1 2 1 0
2 3 1 2
--OUT
-1
--IN
3 3
0 2 3
1 2 2 0
2 3 2 2
1 3 1 3
--OUT
4
--IN
2 1
0 0
1 2 3 0
--OUT
3
@@EXPL
(1) 접근·핵심 아이디어

- 어떤 통로를 지날 수 있는지가 "지금까지 모은 열쇠"에 달려 있으므로, 정점에 열쇠 집합을 얹은 `(방, 마스크)`가 진짜 상태다. 열쇠는 3종이라 마스크는 8가지뿐이고, 상태 간 이동 비용은 통로 길이(≥ 0)이므로 Dijkstra가 성립한다.
- 열쇠는 잃지 않으므로 마스크는 커지기만 한다. 같은 방이라도 마스크가 다르면 다른 상태이므로, 열쇠를 얻은 뒤 왔던 방으로 돌아가는 경로(예제1)가 자연스럽게 허용된다.

(2) 코드 단계별

- 각 방의 열쇠와 `(v, w, c)` 방향 간선을 읽는다.
- 출발 상태의 마스크는 방 1의 열쇠(있으면 비트 하나). `dist[1][start] = 0`.
- pop → 지연 삭제 → 간선마다 자물쇠 검사(`c`가 0이 아니고 비트가 없으면 skip) → 도착 방 열쇠를 OR 한 `nmask`로 완화.
- `min(dist[n])`이 INF면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "특정 정점을 거쳐야만 열리는 간선"을 보면 상태를 비트마스크로 얹는 Dijkstra를 떠올린다(열쇠 종류 수가 작은지 먼저 확인).
- 전이 규칙을 "통과 조건"과 "상태 갱신" 두 줄로 분리해 적는다.
- 경계: 출발 방에 열쇠가 있는 경우, 열쇠가 도착 방에만 있어 소용없는 경우(-1), 자물쇠 없는 단순 경로(예제4). 복잡도 O(8·M log(8·N)).
```

**10) 합배송 후 분기 최소 비용** · Hard

- **요구사항**: 양방향 도로로 연결된 도시 N곳이 있다. 물류 센터 S에서 두 고객 A, B에게 보낼 상품을 트럭 한 대가 **어느 도시 P까지 함께 싣고 간 뒤**, P에서 두 배송원이 각각 A와 B로 따로 이동한다(P는 S·A·B를 포함한 어떤 도시여도 되고, 함께 가는 구간이 없어도 된다). 총 이동 비용 `S→P + P→A + P→B`의 최솟값을 구하라. 불가능하면 -1.
- **입력**: 첫 줄 `N M`(1 ≤ N ≤ 200, 0 ≤ M ≤ 5000), 둘째 줄 `S A B`, 이후 M줄 `u v w`(양방향, 1 ≤ w ≤ 10^5).
- **출력**: 최소 총 비용 또는 -1.
- **예제**: `5 6 / 1 4 5 / 1 2 3 / 2 3 2 / 3 4 4 / 3 5 4 / 2 4 8 / 2 5 8` → `13` · `3 2 / 1 2 3 / 1 2 4 / 1 3 4` → `8`
- **셀프체크**: 분기점 P를 정하면 세 조각은 각각 최단 경로여도 된다 → Floyd로 모든 쌍을 구해 두고 `min over P (dist[S][P] + dist[P][A] + dist[P][B])`. 예제1: P=3에서 5+4+4 = 13(따로 가면 P=S로 9+9 = 18). 예제2: 합배송 이득이 없어 P=S가 최선(8). P=A(또는 B)일 때 `dist[A][A] = 0`이라 자연히 "한 명은 이미 도착" 경우가 포함된다. 어떤 P든 조각 하나가 INF면 그 P는 불가.

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); idx += 2
    s = int(data[idx]); a = int(data[idx + 1]); b = int(data[idx + 2]); idx += 3
    INF = float('inf')
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        if w < dist[u][v]:
            dist[u][v] = w
            dist[v][u] = w            # 양방향
    for k in range(1, n + 1):         # Floyd: 경유지 k 최외곽
        dk = dist[k]
        for i in range(1, n + 1):
            dik = dist[i][k]
            if dik == INF:
                continue
            di = dist[i]
            for j in range(1, n + 1):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    best = INF
    for p in range(1, n + 1):         # 분기점 전수
        cost = dist[s][p] + dist[p][a] + dist[p][b]
        if cost < best:
            best = cost
    print(-1 if best == INF else best)

main()
@@TESTS
--IN
5 6
1 4 5
1 2 3
2 3 2
3 4 4
3 5 4
2 4 8
2 5 8
--OUT
13
--IN
3 2
1 2 3
1 2 4
1 3 4
--OUT
8
--IN
3 1
1 2 3
1 2 1
--OUT
-1
--IN
2 1
1 1 1
1 2 5
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 총 비용은 "함께 가는 구간 S→P"와 "따로 가는 두 구간 P→A, P→B"의 합이다. P를 고정하면 세 구간은 서로 독립이라 각각 최단으로 잡는 것이 최선이므로, 답은 모든 P에 대한 `dist[S][P] + dist[P][A] + dist[P][B]`의 최솟값이다.
- 세 조각의 끝점 조합이 다양하므로 모든 쌍 최단거리가 필요 → N ≤ 200이면 Floyd-Warshall O(N^3)이 간단하다. 양방향 그래프라 `dist[P][A] = dist[A][P]`이므로 방향은 신경 쓰지 않아도 된다.

(2) 코드 단계별

- `dist`를 INF/대각 0으로 초기화하고 양방향 간선을 대칭으로(중복은 min) 넣는다.
- 경유지 최외곽 삼중 루프로 모든 쌍 최단거리를 계산한다.
- P를 1..N 전부 돌며 세 조각 합의 최솟값을 구한다. 어느 조각이 INF면 합도 INF라 자동 탈락.
- 최솟값이 INF면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "어딘가까지 같이 가다 갈라진다"는 구조를 보면 분기점 P를 전수 조사 + 조각별 최단으로 분해한다.
- 조각이 여러 쌍을 잇는 순간 all-pairs(Floyd)를 선택한다(N이 크면 S, A, B 세 출발점 Dijkstra로 대체 가능).
- 경계: 함께 가는 구간이 없는 경우(P=S), 한 명이 이미 도착한 경우(P=A), S=A=B(0), 단절(-1).
```
