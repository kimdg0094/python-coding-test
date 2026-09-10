## L3. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch4(BFS)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. 새 문법은 없다. `queue`·`dist` 배열·다중 시작점·상태 확장·0-1 BFS(`deque` 양끝)만으로 12문제를 푼다.

- **반복 훈련 개념**
- push 시점 방문 표시 + 거리 배열: 큐에 넣는 순간 거리를 확정 — `if (dist[nr][nc] == -1) { dist[nr][nc] = dist[r][c] + 1; q.push({nr, nc}); }`
- 꺼내기 두 줄 한 세트: `queue`의 `pop()`은 값을 돌려주지 않는다 — `pair<int,int> cur = q.front(); q.pop();`
- 다중 시작점: 시작점 전부를 거리 0으로 먼저 넣고 한 번에 퍼뜨리기 — `dist[r][c] = 0; q.push({r, c});`를 모든 시작 칸에 대해 반복
- 상태 확장: 좌표에 추가 정보를 붙여 정점으로 삼고 방문 배열의 차원을 늘리기 — `dist[r][c][k]`(`vector<vector<vector<int>>>`), `q.push({nr, nc, nk})`
- 0-1 BFS: 비용 0인 전이는 `deque`의 앞(`push_front`), 비용 1인 전이는 뒤(`push_back`)에 넣어 최소 비용 보장
- 층(시간) 단위 처리: 큐 원소나 거리 배열에 시각을 실어 "t분 후"를 판정 — `if (t[r][c] == T) continue;`

- **코딩테스트 출제 맵**: 이 챕터의 유형은 백준 「단계별로 풀어보기」의 'DFS와 BFS'·'최단 경로' 단계(미로·토마토·숨바꼭질·벽 부수기·불 피해 탈출 류), 삼성 SW 역량테스트의 '시뮬레이션·BFS' 유형(격자 상태 변화 + 최단 이동), NeetCode 150의 'Graphs'(Rotting Oranges·Open the Lock·Walls and Gates 류)에 그대로 등장한다. 이 레슨의 유형 확장 문제는 그 대표 유형을 소재와 수치를 새로 만들어 재구성한 것이다.

- **문제 구성표**

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 가장 가까운 충전소 | Easy | 격자 BFS + 목표 여러 개 중 최단 | 반복 훈련 |
| 2 | K단계 건너 아는 사람 | Easy | 그래프 BFS 거리 + k번째 층 정점 수 | 반복 훈련 |
| 3 | 산불 T분 후 지도 | Medium | 다중 시작점 + 시간 제한 상태 | 반복 훈련 |
| 4 | 화물 리프트 버튼 최소 누름 | Medium | 1차원 상태 BFS(값 범위·금지 상태) | 반복 훈련 |
| 5 | 최소로 뚫는 벽의 수 | Medium | 0-1 BFS(`deque`) | 유형 확장 (백준 '최단 경로' 단계 0-1 BFS 스타일) |
| 6 | 열쇠와 잠긴 문 | Medium | 상태 확장(좌표+열쇠 보유) | 유형 확장 (삼성 SW 역량테스트 BFS 변형 스타일) |
| 7 | 두 사람의 만남 지점 | Medium | 그래프 BFS 두 번 + 거리 결합 | 반복 훈련 |
| 8 | 금고 다이얼 최소 회전 | Medium | 문자열 상태 BFS + 금지 상태 | 유형 확장 (NeetCode 'Graphs' Open the Lock 스타일) |
| 9 | 용암을 피해 탈출 | Hard | 두 단계 BFS(번짐 계산 후 이동) | 유형 확장 (백준 'DFS와 BFS' 단계 불 피해 탈출 스타일) |
| 10 | 최단 경로의 개수 | Hard | dist 층 구조 + 경로 수 누적(`long long`) | 유형 확장 (백준 '최단 경로' 단계 최단 경로 개수 스타일) |
| 11 | 얼음판 미끄러지기 | Hard | 전이가 "미끄러짐"인 격자 BFS | 유형 확장 (삼성 SW 역량테스트 시뮬레이션·BFS 스타일) |
| 12 | 최소 굴곡 배관 | Hard | 0-1 BFS + 방향 상태 | 반복 훈련 |

**문제**

**1) 가장 가까운 충전소** · Easy

- **요구사항**: `N×M` 격자에서 `S`는 로봇의 위치, `C`는 충전소(여러 개일 수 있음), `#`은 벽, `.`은 빈칸이다. 로봇이 상하좌우로 한 칸씩 이동할 때, 어떤 충전소든 가장 가까운 충전소까지의 최소 이동 횟수를 출력하라. 도달할 수 있는 충전소가 없으면 `-1`.
- **입력**: 첫 줄에 `N M`. 다음 `N`줄에 각 `M`개의 문자(`S`, `C`, `#`, `.`)가 공백 없이 주어진다. `S`는 정확히 1개. (`1 ≤ N, M ≤ 50`)
- **출력**: 최소 이동 횟수, 또는 `-1`.
- **예제**: `4 5 / S..#C / .#.#. / .#... / C#..#` → `3` · `2 3 / S#C / .#.` → `-1`
- **셀프체크**: `S`에서 BFS를 돌리다가 `C`를 **처음 꺼내는 순간**의 거리가 답이다(BFS는 가까운 층부터 꺼내므로 더 볼 필요 없다). 충전소가 0개이거나 벽에 막혀 못 가면 `-1`. 첫 예제에서 `(0,4)`의 충전소는 8칸 떨어져 있고 `(3,0)`의 충전소가 3칸이라 `3`. 격자는 `vector<string>`으로 받으면 `grid[i][j]`가 그대로 문자다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M;
    cin >> N >> M;
    vector<string> grid(N);
    for (int i = 0; i < N; i++) cin >> grid[i];

    int sr = 0, sc = 0;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++)
            if (grid[i][j] == 'S') { sr = i; sc = j; }

    vector<vector<int>> dist(N, vector<int>(M, -1));
    dist[sr][sc] = 0;
    queue<pair<int, int>> q;
    q.push({sr, sc});
    int dr[4] = {-1, 1, 0, 0};
    int dc[4] = {0, 0, -1, 1};

    while (!q.empty()) {
        pair<int, int> cur = q.front();    // front()로 읽고
        q.pop();                           // pop()으로 버린다 (두 줄이 한 세트)
        int r = cur.first, c = cur.second;
        if (grid[r][c] == 'C') {           // 처음 꺼낸 충전소가 가장 가깝다
            cout << dist[r][c] << '\n';
            return 0;
        }
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;
            if (dist[nr][nc] != -1 || grid[nr][nc] == '#') continue;
            dist[nr][nc] = dist[r][c] + 1;
            q.push({nr, nc});
        }
    }
    cout << -1 << '\n';
    return 0;
}
@@TESTS
--IN
4 5
S..#C
.#.#.
.#...
C#..#
--OUT
3
--IN
2 3
S#C
.#.
--OUT
-1
--IN
1 2
SC
--OUT
1
--IN
1 1
S
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- 이동 비용이 전부 1이므로 `S`에서 BFS를 돌리면 각 칸에 "처음 도달한 거리 = 최단거리"가 된다. 목표가 여러 개여도 BFS를 목표마다 따로 돌릴 필요가 없다: 한 번의 BFS에서 가장 먼저 큐에서 꺼내지는 `C`가 곧 가장 가까운 충전소다.
- "꺼낼 때 판정"이 안전하다. 큐에서 나오는 순서는 거리 오름차순이므로 첫 `C`를 만난 순간 종료해도 된다.
- 충전소가 하나도 큐에 들어오지 못하면(벽으로 고립, 또는 존재하지 않음) 큐가 비고 `-1`.

(2) 코드 단계별

- 격자를 `vector<string>`으로 읽으며 `S`의 좌표를 찾는다. `dist`는 `vector<vector<int>> dist(N, vector<int>(M, -1))`로 한 번에 `-1`로 채운다 — 안쪽 `vector<int>(M, -1)`를 빠뜨리고 `vector<vector<int>> dist(N)`이라고 쓰면 행이 전부 **빈 벡터**라 `dist[0][0]`에서 바로 터진다.
- 큐는 `queue<pair<int,int>>`. C++의 `queue::pop()`은 값을 반환하지 않으므로 `front()`로 읽고 `pop()`으로 지우는 두 줄이 항상 짝이다. 이때 `auto& cur = q.front(); q.pop();`처럼 **참조로 받으면 안 된다** — `pop()` 뒤 그 참조는 무효가 되어 정의되지 않은 동작이 된다. 값으로 복사해서 받는다.
- 꺼낸 칸이 `C`면 그 거리를 출력하고 종료. 아니면 4방향 이웃 중 범위 안·미방문·벽이 아닌 칸에 `dist+1`을 기록하고 push한다(`C`도 지나갈 수 있는 칸으로 취급).
- 큐가 다 비면 `-1`.

(3) 스스로 다시 짤 때 생각 순서

- "여러 목표 중 가장 가까운 것" → 시작점 하나에서 BFS 한 번, 첫 목표 도달 시 종료.
- 표준 격자 BFS 뼈대(2차원 `dist` 초기화 → push 시점 표시 → 4방향 확장)를 쓴다.
- 도달 불가(-1)와 시작 칸만 있는 1×1 같은 경계값을 점검한다.
```

**2) K단계 건너 아는 사람** · Easy

- **요구사항**: `N`명의 사람과 `M`개의 친구 관계(양방향)가 있다. 1번 사람을 기준으로 "친구"는 1단계, "친구의 친구(1번 자신·1단계 제외)"는 2단계, … 처럼 가장 짧은 관계 사슬의 길이를 단계라 한다. 정확히 `K`단계인 사람의 수를 출력하라.
- **입력**: 첫 줄에 `N M K`. 다음 `M`줄에 친구인 두 사람 `a b`(1-based). (`1 ≤ N ≤ 1000`, `0 ≤ M ≤ 5000`, `1 ≤ K ≤ N`)
- **출력**: 1번으로부터 정확히 `K`단계인 사람의 수(없으면 `0`).
- **예제**: `7 7 2 / 1 2 / 1 3 / 2 4 / 2 5 / 3 5 / 5 6 / 6 7` → `2` · `4 2 1 / 1 2 / 3 4` → `1`
- **셀프체크**: 단계 = BFS 거리다. "정확히 `K`"이므로 `dist == K`인 정점만 센다(`≤ K` 아님). 5번처럼 두 경로(2를 거쳐, 3을 거쳐)로 닿는 사람은 처음 도달한 거리(2)만 인정된다. 1번과 연결되지 않은 사람(`dist == -1`)은 어떤 단계에도 속하지 않는다. 1-based 번호를 그대로 쓰려면 `vector<vector<int>> adj(N + 1)`처럼 크기를 하나 더 잡는다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M, K;
    cin >> N >> M >> K;
    vector<vector<int>> adj(N + 1);        // 1-based: 크기를 하나 더
    for (int i = 0; i < M; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    vector<int> dist(N + 1, -1);
    dist[1] = 0;
    queue<int> q;
    q.push(1);
    while (!q.empty()) {
        int cur = q.front();
        q.pop();
        for (int nxt : adj[cur]) {
            if (dist[nxt] == -1) {
                dist[nxt] = dist[cur] + 1;
                q.push(nxt);
            }
        }
    }

    int cnt = 0;
    for (int v = 1; v <= N; v++)
        if (dist[v] == K) cnt++;
    cout << cnt << '\n';
    return 0;
}
@@TESTS
--IN
7 7 2
1 2
1 3
2 4
2 5
3 5
5 6
6 7
--OUT
2
--IN
4 2 1
1 2
3 4
--OUT
1
--IN
5 3 4
1 2
2 3
3 4
--OUT
0
--IN
1 0 1
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- "가장 짧은 관계 사슬의 길이"는 간선 비용이 모두 1인 그래프의 최단거리이므로 1번에서 BFS 한 번으로 모든 사람의 단계를 얻는다.
- BFS는 정점을 층(거리) 단위로 방문하므로 `dist` 배열에서 값이 `K`인 정점을 세면 "k번째 층의 정점 수"가 된다.
- 같은 사람에게 여러 경로로 닿아도 push 시점에 방문을 확정하므로 거리는 처음 도달한 값 하나로 고정된다.

(2) 코드 단계별

- 인접리스트는 `vector<vector<int>> adj(N + 1)`. 정점 번호가 1..N이므로 크기를 `N+1`로 잡아야 `adj[N]`이 유효하다. `adj(N)`으로 만들면 마지막 정점에서 범위를 벗어나 조용히 메모리를 망가뜨린다.
- `dist[1] = 0`으로 두고 BFS: 꺼낸 정점의 미방문 이웃에 `dist+1`을 기록하며 push. `queue<int>`이므로 `q.front()`로 읽고 `q.pop()`.
- 1..N을 훑어 `dist[v] == K`인 정점을 센다. 도달 불가(-1)나 다른 층은 제외된다.
- `M = 0`이면 간선 입력 루프가 아예 돌지 않는다(`for (int i = 0; i < 0; i++)`). 별도 처리가 필요 없다.

(3) 스스로 다시 짤 때 생각 순서

- "n단계 관계" → 최단거리 → BFS.
- 1-based 인접리스트 크기(`N+1`)를 먼저 확정하고 표준 그래프 BFS로 `dist`를 채운다.
- 조건이 "정확히"인지 "이하"인지 확인해 마지막 집계 조건을 정한다. 간선이 없는 경우(`0`)도 손으로 돌려 본다.
```

**3) 산불 T분 후 지도** · Medium

- **요구사항**: `N×M` 격자 숲에서 `T`는 나무, `F`는 불타는 칸, `R`은 바위다. 매분 모든 불타는 칸은 상하좌우로 인접한 나무 칸에 불을 옮긴다(그 칸도 불타는 칸이 된다). 바위에는 불이 붙지 않고 불도 통과하지 못한다. 불이 붙은 칸은 계속 타오른다. 정확히 `T`분이 지난 뒤의 지도를 출력하라.
- **입력**: 첫 줄에 `N M T`. 다음 `N`줄에 각 `M`개의 문자(`T`, `F`, `R`)가 공백 없이 주어진다. (`1 ≤ N, M ≤ 50`, `0 ≤ T ≤ 100`)
- **출력**: `N`줄에 걸쳐 `T`분 후의 지도를 같은 형식으로 출력한다.
- **예제**: `3 4 1 / TTTT / TFTR / TTTT` → `TFTT / FFFR / TFTT` · `2 2 5 / FR / RT` → `FR / RT`
- **셀프체크**: 불타는 칸 전부를 시각 0으로 큐에 넣는 다중 시작점 BFS로 각 나무에 불이 닿는 시각을 구한 뒤, 시각이 `T` 이하인 칸만 `F`로 바꾼다. `T=0`이면 입력 그대로. 불이 하나도 없으면 아무 변화가 없다. 바위로 둘러싸인 나무는 영원히 남는다(두 번째 예제). C++의 `string`은 가변이므로 `grid[i][j] = 'F'`로 격자를 제자리에서 고칠 수 있고, 출력도 `cout << grid[i]` 한 줄이면 된다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M, T;
    cin >> N >> M >> T;
    vector<string> grid(N);
    for (int i = 0; i < N; i++) cin >> grid[i];

    vector<vector<int>> burn(N, vector<int>(M, -1));   // 불이 닿는 시각
    queue<pair<int, int>> q;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++)
            if (grid[i][j] == 'F') {                  // 모든 불을 시각 0으로
                burn[i][j] = 0;
                q.push({i, j});
            }

    int dr[4] = {-1, 1, 0, 0};
    int dc[4] = {0, 0, -1, 1};
    while (!q.empty()) {
        pair<int, int> cur = q.front();
        q.pop();
        int r = cur.first, c = cur.second;
        if (burn[r][c] == T) continue;                // T분에 붙은 불은 더 번지지 않는다
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;
            if (grid[nr][nc] != 'T' || burn[nr][nc] != -1) continue;
            burn[nr][nc] = burn[r][c] + 1;
            grid[nr][nc] = 'F';
            q.push({nr, nc});
        }
    }

    for (int i = 0; i < N; i++) cout << grid[i] << '\n';
    return 0;
}
@@TESTS
--IN
3 4 1
TTTT
TFTR
TTTT
--OUT
TFTT
FFFR
TFTT
--IN
2 2 5
FR
RT
--OUT
FR
RT
--IN
3 4 0
TTTT
TFTR
TTTT
--OUT
TTTT
TFTR
TTTT
--IN
3 4 3
TTTT
TFTR
TTTT
--OUT
FFFF
FFFR
FFFF
@@EXPL
(1) 접근·핵심 아이디어

- 불이 여러 군데서 동시에 번지므로 다중 시작점 BFS다. 모든 `F`를 시각 0으로 큐에 넣으면 BFS의 층 하나가 "1분 경과"와 정확히 대응한다.
- "T분 후 상태"는 불이 닿는 시각이 `T` 이하인 나무만 `F`로 바꾸면 된다. 시각 `T`에 붙은 불은 `T+1`분에야 번지므로 그 칸에서는 더 확장하지 않는다(그래야 `T+1` 이후의 변화가 지도에 섞이지 않는다).
- 바위(`R`)는 이동 조건에서 제외되어 자연스럽게 방화벽이 된다.

(2) 코드 단계별

- 격자를 `vector<string>`으로 읽는다. C++의 `string`은 원소를 바꿀 수 있으므로 별도의 문자 배열로 옮기지 않고 `grid[nr][nc] = 'F'`로 바로 고친다.
- 시각 배열 이름을 `time`으로 쓰지 않는다 — `<bits/stdc++.h>` + `using namespace std;` 환경에서는 `time`·`tm`이 표준 이름과 부딪혀 헷갈리는 오류가 난다. 여기서는 `burn`으로 두었다.
- `F` 칸을 모두 시각 0으로 큐에 넣고 BFS. 꺼낸 칸의 시각이 `T`면 확장 중단(`continue`). 아니면 4방향의 미방문 나무 칸에 `burn+1`을 기록하고 `F`로 바꾼 뒤 push.
- 종료 후 `cout << grid[i] << '\n'`으로 줄 단위 출력. `T=0`이면 시작 칸에서 바로 중단되어 입력 그대로 나온다.

(3) 스스로 다시 짤 때 생각 순서

- "동시에 여러 곳에서 번짐 + 몇 분 후" → 다중 시작점 BFS + 시각 기록.
- 확장 중단 조건(`burn == T`)을 어디에 둘지 정한다(꺼낼 때).
- `T=0`, 불 없음, 바위로 고립된 나무를 손으로 검산한다.
```

**4) 화물 리프트 버튼 최소 누름** · Medium

- **요구사항**: 물류 창고의 리프트는 `1`층부터 `F`층까지 움직인다. 버튼은 두 개뿐이다: 위 버튼을 누르면 `U`층 위로, 아래 버튼을 누르면 `D`층 아래로 이동한다. 이동 결과가 `1`층 미만이거나 `F`층 초과이면 리프트는 움직이지 않는다(그 누름은 무의미). 또한 점검 중인 층에는 멈출 수 없으므로 그 층으로 이동하는 누름도 무효다. 현재 `S`층에서 `G`층으로 가기 위한 최소 버튼 누름 횟수를 출력하라. 갈 수 없으면 `-1`.
- **입력**: 첫 줄에 `F S G U D`. 둘째 줄에 점검 중인 층의 수 `K`, 셋째 줄에 `K`개의 층 번호(공백 구분, `K=0`이면 셋째 줄 없음). `S`와 `G`는 점검 중인 층이 아니다. (`1 ≤ F ≤ 100000`, `1 ≤ S, G ≤ F`, `0 ≤ U, D ≤ F`, `0 ≤ K ≤ 100`)
- **출력**: 최소 누름 횟수, 또는 `-1`.
- **예제**: `10 1 8 3 2 / 1 / 7` → `4` · `6 2 5 2 2 / 0` → `-1`
- **셀프체크**: 정점 = 층, 간선 = 두 버튼(각 비용 1)인 1차원 상태 BFS다. 방문 배열은 `vector<int> dist(F + 1, -1)`. 점검 층은 처음부터 "방문 불가"로 표시해 두면 이동 조건이 한 줄로 줄어든다. `S == G`면 `0`. 첫 예제는 `1→4→2→5→8`(7층이 점검 중이라 `1→4→7`이 막힘). `U` 또는 `D`가 0이면 그 버튼은 제자리라 무시된다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int F, S, G, U, D;
    cin >> F >> S >> G >> U >> D;
    int K;
    cin >> K;
    vector<char> closed(F + 1, 0);         // vector<bool> 대신 vector<char>가 다루기 쉽다
    for (int i = 0; i < K; i++) {
        int x;
        cin >> x;
        if (x >= 1 && x <= F) closed[x] = 1;
    }

    vector<int> dist(F + 1, -1);
    dist[S] = 0;
    queue<int> q;
    q.push(S);
    while (!q.empty()) {
        int cur = q.front();
        q.pop();
        if (cur == G) {
            cout << dist[cur] << '\n';
            return 0;
        }
        int cand[2] = {cur + U, cur - D};
        for (int t = 0; t < 2; t++) {
            int nxt = cand[t];
            if (nxt < 1 || nxt > F) continue;
            if (closed[nxt] || dist[nxt] != -1) continue;
            dist[nxt] = dist[cur] + 1;
            q.push(nxt);
        }
    }
    cout << -1 << '\n';
    return 0;
}
@@TESTS
--IN
10 1 8 3 2
1
7
--OUT
4
--IN
6 2 5 2 2
0
--OUT
-1
--IN
5 5 1 1 3
0
--OUT
4
--IN
3 2 2 1 1
0
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 층을 정점, 버튼 한 번을 간선(비용 1)으로 보면 최소 누름 횟수는 BFS 최단거리다. 값(층)이 상태인 1차원 상태 BFS로, 숨바꼭질 문제와 같은 뼈대에 전이만 `+U`, `-D` 두 개다.
- 범위 밖 이동과 점검 층 이동은 "간선이 없는 것"과 같으므로 큐에 넣지 않는다. 점검 층을 미리 `closed`로 표시하면 이동 조건이 `범위 안 && !closed && 미방문`으로 정리된다.
- 두 번째 예제처럼 `U`, `D`가 모두 짝수면 시작 층의 홀짝이 유지되어 홀수 층엔 절대 못 간다 → 큐가 비어 `-1`.

(2) 코드 단계별

- `F S G U D`, `K`, 점검 층을 차례로 읽는다. `K=0`이면 셋째 줄 토큰이 없고 루프도 돌지 않으므로 `cin`은 그대로 다음 입력을 기다리지 않는다.
- 방문·거리 배열 크기는 `F+1`. 층 번호를 인덱스로 쓰므로 0번 칸을 버리고 1..F를 쓴다. 크기를 `F`로 잡으면 `F`층 접근이 범위 밖이다.
- `dist[S] = 0`으로 BFS. 꺼낸 층이 `G`면 즉시 출력(`S == G`면 0). 아니면 두 전이 각각 조건 검사 후 push.
- 전이 값 `cur + U`는 최대 `2F = 200000`이라 `int`로 충분하고, `cur - D`는 음수가 될 수 있으니 **범위 검사를 배열 접근보다 먼저** 해야 한다. `closed[nxt]`를 먼저 쓰면 음수 인덱스로 메모리를 짓밟는다.
- 큐가 비면 `-1`. `U`나 `D`가 0이면 `nxt == cur`라 이미 방문 상태여서 자동으로 무시된다.

(3) 스스로 다시 짤 때 생각 순서

- "조작 최소 횟수" → 상태(값) BFS. 상태 범위(1..F)로 방문 배열 크기를 정한다.
- 전이 목록(+U, −D)과 금지 조건(범위, 점검 층)을 적되, 범위 검사를 배열 접근보다 앞에 둔다.
- 시작=목표, 이동 불가 케이스를 넣어 돌려 본다.
```

**5) 최소로 뚫는 벽의 수** · Medium

- **요구사항**: `N×M` 격자에서 `0`은 빈칸, `1`은 벽이다. `(0,0)`에서 `(N-1,M-1)`까지 상하좌우로 이동하는데, 벽 칸은 뚫고 지나갈 수 있다. 뚫어야 하는 벽 칸 수의 최솟값을 출력하라. 시작 칸과 도착 칸은 항상 빈칸이다.
- **입력**: 첫 줄에 `N M`. 다음 `N`줄에 각 `M`개의 `0/1`이 공백 없이 주어진다. (`1 ≤ N, M ≤ 100`)
- **출력**: 뚫어야 하는 벽의 최소 개수.
- **예제**: `3 4 / 0110 / 0100 / 1100` → `1` · `1 5 / 01110` → `3`
- **셀프체크**: 빈칸으로 이동은 비용 0, 벽으로 이동은 비용 1인 "0-1 가중치" 문제다. 일반 BFS(모두 비용 1)로 풀면 틀리고, `deque`를 써서 비용 0 전이는 `push_front`, 비용 1 전이는 `push_back`으로 넣으면 꺼내는 순서가 비용 오름차순이 된다. 방문 확정이 아니라 "더 작은 비용이면 갱신"으로 처리해야 한다. 벽이 전혀 없으면 `0`, `1×1`이면 `0`.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M;
    cin >> N >> M;
    vector<string> grid(N);
    for (int i = 0; i < N; i++) cin >> grid[i];

    const int INF = 1000000000;
    vector<vector<int>> cost(N, vector<int>(M, INF));
    cost[0][0] = 0;
    deque<pair<int, int>> dq;
    dq.push_back({0, 0});
    int dr[4] = {-1, 1, 0, 0};
    int dc[4] = {0, 0, -1, 1};

    while (!dq.empty()) {
        pair<int, int> cur = dq.front();
        dq.pop_front();
        int r = cur.first, c = cur.second;
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;
            int w = (grid[nr][nc] == '1') ? 1 : 0;
            if (cost[r][c] + w < cost[nr][nc]) {
                cost[nr][nc] = cost[r][c] + w;
                if (w == 0) dq.push_front({nr, nc});   // 비용 0: 앞에
                else dq.push_back({nr, nc});           // 비용 1: 뒤에
            }
        }
    }
    cout << cost[N - 1][M - 1] << '\n';
    return 0;
}
@@TESTS
--IN
3 4
0110
0100
1100
--OUT
1
--IN
1 5
01110
--OUT
3
--IN
2 2
00
00
--OUT
0
--IN
3 3
011
111
110
--OUT
3
@@EXPL
(1) 접근·핵심 아이디어

- 이동 비용이 0(빈칸)과 1(벽) 두 종류뿐이다. 이런 그래프에서는 `deque` 하나로 최단거리를 구할 수 있다(0-1 BFS): 비용 0으로 가는 칸은 지금 칸과 같은 비용이므로 덱 **앞**(`push_front`)에, 비용 1로 가는 칸은 한 층 뒤이므로 덱 **뒤**(`push_back`)에 넣는다. 그러면 꺼내는 순서가 항상 비용 오름차순이 되어 `priority_queue` 없이도 정확하다.
- 일반 BFS처럼 "처음 방문이 최단"이 아니라서, 나중에 더 싼 경로로 도달할 수 있다. 따라서 `cost` 배열을 두고 "더 작아질 때만 갱신·push"한다.
- 첫 예제에서 `(1,1)` 벽 하나만 뚫으면 오른쪽 아래로 이어지고, 다른 길은 벽 두 개 이상이라 답은 `1`.

(2) 코드 단계별

- `cost`를 `vector<vector<int>> cost(N, vector<int>(M, INF))`로 만들고 시작 칸을 0으로 두며 덱에 넣는다.
- 꺼낸 칸의 4방향 이웃에 대해 `w`(벽이면 1, 아니면 0)를 정하고 `cost[r][c] + w`가 더 작으면 갱신. `w == 0`이면 `push_front`, 아니면 `push_back`.
- `INF`를 `INT_MAX`로 두면 `cost[r][c] + w`가 오버플로해 음수가 되고 "더 작다"가 항상 참이 되어 무한 루프에 빠진다. 여기서는 `1e9`로 잡아 `INF + 1`이 `int` 범위 안에 남게 했다 — 0-1 BFS·다익스트라에서 반복되는 표준 예방책이다.
- 덱이 비면 도착 칸의 `cost`를 출력한다(격자는 항상 연결되어 있으므로 INF는 나오지 않는다).

(3) 스스로 다시 짤 때 생각 순서

- "비용이 0 아니면 1" → 0-1 BFS로 분류한다(비용이 여러 값이면 다익스트라).
- 비용 배열 + 갱신 조건 + 덱 앞/뒤 규칙 세 가지를 뼈대로 적고, `INF`는 더해도 안전한 값(`1e9`)으로 둔다.
- 벽이 없는 격자와 벽이 빽빽한 격자로 값이 말이 되는지 검산한다.
```

**6) 열쇠와 잠긴 문** · Medium

- **요구사항**: `N×M` 격자에서 `S`는 시작, `E`는 출구, `K`는 열쇠(정확히 1개 이하), `D`는 잠긴 문(여러 개 가능), `#`은 벽, `.`은 빈칸이다. 상하좌우로 한 칸씩 이동한다. 열쇠 칸을 밟으면 열쇠를 얻고, 열쇠가 있어야만 문 칸으로 들어갈 수 있다(모든 문은 같은 열쇠로 열린다). `S`에서 `E`까지의 최소 이동 횟수를 출력하라. 불가능하면 `-1`.
- **입력**: 첫 줄에 `N M`. 다음 `N`줄에 각 `M`개의 문자가 공백 없이 주어진다. (`1 ≤ N, M ≤ 50`)
- **출력**: 최소 이동 횟수, 또는 `-1`.
- **예제**: `3 5 / S.D.E / K###. / .....` → `6` · `2 4 / S#.E / K.D.` → `5`
- **셀프체크**: 정점을 `(r, c, 열쇠 보유 여부)`로 잡는 상태 BFS. 방문 배열은 `vector<vector<vector<int>>> dist(N, vector<vector<int>>(M, vector<int>(2, -1)))`로 `N×M×2`. 첫 예제는 열쇠를 집으러 `(1,0)`에 갔다가 다시 `(0,0)`으로 돌아오는데, 방문 배열이 2차원이면 `(0,0)`을 이미 방문했다며 되돌아오지 못해 우회로(8칸)만 찾게 된다. 상태를 빼먹으면 프로그램이 죽는 게 아니라 **"덜 간 답"이나 `-1`이 조용히 나온다** — 이게 상태 BFS의 진짜 위험이다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M;
    cin >> N >> M;
    vector<string> grid(N);
    for (int i = 0; i < N; i++) cin >> grid[i];

    int sr = 0, sc = 0;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++)
            if (grid[i][j] == 'S') { sr = i; sc = j; }

    // dist[r][c][k]: k = 열쇠 보유 여부(0/1)
    vector<vector<vector<int>>> dist(N, vector<vector<int>>(M, vector<int>(2, -1)));
    dist[sr][sc][0] = 0;
    queue<array<int, 3>> q;
    q.push({sr, sc, 0});
    int dr[4] = {-1, 1, 0, 0};
    int dc[4] = {0, 0, -1, 1};

    while (!q.empty()) {
        array<int, 3> cur = q.front();
        q.pop();
        int r = cur[0], c = cur[1], k = cur[2];
        if (grid[r][c] == 'E') {
            cout << dist[r][c][k] << '\n';
            return 0;
        }
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;
            char ch = grid[nr][nc];
            if (ch == '#') continue;
            if (ch == 'D' && k == 0) continue;      // 열쇠 없이는 문을 못 연다
            int nk = (ch == 'K') ? 1 : k;           // 열쇠 칸이면 획득
            if (dist[nr][nc][nk] == -1) {
                dist[nr][nc][nk] = dist[r][c][k] + 1;
                q.push({nr, nc, nk});
            }
        }
    }
    cout << -1 << '\n';
    return 0;
}
@@TESTS
--IN
3 5
S.D.E
K###.
.....
--OUT
6
--IN
2 4
S#.E
K.D.
--OUT
5
--IN
2 4
S#.E
..D.
--OUT
-1
--IN
1 3
S.E
--OUT
2
@@EXPL
(1) 접근·핵심 아이디어

- 같은 칸이라도 "열쇠가 있을 때"와 "없을 때"는 갈 수 있는 곳이 다르므로 서로 다른 상태다. 정점을 `(r, c, k)`로 확장하고 방문 배열의 차원을 하나 늘린다. 이동 비용은 전부 1이라 BFS가 최단을 보장한다.
- 전이 규칙: 벽은 항상 불가, 문은 `k == 1`일 때만 가능, 열쇠 칸에 들어가면 `k`가 1이 된다(이미 1이면 그대로). 열쇠는 한 번 얻으면 사라지지 않으므로 `k`는 0→1로만 바뀐다.
- 첫 예제에서 최단 경로는 `S → K → S → (0,1) → D → (0,3) → E`(6번)이며, 2차원 방문 배열로는 `S`를 두 번 밟지 못해 우회로 8번이 나온다.

(2) 코드 단계별

- 3차원 방문 배열은 `vector<vector<vector<int>>> dist(N, vector<vector<int>>(M, vector<int>(2, -1)))`처럼 안쪽부터 채워 만든다. 안쪽 인자를 빠뜨리면 빈 행·빈 칸이 생겨 첫 접근에서 터진다. 크기가 고정이라면 `int dist[50][50][2];` + `memset(dist, -1, sizeof dist)`도 좋다(`memset`의 `-1`은 모든 바이트가 `0xFF`라 `int` `-1`이 정확히 만들어지는 특수한 경우다).
- 큐 원소는 좌표 둘에 상태 하나가 붙으므로 `queue<array<int,3>>`. `pair`를 중첩하는 것보다 `array`나 작은 `struct`가 읽기 쉽다.
- 꺼낸 상태가 `E` 칸이면 그 거리를 출력(BFS라 첫 도달이 최단). 아니면 4방향 이웃을 보며 벽·잠긴 문을 거르고, 다음 열쇠 상태 `nk`를 정한 뒤 미방문이면 기록·push.
- 큐가 비면 `-1`(세 번째 예제처럼 열쇠가 없는데 문이 유일한 길인 경우).

(3) 스스로 다시 짤 때 생각 순서

- "무엇을 가지고 있느냐에 따라 이동 가능 여부가 바뀐다" → 상태에 그 정보를 넣고 `dist`의 차원을 함께 늘린다.
- 전이 규칙을 칸 종류별(`#`, `D`, `K`, 그 외)로 표로 적는다.
- "되돌아오는 경로"가 필요한 예제로 검산한다. 답이 이상하면 먼저 방문 배열 차원을 의심한다.
```

**7) 두 사람의 만남 지점** · Medium

- **요구사항**: `N`개의 역과 `M`개의 양방향 구간(모든 구간의 소요 시간은 1)이 있다. 두 사람이 각각 역 `A`와 역 `B`에서 동시에 출발해 어떤 역 `v`에서 만나려 한다. 두 사람이 모두 도착하는 시각(두 사람의 이동 시간 중 큰 쪽)이 가장 이른 역 `v`를 구하라. 그런 역이 여러 개면 번호가 가장 작은 역을 고른다.
- **입력**: 첫 줄에 `N M A B`. 다음 `M`줄에 `u v`(1-based). (`1 ≤ N ≤ 1000`, `0 ≤ M ≤ 5000`, `1 ≤ A, B ≤ N`)
- **출력**: `역 번호`와 `만나는 시각`을 공백으로 구분해 한 줄에. 두 사람이 모두 갈 수 있는 역이 없으면 `-1`.
- **예제**: `5 4 1 5 / 1 2 / 2 3 / 3 4 / 4 5` → `3 2` · `4 3 1 2 / 1 2 / 1 3 / 2 4` → `1 1`
- **셀프체크**: `A`에서 BFS, `B`에서 BFS로 두 거리 배열을 만든 뒤 모든 역에 대해 `max(dA, dB)`가 최소인 역을 고른다. 둘 중 하나라도 `-1`인 역은 후보가 아니다. 동률 처리는 "번호 오름차순으로 훑으면서 **더 작을 때만** 갱신"으로 자연히 해결된다. `A == B`면 답은 `A 0`. 인접리스트를 함수에 넘길 때는 `const vector<vector<int>>&`로 — 값으로 받으면 호출마다 통째로 복사된다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

vector<int> bfs(int start, int N, const vector<vector<int>>& adj) {   // 참조로 받아 복사 방지
    vector<int> dist(N + 1, -1);
    dist[start] = 0;
    queue<int> q;
    q.push(start);
    while (!q.empty()) {
        int cur = q.front();
        q.pop();
        for (int nxt : adj[cur]) {
            if (dist[nxt] == -1) {
                dist[nxt] = dist[cur] + 1;
                q.push(nxt);
            }
        }
    }
    return dist;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M, A, B;
    cin >> N >> M >> A >> B;
    vector<vector<int>> adj(N + 1);
    for (int i = 0; i < M; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<int> da = bfs(A, N, adj);
    vector<int> db = bfs(B, N, adj);
    int bestV = -1, bestT = -1;
    for (int v = 1; v <= N; v++) {
        if (da[v] == -1 || db[v] == -1) continue;
        int t = max(da[v], db[v]);
        if (bestV == -1 || t < bestT) {   // 동률이면 먼저 본(작은) 번호 유지
            bestV = v;
            bestT = t;
        }
    }
    if (bestV == -1) cout << -1 << '\n';
    else cout << bestV << ' ' << bestT << '\n';
    return 0;
}
@@TESTS
--IN
5 4 1 5
1 2
2 3
3 4
4 5
--OUT
3 2
--IN
4 3 1 2
1 2
1 3
2 4
--OUT
1 1
--IN
6 4 1 6
1 2
2 3
4 5
5 6
--OUT
-1
--IN
3 2 2 2
1 2
2 3
--OUT
2 0
@@EXPL
(1) 접근·핵심 아이디어

- 구간 소요 시간이 모두 1이므로 각 사람의 도착 시각은 BFS 최단거리다. 두 사람이 서로 독립적으로 움직이니 BFS를 두 번(각 출발점에서) 돌려 거리 배열 두 개를 얻고, 역마다 `max(dA, dB)`를 비교하면 된다.
- "둘 다 도착하는 시각 = 큰 쪽"이라는 결합 규칙과 "동률이면 작은 번호"라는 정렬 규칙을 코드로 정확히 옮기는 것이 핵심이다.
- 두 번째 예제에서 역 1(`max(0,1)=1`)과 역 2(`max(1,0)=1`)가 동률이고, 작은 번호 1이 답이다.

(2) 코드 단계별

- 양방향 인접리스트를 만들고, 시작점을 받아 `vector<int> dist`를 반환하는 `bfs` 함수를 정의한다. 인접리스트 매개변수는 **`const vector<vector<int>>&`** — 값으로 받으면 정점 1000개·간선 5000개짜리 구조를 호출할 때마다 복사한다. 반환하는 `dist`는 이동(move)되므로 복사 걱정이 없다.
- `da = bfs(A, ...)`, `db = bfs(B, ...)`를 구한 뒤 역 1..N을 순서대로 보며 둘 다 도달 가능한 역만 후보로 삼는다.
- `t = max(da[v], db[v])`가 현재 최선보다 **작을 때만** 갱신(같으면 유지)하면 작은 번호가 남는다. 후보가 없으면 `-1`.
- 출력은 `cout << bestV << ' ' << bestT << '\n'` — 파이썬 `print(a, b)`가 자동으로 넣던 공백을 직접 써 줘야 한다.

(3) 스스로 다시 짤 때 생각 순서

- "두 출발점" → BFS 두 번, 결과를 정점별로 결합.
- 결합 함수(`max`)와 동률 규칙(작은 번호)을 명시적으로 적는다.
- 도달 불가 역 제외, `A == B` 케이스를 검산한다.
```

**8) 금고 다이얼 최소 회전** · Medium

- **요구사항**: 금고의 다이얼은 세 개의 바퀴로 되어 있고 각 바퀴에는 `0`~`9`가 적혀 있다. 한 번의 회전으로 바퀴 하나를 한 칸 돌릴 수 있으며 `9`에서 한 칸 더 돌리면 `0`, `0`에서 반대로 돌리면 `9`가 된다. 현재 상태에서 목표 상태로 만드는 최소 회전 수를 구하라. 단, 경보가 울리는 금지 조합이 있어 그 상태는 거쳐 갈 수 없다(현재 상태나 목표 상태가 금지 조합이면 불가능).
- **입력**: 첫 줄에 현재 상태와 목표 상태(각각 세 자리 숫자 문자열, 예: `090`). 둘째 줄에 금지 조합의 수 `K`, 셋째 줄에 `K`개의 금지 조합(공백 구분, `K=0`이면 셋째 줄 없음). (`0 ≤ K ≤ 500`)
- **출력**: 최소 회전 수, 불가능하면 `-1`.
- **예제**: `000 002 / 1 / 001` → `4` · `999 000 / 0` → `3`
- **셀프체크**: 상태 수가 1000개뿐이므로 상태를 `string` `"090"` 그대로 두고 `map<string,int>`(또는 `unordered_map`)로 방문·거리를 관리해도 충분하다. 각 상태에서 전이는 바퀴 3개 × 방향 2개 = 6가지. 자릿수 순환은 `(d + 1) % 10`과 `(d + 9) % 10`으로 쓴다 — **C++의 `%`는 음수를 그대로 남기므로 `(d - 1) % 10`은 `d = 0`일 때 `-1`이 되어 `'/'` 같은 엉뚱한 문자를 만든다.** 시작 = 목표면 `0`.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    string start, goal;
    cin >> start >> goal;
    int K;
    cin >> K;
    set<string> banned;
    for (int i = 0; i < K; i++) {
        string s;
        cin >> s;
        banned.insert(s);
    }
    if (banned.count(start) || banned.count(goal)) {
        cout << -1 << '\n';
        return 0;
    }

    map<string, int> dist;
    dist[start] = 0;
    queue<string> q;
    q.push(start);
    while (!q.empty()) {
        string cur = q.front();
        q.pop();
        int cd = dist[cur];
        if (cur == goal) {
            cout << cd << '\n';
            return 0;
        }
        for (int i = 0; i < 3; i++) {
            int d = cur[i] - '0';
            for (int s = 0; s < 2; s++) {
                int nd = (s == 0) ? (d + 1) % 10 : (d + 9) % 10;   // 0에서 내리면 9
                string nxt = cur;
                nxt[i] = char('0' + nd);
                if (dist.count(nxt) || banned.count(nxt)) continue;
                dist[nxt] = cd + 1;
                q.push(nxt);
            }
        }
    }
    cout << -1 << '\n';
    return 0;
}
@@TESTS
--IN
000 002
1
001
--OUT
4
--IN
999 000
0
--OUT
3
--IN
000 555
6
100 900 010 090 001 009
--OUT
-1
--IN
123 123
0
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 정점 = 세 자리 조합(1000개), 간선 = 한 칸 회전(6가지, 비용 1)인 상태 그래프에서의 최단거리이므로 BFS다. 좌표가 아니어도 "상태 + 전이"만 정의되면 BFS 뼈대는 동일하다.
- 금지 조합은 "없는 정점"으로 취급해 큐에 넣지 않으면 된다. 시작이나 목표 자체가 금지면 즉시 `-1`.
- 순환(9↔0)은 `% 10`으로 처리한다. 두 번째 예제는 각 바퀴를 `9→0`으로 한 칸씩 돌리면 3번이지만, 순환을 잊고 `9→8→…→0`으로 세면 27번이 나온다.

(2) 코드 단계별

- 시작·목표를 `string`으로 읽고 금지 조합은 `set<string>`에 담는다. `K=0`이면 루프가 돌지 않는다.
- 거리·방문을 `map<string,int> dist` 하나로 겸한다(`dist.count(nxt)`가 곧 방문 검사). 상태가 1000개뿐이라 `map`의 로그 비용도 문제없다.
- **음수 나머지 함정**: 한 칸 내리는 전이를 `(d - 1) % 10`으로 쓰면 `d = 0`에서 `-1`이 되고, `char('0' + (-1))`은 `'/'`가 되어 다이얼에 없는 문자가 상태에 섞인다. 파이썬의 `%`는 항상 0 이상을 돌려주지만 C++은 피제수의 부호를 따르므로, `(d + 9) % 10`(또는 `(d - 1 + 10) % 10`)으로 미리 양수를 만들어야 한다.
- 문자열 상태를 만들 때는 `string nxt = cur;` 복사 후 `nxt[i]`만 바꾼다. `cur` 자체를 고치면 같은 반복문 안의 나머지 전이가 오염된다.
- 세 번째 예제는 시작의 6개 이웃이 전부 금지라 큐가 바로 비어 `-1`.

(3) 스스로 다시 짤 때 생각 순서

- "조작 최소 횟수 + 상태 수가 작다" → 상태 그대로(문자열) BFS, `map`으로 거리 관리.
- 전이 생성(바퀴 × 방향)과 순환 처리를 함수처럼 따로 생각하고, 나머지 연산에 음수가 들어가지 않게 만든다.
- 금지 상태·시작=목표·완전 고립 케이스로 검산한다.
```

**9) 용암을 피해 탈출** · Hard

- **요구사항**: `N×M` 격자 동굴에서 `S`는 탐험가, `E`는 출구, `L`은 용암(여러 개 가능), `#`은 바위, `.`은 빈 통로다. 매분 다음이 동시에 일어난다: 탐험가는 상하좌우 인접한 칸으로 한 칸 이동하고, 모든 용암은 상하좌우 인접한 빈 통로로 번진다(바위와 출구에는 번지지 않는다). 탐험가는 이동한 순간 용암이 되는 칸(그 분에 용암이 번지는 칸)이나 이미 용암인 칸으로는 이동할 수 없다. 출구에 도착하는 최소 분을 출력하라. 불가능하면 `-1`.
- **입력**: 첫 줄에 `N M`. 다음 `N`줄에 각 `M`개의 문자가 공백 없이 주어진다. `S`, `E`는 각각 1개. (`1 ≤ N, M ≤ 50`)
- **출력**: 출구 도착 최소 분, 또는 `-1`.
- **예제**: `3 4 / S... / .##. / L..E` → `5` · `2 3 / S.E / .L.` → `-1`
- **셀프체크**: 두 단계 BFS다. (1) 모든 용암에서 다중 시작점 BFS로 각 칸에 용암이 닿는 시각 `lava[r][c]`를 구한다(닿지 않으면 `INF`). (2) 탐험가 BFS에서 시각 `t`에 있는 칸에서 이웃으로 갈 때 `lava[nr][nc] > t + 1`일 때만 허용한다(등호가 함정: 같은 분에 용암이 오면 못 간다). 출구는 용암이 못 들어오므로 항상 허용. 첫 예제는 아래쪽 통로가 1분 만에 용암에 막혀 위쪽으로 돌아가야 한다. `INF`는 `1e9`처럼 더해도 넘치지 않는 값으로 둔다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M;
    cin >> N >> M;
    vector<string> grid(N);
    for (int i = 0; i < N; i++) cin >> grid[i];

    const int INF = 1000000000;
    int dr[4] = {-1, 1, 0, 0};
    int dc[4] = {0, 0, -1, 1};

    // 1단계: 용암이 각 칸에 닿는 시각
    vector<vector<int>> lava(N, vector<int>(M, INF));
    queue<pair<int, int>> q;
    int sr = 0, sc = 0;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++) {
            if (grid[i][j] == 'L') { lava[i][j] = 0; q.push({i, j}); }
            else if (grid[i][j] == 'S') { sr = i; sc = j; }
        }
    while (!q.empty()) {
        pair<int, int> cur = q.front();
        q.pop();
        int r = cur.first, c = cur.second;
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;
            if (lava[nr][nc] != INF) continue;
            char ch = grid[nr][nc];
            if (ch != '.' && ch != 'S') continue;      // 바위·출구에는 번지지 않는다
            lava[nr][nc] = lava[r][c] + 1;
            q.push({nr, nc});
        }
    }

    // 2단계: 탐험가 이동 (용암보다 먼저 도착해야 함)
    vector<vector<int>> dist(N, vector<int>(M, -1));
    dist[sr][sc] = 0;
    queue<pair<int, int>> qe;
    qe.push({sr, sc});
    while (!qe.empty()) {
        pair<int, int> cur = qe.front();
        qe.pop();
        int r = cur.first, c = cur.second;
        int t = dist[r][c];
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;
            char ch = grid[nr][nc];
            if (ch == '#' || ch == 'L' || dist[nr][nc] != -1) continue;
            if (ch == 'E') {
                cout << t + 1 << '\n';
                return 0;
            }
            if (lava[nr][nc] > t + 1) {                // 같은 분에 용암이 오면 못 들어간다
                dist[nr][nc] = t + 1;
                qe.push({nr, nc});
            }
        }
    }
    cout << -1 << '\n';
    return 0;
}
@@TESTS
--IN
3 4
S...
.##.
L..E
--OUT
5
--IN
2 3
S.E
.L.
--OUT
-1
--IN
1 3
S.E
--OUT
2
--IN
3 3
S.L
##.
E..
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- 용암의 번짐은 탐험가와 무관하게 정해지므로 먼저 계산해 둘 수 있다. 모든 용암을 시각 0으로 넣는 다중 시작점 BFS로 "각 칸에 용암이 닿는 시각" 표를 만든다(바위·출구는 용암이 못 들어가므로 제외).
- 그다음 탐험가 BFS에서는 이웃 칸으로 갈 때 "내가 `t+1`분에 도착하는데 용암은 그보다 늦게(`lava > t+1`) 오는가"만 검사한다. 이렇게 두 BFS를 분리하면 두 물체가 동시에 움직이는 복잡한 시뮬레이션이 조건 하나로 줄어든다.
- 등호가 함정이다: `lava == t+1`이면 같은 분에 용암이 번지므로 들어갈 수 없다(두 번째 예제는 `(0,1)`, `(1,0)` 모두 1분에 용암이라 탐험가가 갇힌다).

(2) 코드 단계별

- 1단계 BFS: `L`을 전부 시각 0으로 큐에 넣고 빈 통로(`.`, `S`)로만 번지며 `lava`를 채운다. 출구 `E`와 바위는 `INF`로 남는다. `INF`를 `INT_MAX`로 두면 뒤에서 `lava > t + 1` 비교는 괜찮아도, 같은 뼈대를 조금만 고쳐 `lava + 1`을 쓰는 순간 오버플로해 음수가 된다 — 처음부터 `1e9`로 잡아 두는 편이 안전하다.
- 큐 두 개를 따로 만든다(`q`, `qe`). 하나를 재사용하려면 1단계가 끝난 뒤 반드시 비어 있는지 확인해야 하는데, C++의 `queue`에는 `clear()`가 없어 `q = queue<pair<int,int>>();`처럼 통째로 갈아 끼워야 한다.
- 2단계 BFS: `S`에서 시작. 이웃이 바위·용암 원점·방문 완료면 건너뛰고, `E`면 `t+1`을 출력하고 종료. 그 외 통로는 `lava[nr][nc] > t+1`일 때만 기록·push.
- 큐가 비면 `-1`. 네 번째 예제는 `(1,2)`가 1분에 용암이 되어 출구 쪽 길이 끊긴다.

(3) 스스로 다시 짤 때 생각 순서

- "장애물이 시간에 따라 번진다" → 번짐 시각표를 먼저 만들고(다중 시작점 BFS), 이동 BFS는 그 표만 참조한다.
- 두 BFS의 이동 가능 칸 정의를 각각 적는다(용암: 빈 통로만 / 탐험가: 바위·용암 제외, 출구 항상 허용).
- 부등호(초과 vs 이상)를 예제로 확인하고, 용암이 없는 경우도 돌려 본다.
```

**10) 최단 경로의 개수** · Hard

- **요구사항**: `N×M` 격자에서 `.`은 길, `#`은 벽이다. `(0,0)`에서 `(N-1,M-1)`까지 상하좌우로 이동하는 최단 경로의 길이(이동 횟수)와, 그 길이를 갖는 서로 다른 최단 경로의 개수를 출력하라. 시작·도착 칸은 항상 길이다.
- **입력**: 첫 줄에 `N M`. 다음 `N`줄에 각 `M`개의 `.`/`#`이 공백 없이 주어진다. (`1 ≤ N, M ≤ 30`)
- **출력**: `최단 길이`와 `최단 경로의 개수`를 공백으로 구분해 한 줄에. 도달 불가면 `-1`.
- **예제**: `3 3 / ... / ... / ...` → `4 6` · `3 3 / ... / .#. / ...` → `4 2`
- **셀프체크**: BFS로 `dist`를 채우면서 경로 수 `cnt`도 함께 누적한다. 이웃을 **처음** 방문하면 `cnt[nxt] = cnt[cur]`, 이미 방문됐지만 `dist[nxt] == dist[cur] + 1`이면(같은 최단 층에서 또 도달) `cnt[nxt] += cnt[cur]`. 이미 더 짧은 거리로 방문된 칸에는 더하지 않는다. `1×1` 격자는 `0 1`. **경로 수는 `int`를 넘긴다** — 30×30 빈 격자의 최단 경로 수는 `C(58,29) ≈ 3.0×10¹⁶`이므로 `cnt`는 반드시 `long long`이어야 한다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M;
    cin >> N >> M;
    vector<string> grid(N);
    for (int i = 0; i < N; i++) cin >> grid[i];

    vector<vector<int>> dist(N, vector<int>(M, -1));
    vector<vector<long long>> cnt(N, vector<long long>(M, 0));   // int로는 넘친다
    dist[0][0] = 0;
    cnt[0][0] = 1;
    queue<pair<int, int>> q;
    q.push({0, 0});
    int dr[4] = {-1, 1, 0, 0};
    int dc[4] = {0, 0, -1, 1};

    while (!q.empty()) {
        pair<int, int> cur = q.front();
        q.pop();
        int r = cur.first, c = cur.second;
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;
            if (grid[nr][nc] == '#') continue;
            if (dist[nr][nc] == -1) {                  // 처음 도달: 거리 확정, 경로 수 복사
                dist[nr][nc] = dist[r][c] + 1;
                cnt[nr][nc] = cnt[r][c];
                q.push({nr, nc});
            } else if (dist[nr][nc] == dist[r][c] + 1) {   // 같은 최단 층: 경로 수 합산
                cnt[nr][nc] += cnt[r][c];
            }
        }
    }

    if (dist[N - 1][M - 1] == -1) cout << -1 << '\n';
    else cout << dist[N - 1][M - 1] << ' ' << cnt[N - 1][M - 1] << '\n';
    return 0;
}
@@TESTS
--IN
3 3
...
...
...
--OUT
4 6
--IN
3 3
...
.#.
...
--OUT
4 2
--IN
2 2
.#
#.
--OUT
-1
--IN
1 1
.
--OUT
0 1
@@EXPL
(1) 접근·핵심 아이디어

- BFS는 정점을 거리 층 단위로 처리하므로, 어떤 칸의 최단 경로 수는 "그 칸보다 거리가 정확히 1 작은 이웃들의 최단 경로 수의 합"이다. BFS로 거리를 확정해 가면서 그 합을 동시에 누적하면 별도의 DP 없이 개수까지 얻는다.
- 핵심 규칙 두 가지: (a) 처음 방문할 때 `cnt`를 복사, (b) 이미 방문된 이웃이라도 거리가 `dist[cur]+1`과 같으면 `cnt`를 더한다. 거리가 더 작은 이웃(이미 지나온 층)에 더하면 안 된다.
- 층 순서로 처리되기 때문에 `cnt[cur]`가 확정된 뒤에만 이웃에 더해지는 것이 보장된다(더 먼 칸이 먼저 큐에서 나올 일이 없다).

(2) 코드 단계별

- `dist`는 `-1`, `cnt`는 `0`으로 초기화하고 시작 칸을 `dist 0`, `cnt 1`로 둔다.
- **경로 수 배열의 타입이 이 문제의 진짜 함정이다.** 30×30 빈 격자의 최단 경로 수는 오른쪽 29번·아래 29번을 섞는 가짓수 `C(58,29) ≈ 3.0×10¹⁶`이다. `int`(약 21억)로 두면 조용히 음수가 되거나 엉뚱한 값이 나오고, 컴파일 경고조차 없다. `vector<vector<long long>> cnt`으로 잡으면 `long long`의 상한 약 `9.2×10¹⁸` 안에 넉넉히 들어간다. 파이썬은 정수가 무한 자릿수라 이 함정이 아예 없다는 점이 C++로 옮길 때 가장 흔히 놓치는 부분이다.
- 꺼낸 칸의 4방향 이웃 중 벽이 아닌 칸에 대해: 미방문이면 거리·경로 수를 기록하고 push, 방문됐지만 거리가 한 층 아래면 경로 수만 합산.
- 도착 칸이 미방문이면 `-1`, 아니면 `dist`와 `cnt`를 공백으로 구분해 출력한다. 3×3 빈 격자에서 4번 이동 경로가 6개(`C(4,2)`)인지로 검산한다.

(3) 스스로 다시 짤 때 생각 순서

- "최단 길이 + 그 개수" → BFS 거리 층을 이용한 누적 계산.
- 갱신 규칙 두 가지(처음/같은 층)를 먼저 적고, "더 짧은 층에는 더하지 않음"을 명시한다.
- 개수를 담는 변수의 최대 크기를 손으로 어림해 `int`인지 `long long`인지부터 정한다.
```

**11) 얼음판 미끄러지기** · Hard

- **요구사항**: `N×M` 격자 얼음판에서 `.`은 얼음, `#`은 바위, `S`는 시작, `G`는 목표다. 한 번 밀면 상하좌우 중 한 방향으로 바위나 격자 경계에 부딪히기 직전까지 계속 미끄러진다(중간에 멈출 수 없다). 정확히 `G` 위에 멈춰야 도착한 것으로 본다(미끄러지며 지나치기만 하면 도착이 아니다). 최소 몇 번 밀어야 하는지 출력하라. 불가능하면 `-1`.
- **입력**: 첫 줄에 `N M`. 다음 `N`줄에 각 `M`개의 문자가 공백 없이 주어진다. (`1 ≤ N, M ≤ 50`)
- **출력**: 최소 밀기 횟수, 또는 `-1`.
- **예제**: `4 5 / S..#. / .#... / ..... / ..G..` → `2` · `1 4 / S.G.` → `-1`
- **셀프체크**: 정점은 "멈출 수 있는 칸", 간선은 "한 방향으로 끝까지 미끄러진 결과"다. 이웃 칸이 아니라 미끄러진 **도착 칸**을 큐에 넣는다. 한 칸도 못 움직이는 방향(바로 앞이 바위/경계)은 전이가 없다. 첫 예제는 오른쪽으로 밀면 `(0,3)`의 바위 앞 `(0,2)`에 멈추고, 아래로 밀면 경계까지 내려가 `(3,2)`의 `G`에 정확히 멈춘다. 두 번째 예제는 `G`를 지나쳐 끝까지 미끄러지므로 불가능.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M;
    cin >> N >> M;
    vector<string> grid(N);
    for (int i = 0; i < N; i++) cin >> grid[i];

    int sr = 0, sc = 0;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++)
            if (grid[i][j] == 'S') { sr = i; sc = j; }

    vector<vector<int>> dist(N, vector<int>(M, -1));
    dist[sr][sc] = 0;
    queue<pair<int, int>> q;
    q.push({sr, sc});
    int dr[4] = {-1, 1, 0, 0};
    int dc[4] = {0, 0, -1, 1};

    while (!q.empty()) {
        pair<int, int> cur = q.front();
        q.pop();
        int r = cur.first, c = cur.second;
        if (grid[r][c] == 'G') {
            cout << dist[r][c] << '\n';
            return 0;
        }
        for (int d = 0; d < 4; d++) {
            int nr = r, nc = c;
            while (true) {                     // 바위나 경계 직전까지 미끄러진다
                int tr = nr + dr[d], tc = nc + dc[d];
                if (tr < 0 || tr >= N || tc < 0 || tc >= M) break;
                if (grid[tr][tc] == '#') break;
                nr = tr;
                nc = tc;
            }
            if (nr == r && nc == c) continue;  // 한 칸도 못 움직임
            if (dist[nr][nc] == -1) {
                dist[nr][nc] = dist[r][c] + 1;
                q.push({nr, nc});
            }
        }
    }
    cout << -1 << '\n';
    return 0;
}
@@TESTS
--IN
4 5
S..#.
.#...
.....
..G..
--OUT
2
--IN
1 4
S.G.
--OUT
-1
--IN
1 3
S.G
--OUT
1
--IN
2 2
S#
#G
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- 이동 규칙이 "한 칸"이 아니라 "멈출 때까지"라는 점만 다를 뿐, 정점(멈춘 칸)과 간선(밀기 한 번, 비용 1)이 정의되므로 BFS로 최소 횟수를 구한다. 간선을 만들 때 미끄러짐을 `while` 루프로 시뮬레이션해 도착 칸을 얻는 것이 핵심이다.
- "지나치기만 하면 도착이 아니다"라는 조건은 자연스럽게 처리된다: 멈춘 칸만 정점이 되므로 `G`를 스쳐 지나가는 경우는 `G`가 큐에 들어가지 않는다.
- 미끄러짐 루프는 "다음 칸이 범위 안이고 바위가 아닌 동안 전진"으로 쓰면 경계·바위를 한 조건으로 처리한다.

(2) 코드 단계별

- `S`를 찾아 `dist`를 초기화하고 큐에 넣는다.
- 꺼낸 칸이 `G`면 거리 출력. 아니면 4방향 각각에 대해 `while`로 끝까지 밀어 `(nr, nc)`를 구한다. 제자리면 건너뛰고, 미방문이면 거리 기록·push.
- 미끄러짐 루프에서 다음 칸 좌표를 `tr`, `tc`로 따로 계산해 **검사한 뒤에** `nr`, `nc`에 반영한다. `nr += dr[d]`를 먼저 하고 나서 범위를 검사하면 이미 격자 밖 인덱스로 `grid[nr][nc]`를 읽은 뒤다 — 파이썬 리스트라면 `IndexError`가 나거나 음수 인덱스로 반대편을 읽지만, C++의 `vector`·`string`은 `[]`에 범위 검사가 없어 **아무 경고 없이 남의 메모리를 읽는다.**
- 좌표 변수는 `int`로 둔다. `grid[i].size()`가 돌려주는 `size_t`(부호 없는 정수)와 섞어 `nc < grid[r].size() - 1` 같은 비교를 쓰면, 크기가 0일 때 `0 - 1`이 거대한 양수가 되어 조건이 뒤집힌다.
- 큐가 비면 `-1`. 네 번째 예제는 시작에서 어느 방향도 못 움직여 바로 `-1`.

(3) 스스로 다시 짤 때 생각 순서

- "한 번의 조작이 여러 칸을 움직인다" → 조작 결과 칸을 이웃으로 삼는 BFS.
- 미끄러짐 시뮬레이션(전진 조건: 범위 안·바위 아님)을 "검사 후 이동" 순서로 정확히 짠다.
- 지나침/제자리/고립 케이스를 예제로 검산한다.
```

**12) 최소 굴곡 배관** · Hard

- **요구사항**: `N×M` 격자에서 `.`은 배관을 놓을 수 있는 칸, `#`은 놓을 수 없는 칸이다. 칸 `(r1, c1)`에서 `(r2, c2)`까지 상하좌우로 이어지는 배관을 놓을 때, 방향이 바뀌는 지점(굴곡)의 최소 개수를 출력하라. 첫 구간의 방향은 자유롭게 고를 수 있으며 굴곡으로 세지 않는다. 두 칸이 같으면 `0`. 불가능하면 `-1`.
- **입력**: 첫 줄에 `N M`. 다음 `N`줄에 격자. 마지막 줄에 `r1 c1 r2 c2`(0-based, 두 칸 모두 `.`). (`1 ≤ N, M ≤ 50`)
- **출력**: 최소 굴곡 수, 또는 `-1`.
- **예제**: `3 3 / .#. / .#. / ... / 0 0 0 2` → `2` · `3 4 / .... / .##. / .... / 0 0 2 3` → `1`
- **셀프체크**: 정점을 `(r, c, 진행 방향)`으로 잡으면, 같은 방향으로 한 칸 더 가는 전이는 비용 0, 방향을 바꾸는 전이는 비용 1이다 → 0-1 BFS. 시작 칸은 4방향 모두 비용 0으로 덱에 넣는다. 비용 배열은 `vector<vector<vector<int>>> cost(N, vector<vector<int>>(M, vector<int>(4, INF)))`이며 "더 작은 비용이면 갱신" 규칙을 쓴다. 답은 도착 칸의 4방향 비용 중 최솟값. 첫 예제는 아래→오른쪽→위로 두 번 꺾어야 한다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, M;
    cin >> N >> M;
    vector<string> grid(N);
    for (int i = 0; i < N; i++) cin >> grid[i];
    int r1, c1, r2, c2;
    cin >> r1 >> c1 >> r2 >> c2;
    if (r1 == r2 && c1 == c2) {
        cout << 0 << '\n';
        return 0;
    }

    const int INF = 1000000000;
    int dr[4] = {-1, 1, 0, 0};
    int dc[4] = {0, 0, -1, 1};
    vector<vector<vector<int>>> cost(N, vector<vector<int>>(M, vector<int>(4, INF)));
    deque<array<int, 3>> dq;
    for (int d = 0; d < 4; d++) {          // 첫 방향은 자유: 4방향 모두 비용 0
        cost[r1][c1][d] = 0;
        dq.push_back({r1, c1, d});
    }

    while (!dq.empty()) {
        array<int, 3> st = dq.front();
        dq.pop_front();
        int r = st[0], c = st[1], d = st[2];
        int cur = cost[r][c][d];
        for (int nd = 0; nd < 4; nd++) {
            int nr = r + dr[nd], nc = c + dc[nd];
            if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;
            if (grid[nr][nc] == '#') continue;
            int w = (nd == d) ? 0 : 1;     // 같은 방향 0, 꺾으면 1
            if (cur + w < cost[nr][nc][nd]) {
                cost[nr][nc][nd] = cur + w;
                if (w == 0) dq.push_front({nr, nc, nd});
                else dq.push_back({nr, nc, nd});
            }
        }
    }

    int ans = INF;
    for (int d = 0; d < 4; d++) ans = min(ans, cost[r2][c2][d]);
    cout << (ans == INF ? -1 : ans) << '\n';
    return 0;
}
@@TESTS
--IN
3 3
.#.
.#.
...
0 0 0 2
--OUT
2
--IN
3 4
....
.##.
....
0 0 2 3
--OUT
1
--IN
2 2
.#
#.
0 0 1 1
--OUT
-1
--IN
1 4
....
0 3 0 3
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 굴곡 수는 "방향이 바뀐 횟수"이므로 지금 어느 방향으로 가고 있는지가 상태에 있어야 한다. 정점을 `(r, c, d)`로 확장하면, 같은 방향으로 전진(비용 0)과 방향 전환(비용 1) 두 종류의 간선만 남는다.
- 비용이 0/1뿐이므로 0-1 BFS: 비용 0 전이는 덱 앞(`push_front`), 비용 1 전이는 덱 뒤(`push_back`)에 넣어 꺼내는 순서를 비용 오름차순으로 유지한다. "더 작아질 때만 갱신"하는 비용 배열이 방문 배열을 겸한다.
- 첫 방향에 제약이 없으므로 시작 칸을 4방향 상태 모두 비용 0으로 넣는다. 도착 칸은 어느 방향으로 들어와도 되므로 4개 비용의 최솟값이 답이다.

(2) 코드 단계별

- 격자와 두 좌표를 읽고, 같은 칸이면 `0`을 출력하고 끝낸다.
- `cost[r][c][d]`는 3차원 `vector`로 `INF` 초기화. 안쪽부터 `vector<int>(4, INF)` → `vector<vector<int>>(M, …)` → `vector<vector<vector<int>>>(N, …)` 순으로 감싼다. 고정 크기라면 `int cost[50][50][4];`도 좋다.
- 큐 원소는 좌표 + 방향 세 값이므로 `deque<array<int,3>>`. 꺼낼 때는 `dq.front()`를 **값으로 복사**한 뒤 `pop_front()` — 참조로 잡아 두면 `pop_front()` 순간 무효가 되어 정의되지 않은 동작이다.
- 꺼낸 상태에서 4방향 `nd`로 한 칸 이동을 시도: 범위 밖·막힌 칸은 제외, `w = (nd == d) ? 0 : 1`. 더 싸지면 갱신하고 `w`에 따라 앞/뒤에 push.
- 도착 칸 네 방향의 최소 비용을 출력(`INF`면 `-1`). 두 번째 예제는 오른쪽으로 쭉 간 뒤 한 번 꺾어 내려가면 된다.

(3) 스스로 다시 짤 때 생각 순서

- "꺾는 횟수 최소" → 방향을 상태에 넣고, 직진 0·전환 1의 0-1 BFS로 분류한다.
- 시작 상태 4개, 도착 상태 4개(최솟값)라는 양 끝 처리를 먼저 정한다.
- 같은 칸·도달 불가·일직선 케이스로 검산한다.
```
