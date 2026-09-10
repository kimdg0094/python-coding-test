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
  queue        deque        pq + greater<>   good only while V <= ~400
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
   answer dist[t]                 answer min over dist[t][s]
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

C++에서는 여기에 **자료형 함정**이 한 겹 더 얹힌다. 거리 합과 INF 값을 먼저 정하고 시작해야 한다.

```text
   pick INF before writing any relax line

   INT_MAX   = 2147483647          INT_MAX + 1   -> negative  (UB)
   LLONG_MAX = 9.22e18             LLONG_MAX + 1 -> negative
   1e18                            1e18 + 1e18 = 2e18 < 9.22e18   OK

   path sum : 1e5 edges * 1e5 weight = 1e10   -> int is NOT enough
   rule     : dist / nd / heap.first are all long long

   priority_queue<pair<ll,int>>              pops the LARGEST  (wrong)
   priority_queue<..., greater<>>            pops the SMALLEST (right)
   pair order must be (distance, vertex), never (vertex, distance)
```

**뼈대 코드**

1) Dijkstra — 지연 삭제 + 경로 복원. 이 챕터의 기본형이다.

```cpp
const long long INF = 1e18;              // LLONG_MAX 금지(더하면 뒤집힌다)
vector<long long> dist(n + 1, INF);
vector<int> par(n + 1, 0);               // 경로 복원이 필요할 때만
dist[start] = 0;
priority_queue<pair<long long,int>,
               vector<pair<long long,int>>, greater<>> pq;   // 최소 힙
pq.push({0, start});

while (!pq.empty()) {
    auto [d, u] = pq.top(); pq.pop();
    if (d > dist[u]) continue;           // 낡은 항목 — visited 배열 대신 이 한 줄
    for (auto [v, w] : graph[u]) {       // graph[u] = {(v, w), ...}
        long long nd = d + w;            // ← 문제마다 바뀜: max(d, w)면 병목 최소화
        if (nd < dist[v]) {
            dist[v] = nd;
            par[v] = u;                  // 갱신하는 그 순간에 기록
            pq.push({nd, v});
        }
    }
}

vector<int> path;                        // 복원: 목표에서 거꾸로 따라 올라간다
for (int cur = goal; cur != start; cur = par[cur]) path.push_back(cur);
path.push_back(start);
reverse(path.begin(), path.end());
```

2) Floyd-Warshall — 모든 쌍. **`k`가 반드시 최외곽.**

```cpp
const long long INF = 1e18;
vector<vector<long long>> dist(n + 1, vector<long long>(n + 1, INF));
for (int i = 1; i <= n; i++) dist[i][i] = 0;          // 자기 자신은 0
for (auto& [u, v, w] : edges) {
    dist[u][v] = min(dist[u][v], (long long)w);       // 중복 간선은 최솟값
    // dist[v][u] = min(dist[v][u], (long long)w);    // ← 무방향이면 이 줄도
}

for (int k = 1; k <= n; k++) {           // 경유지 — 반드시 가장 바깥
    for (int i = 1; i <= n; i++) {
        if (dist[i][k] == INF) continue; // 못 가는 경유는 건너뛴다
        long long dik = dist[i][k];
        auto& ri = dist[i];              // 행 참조를 미리 잡아 인덱싱을 줄인다
        auto& rk = dist[k];
        for (int j = 1; j <= n; j++) {
            if (rk[j] == INF) continue;
            if (dik + rk[j] < ri[j]) ri[j] = dik + rk[j];
        }
    }
}

bool neg_cycle = false;
for (int i = 1; i <= n; i++) if (dist[i][i] < 0) neg_cycle = true;
```

3) 0-1 BFS — 가중치가 0과 1(또는 0과 c) 두 가지뿐일 때. 힙 없이 덱만으로 O(V+E).

```cpp
vector<int> dist(n + 1, INT_MAX);
dist[start] = 0;
deque<int> dq;
dq.push_back(start);

while (!dq.empty()) {
    int u = dq.front(); dq.pop_front();
    for (auto [v, w] : graph[u]) {       // w 는 0 또는 1
        if (dist[u] + w < dist[v]) {
            dist[v] = dist[u] + w;
            if (w == 0) dq.push_front(v);   // 비용 0 → 같은 층, 앞에 넣는다
            else        dq.push_back(v);    // 비용 1 → 다음 층, 뒤에 넣는다
        }
    }
}
```

4) 상태 확장 Dijkstra — 연료·열쇠·남은 쿠폰처럼 **가짓수가 작은** 부가 상태.

```cpp
const int S = 1 << K;                    // ← 문제마다 바뀜: 연료 잔량이면 FUEL+1
const long long INF = 1e18;
vector<vector<long long>> dist(n + 1, vector<long long>(S, INF));
dist[start][0] = 0;
priority_queue<tuple<long long,int,int>,
               vector<tuple<long long,int,int>>, greater<>> pq;
pq.push({0, start, 0});

while (!pq.empty()) {
    auto [d, u, s] = pq.top(); pq.pop();
    if (d > dist[u][s]) continue;        // 상태별로 따로 판정한다
    for (auto [v, w] : graph[u]) {
        int ns = s;                      // ← 문제마다 바뀜: 상태 전이 규칙
        if (locked[v] && !((s >> key[v]) & 1)) continue;   // 열쇠가 없으면 못 지나감
        if (has_key[v]) ns = s | (1 << key[v]);            // 주우면 상태가 바뀐다
        if (d + w < dist[v][ns]) {
            dist[v][ns] = d + w;
            pq.push({d + w, v, ns});
        }
    }
}
cout << *min_element(dist[goal].begin(), dist[goal].end()) << '\n';
```

5) Bellman-Ford — 음수 간선이 있고 출발점이 하나일 때.

```cpp
const long long INF = 1e18;
vector<long long> dist(n + 1, INF);
dist[start] = 0;
bool neg = false;
for (int i = 0; i < n; i++) {            // V-1 라운드 + 판정용 1라운드
    for (auto& [u, v, w] : edges) {
        if (dist[u] == INF) continue;    // 도달 못 한 정점에서 완화 금지
        if (dist[u] + w < dist[v]) {
            dist[v] = dist[u] + w;
            if (i == n - 1) neg = true;  // V번째에도 줄면 음수 사이클
        }
    }
}
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 가중치가 없다(모든 간선 1) | BFS(`queue`) | 큐에 든 정점이 항상 같은 거리 층이다 | O(V+E) |
| 가중치가 0과 1 두 종류 | 0-1 BFS(`deque`) | 0은 앞, 1은 뒤에 넣으면 덱이 정렬 상태를 유지 | O(V+E) |
| 가중치 ≥ 0, 출발점 하나 | Dijkstra(`priority_queue` + `greater<>`) | 최소 거리로 처음 꺼낸 정점은 그 자리에서 확정 | O(E log V) |
| 가중치 ≥ 0, 도착점이 하나이고 출발이 여럿 | 역방향 그래프 + Dijkstra 1회 | 간선을 뒤집으면 "모두→X"가 "X→모두"가 된다 | O(E log V) |
| 정점에 작은 부가 상태가 붙음 | 상태 확장 Dijkstra | 정점을 상태 수만큼 복제하면 규칙은 그대로 | O(S·E·log(S·V)) |
| 모든 쌍이 필요하고 V가 작다(≲400) | Floyd-Warshall | 삼중 루프 한 번으로 표 전체가 완성 | O(V³) |
| 모든 쌍인데 V가 크고 E가 성기다 | 정점마다 Dijkstra | V³보다 V·E log V가 싸다 | O(V·E log V) |
| 반드시 특정 정점 P를 경유 | Floyd 후 `dist[s][P]+dist[P][t]` | 부분 경로 최적성으로 두 조각을 그냥 이으면 됨 | O(V³) |
| 음수 간선이 있고 출발점 하나 | Bellman-Ford | 완화를 V-1번 반복하면 모든 최단이 확정 | O(V·E) |
| 음수 사이클 존재 여부 | Bellman-Ford V번째 라운드 또는 `dist[i][i] < 0` | 더 줄어들면 무한히 줄어든다는 뜻 | O(V·E) / O(V³) |
| 경로의 "최대 간선"을 최소화(병목) | Dijkstra + 완화식 `max(d, w)` | 경로 연장이 값을 한 방향으로만 움직여 단조 | O(E log V) |
| 도달 가능성만 필요(가중치 무시) | Floyd의 min/plus를 or/and로 치환 | 삼중 루프 구조가 그대로다 | O(V³) |

메모리·자료형도 선택의 일부다. 아래 기준으로 미리 못 박고 시작한다.

| 규모 | 자료형·구조 | 근거 |
|---|---|---|
| 경로 합이 `2·10^9` 이하 | `int` + `INF = 1e9` | `int` 안에서 끝난다 |
| 경로 합이 그 이상 | `long long` + `INF = 1e18` | `1e18 + 1e18`도 `long long`에 들어간다 |
| `V ≤ 500`, 모든 쌍 | `vector<vector<long long>>` | `500²×8B = 2MB`로 여유 |
| `V ≥ 2000`, 모든 쌍 | Floyd 포기(정점마다 Dijkstra) | 표만 32MB, 연산도 `8·10^9` |
| `E`가 `10^5` 이상 | 인접 리스트 + `const&` 전달 | 인접 행렬은 `V²` 메모리, 값 전달은 전체 복사 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: Dijkstra에서 "힙에서 처음 꺼낸 정점은 확정"이 성립하는 이유와, 그 논증이 음수 간선에서 정확히 어디서 깨지는지.
- [ ] 설명할 수 있다: 지연 삭제(`d > dist[u]`면 버림)가 `visited` 배열보다 안전한 이유, 특히 상태를 얹었을 때.
- [ ] 설명할 수 있다: Dijkstra 복잡도 O(E log V)에서 log 안이 왜 V(또는 E)인지, push 횟수를 세는 과정과 함께.
- [ ] 설명할 수 있다: `priority_queue`가 기본으로 최대 힙인 이유와, `greater<>`가 하는 일.
- [ ] 설명할 수 있다: 힙에 `(거리, 정점)` 순서로 넣어야 하는 이유를 `pair`의 사전식 비교로.
- [ ] 설명할 수 있다: 경로 복원을 위해 `par`를 기록하는 시점이 왜 "완화에 성공한 순간"인지.
- [ ] 설명할 수 있다: 0-1 BFS가 힙 없이도 옳은 이유(덱 안의 거리 값이 항상 두 종류뿐).
- [ ] 설명할 수 있다: Floyd의 상태 정의 `D[k][i][j]`와, 점화식이 "k를 쓴다 / 안 쓴다" 두 갈래에서 나오는 과정.
- [ ] 설명할 수 있다: Floyd에서 `k`가 최외곽이어야 하는 이유를, 순서를 바꿨을 때 못 만들어지는 경로를 예로 들어.
- [ ] 설명할 수 있다: Floyd를 배열 한 장으로 덮어써도 답이 맞는 이유(k행·k열이 그 단계에서 안 바뀜).
- [ ] 설명할 수 있다: `dist[i][i] < 0`이 음수 사이클 판정인 이유와, 그때 최단 거리가 정의되지 않는 이유.
- [ ] 설명할 수 있다: `INF`를 `LLONG_MAX`로 두면 왜 위험하고, `1e18`이 왜 안전한지.
- [ ] 설명할 수 있다: 상태 확장에서 "정점을 복제한다"는 말의 뜻과, 상태 가짓수가 복잡도에 곱해지는 방식.
- [ ] 설명할 수 있다: "모든 정점에서 X까지"를 역방향 그래프 한 번으로 푸는 원리.
- [ ] 설명할 수 있다: 같은 입력에서 BFS·0-1 BFS·Dijkstra·Floyd·Bellman-Ford 중 무엇을 고를지, 그 판단 근거를 순서대로.

**⚠️ 자주 하는 실수**

**1) Floyd의 `k`를 가장 바깥에 두지 않는다 — 이 챕터 최대의 함정**

```cpp
// ❌ 틀린 코드
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= n; j++)
        for (int k = 1; k <= n; k++)          // 경유지가 가장 안쪽
            if (dist[i][k] + dist[k][j] < dist[i][j])
                dist[i][j] = dist[i][k] + dist[k][j];
```

왜: `dist[i][j]`를 `dist[i][k] + dist[k][j]`로 만들려면 그 두 조각이 **이미 완성**돼 있어야 한다. `k`를 안쪽에 두면 특정 `(i, j)` 하나를 붙잡고 경유지만 훑는 셈이라, 아직 계산되지 않은 조각을 읽는다. 간선이 `1→4→3→2`뿐일 때 `i=1, j=2`를 볼 시점에는 `dist[1][3]`도 `dist[4][2]`도 INF라 `dist[1][2]`가 영영 3이 되지 못한다. 게다가 이 코드는 작은 그래프에서는 우연히 맞는 답을 내서 **테스트를 통과했다가 큰 입력에서만 틀린다.**

```cpp
// ✅ 고친 코드
for (int k = 1; k <= n; k++)                  // 경유지 k 가 최외곽
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            if (dist[i][k] + dist[k][j] < dist[i][j])
                dist[i][j] = dist[i][k] + dist[k][j];
```

**2) `INF`를 `LLONG_MAX`로 두고 그대로 더한다**

```cpp
// ❌ 틀린 코드
const long long INF = LLONG_MAX;
for (int k = 1; k <= n; k++)
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) {
            long long nd = dist[i][k] + dist[k][j];   // INF + 유한값 -> 오버플로
            if (nd < dist[i][j]) dist[i][j] = nd;     // 음수가 되어 덮어쓴다
        }
```

왜: `LLONG_MAX`에 1만 더해도 부호가 뒤집혀 큰 음수가 된다. 그 음수는 어떤 `dist[i][j]`보다도 작으므로 도달 불가 쌍이 **가짜 거리로 오염**되고, 다음 k 라운드에서 다른 칸까지 번진다. 최종적으로 `dist[i][i] < 0`이 참이 되어 **없는 음수 사이클을 보고**한다. `INT_MAX`도 같은 이유로 위험하다.

```cpp
// ✅ 고친 코드 — 둘 중 하나
const long long INF = 1e18;                   // 1e18 + 1e18 = 2e18 < 9.2e18
// 또는 INF 경유 자체를 걸러낸다
for (int k = 1; k <= n; k++)
    for (int i = 1; i <= n; i++) {
        if (dist[i][k] == INF) continue;
        for (int j = 1; j <= n; j++) {
            if (dist[k][j] == INF) continue;
            if (dist[i][k] + dist[k][j] < dist[i][j])
                dist[i][j] = dist[i][k] + dist[k][j];
        }
    }
```

**3) `priority_queue`를 그냥 써서 최대 힙으로 돌린다**

```cpp
// ❌ 틀린 코드
priority_queue<pair<long long,int>> pq;       // 기본 비교자 less = 최대 힙
pq.push({0, start});
while (!pq.empty()) {
    auto [d, u] = pq.top(); pq.pop();         // 가장 "먼" 항목부터 나온다
    ...
}
```

왜: C++의 `priority_queue`는 `top()`이 **최댓값**이다. Dijkstra의 정당성은 "남은 것 중 가장 가까운 것을 확정한다"에 전적으로 기대므로, 방향이 뒤집히면 확정 순서가 무너져 답이 커진다. 컴파일 오류도 런타임 오류도 없이 값만 틀리는 것이 이 실수의 특징이다. `(정점, 거리)` 순서로 넣어 정점 번호 기준으로 꺼내는 것도 같은 부류의 사고다.

```cpp
// ✅ 고친 코드
priority_queue<pair<long long,int>,
               vector<pair<long long,int>>, greater<>> pq;   // 최소 힙
pq.push({0, start});                          // (거리, 정점) — 정렬 기준이 앞
```

**4) Dijkstra를 `visited` 배열로 막는다**

```cpp
// ❌ 틀린 코드
while (!pq.empty()) {
    auto [d, u, s] = pq.top(); pq.pop();
    if (visited[u]) continue;                 // 정점 단위로 재방문을 막는다
    visited[u] = true;
    ...
}
```

왜: 상태를 얹은 순간 **같은 정점이라도 다른 상태로는 다시 방문해야 한다.** `visited[u]`는 그 재방문을 통째로 지워 오답을 만든다. 기본형에서는 우연히 맞기 때문에 습관이 굳어져 더 위험하다. `d > dist[u][s]`라는 값 비교는 상태가 몇 차원이든 그대로 성립한다.

```cpp
// ✅ 고친 코드
while (!pq.empty()) {
    auto [d, u, s] = pq.top(); pq.pop();
    if (d > dist[u][s]) continue;             // 값으로 걸러낸다(지연 삭제)
    ...
}
```

**5) 거리를 `int`로 받아 오버플로시킨다**

```cpp
// ❌ 틀린 코드
vector<int> dist(n + 1, 1e9);
...
int nd = dist[u] + w;                         // 1e5개 간선 * 1e5 가중치 = 1e10
if (nd < dist[v]) dist[v] = nd;               // int로는 담기지 않는다
```

왜: `int`는 약 21억까지다. 간선 `10^5`개에 가중치 `10^5`면 경로 합이 `10^10`이라 부호가 뒤집혀 **음수 거리**가 생기고, 그 음수가 모든 완화를 통과하며 답을 오염시킨다. 오버플로는 예외를 던지지 않으므로 "왜 답이 음수지?"라는 증상으로만 드러난다.

```cpp
// ✅ 고친 코드
const long long INF = 1e18;
vector<long long> dist(n + 1, INF);
long long nd = dist[u] + w;                   // 힙의 first도 long long 이어야 한다
if (nd < dist[v]) dist[v] = nd;
```

**6) 자기 자신까지의 거리를 0으로 초기화하지 않는다**

```cpp
// ❌ 틀린 코드
vector<vector<long long>> dist(n + 1, vector<long long>(n + 1, INF));
for (auto& [u, v, w] : edges) dist[u][v] = w;    // 대각선을 INF 로 남겨 둔다
```

왜: `dist[i][i]`가 INF면 "i를 지나 i로 돌아오는" 경유가 전부 막혀, `dist[i][k] + dist[k][i]` 같은 조합이 계산되지 않는다. 무엇보다 **음수 사이클 판정 `dist[i][i] < 0`이 영영 참이 되지 않는다.** 판정의 기준선이 0이라는 사실 자체가 대각선 초기화에서 나온다. Dijkstra에서도 `dist[start] = 0`을 빼면 힙이 곧바로 비어 전부 INF가 나온다.

```cpp
// ✅ 고친 코드
vector<vector<long long>> dist(n + 1, vector<long long>(n + 1, INF));
for (int i = 1; i <= n; i++) dist[i][i] = 0;              // 판정의 기준선
for (auto& [u, v, w] : edges)
    dist[u][v] = min(dist[u][v], (long long)w);           // 중복 간선은 최솟값
```

**7) 무방향 그래프인데 간선을 한 방향만 넣는다**

```cpp
// ❌ 틀린 코드
for (int i = 0; i < m; i++) {
    int u, v, w; cin >> u >> v >> w;
    graph[u].push_back({v, w});               // u -> v 만 등록
}
```

왜: 무방향이면 `v`에서 `u`로도 갈 수 있어야 한다. 한쪽만 넣으면 도달 가능한 정점이 INF로 남거나, 답이 실제보다 커진다. 반대로 **일방통행 문제에 양방향으로 넣으면** 없는 길이 생겨 답이 작아진다. 문제 문장에서 방향 여부를 먼저 확인하고 코드에 한 번만 반영한다.

```cpp
// ✅ 고친 코드
for (int i = 0; i < m; i++) {
    int u, v, w; cin >> u >> v >> w;
    graph[u].push_back({v, w});
    graph[v].push_back({u, w});               // 무방향이면 양쪽 모두
}
// Floyd라면  dist[u][v] = dist[v][u] = min(dist[u][v], (long long)w);
```

**8) 큰 컨테이너를 값으로 넘겨 시간 초과가 난다**

```cpp
// ❌ 틀린 코드
vector<long long> dijkstra(int n, vector<vector<pair<int,int>>> graph, int s) {
    ...                                       // 호출할 때마다 그래프 전체가 복사된다
}
for (int s = 1; s <= n; s++) dijkstra(n, graph, s);   // V번 호출 = V번 복사
```

왜: C++에서 `vector`를 값으로 받으면 원소가 전부 복사된다. 간선 `10^5`개짜리 그래프를 정점 수만큼 복사하면 알고리즘 자체는 맞아도 복사 비용만으로 시간이 날아간다. 게다가 함수 안에서 고친 내용이 호출자에게 반영되지 않아 "왜 값이 안 바뀌지?"라는 별개의 버그도 같이 생긴다.

```cpp
// ✅ 고친 코드
vector<long long> dijkstra(int n, const vector<vector<pair<int,int>>>& graph, int s) {
    ...                                       // 참조로 받으면 복사가 없다
}
// 고쳐야 하는 인자는 const 없이 참조로: void relax(vector<long long>& dist, ...)
```

**다음 챕터로**

- 여기서 만든 "인접 리스트 + 완화 + `priority_queue`" 뼈대는 최소 신장 트리(프림)에서 완화식만 `dist[u]+w`에서 `w`로 바꿔 그대로 재사용된다. "무엇을 최소화하는가"만 다르고 확정 방식은 같다.
- 상태 확장(`dist[v][s]`)은 비트마스크 DP로 이어진다. 열쇠 집합을 정수 하나로 들고 다니는 이 챕터의 습관이, 방문 집합을 정수로 들고 다니는 외판원 문제의 상태 정의와 정확히 같은 아이디어다.
