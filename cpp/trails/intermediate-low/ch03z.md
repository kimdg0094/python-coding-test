## L3. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 레슨은 Ch3에서 배운 DFS를 한 장으로 묶고, 문제를 만났을 때 바로 꺼내 쓸 수 있는 뼈대와 판단 기준을 정리한다. 새 개념은 없다. 다만 C++에서는 재귀 DFS가 **OS 스택** 위에서 돈다는 사실 하나가 설계를 바꾼다. 깊이가 수십만을 넘길 가능성이 조금이라도 있으면 처음부터 `std::stack` 반복판으로 짜는 것이 안전하다.

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

재귀로 갈지 반복으로 갈지는 깊이가 정한다. 이 표를 기준으로 고른다.

```text
 recursion or explicit stack ?

   frame size ~ 48 B   (a few locals + return address + saved registers)
   OS stack            1 MB (Windows)  ..  8 MB (Linux)
   -> safe depth       roughly 20k .. 170k

   V or R*C  <= 10^4        recursion is fine
   V or R*C  ~  10^5        risky : a snake-shaped input reaches depth V
   V or R*C  >= 10^6        use std::stack : the state lives on the heap

   passing a container BY VALUE into the recursion multiplies the frame
   size and can overflow the stack at depth 10^3 already.
```

**뼈대 코드**

```cpp
// (1) 그래프 DFS — 재귀판과 반복(명시적 스택)판
#include <bits/stdc++.h>
using namespace std;

int V;
vector<vector<int>> graph;          // graph.assign(V + 1, {}) 로 1-indexed 확보
vector<char> visited;               // vector<bool> 대신 char: 참조·주소를 얻을 수 있다

void dfs(int cur) {
    visited[cur] = 1;               // 들어오자마자 표시 (규칙 1)
    // 여기서 방문 순서 기록·카운트 등     // <- 문제마다 바뀜
    for (int nxt : graph[cur])      // 참조로 순회 : 인접리스트를 복사하지 않는다
        if (!visited[nxt]) dfs(nxt);
}

void dfs_iter(int start) {          // 깊이가 수십만을 넘길 위험이 있으면 이쪽
    stack<int> st;
    st.push(start);
    visited[start] = 1;             // push 시점에 표시 (중복 push 방지)
    while (!st.empty()) {
        int cur = st.top(); st.pop();
        for (int nxt : graph[cur]) {
            if (visited[nxt]) continue;
            visited[nxt] = 1;
            st.push(nxt);
        }
    }
}
```

```cpp
// (2) 격자 DFS — 이동 조건만 갈아 끼우면 대부분의 격자 문제가 된다
int N, M;
vector<vector<int>> grid;
vector<vector<char>> vis2d;

const int dr[4] = {-1, 1, 0, 0};
const int dc[4] = {0, 0, -1, 1};    // 8방향이면 여기에 4개 추가 // <- 문제마다 바뀜

void dfs_grid(int r, int c) {
    vis2d[r][c] = 1;
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;   // 범위 검사가 항상 먼저
        if (vis2d[nr][nc]) continue;
        if (grid[nr][nc] != 1) continue;      // 이동 가능 조건 // <- 문제마다 바뀜
        dfs_grid(nr, nc);
    }
}
```

`N`과 `M`을 `int`로 따로 받아 둔 것에 이유가 있다. `nr < grid.size()`처럼 `size()`와 직접 비교하면 `size()`가 부호 없는 타입이라 `nr`이 -1일 때 거대한 양수로 변환되어 조건이 참이 되고, 그대로 범위 밖을 읽는다.

```cpp
// (3) 연결 요소 세기 / 각 요소의 크기
int area;                            // dfs_grid 안에서 area++ 하도록 고쳐 쓴다

int count_components() {
    int cnt = 0, best = 0;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            if (grid[i][j] == 1 && !vis2d[i][j]) {   // 새 덩어리의 첫 칸
                cnt++;
                area = 0;
                dfs_grid(i, j);
                best = max(best, area);
            }
        }
    }
    return cnt;
}
// 그래프판: for (int s = 1; s <= V; s++) if (!visited[s]) { cnt++; dfs(s); }
```

```cpp
// (4) 백트래킹 DFS — 모든 경로/조합을 세거나 나열할 때만
vector<int> path;
long long cnt_paths = 0;             // 경로 수는 지수라 int 로는 금방 넘친다

void dfs_path(int cur, int goal) {
    if (cur == goal) {               // 종료 조건 // <- 문제마다 바뀜
        cnt_paths++;
        return;
    }
    for (int nxt : graph[cur]) {
        if (visited[nxt]) continue;
        visited[nxt] = 1;
        path.push_back(nxt);
        dfs_path(nxt, goal);
        path.pop_back();
        visited[nxt] = 0;            // 되돌리기 — 이 줄이 (1)과의 유일한 차이
    }
}
```

```cpp
// (5) 사이클 판정 — 방향 그래프는 3색, 무방향은 부모 비교
vector<int> state;                   // 0=미방문, 1=현재 경로 위, 2=완료

bool dfs_directed(int cur) {
    state[cur] = 1;
    for (int nxt : graph[cur]) {
        if (state[nxt] == 1) return true;                  // 현재 경로로 되돌아감 = 사이클
        if (state[nxt] == 0 && dfs_directed(nxt)) return true;
    }
    state[cur] = 2;
    return false;
}

bool dfs_undirected(int cur, int parent) {
    visited[cur] = 1;
    for (int nxt : graph[cur]) {
        if (!visited[nxt]) {
            if (dfs_undirected(nxt, cur)) return true;
        } else if (nxt != parent) {                        // 부모가 아닌 방문 정점 = 사이클
            return true;
        }
    }
    return false;
}
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 도달 가능한가 / 연결되어 있는가 | DFS(재귀 또는 `std::stack`) | 방문만 하면 되고 순서는 답에 영향이 없다 | O(V+E) |
| 덩어리 개수·크기 | 미방문 시작점마다 DFS | 시작 횟수 = 요소 수, 방문 칸 수 = 크기 | O(V+E) |
| 격자 영역 칠하기·번호 매기기 | 격자 DFS(플러드 필) | 이동 조건만 갈아 끼우면 같은 뼈대 | O(N·M) |
| 재귀 깊이가 수만 이상일 위험 | 명시적 `std::stack` DFS | 상태가 힙에 쌓여 OS 스택 한계와 무관해진다 | O(V+E) |
| 그래프·격자를 여러 함수가 함께 봐야 함 | 전역 또는 `const ...&` 참조 | 값 전달은 호출마다 전체 복사 + 프레임 폭증 | 복사 비용 0 |
| 모든 경로 나열·경로 개수 | 백트래킹 DFS(표시 복원) | 다른 경로가 같은 정점을 다시 써야 한다 | 경로 수에 비례(지수) |
| 경로 개수가 수십억을 넘을 수 있음 | 카운터를 `long long` | `int`는 약 21억에서 조용히 넘친다 | 같음 |
| 방향 그래프 사이클 판정 | 3색 DFS | "현재 경로 위"와 "완료"를 구분해야 오판이 없다 | O(V+E) |
| 무방향 그래프 사이클 판정 | 부모 비교 DFS | 부모로 되짚는 간선만 예외 처리하면 된다 | O(V+E) |
| 선후 관계를 만족하는 순서 | 후위 기록 + `reverse`(위상 정렬) | 자식을 다 마친 뒤 기록하므로 앞→뒤가 보장된다 | O(V+E) |
| 서브트리 값 누적 | 반환값 있는 후위 DFS | 자식 결과를 받아 자기 값을 확정한다 | O(V) |
| 방문 배열에 참조·주소가 필요함 | `vector<char>` / `vector<vector<char>>` | `vector<bool>`은 비트 특수화라 참조를 못 얻는다 | 같음 |
| **간선 비용이 같은 최단 거리** | **BFS (Ch4)** | DFS의 "처음 도달"은 최단이 아니다 | O(V+E) |
| 좌표에 상태가 붙는 최단 | 상태 BFS (Ch4) | 층 구조가 있어야 최단이 보장된다 | O(V × 상태 수) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: DFS의 "되돌아오기"가 코드의 어느 부분에서 일어나는지(= `return`과 콜스택).
- [ ] 설명할 수 있다: 방문 표시를 함수 진입 즉시 해야 하는 이유와, 미루면 무엇이 터지는지.
- [ ] 설명할 수 있다: 재귀 DFS와 명시적 스택 DFS가 같은 순회를 하는데도 방문 순서가 달라지는 이유(스택은 나중에 넣은 것을 먼저 꺼낸다).
- [ ] 설명할 수 있다: 시간복잡도가 O(V+E)인 근거를 "호출 V번 + 인접리스트 총 순회 2E"로 세는 과정.
- [ ] 설명할 수 있다: 연결 요소 개수가 왜 "DFS 시작 횟수"와 같은지.
- [ ] 설명할 수 있다: 격자 DFS에서 범위 검사를 값 읽기보다 먼저 해야 하는 이유(범위 밖 접근은 예외가 아니라 미정의 동작이다).
- [ ] 설명할 수 있다: `int`와 `size()`를 섞어 비교하면 왜 음수가 조건을 거꾸로 만드는지.
- [ ] 설명할 수 있다: 순회용 DFS는 `visited`를 켜 두고, 백트래킹 DFS는 되돌리는 이유.
- [ ] 설명할 수 있다: C++ 재귀 깊이의 한계가 어디서 오는지(OS 스택 크기와 프레임 크기), 그리고 그것이 예외가 아니라 강제 종료로 나타나는 이유.
- [ ] 설명할 수 있다: 재귀 함수에 그래프나 격자를 값으로 넘기면 시간과 스택 양쪽에서 무슨 일이 벌어지는지.
- [ ] 설명할 수 있다: 방향 그래프 사이클 판정에 왜 2색이 아니라 3색이 필요한지.
- [ ] 설명할 수 있다: 무방향 그래프에서 부모를 예외로 두지 않으면 어떤 그래프가 오판되는지.
- [ ] 설명할 수 있다: 위상 정렬에서 "후위 기록의 역순"이 왜 모든 간선의 방향을 지키는지.
- [ ] 설명할 수 있다: 트리 DFS에서 `visited` 대신 `parent`만으로 충분한 이유.
- [ ] 설명할 수 있다: DFS로 최단거리를 구하려면 왜 모든 경로를 봐야 하고, 그래서 왜 BFS를 쓰는지.
- [ ] 설명할 수 있다: 재귀 깊이가 최악에 V가 되는 입력의 모양과, 그때 무엇으로 바꿔야 하는지.

**⚠️ 자주 하는 실수**

1. **방문 표시를 안 하거나 늦게 한다**

   ```cpp
   // ❌ 틀린 코드
   void dfs(int cur) {
       for (int nxt : graph[cur]) {
           if (!visited[nxt]) {
               visited[nxt] = 1;      // 표시가 '다음 노드'에만 찍힌다
               dfs(nxt);
           }
       }
   }
   dfs(start);                        // 시작 노드는 끝내 표시되지 않는다
   ```

   왜: 시작 노드가 미표시라 이웃이 다시 시작 노드로 들어오고, 무방향 그래프에서는 그대로 무한 재귀가 된다. 파이썬이라면 `RecursionError`로 멈추지만 C++은 스택 오버플로로 프로세스가 통째로 죽어 단서조차 남지 않는다.

   ```cpp
   // ✅ 고친 코드
   void dfs(int cur) {
       visited[cur] = 1;              // 들어오자마자, 한 곳에서만
       for (int nxt : graph[cur])
           if (!visited[nxt]) dfs(nxt);
   }
   dfs(start);                        // 시작 노드도 진입하며 자동 표시된다
   ```

2. **재귀 깊이가 OS 스택을 넘긴다**

   ```cpp
   // ❌ 틀린 코드
   void dfs(int r, int c) {
       vis2d[r][c] = 1;
       // ... 네 방향 재귀 ...
   }
   dfs(0, 0);      // 1000x1000 뱀 모양 격자 -> 깊이 10^6 -> 스택 오버플로
   ```

   왜: C++ 재귀는 OS가 준 스택(보통 1MB~8MB)에 프레임을 쌓는다. 프레임 하나가 48바이트만 되어도 깊이 100만이면 48MB라 한참 모자란다. 파이썬의 `setrecursionlimit` 같은 조절 손잡이가 없고, 넘기는 순간 예외 없이 강제 종료된다.

   ```cpp
   // ✅ 고친 코드
   void dfs_iter(int sr, int sc) {          // 상태를 힙(std::stack)에 쌓는다
       stack<pair<int,int>> st;
       st.push({sr, sc});
       vis2d[sr][sc] = 1;                   // push 시점에 표시
       while (!st.empty()) {
           auto [r, c] = st.top(); st.pop();
           for (int d = 0; d < 4; d++) {
               int nr = r + dr[d], nc = c + dc[d];
               if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;
               if (vis2d[nr][nc] || grid[nr][nc] != 1) continue;
               vis2d[nr][nc] = 1;
               st.push({nr, nc});
           }
       }
   }
   ```

3. **격자에서 범위 검사를 빠뜨린다**

   ```cpp
   // ❌ 틀린 코드
   int nr = r + dr[d], nc = c + dc[d];
   if (grid[nr][nc] == 1 && !vis2d[nr][nc])   // 검사 없이 먼저 읽는다
       dfs_grid(nr, nc);
   ```

   왜: `nr`이 -1이면 `grid[-1]`의 인덱스가 부호 없는 타입으로 변환되어 거대한 값이 되고, 벡터 바깥의 엉뚱한 메모리를 읽는다. 예외도 안 나고 크래시도 잘 안 나서, 그럴듯한 쓰레기 값이 조용히 답을 오염시킨다.

   ```cpp
   // ✅ 고친 코드
   int nr = r + dr[d], nc = c + dc[d];
   if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;   // 범위를 가장 먼저
   if (vis2d[nr][nc]) continue;                            // 그다음 방문
   if (grid[nr][nc] != 1) continue;                        // 마지막에 값
   dfs_grid(nr, nc);
   ```

4. **모든 경로를 세는데 방문 표시를 되돌리지 않는다**

   ```cpp
   // ❌ 틀린 코드
   void dfs(int cur) {
       if (cur == N) { cnt_paths++; return; }
       for (int nxt : graph[cur]) {
           if (!visited[nxt]) {
               visited[nxt] = 1;
               dfs(nxt);              // 복원이 없다
           }
       }
   }
   ```

   왜: 첫 경로가 쓴 정점이 영원히 막혀, 그 정점을 지나는 다른 경로가 전부 사라진다. 네 갈래가 있어도 답이 `1`로 나온다.

   ```cpp
   // ✅ 고친 코드
   for (int nxt : graph[cur]) {
       if (visited[nxt]) continue;
       visited[nxt] = 1;
       dfs(nxt);
       visited[nxt] = 0;              // 이 경로를 벗어나면 다시 쓸 수 있게
   }
   ```

5. **그래프나 격자를 재귀에 값으로 넘긴다**

   ```cpp
   // ❌ 틀린 코드
   void dfs(int cur, vector<vector<int>> graph, vector<char> visited) {
       visited[cur] = 1;              // 이 프레임의 복사본에만 찍힌다
       for (int nxt : graph[cur])
           if (!visited[nxt]) dfs(nxt, graph, visited);
   }
   ```

   왜: 두 가지가 한꺼번에 망가진다. 호출마다 인접리스트 전체가 복사되어 `O(V+E)`가 `O(V·(V+E))`가 되고, 방문 표시가 호출한 쪽으로 돌아가지 않아 같은 정점을 무한히 다시 방문한다. 프레임에 컨테이너 복사본이 얹혀 스택도 훨씬 빨리 바닥난다.

   ```cpp
   // ✅ 고친 코드
   vector<vector<int>> graph;         // 공유 상태는 전역이나 참조로
   vector<char> visited;
   void dfs(int cur) {
       visited[cur] = 1;
       for (int nxt : graph[cur]) if (!visited[nxt]) dfs(nxt);
   }
   // 매개변수로 넘겨야 한다면 반드시 참조로:
   // void dfs(int cur, const vector<vector<int>>& g, vector<char>& vis)
   ```

6. **인접리스트·방문 배열의 크기를 모자라게 잡는다**

   ```cpp
   // ❌ 틀린 코드
   int V, E;
   cin >> V >> E;
   vector<vector<int>> graph(V);      // 정점 번호가 1..V 인데 인덱스는 0..V-1
   char visited[100];                 // 지역 배열: 쓰레기 값으로 시작
   for (int i = 0; i < E; i++) {
       int a, b; cin >> a >> b;
       graph[a].push_back(b);         // a == V 이면 범위 밖 쓰기
   }
   ```

   왜: 대부분의 문제가 정점을 1번부터 준다. `V`개짜리 벡터에 `graph[V]`를 쓰면 범위 밖이다. 그리고 지역 배열은 0으로 초기화되지 않으므로, 방문 배열이 무작위로 켜진 채 시작해 실행할 때마다 답이 달라진다.

   ```cpp
   // ✅ 고친 코드
   vector<vector<int>> graph(V + 1);       // 1..V 를 그대로 쓰려면 V+1 개
   vector<char> visited(V + 1, 0);         // 벡터 생성자로 0 초기화
   // 지역 배열을 쓸 거면 char visited[100] = {}; 또는 memset(visited, 0, sizeof(visited));
   // memset 은 바이트를 채우므로 0 과 -1(0xFF) 외의 값에는 쓸 수 없다
   ```

7. **무방향 그래프 사이클 판정에서 부모를 빼지 않는다**

   ```cpp
   // ❌ 틀린 코드
   void dfs(int cur) {
       visited[cur] = 1;
       for (int nxt : graph[cur]) {
           if (!visited[nxt]) dfs(nxt);
           else found = true;              // 방금 온 부모도 '방문됨'이다
       }
   }
   ```

   왜: 간선이 `1-2` 하나뿐인 그래프에서도 `2`가 부모 `1`을 보고 사이클이라 답한다. 무방향 간선은 양쪽 인접리스트에 모두 들어 있기 때문이다.

   ```cpp
   // ✅ 고친 코드
   void dfs(int cur, int parent) {
       visited[cur] = 1;
       for (int nxt : graph[cur]) {
           if (!visited[nxt]) dfs(nxt, cur);
           else if (nxt != parent) found = true;   // 부모로 되짚는 간선만 예외
       }
   }
   ```

8. **DFS의 첫 도달 거리를 최단이라고 믿는다**

   ```cpp
   // ❌ 틀린 코드
   void dfs(int r, int c, int d) {
       if (vis2d[r][c]) return;
       vis2d[r][c] = 1;
       dist[r][c] = d;                     // 처음 닿은 거리를 최단으로 기록
       for (int k = 0; k < 4; k++) dfs(r + dr[k], c + dc[k], d + 1);
   }
   ```

   왜: DFS는 한 방향으로 끝까지 파고들므로, 최단이 3인 칸에 길이 11짜리 경로로 먼저 닿을 수 있다. 첫 도달 거리는 "탐색 순서가 우연히 만든 경로의 길이"일 뿐이다. 위 코드는 범위 검사도 없어 재귀 첫 줄에서 범위 밖을 읽는 문제까지 겹쳐 있다.

   ```cpp
   // ✅ 고친 코드
   queue<pair<int,int>> q;
   q.push({sr, sc});
   dist[sr][sc] = 0;                       // BFS: 층 단위로 퍼지므로
   while (!q.empty()) {                    // 처음 적힌 값이 곧 최단
       auto [r, c] = q.front(); q.pop();
       // 이웃에 dist[r][c] + 1 을 적으며 push (push 시점에 방문 표시)
   }
   ```

**다음 챕터로**

- Ch4의 BFS는 이 챕터의 뼈대에서 자료구조 하나만 바꾼다: 스택(재귀) → 큐(`std::queue`). 방문 배열·4방향 오프셋·범위 검사는 그대로 쓴다.
- 바뀌는 것은 **보장**이다. 층 단위로 퍼지므로 "처음 도달한 거리 = 최단거리"가 되고, 이 챕터에서 DFS로는 못 하던 최단거리 문제가 열린다.
- 덤으로 얻는 것이 하나 더 있다. BFS는 상태를 큐(힙 메모리)에 쌓으므로 재귀 깊이 문제가 아예 없다. 큰 격자에서 DFS 재귀가 스택 오버플로로 죽는다면 BFS로 바꾸는 것만으로 해결되는 경우가 많다.
- 여기서 익힌 "연결 요소 = 시작 횟수", "상태를 방문 키에 넣는다"는 감각은 Ch4의 다중 시작점 BFS·상태 BFS로 그대로 이어진다.
