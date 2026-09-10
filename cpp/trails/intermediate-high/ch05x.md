## L5. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch05(Advanced DP)의 핵심 — 양방향으로 훑는 Bitonic DP, 짧은 구간에서 긴 구간으로 올라가는 구간 DP, 집합을 정수로 다루는 비트마스크, 방문 상태를 압축하는 Bitmask DP — 를 소재만 바꿔 **반복 훈련**하고, 코딩테스트 단골 DP 유형으로 **확장**하는 연습 세트다.
- **반복 훈련 개념**:
  - 양방향 결합: 왼쪽에서 `inc[i]`(i에서 끝나는 증가), 오른쪽에서 `dec[i]`(i에서 시작하는 감소)를 따로 채우고 꼭대기 `i`에서 `inc[i] + dec[i] - 1`로 합친다.
  - 구간 DP 뼈대: `for (int len = 2; len <= n; len++) for (int i = 0; i + len - 1 < n; i++) { int j = i + len - 1; for (int k = i; k < j; k++) dp[i][j] = best(dp[i][k] + dp[k+1][j] + cost); }`. 바깥 루프는 반드시 길이.
  - 비트마스크 기본: 포함 여부 `(mask >> i) & 1`, 추가 `mask | (1 << i)`, 최하위 비트 `mask & (-mask)`, 그 인덱스 `__builtin_ctz(mask)`, 크기 `__builtin_popcount(mask)`.
  - **비트 연산 우선순위**: C++에서 `&`는 `==`보다 **낮다**. `mask & 1 == 0`은 `mask & (1 == 0)`으로 묶여 항상 0이 된다(파이썬은 정반대라 그대로 동작한다). 비트 조건에는 무조건 괄호를 친다. 또 `1 << n`의 `1`은 `int`라 n이 31 이상이면 `1LL << n`으로 써야 한다.
  - Bitmask DP: `vector<vector<int>> dp(1 << n, vector<int>(n, INF))`. `mask`를 오름차순으로 돌면 부분집합이 먼저 계산되므로 forward 갱신이 안전하다. `memset(dp, INF, ...)`은 **바이트 단위**라 0과 -1 외의 값으로는 채울 수 없다.
  - 마스크별 합 O(2^n): `ssum[mask] = ssum[mask ^ low] + a[__builtin_ctz(mask)]` — 원소를 매번 다시 더하지 않는다.
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '동적 계획법 3' 단계, NeetCode 150의 '2-D DP'·'Bit Manipulation' 유형, 삼성 SW 역량테스트의 'BFS + 순열/비트마스크' 조합 문제가 이 챕터 유형을 낸다.
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 가장 긴 산 모양 부분수열 | Easy | 양방향 LIS 결합(길이) | 반복 훈련 |
| 2 | 산 모양 만들기 최소 제거 | Medium | 양방향 LIS 결합 + 양쪽 필수 조건 | 반복 훈련 |
| 3 | 양 끝 카드 뽑기 게임 | Medium | 구간 DP(점수 차 상태) | 유형 확장 (NeetCode '2-D DP' 스타일) |
| 4 | 팰린드롬 최소 삽입 | Medium | 구간 DP(양끝 비교) | 반복 훈련 |
| 5 | 초대 가능한 손님 조합 수 | Medium | 마스크 전체 열거 + 최하위 비트 DP | 반복 훈련 |
| 6 | 창고 출발 배달 경로 | Medium | Bitmask DP(외판원 축소판, 복귀 없음) | 반복 훈련 |
| 7 | 카드 제거 점수 최대화 | Hard | 구간 DP("마지막에 제거되는 것" 분할) | 유형 확장 (NeetCode '2-D DP' 스타일) |
| 8 | K개 팀 균등 분할 | Hard | 마스크별 합 DP + 도달 가능 DP | 유형 확장 (NeetCode 'Bit Manipulation' 스타일) |
| 9 | 청소 로봇 최소 이동 | Hard | BFS 거리표 + Bitmask DP | 유형 확장 (삼성 SW 역량테스트 스타일) |
| 10 | 최단 공통 초문자열 길이 | Hard | 겹침 계산 + Bitmask DP | 유형 확장 (NeetCode '2-D DP' 스타일) |

**문제**

**1) 가장 긴 산 모양 부분수열** · Easy

- **요구사항**: 길이 `n` 수열에서 원소 몇 개를 골라(순서 유지) **엄격히 증가하다가 엄격히 감소하는** 부분수열을 만든다. 꼭대기 하나를 기준으로 왼쪽은 증가, 오른쪽은 감소이며 한쪽이 비어 있어도 된다(순증가·순감소 허용). 가능한 최대 길이를 구하라.
- **입력**: 첫 줄 `n` (1 ≤ n ≤ 1,000), 둘째 줄 정수 n개 (절댓값 ≤ 10^6).
- **출력**: 최대 길이.
- **예제**: `7 / 1 3 2 5 4 2 1` → `6` · `4 / 5 4 3 2` → `4`
- **셀프체크**: `inc[i]`(i에서 끝나는 최장 증가)와 `dec[i]`(i에서 시작하는 최장 감소)를 각각 O(n^2)로 채우고 `inc[i] + dec[i] - 1`의 최댓값. 꼭대기를 두 번 세지 않도록 1을 빼는가? 같은 값은 증가도 감소도 아니므로(엄격) `2 2 2`의 답은 1이다. `dec`는 오른쪽에서 왼쪽으로 채워야 한다 — 역주행 루프의 인덱스를 `int`로 두었는가(`size_t`로 두면 0에서 감소해 감싸 돌아 무한 루프가 된다)?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    vector<int> inc(n, 1);        // i에서 끝나는 최장 엄격 증가 부분수열 길이
    vector<int> dec(n, 1);        // i에서 시작하는 최장 엄격 감소 부분수열 길이
    for (int i = 0; i < n; i++)
        for (int j = 0; j < i; j++)
            if (a[j] < a[i] && inc[j] + 1 > inc[i]) inc[i] = inc[j] + 1;
    for (int i = n - 1; i >= 0; i--)
        for (int j = i + 1; j < n; j++)
            if (a[j] < a[i] && dec[j] + 1 > dec[i]) dec[i] = dec[j] + 1;
    int best = 0;
    for (int i = 0; i < n; i++) best = max(best, inc[i] + dec[i] - 1);
    cout << best << '\n';
    return 0;
}
@@TESTS
--IN
7
1 3 2 5 4 2 1
--OUT
6
--IN
4
5 4 3 2
--OUT
4
--IN
3
2 2 2
--OUT
1
@@EXPL
(1) 접근·핵심 아이디어

- 산 모양 부분수열은 꼭대기 `i`를 기준으로 "i에서 끝나는 증가 부분수열"과 "i에서 시작하는 감소 부분수열"의 결합이다. 각각의 최장 길이를 알면 꼭대기별 최대 길이는 `inc[i] + dec[i] - 1`(꼭대기 중복 제거).
- `inc`는 LIS 점화식(`a[j] < a[i]`인 `j < i` 중 최대 + 1), `dec`는 같은 점화식을 오른쪽에서 왼쪽으로 적용한 것. 각각 O(n^2), n ≤ 1,000이면 충분하다.
- 한쪽이 비어 있으면 `inc` 또는 `dec`가 1이므로 순증가·순감소가 자연히 포함된다.

(2) 코드 단계별

- `inc`, `dec`를 1로 초기화(`vector<int> inc(n, 1)`).
- `i`를 왼쪽부터 돌며 `j < i`, `a[j] < a[i]`이면 `inc[i] = max(inc[i], inc[j] + 1)`.
- `i`를 오른쪽부터 돌며 `j > i`, `a[j] < a[i]`이면 `dec[i] = max(dec[i], dec[j] + 1)`.
- `max(inc[i] + dec[i] - 1)` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "증가 후 감소" → 꼭대기를 고정하고 좌·우로 쪼개는 양방향 DP.
- 각 방향은 LIS 그대로. 감소 쪽은 배열을 뒤집어 LIS를 돌린 것과 같다.
- C++ 함정: 역방향 루프 변수는 반드시 부호 있는 타입으로. `for (size_t i = n - 1; i >= 0; i--)`는 `i`가 0일 때도 조건이 참이고 다음 감소에서 거대한 값으로 감싸 돌아 범위 밖을 읽는다. 배열 이름을 `dec`로 지어도 표준과 충돌하지 않지만(`std::dec`는 입출력 조작자다) `cout << dec`를 함께 쓰는 코드에서는 헷갈리니 주의한다.
- 엄격 비교(`<`)와 꼭대기 중복 제거(`-1`), 전부 같은 값일 때 1을 확인.
```

**2) 산 모양 만들기 최소 제거** · Medium

- **요구사항**: 길이 `n` 수열에서 원소 몇 개를 **제거**해 남은 수열이 산 모양이 되게 한다. 여기서 산 모양은 꼭대기 하나가 있고, 꼭대기 **왼쪽에 1개 이상**·**오른쪽에 1개 이상**의 원소가 있으며, 왼쪽은 엄격 증가·오른쪽은 엄격 감소인 수열이다. 필요한 최소 제거 개수를 구하라. 불가능하면 `-1`.
- **입력**: 첫 줄 `n` (1 ≤ n ≤ 1,000), 둘째 줄 정수 n개.
- **출력**: 최소 제거 개수 또는 `-1`.
- **예제**: `8 / 2 1 1 5 6 2 3 1` → `3` · `3 / 1 2 3` → `-1`
- **셀프체크**: 1번과 같은 `inc`/`dec`를 쓰되, 꼭대기 후보는 **`inc[i] >= 2`이고 `dec[i] >= 2`**인 `i`로 제한된다(양쪽에 실제 원소가 있어야 하므로). 남기는 최대 개수 `inc[i] + dec[i] - 1`을 구해 `n - 최대`가 답. 후보가 하나도 없으면 `-1`(순증가·순감소만 가능한 경우). 이미 산 모양(`1 3 2`)이면 0.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    vector<int> inc(n, 1), dec(n, 1);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < i; j++)
            if (a[j] < a[i] && inc[j] + 1 > inc[i]) inc[i] = inc[j] + 1;
    for (int i = n - 1; i >= 0; i--)
        for (int j = i + 1; j < n; j++)
            if (a[j] < a[i] && dec[j] + 1 > dec[i]) dec[i] = dec[j] + 1;
    int keep = 0;
    for (int i = 0; i < n; i++)
        if (inc[i] >= 2 && dec[i] >= 2)          // 양쪽에 원소가 실제로 있는 꼭대기만
            keep = max(keep, inc[i] + dec[i] - 1);
    cout << (keep > 0 ? n - keep : -1) << '\n';
    return 0;
}
@@TESTS
--IN
8
2 1 1 5 6 2 3 1
--OUT
3
--IN
3
1 2 3
--OUT
-1
--IN
3
1 3 2
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- "최소 제거"는 "최대 유지"와 같다. 남길 수 있는 가장 긴 산 모양 부분수열 길이 `keep`을 구하면 답은 `n - keep`.
- 산 모양의 최대 길이는 꼭대기별 `inc[i] + dec[i] - 1`인데, 이 문제는 양쪽이 비어 있으면 안 되므로 `inc[i] >= 2`(왼쪽에 최소 1개)와 `dec[i] >= 2`(오른쪽에 최소 1개)를 동시에 만족하는 꼭대기만 후보다.
- 후보가 없으면 어떤 제거로도 산을 못 만드니 `-1`. 첫 예제는 `1 5 6 3 1`(꼭대기 6)을 남겨 3개 제거.

(2) 코드 단계별

- `inc`, `dec`를 1번 문제와 동일하게 O(n^2)로 채운다.
- 조건 `inc[i] >= 2 && dec[i] >= 2`인 `i`에 대해서만 `inc[i] + dec[i] - 1`의 최댓값 `keep`을 갱신.
- `keep`이 0이면 `-1`, 아니면 `n - keep`. 삼항 연산자의 두 갈래 타입이 모두 `int`라 그대로 출력할 수 있다.

(3) 스스로 다시 짤 때 생각 순서

- "제거 최소" → "유지 최대"로 뒤집는다. 유지 대상이 산 모양이므로 양방향 DP 재사용.
- 요구 조건(양쪽 필수)을 후보 필터로 옮긴다 — 점화식은 그대로, 답을 고르는 조건만 바뀐다.
- C++ 함정: 논리 AND는 `&&`이고 비트 AND는 `&`다. `inc[i] >= 2 & dec[i] >= 2`라고 써도 여기서는 우연히 같은 결과가 나오지만(`>=`가 `&`보다 우선순위가 높아 두 bool의 비트 AND가 된다), 단축 평가가 사라져 오른쪽이 항상 평가되므로 범위 검사 같은 방어 코드에서는 곧바로 사고가 된다.
- 순증가만 있는 입력(`-1`), 이미 산인 입력(0)으로 확인.
```

**3) 양 끝 카드 뽑기 게임** · Medium

- **요구사항**: 일렬로 놓인 카드 `n`장에 점수가 적혀 있다. 두 사람이 번갈아 **왼쪽 끝 또는 오른쪽 끝** 카드 한 장을 가져간다. 둘 다 자기 점수 합을 최대화하도록 최선을 다할 때, **먼저 시작하는 사람**의 최종 점수 합을 구하라.
- **입력**: 첫 줄 `n` (1 ≤ n ≤ 100), 둘째 줄 카드 점수 n개 (1 ≤ 점수 ≤ 1,000).
- **출력**: 선공의 최종 점수.
- **예제**: `4 / 1 5 2 3` → `8` · `3 / 10 100 10` → `20`
- **셀프체크**: 상태를 "구간 `[i, j]`가 남았을 때 **지금 차례인 사람 − 상대**의 최대 점수 차"로 잡으면 상대의 최선이 자동으로 반영된다: `dp[i][j] = max(a[i] - dp[i+1][j], a[j] - dp[i][j-1])`. 선공 점수는 `(전체 합 + dp[0][n-1]) / 2`이고, 합과 차가 모두 음이 아니라 C++의 `/`(0 방향 절단)와 파이썬의 `//`(내림)가 여기서는 같은 값을 준다. 둘째 예제에서 100을 탐내 양 끝 중 아무거나 집으면 상대가 100을 가져가므로 선공은 20밖에 못 얻는다 — 그리디(큰 쪽 집기)가 틀리는 이유다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    // dp[i][j] = 구간 [i, j]에서 "지금 차례인 사람 − 상대"의 최대 점수 차
    vector<vector<int>> dp(n, vector<int>(n, 0));
    for (int i = 0; i < n; i++) dp[i][i] = a[i];
    for (int len = 2; len <= n; len++) {
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            int takeLeft = a[i] - dp[i + 1][j];
            int takeRight = a[j] - dp[i][j - 1];
            dp[i][j] = max(takeLeft, takeRight);
        }
    }
    int total = 0;
    for (int x : a) total += x;
    cout << (total + dp[0][n - 1]) / 2 << '\n';
    return 0;
}
@@TESTS
--IN
4
1 5 2 3
--OUT
8
--IN
3
10 100 10
--OUT
20
--IN
1
7
--OUT
7
@@EXPL
(1) 접근·핵심 아이디어

- 두 사람이 번갈아 최선을 다하는 게임은 "내 점수"만 상태로 두면 상대의 선택을 표현하기 어렵다. 대신 **차이**를 상태로 두면 한 사람의 관점만으로 충분하다: 내가 `a[i]`를 가져가면 남은 구간에서는 상대가 선공이 되고, 그 구간의 차이 `dp[i+1][j]`만큼 상대가 유리해지므로 내 순차이는 `a[i] - dp[i+1][j]`.
- 구간 `[i, j]`의 답은 안쪽 구간 `[i+1, j]`, `[i, j-1]`에서 나오므로 길이가 짧은 구간부터 채우는 구간 DP. O(n^2).
- 최종 차이 `D = dp[0][n-1]`, 합 `S`에서 선공 점수는 `(S + D) / 2`(항상 정수).

(2) 코드 단계별

- 2차원 DP는 `vector<vector<int>> dp(n, vector<int>(n, 0))`로 잡는다. 길이 1 구간은 `dp[i][i] = a[i]`.
- 길이 2부터 n까지, 각 `[i, j]`에서 왼쪽 집기 `a[i] - dp[i+1][j]`와 오른쪽 집기 `a[j] - dp[i][j-1]` 중 최댓값.
- `(total + dp[0][n-1]) / 2` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "번갈아 + 양 끝 + 최선" → 구간 게임 DP. 상태는 점수 차로 잡는다는 관용 패턴.
- C++ 함정: 정수 나눗셈의 방향이 파이썬과 다르다. 파이썬 `//`는 항상 내림이라 `-7 // 2 == -4`지만 C++의 `/`는 0 쪽으로 자르므로 `-7 / 2 == -3`이다(나머지도 부호가 다르다). 이 문제는 `total + D`가 음이 아님을 먼저 확인했기에 그대로 옮겨도 안전하지만, 음수가 섞이는 식이라면 반드시 손으로 검산해야 한다.
- 카드 1장, `10 100 10`처럼 그리디가 실패하는 예로 검산.
```

**4) 팰린드롬 최소 삽입** · Medium

- **요구사항**: 문자열 `s`의 **아무 위치**에나 문자를 삽입해 팰린드롬으로 만들 때 필요한 최소 삽입 횟수를 구하라.
- **입력**: 한 줄에 소문자 문자열 `s` (1 ≤ |s| ≤ 500).
- **출력**: 최소 삽입 횟수.
- **예제**: `mbadm` → `2` · `leetcode` → `5`
- **셀프체크**: `dp[i][j]` = `s[i..j]`를 팰린드롬으로 만드는 최소 삽입 수. 양 끝이 같으면 안쪽 문제 `dp[i+1][j-1]`과 같고, 다르면 한쪽 끝을 짝 맞춰 주는 삽입 1회 + `min(dp[i+1][j], dp[i][j-1])`. 길이 2에서 `dp[i+1][j-1]`은 `i+1 > j-1`인 빈 구간이니 0으로 취급(그대로 인덱싱하면 `dp[i+1][i]`를 읽게 되는데, 0으로 초기화돼 있어 우연히 맞지만 조건으로 분명히 갈라 두는 편이 낫다). 이미 팰린드롬(`zzazz`)이면 0.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    int n = (int)s.size();
    // dp[i][j] = s[i..j]를 팰린드롬으로 만드는 최소 삽입
    vector<vector<int>> dp(n, vector<int>(n, 0));
    for (int len = 2; len <= n; len++) {
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            if (s[i] == s[j]) dp[i][j] = (len > 2) ? dp[i + 1][j - 1] : 0;
            else dp[i][j] = 1 + min(dp[i + 1][j], dp[i][j - 1]);
        }
    }
    cout << dp[0][n - 1] << '\n';
    return 0;
}
@@TESTS
--IN
mbadm
--OUT
2
--IN
leetcode
--OUT
5
--IN
zzazz
--OUT
0
--IN
a
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 구간 `[i, j]`의 양 끝을 본다. `s[i] == s[j]`면 두 글자는 이미 짝이므로 안쪽 `[i+1, j-1]`만 해결하면 된다. 다르면 둘 중 하나를 반대편에 복사해 넣어 짝을 만들고(삽입 1회) 남은 구간 `[i+1, j]` 또는 `[i, j-1]`을 해결하는 두 선택 중 최소.
- 안쪽·짧은 구간이 먼저 필요하므로 길이 오름차순 구간 DP. O(n^2) 시간·공간, n ≤ 500이면 충분.
- 길이 1은 0(이미 팰린드롬), 길이 2에서 두 글자가 같으면 0.

(2) 코드 단계별

- `dp`를 0으로 초기화(길이 1 = 0).
- 길이 2..n, 시작 `i`마다 `j = i + len - 1`. 같으면 `dp[i+1][j-1]`(길이 2면 0), 다르면 `1 + min(dp[i+1][j], dp[i][j-1])`.
- `dp[0][n-1]` 출력. n = 1이면 루프가 한 번도 안 돌고 `dp[0][0] = 0`.

(3) 스스로 다시 짤 때 생각 순서

- "양끝을 맞춰 가는 문자열 변형" → 양끝 비교형 구간 DP(팰린드롬 분할과는 상태가 다름: 구간 전체가 답).
- C++ 함정: `vector<vector<int>> dp(n, vector<int>(n))`은 안쪽 벡터가 값 초기화되어 0으로 채워지지만, `int dp[500][500];`처럼 지역 배열로 잡으면 **초기화되지 않은 쓰레기 값**이 들어 있다. 전역이면 0으로 초기화되고 지역이면 아니라는 차이를 기억하고, 필요하면 `= {}`를 붙이거나 `memset(dp, 0, sizeof dp)`로 채운다(0은 `memset`으로 안전한 몇 안 되는 값이다).
- 이미 팰린드롬인 문자열과 한 글자로 0이 나오는지 확인. 답은 `n - (최장 팰린드롬 부분수열)`과도 같다는 사실로 교차 검산 가능.
```

**5) 초대 가능한 손님 조합 수** · Medium

- **요구사항**: 손님 후보 `n`명(0..n-1) 중 일부를 초대한다. 서로 싫어하는 쌍 `m`개가 주어지며, 싫어하는 두 사람을 **동시에** 초대할 수는 없다. 가능한 초대 조합의 수(아무도 안 부르는 경우 포함)와, 그중 가장 많은 인원을 출력하라.
- **입력**: 첫 줄 `n m` (1 ≤ n ≤ 16, 0 ≤ m ≤ n(n-1)/2), 이후 m줄 `x y`(서로 다른 두 사람).
- **출력**: `조합 수 최대 인원`을 공백으로.
- **예제**: `3 1 / 0 1` → `6 2` · `4 0` → `16 4`
- **셀프체크**: 각 사람의 "싫어하는 상대 집합"을 마스크 `adj[i]`로 만들어 두면 조합 `mask`가 가능한지는 마스크 연산으로 판정된다. 마스크마다 켜진 비트를 전부 확인하면 O(2^n · n)이지만, **최하위 비트 하나를 뗀 부분집합** `rest`가 가능하고 `(adj[low] & rest) == 0`이면 `mask`도 가능하다는 관계로 `ok[mask]`를 O(1)에 채울 수 있다(부분집합이 먼저 계산되도록 오름차순). **`adj[i] & rest == 0`처럼 괄호를 빼면 `adj[i] & (rest == 0)`으로 묶여 조용히 틀린다** — C++에서 `&`는 `==`보다 우선순위가 낮다. 공집합도 세는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<int> adj(n, 0);
    for (int i = 0; i < m; i++) {
        int x, y;
        cin >> x >> y;
        adj[x] |= (1 << y);
        adj[y] |= (1 << x);
    }
    vector<char> ok(1 << n, 0);
    ok[0] = 1;
    int count = 1;                     // 공집합
    int best = 0;
    for (int mask = 1; mask < (1 << n); mask++) {
        int low = mask & (-mask);              // 가장 낮은 켜진 비트
        int i = __builtin_ctz(mask);           // 그 비트의 인덱스
        int rest = mask ^ low;                 // low를 뺀 나머지 집합
        if (ok[rest] && (adj[i] & rest) == 0) {   // 괄호 필수
            ok[mask] = 1;
            count++;
            best = max(best, __builtin_popcount(mask));
        }
    }
    cout << count << ' ' << best << '\n';
    return 0;
}
@@TESTS
--IN
3 1
0 1
--OUT
6 2
--IN
4 0
--OUT
16 4
--IN
2 1
0 1
--OUT
3 1
--IN
3 3
0 1
1 2
0 2
--OUT
4 1
@@EXPL
(1) 접근·핵심 아이디어

- n ≤ 16이므로 모든 조합 `2^n`개를 마스크로 열거한다. 조합이 유효하려면 포함된 모든 `i`에 대해 `(adj[i] & mask) == 0`(싫어하는 사람이 함께 없음)이어야 한다.
- 매 마스크마다 원소를 전부 검사하는 대신, `mask`에서 최하위 비트 `low`(사람 `i`)를 뗀 `rest`를 보면 "`rest`가 유효하고 `i`가 `rest`의 누구와도 충돌하지 않음"이 `mask`의 유효성과 동치다. `rest < mask`이므로 오름차순 순회에서 이미 계산돼 있어 O(1). 전체 O(2^n).
- 첫 예제: {}, {0}, {1}, {2}, {0,2}, {1,2} 6가지, 최대 2명.

(2) 코드 단계별

- 싫어하는 쌍을 양방향으로 `adj` 마스크에 기록.
- `ok[0] = 1`, `count = 1`로 시작. `mask`를 1부터 오름차순으로 돌며 `low = mask & (-mask)`, `i = __builtin_ctz(mask)`, `rest = mask ^ low`.
- `ok[rest] && (adj[i] & rest) == 0`이면 `ok[mask] = 1`, 개수 증가, `__builtin_popcount(mask)`로 인원 최댓값 갱신.
- `count best` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "n ≤ 16, 조건 만족 부분집합 세기" → 마스크 전체 열거.
- C++ 함정: **비트 연산 우선순위**가 파이썬과 정반대다. C++은 `&` < `==`이라 `adj[i] & rest == 0`이 `adj[i] & (rest == 0)`으로 묶이고, 파이썬은 `&` > `==`이라 같은 문장이 `(adj[i] & rest) == 0`으로 묶인다. 파이썬 코드를 옮길 때 가장 자주 나오는 조용한 버그이므로 비트 조건에는 늘 괄호를 친다.
- `__builtin_ctz(0)`은 정의되지 않은 동작이라 `mask`가 1부터 시작하는 것이 중요하다. `mask & (-mask)`는 `int`가 2의 보수라서 성립하는 관용구이고, 부호 없는 타입에서도 잘 동작한다.
- 공집합 포함 여부, `m = 0`(전부 가능 = 2^n), 모두가 서로 싫어함(n+1가지, 최대 1명) 경계 확인.
```

**6) 창고 출발 배달 경로** · Medium

- **요구사항**: 지점 `n`개(0번이 창고)와 지점 간 이동 비용 `cost[i][j]`(비대칭 가능)가 주어진다. 창고에서 출발해 **모든 지점을 정확히 한 번씩** 방문하되 **창고로 돌아올 필요는 없다**. 최소 총 비용을 구하라.
- **입력**: 첫 줄 `n` (1 ≤ n ≤ 10), 이후 n줄에 n×n 비용 행렬 (0 ≤ cost ≤ 1,000, 대각선 0).
- **출력**: 최소 비용.
- **예제**: `4 / 0 3 8 4 / 3 0 2 9 / 8 2 0 5 / 4 9 5 0` → `10` · `2 / 0 7 / 3 0` → `7`
- **셀프체크**: `dp[mask][u]` = "mask의 지점들을 방문했고 현재 u"의 최소 비용, `dp[1][0] = 0`에서 시작. 외판원 순회와의 차이는 **마지막에 창고로 돌아오는 비용을 더하지 않고** `min(dp[full][u])`로 끝내는 것뿐이다. INF는 `memset`으로 채울 수 없으니 `vector<vector<int>> dp(1 << n, vector<int>(n, INF))`로 값을 직접 주었는가? `n = 1`이면 창고만 있으므로 0. 비대칭 비용이므로 `cost[u][v]` 방향을 헷갈리지 마라.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<vector<int>> cost(n, vector<int>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) cin >> cost[i][j];

    const int INF = 1e9;
    int full = (1 << n) - 1;
    // memset으로는 INF를 채울 수 없다(바이트 단위라 0과 -1만 안전)
    vector<vector<int>> dp(1 << n, vector<int>(n, INF));
    dp[1][0] = 0;                          // 창고(0)만 방문, 창고에 있음
    for (int mask = 0; mask < (1 << n); mask++) {
        for (int u = 0; u < n; u++) {
            int cur = dp[mask][u];
            if (cur == INF) continue;
            for (int v = 0; v < n; v++) {
                if ((mask >> v) & 1) continue;      // 괄호 필수
                int nm = mask | (1 << v);
                int nc = cur + cost[u][v];
                if (nc < dp[nm][v]) dp[nm][v] = nc;
            }
        }
    }
    cout << *min_element(dp[full].begin(), dp[full].end()) << '\n';
    return 0;
}
@@TESTS
--IN
4
0 3 8 4
3 0 2 9
8 2 0 5
4 9 5 0
--OUT
10
--IN
2
0 7
3 0
--OUT
7
--IN
1
0
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 방문 집합을 마스크로 압축한 `dp[mask][u]`(mask를 방문했고 현재 u에 있을 때 최소 비용)는 외판원 순회와 같다. 시작이 창고 0으로 고정이므로 `dp[1][0] = 0`.
- 복귀가 없으므로 답은 전체 집합 `full`에서 **어느 지점에서 끝나든** 최소: `min(dp[full][u])`. 복귀 비용 `cost[u][0]`을 더하지 않는 것이 유일한 차이다.
- 상태 `2^n · n`, 전이 `n` → O(2^n · n^2). n ≤ 10이면 약 10만 단위.

(2) 코드 단계별

- 비용 행렬을 읽고 `dp`를 INF로, `dp[1][0] = 0`.
- `mask` 오름차순, 현재 위치 `u`(도달 가능한 것만), 미방문 `v`로 `dp[mask | (1<<v)][v]`를 `dp[mask][u] + cost[u][v]`로 완화.
- `*min_element(dp[full].begin(), dp[full].end())` 출력. 파이썬의 `min(리스트)`에 대응하는 C++ 표준 알고리즘은 **반복자를 돌려주는** `min_element`라 `*`로 값을 꺼내야 한다.

(3) 스스로 다시 짤 때 생각 순서

- "모든 지점 한 번씩 + n ≤ 10" → 비트마스크 TSP 계열. "복귀 없음"이라는 조건이 답 계산 방식만 바꾼다.
- 시작 고정(마스크 1, 위치 0)과 종료 조건(전체 마스크, 위치 자유)을 먼저 정한다.
- C++ 함정: INF를 `INT_MAX`로 두면 `cur + cost`가 오버플로할 수 있어 `1e9`처럼 "더해도 `int` 안에 남는" 값을 쓰는 것이 관례다. 그리고 그 값은 `memset`으로 못 채운다 — `memset`은 **바이트를 반복**하므로 `int` 배열에 넣을 수 있는 의미 있는 값은 0(0x00)과 -1(0xff), 그리고 관용적으로 쓰는 0x3f3f3f3f 정도다.
- 비대칭 행렬에서 `cost[u][v]` 방향, INF 상태에서의 전이 생략을 확인.
```

**7) 카드 제거 점수 최대화** · Hard

- **요구사항**: 일렬로 놓인 카드 `n`장에 양의 정수가 적혀 있다. 카드 하나를 제거하면 `(왼쪽 이웃 값) × (그 카드 값) × (오른쪽 이웃 값)`의 점수를 얻고, 이웃이 없는 쪽은 값 1로 계산한다. 제거 후 양옆이 새로 이웃이 된다. 모든 카드를 제거할 때 얻을 수 있는 **최대 총점**을 구하라.
- **입력**: 첫 줄 `n` (1 ≤ n ≤ 100), 둘째 줄 카드 값 n개 (1 ≤ 값 ≤ 100).
- **출력**: 최대 총점.
- **예제**: `4 / 3 1 5 8` → `167` · `2 / 2 3` → `9`
- **셀프체크**: "처음에 무엇을 제거할까"로 나누면 양옆이 계속 바뀌어 상태가 안 잡힌다. 대신 양끝에 값 1인 가상 카드를 붙이고 **열린 구간 `(i, j)`에서 마지막에 제거되는 카드 `k`**를 고르면, 그 순간 `k`의 이웃은 정확히 `i`와 `j`다: `dp[i][j] = max(dp[i][k] + dp[k][j] + b[i]*b[k]*b[j])`. 구간 폭 `j - i`가 작은 것부터 채운다. 값이 100이고 카드가 100장이면 총점이 `int` 상한 근처까지 갈 수 있으니 `long long`으로 받았는가? `2 3`은 2를 먼저(1·2·3=6) 지우고 3(1·3·1=3)을 지워 9가 최대인지 손검산.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> b(n + 2, 1);          // 양끝 가상 카드(값 1)
    for (int i = 1; i <= n; i++) cin >> b[i];
    int m = n + 2;
    // dp[i][j] = 열린 구간 (i, j) 안 카드를 모두 제거한 최대 점수
    vector<vector<long long>> dp(m, vector<long long>(m, 0));
    for (int len = 2; len < m; len++) {     // len = j - i
        for (int i = 0; i + len < m; i++) {
            int j = i + len;
            long long best = 0;
            for (int k = i + 1; k < j; k++) {   // k = (i, j) 안에서 마지막에 제거되는 카드
                long long v = dp[i][k] + dp[k][j] + b[i] * b[k] * b[j];
                if (v > best) best = v;
            }
            dp[i][j] = best;
        }
    }
    cout << dp[0][m - 1] << '\n';
    return 0;
}
@@TESTS
--IN
4
3 1 5 8
--OUT
167
--IN
2
2 3
--OUT
9
--IN
1
5
--OUT
5
@@EXPL
(1) 접근·핵심 아이디어

- 제거 순서에 따라 이웃이 바뀌므로 "먼저 제거할 것"을 고르면 부분 문제가 독립적이지 않다. 반대로 **마지막에 제거할 카드 `k`**를 고르면, 그때 `k`의 양옆은 구간 밖 경계 `i`, `j`로 확정되고, 그 전에 `(i, k)`와 `(k, j)` 안쪽은 서로 영향 없이 독립적으로 제거된다.
- 양끝에 값 1인 가상 카드를 붙여 경계 처리를 없앤다: `dp[i][j] = max over k of dp[i][k] + dp[k][j] + b[i]*b[k]*b[j]`, 열린 구간이라 `dp[i][i+1] = 0`.
- 구간 폭이 작은 것부터 채우는 구간 DP, O(n^3). n ≤ 100이면 약 100만 번의 내부 연산.

(2) 코드 단계별

- `b`를 크기 `n + 2`에 전부 1로 만들고 1..n에 입력을 채우면 `[1] + a + [1]`과 같은 배열이 된다.
- `len = j - i`를 2부터 `m - 1`까지, 각 `i`에 대해 `j = i + len`, `k`를 `i+1..j-1`로 돌며 최댓값.
- `dp[0][m-1]` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "제거하면 이웃이 바뀐다" → 처음이 아니라 **마지막** 선택으로 분할하는 구간 DP 관용구.
- 가상 경계 카드를 붙여 "이웃 없음 = 1"을 코드에서 없앤다. 열린 구간이라 `k`의 범위와 base(폭 1 = 0)를 정확히.
- C++ 함정: `b`를 `vector<int>`로 두면 `b[i] * b[k] * b[j]`가 `int` 곱셈으로 계산된 뒤에야 `long long`에 대입되므로, 중간 결과가 21억을 넘으면 이미 망가진 값이 들어간다. **곱셈에 참여하는 값 자체를 `long long`으로 두거나** `(long long)b[i] * b[k] * b[j]`처럼 첫 항을 캐스팅해 승격시켜야 한다.
- 카드 1장(`1·5·1 = 5`), 2장 손검산으로 점화식 방향을 확인.
```

**8) K개 팀 균등 분할** · Hard

- **요구사항**: 양의 정수 `n`개를 **모두 사용**해 `K`개의 비어 있지 않은 그룹으로 나누되 모든 그룹의 합이 같게 할 수 있는지 판정하라.
- **입력**: 첫 줄 `n K` (1 ≤ K ≤ n ≤ 16), 둘째 줄 양의 정수 n개 (각 ≤ 10,000).
- **출력**: 가능하면 `YES`, 아니면 `NO`.
- **예제**: `4 2 / 1 5 11 5` → `YES` · `4 3 / 1 2 3 4` → `NO`
- **셀프체크**: 전체 합이 K로 나눠떨어지지 않으면 즉시 `NO`. 목표 `target = 합 / K`. `ok[mask]` = "mask의 원소들을 순서대로 담아 **완성된 그룹 몇 개 + 채우는 중인 그룹 하나**로 만들 수 있다"로 정의하면, 채우는 중인 그룹의 현재 합은 `ssum[mask] % target`이고, 원소 `a[i]`를 더 담을 수 있는 조건은 `ssum[mask] % target + a[i] <= target`이다. `ssum`은 최하위 비트를 떼는 O(2^n) DP로 미리 만든다. `target`보다 큰 원소가 있으면 자연히 어디에도 못 들어가 `NO`가 된다. 나머지 연산의 우변 `target`이 0이 될 수 없음을 확인했는가(원소가 전부 양수라 안전하다)?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    int total = 0;
    for (int i = 0; i < n; i++) { cin >> a[i]; total += a[i]; }
    if (total % k != 0) {
        cout << "NO" << '\n';
        return 0;
    }
    int target = total / k;
    int full = (1 << n) - 1;
    // ssum[mask] = mask에 속한 원소 합 (최하위 비트 하나 떼어 내며 O(2^n))
    vector<int> ssum(1 << n, 0);
    for (int mask = 1; mask <= full; mask++) {
        int low = mask & (-mask);
        ssum[mask] = ssum[mask ^ low] + a[__builtin_ctz(mask)];
    }
    vector<char> ok(1 << n, 0);
    ok[0] = 1;
    for (int mask = 0; mask <= full; mask++) {
        if (!ok[mask]) continue;
        int cur = ssum[mask] % target;             // 지금 채우는 중인 그룹의 부분합
        for (int i = 0; i < n; i++) {
            if ((mask >> i) & 1) continue;         // 괄호 필수
            if (cur + a[i] <= target)              // 이 그룹에 더 담을 수 있으면
                ok[mask | (1 << i)] = 1;
        }
    }
    cout << (ok[full] ? "YES" : "NO") << '\n';
    return 0;
}
@@TESTS
--IN
4 2
1 5 11 5
--OUT
YES
--IN
4 3
1 2 3 4
--OUT
NO
--IN
3 3
2 2 2
--OUT
YES
--IN
5 2
1 1 1 1 6
--OUT
NO
@@EXPL
(1) 접근·핵심 아이디어

- 합이 같은 K개 그룹이므로 각 그룹의 합은 `target = total / K`로 고정된다. 나눠떨어지지 않으면 불가능.
- 원소를 "한 그룹이 꽉 찰 때까지 담고, 차면 다음 그룹을 시작"하는 방식으로 하나씩 배정한다고 보면, 상태는 "지금까지 사용한 원소 집합 `mask`"만으로 충분하다: 완성된 그룹 수와 채우는 중인 그룹의 부분합이 `ssum[mask]`에서 `/ target`, `% target`으로 결정되기 때문이다.
- 전이: `ok[mask]`이고 `ssum[mask] % target + a[i] <= target`이면 `ok[mask | (1<<i)]`. 넘치는 배정을 금지하므로 `ok[full]`이면 정확히 K개 그룹이 모두 `target`으로 채워진 것이다. O(2^n · n).
- 첫 예제: 합 22, target 11 → {11}, {1, 5, 5}.

(2) 코드 단계별

- 합을 확인하고 `target`을 구한다. 원소가 전부 양수이고 `k ≤ n`이므로 `target ≥ 1`이라 `% target`이 0으로 나누는 일은 없다.
- `ssum[mask] = ssum[mask ^ low] + a[__builtin_ctz(mask)]`로 마스크별 합을 O(2^n)에 채운다. `__builtin_ctz`는 "뒤에서부터 연속된 0의 개수"라 곧 최하위 켜진 비트의 인덱스다.
- `ok[0] = 1`, 오름차순 `mask`마다 `cur = ssum[mask] % target`, 미사용 `i` 중 `cur + a[i] <= target`인 것으로 전이.
- `ok[full]` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "n ≤ 16 + 집합을 여러 그룹으로" → 사용 집합을 마스크로, 그룹 정보는 합에서 유도(상태 압축의 핵심 관찰).
- 마스크별 합을 매번 다시 더하지 않고 최하위 비트 DP로 준비한다.
- C++ 함정: `vector<bool>`은 비트로 압축된 특수화라 원소의 참조를 얻을 수 없고 반복 접근도 느리다. 불리언 배열이 필요하면 `vector<char>`를 쓰는 편이 예측 가능하다. 또 `1 << n`은 n이 16이면 65536으로 안전하지만, n이 31 이상으로 커지는 문제에서는 `1LL << n`이어야 한다.
- 함정: `target`보다 큰 원소(`NO`), 모든 원소가 같은 값(`YES`), `K = 1`(항상 `YES`)을 확인.
```

**9) 청소 로봇 최소 이동** · Hard

- **요구사항**: `R×C` 격자에 로봇 `R`, 빈칸 `.`, 벽 `#`, 먼지 `*`가 있다. 로봇은 상하좌우 인접 칸으로 한 번에 한 칸 이동하며 벽은 지날 수 없다. 먼지 칸에 도착하면 청소된다. **모든 먼지를 청소하는 최소 이동 횟수**를 구하라. 불가능하면 `-1`, 먼지가 없으면 `0`.
- **입력**: 첫 줄 `R C` (1 ≤ R, C ≤ 10), 이후 R줄의 격자(먼지는 최대 8개, 로봇은 정확히 1개).
- **출력**: 최소 이동 횟수 또는 `-1`.
- **예제**: `3 4 / R..* / .#.. / *..*` → `7` · `2 2 / R. / ..` → `0`
- **셀프체크**: 격자 한 칸씩 상태에 넣으면 폭발한다. 먼지가 8개 이하이므로 **로봇·먼지 사이의 최단 거리를 BFS로 미리 표**로 만들고(정점 ≤ 9개), 그 위에서 "방문한 먼지 집합 + 현재 먼지"를 상태로 하는 Bitmask DP(외판원 경로)를 돌린다. 어떤 먼지까지의 거리가 없으면 `-1`. INF를 `1e9`로 두고 **INF에서 출발하는 전이와 INF를 더하는 전이를 모두 걸러야** 파이썬의 `inf` 산술을 정확히 흉내 낼 수 있다. 먼지 0개는 DP 전에 `0`으로 처리해야 빈 마스크에서 `min_element`를 부르지 않는다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int R, C;
    cin >> R >> C;
    vector<string> grid(R);
    for (int i = 0; i < R; i++) cin >> grid[i];

    pair<int, int> start = {0, 0};
    vector<pair<int, int>> dust;
    for (int i = 0; i < R; i++)
        for (int j = 0; j < C; j++) {
            if (grid[i][j] == 'R') start = {i, j};
            else if (grid[i][j] == '*') dust.push_back({i, j});
        }
    vector<pair<int, int>> pts;
    pts.push_back(start);                       // pts[0] = 로봇, 이후 먼지들
    for (auto &d : dust) pts.push_back(d);
    int m = (int)pts.size();

    const int INF = 1e9;
    const int dx[4] = {1, -1, 0, 0};
    const int dy[4] = {0, 0, 1, -1};
    vector<vector<int>> dist(m, vector<int>(m, INF));   // 정점(로봇·먼지) 사이 최단 거리표
    for (int i = 0; i < m; i++) {
        vector<vector<int>> d(R, vector<int>(C, -1));
        d[pts[i].first][pts[i].second] = 0;
        queue<pair<int, int>> q;
        q.push(pts[i]);
        while (!q.empty()) {
            auto [x, y] = q.front(); q.pop();
            for (int t = 0; t < 4; t++) {
                int nx = x + dx[t], ny = y + dy[t];
                if (nx < 0 || nx >= R || ny < 0 || ny >= C) continue;
                if (grid[nx][ny] == '#' || d[nx][ny] != -1) continue;
                d[nx][ny] = d[x][y] + 1;
                q.push({nx, ny});
            }
        }
        for (int j = 0; j < m; j++) {
            int v = d[pts[j].first][pts[j].second];
            if (v != -1) dist[i][j] = v;
        }
    }

    int k = m - 1;                               // 먼지 수
    if (k == 0) {
        cout << 0 << '\n';
        return 0;
    }
    int full = (1 << k) - 1;
    vector<vector<int>> dp(1 << k, vector<int>(k, INF));   // dp[mask][u]
    for (int j = 0; j < k; j++) dp[1 << j][j] = dist[0][j + 1];
    for (int mask = 0; mask <= full; mask++) {
        for (int u = 0; u < k; u++) {
            int cur = dp[mask][u];
            if (cur == INF) continue;
            for (int v = 0; v < k; v++) {
                if ((mask >> v) & 1) continue;
                if (dist[u + 1][v + 1] == INF) continue;   // 못 가는 쌍은 전이 금지
                int nc = cur + dist[u + 1][v + 1];
                int nm = mask | (1 << v);
                if (nc < dp[nm][v]) dp[nm][v] = nc;
            }
        }
    }
    int ans = *min_element(dp[full].begin(), dp[full].end());
    cout << (ans == INF ? -1 : ans) << '\n';
    return 0;
}
@@TESTS
--IN
3 4
R..*
.#..
*..*
--OUT
7
--IN
2 2
R.
..
--OUT
0
--IN
1 3
R#*
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- 먼지를 방문하는 **순서**만 정하면 그 사이 이동은 항상 최단 경로로 가면 되므로, 문제는 "로봇과 먼지들 사이의 거리표 위에서 모든 먼지를 도는 최단 경로" = 복귀 없는 외판원 경로다.
- 거리표는 각 정점(로봇 + 먼지 ≤ 9개)에서 BFS 한 번씩 O(9·RC). 벽으로 막혀 못 가는 쌍은 INF.
- 그 위에서 `dp[mask][u]` = "mask의 먼지를 청소했고 지금 u에 있음"의 최소 이동. 시작은 로봇에서 각 먼지로 가는 `dist[0][j+1]`, 답은 `min(dp[full][u])`. O(2^k · k^2), k ≤ 8.
- 첫 예제: 로봇(0,0) → (2,0) 2칸 → (2,3) 3칸 → (0,3) 2칸 = 7.

(2) 코드 단계별

- 격자를 `vector<string>`으로 읽는다. 각 줄에 공백이 없으므로 `cin >> grid[i]`면 충분하다.
- 로봇 좌표와 먼지 좌표 목록을 `pts`에 모으고, 각 `pts[i]`에서 BFS로 거리 배열을 얻어 `dist[i][j]`에 채운다(도달 불가는 INF 유지).
- 먼지가 0개면 `0` 출력 후 종료. 아니면 `dp[1<<j][j] = dist[0][j+1]`로 초기화하고 마스크 오름차순 전이.
- `min_element`가 INF면 `-1`, 아니면 그 값.

(3) 스스로 다시 짤 때 생각 순서

- "격자 + 목표 지점 몇 개 전부 방문" → 격자 상태를 버리고 목표 지점 그래프로 축약(BFS 거리표) + 비트마스크 DP.
- 정점 번호 체계(0 = 로봇, 1.. = 먼지)와 `dp`의 먼지 인덱스(0..k-1) 사이의 `+1` 변환을 정확히.
- C++ 함정: 파이썬의 `float('inf')`는 아무리 더해도 `inf`라 "INF + x"를 신경 쓸 필요가 없지만, 유한한 INF 상수를 쓰는 C++에서는 `INF + dist`가 INF보다 커져 비교 조건에 걸리지 않을 뿐 값 자체는 의미가 없다. 여기처럼 **출발 상태가 INF면 건너뛰고, 전이 비용이 INF여도 건너뛴다**는 두 겹 방어를 넣어야 `-1` 판정이 정확해진다.
- 먼지 없음(0), 벽으로 고립(-1), 먼지 1개(단순 BFS 거리) 경계 확인.
```

**10) 최단 공통 초문자열 길이** · Hard

- **요구사항**: 서로 다른 소문자 문자열 `n`개가 주어진다(어느 것도 다른 것의 부분문자열이 아니다). 이 모든 문자열을 **부분문자열로 포함하는** 가장 짧은 문자열의 길이를 구하라.
- **입력**: 첫 줄 `n` (1 ≤ n ≤ 8), 이후 n줄에 문자열(각 길이 ≤ 20).
- **출력**: 최단 공통 초문자열의 길이.
- **예제**: `3 / abcd / cdef / efgh` → `8` · `2 / aaa / aab` → `4`
- **셀프체크**: 문자열들을 어떤 순서로 이어 붙이되, 앞 문자열의 접미사와 뒤 문자열의 접두사가 겹치는 만큼 줄일 수 있다. 먼저 모든 순서쌍의 겹침 `ov[i][j]`(i의 접미사 = j의 접두사인 최대 길이)를 구하고, `dp[mask][last]` = "mask의 문자열들을 이어 붙였고 마지막이 last일 때 최소 길이"로 Bitmask DP. 전이 비용은 `len[j] - ov[last][j]`. 겹침 방향(`ov[i][j]`와 `ov[j][i]`는 다름)을 헷갈리지 마라. 부분문자열 비교는 `words[i].compare(L[i] - k, k, words[j], 0, k) == 0`처럼 복사 없이 할 수 있고, 길이 변수를 `int`로 두어 `s.size() - k`가 부호 없는 뺄셈이 되지 않게 했는가? 문자열 1개면 그 길이.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<string> words(n);
    for (int i = 0; i < n; i++) cin >> words[i];
    vector<int> L(n);
    for (int i = 0; i < n; i++) L[i] = (int)words[i].size();

    // ov[i][j] = words[i]의 접미사와 words[j]의 접두사가 겹치는 최대 길이
    vector<vector<int>> ov(n, vector<int>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            for (int k = min(L[i], L[j]); k >= 1; k--)
                if (words[i].compare(L[i] - k, k, words[j], 0, k) == 0) {
                    ov[i][j] = k;
                    break;
                }
        }

    const int INF = 1e9;
    int full = (1 << n) - 1;
    vector<vector<int>> dp(1 << n, vector<int>(n, INF));   // dp[mask][last] = 최소 길이
    for (int i = 0; i < n; i++) dp[1 << i][i] = L[i];
    for (int mask = 0; mask <= full; mask++) {
        for (int u = 0; u < n; u++) {
            int cur = dp[mask][u];
            if (cur == INF) continue;
            for (int v = 0; v < n; v++) {
                if ((mask >> v) & 1) continue;
                int nc = cur + L[v] - ov[u][v];
                int nm = mask | (1 << v);
                if (nc < dp[nm][v]) dp[nm][v] = nc;
            }
        }
    }
    cout << *min_element(dp[full].begin(), dp[full].end()) << '\n';
    return 0;
}
@@TESTS
--IN
3
abcd
cdef
efgh
--OUT
8
--IN
2
aaa
aab
--OUT
4
--IN
3
alex
loves
leetcode
--OUT
17
--IN
1
xyz
--OUT
3
@@EXPL
(1) 접근·핵심 아이디어

- 어느 문자열도 다른 것의 부분문자열이 아니므로, 최단 초문자열은 n개를 **어떤 순서로 이어 붙이되 인접한 둘의 겹침을 최대한 활용**한 형태다. 순서가 문제의 전부이고 n ≤ 8이므로 순열 대신 방문 집합 마스크로 압축한다.
- 겹침 `ov[i][j]`는 `i`의 접미사와 `j`의 접두사가 같은 최대 길이(방향 있음). 길이가 짧으니 큰 `k`부터 비교해 첫 일치에서 끊으면 충분하다.
- `dp[mask][last]`에서 `v`를 뒤에 붙이면 길이가 `L[v] - ov[last][v]`만큼 늘어난다. 시작은 각 문자열 단독(`dp[1<<i][i] = L[i]`), 답은 `min(dp[full][last])`. O(2^n · n^2).
- 첫 예제: `abcd`+`cdef`(겹침 2)+`efgh`(겹침 2) = 4 + 2 + 2 = 8.

(2) 코드 단계별

- 단어 길이를 `int` 벡터 `L`에 담아 둔다. `words[i].size()`를 그대로 쓰면 부호 없는 타입이라 `size() - k` 같은 식이 음수가 될 때 거대한 값으로 감싸 돈다.
- 겹침표 `ov`를 계산한다. `compare(pos1, len1, str2, pos2, len2)`는 부분 구간끼리 직접 비교해 주므로 `substr`로 임시 문자열을 만들지 않아도 된다.
- `dp`를 INF로 두고 단독 상태를 초기화한 뒤, 마스크 오름차순으로 도달 가능한 `(mask, u)`에서 미사용 `v`로 완화.
- `*min_element(dp[full].begin(), dp[full].end())` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "n ≤ 8개를 전부 포함하는 최단 결합" → 순서 문제 = 외판원 계열, 비용은 "덧붙일 때 늘어나는 길이".
- 비용표(겹침)를 먼저 독립적으로 만들고 검증한 뒤 DP를 얹는다. 겹침 방향과 `L[v] - ov[u][v]` 부호를 확인.
- C++ 함정: `.size()`가 `size_t`(부호 없음)라는 점이 문자열 문제에서 특히 자주 문다. `for (int k = words[i].size() - 1; k >= 0; k--)`는 빈 문자열에서 `k`가 4294967295쯤 되어 곧바로 범위 밖 접근이다. 길이는 받는 즉시 `int`로 캐스팅해 두는 습관이 이런 사고를 통째로 막는다.
- 겹침이 전혀 없는 경우(길이 합), 한 문자열, 접미사 전체가 겹치는 `aaa/aab` 경계로 검산.
```
