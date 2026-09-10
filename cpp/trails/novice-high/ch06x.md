## L6. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch06(트리)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. 부모 배열·간선 목록·자식 배열·1-based 배열 등 서로 다른 입력 형식으로 트리를 만들고, 순회·BST·힙을 소재만 바꿔 다시 쓴다.
- **C++에서 가장 먼저 짚어야 할 차이 — 힙의 기본 방향**: 파이썬 `heapq`는 **최소 힙**이 기본이라 최대 힙이 필요하면 `-x`로 부호를 뒤집는다. C++ `priority_queue`는 정반대로 **최대 힙이 기본**이다. 최소 힙을 쓰려면 비교자를 명시해야 한다 — `priority_queue<int, vector<int>, greater<int>> pq;`. 이 선언을 빠뜨리면 컴파일은 되고 답만 조용히 뒤집힌다. 그리고 여기서도 `pop()`은 값을 돌려주지 않으므로 `int x = pq.top(); pq.pop();` 2단계다.
- **반복 훈련 개념**:
  - 입력 → 트리 구성: 부모 배열은 `children[parent[v]].push_back(v)`, 간선 목록은 `adj[u].push_back(v); adj[v].push_back(u)` — 둘 다 `vector<vector<int>>`
  - 재귀 순회 뼈대: `if (v == -1) return;` 뒤에 "현재를 어디서 `push_back` 하느냐"로 전위/중위/후위가 갈린다
  - 내려가며 누적 / 올라오며 합치기: `path[c] = path[v] + val[c]` vs `sz[parent[v]] += sz[v]`
  - BST 하강: `cur = (x < val[cur]) ? L[cur] : R[cur];`
  - 힙 인덱스(0-based): 부모 `(i - 1) / 2`, 자식 `2 * i + 1`·`2 * i + 2`
- **트리를 무엇으로 담을까**: 자식이 여럿이면 `vector<vector<int>>` 인접 리스트, 이진 트리는 노드 번호 배열 세 개(`val`/`L`/`R`)나 `struct Node { int val, l, r; };`가 편하다. 값을 키로 하는 `map`은 BST 삭제처럼 "값만 바꿔치기"가 필요한 순간에 곤란해진다.
- **재귀 깊이**: C++의 기본 호출 스택은 보통 1MB 정도라, 사슬 모양 트리에서 재귀 깊이가 수십만이 되면 스택 오버플로로 죽는다(예외가 아니라 프로세스 종료다). 이 레슨의 N은 1000 이하라 재귀가 안전하지만, N이 크면 명시적 `stack`으로 바꾸는 습관을 들인다.
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '트리'·'우선순위 큐' 단계, 프로그래머스 「코딩테스트 고득점 Kit」의 '힙', NeetCode 150의 'Trees'·'Heap'.
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 간선 목록으로 노드별 깊이 | Easy | 인접 리스트 + 내려가며 깊이 | 반복 훈련 |
| 2 | 배열 완전 이진 트리의 전위·후위 순회 | Easy | 1-based 배열 자식 공식 + 순회 | 반복 훈련 |
| 3 | BST의 최솟값·최댓값·높이 | Easy | BST 삽입 하강(노드 번호 배열) | 반복 훈련 |
| 4 | 최소 힙 삽입 후 배열 상태 | Easy | 힙 sift-up 직접 구현 | 반복 훈련 |
| 5 | 후위+중위로 전위 복원 | Medium | 순회 결과로 트리 분할 | 반복 훈련 |
| 6 | 루트에서 리프까지 경로 합 최댓값 | Medium | 부모 배열 + 내려가며 누적 | 반복 훈련 |
| 7 | 좌우 대칭 이진 트리 판정 | Medium | 두 노드 동시 재귀 | 유형 확장 (NeetCode 'Trees' 스타일) |
| 8 | k개 정렬 목록 합치기 | Medium | `tuple` 최소 우선순위 큐(`greater`) | 유형 확장 (NeetCode 'Heap' 스타일) |
| 9 | 묶음 합치기 최소 비용 | Medium | 최소 힙에서 두 개 꺼내 합치기 | 유형 확장 (백준 '우선순위 큐' 단계 스타일) |
| 10 | BST 삭제 후 순회 | Hard | BST 삭제 세 경우 + 순회 | 유형 확장 (백준 '트리' 단계 스타일) |
| 11 | 배열 힙 직접 구현 — 삽입과 삭제 | Hard | sift-up + sift-down | 반복 훈련 |
| 12 | 트리의 지름 | Hard | 간선 목록 + BFS 두 번 | 유형 확장 (백준 '트리' 단계 스타일) |

**문제**

**1) 간선 목록으로 노드별 깊이** · Easy

- **요구사항**: 노드 1..N과 N−1개의 간선(방향 없음)으로 주어진 트리에서, 루트를 1번으로 두었을 때 각 노드의 깊이(루트 0)를 구하라.

- **입력**: 첫 줄 N(1 ≤ N ≤ 1000). 이후 N−1줄에 간선 `u v`.

- **출력**: 노드 1..N의 깊이를 공백으로 구분해 한 줄.

- **예제**:

  - `5 / 1 2 / 1 3 / 3 4 / 3 5` → `0 1 1 2 2`  (1의 자식 2,3; 3의 자식 4,5)

  - `4 / 2 1 / 3 2 / 4 3` → `0 1 2 3`  (간선이 `자식 부모` 순으로 적혀 있어도 1→2→3→4 사슬)

- **셀프체크**: 간선 `u v`를 양쪽 인접 리스트에 모두 넣었는가(한쪽만 넣으면 `2 1`처럼 자식이 먼저 적힌 간선에서 끊김). 인접 리스트를 `vector<vector<int>> adj(n + 1)`로 잡아 1..N을 그대로 인덱스로 쓰는가(크기를 `n`으로 잡으면 `adj[n]`이 범위 밖). 방향이 없으니 부모로 되돌아가지 않도록 `depth == -1`(미방문) 검사를 했는가. N=1이면 간선 줄이 없고 `0`만 출력되는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<vector<int>> adj(n + 1);      // 1-based 이므로 크기는 n+1
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);             // 방향 없음 → 양쪽에 등록
    }

    vector<int> depth(n + 1, -1);
    depth[1] = 0;
    queue<int> q;
    q.push(1);
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        for (int w : adj[v]) {
            if (depth[w] == -1) {        // 아직 안 간 곳만 (부모로 되돌아가기 방지)
                depth[w] = depth[v] + 1;
                q.push(w);
            }
        }
    }

    for (int v = 1; v <= n; v++) {
        if (v > 1) cout << ' ';
        cout << depth[v];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
5
1 2
1 3
3 4
3 5
--OUT
0 1 1 2 2
--IN
4
2 1
3 2
4 3
--OUT
0 1 2 3
--IN
1
--OUT
0
--IN
6
1 2
1 3
1 4
1 5
1 6
--OUT
0 1 1 1 1 1
@@EXPL
(1) 접근·핵심 아이디어

- 간선 목록에는 부모/자식 구분이 없으므로 양방향 인접 리스트로 만든 뒤, 루트 1에서 출발해 "만나는 순서대로" 깊이를 부모 깊이+1로 매긴다. 방향이 없으니 방금 온 부모로 되돌아갈 수 있는데, 깊이가 이미 정해진 노드는 건너뛰면 된다. 노드·간선을 한 번씩 보므로 O(N).

(2) 코드 단계별

- `vector<vector<int>> adj(n + 1)`을 만들고 `adj[u].push_back(v)`, `adj[v].push_back(u)`로 양쪽에 서로를 추가한다. 노드 번호가 1부터라 크기를 `n + 1`로 잡는 것이 C++ 인접 리스트의 관용구다.
- `depth`를 -1로 초기화하고 루트만 0으로 둔 뒤 `queue<int>`로 BFS(L2·L3의 레벨 순회와 같은 골격).
- `q.front()`로 읽고 `q.pop()`으로 버리는 2단계 — `pop()`은 값을 돌려주지 않는다.
- 이웃 `w`의 `depth`가 -1일 때만 `depth[v] + 1`로 채우고 큐에 넣는다.
- 1..N 순서로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "부모 배열이 아니라 간선"이면 먼저 양방향 인접 리스트로 바꾼다는 습관.
- 깊이는 "내려가며 계산"이므로 BFS/DFS 어느 쪽이든 부모 값+1.
- 되돌아가기 방지(방문 표시)를 빠뜨리면 무한 루프. N=1(간선 0개, 루프가 아예 돌지 않음) 경계값 확인.
```

**2) 배열 완전 이진 트리의 전위·후위 순회** · Easy

- **요구사항**: 1-based 배열 A[1..N]에 저장된 완전 이진 트리(노드 i의 왼쪽 자식 2i, 오른쪽 자식 2i+1)를 전위·후위 순회한 값을 출력하라.

- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 A[1..N].

- **출력**: 두 줄 — 전위 순회 결과, 후위 순회 결과(공백 구분).

- **예제**:

  - `6 / 1 2 3 4 5 6` → `1 2 4 5 3 6 / 4 5 2 6 3 1`  (1의 자식 2,3; 2의 자식 4,5; 3의 왼쪽 자식 6)

  - `3 / 9 8 7` → `9 8 7 / 8 7 9`

- **셀프체크**: 재귀 기저를 "인덱스가 N을 넘으면 반환"으로 두었는가(자식 배열 없이 인덱스 공식만으로 순회). 전위는 진입 시, 후위는 두 자식을 마친 뒤 `push_back` 했는가. 배열을 `vector<int> a(n + 1)`로 잡아 1-based를 맞췄는가(0번 칸은 버린다). N=1이면 두 줄 모두 값 하나인가. 완전 이진 트리라 재귀 깊이는 log2(N) 수준이라 스택 걱정이 없음을 알고 있는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> a, pre, post;

void dfs(int i) {
    if (i > n) return;                   // 자식 인덱스가 N을 넘으면 없음
    pre.push_back(a[i]);                 // 전위: 진입 시
    dfs(2 * i);
    dfs(2 * i + 1);
    post.push_back(a[i]);                // 후위: 두 자식을 마친 뒤
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    a.assign(n + 1, 0);                  // 0번 칸은 버리고 1-based 로 쓴다
    for (int i = 1; i <= n; i++) cin >> a[i];

    dfs(1);

    for (size_t i = 0; i < pre.size(); i++) {
        if (i) cout << ' ';
        cout << pre[i];
    }
    cout << '\n';
    for (size_t i = 0; i < post.size(); i++) {
        if (i) cout << ' ';
        cout << post[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
6
1 2 3 4 5 6
--OUT
1 2 4 5 3 6
4 5 2 6 3 1
--IN
3
9 8 7
--OUT
9 8 7
8 7 9
--IN
1
7
--OUT
7
7
--IN
4
10 20 30 40
--OUT
10 20 40 30
40 20 30 10
@@EXPL
(1) 접근·핵심 아이디어

- 완전 이진 트리는 자식 배열을 따로 만들 필요 없이 인덱스 공식(2i, 2i+1)만으로 내려갈 수 있다. 순회 뼈대는 L3과 같고, 기저가 `v == -1` 대신 `i > n`으로 바뀔 뿐이다. 각 노드를 한 번 방문하므로 O(N).

(2) 코드 단계별

- `vector<int> a(n + 1)`로 잡아 0번 칸을 비워 두면 파이썬에서 앞에 0을 붙이던 것과 같은 1-based가 된다.
- `dfs(i)`: `i > n`이면 반환, `pre`에 `a[i]` 추가, `dfs(2i)`, `dfs(2i+1)`, `post`에 `a[i]` 추가.
- `dfs`가 `n`·`a`·`pre`·`post`를 쓰므로 이들을 전역에 둔다. 지역 변수를 쓰려면 매개변수로 넘기거나 람다에 `[&]`로 캡처해야 하는데, `std::function`을 쓰면 느려지므로 짧은 문제에선 전역이 무난하다.
- `dfs(1)` 후 두 벡터를 각각 한 줄로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "배열 표현"이면 자식은 계산으로 얻는다 — 1-based 공식 `2i`/`2i+1`(0-based `2i+1`/`2i+2`와 혼동 금지).
- 전위/후위의 `push_back` 위치만 다르다는 L3 원칙 그대로.
- 마지막 레벨이 덜 찬 경우(`N=6`, 3의 오른쪽 자식 7 없음)에도 `i > n` 기저가 자연스럽게 처리하는지 검산.
```

**3) BST의 최솟값·최댓값·높이** · Easy

- **요구사항**: 서로 다른 정수를 주어진 순서대로 빈 BST에 삽입한 뒤, 트리의 최솟값·최댓값·높이(간선 기준)를 구하라.

- **입력**: 첫 줄 N(1 ≤ N ≤ 500), 둘째 줄 정수 N개(삽입 순서).

- **출력**: 최솟값 최댓값 높이를 공백으로 구분해 한 줄.

- **예제**:

  - `5 / 4 2 6 1 3` → `1 6 2`  (4 아래 2·6, 2 아래 1·3 → 높이 2)

  - `4 / 1 2 3 4` → `1 4 3`  (오름차순 삽입 → 오른쪽 사슬, 높이 3)

- **셀프체크**: 최솟값은 루트에서 왼쪽으로만, 최댓값은 오른쪽으로만 끝까지 내려가 구했는가. 높이를 "삽입할 때 내려간 깊이의 최댓값"으로 잡았는가(새 노드는 항상 리프에 붙고 기존 노드의 깊이는 변하지 않음). 값을 키로 한 `map` 대신 노드 번호 배열(`val`/`L`/`R`)로 두었는가 — 새 노드를 만들며 `L[cur] = newNode(x)`처럼 한 줄로 쓰면 `push_back`이 벡터를 재할당해 왼쪽 참조가 무효가 될 수 있으니, 새 번호를 먼저 지역 변수에 받고 나서 대입했는가. N=1이면 높이 0인가. 같은 값 집합이라도 삽입 순서에 따라 높이가 달라짐을 이해했는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

vector<int> val, L, R;

int newNode(int x) {
    val.push_back(x);
    L.push_back(-1);
    R.push_back(-1);
    return (int)val.size() - 1;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];

    int root = newNode(nums[0]);
    int height = 0;
    for (int i = 1; i < n; i++) {
        int x = nums[i];
        int cur = root;
        int d = 0;
        while (true) {
            d++;                         // 한 칸 내려감
            if (x < val[cur]) {
                if (L[cur] == -1) {
                    int nd = newNode(x); // 먼저 만들고 나서 대입 (재할당 주의)
                    L[cur] = nd;
                    break;
                }
                cur = L[cur];
            } else {
                if (R[cur] == -1) {
                    int nd = newNode(x);
                    R[cur] = nd;
                    break;
                }
                cur = R[cur];
            }
        }
        if (d > height) height = d;      // 새 리프의 깊이가 곧 높이 후보
    }

    int mn = root;
    while (L[mn] != -1) mn = L[mn];
    int mx = root;
    while (R[mx] != -1) mx = R[mx];

    cout << val[mn] << ' ' << val[mx] << ' ' << height << '\n';
    return 0;
}
@@TESTS
--IN
5
4 2 6 1 3
--OUT
1 6 2
--IN
4
1 2 3 4
--OUT
1 4 3
--IN
1
10
--OUT
10 10 0
--IN
6
50 30 70 20 40 60
--OUT
20 70 2
@@EXPL
(1) 접근·핵심 아이디어

- BST에서 최솟값은 "왼쪽으로만" 내려간 끝, 최댓값은 "오른쪽으로만" 내려간 끝이다. 높이는 별도 재귀 없이도 구할 수 있다: 새 노드는 항상 리프로 붙고 기존 노드의 깊이는 변하지 않으므로, 삽입하며 내려간 칸 수의 최댓값이 곧 트리 높이다. 삽입 N번 × O(높이).

(2) 코드 단계별

- 파이썬의 `left`/`right` dict 대신 노드 번호를 인덱스로 하는 `val`/`L`/`R` 세 벡터를 쓴다. `newNode(x)`가 세 벡터에 한 칸씩 밀어 넣고 새 번호를 돌려준다. 이름을 `left`/`right`로 지으면 `<ios>`의 `std::left`/`std::right`와 겹쳐 `using namespace std;` 아래에서 모호해지므로 `L`/`R`로 둔다.
- 첫 값을 루트로 두고, 나머지는 L4와 같은 while 하강으로 빈 자리에 단다. 내려갈 때마다 `d`를 1씩 올려 삽입 깊이를 세고 `height`를 갱신한다.
- `L[cur] = newNode(x);`를 한 줄로 쓰면, `newNode` 안의 `push_back`이 벡터를 다른 메모리로 옮겼을 때 왼쪽의 `L[cur]`가 가리키던 자리가 무효가 될 수 있다(C++17에선 우변이 먼저 계산돼 안전하지만, 표준 판본에 기대지 말고 지역 변수에 받아 두는 편이 안전하다).
- `mn`: 루트에서 `L`이 -1이 될 때까지 왼쪽으로. `mx`: 오른쪽으로.
- 세 값을 한 줄로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "BST 최소/최대 = 한쪽 끝"이라는 성질을 먼저 떠올린다.
- 높이를 재귀로 다시 계산해도 되지만, "삽입 깊이 최댓값"이 더 짧고 같은 답임을 이해한다.
- 정렬 순 삽입(`1 2 3 4`)이 사슬이 되어 높이 N−1이 되는 최악 경우를 확인. N=1은 루프에 들어가지 않아 높이 0.
```

**4) 최소 힙 삽입 후 배열 상태** · Easy

- **요구사항**: 빈 배열(0-based)로 표현한 최소 힙에 정수를 순서대로 삽입하라. 삽입 규칙: 배열 끝에 붙인 뒤, "부모 값이 새 값보다 클 동안" 부모와 자리를 바꾸며 올라간다(같으면 멈춤). 모든 삽입이 끝난 배열을 출력하라. `priority_queue`를 쓰지 말고 직접 구현한다(`priority_queue`는 내부 배열 배치를 보여 주지도 않고, 애초에 기본이 최대 힙이다).

- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 정수 N개(중복 가능).

- **출력**: 최종 배열을 인덱스 0부터 공백으로 구분해 한 줄.

- **예제**:

  - `5 / 5 3 8 1 4` → `1 3 8 5 4`
    - 검산: `[5]` → `[3,5]` → `[3,5,8]` → 1 삽입 `[3,5,8,1]` → 부모(5)와 교환 `[3,1,8,5]` → 부모(3)와 교환 `[1,3,8,5]` → 4 삽입 `[1,3,8,5,4]`, 부모 3 ≤ 4라 멈춤

  - `4 / 9 7 5 3` → `3 5 7 9`

- **셀프체크**: 부모 인덱스를 `(j - 1) / 2`(0-based)로 썼는가(1-based 공식 `i / 2`와 혼동 금지). 인덱스를 `int`로 두었는가 — `heap.size()`는 부호 없는 타입이라 `size() - 1`을 그대로 쓰면 빈 배열에서 거대한 값이 된다. 교환 조건이 `heap[p] > heap[j]`(엄격)라 같은 값끼리는 교환하지 않는가(`2 2 2` → `2 2 2`). j가 0(루트)에 도달하면 멈추는가. 교환은 `swap(heap[p], heap[j])` 한 줄로 되는가(파이썬의 동시 대입 `a, b = b, a`에 해당하는 C++ 도구가 `swap`이다).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> heap;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        heap.push_back(x);               // 끝에 붙이고
        int j = (int)heap.size() - 1;    // size()는 unsigned → 캐스팅
        while (j > 0) {                  // 부모보다 작으면 올라간다 (sift-up)
            int p = (j - 1) / 2;
            if (heap[p] > heap[j]) {
                swap(heap[p], heap[j]);  // 파이썬 동시 대입 대신 swap
                j = p;
            } else {
                break;
            }
        }
    }

    for (int i = 0; i < (int)heap.size(); i++) {
        if (i) cout << ' ';
        cout << heap[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
5
5 3 8 1 4
--OUT
1 3 8 5 4
--IN
4
9 7 5 3
--OUT
3 5 7 9
--IN
3
2 2 2
--OUT
2 2 2
--IN
1
42
--OUT
42
@@EXPL
(1) 접근·핵심 아이디어

- 힙 삽입(sift-up)은 "끝에 붙이고 부모보다 작으면 부모와 바꾸며 올라가기"다. 완전 이진 트리를 배열로 두었으므로 부모는 `(j - 1) / 2` 한 줄로 찾는다. 한 번 올라갈 때마다 깊이가 1 줄어 삽입당 O(log N), 전체 O(N log N).

(2) 코드 단계별

- `heap.push_back(x)` 후 `j`를 마지막 인덱스로 — `(int)heap.size() - 1`처럼 부호 있는 타입으로 바꿔 둔다.
- `j > 0`인 동안 부모 `p = (j - 1) / 2`를 구해 `heap[p] > heap[j]`면 `swap`하고 `j = p`, 아니면 중단.
- 모든 삽입 후 배열을 그대로 출력.
- `(j - 1) / 2`는 j가 1 이상일 때만 계산되므로 음수 나눗셈(C++은 0 방향 절삭이라 파이썬의 내림과 다르다)을 걱정하지 않아도 된다. 루프 조건 `j > 0`이 그 보장이다.

(3) 스스로 다시 짤 때 생각 순서

- 0-based 부모 공식 `(j - 1) / 2`를 먼저 적어 두기(L5 개념표 참고).
- 비교를 엄격(`>`)으로 두어야 같은 값이 불필요하게 자리를 바꾸지 않아 답이 유일해진다.
- 내림차순 입력(`9 7 5 3`)은 매번 루트까지 올라가는 최악 경우 — 손으로 한 번 따라가 보기.
```

**5) 후위+중위로 전위 복원** · Medium

- **요구사항**: 어떤 이진 트리의 후위 순회와 중위 순회(노드 값은 서로 다른 정수)가 주어진다. 그 트리의 전위 순회를 출력하라.

- **입력**: 첫 줄 N(1 ≤ N ≤ 500), 둘째 줄 후위 수열, 셋째 줄 중위 수열.

- **출력**: 전위 순회 결과(공백 구분).

- **예제**:

  - `5 / 4 5 2 3 1 / 4 2 5 1 3` → `1 2 4 5 3`
    - 검산: 후위 마지막 1=루트. 중위에서 1의 왼쪽 `{4,2,5}`(3개)·오른쪽 `{3}`. 후위 앞 3개 `4 5 2`가 왼 서브트리(루트 2) → 전위 `2 4 5`. 전체 전위 = 1 + (2 4 5) + (3)

  - `4 / 1 2 3 4 / 1 2 3 4` → `4 3 2 1`  (왼쪽 사슬)

- **셀프체크**: 후위의 "마지막" 원소가 루트임을 썼는가(전위는 첫 원소). 왼 서브트리 크기 `mid - il`로 후위 구간도 함께 잘랐는가(후위 구간 `[pl, pl+ls-1]`이 왼쪽, `[pl+ls, pr-1]`이 오른쪽). 값→중위 인덱스를 파이썬 dict 대신 `unordered_map<int,int>`로 두어 분할 위치를 O(1)에 찾았는가. 사슬 입력에서 재귀 깊이가 N까지 가는데 N ≤ 500이라 안전함을 확인했는가. N=1이면 그 값 하나인가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> post, ino, pre;
unordered_map<int, int> pos;             // 값 → 중위 인덱스

void build(int il, int ir, int pl, int pr) {
    // 중위 구간 [il, ir], 후위 구간 [pl, pr] 은 같은 서브트리
    if (il > ir) return;
    int root = post[pr];                 // 후위의 마지막 = 루트
    pre.push_back(root);                 // 전위: 루트 먼저
    int mid = pos[root];
    int ls = mid - il;                   // 왼 서브트리 크기
    build(il, mid - 1, pl, pl + ls - 1);
    build(mid + 1, ir, pl + ls, pr - 1);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    post.resize(n);
    ino.resize(n);
    for (int i = 0; i < n; i++) cin >> post[i];
    for (int i = 0; i < n; i++) cin >> ino[i];
    for (int i = 0; i < n; i++) pos[ino[i]] = i;

    build(0, n - 1, 0, n - 1);

    for (size_t i = 0; i < pre.size(); i++) {
        if (i) cout << ' ';
        cout << pre[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
5
4 5 2 3 1
4 2 5 1 3
--OUT
1 2 4 5 3
--IN
4
1 2 3 4
1 2 3 4
--OUT
4 3 2 1
--IN
3
2 3 1
2 1 3
--OUT
1 2 3
--IN
1
7
7
--OUT
7
@@EXPL
(1) 접근·핵심 아이디어

- 후위 순회는 "왼 → 오 → 루트"이므로 구간의 마지막 원소가 루트다. 중위에서 그 루트 위치로 좌/우를 나누면, 왼 서브트리 크기 `ls`만큼이 후위 구간 앞쪽, 나머지가 오른쪽이다. 중위·후위 구간을 쌍으로 넘기는 재귀로 전위(루트 → 왼 → 오)를 바로 만든다. 해시 맵으로 위치를 찾으면 O(N).

(2) 코드 단계별

- `unordered_map<int,int> pos`로 값→중위 인덱스를 미리 만든다(파이썬 dict의 대응물; 정렬이 필요 없으니 `map`보다 `unordered_map`이 빠르다).
- `build(il, ir, pl, pr)`: 비었으면 반환. `root = post[pr]`를 `pre`에 추가, `mid = pos[root]`, `ls = mid - il`.
- 왼쪽: 중위 `[il, mid-1]`, 후위 `[pl, pl+ls-1]`. 오른쪽: 중위 `[mid+1, ir]`, 후위 `[pl+ls, pr-1]`.
- 왼쪽 → 오른쪽 순으로 재귀하면 `push_back` 순서가 전위가 된다.
- 재귀가 `post`·`pre`·`pos`를 쓰므로 전역에 둔다. 사슬 입력이면 깊이가 N이 되는데 N ≤ 500이라 호출 스택에 여유가 있다.

(3) 스스로 다시 짤 때 생각 순서

- L3의 "전위+중위 → 후위"와 대칭: 이번엔 루트가 후위의 끝, 그리고 출력이 전위라 루트를 진입 시 `push_back`.
- 후위를 포인터 하나로 뒤에서 소비하면 오른쪽을 먼저 재귀해야 해서 전위 순서가 꼬인다 — 구간 쌍으로 넘기면 왼쪽 먼저 재귀가 가능해 이 함정을 피한다.
- 사슬(`4 3 2 1`)과 N=1로 구간 계산(`pl+ls-1`)이 어긋나지 않는지 검산.
```

**6) 루트에서 리프까지 경로 합 최댓값** · Medium

- **요구사항**: 부모 배열과 각 노드의 값(음수 가능)이 주어진 트리에서, 루트에서 어떤 리프까지 내려가는 경로 위 값들의 합이 최대가 되는 값을 구하라. 경로의 끝은 반드시 리프여야 한다.

- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 `parent[0..N-1]`(루트 -1), 셋째 줄 값 `V[0..N-1]`(−1000 ≤ V ≤ 1000).

- **출력**: 최대 경로 합.

- **예제**:

  - `5 / -1 0 0 1 1 / 1 2 3 -4 5` → `8`  (경로 0→1→4: 1+2+5=8; 0→2: 4; 0→1→3: −1)

  - `3 / -1 0 1 / 5 -2 -3` → `0`  (리프는 2뿐이라 경로 합 5−2−3=0. 루트 값 5가 더 크지만 리프가 아니므로 답이 아님)

- **셀프체크**: 누적합을 "내려가며" `path[c] = path[v] + V[c]`로 전달했는가. 최댓값 갱신을 리프에서만 했는가(음수가 있으면 내부 노드 합이 더 클 수 있음). 값이 모두 음수여도 답이 나오도록 초깃값을 0으로 두지 않았는가 — 파이썬의 `None` 대신 C++에선 `bool found` 깃발을 함께 두거나 `LLONG_MIN`으로 시작한다(`1 / -1 / -7` → `-7`). 루트가 0번이 아닐 수도 있는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> parent(n), val(n);
    for (int i = 0; i < n; i++) cin >> parent[i];
    for (int i = 0; i < n; i++) cin >> val[i];

    vector<vector<int>> children(n);
    int root = -1;
    for (int v = 0; v < n; v++) {
        if (parent[v] == -1) root = v;
        else children[parent[v]].push_back(v);
    }

    vector<long long> path(n, 0);        // path[v] = 루트에서 v까지 값 합
    path[root] = val[root];
    bool found = false;                  // 파이썬 None 대신 깃발
    long long best = 0;

    stack<int> st;                       // 재귀 대신 명시적 스택
    st.push(root);
    while (!st.empty()) {
        int v = st.top();
        st.pop();
        if (children[v].empty()) {       // 리프에서만 답 후보
            if (!found || path[v] > best) {
                best = path[v];
                found = true;
            }
        }
        for (int c : children[v]) {
            path[c] = path[v] + val[c];  // 내려가며 누적
            st.push(c);
        }
    }

    cout << best << '\n';
    return 0;
}
@@TESTS
--IN
5
-1 0 0 1 1
1 2 3 -4 5
--OUT
8
--IN
3
-1 0 1
5 -2 -3
--OUT
0
--IN
1
-1
-7
--OUT
-7
--IN
3
2 2 -1
4 -9 1
--OUT
5
@@EXPL
(1) 접근·핵심 아이디어

- 깊이처럼 "내려가며 계산"하는 값이다. 루트의 경로 합은 자기 값, 자식의 경로 합은 부모 경로 합 + 자기 값. 이렇게 모든 노드의 경로 합을 한 번에 채우고, 리프의 경로 합 중 최댓값을 고른다. 노드마다 한 번씩 보므로 O(N). 재귀 대신 명시적 `stack<int>`를 써서 깊은 사슬에도 호출 스택이 터지지 않는다.

(2) 코드 단계별

- 부모 배열을 `vector<vector<int>> children`으로 바꾸고 루트를 찾는다(L1 패턴).
- `path[root] = val[root]`로 시작해 스택 DFS: `st.top()`으로 읽고 `st.pop()`으로 버린 뒤, 꺼낸 노드가 리프면 `best` 갱신, 자식마다 `path[c] = path[v] + val[c]` 후 push.
- `best`를 출력.
- 파이썬의 `best = None` 관용구는 C++에 그대로 옮길 수 없다. `bool found` 깃발을 두거나 `long long best = LLONG_MIN;`(`<climits>`)으로 시작한다. `best = 0`으로 두면 전부 음수인 트리에서 0이 나오는 함정.
- 값이 최대 1000, 노드 1000개라 합은 ±10^6로 `int`도 되지만, 누적값에 `long long`을 쓰는 습관이 안전하다.

(3) 스스로 다시 짤 때 생각 순서

- "루트에서 내려오는 경로" → 내려가며 누적(깊이와 같은 방향). 서브트리 크기처럼 올라오며 합치는 게 아님을 구분.
- 리프 판정은 `children[v].empty()`로. 내부 노드 합을 답에 넣으면 두 번째 예제가 5로 틀린다.
- 초깃값 함정(`0` vs 첫 리프)을 반드시 `-7` 케이스로 검산.
```

**7) 좌우 대칭 이진 트리 판정** · Medium

- **요구사항**: 이진 트리가 루트를 기준으로 좌우 거울처럼 대칭인지 판정하라. 대칭이란 왼쪽 서브트리와 오른쪽 서브트리가 모양도 값도 서로 거울상이라는 뜻이다.

- **입력**: 첫 줄 N(1 ≤ N ≤ 500, 루트 1). 둘째 줄 노드 값 V[1..N]. 이후 N줄, i번째 줄 `left_i right_i`(없으면 0).

- **출력**: 대칭이면 `YES`, 아니면 `NO`.

- **예제**:

  - `7 / 1 2 2 3 4 4 3 / 2 3 / 4 5 / 6 7 / 0 0 / 0 0 / 0 0 / 0 0` → `YES`  (2(3,4)와 2(4,3)이 거울상)

  - `4 / 1 2 2 5 / 2 3 / 4 0 / 0 0 / 0 0` → `NO`  (왼쪽 2에는 왼쪽 자식 5가 있는데 오른쪽 2에는 오른쪽 자식이 없음)

- **셀프체크**: 노드 하나가 아니라 "두 노드 (a, b)"를 함께 재귀했는가 — a의 왼쪽은 b의 오른쪽과, a의 오른쪽은 b의 왼쪽과 짝지었는가. 둘 다 0이면 `true`, 하나만 0이면 `false`, 값이 다르면 `false` 순으로 기저를 두었는가. 반환형을 `bool`로 두고 `&&`의 단락 평가로 불필요한 재귀를 줄였는가. 자식 배열 이름을 `left`/`right`로 지으면 `<ios>`의 `std::left`/`std::right`와 겹쳐 `using namespace std;` 아래에서 모호해지니 `L`/`R`로 바꿨는가. 값은 같지만 배치가 거울상이 아닌 경우(`3 4 / 3 4`)를 걸렀는가. N=1이면 YES인가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

vector<int> val, L, R;

bool mirror(int a, int b) {
    if (a == 0 && b == 0) return true;
    if (a == 0 || b == 0) return false;  // 한쪽만 비면 모양이 다름
    if (val[a] != val[b]) return false;
    return mirror(L[a], R[b]) && mirror(R[a], L[b]);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    val.assign(n + 1, 0);
    L.assign(n + 1, 0);
    R.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> val[i];
    for (int i = 1; i <= n; i++) cin >> L[i] >> R[i];

    cout << (mirror(L[1], R[1]) ? "YES" : "NO") << '\n';
    return 0;
}
@@TESTS
--IN
7
1 2 2 3 4 4 3
2 3
4 5
6 7
0 0
0 0
0 0
0 0
--OUT
YES
--IN
4
1 2 2 5
2 3
4 0
0 0
0 0
--OUT
NO
--IN
7
1 2 2 3 4 3 4
2 3
4 5
6 7
0 0
0 0
0 0
0 0
--OUT
NO
--IN
1
5
0 0
--OUT
YES
@@EXPL
(1) 접근·핵심 아이디어

- 대칭은 "왼 서브트리와 오른 서브트리가 서로 거울"이라는 뜻이므로, 노드 하나를 재귀하는 대신 노드 쌍 (a, b)를 재귀한다. a의 왼쪽 ↔ b의 오른쪽, a의 오른쪽 ↔ b의 왼쪽을 짝지어 내려가며 모양(둘 다 없음/하나만 없음)과 값을 비교한다. 각 노드가 한 번씩 짝지어지므로 O(N).

(2) 코드 단계별

- 값·자식 배열을 크기 `n + 1`로 잡아 1-based로 읽는다. 0번은 "자식 없음"을 뜻하는 자리라 값이 들어가지 않는다.
- `mirror(a, b)`: 둘 다 0 → `true`, 하나만 0 → `false`, 값 다름 → `false`, 아니면 교차 재귀 두 개의 `&&`.
- 루트의 왼쪽·오른쪽 자식 쌍으로 시작해 결과를 삼항 연산자로 출력(양쪽 다 `const char*`라 타입이 맞는다).
- `&&`는 단락 평가라 왼쪽 재귀가 `false`면 오른쪽 재귀를 아예 호출하지 않는다 — 파이썬 `and`와 같은 성질이라 그대로 옮길 수 있다.

(3) 스스로 다시 짤 때 생각 순서

- "두 트리가 같은가" 유형의 변형 — 비교 대상을 교차(L↔R)시키는 것만 다르다.
- 기저 순서(둘 다 없음 → 하나만 없음 → 값 비교)를 지켜야 `val[0]` 같은 무의미한 접근이 없다.
- 배열 이름을 정할 때 `using namespace std;`가 끌어온 이름(`left`, `right`, `count`, `size`, `data`, `end` 등)과 겹치지 않는지 한 번 확인하는 습관.
- 값 배열이 좌우 대칭처럼 보여도(`3 4 3 4`) 배치가 거울이 아니면 NO — 값만 비교하면 안 되는 이유.
```

**8) k개 정렬 목록 합치기** · Medium

- **요구사항**: 오름차순으로 정렬된 목록 K개를 하나의 오름차순 목록으로 합쳐라. 힙에는 "각 목록의 현재 맨 앞 값"만 두어 매번 최솟값을 O(log K)에 뽑는다.

- **입력**: 첫 줄 K(1 ≤ K ≤ 100). 이후 K줄, 각 줄 첫 수는 목록 길이 L_i(0 ≤ L_i ≤ 100), 이어서 L_i개의 정수(오름차순). 총 원소 ≤ 5000.

- **출력**: 합친 결과를 공백으로 구분해 한 줄. 원소가 하나도 없으면 `EMPTY`.

- **예제**:

  - `3 / 3 1 4 9 / 2 2 8 / 1 5` → `1 2 4 5 8 9`

  - `2 / 0 / 2 3 3` → `3 3`  (빈 목록이 섞여 있음)

- **셀프체크**: **C++ `priority_queue`는 기본이 최대 힙이므로 `priority_queue<T, vector<T>, greater<T>>`로 선언해 최소 힙을 만들었는가** — 이걸 빠뜨리면 결과가 내림차순으로 나온다(파이썬 `heapq`는 기본이 최소 힙이라 이런 선언이 없다). 힙에 `tuple<int,int,int>`(값, 목록 번호, 위치)를 넣어 어느 목록에서 왔는지 알 수 있게 했는가(`tuple` 비교는 파이썬 튜플처럼 사전식이다). 꺼낼 때 `pq.top()`으로 읽고 `pq.pop()`으로 버리는 2단계인가. 하나를 꺼낼 때마다 같은 목록의 다음 원소를 넣었는가(끝이면 넣지 않음). 길이 0인 목록을 처음에 힙에 넣지 않도록 방어했는가. 전부 빈 목록이면 `EMPTY`인가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int k;
    cin >> k;
    vector<vector<int>> lists(k);
    for (int i = 0; i < k; i++) {
        int len;
        cin >> len;
        lists[i].resize(len);
        for (int j = 0; j < len; j++) cin >> lists[i][j];
    }

    // (값, 목록 번호, 위치) — greater<> 를 줘야 '최소' 힙이 된다.
    // C++ priority_queue 의 기본은 최대 힙이라는 점이 파이썬 heapq 와 정반대다.
    typedef tuple<int, int, int> Node;
    priority_queue<Node, vector<Node>, greater<Node>> pq;
    for (int i = 0; i < k; i++) {
        if (!lists[i].empty()) {         // 빈 목록은 넣지 않음
            pq.push(make_tuple(lists[i][0], i, 0));
        }
    }

    vector<int> out;
    while (!pq.empty()) {
        Node cur = pq.top();             // 읽고
        pq.pop();                        // 버리고
        int v = get<0>(cur), i = get<1>(cur), j = get<2>(cur);
        out.push_back(v);
        if (j + 1 < (int)lists[i].size()) {          // 같은 목록의 다음 원소
            pq.push(make_tuple(lists[i][j + 1], i, j + 1));
        }
    }

    if (out.empty()) {
        cout << "EMPTY" << '\n';
    } else {
        for (size_t t = 0; t < out.size(); t++) {
            if (t) cout << ' ';
            cout << out[t];
        }
        cout << '\n';
    }
    return 0;
}
@@TESTS
--IN
3
3 1 4 9
2 2 8
1 5
--OUT
1 2 4 5 8 9
--IN
2
0
2 3 3
--OUT
3 3
--IN
1
0
--OUT
EMPTY
--IN
2
2 1 1
2 1 1
--OUT
1 1 1 1
@@EXPL
(1) 접근·핵심 아이디어

- 목록이 각각 정렬돼 있으므로 "전체 최솟값"은 반드시 어떤 목록의 맨 앞에 있다. 각 목록의 맨 앞 하나씩만 힙에 넣어 두고, 최솟값을 꺼낼 때마다 그 목록의 다음 원소를 넣으면 힙 크기가 K를 넘지 않는다. 원소 총 수 M에 대해 O(M log K).

(2) 코드 단계별

- 목록을 읽어 `vector<vector<int>> lists`에 담는다.
- **힙 선언이 이 문제의 핵심 함정**이다. `priority_queue<Node> pq;`라고만 쓰면 최대 힙이 되어 답이 내림차순으로 나온다. 세 번째 템플릿 인자로 `greater<Node>`를 넘겨야 파이썬 `heapq`와 같은 최소 힙이 된다. 두 번째 인자(내부 컨테이너 `vector<Node>`)를 생략할 수 없으므로 셋을 모두 적는다.
- 비어 있지 않은 목록의 첫 원소를 `make_tuple(값, i, 0)`으로 push. `tuple`의 비교는 앞 원소부터 차례로 보는 사전식이라 파이썬 튜플과 동작이 같고, 값이 같아도 정수끼리 비교되어 오류가 없다.
- 힙이 빌 때까지 `pq.top()` → `pq.pop()` → 결과에 추가 → `j + 1`이 범위 안이면 다음 원소 push. `get<0>`/`get<1>`/`get<2>`로 튜플 원소를 꺼낸다(C++17이면 `auto [v, i, j] = cur;`도 된다).
- 결과가 없으면 `EMPTY`.

(3) 스스로 다시 짤 때 생각 순서

- "정렬된 것 여러 개 합치기" → 각각의 앞 원소만 경쟁시키는 힙.
- C++에서 힙을 쓸 때 가장 먼저 자문할 것: **최대인가 최소인가**. 파이썬 코드를 옮길 때 `heapq`가 보이면 거의 항상 `greater<>`가 필요하고, 반대로 파이썬이 `-x`로 부호를 뒤집어 최대 힙을 흉내 냈다면 C++에선 부호를 되돌리고 기본 `priority_queue`를 그냥 쓰면 된다.
- 튜플에 목록 번호·위치를 넣어야 다음 원소를 찾을 수 있다.
- 빈 목록·전부 빈 경우·전부 같은 값을 경계값으로 검산.
```

**9) 묶음 합치기 최소 비용** · Medium

- **요구사항**: 크기가 각각 s_i인 묶음 N개가 있다. 두 묶음을 하나로 합치는 비용은 두 크기의 합이고, 합친 묶음의 크기도 그 합이다. 모든 묶음이 하나가 될 때까지 합칠 때 드는 총 비용의 최솟값을 구하라.

- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 s_1..s_N(1 ≤ s_i ≤ 1000).

- **출력**: 최소 총 비용. N=1이면 0.

- **예제**:

  - `3 / 10 20 40` → `100`  (10+20=30, 30+40=70 → 30+70=100. 40+20을 먼저 하면 60+70=130으로 손해)

  - `4 / 1 1 1 1` → `8`  (2, 2, 4 → 2+2+4=8)

- **셀프체크**: 매번 "가장 작은 두 개"를 골라 합쳤는가(먼저 합친 묶음은 뒤에서 계속 다시 더해지므로 작은 것부터). **최소 힙이 필요하므로 `priority_queue<int, vector<int>, greater<int>>`로 선언했는가** — 기본형으로 두면 가장 큰 두 개를 합쳐 답이 커진다. 합친 결과를 힙에 다시 넣었는가. 파이썬 `heapify`에 해당하는 "벡터로 한 번에 만들기"를 반복자 두 개를 받는 생성자로 처리했는가. `pq.top()`으로 읽고 `pq.pop()`으로 버리는 2단계인가. N=1이면 루프에 안 들어가 0인가. N=2면 두 수의 합인가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> s(n);
    for (int i = 0; i < n; i++) cin >> s[i];

    // greater<int> 가 있어야 '최소' 힙. 기본 priority_queue 는 최대 힙이다.
    // 반복자 두 개를 받는 생성자가 파이썬 heapify 에 해당한다.
    priority_queue<int, vector<int>, greater<int>> pq(s.begin(), s.end());

    long long cost = 0;
    while (pq.size() > 1) {
        int a = pq.top(); pq.pop();      // 가장 작은 둘을
        int b = pq.top(); pq.pop();
        cost += (long long)a + b;        // 합치고
        pq.push(a + b);                  // 합친 묶음을 다시 넣는다
    }

    cout << cost << '\n';
    return 0;
}
@@TESTS
--IN
3
10 20 40
--OUT
100
--IN
4
1 1 1 1
--OUT
8
--IN
1
5
--OUT
0
--IN
2
3 4
--OUT
7
@@EXPL
(1) 접근·핵심 아이디어

- 일찍 합쳐진 묶음은 이후 합칠 때마다 비용에 다시 포함된다. 그러므로 큰 묶음은 가능한 한 늦게, 작은 묶음은 먼저 합쳐야 총 비용이 최소가 된다. "현재 가장 작은 두 개"를 반복해서 꺼내려면 최소 힙이 딱 맞다. N−1번의 pop·pop·push로 O(N log N).

(2) 코드 단계별

- 크기 배열을 읽어 `priority_queue<int, vector<int>, greater<int>> pq(s.begin(), s.end());`로 한 번에 힙을 만든다. 이 생성자가 내부에서 `make_heap`을 불러 O(N)에 정리하므로 파이썬 `heapify`와 같은 역할이다.
- **`greater<int>`를 빼면 최대 힙이 되어 `10 20 40`이 100이 아니라 130을 낸다.** 컴파일 오류가 아니라 답만 틀리는 종류의 실수라 더 위험하다.
- 힙에 2개 이상 남은 동안: `pq.top()`을 읽고 `pq.pop()`으로 버리기를 두 번 해 두 최솟값을 얻고, 합을 비용에 더한 뒤 합을 다시 push.
- 누적 비용 출력. 여기서는 최대 약 10^7이라 `int`도 되지만, 합계 누적은 `long long`으로 두는 편이 안전하다.
- `pq.size() > 1`의 `size()`는 부호 없는 타입이다. `pq.size() - 1 > 0` 같은 식으로 바꿔 쓰면 크기 0일 때 거대한 양수가 되어 무한 루프에 빠진다.

(3) 스스로 다시 짤 때 생각 순서

- "합친 결과가 다시 후보가 된다" → 정렬 한 번으로는 부족하고 힙이 필요한 이유.
- 힙을 선언하는 순간 "최대인가 최소인가"를 소리 내어 확인한다.
- 반례(`40+20` 먼저 → 130)로 "작은 것부터"가 왜 옳은지 확인.
- N=1은 루프 자체가 돌지 않아 0, N=2는 단 한 번 합침.
```

**10) BST 삭제 후 순회** · Hard

- **요구사항**: 서로 다른 정수 N개를 순서대로 BST에 삽입한 뒤, M개의 값을 순서대로 삭제하라(삭제할 값은 그 시점에 반드시 트리에 있고, 서로 다르다). 삭제 규칙: 자식이 없으면 그냥 제거, 하나면 그 자식으로 대체, 둘이면 오른쪽 서브트리의 최솟값(후계자)을 그 자리의 값으로 복사한 뒤 후계자 노드를 오른쪽 서브트리에서 삭제한다. 삭제가 끝난 트리의 전위·중위 순회를 출력하라.

- **입력**: 첫 줄 N M(1 ≤ M ≤ N ≤ 500), 둘째 줄 삽입 값 N개, 셋째 줄 삭제 값 M개.

- **출력**: 두 줄 — 전위 순회, 중위 순회(공백 구분). 트리가 비면 `EMPTY` 한 줄.

- **예제**:

  - `7 1 / 5 3 8 2 4 7 9 / 5` → `7 3 2 4 8 9 / 2 3 4 7 8 9`  (루트 5의 후계자 7을 루트로 복사, 리프 7 제거)

  - `7 2 / 5 3 8 2 4 7 9 / 2 8` → `5 3 4 9 7 / 3 4 5 7 9`  (2는 리프 제거; 8은 후계자 9로 대체)

- **셀프체크**: 삭제 함수가 "새 서브트리 루트"를 반환해 부모의 L/R에 다시 연결하는 구조인가(루트 자체가 삭제될 때도 `root = removeNode(root, x)`로 처리). 함수 이름을 `delete`로 지으면 **C++ 예약어**라 컴파일이 안 되니 `removeNode` 같은 이름으로 바꿨는가. 자식 둘인 경우 후계자를 "오른쪽으로 한 번, 그다음 왼쪽으로 끝까지"로 찾았는가. 후계자 값을 복사한 뒤 후계자를 오른쪽 서브트리에서 재귀 삭제했는가(후계자는 왼쪽 자식이 없어 0·1개 경우로 끝남). 값을 `map` 키로 쓰면 "값 복사"가 곤란하니 노드 번호 배열(`val`/`L`/`R`)로 구현했는가. 전부 삭제되면 `EMPTY`인가. 중위 순회는 삭제 후에도 오름차순인가(BST 성질 검산).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

vector<int> val, L, R;

int newNode(int x) {
    val.push_back(x);
    L.push_back(-1);
    R.push_back(-1);
    return (int)val.size() - 1;
}

// x 를 지운 뒤 이 서브트리의 새 루트를 반환. (delete 는 예약어라 못 쓴다)
int removeNode(int node, int x) {
    if (node == -1) return -1;
    if (x < val[node]) {
        L[node] = removeNode(L[node], x);
    } else if (x > val[node]) {
        R[node] = removeNode(R[node], x);
    } else {
        if (L[node] == -1) return R[node];   // 자식 0개 또는 오른쪽만
        if (R[node] == -1) return L[node];   // 왼쪽만
        int s = R[node];                     // 자식 2개: 후계자
        while (L[s] != -1) s = L[s];
        int sv = val[s];
        val[node] = sv;
        R[node] = removeNode(R[node], sv);
    }
    return node;
}

vector<int> pre, ino;

void dfs(int v) {
    if (v == -1) return;
    pre.push_back(val[v]);
    dfs(L[v]);
    ino.push_back(val[v]);
    dfs(R[v]);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<int> nums(n), dels(m);
    for (int i = 0; i < n; i++) cin >> nums[i];
    for (int i = 0; i < m; i++) cin >> dels[i];

    int root = -1;
    for (int i = 0; i < n; i++) {
        int x = nums[i];
        if (root == -1) { root = newNode(x); continue; }
        int cur = root;
        while (true) {
            if (x < val[cur]) {
                if (L[cur] == -1) { int nd = newNode(x); L[cur] = nd; break; }
                cur = L[cur];
            } else {
                if (R[cur] == -1) { int nd = newNode(x); R[cur] = nd; break; }
                cur = R[cur];
            }
        }
    }

    for (int i = 0; i < m; i++) root = removeNode(root, dels[i]);

    if (root == -1) {
        cout << "EMPTY" << '\n';
        return 0;
    }
    dfs(root);
    for (size_t i = 0; i < pre.size(); i++) {
        if (i) cout << ' ';
        cout << pre[i];
    }
    cout << '\n';
    for (size_t i = 0; i < ino.size(); i++) {
        if (i) cout << ' ';
        cout << ino[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
7 1
5 3 8 2 4 7 9
5
--OUT
7 3 2 4 8 9
2 3 4 7 8 9
--IN
7 2
5 3 8 2 4 7 9
2 8
--OUT
5 3 4 9 7
3 4 5 7 9
--IN
3 3
2 1 3
2 1 3
--OUT
EMPTY
--IN
4 1
4 2 1 3
2
--OUT
4 3 1
1 3 4
@@EXPL
(1) 접근·핵심 아이디어

- BST 삭제는 세 경우로 나뉜다. 자식 0개·1개는 그 노드를 자식(또는 없음)으로 갈아 끼우면 끝이고, 자식 2개는 "오른쪽 서브트리의 최솟값(후계자)"이 BST 순서를 깨지 않고 그 자리에 올 수 있는 유일한 후보라 값을 복사한 뒤 후계자를 오른쪽에서 지운다. 후계자는 왼쪽 자식이 없으므로 그 삭제는 반드시 0·1개 경우로 끝난다. 각 삭제는 O(높이).

(2) 코드 단계별

- 값을 `map` 키로 쓰지 않고 `val`/`L`/`R` 벡터에 노드 번호로 저장한다 — "값 복사"가 필요하기 때문. 이름을 `left`/`right`로 지으면 `std::left`/`std::right`와 겹치므로 `L`/`R`.
- 삽입은 L4와 같은 while 하강. `L[cur] = newNode(x)`를 한 줄로 쓰지 않고 새 번호를 `nd`에 먼저 받는다 — `newNode` 안의 `push_back`이 벡터를 재할당할 수 있기 때문.
- `removeNode(node, x)`: `delete`가 C++ 예약어라 이름을 바꿨다. x가 작으면 왼쪽, 크면 오른쪽으로 재귀하고 그 반환값을 자식 링크에 다시 대입. 찾으면 세 경우 처리 후 `node`(또는 대체 자식)를 반환.
- 후계자 값을 지역 변수 `sv`에 먼저 담고 `val[node] = sv;` 다음에 `removeNode(R[node], sv)`를 부른다. `val[s]`를 그대로 인자로 넘기면 `val[node]`를 이미 덮어쓴 뒤라 읽는 값이 헷갈리기 쉽다.
- 모든 삭제 후 전위·중위를 한 DFS에서 만들어 출력, 루트가 -1이면 `EMPTY`. N ≤ 500이라 사슬이어도 재귀 깊이가 안전하다.

(3) 스스로 다시 짤 때 생각 순서

- "재귀가 새 서브트리 루트를 반환"하는 구조를 먼저 잡으면 루트 삭제·자식 갈아 끼우기가 한 코드로 처리된다.
- 후계자 찾기는 "오른쪽 한 번, 그다음 왼쪽 끝까지"(왼쪽 서브트리 최댓값을 쓰는 방식도 있지만 문제가 후계자를 지정).
- C++로 옮길 때 이름 충돌을 먼저 점검한다: `delete`·`new`·`class`·`template`은 예약어, `left`·`right`·`count`·`data`는 `std`와 겹칠 수 있다.
- 삭제 뒤 중위 순회가 여전히 오름차순인지가 가장 빠른 검산. 전부 삭제한 `EMPTY`와 루트 삭제 케이스를 꼭 돌려 볼 것.
```

**11) 배열 힙 직접 구현 — 삽입과 삭제** · Hard

- **요구사항**: 빈 배열(0-based) 최소 힙에 명령을 처리한다. `push x`: 끝에 붙인 뒤 부모가 더 클 동안 교환하며 올라간다. `pop`: 루트(최솟값)를 꺼내 출력하고, 마지막 원소를 루트로 옮긴 뒤 "두 자식 중 더 작은 쪽(같으면 왼쪽)이 현재 값보다 작은 동안" 그 자식과 교환하며 내려간다. 빈 힙에서 `pop`이면 `-1`을 출력. 모든 명령 뒤 배열 상태를 출력하라. `priority_queue`는 내부 배열 배치가 이 규칙과 다르고 들여다볼 수도 없으므로 쓰지 않는다.

- **입력**: 첫 줄 Q(1 ≤ Q ≤ 1000), 이후 Q줄에 `push x`(−10^9 ≤ x ≤ 10^9) 또는 `pop`.

- **출력**: `pop`마다 결과를 한 줄씩, 마지막 줄에 최종 배열(인덱스 0부터 공백 구분; 비면 `EMPTY`).

- **예제**:

  - `7 / push 5 / push 3 / push 8 / push 1 / pop / pop / push 2` → `1 / 3 / 2 8 5`
    - 검산: 삽입 후 `[1,3,8,5]` → pop 1: 5를 루트로 `[5,3,8]`, 자식 3<5 교환 `[3,5,8]` → pop 3: `[8,5]` → `[5,8]` → push 2: `[5,8,2]` → 부모 5>2 교환 `[2,8,5]`

  - `2 / pop / push 4` → `-1 / 4`

- **셀프체크**: pop에서 마지막 원소를 먼저 떼어낸 뒤(`int last = heap.back(); heap.pop_back();`) 힙이 비어 있지 않을 때만 루트에 덮어썼는가(원소 1개일 때 인덱스 오류 방지). `vector::pop_back()`도 값을 돌려주지 않으므로 `back()`으로 읽고 `pop_back()`으로 버리는 2단계인가. sift-down에서 오른쪽 자식이 없을 수 있음을 `r < size`로 검사했는가(`size`를 `int`로 두어야 비교가 안전하다). "더 작은 자식"을 고를 때 왼쪽을 먼저 후보로 두어 동점이면 왼쪽과 교환하는가. 비교가 엄격(`<`)이라 같은 값이면 멈추는가. 최종 배열이 힙 조건(부모 ≤ 자식)을 만족하는지 검산했는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

vector<int> heap;

void heapPush(int x) {
    heap.push_back(x);
    int j = (int)heap.size() - 1;
    while (j > 0) {                      // sift-up
        int p = (j - 1) / 2;
        if (heap[p] > heap[j]) {
            swap(heap[p], heap[j]);
            j = p;
        } else {
            break;
        }
    }
}

int heapPop() {
    int top = heap[0];
    int last = heap.back();              // 읽고
    heap.pop_back();                     // 버리고 (pop_back 도 값을 안 준다)
    if (!heap.empty()) {                 // 남은 게 있으면 루트에 덮고 내려간다
        heap[0] = last;
        int j = 0;
        int size = (int)heap.size();
        while (true) {                   // sift-down
            int l = 2 * j + 1;
            int r = 2 * j + 2;
            int small = j;
            if (l < size && heap[l] < heap[small]) small = l;
            if (r < size && heap[r] < heap[small]) small = r;
            if (small == j) break;
            swap(heap[j], heap[small]);
            j = small;
        }
    }
    return top;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    for (int t = 0; t < q; t++) {
        string cmd;
        cin >> cmd;
        if (cmd == "push") {
            int x;
            cin >> x;
            heapPush(x);
        } else {
            if (heap.empty()) cout << -1 << '\n';
            else cout << heapPop() << '\n';
        }
    }

    if (heap.empty()) {
        cout << "EMPTY" << '\n';
    } else {
        for (int i = 0; i < (int)heap.size(); i++) {
            if (i) cout << ' ';
            cout << heap[i];
        }
        cout << '\n';
    }
    return 0;
}
@@TESTS
--IN
7
push 5
push 3
push 8
push 1
pop
pop
push 2
--OUT
1
3
2 8 5
--IN
2
pop
push 4
--OUT
-1
4
--IN
5
push 9
push 4
push 7
push 1
pop
--OUT
1
4 9 7
--IN
2
push 1
pop
--OUT
1
EMPTY
@@EXPL
(1) 접근·핵심 아이디어

- 힙의 두 기본 연산을 배열 위에서 직접 구현한다. push는 문제 4의 sift-up 그대로, pop은 "루트를 꺼내고 마지막 원소를 루트로 올린 뒤, 더 작은 자식과 바꾸며 내려가기(sift-down)"다. 두 연산 모두 트리 높이만큼만 움직이므로 O(log N). 출력 배열이 규칙에 따라 유일하게 정해지므로, 내부 배치를 보여 주지 않는 `priority_queue`를 쓰면 안 된다.

(2) 코드 단계별

- `heapPush(x)`: `push_back` 후 `(j - 1) / 2` 부모와 비교·`swap`.
- `heapPop()`: `top = heap[0]`을 보관하고 `last = heap.back(); heap.pop_back();`. 힙이 남아 있으면 `heap[0] = last` 후 sift-down — 왼쪽 자식을 먼저 후보로, 오른쪽이 더 작을 때만 후보 교체, 후보가 자기 자신이면 종료.
- `size`를 `int`로 받아 두는 것이 중요하다. `heap.size()`(부호 없음)와 `l`·`r`(부호 있음)을 직접 비교하면 컴파일러 경고가 나고, 크기가 0인 경우의 산술이 위험해진다.
- 명령을 `cin >> cmd`로 읽어 `push`/`pop` 분기. `pop`은 빈 힙이면 `-1`.
- 마지막에 배열 상태 한 줄(비면 `EMPTY`).

(3) 스스로 다시 짤 때 생각 순서

- 0-based 인덱스 공식(부모 `(j - 1) / 2`, 자식 `2j + 1`·`2j + 2`)을 먼저 적는다.
- pop에서 "마지막 원소 떼기 → 비었는지 검사 → 루트 덮기" 순서가 원소 1개일 때의 오류를 막는다. 빈 `vector`에 `back()`을 부르면 예외가 아니라 정의되지 않은 동작이므로, 호출부에서 `heap.empty()`를 먼저 확인하는 구조를 유지한다.
- 자식이 하나(오른쪽 없음)인 경우와 동점 시 왼쪽 우선 규칙을 `5 / push 9 4 7 1 / pop`(`4 9 7`)로 검산. 마지막 배열이 힙 조건을 만족하는지 눈으로 확인.
```

**12) 트리의 지름** · Hard

- **요구사항**: 노드 1..N과 가중치가 있는 간선 N−1개(방향 없음)로 주어진 트리에서, 두 노드 사이 거리(경로 위 가중치 합)의 최댓값(지름)을 구하라.

- **입력**: 첫 줄 N(1 ≤ N ≤ 1000). 이후 N−1줄에 `u v w`(1 ≤ w ≤ 100).

- **출력**: 지름.

- **예제**:

  - `5 / 1 2 3 / 1 3 2 / 3 4 5 / 3 5 1` → `10`  (2→1→3→4: 3+2+5)

  - `3 / 1 2 7 / 1 3 7` → `14`  (2→1→3)

- **셀프체크**: "아무 노드에서 가장 먼 노드 a를 찾고, a에서 가장 먼 거리"가 지름이라는 두 번 탐색 원리를 썼는가. 가중치를 함께 담아야 하므로 인접 리스트를 `vector<vector<pair<int,int>>>`로 두었는가(파이썬 튜플 → C++ `pair`). BFS에서 거리 배열 `dist`를 -1로 초기화해 되돌아가기를 막았는가(방향 없는 간선). 두 값을 함께 반환해야 하니 함수 반환형을 `pair<int,int>`로 두었는가. 가장 먼 노드가 여럿이라도 지름 값은 같은가. N=1이면 0인가. 모든 쌍을 다 재면 O(N²)인데 두 번 탐색은 O(N)임을 이해했는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int n;
vector<vector<pair<int, int>>> adj;      // (이웃, 가중치)

// start 에서 가장 먼 노드와 그 거리
pair<int, int> farthest(int start) {
    vector<int> dist(n + 1, -1);
    dist[start] = 0;
    queue<int> q;
    q.push(start);
    int far = start;
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        if (dist[v] > dist[far]) far = v;
        for (size_t k = 0; k < adj[v].size(); k++) {
            int w = adj[v][k].first, c = adj[v][k].second;
            if (dist[w] == -1) {         // 아직 안 간 곳만
                dist[w] = dist[v] + c;
                q.push(w);
            }
        }
    }
    return make_pair(far, dist[far]);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    adj.assign(n + 1, vector<pair<int, int>>());
    for (int i = 0; i < n - 1; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back(make_pair(v, w));
        adj[v].push_back(make_pair(u, w));
    }

    pair<int, int> first = farthest(1);  // 1번에서 가장 먼 노드
    pair<int, int> second = farthest(first.first);
    cout << second.second << '\n';       // a 에서 가장 먼 거리가 지름
    return 0;
}
@@TESTS
--IN
5
1 2 3
1 3 2
3 4 5
3 5 1
--OUT
10
--IN
3
1 2 7
1 3 7
--OUT
14
--IN
1
--OUT
0
--IN
4
1 2 1
2 3 1
3 4 1
--OUT
3
@@EXPL
(1) 접근·핵심 아이디어

- 트리에서는 "임의의 노드에서 가장 먼 노드"가 항상 지름의 한쪽 끝이 된다. 그래서 1번에서 가장 먼 노드 a를 찾고, a에서 가장 먼 거리를 재면 그것이 지름이다. 모든 쌍을 재면 O(N²)이지만 이 방법은 탐색 두 번으로 O(N). 가중치가 있어도 트리는 경로가 유일하므로 BFS로 거리를 누적해도 된다.

(2) 코드 단계별

- 간선을 `pair<int,int>`(이웃, 가중치)로 양쪽 인접 리스트에 넣는다. 리스트 타입은 `vector<vector<pair<int,int>>>`.
- `farthest(start)`: `dist`를 -1로 초기화하고 BFS로 `dist[w] = dist[v] + c`를 채우며, 거리가 가장 큰 노드 `far`를 추적해 `make_pair(far, dist[far])`를 반환한다. C++ 함수는 값을 하나만 돌려주므로 두 개가 필요하면 `pair`(또는 `tuple`, 참조 인자, 작은 `struct`)를 쓴다.
- `farthest(1)`로 a를 얻고, `farthest(a)`의 거리를 출력.
- `n`과 `adj`를 전역에 둬서 함수가 매개변수 없이 쓸 수 있게 했다. 지역으로 두려면 `const vector<...>&`로 넘겨 복사를 피한다 — 값으로 넘기면 인접 리스트 전체가 복사된다.
- 거리는 최대 1000 × 100 = 10^5라 `int`로 충분하다.

(3) 스스로 다시 짤 때 생각 순서

- "가장 먼 두 노드" → 두 번 탐색 원리를 떠올린다(증명은 몰라도 결론은 외워 둘 것).
- 방향 없는 간선이므로 `dist == -1` 검사로 부모로 되돌아가지 않게 한다.
- N=1이면 간선 줄이 없고 BFS가 시작 노드만 보므로 거리 0이 나온다. 사슬(`3`)로도 경계값 검산. 가장 먼 노드가 여럿이면 어느 것을 골라도 지름 값은 같다.
```
