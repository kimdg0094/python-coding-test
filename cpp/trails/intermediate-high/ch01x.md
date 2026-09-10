## L5. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch01(트리)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. 루트 고정 순회·서브트리 누적·지름·이진 트리 스택 순회·Tree DP·LCA를 소재와 입력 형식을 바꿔 여러 번 다시 짜 본다.
- **반복 훈련 개념**:
  - 트리는 `vector<vector<int>> g(n + 1)` 인접 리스트로. 루트를 고정해 **반복 BFS**로 `parent/depth/order`를 채우고, 서브트리 값은 `for (int i = (int)order.size() - 1; i >= 0; i--) { int u = order[i]; if (parent[u]) acc[parent[u]] += acc[u]; }`로 아래→위 누적
  - **깊이·부모·서브트리 크기는 재귀 대신 반복(BFS/명시적 스택)으로 구한다.** 일자 트리에서 재귀 DFS는 호출 깊이가 N까지 가서 스택을 넘긴다(C++의 기본 스택은 보통 1MB 남짓이고, 넘치면 예외가 아니라 그냥 죽는다)
  - 지름은 BFS 두 번(`a = far(1)`, `b = far(a)`), 그리고 "임의 정점의 최원점은 지름 끝점 중 하나"라 `ecc[v] = max(dA[v], dB[v])`
  - 이진 트리는 `vector<int> lch, rch, value` 배열 + 명시적 `stack<int>`으로 재귀 없이 순회. C++ `stack::pop()`은 **값을 반환하지 않으므로** `int u = st.top(); st.pop();` 두 줄로 쓴다. 레벨은 `cur = nxt`로 한 층씩 교체
  - Tree DP는 정점당 상태 2개(`dp0[u]`, `dp1[u]`)를 두고 자식→부모로 `min`/`max`/`+` 누적
  - LCA는 깊이 맞춘 뒤 같이 올리기(`while (a != b) { a = par[a]; b = par[b]; }` — C++엔 동시 대입이 없지만 `a`와 `b`가 서로 다른 변수이고 `par`는 바뀌지 않으므로 두 줄로 나눠도 안전하다) 또는 `up[k][v] = up[k-1][up[k-1][v]]` 희소 표 `vector<vector<int>> up(LOG, vector<int>(n + 1))`
  - 희소 표의 `LOG`는 **2^LOG > N**이 되게 잡는다(`int LOG = 1; while ((1 << LOG) <= n) LOG++;`). 부족하면 깊은 트리에서 점프가 모자라 답이 틀린다
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '트리'·'최소 공통 조상' 단계, solved.ac CLASS 4~5의 트리 DP·LCA 문제, NeetCode 150의 'Trees'(지그재그 레벨 순회·BST 유효성·k번째 원소).
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 루트를 바꾼 부모 표 | Easy | 루트 고정 BFS·parent | 반복 훈련 |
| 2 | 지그재그 레벨 순회 | Medium | 레벨별 큐 교체·홀수 층 뒤집기 | 유형 확장 (NeetCode 'Trees' 스타일) |
| 3 | BST 유효성 검사 | Medium | 스택 순회 + (lo, hi) 범위 전파 | 유형 확장 (NeetCode 'Trees' 스타일) |
| 4 | 임계값 이상 서브트리 수 | Medium | order 역순 서브트리 합 | 반복 훈련 |
| 5 | 트리 센트로이드 찾기 | Medium | 서브트리 크기 → 제거 후 최대 조각 | 반복 훈련 |
| 6 | 부모 배열로 경로 위 정점 수 | Medium | 단순 상승 LCA + 거리 공식 | 반복 훈련 |
| 7 | BST k번째 작은 값 질의 | Hard | BST 삽입 + 서브트리 크기 + 순위 탐색 | 반복 훈련 |
| 8 | 경비 초소 최소 비용 | Hard | Tree DP 두 상태(min 버전) | 유형 확장 (백준 '트리' 단계 스타일) |
| 9 | 모든 정점의 최원거리 | Hard | 지름 끝점 BFS 3회 | 반복 훈련 |
| 10 | 경로 위 최대 간선 가중치 질의 | Hard | 희소 표 + 점프별 최댓값 | 유형 확장 (백준 '최소 공통 조상' 단계 스타일) |

**문제**

**1) 루트를 바꾼 부모 표** · Easy

- **요구사항**: 트리와 루트 정점 r이 주어진다. r을 루트로 잡았을 때 각 정점의 부모를 구하라. 루트의 부모는 0으로 둔다.
- **입력**: 첫 줄에 `N r` (1 ≤ N ≤ 300, 1 ≤ r ≤ N). 다음 N-1줄에 간선 `a b` (1-indexed).
- **출력**: 정점 1부터 N까지의 부모를 공백으로 구분해 한 줄에.
- **예제**:
  `7 3 / 1 2 / 1 3 / 3 4 / 3 5 / 5 6 / 5 7` → `3 1 0 3 3 5 5`
  (3이 루트이므로 1의 부모는 3, 2의 부모는 1)
  `4 4 / 1 2 / 2 3 / 3 4` → `2 3 4 0`
- **셀프체크**: 루트가 1이 아닐 때 BFS 시작점을 r로 바꿨는가? 방문 표시를 `parent == -1`로 대신하면 루트(부모 0)와 미방문(-1)이 구분되는가? N=1이면 `0` 하나만 출력되는가? 여러 값을 한 줄에 낼 때 구분자를 직접 넣어야 하므로(`if (i > 1) cout << ' ';`), 끝에 여분의 공백이 붙지 않게 인덱스로 제어했는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, r;
    cin >> n >> r;
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        g[a].push_back(b);
        g[b].push_back(a);
    }
    vector<int> parent(n + 1, -1);      // -1: 아직 방문 안 함
    parent[r] = 0;                      // 루트의 부모는 0
    queue<int> q;
    q.push(r);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : g[u]) {
            if (parent[v] == -1) {
                parent[v] = u;
                q.push(v);
            }
        }
    }
    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << parent[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
7 3
1 2
1 3
3 4
3 5
5 6
5 7
--OUT
3 1 0 3 3 5 5
--IN
4 4
1 2
2 3
3 4
--OUT
2 3 4 0
--IN
1 1
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 트리는 루트를 어디로 잡느냐에 따라 부모 관계가 완전히 달라진다. "루트 고정 → BFS로 방향 주기"가 모든 트리 문제의 첫 단계이며, 여기서는 시작점만 1 대신 r로 바꾸면 된다.
- 무방향 인접 리스트에서 되돌아가는 간선을 막아야 하므로 방문 여부가 필요한데, `parent`를 -1로 초기화하면 방문 배열을 따로 두지 않아도 된다(루트는 0, 미방문은 -1로 구분).

(2) 코드 단계별

- `vector<vector<int>> g(n + 1)`을 양방향으로 채운다.
- `parent[r] = 0`으로 두고 `queue<int>`에 r을 넣어 BFS. 이웃 v가 -1(미방문)이면 `parent[v] = u`로 기록하고 큐에 넣는다.
- `parent[1..N]`을 공백으로 출력한다.

(3) 스스로 다시 짤 때 생각 순서

- 루트 r 확인 → BFS 시작점을 r로 → 방문 체크를 parent 값으로 대신 → 출력. N=1이면 간선이 없어 BFS가 바로 끝나고 `0`만 출력된다.
- 시간 O(N), 공간 O(N). BFS는 반복문이라 일자 트리에서도 스택이 넘치지 않는다 — 같은 일을 재귀 DFS로 하면 N이 커질 때 위험하다.
- `queue::pop()`은 값을 돌려주지 않는다. `int u = q.front(); q.pop();`를 한 쌍으로 외운다.
```

**2) 지그재그 레벨 순회** · Medium

- **요구사항**: 1번을 루트로 하는 이진 트리가 각 노드의 왼쪽/오른쪽 자식으로 주어진다. 레벨(깊이)별로 노드 번호를 출력하되, 깊이 0은 왼쪽→오른쪽, 깊이 1은 오른쪽→왼쪽, 깊이 2는 다시 왼쪽→오른쪽 … 처럼 방향을 번갈아 가며 출력하라.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 다음 N줄: `node left right` (자식이 없으면 0). 노드 번호는 1..N.
- **출력**: 깊이 0부터 한 줄에 한 레벨씩, 노드 번호를 공백으로 구분.
- **예제**:
  `7 / 1 2 3 / 2 4 5 / 3 6 7 / 4 0 0 / 5 0 0 / 6 0 0 / 7 0 0` → `1 / 3 2 / 4 5 6 7`
  `4 / 1 0 2 / 2 3 0 / 3 0 4 / 4 0 0` → `1 / 2 / 3 / 4`
- **셀프체크**: 다음 레벨을 만들 때는 반드시 **원래(왼→오) 순서**의 현재 레벨을 훑어야 한다 — 뒤집은 벡터로 자식을 모으면 다음 레벨 순서가 꼬인다. 그래서 `cur`는 항상 왼→오로 두고, 출력 직전에 **복사본**을 `reverse` 한다(`reverse(cur.begin(), cur.end())`로 원본을 뒤집으면 다음 층이 틀린다). 자식 배열 이름을 `left`/`right`로 쓰면 `using namespace std;` 아래에서 `<iomanip>`의 `std::left`/`std::right` 조작자와 이름이 겹치니 `lch`/`rch`처럼 다른 이름을 쓴다. 자식 0을 큐에 넣지 않았는가? 한쪽으로 치우친 트리에서 각 레벨이 한 개씩 출력되는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> lch(n + 1, 0), rch(n + 1, 0);   // left/right 는 std 조작자와 충돌
    for (int i = 0; i < n; i++) {
        int node, l, r;
        cin >> node >> l >> r;
        lch[node] = l;
        rch[node] = r;
    }
    vector<int> cur;
    cur.push_back(1);          // 현재 레벨(항상 왼→오 순서로 유지)
    int level = 0;
    while (!cur.empty()) {
        vector<int> nxt;
        for (int u : cur) {    // 원래 순서로 자식을 모아야 다음 레벨 순서가 맞다
            if (lch[u]) nxt.push_back(lch[u]);
            if (rch[u]) nxt.push_back(rch[u]);
        }
        vector<int> row = cur;                       // 복사본만 뒤집는다
        if (level % 2 == 1) reverse(row.begin(), row.end());
        for (size_t i = 0; i < row.size(); i++) {
            if (i) cout << ' ';
            cout << row[i];
        }
        cout << '\n';
        cur = nxt;
        level++;
    }
    return 0;
}
@@TESTS
--IN
7
1 2 3
2 4 5
3 6 7
4 0 0
5 0 0
6 0 0
7 0 0
--OUT
1
3 2
4 5 6 7
--IN
4
1 0 2
2 3 0
3 0 4
4 0 0
--OUT
1
2
3
4
--IN
1
1 0 0
--OUT
1
--IN
6
1 2 3
2 0 4
3 5 0
4 6 0
5 0 0
6 0 0
--OUT
1
3 2
4 5
6
@@EXPL
(1) 접근·핵심 아이디어

- 레벨 순회(BFS)를 "한 층 전체를 `vector`로 들고 다음 층 `vector`로 교체"하는 형태로 쓰면 레벨 경계가 자연스럽게 생긴다. 지그재그는 출력할 때만 홀수 층을 뒤집으면 된다.
- 함정: 다음 층을 만들 때 뒤집힌 순서로 자식을 모으면 그 다음 층의 "왼→오" 기준이 깨진다. 내부 상태(`cur`)는 항상 왼→오로 유지하고, 뒤집기는 출력용 복사본에만 적용한다. C++ `reverse`는 **제자리(in-place)** 로 뒤집으므로 원본에 직접 걸면 안 된다.

(2) 코드 단계별

- `lch/rch` 배열을 입력대로 채운다(자식 없음은 0).
- `cur = {1}`, `level = 0`에서 시작. `cur`를 원래 순서로 돌며 0이 아닌 자식만 `nxt`에 추가.
- `vector<int> row = cur;`로 복사한 뒤 `level`이 홀수면 `reverse(row...)`, 그 줄을 출력. `cur = nxt; level++;`.
- `cur`가 비면 종료.

(3) 스스로 다시 짤 때 생각 순서

- 레벨 단위 BFS 골격(현재 층 → 다음 층) → 홀수 층만 출력 방향 반전 → 자식 0 걸러내기. 시간 O(N), 공간 O(가장 넓은 층).
- `using namespace std;` 아래에서 `left`, `right`, `size`, `count`, `next`, `prev`, `distance`, `data` 같은 이름은 표준 라이브러리와 겹친다. 전역에 그런 이름을 두면 모호해지므로 짧고 겹치지 않는 이름을 고르는 습관을 들인다.
- 재귀 DFS로 깊이별 목록을 모아도 되지만, 치우친 트리에서 깊이가 N까지 커질 수 있으므로 반복형이 안전하다.
```

**3) BST 유효성 검사** · Medium

- **요구사항**: 1번을 루트로 하는 이진 트리가 각 노드의 값과 자식으로 주어진다. 모든 노드에서 "왼쪽 서브트리의 모든 값 < 노드 값 < 오른쪽 서브트리의 모든 값"이 성립하면(같은 값도 허용하지 않음) `YES`, 아니면 `NO`를 출력하라.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 다음 N줄: `node value left right` (자식 없으면 0, -10^9 ≤ value ≤ 10^9).
- **출력**: `YES` 또는 `NO`.
- **예제**:
  `5 / 1 8 2 3 / 2 3 4 5 / 3 10 0 0 / 4 1 0 0 / 5 6 0 0` → `YES`
  `4 / 1 10 2 0 / 2 5 3 4 / 3 1 0 0 / 4 12 0 0` → `NO`
  (노드 4(값 12)는 부모 5보다는 크지만 조상 10의 왼쪽에 있으므로 10보다 작아야 한다)
- **셀프체크**: 부모와만 비교하면 둘째 예제를 잡지 못한다 — 각 노드가 가질 수 있는 **허용 범위 (lo, hi)** 를 위에서 아래로 전파했는가? 같은 값이 나오면 NO로 판정했는가(부등호가 엄격한가)? 노드 하나뿐인 트리는 YES인가? 범위 경계는 값(±10^9)보다 넉넉해야 하므로 `long long`으로 `-1e18`, `1e18`을 쓴다 — `int`의 `INT_MIN`/`INT_MAX`를 쓰면 값이 딱 그 경계일 때 판정이 흔들린다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> val(n + 1, 0);
    vector<int> lch(n + 1, 0), rch(n + 1, 0);
    for (int i = 0; i < n; i++) {
        int node, l, r;
        long long v;
        cin >> node >> v >> l >> r;
        val[node] = v;
        lch[node] = l;
        rch[node] = r;
    }
    const long long NEG = -1e18, POS = 1e18;
    // (노드, 허용 하한, 허용 상한) — 열린 구간
    stack<tuple<int, long long, long long>> st;
    st.push(make_tuple(1, NEG, POS));
    bool ok = true;
    while (!st.empty()) {
        int u;
        long long lo, hi;
        tie(u, lo, hi) = st.top();
        st.pop();
        if (!(lo < val[u] && val[u] < hi)) {
            ok = false;
            break;
        }
        if (lch[u]) st.push(make_tuple(lch[u], lo, val[u]));
        if (rch[u]) st.push(make_tuple(rch[u], val[u], hi));
    }
    cout << (ok ? "YES" : "NO") << '\n';
    return 0;
}
@@TESTS
--IN
5
1 8 2 3
2 3 4 5
3 10 0 0
4 1 0 0
5 6 0 0
--OUT
YES
--IN
4
1 10 2 0
2 5 3 4
3 1 0 0
4 12 0 0
--OUT
NO
--IN
1
1 5 0 0
--OUT
YES
--IN
2
1 5 2 0
2 5 0 0
--OUT
NO
@@EXPL
(1) 접근·핵심 아이디어

- BST 조건은 "부모와 자식의 비교"가 아니라 "조상 전체가 만드는 범위"다. 루트는 (-무한, +무한), 왼쪽 자식으로 내려가면 상한이 부모 값으로, 오른쪽으로 내려가면 하한이 부모 값으로 좁아진다. 각 노드 값이 자기 범위 안에 있으면 유효하다.
- 이렇게 "부모 정보를 자식에 전파"하는 것은 전위 순회 패턴이며, 명시적 `stack`으로 반복 구현하면 깊은 트리에서도 안전하다.

(2) 코드 단계별

- `val/lch/rch` 배열을 채운다.
- `stack<tuple<int, long long, long long>>`에 `(1, NEG, POS)`를 넣고 시작. `tie(u, lo, hi) = st.top(); st.pop();`로 꺼낸 뒤 `lo < val[u] && val[u] < hi`를 어기면 즉시 NO.
- 왼쪽 자식은 `(lch, lo, val[u])`, 오른쪽 자식은 `(rch, val[u], hi)`로 범위를 좁혀 push.
- 스택이 빌 때까지 위반이 없으면 YES.

(3) 스스로 다시 짤 때 생각 순서

- "범위 전파" 아이디어 확정 → 스택 원소를 (노드, lo, hi) 튜플로 → 열린 구간 비교로 중복 값 배제 → 위반 즉시 종료. 시간 O(N), 공간 O(높이).
- C++에는 `-inf`가 없으니 값 범위보다 확실히 넓은 상수를 `long long`으로 잡는다. 값이 `int` 경계에 있을 수 있는 문제에서 `INT_MIN`을 초기 하한으로 쓰면 첫 비교부터 틀린다.
- 대안: 중위 순회가 엄격히 증가하는지 확인해도 된다. 어느 쪽이든 "부모하고만 비교"는 오답임을 기억하자.
```

**4) 임계값 이상 서브트리 수** · Medium

- **요구사항**: 정점 1을 루트로 하는 트리의 각 정점에 정수 가중치(음수 가능)가 있다. 서브트리(자신 포함) 가중치 합이 T 이상인 정점의 개수를 세고, 그 정점 번호들을 오름차순으로 출력하라.
- **입력**: 첫 줄 `N T` (1 ≤ N ≤ 300, -10^6 ≤ T ≤ 10^6). 둘째 줄 정점 1..N의 가중치(-100 ≤ w ≤ 100). 다음 N-1줄 간선 `a b`.
- **출력**: 첫 줄에 개수. 개수가 1 이상이면 둘째 줄에 해당 정점 번호를 오름차순으로 공백 구분.
- **예제**:
  `7 20 / 10 5 20 8 15 -6 9 / 1 2 / 1 3 / 3 4 / 3 5 / 5 6 / 5 7` → `2 / 1 3`
  (정점 5의 서브트리 합은 15-6+9=18로 미달, 3은 46, 1은 61)
  `3 100 / 1 2 3 / 1 2 / 2 3` → `0`
- **셀프체크**: 가중치에 음수가 있으면 "부모 합 ≥ 자식 합"이 성립하지 않는다 — 조상이 미달이어도 자식이 조건을 만족할 수 있음을 반영했는가? 리프의 합은 자기 가중치 그대로인가? 개수 0일 때 둘째 줄을 출력하지 않는가? 합 배열을 만들 때 `vector<long long> ssum = w;`처럼 **값 복사**해야 한다(파이썬의 `w[:]`에 해당). `vector<long long>& ssum = w;`로 참조를 잡으면 원본 가중치가 누적으로 덮인다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long t;
    cin >> n >> t;
    vector<long long> w(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> w[i];
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        g[a].push_back(b);
        g[b].push_back(a);
    }
    vector<int> parent(n + 1, 0), order;
    vector<char> seen(n + 1, 0);
    seen[1] = 1;
    queue<int> q;
    q.push(1);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (int v : g[u]) {
            if (!seen[v]) {
                seen[v] = 1;
                parent[v] = u;
                q.push(v);
            }
        }
    }
    vector<long long> ssum = w;              // 값 복사 (참조로 잡으면 원본이 망가진다)
    for (int i = (int)order.size() - 1; i >= 0; i--) {   // 자식이 먼저 확정
        int u = order[i];
        if (parent[u]) ssum[parent[u]] += ssum[u];
    }
    vector<int> res;
    for (int i = 1; i <= n; i++)
        if (ssum[i] >= t) res.push_back(i);
    cout << res.size() << '\n';
    if (!res.empty()) {
        for (size_t i = 0; i < res.size(); i++) {
            if (i) cout << ' ';
            cout << res[i];
        }
        cout << '\n';
    }
    return 0;
}
@@TESTS
--IN
7 20
10 5 20 8 15 -6 9
1 2
1 3
3 4
3 5
5 6
5 7
--OUT
2
1 3
--IN
3 100
1 2 3
1 2
2 3
--OUT
0
--IN
4 0
-5 3 -2 4
1 2
1 3
3 4
--OUT
4
1 2 3 4
--IN
1 5
5
--OUT
1
1
@@EXPL
(1) 접근·핵심 아이디어

- 서브트리 합은 "자식들의 서브트리 합 + 자기 가중치"라는 Tree DP의 가장 기본형이다. 루트에서 BFS로 방문순서를 얻고 역순으로 누적하면 재귀 없이 아래→위로 채워진다.
- 함정: 음수 가중치가 있으면 서브트리 합이 위로 갈수록 커진다는 보장이 없다. 셋째 테스트에서 루트 합은 0인데 자식 합은 3, 4처럼 더 크다. 따라서 "루트가 미달이면 전부 미달" 같은 가지치기는 오답이다. 모든 정점을 개별로 검사한다.

(2) 코드 단계별

- 가중치와 무방향 인접 리스트를 읽는다.
- 루트 1에서 BFS로 `parent`, `order`를 만든다.
- `vector<long long> ssum = w;`로 복사한 뒤 `order` **역순 인덱스 루프**로 `ssum[parent[u]] += ssum[u]`. `order.size()`는 부호 없는 `size_t`이므로 `(int)`로 캐스팅해 내려가는 루프를 쓴다 — `size_t i = order.size() - 1; i >= 0; i--`는 0에서 감싸며 무한 루프가 된다.
- `ssum[i] >= t`인 i를 오름차순으로 모아 개수를 출력하고, 비어 있지 않으면 목록도 출력한다.

(3) 스스로 다시 짤 때 생각 순서

- BFS로 parent/order → 합 배열을 가중치로 초기화 → 역순 누적 → 조건 필터. 시간 O(N), 공간 O(N).
- 검산: 루트의 `ssum[1]`은 모든 가중치의 총합과 같아야 한다. N=1이면 order가 `{1}`뿐이고 누적이 없어 `ssum[1] = w[1]`이다.
```

**5) 트리 센트로이드 찾기** · Medium

- **요구사항**: 트리에서 정점 하나를 제거하면 여러 조각(연결 요소)으로 나뉜다. "제거했을 때 남는 가장 큰 조각의 크기"가 최소가 되는 정점(센트로이드)을 찾아, 그 정점 번호와 그때의 최대 조각 크기를 출력하라. 후보가 여럿이면 번호가 가장 작은 것을 고른다.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 다음 N-1줄 간선 `a b`.
- **출력**: `정점번호 최대조각크기` 한 줄.
- **예제**:
  `7 / 1 2 / 1 3 / 3 4 / 3 5 / 5 6 / 5 7` → `3 3`
  (3을 제거하면 {1,2}, {4}, {5,6,7}로 나뉘어 최대 3. 1을 제거하면 {3,4,5,6,7}=5)
  `4 / 1 2 / 2 3 / 3 4` → `2 2`
  (2와 3 모두 최대 조각 2, 번호가 작은 2)
- **셀프체크**: 정점 u를 제거할 때 조각은 "각 자식의 서브트리"들과 "위쪽 나머지(N - sz[u])" 이렇게 두 종류임을 모두 고려했는가? 서브트리 크기를 자식→부모 순으로 누적했는가? N=1이면 제거 후 남는 게 없어 `1 0`이 나오는가? 크기 배열 이름을 `size`로 두면 `using namespace std;` 아래에서 C++17의 `std::size`와 겹치므로 `sz` 같은 이름을 쓴다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        g[a].push_back(b);
        g[b].push_back(a);
    }
    vector<int> parent(n + 1, 0), order;
    vector<char> seen(n + 1, 0);
    seen[1] = 1;
    queue<int> q;
    q.push(1);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (int v : g[u]) {
            if (!seen[v]) {
                seen[v] = 1;
                parent[v] = u;
                q.push(v);
            }
        }
    }
    vector<int> sz(n + 1, 1);                // size 는 std::size 와 겹친다
    for (int i = (int)order.size() - 1; i >= 0; i--) {
        int u = order[i];
        if (parent[u]) sz[parent[u]] += sz[u];
    }
    int best_u = 1, best_w = n;
    for (int u = 1; u <= n; u++) {
        int worst = n - sz[u];               // 위쪽 나머지 조각
        for (int v : g[u])
            if (parent[v] == u && sz[v] > worst) worst = sz[v];   // 자식 서브트리 조각
        if (worst < best_w) {                // 같으면 작은 번호 유지 (엄격 부등호)
            best_w = worst;
            best_u = u;
        }
    }
    cout << best_u << ' ' << best_w << '\n';
    return 0;
}
@@TESTS
--IN
7
1 2
1 3
3 4
3 5
5 6
5 7
--OUT
3 3
--IN
4
1 2
2 3
3 4
--OUT
2 2
--IN
1
--OUT
1 0
--IN
5
1 2
1 3
1 4
1 5
--OUT
1 1
@@EXPL
(1) 접근·핵심 아이디어

- 정점 u를 지우면 트리는 (a) u의 각 자식 c가 이끄는 서브트리(크기 `sz[c]`)와 (b) u의 위쪽에 남는 나머지(크기 `N - sz[u]`)로 나뉜다. 이 조각들 중 최댓값이 u의 "나쁨"이고, 그 값이 최소인 정점이 센트로이드다.
- 서브트리 크기만 있으면 모든 정점의 값을 O(N)에 한 번에 구할 수 있다. 센트로이드는 항상 존재하며 최대 조각이 N/2 이하가 됨이 알려져 있다(분할 정복의 기초).

(2) 코드 단계별

- 루트 1에서 BFS로 `parent`, `order`를 만들고 역순 누적으로 `sz`를 채운다.
- 각 u에 대해 `worst = n - sz[u]`로 시작하고, 자식(`parent[v] == u`)의 `sz[v]`와 비교해 최댓값을 갱신.
- `worst < best_w`일 때만 갱신하면(엄격 부등호) 같은 값에서 먼저 본 작은 번호가 유지된다. `<=`로 쓰면 마지막 후보가 남아 둘째 예제가 `3 2`로 틀린다.
- `best_u best_w` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "제거 후 조각 = 자식 서브트리들 + 위쪽 나머지" 분해를 먼저 떠올린다 → sz 누적 → 정점마다 max 조각 계산 → 최소 선택(동률은 작은 번호). 시간 O(N).
- 경계: 루트는 위쪽 나머지가 0이고, N=1이면 자식도 없어 worst=0 → `1 0`. 별 모양(넷째 테스트)에서는 중심만 값 1, 나머지는 N-1이다.
```

**6) 부모 배열로 경로 위 정점 수** · Medium

- **요구사항**: 트리가 간선 목록이 아니라 **부모 배열**로 주어진다(루트의 부모는 0). Q개의 질의 `u v`에 대해 u에서 v로 가는 경로 위에 있는 정점의 개수(양 끝 포함)를 출력하라.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 둘째 줄 정점 1..N의 부모(정확히 하나가 0). 셋째 줄 Q (1 ≤ Q ≤ 100). 다음 Q줄 `u v`.
- **출력**: 질의마다 정점 개수를 한 줄에 하나씩.
- **예제**:
  `7 / 3 1 0 3 3 5 5 / 3 / 4 6 / 2 7 / 3 3` → `4 / 5 / 1`
  (루트는 3. 4-3-5-6은 정점 4개, 2-1-3-5-7은 5개, 같은 정점이면 1개)
  `1 / 0 / 1 / 1 1` → `1`
- **셀프체크**: 깊이를 구하려면 부모 배열에서 자식 목록을 만들어 루트부터 BFS해야 한다(부모 배열 순서가 깊이 순이라는 보장은 없다). 정점 수 = 간선 수 + 1 = `depth[u] + depth[v] - 2*depth[lca] + 1`인가? u=v면 1인가? 두 정점을 함께 올릴 때 C++에는 동시 대입이 없지만 `a = par[a]; b = par[b];`처럼 두 줄로 써도 안전하다 — `a`와 `b`는 서로 다른 변수이고 `par`는 이 사이에 바뀌지 않기 때문이다(같은 변수를 서로 참조하는 교환이라면 `swap`이 필요하다).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> par(n + 1, 0);
    vector<vector<int>> children(n + 1);
    int root = 0;
    for (int i = 1; i <= n; i++) {
        int p;
        cin >> p;
        par[i] = p;
        if (p == 0) root = i;
        else children[p].push_back(i);
    }
    vector<int> depth(n + 1, 0);
    queue<int> q;
    q.push(root);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : children[u]) {
            depth[v] = depth[u] + 1;
            q.push(v);
        }
    }
    int Q;
    cin >> Q;
    for (int i = 0; i < Q; i++) {
        int u, v;
        cin >> u >> v;
        int a = u, b = v;
        while (depth[a] > depth[b]) a = par[a];   // 깊은 쪽을 먼저 올려 깊이 맞추기
        while (depth[b] > depth[a]) b = par[b];
        while (a != b) {                          // 같이 한 칸씩 올리기
            a = par[a];
            b = par[b];
        }
        cout << depth[u] + depth[v] - 2 * depth[a] + 1 << '\n';
    }
    return 0;
}
@@TESTS
--IN
7
3 1 0 3 3 5 5
3
4 6
2 7
3 3
--OUT
4
5
1
--IN
1
0
1
1 1
--OUT
1
--IN
5
0 1 2 3 4
2
5 1
5 3
--OUT
5
3
@@EXPL
(1) 접근·핵심 아이디어

- 부모 배열이 곧 "위로 올라가는 포인터"이므로 LCA를 가장 단순한 방식으로 구할 수 있다: 두 정점의 깊이를 맞춘 뒤 같아질 때까지 함께 한 칸씩 올린다. N <= 300, Q <= 100이면 질의당 O(깊이)로 충분하다.
- 경로 위 정점 수는 간선 수 + 1이고, 간선 수는 `depth[u] + depth[v] - 2*depth[lca]`다.

(2) 코드 단계별

- 부모 배열을 읽으며 루트(부모 0)를 찾고 `children` 목록을 만든다.
- 루트부터 BFS로 `depth`를 채운다. 입력 순서가 깊이 순이 아닐 수 있으므로 한 줄씩 `depth[i] = depth[par[i]] + 1`로 채우면 틀릴 수 있다.
- 질의마다 깊은 쪽을 올려 깊이를 맞추고, 다르면 둘 다 부모로 올린다. 만나는 정점이 LCA.
- 거리 공식 + 1을 출력.

(3) 스스로 다시 짤 때 생각 순서

- 입력 형식(부모 배열)에서 자식 리스트·루트 복원 → BFS depth → 단순 상승 LCA → 정점 수 공식. 전처리 O(N), 질의당 O(N) 최악(일자 트리).
- 파이썬의 `a, b = par[a], par[b]` 같은 동시 대입은 C++에 없다. 다만 서로 독립인 두 변수를 각자 갱신하는 경우는 순서를 나눠도 결과가 같다. 정말로 값을 맞바꿔야 할 때만 `swap(a, b)`를 쓴다.
- 경계: u=v면 깊이 맞추기·상승 루프가 모두 0번 돌고 공식이 `0 + 1 = 1`을 준다. 한쪽이 다른 쪽의 조상이면 깊이 맞추기만으로 같아진다.
```

**7) BST k번째 작은 값 질의** · Hard

- **요구사항**: 값을 주어진 순서대로 BST에 삽입한 뒤(중복 없음), Q개의 질의 k에 대해 "k번째로 작은 값"을 출력하라. 질의마다 중위 순회를 처음부터 다시 하지 말고, 각 노드의 **서브트리 크기**를 미리 구해 루트에서 한 번 내려가며 찾아라.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 둘째 줄 삽입할 N개의 서로 다른 정수. 셋째 줄 Q (1 ≤ Q ≤ 100). 넷째 줄 Q개의 k (1 ≤ k ≤ N).
- **출력**: 질의마다 k번째 작은 값을 한 줄에 하나씩.
- **예제**:
  `7 / 5 3 8 1 4 7 9 / 3 / 1 4 7` → `1 / 5 / 9`
  `5 / 10 20 30 40 50 / 2 / 5 1` → `50 / 10`
  (오름차순 삽입이라 오른쪽으로만 치우친 트리)
- **셀프체크**: 노드 u에서 왼쪽 서브트리 크기를 L이라 할 때, `k <= L`이면 왼쪽으로, `k == L+1`이면 u가 답, 아니면 `k -= L+1` 후 오른쪽으로 가는 분기를 정확히 썼는가? 서브트리 크기는 자식이 먼저 확정되는 순서(전위 방문의 역순)로 누적했는가? 치우친 트리에서도 재귀 없이 동작하는가? 인덱스 0을 "빈 노드"로 두고 `sz[0] = 0`으로 놓으면 자식 유무 분기가 사라지는데, 이때 `lch/rch/sz` 배열 크기를 `n + 1`로 잡아 0번 칸이 실제로 존재하게 해야 한다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> vals(n);
    for (int i = 0; i < n; i++) cin >> vals[i];
    int Q;
    cin >> Q;

    vector<int> lch(n + 1, 0), rch(n + 1, 0), value(n + 1, 0);
    int root = 0, cnt = 0;
    for (int i = 0; i < n; i++) {          // 반복형 삽입 (재귀 없음)
        int v = vals[i];
        cnt++;
        value[cnt] = v;
        if (root == 0) {
            root = cnt;
            continue;
        }
        int cur = root;
        while (true) {
            if (v < value[cur]) {
                if (lch[cur] == 0) { lch[cur] = cnt; break; }
                cur = lch[cur];
            } else {
                if (rch[cur] == 0) { rch[cur] = cnt; break; }
                cur = rch[cur];
            }
        }
    }

    // 서브트리 크기: 전위 방문 순서의 역순 = 자식이 먼저 확정
    vector<int> order;
    stack<int> st;
    st.push(root);
    while (!st.empty()) {
        int u = st.top();
        st.pop();
        order.push_back(u);
        if (lch[u]) st.push(lch[u]);
        if (rch[u]) st.push(rch[u]);
    }
    vector<int> sz(n + 1, 0);              // sz[0] = 0 (빈 노드)
    for (int i = (int)order.size() - 1; i >= 0; i--) {
        int u = order[i];
        sz[u] = 1 + sz[lch[u]] + sz[rch[u]];
    }

    for (int i = 0; i < Q; i++) {
        int k;
        cin >> k;
        int cur = root;
        while (true) {
            int ls = sz[lch[cur]];
            if (k <= ls) {
                cur = lch[cur];
            } else if (k == ls + 1) {
                cout << value[cur] << '\n';
                break;
            } else {
                k -= ls + 1;
                cur = rch[cur];
            }
        }
    }
    return 0;
}
@@TESTS
--IN
7
5 3 8 1 4 7 9
3
1 4 7
--OUT
1
5
9
--IN
5
10 20 30 40 50
2
5 1
--OUT
50
10
--IN
1
42
1
1
--OUT
42
--IN
6
40 20 60 10 30 50
3
3 4 6
--OUT
30
40
60
@@EXPL
(1) 접근·핵심 아이디어

- BST에서 노드 u의 왼쪽 서브트리에는 u보다 작은 값만 있다. 왼쪽 크기를 L이라 하면 u는 자기 서브트리 안에서 정확히 L+1번째다. 따라서 k와 L을 비교해 한쪽으로만 내려가면 O(높이)에 k번째를 찾는다(순위 통계 트리의 기본 아이디어).
- 서브트리 크기는 Ch01 L1의 "order 역순 누적"을 이진 트리에 그대로 적용한다. 인덱스 0을 "빈 노드"로 두고 `sz[0] = 0`으로 놓으면 자식 유무 분기가 사라진다.

(2) 코드 단계별

- L2와 같은 배열 기반 반복형 삽입으로 BST를 만든다. 노드 번호는 삽입 순서대로 1..N.
- `stack<int>`으로 전위 방문 순서 `order`를 얻고(`int u = st.top(); st.pop();`), 역순으로 `sz[u] = 1 + sz[lch[u]] + sz[rch[u]]`.
- 질의: `ls = sz[lch[cur]]`. `k <= ls`면 왼쪽으로, `k == ls+1`이면 현재 값이 답, 아니면 `k -= ls+1` 하고 오른쪽으로.
- 결과를 줄마다 출력.

(3) 스스로 다시 짤 때 생각 순서

- BST 삽입(반복형) → 서브트리 크기(전위 역순) → 순위 탐색 분기 3가지. 전처리 O(N), 질의당 O(높이)이며 최악(치우침) O(N).
- `sz[0]`을 유효한 칸으로 만들려면 배열 길이가 `n + 1`이어야 한다. C++ `vector`는 범위를 검사하지 않으므로 `lch[u]`가 0일 때 `sz[0]`이 실제로 존재하는지를 코드로 보장해야 한다.
- 경계: 둘째 예제처럼 오름차순 삽입이면 왼쪽 크기가 항상 0이라 `k -= 1`을 반복하며 오른쪽으로 내려간다. k=1은 항상 최솟값, k=N은 최댓값이 나와야 한다.
```

**8) 경비 초소 최소 비용** · Hard

- **요구사항**: 트리의 각 정점에 초소를 세우는 비용이 있다. 모든 간선은 양 끝점 중 **적어도 하나**에 초소가 있어야 감시된다. 모든 간선을 감시하는 데 드는 최소 총비용을 구하라(트리의 최소 가중 정점 커버).
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 둘째 줄 정점 1..N의 비용(1 ≤ c ≤ 1000). 다음 N-1줄 간선 `a b`.
- **출력**: 최소 총비용.
- **예제**:
  `7 / 10 5 20 8 15 6 9 / 1 2 / 1 3 / 3 4 / 3 5 / 5 6 / 5 7` → `33`
  (예: {1, 4, 5} = 10+8+15. 1이 1-2·1-3을, 4가 3-4를, 5가 3-5·5-6·5-7을 감시)
  `3 / 4 1 4 / 1 2 / 2 3` → `1`
  (가운데 2 하나로 두 간선 모두 감시)
- **셀프체크**: 상태를 "u에 초소를 세움(dp1)/안 세움(dp0)"으로 나눴을 때, u에 안 세우면 **모든 자식에 반드시** 세워야 하고(`dp0[u] += dp1[c]`), u에 세우면 자식은 자유(`dp1[u] += min(dp0[c], dp1[c])`)라는 점화식이 맞는가? L3의 독립 집합(max)과 방향이 어떻게 다른지 설명할 수 있는가? N=1이면 간선이 없어 0인가? `dp0`, `dp1` 배열은 0으로 초기화되어야 누적이 맞는다 — `vector<long long> dp0(n + 1, 0)`처럼 초깃값을 명시한다(C++에서 지역 배열·변수는 자동으로 0이 되지 않는다).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> c(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> c[i];
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        g[a].push_back(b);
        g[b].push_back(a);
    }
    if (n == 1) {                     // 감시할 간선이 없다
        cout << 0 << '\n';
        return 0;
    }
    vector<int> parent(n + 1, 0), order;
    vector<char> seen(n + 1, 0);
    seen[1] = 1;
    queue<int> q;
    q.push(1);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (int v : g[u]) {
            if (!seen[v]) {
                seen[v] = 1;
                parent[v] = u;
                q.push(v);
            }
        }
    }
    vector<long long> dp0(n + 1, 0);   // u에 초소 없음 → 자식 전부 필수
    vector<long long> dp1(n + 1, 0);   // u에 초소 있음 → 자식 자유
    for (int i = (int)order.size() - 1; i >= 0; i--) {
        int u = order[i];
        dp1[u] += c[u];
        int p = parent[u];
        if (p) {
            dp0[p] += dp1[u];
            dp1[p] += min(dp0[u], dp1[u]);
        }
    }
    cout << min(dp0[1], dp1[1]) << '\n';
    return 0;
}
@@TESTS
--IN
7
10 5 20 8 15 6 9
1 2
1 3
3 4
3 5
5 6
5 7
--OUT
33
--IN
3
4 1 4
1 2
2 3
--OUT
1
--IN
1
7
--OUT
0
--IN
2
3 5
1 2
--OUT
3
@@EXPL
(1) 접근·핵심 아이디어

- 간선 (u, c)를 감시하려면 u 또는 c에 초소가 있어야 한다. 그래서 u에 초소가 없으면 모든 자식 c에는 반드시 있어야 하고, u에 있으면 자식은 있어도 없어도 된다. 이를 두 상태 Tree DP로 쓴다: `dp0[u] = sum dp1[c]`, `dp1[u] = c[u] + sum min(dp0[c], dp1[c])`.
- L3의 최대 독립 집합과 골격은 같지만 "고르면 자식은 못 고름(max)"이 "안 고르면 자식은 반드시 골라야 함(min)"으로 뒤집힌 구조다. 독립 집합의 여집합이 정점 커버라는 사실과도 맞물린다.

(2) 코드 단계별

- 비용과 인접 리스트를 읽는다. N=1이면 감시할 간선이 없으므로 0을 출력하고 끝낸다.
- 루트 1에서 BFS로 `parent`, `order`를 만든다.
- `order` 역순으로: `dp1[u] += c[u]`로 자기 비용을 더한 뒤 부모 p에 `dp0[p] += dp1[u]`, `dp1[p] += min(dp0[u], dp1[u])`를 누적한다(u를 처리하는 시점에 u의 두 값은 완성돼 있다).
- 답은 `min(dp0[1], dp1[1])`.

(3) 스스로 다시 짤 때 생각 순서

- 상태 정의(초소 있음/없음) → 간선 조건을 점화식으로 번역 → BFS order 역순 누적 → 루트에서 min. 시간 O(N), 공간 O(N).
- 누적용 배열은 반드시 0으로 초기화한다. `vector`는 기본 생성자로 0을 채우지만, 습관적으로 `(n + 1, 0)`을 적어 두면 나중에 원시 배열(`long long dp[305];`)로 바꿔도 같은 실수를 하지 않는다.
- 경계: 리프는 자식이 없어 `dp0 = 0`, `dp1 = c`로 자연 초기화된다. 정점 2개 트리에서는 싼 쪽 하나만 세우면 되므로 `min(c1, c2)`가 나와야 한다(넷째 테스트).
```

**9) 모든 정점의 최원거리** · Hard

- **요구사항**: 트리의 **모든 정점 v**에 대해, v에서 가장 먼 정점까지의 거리(간선 수)를 구하라. 정점마다 BFS를 돌리는 O(N²) 대신, 지름의 두 끝점만 이용해 BFS 세 번으로 해결하라.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 다음 N-1줄 간선 `a b`.
- **출력**: 정점 1..N의 최원거리를 공백으로 구분해 한 줄에.
- **예제**:
  `7 / 1 2 / 1 3 / 3 4 / 3 5 / 5 6 / 5 7` → `3 4 2 3 3 4 4`
  (3에서 가장 먼 정점은 2·6·7로 거리 2. 지름 끝점 2와 6(또는 7)까지의 거리 중 큰 쪽)
  `4 / 1 2 / 1 3 / 1 4` → `1 2 2 2`
- **셀프체크**: "임의의 정점 v에서 가장 먼 정점은 반드시 지름의 한 끝점"이라는 성질을 설명할 수 있는가(아니라면 v에서의 최원 경로와 지름을 이어 더 긴 경로를 만들 수 있어 모순)? 첫 BFS로 끝점 A, A에서 BFS로 끝점 B와 `da`, B에서 BFS로 `db`를 얻은 뒤 `max(da[v], db[v])`를 썼는가? N=1이면 0인가? 파이썬처럼 `(far, dist)` 두 값을 한 번에 돌려줄 수 없으므로, 거리 배열은 **출력 인자(`vector<int>&`)** 로 받고 끝점만 반환하거나 `pair`로 묶어 돌려준다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int n;
vector<vector<int>> g;

// 가장 먼 정점을 반환하고, 거리 배열은 참조 인자로 채운다
int bfs(int src, vector<int>& dist) {
    dist.assign(n + 1, -1);
    dist[src] = 0;
    queue<int> q;
    q.push(src);
    int far = src;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : g[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                if (dist[v] > dist[far]) far = v;
                q.push(v);
            }
        }
    }
    return far;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    g.assign(n + 1, vector<int>());
    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        g[a].push_back(b);
        g[b].push_back(a);
    }
    vector<int> tmp, da, db;
    int a = bfs(1, tmp);      // 아무 정점에서 가장 먼 정점 A = 지름의 한 끝
    int b = bfs(a, da);       // A에서 가장 먼 정점 B = 반대쪽 끝, da = A로부터 거리
    bfs(b, db);               // db = B로부터 거리
    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << max(da[i], db[i]);
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
7
1 2
1 3
3 4
3 5
5 6
5 7
--OUT
3 4 2 3 3 4 4
--IN
4
1 2
1 3
1 4
--OUT
1 2 2 2
--IN
1
--OUT
0
--IN
2
1 2
--OUT
1 1
@@EXPL
(1) 접근·핵심 아이디어

- 정점마다 BFS를 돌리면 O(N²)다. 대신 지름 성질을 한 단계 확장한다: 트리에서 임의 정점 v의 최원점은 항상 지름의 두 끝점 A, B 중 하나다. 따라서 `ecc[v] = max(dist(A, v), dist(B, v))`이고, A·B로부터의 거리 배열 두 개만 있으면 모든 정점의 답이 O(N)에 나온다.
- 왜 성립하나: v의 최원점 X가 A, B 어느 쪽도 아니라고 하자. v에서 지름 경로로 가는 갈림 지점을 P라 하면, X까지의 경로와 A 또는 B까지의 경로를 P에서 이어 붙여 지름보다 긴 경로가 만들어져 모순이다(L1의 "BFS 두 번" 증명과 같은 논리).

(2) 코드 단계별

- 인접 리스트를 만들고, `int bfs(int src, vector<int>& dist)`가 "가장 먼 정점"을 반환하면서 거리 배열은 참조 인자에 채우도록 작성한다. C++ 함수는 값 하나만 반환하므로, 두 결과 중 하나를 참조로 빼는 것이 관용적이다(`pair<int, vector<int>>`로 묶어도 된다).
- `bfs(1, tmp)`로 끝점 A, `bfs(A, da)`로 끝점 B와 `da`, `bfs(B, db)`로 `db`를 얻는다.
- 정점마다 `max(da[i], db[i])`를 출력한다.

(3) 스스로 다시 짤 때 생각 순서

- 지름 BFS 2회 골격 재사용 → 세 번째 BFS로 반대 끝점 거리 확보 → 정점별 max. 시간 O(N), 공간 O(N).
- `dist.assign(n + 1, -1)`로 매 호출마다 초기화한다. 참조로 받은 배열을 지우지 않으면 앞 호출의 값이 남아 "이미 방문함"으로 오판한다.
- 경계: N=1이면 세 BFS 모두 자기 자신만 방문해 0. 별 모양에서는 중심 1, 나머지 2가 나와야 한다. 지름 끝점 선택이 여러 개(예: 6과 7)여도 어느 쪽을 골라도 답은 같다.
```

**10) 경로 위 최대 간선 가중치 질의** · Hard

- **요구사항**: 각 간선에 양의 가중치가 있는 트리에서 Q개의 질의 `u v`에 대해, u에서 v로 가는 경로 위 간선 가중치의 **최댓값**을 출력하라. u = v이면 0이다. 희소 표(binary lifting)에 "2^k칸 위로 가는 동안의 최대 가중치"를 함께 저장해 질의당 O(log N)에 답하라.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 다음 N-1줄 간선 `a b w` (1 ≤ w ≤ 10^9). 다음 줄 Q (1 ≤ Q ≤ 100). 다음 Q줄 `u v`.
- **출력**: 질의마다 최댓값을 한 줄에 하나씩.
- **예제**:
  `5 / 1 2 2 / 1 3 3 / 3 4 4 / 3 5 1 / 3 / 2 4 / 4 5 / 5 5` → `4 / 4 / 0`
  (2-1-3-4는 2,3,4 중 4; 4-3-5는 4,1 중 4)
  `2 / 1 2 7 / 1 / 2 1` → `7`
- **셀프체크**: `mx[k][v] = max(mx[k-1][v], mx[k-1][up[k-1][v]])`처럼 점프를 반으로 쪼개 최댓값도 합쳤는가? 깊이 맞추기 단계에서 올라가며 지나간 간선의 최댓값을 잊지 않았는가? 마지막에 LCA 바로 아래에서 멈춘 두 정점에서 **한 칸 더**(`mx[0][u]`, `mx[0][v]`)를 반영했는가? 표 크기 `LOG`는 **2^LOG > N**이어야 한다 — `int LOG = 1; while ((1 << LOG) <= n) LOG++;`로 잡고, 모자라면 깊은 트리에서 깊이 차를 다 못 올라가 답이 틀린다. 가중치가 10^9까지라 `int`에 들어가지만(최댓값만 구하고 더하지 않는다), 합을 구하는 변형으로 바꿀 때는 즉시 `long long`이 필요하다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<pair<int, int>>> g(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int a, b, w;
        cin >> a >> b >> w;
        g[a].push_back(make_pair(b, w));
        g[b].push_back(make_pair(a, w));
    }
    int Q;
    cin >> Q;

    vector<int> parent(n + 1, 0), pw(n + 1, 0), depth(n + 1, 0);
    vector<char> seen(n + 1, 0);
    seen[1] = 1;
    queue<int> q;
    q.push(1);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (size_t e = 0; e < g[u].size(); e++) {
            int v = g[u][e].first, w = g[u][e].second;
            if (!seen[v]) {
                seen[v] = 1;
                parent[v] = u;
                pw[v] = w;                  // 부모로 가는 간선의 가중치
                depth[v] = depth[u] + 1;
                q.push(v);
            }
        }
    }

    int LOG = 1;
    while ((1 << LOG) <= n) LOG++;          // 2^LOG > N 이 되게
    vector<vector<int>> up(LOG, vector<int>(n + 1, 0));
    vector<vector<int>> mx(LOG, vector<int>(n + 1, 0));
    up[0] = parent;
    mx[0] = pw;
    for (int k = 1; k < LOG; k++) {
        for (int v = 1; v <= n; v++) {
            int mid = up[k - 1][v];
            up[k][v] = up[k - 1][mid];
            mx[k][v] = max(mx[k - 1][v], mx[k - 1][mid]);
        }
    }

    for (int i = 0; i < Q; i++) {
        int u, v;
        cin >> u >> v;
        int res = 0;
        if (depth[u] < depth[v]) swap(u, v);      // 동시 대입 대신 swap
        int diff = depth[u] - depth[v];
        for (int k = 0; k < LOG; k++) {           // 깊이 맞추기 — 지나간 최대도 반영
            if ((diff >> k) & 1) {
                res = max(res, mx[k][u]);
                u = up[k][u];
            }
        }
        if (u == v) {
            cout << res << '\n';
            continue;
        }
        for (int k = LOG - 1; k >= 0; k--) {      // 큰 점프부터, 조상이 다를 때만
            if (up[k][u] != up[k][v]) {
                res = max(res, max(mx[k][u], mx[k][v]));
                u = up[k][u];
                v = up[k][v];
            }
        }
        cout << max(res, max(mx[0][u], mx[0][v])) << '\n';   // 마지막 한 칸(LCA 직전)
    }
    return 0;
}
@@TESTS
--IN
5
1 2 2
1 3 3
3 4 4
3 5 1
3
2 4
4 5
5 5
--OUT
4
4
0
--IN
2
1 2 7
1
2 1
--OUT
7
--IN
4
1 2 5
2 3 3
3 4 9
2
1 4
1 3
--OUT
9
5
@@EXPL
(1) 접근·핵심 아이디어

- LCA 희소 표의 점화식 `up[k][v] = up[k-1][up[k-1][v]]`는 "2^k칸 = 2^(k-1)칸 두 번"이다. 같은 분해로 "그 구간의 최대 간선"도 `mx[k][v] = max(mx[k-1][v], mx[k-1][up[k-1][v]])`로 합칠 수 있다. 최댓값은 결합법칙을 만족하므로 점프를 쪼개 합쳐도 결과가 같다(합·최소·gcd 등도 같은 방식).
- 질의는 LCA 알고리즘과 동일하게 진행하되, 실제로 점프할 때마다 그 점프 구간의 `mx`를 답에 반영한다. LCA 자체를 반환할 필요는 없고 경로를 두 조각(u→LCA, v→LCA)으로 훑는 셈이다.

(2) 코드 단계별

- BFS로 `parent`, `depth`, 그리고 각 정점이 부모로 올라가는 간선 가중치 `pw`를 채운다.
- `LOG`를 `2^LOG > N`이 되도록 정하고 `vector<vector<int>> up(LOG, vector<int>(n + 1, 0))`, `mx`도 같은 모양으로 잡는다. `up[0] = parent; mx[0] = pw;`(벡터 대입은 값 복사) 후 k를 키우며 표를 채운다(가상 루트 0은 가중치 0이라 넘쳐도 무해).
- 질의: (1) 깊은 쪽이 `u`가 되도록 `swap(u, v)` → 깊이 차의 비트마다 올리며 `mx[k][u]`를 `res`에 반영. (2) 같아졌으면 출력. (3) 큰 k부터 조상이 다를 때만 두 정점을 함께 올리며 `mx`를 반영. (4) 마지막에 LCA 바로 아래에 멈춘 두 정점의 부모 간선 `mx[0]`을 더한다.

(3) 스스로 다시 짤 때 생각 순서

- LCA 골격 복사 → 표에 `mx` 추가 → 질의의 세 단계마다 "점프 = 답 갱신" 한 줄씩 삽입 → 마지막 한 칸 잊지 않기. 전처리 O(N log N), 질의 O(log N).
- `LOG`를 상수(예: 20)로 크게 잡아도 되지만, 작게 잡으면 조용히 틀린다. `(1 << LOG) > n`을 코드로 보장하는 습관이 안전하다.
- `max(a, b, c)`는 C++에 없다. `max(a, max(b, c))`로 중첩하거나 `max({a, b, c})`(초기화 리스트 버전)를 쓴다.
- 경계: u=v는 깊이 차 0·즉시 같음으로 0 출력. 한쪽이 조상이면 깊이 맞추기 단계만으로 끝나므로 그 단계에서도 `mx`를 반영해야 한다(셋째 테스트의 1-4처럼 일자 경로).
```
