## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

최단 경로 문제는 알고리즘이 어렵다기보다 **고르는 데서 갈린다**. 가중치가 어떻게 생겼는지, 출발점이 하나인지 모든 쌍인지, 정점에 부가 상태가 붙는지 — 이 세 질문에 답하면 쓸 도구가 하나로 좁혀진다. 아래에서 그 갈림길을 도식과 표로 못 박고, 뼈대와 실수 목록으로 마무리한다.

**개념 지도**

```text
                    Ch05 : shortest path
                              |
        +---------------------+---------------------+
        |                                           |
   ONE SOURCE                                  ALL PAIRS
   dist[] over V                               dist[][] over V x V
        |                                           |
   +----+---------+-----------+              Floyd-Warshall O(V^3)
   |              |           |              k outermost, then i, j
  w == 1       w in {0,1}   w >= 0           negative edges are OK
  BFS          0-1 BFS      Dijkstra         dist[i][i] < 0 -> neg cycle
  deque        deque        heapq            good only while V <= ~400
  O(V+E)       O(V+E)       O(E log V)
   |              |           |
   +--------------+-----------+
                  |
          some w may be negative
                  |
          Bellman-Ford  O(V*E)   # V-1 rounds, one more round detects a
                                 # negative cycle
```

정점에 부가 상태(연료·열쇠·남은 무료권)가 붙으면 **알고리즘을 바꾸는 게 아니라 정점을 복제한다.** 완화 규칙은 그대로다.

```text
   plain graph                    state expanded  (S layers)

     (1)---(2)                    s=0 :  1 --- 2 --- 3
      |     |                              \       \      # use the ticket
     (3)---(4)                              v       v
                                   s=1 :  1 --- 2 --- 3
   dist[v]      : V cells         dist[v][s] : V * S cells
   pq : (d, v)                    pq : (d, v, s)
   answer dist[t]                 answer min(dist[t][s] for all s)
```

플로이드의 삼중 루프 순서는 이 챕터에서 가장 비싼 실수다. 왜 `k`가 밖이어야 하는지는 작은 사슬 하나로 드러난다.

```text
   edges :  1 -> 4 : 1     4 -> 3 : 1     3 -> 2 : 1
   truth :  dist[1][2] = 1 + 1 + 1 = 3

   k outermost                     k innermost (for i: for j: for k)
   k=3 : dist[4][2] = 2            i=1, j=2 : dist[4][2] is still INF
   k=4 : dist[1][3] = 2                       dist[1][3] is still INF
         dist[1][2] = 3                       -> dist[1][2] stays INF
   -> correct                      -> WRONG, and i=1 never comes back
```

**뼈대 코드**

1) 다익스트라 — 지연 삭제 + 경로 복원. 이 챕터의 기본형이다.

```python
import heapq

INF = float('inf')
dist = [INF] * (n + 1)
parent = [0] * (n + 1)          # 경로 복원이 필요할 때만
dist[start] = 0
pq = [(0, start)]

while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]:             # 낡은 항목 — visited 배열 대신 이 한 줄
        continue
    for v, w in graph[u]:       # graph[u] = [(v, w), ...]
        nd = d + w              # ← 문제마다 바뀜: max(d, w) 면 병목 최소화
        if nd < dist[v]:
            dist[v] = nd
            parent[v] = u       # 갱신하는 그 순간에 기록
            heapq.heappush(pq, (nd, v))

path, cur = [], goal            # 복원: 목표에서 거꾸로 따라 올라간다
while cur != start:
    path.append(cur)
    cur = parent[cur]
path.append(start)
path.reverse()
```

2) 플로이드-워셜 — 모든 쌍. **`k`가 반드시 최외곽.**

```python
INF = float('inf')
dist = [[INF] * (n + 1) for _ in range(n + 1)]   # 행 공유 버그 방지 형태
for i in range(1, n + 1):
    dist[i][i] = 0                               # 자기 자신은 0
for u, v, w in edges:
    dist[u][v] = min(dist[u][v], w)              # 중복 간선은 최솟값
    # dist[v][u] = min(dist[v][u], w)            # ← 무방향이면 이 줄도

for k in range(1, n + 1):            # 경유지 — 반드시 가장 바깥
    for i in range(1, n + 1):
        if dist[i][k] == INF:        # 못 가는 경유는 건너뛴다
            continue
        dik, rk, ri = dist[i][k], dist[k], dist[i]
        for j in range(1, n + 1):
            if dik + rk[j] < ri[j]:
                ri[j] = dik + rk[j]

neg_cycle = any(dist[i][i] < 0 for i in range(1, n + 1))
```

3) 0-1 BFS — 가중치가 0과 1(또는 0과 c) 두 가지뿐일 때. 힙 없이 덱만으로 O(V+E).

```python
from collections import deque

INF = float('inf')
dist = [INF] * (n + 1)
dist[start] = 0
dq = deque([start])

while dq:
    u = dq.popleft()
    for v, w in graph[u]:           # w 는 0 또는 1
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            if w == 0:
                dq.appendleft(v)    # 비용 0 → 같은 층, 앞에 넣는다
            else:
                dq.append(v)        # 비용 1 → 다음 층, 뒤에 넣는다
```

4) 상태 확장 다익스트라 — 연료·열쇠·남은 쿠폰처럼 **가짓수가 작은** 부가 상태.

```python
import heapq

S = 1 << K                    # ← 문제마다 바뀜: 연료 잔량이면 FUEL+1
INF = float('inf')
dist = [[INF] * S for _ in range(n + 1)]
dist[start][0] = 0
pq = [(0, start, 0)]

while pq:
    d, u, s = heapq.heappop(pq)
    if d > dist[u][s]:                    # 상태별로 따로 판정한다
        continue
    for v, w in graph[u]:
        ns = s                            # ← 문제마다 바뀜: 상태 전이 규칙
        if locked[v] and not (s >> key[v]) & 1:
            continue                      # 열쇠가 없으면 못 지나감
        if has_key[v]:
            ns = s | (1 << key[v])        # 열쇠를 주우면 상태가 바뀐다
        if d + w < dist[v][ns]:
            dist[v][ns] = d + w
            heapq.heappush(pq, (d + w, v, ns))

print(min(dist[goal]))                    # 목표 정점의 모든 상태 중 최소
```

5) 벨만-포드 — 음수 간선이 있고 출발점이 하나일 때.

```python
dist = [float('inf')] * (n + 1)
dist[start] = 0
for i in range(n):                    # V-1 라운드 + 판정용 1라운드
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            if i == n - 1:            # V번째에도 줄면 음수 사이클
                print(-1)
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 가중치가 없다(모든 간선 1) | BFS | 큐에 든 정점이 항상 같은 거리 층이다 | O(V+E) |
| 가중치가 0과 1 두 종류 | 0-1 BFS(`deque`) | 0은 앞, 1은 뒤에 넣으면 덱이 정렬 상태를 유지 | O(V+E) |
| 가중치 ≥ 0, 출발점 하나 | 다익스트라(`heapq`) | 최소 거리로 처음 꺼낸 정점은 그 자리에서 확정 | O(E log V) |
| 가중치 ≥ 0, 도착점이 하나이고 출발이 여럿 | 역방향 그래프 + 다익스트라 1회 | 간선을 뒤집으면 "모두→X"가 "X→모두"가 된다 | O(E log V) |
| 정점에 작은 부가 상태가 붙음 | 상태 확장 다익스트라 | 정점을 상태 수만큼 복제하면 규칙은 그대로 | O(S·E·log(S·V)) |
| 모든 쌍이 필요하고 V가 작다(≲400) | 플로이드-워셜 | 삼중 루프 한 번으로 표 전체가 완성 | O(V³) |
| 모든 쌍인데 V가 크고 E가 성기다 | 정점마다 다익스트라 | V³보다 V·E log V가 싸다 | O(V·E log V) |
| 반드시 특정 정점 P를 경유 | 플로이드 후 `dist[s][P]+dist[P][t]` | 부분 경로 최적성으로 두 조각을 그냥 이으면 됨 | O(V³) |
| 음수 간선이 있고 출발점 하나 | 벨만-포드 | 완화를 V-1번 반복하면 모든 최단이 확정 | O(V·E) |
| 음수 사이클 존재 여부 | 벨만-포드 V번째 라운드 또는 `dist[i][i] < 0` | 더 줄어들면 무한히 줄어든다는 뜻 | O(V·E) / O(V³) |
| 경로의 "최대 간선"을 최소화(병목) | 다익스트라 + 완화식 `max(d, w)` | 경로 연장이 값을 한 방향으로만 움직여 단조 | O(E log V) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 다익스트라에서 "힙에서 처음 꺼낸 정점은 확정"이 성립하는 이유와, 그 논증이 음수 간선에서 정확히 어디서 깨지는지.
- [ ] 설명할 수 있다: 지연 삭제(`d > dist[u]`면 버림)가 `visited` 배열보다 안전한 이유, 특히 상태를 얹었을 때.
- [ ] 설명할 수 있다: 다익스트라 복잡도 O(E log V)에서 log 안이 왜 V(또는 E)인지, push 횟수를 세는 과정과 함께.
- [ ] 설명할 수 있다: 경로 복원을 위해 `parent`를 기록하는 시점이 왜 "완화에 성공한 순간"인지.
- [ ] 설명할 수 있다: 0-1 BFS가 힙 없이도 옳은 이유(덱 안의 거리 값이 항상 두 종류뿐).
- [ ] 설명할 수 있다: 플로이드의 상태 정의 `D[k][i][j]`와, 점화식이 "k를 쓴다 / 안 쓴다" 두 갈래에서 나오는 과정.
- [ ] 설명할 수 있다: 플로이드에서 `k`가 최외곽이어야 하는 이유를, 순서를 바꿨을 때 못 만들어지는 경로를 예로 들어.
- [ ] 설명할 수 있다: 플로이드를 배열 한 장으로 덮어써도 답이 맞는 이유(k행·k열이 그 단계에서 안 바뀜).
- [ ] 설명할 수 있다: `dist[i][i] < 0`이 음수 사이클 판정인 이유와, 그때 최단 거리가 정의되지 않는 이유.
- [ ] 설명할 수 있다: 상태 확장에서 "정점을 복제한다"는 말의 뜻과, 상태 가짓수가 복잡도에 곱해지는 방식.
- [ ] 설명할 수 있다: "모든 정점에서 X까지"를 역방향 그래프 한 번으로 푸는 원리.
- [ ] 설명할 수 있다: 같은 입력에서 BFS·0-1 BFS·다익스트라·플로이드·벨만-포드 중 무엇을 고를지, 그 판단 근거를 순서대로.
- [ ] 설명할 수 있다: `float('inf')`와 정수 INF의 차이가 어떤 상황에서 오답을 만드는지.

**⚠️ 자주 하는 실수**

**1) 플로이드의 `k`를 가장 바깥에 두지 않는다 — 이 챕터 최대의 함정**

```python
# ❌ 틀린 코드
for i in range(1, n + 1):
    for j in range(1, n + 1):
        for k in range(1, n + 1):        # 경유지가 가장 안쪽
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
```

왜: `dist[i][j]`를 `dist[i][k] + dist[k][j]`로 만들려면 그 두 조각이 **이미 완성**돼 있어야 한다. `k`를 안쪽에 두면 특정 `(i, j)` 하나를 붙잡고 경유지만 훑는 셈이라, 아직 계산되지 않은 조각을 읽는다. 간선이 `1→4→3→2`뿐일 때 `i=1, j=2`를 볼 시점에는 `dist[1][3]`도 `dist[4][2]`도 INF라 `dist[1][2]`가 영영 3이 되지 못한다. 게다가 이 코드는 작은 그래프에서는 우연히 맞는 답을 내서 **테스트를 통과했다가 큰 입력에서만 틀린다.**

```python
# ✅ 고친 코드
for k in range(1, n + 1):                # 경유지 k 가 최외곽
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
```

**2) 다익스트라를 `visited` 배열로 막는다**

```python
# ❌ 틀린 코드
while pq:
    d, u, s = heapq.heappop(pq)
    if visited[u]:            # 정점 단위로 재방문을 막는다
        continue
    visited[u] = True
    ...
```

왜: 상태를 얹은 순간 **같은 정점이라도 다른 상태로는 다시 방문해야 한다.** `visited[u]`는 그 재방문을 통째로 지워 오답을 만든다. 기본형에서는 우연히 맞기 때문에 습관이 굳어져 더 위험하다. `d > dist[u][s]`라는 값 비교는 상태가 몇 차원이든 그대로 성립한다.

```python
# ✅ 고친 코드
while pq:
    d, u, s = heapq.heappop(pq)
    if d > dist[u][s]:        # 값으로 걸러낸다(지연 삭제)
        continue
    ...
```

**3) 음수 간선이 있는데 다익스트라를 쓴다**

```python
# ❌ 틀린 코드
# 간선: 1->2 : 2 ,  1->3 : 5 ,  3->2 : -4
dijkstra(1)
print(dist[2])            # 2 를 출력. 실제 최단은 5 + (-4) = 1
```

왜: 다익스트라의 정당성은 "경로를 연장하면 비용이 줄지 않는다"에 전적으로 기댄다. 음수 간선이 하나만 있어도 이미 확정한 정점이 나중에 더 짧아질 수 있어, 확정 자체가 무효가 된다. 정점이 적으면 플로이드, 출발점이 하나면 벨만-포드로 간다.

```python
# ✅ 고친 코드 — 음수 간선은 벨만-포드로
dist = [INF] * (n + 1)
dist[start] = 0
for _ in range(n - 1):
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
```

**4) 정수 INF를 더해 존재하지 않는 경로를 만든다**

```python
# ❌ 틀린 코드
INF = 10 ** 9
...
for k in range(1, n + 1):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            nd = dist[i][k] + dist[k][j]      # INF + INF = 2 * 10^9
            if nd < dist[i][j]:
                dist[i][j] = nd               # INF 보다 작은 "가짜 거리"
```

왜: `dist[i][k]`와 `dist[k][j]`가 둘 다 INF여도 덧셈 결과는 그냥 큰 정수일 뿐이다. `dist[i][j]`가 원래 INF였다면 `2*10^9 < 10^9`은 거짓이라 넘어가지만, 한쪽만 INF인 경우나 INF 값을 작게 잡은 경우 도달 불가 쌍이 유한한 값으로 오염되고 그 값이 다시 다른 칸으로 번진다.

```python
# ✅ 고친 코드 — 둘 중 하나
INF = float('inf')                    # inf + 유한값 = inf 라 안전
# 또는 정수 INF를 쓴다면 경유 자체를 걸러낸다
for k in range(1, n + 1):
    for i in range(1, n + 1):
        if dist[i][k] == INF:
            continue
        for j in range(1, n + 1):
            if dist[k][j] == INF:
                continue
            ...
```

**5) 자기 자신까지의 거리를 0으로 초기화하지 않는다**

```python
# ❌ 틀린 코드
dist = [[INF] * (n + 1) for _ in range(n + 1)]
for u, v, w in edges:
    dist[u][v] = w                    # 대각선을 INF 로 남겨 둔다
```

왜: `dist[i][i]`가 INF면 "i를 지나 i로 돌아오는" 경유가 전부 막혀, `dist[i][k] + dist[k][i]` 같은 조합이 계산되지 않는다. 무엇보다 **음수 사이클 판정 `dist[i][i] < 0`이 영영 참이 되지 않는다.** 판정의 기준선이 0이라는 사실 자체가 대각선 초기화에서 나온다. 다익스트라에서도 `dist[start] = 0`을 빼면 힙이 곧바로 비어 전부 INF가 나온다.

```python
# ✅ 고친 코드
dist = [[INF] * (n + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    dist[i][i] = 0                    # 자기 자신은 0 — 판정의 기준선
for u, v, w in edges:
    dist[u][v] = min(dist[u][v], w)   # 중복 간선은 최솟값으로
```

**6) 무방향 그래프인데 간선을 한 방향만 넣는다**

```python
# ❌ 틀린 코드
for _ in range(m):
    u, v, w = read_edge()
    graph[u].append((v, w))           # u -> v 만 등록
```

왜: 무방향이면 `v`에서 `u`로도 갈 수 있어야 한다. 한쪽만 넣으면 도달 가능한 정점이 INF로 남거나, 답이 실제보다 커진다. 반대로 **일방통행 문제에 양방향으로 넣으면** 없는 길이 생겨 답이 작아진다. 문제 문장에서 방향 여부를 먼저 확인하고 코드에 한 번만 반영한다.

```python
# ✅ 고친 코드
for _ in range(m):
    u, v, w = read_edge()
    graph[u].append((v, w))
    graph[v].append((u, w))           # 무방향이면 양쪽 모두
# 플로이드라면  dist[u][v] = dist[v][u] = min(dist[u][v], w)
```

**7) 힙에 넣는 튜플의 순서를 뒤집는다**

```python
# ❌ 틀린 코드
heapq.heappush(pq, (v, d))            # (정점, 거리) 로 넣었다
...
v, d = heapq.heappop(pq)              # 정점 번호가 작은 것부터 나온다
```

왜: `heapq`는 튜플을 앞에서부터 사전식으로 비교한다. 첫 원소가 정점 번호면 "번호가 가장 작은 정점"이 먼저 나오므로 거리 순 확정이 무너지고, 다익스트라의 정당성이 통째로 사라진다. 결과는 대개 **더 큰 값이 답으로 남는** 조용한 오답이다. 항상 **정렬 기준이 되는 값을 튜플의 맨 앞**에 둔다.

```python
# ✅ 고친 코드
heapq.heappush(pq, (d, v))            # (거리, 정점) — 거리 우선
d, v = heapq.heappop(pq)
# 상태를 얹으면 (거리, 정점, 상태) 순서를 그대로 유지한다
```

**다음 챕터로**

- 여기서 만든 "인접 리스트 + 완화 + 우선순위 큐" 뼈대는 최소 신장 트리(프림)에서 완화식만 `dist[u]+w`에서 `w`로 바꿔 그대로 재사용된다. "무엇을 최소화하는가"만 다르고 확정 방식은 같다.
- 상태 확장(`dist[v][s]`)은 비트마스크 DP로 이어진다. 열쇠 집합을 정수 하나로 들고 다니는 이 챕터의 습관이, 방문 집합을 정수로 들고 다니는 외판원 문제의 상태 정의와 정확히 같은 아이디어다.
