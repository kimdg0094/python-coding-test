## L7. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

Ch9에서 배운 것을 한 장으로 묶고, 문제를 만나면 바로 꺼내 쓸 수 있는 뼈대와 함정 목록으로 정리한다.

**개념 지도**

```text
                    graph = (V, E)
                          |
              +-----------+-----------+
        adjacency matrix        adjacency list
        O(V^2) space            O(V+E) space
        edge query O(1)         neighbor scan O(deg)
              +-----------+-----------+
                          |  traversal
              +-----------+-----------+
        DFS (stack/recursion)     BFS (queue)
        go deep, backtrack        expand layer by layer
              |                       |
    components, path, cycle     shortest dist (unweighted)
              |                       |
              +-----------+-----------+
                          |
              grid : cell is a vertex, 4-dir is an edge
                          |
              +-----------+-----------+
        multi-source BFS         all weights = w
        (push every source)      dist x w  -> Ch10 dijkstra
```

한 줄로 요약하면 이렇다. **저장 방식(행렬/리스트)을 고르고 -> 탐색 방식(DFS/BFS)을 고른다.** 거리가 필요 없으면 DFS, 필요하면 BFS다. 격자는 그래프를 따로 만들지 않고 좌표 그대로 쓰는 특수 케이스이고, 간선 가중치가 서로 달라지는 순간 BFS를 버리고 Ch10으로 넘어간다.

C++에서는 여기에 "무엇을 어떤 통에 담는가"가 하나 더 붙는다. 세 통의 차이가 곧 세 알고리즘의 차이다.

```text
  same skeleton, different container

  DFS   stack<int>        LIFO   take the newest      -> goes deep
  BFS   queue<int>        FIFO   take the oldest      -> goes wide
  Ch10  priority_queue    min    take the cheapest    -> needs greater<>

  stack : top() then pop()      # pop() returns nothing
  queue : front() then pop()    # pop() returns nothing
```

**뼈대 코드**

(1) 입력 -> 인접 리스트

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);                     // 입출력이 많으면 필수

    int N, M;
    cin >> N >> M;
    vector<vector<int>> adj(N + 1);       // 정점 번호가 0-based면 (N)
    for (int i = 0; i < M; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);              // 방향 그래프면 이 줄을 지운다
    }
    // for (int i = 1; i <= N; i++) sort(adj[i].begin(), adj[i].end());
    //   ^ 이웃을 번호순으로 방문해야 할 때만
    return 0;
}
```

(2) DFS — 재귀와 명시적 스택

```cpp
vector<vector<int>> adj;
vector<bool> visited;

void dfs(int u) {                         // 재귀 버전: 짧지만 깊이 제한이 있다
    visited[u] = true;
    for (int v : adj[u])                  // 여기에 문제별 처리를 넣는다
        if (!visited[v]) dfs(v);
}

void dfs_stack(int s) {                   // 스택 버전: 깊이 걱정이 없다
    stack<int> st;
    st.push(s);
    visited[s] = true;
    while (!st.empty()) {
        int u = st.top(); st.pop();       // top() 으로 읽고 pop() 으로 버린다
        for (int v : adj[u])
            if (!visited[v]) {
                visited[v] = true;        // push 하는 순간 표시
                st.push(v);
            }
    }
}
```

(3) BFS — 거리와 경로 복원

```cpp
pair<int, vector<int>> bfs(const vector<vector<int>>& adj, int N,
                           int start, int goal) {
    vector<int> dist(N + 1, -1), par(N + 1, -1);   // par 은 경로 복원용 부모
    queue<int> q;
    dist[start] = 0;
    q.push(start);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u])
            if (dist[v] == -1) {          // 미방문 = 아직 거리 없음
                dist[v] = dist[u] + 1;
                par[v] = u;
                q.push(v);
            }
    }
    if (dist[goal] == -1) return {-1, {}};
    vector<int> path;
    for (int cur = goal; cur != -1; cur = par[cur])   // 거꾸로 따라 올라간다
        path.push_back(cur);
    reverse(path.begin(), path.end());
    return {dist[goal], path};
}
```

(4) 격자 BFS

```cpp
const int dr[4] = {1, -1, 0, 0};          // 8방향이면 대각선 4개를 추가
const int dc[4] = {0, 0, 1, -1};

vector<vector<int>> grid_bfs(const vector<string>& grid, int H, int W,
                             int sr, int sc) {
    vector<vector<int>> dist(H, vector<int>(W, -1));
    queue<pair<int,int>> q;
    dist[sr][sc] = 0;
    q.push({sr, sc});
    while (!q.empty()) {
        auto [r, c] = q.front(); q.pop();
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= H || nc < 0 || nc >= W) continue;  // 경계 먼저
            if (dist[nr][nc] != -1) continue;                      // 이미 방문
            if (grid[nr][nc] == '0') continue;   // 벽 판정은 문제마다 바뀜
            dist[nr][nc] = dist[r][c] + 1;
            q.push({nr, nc});
        }
    }
    return dist;
}
```

(5) 연결 요소 세기 · 다중 시작 BFS

```cpp
int count_components(const vector<vector<int>>& adj, int N) {
    vector<bool> visited(N + 1, false);
    int cnt = 0;
    for (int s = 1; s <= N; s++) {        // 0-based면 0..N-1
        if (visited[s]) continue;
        cnt++;
        visited[s] = true;
        queue<int> q;
        q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u])
                if (!visited[v]) { visited[v] = true; q.push(v); }
        }
    }
    return cnt;
}

// 다중 시작 BFS: 시작점을 전부 dist 0 으로 두고 한꺼번에 큐에 넣는다
queue<int> q;
for (int v : sources) {                   // 시작점 목록은 문제마다 바뀜
    dist[v] = 0;
    q.push(v);
}
// 이후 while 루프는 일반 BFS와 완전히 같다
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 정점이 적고(대략 `V <= 2000`) "두 점이 이어졌나"를 자주 묻는다 | 인접행렬 | 칸 하나만 보면 끝 | 공간 `O(V^2)`, 질의 `O(1)` |
| 간선이 정점 수의 몇 배 수준(희소)이고 탐색을 돌린다 | 인접리스트 | 실제 있는 간선만 저장 | 공간 `O(V+E)`, 탐색 `O(V+E)` |
| 연결 요소 개수, 경로 존재 여부, 사이클 유무 | DFS | 거리는 필요 없고 도달만 보면 된다 | `O(V+E)` |
| 최소 이동 횟수, 최단 간선 수, 층별 처리 | BFS | 처음 도달한 순간이 곧 최단 | `O(V+E)` |
| 격자에서 최단 이동 | 격자 BFS | 칸=정점, 한 칸 이동=비용 1 | `O(H*W)` |
| 여러 출발점에서 동시에 번진다 | 다중 시작 BFS | 시작점을 한꺼번에 큐에 넣으면 끝 | `O(V+E)` |
| 간선 가중치가 전부 같은 상수 `w` | BFS 후 `× w` | 간선 수 최소 = 비용 최소 | `O(V+E)` |
| 정점이 수만 개이고 깊이가 깊어질 수 있다 | 스택 DFS 또는 BFS | 재귀 스택 오버플로를 아예 피한다 | `O(V+E)` |
| 간선 가중치가 서로 다르다 | Ch10 Dijkstra | BFS의 층 논증이 깨진다 | `O(E log V)` |

C++ 자료구조 선택은 이 표로 못 박는다.

| 담을 것 | 고르는 것 | 이유 |
| --- | --- | --- |
| 인접 리스트 | `vector<vector<int>>` | 크기 가변, 순회가 캐시 친화적 |
| 가중치 있는 인접 리스트 | `vector<vector<pair<int,int>>>` | `{이웃, 가중치}` 한 쌍으로 |
| 방문 표시 | `vector<bool>` 또는 `vector<char>` | `bool`은 비트 압축이라 메모리가 8배 작다 |
| 거리 | `vector<int>`(초기값 `-1`) | `-1`이 미방문 표시와 거리를 겸한다 |
| BFS 큐 | `queue<int>` | 앞뒤 연산이 `O(1)` |
| DFS 스택 | `stack<int>` | 재귀 깊이 제한을 피한다 |
| 격자 좌표 | `pair<int,int>` 또는 `r * W + c` | 후자는 1차원 인덱스라 더 빠르다 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 정점·간선·차수·경로·사이클·연결 요소가 각각 무엇인지.
- [ ] 설명할 수 있다: 무방향 그래프에서 차수의 합이 왜 간선 수의 두 배인지.
- [ ] 설명할 수 있다: 인접행렬과 인접리스트의 공간·질의·순회 복잡도가 왜 그렇게 되는지.
- [ ] 설명할 수 있다: 어떤 상황에서 인접행렬이 인접리스트보다 유리한지, 그 기준이 무엇인지.
- [ ] 설명할 수 있다: DFS가 "깊이 들어갔다 되돌아온다"는 것이 스택에서 어떤 모양으로 나타나는지.
- [ ] 설명할 수 있다: 재귀 DFS의 스택 깊이가 왜 위험한지, 어느 정도 깊이부터 문제가 되는지.
- [ ] 설명할 수 있다: BFS가 왜 가중치 없는 그래프의 최단 거리를 주는지(큐 안의 거리가 두 종류뿐이라는 층 논증).
- [ ] 설명할 수 있다: 같은 그래프를 DFS와 BFS로 훑었을 때 방문 순서가 왜 달라지는지.
- [ ] 설명할 수 있다: 방문 표시를 큐에 넣을 때 해야 하는 이유와, 꺼낼 때 하면 무엇이 깨지는지.
- [ ] 설명할 수 있다: 탐색의 복잡도 `O(V + E)`에서 `V`와 `E`가 각각 어디서 나온 항인지.
- [ ] 설명할 수 있다: 격자 문제를 그래프로 바꾸는 관점(칸=정점, 상하좌우 인접=간선).
- [ ] 설명할 수 있다: 다중 시작 BFS가 시작점마다 따로 돌리는 것보다 왜 빠른지.
- [ ] 설명할 수 있다: 간선 가중치가 모두 같을 때 BFS로 충분한 이유와, 달라지는 순간 왜 틀리는지.
- [ ] 설명할 수 있다: BFS로 거리뿐 아니라 실제 경로를 복원하는 방법(부모 배열).
- [ ] 설명할 수 있다: `stack`·`queue`의 `pop()`이 값을 반환하지 않는다는 것과, 그래서 코드가 두 줄이 되는 이유.

**⚠️ 자주 하는 실수**

(1) 무방향 그래프인데 한 방향만 넣는다

```cpp
// ❌ 틀린 코드
for (int i = 0; i < M; i++) {
    int u, v; cin >> u >> v;
    adj[u].push_back(v);          // v -> u 가 없다
}
```

왜: 무방향 간선 하나는 "양쪽으로 갈 수 있다"는 뜻이라 두 리스트에 모두 들어가야 한다. 한쪽만 넣으면 `v`에서 출발한 탐색이 `u`를 영원히 못 찾아, 연결 요소가 실제보다 많이 세어지거나 거리가 `-1`로 남는다.

```cpp
// ✅ 고친 코드
for (int i = 0; i < M; i++) {
    int u, v; cin >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);          // 방향 그래프면 이 줄만 지운다
}
```

(2) 방문 표시를 큐에서 꺼낼 때 한다

```cpp
// ❌ 틀린 코드
queue<int> q;
q.push(start);
while (!q.empty()) {
    int u = q.front(); q.pop();
    visited[u] = true;            // 꺼낼 때 표시
    for (int v : adj[u])
        if (!visited[v]) q.push(v);   // 같은 정점이 여러 번 들어간다
}
```

왜: `u`를 꺼내 이웃 `v`를 넣은 뒤, 아직 큐에 남아 있던 다른 정점도 같은 `v`를 넣는다. `v`가 큐에 중복으로 쌓여 큐 길이가 최악 `O(E)`까지 부풀고, 두 번째로 꺼낸 `v`가 거리를 더 큰 값으로 덮어써 최단성이 깨진다.

```cpp
// ✅ 고친 코드
queue<int> q;
q.push(start);
visited[start] = true;
while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : adj[u])
        if (!visited[v]) {
            visited[v] = true;    // push 하는 순간 표시
            q.push(v);
        }
}
```

(3) 재귀 DFS가 스택 오버플로로 죽는다

```cpp
// ❌ 틀린 코드
void dfs(int u) {                 // N = 100000, 그래프가 한 줄 사슬이면
    visited[u] = true;            // 재귀 깊이가 100000 까지 간다
    for (int v : adj[u])
        if (!visited[v]) dfs(v);  // 스택 오버플로 -> 프로그램이 그냥 죽는다
}
```

왜: C++의 기본 스택은 보통 1MB 남짓이다. 프레임 하나가 수십 바이트라 해도 깊이 수만~십수만이면 한계를 넘는다. 이때는 예외도 오류 메시지도 없이 프로세스가 종료돼, 채점 결과에는 "런타임 에러"만 남고 원인을 알기 어렵다.

```cpp
// ✅ 고친 코드
void dfs_stack(int s) {           // 명시적 스택으로 바꾼다
    stack<int> st;
    st.push(s);
    visited[s] = true;
    while (!st.empty()) {
        int u = st.top(); st.pop();
        for (int v : adj[u])
            if (!visited[v]) { visited[v] = true; st.push(v); }
    }
}
```

(4) `pop()`이 값을 돌려준다고 생각한다

```cpp
// ❌ 틀린 코드
while (!q.empty()) {
    int u = q.pop();              // 컴파일 오류: pop() 은 void 를 반환한다
    // ...
}

int& u = q.front();               // 참조를 받아 두고
q.pop();                          // 지운 뒤에 u 를 쓰면 이미 없는 자리다
```

왜: `queue`와 `stack`의 `pop()`은 반환값이 없다(`void`). 값을 얻으려면 `front()`/`top()`을 먼저 부른다. 그런데 이 둘은 **참조**를 돌려주므로 `pop()` 이후에는 그 참조가 가리키던 자리가 사라진다. 반드시 값으로 복사해 둔 뒤에 `pop()`한다.

```cpp
// ✅ 고친 코드
while (!q.empty()) {
    int u = q.front();            // 값으로 복사
    q.pop();                      // 그 다음에 버린다
    // ...
}
```

(5) 격자에서 경계 검사를 나중에 한다

```cpp
// ❌ 틀린 코드
int nr = r + dr[d], nc = c + dc[d];
if (grid[nr][nc] == '1' && nr >= 0 && nr < H) {   // 배열 접근이 먼저다
    // ...
}
```

왜: `&&`는 왼쪽부터 평가한다. `nr`이 `-1`이면 `grid[-1]`을 **먼저** 읽어 범위 밖 메모리에 접근한다. 예외가 나지 않고 우연히 통과하기도 해서, 큰 입력에서만 결과가 달라지는 형태로 나타난다.

```cpp
// ✅ 고친 코드
int nr = r + dr[d], nc = c + dc[d];
if (nr < 0 || nr >= H || nc < 0 || nc >= W) continue;   // 경계를 맨 앞에
if (grid[nr][nc] != '1') continue;
```

(6) 인접 리스트를 값으로 넘긴다

```cpp
// ❌ 틀린 코드
void dfs(vector<vector<int>> adj, int u) {   // 호출마다 그래프 전체를 복사
    // ...
    dfs(adj, v);                             // 재귀 호출마다 또 복사
}
```

왜: C++의 함수 인자는 기본이 **값 복사**다. 정점 10만 개짜리 인접 리스트를 재귀 호출마다 통째로 복사하면 시간과 메모리가 폭발한다. 알고리즘은 `O(V+E)`인데 실제로는 그 몇만 배가 걸려 시간 초과가 난다.

```cpp
// ✅ 고친 코드
void dfs(const vector<vector<int>>& adj, int u) {   // 참조로 받는다
    // ...
    dfs(adj, v);
}
// 또는 adj 를 전역으로 두어 인자에서 아예 뺀다
```

(7) 시작점의 거리를 초기화하지 않는다

```cpp
// ❌ 틀린 코드
vector<int> dist(N + 1, -1);
queue<int> q;
q.push(start);                    // dist[start] 가 -1 로 남아 있다
while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : adj[u])
        if (dist[v] == -1)
            dist[v] = dist[u] + 1;   // -1 + 1 = 0 부터 시작한다
}
```

왜: `dist[start]`가 `-1`이면 "미방문"으로 취급돼 시작점이 다시 큐에 들어갈 수 있고, 거리 계산도 한 칸씩 밀린다. `-1`은 미방문 표시와 거리 저장을 겸하고 있으므로 시작점만은 반드시 `0`으로 못 박아야 한다.

```cpp
// ✅ 고친 코드
vector<int> dist(N + 1, -1);
dist[start] = 0;                  // 큐에 넣기 전에 확정
queue<int> q;
q.push(start);
```

(8) 출력이 많은데 `endl`을 쓴다

```cpp
// ❌ 틀린 코드
for (int i = 1; i <= N; i++)
    cout << dist[i] << endl;      // 매 줄마다 버퍼를 강제로 비운다
```

왜: `endl`은 줄바꿈에 더해 **출력 버퍼 비우기(flush)**까지 한다. 10만 줄을 출력하면 10만 번 디스크/파이프에 밀어내느라 눈에 띄게 느려져 시간 초과가 난다. 줄바꿈만 필요하면 `'\n'`으로 충분하다.

```cpp
// ✅ 고친 코드
ios_base::sync_with_stdio(false);
cin.tie(nullptr);                 // main 첫 줄에 두는 정석
for (int i = 1; i <= N; i++)
    cout << dist[i] << '\n';
```

**다음 챕터로**

- Ch9에서는 간선의 비용이 전부 같다고 보고 "간선 수"만 셌다. Ch10은 간선마다 비용이 다른 세계로 넘어가, 큐 대신 **우선순위 큐**로 "지금 가장 가까운 정점"을 꺼내는 Dijkstra를 배운다.
- BFS의 층 논증이 왜 무너지는지를 이해했다면, Dijkstra가 왜 "확정" 개념을 따로 두는지, 그리고 왜 음수 간선에서 깨지는지가 자연스럽게 이어진다.
- 여기서 익힌 인접 리스트·`visited`·`dist` 배열은 Ch10의 모든 알고리즘에서 그대로 재사용된다. 달라지는 것은 `queue<int>`가 `priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>>`로 바뀐다는 점뿐이다.
