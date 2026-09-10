## L3. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch05(Shortest Path)의 핵심 — 지연 삭제 Dijkstra와 **상태를 얹은 확장**(경로 복원·연료·열쇠), 그리고 모든 쌍을 구해 두고 **조각을 합쳐 읽는 Floyd-Warshall**(경유지·간선 수 제한·분기점) — 을 소재만 바꿔 **반복 훈련**하고, 코딩테스트 단골 유형(가장 먼 노드·격자 비용·파티(왕복)·합승 요금 류)으로 **확장**하는 연습 세트다.
- **반복 훈련 개념**:
  - Dijkstra 뼈대: `priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;` → `pq.push({0, s});` → 꺼낼 때 `if (d > dist[u]) continue;`(지연 삭제) → 완화 `if (d + w < dist[v]) { dist[v] = d + w; pq.push({dist[v], v}); }`.
  - **C++ `priority_queue`는 기본이 최대 힙**이다. `greater<>`(세 번째 템플릿 인자)를 빼면 가장 먼 것부터 꺼내며 최단이 아니라 엉뚱한 값을 확정하므로, Dijkstra에서는 반사적으로 붙인다.
  - 경로 복원: 완화하는 순간 `parent[v] = u`, 끝에서 `while (v != s) { path.push_back(v); v = parent[v]; }` 후 `reverse(path.begin(), path.end())`.
  - 상태 확장: 연료 잔량·열쇠 비트마스크처럼 가짓수가 작은 부가 상태를 차원으로 얹어 `dist[v][state]`(= `vector<vector<long long>>`), 힙에는 `tuple<long long, int, int>`(거리, 정점, 상태).
  - 역방향 그래프: "모든 정점 → X"의 최단은 간선을 뒤집은 그래프에서 X 출발 Dijkstra 한 번으로.
  - Floyd 뼈대: `for (int k...) for (int i...) for (int j...) dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);` — **`k`가 반드시 가장 바깥**이다. 모든 쌍을 구해 두면 경유지·분기점 질의는 `dist` 조각의 합으로 읽는다.
  - 격자 = 그래프: 칸이 정점, 4방향 이웃이 간선, 비용은 "들어가는 칸의 값".
  - 거리 변수는 `long long`, `INF`는 `1e18` 정도로 잡되 **INF + w를 그대로 비교하지 않는다**(오버플로). 더하기 전에 `if (a >= INF) continue;`로 걸러 낸다.
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
- **셀프체크**: 힙에 `(거리, 정점)`을 넣고, 꺼낸 거리가 `dist[u]`보다 크면 낡은 항목이므로 버린다(지연 삭제). `priority_queue`의 세 번째 인자에 `greater<>`를 넣어 **최소 힙**으로 만들었는가 — 빼면 가장 먼 것부터 꺼내므로 답이 무너진다. `pair`를 `(거리, 정점)` 순서로 담으면 기본 사전식 비교가 곧 거리 비교라 비교자를 따로 쓸 필요가 없다. 예제1: S=2 → 3(1) → 1(1+2=3, 직행 4보다 짧음) → 4(3+1=4, 3→4 직행 1+5=6보다 짧음). 일방통행이므로 간선을 한 방향만 넣는다. `1e18`로 남은 정점을 문자열 `INF`로 바꿔 출력.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;
typedef pair<long long, int> P;         // (거리, 정점) — 사전식 비교가 곧 거리 비교

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, s;
    cin >> n >> m >> s;
    vector<vector<pair<int, int>>> graph(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        graph[u].push_back(make_pair(v, w));   // 일방통행: 한 방향만
    }
    const long long INF = 1e18;
    vector<long long> dist(n + 1, INF);
    dist[s] = 0;
    priority_queue<P, vector<P>, greater<>> pq;   // greater<> 없으면 최대 힙!
    pq.push(P(0, s));
    while (!pq.empty()) {
        long long d = pq.top().first;
        int u = pq.top().second;
        pq.pop();
        if (d > dist[u]) continue;               // 지연 삭제
        for (size_t e = 0; e < graph[u].size(); e++) {
            int v = graph[u][e].first, w = graph[u][e].second;
            long long nd = d + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                pq.push(P(nd, v));
            }
        }
    }
    for (int i = 1; i <= n; i++) {
        if (dist[i] == INF) cout << "INF" << '\n';
        else cout << dist[i] << '\n';
    }
    return 0;
}
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

- 인접 리스트 `vector<vector<pair<int,int>>> graph`를 일방통행 방향으로만 채운다.
- `dist[s] = 0`, `pq.push({0, s})`에서 시작해 pop → 낡은 항목 필터 → 이웃 완화·push.
- 끝나면 `dist`를 1..N 순서로 출력하되, `INF`로 남은 정점은 문자열 `INF`.

(3) 스스로 다시 짤 때 생각 순서

- "출발점 하나 + 가중치 >= 0" → Dijkstra 뼈대(힙·지연 삭제·완화) 세 줄을 먼저 쓴다. 그 첫 줄에서 `greater<>`를 잊지 않는 것이 C++에서 가장 자주 나는 실수다(파이썬 `heapq`는 기본이 최소 힙이라 정반대 습관이 붙어 있다).
- 방향성(일방통행)과 다중 간선(그대로 넣어도 완화가 알아서 처리)을 입력 단계에서 확인한다.
- 거리 합의 상한(10^4개 간선 × 10^4)은 `int`에 들어가지만, 습관적으로 `long long`을 쓰면 문제가 커져도 그대로 통한다. 출력 규칙(도달 불가 표기, 자기 자신 0)을 마지막에 맞춘다. 복잡도 O((N+M) log N).
```

**2) 본사에서 가장 먼 지점 개수** · Easy

- **요구사항**: 양방향 도로로 연결된 지점 N개가 있다. 본사(지점 1)에서 **도달 가능한** 지점들 중, 최단 거리가 **가장 먼** 지점이 몇 개인지 구하라(본사 자신도 거리 0인 후보로 포함).
- **입력**: 첫 줄 `N M`(1 ≤ N ≤ 10^4, 0 ≤ M ≤ 10^5), 이후 M줄 `u v w`(양방향, 1 ≤ w ≤ 10^4).
- **출력**: `최대거리 개수`를 공백으로 한 줄에.
- **예제**: `6 6 / 1 2 3 / 1 3 1 / 3 2 1 / 2 4 4 / 3 5 6 / 4 6 1` → `7 2` · `3 1 / 2 3 4` → `0 1`
- **셀프체크**: 먼저 Dijkstra로 `dist`를 채운 뒤, `INF`가 아닌 값들의 최댓값과 그 값의 등장 횟수를 센다. 예제1: 1→3(1)→2(2)→4(6)→6(7), 3→5(6+1=7)이므로 거리 7이 두 개(5, 6). 도달 불가 정점을 최댓값 계산에 넣으면 `1e18`이 답이 되니 반드시 걸러야 한다. 아무 도로도 없으면 본사만 남아 `0 1`(예제2). 두 값을 한 줄에 낼 때 `cout << far << ' ' << cnt << '\n';`처럼 구분자를 직접 넣는다 — C++에는 파이썬 `print(a, b)`처럼 자동으로 공백을 끼워 주는 기능이 없다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;
typedef pair<long long, int> P;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int, int>>> graph(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        graph[u].push_back(make_pair(v, w));
        graph[v].push_back(make_pair(u, w));   // 양방향
    }
    const long long INF = 1e18;
    vector<long long> dist(n + 1, INF);
    dist[1] = 0;
    priority_queue<P, vector<P>, greater<>> pq;
    pq.push(P(0, 1));
    while (!pq.empty()) {
        long long d = pq.top().first;
        int u = pq.top().second;
        pq.pop();
        if (d > dist[u]) continue;
        for (size_t e = 0; e < graph[u].size(); e++) {
            int v = graph[u][e].first, w = graph[u][e].second;
            long long nd = d + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                pq.push(P(nd, v));
            }
        }
    }
    long long far = 0;
    int cnt = 0;
    for (int i = 1; i <= n; i++) {
        if (dist[i] == INF) continue;          // 도달 불가는 후보에서 제외
        if (dist[i] > far) {
            far = dist[i];
            cnt = 1;
        } else if (dist[i] == far) {
            cnt++;
        }
    }
    cout << far << ' ' << cnt << '\n';
    return 0;
}
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

- 양방향 간선을 두 방향으로 `push_back` 하고 정점 1에서 Dijkstra.
- `far = 0, cnt = 0`으로 시작해 1..N을 보며, `INF`는 건너뛰고 더 크면 `far` 갱신·`cnt = 1`, 같으면 `cnt++`.
- `far`와 `cnt` 사이에 공백을 직접 넣어 한 줄로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "최단 거리로 가장 먼 것" → Dijkstra 후 집계라는 두 단계로 나눈다.
- 집계에서 INF 제외, 본사 포함(거리 0) 규칙을 먼저 정한다. `far`를 `INF`로 초기화하는 실수를 하지 않도록 "최댓값 찾기는 0(또는 -1)에서 시작"을 기억한다.
- 경계: 도로가 없으면 `0 1`, 여러 정점이 같은 최대 거리(예제3).
```

**3) 최단 배송 경로 복원** · Medium

- **요구사항**: 일방통행 가중 그래프에서 S→T 최단 거리와 **그 경로(정점 나열)** 를 출력하라. 입력은 **S→T 최단 경로가 유일**하도록 주어진다. 도달할 수 없으면 `-1` 한 줄만.
- **입력**: 첫 줄 `N M S T`(1 ≤ N ≤ 10^4, 0 ≤ M ≤ 10^5), 이후 M줄 `u v w`(u→v, 1 ≤ w ≤ 10^4).
- **출력**: 첫 줄 최단 거리, 둘째 줄 S부터 T까지의 정점을 공백으로. S=T면 거리 0과 정점 하나.
- **예제**: `5 6 1 5 / 1 2 2 / 1 3 5 / 2 3 1 / 3 4 2 / 2 4 6 / 4 5 1` → `6 / 1 2 3 4 5` · `4 3 1 4 / 1 2 1 / 2 3 1 / 4 3 1` → `-1`
- **셀프체크**: 완화가 일어나는 순간(`nd < dist[v]`)에 `parent[v] = u`를 기록하면, 마지막에 남은 `parent`는 최단 경로 트리다. T에서 `parent`를 따라 S까지 거슬러 올라가 `vector`에 담은 뒤 `reverse`한다. 예제1: 1→2(2)→3(3)→4(5)→5(6). `dist[T]`가 INF면 경로 복원을 시도하지 말고 -1(그대로 두면 `parent`가 0이라 정점 0을 밟으며 무한 루프에 빠진다). S=T면 역추적 루프가 한 번도 돌지 않으므로 S 하나만 출력되는지 확인. 마지막 정점 뒤에 공백이 붙지 않도록 구분자를 인덱스로 제어한다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;
typedef pair<long long, int> P;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, s, t;
    cin >> n >> m >> s >> t;
    vector<vector<pair<int, int>>> graph(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        graph[u].push_back(make_pair(v, w));
    }
    const long long INF = 1e18;
    vector<long long> dist(n + 1, INF);
    vector<int> parent(n + 1, 0);
    dist[s] = 0;
    priority_queue<P, vector<P>, greater<>> pq;
    pq.push(P(0, s));
    while (!pq.empty()) {
        long long d = pq.top().first;
        int u = pq.top().second;
        pq.pop();
        if (d > dist[u]) continue;
        for (size_t e = 0; e < graph[u].size(); e++) {
            int v = graph[u][e].first, w = graph[u][e].second;
            long long nd = d + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                parent[v] = u;                 // 완화 순간에 직전 정점 기록
                pq.push(P(nd, v));
            }
        }
    }
    if (dist[t] == INF) {                      // 역추적보다 먼저 판정
        cout << -1 << '\n';
        return 0;
    }
    vector<int> path;
    int v = t;
    while (v != s) {                           // T에서 거꾸로 따라감
        path.push_back(v);
        v = parent[v];
    }
    path.push_back(s);
    reverse(path.begin(), path.end());
    cout << dist[t] << '\n';
    for (size_t i = 0; i < path.size(); i++) {
        if (i) cout << ' ';
        cout << path[i];
    }
    cout << '\n';
    return 0;
}
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
- `v = t`에서 `v != s`인 동안 `path.push_back(v)`, `v = parent[v]`, 마지막에 s를 붙이고 `reverse(path.begin(), path.end())`.
- 거리와 경로를 두 줄로 출력. 경로는 `if (i) cout << ' ';`로 앞에 구분자를 붙여 끝에 여분의 공백이 남지 않게 한다.

(3) 스스로 다시 짤 때 생각 순서

- "경로도 출력"을 보면 `parent` 배열 한 줄 추가를 떠올린다(완화 안에서만 기록).
- 도달 불가 판정을 역추적보다 먼저 한다. C++에서는 `parent[v] = 0`인 채로 올라가면 `parent[0] = 0`이라 while이 영원히 돌거나, 인덱스 범위를 벗어나 정의되지 않은 동작이 된다.
- 경계: S=T(경로가 정점 하나), 유일성이 깨지면 정답이 여럿이 되므로 문제 조건을 확인한다.
```

**4) 격자 최소 통행료** · Medium

- **요구사항**: N×M 격자의 각 칸에 통행료(0~9)가 적혀 있다. 왼쪽 위 (0,0)에서 출발해 오른쪽 아래 (N-1,M-1)까지 **상하좌우 4방향**으로 이동한다. 지나는 모든 칸(출발 칸 포함)의 통행료 합을 최소화하라.
- **입력**: 첫 줄 `N M`(1 ≤ N, M ≤ 100), 이후 N줄에 M개의 정수(0~9).
- **출력**: 최소 통행료 합.
- **예제**: `3 4 / 2 8 3 1 / 1 1 9 1 / 6 1 1 1` → `7` · `5 3 / 1 1 1 / 9 9 1 / 1 1 1 / 1 9 9 / 1 1 1` → `11`
- **셀프체크**: 오른쪽·아래로만 간다면 DP지만, 4방향이면 위·왼쪽으로 되돌아가는 경로가 더 쌀 수 있어(예제2는 뱀처럼 왼쪽으로 돌아가야 11, 우·하만 쓰면 15) **격자를 그래프로 보고 Dijkstra**를 돌린다. 정점 = 칸, 간선 비용 = 들어가는 칸의 값, `dist[0][0] = grid[0][0]`으로 시작. 힙 원소는 `tuple<int,int,int>`(비용, r, c)로 두면 `greater<>`가 사전식으로 비교해 비용 우선이 된다. 범위 검사 `0 <= nr && nr < n`을 빠뜨리면 `vector`의 `[]`는 검사를 하지 않으므로 조용히 메모리를 밟는다(파이썬처럼 예외가 나지 않는다).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;
typedef tuple<int, int, int> T;         // (비용, r, c)

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> grid(n, vector<int>(m));
    for (int r = 0; r < n; r++)
        for (int c = 0; c < m; c++) cin >> grid[r][c];
    const int INF = 1e9;
    vector<vector<int>> dist(n, vector<int>(m, INF));
    dist[0][0] = grid[0][0];            // 출발 칸 비용 포함
    priority_queue<T, vector<T>, greater<>> pq;
    pq.push(T(grid[0][0], 0, 0));
    int dr[4] = {1, -1, 0, 0};
    int dc[4] = {0, 0, 1, -1};
    while (!pq.empty()) {
        int d, r, c;
        tie(d, r, c) = pq.top();
        pq.pop();
        if (d > dist[r][c]) continue;
        if (r == n - 1 && c == m - 1) break;      // 목표 칸이 확정되면 종료
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;   // 범위 검사 필수
            int nd = d + grid[nr][nc];
            if (nd < dist[nr][nc]) {
                dist[nr][nc] = nd;
                pq.push(T(nd, nr, nc));
            }
        }
    }
    cout << dist[n - 1][m - 1] << '\n';
    return 0;
}
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

- 격자를 `vector<vector<int>>`로 읽고 `dist`를 INF(여기서는 값이 최대 100×100×9라 `1e9`면 충분)로 채운다.
- 힙에 `(비용, r, c)` 튜플을 넣고 `tie(d, r, c) = pq.top();`로 꺼낸다 → 지연 삭제 → 목표 칸이면 종료(그 순간 확정).
- 네 방향 이웃 중 범위 안인 칸을 `d + grid[nr][nc]`로 완화·push.
- `dist[n-1][m-1]` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "격자 + 칸마다 비용 + 4방향"을 보면 BFS(균일 비용)가 아니라 Dijkstra임을 떠올린다.
- 출발 칸 비용 포함 여부를 문제에서 확인해 초기값을 정한다.
- C++ `vector`의 `[]`에는 경계 검사가 없다. 음수 인덱스가 예외가 아니라 **정의되지 않은 동작**이므로 이동 전에 네 조건을 모두 적는다.
- 경계: 1×1 격자(출발=도착), 되돌아가야 싼 뱀 모양 경로(예제2)로 DP 대비 검산.
```

**5) 충전소를 거치는 전기차 최단 경로** · Medium

- **요구사항**: 양방향 도로로 연결된 도시 N곳이 있다. 전기차는 배터리 용량이 C이고, 도로 하나를 지나면 길이 w만큼 배터리가 소모된다(남은 배터리가 w 미만이면 그 도로를 지날 수 없다). 일부 도시에는 충전소가 있어 도착하면 **즉시 C까지 완충**된다(비용 없음). 완충 상태로 도시 1에서 출발해 도시 N에 도착하는 **최소 총 이동 거리**를 구하라. 불가능하면 -1.
- **입력**: 첫 줄 `N M C K`(1 ≤ N ≤ 10^3, 0 ≤ M ≤ 10^4, 1 ≤ C ≤ 20, 1 ≤ K ≤ N), 둘째 줄 충전소 도시 번호 K개, 이후 M줄 `u v w`(양방향, 1 ≤ w ≤ C).
- **출력**: 최소 이동 거리 또는 -1.
- **예제**: `4 4 5 1 / 2 / 1 2 3 / 2 3 3 / 1 3 7 / 3 4 2` → `8` · `4 4 5 1 / 4 / 1 2 3 / 2 3 3 / 1 3 7 / 3 4 2` → `-1`
- **셀프체크**: 상태를 `(도시, 남은 배터리)`로 두고 `dist[u][f]`(= `vector<vector<long long>>`)를 관리한다(C ≤ 20이라 상태 수가 작다). 간선 `w > f`면 이동 불가, 도착 도시가 충전소면 `nf = C`, 아니면 `nf = f - w`. 답은 `dist[N]` 행 전체의 최솟값(`*min_element(dist[n].begin(), dist[n].end())`). 예제1: 1→3 직행(7)은 배터리 5로 불가, 1→2(충전)→3→4 = 8. 예제2: 충전소가 도착지뿐이라 3에 도달할 수 없어 -1. `visited` 배열로 정점 재방문을 막으면 "같은 도시, 다른 배터리"를 놓치니 지연 삭제만 쓴다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;
typedef tuple<long long, int, int> T;   // (거리, 도시, 남은 배터리)

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, cap, k;
    cin >> n >> m >> cap >> k;
    vector<char> station(n + 1, 0);
    for (int i = 0; i < k; i++) {
        int c;
        cin >> c;
        station[c] = 1;
    }
    vector<vector<pair<int, int>>> graph(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        graph[u].push_back(make_pair(v, w));
        graph[v].push_back(make_pair(u, w));
    }
    const long long INF = 1e18;
    // dist[u][f]: 도시 u에 배터리 f 남기고 도달하는 최소 거리
    vector<vector<long long>> dist(n + 1, vector<long long>(cap + 1, INF));
    dist[1][cap] = 0;
    priority_queue<T, vector<T>, greater<>> pq;
    pq.push(T(0, 1, cap));
    while (!pq.empty()) {
        long long d;
        int u, f;
        tie(d, u, f) = pq.top();
        pq.pop();
        if (d > dist[u][f]) continue;
        for (size_t e = 0; e < graph[u].size(); e++) {
            int v = graph[u][e].first, w = graph[u][e].second;
            if (w > f) continue;                    // 배터리 부족 → 이 도로 불가
            int nf = station[v] ? cap : f - w;      // 충전소면 완충
            long long nd = d + w;
            if (nd < dist[v][nf]) {
                dist[v][nf] = nd;
                pq.push(T(nd, v, nf));
            }
        }
    }
    long long ans = *min_element(dist[n].begin(), dist[n].end());
    if (ans == INF) cout << -1 << '\n';
    else cout << ans << '\n';
    return 0;
}
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
- 상태 전이 규칙 두 가지: 배터리가 부족한 도로는 건너뛰고, 충전소에 도착하면 배터리를 C로 되돌린다. 목표는 도시 N에 어떤 배터리로 도착하든 상관없으므로 `dist[N]` 행의 최솟값이 답이다.

(2) 코드 단계별

- 충전소 여부를 `vector<char>`로(`vector<bool>`은 비트 압축 특수화라 원소 참조가 일반 `bool&`가 아니다 — 단순 플래그에는 `char`가 무난하다) 두고 양방향 인접 리스트를 만든다.
- `dist`를 `(n+1) × (cap+1)` 2차원으로 잡고 `dist[1][cap] = 0`, 힙에 `(0, 1, cap)`.
- pop → 지연 삭제 → 각 간선에 대해 `w > f`면 continue, 아니면 `nf`를 계산해 `dist[v][nf]` 완화.
- `*min_element(dist[n].begin(), dist[n].end())`가 INF면 -1.

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
- **셀프체크**: Floyd의 `min/plus` 연산을 행렬 곱처럼 보면, 인접 행렬 A(대각선 0, 간선 w, 없으면 INF)를 K번 "min-plus 곱"한 결과 `A^K[i][j]`가 **간선 K개 이하**로 가는 최소 비용이다(대각선 0이 "제자리"를 허용해 "정확히 K개"가 아니라 "K개 이하"가 된다). 예제1: K=2면 1→2→3→4(간선 3개)는 못 쓰고 직행 10, 예제2는 K=3이라 3. K=0이면 s=t만 0. **삼중 루프 안에서 `A[i][t] + B[t][j]`를 무턱대고 더하면 `1e18 + 1e18`이 `long long`을 넘어 음수가 된다** — 더하기 전에 양쪽이 INF인지 검사한다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;
typedef vector<vector<long long>> Mat;

const long long INF = 1e18;
int n;

Mat minplus(const Mat& A, const Mat& B) {   // C[i][j] = min_t (A[i][t] + B[t][j])
    Mat C(n + 1, vector<long long>(n + 1, INF));
    for (int i = 1; i <= n; i++) {
        for (int t = 1; t <= n; t++) {
            if (A[i][t] >= INF) continue;       // INF + INF 오버플로 방지
            long long ait = A[i][t];
            for (int j = 1; j <= n; j++) {
                if (B[t][j] >= INF) continue;
                if (ait + B[t][j] < C[i][j]) C[i][j] = ait + B[t][j];
            }
        }
    }
    return C;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, k;
    cin >> n >> m >> k;
    Mat adj(n + 1, vector<long long>(n + 1, INF));
    for (int i = 1; i <= n; i++) adj[i][i] = 0;   // "제자리" 허용 → 간선 K개 이하
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        if (w < adj[u][v]) adj[u][v] = w;
    }
    Mat res(n + 1, vector<long long>(n + 1, INF));
    for (int i = 1; i <= n; i++) res[i][i] = 0;   // 간선 0개: 자기 자신만 도달
    for (int step = 0; step < k; step++)
        res = minplus(res, adj);                  // 허용 간선 수를 하나씩 늘림
    int q;
    cin >> q;
    for (int i = 0; i < q; i++) {
        int s, t;
        cin >> s >> t;
        if (res[s][t] >= INF) cout << -1 << '\n';
        else cout << res[s][t] << '\n';
    }
    return 0;
}
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
- `minplus(A, B)`: 삼중 루프로 `min_t A[i][t] + B[t][j]`. `A[i][t]`나 `B[t][j]`가 INF면 건너뛴다 — 이 검사가 없으면 `1e18 + 1e18`이 `long long`(약 9.2×10^18)을 넘어 음수로 감싸며 "INF 경로가 제일 싸다"는 결과가 나온다.
- `res`를 단위 행렬(대각 0, 나머지 INF)로 두고 K번 `res = minplus(res, adj)`.
- 질의마다 `res[s][t]`를 읽어 INF면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "간선 K개 이하"라는 제한을 보면 Floyd의 경유지 루프 대신 "허용 간선 수를 하나씩 늘리는" 반복을 떠올린다.
- 대각선 0의 의미("이하"로 만들어 줌)를 확인하고, K=0(자기 자신만)을 경계로 검산한다.
- INF를 `1e18`처럼 "더해도 안 넘치는" 값으로 잡거나, 아예 더하기 전에 걸러 낸다. `LLONG_MAX`를 INF로 쓰면 한 번의 덧셈으로 바로 무너진다.
- 복잡도 O(K·N^3)이므로 N·K가 작을 때만 쓴다. 큰 행렬을 함수에 넘길 때는 `const Mat&`(참조)로 받아 복사를 피한다.
```

**7) 본부로 갔다 돌아오는 최장 왕복 시간** · Medium

- **요구사항**: 일방통행 도로로 연결된 지점 N곳이 있다. 모든 지점의 직원이 본부 X에 갔다가 **각자 자기 지점으로 돌아온다**(갈 때·올 때 모두 최단 경로, 일방통행이라 두 경로가 다를 수 있다). 왕복 시간이 가장 긴 직원의 왕복 시간을 구하라. 모든 지점에서 왕복이 가능하도록 입력이 주어진다.
- **입력**: 첫 줄 `N M X`(1 ≤ N ≤ 10^3, 0 ≤ M ≤ 10^4), 이후 M줄 `u v w`(u→v, 1 ≤ w ≤ 10^3).
- **출력**: 최장 왕복 시간.
- **예제**: `4 6 1 / 1 2 3 / 2 1 5 / 1 3 1 / 3 4 2 / 4 1 4 / 2 4 1` → `8` · `3 4 3 / 1 3 2 / 3 1 2 / 2 3 1 / 3 2 9` → `10`
- **셀프체크**: "X → 모든 정점"은 X 출발 Dijkstra 한 번. "모든 정점 → X"를 정점마다 Dijkstra로 구하면 N번이라 느리다 — **간선을 뒤집은 그래프**에서 X 출발 Dijkstra 한 번이면 `go[i]` = i→X 최단이다. 답은 `max(go[i] + back[i])`. 예제1: 2번 지점이 갈 때 5(2→1), 올 때 3(1→2)으로 8. 본부 자신은 0이다. 같은 Dijkstra 코드를 그래프만 바꿔 두 번 부르되, 매개변수를 `const vector<vector<pair<int,int>>>&`(참조)로 받아야 인접 리스트가 통째로 복사되지 않는다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;
typedef pair<long long, int> P;
typedef vector<vector<pair<int, int>>> Graph;

const long long INF = 1e18;

vector<long long> dijkstra(const Graph& g, int src, int n) {   // 참조로 받아 복사 방지
    vector<long long> dist(n + 1, INF);
    dist[src] = 0;
    priority_queue<P, vector<P>, greater<>> pq;
    pq.push(P(0, src));
    while (!pq.empty()) {
        long long d = pq.top().first;
        int u = pq.top().second;
        pq.pop();
        if (d > dist[u]) continue;
        for (size_t e = 0; e < g[u].size(); e++) {
            int v = g[u][e].first, w = g[u][e].second;
            long long nd = d + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                pq.push(P(nd, v));
            }
        }
    }
    return dist;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, x;
    cin >> n >> m >> x;
    Graph graph(n + 1), rgraph(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        graph[u].push_back(make_pair(v, w));
        rgraph[v].push_back(make_pair(u, w));      // 역방향 그래프
    }
    vector<long long> go = dijkstra(rgraph, x, n);   // go[i] = i -> x 최단
    vector<long long> back = dijkstra(graph, x, n);  // back[i] = x -> i 최단
    long long best = 0;
    for (int i = 1; i <= n; i++)
        if (go[i] + back[i] > best) best = go[i] + back[i];
    cout << best << '\n';
    return 0;
}
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
- `dijkstra`를 별도 함수로 빼고 그래프를 `const Graph&`로 받는다. 값으로 받으면 호출할 때마다 인접 리스트 전체가 복사돼 시간·메모리를 낭비한다.
- `dijkstra(rgraph, x, n)`으로 각 정점에서 X까지, `dijkstra(graph, x, n)`으로 X에서 각 정점까지의 최단을 구한다.
- 두 배열의 합의 최댓값을 출력한다(왕복 보장이라 INF는 없다).

(3) 스스로 다시 짤 때 생각 순서

- "여러 출발점 → 한 도착점"을 보면 역방향 그래프 트릭을 떠올린다(일방통행일 때만 의미가 있다).
- 같은 Dijkstra 함수를 그래프 인자만 바꿔 두 번 호출하는 구조로 짠다. 반환은 `vector<long long>` 값 복사지만 이동(move)으로 처리돼 비용이 없다.
- 경계: 본부 자신(0), 지점 하나뿐인 그래프(예제3).
```

**8) 필수 방문 지점 K개 최단 순회** · Hard

- **요구사항**: 양방향 가중 그래프에서 지점 1에서 출발해 지점 N에 도착하되, 지정된 **필수 지점 K개를 모두**(순서는 자유, 같은 지점·도로를 여러 번 지나도 됨) 거쳐야 한다. 최소 이동 거리를 구하라. 불가능하면 -1.
- **입력**: 첫 줄 `N M K`(2 ≤ N ≤ 50, 0 ≤ M ≤ 1000, 1 ≤ K ≤ 5), 둘째 줄 필수 지점 K개(서로 다름), 이후 M줄 `u v w`(양방향, 1 ≤ w ≤ 10^4).
- **출력**: 최소 이동 거리 또는 -1.
- **예제**: `5 6 2 / 2 4 / 1 2 1 / 2 3 1 / 3 4 1 / 4 5 1 / 1 4 3 / 2 5 6` → `4` · `4 4 2 / 3 2 / 1 2 1 / 2 3 1 / 3 4 1 / 1 3 5` → `3`
- **셀프체크**: 경로는 `1 → p1 → p2 → ... → pK → N` 조각으로 쪼개지고 각 조각은 최단 경로여도 된다(재방문 허용). Floyd로 모든 쌍 최단거리를 구한 뒤, 필수 지점의 **순서 K!가지**를 전부 시도해 조각 합의 최솟값을 취한다. C++에서는 `sort` 후 `do { ... } while (next_permutation(v.begin(), v.end()));` — **정렬하지 않고 `next_permutation`을 돌리면 현재 순서 이후만 나오므로 일부 순열을 빠뜨린다.** 예제2: 1→2→3→4 = 3이 1→3→2→4 = 5보다 짧다. 어떤 조각이라도 INF면 그 순서는 불가능, 모두 불가능하면 -1. K ≤ 5라 120가지 × K번 덧셈뿐이다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, k;
    cin >> n >> m >> k;
    vector<int> must(k);
    for (int i = 0; i < k; i++) cin >> must[i];
    const long long INF = 1e18;
    vector<vector<long long>> dist(n + 1, vector<long long>(n + 1, INF));
    for (int i = 1; i <= n; i++) dist[i][i] = 0;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        if (w < dist[u][v]) {
            dist[u][v] = w;
            dist[v][u] = w;
        }
    }
    for (int t = 1; t <= n; t++) {              // Floyd: 경유지 t 가 가장 바깥
        for (int i = 1; i <= n; i++) {
            if (dist[i][t] >= INF) continue;    // INF 덧셈 방지
            for (int j = 1; j <= n; j++) {
                if (dist[t][j] >= INF) continue;
                if (dist[i][t] + dist[t][j] < dist[i][j])
                    dist[i][j] = dist[i][t] + dist[t][j];
            }
        }
    }
    sort(must.begin(), must.end());             // next_permutation 전 반드시 정렬
    long long best = INF;
    do {
        long long total = 0;
        int prev = 1;
        bool ok = true;
        for (int i = 0; i < k; i++) {
            if (dist[prev][must[i]] >= INF) { ok = false; break; }
            total += dist[prev][must[i]];
            prev = must[i];
        }
        if (ok && dist[prev][n] < INF) {
            total += dist[prev][n];
            if (total < best) best = total;
        }
    } while (next_permutation(must.begin(), must.end()));
    if (best == INF) cout << -1 << '\n';
    else cout << best << '\n';
    return 0;
}
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
- 조각의 양 끝이 다양한 정점 쌍이므로 모든 쌍 최단거리가 필요하다 → N이 작으니 Floyd-Warshall 한 번. 순서는 K! <= 120가지라 전수 시도해도 된다.

(2) 코드 단계별

- `dist`를 INF/대각 0으로 초기화하고 양방향 간선을 대칭으로(중복은 min) 넣는다.
- 경유지가 **가장 바깥**인 삼중 루프로 모든 쌍 최단거리를 구한다. 루프 순서를 바꾸면(예: i가 바깥) "아직 계산되지 않은 경유지"를 참조하게 되어 답이 틀린다.
- `sort(must...)` 후 `do { ... } while (next_permutation(...))`로 모든 순서를 훑으며 1→…→N 조각 합을 계산한다. 조각 중 하나라도 INF면 그 순서를 버린다(더하지 않으므로 오버플로도 없다).
- 최솟값이 INF면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "반드시 지나야 하는 정점 여러 개 + 순서 자유"를 보면 Floyd + 순열 전수라는 결합을 떠올린다(L2의 경유지 하나 문제의 일반화).
- `next_permutation`은 **사전순으로 다음 순열**을 만들고 마지막(내림차순)에서 `false`를 반환한다. 그래서 오름차순 정렬로 시작해야 K!가지를 모두 본다.
- 조각 합이 정당한 이유(재방문 허용 + 부분 경로 최적성)를 한 줄로 확인한다.
- 경계: 필수 지점이 1 또는 N과 같아도 `dist[x][x] = 0`이라 자연히 처리, 일부 쌍이 단절되면 -1.
```

**9) 열쇠를 모아 잠긴 통로 열기** · Hard

- **요구사항**: 일방통행 통로로 연결된 방 N개가 있다. 일부 방에는 **열쇠**(색 1·2·3 중 하나, 방당 최대 하나)가 놓여 있어 그 방에 들어서는 순간 획득한다(여러 번 들어가도 상관없음). 일부 통로는 색 c의 **자물쇠**가 걸려 있어 같은 색 열쇠가 있어야 지날 수 있다. 방 1에서 출발해(방 1의 열쇠는 출발과 동시에 획득) 방 N에 도착하는 최소 이동 거리를 구하라. 불가능하면 -1.
- **입력**: 첫 줄 `N M`(2 ≤ N ≤ 10^3, 0 ≤ M ≤ 10^4), 둘째 줄 각 방의 열쇠 N개(0=없음, 1~3), 이후 M줄 `u v w c`(u→v, 1 ≤ w ≤ 10^4, c=0이면 자물쇠 없음, 1~3이면 그 색 자물쇠).
- **출력**: 최소 이동 거리 또는 -1.
- **예제**: `4 4 / 0 1 0 0 / 1 4 5 1 / 1 2 1 0 / 2 1 1 0 / 2 4 10 0` → `7` · `3 2 / 0 0 0 / 1 2 1 0 / 2 3 1 2` → `-1`
- **셀프체크**: 상태 = `(방, 가진 열쇠 비트마스크)`, 마스크는 0~7. 간선을 지날 때 `c != 0`이면 `(mask >> (c-1)) & 1`을 검사하고, 도착 방에 열쇠가 있으면 마스크에 비트를 OR 한다. 답은 `dist[N]` 행의 최솟값. 예제1: 1→2(열쇠 1 획득)→1→4(자물쇠 1 열림) = 1+1+5 = 7이 2→4 직행 11보다 짧다 — 열쇠를 가지고 **같은 방으로 되돌아오는** 것이 새로운 상태이므로 `visited`로 막으면 안 된다. 열쇠가 없는 방(0)에서 `1 << (0 - 1)`은 음수 시프트라 **정의되지 않은 동작**이다(파이썬처럼 예외가 나지 않고 아무 값이나 나온다) — 반드시 `key[v] ? ... : mask`로 분기한다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;
typedef tuple<long long, int, int> T;   // (거리, 방, 열쇠 마스크)

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> key(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> key[i];
    // 간선: (v, w, c)
    vector<vector<tuple<int, int, int>>> graph(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v, w, c;
        cin >> u >> v >> w >> c;
        graph[u].push_back(make_tuple(v, w, c));
    }
    const long long INF = 1e18;
    const int S = 8;                    // 열쇠 3종 → 비트마스크 0..7
    vector<vector<long long>> dist(n + 1, vector<long long>(S, INF));
    int start = key[1] ? (1 << (key[1] - 1)) : 0;   // 음수 시프트 금지
    dist[1][start] = 0;
    priority_queue<T, vector<T>, greater<>> pq;
    pq.push(T(0, 1, start));
    while (!pq.empty()) {
        long long d;
        int u, mask;
        tie(d, u, mask) = pq.top();
        pq.pop();
        if (d > dist[u][mask]) continue;
        for (size_t e = 0; e < graph[u].size(); e++) {
            int v, w, c;
            tie(v, w, c) = graph[u][e];
            if (c && !((mask >> (c - 1)) & 1)) continue;   // 잠긴 통로인데 열쇠 없음
            int nmask = key[v] ? (mask | (1 << (key[v] - 1))) : mask;
            long long nd = d + w;
            if (nd < dist[v][nmask]) {
                dist[v][nmask] = nd;
                pq.push(T(nd, v, nmask));
            }
        }
    }
    long long ans = *min_element(dist[n].begin(), dist[n].end());
    if (ans == INF) cout << -1 << '\n';
    else cout << ans << '\n';
    return 0;
}
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

- 어떤 통로를 지날 수 있는지가 "지금까지 모은 열쇠"에 달려 있으므로, 정점에 열쇠 집합을 얹은 `(방, 마스크)`가 진짜 상태다. 열쇠는 3종이라 마스크는 8가지뿐이고, 상태 간 이동 비용은 통로 길이(>= 0)이므로 Dijkstra가 성립한다.
- 열쇠는 잃지 않으므로 마스크는 커지기만 한다. 같은 방이라도 마스크가 다르면 다른 상태이므로, 열쇠를 얻은 뒤 왔던 방으로 돌아가는 경로(예제1)가 자연스럽게 허용된다.

(2) 코드 단계별

- 각 방의 열쇠와 `(v, w, c)` 방향 간선을 `tuple<int,int,int>`로 읽는다. 꺼낼 때는 `tie(v, w, c) = ...`로 한 번에 푼다.
- 출발 상태의 마스크는 방 1의 열쇠(있으면 비트 하나). `dist[1][start] = 0`.
- pop → 지연 삭제 → 간선마다 자물쇠 검사(`c`가 0이 아니고 비트가 없으면 skip) → 도착 방 열쇠를 OR 한 `nmask`로 완화.
- `dist[n]` 행의 최솟값이 INF면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "특정 정점을 거쳐야만 열리는 간선"을 보면 상태를 비트마스크로 얹는 Dijkstra를 떠올린다(열쇠 종류 수가 작은지 먼저 확인).
- 전이 규칙을 "통과 조건"과 "상태 갱신" 두 줄로 분리해 적는다.
- 시프트 폭은 항상 0 이상이어야 한다. `1 << (key - 1)`을 쓰기 전에 `key`가 0인지 반드시 분기한다 — C++에서 음수 시프트는 예외가 아니라 정의되지 않은 동작이라 디버깅이 어렵다.
- 경계: 출발 방에 열쇠가 있는 경우, 열쇠가 도착 방에만 있어 소용없는 경우(-1), 자물쇠 없는 단순 경로(예제4). 복잡도 O(8·M log(8·N)).
```

**10) 합배송 후 분기 최소 비용** · Hard

- **요구사항**: 양방향 도로로 연결된 도시 N곳이 있다. 물류 센터 S에서 두 고객 A, B에게 보낼 상품을 트럭 한 대가 **어느 도시 P까지 함께 싣고 간 뒤**, P에서 두 배송원이 각각 A와 B로 따로 이동한다(P는 S·A·B를 포함한 어떤 도시여도 되고, 함께 가는 구간이 없어도 된다). 총 이동 비용 `S→P + P→A + P→B`의 최솟값을 구하라. 불가능하면 -1.
- **입력**: 첫 줄 `N M`(1 ≤ N ≤ 200, 0 ≤ M ≤ 5000), 둘째 줄 `S A B`, 이후 M줄 `u v w`(양방향, 1 ≤ w ≤ 10^5).
- **출력**: 최소 총 비용 또는 -1.
- **예제**: `5 6 / 1 4 5 / 1 2 3 / 2 3 2 / 3 4 4 / 3 5 4 / 2 4 8 / 2 5 8` → `13` · `3 2 / 1 2 3 / 1 2 4 / 1 3 4` → `8`
- **셀프체크**: 분기점 P를 정하면 세 조각은 각각 최단 경로여도 된다 → Floyd로 모든 쌍을 구해 두고 `min over P (dist[S][P] + dist[P][A] + dist[P][B])`. 예제1: P=3에서 5+4+4 = 13(따로 가면 P=S로 9+9 = 18). 예제2: 합배송 이득이 없어 P=S가 최선(8). P=A(또는 B)일 때 `dist[A][A] = 0`이라 자연히 "한 명은 이미 도착" 경우가 포함된다. 어떤 P든 조각 하나가 INF면 그 P는 불가 — **세 INF를 그대로 더하면 `long long`을 넘으므로 더하기 전에 검사한다.** Floyd 삼중 루프에서 `k`가 가장 바깥이어야 한다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    int s, a, b;
    cin >> s >> a >> b;
    const long long INF = 1e18;
    vector<vector<long long>> dist(n + 1, vector<long long>(n + 1, INF));
    for (int i = 1; i <= n; i++) dist[i][i] = 0;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        if (w < dist[u][v]) {
            dist[u][v] = w;
            dist[v][u] = w;                     // 양방향
        }
    }
    for (int k = 1; k <= n; k++) {              // Floyd: 경유지 k 가 가장 바깥
        for (int i = 1; i <= n; i++) {
            if (dist[i][k] >= INF) continue;
            for (int j = 1; j <= n; j++) {
                if (dist[k][j] >= INF) continue;
                if (dist[i][k] + dist[k][j] < dist[i][j])
                    dist[i][j] = dist[i][k] + dist[k][j];
            }
        }
    }
    long long best = INF;
    for (int p = 1; p <= n; p++) {              // 분기점 전수
        if (dist[s][p] >= INF || dist[p][a] >= INF || dist[p][b] >= INF) continue;
        long long cost = dist[s][p] + dist[p][a] + dist[p][b];
        if (cost < best) best = cost;
    }
    if (best == INF) cout << -1 << '\n';
    else cout << best << '\n';
    return 0;
}
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
- 세 조각의 끝점 조합이 다양하므로 모든 쌍 최단거리가 필요 → N <= 200이면 Floyd-Warshall O(N^3)이 간단하다. 양방향 그래프라 `dist[P][A] = dist[A][P]`이므로 방향은 신경 쓰지 않아도 된다.

(2) 코드 단계별

- `dist`를 INF/대각 0으로 초기화하고 양방향 간선을 대칭으로(중복은 min) 넣는다.
- **경유지 `k`가 가장 바깥**인 삼중 루프로 모든 쌍 최단거리를 계산한다. `k`를 안쪽에 두면 "k까지만 경유한 최단"이라는 불변식이 깨져 결과가 틀린다.
- P를 1..N 전부 돌며 세 조각 합의 최솟값을 구한다. 조각 중 하나라도 INF면 그 P를 건너뛴다(더하면 `1e18 × 3`이 `long long`을 넘어 음수가 되고, 그 P가 최적으로 뽑힌다).
- 최솟값이 INF면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "어딘가까지 같이 가다 갈라진다"는 구조를 보면 분기점 P를 전수 조사 + 조각별 최단으로 분해한다.
- 조각이 여러 쌍을 잇는 순간 all-pairs(Floyd)를 선택한다(N이 크면 S, A, B 세 출발점 Dijkstra로 대체 가능).
- Floyd를 쓸 때마다 "k가 가장 바깥"과 "INF 덧셈 방지" 두 가지를 고정 습관으로 붙인다.
- 경계: 함께 가는 구간이 없는 경우(P=S), 한 명이 이미 도착한 경우(P=A), S=A=B(0), 단절(-1).
```
