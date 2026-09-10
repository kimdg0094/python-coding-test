## L5. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터는 도구 하나와 그 도구로 만든 알고리즘 둘로 되어 있다. **유니온-파인드**는 "이 둘이 이미 이어져 있나"를 거의 상수 시간에 답하는 부품이고, **크루스칼**은 그 부품에 정렬을 얹은 것, **프림**은 같은 컷 성질을 정점 쪽에서 적용한 것이다. 셋의 관계와 갈림길을 아래 지도로 못 박는다.

**개념 지도**

```text
  Ch02 map : connectivity first, spanning tree second

  disjoint set (union-find)
   |    parent[] + rnk[] (or sz[])
   |    find  : walk up to the root, then compress the path
   |    unite : hang the shorter root under the taller one
   |    cost  : O(alpha(V)) amortized -> treat it as O(1)
   |
   +-- used alone
   |     same group ?        find(a) == find(b)
   |     group count         V minus the number of successful unions
   |     cycle detection     unite(a, b) returns false
   |     offline queries     process merges in the given order
   |
   +-- used inside Kruskal
         "does this edge join two different components ?"

  minimum spanning tree : V-1 edges, no cycle, minimum total weight
   |    cut property : the cheapest edge crossing any cut is safe
   |
   +-- Kruskal      edge driven    sort + union-find    O(E log E)
   |                  edge list given, sparse graph
   |
   +-- Prim (heap)  vertex driven  one growing tree     O(E log V)
   |                  adjacency list, sparse to medium
   |
   +-- Prim (array) vertex driven  scan keys, no heap   O(V^2)
                      dense or complete graph built from points
```

MST 뼈대는 하나인데, 비교 방향과 멈추는 시점만 바꾸면 다른 문제가 된다.

```text
  same loop, different twist

  minimum spanning tree     sort ascending, stop at V-1 edges
  maximum spanning tree     sort descending, everything else same
  k clusters                keep only the first V-k accepted edges
  edges already built       unite them first (cost 0), then run
  bottleneck path u..v      the w that first connects u and v
  is edge e in some MST ?   compare against the path max in the MST
```

두 알고리즘의 진행 모양이 다르다는 점이 선택의 감각을 만든다.

```text
  Kruskal : many islands appear first, then they merge

     step 1    {0,1}   {2}   {3}   {4}
     step 2    {0,1,2}   {3}   {4}
     step 4    {0,1,2,3,4}

  Prim : never more than one island, it only grows

     step 1    [0]   (1) (2) (3) (4)
     step 2    [0]=[1]   (2) (3) (4)
     step 5    [0]=[1]=[2]=[3]=[4]

  Both obey the cut property, so the total weight is always equal.
```

C++로 옮길 때 언어 쪽에서 새로 생기는 함정은 딱 네 갈래다.

```text
  what C++ adds on top of the algorithm

  overflow      total of E edges : long long , never int
  comparator    sort needs a STRICT weak order : use < , never <=
  heap default  priority_queue is a MAX heap : add greater<> for Prim
  recursion     recursive find blows the 1MB stack with no message
```

**뼈대 코드**

1) 유니온-파인드 — 경로 압축 + union by rank

```cpp
#include <bits/stdc++.h>
using namespace std;

int n;                                      // 원소 개수는 문제마다 바뀜
vector<int> parent, rnk;                    // rnk = 트리 높이의 상한
int groups;                                 // 남은 그룹 수

void initDsu(int sz_) {
    n = sz_;
    parent.resize(n + 1);
    rnk.assign(n + 1, 0);
    iota(parent.begin(), parent.end(), 0);  // parent[i] = i  (<numeric>)
    groups = n;
}

int find(int x) {                           // 반복 버전 — 스택이 터질 일이 없다
    int root = x;
    while (parent[root] != root) root = parent[root];   // 1) 뿌리까지
    while (parent[x] != root) {                          // 2) 지나온 길 압축
        int nx = parent[x];
        parent[x] = root;                                // 대입해야 압축이 남는다
        x = nx;
    }
    return root;
}

bool unite(int a, int b) {
    int ra = find(a), rb = find(b);         // 반드시 '뿌리끼리' 붙인다
    if (ra == rb) return false;             // 이미 같은 그룹 -> 붙이면 사이클
    if (rnk[ra] < rnk[rb]) swap(ra, rb);    // 낮은 트리를 높은 트리 밑으로
    parent[rb] = ra;
    if (rnk[ra] == rnk[rb]) rnk[ra]++;      // 높이가 같을 때만 1 올라간다
    groups--;
    return true;                            // 실제로 합쳐졌다
}
```

2) 크루스칼 — 정렬 + 유니온-파인드

```cpp
struct Edge { long long w; int a, b; };     // 가중치를 맨 앞에 두는 편이 안전

vector<Edge> e(m);                          // 간선 수·입력 형식은 문제마다 바뀜
for (int i = 0; i < m; i++)
    cin >> e[i].a >> e[i].b >> e[i].w;

sort(e.begin(), e.end(),                    // 최대 신장 트리면 a.w > b.w
     [](const Edge& x, const Edge& y) { return x.w < y.w; });   // '<' 만 쓴다

long long total = 0;                        // 누적은 반드시 long long
int cnt = 0;
vector<Edge> used;                          // MST 간선 목록이 필요할 때만
for (const Edge& ed : e) {
    if (unite(ed.a, ed.b)) {                // 다른 컴포넌트일 때만 true
        total += ed.w;
        cnt++;
        used.push_back(ed);
        if (cnt == n - 1) break;            // V-1개 모으면 더 볼 필요 없음
    }
}
cout << (cnt == n - 1 ? total : -1) << "\n";   // 못 채우면 비연결
```

3) 프림 — priority_queue 버전(희소~중간 밀도)

```cpp
// adj[u] = {(도착정점 v, 가중치 w), ...}
long long primHeap(int n, const vector<vector<pair<int,long long>>>& adj,
                   int start = 1) {
    vector<char> visited(n + 1, 0);
    priority_queue<pair<long long,int>,
                   vector<pair<long long,int>>, greater<>> pq;   // 최소 힙
    pq.push({0, start});                    // 시작 정점 진입 비용은 0
    long long total = 0;
    int cnt = 0;
    while (!pq.empty() && cnt < n) {
        auto [w, u] = pq.top(); pq.pop();   // 복사한 뒤에 pop 한다
        if (visited[u]) continue;           // 지연 삭제: 꺼낸 직후에 검사
        visited[u] = 1;
        total += w;
        cnt++;
        for (const auto& [v, wv] : adj[u])
            if (!visited[v]) pq.push({wv, v});   // 키는 w (dist + w 가 아니다)
    }
    return cnt == n ? total : -1;           // 다 못 넣으면 비연결
}
```

4) 프림 — O(V²) 배열 버전(밀집·완전 그래프)

```cpp
// cost[u][v] = 가중치, 간선이 없으면 INF
long long primDense(int n, const vector<vector<long long>>& cost) {
    const long long INF = LLONG_MAX / 4;    // memset 으로는 만들 수 없다
    vector<long long> key(n, INF);          // 트리에 붙이는 최소 간선 비용
    vector<char> used(n, 0);
    key[0] = 0;                             // 시작 정점은 아무거나
    long long total = 0;
    for (int t = 0; t < n; t++) {
        int u = -1;
        for (int i = 0; i < n; i++)         // 안 쓴 것 중 key 최소를 선형 탐색
            if (!used[i] && (u == -1 || key[i] < key[u])) u = i;
        if (key[u] >= INF) return -1;       // 닿을 수 있는 정점이 없다 = 비연결
        used[u] = 1;
        total += key[u];
        for (int v = 0; v < n; v++)         // 새 정점 기준으로 key 갱신
            if (!used[v] && cost[u][v] < key[v]) key[v] = cost[u][v];
    }
    return total;                           // 힙도 정렬도 필요 없다
}
```

5) 최소 병목 경로 — s에서 t까지 "가장 큰 간선"을 최소화

```cpp
sort(e.begin(), e.end(),
     [](const Edge& x, const Edge& y) { return x.w < y.w; });
long long answer = -1;
for (const Edge& ed : e) {
    unite(ed.a, ed.b);
    if (find(s) == find(t)) {               // 질의 쌍 (s, t)는 문제마다 바뀜
        answer = ed.w;                      // 처음 이어지는 순간의 간선이 답
        break;
    }
}
cout << answer << "\n";                     // s == t 는 루프 전에 0으로 처리
```

6) k개 군집 분할 · 최대 신장 트리 · 이미 놓인 간선

```cpp
// (1) k개 군집: MST 간선을 오름차순으로 모으되 앞에서 n-k개만 더한다
sort(e.begin(), e.end(),
     [](const Edge& x, const Edge& y) { return x.w < y.w; });
int picked = 0;
long long total = 0;
for (const Edge& ed : e) {
    if (unite(ed.a, ed.b)) {
        picked++;
        if (picked <= n - k) total += ed.w;   // 비싼 k-1개는 자동으로 잘린다
    }
}
cout << (picked == n - 1 ? total : -1) << "\n";

// (2) 최대 신장 트리: 비교 방향만 뒤집는다
sort(e.begin(), e.end(),
     [](const Edge& x, const Edge& y) { return x.w > y.w; });
// 이후 채택 루프는 크루스칼과 한 글자도 다르지 않다

// (3) 일부 간선이 이미 건설됨: 그것부터 합치고 시작 (비용 0으로 미리 채택한 셈)
for (const auto& [a, b] : prebuilt) unite(a, b);
```

**언제 무엇을 쓰나**

먼저 "이 문제가 MST인가, 아니면 연결성 질의로 끝나는가"를 가른다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 연결 여부·그룹 수만 묻는다(간선 추가만) | 유니온-파인드 단독 | 신장 트리를 만들 이유가 없다 | O(m·α(V)) |
| 간선을 넣다가 사이클이 되는 순간을 찾는다 | 유니온-파인드 단독 | `unite`가 `false`를 돌려주는 시점 | O(m·α(V)) |
| "합쳐라 / 같은 그룹인가"가 섞여 들어온다 | 유니온-파인드 단독 | 온라인 질의를 그대로 처리 | 질의당 사실상 O(1) |
| 간선 목록이 주어진 희소 그래프의 MST | 크루스칼 | 정렬 한 번이면 끝, 코드가 가장 짧다 | O(E log E) |
| 간선이 이미 가중치순으로 들어온다 | 크루스칼(정렬 생략) | 지배항인 정렬이 사라진다 | O(E·α(V)) |
| 인접 리스트가 주어진 중간 밀도 그래프 | 힙 프림 | 간선 전부를 정렬하지 않아도 된다 | O(E log V) |
| 좌표 V개로 만든 완전 그래프(E ≈ V²) | 배열 프림 | 간선 나열·정렬 비용 O(V² log V)를 피한다 | O(V²) |
| V ≤ 약 1000인 인접 행렬 입력 | 배열 프림 | 힙 없이도 충분히 빠르고 구현이 단순 | O(V²) |
| 일부 도로가 이미 놓여 있다 | 미리 `unite` 후 크루스칼 | 비용 0 간선을 먼저 채택한 것과 같다 | O(E log E) |
| 최대 신장 트리 | 내림차순 크루스칼 | 컷 성질이 부호를 뒤집어도 성립 | O(E log E) |
| s–t 경로의 최대 간선을 최소화 | 오름차순 크루스칼 | 처음 이어지는 순간의 w가 곧 답 | O(E log E) |
| 정확히 k개 군집으로 나눈다 | MST 간선 앞 V-k개 | 비싼 간선 k-1개를 끊는 것과 동치 | O(E log E) |
| 그래프가 연결인지 함께 판정 | 채택 간선 수 검사 | V-1개를 못 채우면 비연결 | 추가 비용 없음 |
| 간선 "삭제"가 섞여 있다 | 질의를 역순으로 처리 | 유니온-파인드는 분리를 지원하지 않는다 | O((E+Q)·α(V)) |

**크루스칼 vs 프림 — 무엇을 보고 고르나**

| 판단 기준 | 크루스칼 | 힙 프림 | 배열 프림 |
| --- | --- | --- | --- |
| 입력 형태 | 간선 목록 `(u, v, w)` | 인접 리스트 | 인접 행렬 · 좌표 |
| 지배 비용 | 정렬 O(E log E) | 힙 O(E log V) | 선형 탐색 O(V²) |
| 밀도가 희소(E ≈ V) | **가장 유리** | 비슷 | 불리 |
| 밀도가 중간(E ≈ V log V) | 비슷 | **가장 유리** | 불리 |
| 밀도가 밀집(E ≈ V²) | 불리(정렬이 V² log V) | 애매 | **가장 유리** |
| 좌표 완전 그래프 | 간선 O(V²)을 만들어야 함 | 간선 O(V²)을 만들어야 함 | **간선을 안 만들어도 됨** |
| 필요한 부품 | `sort` + 유니온-파인드 | `priority_queue` | 배열 두 개뿐 |
| C++ 주의점 | 비교자는 `<`, 누적은 `long long` | `greater<>` 없으면 최대 힙 | INF를 `memset`으로 못 만듦 |
| 비연결 판정 | 채택 간선 < V-1 | 편입 정점 < V | `key[u]`가 INF |
| 간선 목록이 필요한가 | 채택 간선을 그대로 모으면 됨 | 부모 배열을 따로 기록 | 부모 배열을 따로 기록 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 유니온-파인드가 각 그룹을 "대표원소를 뿌리로 하는 트리"로 표현한다는 것과, 그래서 `find`가 무엇을 반환하는지.
- [ ] 설명할 수 있다: 경로 압축이 왜 "비싼 탐색이 스스로를 없애는" 최적화인지.
- [ ] 설명할 수 있다: union by rank/size만으로도 트리 높이가 왜 `log2 V` 이하인지.
- [ ] 설명할 수 있다: 두 최적화를 합쳤을 때의 α(V)가 무슨 뜻이고 왜 상수로 취급해도 되는지.
- [ ] 설명할 수 있다: 왜 원소끼리가 아니라 반드시 뿌리끼리 붙여야 하는지.
- [ ] 설명할 수 있다: MST의 간선이 왜 항상 정확히 V-1개인지.
- [ ] 설명할 수 있다: 컷 성질을 교환 논증으로. 그리고 그것이 왜 크루스칼과 프림 양쪽의 정당성 근거인지.
- [ ] 설명할 수 있다: 크루스칼이 간선을 채택하는 순간이 왜 "어떤 컷의 최소 간선"인지.
- [ ] 설명할 수 있다: 프림의 힙 키가 `w`이고 다익스트라는 `dist[u] + w`인 이유, 그리고 바꿔 쓰면 무엇이 나오는지.
- [ ] 설명할 수 있다: 프림의 지연 삭제가 왜 정당하고, 검사를 꺼낸 직후에 해야 하는 이유.
- [ ] 설명할 수 있다: `E log V`와 `V²`를 비교해 크루스칼·힙 프림·배열 프림을 고르는 기준.
- [ ] 설명할 수 있다: 시작 정점을 바꿔도 프림의 총합이 변하지 않는 이유.
- [ ] 설명할 수 있다: 최소 병목 경로의 답이 왜 MST 위 경로의 최대 간선과 같은지.
- [ ] 설명할 수 있다: k개 군집 문제가 왜 "MST에서 비싼 간선 k-1개 끊기"로 환원되는지.
- [ ] 설명할 수 있다: 비연결 그래프를 어떻게 감지하고, 크루스칼과 프림에서 각각 어느 값으로 판정하는지.
- [ ] 설명할 수 있다: C++에서 `sort` 비교자가 왜 `<=`가 아니라 `<`여야 하는지, 어기면 무슨 일이 생기는지.
- [ ] 설명할 수 있다: 왜 `priority_queue`가 기본으로 최대 힙이고, 프림에 쓰려면 무엇을 붙여야 하는지.
- [ ] 설명할 수 있다: 가중치가 `int`에 들어가는데도 누적 합을 `long long`으로 두어야 하는 이유.

**⚠️ 자주 하는 실수**

**1) `find`에서 경로 압축 결과를 대입하지 않는다**

```cpp
// ❌ 틀린 코드
int find(int x) {
    if (parent[x] == x) return x;
    find(parent[x]);        // 결과를 어디에도 대입하지 않는다
    return parent[x];       // parent[x]는 압축 전 값 그대로
}
```

왜: 재귀가 뿌리를 찾아 돌아오지만 `parent[x]`를 갱신하지 않으므로 트리가 조금도 납작해지지 않는다. 게다가 `return parent[x]`는 뿌리가 아니라 "한 칸 위"를 돌려주므로, 깊이 2 이상에서는 대표원소 자체가 틀린다. `find(a) == find(b)` 판정이 무너져 사이클을 못 잡는다.

```cpp
// ✅ 고친 코드
int find(int x) {
    int root = x;
    while (parent[root] != root) root = parent[root];
    while (parent[x] != root) {          // 지나온 노드를 뿌리에 직결
        int nx = parent[x];
        parent[x] = root;
        x = nx;
    }
    return root;                         // 반복형이라 스택 걱정도 없다
}
// 재귀로 쓰고 싶다면 return parent[x] = find(parent[x]); — '대입'이 핵심이다
```

**2) `sort` 비교자에 `<=`를 쓴다**

```cpp
// ❌ 틀린 코드
sort(e.begin(), e.end(),
     [](const Edge& a, const Edge& b) { return a.w <= b.w; });
```

왜: `std::sort`는 비교자가 **엄격 약순서**(strict weak ordering)임을 전제로 최적화한다. `<=`는 같은 값 두 개에 대해 `cmp(x,y)`와 `cmp(y,x)`가 **둘 다 참**이 되어 그 전제를 깨고, 내부 파티션이 경계를 넘어 배열 밖을 읽는다. 결과는 "가끔 죽고 가끔 통과"라 재현이 가장 어려운 유형의 버그다. 파이썬 `sort`는 키 함수를 받으므로 이 함정 자체가 없다.

```cpp
// ✅ 고친 코드
sort(e.begin(), e.end(),
     [](const Edge& a, const Edge& b) { return a.w < b.w; });   // '<' 만
// 가중치를 구조체 첫 멤버로 두면 tuple 비교로 대신할 수도 있다
// sort(v.begin(), v.end());  // v 가 vector<tuple<long long,int,int>> 일 때
```

**3) 누적 가중치를 `int`로 받는다**

```cpp
// ❌ 틀린 코드
int total = 0;
for (const Edge& ed : e)
    if (unite(ed.a, ed.b)) total += ed.w;   // 20만 * 100만 = 2e11
cout << total << "\n";
```

왜: 간선 하나의 가중치가 `int`에 들어가도 **합은 별개**다. 간선 20만 개에 가중치 100만이면 총합이 `2 × 10^11`이라 `int`(약 21억)를 훌쩍 넘는다. 넘는 순간 경고도 예외도 없이 음수로 감기고, 작은 예제에서는 멀쩡히 맞아 원인 추적이 늦어진다. 파이썬은 정수가 무한 자릿수라 이 실수 자체가 없다.

```cpp
// ✅ 고친 코드
long long total = 0;                        // 누적은 언제나 long long
for (const Edge& ed : e)
    if (unite(ed.a, ed.b)) total += ed.w;
cout << total << "\n";
// 가중치 자체가 클 수도 있으면 Edge::w 도 long long 으로 둔다
```

**4) 채택 간선이 V-1개인지 확인하지 않는다**

```cpp
// ❌ 틀린 코드
long long total = 0;
for (const Edge& ed : e)
    if (unite(ed.a, ed.b)) total += ed.w;
cout << total << "\n";      // 비연결 그래프에서도 태연히 숫자를 출력한다
```

왜: 그래프가 두 덩어리로 끊겨 있으면 채택 간선이 V-2개 이하에서 멈춘다. 그런데 위 코드는 "각 덩어리의 MST 합"을 더한 값을 내보낸다. 신장 트리가 아예 존재하지 않는데 그럴듯한 수가 나오므로 틀렸다는 사실조차 드러나지 않는다.

```cpp
// ✅ 고친 코드
long long total = 0;
int cnt = 0;
for (const Edge& ed : e) {
    if (unite(ed.a, ed.b)) {
        total += ed.w;
        if (++cnt == n - 1) break;          // 다 모았으면 조기 종료까지 덤으로
    }
}
cout << (cnt == n - 1 ? total : -1) << "\n";   // 비연결 표기는 문제마다 바뀜
```

**5) union by rank/size 없이 한쪽으로만 붙인다**

```cpp
// ❌ 틀린 코드
bool unite(int a, int b) {
    int ra = find(a), rb = find(b);
    if (ra == rb) return false;
    parent[rb] = ra;            // 항상 b 쪽을 a 밑으로만 붙인다
    return true;
}
```

왜: `unite(1,2), unite(2,3), unite(3,4), ...`처럼 한 방향으로 들어오는 입력에서 트리가 한 줄로 늘어난다. 경로 압축이 있으면 대체로 버티지만, 압축까지 빠지면 `find` 한 번이 O(V)가 되어 간선 20만 개짜리 크루스칼이 시간 초과로 죽는다. 재귀 `find`를 쓰고 있었다면 시간 초과 대신 **스택 오버플로로 아무 메시지 없이 죽는다**.

```cpp
// ✅ 고친 코드
bool unite(int a, int b) {
    int ra = find(a), rb = find(b);
    if (ra == rb) return false;
    if (rnk[ra] < rnk[rb]) swap(ra, rb);    // 낮은 트리를 높은 트리 밑으로
    parent[rb] = ra;
    if (rnk[ra] == rnk[rb]) rnk[ra]++;      // 높이가 같았을 때만 1 증가
    return true;                            // 높이가 log2 V 이하로 묶인다
}
```

**6) `priority_queue`에 `greater<>`를 빼먹는다**

```cpp
// ❌ 틀린 코드
priority_queue<pair<long long,int>> pq;     // 기본은 '최대' 힙이다
pq.push({0, start});
while (!pq.empty()) {
    auto [w, u] = pq.top(); pq.pop();       // 가장 비싼 간선부터 나온다
    ...
}
```

왜: 파이썬 `heapq`가 최소 힙이라 그 감각으로 옮기면 정확히 반대로 동작한다. 가장 비싼 간선부터 채택하므로 최대 신장 트리가 나오고, 답이 "그럴듯하게 큰 수"라 오류로 보이지 않는다. 시작 원소 `{0, start}`가 최댓값이 아니라 최솟값이라, 첫 pop부터 엉뚱한 정점이 나오는 것이 힌트다.

```cpp
// ✅ 고친 코드
priority_queue<pair<long long,int>,
               vector<pair<long long,int>>, greater<>> pq;   // 최소 힙
// 최대 신장 트리를 원할 때만 기본 최대 힙을 그대로 쓴다
// 꺼낼 때 이름도 다르다: queue 는 front(), priority_queue 는 top()
```

**7) 프림에서 방문 검사를 push 시점에만 한다**

```cpp
// ❌ 틀린 코드
while (!pq.empty()) {
    auto [w, u] = pq.top(); pq.pop();
    visited[u] = 1;                 // 꺼낸 뒤 검사 없이 바로 편입
    total += w;
    for (const auto& [v, wv] : adj[u])
        if (!visited[v]) pq.push({wv, v});   // push 시점 검사만으로 충분하다고 착각
}
```

왜: 정점 `v`가 힙에 여러 번 들어간 뒤 그중 하나가 꺼내져 트리에 편입되면, 힙에 남은 나머지 `v` 항목들은 push된 시점에는 미방문이었으므로 걸러지지 않았다. 그것들이 다시 꺼내지면 같은 정점의 비용이 총합에 중복으로 더해져 답이 커진다.

```cpp
// ✅ 고친 코드
while (!pq.empty() && cnt < n) {
    auto [w, u] = pq.top(); pq.pop();
    if (visited[u]) continue;       // 지연 삭제: 반드시 꺼낸 직후에 검사
    visited[u] = 1;
    total += w;
    cnt++;
    for (const auto& [v, wv] : adj[u])
        if (!visited[v]) pq.push({wv, v});
}
```

**8) 프림의 힙 키를 다익스트라처럼 누적 거리로 넣는다**

```cpp
// ❌ 틀린 코드
for (const auto& [v, wv] : adj[u])
    if (!visited[v]) pq.push({w + wv, v});   // 시작점부터의 누적 거리
```

왜: 그 코드는 MST가 아니라 최단 경로 트리를 만든다. 두 트리는 다른 것이고, 최단 경로 트리의 간선 합은 MST보다 크거나 같다. 별 모양 그래프처럼 시작점에서 모두 직결된 경우에는 우연히 일치해 통과하기도 해서 더 헷갈린다.

```cpp
// ✅ 고친 코드
for (const auto& [v, wv] : adj[u])
    if (!visited[v]) pq.push({wv, v});       // 트리에 붙이는 간선 하나만 본다
// 최소화 대상이 다르다: 다익스트라는 경로 합, 프림은 뽑은 간선들의 총합
```

**9) 무방향 간선을 인접 리스트에 한 방향만 넣는다**

```cpp
// ❌ 틀린 코드
for (int i = 0; i < m; i++) {
    int a, b; long long w;
    cin >> a >> b >> w;
    adj[a].push_back({b, w});       // b 쪽에서는 이 간선이 보이지 않는다
}
```

왜: 프림은 "지금 트리에서 나가는 간선"만 힙에 넣는다. 간선이 한 방향만 등록되어 있으면, 트리가 `b`를 먼저 흡수했을 때 `a`로 돌아오는 길을 찾지 못한다. 결과적으로 도달 못 한 정점이 남아 `cnt < n`이 되고, 멀쩡히 연결된 그래프를 비연결로 판정한다.

```cpp
// ✅ 고친 코드
for (int i = 0; i < m; i++) {
    int a, b; long long w;
    cin >> a >> b >> w;
    adj[a].push_back({b, w});
    adj[b].push_back({a, w});       // 무방향은 반드시 양쪽 등록
}
```

**10) 배열 프림의 INF를 `memset`으로 깐다**

```cpp
// ❌ 틀린 코드
long long key[1005];
memset(key, 0x7f, sizeof(key));     // LLONG_MAX 를 깔았다고 생각한다
key[0] = 0;
```

왜: `memset`은 **바이트 단위**로 채우므로 각 `long long` 칸이 `0x7f7f...7f`(약 9.1×10^18)가 된다. `LLONG_MAX`와 비슷해 보이지만 두 개만 더해도 넘치고, 값 자체도 의도한 수가 아니다. `memset(key, 1, ...)`처럼 쓰면 `0x0101...01`이라는 전혀 다른 수가 깔린다. 초기화는 `vector` 생성자나 `fill`로 한다.

```cpp
// ✅ 고친 코드
const long long INF = LLONG_MAX / 4;        // 더해도 넘치지 않을 여유
vector<long long> key(n, INF);              // 또는 fill(key, key + n, INF);
key[0] = 0;
// memset 이 안전한 경우는 0 이나 -1 로 채울 때뿐이다(모든 바이트가 같은 값)
```

**다음 챕터로**

- 프림의 뼈대는 다익스트라와 한 줄만 다르다. 힙 키를 `w`에서 `dist[u] + w`로 바꾸면 그대로 최단 경로가 되므로, 최단 경로 챕터에서 이 코드를 다시 꺼내 쓰게 된다.
- 유니온-파인드는 MST 밖에서도 계속 등장한다. "간선을 지우는 질의"를 역순으로 뒤집어 합치기로 바꾸는 오프라인 기법, 그리고 좌표·격자를 그룹으로 묶는 문제들이 모두 같은 부품 위에 서 있다.
- C++ 쪽에서 이 챕터가 남긴 습관은 세 가지다. **누적은 `long long`**, **비교자는 `<`**, **재귀 대신 반복**. 앞으로의 그래프·DP 챕터에서 그대로 다시 쓰인다.
