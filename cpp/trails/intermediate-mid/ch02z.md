## L8. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터의 여섯 레슨은 전부 같은 관찰에서 출발한다. **"똑같은 계산이 질의마다 다시 일어나고 있다."** 누적합·차분·LR·전처리 표는 그 반복을 한 번의 스캔으로 뽑아 표에 넣어 두는 쪽이고, 좌표 압축은 표를 만들 수 있는 크기로 정의역을 줄이는 쪽이며, 투 포인터는 아예 표를 만들지 않고 "되돌아가지 않는 한 번의 스캔"으로 같은 절약을 얻는다. C++로 옮기면 여기에 조건이 하나 더 붙는다 — **표에 담기는 값이 `int`를 넘는지**를 매번 따져야 한다는 것이다. 아래에서 그 갈래를 한 장으로 잇고, 뼈대와 자주 넘어지는 지점을 모은다.

**개념 지도**

챕터 전체는 절약하는 방식에 따라 두 갈래로 갈린다. 왼쪽은 **미리 표를 만들고 조회로 답하는** 쪽, 오른쪽은 **표 없이 한 번만 훑는** 쪽이다.

```text
                   Ch02 : shorten the time
                              |
          the same work is being redone every time
                              |
       +----------------------+----------------------+
       |                                             |
   BUILD A TABLE ONCE                          SCAN WITHOUT GOING BACK
   answer every query by lookup                pointers only move right
       |                                             |
   +-------+-------+-------+-------+            +----+-----+
   |       |       |       |       |            |          |
 prefix   diff     LR    compress  tables    fixed window  variable
 sum      imos     L / R  coords   sieve etc  size = W     grows and
 L1       L4       L3     L2       L5         L6           shrinks  L6
   |       |       |       |       |            |          |
 query    update  both    index    heavy      two cells   each pointer
 O(1)     O(1)    sides   space    calc once  per step    moves <= n
```

누적합과 차분은 남남이 아니라 **서로의 역연산**이다. 한쪽은 질의를, 다른 쪽은 갱신을 상수로 만든다.

```text
  prefix sum and difference undo each other

     a  :   3    1    4    1    5

     S  : 0 3    4    8    9   14      S[i] = S[i-1] + a[i] , S[0] = 0
     D  :   3   -2    3   -3    4      D[i] = a[i] - a[i-1]

  with S :  sum of [l, r]   = S[r] - S[l-1]            // QUERY  O(1)
  with D :  add v on [l, r] = D[l] += v , D[r+1] -= v  // UPDATE O(1)
            running sum of D gives a back

  both S and D must be vector<long long>       // int 는 금방 넘친다

  fast QUERY and fast UPDATE at the same time
  -> past this chapter : Fenwick tree / segment tree
```

문제의 입력 상한을 거꾸로 읽으면 "어떤 복잡도가 기대되는가"가 나오고, 그것이 곧 기법 선택이다.

```text
  how big an n does each cost survive ?   (about 1e8 simple ops / sec)

  O(n^2)      n = 3e3   ok        n = 1e5   NO   (1e10 ops)
  O(n log n)  n = 1e6   ok        sorting , binary search , compression
  O(n + q)    n = q = 1e6   ok    prefix / diff / LR
  O(n)        n = 1e7   ok        one pass , two pointers

  read the limits backwards :
    n <= 1e3          anything, even a double loop
    n <= 1e5          O(n log n) at worst -> sort / lower_bound / compress
    n , q <= 1e5      O(n + q)            -> prefix / diff / LR
    n <= 1e6          O(n)                -> two pointers / single scan

  and read the VALUES too :
    n * max(a) > 2e9  ->  long long                // 합이 int 를 넘는다
```

**뼈대 코드**

1) 1차원 누적합 — 1-인덱스로 만들고 `pre[0] = 0`을 반드시 둔다. 타입은 `long long`.

```cpp
#include <bits/stdc++.h>
using namespace std;

int n = a.size();
vector<long long> pre(n + 1, 0);      // pre[0] = 0 이 경계 분기를 통째로 없앤다
for (int i = 1; i <= n; i++)
    pre[i] = pre[i-1] + a[i-1];       // <- 문제마다 바뀜: 합 대신 조건 카운트도 가능

// 1-인덱스 폐구간 [l, r]
long long rangeSum(int l, int r) {
    return pre[r] - pre[l-1];         // 빼는 쪽은 구간이 "시작되기 직전"까지
}
```

2) 2차원 누적합 — 포함배제 네 항.

```cpp
vector<vector<long long>> P(n + 1, vector<long long>(m + 1, 0));
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++)
        P[i][j] = g[i-1][j-1] + P[i-1][j] + P[i][j-1] - P[i-1][j-1];

// 1-인덱스, 양끝 포함
long long rect(int r1, int c1, int r2, int c2) {
    return P[r2][c2] - P[r1-1][c2] - P[r2][c1-1] + P[r1-1][c1-1];
    //      전체        위쪽 띠        왼쪽 띠       두 번 빠진 모서리 복구
}
```

3) 차분 배열(imos) — 갱신은 두 칸, 복원은 한 번의 누적합. 크기는 `N+2`.

```cpp
vector<long long> diff(N + 2, 0);     // r+1 이 최대 N+1 이므로 여유 두 칸
for (auto& u : updates) {             // 1-인덱스 폐구간 [l, r]에 v 더하기
    diff[u.l] += u.v;
    diff[u.r + 1] -= u.v;             // <- 끄는 위치는 구간 "밖" 첫 칸
}

vector<long long> arr(N + 1, 0);
long long run = 0;
for (int i = 1; i <= N; i++) {
    run += diff[i];
    arr[i] = run;                     // 겹침 최댓값이 필요하면 v=1로 두고 max(run)
}
```

4) LR 접두·접미 — 정의를 먼저 한 줄로 적고 시작한다.

```cpp
// L[i] = op(a[0..i-1]) , R[i] = op(a[i+1..n-1])   <- 자기 자신은 빠진다
const int E = INT_MIN / 2;   // <- 문제마다 바뀜: 항등원(합 0, 곱 1, min INT_MAX/2)
                             //    /2 로 여유를 둬야 뺄셈에서 오버플로가 없다
vector<int> L(n, E);
for (int i = 1; i < n; i++)
    L[i] = max(L[i-1], a[i-1]);       // 이웃이 계산해 둔 결과를 재사용

vector<int> R(n, E);
for (int i = n - 2; i >= 0; i--)
    R[i] = max(R[i+1], a[i+1]);

vector<int> ans(n);
for (int i = 0; i < n; i++)
    ans[i] = max(L[i], R[i]);         // 결합법칙이 있는 연산이어야 성립
```

5) 투 포인터 2종 — 고정 창과 가변 창. 창의 합은 `long long`.

```cpp
// (A) 고정 창: 길이 W 구간의 통계. 창이 한 칸 움직이면 두 칸만 바뀐다.
long long cur = 0;
for (int i = 0; i < W; i++) cur += a[i];
long long best = cur;
for (int r = W; r < n; r++) {
    cur += a[r] - a[r - W];           // 들어온 값 - 나간 값
    best = max(best, cur);            // <- 문제마다 바뀜: max / min / 조건 카운트
}

// (B) 가변 창: 조건을 만족하는 최장·최단 구간. 두 포인터 모두 오른쪽으로만.
int lo = 0, bestLen = 0;
long long sum = 0;
for (int r = 0; r < n; r++) {
    sum += a[r];                      // 오른쪽 확장
    while (sum > K) {                 // <- 문제마다 바뀜: 조건이 깨졌을 때의 회복
        sum -= a[lo];
        lo++;
    }
    bestLen = max(bestLen, r - lo + 1);   // 불변식이 회복된 직후에 답 갱신
}
```

6) 좌표 압축 — 정렬 + 중복 제거 + 순위 조회, 그리고 실제 폭 복원.

```cpp
vector<int> order(xs.begin(), xs.end());
sort(order.begin(), order.end());
order.erase(unique(order.begin(), order.end()), order.end());
//           ^ unique는 밀어내기만 한다. erase와 반드시 짝을 지어야 크기가 준다

vector<int> comp(xs.size());
for (size_t i = 0; i < xs.size(); i++)
    comp[i] = lower_bound(order.begin(), order.end(), xs[i]) - order.begin();

// 되돌리기: 압축은 "순서"만 보존하고 "간격"은 버린다
int real  = order[idx];                          // 실제 값
long long width = (long long)order[idx + 1] - order[idx];
//                ^ 길이·면적을 물으면 반드시 이 폭을 곱한다. 곱하기 전에 승격
```

**언제 무엇을 쓰나**

먼저 "단순하게 짜면 얼마인가 → 무엇이 반복되는가 → 어떤 기법인가 → 얼마가 되는가"를 대응표로 못 박는다. 기법 선택은 사실상 이 표의 왼쪽 열을 알아보는 일이다.

| 단순하게 짜면 (복잡도) | 무엇이 반복되는가 | 어떤 기법 | 개선 후 복잡도 |
| --- | --- | --- | --- |
| 질의마다 구간을 다시 더함 O(nq) | 앞쪽 부분합 | 누적합 `vector<long long>` (L1) | O(n + q) |
| 질의마다 직사각형을 다시 훑음 O(q·nm) | 왼쪽 위 직사각형의 합 | 2D 누적합 + 포함배제 (L1) | O(nm + q) |
| 갱신마다 구간 전체를 돌음 O(nq) | 구간 안쪽 칸 전부 | 차분 배열 / imos (L4) | O(n + q) |
| 각 i마다 나머지를 다시 훑음 O(n²) | 왼쪽 누적과 오른쪽 누적 | LR 접두·접미 (L3) | O(n) |
| 모든 쌍을 다 봄 O(n²) | 짝 후보 찾기 | `unordered_set` 존재 판정 / `sort` + 마주보는 투 포인터 (L6) | O(n) / O(n log n) |
| 각 시작점마다 구간을 다시 늘림 O(n²) | 창 안의 합·개수 | 투 포인터 (L6) | O(n) |
| 창마다 `accumulate`로 다시 더함 O(nW) | 창 안의 W개 중 W-2개 | 고정 창 차이 갱신 (L6) | O(n) |
| 10⁹ 크기 배열을 만들려 함 (불가능) | 실제로 쓰이는 좌표는 n개뿐 | 좌표 압축 `sort` + `unique` (L2) | 시간 O(n log n), 공간 O(n) |
| 질의마다 같은 무거운 계산 O(q·A) | 그 계산 자체 | 전처리 표(체·SPF·팩토리얼) (L5) | O(P + q) |
| 매 질의마다 정렬을 다시 함 O(q·n log n) | 정렬 결과 | 한 번만 정렬하고 재사용 | O(n log n + q log n) |

그다음 아래 표에서 구체적인 도구를 고른다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 값이 변하지 않고 구간합 질의만 여러 번 | 1D 누적합 | 앞쪽 공통 부분이 뺄셈으로 소거된다 | 전처리 O(n), 질의 O(1) |
| 부분 직사각형 합 질의 | 2D 누적합 + 포함배제 | 같은 소거를 두 방향으로 겹친 것 | 전처리 O(nm), 질의 O(1) |
| "조건을 만족하는 원소가 구간에 몇 개" | 조건을 1/0으로 바꾼 누적합 | 개수도 결국 합이다 | 전처리 O(n), 질의 O(1) |
| 구간 일괄 더하기가 여러 번, 최종 배열만 필요 | 차분 배열(imos) | 갱신이 양 끝 두 칸만 건드린다 | O(n + m) |
| "가장 많이 겹치는 지점"의 겹침 수 | v=1 차분 후 누적합의 최댓값 | 겹침 수 = 켜져 있는 구간 수 | O(n + m) |
| 각 i에 대해 "자기를 뺀 전체" 정보 | LR 접두·접미 배열 | 이웃 결과를 재사용해 스캔 두 번 | O(n), 공간 O(n) |
| 나눗셈 없이 자기 제외 곱 | LR (곱, 항등원 1, `long long`) | 0이 섞여도 안전하다 | O(n) |
| 좌표가 10⁹인데 서로 다른 값은 n개 | 좌표 압축 | 답이 크기가 아니라 순위에만 의존 | O(n log n) |
| 압축한 뒤 길이·면적을 물음 | 압축 + `order`로 실제 폭 복원 | 압축이 버린 간격을 되돌려야 한다 | O(n log n) |
| 원소가 모두 양수, "합 조건 최장·최단 구간" | 가변 창 투 포인터 | 단조성: r↑이면 합↑, l↑이면 합↓ | O(n), 공간 O(1) |
| 길이가 고정된 창의 최대·최소 | 고정 창 투 포인터 | 한 칸 이동이 두 칸 갱신 | O(n) |
| 고정 창 안의 최댓값이 필요 | 단조 `deque` | 뒤에서 쓸모없는 후보를 버리며 유지 | O(n) |
| 정렬 배열에서 합이 T인 쌍 | 마주보는 투 포인터 | 한 번 버린 후보는 다시 답이 될 수 없다 | O(n log n) (정렬 지배) |
| 음수가 섞인 배열의 구간합 조건 | 투 포인터 말고 누적합 + 정렬·해시 | 단조성이 깨져 포인터 규칙이 무의미 | O(n log n) |
| 같은 무거운 계산이 질의마다 반복 | 전처리 표(체·SPF·팩토리얼) | `Q > P / (A - B)`면 반드시 이득 | 체 O(n log log n), 질의 O(1) |
| 질의와 갱신이 번갈아 들어옴 | 이 챕터 밖(펜윅·세그먼트 트리) | 누적합·차분은 한쪽만 상수로 만든다 | 연산당 O(log n) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: `pre[r] - pre[l-1]`을 `pre`의 정의에서 직접 유도하고, 왜 빼는 쪽이 `l`이 아니라 `l-1`인지.
- [ ] 설명할 수 있다: `pre[0] = 0` 한 칸이 없애 주는 분기가 정확히 어떤 코드였는지.
- [ ] 설명할 수 있다: 2차원 포함배제의 부호가 `-, -, +`인 이유를 네 영역으로 나눠서.
- [ ] 설명할 수 있다: 차분 배열의 갱신이 `[l, r]`에만 살아남는 이유를 `i < l`, `l ≤ i ≤ r`, `i > r` 세 경우로 나눠서.
- [ ] 설명할 수 있다: 왜 `r`이 아니라 `r+1`에서 빼야 하고, 그래서 배열을 `N+2`로 잡아야 하는지.
- [ ] 설명할 수 있다: 누적합과 차분이 서로의 역연산이고 각각 질의·갱신 **한쪽만** 상수로 만든다는 것, 그리고 그 경계 너머에 무엇이 있는지.
- [ ] 설명할 수 있다: 누적합·창의 합·자기 제외 곱을 `long long`으로 잡아야 하는 기준을 "n × 원소 최대치"로 즉석에서 계산하기.
- [ ] 설명할 수 있다: `int` 오버플로가 왜 예외가 아니라 "조용히 틀린 답"으로 나타나는지, 그리고 그 결과 어떤 증상이 보이는지.
- [ ] 설명할 수 있다: LR이 스캔 두 번으로 충분한 이유와, 항등원(합 0·곱 1·max `INT_MIN`)이 필요한 자리가 어디인지.
- [ ] 설명할 수 있다: 항등원으로 `INT_MIN`을 그대로 쓰면 위험하고 `INT_MIN / 2`가 안전한 이유.
- [ ] 설명할 수 있다: LR 결합에 결합법칙이 필요한 이유와, 뺄셈·나눗셈을 이 틀에 그대로 넣을 수 없는 이유.
- [ ] 설명할 수 있다: 좌표 압축이 답을 바꾸지 않는 조건(강한 단조 증가)과, 바꿔 버리는 질문(거리·면적)의 구분.
- [ ] 설명할 수 있다: `sort`와 `unique`+`erase` 중 하나만 빠져도 압축이 어떻게 깨지는지 각각.
- [ ] 설명할 수 있다: 투 포인터가 O(N)인 근거를 "왼쪽 포인터가 되돌아가지 않는다"의 분할상환으로.
- [ ] 설명할 수 있다: 투 포인터의 전제인 단조성이 무엇이고, 음수가 섞이면 왜 깨지는지 예시와 함께.
- [ ] 설명할 수 있다: 마주보는 투 포인터에서 한쪽 끝을 버려도 되는 이유와, 그 논증이 정렬을 왜 요구하는지.
- [ ] 설명할 수 있다: 고정 창과 가변 창이 각각 어떤 문장에서 나오는지, 갱신 방식이 어떻게 다른지.
- [ ] 설명할 수 있다: 전처리가 이득인 조건 `Q > P / (A - B)`가 무슨 뜻인지, Q가 작으면 왜 손해인지.
- [ ] 설명할 수 있다: 문제의 N·Q 상한만 보고 요구되는 복잡도를 역산해 기법 후보를 좁히는 방법.

**⚠️ 자주 하는 실수**

**1) 누적합을 `int`로 잡아 조용히 오버플로시킨다**

```cpp
// ❌ 틀린 코드
vector<int> pre(n + 1, 0);              // n = 100000, a[i] <= 100000
for (int i = 1; i <= n; i++)
    pre[i] = pre[i-1] + a[i-1];         // 총합 1e10 -> int(약 2.1e9)를 넘는다
cout << pre[r] - pre[l-1] << '\n';      // 음수가 섞인 엉뚱한 값
```

왜: C++의 부호 있는 정수 오버플로는 **예외도 경고도 없이** 값이 뒤집힌다(형식상으로는 미정의 동작이다). 파이썬은 정수가 임의 정밀도라 이 사고 자체가 없으므로, 파이썬 풀이를 그대로 옮길 때 가장 먼저 밟는 지뢰다. 작은 예제는 통과하고 큰 입력에서만 틀리는 것이 특징이다.

```cpp
// ✅ 고친 코드 — 누적하는 배열은 기본값이 long long
vector<long long> pre(n + 1, 0);
for (int i = 1; i <= n; i++)
    pre[i] = pre[i-1] + a[i-1];         // 오른쪽이 long long으로 승격된다
// 판단 기준: n * max(|a[i]|) 가 2e9 를 넘으면 무조건 long long
```

**2) `l = 1`에서 `pre[l-1]`이 배열 밖으로 나간다**

```cpp
// ❌ 틀린 코드 — 0-인덱스 누적합에 1-인덱스 공식을 섞었다
vector<long long> pre(n);
pre[0] = a[0];
for (int i = 1; i < n; i++) pre[i] = pre[i-1] + a[i];
for (auto& q : queries)                  // 0-인덱스 폐구간 [l, r]
    cout << pre[q.r] - pre[q.l - 1] << '\n';   // l = 0 이면 pre[-1] 을 읽는다
```

왜: 파이썬이라면 `S[-1]`이 "뒤에서 읽기"라 전체 합이 되어 **틀린 답이 조용히 나오지만**, C++ `vector::operator[]`의 음수 인덱스는 **범위 검사 없이 남의 메모리를 읽는 미정의 동작**이다. 값이 쓰레기이거나, 운이 나쁘면 그대로 통과했다가 채점 서버에서만 죽는다.

```cpp
// ✅ 고친 코드 — 앞에 0을 한 칸 붙여 1-인덱스로 통일한다
vector<long long> pre(n + 1, 0);         // pre[0] = 0
for (int i = 1; i <= n; i++) pre[i] = pre[i-1] + a[i-1];
for (auto& q : queries)                  // 입력이 0-인덱스면 한 칸씩 밀어서 맞춘다
    cout << pre[q.r + 1] - pre[q.l] << '\n';
// 디버깅 중이라면 pre.at(...) 로 바꿔 돌려 보면 범위 초과가 예외로 잡힌다
```

**3) 차분 배열의 `r+1`이 배열 밖으로 나간다**

```cpp
// ❌ 틀린 코드
vector<long long> diff(N);               // 1-인덱스인데 크기를 N으로 잡았다
for (auto& u : updates) {
    diff[u.l] += u.v;
    diff[u.r + 1] -= u.v;                // r = N 이면 diff[N+1] -> 범위 밖
}
```

왜: 폐구간 `[l, r]`을 표현하려면 끄는 위치가 **구간 밖 첫 칸**인 `r+1`이어야 한다. `r`은 최대 `N`까지 오므로 `r+1`은 `N+1`까지 간다. 1-인덱스라 0번 칸도 하나 필요하니 크기는 `N+2`다. 게다가 C++는 범위를 검사하지 않으므로 "마지막 구간을 포함하는 갱신"에서만 조용히 남의 메모리를 덮어써 발견이 매우 늦다.

```cpp
// ✅ 고친 코드
vector<long long> diff(N + 2, 0);        // 0번 칸 + 1..N + r+1의 최대치 N+1
for (auto& u : updates) {
    diff[u.l] += u.v;
    diff[u.r + 1] -= u.v;
}
vector<long long> arr(N + 1, 0);
long long run = 0;
for (int i = 1; i <= N; i++) { run += diff[i]; arr[i] = run; }
```

**4) 투 포인터에서 왼쪽 포인터를 되돌려 O(n²)을 만든다**

```cpp
// ❌ 틀린 코드
int best = 0;
for (int r = 0; r < n; r++) {
    long long cur = 0;
    int lo = r;
    while (lo >= 0 && cur + a[lo] <= K) {   // r마다 왼쪽으로 다시 훑는다
        cur += a[lo];
        lo--;
    }
    best = max(best, r - lo);
}
```

왜: 겉모습은 포인터 두 개지만 실제로는 이중 루프다. `r`마다 왼쪽 끝을 처음부터 다시 찾으므로 최악 O(N²)이고, N=10만이면 100억 번이다. 투 포인터가 O(N)인 유일한 근거는 **`lo`가 전체 과정에서 오직 오른쪽으로만, 합쳐서 N칸만 움직인다**는 사실이다. `lo`를 되돌리는 순간 그 근거가 사라진다.

```cpp
// ✅ 고친 코드 — lo는 루프 밖에 두고 절대 줄이지 않는다
int lo = 0, best = 0;
long long cur = 0;
for (int r = 0; r < n; r++) {
    cur += a[r];
    while (cur > K) {                 // 조건이 깨졌을 때만, 오른쪽으로만
        cur -= a[lo];
        lo++;
    }
    best = max(best, r - lo + 1);
}
```

**5) 정렬하지 않고 마주보는 투 포인터를 쓴다**

```cpp
// ❌ 틀린 코드
vector<int> a = {5, 1, 4};            // 정렬하지 않았다. T = 5
int i = 0, j = (int)a.size() - 1;
while (i < j) {
    int s = a[i] + a[j];
    if (s == T) break;
    else if (s < T) i++;              // "작으면 왼쪽을 당긴다"의 근거가 없다
    else j--;
}
```

왜: 이 기법의 정당성은 "정렬돼 있으므로 `a[i]+a[j] > T`면 `a[j]`는 남은 누구와도 짝이 될 수 없다"에서 나온다. 정렬이 없으면 그 논증이 통째로 무너진다. 위 예에서 정답은 `1 + 4 = 5`인데, 첫 비교 `5+4=9 > 5`에서 `j`를 당기고 다음 `5+1=6 > 5`에서 또 당겨 루프가 끝나 버린다.

```cpp
// ✅ 고친 코드
sort(a.begin(), a.end());             // 마주보는 투 포인터의 전제 조건
int i = 0, j = (int)a.size() - 1;
while (i < j) {
    int s = a[i] + a[j];
    if (s == T) break;
    else if (s < T) i++;
    else j--;
}
// 원래 인덱스를 답으로 내야 하면 정렬 전에 pair<값, 인덱스>로 묶어 둔다
```

**6) 2차원 포함배제에서 겹치는 모서리를 처리하지 않는다**

```cpp
// ❌ 틀린 코드
long long area = P[r2][c2] - P[r1-1][c2] - P[r2][c1-1];   // 마지막 항을 빠뜨렸다
```

왜: 위쪽 띠 `P[r1-1][c2]`는 `B + D`, 왼쪽 띠 `P[r2][c1-1]`은 `C + D`다. 둘을 빼면 왼쪽 위 모서리 `D`가 **두 번** 빠져 결과가 `A - D`가 된다. 한 번 되돌려 줘야 정확히 `A`다. 반대로 부호를 `- P[r1-1][c1-1]`로 잘못 쓰면 `D`가 세 번 빠진다.

```cpp
// ✅ 고친 코드
long long area = P[r2][c2] - P[r1-1][c2] - P[r2][c1-1] + P[r1-1][c1-1];
// 검산: 1x1 직사각형(r1=r2=i, c1=c2=j)에 넣으면 g[i-1][j-1] 한 칸이 나와야 한다
```

**7) `unique` 뒤에 `erase`를 빠뜨리거나, 압축 인덱스 간격을 실제 폭으로 쓴다**

```cpp
// ❌ 틀린 코드
vector<int> order = xs;
sort(order.begin(), order.end());
unique(order.begin(), order.end());        // 크기가 줄지 않는다. 뒤에 쓰레기가 남음

long long total = 0;
for (int i = 0; i + 1 < (int)order.size(); i++)
    if (covered[i]) total += 1;            // 모든 칸의 폭을 1로 세어 버린다
```

왜: `std::unique`는 연속된 중복을 뒤로 밀어내고 "새로운 끝"만 알려줄 뿐 컨테이너를 줄이지 않는다. `erase`와 짝을 지어야 `order.size()`가 맞는다. 그리고 압축은 **순서만 보존하고 간격은 버리므로**, `order = {0, 5, 100}`에서 0번 칸의 실제 폭은 5, 1번 칸은 95인데 둘 다 1로 세면 길이·면적이 통째로 어긋난다.

```cpp
// ✅ 고친 코드
sort(order.begin(), order.end());
order.erase(unique(order.begin(), order.end()), order.end());   // 반드시 짝으로

long long total = 0;
for (int i = 0; i + 1 < (int)order.size(); i++)
    if (covered[i]) total += (long long)order[i+1] - order[i];  // 실제 폭 복원
// 2차원 면적이면 (long long)(ox[i+1]-ox[i]) * (oy[j+1]-oy[j]) — 곱하기 전에 승격
```

**8) 창을 옮길 때마다 창 안을 다시 계산한다**

```cpp
// ❌ 틀린 코드
long long best = 0;
for (int r = W - 1; r < n; r++) {
    long long s = accumulate(a.begin() + (r - W + 1), a.begin() + r + 1, 0LL);
    best = max(best, s);                 // 창마다 W개를 처음부터 다시 더한다
}
```

왜: 창이 한 칸 움직이면 실제로 바뀌는 것은 **들어온 값 하나와 나간 값 하나**뿐인데, 매번 W개를 다시 더하면 O(N·W)다. N=W=10만이면 100억 번이다. `accumulate` 한 줄이라 싸 보이지만 그 안에서 W번을 도는 것이 함정이고, 같은 실수가 "창 안의 최댓값을 `max_element`로 구하기"에서도 그대로 반복된다(그쪽은 단조 `deque`가 정답이다).

```cpp
// ✅ 고친 코드 — 차이만 갱신한다
long long cur = accumulate(a.begin(), a.begin() + W, 0LL);
long long best = cur;
for (int r = W; r < n; r++) {
    cur += a[r] - a[r - W];              // 들어온 값 - 나간 값, 창당 O(1)
    best = max(best, cur);
}
```

**다음 챕터로**

- 이 챕터가 만든 습관 — "단순 방법의 복잡도를 먼저 세고, 무엇이 반복되는지 지목한 뒤 그 반복을 없앤다" — 는 다음 챕터(이진탐색·매개변수 탐색)에서 그대로 쓰인다. 다르다면 줄이는 대상이 "반복 계산"이 아니라 "탐색 공간"이라는 점뿐이다.
- 투 포인터의 정당성 근거인 **단조성**이 특히 곧바로 이어진다. "`lo`를 오른쪽으로만 밀어도 되는 이유"와 "답을 절반씩 버려도 되는 이유"는 같은 성질의 두 얼굴이고, 매개변수 탐색은 그 단조성을 예/아니오 판정 함수 위에서 다시 쓴다.
- `long long` 습관도 그대로 넘어간다. 다음 챕터의 판정 함수 안에서 합·개수를 누적할 때 `int`로 받으면 판정이 통째로 뒤집혀 "전 구간 실패"로 나타나는데, 증상만 보고는 이진탐색의 경계 버그로 오해하기 쉽다.
- 누적합·차분으로는 질의와 갱신을 동시에 빠르게 할 수 없다는 이 챕터의 결론은, 펜윅 트리·세그먼트 트리가 왜 필요한지에 대한 정확한 동기로 남는다.
