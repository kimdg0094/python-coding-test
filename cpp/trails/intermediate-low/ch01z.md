## L7. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터는 "격자 위에서 규칙을 그대로 옮긴다"는 하나의 기술을 다섯 갈래로 펼친 것이다.
L1이 좌표계·방향·경계라는 바닥을 깔고, L2~L3이 "값들이 움직인다", L4~L5가 "객체가
움직인다"로 갈라진다. C++에서는 여기에 하나가 더 붙는다 — **무엇을 복사하고 무엇을
참조로 넘길 것인가**. 격자 하나가 곧 수십만 개의 정수라, 이 결정이 시간 초과와 통과를
가른다. 마지막 절의 실수 목록은 실제 채점에서 오답을 만드는 것들만 모았다.

**개념 지도**

```text
 L1  grid scan
     coords (r,c) / dir vectors dr,dc / in_range()
       |
       +---> L2  push & gravity
       |         one-line function + transpose / reverse  ==> 4 dirs
       |           |
       |           +---> L3  clear & fall
       |                 mark all -> clear once -> fall -> repeat
       |
       +---> L4  a single actor
                 state = (r, c, dir) + turn / reflect / wrap
                   |
                   +---> L5  many actors
                         simultaneous vs sequential update
                           |
                           +---> collision: group by destination cell
```

위쪽 두 줄(좌표계·경계 검사)이 무너지면 아래 전부가 무너진다. 왼쪽 가지(L2·L3)는
"칸에 담긴 값"이 주인공이고, 오른쪽 가지(L4·L5)는 "칸 위를 걷는 물체"가 주인공이다.

```text
 what is actually moving?
   nothing, only counting          -> L1  double for loop + in_range
   a whole row or column of values -> L2  push_left + rotate trick
   values vanish, then refill      -> L3  mark -> clear -> fall -> loop
   exactly one actor               -> L4  (r, c, dir) state machine
   many actors at the same time    -> L5  new board / dest grouping
```

문제를 읽고 이 다섯 줄 중 하나를 고르는 것이 첫 번째 결정이다. 고르고 나면 아래 뼈대를
그대로 꺼내 쓰면 된다.

C++에서 격자를 다룰 때의 전달 방식은 아래 세 갈래로 외워 둔다. 이것을 틀리면 알고리즘이
맞아도 결과가 안 바뀌거나(복사본만 고침) 시간이 터진다(복사 폭발).

```text
 how to hand a grid to a function

   read only            const vector<vector<int>>& g     no copy, cannot modify
   modify in place            vector<vector<int>>& g     no copy, caller sees it
   need a fresh copy          vector<vector<int>>  h = g deep copy on purpose

   by value  vector<vector<int>> g   -> R*C ints copied + R heap allocations
                                        on EVERY call.  almost always a bug.
```

**뼈대 코드**

(1) 격자 입력 · 순회 · 경계 검사 — 모든 문제의 첫 20줄

```cpp
#include <bits/stdc++.h>
using namespace std;

int R, C;
vector<vector<int>> g;

const int DR[4] = {-1, 0, 1, 0};        // 북 동 남 서 (시계 방향)
const int DC[4] = {0, 1, 0, -1};

inline bool in_range(int r, int c) {
    return 0 <= r && r < R && 0 <= c && c < C;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> R >> C;
    g.assign(R, vector<int>(C, 0));     // 각 행이 독립된 벡터, 0으로 초기화
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            cin >> g[r][c];             // <- 문제마다 바뀜(정수/문자)

    for (int r = 0; r < R; r++) {
        for (int c = 0; c < C; c++) {
            for (int d = 0; d < 4; d++) {          // <- 문제마다 바뀜(4방향/8방향)
                int nr = r + DR[d], nc = c + DC[d];
                if (!in_range(nr, nc)) continue;   // 검사 먼저, 접근은 그다음
                // <- 문제마다 바뀜(세기/최댓값/표시)
            }
        }
    }
    return 0;
}
```

격자를 문자로 읽어야 하면 `vector<string> grid(R); for (auto& s : grid) cin >> s;`가 가장
짧다. 각 칸은 문자라 `grid[r][c] == '1'`로 비교하거나 `grid[r][c] - '0'`으로 정수화한다.

(2) 한 줄 밀기 + 전치·회전 유틸 — 좌 밀기 하나로 네 방향을 만든다

```cpp
// 한 줄을 왼쪽으로 밀며 합치기. 길이는 그대로 유지한다.
vector<int> push_left(const vector<int>& row) {
    int n = (int)row.size();
    vector<int> vals;
    for (int x : row) if (x != 0) vals.push_back(x);   // 빈칸 제거, 순서 유지
    vector<int> res;
    int i = 0;
    while (i < (int)vals.size()) {
        if (i + 1 < (int)vals.size() && vals[i] == vals[i + 1]) {
            res.push_back(vals[i] * 2);   // <- 문제마다 바뀜(합치기 규칙)
            i += 2;                       // 2씩 건너뛰어 이중 합치기 차단
        } else {
            res.push_back(vals[i]);
            i += 1;
        }
    }
    while ((int)res.size() < n) res.push_back(0);
    return res;
}

// 전치 : (r,c) -> (c,r).  모양이 R x C 에서 C x R 로 바뀐다
vector<vector<int>> transpose(const vector<vector<int>>& a) {
    int n = (int)a.size(), m = (int)a[0].size();
    vector<vector<int>> t(m, vector<int>(n));
    for (int r = 0; r < n; r++)
        for (int c = 0; c < m; c++)
            t[c][r] = a[r][c];
    return t;
}

// 각 행 좌우 반전 : (r,c) -> (r, C-1-c).  참조로 받아 제자리에서 뒤집는다
void flip_h(vector<vector<int>>& a) {
    for (auto& row : a) reverse(row.begin(), row.end());
}

// 네 방향 이동을 push_left 하나로 처리한다
void move_all(vector<vector<int>>& a, char d) {
    if (d == 'L') {
        for (auto& row : a) row = push_left(row);
    } else if (d == 'R') {
        flip_h(a);
        for (auto& row : a) row = push_left(row);
        flip_h(a);
    } else if (d == 'U') {
        a = transpose(a);
        for (auto& row : a) row = push_left(row);
        a = transpose(a);
    } else {                       // 'D'
        a = transpose(a);
        flip_h(a);
        for (auto& row : a) row = push_left(row);
        flip_h(a);
        a = transpose(a);
    }
}
```

`push_left` 하나만 테스트해 두면 네 방향이 자동으로 옳다. 방향마다 따로 짜지 않는다.
`move_all`과 `flip_h`의 매개변수가 `&`인 것에 주목하라 — 값으로 받으면 복사본만 바뀌고
호출한 쪽 격자는 하나도 안 변한다.

전치를 쓰지 않고 열을 직접 뽑아 쓰는 방법도 있다. 임시 격자 할당이 없어 더 빠르다.

```cpp
// 위로 밀기 : 열 하나를 벡터로 뽑아 push_left 한 뒤 되써넣는다
void push_up(vector<vector<int>>& a) {
    int n = (int)a.size(), m = (int)a[0].size();
    vector<int> col(n);
    for (int c = 0; c < m; c++) {
        for (int r = 0; r < n; r++) col[r] = a[r][c];
        vector<int> out = push_left(col);
        for (int r = 0; r < n; r++) a[r][c] = out[r];
    }
}
```

(3) 연쇄 제거 · 낙하 루프 — 표시 → 종료 판정 → 일괄 제거 → 낙하

```cpp
// 가로 K연속을 표시한다. 세로도 같은 모양으로 이어 붙인다.
bool mark(const vector<vector<int>>& a, vector<vector<char>>& boom, int K) {
    int n = (int)a.size(), m = (int)a[0].size();
    bool hit = false;
    for (auto& row : boom) fill(row.begin(), row.end(), 0);
    for (int r = 0; r < n; r++) {                 // 가로 런
        int run = 1;
        for (int c = 1; c <= m; c++) {
            bool same = (c < m) && a[r][c] != 0 && a[r][c] == a[r][c - 1];
            if (same) { run++; continue; }
            if (run >= K) {                       // <- 문제마다 바뀜(K, 판정 방식)
                for (int k = c - run; k < c; k++) boom[r][k] = 1;
                hit = true;
            }
            run = 1;
        }
    }
    return hit;                                   // 세로 런도 같은 모양으로 추가
}

// 아래 방향 중력. 쓰기 포인터를 바닥부터 올린다.
void fall(vector<vector<int>>& a) {
    int n = (int)a.size(), m = (int)a[0].size();
    for (int c = 0; c < m; c++) {
        int w = n - 1;
        for (int r = n - 1; r >= 0; r--)
            if (a[r][c] != 0) a[w--][c] = a[r][c];
        while (w >= 0) a[w--][c] = 0;
    }
}

void run_until_stable(vector<vector<int>>& a, int K) {
    int n = (int)a.size(), m = (int)a[0].size();
    vector<vector<char>> boom(n, vector<char>(m, 0));
    while (true) {
        if (!mark(a, boom, K)) break;             // 종료: 이번 라운드에 아무것도 안 터짐
        for (int r = 0; r < n; r++)
            for (int c = 0; c < m; c++)
                if (boom[r][c]) a[r][c] = 0;      // 표시된 것을 한꺼번에 제거
        fall(a);
    }
}
```

표시 격자는 `vector<vector<bool>>`이 아니라 `vector<vector<char>>`로 잡았다.
`vector<bool>`은 비트로 압축된 특수화라 원소의 참조나 주소를 얻을 수 없어, 나중에
포인터·참조가 필요해지면 컴파일이 막힌다.

(4) 단일 객체 이동 — 상태 (r, c, d) + 회전 · 반사 · 래핑

```cpp
// 회전용 방향 배열은 반드시 시계 순서(북 동 남 서)여야 한다
const int RR[4] = {-1, 0, 1, 0};
const int RC[4] = {0, 1, 0, -1};

inline int turn_right(int d) { return (d + 1) % 4; }
inline int turn_left(int d)  { return (d + 3) % 4; }   // (d-1)%4 는 음수가 된다

void simulate(int n, int m, int& r, int& c, int& d, const string& cmds) {
    for (char ch : cmds) {                     // <- 문제마다 바뀜(명령 집합)
        if (ch == 'R') { d = turn_right(d); continue; }
        if (ch == 'L') { d = turn_left(d);  continue; }
        int nr = r + RR[d], nc = c + RC[d];
        if (0 <= nr && nr < n && 0 <= nc && nc < m) {
            r = nr; c = nc;
        } else {
            // <- 문제마다 바뀜(무시 / 반사 / 회전 / 래핑)
        }
    }
}

// 벽 반사 : 부딪힌 축의 성분만 부호를 뒤집는다
void reflect(int& dr, int& dc, int nr, int nc, int n, int m) {
    if (nr < 0 || nr >= n) dr = -dr;           // 위/아래 벽: 행 성분만
    if (nc < 0 || nc >= m) dc = -dc;           // 좌/우 벽: 열 성분만
}

// 래핑(토러스) : C++ 의 % 는 음수를 그대로 돌려주므로 한 번 더 더한다
inline int wrap(int x, int n) { return (x % n + n) % n; }
```

명령 수 T가 매우 클 때는 상태 `(r, c, d)`를 `(r * C + c) * 4 + d`라는 정수 하나로 접어
`vector<int> seen(R * C * 4, -1)`에 "몇 번째 스텝에 처음 봤는지"를 기록한다. 상태가
`R*C*4`개뿐이라 반드시 반복되고, 주기를 찾으면 남은 스텝을 나머지 연산으로 건너뛴다.
스텝 수는 `long long`으로 잡는다 — `int`로는 10^9 근처에서 곱셈 한 번에 넘친다.

(5) 여러 객체 동시 이동 + 충돌 — 도착 칸으로 그룹핑

```cpp
struct Obj { int r, c, size, d; };

// 한 턴. 원본은 읽기만 하고 결과는 새 벡터에 쓴다.
vector<Obj> one_turn(const vector<Obj>& objs, int n, int m) {
    unordered_map<int, vector<int>> dest;          // key = nr * m + nc
    vector<pair<int,int>> nxt(objs.size());        // 각 객체의 도착 칸
    for (int i = 0; i < (int)objs.size(); i++) {
        int nr = objs[i].r + RR[objs[i].d];
        int nc = objs[i].c + RC[objs[i].d];
        if (nr < 0 || nr >= n || nc < 0 || nc >= m) {
            nr = objs[i].r; nc = objs[i].c;        // <- 문제마다 바뀜(벽 처리)
        }
        nxt[i] = {nr, nc};
        dest[nr * m + nc].push_back(i);            // 없으면 빈 벡터가 자동 생성
    }
    vector<Obj> out;
    for (auto& kv : dest) {                        // auto& : 그룹을 복사하지 않는다
        int r = kv.first / m, c = kv.first % m;
        vector<int>& grp = kv.second;
        if (grp.size() == 1) {
            Obj o = objs[grp[0]]; o.r = r; o.c = c;
            out.push_back(o);
        } else {                                   // <- 문제마다 바뀜(생존/합체 규칙)
            int total = 0, bestIdx = grp[0];
            for (int id : grp) {
                total += objs[id].size;
                if (objs[id].size > objs[bestIdx].size) bestIdx = id;
            }
            out.push_back({r, c, total, objs[bestIdx].d});
        }
    }
    return out;
}
```

동시 갱신이면 **원본을 읽고 결과는 새 벡터/새 격자에** 쓴다. 순차 갱신이면 정렬 키를
문제 문장 그대로 못 박은 뒤 하나씩 즉시 반영한다. `unordered_map`은 순회 순서가 정해져
있지 않으므로, 판정 순서가 답을 바꾸는 문제라면 `map`을 쓰거나 키를 모아 정렬해서 돈다.

(6) 시간 순 이벤트 루프 — "T초 동안" 류 문제의 바깥 틀

```cpp
int solve(int T, State& state) {
    for (int t = 1; t <= T; t++) {          // <- 문제마다 바뀜(초/턴/명령 개수)
        phase_move(state);                  // 1단계: 이동
        phase_collide(state);               // 2단계: 충돌/합체
        phase_spawn(state, t);              // 3단계: 생성/소멸
        if (is_done(state)) return t;       // <- 문제마다 바뀜(조기 종료 조건)
    }
    return -1;
}
```

한 턴 안의 단계 순서를 문제 문장에서 그대로 베껴 함수 이름으로 남기면, 순서를
바꿔 끼우는 실수가 사라진다. 각 단계가 `State&`를 받는 것에 주목하라 — 값으로 받으면
단계마다 상태 전체가 복사되고 갱신은 밖으로 나가지 않는다.

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 각 칸에서 이웃만 보면 되는 세기/판정 | 이중 for + 방향 벡터 | 상태가 없고 순서도 무관 | O(R·C) |
| 고정 크기 K×K 창을 전부 훑기 | 시작점 범위를 `r < R-K+1`로 제한 | 경계 넘침을 원천 차단 | O(R·C·K²) |
| K가 커서 창 합산이 무거움 | 2차원 누적합 | 창 하나를 O(1)로 계산 | O(R·C) |
| 한 방향으로 값 몰기(합치기 포함) | `push_left` + 전치·반전 | 함수 하나만 검증하면 4방향이 옳다 | O(R·C) / 회 |
| 합치기 없는 단순 낙하 | 열마다 쓰기 포인터를 바닥부터 올리기 | 이동을 시뮬레이션할 필요가 없다 | O(R·C) |
| "가로·세로 K개 연속" 소거 | 런(run) 스캔 | 연결성이 아니라 연속성 조건 | O(R·C) / 라운드 |
| "상하좌우로 이어진 덩어리 K개" 소거 | `queue` 기반 반복 BFS + `visited` | 연결 요소 크기를 재야 함 | O(R·C) / 라운드 |
| 연쇄가 안정될 때까지 | 표시→제거→낙하 while 루프 | 종료 조건이 명확해야 무한 루프가 없다 | 최악 O((R·C)²) |
| 주인공이 정확히 하나 | `(r, c, d)` 상태 + 모듈러 회전 | 격자를 갱신할 필요 없이 상태만 | O(T) |
| 명령 수 T가 10⁸ 수준 | 상태를 정수로 접고 `vector`로 사이클 탐지 | 상태가 `R·C·4`개뿐이라 반드시 반복 | O(R·C) |
| 여러 객체가 동시에 이동 | 새 격자/새 벡터에 쓰기 | 이미 움직인 값이 다시 읽히는 오염 차단 | O(K + R·C) / 턴 |
| 같은 칸에 여럿이 도착 | 좌표를 `r*C+c`로 접어 `unordered_map` 그룹핑 | 충돌 규칙을 한 곳에서 처리 | O(K) / 턴 |
| 도착 칸을 정해진 순서로 처리해야 함 | `map` 또는 키를 모아 `sort` | `unordered_map`은 순회 순서가 미정 | O(K log K) / 턴 |
| 객체가 정해진 순서로 하나씩 | 동점 기준까지 적은 비교 함수로 `sort` | `sort`는 동점 순서를 보장하지 않는다 | O(K log K) / 턴 |
| 큰 격자를 여러 함수에 넘겨야 함 | `const vector<vector<int>>&` / `vector<vector<int>>&` | 값 전달은 호출마다 R·C개 복사 | 복사 비용 0 |
| 매 턴 격자를 통째로 새로 만들어야 함 | 격자 두 개를 미리 잡고 `swap` | 매 턴 R번의 힙 할당을 없앤다 | O(1) 할당 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: `g[r][c]`에서 r과 c가 각각 어느 방향으로 증가하는지, 그리고 방향 배열 `DR/DC`의 순서를 회전 규칙과 어떻게 맞추는지.
- [ ] 설명할 수 있다: 경계 검사를 "이동 후 접근 전"에 넣어야 하는 이유와, `vector`의 `operator[]`가 범위를 검사하지 않아 범위 밖 접근이 조용한 미정의 동작이 된다는 사실.
- [ ] 설명할 수 있다: `int`와 `size()`를 섞어 비교하면 음수가 거대한 양수로 변환되어 조건이 뒤집히는 과정.
- [ ] 설명할 수 있다: K×K 창의 시작점 범위가 왜 `r < R-K+1`인지 오프바이원까지.
- [ ] 설명할 수 있다: 한 줄 좌 밀기가 "빈칸 제거 → 합치기 → 0으로 채우기" 세 단계로 쪼개지는 이유.
- [ ] 설명할 수 있다: 인덱스를 2씩 건너뛰는 것이 왜 "한 번 합쳐진 타일의 재합치기"를 막는지.
- [ ] 설명할 수 있다: 전치와 좌우 반전이 좌표 `(r,c)`를 각각 어디로 보내는지, 그리고 그 조합으로 시계·반시계 회전이 어떻게 만들어지는지.
- [ ] 설명할 수 있다: 좌 밀기 함수 하나만 검증해도 네 방향이 옳은 이유, 그리고 그것이 버그를 왜 줄이는지.
- [ ] 설명할 수 있다: 제자리(in-place) 밀기가 값을 복제하는 구체적 과정과, 새 벡터를 만들어 반환하면 왜 안전해지는지.
- [ ] 설명할 수 있다: 함수 매개변수를 값·참조·const 참조 중 무엇으로 받을지 정하는 기준과, `&`를 빠뜨렸을 때 나타나는 두 가지 증상(안 바뀜 / 느려짐).
- [ ] 설명할 수 있다: "표시 후 일괄 제거"가 필요한 이유를 가로·세로 매치가 겹치는 예로.
- [ ] 설명할 수 있다: "연속 K개"와 "연결 덩어리 K개"의 차이, 각각에 런 스캔과 BFS 중 무엇을 쓰는지.
- [ ] 설명할 수 있다: 연쇄 루프의 종료 조건을 무엇으로 잡아야 무한 루프가 나지 않는지.
- [ ] 설명할 수 있다: 큰 격자에서 재귀 DFS 대신 `queue` 반복 BFS를 쓰는 이유(스택 크기와 깊이).
- [ ] 설명할 수 있다: 동시 갱신과 순차 갱신이 같은 입력에서 다른 답을 내는 상황 하나.
- [ ] 설명할 수 있다: 충돌 처리를 도착 칸 그룹핑으로 하는 이유와, 두 객체가 자리를 맞바꾸는 경우가 왜 따로 다뤄야 하는지.
- [ ] 설명할 수 있다: `map`과 `unordered_map`의 차이가 답을 바꿀 수 있는 상황, 그리고 `pair`를 해시 키로 바로 못 쓰는 이유.
- [ ] 설명할 수 있다: C++의 `%`가 음수에서 어떻게 동작하는지와, 순환 인덱스를 안전하게 만드는 `(x % n + n) % n`의 논리.
- [ ] 설명할 수 있다: 명령 수 T가 매우 클 때 상태 사이클을 찾아 시간을 줄이는 논리와, 왜 스텝 수를 `long long`으로 잡아야 하는지.

**⚠️ 자주 하는 실수**

(1) 격자를 값으로 받아 고친다 — 호출한 쪽은 그대로

```cpp
// ❌ 틀린 코드
void clear_row(vector<vector<int>> a, int r) {   // 값 전달: 통째로 복사된다
    for (auto& x : a[r]) x = 0;
}
clear_row(g, 0);
cout << g[0][0] << "\n";      // 0 이 아니라 원래 값이 그대로 나온다
```

왜: 값 전달이면 함수 안의 `a`는 `g`의 **복사본**이다. 복사본을 고치고 함수가 끝나면 그
복사본은 버려진다. 게다가 호출할 때마다 R×C개 원소를 전부 복사하므로, 알고리즘이
맞아도 시간 초과가 난다.

```cpp
// ✅ 고친 코드
void clear_row(vector<vector<int>>& a, int r) {  // 참조: 주소만 넘어간다
    for (auto& x : a[r]) x = 0;
}
clear_row(g, 0);
cout << g[0][0] << "\n";      // 0
// 읽기만 할 함수는 const vector<vector<int>>& 로 받아 실수를 원천 차단한다
```

(2) 범위 밖 인덱스가 예외가 아니라 조용한 미정의 동작

```cpp
// ❌ 틀린 코드
int nr = r + dr, nc = c + dc;
int val = g[nr][nc];                              // 먼저 읽고
if (0 <= nr && nr < R && 0 <= nc && nc < C)       // 나중에 검사
    total += val;
```

왜: `nr`이 -1이면 `g[-1]`의 인덱스가 부호 없는 타입으로 변환되어 거대한 값이 되고,
벡터 바깥의 엉뚱한 메모리를 읽는다. 예외도 안 나고 대개 크래시도 안 나서, 그럴듯한
쓰레기 값이 조용히 답을 오염시킨다.

```cpp
// ✅ 고친 코드
int nr = r + dr, nc = c + dc;
if (0 <= nr && nr < R && 0 <= nc && nc < C)       // 검사 먼저
    total += g[nr][nc];                           // 접근은 그다음
```

(3) `int`와 `size()`를 섞어 비교 — 음수가 거대한 양수가 된다

```cpp
// ❌ 틀린 코드
for (int c = -1; c < g[r].size(); c++) {   // size() 는 부호 없는 타입
    // c 가 -1 일 때 비교를 위해 c 가 unsigned 로 변환된다
    // -1 -> 18446744073709551615 이므로 조건이 거짓, 루프가 아예 안 돈다
}
if (c < g[r].size() - 1) { /* g[r] 이 비면 0-1 이 최댓값이라 항상 참 */ }
```

왜: `int`와 `unsigned`를 비교하면 `int` 쪽이 부호 없는 타입으로 변환된다. 음수는 거대한
양수가 되어 조건이 의도와 정반대로 뒤집히고, `size() - 1`은 빈 컨테이너에서 최댓값이 된다.

```cpp
// ✅ 고친 코드
int C = (int)g[r].size();          // 한 번 정수로 받아 둔다
for (int c = -1; c < C; c++) { /* 의도대로 돈다 */ }
if (c + 1 < C) { /* 뺄셈을 부호 없는 타입에서 하지 않는다 */ }
```

(4) 제자리 밀기로 값이 유령처럼 복제됨

```cpp
// ❌ 틀린 코드
void push_left_bad(vector<int>& row) {
    for (int i = 0; i < (int)row.size(); i++) {
        if (row[i] == 0) continue;
        int j = i;
        while (j > 0 && row[j - 1] == 0) {
            row[j - 1] = row[j];      // 앞으로 옮기고
            j--;                      // 원래 자리를 지우지 않았다
        }
    }
}
```

왜: 값을 앞 칸에 쓰면서 원래 칸을 비우지 않으면, 뒤이어 그 칸을 다시 읽어 같은 값이
두 번 등장한다. `[0,2,0,0]`이 `[2,2,0,0]`이 되는 식이다.

```cpp
// ✅ 고친 코드
vector<int> push_left_good(const vector<int>& row) {
    vector<int> vals;
    for (int x : row) if (x != 0) vals.push_back(x);   // 읽기 전용으로 모으고
    vals.resize(row.size(), 0);                        // 뒤를 0으로 채워 반환
    return vals;                                       // 반환은 move 라 복사 비용도 없다
}
```

(5) 이중 합치기 — 방금 합친 타일을 또 합친다

```cpp
// ❌ 틀린 코드
vector<int> res;
for (int i = 0; i < (int)vals.size(); i++) {
    if (!res.empty() && res.back() == vals[i]) res.back() *= 2;   // 결과와 또 합친다
    else res.push_back(vals[i]);
}
```

왜: `vals = {4, 4, 8}`이면 `4+4=8`이 되고, 다음 `8`이 그 결과와 다시 합쳐져 `16`이
된다. 실제 규칙은 한 이동에서 각 타일이 최대 한 번만 합쳐지는 것이다.

```cpp
// ✅ 고친 코드
vector<int> res;
int i = 0;
while (i < (int)vals.size()) {
    if (i + 1 < (int)vals.size() && vals[i] == vals[i + 1]) {
        res.push_back(vals[i] * 2);
        i += 2;                      // 소비한 두 칸을 건너뛴다
    } else {
        res.push_back(vals[i]);
        i += 1;
    }
}
```

(6) 전치 후에도 R, C를 그대로 쓴다

```cpp
// ❌ 틀린 코드
vector<vector<int>> t = transpose(g);    // 이제 t 는 C행 R열
for (int r = 0; r < R; r++)
    for (int c = 0; c < C; c++)
        t[r][c] = 0;                     // R != C 이면 범위 밖 접근
```

왜: 전치는 `(r,c) → (c,r)`이라 모양이 `R×C`에서 `C×R`로 바뀐다. 행·열 개수를 그대로
두면 정사각 격자에서만 우연히 통과하고 직사각에서 조용히 남의 메모리를 건드린다.

```cpp
// ✅ 고친 코드
vector<vector<int>> t = transpose(g);
int TR = (int)t.size(), TC = (int)t[0].size();   // 크기를 다시 잰다
for (int r = 0; r < TR; r++)
    for (int c = 0; c < TC; c++)
        t[r][c] = 0;
```

(7) 표시 없이 발견 즉시 제거 — 겹친 매치가 사라진다

```cpp
// ❌ 틀린 코드
for (int r = 0; r < R; r++)
    for (int c = 0; c + 2 < C; c++)
        if (g[r][c] != 0 && g[r][c] == g[r][c+1] && g[r][c] == g[r][c+2])
            g[r][c] = g[r][c+1] = g[r][c+2] = 0;   // 바로 지운다
// 이어서 세로 런을 검사하면, 이미 0 이 되어 세로 매치를 놓친다
```

왜: 가로 매치와 세로 매치가 한 칸을 공유할 때, 가로를 먼저 지우면 그 칸이 0이 되어
세로 런이 끊긴다. 같은 라운드에서 터져야 할 칸이 살아남는다.

```cpp
// ✅ 고친 코드
vector<vector<char>> boom(R, vector<char>(C, 0));
// 가로 스캔에서 boom 표시, 세로 스캔에서도 boom 표시 (격자는 그대로 둔다)
for (int r = 0; r < R; r++)
    for (int c = 0; c < C; c++)
        if (boom[r][c]) g[r][c] = 0;      // 다 표시한 뒤 한꺼번에 제거
```

(8) 동시 갱신인데 원본 격자를 고쳐가며 읽는다

```cpp
// ❌ 틀린 코드
for (int r = 0; r < R; r++)
    for (int c = 0; c < C; c++)
        if (g[r][c] == 1 && c + 1 < C) {
            g[r][c] = 0;
            g[r][c + 1] = 1;      // 다음 c 반복에서 이 1 을 또 읽는다
        }
```

왜: 방금 오른쪽으로 옮긴 값을 같은 스캔이 다시 만나 또 옮긴다. 한 턴에 한 칸만
움직여야 할 객체가 줄 끝까지 흘러간다.

```cpp
// ✅ 고친 코드
vector<vector<int>> nxt(R, vector<int>(C, 0));
for (int r = 0; r < R; r++)
    for (int c = 0; c < C; c++)
        if (g[r][c] == 1 && c + 1 < C)
            nxt[r][c + 1] = 1;    // 읽기는 g, 쓰기는 nxt
g.swap(nxt);                      // swap 은 포인터 교환이라 복사가 없다
```

(9) 회전 규칙과 방향 배열 순서가 어긋난다 / 좌회전에 음수 나머지

```cpp
// ❌ 틀린 코드
int DR[4] = {-1, 1, 0, 0};      // 북 남 서 동 (시계 순서가 아님)
int DC[4] = {0, 0, -1, 1};
d = (d + 1) % 4;                // "우회전"이라고 썼지만 북 -> 남 이 된다
d = (d - 1) % 4;                // "좌회전": d=0 이면 -1 이라 DR[-1] 범위 밖 접근
```

왜: `(d+1) % 4`가 우회전이 되려면 배열이 시계 방향(북·동·남·서)으로 정렬돼 있어야
한다. 그리고 C++의 `%`는 피제수의 부호를 따라가므로 `(0-1) % 4`는 3이 아니라 -1이다.

```cpp
// ✅ 고친 코드
int DR[4] = {-1, 0, 1, 0};      // 북 동 남 서 (시계 방향)
int DC[4] = {0, 1, 0, -1};
d = (d + 1) % 4;                // 우회전: 북 -> 동
d = (d + 3) % 4;                // 좌회전: 먼저 양수로 만들어 나머지를 구한다
// 검산: d=0(북)에서 우회전 한 번이 동쪽인지 작은 예제로 반드시 확인
```

(10) 지역 배열 미초기화 · `memset`으로 1을 채우려 함

```cpp
// ❌ 틀린 코드
void solve() {
    int dist[100][100];                    // 지역 배열: 쓰레기 값으로 시작
    memset(dist, 1, sizeof(dist));         // 1 로 채운 줄 알지만 아니다
    if (dist[0][0] == 1) { /* 절대 참이 되지 않는다 */ }
}
```

왜: 지역 배열은 0으로 초기화되지 않는다(전역·`static`이라야 0이다). 그리고 `memset`은
**바이트 단위**로 채우므로 각 `int`가 `0x01010101`(16843009)이 된다. 0과 -1(`0xFF`)만
바이트를 채워도 원하는 값이 나온다.

```cpp
// ✅ 고친 코드
void solve() {
    int dist[100][100];
    memset(dist, 0, sizeof(dist));                       // 0 은 안전
    memset(dist, -1, sizeof(dist));                      // -1 도 안전(0xFF)
    fill(&dist[0][0], &dist[0][0] + 100 * 100, 1);       // 임의의 값은 fill 로
    vector<vector<int>> d2(100, vector<int>(100, 1));    // 벡터면 생성자로 끝
}
```

(11) 범위 기반 for에서 `&`를 빠뜨려 복사본만 고친다

```cpp
// ❌ 틀린 코드
for (auto row : g)                    // row 는 행 전체의 복사본
    for (auto x : row) x = 0;         // 복사본의 복사본을 고친다
// g 는 하나도 안 바뀌고, 행 개수만큼 벡터 복사만 일어난다
```

왜: 범위 기반 for의 변수는 기본이 값 복사다. 큰 행이면 반복마다 통째로 복사되고,
거기에 가한 수정은 원본에 반영되지 않는다.

```cpp
// ✅ 고친 코드
for (auto& row : g)                   // 고칠 것은 auto&
    for (auto& x : row) x = 0;
for (const auto& row : g)             // 읽기만 할 것은 const auto&
    for (int x : row) { /* int 처럼 작은 값은 값 복사가 더 싸다 */ }
```

**다음 챕터로**

여기서 만든 "격자를 상태로 들고 규칙대로 갱신한다"는 감각은 다음 챕터의 백트래킹에서
"선택을 상태로 들고 되돌린다"로 이어진다. 특히 L5의 "새 격자에 쓰기 vs 제자리 수정"은
백트래킹의 "복사본 저장 vs 되돌리기"와 정확히 같은 고민이고, 여기서 익힌 참조 전달
습관은 재귀 함수의 프레임 크기를 줄여 스택 오버플로를 막는 데 그대로 쓰인다. 또 L3의
BFS 덩어리 세기는 이후 그래프 탐색 챕터에서 방문 배열과 큐를 다루는 기초가 된다.
