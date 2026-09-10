## L7. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터에서 배운 것은 결국 **하나의 모양(트리) 위에 서로 다른 규칙을 얹은 것**이다. 규칙이 "왼쪽 < 나 < 오른쪽"이면 BST, "부모 ≤ 자식"이면 힙, 아무 규칙도 없으면 그냥 트리다. 아래 지도로 전체를 한 번에 훑고, 뼈대 코드·선택 기준표·체크리스트로 정리한다.

C++에서는 여기에 두 가지가 더 붙는다. 하나는 **표준 컨테이너가 이미 그 규칙을 구현해 두었다는 것** — `std::set`/`std::map`이 균형 BST이고 `std::priority_queue`가 힙이다. 다른 하나는 **메모리와 재귀를 직접 관리해야 한다는 것** — 포인터가 `nullptr`인지, 큰 컨테이너를 참조로 넘겼는지, 콜 스택이 넘치지 않는지를 언어가 대신 봐 주지 않는다.

**개념 지도**

```text
  Ch06 map : one shape, many rules

  tree  (N nodes, N-1 edges, no cycle, exactly one root)
   |
   +-- how the input arrives
   |    parent[v]            -> children[parent[v]].push_back(v)
   |    edge list u v        -> adj[u].push_back(v); adj[v].push_back(u)
   |    left[i], right[i]    -> binary tree, 0 means "no child"
   |
   +-- DFS on a tree
   |    going down : depth[c] = depth[v] + 1
   |    coming up  : size[v]  = 1 + sum(size[c])
   |
   +-- binary tree  (at most 2 children, left and right differ)
        |
        +-- traversal
        |    pre  : node left right    -> copy, serialize
        |    in   : left node right    -> sorted order in a BST
        |    post : left right node    -> subtree sum, delete
        |    BFS  : level by level     -> queue, nearest first
        |
        +-- complete tree -> array with no gap
        |    1-based : 2i, 2i+1, i/2
        |    0-based : 2i+1, 2i+2, (i-1)/2
        |    height = floor(log2 N)
        |
        +-- BST   left subtree < node < right subtree
        |    search / insert / delete : O(h)
        |    inorder = sorted
        |    skewed -> h = N-1 -> O(N)
        |    std::set / std::map are balanced -> O(log N) always
        |
        +-- heap  parent <= child (min-heap)
             push / pop : O(log N),  top : O(1)
             priority_queue is a MAX heap by default
             greater<T> as comparator makes it a min-heap
```

문제를 만나면 아래 순서로 한 칸씩 좁힌다.

```text
  which tool ?

  visit every node once           -> DFS or BFS
  child answers needed first      -> postorder  (coming up)
  parent info carried downward    -> preorder   (going down)
  distance measured in levels     -> BFS with a queue
  sorted order or rank            -> std::set, or sort + lower_bound
  only the current min or max     -> priority_queue
  the k largest values            -> min-heap of size k
  depth may reach 100000          -> explicit stack, not recursion
```

C++ 표준 컨테이너와 손으로 만든 구조가 어떻게 대응하는지도 한 장으로 붙여 둔다.

```text
  hand-written        std::  equivalent        guarantee
  ---------------------------------------------------------
   struct Node BST     set<T> / map<K,V>       O(log N) worst
   array heap          priority_queue<T>       O(log N) push/pop
   children lists      vector<vector<int>>     O(1) amortized append
   visited flags       vector<char> or bitset  O(1) access
   # 개념은 직접 만들어 이해하고, 실전 코드는 표준 컨테이너를 쓴다
```

**뼈대 코드**

1) 부모 배열 입력 → 깊이·서브트리 크기 (재귀 없이)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> parent(n);
    for (int i = 0; i < n; i++) cin >> parent[i];      // 입력 형식은 문제마다 바뀜

    vector<vector<int>> children(n);
    int root = -1;
    for (int v = 0; v < n; v++) {
        if (parent[v] == -1) root = v;                 // 루트 표시는 문제마다 바뀜
        else children[parent[v]].push_back(v);
    }

    vector<int> order, st{root}, depth(n, 0);
    while (!st.empty()) {                              // 스택 DFS: 재귀 대신
        int v = st.back(); st.pop_back();              // 읽고 나서 버린다
        order.push_back(v);
        for (int c : children[v]) {
            depth[c] = depth[v] + 1;                   // 내려가며 계산
            st.push_back(c);
        }
    }

    vector<int> size(n, 1);
    for (int i = (int)order.size() - 1; i >= 0; i--) { // 역순 = 자식이 먼저 확정
        int v = order[i];
        if (parent[v] != -1) size[parent[v]] += size[v];  // 올라오며 계산
    }
    return 0;
}
```

2) 무방향 간선 목록 입력 → 인접 리스트 + BFS 깊이

```cpp
int n, start = 1;                                 // 루트 번호는 문제마다 바뀜
cin >> n;
vector<vector<int>> adj(n + 1);
for (int i = 0; i < n - 1; i++) {
    int u, v;
    cin >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);                          // 방향이 없으면 양쪽에 등록
}

vector<int> dist(n + 1, -1);
dist[start] = 0;
queue<int> q;
q.push(start);
while (!q.empty()) {
    int v = q.front(); q.pop();
    for (int c : adj[v]) {
        if (dist[c] == -1) {                      // 미방문 검사 = 부모로 안 돌아가기
            dist[c] = dist[v] + 1;
            q.push(c);
        }
    }
}
```

3) 순회 3종 — 재귀형과 반복형

```cpp
// 재귀형: 한 번의 DFS로 세 결과를 동시에 만든다 (left/right 는 인덱스 배열)
vector<int> pre, ino, post;

void dfs(int v, const vector<int>& left, const vector<int>& right) {
    if (v == 0) return;                    // '자식 없음' 표기는 문제마다 바뀜
    pre.push_back(v);
    dfs(left[v], left, right);
    ino.push_back(v);
    dfs(right[v], left, right);
    post.push_back(v);
}

// 반복형 전위: 오른쪽을 먼저 push해야 왼쪽이 먼저 pop된다
vector<int> preorderIter(int root, const vector<int>& left, const vector<int>& right) {
    vector<int> out, st{root};
    while (!st.empty()) {
        int v = st.back(); st.pop_back();
        if (v == 0) continue;
        out.push_back(v);
        st.push_back(right[v]);
        st.push_back(left[v]);
    }
    return out;
}

// 반복형 중위: 왼쪽 끝까지 push -> pop해서 기록 -> 오른쪽으로
vector<int> inorderIter(int root, const vector<int>& left, const vector<int>& right) {
    vector<int> out, st;
    int cur = root;
    while (!st.empty() || cur != 0) {
        while (cur != 0) { st.push_back(cur); cur = left[cur]; }
        cur = st.back(); st.pop_back();
        out.push_back(cur);
        cur = right[cur];
    }
    return out;
}
```

4) priority_queue 실전 패턴 모음

```cpp
priority_queue<int, vector<int>, greater<int>> minh;   // 최소 힙 (비교자 필수)
minh.push(5);                                          // 삽입 O(log N)
int peek = minh.top();                                 // 최솟값 조회 O(1), 제거 안 함
minh.pop();                                            // 최솟값 제거 O(log N)

priority_queue<int> maxh;                              // 기본이 최대 힙
for (int x : nums) maxh.push(x);
int biggest = maxh.top(); maxh.pop();                  // 부호 뒤집기가 필요 없다

using P = pair<int,int>;                               // (우선순위, 데이터)
priority_queue<P, vector<P>, greater<P>> pq;           // 첫 원소로 비교, 같으면 둘째
for (auto& t : tasks) pq.push({t.cost, t.id});         // 튜플 구성은 문제마다 바뀜

priority_queue<int, vector<int>, greater<int>> topk;   // 가장 큰 k개 -> 크기 k 최소 힙
for (int x : nums) {
    if ((int)topk.size() < k) topk.push(x);
    else if (x > topk.top()) { topk.pop(); topk.push(x); }
}
int kthLargest = topk.top();                           // 상위 k개 중 가장 작은 값

vector<int> h = nums;                                  // 벡터를 직접 힙으로 다루기
make_heap(h.begin(), h.end());                         // O(N), 최대 힙
```

5) BST 삽입·탐색과 표준 컨테이너

```cpp
struct Node {
    int val;
    Node* left = nullptr;
    Node* right = nullptr;
    Node(int v) : val(v) {}
};

Node* insert(Node* node, int val) {
    if (!node) return new Node(val);
    if (val < node->val)      node->left  = insert(node->left, val);   // 반드시 재대입
    else if (val > node->val) node->right = insert(node->right, val);
    return node;                                   // 중복 규칙은 문제마다 바뀜
}

bool search(Node* node, int val) {
    while (node) {                                 // 반복문이면 스택 깊이와 무관
        if (val == node->val) return true;
        node = (val < node->val) ? node->left : node->right;
    }
    return false;
}

// 실전에서는 대개 이쪽 — 균형이 보장된 표준 컨테이너
set<int> s;
s.insert(4); s.insert(2); s.insert(6);
for (int x : s) cout << x << ' ';                  // 2 4 6  (순회 = 중위 = 정렬)
auto it = s.lower_bound(5);                        // 5 이상인 첫 값 -> 6  O(log N)
bool has3 = s.count(3) > 0;                        // 존재 확인 O(log N)
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 부모 배열만 주어졌고 깊이·크기를 묻는다 | `vector<vector<int>>` 자식 리스트 + DFS | 위에서 아래로 훑을 경로가 있어야 한다 | O(N) |
| 간선이 방향 없이 주어진다 | 인접 리스트 + 방문 표시 | `adj[v]`에 부모도 들어 있어 되돌아감을 막아야 | O(N) |
| 자식들의 답을 모아 내 답을 만든다 | 후위 순회 | 내 차례에 자식이 전부 확정돼 있다 | O(N) |
| 부모에게서 물려받아 아래로 전달한다 | 전위 순회 | 내 차례에 부모 정보만 있으면 충분하다 | O(N) |
| 몇 번째 층인가, 층 단위로 처리 | BFS(`queue`) | 큐에 든 원소가 항상 같은 층이다 | O(N) |
| 트리 깊이가 수만 이상일 수 있다 | 명시적 스택 DFS | C++ 콜 스택이 넘치면 예외 없이 죽는다 | O(N) |
| 입력이 완전 이진 트리다 | 배열 인덱싱(`vector`) | 포인터 없이 계산만으로 자식·부모로 이동 | 이동 O(1) |
| 삽입·삭제가 섞이며 정렬 순서를 유지해야 한다 | `std::set` / `std::map` | 균형이 보장돼 최악에도 O(log N) | O(log N) |
| 개념 연습으로 BST를 직접 만든다 | `struct Node` + 재귀 삽입 | 규칙과 삭제 세 경우를 손으로 익힌다 | O(h) |
| 값이 고정이고 순위·범위만 물어본다 | `sort` + `lower_bound` | 균형 걱정 없이 항상 O(log N)이 보장된다 | O(log N) |
| "x 이상인 첫 값"·"y 이하인 마지막 값" | `set::lower_bound` | 해시엔 없는 근접 질의를 트리가 제공 | O(log N) |
| 남은 것 중 최소/최대만 반복해서 꺼낸다 | `priority_queue` | 전체 순서를 포기해 삽입·삭제를 싸게 만든다 | O(log N) |
| 최소 힙이 필요하다 | `priority_queue<T, vector<T>, greater<T>>` | 기본이 최대 힙이라 비교자를 바꿔야 한다 | O(log N) |
| 상위 k개 또는 k번째 큰 값 | 크기 k 최소 힙 | 전체 정렬 O(N log N)보다 싸다 | O(N log k) |
| 한 번 정렬해 놓고 더 안 바뀐다 | `sort` | 갱신이 없으면 정렬이 가장 단순하고 빠르다 | O(N log N) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 노드가 N개인 트리의 간선이 왜 정확히 N-1개인지.
- [ ] 설명할 수 있다: 깊이와 높이의 차이, 그리고 각각이 왜 반대 방향으로 계산되는지.
- [ ] 설명할 수 있다: 부모 배열·간선 목록·자식 배열 중 어떤 입력이 와도 트리를 만드는 방법.
- [ ] 설명할 수 있다: 1-based `2i`/`2i+1`과 0-based `2i+1`/`2i+2`가 왜 같은 그림의 다른 번호인지.
- [ ] 설명할 수 있다: 완전 이진 트리의 높이가 왜 약 log2(N)인지.
- [ ] 설명할 수 있다: 전위·중위·후위가 왜 같은 코드에서 `push_back` 위치만 다른 것인지.
- [ ] 설명할 수 있다: 서브트리 크기·합 계산에 왜 후위 순회가 맞는지.
- [ ] 설명할 수 있다: 전위+중위로는 트리가 복원되는데 전위+후위로는 안 되는 이유.
- [ ] 설명할 수 있다: BST에서 중위 순회 결과가 왜 항상 오름차순인지.
- [ ] 설명할 수 있다: BST 연산이 O(log N)이 되는 조건과, O(N)으로 무너지는 입력.
- [ ] 설명할 수 있다: BST 삭제의 세 경우와, 자식이 둘일 때 오른쪽 최솟값을 쓰는 이유.
- [ ] 설명할 수 있다: 직접 만든 BST 대신 `std::set`을 쓰면 무엇이 보장되는지.
- [ ] 설명할 수 있다: 힙의 sift-up/sift-down이 왜 높이만큼만 움직이는지.
- [ ] 설명할 수 있다: `priority_queue`가 왜 기본으로 최대 힙인지와, 최소 힙으로 바꾸는 방법.
- [ ] 설명할 수 있다: 재귀 삽입의 반환값을 다시 대입해야 트리가 자라는 이유.
- [ ] 설명할 수 있다: 큰 컨테이너를 값으로 넘길 때 생기는 비용과 `const&`가 그것을 어떻게 없애는지.
- [ ] 설명할 수 있다: 정렬·BST·힙 중 무엇을 언제 고를지, 그 판단 근거.

**⚠️ 자주 하는 실수**

**1) 깊은 트리에서 재귀가 콜 스택을 넘긴다**

```cpp
// ❌ 틀린 코드
int subtreeSize(int v, const vector<vector<int>>& children) {
    int sz = 1;
    for (int c : children[v]) sz += subtreeSize(c, children);
    return sz;
}
// 노드 10만 개짜리 사슬 트리 -> 스택 오버플로로 그냥 죽는다
```

왜: C++에는 파이썬 같은 "재귀 한도" 설정이 없다. 대신 콜 스택(보통 1MB 안팎)이 넘치면 예외가 아니라 **세그멘테이션 폴트**로 프로그램이 죽는다. 어디서 죽었는지도 안 알려 주고, 얕은 테스트에서는 멀쩡히 통과하다가 큰 입력에서만 터진다.

```cpp
// ✅ 고친 코드 — 명시적 스택으로 바꾼다
vector<int> order, st{root};
while (!st.empty()) {
    int v = st.back(); st.pop_back();
    order.push_back(v);
    for (int c : children[v]) st.push_back(c);
}
vector<int> sz(n, 1);
for (int i = (int)order.size() - 1; i >= 0; i--) {   // 역순으로 합쳐 올린다
    int v = order[i];
    if (parent[v] != -1) sz[parent[v]] += sz[v];
}
```

**2) 0-based 배열에 1-based 자식 공식을 쓴다**

```cpp
// ❌ 틀린 코드
vector<int> h = {3, 1, 4, 1, 5};   // 0-based vector
int left  = 2 * i;                 // L2에서 본 1-based 공식을 그대로 가져옴
int right = 2 * i + 1;
```

왜: 0-based에서 `i = 0`의 왼쪽 자식은 1인데 `2 * 0`은 0이라 자기 자신을 가리킨다. 루트에서 무한 루프가 돌거나, 인덱스가 한 칸씩 밀려 엉뚱한 노드끼리 비교된다. 게다가 `vector`는 범위를 검사하지 않으므로 밀린 인덱스가 배열 밖으로 나가도 조용히 쓰레기 값을 읽는다.

```cpp
// ✅ 고친 코드
int left   = 2 * i + 1;
int right  = 2 * i + 2;
int parent = (i - 1) / 2;          // 0-based는 1-based보다 전부 1씩 밀린다
if (left  < (int)h.size()) use(h[left]);    // 범위 검사는 직접 넣어야 한다
if (right < (int)h.size()) use(h[right]);
```

**3) `priority_queue`를 최소 힙으로 착각한다**

```cpp
// ❌ 틀린 코드
priority_queue<pair<int,int>> pq;      // 파이썬 heapq 코드를 그대로 옮겨 왔다
pq.push({dist, node});
auto cur = pq.top(); pq.pop();         // 가장 '먼' 정점이 먼저 나온다
```

왜: 기본 비교자가 `less`라 **큰 값이 위로** 온다. 파이썬 `heapq`는 최소 힙이므로 같은 코드가 정반대로 동작한다. 컴파일도 되고 실행도 되는데 답만 틀려서, 다익스트라 같은 곳에 쓰면 원인을 찾기가 매우 어렵다.

```cpp
// ✅ 고친 코드
using P = pair<int,int>;
priority_queue<P, vector<P>, greater<P>> pq;   // 작은 것부터 나온다
pq.push({dist, node});
auto cur = pq.top(); pq.pop();                 // 가장 가까운 정점
```

**4) 무방향 간선에서 부모로 되돌아간다**

```cpp
// ❌ 틀린 코드
void dfs(int v, int d) {
    depth[v] = d;
    for (int c : adj[v]) dfs(c, d + 1);   // adj[v]에는 자식뿐 아니라 부모도 있다
}
```

왜: 간선 `u v`를 `adj[u]`와 `adj[v]` 양쪽에 넣었으므로 `adj[v]`를 훑으면 부모도 나온다. 부모로 다시 내려가고 부모는 또 나에게 내려와 무한 재귀가 된다. 파이썬이라면 `RecursionError`로 멈추지만 C++은 스택이 터질 때까지 달린다.

```cpp
// ✅ 고친 코드
void dfs(int v, int p, int d) {           // p = 나를 호출한 부모 번호
    depth[v] = d;
    for (int c : adj[v]) {
        if (c != p) dfs(c, v, d + 1);     // 부모 하나만 건너뛰면 된다
    }
}
```

**5) 힙에서 `top()`만 하고 `pop()`을 안 한다**

```cpp
// ❌ 틀린 코드
while (!pq.empty()) {
    int x = pq.top();       // 최솟값을 보기만 했다
    total += x;             // 힙 크기가 줄지 않아 while 이 끝나지 않는다
}
```

왜: `top()`은 조회일 뿐 원소를 제거하지 않는다. 같은 값을 영원히 다시 읽으며 무한 루프에 빠진다. `pop()`이 값을 돌려주지 않기 때문에 "읽기와 제거는 항상 두 줄"이라는 규칙을 잊는 순간 이 형태가 나온다.

```cpp
// ✅ 고친 코드
while (!pq.empty()) {
    int x = pq.top();       // (1) 읽고
    pq.pop();               // (2) 반드시 제거한다
    total += x;
}
```

**6) BST 재귀 삽입의 반환값을 부모에 다시 연결하지 않는다**

```cpp
// ❌ 틀린 코드
Node* insert(Node* node, int val) {
    if (!node) return new Node(val);
    if (val < node->val) insert(node->left, val);    // 반환값을 그냥 버렸다
    else                 insert(node->right, val);
    return node;
}
```

왜: `node->left`는 **값이 복사돼 넘어간 포인터**다. 함수 안에서 `new Node(val)`을 만들어 돌려줘도 받는 쪽이 없으니 그 노드는 어디에도 매달리지 않는다. 루트만 남고 트리가 자라지 않아 이후 탐색이 전부 실패하고, 만든 노드는 해제도 안 돼 메모리 누수까지 난다.

```cpp
// ✅ 고친 코드
Node* insert(Node* node, int val) {
    if (!node) return new Node(val);
    if (val < node->val) node->left  = insert(node->left, val);   // 다시 매단다
    else                 node->right = insert(node->right, val);
    return node;
}
```

**7) `nullptr` 검사를 빠뜨리고 자식을 따라간다**

```cpp
// ❌ 틀린 코드
int height(Node* node) {
    return 1 + max(height(node->left), height(node->right));
    // 리프의 자식은 nullptr -> nullptr->left 접근 -> 세그멘테이션 폴트
}
```

왜: 파이썬이라면 `None.left`가 `AttributeError`로 어디서 났는지 알려 준다. C++에서 널 포인터 역참조는 **미정의 동작**이라 즉시 죽거나, 더 나쁘게는 엉뚱한 메모리를 읽고 계속 실행된다. 재귀의 기저 조건은 문법이 아니라 안전장치다.

```cpp
// ✅ 고친 코드
int height(Node* node) {
    if (!node) return -1;              // 기저 조건이 항상 첫 줄
    return 1 + max(height(node->left), height(node->right));
}
```

**8) 인접 리스트를 값으로 넘긴다**

```cpp
// ❌ 틀린 코드
int subtreeSize(int v, vector<vector<int>> children) {   // & 가 빠졌다
    int sz = 1;
    for (int c : children[v]) sz += subtreeSize(c, children);
    return sz;
}
```

왜: 호출할 때마다 **인접 리스트 전체가 통째로 복사된다.** 노드 10만 개 트리에서 재귀 10만 번이면 복사만으로 시간과 메모리가 끝난다. 알고리즘은 O(N)인데 실제로는 O(N²) 이상이 되고, 파이썬에서 옮겨 온 코드일수록 이 `&` 하나를 놓치기 쉽다.

```cpp
// ✅ 고친 코드
int subtreeSize(int v, const vector<vector<int>>& children) {   // 주소만 넘어간다
    int sz = 1;
    for (int c : children[v]) sz += subtreeSize(c, children);
    return sz;
}
```

**9) 서브트리 합을 `int`로 받아 오버플로를 낸다**

```cpp
// ❌ 틀린 코드
int sumSubtree(int v) {
    int s = value[v];                       // 값이 10^6, 노드가 10^5 개면
    for (int c : children[v]) s += sumSubtree(c);   // 합이 10^11 -> int 를 넘는다
    return s;
}
```

왜: C++ `int`는 약 21억(2^31-1)까지다. 넘으면 예외가 아니라 **조용히 음수로 감긴다.** 파이썬 정수는 자리수 제한이 없어 이 사고가 없으므로, 옮겨 온 코드에서 가장 발견이 늦는 버그다. 합·곱·누적이 들어가면 값의 범위를 먼저 계산해 보는 습관이 필요하다.

```cpp
// ✅ 고친 코드
long long sumSubtree(int v) {
    long long s = value[v];                 // 약 9.2 * 10^18 까지 담는다
    for (int c : children[v]) s += sumSubtree(c);
    return s;
}
```

**다음 챕터로**

- 여기서 만든 "인접 리스트 + 방문 표시 + DFS/BFS" 뼈대는 그래프 챕터에서 그대로 재사용된다. 트리는 사이클이 없는 특수한 그래프라, 달라지는 것은 "방문 표시를 반드시 해야 한다"는 조건 하나뿐이다.
- 힙은 최단 경로(다익스트라)에서 "다음에 확정할 가장 가까운 정점"을 고르는 도구로 다시 등장한다. `pair<int,int>`를 넣는 `priority_queue`에 `greater`를 붙여 최소 힙으로 만드는 패턴이 그 자리에서 그대로 쓰인다.
