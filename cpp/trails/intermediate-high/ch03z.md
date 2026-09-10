## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터는 두 문장으로 요약된다. **"의존 관계가 있으면 순서를 먼저 만든다"**(L1), **"그 순서가 곧 DP를 채우는 안전한 순서다"**(L2). 위상 정렬 자체는 코드가 짧지만, 실제 문제는 거의 항상 "순서를 만든 다음 그 위에서 무언가를 계산하는" 두 단계로 온다. 아래에서 두 단계를 한 장으로 잇고, 뼈대와 실수 목록으로 마무리한다.

**개념 지도**

```text
                  Ch03 : topological sort
                            |
            edge u -> v means "u must come before v"
                            |
        +-------------------+--------------------+
        |                                        |
   BUILD THE ORDER                          USE THE ORDER
        |                                        |
   Kahn : indeg == 0 -> queue           DAG DP : dp[v] <- dp[pred]
   DFS  : post-order, then reverse        op = max -> longest path
        |                                  op = min -> cheapest path
   order.size() < N     -> cycle          op = +   -> path count
   queue                -> any order      op = max -> finish time
   priority_queue       -> smallest one        |
   queue size always 1  -> unique              |
        |                                      |
        +--------------------------------------+
                       |
        the order must exist before the DP can run
```

DAG DP가 위상 순서를 요구하는 이유는 한 장면이면 충분하다. 순서를 어기면 **아직 비어 있는 값을 읽고**, 그 값이 나중에 커져도 아무도 되돌아오지 않는다.

```text
   (1)--3-->(2)--4-->(4)--2-->(5)      # numbers on edges are weights
    |                 ^
    2                 1
    +----->(3)--------+

   order respected 1,2,3,4,5      order violated : 4 computed first
   dp[2] = 0 + 3 = 3              dp[4] reads dp[2] = 0, dp[3] = 0
   dp[3] = 0 + 2 = 2              dp[4] = 0
   dp[4] = max(3+4, 2+1) = 7      later dp[2] becomes 3, but nobody
   dp[5] = 7 + 2 = 9              ever revisits 4 -> dp[5] = 2  WRONG
```

큐에 몇 개가 들어 있는지는 그 자체로 정보다. 사이클 판정도, 순서의 유일성 판정도 여기서 읽는다.

```text
   the queue holds every vertex that is ready RIGHT NOW

   size 1 at every step           size >= 2 at some step
   1 -> 2 -> 3 -> 4               1 -> 3 ,  2 -> 3
   queue : [1] [2] [3] [4]        queue : [1, 2] [3]
   -> the order is UNIQUE         -> "1 2 3" and "2 1 3" both valid

   cycle :  1 -> 2 -> 3 -> 4 -> 2
   pop 1, indeg[2] goes 2 -> 1, so 2 never reaches 0
   the queue dries up, order.size() = 1 < 4    -> cycle detected
```

C++로 옮길 때 새로 조심할 것은 컨테이너 이름과 감소 연산자, 그리고 스택 깊이다.

```text
  from Python to C++ : four one-line traps

  deque.popleft()   ->  queue<int> q ; q.front() then q.pop()
  heapq             ->  priority_queue<int, vector<int>, greater<int>>
  indeg[v] -= 1     ->  --indeg[v]   (NOT indeg[v]-- inside the test)
  recursive dfs     ->  explicit stack ; 1e5 depth kills the 1MB stack
```

**뼈대 코드**

1) Kahn — 진입차수 큐. 이 챕터의 기본형이다.

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, m;
vector<vector<int>> graph;                 // graph[u] = u 다음에 올 수 있는 것들
vector<int> indeg;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> m;
    graph.assign(n + 1, {});
    indeg.assign(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;                     // u 를 먼저, 그다음 v
        graph[u].push_back(v);
        indeg[v]++;                        // 화살표가 '들어오는' 쪽에 센다
    }

    queue<int> q;
    for (int v = 1; v <= n; v++)
        if (indeg[v] == 0) q.push(v);

    vector<int> order;
    order.reserve(n);
    while (!q.empty()) {
        int u = q.front(); q.pop();        // front() 로 보고 pop() 으로 버린다
        order.push_back(u);
        for (int v : graph[u])
            if (--indeg[v] == 0) q.push(v);   // 먼저 깎고, 0이면 넣는다
    }

    if ((int)order.size() < n) {           // 사이클 판정은 항상 이 한 줄
        cout << -1 << "\n";
        return 0;
    }
    for (int i = 0; i < n; i++) cout << order[i] << " \n"[i == n - 1];
    return 0;
}
```

2) 사전순 최소 — 큐를 최소 힙으로 바꾸기만 한다

```cpp
priority_queue<int, vector<int>, greater<int>> pq;   // 기본은 최대 힙이라 greater 필수
for (int v = 1; v <= n; v++)
    if (indeg[v] == 0) pq.push(v);

vector<int> order;
while (!pq.empty()) {
    int u = pq.top(); pq.pop();            // 지금 놓을 수 있는 것 중 가장 작은 번호
    order.push_back(u);
    for (int v : graph[u])
        if (--indeg[v] == 0) pq.push(v);
}
// 사전순 '최대'가 필요하면 비교자를 빼고 기본 최대 힙을 그대로 쓴다
```

3) 사이클 판정 — 못 꺼낸 정점이 곧 사이클에 얽힌 정점이다

```cpp
// 위 Kahn 을 그대로 돌린 뒤
if ((int)order.size() < n) {
    vector<int> stuck;
    for (int v = 1; v <= n; v++)
        if (indeg[v] > 0) stuck.push_back(v);
    // stuck = 사이클에 속하거나, 사이클에 의존해 영영 못 하는 작업들
    cout << "CYCLE";
    for (int v : stuck) cout << ' ' << v;
    cout << "\n";
}
```

4) DAG DP — 위상 순서로 밀면서(Push) 값을 확정한다. `op`만 갈아 끼운다

```cpp
// graph[u] = {(v, w), ...}  가중 DAG
const long long NEG = LLONG_MIN / 4;       // 더해도 넘치지 않을 여유를 남긴다
vector<long long> dp(n + 1, 0);            // 아래 세 갈래에 따라 초기값이 바뀜

queue<int> q;
for (int v = 1; v <= n; v++)
    if (indeg[v] == 0) q.push(v);

while (!q.empty()) {
    int u = q.front(); q.pop();            // u 를 꺼낸 순간 dp[u] 는 확정
    for (const auto& [v, w] : wgraph[u]) {
        // (A) 최장 경로 : dp[v] = max(dp[v], dp[u] + w)
        // (B) 경로 수   : dp[v] = (dp[v] + dp[u]) % MOD      (dp[start] = 1)
        // (C) 완료 시각 : dp[v] = max(dp[v], dp[u] + t[v])   (병렬이라 max)
        if (dp[u] + w > dp[v]) dp[v] = dp[u] + w;
        if (--indeg[v] == 0) q.push(v);
    }
}

long long best = *max_element(dp.begin() + 1, dp.end());   // 끝점이 자유면 최댓값
cout << best << "\n";                                      // 고정이면 dp[goal]
```

도달 불가를 값 0과 구분해야 하면 초기값을 바꾼다.

```cpp
vector<long long> dp(n + 1, NEG);
for (int v = 1; v <= n; v++)
    if (indeg[v] == 0) dp[v] = 0;          // 시작 후보만 base 를 갖는다
// 출발점이 하나로 고정이면 dp[start] = 0 하나만 두고 나머지는 NEG
// 전이 직전에 if (dp[u] == NEG) continue; 로 미도달을 반드시 거른다
```

5) 위상 순서 유일성 판정 — 매 단계 큐 크기를 본다

```cpp
queue<int> q;
for (int v = 1; v <= n; v++)
    if (indeg[v] == 0) q.push(v);

vector<int> order;
bool unique_ = true;
while (!q.empty()) {
    if (q.size() > 1) unique_ = false;     // 지금 놓을 수 있는 후보가 둘 이상
    int u = q.front(); q.pop();
    order.push_back(u);
    for (int v : graph[u])
        if (--indeg[v] == 0) q.push(v);
}

if ((int)order.size() < n)      cout << "IMPOSSIBLE\n";   // 사이클 — 순서가 없음
else if (!unique_)              cout << "AMBIGUOUS\n";    // 순서가 여러 개
else { for (int v : order) cout << v << ' '; cout << "\n"; }
```

**언제 무엇을 쓰나**

먼저 "이 문제가 위상 정렬인가"를 신호로 판정한다.

| 문제 문장의 신호 | 그래프로 옮기면 | 다음 단계 |
|---|---|---|
| "A를 들어야 B를 들을 수 있다"(선수과목) | `A → B` | Kahn + 레벨 DP(최소 학기) |
| "A가 끝나야 B를 시작한다"(작업·공정) | `A → B` | 완료 시각 DP(`max` + 소요 시간) |
| "A가 B보다 앞선다"(순위·경기 결과) | `A → B` | 순서 생성 + 유일성 판정 |
| "이 모듈은 저 모듈을 필요로 한다"(빌드) | `필요한 것 → 쓰는 것` | 사전순 최소면 `priority_queue`-Kahn |
| "규칙이 서로 모순인지 확인하라" | 방향 그래프 전체 | 사이클 판정(`order.size() < N`) |
| "가능한 순서가 몇 가지인가" | DAG | N이 작으면 백트래킹·비트마스크 DP |

판정을 통과했으면 아래에서 도구를 고른다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 순서 하나만 아무거나 | Kahn(`queue`) | 재귀가 없어 스택 깊이 걱정이 없다 | O(V+E) |
| 사전순 가장 앞선 순서 | Kahn의 큐를 `priority_queue`+`greater<int>`로 | 매번 "지금 가능한 것 중 최소"를 확정 | O((V+E) log V) |
| 사전순 가장 뒤인 순서·역방향 조건 | 역그래프 + 기본(최대) 힙 Kahn | 뒤에서부터 채우면 같은 그리디가 성립 | O((V+E) log V) |
| 사이클 존재 여부 | Kahn 후 `order.size() < N` | 사이클 정점은 진입차수가 0이 될 수 없다 | O(V+E) |
| 사이클에 얽힌 정점 목록 | Kahn 후 `indeg[v] > 0`인 정점 | 못 꺼낸 것이 곧 못 하는 작업 | O(V) |
| 사이클의 증거 정점 하나 | DFS 3색(회색 재방문) | 되돌아가는 간선을 만나는 그 순간이 증거 | O(V+E) |
| 순서가 유일한지 판정 | Kahn 중 매 단계 `q.size()` | 후보가 둘 이상인 순간이 곧 분기점 | O(V+E) |
| 각 정점의 최소 단계·학기 | Kahn + 레벨 전파 | `level[v] = max(level[pred]) + 1` | O(V+E) |
| DAG 최장·최단 경로, 경로 수 | 위상 순서 Push DP | 선행이 전부 확정된 뒤에만 v를 계산 | O(V+E) |
| 병렬 작업의 총 완료 시각 | 완료 시각 DP(`max`) | 선행이 동시에 진행되므로 합이 아니라 최대 | O(V+E) |
| 각 작업의 여유 시간(slack) | 정방향 최이른 + 역방향 최늦 | 두 값의 차가 곧 늦출 수 있는 여유 | O(V+E) |
| 정점이 10만 개를 넘는다 | 반드시 Kahn(반복형) | 재귀 DFS는 기본 1MB 스택에서 죽는다 | O(V+E) |

**위상 정렬만으로 끝나는가, DP까지 필요한가**는 이 표로 가른다.

| 묻는 것 | 필요한 것 | 이유 |
|---|---|---|
| 순서 자체 / 가능한지 여부 | 위상 정렬만 | 정점을 세우는 것이 곧 답 |
| 순서가 유일한지 | 위상 정렬 + 큐 크기 관찰 | 분기 여부는 순서를 만들며 알 수 있다 |
| 각 정점의 "몇 번째 층인가" | 위상 정렬 + 레벨 전파 | 값이 선행의 최댓값에만 의존 |
| 최대/최소/개수/시각을 정점마다 | 위상 정렬 + DAG DP | 값이 선행들의 값에 의존 |
| 두 정점을 잇는 조건부 경로 수 | 정방향 DP × 역방향 DP | 경유 강제는 두 조각의 곱으로 읽는다 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 사이클이 하나라도 있으면 위상 순서가 존재할 수 없는 이유를 모순으로.
- [ ] 설명할 수 있다: 진입차수를 `u → v`에서 왜 `v` 쪽에 세는지, 방향을 뒤집으면 무슨 일이 생기는지.
- [ ] 설명할 수 있다: Kahn이 사이클을 감지하는 원리와, 못 꺼낸 정점들이 무엇을 뜻하는지.
- [ ] 설명할 수 있다: 위상 정렬의 답이 여러 개일 수 있는 이유와, 유일해지는 정확한 조건.
- [ ] 설명할 수 있다: 사전순 최소를 왜 `queue` 대신 `priority_queue`로 얻는지, 그 그리디가 옳은 이유와 함께.
- [ ] 설명할 수 있다: DFS 후위 순서를 뒤집으면 위상 순서가 되는 이유와, 3색 칠하기에서 회색 정점 재방문이 사이클의 증거인 이유.
- [ ] 설명할 수 있다: Kahn과 DFS 중 무엇을 고를지, 사전순·레벨·스택 깊이를 근거로.
- [ ] 설명할 수 있다: 위상 정렬의 복잡도가 O(V+E)인 이유를, 정점·간선이 각각 몇 번 처리되는지 세면서.
- [ ] 설명할 수 있다: "위상 순서 = DP를 채우는 안전한 순서"라는 문장의 뜻과, 어겼을 때 생기는 증상.
- [ ] 설명할 수 있다: DAG DP에서 `op`를 `max`/`min`/`+`로 바꾸면 무엇이 계산되는지, 뼈대는 왜 그대로인지.
- [ ] 설명할 수 있다: Push(전방 갱신)와 Pull(재귀+메모)이 같은 계산인 이유.
- [ ] 설명할 수 있다: 병렬 작업의 완료 시각이 선행들의 "합"이 아니라 "최대"인 이유.
- [ ] 설명할 수 있다: DP 초기값에서 "도달 불가"와 "값 0"을 구분해야 하는 상황과 그 방법.
- [ ] 설명할 수 있다: 역그래프를 언제 만들어야 하는지, 그리고 그것이 어떤 질문을 뒤집어 주는지.
- [ ] 설명할 수 있다: `--indeg[v]`와 `indeg[v]--`가 조건식 안에서 어떻게 다르게 동작하는지.
- [ ] 설명할 수 있다: `LLONG_MIN`을 INF로 쓰면 왜 위험하고, 대신 무엇을 쓰는지.

**⚠️ 자주 하는 실수**

**1) 진입차수를 깎지 않고 검사만 한다**

```cpp
// ❌ 틀린 코드
while (!q.empty()) {
    int u = q.front(); q.pop();
    order.push_back(u);
    for (int v : graph[u]) {
        if (indeg[v] == 0) q.push(v);      // 깎기 전에 검사한다
    }
}
```

왜: `indeg[v]`가 줄지 않으니 선행이 있는 정점은 영영 0이 되지 못하고, 출력이 시작 정점들에서 끊긴다. 반대로 진입차수가 원래 0이던 정점은 조건을 계속 만족해 **여러 번 큐에 들어가** 같은 정점이 중복 출력되기도 한다. 순서는 "깎기 → 0인지 보기"다.

```cpp
// ✅ 고친 코드
for (int v : graph[u]) {
    indeg[v]--;                            // 먼저 깎고
    if (indeg[v] == 0) q.push(v);          // 0이 되는 그 순간에만 넣는다
}
// 한 줄로 쓰면 if (--indeg[v] == 0) q.push(v);  ← 전위 감소여야 한다
```

**2) 조건식 안에서 후위 감소를 쓴다**

```cpp
// ❌ 틀린 코드
for (int v : graph[u])
    if (indeg[v]-- == 0) q.push(v);        // 감소 '전' 값과 비교한다
```

왜: 후위 `--`는 감소하기 전의 값을 돌려준다. 그래서 이 조건은 "차수가 이미 0인가"를 묻는 셈이 되어, 방금 꺼낸 정점의 이웃 중 **원래부터 0이던 것만** 다시 큐에 넣고 차수를 음수로 만든다. 정점이 중복 출력되거나 아예 순서가 완성되지 않는데, 컴파일 경고조차 없다. 파이썬에는 `--` 자체가 없어 옮길 때 새로 생기는 함정이다.

```cpp
// ✅ 고친 코드
for (int v : graph[u])
    if (--indeg[v] == 0) q.push(v);        // 감소 '후' 값과 비교
// 헷갈리면 두 줄로 나눠 쓰는 편이 언제나 안전하다
```

**3) 진입차수를 화살표 반대쪽에 센다**

```cpp
// ❌ 틀린 코드
for (int i = 0; i < m; i++) {
    int u, v; cin >> u >> v;               // u 를 먼저 해야 v 를 할 수 있다
    graph[u].push_back(v);
    indeg[u]++;                            // 나가는 쪽에 세었다
}
```

왜: 진입차수는 "나보다 먼저 끝나야 할 것이 몇 개 남았는가"다. 나가는 쪽에 세면 의미가 뒤집혀, 선행이 없는 정점이 큐에 못 들어가고 선행이 많은 정점이 곧바로 들어간다. 결과는 순서가 통째로 거꾸로 나오거나, 사이클이 없는데도 `order.size() < N`이 뜬다.

```cpp
// ✅ 고친 코드
for (int i = 0; i < m; i++) {
    int u, v; cin >> u >> v;
    graph[u].push_back(v);
    indeg[v]++;                            // 화살표가 들어오는 v 쪽에 센다
}
```

**4) 사전순 최소를 요구하는데 `queue`를 쓴다**

```cpp
// ❌ 틀린 코드
queue<int> q;
for (int v = 1; v <= n; v++)
    if (indeg[v] == 0) q.push(v);
while (!q.empty()) {
    int u = q.front(); q.pop();            // 들어온 순서대로 나온다
    ...
}
```

왜: `queue`는 FIFO라 "먼저 준비된 것"을 꺼낼 뿐, "번호가 가장 작은 것"을 꺼내지 않는다. 두 정점이 동시에 준비되면 입력 순서가 답을 좌우해 사전순이 깨진다. 정점 `1, 2`가 함께 준비되고 간선을 `2`부터 읽었다면 `2 1 …`이 나온다. **정렬 기준이 붙는 순간 큐는 힙이 된다.** C++에서는 여기에 함정이 하나 더 있다 — `priority_queue`는 기본이 **최대** 힙이라 그냥 바꾸면 사전순 최대가 나온다.

```cpp
// ✅ 고친 코드
priority_queue<int, vector<int>, greater<int>> pq;   // greater 로 최소 힙
for (int v = 1; v <= n; v++)
    if (indeg[v] == 0) pq.push(v);
while (!pq.empty()) {
    int u = pq.top(); pq.pop();            // top() 이다 — front() 가 아니다
    ...
    if (--indeg[v] == 0) pq.push(v);       // 큐 연산 세 군데를 모두 힙으로
}
```

**5) DAG DP를 위상 순서 없이 계산한다**

```cpp
// ❌ 틀린 코드
for (int u = 1; u <= n; u++)               // 정점 번호 순으로 그냥 훑는다
    for (const auto& [v, w] : wgraph[u])
        dp[v] = max(dp[v], dp[u] + w);
```

왜: `dp[u]`가 확정되기 전에 `u`를 꺼내 미완성 값을 이웃에 퍼뜨린다. 번호 순이 우연히 위상 순서와 같으면 맞고 아니면 틀리므로, **입력 번호 붙이기 방식에 답이 좌우되는** 최악의 버그가 된다. 앞의 도식에서 `4`를 먼저 계산하면 `dp[5]`가 9가 아니라 2로 굳는 것이 정확히 이 증상이다.

```cpp
// ✅ 고친 코드
queue<int> q;
for (int v = 1; v <= n; v++)
    if (indeg[v] == 0) q.push(v);
while (!q.empty()) {
    int u = q.front(); q.pop();            // 꺼낸 순간 dp[u] 는 확정돼 있다
    for (const auto& [v, w] : wgraph[u]) {
        if (dp[u] + w > dp[v]) dp[v] = dp[u] + w;
        if (--indeg[v] == 0) q.push(v);
    }
}
```

**6) 도달 불가를 `LLONG_MIN`으로 표시하고 그대로 더한다**

```cpp
// ❌ 틀린 코드
vector<long long> dp(n + 1, LLONG_MIN);
dp[s] = 0;
...
for (const auto& [v, w] : wgraph[u])
    dp[v] = max(dp[v], dp[u] + w);         // dp[u] 가 LLONG_MIN 이면 즉시 넘친다
```

왜: `LLONG_MIN + w`는 **부호 있는 정수 오버플로**이고, C++ 표준에서 이것은 정의되지 않은 동작(UB)이다. 값이 거대한 양수로 감겨 미도달 정점이 최댓값을 차지하거나, 컴파일러가 "넘칠 리 없다"고 가정하고 검사를 지워 최적화 빌드에서만 답이 달라진다. 파이썬의 `float('-inf')`는 더해도 `-inf`라 이 문제가 없었다.

```cpp
// ✅ 고친 코드
const long long NEG = LLONG_MIN / 4;       // 더해도 넘치지 않을 여유
vector<long long> dp(n + 1, NEG);
dp[s] = 0;                                 // base 는 출발점만
...
for (const auto& [v, w] : wgraph[u]) {
    if (dp[u] == NEG) continue;            // 미도달에서는 밀지 않는다
    dp[v] = max(dp[v], dp[u] + w);
}
cout << (dp[t] == NEG ? -1 : dp[t]) << "\n";
```

**7) 유일성 판정을 처음 한 번만 한다**

```cpp
// ❌ 틀린 코드
queue<int> q;
for (int v = 1; v <= n; v++)
    if (indeg[v] == 0) q.push(v);
bool unique_ = (q.size() == 1);            // 시작할 때만 검사한다
while (!q.empty()) { ... }
```

왜: 분기는 중간에도 얼마든지 생긴다. 시작 정점이 하나여도, 그 정점을 꺼낸 뒤 두 개가 한꺼번에 준비되면 순서는 두 가지가 된다. `1 → 2`, `1 → 3`만 있는 그래프가 그렇다 — 시작 큐는 `[1]` 하나지만 답은 `1 2 3`과 `1 3 2` 둘이다. **매 반복마다** 후보 수를 봐야 한다.

```cpp
// ✅ 고친 코드
bool unique_ = true;
while (!q.empty()) {
    if (q.size() > 1) unique_ = false;     // 루프 안에서 매번 확인
    int u = q.front(); q.pop();
    ...
}
// 사이클(order.size() < n) 판정과 유일성 판정은 서로 다른 검사다 — 둘 다 한다
```

**8) 큰 컨테이너를 값으로 넘기거나, `indeg`를 참조로 넘긴다**

```cpp
// ❌ 틀린 코드
vector<int> topoKahn(int n, vector<vector<int>> graph, vector<int>& indeg) {
    //                        ^ 값 복사: 간선 20만 개를 통째로 복사한다
    //                                            ^ 참조: 호출자의 배열을 소모한다
    ...
}
```

왜: 두 가지가 동시에 틀렸다. 읽기만 하는 `graph`를 값으로 받으면 인접 리스트 전체가 복사돼 시간·메모리가 배로 든다. 반대로 Kahn이 소모하는 `indeg`를 참조로 받으면 함수가 끝난 뒤 호출자의 배열이 전부 0이 되어, 같은 그래프로 두 번째 계산(예: 유일성 판정, DAG DP)을 돌리면 엉뚱한 답이 나온다. 파이썬은 리스트가 늘 참조라 "복사 비용"은 없었지만 "소모" 문제는 똑같이 있었다.

```cpp
// ✅ 고친 코드
vector<int> topoKahn(int n, const vector<vector<int>>& graph, vector<int> indeg) {
    //                        ^ const 참조: 복사 없음      ^ 값 복사: 소모해도 안전
    ...
}
// 규칙: 읽기만 하면 const&, 안에서 부수면 값 복사
```

**9) 재귀 DFS로 위상 정렬을 짠다**

```cpp
// ❌ 틀린 코드
void dfs(int u) {
    color[u] = 1;
    for (int v : graph[u]) if (!color[v]) dfs(v);
    color[u] = 2;
    order.push_back(u);
}
```

왜: 정점이 한 줄로 이어진 DAG(`1→2→3→…→100000`)에서는 재귀 깊이가 그대로 10만이 된다. 기본 스택은 보통 1MB라 프레임 하나가 수십 바이트여도 넘치고, 파이썬처럼 `RecursionError` 예외가 뜨는 게 아니라 **아무 메시지 없이 죽는다**(채점 결과는 "런타임 에러"). 게다가 재귀 깊이를 늘리는 표준적인 방법도 없다.

```cpp
// ✅ 고친 코드 — 프레임을 직접 쌓는다
vector<pair<int,int>> stk = {{s, 0}};      // (정점, 다음에 볼 자식 인덱스)
color[s] = 1;
while (!stk.empty()) {
    auto& [u, pi] = stk.back();
    if (pi < (int)graph[u].size()) {
        int v = graph[u][pi++];
        if (color[v] == 1) hasCycle = true;              // 회색 재방문 = 사이클
        else if (color[v] == 0) { color[v] = 1; stk.push_back({v, 0}); }
    } else {
        color[u] = 2;
        order.push_back(u);                              // 완료 시점에 쌓기
        stk.pop_back();
    }
}
// 정점 수가 크면 애초에 Kahn 쪽을 기본형으로 삼는 것이 가장 안전하다
```

**다음 챕터로**

- 위상 순서는 "의존이 한 방향으로만 흐를 때 DP를 안전하게 채우는 순서"였다. 다음 단계의 DP들은 이 순서를 그래프가 아니라 **인덱스·부분집합**에서 찾는다. 구간 DP의 "짧은 구간부터", 비트마스크 DP의 "마스크 값 오름차순"이 모두 같은 요구를 다른 모양으로 만족시키는 것이다.
- 사이클이 있어서 위상 정렬이 실패하는 그래프도, 강한 연결 요소로 뭉치면 다시 DAG가 된다. "먼저 DAG로 만든 뒤 그 위에서 DP"라는 이 챕터의 두 단계 구조가 그대로 재사용된다.
- C++ 쪽에서 이 챕터가 남긴 습관은 세 가지다. **조건식 안에서는 전위 `--`**, **읽기만 하면 `const&`**, **깊어질 수 있으면 반복형**.
