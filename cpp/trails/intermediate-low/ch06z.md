## L5. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 레슨은 Ch6(DP II) 전체를 **상태 설계**라는 하나의 축으로 묶는다. Ch5까지의 DP는 지문이 상태 축을 알려 주었다. Ch6의 세 유형 — state를 정의해 나아가는 DP, 직전 상황에 영향받는 연속 DP, String Matching — 은 전부 "`dp[i]` 하나로는 다음 결정을 내릴 수 없다"는 같은 벽에서 출발한다. 그 벽 앞에서 **무엇을 축으로 승격할 것인가**가 이 챕터의 전부다.

**개념 지도**

- 상태를 하나 더 붙여야 하는지는 질문 하나로 판정된다. "i에 서서, 여기까지 왔다는 사실만으로 다음 선택을 정할 수 있는가?"

```text
  do I need one more axis in the state ?

  standing at i, can I decide the next move
  knowing only "how far I got" ?
     |
    yes -> dp[i] is enough                    # Ch5 로 충분하다
     |
     no -> what exactly is missing ?
            |
   +--------+---------+-----------+-----------+-----------+
   |        |         |           |           |           |
  what I   how many  which mode  how much    where the   is it still
  picked   in a row  am I in     is left     other word  connected
  last                                       sits        (streak)
   |        |         |           |           |           |
 dp[i][p] dp[i][run] dp[i][mode] dp[i][rest] dp[i][j]   cur / best

  rule of thumb : the smallest past information that changes the future
```

- 직전 선택 의존형은 **전이표**를 먼저 그리면 코드가 저절로 나온다. 금지된 전이 한 칸이 곧 문제의 조건이다.

```text
  "cannot pick two in a row"    s = 0 skipped i,  s = 1 picked i

     from        to      allowed ?    gain
     -----------------------------------------
      0  ----->   0        yes         0
      0  ----->   1        yes         a[i]
      1  ----->   0        yes         0
      1  ----->   1        NO          -          # 연속 선택 금지

     dp[i][0] = max(dp[i-1][0], dp[i-1][1])
     dp[i][1] = dp[i-1][0] + a[i]
```

- String Matching은 문제가 달라도 **읽는 칸 세 개가 같다**. 달라지는 것은 "같을 때 / 다를 때 무엇을 하는가"뿐이다.

```text
  two-word table : every problem reads the same three cells

          j-1   j
        +----+----+
    i-1 | \  | ^  |
        +----+----+
     i  | <  | *  |
        +----+----+

  LCS             same -> \ + 1      diff -> max( ^ , < )
  edit distance   same -> \          diff -> 1 + min( \ , ^ , < )
  count subseq    same -> \ + ^      diff -> ^
  common substr   same -> \ + 1      diff -> 0     # 이어짐이 끊긴다

  base   LCS      all zero
         edit     dp[i][0] = i , dp[0][j] = j
         subseq   dp[i][0] = 1                     # 빈 패턴은 1번 등장
```

- C++에서 이 표들을 담는 그릇과, 표에 쓰는 "도달 불가" 표식은 미리 정해 두면 실수가 준다.

```text
  what                     container                     unreachable mark
  ----------------------   ---------------------------   ------------------
  dp[i][s], S fixed        vector<array<long long,S>>     LLONG_MIN / 4
  dp[i][s], S from input   vector<vector<long long>>      LLONG_MIN / 4
  two-word table           vector<vector<int>> (n+1)x(m+1)  0 or i / j base
  rolling two rows         vector<int> prv, cur           swap(prv, cur)
  Kadane                   long long cur, best            start at a[0]

  never use LLONG_MIN itself : NEG + gain flips to a huge positive
```

**뼈대 코드**

- (1) `dp[i][s]` 일반형. 상태 축을 붙이는 모든 문제가 이 모양이다.

```cpp
#include <bits/stdc++.h>
using namespace std;

const long long NEG = LLONG_MIN / 4;         // 더해도 안 넘치게 여유를 둔다
const int S = 2;                             // 상태 개수: 문제마다 바뀜

vector<array<long long, S>> dp(n + 1);
for (auto& row : dp) row.fill(NEG);
dp[0][START] = 0;                            // 시작 상태만 유효하게 연다

for (int i = 1; i <= n; i++) {
    for (int s = 0; s < S; s++) {
        if (dp[i - 1][s] == NEG) continue;   // 도달 못 한 상태에서 잇지 않는다
        for (auto [ns, gain] : moves(s, i))  // 허용된 전이만 돌려주는 함수
            dp[i][ns] = max(dp[i][ns], dp[i - 1][s] + gain);
    }
}

long long ans = NEG;                         // 마지막 칸에서 '허용되는' 상태만 후보
for (int s = 0; s < S; s++)
    if (dp[n][s] != NEG) ans = max(ans, dp[n][s]);
cout << ans << "\n";
```

- (2) 직전 선택 의존형. 상태가 곧 "직전에 무엇을 했는가"다.

```cpp
// 두 가게를 오가며 일하고, 가게를 바꾸면 이동 비용 c가 든다
long long da = A[0], db = B[0];              // 첫날은 이동 비용이 없다
for (int i = 1; i < n; i++) {
    long long pa = da, pb = db;              // 어제 값을 먼저 복사한다
    da = A[i] + max(pa, pb - c);             // 오늘 A: 어제 A 유지 or B에서 이동
    db = B[i] + max(pb, pa - c);             // 두 값을 '동시에' 갱신해야 한다
}
cout << max(da, db) << "\n";
// pa, pb 없이 da를 먼저 고치면 둘째 줄이 '오늘 A'를 읽어 하루가 어긋난다
```

- (3) 연속(이어짐) DP. "이어붙일까, 여기서 새로 시작할까"의 한 줄 전이다.

```cpp
// Kadane: cur = i를 반드시 포함하는 연속 구간의 최대합
long long best = a[0], cur = a[0];           // 0이 아니라 a[0]으로 연다
for (int i = 1; i < n; i++) {
    cur = max((long long)a[i], cur + a[i]);  // 새로 시작 vs 이어붙이기
    best = max(best, cur);                   // 전역 답은 따로 기록
}

// 한 번 삭제 허용: 상태 축 하나로 확장된다
long long keep = a[0], drop = a[0], ans = a[0];   // keep=삭제 안 씀, drop=한 번 씀
for (int i = 1; i < n; i++) {
    long long pk = keep, pd = drop;          // 어제 값 복사(동시 갱신)
    drop = max(pk, pd + a[i]);               // 지금 a[i]를 버리거나, 이미 버렸거나
    keep = max((long long)a[i], pk + a[i]);
    ans = max({ans, keep, drop});            // max({..})는 초기화 리스트 형태
}
```

- (4) LIS. 조건을 만족하는 이전 것만 골라 잇는다.

```cpp
// O(n^2): dp[i] = a[i]를 마지막으로 쓰는 증가 수열의 최대 길이
vector<int> dp(n, 1);
for (int i = 0; i < n; i++)
    for (int j = 0; j < i; j++)
        if (a[j] < a[i])                     // 조건: '<' 인가 '<=' 인가 확인
            dp[i] = max(dp[i], dp[j] + 1);
cout << *max_element(dp.begin(), dp.end()) << "\n";

// O(n log n): tails[k] = 길이 k+1 증가수열이 가질 수 있는 최소 끝값
vector<int> tails;
for (int x : a) {
    auto it = lower_bound(tails.begin(), tails.end(), x);  // 비감소면 upper_bound
    if (it == tails.end()) tails.push_back(x);
    else *it = x;
}
cout << tails.size() << "\n";   // 길이만 답. tails는 실제 LIS가 아니다
```

- (5) 두 문자열 표. LCS와 편집 거리는 초기화와 세 칸 결합만 다르다.

```cpp
int n = A.size(), m = B.size();
vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));   // (n+1) x (m+1)

// LCS
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++) {
        if (A[i - 1] == B[j - 1])            // dp는 1-based, string은 0-based
            dp[i][j] = dp[i - 1][j - 1] + 1;
        else
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
    }

// 편집 거리: 경계 초기화가 필수다
vector<vector<int>> ed(n + 1, vector<int>(m + 1, 0));
for (int i = 0; i <= n; i++) ed[i][0] = i;   // A의 i글자를 전부 삭제
for (int j = 0; j <= m; j++) ed[0][j] = j;   // B의 j글자를 전부 삽입
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++) {
        if (A[i - 1] == B[j - 1])
            ed[i][j] = ed[i - 1][j - 1];
        else
            ed[i][j] = 1 + min({ed[i - 1][j - 1],   // 교체
                                ed[i - 1][j],       // 삭제
                                ed[i][j - 1]});     // 삽입
    }
```

- (6) 부분수열 등장 횟수. 한 줄짜리 표로 압축하려면 방향이 중요하다.

```cpp
const long long MOD = 1000000007LL;          // 문제마다 바뀜
vector<long long> dp(m + 1, 0);
dp[0] = 1;                                   // 빈 패턴은 언제나 1번 등장
for (char ch : A)                            // A를 한 글자씩 흘려보낸다
    for (int j = m; j >= 1; j--)             // 역순! 같은 글자를 두 번 쓰지 않게
        if (B[j - 1] == ch)
            dp[j] = (dp[j] + dp[j - 1]) % MOD;
cout << dp[m] << "\n";
```

- (7) 원형(첫 칸과 마지막 칸이 이웃). 시작 상태를 고정해 선형 문제로 되돌린다.

```cpp
const int K = 3;                             // 색의 개수: 문제마다 바뀜
long long total = 0;
for (int first = 0; first < K; first++) {    // 1번 칸의 색을 하나로 고정
    vector<vector<long long>> dp(n, vector<long long>(K, 0));
    dp[0][first] = 1;
    for (int i = 1; i < n; i++)
        for (int c = 0; c < K; c++)
            for (int p = 0; p < K; p++)
                if (p != c)                  // 인접 금지 조건
                    dp[i][c] = (dp[i][c] + dp[i - 1][p]) % MOD;
    for (int c = 0; c < K; c++)
        if (c != first)                      // 마지막 칸도 첫 칸과 이웃이다
            total = (total + dp[n - 1][c]) % MOD;
}
cout << total << "\n";
```

**언제 무엇을 쓰나**

- 지문의 표현을 상태 정의로 옮긴다. 상태 축은 "미래의 결정을 바꾸는 최소한의 과거 정보"만 담는다. 이것이 이 챕터의 핵심 대응표다.

| 지문에 이런 말이 보이면 | 이렇게 상태를 잡는다 |
|---|---|
| "직전에 고른 것과 같으면 안 된다" | `dp[i][p]` — p에 직전 선택을 넣는다 |
| "연속으로 k번까지만" | `dp[i][run]` — run은 지금까지 연속 횟수 |
| "쉬는 날/근무 모드가 바뀐다" | `dp[i][mode]` — mode는 지금 어떤 상태인지 |
| "정확히 K개를 쓴다" | `dp[i][k]` — 축을 하나 더 붙인다 |
| "예산/남은 자원이 있다" | `dp[i][rest]` — 남은 양을 축으로 |
| "연속된 구간"(끊기면 안 됨) | `dp[i]` = i를 **반드시 포함**하는 값, 답은 따로 `best` |
| "부분수열"(순서만 지키면 됨) | 연속 제약이 없으니 리셋하지 않는다 |
| "두 문자열/수열을 비교" | `dp[i][j]` — 두 인덱스가 곧 두 축 |
| "몇 번 고쳐야", "최소 연산" | 편집 거리 꼴, 경계는 `i`와 `j` |
| "첫 칸과 마지막 칸이 이웃"(원형) | 첫 상태를 고정하고 K번 반복 |
| "…로 나눈 나머지" | 상태는 그대로, `long long` + 연산마다 `% MOD` |
| "상태가 2~3개뿐이다" | 배열 대신 `long long` 변수 몇 개로 굴린다 |

- 축을 정했으면 도구를 고른다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| i만으로 다음 결정을 못 내린다 | 상태 축 추가 `dp[i][s]` | 부족한 정보를 축으로 승격 | O(n × S) |
| 상태 축 후보가 여러 개 떠오른다 | 미래를 바꾸는 것만 | 축이 늘면 시간·메모리가 곱해진다 | O(n × ΠS) |
| 상태 개수가 컴파일 때 고정 | `vector<array<long long, S>>` | 안쪽 할당이 한 번뿐이라 빠르다 | 공간 O(n·S) |
| 구간이 반드시 연속이어야 한다 | Kadane형 한 줄 전이 | "이어붙이기 vs 새로 시작" 둘뿐 | O(n) |
| 순서만 지키면 되고 연속은 아니다 | LIS형 `dp[i]` + 조건 필터 | 이을 수 있는 후보를 전부 본다 | O(n²) |
| LIS인데 n이 10만 규모다 | `tails` + `lower_bound` | 길이만 필요하면 끝값만 관리하면 충분 | O(n log n) |
| 두 수열의 공통 구조를 잰다 | `dp[i][j]` 표 | 축이 둘이라 2차원이 자연스럽다 | O(n·m) |
| 공통 부분이 **연속**이어야 한다 | 다르면 0으로 리셋 | 이어짐이 끊기면 처음부터 다시 | O(n·m) |
| 표는 크고 역추적은 필요 없다 | 두 행(`prv`, `cur`)만 유지 | 전이가 직전 행만 읽는다 | 공간 O(m) |
| 실제 수열·연산 순서를 복원해야 한다 | 표 전체 보관 후 역추적 | 어느 칸에서 왔는지 되짚어야 한다 | 공간 O(n·m) |
| 원형이라 양 끝이 서로 묶인다 | 시작 상태 고정 × K회 | 고정하면 다시 선형 문제가 된다 | O(K × n × S) |
| `5000 × 5000` 표가 필요하다 | `vector<vector<int>>`·두 줄 압축 | `long long` 2500만 칸은 200MB다 | 공간 주의 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: "상태 축을 하나 더 붙여야 한다"는 신호가 무엇인지, 판정 질문 한 문장으로.
- [ ] 설명할 수 있다: 상태에 과거 정보를 다 넣으면 왜 안 되는지(무엇이 폭발하는지).
- [ ] 설명할 수 있다: `dp[i][s]`에서 s가 "직전 선택"일 때, 금지된 전이가 코드의 어디에 나타나는지.
- [ ] 설명할 수 있다: 두 상태를 동시에 갱신해야 하는 이유와, 굴림 변수에서 어제 값을 복사해야 하는 이유.
- [ ] 설명할 수 있다: 도달 불가 표식으로 `LLONG_MIN`을 그대로 쓰면 왜 안 되고 `LLONG_MIN/4`를 쓰는지.
- [ ] 설명할 수 있다: Kadane의 `cur`가 왜 "i를 반드시 포함하는" 값이어야 하고, 전역 답을 왜 따로 기록하는지.
- [ ] 설명할 수 있다: LIS의 `dp[i]`에 "i를 마지막으로 쓴다"는 제약이 꼭 필요한 이유.
- [ ] 설명할 수 있다: `tails` 배열이 실제 LIS가 아닌데도 길이는 맞는 이유.
- [ ] 설명할 수 있다: `lower_bound`와 `upper_bound`가 중복 값에서 어떻게 갈리는지.
- [ ] 설명할 수 있다: LCS 점화식에서 같을 때 대각선, 다를 때 위·왼쪽을 쓰는 근거.
- [ ] 설명할 수 있다: 부분수열과 연속 부분문자열의 점화식 차이(다를 때 max인가 0인가)와 그 이유.
- [ ] 설명할 수 있다: 편집 거리의 경계 `dp[i][0]=i`, `dp[0][j]=j`가 각각 무슨 연산을 뜻하는지.
- [ ] 설명할 수 있다: 두 문자열 DP에서 `A[i-1]`처럼 1을 빼는 이유.
- [ ] 설명할 수 있다: `string::size()`가 부호 없는 타입이라 `i < s.size() - 1`이 언제 터지는지.
- [ ] 설명할 수 있다: 원형 문제를 시작 상태 고정으로 선형화하는 원리와, 그 대가가 무엇인지.
- [ ] 설명할 수 있다: 2차원 표를 `vector<vector<int>> dp(n)`으로 만들면 왜 범위 밖 접근이 되는지.

**⚠️ 자주 하는 실수**

**1) 상태를 덜 잡고 값만 최적으로 고른다**

```cpp
// ❌ 틀린 코드
// "직전에 고른 것과 같은 색은 못 쓴다"인데 축이 i 하나뿐이다
vector<long long> dp(n, 0);
dp[0] = *max_element(color[0].begin(), color[0].end());
for (int i = 1; i < n; i++)
    dp[i] = dp[i - 1] + *max_element(color[i].begin(), color[i].end());
    // 직전에 무슨 색을 썼는지 모른다
```

왜: `dp[i-1]`은 "i-1까지의 최댓값" 하나로 뭉쳐 있어, 그 최댓값이 어떤 색으로 끝났는지가 지워졌다. 그래서 같은 색을 연달아 쓴 답이 그대로 섞여 들어간다. **i만으로 다음 결정을 못 내린다는 것이 곧 축을 하나 더 붙이라는 신호다.**

```cpp
// ✅ 고친 코드
int K = color[0].size();
vector<vector<long long>> dp(n, vector<long long>(K, 0));   // 축 추가: 마지막 색
for (int c = 0; c < K; c++) dp[0][c] = color[0][c];
for (int i = 1; i < n; i++)
    for (int c = 0; c < K; c++)
        for (int p = 0; p < K; p++)
            if (p != c)                      // 금지된 전이를 여기서 막는다
                dp[i][c] = max(dp[i][c], dp[i - 1][p] + color[i][c]);
cout << *max_element(dp[n - 1].begin(), dp[n - 1].end()) << "\n";
```

**2) 도달 불가 표식으로 `LLONG_MIN`을 그대로 쓴다**

```cpp
// ❌ 틀린 코드
vector<array<long long, S>> dp(n + 1);
for (auto& row : dp) row.fill(LLONG_MIN);    // 여유가 없는 최솟값
dp[0][START] = 0;
for (int i = 1; i <= n; i++)
    for (int s = 0; s < S; s++)
        for (auto [ns, gain] : moves(s, i))
            dp[i][ns] = max(dp[i][ns], dp[i - 1][s] + gain);
            // LLONG_MIN + gain 이 거대한 양수로 뒤집힌다
```

왜: 부호 있는 정수의 오버플로는 예외를 던지지 않고 값을 조용히 감싼다. `LLONG_MIN`에 음수 이익을 더하면 부호가 뒤집혀 아주 큰 양수가 되고, 도달 불가 상태가 오히려 "최고 이익"으로 둔갑해 표 전체를 오염시킨다.

```cpp
// ✅ 고친 코드
const long long NEG = LLONG_MIN / 4;         // 더해도 안 넘치는 여유값
for (auto& row : dp) row.fill(NEG);
dp[0][START] = 0;
for (int i = 1; i <= n; i++)
    for (int s = 0; s < S; s++) {
        if (dp[i - 1][s] == NEG) continue;   // 닫힌 상태에서는 잇지 않는다
        for (auto [ns, gain] : moves(s, i))
            dp[i][ns] = max(dp[i][ns], dp[i - 1][s] + gain);
    }
```

**3) 굴림 변수를 순서대로 덮어써 하루가 어긋난다**

```cpp
// ❌ 틀린 코드
for (int i = 1; i < n; i++) {
    da = A[i] + max(da, db - c);      // da가 '오늘 값'으로 바뀐다
    db = B[i] + max(db, da - c);      // 그 오늘 값을 어제 값인 줄 알고 읽는다
}
```

왜: 두 상태는 **같은 시점의 값**을 서로 참조해야 한다. 첫 줄에서 `da`를 갱신하는 순간 그것은 오늘 값이고, 둘째 줄이 그 오늘 값을 읽으면 "오늘 A에서 오늘 B로 이동"이라는 없는 전이가 생긴다. 답이 조용히 커진다.

```cpp
// ✅ 고친 코드
for (int i = 1; i < n; i++) {
    long long pa = da, pb = db;       // 어제 값을 먼저 복사
    da = A[i] + max(pa, pb - c);
    db = B[i] + max(pb, pa - c);      // 둘 다 어제 값만 읽는다
}
// 배열 두 줄(dp[i-1], dp[i])로 쓰면 이 실수 자체가 생기지 않는다
```

**4) 2차원 표를 안쪽 크기 없이 만든다**

```cpp
// ❌ 틀린 코드
vector<vector<int>> dp(n + 1);        // 빈 행 n+1개 — 안쪽에 칸이 하나도 없다
dp[1][1] = 5;                         // 범위 밖 접근 (정의되지 않은 동작)

// ❌ 또 다른 변형
int dp2[5001][5001];                  // 2500만 칸 * 4바이트 = 100MB, 지역이면 스택
```

왜: `vector<vector<int>> dp(n + 1);`은 "빈 `vector`가 n+1개"라는 뜻이라 `dp[1].size()`가 0이다. `operator[]`는 범위를 검사하지 않으므로 예외 대신 엉뚱한 메모리를 건드려 조용히 망가진다. 큰 고정 배열을 함수 안에 두는 것도 위험하다 — 지역 변수는 스택에 잡히는데 스택은 보통 1~8MB뿐이다.

```cpp
// ✅ 고친 코드
vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));   // 안쪽 크기까지 지정
// 큰 고정 배열이 꼭 필요하면 전역(또는 static)으로 둔다
static int dp2[5001][5001];
// 표가 너무 크면 두 줄만 유지한다: vector<int> prv(m+1), cur(m+1);
```

**5) 편집 거리의 경계를 초기화하지 않는다**

```cpp
// ❌ 틀린 코드
vector<vector<int>> ed(n + 1, vector<int>(m + 1, 0));   // 첫 행·첫 열이 전부 0
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++) {
        if (A[i - 1] == B[j - 1]) ed[i][j] = ed[i - 1][j - 1];
        else ed[i][j] = 1 + min({ed[i-1][j-1], ed[i-1][j], ed[i][j-1]});
    }
```

왜: `ed[i][0]`은 "A의 앞 i글자를 빈 문자열로 만드는 비용"이라 `i`여야 하는데 0으로 깔려 있다. "공짜로 지울 수 있다"는 뜻이 되어 모든 비용이 실제보다 작게 나온다. LCS는 경계가 진짜로 0이라 문제가 없지만, 편집 거리는 다르다.

```cpp
// ✅ 고친 코드
vector<vector<int>> ed(n + 1, vector<int>(m + 1, 0));
for (int i = 0; i <= n; i++) ed[i][0] = i;   // i번 삭제
for (int j = 0; j <= m; j++) ed[0][j] = j;   // j번 삽입
```

**6) 표는 1-based인데 문자열을 0-based로 읽지 않는다**

```cpp
// ❌ 틀린 코드
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++)
        if (A[i] == B[j])                    // i가 n일 때 문자열 끝을 넘어 읽는다
            dp[i][j] = dp[i - 1][j - 1] + 1;
```

왜: `dp[i][j]`의 i는 "A의 앞 i글자를 봤다"는 **개수**이고, `A`의 인덱스는 0부터 세는 **위치**다. i번째 글자는 `A[i-1]`이다. `std::string`의 `operator[]`는 범위를 검사하지 않아 예외가 나지 않고, `A[n]`은 널 문자를 돌려주므로 오류 없이 **조용히 틀린 답**이 나온다.

```cpp
// ✅ 고친 코드
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++)
        if (A[i - 1] == B[j - 1])            // 개수 i -> 위치 i-1
            dp[i][j] = dp[i - 1][j - 1] + 1;
```

**7) 문자열 길이를 부호 없는 값 그대로 비교한다**

```cpp
// ❌ 틀린 코드
for (int i = 0; i < A.size() - 1; i++)       // A가 빈 문자열이면?
    // 0 - 1 이 -1 이 아니라 약 1.8e19 가 되어 루프가 폭주한다

int diff = A.size() - B.size();              // B가 더 길면 거대한 양수가 된다
```

왜: `size()`는 부호 없는 `size_t`를 돌려준다. 부호 없는 뺄셈에서 0보다 작아지는 값은 음수가 아니라 **최댓값 근처로 감싼다**. 게다가 `int`와 `size_t`를 비교하면 `int` 쪽이 부호 없는 쪽으로 승격되어, 음수 인덱스가 거대한 양수로 바뀐다.

```cpp
// ✅ 고친 코드
int n = A.size(), m = B.size();              // 먼저 int로 받아 둔다
for (int i = 0; i + 1 < n; i++)              // 뺄셈 대신 덧셈으로 비교
    ;
int diff = n - m;                            // int끼리라 음수가 제대로 나온다
```

**8) 연속이어야 하는데 부분수열 점화식을 쓴다**

```cpp
// ❌ 틀린 코드
// "가장 긴 공통 부분 '문자열'(연속)"을 묻는데 LCS 식을 그대로 썼다
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++) {
        if (A[i - 1] == B[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
        else dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);   // 끊겼는데 이어받는다
    }
cout << dp[n][m] << "\n";
```

왜: 글자가 다르면 이어짐이 **끊긴다**. 그런데 `max(위, 왼쪽)`은 끊긴 길이를 그대로 물려받아 "연속이 아닌" 답을 센다. 연속 문제는 끊긴 자리를 0으로 리셋해야 하고, 답도 `dp[n][m]`이 아니라 표 전체의 최댓값이다.

```cpp
// ✅ 고친 코드
int best = 0;
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++) {
        if (A[i - 1] == B[j - 1]) {
            dp[i][j] = dp[i - 1][j - 1] + 1;
            best = max(best, dp[i][j]);      // 끝나는 위치가 어디든 후보다
        } else {
            dp[i][j] = 0;                    // 끊기면 처음부터 다시
        }
    }
cout << best << "\n";
```

**다음 챕터로**

- 상태 설계는 여기서 끝나지 않는다. 축이 "위치 + 부가 정보"에서 "집합"이나 "구간"으로 넓어지면 비트마스크 DP·구간 DP가 되고, 축이 그래프의 정점이 되면 최단 경로가 된다. 판정 질문은 그대로다 — "지금 결정을 내리려면 무엇을 알아야 하는가."
- 반대로 축이 늘수록 상태 수가 곱해지므로, "이 정보를 정말 기억해야 하는가"를 되묻는 습관이 그대로 성능이 된다. Ch6에서 익힌 "최소한의 과거 정보"라는 기준이 그 판단의 근거다.
- C++에서는 그 곱셈이 곧 메모리다. 축을 하나 더 붙이기 전에 `상태 수 × 원소 크기`를 먼저 계산해 보고, 넘칠 것 같으면 `int`·`char`로 타입을 줄이거나 두 줄 압축으로 축 하나를 지우는 선택지를 함께 검토한다.
