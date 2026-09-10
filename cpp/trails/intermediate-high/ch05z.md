## L6. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터의 네 도구는 전부 같은 질문에 대한 서로 다른 대답이다. **"지금까지 무엇을 썼는지"를 기억하려면 상태가 `2^n`으로 폭발한다 — 그것을 어떻게 줄일 것인가.** 정렬로 단조성을 얻어 기억할 필요를 없애면 Bitonic, 답이 경계 하나에서 갈라지면 구간 DP, 집합을 끝내 기억해야 하면 비트마스크, 집합이 아니라 합만 중요하면 값 DP다. 그래서 유형 선택의 첫 단서는 언제나 **입력 크기**다.

**개념 지도**

```text
  Ch05 map : shrink the state until the table fits

  a DP whose naive state is "which ones did I already use ?"
   |
   +-- sorting gives monotonicity      ->  Bitonic
   |     x-sorted, both chains only move right
   |     the visited set is forced to be {0..j} -> two ends suffice
   |     dp[i][j] , O(n^2) instead of O(2^n)
   |
   +-- the answer splits at a boundary ->  interval DP
   |     dp[i][j] = best over k of dp[i][k] + dp[k+1][j] + cost(i,j)
   |     fill by span length, shortest first , O(n^3)
   |
   +-- the set itself must be kept     ->  bitmask
   |     element i is in the set  <->  bit i is 1
   |     one integer = one subset , 2^n of them
   |     |
   |     +-- order does not matter   dp[mask]       O(2^n * n)
   |     +-- "where am I now"        dp[mask][u]    O(2^n * n^2)
   |     +-- split into two groups   subset walk    O(3^n)
   |
   +-- only the total value matters    ->  DP over values
         dp[w] = can we reach sum w , O(n * S) , fine even at n = 1e5
```

지문보다 먼저 **제한**을 읽는다. n의 상한이 유형을 거의 다 정해 준다.

```text
  read the bound on n first, then pick the shape   (C++ budget ~1e8/s)

  n <= 16     2^n * n^2   bitmask DP with a position    ~1.7e7
  n <= 18     3^n         every subset of every mask    ~3.9e8  tight
  n <= 20     2^n * n     one pass over all subsets     ~2.1e7
  n <= 20     2^n * n * 8 bytes for a long long table   ~168MB  memory !
  n <= 500    n^3         interval DP                   ~1.2e8
  n <= 1000   n^3         interval DP, too slow in C++  ~1.0e9
  n <= 5000   n^2         two-way LIS by plain DP       ~2.5e7
  n <= 1e5    n log n     two-way LIS by lower_bound    ~1.7e6
  S <= 1e5    n * S       subset sum over values
  # n = 1e5 with a "choose a subset" story is never bitmask
  # n = 15 with a vague statement is almost always bitmask
```

네 유형이 공유하는 진짜 뼈대는 점화식이 아니라 **채우는 순서**다.

```text
  every DP here fills cells in an order where the sources are done

  bitonic     frontier j ascending    dp[i][j] reads dp[*][j-1]
  interval    span length ascending   dp[i][j] reads shorter spans only
  bitmask     mask value ascending    dp[m | b] is written from dp[m]
  subset sum  weight descending       keeps each item usable only once
  # break the order and you read a cell that still holds its init value
```

C++에서는 여기에 **연산자 우선순위**라는 함정이 하나 더 붙는다. 파이썬과 정반대라 옮길 때 반드시 확인해야 한다.

```text
  binding strength , strongest at the top

  C++                          Python
  ---------------------        ---------------------
  ~  !                         ~
  <<  >>                       <<  >>
  <  >  <=  >=                 &                  <- & is STRONG here
  ==  !=                       ^
  &                  <- weak   |
  ^                            ==  !=  <  >       <- comparison is WEAK
  |                            not / and / or
  &&  ||

  m & 1 == 0     in C++    ->  m & (1 == 0)  ->  m & 0  ->  always 0
  m & 1 == 0     in Python ->  (m & 1) == 0  ->  works as intended
  1 << n - 1     in BOTH   ->  1 << (n - 1)  ->  NOT (1 << n) - 1
  # rule : always parenthesize a bit test and a shift
```

**뼈대 코드**

1) 비트 연산 관용구 모음 — 집합 하나가 정수 하나

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, mask, other, i;

// --- 원소 하나를 다루는 연산 (괄호는 선택이 아니라 필수다) ---
bool has  = ((mask >> i) & 1) == 1;     // 원소 i 포함 여부
int  add  = mask | (1 << i);            // 원소 i 추가
int  del  = mask & ~(1 << i);           // 원소 i 제거
int  flip = mask ^ (1 << i);            // 원소 i 토글

// --- 최하위 비트 ---
int dropLow = mask & (mask - 1);        // 최하위 1비트 하나 끄기
int low     = mask & (-mask);           // 최하위 1비트만 남기기
int idx     = __builtin_ctz(low);       // 그 비트가 가리키는 원소 번호(0-based)
// __builtin_ctz(0) 은 정의되지 않는다 — mask != 0 을 먼저 확인할 것

// --- 집합 전체 ---
int  bits  = __builtin_popcount(mask);  // 켜진 비트 수. 64비트는 popcountll
int  FULL  = (1 << n) - 1;              // 전체 집합 (괄호 필수)
int  rest  = FULL ^ mask;               // 여집합
bool disjoint = ((mask & other) == 0);  // 서로소인가 — 괄호 필수
bool superset = ((mask & other) == other);   // mask 가 other 를 포함하는가

// --- 64비트가 필요할 때 ---
long long big = 1LL << 40;              // 1 << 40 은 int 연산이라 이미 망가진다
// n >= 31 이면 1 << n 은 부호 있는 오버플로(UB), n >= 32 는 시프트 자체가 UB

// --- 모든 마스크 순회 : 끝값은 1 << n 이다 ---
for (int m = 0; m < (1 << n); m++) {
    // 마스크마다 할 일은 문제마다 바뀜
}

// --- mask 의 모든 부분집합을 한 번씩 (빈 집합 포함) ---
for (int sub = mask; ; sub = (sub - 1) & mask) {
    // sub 를 쓰는 자리
    if (sub == 0) break;                // 사용 -> 검사 -> 갱신 순서
}

// --- 진부분집합만 (자기 자신 제외) ---
for (int sub = (mask - 1) & mask; sub; sub = (sub - 1) & mask) {
    // ...
}
```

2) 비트마스크 DP — TSP형 `dp[mask][u]`와 배정형 `dp[mask]`

```cpp
const long long INF = LLONG_MAX / 4;             // 더해도 넘치지 않을 여유
int FULL = (1 << n) - 1;

// (A) TSP: dp[mask][u] = mask 를 방문했고 지금 u 에 있을 때의 최소 비용
vector<vector<long long>> dp(1 << n, vector<long long>(n, INF));
dp[1][0] = 0;                                    // 이 한 줄이 빠지면 전부 INF
for (int mask = 0; mask < (1 << n); mask++) {    // 오름차순이 그대로 위상 순서
    for (int u = 0; u < n; u++) {
        long long cur = dp[mask][u];
        if (cur >= INF) continue;                // 도달 못 한 상태는 밀지 않는다
        if (((mask >> u) & 1) == 0) continue;    // u 에 있을 수 없는 상태
        for (int v = 0; v < n; v++) {
            if (((mask >> v) & 1) == 1) continue;   // 이미 방문한 곳으로는 안 간다
            int nm = mask | (1 << v);
            if (cur + dist[u][v] < dp[nm][v]) dp[nm][v] = cur + dist[u][v];
        }
    }
}
long long ans = INF;
for (int u = 1; u < n; u++)                      // 복귀가 없으면 dp[FULL] 의 최솟값
    ans = min(ans, dp[FULL][u] + dist[u][0]);

// (B) 배정형: '지금 몇 번째 사람 차례인가'가 popcount 로 정해져 1차원이면 충분
vector<long long> f(1 << n, INF);
f[0] = 0;
for (int mask = 0; mask < (1 << n); mask++) {
    if (f[mask] >= INF) continue;
    int i = __builtin_popcount(mask);            // 이미 배정된 수 = 지금 배정할 사람
    if (i == n) continue;
    for (int j = 0; j < n; j++) {
        if (((mask >> j) & 1) == 1) continue;
        int nm = mask | (1 << j);
        if (f[mask] + cost[i][j] < f[nm]) f[nm] = f[mask] + cost[i][j];
    }
}
long long ans2 = f[FULL];
```

3) 구간 DP — 바깥 루프는 반드시 구간 길이

```cpp
vector<long long> pre(n + 1, 0);
for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + a[i];      // 구간 합을 O(1)로

vector<vector<long long>> dp(n, vector<long long>(n, 0));    // 길이 1 구간은 0
for (int length = 2; length <= n; length++) {                // 짧은 구간부터
    for (int i = 0; i + length - 1 < n; i++) {
        int j = i + length - 1;
        long long cost = pre[j + 1] - pre[i];                // 비용은 문제마다 바뀜
        long long best = LLONG_MAX / 4;
        for (int k = i; k < j; k++) {                        // 마지막에 합쳐질 경계
            long long v = dp[i][k] + dp[k + 1][j];           // 둘 다 이미 완성됨
            if (v < best) best = v;
        }
        dp[i][j] = best + cost;
    }
}
long long ans = dp[0][n - 1];

// 변형: 분할점 없이 '양끝만 비교'하는 형태(회문 계열)는 안쪽 칸 하나만 읽는다
for (int length = 2; length <= n; length++) {
    for (int i = 0; i + length - 1 < n; i++) {
        int j = i + length - 1;
        if (s[i] == s[j]) dp[i][j] = dp[i + 1][j - 1];       // 양끝이 같으면 그대로
        else              dp[i][j] = min(dp[i + 1][j], dp[i][j - 1]) + 1;
    }
}
```

4) Bitonic — 양방향 LIS를 따로 채워 꼭대기에서 붙인다

```cpp
vector<int> inc(n, 1);                           // i에서 '끝나는' 증가 최대 길이
for (int i = 0; i < n; i++)
    for (int j = 0; j < i; j++)                  // 왼쪽 -> 오른쪽
        if (a[j] < a[i] && inc[j] + 1 > inc[i]) inc[i] = inc[j] + 1;

vector<int> dec(n, 1);                           // i에서 '시작하는' 감소 최대 길이
for (int i = n - 1; i >= 0; i--)                 // 반드시 오른쪽 끝부터
    for (int j = i + 1; j < n; j++)
        if (a[j] < a[i] && dec[j] + 1 > dec[i]) dec[i] = dec[j] + 1;

int ans = 0;
for (int i = 0; i < n; i++)
    ans = max(ans, inc[i] + dec[i] - 1);         // 꼭대기가 두 번 세어지므로 -1
// 길이가 아니라 '합'을 최대화하는 문제면 초기값을 a[i]로 두고 마지막에 - a[i]
// 양쪽이 모두 비어 있으면 안 되는 문제면 inc[i] > 1 && dec[i] > 1 조건을 추가
```

5) 부분집합 합 — 마스크별 합과 값 기반 DP

```cpp
// (A) 모든 마스크의 원소 합을 O(2^n)에. 마스크마다 다시 더하면 O(2^n * n)이 된다
vector<long long> ssum(1 << n, 0);
for (int mask = 1; mask < (1 << n); mask++) {
    int low = mask & (-mask);                    // 최하위 원소 하나를 떼어내고
    ssum[mask] = ssum[mask ^ low] + a[__builtin_ctz(low)];   // 나머지는 이미 계산됨
}

// (B) n이 커도 값의 합이 작으면 '집합'이 아니라 '값'을 상태로 잡는다
int S = accumulate(a.begin(), a.end(), 0);
vector<char> can(S + 1, 0);                      // can[w] = 합이 정확히 w인가
can[0] = 1;
for (int x : a)                                  // 원소를 한 번씩만 쓰려면
    for (int w = S; w >= x; w--)                 // 반드시 내림차순
        if (can[w - x]) can[w] = 1;
int best = INT_MAX;
for (int w = 0; w <= S; w++)
    if (can[w]) best = min(best, abs(S - 2 * w));   // 목적식은 문제마다 바뀜
// vector<bool> 은 비트 압축이라 메모리는 작지만 접근이 느리다 — 여기선 vector<char>
```

**언제 무엇을 쓰나**

먼저 **n의 상한에서 유형을 역추론**한다. 지문을 다 읽기 전에 제한부터 본다.

| n(또는 상태 원소 수)의 상한 | 허용되는 복잡도 | 거의 확정인 유형 | 근거 계산 |
| --- | --- | --- | --- |
| n ≤ 12 | 최대 `n!` | 완전탐색·순열 백트래킹 | `12! ≈ 4.8e8` |
| n ≤ 16 | `2^n × n^2` | **비트마스크 DP + 현재 위치**(TSP형) | `6.6e4 × 256 ≈ 1.7e7` |
| n ≤ 18 | `3^n` | **모든 마스크의 모든 부분집합**(그룹 분할) | `3^18 ≈ 3.9e8`, 빠듯 |
| n ≤ 20 | `2^n × n` | **비트마스크 DP 1차원**(배정형) | `1.0e6 × 20 ≈ 2.1e7` |
| n ≤ 22 | `2^n` | 마스크별 값 한 번씩(부분집합 합 전처리) | `4.2e6`, 메모리 34MB |
| n ≤ 300 | `n^3` | **구간 DP**(분할점 있음) | `2.7e7` |
| n ≤ 500 | `n^3` | 구간 DP, C++이라 아직 통과 | `1.2e8` |
| n ≤ 2,000 | `n^2` | Bitonic `dp[i][j]`, 구간 DP(분할점 없음) | `4.0e6` |
| n ≤ 5,000 | `n^2` | 양방향 LIS를 이중 루프로 | `2.5e7` |
| n ≤ 100,000 | `n log n` | 양방향 LIS를 `lower_bound`로 | `1.7e6` |
| n ≤ 100,000 + 합 S ≤ 1e5 | `n × S` | **값 DP**(집합이 아니라 값이 상태) | `1e10`? → S를 다시 확인 |
| n이 20을 훌쩍 넘는데 "부분집합" | — | 비트마스크가 **아니다**. 정렬·그리디·값 DP를 다시 본다 | `2^n`이 불가 |

유형을 좁혔으면 아래에서 상태 정의를 확정한다.

| 지문 신호 | 상태 정의 | 복잡도 | n 상한 |
| --- | --- | --- | --- |
| "왼쪽 끝에서 오른쪽 끝까지 갔다가 되돌아온다", 좌표로 정렬하면 단조 | `dp[i][j]` = 두 체인의 끝점이 i, j | O(n²) | n ≤ 2,000 |
| "증가하다가 감소하는" 산 모양 부분수열 | `inc[i]`, `dec[i]` 두 배열을 따로 | O(n²) | n ≤ 5,000 |
| 같은 산 모양인데 n이 10만 | `inc`, `dec`를 `lower_bound` LIS로 | O(n log n) | n ≤ 10⁵ |
| "인접한 두 더미를 합친다", "괄호를 어디에 치나" | `dp[i][j]` = 구간을 하나로 만드는 최적값 | O(n³) | n ≤ 300~500 |
| "양끝을 동시에 본다"(회문 삽입·분할) | `dp[i][j]`, 분할점 없이 안쪽 한 칸 | O(n²) | n ≤ 3,000 |
| "마지막에 터뜨리는/제거하는 것 하나를 고른다" | `dp[i][j]` + 분할점 k | O(n³) | n ≤ 300 |
| "N개를 켜고 끄는 모든 경우를 본다" | 마스크 정수 하나 | O(2ⁿ × n) | n ≤ 20~22 |
| "모든 도시를 한 번씩, 어디서 왔는지가 비용을 바꾼다" | `dp[mask][u]` | O(2ⁿ × n²) | n ≤ 16 |
| "사람 i를 자리 j에 배정", 순서는 비용과 무관 | `dp[mask]`, 사람 번호 = `__builtin_popcount(mask)` | O(2ⁿ × n) | n ≤ 20 |
| "집합을 그룹 k개로 쪼갠다" | `dp[mask]` + 부분집합 순회 | O(3ⁿ) | n ≤ 18 |
| 마스크마다 원소 합·유효성이 필요 | `ssum[mask] = ssum[mask^low] + a[ctz(low)]` | O(2ⁿ) | n ≤ 22 |
| "부분집합의 합이 목표에 닿나", n은 큰데 값이 작다 | `can[w]` — 집합이 아니라 값이 상태 | O(n × S) | n ≤ 10⁵ |
| 격자 위 "지점 k곳을 다 들르는 최단 이동" | BFS 거리표 + `dp[mask][i]` | O(격자 + 2ᵏ × k²) | k ≤ 12 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: n의 상한만 보고 비트마스크·구간 DP·양방향 LIS 중 무엇인지 좁히는 근거를.
- [ ] 설명할 수 있다: 비트마스크의 한계가 왜 대략 `n ≤ 20`인지를 `2ⁿ × n` 계산과 **메모리** 양쪽으로.
- [ ] 설명할 수 있다: 구간 DP가 왜 `n ≤ 300~500`에서 막히는지를 `n³` 계산으로.
- [ ] 설명할 수 있다: 왜 구간 DP의 바깥 루프가 반드시 "구간 길이"여야 하는지.
- [ ] 설명할 수 있다: 구간 DP의 base case(길이 1)가 왜 0 또는 참인지.
- [ ] 설명할 수 있다: 비트마스크 DP에서 마스크를 오름차순으로 도는 것이 왜 위상 정렬과 같은지.
- [ ] 설명할 수 있다: `dp[mask][u]`에서 왜 지나온 순서를 통째로 기억하지 않아도 되는지.
- [ ] 설명할 수 있다: 배정형이 왜 `dp[mask]` 1차원으로 줄어들고 TSP는 왜 안 줄어드는지.
- [ ] 설명할 수 있다: `sub = (sub - 1) & mask`가 왜 모든 부분집합을 정확히 한 번씩 도는지.
- [ ] 설명할 수 있다: "모든 마스크의 모든 부분집합"이 왜 `2ⁿ`도 `4ⁿ`도 아닌 `3ⁿ`인지.
- [ ] 설명할 수 있다: `mask & (mask - 1)`과 `mask & (-mask)`가 각각 무엇을 남기는지, 비트로.
- [ ] 설명할 수 있다: C++에서 `&`가 `==`보다 **약하다**는 것과, 파이썬에서는 정반대라는 것.
- [ ] 설명할 수 있다: `1 << n`이 언제 넘치고, `1LL << n`으로 고쳐야 하는 정확한 조건.
- [ ] 설명할 수 있다: 왜 `memset`으로 INF를 깔 수 없는지, `0x3f3f3f3f`가 왜 관용적으로 쓰이는지.
- [ ] 설명할 수 있다: Bitonic에서 상태가 왜 "두 끝점"만으로 충분한지(방문 집합이 자동으로 결정되는 이유).
- [ ] 설명할 수 있다: 양방향 LIS를 합칠 때 왜 꼭대기 값을 한 번 빼야 하는지.
- [ ] 설명할 수 있다: `dec` 배열을 왜 오른쪽 끝부터 채워야 하는지.
- [ ] 설명할 수 있다: 0/1 부분집합 합 DP에서 무게 루프를 왜 내림차순으로 도는지.
- [ ] 설명할 수 있다: 같은 "부분집합 고르기" 문제를 마스크로 풀지 값으로 풀지 무엇을 보고 정하는지.

**⚠️ 자주 하는 실수**

**1) 비트 연산과 비교의 우선순위를 파이썬 감각으로 쓴다**

```cpp
// ❌ 틀린 코드
if (mask & 1 == 0) { ... }               // '짝수인가'를 물을 생각이었다
if (mask & (1 << i) == 0) { ... }        // '원소 i가 없나'를 물을 생각이었다
```

왜: **C++에서 `&`는 `==`보다 우선순위가 낮다.** 그래서 첫 줄은 `mask & (1 == 0)` 즉 `mask & 0`이 되어 **언제나 0(거짓)**이고, 둘째 줄은 `mask & (1 << (i == 0))`이라는 전혀 다른 식이 된다. 파이썬에서는 `&`가 비교보다 **높아** 정확히 반대로 묶이므로 같은 코드가 의도대로 동작한다. 파이썬 코드를 옮길 때 가장 자주 터지는 자리이고, 컴파일 오류도 경고도 없이 조건이 통째로 죽는다.

```cpp
// ✅ 고친 코드
if ((mask & 1) == 0) { ... }                 // 괄호로 묶는다
if (((mask >> i) & 1) == 0) { ... }          // 비트 검사는 이 형태를 외운다
// 규칙: 비트 연산과 비교가 한 줄에 같이 나오면 예외 없이 괄호를 친다
```

**2) 시프트와 산술의 우선순위를 착각한다**

```cpp
// ❌ 틀린 코드
int FULL = 1 << n - 1;                   // '전체 집합'을 만들 생각이었다
for (int mask = 0; mask < 1 << n - 1; mask++) { ... }   // '모든 마스크'
long long big = 1 << 40;                 // 2^40 을 담을 생각이었다
```

왜: `+`, `-`는 `<<`보다 **먼저** 묶인다. 그래서 `1 << n - 1`은 `(1 << n) - 1`이 아니라 `1 << (n-1)`이다. `n = 4`면 15가 아니라 8이 나오고, 루프는 마스크 16개 중 절반만 돈다. 세 번째 줄은 더 나쁘다 — 리터럴 `1`은 `int`라 `1 << 40`은 **부호 있는 오버플로(UB)**이고, 그 망가진 값을 `long long`에 담아 봐야 소용없다.

```cpp
// ✅ 고친 코드
int FULL = (1 << n) - 1;                 // 먼저 2^n, 그다음 -1
for (int mask = 0; mask < (1 << n); mask++) { ... }     // 끝값은 1 << n
long long big = 1LL << 40;               // 왼쪽 피연산자를 long long 으로
// n >= 31 이면 1 << n 자체가 UB, n >= 32 는 시프트 폭이 타입 비트 수를 넘어 UB
```

**3) 구간 DP를 왼쪽 인덱스 오름차순으로 돈다**

```cpp
// ❌ 틀린 코드
for (int i = 0; i < n; i++)              // i 오름차순
    for (int j = i + 1; j < n; j++)
        for (int k = i; k < j; k++)
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + cost(i, j));
```

왜: `dp[i][j]`는 `dp[k+1][j]`를 읽는데 `k+1 > i`라 **행 번호가 더 큰 칸**이다. `i` 오름차순이면 그 행은 아직 손도 대지 않은 초기값이다. INF로 초기화했다면 답이 INF로 남아 눈에 띄지만, 0으로 초기화했다면 비용을 빼먹은 채 조용히 작은 값이 나온다. 길이 2, 3짜리 작은 예제는 우연히 맞아 통과하기도 한다.

```cpp
// ✅ 고친 코드
for (int length = 2; length <= n; length++) {          // 짧은 구간부터
    for (int i = 0; i + length - 1 < n; i++) {
        int j = i + length - 1;
        for (int k = i; k < j; k++)
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + cost(i, j));
    }
}
// i 를 내림차순(for (int i = n-1; i >= 0; i--))으로 돌아도 같은 순서가 만들어진다
```

**4) `memset`으로 INF를 깐다**

```cpp
// ❌ 틀린 코드
long long dp[1 << 20][20];
memset(dp, 0x3f, sizeof(dp));            // INF 를 깔았다고 생각한다
dp[1][0] = 0;
```

왜: `memset`은 **바이트 단위**로 채운다. `int` 배열이면 각 칸이 `0x3f3f3f3f`(약 10.6억)가 되지만, `long long` 배열이면 `0x3f3f3f3f3f3f3f3f`(약 4.5×10^18)가 되어 **두 개만 더해도 넘친다**. `memset(dp, 1e9, ...)`처럼 큰 값을 넘기면 하위 한 바이트만 잘려 엉뚱한 수가 깔린다. 게다가 위 코드는 배열 크기가 168MB라 전역이 아니면 스택에서 즉시 죽는다.

```cpp
// ✅ 고친 코드
const long long INF = LLONG_MAX / 4;                   // 더해도 안전한 여유
vector<vector<long long>> dp(1 << n, vector<long long>(n, INF));
dp[1][0] = 0;
// memset 이 안전한 경우는 0 이나 -1 로 채울 때뿐이다(모든 바이트가 같은 값)
// int 배열에 한해 0x3f 는 "더해도 int 안 넘침"이 성립해 관용적으로 쓰인다
```

**5) 비트마스크 DP의 초기 상태를 빼먹는다**

```cpp
// ❌ 틀린 코드
vector<vector<long long>> dp(1 << n, vector<long long>(n, INF));
for (int mask = 0; mask < (1 << n); mask++) {          // dp[1][0] = 0 을 안 썼다
    for (int u = 0; u < n; u++) {
        if (dp[mask][u] >= INF) continue;
        ...
    }
}
cout << *min_element(dp[FULL].begin(), dp[FULL].end()) << "\n";   // INF 출력
```

왜: 전이는 "이미 값이 있는 칸에서 다음 칸으로" 퍼뜨리는 구조라, 시작점이 하나도 없으면 아무 칸도 채워지지 않는다. 표 전체가 INF인 채 끝나고 답도 INF다. 반대로 `0`으로 초기화하면 도달 불가능한 상태가 전부 "비용 0"으로 보여 답이 0으로 나온다. **두 증상 모두 "점화식이 틀렸나"를 먼저 의심하게 만들어 시간을 잡아먹는다.**

```cpp
// ✅ 고친 코드
vector<vector<long long>> dp(1 << n, vector<long long>(n, INF));
dp[1][0] = 0;                            // 0만 방문했고 0에 있음, 비용 0
// 배정형이면 vector<long long> f(1 << n, INF); f[0] = 0;
// 도달 가능성을 INF로 구분하므로 초기값은 반드시 INF, 시작 칸만 0
```

**6) 전체 마스크 `(1 << n) - 1`과 순회 끝값 `1 << n`을 뒤바꾼다**

```cpp
// ❌ 틀린 코드
int FULL = 1 << n;                                   // 전체 집합이라고 쓴 값
for (int mask = 0; mask < (1 << n) - 1; mask++) { ... }   // 모든 마스크라고 쓴 루프
cout << dp[FULL] << "\n";                            // 배열 밖을 읽는다
```

왜: 원소가 `n`개면 마스크는 `0`부터 `2^n - 1`까지 `2^n`개다. **전체 집합**은 비트가 전부 1인 `(1 << n) - 1`이고, **순회 끝값**은 그보다 하나 큰 `1 << n`이다. 두 값을 맞바꾸면 `dp[1 << n]`이 배열 밖을 짚는데, C++의 `vector::operator[]`는 검사를 하지 않아 예외 대신 **쓰레기 값**이 나온다. 그리고 빠지는 마지막 마스크가 하필 "전부 방문한" 상태, 즉 정답이 사는 칸이다.

```cpp
// ✅ 고친 코드
int FULL = (1 << n) - 1;                             // 비트가 전부 1 = 전체 집합
vector<long long> f(1 << n, INF);                    // 길이는 마스크 개수 = 2^n
for (int mask = 0; mask < (1 << n); mask++) { ... }  // 0 .. 2^n - 1 을 전부 돈다
cout << f[FULL] << "\n";
// 디버깅할 때는 f.at(FULL) 로 바꿔 보면 범위 오류를 예외로 잡을 수 있다
```

**7) 부분집합 순회에서 빈 집합을 빠뜨린다**

```cpp
// ❌ 틀린 코드
for (int sub = mask; sub; sub = (sub - 1) & mask)    // sub == 0 이면 들어가지 않는다
    dp[mask] = min(dp[mask], cost[sub] + dp[mask ^ sub]);
```

왜: 조건 `sub`는 `sub`가 0이 되는 순간 본문을 건너뛰고 끝난다. "한 그룹을 통째로 비우는" 분할이 후보에서 빠지는데, 그것이 유효한 선택인 문제에서는 답이 어긋난다. 반대로 빈 집합을 넣으면 `mask ^ sub`가 `mask` 자신이 되어 `dp[mask]`가 자기 값을 읽는 순환 참조가 생긴다 — 대개는 값이 그대로라 무해하지만 "그룹은 비어 있을 수 없다" 같은 제약이 붙은 문제에서는 잘못된 값이 굳는다. **빈 집합을 넣을지 말지는 문제를 보고 정하고, 그 판단이 코드 형태에 드러나야 한다.**

```cpp
// ✅ 고친 코드
for (int sub = mask; ; sub = (sub - 1) & mask) {     // 빈 집합까지 한 번씩
    // sub 를 쓰는 자리
    if (sub == 0) break;                             // 사용 -> 검사 -> 갱신
}

for (int sub = (mask - 1) & mask; sub; sub = (sub - 1) & mask) {
    // 진부분집합만 필요할 때(자기 자신 제외)
}
```

**8) n이 큰데 비트마스크를 적용한다**

```cpp
// ❌ 틀린 코드
// 제한: 1 <= n <= 100000, 부분집합의 합을 목표 S에 맞춘다
for (int mask = 0; mask < (1 << n); mask++)          // n = 100000
    if (ssum[mask] == S) { ... }
```

왜: "부분집합"이라는 단어만 보고 마스크를 떠올린 것이다. `n = 100000`이면 마스크가 `2^100000`개다. C++에서는 파이썬과 달리 여기서 한 단계 더 나쁜 일이 생긴다 — `1 << 100000`은 **정의되지 않은 동작**이라 컴파일러가 임의의 값을 만들어 내고, 루프가 0번 돌거나 엉뚱하게 폭주하거나 아예 최적화로 사라진다. 오류 메시지 하나 없이 "답이 0"으로 끝날 수도 있다. **`2ⁿ`을 쓸 수 있는 것은 n이 20 안팎일 때뿐이다.**

```cpp
// ✅ 고친 코드 — 합의 상한 S가 작다면 '값'을 상태로 잡는다 -> O(n * S)
vector<char> can(S + 1, 0);
can[0] = 1;
for (int x : a)
    for (int w = S; w >= x; w--)
        if (can[w - x]) can[w] = 1;
cout << (can[S] ? "YES" : "NO") << "\n";
// n <= 20 이면 비트마스크, n이 크고 S가 작으면 값 DP, 둘 다 크면 다른 성질을 찾는다
```

**9) 0/1 부분집합 합 DP의 무게 루프를 오름차순으로 돈다**

```cpp
// ❌ 틀린 코드
for (int x : a)
    for (int w = x; w <= S; w++)                     // 오름차순
        if (can[w - x]) can[w] = 1;
```

왜: 오름차순이면 이번 라운드에서 방금 `x`를 써서 참이 된 `can[w-x]`를 같은 라운드의 더 큰 `w`에서 다시 읽는다. 결과적으로 원소 `x`를 두 번, 세 번 쓴 합까지 참이 되어 "각 원소를 최대 한 번"이라는 조건이 무너진다. `a = {3}`, `S = 6`일 때 `can[6]`이 참으로 나오는지 확인하면 바로 드러난다.

```cpp
// ✅ 고친 코드
for (int x : a)
    for (int w = S; w >= x; w--)                     // 내림차순 = 이전 라운드 값만
        if (can[w - x]) can[w] = 1;
// 원소를 여러 번 써도 되는 문제(무한 개수)라면 그때는 오름차순이 정답이다
```

**10) 양방향 LIS를 합치며 꼭대기를 두 번 센다**

```cpp
// ❌ 틀린 코드
vector<int> dec(n, 1);
for (int i = 0; i < n; i++)                          // 왼쪽부터 채운다
    for (int j = i + 1; j < n; j++)
        if (a[j] < a[i]) dec[i] = max(dec[i], dec[j] + 1);   // dec[j]가 아직 1
int ans = 0;
for (int i = 0; i < n; i++) ans = max(ans, inc[i] + dec[i]); // 꼭대기 중복
```

왜: 두 가지가 동시에 틀렸다. 첫째, `dec[i]`는 오른쪽 값들을 읽으므로 **오른쪽 끝부터** 채워야 하는데 왼쪽부터 돌면 `dec[j]`가 아직 초기값 1이라 감소 구간이 언제나 길이 2로 끊긴다. 둘째, `inc[i]`와 `dec[i]`는 둘 다 자기 자신을 포함하므로 그냥 더하면 꼭대기가 중복된다. 길이 문제에서는 답이 정확히 1만큼 커져서, 예제 하나로는 오프바이원인지 구조 오류인지 구분이 안 된다.

```cpp
// ✅ 고친 코드
vector<int> dec(n, 1);
for (int i = n - 1; i >= 0; i--)                     // 오른쪽 끝부터
    for (int j = i + 1; j < n; j++)
        if (a[j] < a[i] && dec[j] + 1 > dec[i]) dec[i] = dec[j] + 1;
int ans = 0;
for (int i = 0; i < n; i++) ans = max(ans, inc[i] + dec[i] - 1);   // 중복 1 제거
// 합을 구하는 문제라면 - 1 대신 - a[i]
```

**다음 챕터로**

- 이 챕터에서 익힌 "상태를 정수 하나로 압축한다"는 감각은 다른 유형에서 **BFS의 방문 표시**로 그대로 넘어간다. 격자 위에서 열쇠 몇 개를 모아야 문을 여는 문제는 `visited[r][c][keymask]`처럼 좌표 뒤에 마스크 한 칸을 붙이는 것으로 끝난다. 상태 설계의 문법이 같다.
- "채우는 순서가 곧 정확성"이라는 이 챕터의 교훈은 앞으로 만나는 모든 DP의 첫 점검 항목이다. 답이 이상하면 점화식보다 **읽는 칸이 이미 완성돼 있는지**를 먼저 확인하는 습관을 들이면 디버깅 시간이 크게 줄어든다.
- C++ 쪽에서 이 챕터가 남긴 습관은 세 가지다. **비트 검사에는 무조건 괄호**, **`1 << n`은 `int`라는 것**, **INF는 `memset`이 아니라 `vector` 생성자로**.
