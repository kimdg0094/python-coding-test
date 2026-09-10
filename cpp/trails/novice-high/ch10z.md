## L7. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

Ch10의 다섯 알고리즘은 각각 다른 질문에 답한다. 그 질문이 무엇인지 한 장으로 정리하고, 뼈대와 함정을 모아 둔다.

**개념 지도**

```text
                    weighted / directed graph
                              |
        +---------------------+---------------------+
   shortest path        spanning tree            ordering
        |                     |                      |
   +----+-----+          +----+----+          topological sort
   |          |          |         |          (Kahn, in-degree)
 dijkstra   floyd     kruskal    prim                |
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
    unite(a,b) : hang one root under the other
    find(a) == find(b)  <=>  already connected
                        <=>  adding edge a-b makes a cycle
```

최단 경로 네 갈래를 그림 한 장으로 보면 이렇다. 왼쪽으로 갈수록 통이 단순하고 빠르다.

```text
  edge weights ?

  none / all equal      only 0 and 1        all >= 0        all pairs
        |                     |                 |               |
     queue<int>          deque<int>       priority_queue   3 nested loops
     BFS                 0-1 BFS          dijkstra         floyd
     O(V+E)              O(V+E)           O(E log V)       O(N^3)
        |                     |                 |               |
     push back           0 -> push front   greater<> !!    k must be outermost
                         1 -> push back
```

**뼈대 코드**

(1) Dijkstra — `priority_queue` + 경로 복원

```cpp
using P = pair<int, int>;                 // (거리, 정점) 순서가 중요하다
const int INF = 1e9;                      // INT_MAX 금지 (더하면 오버플로)

pair<vector<int>, vector<int>> dijkstra(int n,
        const vector<vector<P>>& g, int start) {   // g[u] = {(v, w), ...}
    vector<int> dist(n + 1, INF), par(n + 1, -1);
    priority_queue<P, vector<P>, greater<P>> pq;   // greater<> 가 있어야 최소 힙
    dist[start] = 0;
    pq.push({0, start});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;        // 낡은 항목은 버린다 (지연 삭제)
        for (auto [v, w] : g[u]) {
            if (d + w < dist[v]) {
                dist[v] = d + w;
                par[v] = u;               // 경로가 필요할 때만
                pq.push({dist[v], v});
            }
        }
    }
    return {dist, par};
}

vector<int> restore(const vector<int>& par, int goal) {
    vector<int> path;
    for (int cur = goal; cur != -1; cur = par[cur]) path.push_back(cur);
    reverse(path.begin(), path.end());
    return path;
}
```

(2) Floyd-Warshall — 모든 쌍

```cpp
const int INF = 1e9;

vector<vector<int>> floyd(int n, const vector<array<int,3>>& edges) {
    vector<vector<int>> dist(n + 1, vector<int>(n + 1, INF));
    for (int i = 1; i <= n; i++) dist[i][i] = 0;   // 자기 자신은 0 (빠뜨리기 쉬움)
    for (auto& e : edges) {
        int u = e[0], v = e[1], w = e[2];
        dist[u][v] = min(dist[u][v], w);           // 중복 간선 대비
        dist[v][u] = min(dist[v][u], w);           // 방향 그래프면 이 줄 삭제
    }
    for (int k = 1; k <= n; k++)                   // k 가 반드시 가장 바깥
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                if (dist[i][k] != INF && dist[k][j] != INF)   // 오버플로 방지
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
    return dist;
}
```

(3) Union-Find — 경로 압축

```cpp
vector<int> parent;                       // main 에서 parent[i] = i 로 초기화

int find(int x) {                         // 반복 버전: 재귀 깊이 걱정이 없다
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];    // 경로 압축(절반씩 끌어올림)
        x = parent[x];
    }
    return x;
}

bool unite(int a, int b) {                // union 은 예약어라 쓸 수 없다
    int ra = find(a), rb = find(b);
    if (ra == rb) return false;           // 이미 같은 집합 = 사이클
    parent[ra] = rb;
    return true;
}
```

(4) Kruskal — MST

```cpp
long long kruskal(int n, vector<tuple<int,int,int>>& edges) {  // {w, u, v}
    parent.resize(n + 1);
    for (int i = 0; i <= n; i++) parent[i] = i;
    sort(edges.begin(), edges.end());     // w 가 맨 앞이라 기본 정렬로 끝난다
    long long total = 0;                  // 합은 long long
    int cnt = 0;
    for (auto& [w, u, v] : edges) {
        if (!unite(u, v)) continue;       // 사이클이면 버린다
        total += w;
        if (++cnt == n - 1) break;        // 간선 V-1 개면 완성
    }
    return cnt == n - 1 ? total : -1;     // 연결 아님 처리는 문제마다 바뀜
}
```

(5) Prim — MST

```cpp
using P = pair<int, int>;                 // (간선 가중치, 정점)

long long prim(int n, const vector<vector<P>>& g, int start = 1) {
    vector<bool> visited(n + 1, false);
    priority_queue<P, vector<P>, greater<P>> pq;
    long long total = 0;
    int cnt = 0;
    pq.push({0, start});
    while (!pq.empty() && cnt < n) {
        auto [w, u] = pq.top(); pq.pop();
        if (visited[u]) continue;         // 낡은 항목 (지연 삭제)
        visited[u] = true;
        total += w;                       // 누적 거리가 아니라 간선 가중치
        cnt++;
        for (auto [v, wv] : g[u])
            if (!visited[v]) pq.push({wv, v});   // dist+w 가 아니라 w
    }
    return cnt == n ? total : -1;
}
```

(6) 위상 정렬 — Kahn

```cpp
vector<int> topo(int n, const vector<vector<int>>& g, vector<int> indeg) {
    queue<int> q;                         // 사전순 답이 필요하면
    for (int v = 1; v <= n; v++)          // priority_queue<int, vector<int>,
        if (indeg[v] == 0) q.push(v);     //   greater<int>> 로 바꾼다
    vector<int> order;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : g[u])
            if (--indeg[v] == 0) q.push(v);
    }
    if ((int)order.size() != n) return {};   // 비었으면 사이클
    return order;
}
```

(7) 0-1 BFS — 가중치가 0 또는 1일 때

```cpp
vector<int> zero_one_bfs(int n, const vector<vector<pair<int,int>>>& g,
                         int start) {     // g[u] = {(v, w)}, w 는 0 또는 1
    const int INF = 1e9;
    vector<int> dist(n + 1, INF);
    deque<int> dq;                        // 힙이 아니라 덱을 쓴다
    dist[start] = 0;
    dq.push_back(start);
    while (!dq.empty()) {
        int u = dq.front(); dq.pop_front();
        for (auto [v, w] : g[u])
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (w == 0) dq.push_front(v);   // 비용 0 이면 앞에
                else        dq.push_back(v);    // 비용 1 이면 뒤에
            }
    }
    return dist;
}
```

**언제 무엇을 쓰나**

최단 경로 알고리즘 선택표부터 못 박는다. 이 표가 Ch9~Ch10의 갈림길 전부다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 간선 가중치가 없다(또는 전부 같다), 시작점 하나 | BFS (Ch9) | 처음 도달이 곧 최단, 힙이 필요 없다 | `O(V+E)` |
| 간선 가중치가 0 또는 1뿐, 시작점 하나 | 0-1 BFS (`deque`) | 덱 앞/뒤로 나눠 넣으면 힙 없이 정렬 유지 | `O(V+E)` |
| 간선 가중치가 모두 0 이상, 시작점 하나 | Dijkstra (`priority_queue`) | 최소 거리를 꺼내면 그 값이 확정된다 | `O((V+E) log V)` |
| 모든 정점 쌍, 정점이 적다(대략 `N <= 500`) | Floyd-Warshall | 삼중 루프 한 방, 구현이 가장 짧다 | `O(N^3)` |
| 모든 정점 쌍인데 정점이 많고 간선은 희소 | Dijkstra를 `V`번 | `V·E log V`가 `N^3`보다 작다 | `O(V·E log V)` |
| 음수 간선이 있다 | Dijkstra 금지 | 확정 논증이 "비용이 0 이상"에 기대고 있다 | — |

나머지 도구의 갈림길이다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 모든 정점을 최소 비용으로 연결, 간선 목록이 주어짐 | Kruskal | 정렬 한 번 + 사이클 검사만 | `O(E log E)` |
| 모든 정점을 최소 비용으로 연결, 인접 리스트이거나 밀집 | Prim | 트리 경계 간선만 힙으로 관리 | `O(E log V)` |
| "이미 연결됐나"를 여러 번 물어본다 | Union-Find | `find` 두 번이면 끝 | 사실상 `O(1)` |
| 선후 관계·의존성 순서를 정한다 | 위상 정렬(Kahn) | 진입차수 0을 하나씩 떼어내면 된다 | `O(V+E)` |
| 방향 그래프에 사이클이 있는지 본다 | 위상 정렬 후 길이 확인 | 사이클 정점은 진입차수가 0이 못 된다 | `O(V+E)` |

자료형·INF 선택표도 함께 못 박는다. 여기서 나는 오류는 컴파일도 되고 예제도 통과해서 찾기가 가장 어렵다.

| 상황 | 고르는 것 | 이유 |
| --- | --- | --- |
| Dijkstra·Floyd의 INF | `int INF = 1e9` | `INT_MAX + w`는 오버플로해 음수가 된다 |
| 거리 합이 21억을 넘을 수 있다 | `long long`, `INF = 1e18` | 간선 10만 × 가중치 100만이면 넘는다 |
| MST 가중치 합 | `long long total` | 간선 수 × 가중치가 금세 `int`를 넘는다 |
| 최소 힙 | `priority_queue<P, vector<P>, greater<P>>` | 기본은 **최대** 힙이라 그냥 쓰면 오답 |
| 0-1 BFS의 통 | `deque<int>` | 앞뒤 삽입이 `O(1)`, 힙보다 `log` 만큼 빠르다 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: Dijkstra가 "가장 가까운 정점을 꺼내면 그 값이 확정"이라고 말할 수 있는 근거.
- [ ] 설명할 수 있다: 음수 간선이 하나만 있어도 Dijkstra가 왜 틀리는지, 반례를 직접 그리며.
- [ ] 설명할 수 있다: Dijkstra의 복잡도 `O((V+E) log V)`에서 `log V`와 `V+E`가 각각 어디서 나왔는지.
- [ ] 설명할 수 있다: 지연 삭제(`if (d > dist[u]) continue;`)가 왜 필요하고, 빼면 무슨 일이 생기는지.
- [ ] 설명할 수 있다: `priority_queue`의 기본이 최대 힙이라는 것과, `greater<>`를 빼면 결과가 어떻게 되는지.
- [ ] 설명할 수 있다: Floyd-Warshall의 상태 정의와 점화식이 "마지막 선택"을 무엇으로 쪼갠 결과인지.
- [ ] 설명할 수 있다: 삼중 루프에서 `k`가 왜 반드시 가장 바깥이어야 하는지.
- [ ] 설명할 수 있다: 배열 하나를 제자리에서 덮어써도 되는 이유.
- [ ] 설명할 수 있다: INF를 `INT_MAX`로 두면 왜 표가 오염되는지, `1e9`가 왜 안전한지.
- [ ] 설명할 수 있다: 컷 성질이 무엇이고, 그것이 왜 Kruskal과 Prim을 동시에 정당화하는지.
- [ ] 설명할 수 있다: Kruskal이 간선을 버리는 순간이 정확히 어떤 상황인지.
- [ ] 설명할 수 있다: Union-Find의 경로 압축이 트리 모양을 어떻게 바꾸는지, 왜 빨라지는지.
- [ ] 설명할 수 있다: Prim과 Dijkstra의 코드가 닮았는데도 결과가 다른 이유(`w` vs `dist[u]+w`).
- [ ] 설명할 수 있다: MST의 간선 수가 왜 정확히 `V-1`개인지.
- [ ] 설명할 수 있다: Kahn 알고리즘이 사이클을 어떻게 감지하는지.
- [ ] 설명할 수 있다: 위상 정렬의 답이 여러 개일 수 있는 이유와, 사전순 최소를 얻는 방법.
- [ ] 설명할 수 있다: 최단 경로 선택표의 네 갈래(BFS / 0-1 BFS / Dijkstra / Floyd)를 상황만 보고 고르는 기준.

**⚠️ 자주 하는 실수**

(1) `priority_queue`를 그냥 써서 최대 힙이 된다

```cpp
// ❌ 틀린 코드
priority_queue<pair<int,int>> pq;         // 기본은 최대 힙이다
pq.push({0, start});
while (!pq.empty()) {
    auto [d, u] = pq.top(); pq.pop();     // 가장 '먼' 정점이 먼저 나온다
    // ...
}
```

왜: C++의 `priority_queue`는 기본 비교자가 `less`라서 **가장 큰 값**이 먼저 나온다. Dijkstra는 "가장 가까운 것을 꺼내면 확정"이라는 논증에 기대므로 순서가 뒤집히면 확정이 성립하지 않는다. 컴파일도 되고 그럴듯한 숫자도 나오기 때문에 알아채기 어렵다.

```cpp
// ✅ 고친 코드
using P = pair<int,int>;
priority_queue<P, vector<P>, greater<P>> pq;   // 세 인자를 다 적어야 최소 힙
pq.push({0, start});
```

(2) Dijkstra에서 이미 확정된 정점을 다시 처리한다

```cpp
// ❌ 틀린 코드
while (!pq.empty()) {
    auto [d, u] = pq.top(); pq.pop();
    for (auto [v, w] : g[u])              // 낡은 (d, u) 도 그대로 전개한다
        if (d + w < dist[v]) {
            dist[v] = d + w;
            pq.push({dist[v], v});
        }
}
```

왜: 거리를 갱신할 때마다 힙에 새 항목을 넣으므로, 같은 정점의 낡은 항목이 힙에 여러 개 남는다. 그것까지 전부 전개하면 정점 하나를 여러 번 완화하게 되어, 조밀한 그래프에서 시간 초과로 이어진다.

```cpp
// ✅ 고친 코드
while (!pq.empty()) {
    auto [d, u] = pq.top(); pq.pop();
    if (d > dist[u]) continue;            // 낡은 항목이면 버린다
    for (auto [v, w] : g[u])
        if (d + w < dist[v]) {
            dist[v] = d + w;
            pq.push({dist[v], v});
        }
}
```

(3) INF를 `INT_MAX`로 두고 그대로 더한다

```cpp
// ❌ 틀린 코드
const int INF = INT_MAX;                  // 약 21억
// ...
if (dist[i][k] + dist[k][j] < dist[i][j])         // 21억 + 21억 = 오버플로
    dist[i][j] = dist[i][k] + dist[k][j];         // 음수가 들어간다
```

왜: `int` 두 개를 더해 범위를 넘으면 값이 **음수로 감싸 돈다.** 실제로는 이어지지 않은 경로에 음수 거리가 기록되고, `k`가 커질수록 그 값이 다시 전파되어 표 전체가 오염된다. 오버플로는 예외를 던지지 않으므로 프로그램은 멀쩡히 답을 출력한다.

```cpp
// ✅ 고친 코드
const int INF = 1e9;                      // 두 개를 더해도 int 안에 남는다
if (dist[i][k] != INF && dist[k][j] != INF)       // 그래도 경유 가능 여부 확인
    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
```

(4) Floyd의 루프 순서를 뒤집는다

```cpp
// ❌ 틀린 코드
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= n; j++)
        for (int k = 1; k <= n; k++)      // k 가 가장 안쪽
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
```

왜: `k` 루프 한 바퀴는 "경유 가능한 정점 집합을 `1..k`로 넓히는 한 단계"다. `i`를 바깥에 두면 `dist[i][k]`나 `dist[k][j]`가 아직 완성되지 않은 상태에서 참조된다. `1 -> 3 -> 4 -> 2` 사슬에서 `dist[1][2]`는 INF로 남는다.

```cpp
// ✅ 고친 코드
for (int k = 1; k <= n; k++)              // k 가 반드시 가장 바깥
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
```

(5) 자기 자신까지의 거리를 0으로 두지 않는다

```cpp
// ❌ 틀린 코드
vector<vector<int>> dist(n + 1, vector<int>(n + 1, INF));
for (auto& e : edges)
    dist[e[0]][e[1]] = e[2];              // dist[i][i] 가 INF 로 남아 있다
```

왜: `dist[i][i]`가 INF면 `i`를 경유지로 쓰는 계산이 전부 막히고, "자기 자신까지의 거리"를 묻는 출력에서도 INF가 나온다. 자기 간선이 있는 경우가 아니라면 `dist[i][i] = 0`이 정의상 맞다. 또 같은 두 정점 사이에 간선이 여러 개면 `min`으로 받아야 한다.

```cpp
// ✅ 고친 코드
vector<vector<int>> dist(n + 1, vector<int>(n + 1, INF));
for (int i = 1; i <= n; i++) dist[i][i] = 0;      // 먼저 대각선을 0으로
for (auto& e : edges)
    dist[e[0]][e[1]] = min(dist[e[0]][e[1]], e[2]);
```

(6) Prim의 힙에 누적 거리를 넣는다

```cpp
// ❌ 틀린 코드
for (auto [v, wv] : g[u])
    if (!visited[v])
        pq.push({total + wv, v});         // 누적값을 넣었다
```

왜: MST가 최소로 만들려는 것은 시작점에서의 거리가 아니라 "채택한 간선 가중치의 합"이다. 누적값을 넣으면 시작점에서 먼 정점의 간선이 실제보다 비싸 보여, 최소 신장 트리가 아니라 최단 경로 트리가 만들어진다. Dijkstra 코드를 복사해 고칠 때 가장 자주 남는 줄이다.

```cpp
// ✅ 고친 코드
for (auto [v, wv] : g[u])
    if (!visited[v])
        pq.push({wv, v});                 // 간선 하나의 가중치만
```

(7) `union`이라는 이름을 쓰거나 가중치 합을 `int`로 받는다

```cpp
// ❌ 틀린 코드
bool union(int a, int b) { /* ... */ }    // union 은 C++ 예약어: 컴파일 오류
int total = 0;                            // 간선 10만 x 가중치 100만 = 1000억
for (auto& [w, u, v] : edges)
    if (unite(u, v)) total += w;          // int 를 넘어 음수로 뒤집힌다
```

왜: `union`은 공용체를 선언하는 키워드라 함수 이름으로 쓸 수 없다. 그리고 MST의 가중치 합은 간선 수와 가중치의 곱 규모라 `int`(약 21억)를 쉽게 넘는다. 넘치면 음수가 되어 "최소 비용이 음수"라는 이상한 답이 나온다.

```cpp
// ✅ 고친 코드
bool unite(int a, int b) { /* ... */ }    // 이름을 바꾼다
long long total = 0;                      // 합은 long long
for (auto& [w, u, v] : edges)
    if (unite(u, v)) total += w;
```

(8) 위상 정렬에서 사이클 판정을 빼먹는다

```cpp
// ❌ 틀린 코드
while (!q.empty()) {
    int u = q.front(); q.pop();
    order.push_back(u);
    for (int v : g[u])
        if (--indeg[v] == 0) q.push(v);
}
return order;                             // 사이클이면 짧은 목록을 그냥 돌려준다
```

왜: 사이클 위의 정점은 진입차수가 0이 되지 못해 큐에 들어가지 못한다. 그래서 `order`에는 사이클 밖 정점만 담기고, 검사를 안 하면 "부분 답"을 정답처럼 출력하게 된다. 비교할 때 `order.size()`는 부호 없는 값이니 `int`로 캐스팅한다.

```cpp
// ✅ 고친 코드
if ((int)order.size() != n) return {};    // 길이가 N 미만이면 사이클
return order;
```

(9) 진입차수를 반대 방향으로 센다

```cpp
// ❌ 틀린 코드
for (int i = 0; i < m; i++) {
    int u, v; cin >> u >> v;              // u 를 먼저 해야 한다는 뜻
    g[u].push_back(v);
    indeg[u]++;                           // 출발지를 올렸다
}
```

왜: 진입차수는 "그 정점으로 들어오는 간선 수"이므로 도착지 `v`만 올려야 한다. 출발지를 올리면 선행 조건이 없는 정점의 차수가 0이 아니게 되어 큐가 처음부터 비고, 멀쩡한 DAG를 사이클로 오판한다.

```cpp
// ✅ 고친 코드
for (int i = 0; i < m; i++) {
    int u, v; cin >> u >> v;
    g[u].push_back(v);
    indeg[v]++;                           // 도착지만 올린다
}
```

**다음 챕터로**

- Ch9의 BFS와 Ch10의 Dijkstra는 같은 뼈대(거리 배열 + 자료구조에서 하나 꺼내 이웃 완화)를 공유한다. 다른 것은 "무엇을 꺼내는 통이냐"뿐이다 — `queue`냐, `priority_queue`냐, `deque`냐.
- Union-Find는 MST뿐 아니라 "같은 그룹인가"를 묻는 모든 문제에서 다시 등장한다. 이 챕터에서 손에 익혀 두면 이후 그래프·집합 문제의 절반이 짧아진다.
- 위상 정렬은 "순서가 정해진 상태 공간"이라는 점에서 이후의 DP와 이어진다. DAG 위에서는 위상 순서대로 훑는 것이 곧 올바른 계산 순서다.
- 자료형 감각도 함께 가져간다. 거리·합은 넘칠 것 같으면 `long long`, INF는 `1e9`(또는 `long long`이면 `1e18`), 인덱스는 `int`. 이 세 가지만 지켜도 "예제는 맞는데 채점은 틀리는" 사고의 대부분이 사라진다.
