## L6. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터의 네 레슨은 사실 하나의 흐름이다. **루트를 정해 방향을 주고**(L1), 그 방향을 따라 **아래에서 위로 값을 모으고**(L2·L3), 두 정점 사이 관계를 물으면 **위로 올라가 만나는 지점**을 찾는다(L4). 아래 지도로 전체를 한 번에 훑고, 뼈대 코드·선택 기준표·체크리스트로 못 박는다.

**개념 지도**

```text
  Ch01 map : rooting turns a graph into a hierarchy

  tree  (V vertices, V-1 edges, connected, no cycle)
   |    exactly one path between any two vertices
   |
   +-- pick a root  ->  parent[] depth[] order[] size[]
   |     BFS, or DFS with an explicit stack (never plain recursion)
   |
   +-- sweep top down      depth[c] = depth[v] + 1
   +-- sweep bottom up     size[v]  = 1 + sum of size[c]
   |     order scanned backwards is the postorder-safe direction
   |
   +-- aggregate a subtree  ->  Tree DP
   |     state = (vertex, one extra bit)
   |     dp[v] is built only from dp[children of v]
   |
   +-- extremum over the whole tree  ->  diameter
   |     BFS twice, or DP on the top-2 downward paths
   |
   +-- query about a pair (u, v)  ->  LCA
         naive climb      O(H) per query, no table
         binary lifting   O(V log V) table, O(log V) per query
           |
           +-- dist(u,v) = dep[u] + dep[v] - 2*dep[L]
           +-- "does the path pass through x ?"  compare 3 LCAs
           +-- max edge on the path : same table, second array
```

문제를 만나면 아래 순서로 한 칸씩 좁힌다.

```text
  which tool for a tree query ?

  parent or depth only              -> one BFS from the root
  subtree size / sum / count        -> backward sweep over order
  best value under a constraint     -> Tree DP, 2 states per vertex
  longest path in the whole tree    -> BFS twice
  one or a few LCA questions        -> naive climb, skip the table
  10^4 .. 10^6 LCA questions        -> binary lifting table
  distance or path max, repeated    -> lifting + a parallel array
```

LCA 질의는 늘 두 단계다. 이 순서가 뒤집히면 답이 어긋난다.

```text
  LCA in two phases

  phase 1 : align depth       lift the deeper one by dep[u]-dep[v]
     dep 5   u                    dep 3   u'   v
     dep 3        v               dep 3

  phase 2 : rise together while the ancestors still differ
     up[k][u] != up[k][v]  ->  still below the LCA, lift both
     up[k][u] == up[k][v]  ->  this jump overshoots, try smaller k
     after the loop, u and v sit on two different children of the
     LCA, so the answer is up[0][u]
```

C++에서 트리 문제가 죽는 자리는 거의 항상 두 곳이다. 먼저 재도, 스택도 직접 세어 두고 시작한다.

```text
  two numbers to compute before writing code

  1) recursion depth
     chain tree, N = 200000  ->  DFS depth 200000
     default stack ~ 1 MB , one frame tens of bytes  ->  process DIES
     (no exception, no message : just an abnormal exit)
     fix : explicit stack / BFS + backward sweep over order

  2) sparse table size
     LOG must satisfy  2^LOG > N
     N = 200000 -> LOG = 18
     memory = LOG * (N+1) * 4 B ~ 14 MB   (int, not long long)
     LOG too small -> high bits of the depth gap are never applied
                   -> small tests pass, big tests fail
```

**뼈대 코드**

1) 입력 → 인접 리스트 → 반복 DFS로 부모·깊이·서브트리 크기

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, root = 1;                          // ← 루트 번호는 문제마다 바뀜
vector<vector<int>> g;
vector<int> parent_, depth_, order_, sz;

void read_tree() {
    cin >> n;
    g.assign(n + 1, {});
    for (int i = 0; i < n - 1; i++) {     // ← 간선 수·형식은 문제마다 바뀜
        int a, b; cin >> a >> b;
        g[a].push_back(b);
        g[b].push_back(a);                // 무방향이면 양쪽에 등록
    }
}

void root_tree() {
    parent_.assign(n + 1, 0);
    depth_.assign(n + 1, 0);
    sz.assign(n + 1, 1);
    order_.clear();
    order_.reserve(n);
    vector<char> seen(n + 1, 0);          // vector<bool> 대신 char
    seen[root] = 1;
    vector<int> stk;                      // 반복 DFS: 재귀 깊이와 무관
    stk.push_back(root);
    while (!stk.empty()) {
        int u = stk.back(); stk.pop_back();
        order_.push_back(u);
        for (int v : g[u]) {
            if (!seen[v]) {               // 방문 검사 = 부모 되돌아감 차단
                seen[v] = 1;
                parent_[v] = u;
                depth_[v] = depth_[u] + 1;
                stk.push_back(v);
            }
        }
    }
    for (int i = (int)order_.size() - 1; i >= 0; i--) {   // 역순 = 자식이 먼저
        int u = order_[i];
        if (parent_[u]) sz[parent_[u]] += sz[u];
    }
}
```

2) 지름 — BFS 두 번

```cpp
// 가장 먼 정점과 그 거리를 함께 돌려준다
pair<int,int> bfs_far(int src) {
    vector<int> dist(n + 1, -1);
    dist[src] = 0;
    int far = src;
    queue<int> q;
    q.push(src);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : g[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;    // ← 가중 트리면 +w, 그리고 BFS 대신 스택 DFS
                if (dist[v] > dist[far]) far = v;
                q.push(v);
            }
        }
    }
    return {far, dist[far]};
}

// main 안에서 두 번 부른다
auto [a, d1] = bfs_far(1);                // 아무 정점에서 시작해 끝점 하나 확보
auto [b, diameter] = bfs_far(a);          // 그 끝점에서 다시 재면 지름
```

3) Tree DP 골격 — 포함/미포함 두 상태

```cpp
long long tree_dp(vector<long long>& w) {
    vector<long long> dp0(n + 1, 0), dp1(n + 1, 0);   // 합은 long long
    for (int i = (int)order_.size() - 1; i >= 0; i--) {   // 자식이 먼저 확정
        int u = order_[i];
        dp1[u] += w[u];                               // ← 점화식은 문제마다 바뀜
        int p = parent_[u];
        if (p) {
            dp1[p] += dp0[u];                         // p를 고르면 자식 u는 금지
            dp0[p] += max(dp0[u], dp1[u]);            // p를 안 고르면 u는 자유
        }
    }
    return max(dp0[root], dp1[root]);
}

// 변형: 각 정점에서 아래로 뻗는 최장 경로 1위·2위 -> 지름을 DP로
long long diameter_dp(vector<vector<int>>& children) {
    vector<long long> down(n + 1, 0);
    long long best = 0;
    for (int i = (int)order_.size() - 1; i >= 0; i--) {
        int u = order_[i];
        long long t1 = 0, t2 = 0;
        for (int c : children[u]) {
            long long d = down[c] + 1;                // ← 가중 트리면 + w(u, c)
            if (d > t1) { t2 = t1; t1 = d; }
            else if (d > t2) { t2 = d; }
        }
        down[u] = t1;
        best = max(best, t1 + t2);                    // u를 최상단으로 하는 경로
    }
    return best;
}
```

4) LCA 단순 상승 — 표 없이, 질의가 적을 때

```cpp
int lca_naive(int u, int v) {
    while (depth_[u] > depth_[v]) u = parent_[u];   // 1단계: 깊은 쪽만 끌어올린다
    while (depth_[v] > depth_[u]) v = parent_[v];
    while (u != v) {                                // 2단계: 같은 높이에서 나란히
        u = parent_[u];
        v = parent_[v];
    }
    return u;                                       // 질의당 O(트리 높이)
}
```

5) LCA 희소 테이블(binary lifting) — 전처리 + 질의

```cpp
int LOG;
vector<vector<int>> up;

void build_up() {
    LOG = 1;
    while ((1 << LOG) <= n) LOG++;                  // 2^LOG > n 이면 충분
    up.assign(LOG, vector<int>(n + 1, 0));          // 루트의 부모는 0(가상 노드)
    for (int v = 1; v <= n; v++) up[0][v] = parent_[v];
    for (int k = 1; k < LOG; k++)
        for (int v = 1; v <= n; v++)
            up[k][v] = up[k - 1][up[k - 1][v]];     // 2^k칸 = 2^(k-1)칸 두 번
}                                                   // 전처리 O(V log V)

int lca(int u, int v) {
    if (depth_[u] < depth_[v]) swap(u, v);          // u를 항상 더 깊은 쪽으로
    int diff = depth_[u] - depth_[v];
    for (int k = 0; k < LOG; k++)                   // 켜진 비트마다 점프 한 번
        if ((diff >> k) & 1) u = up[k][u];
    if (u == v) return u;                           // 한쪽이 다른 쪽의 조상
    for (int k = LOG - 1; k >= 0; k--)              // 반드시 큰 k -> 작은 k 순
        if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }
    return up[0][u];                                // 질의당 O(log V)
}

int dist_uv(int u, int v) {
    return depth_[u] + depth_[v] - 2 * depth_[lca(u, v)];
}
```

6) 경로 위 최대 간선 질의 — 같은 표에 배열 하나를 나란히

```cpp
vector<vector<int>> mx;                             // wpar[v] = v와 부모를 잇는 간선

void build_max(vector<int>& wpar) {
    mx.assign(LOG, vector<int>(n + 1, 0));          // ← 최솟값을 원하면 INF로 초기화
    for (int v = 1; v <= n; v++) mx[0][v] = wpar[v];
    for (int k = 1; k < LOG; k++)
        for (int v = 1; v <= n; v++) {
            int mid = up[k - 1][v];
            mx[k][v] = max(mx[k - 1][v], mx[k - 1][mid]);   // 두 구간을 합침
        }
}

int path_max(int u, int v) {
    if (depth_[u] < depth_[v]) swap(u, v);
    int best = 0;
    int diff = depth_[u] - depth_[v];
    for (int k = 0; k < LOG; k++)
        if ((diff >> k) & 1) { best = max(best, mx[k][u]); u = up[k][u]; }
    if (u == v) return best;                        // 올리기 전에 값부터 챙긴다
    for (int k = LOG - 1; k >= 0; k--)
        if (up[k][u] != up[k][v]) {
            best = max({best, mx[k][u], mx[k][v]});
            u = up[k][u]; v = up[k][v];
        }
    return max({best, mx[0][u], mx[0][v]});         // 마지막 한 칸 두 개도 잊지 않는다
}
```

**언제 무엇을 쓰나**

질의 유형이 도구를 정한다. 특히 **단순 상승과 희소 테이블 사이의 선택**은 "질의 수 Q × 트리 높이 H"를 실제로 곱해 보고 정한다.

| 질의 유형 | 고르는 것 | 판단 기준 | 복잡도 |
| --- | --- | --- | --- |
| 부모·깊이만 알면 된다 | 루트에서 BFS 1회 | 표를 만들 이유가 없다 | 전처리 O(V), 조회 O(1) |
| 서브트리 크기·합·개수 | `order_` 역순 스윕 | 자식이 먼저 확정되는 유일한 순서 | O(V) |
| 각 정점의 최적값이 자식 값으로 정해진다 | Tree DP(상태 2개) | 서브트리와 바깥을 잇는 간선이 하나뿐 | O(V) |
| 트리 전체의 최장 경로 | BFS 두 번 | 코드가 짧고 상수가 작다 | O(V) |
| 최장 경로 + 부수 정보(경로 복원, 정점별 값) | 1위·2위 DP | 정점마다 값이 남아 재사용된다 | O(V) |
| LCA 질의가 1회 ~ 수백 회 | 단순 상승 | `Q × H`가 `10^6` 이하면 전처리가 손해 | 질의당 O(H) |
| LCA 질의가 수만 회 이상 | 희소 테이블 | `Q × H`가 `10^7`을 넘어가면 필수 | 전처리 O(V log V), 질의 O(log V) |
| 일자 트리 가능성이 있고 질의가 많다 | 희소 테이블 | H가 V에 가까워 단순 상승은 O(V·Q) | 전처리 O(V log V) |
| 두 점 사이 거리(간선 수·가중치 합) | depth + LCA 공식 | `dep[u]+dep[v]-2dep[L]` 한 줄 | 질의 O(log V) |
| 경로 위 최대·최소 간선 | 희소 테이블 + 병렬 배열 | 점프 구간마다 값을 함께 합칠 수 있다 | 질의 O(log V) |
| u가 v의 조상인가 | `lca(u,v) == u` | 깊이 맞추기 단계에서 즉시 판별된다 | 질의 O(log V) |
| 경로 u–v가 x를 지나는가 | `dist(u,x)+dist(x,v)==dist(u,v)` | 거리 세 번이면 끝, 별도 자료구조 불필요 | 질의 O(log V) |
| 모든 정점을 루트로 했을 때의 답 | 재루팅(스윕 2회) | 아래→위 한 번, 위→아래 한 번 | O(V) |
| V가 10만 이상 | 반복 DFS/BFS | 재귀는 스택에서 먼저 죽는다 | O(V) |

자료형·메모리도 같이 정해 둔다.

| 항목 | 고르는 것 | 근거 |
| --- | --- | --- |
| `parent_` / `depth_` / `up` | `int` | 정점 번호·깊이는 `10^6`을 안 넘는다 |
| 서브트리 합·DP 값 | `long long` | `10^5 × 10^9 = 10^14`로 `int`를 넘는다 |
| 방문 배열 | `vector<char>` | `vector<bool>`은 비트 압축이라 참조를 못 잡는다 |
| 희소 표 | `vector<vector<int>> up(LOG, vector<int>(n+1))` | `int`로 잡아야 `LOG=18, N=2e5`에서 14MB |
| 인접 리스트 전달 | `const vector<vector<int>>&` | 값 전달은 매 호출마다 전체 복사 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 정점 V개 트리의 간선이 왜 정확히 V-1개이고, 두 정점 사이 경로가 왜 유일한지.
- [ ] 설명할 수 있다: "루트를 정한다"는 행위가 그래프를 어떻게 계층 구조로 바꾸는지.
- [ ] 설명할 수 있다: 왜 `order_`의 역순이 "자식이 부모보다 먼저 확정되는" 순서인지.
- [ ] 설명할 수 있다: 깊이는 위에서 아래로, 크기는 아래에서 위로 계산되는 이유.
- [ ] 설명할 수 있다: 무방향 인접 리스트에서 자식과 부모를 구분하는 두 가지 방법(부모 번호 비교, 방문 배열).
- [ ] 설명할 수 있다: 재귀 DFS가 왜 위험하고(스택 오버플로가 예외 없이 프로세스를 죽인다), 반복 DFS로 어떻게 대체하는지.
- [ ] 설명할 수 있다: 지름을 BFS 두 번으로 구하는 방법이 왜 옳은지(임의 시작점의 최원점이 지름의 끝점인 이유).
- [ ] 설명할 수 있다: 왜 한 번의 DFS로 지름을 구하면 틀리는지, 반례를 하나 들어서.
- [ ] 설명할 수 있다: Tree DP의 상태를 (정점, 포함 여부)로 잡는 근거와, 서로 다른 자식이 왜 독립인지.
- [ ] 설명할 수 있다: `dp0`에서 자식을 `max(dp0, dp1)`로 받는 이유.
- [ ] 설명할 수 있다: `up[k][v] = up[k-1][up[k-1][v]]`가 성립하는 이유를 지수 법칙으로.
- [ ] 설명할 수 있다: LCA 질의에서 깊이를 먼저 맞춰야 하는 이유.
- [ ] 설명할 수 있다: 2단계에서 왜 큰 k부터 시도해야 하고, 작은 k부터 하면 무엇이 깨지는지.
- [ ] 설명할 수 있다: `LOG`를 몇으로 잡아야 하는지와 그 근거, 그리고 `log2()` 대신 정수 연산을 쓰는 이유.
- [ ] 설명할 수 있다: 질의 수 Q와 트리 높이 H를 보고 단순 상승과 희소 테이블 중 무엇을 고를지.
- [ ] 설명할 수 있다: 서브트리 합에 `long long`이 필요한 기준과, 희소 표에는 `int`로 충분한 이유.

**⚠️ 자주 하는 실수**

**1) 무방향 인접 리스트에서 부모로 되돌아간다**

```cpp
// ❌ 틀린 코드
vector<int> stk{1};
while (!stk.empty()) {
    int u = stk.back(); stk.pop_back();
    order_.push_back(u);
    for (int v : g[u]) stk.push_back(v);   // g[u]에는 자식뿐 아니라 부모도 있다
}
```

왜: 간선 `a b`를 `g[a]`와 `g[b]` 양쪽에 넣었으므로 `g[u]`를 훑으면 부모가 반드시 섞여 나온다. 부모를 다시 push하면 부모가 또 나를 push해 스택이 끝없이 자라고, `order_`에 같은 정점이 반복해 쌓여 서브트리 크기가 엉뚱하게 커진다. 결국 메모리가 터지거나 답이 크게 부푼다.

```cpp
// ✅ 고친 코드
vector<char> seen(n + 1, 0);
seen[1] = 1;
vector<int> stk{1};
while (!stk.empty()) {
    int u = stk.back(); stk.pop_back();
    order_.push_back(u);
    for (int v : g[u]) {
        if (!seen[v]) {                    // 방문 표시 하나로 부모·재방문을 함께 차단
            seen[v] = 1;
            parent_[v] = u;
            stk.push_back(v);
        }
    }
}
```

**2) 깊은 트리에서 재귀가 스택을 무너뜨린다**

```cpp
// ❌ 틀린 코드
void dfs(int u, int p) {
    for (int v : g[u])
        if (v != p) {
            dfs(v, u);
            sz[u] += sz[v];
        }
}
dfs(1, 0);          // 정점 10만 개짜리 일자 트리 -> 스택 오버플로
```

왜: 기본 스택은 보통 1MB 남짓이고 프레임 하나가 수십 바이트다. 각 정점이 자식을 하나만 갖는 사슬 트리면 깊이가 V-1이라, 알고리즘이 맞아도 호출 스택이 먼저 무너진다. C++은 예외를 던지지 않고 **프로세스가 그냥 종료**되므로 "왜 아무 출력도 없지?"라는 증상으로만 드러난다. 트리 문제의 최악 입력은 거의 항상 일자 트리다.

```cpp
// ✅ 고친 코드 — 애초에 반복 DFS + order_ 역순 스윕으로 짠다
sz.assign(n + 1, 1);
for (int i = (int)order_.size() - 1; i >= 0; i--) {
    int u = order_[i];
    if (parent_[u]) sz[parent_[u]] += sz[u];
}
```

**3) LCA에서 깊이를 맞추지 않고 함께 올린다**

```cpp
// ❌ 틀린 코드
int lca_bad(int u, int v) {
    while (u != v) {
        u = parent_[u];
        v = parent_[v];        // 깊이가 다른데 나란히 올린다
    }
    return u;
}
```

왜: 깊이가 5와 3이면 두 포인터는 항상 2칸 어긋난 채 올라간다. 운 좋게 루트에서 만나면 루트를 답으로 내놓고, 한쪽이 루트를 지나 `parent_[root] = 0`으로 빠지면 영원히 같아지지 않아 **무한 루프**가 된다(그 사이 `parent_[0]`을 계속 읽는다). 한쪽이 다른 쪽의 조상인 경우에서 특히 확실하게 틀린다.

```cpp
// ✅ 고친 코드
int lca_ok(int u, int v) {
    while (depth_[u] > depth_[v]) u = parent_[u];   // 1단계: 깊은 쪽만 끌어올린다
    while (depth_[v] > depth_[u]) v = parent_[v];
    while (u != v) {                                // 2단계: 같은 높이에서만
        u = parent_[u];
        v = parent_[v];
    }
    return u;
}
```

**4) 희소 테이블의 `LOG`를 너무 작게 잡는다**

```cpp
// ❌ 틀린 코드
const int LOG = 10;                        // 2^10 = 1024
vector<vector<int>> up(LOG, vector<int>(n + 1, 0));
// n = 200000 인 일자 트리에서 깊이 차가 1024를 넘는 순간
for (int k = 0; k < LOG; k++)
    if ((diff >> k) & 1) u = up[k][u];     // 상위 비트가 통째로 무시된다
```

왜: 깊이 맞추기는 `diff`의 켜진 비트를 하나씩 처리한다. `LOG`가 `diff`의 비트 수보다 작으면 상위 비트가 반영되지 않아 두 포인터의 깊이가 끝내 맞지 않는다. 작은 테스트는 전부 통과하고 큰 입력에서만 틀리는 전형적인 함정이다. `LOG`를 `log2(n)`으로 계산하는 것도 위험한데, 부동소수 오차로 `log2(8)`이 `2.9999...`가 되어 1이 모자랄 수 있다.

```cpp
// ✅ 고친 코드 — 정수 연산으로 2^LOG > n 을 보장한다
int LOG = 1;
while ((1 << LOG) <= n) LOG++;             // n = 200000 이면 LOG = 18
vector<vector<int>> up(LOG, vector<int>(n + 1, 0));
// __lg(n) + 1 도 같은 값이며 부동소수를 쓰지 않는다
```

**5) 이진 리프팅 2단계를 작은 k부터 시도한다**

```cpp
// ❌ 틀린 코드
for (int k = 0; k < LOG; k++)              // 0, 1, 2, ... 오름차순
    if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }
return up[0][u];
```

왜: 작은 점프는 "아직 다르다"가 계속 참이라 매번 올라가게 되고, 그러다 LCA를 지나쳐 버린다. 한 번 지나치면 그 위는 두 조상이 같아 더 이상 올라가지 않으므로, 실제 LCA보다 위쪽 정점이 답으로 나온다. 큰 k부터 밟아야 "남은 거리"가 항상 직전 점프보다 작게 유지되어 초과가 생기지 않는다.

```cpp
// ✅ 고친 코드
for (int k = LOG - 1; k >= 0; k--)         // 큰 점프부터 내림차순
    if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }
return up[0][u];                           // 멈춘 지점의 바로 위가 LCA
```

**6) 지름을 한 번의 BFS로 구하려 한다**

```cpp
// ❌ 틀린 코드
auto [far, d] = bfs_far(1);                // 정점 1에서 가장 먼 거리를 지름이라 부름
cout << d << '\n';
```

왜: "루트에서 가장 먼 거리"는 지름이 아니라 트리의 높이다. 정점 1이 지름 경로의 한가운데에 있으면 양쪽 절반 중 한쪽만 재게 된다. 예를 들어 1을 중심으로 길이 3짜리 가지가 두 개 뻗은 트리는 높이가 3이지만 지름은 6이다.

```cpp
// ✅ 고친 코드
auto [a, d1] = bfs_far(1);                 // 1단계: 지름의 끝점 하나를 확보
auto [b, d2] = bfs_far(a);                 // 2단계: 그 끝점에서 반대쪽 끝까지
cout << d2 << '\n';                        // BFS 두 번, 전체 O(V)
```

**7) 서브트리 스윕을 `order_` 정순으로 돈다**

```cpp
// ❌ 틀린 코드
sz.assign(n + 1, 1);
for (int u : order_) {                     // 방문 순서 = 부모가 먼저 나오는 순서
    if (parent_[u]) sz[parent_[u]] += sz[u];
}
```

왜: `order_`는 부모가 자식보다 앞에 오는 순서다. 부모에 더하는 시점에 자식의 `sz`가 아직 1(초기값)이라, 손자 이하가 전혀 반영되지 않는다. 깊이 2 이하 트리에서는 우연히 맞아떨어져 통과하기도 해 발견이 늦다.

```cpp
// ✅ 고친 코드
sz.assign(n + 1, 1);
for (int i = (int)order_.size() - 1; i >= 0; i--) {   // 역순 = 자식이 부모보다 먼저
    int u = order_[i];
    if (parent_[u]) sz[parent_[u]] += sz[u];
}
// 검산: sz[root] == n 이면 스윕이 맞은 것
```

**8) 부호 없는 `size()`로 역순 루프를 돈다**

```cpp
// ❌ 틀린 코드
for (size_t i = order_.size() - 1; i >= 0; i--) {     // 두 군데가 동시에 틀렸다
    int u = order_[i];
    if (parent_[u]) sz[parent_[u]] += sz[u];
}
```

왜: `size()`는 부호 없는 `size_t`다. 첫째, `order_`가 비면 `size() - 1`이 0이 아니라 **거대한 양수**로 감싸여 곧바로 범위 밖을 읽는다. 둘째, `size_t`는 음수가 될 수 없으므로 `i >= 0`이 **항상 참**이고, `i`가 0에서 한 번 더 줄면 최댓값으로 돌아가 무한 루프가 된다. 컴파일러는 보통 경고만 내고 넘어간다.

```cpp
// ✅ 고친 코드 — 먼저 int로 캐스팅한 뒤 내려간다
for (int i = (int)order_.size() - 1; i >= 0; i--) {
    int u = order_[i];
    if (parent_[u]) sz[parent_[u]] += sz[u];
}
// 역방향 반복자도 안전하다: for (auto it = order_.rbegin(); it != order_.rend(); ++it)
```

**다음 챕터로**

- 여기서 만든 "인접 리스트 + 방문 표시 + 반복 순회" 뼈대는 다음 챕터의 MST에서 그대로 쓰인다. MST는 결국 "가중치 그래프에서 트리 하나를 뽑는" 작업이라, 뽑고 난 뒤의 자료구조는 이 챕터가 다루던 바로 그 트리다.
- 특히 6번 뼈대(경로 위 최대 간선)는 "MST 위의 두 정점 경로에서 가장 비싼 간선"을 묻는 문제로 바로 이어진다. 최소 병목 경로·차선 MST가 그 형태다.
