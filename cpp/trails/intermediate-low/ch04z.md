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
- 0-1 BFS만 자료구조가 `queue`에서 **`deque`**로 바뀐다. 비용 0 간선을 앞에 넣어 층 순서를 지키기 위해서다.

- C++에서 각 갈래가 어떤 그릇을 쓰는지 한눈에 보면 이렇다. 큐 원소의 모양과 `dist`의 차원이 항상 짝을 이룬다.

```text
  kind            queue element              dist container
  ------------    ------------------------   ------------------------------
  graph BFS       queue<int>                 vector<int> dist(V+1, -1)
  grid BFS        queue<pair<int,int>>       vector<vector<int>> (R x C)
  multi-source    queue<pair<int,int>>       same, many cells start at 0
  state BFS       queue<array<int,3>>        3-D vector  (R x C x S)
  0-1 BFS         deque<pair<int,int>>       dist filled with INF, not -1
```

**뼈대 코드**

```cpp
// (1) 그래프 BFS — dist 하나로 방문 여부(-1)와 거리를 함께 관리
#include <bits/stdc++.h>
using namespace std;

vector<int> bfs(int start, int target, const vector<vector<int>>& graph, int V) {
    vector<int> dist(V + 1, -1);         // -1 = 미방문
    dist[start] = 0;
    queue<int> q;
    q.push(start);
    while (!q.empty()) {
        int cur = q.front(); q.pop();    // front로 읽고 pop으로 버린다(두 단계)
        if (cur == target) break;        // 조기 종료 (필요할 때만) # 문제마다 바뀜
        for (int nxt : graph[cur]) {
            if (dist[nxt] == -1) {       // 아직 값이 없을 때만
                dist[nxt] = dist[cur] + 1;
                q.push(nxt);             // push하는 순간 방문 확정
            }
        }
    }
    return dist;
}
```

```cpp
// (2) 격자 BFS — 칸이 정점, 4방향 이동이 간선(비용 1)
int dr[] = {-1, 1, 0, 0};
int dc[] = {0, 0, -1, 1};                // 8방향이면 4개 추가 # 문제마다 바뀜

vector<vector<int>> dist(N, vector<int>(M, -1));
dist[sr][sc] = 0;
queue<pair<int, int>> q;
q.push({sr, sc});
while (!q.empty()) {
    auto [r, c] = q.front(); q.pop();
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;  // 범위가 항상 먼저
        if (dist[nr][nc] != -1) continue;
        if (grid[nr][nc] == 1) continue;         // 이동 가능 조건 # 문제마다 바뀜
        dist[nr][nc] = dist[r][c] + 1;
        q.push({nr, nc});
    }
}
```

```cpp
// (3) 다중 시작점 BFS — 시작점 전부를 거리 0으로 먼저 넣는다
queue<pair<int, int>> q;
vector<vector<int>> dist(N, vector<int>(M, -1));
for (int r = 0; r < N; r++)
    for (int c = 0; c < M; c++)
        if (grid[r][c] == SOURCE) {      // 시작점의 정의 # 문제마다 바뀜
            dist[r][c] = 0;
            q.push({r, c});
        }
// 이후 루프는 (2)와 글자 하나 다르지 않다.
// 결과 dist[r][c] = "가장 가까운 시작점까지의 거리"
// 전체 확산 시간을 묻는다면 도달한 칸들의 dist 최댓값이 답
```

```cpp
// (4) 상태 BFS — 좌표에 상태를 붙이고 방문 배열의 차원을 늘린다
int S = K + 1;                           // 상태 가짓수 # 문제마다 바뀜
vector<vector<vector<int>>> dist(N, vector<vector<int>>(M, vector<int>(S, -1)));
dist[sr][sc][0] = 0;
queue<array<int, 3>> q;
q.push({sr, sc, 0});
while (!q.empty()) {
    auto [r, c, s] = q.front(); q.pop();
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;
        int ns = next_state(s, nr, nc);  // 상태 전이 규칙 # 문제마다 바뀜
        if (ns < 0) continue;            // 그 상태로는 못 감(문·부수기 소진 등)
        if (dist[nr][nc][ns] != -1) continue;   // 상태가 다르면 다른 정점
        dist[nr][nc][ns] = dist[r][c][s] + 1;
        q.push({nr, nc, ns});
    }
}
int answer = -1;                         // 도착 칸의 모든 상태 중 최소
for (int s = 0; s < S; s++)
    if (dist[er][ec][s] != -1 && (answer == -1 || dist[er][ec][s] < answer))
        answer = dist[er][ec][s];
```

```cpp
// (5) 0-1 BFS — 비용이 0과 1 두 종류일 때. deque의 앞/뒤를 쓴다
const int INF = 1e9;                     // INT_MAX 금지: INF + w 가 넘친다
vector<vector<int>> dist(N, vector<int>(M, INF));
dist[sr][sc] = 0;
deque<pair<int, int>> dq;
dq.push_back({sr, sc});
while (!dq.empty()) {
    auto [r, c] = dq.front(); dq.pop_front();
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;
        int w = (grid[nr][nc] == 1) ? 1 : 0;     // 간선 비용 # 문제마다 바뀜
        if (dist[r][c] + w < dist[nr][nc]) {     // 더 짧아질 때만 갱신
            dist[nr][nc] = dist[r][c] + w;
            if (w == 0) dq.push_front({nr, nc}); // 같은 층 -> 앞
            else        dq.push_back({nr, nc});  // 다음 층 -> 뒤
        }
    }
}
```

```cpp
// (6) 경로 복원 — 처음 방문시킨 직전 정점을 남긴다
vector<int> parent(V + 1, -1);
// BFS 안에서: dist[nxt] = dist[cur] + 1; parent[nxt] = cur; q.push(nxt);

if (dist[goal] == -1) {
    cout << -1 << "\n";
} else {
    vector<int> path;
    for (int v = goal; v != -1; v = parent[v])   // 시작점의 parent가 -1이라 멈춘다
        path.push_back(v);
    reverse(path.begin(), path.end());
    for (int i = 0; i < (int)path.size(); i++)
        cout << path[i] << " \n"[i + 1 == (int)path.size()];
}
// 격자면 parent[r][c] = 직전 칸의 (r, c)를 pair로, 또는 방향 번호만 저장
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 간선 비용이 모두 같은 최단 거리 | BFS | 층 단위로 퍼지므로 첫 도달이 곧 최단 | O(V+E) |
| 격자에서 최소 이동 횟수 | 격자 BFS(`dist` 2차원) | 칸=정점, 4방향=간선, 비용 1 | O(N·M) |
| "가장 가까운 X까지"(X가 여럿) | 다중 시작점 BFS | 모든 X를 거리 0으로 함께 넣으면 한 번에 끝 | O(N·M) |
| 좌표에 조건이 붙는 최단(열쇠·부수기) | 상태 BFS(차원 추가) | 같은 칸이라도 상태가 다르면 다른 정점 | O(N·M·S) |
| 비용이 0과 1 두 종류 | 0-1 BFS(`deque`) | 0은 앞, 1은 뒤 → 우선순위 큐가 필요 없다 | O(V+E) |
| 비용이 제각각인 최단 | 다익스트라(`priority_queue`) | 층 구조가 깨져 BFS·0-1 BFS 모두 틀린다 | O(E log V) |
| 거리뿐 아니라 경로 자체가 필요 | BFS + `parent` 기록 | 처음 방문시킨 정점만 남기면 역추적된다 | O(V+E) |
| "번지는 것"과 "움직이는 것"이 함께 | BFS 두 번(두 단계) | 번짐 시각은 이동과 무관하게 먼저 확정된다 | O(N·M) |
| 도달 가능성·연결 요소만 | DFS든 BFS든 무관 | 순서가 답에 영향을 주지 않는다 | O(V+E) |
| 모든 경로 나열·경로 개수 | DFS 백트래킹 (Ch3) | 표시를 되돌려야 하는데 큐로는 불가능하다 | 경로 수에 비례(지수) |
| 재귀 깊이가 위험한 큰 격자 | BFS(또는 반복 DFS) | 큐는 콜스택 한도와 무관하다 | O(N·M) |
| 상태 수가 수백만을 넘을 때 | 상태 정의 축소·타입 축소 | `int` 3차원은 상태당 4바이트라 메모리가 먼저 터진다 | 메모리 O(V) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: BFS가 최단거리를 보장하는 이유를 "층 단위 확장 → 첫 도달이 최소"로 유도하는 과정.
- [ ] 설명할 수 있다: 큐 안에는 왜 항상 거리 `d`와 `d+1` 두 종류만 들어 있는지.
- [ ] 설명할 수 있다: 방문 표시를 pop이 아니라 **push 시점**에 해야 하는 이유와, 어기면 무엇이 터지는지.
- [ ] 설명할 수 있다: `dist` 배열 하나로 방문 여부와 거리를 동시에 관리하는 방법(`-1` = 미방문).
- [ ] 설명할 수 있다: 시간복잡도 O(V+E)를 "정점당 push·pop 1회 + 인접리스트 총 순회 2E"로 세는 과정.
- [ ] 설명할 수 있다: `std::queue`의 `pop()`이 값을 돌려주지 않는 이유와, `front()`를 참조로 받은 뒤 `pop()` 하면 왜 위험한지.
- [ ] 설명할 수 있다: `vector`의 `erase(begin())`이 왜 O(N)이고 전체가 왜 O(V²)가 되는지.
- [ ] 설명할 수 있다: 2차원·3차원 `vector`를 한 줄로 초기화하는 문법과, `vector<vector<int>> d(R);`이 왜 위험한지.
- [ ] 설명할 수 있다: 다중 시작점 BFS가 왜 한 번의 BFS로 "가장 가까운 시작점까지의 거리"를 주는지.
- [ ] 설명할 수 있다: 어떤 값을 방문 배열의 차원에 넣어야 하고 어떤 값은 넣으면 안 되는지, 그 판단 기준.
- [ ] 설명할 수 있다: 상태를 추가하면 시간·메모리가 어떻게 곱해지는지(`R·C·(K+1)`, `R·C·2^k`).
- [ ] 설명할 수 있다: 0-1 BFS가 다익스트라 없이도 되는 이유(덱의 불변식)와, 왜 "push 시점 확정"을 쓰면 안 되는지.
- [ ] 설명할 수 있다: `INF`를 `INT_MAX`로 두면 `INF + w`가 왜 음수가 되는지, 대신 무엇을 쓰는지.
- [ ] 설명할 수 있다: 간선 비용이 서로 다르면 BFS가 왜 틀리는지, 그때 무엇으로 바꾸는지.
- [ ] 설명할 수 있다: "간선 수"와 "지나는 칸 수"의 차이(+1이 어디서 나오는지).
- [ ] 설명할 수 있다: `parent`를 남겨 최단 경로를 복원하는 절차와, 역추적이 멈추는 조건.
- [ ] 설명할 수 있다: 두 단계 BFS(번짐 시각 계산 → 그 위에서 이동)로 문제를 나누는 이유.

**⚠️ 자주 하는 실수**

1. **`q.pop()`이 값을 돌려준다고 생각한다**

   ```cpp
   // ❌ 틀린 코드
   while (!q.empty()) {
       int cur = q.pop();            // 컴파일 오류: pop()의 반환형은 void
       ...
   }

   // ❌ 더 위험한 변형 (컴파일은 된다)
   while (!q.empty()) {
       auto& cur = q.front();        // 참조로 받고
       q.pop();                      // 가리키던 원소를 없앤다
       use(cur);                     // 사라진 자리를 읽는다 -> 정의되지 않은 동작
   }
   ```

   왜: C++ 표준은 "꺼내면서 반환"을 예외 안전성 때문에 일부러 제공하지 않는다. 값을 복사해 돌려주는 도중 예외가 나면 원소가 큐에서는 이미 빠졌는데 호출자에게는 도달하지 못해 통째로 사라지기 때문이다. 그래서 읽기와 제거가 분리되어 있고, 참조로 받아 두면 `pop()` 직후 그 참조가 무효가 된다.

   ```cpp
   // ✅ 고친 코드
   while (!q.empty()) {
       int cur = q.front();          // 값으로 복사해서 받고
       q.pop();                      // 그다음에 버린다
       use(cur);
   }
   // 격자라면: auto [r, c] = q.front(); q.pop();   (구조적 바인딩도 복사본)
   ```

2. **방문 표시를 pop 시점에 한다**

   ```cpp
   // ❌ 틀린 코드
   while (!q.empty()) {
       int cur = q.front(); q.pop();
       visited[cur] = true;          // 꺼낼 때 표시
       for (int nxt : graph[cur])
           if (!visited[nxt])
               q.push(nxt);          // 큐 안에 이미 있는 정점을 또 넣는다
   }
   ```

   왜: 큐에서 대기 중인 정점은 아직 미표시라, 그 이웃들이 저마다 다시 넣는다. 격자에서는 한 칸이 최대 4번 들어가고 그 4개가 또 이웃을 넣어 큐가 눈덩이처럼 불어난다 → 시간·메모리 초과.

   ```cpp
   // ✅ 고친 코드
   while (!q.empty()) {
       int cur = q.front(); q.pop();
       for (int nxt : graph[cur]) {
           if (dist[nxt] == -1) {
               dist[nxt] = dist[cur] + 1;
               q.push(nxt);          // 넣는 순간 확정 -> 정점당 정확히 1회
           }
       }
   }
   ```

3. **2차원 `dist`를 잘못 만든다**

   ```cpp
   // ❌ 틀린 코드
   vector<vector<int>> dist(N);      // 빈 행 N개 — 안쪽에 칸이 하나도 없다
   dist[sr][sc] = 0;                 // 범위 밖 접근 (정의되지 않은 동작)

   // ❌ 또 다른 변형
   int dist[1000][1000];             // 지역 배열은 0으로 초기화되지 않는다
   ```

   왜: `vector<vector<int>> dist(N);`은 "빈 `vector` `N`개"라는 뜻이라 `dist[0].size()`가 0이다. 파이썬의 중첩 리스트 컴프리헨션에 해당하는 것은 두 번째 인자로 "행 하나"를 통째로 주는 형태다. 지역 배열은 초기화 구문이 없으면 쓰레기값이 들어 있어, 그 값이 우연히 `-1`이 아니면 BFS가 전 칸을 방문 완료로 착각한다.

   ```cpp
   // ✅ 고친 코드
   vector<vector<int>> dist(N, vector<int>(M, -1));      // N x M, 전부 -1
   // 고정 크기 배열을 쓴다면 전역으로 두고 명시적으로 채운다
   static int dist2[1000][1000];
   memset(dist2, -1, sizeof(dist2));   // memset은 -1과 0에만 안전하다
   ```

4. **상태를 방문 배열에 넣지 않는다**

   ```cpp
   // ❌ 틀린 코드
   vector<vector<int>> dist(N, vector<int>(M, -1));   // 차원이 2개뿐
   queue<array<int, 3>> q;
   q.push({sr, sc, 0});
   while (!q.empty()) {
       auto [r, c, key] = q.front(); q.pop();
       // ...
       if (dist[nr][nc] == -1) {                      // key를 무시하고 판단
           dist[nr][nc] = dist[r][c] + 1;
           q.push({nr, nc, key});
       }
   }
   ```

   왜: 열쇠를 줍고 되돌아올 때 지나야 하는 칸이 "이미 방문됨"으로 막힌다. 정답 경로가 통째로 사라져 도달 가능한 문제에 `-1`이 나온다. 큐 원소에는 상태를 넣어 놓고 방문 배열에만 안 넣는 것이 가장 흔한 형태다.

   ```cpp
   // ✅ 고친 코드
   vector<vector<vector<int>>> dist(N, vector<vector<int>>(M, vector<int>(2, -1)));
   // ...
   if (dist[nr][nc][nkey] == -1) {                    // 상태까지 포함해 판단
       dist[nr][nc][nkey] = dist[r][c][key] + 1;
       q.push({nr, nc, nkey});
   }
   ```

5. **시작점의 거리를 초기화하지 않는다**

   ```cpp
   // ❌ 틀린 코드
   vector<vector<int>> dist(N, vector<int>(M, -1));
   queue<pair<int, int>> q;
   q.push({sr, sc});                 // 큐에는 넣었지만 dist는 여전히 -1
   while (!q.empty()) {
       auto [r, c] = q.front(); q.pop();
       // ...
       dist[nr][nc] = dist[r][c] + 1;   // -1 + 1 = 0 -> 거리가 전부 밀린다
   }
   ```

   왜: 시작 칸이 미방문으로 남아 있어 나중에 다시 큐에 들어갈 수도 있고, 거리 계산의 기준점이 `-1`이 되어 모든 값이 1씩 어긋난다.

   ```cpp
   // ✅ 고친 코드
   vector<vector<int>> dist(N, vector<int>(M, -1));
   dist[sr][sc] = 0;                 // 큐에 넣는 것과 표시는 항상 한 쌍
   queue<pair<int, int>> q;
   q.push({sr, sc});
   ```

6. **0-1 BFS에 L1의 "push 시점 확정"을 그대로 쓴다**

   ```cpp
   // ❌ 틀린 코드
   if (dist[nr][nc] == -1) {                 // 한 번 값이 들어가면 다시 못 고친다
       dist[nr][nc] = dist[r][c] + w;
       if (w == 0) dq.push_front({nr, nc});
       else        dq.push_back({nr, nc});
   }
   ```

   왜: 0-1 BFS에서는 같은 칸이 나중에 **더 짧은 값**으로 다시 도달할 수 있다. 비용 1로 먼저 닿아 값이 굳으면 뒤이어 오는 비용 0 경로가 무시되어 답이 커진다. "처음 도달이 곧 최단"은 모든 간선 비용이 같을 때만 성립하는 성질이다.

   ```cpp
   // ✅ 고친 코드
   if (dist[r][c] + w < dist[nr][nc]) {      // 더 짧아질 때만 갱신
       dist[nr][nc] = dist[r][c] + w;
       if (w == 0) dq.push_front({nr, nc});
       else        dq.push_back({nr, nc});
   }
   // dist는 -1이 아니라 INF(=1e9)로 채워 두어야 이 비교가 성립한다
   ```

7. **`INF`를 `INT_MAX`로 잡는다**

   ```cpp
   // ❌ 틀린 코드
   vector<int> dist(V, INT_MAX);
   // ...
   if (dist[cur] + w < dist[nxt]) {   // INT_MAX + 1 = 음수 (오버플로)
       dist[nxt] = dist[cur] + w;     // 음수가 '최단'으로 위장해 표를 오염시킨다
   }
   ```

   왜: 부호 있는 정수의 오버플로는 예외를 던지지 않고 값이 조용히 뒤집힌다. `INT_MAX + 1`은 `INT_MIN`이 되어 어떤 비교에서도 이기므로, 도달 불가 정점이 오히려 "가장 가까운 정점"이 된다.

   ```cpp
   // ✅ 고친 코드
   const int INF = 1e9;               // 더해도 int 범위(약 2.1e9) 안에 남는다
   vector<int> dist(V, INF);
   // long long을 쓴다면 const long long INF = 1e18; (LLONG_MAX 금지)
   ```

8. **간선 비용이 다른데 BFS로 최단을 구한다**

   ```cpp
   // ❌ 틀린 코드
   for (auto [nxt, w] : graph[cur]) { // w가 2, 5, 7 ... 제각각
       if (dist[nxt] == -1) {
           dist[nxt] = dist[cur] + w; // 첫 도달이 최소라는 보장이 깨진다
           q.push(nxt);
       }
   }
   ```

   왜: BFS의 최단 보장은 "모든 간선의 비용이 같다"에서만 나온다. 비용이 다르면 큐에서 먼저 나온 정점이 더 가깝다는 근거가 없어져, 비용 큰 간선 하나로 먼저 닿은 값이 그대로 굳는다.

   ```cpp
   // ✅ 고친 코드 — 비용이 제각각이면 다익스트라
   priority_queue<pair<long long, int>,
                  vector<pair<long long, int>>,
                  greater<>> pq;      // greater<>로 최소 힙(기본은 최대 힙)
   pq.push({0, start});
   while (!pq.empty()) {
       auto [d, cur] = pq.top(); pq.pop();   // 항상 '가장 가까운 것'부터 확정
       if (d > dist[cur]) continue;          // 낡은 항목은 버린다
   }
   // 비용이 0과 1 두 종류뿐이면 우선순위 큐 대신 0-1 BFS(deque)로 충분하다
   ```

9. **"간선 수"와 "지나는 칸 수"를 혼동한다**

   ```cpp
   // ❌ 틀린 코드
   cout << dist[N-1][M-1] << "\n";   // 이동 횟수를 그대로 출력
   ```

   왜: `dist`는 **간선 수**(이동 횟수)이고, 문제가 묻는 "지나는 칸의 개수"는 그보다 1 크다. 게다가 도달 불가(`-1`)일 때 `+1`을 해 버리면 `0`이라는 엉뚱한 값이 나간다.

   ```cpp
   // ✅ 고친 코드
   int ans = dist[N-1][M-1];
   cout << (ans != -1 ? ans + 1 : -1) << "\n";   // 도달 불가는 별도로 처리
   // 또는 시작 칸의 dist를 1로 두고 시작해 처음부터 '칸 수'로 세도 된다
   ```

**다음 챕터로**

- 이 챕터의 BFS는 "모든 간선 비용이 같다"를 전제로 최단을 보장했다. 비용이 제각각이 되는 순간 그 보장이 깨지고, 우선순위 큐(`std::priority_queue`)로 "가장 가까운 것부터 확정"하는 다익스트라가 필요해진다.
- 0-1 BFS는 그 중간 지점이다. `deque`의 앞/뒤만으로 우선순위 큐 흉내를 내는 이 아이디어가, 이후 최단 경로 알고리즘을 배울 때 "왜 우선순위가 필요한가"를 이해하는 발판이 된다.
- 상태 BFS에서 익힌 "정점을 새로 정의한다"는 감각은 이후 상태 압축·비트마스크 탐색으로 그대로 이어진다. 그때는 상태 수가 곧 메모리이므로, 여기서 익힌 "`R·C·S`를 먼저 곱해 본다"는 습관이 더 중요해진다.
