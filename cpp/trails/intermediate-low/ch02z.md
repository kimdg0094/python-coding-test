## L6. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

백트래킹은 "모든 경우를 만든다"가 아니라 **"부분 선택을 하나 늘렸다가, 돌아올 때 원래대로
되돌린다"**는 한 문장이다. 이 챕터의 네 유형은 전부 같은 재귀 골격 위에 있고, 다른 것은
단 두 가지 — **후보를 어떻게 나열하는가**와 **어떤 상태를 되돌려야 하는가**뿐이다.
C++에서는 여기에 언어 고유의 결정이 하나 더 붙는다. **무엇을 값으로 넘기고 무엇을
참조·전역으로 공유할 것인가**다. 값으로 넘긴 것은 프레임이 사라질 때 저절로 원복되므로
되돌리기 코드가 필요 없고, 공유한 것은 직접 되돌려야 한다. 이 구분을 처음에 못 박아
두면 "복원 누락" 부류의 버그가 통째로 사라진다.

**개념 지도**

```text
                     rec(depth, state)
                     |  base : depth == N  -> record answer
                     |  loop : for each candidate
                     |    choose -> rec(depth+1) -> undo
                     v
   +-----------------+------------------+------------------+
   |                 |                  |                  |
  L1 repeated       L2 + pruning       L3 combination     L4 permutation
  for c in 0..K-1   same loop, but     for i in           for i in 0..N-1
  no restriction    if (bad) continue  start .. N-1       if (used[i]) skip
  K^N cases         cuts K^(N-d) at    rec(i+1, cnt+1)    used[i]=true..false
                    one stroke         C(N,M) cases       P(N,M) cases
```

가장 왼쪽 L1이 뼈대이고, 오른쪽으로 갈수록 "무엇을 금지하는가"가 하나씩 붙는다.
L2는 값에 조건을 걸고, L3은 인덱스에 순서를 강제하고, L4는 사용 여부를 기억한다.

```text
 which template?
   same value may repeat, order matters   -> L1  K^N
   ... plus a rule that forbids some picks -> L2  prune before recursing
   order does NOT matter, no repeats       -> L3  start index, C(N,M)
   order matters, no repeats               -> L4  used[], P(N,M)
   pick or skip each element               -> subset, 2^N
```

되돌리기가 필요한지 아닌지는 "그 상태를 누가 들고 있는가"로 갈린다. 이 표 한 장이
복원 누락 버그의 절반을 막는다.

```text
 who owns the state ?           undo needed ?

   value parameter              no   : the frame dies, the value is gone
     rec(depth, cur_sum, prev)         cur_sum is restored for free

   shared array / global        YES  : you changed something everyone sees
     used[i] = true;                   used[i] = false;  right after the call
     chosen.push_back(x);              chosen.pop_back();

   index overwrite              no   : the next loop iteration overwrites it
     picked[depth] = c;                nothing to undo

   reference parameter          YES  : same as shared
     rec(depth, vector<int>& path)     you must pop what you pushed
```

**뼈대 코드**

(1) 중복 순열 — K개 중 하나를 N번 (L1)

```cpp
#include <bits/stdc++.h>
using namespace std;

int K = 3, N = 2;
vector<int> picked;
vector<vector<int>> res;

void rec(int depth) {
    if (depth == N) {
        res.push_back(picked);         // vector 는 값 복사라 그대로 담아도 안전
        return;                        // return 을 빠뜨리면 아래로 흘러 내려간다
    }
    for (int c = 0; c < K; c++) {      // <- 문제마다 바뀜(후보 집합)
        picked[depth] = c;
        rec(depth + 1);
        // 인덱스 덮어쓰기 방식이라 별도 복원이 필요 없다
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    picked.assign(N, 0);
    rec(0);
    return 0;
}
```

(2) 조합 nCr — 순서 없이 M개 (L3)

```cpp
int arr[] = {1, 2, 3, 4};
int N = 4, M = 2;
vector<int> chosen;
vector<vector<int>> res;

void rec(int start, int cnt) {
    if (cnt == M) {
        res.push_back(chosen);
        return;
    }
    if (N - start < M - cnt) return;    // 개수 가지치기: 남은 원소로 못 채움
    for (int i = start; i < N; i++) {   // start 부터 -> 인덱스 증가만 허용
        chosen.push_back(arr[i]);
        rec(i + 1, cnt + 1);            // i+1: 자기 다음 원소부터
        chosen.pop_back();              // 복원
    }
}
```

(3) 순열 — 방문 배열로 사용한 원소를 기억 (L4)

```cpp
const int MAXN = 20;
int arr[MAXN], perm[MAXN];
bool used[MAXN];                        // 전역 bool 배열은 false 로 시작한다
int N = 3, M = 3;

void rec(int depth) {
    if (depth == M) {
        for (int i = 0; i < M; i++) cout << perm[i] << (i + 1 == M ? '\n' : ' ');
        return;
    }
    for (int i = 0; i < N; i++) {
        if (used[i]) continue;
        used[i] = true;                 // 켜기
        perm[depth] = arr[i];
        rec(depth + 1);
        used[i] = false;                // 되돌리기(핵심)
    }
}
```

전체 순열만 필요하면 표준 `next_permutation`이 더 짧다. 단 **오름차순 정렬 후**
`do { ... } while (next_permutation(arr, arr + N));` 형태여야 첫 순열도 빠지지 않는다.

(4) 부분집합 — 각 원소를 고르거나 건너뛰거나

```cpp
int arr[] = {1, 2, 3};
int N = 3;
vector<int> cur;
vector<vector<int>> res;

void rec(int idx) {
    if (idx == N) {
        res.push_back(cur);             // 2^N 개
        return;
    }
    rec(idx + 1);                       // idx번째를 건너뛴다
    cur.push_back(arr[idx]);            // idx번째를 고른다
    rec(idx + 1);
    cur.pop_back();                     // 복원
}

// N 이 20 남짓 이하면 비트마스크가 더 짧고 빠르다
void rec_bitmask() {
    for (int mask = 0; mask < (1 << N); mask++) {
        // int cnt = __builtin_popcount(mask);   // 고른 개수
        for (int i = 0; i < N; i++)
            if (mask & (1 << i)) { /* arr[i] 를 고른 경우 */ }
    }
    // N 이 31 을 넘으면 1LL << i 로 써야 오버플로가 안 난다
}
```

(5) 격자 경로 탐색 — 방문 표시를 켜고 되돌리는 위치가 핵심

```cpp
const int DR[4] = {-1, 1, 0, 0};
const int DC[4] = {0, 0, -1, 1};

int R, C, LIMIT;
vector<vector<int>> g;
vector<vector<char>> visited;          // vector<bool> 대신 char: 참조를 얻을 수 있다

void dfs(int r, int c, int depth) {
    if (depth == LIMIT) {              // <- 문제마다 바뀜(길이/목적지/조건)
        // record(r, c);
        return;
    }
    for (int d = 0; d < 4; d++) {
        int nr = r + DR[d], nc = c + DC[d];
        if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
        if (visited[nr][nc]) continue;
        if (g[nr][nc] == -1) continue;          // <- 문제마다 바뀜(통과 조건)
        visited[nr][nc] = 1;                    // 내려가기 직전에 켠다
        dfs(nr, nc, depth + 1);
        visited[nr][nc] = 0;                    // 올라오면서 끈다
    }
}
```

시작 칸은 재귀 진입 전에 `visited[sr][sc] = 1`로 켜 두어야 한다. 루프 안에서만
켜면 출발점이 표시되지 않아 자기 자리로 되돌아가는 경로가 생긴다. 격자 `g`와 `visited`를
매개변수로 넘기지 않고 전역으로 둔 것에도 이유가 있다 — 재귀 프레임에 컨테이너 복사본이
얹히면 프레임이 커져 깊은 재귀에서 스택이 먼저 바닥난다.

(6) 가지치기(bound)를 넣는 자리 — 최적화 문제의 표준 위치

```cpp
long long best = LLONG_MAX / 2;        // 더해도 넘치지 않게 여유를 둔다

void rec(int depth, long long cur_cost, long long cur_sum) {
    if (cur_cost >= best) return;              // (a) 진입 즉시: 이미 최선보다 나쁨
    if (depth == N) {
        best = min(best, cur_cost);
        return;
    }
    if (cur_sum + remain_max(depth) < TARGET)  // (b) 남은 걸 다 써도 목표 미달
        return;
    for (int c : candidates(depth)) {          // <- 문제마다 바뀜
        if (!ok(c, depth)) continue;           // (c) 후보 단위 필터
        rec(depth + 1, cur_cost + cost(c), cur_sum + c);
    }
}
```

`(a)`는 경로 단위 컷, `(c)`는 후보 단위 필터다. 둘 다 **재귀로 내려가기 전**에 있어야
이득이 있다. 종료 조건 뒤에 두면 이미 그 가지를 다 만든 뒤라 아무것도 아끼지 못한다.
`best`의 초깃값을 `INT_MAX`로 두고 거기에 무언가를 더하면 오버플로로 음수가 되어
가지치기가 정반대로 동작한다. 누적값이 커질 수 있으면 처음부터 `long long`이다.

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 같은 값을 여러 번 골라도 되고 순서가 다르면 다른 경우 | 중복 순열 틀 (L1) | 제약이 없어 각 칸이 독립적으로 K갈래 | O(K^N) |
| "직전과 같으면 안 된다 / 합이 S 이하" 같은 단서가 붙음 | 가지치기 틀 (L2) | 위반 가지를 진입 전에 잘라낸다 | 최악 O(K^N), 실측은 훨씬 적음 |
| "N개 중 M개를 뽑는다", 순서 무관 | 조합 틀 `start` (L3) | 인덱스 증가만 허용해 중복 대표를 제거 | O(C(N,M)·M) |
| "각 원소를 넣거나 뺀다", 부분집합 전체 | 이분 재귀 (pick/skip) | 원소마다 두 갈래가 곧 2^N | O(2^N·N) |
| 원소가 20개 이하이고 부분집합을 전부 봐야 함 | 비트마스크 루프 + `__builtin_popcount` | 재귀 없이 정수 하나가 집합을 표현 | O(2^N·N) |
| "줄을 세운다 / 방문 순서 / 이어붙인 수" | 순열 틀 `used[]` (L4) | 순서가 결과를 바꾸고 재사용은 금지 | O(P(N,M)·M) |
| 전체 순열을 사전순으로 그냥 훑기만 하면 됨 | `sort` 후 `next_permutation` | 표준 함수 한 줄, 상태 관리 불필요 | O(N!·N) |
| 격자 위를 이동하며 경로를 만든다 | DFS + `visited` 켜고 끄기 | 같은 칸을 한 경로에서 두 번 밟지 않게 | O(4^L) |
| 최소/최대를 찾는 최적화 | bound 가지치기 추가 | 이미 최선보다 나쁜 가지는 볼 필요가 없다 | 최악은 같지만 실측 급감 |
| 조건 판정에 매번 배열을 다시 훑고 있음 | 상태를 값 인자로 들고 다니기 | 판정이 O(N)에서 O(1)로, 복원도 불필요 | 상수배 개선 |
| 되돌려야 할 상태가 배열·벡터임 | 전역 또는 참조로 공유 + 짝맞춘 복원 | 값 전달은 호출마다 전체 복사 | 복사 비용 0 |
| 재귀 깊이가 수만을 넘을 위험 | `std::stack` 반복 구현 | OS 스택은 보통 1~8MB뿐 | 힙을 쓰므로 한계 없음 |
| N ≥ 20이고 상태가 "어떤 것들을 썼는가"뿐 | 비트마스크 + 메모이제이션 | 같은 집합이 여러 순서로 반복 계산됨 | O(2^N·N) |
| 나열이 아니라 개수만 필요 | 점화식/DP로 전환 | 경우를 만들 필요 자체가 없다 | 문제마다 다름 |
| 중복 원소가 있는데 같은 결과를 한 번만 | 정렬 후 "앞 형제 미사용이면 skip" | 같은 값의 형제 중 하나만 대표로 | 중복 제거된 개수 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 백트래킹의 세 단계(선택 → 재귀 → 되돌리기)가 각각 무엇을 하는지, 그리고 왜 세 번째가 이름값인지.
- [ ] 설명할 수 있다: `depth`가 "지금까지 몇 칸을 채웠는가"라는 뜻이고, 종료 조건이 왜 `depth == N`인지.
- [ ] 설명할 수 있다: 중복 순열의 경우의 수가 K^N인 이유를 곱의 법칙으로.
- [ ] 설명할 수 있다: 백트래킹의 시간복잡도를 "가지 수^깊이 × 한 경우 처리 비용"으로 어림하는 방법.
- [ ] 설명할 수 있다: 깊이 d에서 가지 하나를 자르면 정확히 몇 개의 잎이 사라지는지.
- [ ] 설명할 수 있다: 가지치기가 최악 복잡도는 못 낮추는데도 실전에서 통과를 만드는 이유.
- [ ] 설명할 수 있다: 조합에서 `start`를 넘기면 왜 `{1,3}`과 `{3,1}`의 중복이 사라지는지.
- [ ] 설명할 수 있다: 조합의 다음 재귀가 `rec(i+1)`이어야 하고 `rec(start+1)`이면 안 되는 이유.
- [ ] 설명할 수 있다: 순열이 `start` 대신 `used[]`를 쓰는 이유, 즉 "인덱스 순서 제약"과 "재사용 금지"의 차이.
- [ ] 설명할 수 있다: `used[i] = false`를 빠뜨리면 결과 개수가 어떻게 줄어드는지 작은 예로.
- [ ] 설명할 수 있다: 어떤 상태가 되돌리기를 필요로 하고 어떤 상태가 필요 없는지를 "값 전달 / 공유"로 갈라 설명.
- [ ] 설명할 수 있다: `res.push_back(picked)`가 C++에서는 왜 안전한지, 그리고 포인터나 참조를 담으면 어떻게 똑같이 망가지는지.
- [ ] 설명할 수 있다: 재귀 함수에 큰 컨테이너를 값으로 넘기면 시간과 스택 양쪽에서 무슨 일이 벌어지는지.
- [ ] 설명할 수 있다: 인덱스 덮어쓰기 방식(`picked[depth] = c`)에서는 왜 명시적 복원이 필요 없는지.
- [ ] 설명할 수 있다: 격자 DFS에서 `visited`를 켜고 끄는 위치가 BFS의 방문 표시와 어떻게 다른지.
- [ ] 설명할 수 있다: 지역 배열과 전역 배열의 초기값 차이, 그리고 `memset`으로 채울 수 있는 값이 왜 0과 -1뿐인지.
- [ ] 설명할 수 있다: N!과 2^N과 C(N,M)이 각각 N이 얼마쯤에서 감당 못 할 크기가 되는지, 그리고 어느 지점부터 `long long`이 필요한지.
- [ ] 설명할 수 있다: C++ 재귀 깊이의 한계가 어디서 오는지(OS 스택 크기)와, 그것이 예외가 아니라 강제 종료로 나타나는 이유.

**⚠️ 자주 하는 실수**

(1) 정답 목록에 포인터나 참조를 담아 나중에 전부 같아진다

```cpp
// ❌ 틀린 코드
vector<int*> res;
void rec(int depth) {
    if (depth == N) {
        res.push_back(picked);      // 배열의 주소를 담는다(배열은 포인터로 붕괴)
        return;
    }
    ...
}
// 끝나고 보면 res 안의 모든 포인터가 같은 배열을 가리킨다
```

왜: `picked`는 재귀 내내 하나뿐인 배열이다. 주소를 담으면 `res`의 모든 항목이 같은
메모리를 가리키고, 이후 재귀가 그 배열을 계속 덮어쓴다. 지역 배열의 주소였다면 함수가
끝난 뒤 그 메모리는 유효하지도 않다.

```cpp
// ✅ 고친 코드
vector<vector<int>> res;
res.push_back(vector<int>(picked, picked + N));   // 그 시점의 복사본을 담는다
// picked 가 vector 라면 res.push_back(picked) 만으로 충분하다.
// C++ 의 vector 는 대입·전달이 기본이 깊은 복사라, 파이썬의 path[:] 같은
// 복사 관용구가 아예 필요 없다. 대신 복사 비용은 실제로 든다.
```

(2) 되돌리기 누락 — `used[i] = false`를 안 쓴다

```cpp
// ❌ 틀린 코드
for (int i = 0; i < N; i++) {
    if (used[i]) continue;
    used[i] = true;
    perm[depth] = arr[i];
    rec(depth + 1);
    // used[i] = false 가 없다
}
```

왜: `used`는 "이 경로에서 썼는가"라는 경로 지역 정보인데, 끄지 않으면 전역 정보가
된다. N=3이면 `1 2 3` 하나만 나오고 나머지 5개 순열은 후보가 모두 소진돼 사라진다.

```cpp
// ✅ 고친 코드
for (int i = 0; i < N; i++) {
    if (used[i]) continue;
    used[i] = true;
    perm[depth] = arr[i];
    rec(depth + 1);
    used[i] = false;            // 위로 올라오면서 반드시 되돌린다
}
```

(3) 조합에서 `rec(start + 1)`로 내려간다

```cpp
// ❌ 틀린 코드
for (int i = start; i < N; i++) {
    chosen.push_back(arr[i]);
    rec(start + 1, cnt + 1);    // i 가 아니라 start
    chosen.pop_back();
}
```

왜: 다음 단계의 시작 위치가 `i`와 무관해져 같은 원소를 다시 고를 수 있고, 오름차순
보장이 깨져 `{1,3}`과 `{3,1}`이 둘 다 나온다.

```cpp
// ✅ 고친 코드
for (int i = start; i < N; i++) {
    chosen.push_back(arr[i]);
    rec(i + 1, cnt + 1);        // 방금 고른 i 의 '다음'부터
    chosen.pop_back();
}
```

(4) `pop_back()` 복원 누락 — 경로가 계속 길어진다

```cpp
// ❌ 틀린 코드
for (int i = start; i < N; i++) {
    chosen.push_back(arr[i]);
    if (!ok(arr[i])) continue;      // 여기서 빠져나가면 복원이 건너뛰어진다
    rec(i + 1, cnt + 1);
    // chosen.pop_back() 없음
}
```

왜: 형제 가지로 넘어갈 때 앞 가지에서 넣은 원소가 그대로 남아 `cnt`와 `chosen.size()`가
어긋난다. 결과 길이가 M을 넘거나 범위 밖 접근이 난다. 조기 `continue`가 `push_back`
뒤에 있으면 복원을 통째로 건너뛰므로 더 나쁘다.

```cpp
// ✅ 고친 코드
for (int i = start; i < N; i++) {
    if (!ok(arr[i])) continue;      // 조기 continue 는 push_back 앞에
    chosen.push_back(arr[i]);
    rec(i + 1, cnt + 1);
    chosen.pop_back();              // push_back 과 짝을 맞춘다
}
```

(5) 가지치기를 종료 조건 뒤에 둔다

```cpp
// ❌ 틀린 코드
void rec(int depth, int cur_sum) {
    if (depth == N) {
        if (cur_sum == S) cnt++;
        return;
    }
    for (int c = 1; c <= K; c++) {
        rec(depth + 1, cur_sum + c);
        if (cur_sum > S) return;    // 다 내려갔다 온 뒤에 검사
    }
}
```

왜: 이미 그 가지의 모든 잎을 다 만든 뒤에 자르는 것이라 아낀 게 없다. 가지치기의 이득은
"깊이 d에서 자르면 K^(N-d)개가 한 번에 사라진다"에서 온다.

```cpp
// ✅ 고친 코드
void rec(int depth, int cur_sum) {
    if (cur_sum > S) return;        // 함수 진입 즉시 컷
    if (depth == N) {
        if (cur_sum == S) cnt++;
        return;
    }
    for (int c = 1; c <= K; c++)
        rec(depth + 1, cur_sum + c);
}
```

(6) 격자 DFS에서 방문 표시를 되돌리는 위치가 틀렸다

```cpp
// ❌ 틀린 코드
void dfs(int r, int c, int depth) {
    visited[r][c] = 1;
    if (depth == LIMIT) {
        record();
        return;                     // 켜 놓은 채로 빠져나간다
    }
    for (int d = 0; d < 4; d++) { /* ... */ dfs(nr, nc, depth + 1); }
    visited[r][c] = 0;
}
```

왜: 종료 지점의 `return`이 `visited[r][c] = 0`을 건너뛴다. 그 칸이 켜진 채로 남아
이후의 모든 경로가 그 칸을 피하고, 답이 실제보다 적게 나온다.

```cpp
// ✅ 고친 코드
void dfs(int r, int c, int depth) {
    if (depth == LIMIT) {
        record();
        return;                     // 여기서는 아직 켜지 않았다
    }
    for (int d = 0; d < 4; d++) {
        // ... 경계·조건 검사 ...
        visited[nr][nc] = 1;        // 켜기와 끄기를 재귀 호출 양옆에 짝으로
        dfs(nr, nc, depth + 1);
        visited[nr][nc] = 0;
    }
}
```

(7) 종료 조건에서 `return`을 빠뜨린다

```cpp
// ❌ 틀린 코드
void rec(int depth) {
    if (depth == N) {
        res.push_back(picked);      // return 이 없다
    }
    for (int c = 0; c < K; c++) {
        picked[depth] = c;          // depth == N 이면 범위 밖 쓰기
        rec(depth + 1);
    }
}
```

왜: 기저 조건에서 멈추지 않으면 `depth`가 N을 넘어 계속 내려간다. 파이썬이라면
`IndexError`로 즉시 멈추지만, C++의 `vector::operator[]`는 범위를 검사하지 않아 남의
메모리를 조용히 덮어쓴다. 크래시가 나면 다행이고, 안 나면 원인을 찾기가 훨씬 어렵다.

```cpp
// ✅ 고친 코드
void rec(int depth) {
    if (depth == N) {
        res.push_back(picked);
        return;                     // 반드시 멈춘다
    }
    for (int c = 0; c < K; c++) {
        picked[depth] = c;
        rec(depth + 1);
    }
}
```

(8) 재귀 함수에 컨테이너를 값으로 넘긴다

```cpp
// ❌ 틀린 코드
void rec(int depth, vector<int> path, vector<vector<int>> g) {
    if (depth == N) { record(path); return; }
    for (int c = 0; c < K; c++) {
        path.push_back(c);          // 이 프레임의 복사본에만 들어간다
        rec(depth + 1, path, g);    // 호출마다 path 와 g 를 통째로 복사
        path.pop_back();
    }
}
```

왜: 두 가지가 동시에 망가진다. (1) 호출마다 벡터 전체가 복사되어 `K^N`번의 호출에
`K^N`번의 복사가 붙는다. 격자 `g`까지 값으로 받으면 호출 하나에 R×C개 원소가 복사된다.
(2) 프레임에 벡터 복사본이 얹혀 프레임이 커지므로, 깊이가 수천만 되어도 스택이 바닥난다.

```cpp
// ✅ 고친 코드
vector<vector<int>> g;              // 공유 상태는 전역이나 참조로
void rec(int depth, vector<int>& path) {
    if (depth == N) { record(path); return; }
    for (int c = 0; c < K; c++) {
        path.push_back(c);
        rec(depth + 1, path);       // 주소만 넘어간다
        path.pop_back();            // 공유하므로 되돌리기는 내가 책임진다
    }
}
// 되돌릴 필요 없는 작은 스칼라(cur_sum, prev, depth)는 값으로 넘기는 편이 낫다.
// 프레임이 사라지면 저절로 원복되어 복원 코드 자체가 필요 없다.
```

(9) 지역 배열을 초기화하지 않는다

```cpp
// ❌ 틀린 코드
void solve() {
    bool used[20];                  // 지역 배열: 쓰레기 값으로 시작
    int  cnt[20];
    memset(cnt, 1, sizeof(cnt));    // 1 로 채운 줄 알지만 0x01010101 이 된다
    rec(0);                         // used 가 처음부터 true 인 칸이 있을 수 있다
}
```

왜: 지역 배열은 0으로 초기화되지 않는다(전역·`static`이라야 0이다). `used`가 무작위로
켜진 채 시작하면 결과가 실행할 때마다 달라진다. 그리고 `memset`은 바이트 단위로 채우는
함수라 0과 -1(`0xFF`) 외의 값은 의도대로 들어가지 않는다.

```cpp
// ✅ 고친 코드
void solve() {
    bool used[20] = {};                       // 전부 false
    int  cnt[20];
    memset(cnt, 0, sizeof(cnt));              // 0 은 안전
    fill(cnt, cnt + 20, 1);                   // 임의의 값은 fill 로
    vector<bool> used2(20, false);            // 크기가 가변이면 벡터 생성자로
    rec(0);
}
```

(10) 카운터를 값으로 받아 갱신이 밖으로 안 나간다 / `int`로 세다 넘친다

```cpp
// ❌ 틀린 코드
void rec(int depth, int answer) {
    if (depth == N) { answer++; return; }     // 이 프레임의 복사본만 증가
    for (int c = 0; c < K; c++) rec(depth + 1, answer);
}
int answer = 0;
rec(0, answer);
cout << answer << "\n";                       // 언제나 0
```

왜: 값 전달이라 함수 안의 `answer`는 호출한 쪽과 다른 변수다. 아무리 올려도 밖은
그대로다. 게다가 `K^N`은 K=2, N=31이면 이미 21억을 넘어 `int`로는 세지도 못한다.

```cpp
// ✅ 고친 코드
long long answer = 0;                         // 경우의 수는 금방 int 를 넘는다
void rec(int depth, long long& answer) {      // 참조로 받아 밖에 반영한다
    if (depth == N) { answer++; return; }
    for (int c = 0; c < K; c++) rec(depth + 1, answer);
}
// 전역 카운터를 쓰는 것도 같은 효과다: long long answer; 를 전역에 두고 answer++
```

(11) 재귀 깊이가 스택을 넘긴다

```cpp
// ❌ 틀린 코드
int chain(int x) {
    if (x == 0) return 0;
    return 1 + chain(x - 1);
}
cout << chain(1000000) << "\n";    // 예외가 아니라 프로그램이 그냥 죽는다
```

왜: C++ 재귀는 OS가 준 스택(보통 1MB~8MB)에 프레임을 쌓는다. 프레임 하나가 48바이트만
되어도 깊이 100만이면 48MB라 한참 모자란다. 파이썬처럼 `RecursionError`가 뜨는 게 아니라
스택 오버플로로 강제 종료되어, 디버깅 단서가 거의 남지 않는다.

```cpp
// ✅ 고친 코드
int chain_iter(int x) {
    int cnt = 0;
    while (x > 0) { cnt++; x--; }      // 꼬리재귀는 루프로 바꾼다
    return cnt;
}
// 그래프·격자 탐색이라면 std::stack 에 상태를 쌓는 반복 DFS 로 바꾼다.
// 스택 자료구조는 힙을 쓰므로 OS 스택 한계와 무관하다.
```

**다음 챕터로**

이 챕터의 "선택 → 재귀 → 되돌리기"는 그대로 격자 위 경로 탐색(DFS)과 이어진다.
다만 DFS에서는 `visited`를 되돌리지 **않는** 것이 기본이라는 차이를 눈여겨보라 —
"모든 경로를 만든다"와 "모든 칸을 한 번씩 본다"의 목적 차이가 그 한 줄에 담긴다.
또 가지치기에서 "이미 계산한 상태를 또 계산하고 있다"는 낭비가 보이기 시작하면,
그 다음 단계가 메모이제이션과 동적 계획법이다. 순열 전수 나열이 막히는 지점
(N이 10을 넘는 순간)이 곧 비트마스크 DP로 넘어가라는 신호다.
