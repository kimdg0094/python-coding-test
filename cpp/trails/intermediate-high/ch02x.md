## L4. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch02(MST)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. Union-Find의 집합 크기·그룹 수 추적, Kruskal의 "정렬 + 사이클 판정" 골격, Prim의 힙·배열 두 버전을 소재만 바꿔 여러 번 다시 짜 본다.
- **반복 훈련 개념**:
  - Union-Find 뼈대: 반복형 `find`(경로 압축) + `unite`(크기/랭크 기준). **`union`은 C++ 예약어**라 함수 이름으로 쓸 수 없어 관례상 `unite`로 짓는다. 합치기 성공 여부를 `bool`로 돌려주면 사이클 판정·그룹 수 감소(`comp--`)·크기 갱신(`sz[ra] += sz[rb]`)이 한 줄로 끝난다
  - Kruskal: `sort(edges.begin(), edges.end())` 후 `for (auto &e : edges) if (unite(e.a, e.b)) { total += e.w; cnt++; }`. 채택 간선 수 `cnt == n-1`로 완성/비연결 판정
  - Kruskal 변형: `sort(edges.rbegin(), edges.rend())`처럼 내림차순이면 최대 신장 트리, "u와 v가 처음 같은 집합이 되는 순간의 w"가 최소 병목, 채택을 `n-k`개에서 멈추면 k개 군집
  - 컷 성질(cut property): 어떤 절단이든 그 절단을 건너는 최소 간선은 반드시 어떤 MST에 들어간다 — Kruskal·Prim 정당성과 "이 간선이 MST에 들어갈 수 있는가" 판정의 근거
  - Prim: 힙 버전은 `priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>>`에 누적이 아닌 `{간선 가중치, 정점}`만 넣는다(기본 `priority_queue`는 **최대 힙**이라 `greater<>`를 반드시 붙여야 최소 힙이 된다). 배열 버전은 `key[v] = min(key[v], cost(u, v))`를 O(V²)로 — 좌표 완전 그래프처럼 간선을 미리 나열하기 어려울 때 유리
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '최소 신장 트리'·'유니온 파인드' 단계, 프로그래머스 「코딩테스트 고득점 Kit」의 '그래프', NeetCode 150의 'Advanced Graphs'(Min Cost to Connect Points·병목 경로).
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 집합 크기 질의 | Easy | union by size·`sz[find(a)]` | 반복 훈련 |
| 2 | 친구 그룹 수와 최대 그룹 추적 | Medium | `unite` 성공 시 `comp--`·크기 갱신 | 반복 훈련 |
| 3 | 최소 병목 경로 | Medium | Kruskal 진행 중 두 정점이 처음 연결되는 순간 | 유형 확장 (NeetCode 'Advanced Graphs' 스타일) |
| 4 | k개 군집으로 나누기 | Medium | MST 간선 중 큰 k-1개 제거 | 유형 확장 (백준 '최소 신장 트리' 단계 스타일) |
| 5 | 맨해튼 완전 그래프 MST | Medium | O(V²) 배열 Prim, 간선을 즉석 계산 | 반복 훈련 |
| 6 | 트리로 만들기 위한 최소 제거 비용 | Medium | 내림차순 Kruskal(최대 신장 숲) | 반복 훈련 |
| 7 | 차선 최소 신장 트리 | Hard | MST 간선 하나씩 제외하고 Kruskal 재실행 | 유형 확장 (백준 '최소 신장 트리' 단계 스타일) |
| 8 | 간선의 MST 소속 판정 | Hard | 컷 성질 + 가중치 기준 Union-Find 두 번 | 유형 확장 (solved.ac CLASS 5 MST 응용 스타일) |
| 9 | 간선 철거 후 연결 질의 | Hard | 역순(오프라인) Union-Find·union by rank | 유형 확장 (백준 '유니온 파인드' 단계 스타일) |
| 10 | 길이 제한과 기존 배선이 있는 전력망 | Hard | 힙 Prim + 즉석 인접 리스트 + 0비용 간선 | 반복 훈련 |

**문제**

**1) 집합 크기 질의** · Easy

- **요구사항**: 원소 0..n-1에 대해 연산이 순서대로 주어진다. `1 a b`는 a와 b가 속한 집합을 합치고, `2 a`는 a가 속한 집합의 원소 수를 출력한다. Union-Find(크기 기준 합치기)로 처리하라.
- **입력**: 첫 줄 `n q` (1 ≤ n ≤ 300, 1 ≤ q ≤ 500). 다음 q줄에 `1 a b` 또는 `2 a`. `2` 연산은 1개 이상 있다.
- **출력**: 각 `2` 연산마다 집합 크기를 한 줄에 하나씩.
- **예제**:
  `6 6 / 1 0 1 / 1 2 3 / 2 0 / 1 1 3 / 2 2 / 2 5` → `2 / 4 / 1`
  `3 2 / 2 0 / 2 2` → `1 / 1`
- **셀프체크**: 크기는 **뿌리**에만 유지되므로 `sz[a]`가 아니라 `sz[find(a)]`를 읽었는가? 이미 같은 집합인 쌍을 다시 합칠 때 크기를 두 번 더하지 않았는가(셋째 테스트)? 연산 종류에 따라 읽는 정수 개수가 다른 입력을 `cin >>`로 올바르게 나눠 읽었는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<int> par(n), sz(n, 1);
    iota(par.begin(), par.end(), 0);          // par[i] = i

    function<int(int)> find = [&](int x) {
        int root = x;
        while (par[root] != root) root = par[root];
        while (par[x] != root) {              // 경로 압축
            int nx = par[x];
            par[x] = root;
            x = nx;
        }
        return root;
    };

    string out;
    for (int i = 0; i < q; i++) {
        int t;
        cin >> t;
        if (t == 1) {
            int a, b;
            cin >> a >> b;
            int ra = find(a), rb = find(b);
            if (ra != rb) {                   // 같은 집합이면 크기 변화 없음
                if (sz[ra] < sz[rb]) swap(ra, rb);
                par[rb] = ra;
                sz[ra] += sz[rb];
            }
        } else {
            int a;
            cin >> a;
            out += to_string(sz[find(a)]);
            out += '\n';
        }
    }
    cout << out;
    return 0;
}
@@TESTS
--IN
6 6
1 0 1
1 2 3
2 0
1 1 3
2 2
2 5
--OUT
2
4
1
--IN
3 2
2 0
2 2
--OUT
1
1
--IN
4 4
1 0 1
1 0 1
1 1 0
2 1
--OUT
2
@@EXPL
(1) 접근·핵심 아이디어

- "합쳐라/크기는?" 질의가 섞여 반복되므로 Union-Find가 정석이다. 크기 기준 합치기(union by size)를 쓰면 `sz` 배열이 부산물로 생기고, 그 값은 항상 **뿌리 원소**에서만 정확하다.
- 따라서 크기 질의는 `sz[find(a)]`. 이미 같은 집합인 쌍을 합치면 아무것도 하지 않아야 크기가 중복 가산되지 않는다.

(2) 코드 단계별

- `iota(par.begin(), par.end(), 0)`으로 `par[i] = i`, `sz`는 전부 1로 초기화한다.
- `find`는 반복형 + 경로 압축. `function<int(int)> find = [&](int x){...}`로 잡으면 람다를 이름으로 재사용할 수 있다. 여기서 이름이 `find`여도 인자가 하나뿐이라 3개를 받는 `std::find` 템플릿과 섞이지 않는다.
- 연산 종류 `t`를 먼저 읽고, `1`이면 두 정수를 더 읽어 뿌리가 다를 때만 작은 쪽을 큰 쪽 아래에 붙이며 크기를 합산. `2`면 정수 하나를 읽어 `sz[find(a)]`를 문자열 버퍼에 기록.
- 결과를 한 번에 `cout`으로 내보낸다.

(3) 스스로 다시 짤 때 생각 순서

- Union-Find 뼈대 → 연산별 읽는 정수 개수가 다르므로 `t`를 먼저 읽고 분기 → 크기는 뿌리에서 읽기. 총 O((n + q)·α(n)).
- C++ 함정: 합치기 함수를 `union`으로 지으면 예약어라 컴파일 오류다. `unite`/`merge_set` 같은 이름을 쓴다.
- 경계: 아무 합치기도 없으면 모든 크기가 1(둘째 테스트). 같은 쌍을 여러 번 합쳐도 크기는 2를 유지해야 한다(셋째 테스트).
```

**2) 친구 그룹 수와 최대 그룹 추적** · Medium

- **요구사항**: 학생 n명이 있고, 처음에는 모두 서로 모른다. 친구 관계 `a b`가 하나씩 추가될 때마다 "현재 친구 그룹(연결 요소)의 수"와 "가장 큰 그룹의 인원 수"를 출력하라. 이미 같은 그룹인 두 사람의 관계가 추가되면 아무 변화도 없다.
- **입력**: 첫 줄 `n m` (1 ≤ n ≤ 300, 1 ≤ m ≤ 500). 다음 m줄 관계 `a b` (0-based, a = b일 수 있음).
- **출력**: 관계마다 `그룹수 최대인원`을 한 줄에.
- **예제**:
  `5 4 / 0 1 / 2 3 / 1 2 / 0 3` → `4 2 / 3 2 / 2 4 / 2 4`
  (마지막 0-3은 이미 같은 그룹이라 변화 없음)
  `4 2 / 0 1 / 2 3` → `3 2 / 2 2`
- **셀프체크**: 그룹 수는 n에서 시작해 `unite`가 **실제로** 성공(`true` 반환)할 때만 1 줄였는가? 최대 인원은 합쳐진 뒤의 뿌리 크기와 비교해 갱신하면 되고, 절대 줄어들지 않는다는 점을 이용했는가? `a == b`인 자기 관계에서 그룹 수가 줄지 않는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<int> par(n), sz(n, 1);
    iota(par.begin(), par.end(), 0);

    function<int(int)> find = [&](int x) {
        int root = x;
        while (par[root] != root) root = par[root];
        while (par[x] != root) {
            int nx = par[x];
            par[x] = root;
            x = nx;
        }
        return root;
    };

    int comp = n;                 // 현재 연결 요소 수
    int largest = 1;              // 가장 큰 그룹 인원(단조 증가)
    string out;
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        int ra = find(a), rb = find(b);
        if (ra != rb) {
            if (sz[ra] < sz[rb]) swap(ra, rb);
            par[rb] = ra;
            sz[ra] += sz[rb];
            comp--;
            if (sz[ra] > largest) largest = sz[ra];
        }
        out += to_string(comp);
        out += ' ';
        out += to_string(largest);
        out += '\n';
    }
    cout << out;
    return 0;
}
@@TESTS
--IN
5 4
0 1
2 3
1 2
0 3
--OUT
4 2
3 2
2 4
2 4
--IN
4 2
0 1
2 3
--OUT
3 2
2 2
--IN
1 1
0 0
--OUT
1 1
--IN
3 3
0 1
1 2
2 0
--OUT
2 2
1 3
1 3
@@EXPL
(1) 접근·핵심 아이디어

- 관계가 추가될 때마다 연결 요소 수를 다시 세면 O(m·(n+m))이지만, Union-Find로 "실제로 두 그룹이 합쳐질 때만 `comp--`"로 추적하면 관계당 거의 상수 시간이다.
- 최대 그룹 크기는 단조 증가한다(합치기만 있고 분리가 없으므로). 그래서 합쳐진 직후의 뿌리 크기 `sz[ra]`와만 비교하면 된다.

(2) 코드 단계별

- `comp = n`, `largest = 1`로 시작한다(모두 혼자인 상태).
- 관계 `(a, b)`의 두 뿌리가 다르면 크기 기준으로 합치고 `comp--`, `largest = max(largest, sz[ra])`.
- 뿌리가 같으면(이미 친구 그룹이거나 `a == b`) 아무 변화 없이 현재 값을 그대로 출력.
- 관계마다 `"comp largest"` 형태로 버퍼에 붙여 마지막에 한 번 출력한다. 줄마다 `cout << ... << endl`을 쓰면 매번 버퍼를 비워 느려지므로 `'\n'`이나 문자열 누적을 쓴다.

(3) 스스로 다시 짤 때 생각 순서

- "그룹 수 = n - 성공한 합치기 수"라는 관계를 먼저 잡는다 → 크기 갱신을 합치기 성공 지점에 넣는다 → 최대는 단조라 갱신만 한다. 총 O(m·α(n)).
- C++ 함정: `swap(ra, rb)`는 지역 변수만 바꾸므로 반드시 그 뒤에 `par[rb] = ra`로 실제 부모를 갱신해야 한다. 두 줄 순서를 바꾸면 조용히 틀린다.
- 경계: n=1에 `0 0` 하나면 `1 1`. 삼각형(넷째 테스트)에서 세 번째 관계는 사이클이라 그룹 수·최대 모두 그대로다.
```

**3) 최소 병목 경로** · Medium

- **요구사항**: 무방향 가중 그래프에서 정점 s에서 t로 가는 경로들 중 "경로 위 가장 큰 간선 가중치"가 최소가 되는 값을 구하라(트럭이 지나야 하는 다리 중 가장 낮은 하중 제한을 최대한 높이는 문제와 같은 구조). 도달할 수 없으면 -1, s = t이면 0을 출력한다.
- **입력**: 첫 줄 `n m` (1 ≤ n ≤ 300, 0 ≤ m ≤ 500). 다음 m줄 간선 `a b w` (0-based, 1 ≤ w ≤ 10^6, 다중 간선 가능). 마지막 줄 `s t`.
- **출력**: 최소 병목 값(또는 -1).
- **예제**:
  `5 6 / 0 1 4 / 1 2 8 / 0 2 10 / 2 3 3 / 3 4 6 / 1 4 9 / 0 4` → `8`
  (0-1-2-3-4는 최대 8, 0-1-4는 9, 0-2-3-4는 10)
  `3 1 / 0 1 5 / 0 2` → `-1`
- **셀프체크**: 간선을 오름차순으로 넣다가 s와 t가 **처음** 같은 집합이 되는 순간의 가중치가 답인 이유(그 전까지는 더 작은 간선만으로 못 이었고, 그 순간 이은 경로는 최대가 현재 w)를 설명할 수 있는가? 사이클 간선(이미 같은 집합)도 그냥 건너뛰면 되는가? s = t를 정렬 전에 먼저 처리했는가? 간선을 `array<int,3>{w, a, b}`처럼 **가중치를 앞에** 두면 기본 `sort`가 곧바로 원하는 순서를 만든다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<array<int, 3>> edges(m);          // {w, a, b} — w가 앞이라 기본 정렬이 곧 가중치 순
    for (int i = 0; i < m; i++) {
        int a, b, w;
        cin >> a >> b >> w;
        edges[i] = {w, a, b};
    }
    int s, t;
    cin >> s >> t;
    if (s == t) {
        cout << 0 << '\n';
        return 0;
    }
    sort(edges.begin(), edges.end());

    vector<int> par(n), sz(n, 1);
    iota(par.begin(), par.end(), 0);

    function<int(int)> find = [&](int x) {
        int root = x;
        while (par[root] != root) root = par[root];
        while (par[x] != root) {
            int nx = par[x];
            par[x] = root;
            x = nx;
        }
        return root;
    };

    for (auto &e : edges) {
        int w = e[0], a = e[1], b = e[2];
        int ra = find(a), rb = find(b);
        if (ra != rb) {
            if (sz[ra] < sz[rb]) swap(ra, rb);
            par[rb] = ra;
            sz[ra] += sz[rb];
            if (find(s) == find(t)) {        // 처음 연결되는 순간의 w가 답
                cout << w << '\n';
                return 0;
            }
        }
    }
    cout << -1 << '\n';
    return 0;
}
@@TESTS
--IN
5 6
0 1 4
1 2 8
0 2 10
2 3 3
3 4 6
1 4 9
0 4
--OUT
8
--IN
3 1
0 1 5
0 2
--OUT
-1
--IN
2 2
0 1 7
0 1 2
0 1
--OUT
2
--IN
3 2
0 1 1
1 2 1
1 1
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- "경로의 최댓값을 최소화"는 Kruskal이 자연스럽다. 간선을 가중치 오름차순으로 하나씩 켜 나가면, 가중치 w 이하의 간선만으로 s와 t가 이어지는 최초의 w가 답이다. 그 전에는 더 작은 간선들만으로는 연결이 불가능했고, 그 순간에는 최대 가중치가 w인 경로가 존재하기 때문이다.
- 이 값은 MST 위의 s-t 경로의 최대 간선과도 같다(MST의 병목 성질). 그래서 "최소 병목 경로 = MST 위 경로"라는 결과를 기억해 두면 다른 문제에서도 쓰인다.

(2) 코드 단계별

- 간선을 `array<int,3>{w, a, b}`로 담고 `sort`. `array`와 `tuple`은 사전순 비교가 기본이라 첫 원소인 w가 정렬 키가 된다. 입력은 `a b w` 순인데 저장은 `{w, a, b}` 순임에 주의.
- s = t는 정렬 전에 0으로 처리하고 즉시 종료.
- Union-Find를 초기화하고 정렬 순서대로 합친다. 실제로 합쳐진 뒤 `find(s) == find(t)`가 되면 그 w를 출력하고 종료.
- 끝까지 이어지지 않으면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "최대의 최소" 구조를 보면 정렬 + Union-Find → 연결 시점 체크. O(m log m + m·α(n)).
- C++ 함정: 비교자를 직접 쓸 때는 strict weak ordering을 지켜야 한다. `return a[0] <= b[0];`처럼 `<=`를 넣으면 같은 값에서 "a가 b보다 앞이고 b도 a보다 앞"이 되어 `sort`가 범위를 벗어나 크래시할 수 있다. 여기처럼 기본 `<`를 쓰면 그런 실수가 아예 없다.
- 경계: 다중 간선은 작은 것이 먼저 오므로 자연히 유리한 쪽이 선택된다(셋째 테스트). 사이클 간선은 합치기가 실패하므로 연결 상태가 바뀌지 않아 체크를 건너뛰어도 된다.
```

**4) k개 군집으로 나누기** · Medium

- **요구사항**: 연결 무방향 가중 그래프의 정점들을 정확히 k개의 군집으로 나누되, "군집 내부를 잇는 데 쓴 간선 비용의 합"을 최소로 하고 싶다. MST를 구한 뒤 가중치가 큰 간선 k-1개를 끊으면 되는 것으로 알려져 있다. 남은 간선 비용의 합을 출력하라. 그래프가 연결되어 있지 않으면 -1을 출력한다.
- **입력**: 첫 줄 `n m k` (1 ≤ n ≤ 300, 0 ≤ m ≤ 500, 1 ≤ k ≤ n). 다음 m줄 간선 `a b w` (0-based, 1 ≤ w ≤ 10^6).
- **출력**: 남은 간선 비용의 합(또는 -1).
- **예제**:
  `6 7 2 / 0 1 1 / 1 2 5 / 2 3 2 / 3 4 7 / 4 5 1 / 0 5 9 / 1 4 6` → `9`
  (MST 간선 1,1,2,5,6 중 가장 큰 6을 끊으면 1+1+2+5=9)
  `6 7 1 / 0 1 1 / 1 2 5 / 2 3 2 / 3 4 7 / 4 5 1 / 0 5 9 / 1 4 6` → `15`
- **셀프체크**: MST 간선을 오름차순으로 모았을 때 앞에서 `n-k`개만 더하면 "큰 k-1개 제거"와 같은가? k = n이면 아무 간선도 남지 않아 0인가? MST가 여러 개여도 간선 가중치의 **정렬된 목록**은 항상 같으므로 답이 유일함을 이해했는가? 비연결이면 채택 간선이 n-1개 미만이다. 합은 `long long`으로 받았는가(간선 300개 × 10^6이면 `int` 한계에 가깝다)?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, k;
    cin >> n >> m >> k;
    vector<array<int, 3>> edges(m);
    for (int i = 0; i < m; i++) {
        int a, b, w;
        cin >> a >> b >> w;
        edges[i] = {w, a, b};
    }
    sort(edges.begin(), edges.end());

    vector<int> par(n), sz(n, 1);
    iota(par.begin(), par.end(), 0);

    function<int(int)> find = [&](int x) {
        int root = x;
        while (par[root] != root) root = par[root];
        while (par[x] != root) {
            int nx = par[x];
            par[x] = root;
            x = nx;
        }
        return root;
    };

    vector<int> chosen;                       // MST 간선 가중치(오름차순으로 쌓임)
    for (auto &e : edges) {
        int w = e[0], a = e[1], b = e[2];
        int ra = find(a), rb = find(b);
        if (ra == rb) continue;
        if (sz[ra] < sz[rb]) swap(ra, rb);
        par[rb] = ra;
        sz[ra] += sz[rb];
        chosen.push_back(w);
        if ((int)chosen.size() == n - 1) break;
    }

    if ((int)chosen.size() < n - 1) {
        cout << -1 << '\n';
        return 0;
    }
    long long total = 0;                      // 작은 n-k개만 남김 = 큰 k-1개 제거
    for (int i = 0; i < n - k; i++) total += chosen[i];
    cout << total << '\n';
    return 0;
}
@@TESTS
--IN
6 7 2
0 1 1
1 2 5
2 3 2
3 4 7
4 5 1
0 5 9
1 4 6
--OUT
9
--IN
6 7 1
0 1 1
1 2 5
2 3 2
3 4 7
4 5 1
0 5 9
1 4 6
--OUT
15
--IN
3 3 3
0 1 1
1 2 2
0 2 3
--OUT
0
--IN
4 2 2
0 1 1
2 3 1
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- MST는 "전체를 가장 싸게 잇는 트리"다. 트리에서 간선 하나를 끊으면 조각이 하나 늘어나므로, k개 조각을 만들려면 k-1개를 끊어야 하고, 남는 비용을 최소로 하려면 가장 비싼 k-1개를 끊는 것이 최적이다(MST 간선 집합에서 부분 집합을 고르는 셈이고, 어떤 다른 신장 숲도 이보다 싸지 않다는 것이 Kruskal의 탐욕 근거로 보장된다).
- 구현은 Kruskal에서 채택 간선을 오름차순으로 모아 두고 앞의 `n-k`개만 더하면 된다 — Kruskal은 오름차순으로 채택하므로 따로 정렬할 필요가 없다.

(2) 코드 단계별

- 간선을 정렬하고 Union-Find로 Kruskal을 돌리며 채택 가중치를 `chosen`에 쌓는다.
- 채택 개수가 n-1 미만이면 비연결 → -1.
- `chosen`의 앞 `n-k`개를 `long long total`에 더해 출력. k = 1이면 전체 MST, k = n이면 루프가 0번 돌아 0.

(3) 스스로 다시 짤 때 생각 순서

- Kruskal 골격 → 채택 가중치 배열화 → 조각 수와 끊는 간선 수의 관계(k개 조각 = k-1개 절단) → 앞에서 n-k개 합. O(m log m).
- C++ 함정: `chosen.size()`는 부호 없는 `size_t`라 `chosen.size() < n - 1`에서 `n - 1`이 음수가 되면(n = 0 같은 상황) 거대한 양수로 변환돼 비교가 뒤집힌다. `(int)chosen.size()`로 캐스팅하거나 `chosen.size() + 1 < (size_t)n`처럼 뺄셈을 피한다.
- 경계: MST가 유일하지 않아도 채택 가중치의 정렬 목록은 같으므로 답은 유일하다. 비연결 그래프는 이미 조각이 나뉘어 있어 문제 정의가 애매하므로 -1로 규정했다.
```

**5) 맨해튼 완전 그래프 MST** · Medium

- **요구사항**: 평면 위 n개의 점이 있고, 두 점을 잇는 비용은 맨해튼 거리 `|x1-x2| + |y1-y2|`다. 모든 점을 연결하는 최소 총비용을 구하라. 모든 쌍이 간선이므로 간선 목록을 만들지 말고, O(V²) 배열 기반 Prim으로 거리를 즉석에서 계산하라.
- **입력**: 첫 줄 n (1 ≤ n ≤ 300). 다음 n줄 `x y` (-10^4 ≤ x, y ≤ 10^4, 같은 좌표가 반복될 수 있음).
- **출력**: 최소 총비용.
- **예제**:
  `4 / 0 0 / 0 3 / 4 0 / 4 3` → `10`
  (3 + 3 + 4)
  `3 / 1 1 / 3 5 / 6 2` → `12`
- **셀프체크**: 간선 수가 n(n-1)/2라 Kruskal은 정렬 비용 O(n² log n)이 들지만, 배열 Prim은 O(n²)로 끝난다는 비교를 할 수 있는가? `key[v]`를 "현재 트리에서 v까지의 최소 거리"로 유지하고 정점이 편입될 때마다 나머지 정점의 key를 갱신했는가? INF는 `INT_MAX`로 두되 **`INT_MAX`에 무언가를 더하지 않도록** 편입 전에만 비교하는가? 같은 좌표의 점은 비용 0으로 이어지는가? n = 1이면 0인가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> xs(n), ys(n);
    for (int i = 0; i < n; i++) cin >> xs[i] >> ys[i];

    const int INF = INT_MAX;
    vector<int> key(n, INF);          // 트리까지의 최소 연결 비용
    vector<char> used(n, 0);
    key[0] = 0;
    long long total = 0;
    for (int step = 0; step < n; step++) {
        int u = -1, best = INF;
        for (int v = 0; v < n; v++)   // 아직 안 넣은 정점 중 key 최소
            if (!used[v] && key[v] < best) { best = key[v]; u = v; }
        used[u] = 1;
        total += key[u];
        int ux = xs[u], uy = ys[u];
        for (int v = 0; v < n; v++) { // 새 정점 기준으로 나머지 key 갱신(거리 즉석 계산)
            if (used[v]) continue;
            int d = abs(ux - xs[v]) + abs(uy - ys[v]);
            if (d < key[v]) key[v] = d;
        }
    }
    cout << total << '\n';
    return 0;
}
@@TESTS
--IN
4
0 0
0 3
4 0
4 3
--OUT
10
--IN
3
1 1
3 5
6 2
--OUT
12
--IN
1
5 5
--OUT
0
--IN
3
2 2
2 2
9 9
--OUT
14
@@EXPL
(1) 접근·핵심 아이디어

- 좌표 완전 그래프는 간선이 O(n²)개다. Kruskal은 그 간선을 전부 만들어 정렬해야 하므로 O(n² log n)인 반면, 배열 Prim은 "매 단계 key 최소 정점 선택 + 이웃 key 갱신"을 n번 반복해 O(n²)로 끝나고 간선을 저장할 필요도 없다. 밀집 그래프에서 배열 Prim이 유리한 전형적인 사례다.
- 정당성은 컷 성질: 현재 트리와 바깥을 가르는 절단에서 가장 싼 간선(= key 최소 정점의 연결 간선)은 항상 어떤 MST에 포함된다.

(2) 코드 단계별

- 좌표를 `xs`, `ys`에 담는다.
- `key[0] = 0`으로 시작. n번 반복: 미편입 정점 중 key 최소 `u`를 선형 탐색으로 고르고 편입(`total += key[u]`).
- `u`와 나머지 미편입 정점 v 사이 맨해튼 거리를 계산해 `key[v]`를 더 작으면 갱신.
- `total` 출력. 완전 그래프라 항상 연결되므로 `key[u]`가 INF인 채 더해지는 일은 없다.

(3) 스스로 다시 짤 때 생각 순서

- "간선을 미리 못 만들겠다/너무 많다" → 배열 Prim → 거리 함수를 갱신 루프 안에서 직접 호출.
- C++ 함정: `key`를 `memset(key, 0x3f, ...)`처럼 초기화하는 습관이 있는데, `memset`은 **바이트 단위**라 `int` 배열을 0과 -1 외의 값으로 채우려면 반드시 그 바이트 패턴이 의미가 있어야 한다(0x3f3f3f3f는 우연히 쓸 만한 INF일 뿐이다). `vector<int> key(n, INF)`처럼 값을 직접 주는 편이 안전하다. 방문 표시는 `vector<bool>`의 비트 압축을 피해 `vector<char>`를 썼다.
- 경계: n = 1이면 첫 반복에서 0번만 편입하고 끝(0). 같은 좌표 점은 거리 0으로 이어진다(넷째 테스트: 0 + 14).
```

**6) 트리로 만들기 위한 최소 제거 비용** · Medium

- **요구사항**: 무방향 가중 그래프에서 간선을 몇 개 제거해 **사이클이 하나도 없게** 만들되, 원래 연결되어 있던 정점 쌍은 여전히 연결되어 있어야 한다(각 연결 요소를 트리로 만든다). 제거한 간선 가중치 합의 최솟값을 구하라.
- **입력**: 첫 줄 `n m` (1 ≤ n ≤ 300, 0 ≤ m ≤ 500). 다음 m줄 간선 `a b w` (0-based, 1 ≤ w ≤ 10^6, 다중 간선 가능).
- **출력**: 제거 비용의 최솟값.
- **예제**:
  `4 5 / 0 1 3 / 1 2 4 / 2 0 5 / 2 3 2 / 3 0 6` → `5`
  (6, 5, 4를 남기고 3과 2를 제거)
  `3 2 / 0 1 1 / 1 2 1` → `0`
- **셀프체크**: "제거 비용 최소 = 남기는 비용 최대 = 최대 신장 숲"으로 뒤집었는가? 내림차순 정렬한 Kruskal에서 채택되지 않은(사이클을 만드는) 간선의 합이 곧 답인가? 내림차순은 `sort(v.rbegin(), v.rend())` 한 줄로 되는가? 그래프가 비연결이어도 각 컴포넌트마다 독립적으로 동작하므로 -1 처리가 필요 없는가? 같은 쌍의 다중 간선 중 큰 것 하나만 남는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<array<int, 3>> edges(m);
    for (int i = 0; i < m; i++) {
        int a, b, w;
        cin >> a >> b >> w;
        edges[i] = {w, a, b};
    }
    // 최대 신장 숲: 비싼 간선부터 채택 → 역방향 반복자로 정렬하면 내림차순
    sort(edges.rbegin(), edges.rend());

    vector<int> par(n), sz(n, 1);
    iota(par.begin(), par.end(), 0);

    function<int(int)> find = [&](int x) {
        int root = x;
        while (par[root] != root) root = par[root];
        while (par[x] != root) {
            int nx = par[x];
            par[x] = root;
            x = nx;
        }
        return root;
    };

    long long removed = 0;
    for (auto &e : edges) {
        int w = e[0], a = e[1], b = e[2];
        int ra = find(a), rb = find(b);
        if (ra == rb) {
            removed += w;                 // 사이클을 만드는 간선 = 제거 대상
            continue;
        }
        if (sz[ra] < sz[rb]) swap(ra, rb);
        par[rb] = ra;
        sz[ra] += sz[rb];
    }
    cout << removed << '\n';
    return 0;
}
@@TESTS
--IN
4 5
0 1 3
1 2 4
2 0 5
2 3 2
3 0 6
--OUT
5
--IN
3 2
0 1 1
1 2 1
--OUT
0
--IN
5 4
0 1 2
1 2 3
2 0 4
3 4 1
--OUT
2
--IN
2 3
0 1 5
0 1 1
0 1 3
--OUT
4
@@EXPL
(1) 접근·핵심 아이디어

- 각 연결 요소를 트리로 만들 때 남는 간선 수는 정해져 있다(정점 수 - 1). 제거 비용을 최소화하려면 **남기는** 간선 비용을 최대화하면 되고, 그것이 최대 신장 숲(maximum spanning forest)이다. Kruskal에서 정렬 방향만 내림차순으로 바꾸면 된다.
- Kruskal이 건너뛰는 간선(이미 같은 집합)은 정확히 "사이클을 만드는 간선"이며, 내림차순이므로 그 사이클에서 가장 싼 쪽이 버려진다. 따라서 건너뛴 가중치의 합이 답이다. 비연결 그래프도 컴포넌트별로 독립이라 그대로 동작한다.

(2) 코드 단계별

- 간선을 `{w, a, b}`로 담고 `sort(edges.rbegin(), edges.rend())`로 내림차순 정렬한다. `sort(edges.begin(), edges.end(), greater<>())`도 같은 결과다.
- Union-Find로 순서대로 처리: 뿌리가 같으면 `removed += w`, 다르면 합친다.
- `removed` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "제거 최소 ↔ 유지 최대" 변환 → 최대 신장 숲 = 내림차순 Kruskal → 건너뛴 간선 합. O(m log m).
- C++ 함정: 누적 합은 `long long`으로 받는다. 간선 500개에 가중치 10^6이면 5·10^8이라 아직 `int` 안이지만, 제한이 조금만 커져도 21억을 넘겨 조용히 음수가 된다. "합·곱은 일단 `long long`"이 안전한 습관이다.
- 경계: 이미 숲이면 0(둘째 테스트). 다중 간선은 가장 비싼 것만 남고 나머지는 전부 제거된다(넷째 테스트: 1 + 3). 검산: `총합 - 채택합 = removed`.
```

**7) 차선 최소 신장 트리** · Hard

- **요구사항**: 연결 무방향 가중 그래프에서 MST 비용을 C라 하자. 간선 집합이 MST와 **다른** 신장 트리 중 비용이 가장 작은 것(차선 MST)의 비용을 구하라. 비용이 C와 같아도 간선 집합이 다르면 인정한다. 그런 트리가 없거나(신장 트리가 하나뿐) 그래프가 비연결이면 -1을 출력한다.
- **입력**: 첫 줄 `n m` (2 ≤ n ≤ 50, 1 ≤ m ≤ 200). 다음 m줄 간선 `a b w` (0-based, 1 ≤ w ≤ 10^6, 다중 간선 가능).
- **출력**: 차선 MST 비용(또는 -1).
- **예제**:
  `4 5 / 0 1 1 / 1 2 2 / 2 3 3 / 0 3 4 / 0 2 5` → `7`
  (MST {1,2,3}=6. 간선 3을 빼면 {1,2,4}=7이 최소)
  `3 2 / 0 1 1 / 1 2 1` → `-1`
- **셀프체크**: 차선 트리는 MST에서 간선 **정확히 하나**를 빼고 하나를 넣은 형태로 항상 얻을 수 있다는 사실(교환 논증)을 근거로, "MST의 각 간선을 하나씩 제외하고 Kruskal을 다시 돌린 결과의 최솟값"을 취했는가? 제외 후 신장 트리가 안 만들어지면 그 후보는 버렸는가? 간선에 **원래 입력 번호**를 붙여 정렬해야 "몇 번 간선을 제외"가 성립하는가? 가중치가 같은 간선이 여럿이면 답이 C와 같을 수 있는가(셋째 테스트)?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<array<int, 4>> edges(m);           // {w, a, b, 원래 번호}
    for (int i = 0; i < m; i++) {
        int a, b, w;
        cin >> a >> b >> w;
        edges[i] = {w, a, b, i};
    }
    sort(edges.begin(), edges.end());

    // skip 번호 간선을 제외하고 MST. 성공하면 true, cost/used를 채운다.
    auto kruskal = [&](int skip, long long &cost, vector<int> &used) -> bool {
        vector<int> par(n), sz(n, 1);
        iota(par.begin(), par.end(), 0);
        function<int(int)> find = [&](int x) {
            int root = x;
            while (par[root] != root) root = par[root];
            while (par[x] != root) {
                int nx = par[x];
                par[x] = root;
                x = nx;
            }
            return root;
        };
        cost = 0;
        used.clear();
        for (auto &e : edges) {
            int w = e[0], a = e[1], b = e[2], id = e[3];
            if (id == skip) continue;
            int ra = find(a), rb = find(b);
            if (ra == rb) continue;
            if (sz[ra] < sz[rb]) swap(ra, rb);
            par[rb] = ra;
            sz[ra] += sz[rb];
            cost += w;
            used.push_back(id);
            if ((int)used.size() == n - 1) break;
        }
        return (int)used.size() == n - 1;
    };

    long long base = 0;
    vector<int> baseUsed;
    if (!kruskal(-1, base, baseUsed)) {
        cout << -1 << '\n';
        return 0;
    }
    long long best = -1;
    for (int e : baseUsed) {                  // MST 간선을 하나씩 제외
        long long cost;
        vector<int> used;
        if (kruskal(e, cost, used) && (best == -1 || cost < best)) best = cost;
    }
    cout << best << '\n';
    return 0;
}
@@TESTS
--IN
4 5
0 1 1
1 2 2
2 3 3
0 3 4
0 2 5
--OUT
7
--IN
3 2
0 1 1
1 2 1
--OUT
-1
--IN
3 3
0 1 1
1 2 1
0 2 1
--OUT
2
--IN
4 2
0 1 1
2 3 1
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- 교환 논증: 어떤 신장 트리 T'가 MST T와 다르면 T에는 있고 T'에는 없는 간선 e가 존재한다. 그러면 T'는 "e를 제외한 그래프"의 신장 트리이므로, 비용은 `MST(G - e)` 이상이다. 따라서 차선 비용은 T의 간선 e를 하나씩 제외하며 구한 `MST(G - e)`들의 최솟값과 같다(그 최솟값을 주는 트리는 e를 안 쓰므로 T와 다르다).
- n ≤ 50, m ≤ 200이므로 Kruskal을 최대 n번(=MST 간선 수) 다시 돌려도 O(n·m·α)로 충분하다. 간선 정렬은 한 번만 하고 `skip`만 바꿔 재사용한다.

(2) 코드 단계별

- 간선에 원래 번호를 붙여 `array<int,4>{w, a, b, id}`로 정렬한다. 정렬하면 순서가 뒤섞이므로 번호를 따로 들고 있지 않으면 "몇 번 간선을 제외"를 말할 수 없다.
- `kruskal(skip, cost, used)`: 번호 `skip`을 건너뛰며 Kruskal. 결과는 참조 매개변수 `cost`·`used`로 돌려주고, 성공 여부만 `bool`로 반환한다(파이썬처럼 `None`이나 튜플을 돌려주는 대신 쓰는 C++ 관용구다).
- `kruskal(-1, ...)`로 기준 MST를 얻는다(없으면 -1).
- MST의 각 채택 간선을 제외하고 다시 돌려 유효한 결과 중 최솟값을 취한다. 하나도 없으면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "MST와 다른 트리"를 "MST의 어떤 간선을 안 쓰는 트리"로 바꿔 생각 → 그 간선 제외 후 MST → 최소. 제외 시 비연결이면 후보에서 제거.
- C++ 함정: 큰 벡터를 값으로 주고받으면 매번 복사가 일어난다. 여기처럼 `vector<int> &used`로 참조를 넘기거나, 루프 바깥에서 만든 벡터를 `clear()` 후 재사용하면 복사가 사라진다. 반대로 **읽기만 하는 큰 컨테이너는 `const &`**로 받는다.
- 경계: 그래프 자체가 트리면 어떤 간선을 빼도 끊기므로 -1(둘째 테스트). 동일 가중치 삼각형은 어느 간선을 빼도 비용 2가 나와 C와 같다(셋째 테스트). 다중 간선도 번호로 구분되므로 같은 쌍의 다른 간선으로 대체할 수 있다.
```

**8) 간선의 MST 소속 판정** · Hard

- **요구사항**: 연결 무방향 가중 그래프(자기 루프·다중 간선 없음)의 각 간선에 대해, 그 간선이 **모든** MST에 들어가면 `ALL`, 일부 MST에만 들어가면 `SOME`, 어떤 MST에도 들어가지 않으면 `NONE`을 출력하라. 가중치가 같은 간선이 여럿일 수 있다.
- **입력**: 첫 줄 `n m` (2 ≤ n ≤ 50, 1 ≤ m ≤ 200). 다음 m줄 간선 `a b w` (0-based, 1 ≤ w ≤ 10^6).
- **출력**: 입력 순서대로 간선마다 `ALL`/`SOME`/`NONE`을 한 줄에 하나씩.
- **예제**:
  `4 5 / 0 1 1 / 1 2 2 / 2 3 2 / 0 3 2 / 0 2 3` → `ALL / SOME / SOME / SOME / NONE`
  (가중치 2인 세 간선은 0-1과 함께 사이클을 이루므로 그중 둘만 쓰인다. 0-2(3)는 더 싼 경로로 이미 연결되어 있어 불필요)
  `3 3 / 0 1 1 / 1 2 2 / 0 2 3` → `ALL / ALL / NONE`
- **셀프체크**: 간선 e=(u,v,w)가 어떤 MST에 들어갈 수 있는 조건은 "가중치 **w 미만**인 간선만으로 u와 v가 이어지지 않는다"(컷 성질)이고, 모든 MST에 들어갈 조건은 "e를 제외한 가중치 **w 이하**인 간선만으로도 u와 v가 이어지지 않는다"(같은 무게의 대체 경로가 없음)라는 두 판정을 순서대로 적용했는가? 각 판정마다 Union-Find를 새로 만들었는가(이전 판정의 `par`를 그대로 쓰면 조용히 틀린다)?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<array<int, 3>> edges(m);           // {a, b, w}
    for (int i = 0; i < m; i++) {
        int a, b, w;
        cin >> a >> b >> w;
        edges[i] = {a, b, w};
    }

    // 가중치가 limit 미만(strict) 또는 이하(!strict)인 간선만 합친 뒤 u, v 연결 여부
    auto connected = [&](int u, int v, int limit, bool strict, int skip) -> bool {
        vector<int> par(n), sz(n, 1);
        iota(par.begin(), par.end(), 0);
        function<int(int)> find = [&](int x) {
            int root = x;
            while (par[root] != root) root = par[root];
            while (par[x] != root) {
                int nx = par[x];
                par[x] = root;
                x = nx;
            }
            return root;
        };
        for (int j = 0; j < m; j++) {
            if (j == skip) continue;
            int a = edges[j][0], b = edges[j][1], w = edges[j][2];
            bool take = strict ? (w < limit) : (w <= limit);
            if (!take) continue;
            int ra = find(a), rb = find(b);
            if (ra == rb) continue;
            if (sz[ra] < sz[rb]) swap(ra, rb);
            par[rb] = ra;
            sz[ra] += sz[rb];
        }
        return find(u) == find(v);
    };

    string out;
    for (int i = 0; i < m; i++) {
        int u = edges[i][0], v = edges[i][1], w = edges[i][2];
        if (connected(u, v, w, true, -1))          // 더 싼 간선만으로 이미 연결
            out += "NONE\n";
        else if (connected(u, v, w, false, i))     // 같은 무게 이하의 대체 경로 존재
            out += "SOME\n";
        else
            out += "ALL\n";
    }
    cout << out;
    return 0;
}
@@TESTS
--IN
4 5
0 1 1
1 2 2
2 3 2
0 3 2
0 2 3
--OUT
ALL
SOME
SOME
SOME
NONE
--IN
3 3
0 1 1
1 2 2
0 2 3
--OUT
ALL
ALL
NONE
--IN
2 1
0 1 5
--OUT
ALL
--IN
4 4
0 1 7
1 2 7
2 3 7
3 0 7
--OUT
SOME
SOME
SOME
SOME
@@EXPL
(1) 접근·핵심 아이디어

- Kruskal의 관점에서 간선 e=(u,v,w)를 볼 차례가 왔을 때, 이미 w 미만 간선들로 u-v가 이어져 있으면 e는 어떤 순서로 돌려도 사이클이 되어 절대 채택되지 않는다 → `NONE`. 반대로 이어져 있지 않으면 컷 성질에 의해 e를 포함하는 MST가 존재한다.
- 그 경우, e를 빼고 w 이하 간선(같은 무게 포함)만으로 u-v가 이어진다면 e 대신 그 경로의 간선을 써도 비용이 같은 MST가 되므로 e 없는 MST가 존재 → `SOME`. 이어지지 않으면 어떤 MST도 e 없이는 u-v를 w 이하로 못 잇는다 → `ALL`(e는 "가중치 w 이하 부분 그래프"의 다리).

(2) 코드 단계별

- 간선 목록을 `{a, b, w}` 순으로 저장한다(이 문제는 정렬이 필요 없어 입력 순서 그대로 둔다).
- `connected(u, v, limit, strict, skip)` 람다: 호출될 때마다 `par`·`sz`를 **새로 만든다**. 조건(미만/이하)에 맞는 간선만 합친 뒤 u, v가 같은 집합인지 반환. `skip`은 자기 자신 제외용.
- 간선마다 (1) `strict=true, skip=-1`로 NONE 판정, (2) 아니면 `strict=false, skip=i`로 SOME/ALL 판정.
- 결과를 문자열 버퍼에 모아 한 번에 출력.

(3) 스스로 다시 짤 때 생각 순서

- 컷 성질에서 "w 미만으로 연결됐는가"를 먼저, 그다음 "동점 대체 경로가 있는가"를 확인하는 2단계 판정으로 정리. 간선당 Union-Find 2회 → O(m²·α(n)).
- C++ 함정: `bool take = strict ? (w < limit) : (w <= limit);`에서 삼항 연산자의 우선순위는 대입보다 높지만 비교보다 낮다. `strict ? w < limit : w <= limit`도 같은 뜻이긴 하나, 조건식이 조금만 복잡해지면 의도와 달리 묶이므로 괄호를 넣는 편이 안전하다.
- 경계: 모든 가중치가 같은 사이클(넷째 테스트)은 어느 간선이든 빼도 나머지 셋으로 이어지므로 전부 SOME. 정점 2개·간선 1개면 대체 경로가 없어 ALL. 가중치가 전부 다르면 MST가 유일해 SOME은 나오지 않는다.
```

**9) 간선 철거 후 연결 질의** · Hard

- **요구사항**: 무방향 그래프의 간선이 입력 순서대로 1번부터 하나씩 철거된다. 질의 `t u v`는 "앞에서부터 t개의 간선을 철거한 시점에 u와 v가 연결되어 있는가"를 묻는다. 질의는 임의의 순서로 주어지며 원래 순서대로 답하라. Union-Find는 삭제를 지원하지 않으므로, 질의를 t 내림차순으로 정렬해 **간선을 거꾸로 되살리며** 처리하라(오프라인 역순 처리). 랭크 기준 합치기를 사용한다.
- **입력**: 첫 줄 `n m` (1 ≤ n ≤ 300, 0 ≤ m ≤ 500). 다음 m줄 간선 `a b` (0-based). 다음 줄 q (1 ≤ q ≤ 300). 다음 q줄 `t u v` (0 ≤ t ≤ m).
- **출력**: 질의마다 입력 순서대로 `YES` 또는 `NO`.
- **예제**:
  `5 5 / 0 1 / 1 2 / 2 3 / 3 4 / 0 4 / 5 / 0 0 3 / 2 0 3 / 4 0 3 / 5 2 2 / 1 0 1` → `YES / YES / NO / YES / YES`
  (t=4면 간선 0-4만 남아 0-3은 NO. t=5는 간선이 없지만 u=v라 YES)
  `2 1 / 0 1 / 2 / 0 0 1 / 1 0 1` → `YES / NO`
- **셀프체크**: 시각 t에 남아 있는 간선은 번호 t+1..m이며, 큰 t부터 처리하면서 포인터 p를 m에서 t까지 내리며 간선 p를 합치면 되는가? 답을 원래 질의 순서로 되돌려 놓았는가(질의에 번호를 붙여 저장)? 정렬 비교자를 `a.t > b.t`처럼 **엄격한 부등호**로 썼는가(`>=`를 쓰면 strict weak ordering이 깨져 `sort`가 미정의 동작이다)? t=m(전부 철거)에서 u=v면 YES인가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

struct Query { int t, u, v, id; };

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<pair<int, int>> edges(m);
    for (int i = 0; i < m; i++) cin >> edges[i].first >> edges[i].second;
    int q;
    cin >> q;
    vector<Query> qs(q);
    for (int i = 0; i < q; i++) {
        cin >> qs[i].t >> qs[i].u >> qs[i].v;
        qs[i].id = i;
    }
    // 많이 철거된 시점부터. 비교자는 반드시 엄격한 부등호(strict weak ordering)
    sort(qs.begin(), qs.end(), [](const Query &a, const Query &b) { return a.t > b.t; });

    vector<int> par(n), rnk(n, 0);        // rank는 <type_traits>의 std::rank와 헷갈리니 rnk
    iota(par.begin(), par.end(), 0);

    function<int(int)> find = [&](int x) {
        int root = x;
        while (par[root] != root) root = par[root];
        while (par[x] != root) {
            int nx = par[x];
            par[x] = root;
            x = nx;
        }
        return root;
    };
    auto unite = [&](int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return;
        if (rnk[ra] < rnk[rb]) swap(ra, rb);   // 낮은 트리를 높은 트리 밑에
        par[rb] = ra;
        if (rnk[ra] == rnk[rb]) rnk[ra]++;
    };

    vector<string> ans(q);
    int p = m;                                 // 간선 p+1..m 이 되살아난 상태
    for (auto &Q : qs) {
        while (p > Q.t) {                      // 시각 t까지 간선을 거꾸로 복구
            unite(edges[p - 1].first, edges[p - 1].second);
            p--;
        }
        ans[Q.id] = (find(Q.u) == find(Q.v)) ? "YES" : "NO";
    }
    string out;
    for (int i = 0; i < q; i++) { out += ans[i]; out += '\n'; }
    cout << out;
    return 0;
}
@@TESTS
--IN
5 5
0 1
1 2
2 3
3 4
0 4
5
0 0 3
2 0 3
4 0 3
5 2 2
1 0 1
--OUT
YES
YES
NO
YES
YES
--IN
2 1
0 1
2
0 0 1
1 0 1
--OUT
YES
NO
--IN
3 0
1
0 0 2
--OUT
NO
--IN
4 3
0 1
1 2
2 3
3
3 0 3
3 1 1
2 2 3
--OUT
NO
YES
YES
@@EXPL
(1) 접근·핵심 아이디어

- Union-Find는 합치기만 되고 분리는 안 된다. 그런데 "철거"를 시간을 거꾸로 보면 "설치"가 된다. 모든 질의를 미리 받아(오프라인) t가 큰 순서로 처리하면, 시각 t로 갈수록 남은 간선이 늘어나므로 합치기만으로 상태를 유지할 수 있다.
- 시각 t에 남은 간선은 번호 t+1..m이다. 포인터 p를 m에서 시작해 `p > t`인 동안 간선 p를 합치고 p를 내린다. 질의는 t 내림차순이라 p는 단조 감소하며 각 간선은 정확히 한 번만 합쳐진다.

(2) 코드 단계별

- 간선과 질의를 읽고, 질의 구조체에 원래 번호 `id`를 붙여 t 내림차순으로 정렬한다.
- 랭크 기준 `unite`(높이가 낮은 트리를 높은 트리 밑에, 같으면 랭크 +1)와 경로 압축 `find`를 준비한다. 랭크 배열 이름을 `rank`로 지으면 `using namespace std;` 아래에서 `std::rank`와 이름이 겹쳐 읽기 헷갈리므로 `rnk`로 둔다.
- 정렬된 질의를 돌며 필요한 간선을 되살린 뒤 `find(u) == find(v)`를 `ans[id]`에 기록.
- `ans`를 원래 순서로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "삭제 질의 → 시간 역순 삽입"이라는 변환을 먼저 떠올린다 → 질의 정렬(번호 보존) → 포인터로 간선 복구 → 답을 원래 순서로 복원. O((m + q)·α(n) + q log q).
- C++ 함정: `sort`의 비교자는 strict weak ordering이어야 한다. `return a.t >= b.t;`처럼 같음을 참으로 만들면 "a<b이고 b<a"인 상태가 생겨 표준이 정의하지 않은 동작(대개 범위 밖 접근으로 크래시)이 된다. 안정성이 필요하면 `stable_sort`를 쓰되 비교자는 여전히 엄격해야 한다.
- 경계: t=m이면 간선이 하나도 없지만 u=v면 같은 집합이라 YES. m=0이면 복구할 간선이 없고 모든 다른 두 정점은 NO. 같은 t의 질의가 연속되어도 `while (p > t)`가 0번 돌 뿐이다.
```

**10) 길이 제한과 기존 배선이 있는 전력망** · Hard

- **요구사항**: 평면 위 n개의 건물이 있고, 두 건물을 직접 잇는 전선 비용은 맨해튼 거리다. 단, 한 전선의 길이는 L을 넘을 수 없다(거리가 L보다 크면 직접 연결 불가). 또 일부 건물 쌍은 이미 배선되어 있어 비용 0으로 연결된 것으로 본다(길이 제한과 무관). 모든 건물을 연결하는 최소 총비용을 구하고, 불가능하면 -1을 출력하라. 힙 기반 Prim으로 풀되, 인접 리스트를 직접 만들어 사용한다.
- **입력**: 첫 줄 `n L` (1 ≤ n ≤ 100, 0 ≤ L ≤ 10^5). 다음 n줄 `x y` (0 ≤ x, y ≤ 10^4). 다음 줄 f (0 ≤ f ≤ 100). 다음 f줄 기존 배선 `a b` (0-based).
- **출력**: 최소 총비용(또는 -1).
- **예제**:
  `5 5 / 0 0 / 3 0 / 3 4 / 10 10 / 12 10 / 1 / 2 3` → `9`
  (0-1(3), 1-2(4), 2-3(기존 0), 3-4(2). 2-3은 거리 13이지만 기존 배선)
  `5 5 / 0 0 / 3 0 / 3 4 / 10 10 / 12 10 / 0` → `-1`
  (건물 3, 4까지 5 이하 전선으로 닿을 수 없음)
- **셀프체크**: 모든 쌍 중 거리가 L 이하인 것만 인접 리스트에 양방향으로 넣고, 기존 배선은 거리와 무관하게 비용 0 간선으로 추가했는가? `priority_queue`에 `greater<>`를 붙여 **최소 힙**으로 만들었는가(기본은 최대 힙이라 붙이지 않으면 가장 비싼 간선부터 꺼낸다)? 힙에서 꺼낸 정점이 이미 편입됐으면 건너뛰는 지연 삭제를 했는가? 편입 정점이 n개 미만이면 -1인가? L=0이면 같은 좌표끼리만 직접 연결되는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, L;
    cin >> n >> L;
    vector<int> xs(n), ys(n);
    for (int i = 0; i < n; i++) cin >> xs[i] >> ys[i];
    int f;
    cin >> f;

    vector<vector<pair<int, int>>> adj(n);      // {상대, 비용}
    for (int i = 0; i < n; i++)                 // 길이 제한 이하인 쌍만 간선으로
        for (int j = i + 1; j < n; j++) {
            int d = abs(xs[i] - xs[j]) + abs(ys[i] - ys[j]);
            if (d <= L) {
                adj[i].push_back({j, d});
                adj[j].push_back({i, d});
            }
        }
    for (int i = 0; i < f; i++) {               // 기존 배선: 비용 0, 제한 무관
        int a, b;
        cin >> a >> b;
        adj[a].push_back({b, 0});
        adj[b].push_back({a, 0});
    }

    vector<char> visited(n, 0);
    // 기본 priority_queue는 최대 힙 → greater<>를 붙여야 최소 힙
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    pq.push({0, 0});                            // {비용, 정점}
    long long total = 0;
    int cnt = 0;
    while (!pq.empty() && cnt < n) {
        auto [w, u] = pq.top();
        pq.pop();
        if (visited[u]) continue;               // 지연 삭제
        visited[u] = 1;
        total += w;
        cnt++;
        for (auto &[v, wv] : adj[u])
            if (!visited[v]) pq.push({wv, v});
    }
    cout << (cnt == n ? total : -1) << '\n';
    return 0;
}
@@TESTS
--IN
5 5
0 0
3 0
3 4
10 10
12 10
1
2 3
--OUT
9
--IN
5 5
0 0
3 0
3 4
10 10
12 10
0
--OUT
-1
--IN
1 1
0 0
0
--OUT
0
--IN
3 0
1 1
1 1
2 2
1
0 2
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 좌표 완전 그래프에 두 가지 변형이 붙었다: (a) 길이 제한 — 거리 > L인 쌍은 간선이 아예 없다(그래프가 비연결이 될 수 있음). (b) 기존 배선 — 비용 0 간선을 제한과 무관하게 추가. 이 두 조건을 인접 리스트를 만드는 단계에서 처리하면, 그 뒤는 표준 힙 Prim이다.
- 기존 배선을 "미리 합치기"로 처리하는 Kruskal 방식도 되지만, 여기서는 비용 0 간선으로 넣어 Prim이 자연스럽게 먼저 꺼내게 한다(최소 힙에서 0이 가장 먼저 나오므로).

(2) 코드 단계별

- 좌표를 읽고, 모든 쌍 (i, j)에 대해 맨해튼 거리 d가 L 이하일 때만 양방향으로 `adj`에 추가한다(n ≤ 100이라 O(n²) 간선이 부담 없다).
- 기존 배선 f개를 `{상대, 0}`으로 양방향 추가.
- `priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>>`에 `{0, 0}`을 넣고 Prim: 꺼낸 정점이 이미 편입이면 건너뛰고, 아니면 편입해 비용 누적 후 이웃을 push. `auto [w, u] = pq.top();`은 C++17 구조적 바인딩으로 `pair`를 두 이름으로 한 번에 푸는 표기다.
- 편입 수가 n이면 `total`, 아니면 -1.

(3) 스스로 다시 짤 때 생각 순서

- 조건을 "간선 생성 규칙"으로 번역(제한 → 필터, 기존 배선 → 0비용) → 인접 리스트 → 힙 Prim + 지연 삭제 + `cnt == n` 판정. O(n² log n).
- C++ 함정: `priority_queue`의 기본 비교자는 `less<>`이고 **가장 큰 원소**가 top이다. 파이썬 `heapq`는 최소 힙이라 그대로 옮기면 정반대로 동작한다. `greater<>`를 넣거나 비용에 음수를 넣는 두 방법 중 하나를 반드시 써야 한다.
- 경계: n=1이면 시작 정점만 편입해 0. L=0이면 같은 좌표(거리 0)끼리만 이어지고 나머지는 기존 배선에 의존한다(넷째 테스트). 둘째 테스트처럼 멀리 떨어진 건물은 기존 배선이 없으면 -1.
```
