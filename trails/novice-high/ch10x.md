## L6. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch10(그래프 알고리즘)의 핵심 다섯 가지 — Dijkstra, Floyd-Warshall, Kruskal(Union-Find), Prim, 위상 정렬(Kahn) — 를 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. 새 문법은 없다. `heapq`, 2차원 리스트, `deque`, 배열 기반 Union-Find만으로 12문제를 푼다.

- **반복 훈련 개념**
- Dijkstra: 최소 힙에서 `(거리, 정점)`을 꺼내 낡은 항목은 스킵, 이웃을 완화 — `if d > dist[u]: continue` … `if d + w < dist[v]: dist[v] = d + w; heappush(pq, (dist[v], v))`
- Floyd-Warshall: 경유지 `k`가 최외곽인 삼중 루프 — `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`
- Kruskal + Union-Find: 간선을 가중치순 정렬, 대표가 다르면 채택 — `if find(u) != find(v): p[ru] = rv; total += w`
- Prim: 힙에 "누적 거리"가 아니라 **간선 가중치 그 자체**를 넣는다 — `heappush(pq, (wv, v))`
- 위상 정렬(Kahn): 진입차수 0을 큐(또는 사전순이면 힙)에 넣고 꺼내며 이웃 차수 감소, 결과 길이 `< N`이면 사이클 — `indeg[v] -= 1; if indeg[v] == 0: q.append(v)`

- **코딩테스트 출제 맵**: 이 챕터의 유형은 백준 「단계별로 풀어보기」의 '최단 경로'(특정 정점 경유·경로 복원·왕복 류), '최소 신장 트리', '위상 정렬'(선후 관계·작업 완료 시각 류) 단계, 프로그래머스 「코딩테스트 고득점 Kit」의 '그래프', 『이것이 취업을 위한 코딩테스트다』의 '최단 경로'·'그래프 이론'(Union-Find·크루스칼·위상 정렬) 파트에 그대로 등장한다. 이 레슨의 유형 확장 문제는 그 대표 유형을 소재·수치·조건을 새로 만들어 재구성한 것이다.

- **문제 구성표**

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 산장까지 최단 시간 | Easy | Dijkstra(무방향, 단일 목적지, 도달 불가 -1) | 반복 훈련 |
| 2 | 도시 간 거리 질의 | Easy | Floyd-Warshall + 다중 질의 | 반복 훈련 |
| 3 | 최소 신장 트리 간선 목록 | Easy | Kruskal + 정렬 동률 규칙 + 채택 간선 기록 | 반복 훈련 |
| 4 | 배송 경로 복원 | Medium | Dijkstra + parent 배열 역추적 | 반복 훈련 |
| 5 | 두 창고를 거치는 최단 경로 | Medium | Dijkstra 3회 + 경유 순서 두 가지 비교 | 유형 확장 (백준 '최단 경로' 단계 스타일) |
| 6 | 모임 장소 정하기 | Medium | Floyd-Warshall + 거리 합 최소 정점 | 유형 확장 (백준 '최단 경로' 단계 스타일) |
| 7 | 이미 놓인 도로 활용 | Medium | Union-Find 사전 병합 + Kruskal | 반복 훈련 |
| 8 | 섬별 전력망 | Medium | Prim 반복(최소 신장 숲) | 반복 훈련 |
| 9 | 병렬 작업 완료 시각 | Medium | Kahn + 선행 완료 시각 최댓값 | 유형 확장 (백준 '위상 정렬' 단계 · 이코테 '그래프 이론' 스타일) |
| 10 | 왕복 최단 최대 | Hard | 역방향 그래프 Dijkstra 2회 | 유형 확장 (백준 '최단 경로' 단계 스타일) |
| 11 | 공정 임계 경로 | Hard | Kahn + 최장 경로 + 동률 규칙 + 경로 복원 | 유형 확장 (이코테 '그래프 이론' 스타일 발전형) |
| 12 | 플로이드 경로 복원 | Hard | Floyd-Warshall + `nxt` 배열 + 다중 질의 | 반복 훈련 |

**문제**

**1) 산장까지 최단 시간** · Easy

- **요구사항**: `N`개 지점(1번~`N`번)이 `M`개의 **양방향** 등산로로 이어져 있고 각 등산로에 소요 시간이 있다. 출발 지점 `s`에서 산장 `t`까지 걸리는 최소 시간을 출력하라. 도달 불가면 `-1`.
- **입력**: 첫 줄 `N M s t` (`1 ≤ N ≤ 100`, `0 ≤ M ≤ 1000`). 이어 `M`개 줄 `u v w` (`1 ≤ w ≤ 1000`, 무방향).
- **출력**: 최소 시간 또는 `-1`.
- **예제**: `5 6 1 5 / 1 2 4 / 1 3 1 / 3 2 2 / 2 5 5 / 3 4 7 / 4 5 1` → `8` · `4 2 1 4 / 1 2 3 / 3 4 1` → `-1`
- **셀프체크**: 무방향이므로 간선을 `graph[u]`, `graph[v]` **양쪽**에 넣었는가? `s == t`이면 답은 `0`이다. 힙에서 꺼낸 거리가 `dist[u]`보다 크면 낡은 항목이라 스킵(지연 삭제)했는가? `INF`를 `-1`로 바꾸는 건 출력 직전에만.

```runner
@@SOLUTION
import sys, heapq
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    s = int(data[idx]); idx += 1
    t = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2]); idx += 3
        graph[u].append((v, w))
        graph[v].append((u, w))
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == t:
            break
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    print(dist[t] if dist[t] != INF else -1)
main()
@@TESTS
--IN
5 6 1 5
1 2 4
1 3 1
3 2 2
2 5 5
3 4 7
4 5 1
--OUT
8
--IN
4 2 1 4
1 2 3
3 4 1
--OUT
-1
--IN
3 3 2 2
1 2 5
2 3 5
1 3 1
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 간선 가중치가 모두 양수인 그래프에서 한 시작점으로부터의 최단 거리 → Dijkstra. 목적지가 하나뿐이어도 표준 Dijkstra를 돌리고 `dist[t]`만 읽으면 된다.
- 힙에서 `t`가 꺼내지는 순간 `dist[t]`는 확정되므로 그 자리에서 멈춰도 된다(음수 간선이 없기 때문). 멈추지 않아도 정답은 같다.
- 복잡도 `O(M log N)`.

(2) 코드 단계별

- 무방향이므로 `(v, w)`를 `graph[u]`에, `(u, w)`를 `graph[v]`에 넣는다.
- `dist[s] = 0`, 힙에 `(0, s)`. 꺼낸 `(d, u)`가 `d > dist[u]`면 낡은 항목이라 스킵.
- 이웃 완화: `d + w < dist[v]`면 갱신하고 push. `u == t`면 `break`.
- 출력 직전에 `INF`면 `-1`.
- 예제 1 검산: 1→3(1)→2(2)→5(5) = 8. 1→3→4→5는 1+7+1 = 9, 1→2→5는 4+5 = 9.

(3) 스스로 다시 짤 때 생각 순서

- "양방향 인접리스트" → "dist/힙 초기화" → "꺼내기·스킵·완화" → "dist[t] 출력(INF → -1)". 경계값: `s == t`(예제 3, `0`), `t`가 다른 덩어리(예제 2), 같은 두 지점을 잇는 등산로가 여러 개여도 완화식이 알아서 작은 것을 고른다.
```

**2) 도시 간 거리 질의** · Easy

- **요구사항**: `N`개 도시(1번~`N`번)와 `M`개의 **양방향** 도로(길이 있음)가 주어진다. 이어 `Q`개의 질의 `a b`에 대해 도시 `a`에서 `b`까지의 최단 거리를 각각 출력하라. 도달 불가면 `-1`.
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 60`, `0 ≤ M ≤ 500`). 이어 `M`개 줄 `u v w` (`1 ≤ w ≤ 1000`). 다음 줄 `Q` (`1 ≤ Q ≤ 100`), 이어 `Q`개 줄 `a b`.
- **출력**: 질의마다 한 줄.
- **예제**: `4 4 / 1 2 3 / 2 3 4 / 1 3 10 / 3 4 1 / 3 / 1 3 / 1 4 / 2 1` → `7 / 8 / 3` · `3 1 / 1 2 5 / 2 / 1 3 / 3 3` → `-1 / 0`
- **셀프체크**: 질의가 많고 `N`이 작으니 Floyd-Warshall로 전 쌍을 한 번에 구하고 질의는 `O(1)` 조회가 낫다. 같은 도시 쌍에 도로가 여러 개면 초기화 때 `min`을 취했는가? 삼중 루프에서 `k`가 **가장 바깥**인가? `a == b`는 `0`.

```runner
@@SOLUTION
import sys
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    INF = float('inf')
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2]); idx += 3
        if w < dist[u][v]:
            dist[u][v] = w
            dist[v][u] = w
    for k in range(1, n + 1):
        dk = dist[k]
        for i in range(1, n + 1):
            dik = dist[i][k]
            if dik == INF:
                continue
            di = dist[i]
            for j in range(1, n + 1):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd
    q = int(data[idx]); idx += 1
    out = []
    for _ in range(q):
        a = int(data[idx]); b = int(data[idx+1]); idx += 2
        out.append('-1' if dist[a][b] == INF else str(dist[a][b]))
    print('\n'.join(out))
main()
@@TESTS
--IN
4 4
1 2 3
2 3 4
1 3 10
3 4 1
3
1 3
1 4
2 1
--OUT
7
8
3
--IN
3 1
1 2 5
2
1 3
3 3
--OUT
-1
0
--IN
2 2
1 2 9
1 2 2
1
1 2
--OUT
2
@@EXPL
(1) 접근·핵심 아이디어

- "여러 쌍에 대한 최단 거리"를 물으니 모든 쌍을 미리 구해 두는 Floyd-Warshall이 자연스럽다. `N ≤ 60`이면 `O(N^3) = 216,000`번의 갱신으로 충분히 빠르고, 질의는 표를 읽기만 하면 된다.
- 경유지 `k`를 하나씩 허용해 가며 `i→k→j`가 더 짧으면 `dist[i][j]`를 갱신한다. `k`가 최외곽이어야 "1..k까지만 경유 허용"이라는 DP 의미가 유지된다.

(2) 코드 단계별

- `dist`를 `INF`, 대각선은 `0`으로 초기화. 무방향 도로는 `dist[u][v]`와 `dist[v][u]` 양쪽에, 중복 도로는 `min`으로.
- 삼중 루프 `k → i → j`. `dist[i][k]`가 `INF`면 그 `i`는 건너뛰어 불필요한 덧셈을 줄인다.
- 질의 `a b`마다 `dist[a][b]`가 `INF`면 `-1`, 아니면 그 값을 모아 한 번에 출력.
- 예제 1 검산: 1→3은 직통 10보다 1→2→3 = 7이 짧고, 1→4 = 7 + 1 = 8.

(3) 스스로 다시 짤 때 생각 순서

- "INF 행렬 + 대각선 0" → "간선 입력(양방향, min)" → "k 최외곽 삼중 루프" → "질의 조회". 경계값: `a == b`(0), 다른 덩어리(예제 2), 같은 쌍의 도로 2개(예제 3). 계산 중에는 `INF`를 유지하고 출력 때만 `-1`로 바꿔야 잘못된 경유가 생기지 않는다.
```

**3) 최소 신장 트리 간선 목록** · Easy

- **요구사항**: `N`개 마을과 `M`개의 후보 도로(양방향, 비용)가 있다. 모든 마을을 잇는 최소 비용 도로 집합(MST)을 Kruskal로 구해, 첫 줄에 총비용을, 이어서 **채택한 순서대로** 각 도로를 `u v w`(`u < v`)로 출력하라. 간선은 `(비용, 작은 번호, 큰 번호)` 오름차순으로 검사한다. 모두 연결 불가면 `-1`만 출력.
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 100`, `0 ≤ M ≤ 1000`). 이어 `M`개 줄 `u v w` (`1 ≤ w ≤ 1000`).
- **출력**: 총비용 한 줄 + 채택 간선 `N-1`줄, 또는 `-1`.
- **예제**: `4 5 / 1 2 3 / 3 1 3 / 2 3 1 / 3 4 2 / 4 1 6` → `6 / 2 3 1 / 3 4 2 / 1 2 3` · `3 1 / 1 2 4` → `-1`
- **셀프체크**: 정렬 전에 `u > v`면 바꿔서 `(w, u, v)`로 저장해야 동률 간선의 검사 순서가 문제 규칙과 같아진다. `find`에 경로 압축을 넣었는가? `N = 1`이면 채택 간선 0개로 `0`만 출력된다.

```runner
@@SOLUTION
import sys
def find(p, x):
    while p[x] != x:
        p[x] = p[p[x]]
        x = p[x]
    return x
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    edges = []
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2]); idx += 3
        if u > v:
            u, v = v, u
        edges.append((w, u, v))
    edges.sort()
    p = list(range(n + 1))
    total = 0
    chosen = []
    for w, u, v in edges:
        ru, rv = find(p, u), find(p, v)
        if ru != rv:
            p[ru] = rv
            total += w
            chosen.append((u, v, w))
            if len(chosen) == n - 1:
                break
    if len(chosen) != n - 1:
        print(-1)
    else:
        print(total)
        for u, v, w in chosen:
            print(u, v, w)
main()
@@TESTS
--IN
4 5
1 2 3
3 1 3
2 3 1
3 4 2
4 1 6
--OUT
6
2 3 1
3 4 2
1 2 3
--IN
3 1
1 2 4
--OUT
-1
--IN
1 0
--OUT
0
--IN
3 3
2 3 5
1 3 5
1 2 5
--OUT
10
1 2 5
1 3 5
@@EXPL
(1) 접근·핵심 아이디어

- Kruskal은 간선을 가벼운 순으로 보며 "사이클을 만들지 않는" 간선만 채택하는 그리디다. 사이클 판정은 Union-Find로: 두 끝점의 대표가 같으면 이미 이어져 있으니 버린다.
- 비용이 같은 간선이 여러 개면 어떤 걸 먼저 보느냐에 따라 채택 목록이 달라진다. 그래서 문제는 `(비용, 작은 번호, 큰 번호)` 순서를 못 박았고, 튜플을 그 순서로 만들어 `sort()`하면 파이썬 튜플 비교가 규칙을 그대로 구현한다.
- 복잡도: 정렬 `O(M log M)`이 지배적.

(2) 코드 단계별

- 간선 입력 시 `u > v`면 교환해 항상 `u < v`로 두고 `(w, u, v)`를 모아 정렬.
- `p = list(range(n + 1))`로 각자 자기 대표. `find`는 경로 압축.
- 정렬 순서대로 `find(u) != find(v)`면 합치고 `total`에 더하며 `chosen`에 `(u, v, w)` 기록. `N-1`개가 되면 종료.
- `chosen`이 `N-1`개가 아니면 `-1`, 아니면 총비용과 목록 출력.
- 예제 1 검산: 정렬 순서 (1: 2-3), (2: 3-4), (3: 1-2), (3: 1-3), (6: 1-4). 앞 세 개를 채택하면 `N-1 = 3`개 완성, 1-3은 보지도 않는다.

(3) 스스로 다시 짤 때 생각 순서

- "간선 정규화(u<v) + 정렬" → "Union-Find" → "대표 다르면 채택·기록" → "N-1개 확인 후 출력". 경계값: `N = 1`(`0`), 고립 마을(`-1`), 동률 간선(예제 4는 1-2, 1-3이 먼저 채택되고 2-3은 사이클).
```

**4) 배송 경로 복원** · Medium

- **요구사항**: `N`개 물류 거점(1번~`N`번)과 `M`개의 **일방통행** 도로(소요 시간)가 있다. 출발 `s`에서 도착 `t`까지의 최단 시간과 그 경로(거점 나열)를 출력하라. **최단 경로는 유일하다고 보장**된다. 도달 불가면 `-1`만 출력.
- **입력**: 첫 줄 `N M s t` (`1 ≤ N ≤ 100`, `0 ≤ M ≤ 1000`). 이어 `M`개 줄 `u v w` (u→v, `1 ≤ w ≤ 1000`).
- **출력**: 첫 줄 최단 시간, 둘째 줄 경로(`s`부터 `t`까지 공백 구분). 불가면 `-1`.
- **예제**: `5 6 1 5 / 1 2 2 / 1 3 5 / 2 3 1 / 3 5 3 / 2 4 7 / 4 5 1` → `6 / 1 2 3 5` · `3 1 1 3 / 1 2 4` → `-1`
- **셀프체크**: `dist[v]`를 **더 짧게 갱신하는 순간**에만 `parent[v] = u`를 기록해야 한다(힙에서 꺼낼 때 기록하면 틀린다). 시작점의 `parent`를 `0`으로 두면 역추적 종료 조건이 된다. `s == t`면 시간 `0`, 경로 `s` 하나.

```runner
@@SOLUTION
import sys, heapq
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    s = int(data[idx]); idx += 1
    t = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2]); idx += 3
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
                parent[v] = u
                heapq.heappush(pq, (nd, v))
    if dist[t] == INF:
        print(-1)
        return
    path = []
    cur = t
    while cur != 0:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    print(dist[t])
    print(' '.join(map(str, path)))
main()
@@TESTS
--IN
5 6 1 5
1 2 2
1 3 5
2 3 1
3 5 3
2 4 7
4 5 1
--OUT
6
1 2 3 5
--IN
3 1 1 3
1 2 4
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

- Dijkstra에서 `dist[v]`가 갱신될 때 "누구를 거쳐 왔는가"(`parent[v] = u`)를 함께 적어 두면, 알고리즘이 끝난 뒤 `t`에서 `parent`를 거꾸로 따라가 최단 경로를 복원할 수 있다.
- `parent`는 항상 "현재까지 가장 짧은 경로의 직전 정점"이다. 갱신이 여러 번 일어나도 마지막(가장 짧은) 갱신이 남으므로 최종 `parent`는 최단 경로의 것이다. 최단 경로가 유일하다는 보장 덕분에 답이 하나로 정해진다.
- 복잡도 `O(M log N)` + 역추적 `O(N)`.

(2) 코드 단계별

- 일방통행이므로 `graph[u]`에만 넣는다.
- `parent`를 `0`으로 초기화(정점 번호는 1부터라 `0`은 "없음"). `dist[s] = 0`, 힙 시작.
- 완화 성공(`nd < dist[v]`)할 때만 `parent[v] = u`.
- `dist[t]`가 `INF`면 `-1`. 아니면 `t`부터 `parent`를 따라 `0`이 나올 때까지 모아 뒤집는다.
- 예제 1 검산: 1→2→3→5 = 2+1+3 = 6, 1→3→5 = 8, 1→2→4→5 = 10. 3의 `parent`는 처음 1(5)로 적혔다가 2를 거친 3이 더 짧아 2로 덮인다.

(3) 스스로 다시 짤 때 생각 순서

- "방향 인접리스트" → "Dijkstra + 완화 시 parent 기록" → "INF면 -1" → "역추적·reverse". 경계값: `s == t`(예제 3), 도달 불가, 그리고 `parent`를 "꺼낼 때"가 아니라 "갱신할 때" 적는 것이 핵심 함정.
```

**5) 두 창고를 거치는 최단 경로** · Medium

- **요구사항**: `N`개 지점과 `M`개의 **양방향** 도로가 있다. 출발 `s`에서 도착 `t`로 가되, 반드시 창고 `a`와 창고 `b`를 **둘 다** 들러야 한다(순서는 자유, 같은 지점·도로를 여러 번 지나도 됨). 가능한 최소 총거리를 출력하라. 불가능하면 `-1`.
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 100`, `0 ≤ M ≤ 1000`). 이어 `M`개 줄 `u v w` (`1 ≤ w ≤ 1000`). 마지막 줄 `s a b t`.
- **출력**: 최소 총거리 또는 `-1`.
- **예제**: `5 6 / 1 2 1 / 2 3 2 / 3 4 1 / 4 5 2 / 1 4 8 / 2 5 6 / 1 3 4 5` → `6` · `4 2 / 1 2 1 / 3 4 1 / 1 2 3 4` → `-1`
- **셀프체크**: 경로는 `s→a→b→t` 또는 `s→b→a→t` 둘 중 하나다. `s`, `a`, `b`에서 각각 Dijkstra를 돌리면(총 3번) 필요한 거리 6개가 모두 나온다(무방향이라 `dist_a[b] == dist_b[a]`). 어느 한 구간이라도 `INF`면 그 순서는 불가능 — 두 순서 모두 `INF`일 때만 `-1`. `a == b`나 `s == a` 같은 겹침도 그대로 동작하는가?

```runner
@@SOLUTION
import sys, heapq
def dijkstra(n, graph, start):
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2]); idx += 3
        graph[u].append((v, w))
        graph[v].append((u, w))
    s = int(data[idx]); a = int(data[idx+1]); b = int(data[idx+2]); t = int(data[idx+3]); idx += 4
    ds = dijkstra(n, graph, s)
    da = dijkstra(n, graph, a)
    db = dijkstra(n, graph, b)
    r1 = ds[a] + da[b] + db[t]
    r2 = ds[b] + db[a] + da[t]
    ans = min(r1, r2)
    print(ans if ans != float('inf') else -1)
main()
@@TESTS
--IN
5 6
1 2 1
2 3 2
3 4 1
4 5 2
1 4 8
2 5 6
1 3 4 5
--OUT
6
--IN
4 2
1 2 1
3 4 1
1 2 3 4
--OUT
-1
--IN
3 2
1 2 3
2 3 4
1 3 1 2
--OUT
11
@@EXPL
(1) 접근·핵심 아이디어

- "반드시 두 정점을 거친다"는 조건은 경로를 세 구간으로 쪼개면 사라진다: `s→a`, `a→b`, `b→t`(또는 `b`를 먼저). 각 구간은 평범한 최단 거리이고, 정점을 다시 지나도 되므로 구간 합이 곧 답이다.
- 필요한 거리는 `s`, `a`, `b`를 시작점으로 하는 Dijkstra 세 번이면 전부 얻는다. 무방향이라 `da[b] == db[a]`이지만 코드를 대칭으로 두면 읽기 쉽다.
- `INF + 유한값 = INF`이므로 어느 구간이 끊기면 그 순서의 합은 자동으로 `INF`가 된다. 복잡도 `O(3 · M log N)`.

(2) 코드 단계별

- Dijkstra를 함수로 분리해 `ds`, `da`, `db` 세 배열을 만든다.
- `r1 = ds[a] + da[b] + db[t]`(a 먼저), `r2 = ds[b] + db[a] + da[t]`(b 먼저). 둘의 최솟값이 `INF`면 `-1`.
- 예제 1 검산: `s=1, a=3, b=4, t=5`. `1→3 = 3`(1-2-3), `3→4 = 1`, `4→5 = 2` → 6. 반대 순서는 `1→4 = 4`, `4→3 = 1`, `3→5 = 3` → 8.
- 예제 3 검산: `a = 3, b = 1 = s`. `s→b`가 0이라 `r2 = 0 + 7 + 4 = 11`이 `r1 = 7 + 7 + 3 = 17`보다 작다.

(3) 스스로 다시 짤 때 생각 순서

- "경유 조건 → 구간 분할" → "필요한 시작점마다 Dijkstra" → "두 순서 합의 최솟값" → "INF면 -1". 경계값: 창고가 다른 덩어리(예제 2), 창고가 출발점과 같은 경우(예제 3), 두 창고가 같은 정점이면 `da[b] = 0`이라 자연스럽게 처리된다.
```

**6) 모임 장소 정하기** · Medium

- **요구사항**: `N`개 동네(1번~`N`번)가 `M`개의 **양방향** 길로 이어져 있다. `K`명의 친구가 각자 어떤 동네에 산다. 모두가 모일 동네 `x`를 고르되, "각 친구의 집에서 `x`까지 최단 거리의 **합**"이 최소가 되게 하라. 합이 같으면 번호가 작은 동네. 모든 친구가 도달할 수 있는 동네가 없으면 `-1`.
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 60`, `0 ≤ M ≤ 500`). 이어 `M`개 줄 `u v w` (`1 ≤ w ≤ 1000`). 다음 줄 `K` (`1 ≤ K ≤ 20`), 이어 한 줄에 친구들의 동네 번호 `K`개(중복 가능).
- **출력**: `동네 번호 거리 합`을 공백으로 한 줄에, 또는 `-1`.
- **예제**: `5 5 / 1 2 2 / 2 3 2 / 3 4 2 / 4 5 2 / 1 5 3 / 3 / 1 3 5` → `1 7` · `4 1 / 1 2 1 / 2 / 1 3` → `-1`
- **셀프체크**: 모든 친구 집에서 모든 동네까지 거리가 필요하니 Floyd-Warshall이 편하다. 어떤 친구라도 `x`에 못 가면 그 `x`는 후보에서 빠진다(`INF`가 섞인 합은 `INF`). 동률에서 작은 번호를 남기려면 `x`를 오름차순으로 돌며 **엄격히 작을 때만** 갱신한다. 모임 장소가 친구 집이어도 된다(그 친구의 거리는 `0`).

```runner
@@SOLUTION
import sys
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    INF = float('inf')
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2]); idx += 3
        if w < dist[u][v]:
            dist[u][v] = w
            dist[v][u] = w
    for k in range(1, n + 1):
        dk = dist[k]
        for i in range(1, n + 1):
            dik = dist[i][k]
            if dik == INF:
                continue
            di = dist[i]
            for j in range(1, n + 1):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd
    kcnt = int(data[idx]); idx += 1
    people = [int(data[idx + i]) for i in range(kcnt)]
    idx += kcnt
    best = INF
    best_x = -1
    for x in range(1, n + 1):
        total = 0
        for p in people:
            total += dist[p][x]
        if total < best:
            best = total
            best_x = x
    if best_x == -1:
        print(-1)
    else:
        print(best_x, best)
main()
@@TESTS
--IN
5 5
1 2 2
2 3 2
3 4 2
4 5 2
1 5 3
3
1 3 5
--OUT
1 7
--IN
4 1
1 2 1
2
1 3
--OUT
-1
--IN
2 1
1 2 5
1
2
--OUT
2 0
@@EXPL
(1) 접근·핵심 아이디어

- 후보 동네 `x`마다 "친구별 최단 거리의 합"을 알아야 하므로 (친구 집) × (모든 동네) 거리표가 필요하다. `N ≤ 60`이면 Floyd-Warshall 한 번으로 전 쌍 최단 거리를 얻는 것이 가장 간단하다(친구마다 Dijkstra를 돌려도 되지만 코드가 길어진다).
- 어떤 친구가 `x`에 도달 불가면 합이 `INF`가 되어 자동으로 후보에서 탈락한다. 모든 `x`가 탈락하면 `best_x`가 `-1`로 남는다.
- 동률 처리는 "오름차순 순회 + 엄격 미만 갱신"이 정석. 복잡도 `O(N^3 + N·K)`.

(2) 코드 단계별

- `dist` 초기화(대각선 0, 무방향 양쪽, 중복 도로 `min`) 후 `k → i → j` 삼중 루프.
- 친구 수 `K`와 집 목록을 읽는다.
- `x = 1..N`마다 `sum(dist[p][x])`를 구해 `best`보다 **작을 때만** 갱신.
- 예제 1 검산: 합은 `x=1`: 0+4+3 = 7, `x=2`: 2+2+5 = 9, `x=3`: 4+0+4 = 8, `x=4`: 5+2+2 = 9, `x=5`: 3+4+0 = 7. 7이 두 번(1, 5)이지만 작은 번호 1.

(3) 스스로 다시 짤 때 생각 순서

- "Floyd로 전 쌍 거리" → "후보마다 친구 거리 합" → "엄격 미만 갱신으로 최소·동률 처리" → "없으면 -1". 경계값: 친구가 한 명이면 그 집이 답(합 0, 예제 3), 친구들이 서로 다른 덩어리에 살면 `-1`(예제 2), 같은 집에 두 명이 살면 그 거리가 두 번 더해진다.
```

**7) 이미 놓인 도로 활용** · Medium

- **요구사항**: `N`개 마을 사이에 `M`개의 후보 도로(양방향, 건설 비용)가 있고, 그중과 별개로 **이미 놓여 있어 비용 0으로 쓸 수 있는** 도로 `K`개가 있다. 모든 마을이 연결되도록 후보 도로를 추가로 건설할 때 최소 추가 비용을 출력하라. 불가능하면 `-1`.
- **입력**: 첫 줄 `N M K` (`1 ≤ N ≤ 100`, `0 ≤ M ≤ 1000`, `0 ≤ K ≤ 100`). 이어 `M`개 줄 `u v w` (`1 ≤ w ≤ 1000`), 이어 `K`개 줄 `a b`(이미 놓인 도로).
- **출력**: 최소 추가 비용 또는 `-1`.
- **예제**: `5 6 1 / 1 2 5 / 2 3 4 / 3 4 3 / 4 5 2 / 1 5 6 / 2 4 7 / 1 3` → `9` · `4 2 2 / 1 2 3 / 3 4 3 / 1 3 / 2 4` → `3`
- **셀프체크**: 이미 놓인 도로는 Kruskal을 시작하기 **전에** Union-Find로 먼저 합쳐 두면 된다(비용 0이라 정렬 맨 앞에 오는 것과 같다). 남은 덩어리 수를 세어 두고 합칠 때마다 1씩 줄이면, 마지막에 `1`인지로 연결 여부를 판정할 수 있다. 이미 놓인 도로만으로 전부 연결돼 있으면 답은 `0`.

```runner
@@SOLUTION
import sys
def find(p, x):
    while p[x] != x:
        p[x] = p[p[x]]
        x = p[x]
    return x
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    edges = []
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2]); idx += 3
        edges.append((w, u, v))
    p = list(range(n + 1))
    comps = n
    for _ in range(k):
        a = int(data[idx]); b = int(data[idx+1]); idx += 2
        ra, rb = find(p, a), find(p, b)
        if ra != rb:
            p[ra] = rb
            comps -= 1
    edges.sort()
    total = 0
    for w, u, v in edges:
        if comps == 1:
            break
        ru, rv = find(p, u), find(p, v)
        if ru != rv:
            p[ru] = rv
            total += w
            comps -= 1
    print(total if comps == 1 else -1)
main()
@@TESTS
--IN
5 6 1
1 2 5
2 3 4
3 4 3
4 5 2
1 5 6
2 4 7
1 3
--OUT
9
--IN
4 2 2
1 2 3
3 4 3
1 3
2 4
--OUT
3
--IN
3 1 0
1 2 1
--OUT
-1
--IN
3 2 2
1 2 9
2 3 9
1 2
2 3
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- "이미 연결된 도로"는 비용 0짜리 간선과 같다. 비용 0은 정렬하면 맨 앞에 오므로 Kruskal이 반드시 먼저 채택한다 — 그렇다면 굳이 정렬에 섞지 않고 **Union-Find에 미리 합쳐 두는** 것이 같은 효과이면서 더 간단하다.
- 그 뒤는 표준 Kruskal. 채택 간선 수 대신 "남은 덩어리 수 `comps`"를 관리하면, 미리 합친 도로가 몇 개든 상관없이 `comps == 1`로 연결 여부를 판정할 수 있다.
- 복잡도 `O(M log M)`.

(2) 코드 단계별

- 후보 도로를 `(w, u, v)`로 모으고, `p`와 `comps = n`을 준비.
- 이미 놓인 도로 `a b`마다 대표가 다르면 합치고 `comps -= 1`.
- 후보 도로를 정렬해 순서대로 보며 대표가 다르면 합치고 `total += w`, `comps -= 1`. `comps == 1`이면 조기 종료.
- 끝나고 `comps == 1`이면 `total`, 아니면 `-1`.
- 예제 1 검산: 1-3이 미리 연결. 정렬 순서 4-5(2), 3-4(3), 2-3(4) 채택 → 9. 다음 1-2(5)는 1~3~4~2가 이미 이어져 사이클이라 버린다.

(3) 스스로 다시 짤 때 생각 순서

- "Union-Find 준비 + comps = N" → "기존 도로 먼저 union" → "후보 정렬 후 Kruskal" → "comps == 1이면 total". 경계값: 기존 도로만으로 이미 연결(예제 4, `0`), 후보가 부족해 연결 불가(예제 3), 기존 도로가 같은 덩어리 안에서 중복돼도 `comps`는 줄지 않아야 한다(대표 비교로 방어).
```

**8) 섬별 전력망** · Medium

- **요구사항**: `N`개 발전소(1번~`N`번)와 `M`개의 후보 케이블(양방향, 길이)이 있다. 발전소들은 여러 **섬**에 흩어져 있어 후보 케이블만으로는 서로 연결되지 않는 그룹이 있을 수 있다. 각 그룹(연결 요소) 안에서 발전소를 모두 잇는 최소 케이블 길이를 Prim으로 구해, 그룹 수와 모든 그룹의 최소 길이 합을 출력하라.
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 100`, `0 ≤ M ≤ 1000`). 이어 `M`개 줄 `u v w` (`1 ≤ w ≤ 1000`).
- **출력**: `그룹 수 총 길이`를 공백으로 한 줄에.
- **예제**: `6 5 / 1 2 3 / 2 3 1 / 1 3 2 / 4 5 4 / 5 6 4` → `2 11` · `4 0` → `4 0`
- **셀프체크**: 연결 그래프가 아니면 시작점 하나에서 Prim을 돌려도 일부만 편입된다. `1..N`을 훑다 **미방문 발전소를 만날 때마다** Prim을 새로 시작하면 그룹마다 MST가 하나씩 만들어진다(연결 요소 세기와 같은 구조). 힙에 넣는 값은 누적 거리가 아닌 **케이블 길이 자체**인가? 시작 정점의 `(0, s)`는 비용에 0을 더할 뿐이다.

```runner
@@SOLUTION
import sys, heapq
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2]); idx += 3
        graph[u].append((v, w))
        graph[v].append((u, w))
    visited = [False] * (n + 1)
    trees = 0
    total = 0
    for s in range(1, n + 1):
        if visited[s]:
            continue
        trees += 1
        pq = [(0, s)]
        while pq:
            w, u = heapq.heappop(pq)
            if visited[u]:
                continue
            visited[u] = True
            total += w
            for v, wv in graph[u]:
                if not visited[v]:
                    heapq.heappush(pq, (wv, v))
    print(trees, total)
main()
@@TESTS
--IN
6 5
1 2 3
2 3 1
1 3 2
4 5 4
5 6 4
--OUT
2 11
--IN
4 0
--OUT
4 0
--IN
3 3
1 2 1
2 3 1
1 3 1
--OUT
1 2
@@EXPL
(1) 접근·핵심 아이디어

- Prim은 시작 정점에서 트리를 키워 가므로 시작점이 속한 연결 요소만 다룬다. 그래프가 여러 조각이면 "미방문 정점마다 Prim을 새로 시작"해 조각마다 MST를 만든다 — 결과는 최소 신장 **숲**이다.
- Prim 시작 횟수가 곧 그룹(연결 요소) 수다. Ch9의 연결 요소 세기와 뼈대가 같고, 탐색 도구만 BFS에서 힙 기반 Prim으로 바뀐 셈이다.
- 복잡도 `O(M log N)`(전체 간선을 통틀어 각 간선은 힙에 최대 두 번).

(2) 코드 단계별

- 무방향 인접리스트. `visited`는 모든 그룹이 공유한다(한 번 편입된 발전소는 다시 시작점이 되지 않는다).
- `s = 1..N` 중 미방문이면 `trees += 1`, 힙에 `(0, s)`로 Prim 시작.
- 꺼낸 정점이 방문됐으면 스킵(지연 삭제), 아니면 편입해 `total += w`, 미방문 이웃 간선 `(wv, v)`를 push.
- 예제 1 검산: {1,2,3}은 2-3(1)+1-3(2) = 3, {4,5,6}은 4+4 = 8 → 그룹 2, 합 11.

(3) 스스로 다시 짤 때 생각 순서

- "공유 visited" → "미방문 정점마다 Prim 시작(그룹 +1)" → "편입 시 비용 누적" → "그룹 수와 합 출력". 경계값: 케이블이 없으면 그룹 `N`개에 합 0(예제 2), 동률 케이블이 있어도 합은 유일(예제 3).
```

**9) 병렬 작업 완료 시각** · Medium

- **요구사항**: `N`개 작업(1번~`N`번)에 각각 소요 시간이 있고, "`u`가 끝나야 `v`를 시작할 수 있다"는 선후 관계 `M`개가 있다. 선행 작업이 없는 작업은 시각 0에 시작하고, 서로 독립인 작업은 **동시에** 진행할 수 있다. 각 작업이 가장 빨리 끝나는 시각을 1번부터 순서대로 출력하라. 선후 관계에 사이클이 있으면 `-1`.
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 200`, `0 ≤ M ≤ 1000`). 둘째 줄 소요 시간 `N`개 (`1 ≤ 시간 ≤ 100`). 이어 `M`개 줄 `u v` (u→v).
- **출력**: 완료 시각 `N`개를 공백 구분 한 줄, 또는 `-1`.
- **예제**: `5 4 / 3 2 4 1 5 / 1 3 / 2 3 / 3 4 / 3 5` → `3 2 7 8 12` · `3 3 / 1 1 1 / 1 2 / 2 3 / 3 1` → `-1`
- **셀프체크**: 작업 `v`의 시작 시각 = **모든 선행 작업 완료 시각의 최댓값**(합이 아님!). 위상 정렬 순서대로 처리하면 `v`를 꺼낼 때 선행 작업은 이미 전부 확정돼 있다. 진입차수가 0이 되는 순간에 `dur[v]`를 더하는가? 처리한 작업 수가 `N`보다 작으면 사이클.

```runner
@@SOLUTION
import sys
from collections import deque
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    dur = [0] * (n + 1)
    for i in range(1, n + 1):
        dur[i] = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); idx += 2
        graph[u].append(v)
        indeg[v] += 1
    finish = [0] * (n + 1)
    q = deque()
    for v in range(1, n + 1):
        if indeg[v] == 0:
            finish[v] = dur[v]
            q.append(v)
    done = 0
    while q:
        u = q.popleft()
        done += 1
        for v in graph[u]:
            if finish[u] > finish[v]:
                finish[v] = finish[u]
            indeg[v] -= 1
            if indeg[v] == 0:
                finish[v] += dur[v]
                q.append(v)
    if done != n:
        print(-1)
    else:
        print(' '.join(str(finish[i]) for i in range(1, n + 1)))
main()
@@TESTS
--IN
5 4
3 2 4 1 5
1 3
2 3
3 4
3 5
--OUT
3 2 7 8 12
--IN
3 3
1 1 1
1 2
2 3
3 1
--OUT
-1
--IN
2 0
4 6
--OUT
4 6
@@EXPL
(1) 접근·핵심 아이디어

- 독립 작업은 동시에 진행되므로 `v`는 "선행 작업 중 가장 늦게 끝나는 것"이 끝나자마자 시작한다. 즉 `finish[v] = max(finish[u] for u→v) + dur[v]` — DAG 위의 최장 경로 DP다.
- 이 점화식은 선행 작업의 `finish`가 먼저 확정돼야 하므로 위상 정렬 순서로 계산한다. Kahn 알고리즘이 그 순서를 만들어 주고, 결과 길이로 사이클도 함께 판정한다.
- 복잡도 `O(N + M)`.

(2) 코드 단계별

- 소요 시간 `dur`, 인접리스트, 진입차수를 만든다.
- 진입차수 0인 작업은 `finish = dur`로 확정하고 큐에 넣는다.
- 큐에서 `u`를 꺼내 이웃 `v`의 `finish[v]`를 `max(finish[v], finish[u])`로 올린다(아직은 "시작 시각"). `indeg[v]`가 0이 되는 순간 `dur[v]`를 더해 완료 시각으로 확정하고 큐에 넣는다.
- 처리 수가 `N`이 아니면 `-1`, 아니면 `finish[1..N]` 출력.
- 예제 1 검산: 1(3), 2(2) → 3은 max(3, 2)+4 = 7 → 4는 7+1 = 8, 5는 7+5 = 12.

(3) 스스로 다시 짤 때 생각 순서

- "Kahn 뼈대" → "이웃 갱신 시 max로 시작 시각 누적" → "진입차수 0이 될 때 dur 더해 확정" → "처리 수로 사이클 판정". 경계값: 관계가 없으면 각자 `dur`(예제 3), 사이클(예제 2), 선행 작업이 여러 개면 합이 아니라 `max`.
```

**10) 왕복 최단 최대** · Hard

- **요구사항**: `N`개 마을(1번~`N`번)이 `M`개의 **일방통행** 도로로 이어져 있다. 모든 마을 사람이 마을 `X`에 모였다가 각자 집으로 돌아간다. 각 마을 `i`에 대해 "`i`→`X` 최단 거리 + `X`→`i` 최단 거리"를 왕복 거리라 할 때, 왕복 거리의 **최댓값**을 출력하라. 왕복이 불가능한 마을이 하나라도 있으면 `-1`.
- **입력**: 첫 줄 `N M X` (`1 ≤ N ≤ 100`, `0 ≤ M ≤ 1000`). 이어 `M`개 줄 `u v w` (u→v, `1 ≤ w ≤ 1000`).
- **출력**: 최대 왕복 거리 또는 `-1`.
- **예제**: `4 6 2 / 1 2 4 / 1 3 2 / 2 3 1 / 3 1 1 / 2 4 3 / 4 2 2` → `6` · `3 2 1 / 1 2 1 / 1 3 1` → `-1`
- **셀프체크**: 마을마다 Dijkstra를 돌리면 `N`번이라 느리다. `X→i`는 `X`에서 Dijkstra 한 번으로 전부 나온다. `i→X`는 **간선 방향을 모두 뒤집은 그래프**에서 `X`부터 Dijkstra를 돌리면 한 번에 나온다(이 뒤집기가 핵심). `X` 자신의 왕복 거리는 `0`. `N = 1`이면 답 `0`.

```runner
@@SOLUTION
import sys, heapq
def dijkstra(n, graph, start):
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    x = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    rgraph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2]); idx += 3
        graph[u].append((v, w))
        rgraph[v].append((u, w))
    go = dijkstra(n, rgraph, x)
    back = dijkstra(n, graph, x)
    INF = float('inf')
    ans = 0
    for i in range(1, n + 1):
        if go[i] == INF or back[i] == INF:
            print(-1)
            return
        if go[i] + back[i] > ans:
            ans = go[i] + back[i]
    print(ans)
main()
@@TESTS
--IN
4 6 2
1 2 4
1 3 2
2 3 1
3 1 1
2 4 3
4 2 2
--OUT
6
--IN
3 2 1
1 2 1
1 3 1
--OUT
-1
--IN
1 0 1
--OUT
0
--IN
3 3 3
1 2 2
2 3 2
3 1 5
--OUT
9
@@EXPL
(1) 접근·핵심 아이디어

- "여러 시작점 → 한 목적지 `X`" 최단 거리는 간선을 전부 뒤집으면 "`X` → 여러 목적지"가 된다. 뒤집은 그래프에서 `X`부터 Dijkstra를 한 번 돌리면 모든 `i→X` 거리가 나온다. 원래 그래프에서 `X`부터 한 번 더 돌리면 `X→i`. 총 두 번이면 끝.
- 뒤집기는 입력을 읽을 때 `rgraph[v].append((u, w))`로 저장하는 것뿐이다. 일방통행이므로 두 그래프는 다르다.
- 한 마을이라도 어느 방향이 `INF`면 `-1`. 복잡도 `O(2 · M log N)`.

(2) 코드 단계별

- 간선 `u→v`를 `graph[u]`에, 뒤집어 `rgraph[v]`에 넣는다.
- `go = dijkstra(rgraph, X)`(집→X), `back = dijkstra(graph, X)`(X→집).
- `i = 1..N`에 대해 둘 중 하나라도 `INF`면 즉시 `-1`, 아니면 합의 최댓값 갱신.
- 예제 1 검산: `X = 2`. 집→X: 1은 4, 3은 3→1→2 = 5, 4는 2. X→집: 1은 2→3→1 = 2, 3은 1, 4는 3. 왕복: 1은 6, 3은 6, 4는 5 → 6.
- 예제 2 검산: 2와 3에서 1로 돌아오는 길이 없어 `-1`.

(3) 스스로 다시 짤 때 생각 순서

- "정방향·역방향 인접리스트 동시 구성" → "역그래프에서 X부터(가는 길)" → "정그래프에서 X부터(오는 길)" → "합의 최댓값, INF 있으면 -1". 경계값: `N = 1`(`0`), 왕복 불가 마을, 간선을 뒤집지 않고 같은 그래프를 두 번 돌리는 실수.
```

**11) 공정 임계 경로** · Hard

- **요구사항**: `N`개 공정(1번~`N`번)에 소요 시간이 있고 선후 관계 `M`개가 있다. 독립인 공정은 동시에 진행되며 각 공정은 선행 공정이 모두 끝나자마자 시작한다. 전체가 끝나는 시각과, 그 시각을 결정하는 **임계 경로**(맨 앞 공정부터 마지막 공정까지의 번호 나열)를 출력하라. 규칙은 다음과 같다: 마지막 공정은 완료 시각이 최대인 공정(동률이면 번호가 작은 것), 각 공정의 직전 공정은 선행 공정 중 완료 시각이 최대인 것(동률이면 번호가 작은 것). 사이클이 있으면 `-1`.
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 200`, `0 ≤ M ≤ 1000`). 둘째 줄 소요 시간 `N`개 (`1 ≤ 시간 ≤ 100`). 이어 `M`개 줄 `u v` (u→v).
- **출력**: 첫 줄 전체 완료 시각, 둘째 줄 임계 경로(공백 구분). 사이클이면 `-1`.
- **예제**: `6 6 / 2 3 1 4 2 1 / 1 3 / 2 3 / 3 4 / 3 5 / 4 6 / 5 6` → `9 / 2 3 4 6` · `3 3 / 1 1 1 / 1 2 / 2 3 / 3 1` → `-1`
- **셀프체크**: 완료 시각 계산은 9번 문제와 같다(Kahn + `max`). 여기에 "누가 `max`를 만들었는가"를 `crit[v]`에 기록하되, 동률이면 **번호가 작은 선행 공정**을 남겨야 한다 — 간선 입력 순서에 따라 결과가 달라지지 않도록 비교식을 정확히 쓰라. 마지막 공정에서 `crit`를 거꾸로 따라가 뒤집으면 경로다. 선후 관계가 없으면 경로는 공정 하나.

```runner
@@SOLUTION
import sys
from collections import deque
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    dur = [0] * (n + 1)
    for i in range(1, n + 1):
        dur[i] = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); idx += 2
        graph[u].append(v)
        indeg[v] += 1
    start = [0] * (n + 1)
    crit = [0] * (n + 1)
    finish = [0] * (n + 1)
    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    done = 0
    while q:
        u = q.popleft()
        done += 1
        finish[u] = start[u] + dur[u]
        for v in graph[u]:
            if finish[u] > start[v] or (finish[u] == start[v] and u < crit[v]):
                start[v] = finish[u]
                crit[v] = u
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if done != n:
        print(-1)
        return
    end = 1
    for v in range(2, n + 1):
        if finish[v] > finish[end]:
            end = v
    path = []
    cur = end
    while cur != 0:
        path.append(cur)
        cur = crit[cur]
    path.reverse()
    print(finish[end])
    print(' '.join(map(str, path)))
main()
@@TESTS
--IN
6 6
2 3 1 4 2 1
1 3
2 3
3 4
3 5
4 6
5 6
--OUT
9
2 3 4 6
--IN
3 3
1 1 1
1 2
2 3
3 1
--OUT
-1
--IN
3 0
5 5 2
--OUT
5
1
--IN
4 3
2 2 3 1
1 3
2 3
3 4
--OUT
6
1 3 4
@@EXPL
(1) 접근·핵심 아이디어

- 전체 완료 시각은 DAG 최장 경로(9번 문제)이고, 임계 경로는 그 최장 경로를 **복원**한 것이다. 최단 경로 복원에서 `parent`를 쓰듯, 여기서는 "`v`의 시작 시각을 결정한 선행 공정" `crit[v]`를 기록한다.
- 동률 규칙이 있으므로 갱신 조건을 정확히 써야 한다: `finish[u] > start[v]`이면 무조건 교체, 같으면 `u < crit[v]`일 때만 교체. 이렇게 하면 간선이 어떤 순서로 들어와도 같은 답이 나온다.
- 마지막 공정도 "완료 시각 최대, 동률이면 작은 번호"로 고르기 위해 `1..N`을 오름차순으로 돌며 엄격 초과일 때만 갱신한다. 복잡도 `O(N + M)`.

(2) 코드 단계별

- `start`(선행 완료 시각의 최댓값), `crit`(그 선행 공정, 없으면 0), `finish`를 준비. 진입차수 0인 공정을 큐에 넣는다.
- 큐에서 `u`를 꺼내 `finish[u] = start[u] + dur[u]`로 확정. 이웃 `v`마다 위 비교식으로 `start[v]`, `crit[v]` 갱신 후 진입차수 감소, 0이면 큐에 push.
- 처리 수가 `N` 미만이면 `-1`. 아니면 `end`를 고르고 `crit`를 따라 `0`이 나올 때까지 모아 뒤집는다.
- 예제 1 검산: 완료 시각 1:2, 2:3, 3:1+max(2,3) = 4, 4:8, 5:6, 6:1+max(8,6) = 9. 6 ← 4(8) ← 3 ← 2(3이 2보다 큼) → `2 3 4 6`.
- 예제 4 검산: 1과 2가 모두 2에 끝나 동률 → 번호 작은 1이 3의 직전 공정. 경로 `1 3 4`.

(3) 스스로 다시 짤 때 생각 순서

- "Kahn + 최장 경로" → "갱신 시 crit 기록(동률은 작은 번호)" → "end 선택(동률은 작은 번호)" → "crit 역추적·reverse". 경계값: 관계가 없으면 경로가 공정 하나(예제 3), 사이클(예제 2), 동률 선행 공정(예제 4). `crit`의 "없음"을 0으로 두려면 공정 번호가 1부터라는 점을 이용한다.
```

**12) 플로이드 경로 복원** · Hard

- **요구사항**: `N`개 도시와 `M`개의 **일방통행** 도로(거리)가 있다. `Q`개의 질의 `a b`마다 `a`에서 `b`까지의 최단 거리와 그 경로(도시 나열)를 한 줄에 출력하라. **질의로 주어진 쌍의 최단 경로는 유일하다고 보장**된다. 도달 불가면 `-1`. `a == b`면 `0 a`.
- **입력**: 첫 줄 `N M` (`1 ≤ N ≤ 60`, `0 ≤ M ≤ 500`). 이어 `M`개 줄 `u v w` (u→v, `1 ≤ w ≤ 1000`). 다음 줄 `Q` (`1 ≤ Q ≤ 100`), 이어 `Q`개 줄 `a b`.
- **출력**: 질의마다 `거리 a … b` 한 줄, 또는 `-1`.
- **예제**: `4 5 / 1 2 1 / 2 3 1 / 1 3 5 / 3 4 1 / 2 4 4 / 2 / 1 4 / 4 1` → `3 1 2 3 4 / -1` · `3 3 / 1 2 2 / 2 3 2 / 1 3 3 / 2 / 1 3 / 2 2` → `3 1 3 / 0 2`
- **셀프체크**: `nxt[i][j]` = "`i`에서 `j`로 가는 최단 경로에서 `i` 바로 다음 도시"를 함께 관리한다. 간선 `u→v`는 `nxt[u][v] = v`, 경유지 `k`로 갱신될 때는 `nxt[i][j] = nxt[i][k]`(경로의 첫걸음은 `i→k` 구간의 첫걸음). 복원은 `a`에서 `nxt[cur][b]`를 `b`가 될 때까지 따라간다. 같은 쌍의 도로가 여러 개면 초기화 때 짧은 것으로.

```runner
@@SOLUTION
import sys
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    INF = float('inf')
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    nxt = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0
        nxt[i][i] = i
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2]); idx += 3
        if w < dist[u][v]:
            dist[u][v] = w
            nxt[u][v] = v
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            if dist[i][k] == INF:
                continue
            for j in range(1, n + 1):
                nd = dist[i][k] + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
                    nxt[i][j] = nxt[i][k]
    q = int(data[idx]); idx += 1
    out = []
    for _ in range(q):
        a = int(data[idx]); b = int(data[idx+1]); idx += 2
        if dist[a][b] == INF:
            out.append('-1')
            continue
        path = [a]
        cur = a
        while cur != b:
            cur = nxt[cur][b]
            path.append(cur)
        out.append(str(dist[a][b]) + ' ' + ' '.join(map(str, path)))
    print('\n'.join(out))
main()
@@TESTS
--IN
4 5
1 2 1
2 3 1
1 3 5
3 4 1
2 4 4
2
1 4
4 1
--OUT
3 1 2 3 4
-1
--IN
3 3
1 2 2
2 3 2
1 3 3
2
1 3
2 2
--OUT
3 1 3
0 2
--IN
2 2
1 2 5
1 2 2
1
1 2
--OUT
2 1 2
@@EXPL
(1) 접근·핵심 아이디어

- Floyd-Warshall은 거리만 남기지만, 갱신이 일어날 때 "첫걸음"을 같이 적어 두면 경로를 복원할 수 있다. `dist[i][j]`가 `i→k→j`로 짧아졌다면 `i`에서 `j`로 가는 첫걸음은 `i`에서 `k`로 가는 첫걸음과 같다: `nxt[i][j] = nxt[i][k]`.
- 복원은 `a`에서 시작해 `nxt[cur][b]`로 한 칸씩 전진한다. 최단 경로가 유일하면 모든 부분 경로도 유일하므로 이 전진이 정확히 그 경로를 따라간다. 갱신 조건을 **엄격 미만**으로 두어야 동률 경로로 덮어써 경로가 뒤섞이는 일을 막을 수 있다.
- 복잡도 `O(N^3 + Q·N)`.

(2) 코드 단계별

- `dist`는 `INF`·대각선 0, `nxt`는 대각선만 자기 자신. 간선 `u→v`는 더 짧을 때만 `dist[u][v] = w`, `nxt[u][v] = v`.
- 삼중 루프(`k` 최외곽)에서 `nd < dist[i][j]`이면 거리와 함께 `nxt[i][j] = nxt[i][k]`.
- 질의마다 `INF`면 `-1`; 아니면 `path = [a]`에서 `cur != b`인 동안 `cur = nxt[cur][b]`를 붙여 나간다. `a == b`면 루프가 돌지 않아 `[a]`.
- 예제 1 검산: 1→4는 1→2→3→4 = 3. 1→3 직통 5보다 1→2→3 = 2가 짧아 `nxt[1][3] = nxt[1][2] = 2`, 1→4는 3을 거쳐 3이 되고 `nxt[1][4] = nxt[1][3] = 2`. 복원: 1 → nxt[1][4] = 2 → nxt[2][4] = 3 → nxt[3][4] = 4.

(3) 스스로 다시 짤 때 생각 순서

- "dist + nxt 초기화" → "간선은 nxt[u][v] = v" → "삼중 루프에서 갱신 시 nxt[i][j] = nxt[i][k]" → "질의마다 nxt 따라 전진". 경계값: `a == b`(예제 2), 도달 불가, 중복 도로(예제 3, 짧은 것만 반영). 갱신을 `<=`로 쓰면 동률 경로로 덮여 유일성 보장이 있어도 경로가 흔들릴 수 있으니 `<`를 지킨다.
```
