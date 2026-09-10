## L3. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch4(이진탐색)의 핵심 — 정렬 배열에서의 이진탐색, Lower/Upper Bound, 그리고 "정답 후보 범위"에 이진탐색을 거는 파라메트릭 서치 — 를 **반복 훈련**하고, 코딩테스트 단골 이진탐색 유형으로 **확장**하는 연습 세트다. 모든 문제의 공통 질문은 "무엇에 이진탐색을 거는가(배열 인덱스인가, 답의 후보인가)"와 "단조 술어가 무엇인가"다.
- **반복 훈련 개념 1 — 닫힌 구간 이진탐색**: `int lo = 0, hi = n - 1;` / `while (lo <= hi)` / `int mid = lo + (hi - lo) / 2;` / 세 갈래(같다·작다·크다)로 `lo = mid + 1` 또는 `hi = mid - 1`. 못 찾으면 -1을 루프 밖에서. `mid`를 `(lo + hi) / 2`로 쓰면 `lo`, `hi`가 10억을 넘길 때 `int` 오버플로가 나므로 `lo + (hi - lo) / 2` 형태를 습관으로 삼는다.
- **반복 훈련 개념 2 — Lower/Upper Bound 직접 구현**: 반열린 구간 `int lo = 0, hi = (int)a.size();` / `while (lo < hi)` / lower는 `a[mid] < x`일 때 `lo = mid + 1`, upper는 `a[mid] <= x`일 때 `lo = mid + 1`, 아니면 `hi = mid`. 개수 = `upper - lower`. C++ 표준 라이브러리에도 `<algorithm>`의 `lower_bound`/`upper_bound`가 같은 의미로 있고 **반복자**를 돌려주므로 인덱스가 필요하면 `lower_bound(v.begin(), v.end(), x) - v.begin()`처럼 빼야 한다. 직접 구현할 때 함수 이름을 `lower_bound`로 지으면 `using namespace std;` 때문에 표준 함수와 이름이 겹쳐 모호해지니 `lowerBound`처럼 다르게 짓는다.
- **반복 훈련 개념 3 — 답의 후보에 이진탐색(파라메트릭)**: 술어 `ok(mid)`가 한 지점에서 true↔false로 딱 한 번 바뀌면, 참인 최댓값은 `if (ok(mid)) { ans = mid; lo = mid + 1; }`, 참인 최솟값은 `if (ok(mid)) { ans = mid; hi = mid - 1; }`. 후보 범위가 10억을 넘으면 `lo`·`hi`·`ans`·판정 누적값을 모두 `long long`으로 둔다 — `int`로 두면 조용히 틀린 답이 나온다(예외가 나지 않는다).
- **반복 훈련 개념 4 — 회전·봉우리 배열의 단조성 찾기**: 전체가 정렬돼 있지 않아도 `a[mid] > a[hi]`(회전) 또는 `a[mid] < a[mid + 1]`(봉우리)처럼 "한쪽을 버릴 수 있는 판정"이 있으면 O(log n)이 성립한다. `mid + 1`을 읽는 판정은 반열린 구간(`while (lo < hi)`)으로 짜야 배열 밖 접근이 없다 — C++에서 범위 밖 읽기는 예외가 아니라 **정의되지 않은 동작**이다.
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '이분 탐색' 단계(수 찾기·자르기류 파라메트릭), 프로그래머스 「코딩테스트 고득점 Kit」의 '이분탐색', NeetCode 150의 'Binary Search'(회전 배열·봉우리·용량 최소화), 『이것이 취업을 위한 코딩테스트다』의 '이진탐색' 파트.
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 탐색 경로 출력 | Easy | 닫힌 구간 이진탐색 과정 | 반복 훈련 |
| 2 | 회원 번호 조회 | Easy | 정렬 후 존재 여부 다중 질의 | 반복 훈련 (백준 '이분 탐색' 단계 스타일) |
| 3 | 정수 세제곱근 | Easy | 답 범위 이진탐색(단조 술어) + 오버플로 | 반복 훈련 |
| 4 | 온도 구간 관측 횟수 | Medium | lower/upper bound 직접 구현·개수 세기 | 반복 훈련 |
| 5 | 가장 가까운 정류장 | Medium | lower bound + 이웃 비교 | 반복 훈련 |
| 6 | 두 상자 합 맞추기 | Medium | 정렬 배열 두 개 + 등장 횟수 | 유형 확장 (NeetCode 'Binary Search'·'Two Pointers' 스타일) |
| 7 | 가래떡 자르기 | Medium | 파라메트릭(참인 최댓값) | 유형 확장 (백준 '이분 탐색' 단계 자르기류 스타일) |
| 8 | 택배 배달원 배정 | Hard | 파라메트릭(참인 최솟값) + 탐욕 판정 | 유형 확장 (NeetCode 'Binary Search' 용량 최소화 스타일) |
| 9 | 산봉우리 배열 탐색 | Hard | 봉우리 찾기 + 양쪽 이진탐색 결합 | 유형 확장 (NeetCode 'Binary Search' 스타일) |
| 10 | 회전 배열 다중 질의 | Hard | 회전 횟수 + 인덱스 매핑 이진탐색 | 반복 훈련 |

**문제**

**1) 탐색 경로 출력** · Easy

- **요구사항**: 오름차순으로 정렬된 서로 다른 정수 배열과 목표값이 주어진다. 닫힌 구간 이진탐색(`lo = 0`, `hi = n - 1`, `mid = lo + (hi - lo) / 2`, 같으면 종료, 작으면 `lo = mid + 1`, 크면 `hi = mid - 1`)을 수행하며 확인한 `arr[mid]` 값들을 순서대로 출력하고, 다음 줄에 찾은 인덱스(없으면 -1)를 출력하라.
- **입력**: 첫 줄 n(1 ≤ n ≤ 1000), 둘째 줄 오름차순 정수 n개, 셋째 줄 목표값.
- **출력**: 첫 줄에 확인한 값들을 공백으로, 둘째 줄에 인덱스 또는 -1.
- **예제**: `7 / 2 5 8 12 16 23 38 / 23` → `12 23 / 5` · `7 / 2 5 8 12 16 23 38 / 7` → `12 5 8 / -1`
- **셀프체크**: 둘째 예제 — mid=3(12)>7이라 hi=2, mid=1(5)<7이라 lo=2, mid=2(8)>7이라 hi=1, lo>hi로 종료. `mid`를 `(lo + hi + 1) / 2`로 쓰거나 반열린 구간으로 짜면 경로가 달라지니 규칙대로(`lo + (hi - lo) / 2`는 `(lo + hi) / 2`와 값이 같고 오버플로만 막는다). 원소 1개(`1 / 4 / 4` → `4` / `0`)에서도 한 번은 확인한다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];
    int target;
    cin >> target;

    int lo = 0, hi = n - 1;
    vector<int> path;                    // 확인한 값 기록
    int ans = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;    // (lo+hi)/2 와 값은 같고 오버플로만 없다
        path.push_back(arr[mid]);        // 비교 전에 기록
        if (arr[mid] == target) {
            ans = mid;
            break;
        } else if (arr[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }

    for (size_t i = 0; i < path.size(); i++) {
        if (i) cout << ' ';
        cout << path[i];
    }
    cout << '\n' << ans << '\n';
    return 0;
}
@@TESTS
--IN
7
2 5 8 12 16 23 38
23
--OUT
12 23
5
--IN
7
2 5 8 12 16 23 38
7
--OUT
12 5 8
-1
--IN
1
4
4
--OUT
4
0
--IN
8
1 2 3 4 5 6 7 8
8
--OUT
4 6 7 8
7
@@EXPL
(1) 접근·핵심 아이디어

- L1-1의 이진탐색을 그대로 돌리되 "무엇을 확인했는가"를 기록한다. 경로는 구간 규칙(닫힌 구간, `mid = lo + (hi - lo) / 2`)에 의해 유일하게 정해지므로, 규칙을 한 글자도 바꾸지 않는 것이 정답의 조건이다.
- 확인 횟수는 최대 약 log2(n) + 1이다. 경로를 눈으로 보면 "매번 절반을 버린다"는 감각과 off-by-one(`hi = mid - 1`)의 의미가 명확해진다.

(2) 코드 단계별

- `n`, `vector<int> arr`, `target`을 읽고 `lo = 0`, `hi = n - 1`, 빈 `path`, `ans = -1`.
- 루프 진입마다 `mid` 계산 후 즉시 `path.push_back(arr[mid])` — 비교 전에 기록해야 마지막(찾은/버린) 확인도 남는다.
- 같으면 `ans = mid`로 `break`, 작으면 `lo = mid + 1`, 크면 `hi = mid - 1`.
- `path`를 공백으로 이어 출력하고 다음 줄에 `ans`. 시간 O(log n).
- 출력 루프의 인덱스를 `size_t i`로 두었다 — `path.size()`는 부호 없는 타입이라 `int i`와 비교하면 컴파일러 경고가 뜨고, 크기가 0인 벡터에서 `size() - 1`을 쓰면 아주 큰 값이 되어 무한 루프가 된다.

(3) 스스로 다시 짤 때 생각 순서

- 경계 유파(닫힌 구간)를 정하고 `mid` 식을 문제 규칙과 맞춘다 — 다른 유파는 결과 경로가 다르다.
- 기록 시점은 "값을 본 순간" = `mid` 계산 직후.
- 경계 검산: 원소 1개, 목표가 마지막 원소(`1..8`에서 8 → 경로 `4 6 7 8`), 없는 값(-1이지만 경로는 비어 있지 않음).
```

**2) 회원 번호 조회** · Easy

- **요구사항**: 회원 번호 N개(정렬되어 있지 않고 서로 다름)와 조회할 번호 M개가 주어진다. 각 조회 번호가 회원 번호에 있으면 1, 없으면 0을 출력하라. `set`·`unordered_set`이나 `std::binary_search`를 쓰지 말고, 회원 번호를 `sort`로 정렬한 뒤 직접 구현한 이진탐색으로 각 조회를 O(log N)에 처리한다.
- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 회원 번호 N개, 셋째 줄 M(1 ≤ M ≤ 1000), 넷째 줄 조회 번호 M개(정수 범위 -10^9 ~ 10^9).
- **출력**: 조회 순서대로 1 또는 0을 공백으로 구분해 한 줄로.
- **예제**: `6 / 41 7 19 3 25 12 / 5 / 19 4 41 26 3` → `1 0 1 0 1` · `1 / 7 / 2 / 7 8` → `1 0`
- **셀프체크**: 정렬을 빼먹으면 이진탐색이 틀린 답을 낸다(정렬은 한 번만, 조회마다 하지 않는다). 최솟값보다 작거나 최댓값보다 큰 조회(`-4`, `101`)에서 0이 나오는가. 출력 순서는 조회 입력 순서 그대로. 탐색 함수에서 `hi`를 `arr.size() - 1`로 쓰면 `size()`가 부호 없는 타입이라 빈 배열에서 huge 값이 되니 `(int)arr.size() - 1`로 캐스팅했는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

// 있으면 1, 없으면 0
int existsIn(const vector<int>& arr, int x) {
    int lo = 0, hi = (int)arr.size() - 1;   // size()는 unsigned → 반드시 캐스팅
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == x) return 1;
        else if (arr[mid] < x) lo = mid + 1;
        else hi = mid - 1;
    }
    return 0;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> members(n);
    for (int i = 0; i < n; i++) cin >> members[i];
    int m;
    cin >> m;
    vector<int> queries(m);
    for (int i = 0; i < m; i++) cin >> queries[i];

    sort(members.begin(), members.end());   // 이진탐색 전제: 정렬 (한 번만)

    for (int i = 0; i < m; i++) {
        if (i) cout << ' ';
        cout << existsIn(members, queries[i]);
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
6
41 7 19 3 25 12
5
19 4 41 26 3
--OUT
1 0 1 0 1
--IN
1
7
2
7 8
--OUT
1 0
--IN
4
100 -3 50 0
4
-3 -4 101 100
--OUT
1 0 0 1
@@EXPL
(1) 접근·핵심 아이디어

- "여러 번 존재 여부를 묻는다"면 전처리 1회(정렬 O(N log N)) 후 질의마다 O(log N)으로 답하는 것이 정석이다. 질의마다 선형으로 훑으면 O(N·M)이라 둘 다 커지면 느리다.
- 이진탐색은 정렬을 전제로 하므로, 입력이 섞여 있으면 반드시 먼저 `sort`한다. 이 문제는 값이 서로 다르므로 "찾았다/없다"만 판정하면 된다.

(2) 코드 단계별

- `existsIn(arr, x)`: 닫힌 구간 이진탐색으로 찾으면 1, 구간이 비면 0을 반환. 인자를 `const vector<int>&`(참조)로 받아 호출마다 벡터 전체가 복사되는 것을 막는다 — 값으로 받으면 질의 M번마다 N개 복사라 O(N·M)이 된다.
- 회원 번호를 읽어 `sort(members.begin(), members.end())`(한 번만).
- 각 질의에 `existsIn`을 적용해 결과를 공백으로 이어 출력.
- 시간 O(N log N + M log N), 공간 O(N).

(3) 스스로 다시 짤 때 생각 순서

- "다중 질의 + 존재 여부" 신호 → 정렬 1회 + 이진탐색 반복.
- 이진탐색 함수를 따로 빼면 질의 루프가 한 줄로 정리된다. 함수의 반환값(1/0)을 출력 형식에 맞춘다.
- `hi`의 초기값에서 `(int)arr.size() - 1` 캐스팅을 빠뜨리면, 빈 벡터일 때 `hi`가 약 42억이 되어 범위 밖 접근(정의되지 않은 동작)으로 이어진다.
- 경계 검산: 회원 1명, 최솟값 미만·최댓값 초과 질의, 음수 번호가 섞인 경우의 정렬 순서.
```

**3) 정수 세제곱근** · Easy

- **요구사항**: 음이 아닌 정수 x가 주어질 때 `m³ ≤ x`를 만족하는 가장 큰 정수 m(세제곱근의 정수부)을 이진탐색으로 구하라. 부동소수 연산(`cbrt(x)`, `pow(x, 1.0/3)`)은 오차가 있으니 쓰지 말고 정수 곱만 사용한다.
- **입력**: 한 줄에 정수 x(0 ≤ x ≤ 10^18).
- **출력**: 세제곱근의 정수부.
- **예제**: `27` → `3` · `100` → `4`
- **셀프체크**: 술어 `mid * mid * mid <= x`는 mid가 커질수록 true→false로 한 번만 바뀐다(참인 최댓값 문제). x가 10^18까지라 `x`도 `mid`도 `long long`이어야 한다. 탐색 상한을 `x` 그대로 두면 `mid`가 5×10^17쯤에서 `mid³`이 `long long`(약 9.2×10^18)을 훌쩍 넘겨 **조용히 틀린 값**이 되므로, 답이 10^6을 넘을 수 없다는 사실(`(10^6)³ = 10^18`)을 이용해 상한을 10^6으로 둔다. x=0이면 답 0, x=1~7이면 1(`7` → `1`). x=10^18일 때 답이 정확히 10^6인가(부동소수로 풀면 999999.999…로 어긋날 수 있다).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    long long x;
    cin >> x;

    // 답의 상한: (10^6)^3 = 10^18 이므로 m 은 절대 10^6 을 넘지 않는다.
    // hi 를 x 로 두면 mid*mid*mid 가 long long 을 넘겨 조용히 틀린다.
    long long lo = 0, hi = 1000000;
    long long ans = 0;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (mid * mid * mid <= x) {      // 조건 참 → 답 후보, 더 큰 값 시도
            ans = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    cout << ans << '\n';
    return 0;
}
@@TESTS
--IN
27
--OUT
3
--IN
100
--OUT
4
--IN
0
--OUT
0
--IN
1000000000000000000
--OUT
1000000
@@EXPL
(1) 접근·핵심 아이디어

- L1-2(제곱근)와 같은 구조로, 배열이 아니라 "답의 후보 범위"에 이진탐색을 건다. 술어 `mid³ <= x`는 단조(참…참 거짓…거짓)이므로 참인 가장 큰 mid가 답이다.
- 파이썬 정수는 자릿수 제한이 없어 후보 범위를 `[0, x]`로 두어도 되지만, C++의 `long long`은 약 9.2×10^18에서 끊긴다. 오버플로는 예외를 던지지 않고 값만 엉키므로 **탐색 범위를 먼저 수학적으로 좁히는 것**이 정답의 일부다: `m ≤ 10^6`.
- 범위를 좁히기 싫다면 `__int128`로 곱하거나 `mid <= x / (mid * mid)`처럼 나눗셈으로 비교하는 방법도 있다.

(2) 코드 단계별

- `long long x`를 읽고 `lo = 0`, `hi = 1000000`, `ans = 0`.
- `mid³ <= x`면 `ans = mid`로 기록하고 `lo = mid + 1`(더 큰 후보), 아니면 `hi = mid - 1`.
- 루프 종료 후 `ans` 출력. 반복 횟수는 약 log2(10^6) ≈ 20회.

(3) 스스로 다시 짤 때 생각 순서

- "무엇에 이진탐색?" → 정수 후보 m. "술어?" → `m³ <= x`. "참인 최댓값인가 최솟값인가?" → 최댓값.
- 참일 때 `ans` 갱신 + 오른쪽으로, 거짓일 때 왼쪽으로. 이 틀은 파라메트릭 서치 전부에 재사용된다.
- C++에서는 매번 "이 곱셈이 타입 한계를 넘는가"를 먼저 계산해 본다. 넘으면 범위를 좁히거나 `__int128`.
- 경계: x=0(답 0), x=1(답 1), 완전세제곱수(27→3)와 그 직전 값(26→2).
```

**4) 온도 구간 관측 횟수** · Medium

- **요구사항**: 관측된 온도 N개(정렬되어 있지 않고 중복 가능)와 Q개의 구간 질의 `x y`가 주어진다. 각 질의에 대해 `x ≤ 온도 ≤ y`인 관측의 개수를 출력하라. `<algorithm>`의 `lower_bound`/`upper_bound`를 쓰지 말고 lower bound(`x` 이상 첫 위치)와 upper bound(`y` 초과 첫 위치)를 직접 구현해 `upperBound(y) - lowerBound(x)`로 O(log N)에 답한다.
- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 온도 N개(정수), 셋째 줄 Q(1 ≤ Q ≤ 1000), 다음 Q줄에 `x y`(x ≤ y).
- **출력**: 질의마다 개수를 한 줄씩.
- **예제**: `8 / 23 19 31 25 19 28 22 31 / 3 / 19 25 / 30 40 / 26 27` → `5 / 2 / 0` · `3 / 5 5 5 / 2 / 5 5 / 6 9` → `3 / 0`
- **셀프체크**: 정렬하면 `19 19 22 23 25 28 31 31`. [19,25]는 lower(19)=0, upper(25)=5 → 5. 두 함수의 부등호(`<` vs `<=`) 하나 차이가 "이상/초과"를 가른다. `hi`를 `n - 1`이 아니라 `n`으로 두어야 "전부 y 이하"일 때 upper가 n이 된다. 구간 안에 값이 하나도 없으면 두 경계가 같은 위치를 가리켜 0. 직접 만든 함수 이름을 `lower_bound`로 지으면 `using namespace std;` 때문에 표준 함수와 겹쳐 컴파일 오류가 나니 `lowerBound`처럼 지었는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

// a[i] >= x 인 첫 i  (std::lower_bound 와 이름이 겹치지 않게 lowerBound)
int lowerBound(const vector<int>& a, int x) {
    int lo = 0, hi = (int)a.size();       // 반열린 구간 [0, n)
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < x) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

// a[i] > x 인 첫 i
int upperBound(const vector<int>& a, int x) {
    int lo = 0, hi = (int)a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] <= x) lo = mid + 1;    // 같아도 넘어간다 → '초과'
        else hi = mid;
    }
    return lo;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> temps(n);
    for (int i = 0; i < n; i++) cin >> temps[i];
    int q;
    cin >> q;

    sort(temps.begin(), temps.end());

    string out;
    for (int i = 0; i < q; i++) {
        int x, y;
        cin >> x >> y;
        out += to_string(upperBound(temps, y) - lowerBound(temps, x));
        out += '\n';
    }
    cout << out;
    return 0;
}
@@TESTS
--IN
8
23 19 31 25 19 28 22 31
3
19 25
30 40
26 27
--OUT
5
2
0
--IN
3
5 5 5
2
5 5
6 9
--OUT
3
0
--IN
4
-2 0 3 9
2
-10 100
4 8
--OUT
4
0
@@EXPL
(1) 접근·핵심 아이디어

- 정렬 배열에서 "x 이상 y 이하"의 개수는 `(y 이하 개수) - (x 미만 개수)` = `upperBound(y) - lowerBound(x)`다. 두 경계는 L2의 반열린 구간 골격으로 각각 O(log N)에 구한다.
- lower는 `a[mid] < x`일 때 오른쪽으로(아직 부족), upper는 `a[mid] <= x`일 때 오른쪽으로(같아도 넘어감). 이 등호 하나가 "이상"과 "초과"를 구분한다.

(2) 코드 단계별

- `lowerBound`/`upperBound`를 반열린 구간 `[0, n)`, `while (lo < hi)`, `hi = mid`로 구현. 두 함수 모두 `const vector<int>&`로 받아 복사를 막는다.
- 온도 배열을 읽어 한 번 `sort`.
- 질의마다 `x, y`를 읽고 `upperBound(temps, y) - lowerBound(temps, x)`를 문자열 버퍼에 쌓는다.
- 마지막에 한 번에 출력. 질의마다 `cout << ... << '\n'`을 해도 되지만, `endl`은 매번 버퍼를 비워 느려지므로 쓰지 않는다.
- 시간 O(N log N + Q log N).

(3) 스스로 다시 짤 때 생각 순서

- "구간 개수" → 두 경계의 차. 어느 쪽이 lower(x)이고 어느 쪽이 upper(y)인지 부등호 방향으로 확정한다.
- 반열린 구간을 쓰면 `hi = mid`가 안전하고, `hi`의 초기값 `n`이 "모두 조건 미달"을 자연스럽게 표현한다.
- 표준 라이브러리를 쓸 때는 `upper_bound(v.begin(), v.end(), y) - lower_bound(v.begin(), v.end(), x)`로 같은 값을 얻는다 — 반복자를 빼면 개수가 나온다는 점을 기억.
- 검산: 전부 같은 값에서 `[5,5]` → N, 배열 전체를 덮는 구간 → N, 값 사이 빈 구간 → 0.
```

**5) 가장 가까운 정류장** · Medium

- **요구사항**: 직선 도로 위 정류장 위치 N개가 오름차순(서로 다름)으로 주어진다. Q개의 질의 위치 p에 대해 |정류장 − p|가 가장 작은 정류장의 위치를 출력하라. 거리가 같으면 위치가 작은 쪽을 고른다. 각 질의를 O(log N)에 처리한다(lower bound로 삽입 위치를 찾고 양 이웃만 비교).
- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 정류장 위치 N개(오름차순 정수), 셋째 줄 Q(1 ≤ Q ≤ 1000), 넷째 줄 질의 위치 Q개.
- **출력**: 질의 순서대로 정류장 위치를 공백으로 구분해 한 줄로.
- **예제**: `5 / 1 4 9 15 20 / 4 / 10 2 17 25` → `9 1 15 20` · `3 / 2 6 10 / 2 / 4 8` → `2 6`
- **셀프체크**: lower bound `k`가 0이면 왼쪽 이웃이 없고(`stops[0]`), `k == N`이면 오른쪽 이웃이 없다(`stops[N-1]`) — 이 두 경계를 먼저 처리해야 `stops[k]`가 범위 밖을 읽지 않는다. C++ `vector`의 `[]`는 범위를 검사하지 않아 범위 밖 접근이 예외 없이 쓰레기 값을 돌려준다(정의되지 않은 동작). 동률(`4`는 2와 6에서 거리 2)은 `<=`로 왼쪽을 우선. p가 정류장과 정확히 같으면 그 정류장 자신(거리 0).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int lowerBound(const vector<int>& a, int x) {
    int lo = 0, hi = (int)a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < x) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> stops(n);
    for (int i = 0; i < n; i++) cin >> stops[i];
    int q;
    cin >> q;

    for (int t = 0; t < q; t++) {
        int p;
        cin >> p;
        int k = lowerBound(stops, p);    // p 이상인 첫 정류장
        int best;
        if (k == 0) {
            best = stops[0];             // 왼쪽 이웃 없음
        } else if (k == n) {
            best = stops[n - 1];         // 오른쪽 이웃 없음
        } else {
            int left = stops[k - 1], right = stops[k];
            if (p - left <= right - p) best = left;   // 동률이면 작은 위치
            else best = right;
        }
        if (t) cout << ' ';
        cout << best;
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
5
1 4 9 15 20
4
10 2 17 25
--OUT
9 1 15 20
--IN
3
2 6 10
2
4 8
--OUT
2 6
--IN
2
5 8
3
0 5 100
--OUT
5 5 8
@@EXPL
(1) 접근·핵심 아이디어

- 정렬 배열에서 p에 가장 가까운 값은 "p 이상인 첫 원소"(lower bound)와 "그 바로 왼쪽 원소" 둘 중 하나다. 그 사이에 p가 끼어 있으므로 다른 원소는 이 둘보다 멀 수밖에 없다. 따라서 lower bound 한 번 + 이웃 두 개 비교로 O(log N).
- 동률 규칙(작은 위치 우선)은 비교 연산자 `<=`로 왼쪽을 먼저 택하면 된다.

(2) 코드 단계별

- `lowerBound(stops, p)`로 `k`를 구한다.
- `k == 0`이면 왼쪽 이웃이 없으므로 `stops[0]`, `k == n`이면 오른쪽 이웃이 없으므로 `stops[n - 1]`.
- 그 외엔 `stops[k - 1]`, `stops[k]`의 거리를 비교해 `p - left <= right - p`면 왼쪽.
- 질의 순서대로 공백 출력. 시간 O(Q log N).

(3) 스스로 다시 짤 때 생각 순서

- "가장 가까운" = 삽입 위치의 양 이웃 후보 2개로 줄인다.
- 경계 두 개(`k == 0`, `k == n`)를 **먼저** 분기해 인덱스 범위를 안전하게 만든 뒤 일반 경우를 쓴다. 파이썬이라면 범위 밖 인덱스에서 `IndexError`가 나 바로 알아채지만, C++ `vector`의 `[]`는 아무 말 없이 쓰레기를 읽는다 — 검사가 필요하면 `at()`을 쓰면 예외가 난다.
- 동률 규칙을 부등호 하나로 표현하고, p가 정류장과 일치하는 경우를 검산한다 — `p == stops[k]`면 `right - p = 0`이므로 `p - left <= 0`은 거짓, 오른쪽이 정확히 선택된다.
```

**6) 두 상자 합 맞추기** · Medium

- **요구사항**: 오름차순으로 정렬된 두 정수 배열 A(길이 N)와 B(길이 M)가 주어진다(각각 중복 가능). 목표합 S에 대해 `A[i] + B[j] == S`인 쌍 (i, j)의 개수를 출력하라. A의 각 원소마다 B에서 `S − A[i]`의 등장 횟수를 이진탐색(lower/upper bound 직접 구현)으로 구해 합산한다.
- **입력**: 첫 줄 N M S(1 ≤ N, M ≤ 1000, |S| ≤ 10^9), 둘째 줄 A의 원소 N개, 셋째 줄 B의 원소 M개.
- **출력**: 쌍의 개수 하나.
- **예제**: `4 5 7 / 1 2 3 4 / 3 3 4 5 6` → `5` · `3 3 100 / 1 2 3 / 1 2 3` → `0`
- **셀프체크**: 첫 예제 — 1은 6(1개), 2는 5(1개), 3은 4(1개), 4는 3(2개) → 5. B에 같은 값이 여러 개일 때 "존재 여부"만 세면 틀린다(등장 횟수 = upper − lower). `S − A[i]`는 |S| ≤ 10^9이고 A의 값도 10^9급이라 `int`로 계산하면 최대 2×10^9로 넘칠 수 있으니 `long long`으로 두었는가. S − A[i]가 B의 범위 밖이면 두 경계가 같아 0. 음수가 섞여도(`3 4 0 / -2 -1 0 / -2 0 1 2` → `3`) 정렬 순서만 맞으면 동작.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int lowerBound(const vector<long long>& a, long long x) {
    int lo = 0, hi = (int)a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < x) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

int upperBound(const vector<long long>& a, long long x) {
    int lo = 0, hi = (int)a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] <= x) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    long long s;
    cin >> n >> m >> s;
    vector<long long> a(n), b(m);
    for (int i = 0; i < n; i++) cin >> a[i];
    for (int i = 0; i < m; i++) cin >> b[i];

    long long total = 0;
    for (int i = 0; i < n; i++) {
        long long need = s - a[i];       // int 로 두면 최대 2e9 라 넘친다
        total += upperBound(b, need) - lowerBound(b, need);   // 등장 횟수
    }
    cout << total << '\n';
    return 0;
}
@@TESTS
--IN
4 5 7
1 2 3 4
3 3 4 5 6
--OUT
5
--IN
3 3 100
1 2 3
1 2 3
--OUT
0
--IN
1 1 4
2
2
--OUT
1
--IN
3 4 0
-2 -1 0
-2 0 1 2
--OUT
3
@@EXPL
(1) 접근·핵심 아이디어

- 합이 S인 쌍은 A의 원소 x를 고정하면 B에서 `S - x`를 찾는 문제로 바뀐다. B가 정렬돼 있으니 `S - x`의 등장 횟수를 `upperBound - lowerBound`로 O(log M)에 얻고, A 전체에 대해 합산하면 O(N log M)이다. 이중 루프 O(N·M)보다 빠르다.
- 존재 여부(0/1)가 아니라 "횟수"를 세야 하는 이유: B에 같은 값이 여러 개면 각각이 서로 다른 쌍이기 때문이다.

(2) 코드 단계별

- L2 골격의 `lowerBound`, `upperBound`를 `vector<long long>`용으로 정의.
- A의 각 `a[i]`에 대해 `long long need = s - a[i]`, `total += upperBound(b, need) - lowerBound(b, need)`.
- `total` 출력. 추가 공간 O(1).

(3) 스스로 다시 짤 때 생각 순서

- "두 배열 + 합" → 한쪽을 고정하고 다른 쪽에서 보수를 탐색한다.
- 정렬 배열에서 값의 개수는 두 경계의 차 — L2-1과 같은 도구를 그대로 쓴다.
- C++에서는 뺄셈·덧셈 하나하나가 타입 한계 안인지 먼저 본다. `s - a[i]`는 두 값이 모두 10^9급이면 2×10^9로 `int` 한계(약 2.1×10^9)에 아슬아슬하니 처음부터 `long long`으로 읽는 편이 안전하다.
- 경계: 답이 0인 경우(보수가 범위 밖), 원소 1개씩, 음수·0이 섞인 경우. 두 배열이 같은 값들이어도 (i, j)는 서로 다른 배열의 인덱스이므로 그대로 센다.
```

**7) 가래떡 자르기** · Medium

- **요구사항**: 길이가 다른 가래떡 N개를 모두 같은 정수 길이 L로 잘라 조각을 만든다(각 가래떡에서 `길이 / L`개가 나오고 남는 부분은 버린다 — C++의 정수 나눗셈이 곧 버림이다). 조각을 최소 M개 이상 얻을 수 있는 L의 최댓값을 구하라. 가래떡 길이의 합은 M 이상이라 L=1은 항상 가능하다.
- **입력**: 첫 줄 N M(1 ≤ N ≤ 1000, 1 ≤ M ≤ 10^9), 둘째 줄 가래떡 길이 N개(1 ≤ 길이 ≤ 10^9).
- **출력**: L의 최댓값.
- **예제**: `3 7 / 30 14 22` → `7` · `2 3 / 10 10` → `5`
- **셀프체크**: 첫 예제 — L=7이면 4+2+3=9 ≥ 7 가능, L=8이면 3+1+2=6 < 7 불가. 술어 "조각 수 ≥ M"은 L이 커질수록 true→false로 단조 감소하므로 참인 최댓값 문제. 탐색 범위는 `[1, max(길이)]`(0은 0으로 나누기 — C++에서 정수 0 나눗셈은 예외가 아니라 프로그램이 죽는다). 조각 수는 최대 1000 × 10^9 = 10^12이라 누적 변수를 `int`로 두면 넘치니 `long long`인가. `1 5 / 5` → 1, `1 1 / 1000` → 1000처럼 양 끝값이 답인 경우도 확인.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long m;
    cin >> n >> m;
    vector<long long> rice(n);
    for (int i = 0; i < n; i++) cin >> rice[i];

    long long lo = 1, hi = *max_element(rice.begin(), rice.end());
    long long ans = 0;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        long long pieces = 0;            // 최대 1000 * 1e9 = 1e12 → long long
        for (int i = 0; i < n; i++) pieces += rice[i] / mid;   // 정수 나눗셈 = 버림
        if (pieces >= m) {               // 충분 → 더 길게 시도
            ans = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    cout << ans << '\n';
    return 0;
}
@@TESTS
--IN
3 7
30 14 22
--OUT
7
--IN
2 3
10 10
--OUT
5
--IN
1 5
5
--OUT
1
--IN
1 1
1000
--OUT
1000
@@EXPL
(1) 접근·핵심 아이디어

- 답 L 자체를 후보 범위 `[1, max(길이)]`에서 이진탐색한다(파라메트릭 서치). 판정 `f(L) = (조각 수 ≥ M)`은 L이 길어질수록 조각이 줄어 true→false로 한 번만 바뀐다. 따라서 true를 유지하는 가장 큰 L을 찾는다 — L2-3(나무 자르기)과 같은 "참인 최댓값" 틀.
- 판정 비용은 O(N)이고 반복은 약 log2(10^9) ≈ 30회라 전체 O(N log(max)).

(2) 코드 단계별

- `lo = 1`, `hi = *max_element(rice.begin(), rice.end())`, `ans = 0`. `max_element`는 **반복자**를 돌려주므로 앞에 `*`를 붙여 값을 꺼낸다.
- `mid`로 잘랐을 때 `pieces += rice[i] / mid`. C++의 정수 나눗셈은 소수부를 버리므로 파이썬의 `//`와 같은 역할을 한다(단 음수에서는 다르다 — 여기서는 모두 양수라 문제없다).
- `pieces >= m`이면 `ans = mid`, `lo = mid + 1`(더 긴 길이 시도), 아니면 `hi = mid - 1`.
- `ans` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "최대 L을 구하되 조건은 조각 수" → 배열이 아니라 답에 이진탐색.
- 단조성 방향(L↑ ⇒ 조각↓)을 확인해 참일 때 오른쪽으로 간다.
- `pieces`의 타입을 먼저 정한다: N개의 항이 각각 최대 10^9라 합이 10^12 — `int`면 조용히 음수가 되어 판정이 뒤집힌다.
- 경계: `lo`는 0이 아닌 1(0으로 나누면 프로그램이 죽는다), 답이 `max(길이)` 자체인 경우(가래떡 하나, M=1), 답이 1인 경우.
```

**8) 택배 배달원 배정** · Hard

- **요구사항**: 상자 N개의 무게가 배송 순서대로 주어진다. 이 순서를 유지한 채 연속 구간으로 나눠 K명의 배달원에게 배정한다(각 배달원은 1개 이상, 구간은 이어져야 한다). 배달원 중 가장 무거운 적재량(구간 무게 합)을 최소화할 때 그 값을 출력하라.
- **입력**: 첫 줄 N K(1 ≤ K ≤ N ≤ 1000), 둘째 줄 상자 무게 N개(1 ≤ 무게 ≤ 10^6).
- **출력**: 최대 적재량의 최솟값.
- **예제**: `5 2 / 7 2 5 10 8` → `18` · `5 3 / 1 2 3 4 5` → `6`
- **셀프체크**: 첫 예제 — 한도 18이면 `[7,2,5] [10,8]` 2명으로 가능, 17이면 `[7,2,5] [10] [8]` 3명 필요. 판정은 탐욕: 한도 C를 두고 앞에서부터 담다가 넘치면 새 배달원. 필요 인원이 K 이하면 가능(인원이 남으면 구간을 더 쪼개도 최대 적재량은 늘지 않는다). 탐색 범위 하한은 `*max_element`(한 상자는 쪼갤 수 없음), 상한은 `accumulate`로 구한 합. K=N이면 답은 max, K=1이면 sum. 합이 최대 10^9이라 `accumulate`의 초깃값을 `0LL`로 두어야 `long long`으로 누적된다(`0`으로 두면 `int`로 누적돼 넘칠 수 있다).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<long long> w(n);
    for (int i = 0; i < n; i++) cin >> w[i];

    long long lo = *max_element(w.begin(), w.end());          // 한 상자는 못 쪼갠다
    long long hi = accumulate(w.begin(), w.end(), 0LL);       // 0LL: long long 누적
    long long ans = hi;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        int groups = 1;                  // 적재 한도 mid 로 필요한 배달원 수
        long long load = 0;
        for (int i = 0; i < n; i++) {
            if (load + w[i] > mid) {
                groups++;
                load = w[i];
            } else {
                load += w[i];
            }
        }
        if (groups <= k) {               // 가능 → 한도를 더 줄여 본다
            ans = mid;
            hi = mid - 1;
        } else {
            lo = mid + 1;
        }
    }
    cout << ans << '\n';
    return 0;
}
@@TESTS
--IN
5 2
7 2 5 10 8
--OUT
18
--IN
5 3
1 2 3 4 5
--OUT
6
--IN
3 3
4 9 2
--OUT
9
--IN
4 1
1 1 1 1
--OUT
4
@@EXPL
(1) 접근·핵심 아이디어

- "최대값을 최소화"는 파라메트릭 서치의 대표 신호다. 답(적재 한도 C)을 고정하면 "C로 K명 이하에 배정 가능한가"는 C가 커질수록 false→true로 단조 증가하므로, 참인 최솟값을 이진탐색한다 — 앞 문제들과 반대로 참일 때 `hi = mid - 1`.
- 판정은 탐욕이 최적이다: 순서를 유지해야 하므로 앞에서부터 한도까지 꽉 채우고 넘치면 새 사람에게 넘기는 것이 인원을 최소화한다. 인원이 K보다 적게 나와도 구간을 더 쪼개면 되니(최대 적재량은 줄거나 같음) `groups <= k`가 가능 조건이다.

(2) 코드 단계별

- `lo = *max_element(...)`(한 상자보다 작은 한도는 불가능), `hi = accumulate(..., 0LL)`(전부 한 명), `ans = hi`.
- `mid`에 대해 탐욕으로 `groups`를 센다: `load + w[i] > mid`면 `groups++`, `load = w[i]`.
- `groups <= k`면 `ans = mid`, `hi = mid - 1`; 아니면 `lo = mid + 1`.
- `ans` 출력. 시간 O(N log(sum)).

(3) 스스로 다시 짤 때 생각 순서

- "최대의 최소" → 답에 이진탐색, 술어는 "이 한도로 K명 안에 되는가".
- 단조성 방향이 앞 문제들과 반대(C↑ ⇒ 가능)이므로 참일 때 왼쪽으로 좁힌다.
- `accumulate`의 세 번째 인자는 초깃값이자 **누적 타입**을 정한다. `0`을 넘기면 `int`로 더해져 10^9급에서 넘치므로 `0LL`을 쓴다 — C++ 초심자가 가장 자주 밟는 지뢰다.
- 하한을 0이나 1로 잡으면 판정에서 한 상자가 한도를 넘어 `load = w[i]`가 한도 초과인 채로 진행되는 함정 — 반드시 `*max_element`. K=N(답 max), K=1(답 sum)로 양 끝 검산.
```

**9) 산봉우리 배열 탐색** · Hard

- **요구사항**: 배열이 어떤 위치(봉우리)까지는 순증가하고 그 뒤로는 순감소한다(봉우리가 맨 앞이나 맨 뒤일 수도 있고, 값은 모두 서로 다르다). 목표값이 주어질 때 봉우리의 인덱스와 목표값의 인덱스(없으면 -1)를 O(log n)에 구하라. 절차: (1) 봉우리를 이진탐색으로 찾고, (2) 오름 구간 `[0, peak]`에서 일반 이진탐색, (3) 없으면 내림 구간 `[peak+1, n-1]`에서 부등호를 뒤집은 이진탐색.
- **입력**: 첫 줄 n(1 ≤ n ≤ 1000), 둘째 줄 배열, 셋째 줄 목표값.
- **출력**: 첫 줄에 봉우리 인덱스, 둘째 줄에 목표값 인덱스 또는 -1.
- **예제**: `7 / 1 4 7 12 9 5 2 / 5` → `3 / 5` · `7 / 1 4 7 12 9 5 2 / 10` → `3 / -1`
- **셀프체크**: 봉우리 탐색 술어는 `a[mid] < a[mid + 1]`(참이면 봉우리는 오른쪽) — 반열린 구간 `while (lo < hi)`로 짜야 `mid + 1`이 범위를 넘지 않는다. 파이썬이라면 범위를 넘는 순간 `IndexError`로 바로 들통나지만 C++ `vector`의 `[]`는 조용히 쓰레기 값을 읽으므로(정의되지 않은 동작) 구간 유파 선택이 더 중요하다. 내림 구간에서는 `a[mid] > target`일 때 오른쪽으로 가야 한다(부등호 반전 실수 주의). 순증가만 하는 배열(`1 2 3 4`)은 봉우리가 마지막 인덱스, 순감소만 하는 배열(`9 6 3 1`)은 0.

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
    int target;
    cin >> target;

    // 1) 봉우리 찾기: a[mid] < a[mid+1] 이면 봉우리는 오른쪽
    //    while (lo < hi) 라야 mid+1 이 항상 범위 안이다.
    int lo = 0, hi = n - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < a[mid + 1]) lo = mid + 1;
        else hi = mid;
    }
    int peak = lo;

    int ans = -1;
    // 2) 오름 구간 [0, peak]
    lo = 0; hi = peak;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) { ans = mid; break; }
        else if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    // 3) 내림 구간 [peak+1, n-1] (부등호 반대)
    if (ans == -1) {
        lo = peak + 1; hi = n - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] == target) { ans = mid; break; }
            else if (a[mid] > target) lo = mid + 1;
            else hi = mid - 1;
        }
    }

    cout << peak << '\n' << ans << '\n';
    return 0;
}
@@TESTS
--IN
7
1 4 7 12 9 5 2
5
--OUT
3
5
--IN
7
1 4 7 12 9 5 2
10
--OUT
3
-1
--IN
1
5
5
--OUT
0
0
--IN
4
9 6 3 1
9
--OUT
0
0
@@EXPL
(1) 접근·핵심 아이디어

- 배열 전체는 정렬돼 있지 않지만 "봉우리 왼쪽은 오름차순, 오른쪽은 내림차순"이라는 구조가 있다. 그래서 세 번의 이진탐색으로 나눈다: 봉우리 위치 찾기, 오름 구간 탐색, 내림 구간 탐색. 각각 O(log n)이므로 전체도 O(log n).
- 봉우리 찾기의 술어 `a[mid] < a[mid + 1]`은 "아직 오르막" — 참이면 봉우리는 mid보다 오른쪽에 있고, 거짓이면 mid 자신이거나 왼쪽이다. 반열린 골격(`while (lo < hi)`, `hi = mid`)으로 첫 거짓 위치를 찾으면 그것이 봉우리다.

(2) 코드 단계별

- 봉우리: `lo = 0, hi = n - 1`, `a[mid] < a[mid + 1]`면 `lo = mid + 1`, 아니면 `hi = mid`. 종료 시 `peak = lo`.
- 오름 구간 `[0, peak]`에서 표준 이진탐색.
- 못 찾았으면 내림 구간 `[peak + 1, n - 1]`에서 `a[mid] > target`일 때 `lo = mid + 1`(값이 오른쪽으로 갈수록 작아지므로).
- `peak`와 `ans`를 두 줄로 출력.
- 세 탐색이 `lo`, `hi`를 재사용하므로 각 단계 시작에서 반드시 다시 대입한다 — C++에서는 선언과 초기화를 떼어 놓으면 이전 값이 남아 있다.

(3) 스스로 다시 짤 때 생각 순서

- "부분적으로 정렬" → 정렬된 조각으로 쪼개서 각각 이진탐색. 먼저 경계(봉우리)를 이진탐색으로 찾는다.
- 봉우리 탐색은 `mid + 1` 접근 때문에 `while (lo < hi)`가 안전하다(`lo <= hi`면 `mid = n - 1`에서 `a[n]`을 읽어 정의되지 않은 동작).
- 내림 구간은 부등호만 뒤집는다. n=1(봉우리 0, 내림 구간 `[1, 0]`이라 루프에 안 들어감), 순증가·순감소 배열로 경계 검산.
```

**10) 회전 배열 다중 질의** · Hard

- **요구사항**: 서로 다른 정수의 오름차순 배열을 오른쪽으로 r칸 회전한 배열이 주어진다(r은 알려지지 않았고 0 ≤ r < n). 먼저 회전 횟수 r(= 최솟값의 인덱스)을 이진탐색으로 구해 첫 줄에 출력하고, 이어지는 Q개의 목표값 각각에 대해 배열에서의 인덱스(없으면 -1)를 둘째 줄에 출력하라. 각 질의는 "가상의 정렬 배열 인덱스 k ↔ 실제 인덱스 `(k + r) % n`" 대응을 이용해 O(log n)에 처리한다.
- **입력**: 첫 줄 n(1 ≤ n ≤ 1000), 둘째 줄 회전된 배열, 셋째 줄 Q(1 ≤ Q ≤ 1000), 넷째 줄 목표값 Q개.
- **출력**: 첫 줄에 r, 둘째 줄에 질의 순서대로 인덱스(또는 -1)를 공백으로.
- **예제**: `7 / 15 18 2 3 6 12 14 / 3 / 6 15 7` → `2 / 4 0 -1` · `4 / 1 3 5 7 / 2 / 7 1` → `0 / 3 0`
- **셀프체크**: 최솟값 탐색 술어는 `a[mid] > a[hi]`(참이면 최솟값은 mid 오른쪽) — `a[lo]`와 비교하면 회전 0에서 틀리는 함정. 회전 0(`1 3 5 7`)이면 r=0이고 매핑은 항등. 질의 탐색에서는 비교 대상이 `a[(mid + r) % n]`이고, 답으로 출력할 것은 가상 인덱스 mid가 아니라 실제 인덱스라는 점에 주의. `%`는 양수끼리라 파이썬과 결과가 같지만, 만약 왼쪽 회전으로 음수 인덱스가 생기면 C++의 `%`는 음수를 그대로 돌려주므로(파이썬과 다름) `(k + r % n + n) % n` 형태가 필요하다. n=1은 r=0.

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
    int q;
    cin >> q;

    // 1) 회전 횟수 = 최솟값 인덱스
    int lo = 0, hi = n - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi]) lo = mid + 1;   // 최솟값은 mid 오른쪽
        else hi = mid;
    }
    int r = lo;

    // 2) 가상의 정렬 배열 인덱스 k → 실제 인덱스 (k + r) % n
    cout << r << '\n';
    for (int t = 0; t < q; t++) {
        int target;
        cin >> target;
        int l = 0, h = n - 1, ans = -1;
        while (l <= h) {
            int mid = l + (h - l) / 2;
            int real = (mid + r) % n;
            if (a[real] == target) { ans = real; break; }
            else if (a[real] < target) l = mid + 1;
            else h = mid - 1;
        }
        if (t) cout << ' ';
        cout << ans;
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
7
15 18 2 3 6 12 14
3
6 15 7
--OUT
2
4 0 -1
--IN
4
1 3 5 7
2
7 1
--OUT
0
3 0
--IN
1
9
1
9
--OUT
0
0
--IN
5
5 1 2 3 4
3
5 4 0
--OUT
1
0 4 -1
@@EXPL
(1) 접근·핵심 아이디어

- L1-3은 질의 하나를 "정렬된 절반 판정"으로 풀었다. 질의가 많으면 회전 횟수 r을 한 번만 구해 두고, 이후엔 "가상의 정렬 배열"에 표준 이진탐색을 거는 것이 깔끔하다. 가상 인덱스 k의 실제 위치는 `(k + r) % n`이므로 비교할 때만 이 매핑을 거치면 된다.
- r은 최솟값의 인덱스다. 술어 `a[mid] > a[hi]`가 참이면 mid는 회전된 앞부분(큰 값들)에 있어 최솟값이 오른쪽에 있고, 거짓이면 mid 이하 어딘가에 있다. 반열린 골격으로 첫 거짓 위치를 찾는다.

(2) 코드 단계별

- 최솟값: `lo = 0, hi = n - 1`, `a[mid] > a[hi]`면 `lo = mid + 1`, 아니면 `hi = mid`. 종료 시 `r = lo`.
- 각 질의: 가상 구간 `[0, n-1]`에서 `real = (mid + r) % n`으로 실제 값을 읽어 표준 세 갈래 비교. 질의 루프는 바깥 탐색과 변수 이름을 겹치지 않게 `l`, `h`로 따로 둔다.
- 찾으면 `ans = real`(실제 인덱스), 못 찾으면 -1.
- `r`을 먼저 한 줄로 출력하고, 질의 결과를 공백으로 이어 한 줄. 시간 O((1 + Q) log n).

(3) 스스로 다시 짤 때 생각 순서

- "회전 배열 + 다중 질의" → 회전 횟수를 먼저 한 번 구하고 매핑으로 정렬 배열처럼 다룬다.
- 최솟값 탐색은 `a[hi]`와 비교해야 회전 0에서도 맞다(`a[lo]` 비교는 `1 3 5 7`에서 `a[mid] > a[lo]`가 참이라 오른쪽으로 잘못 간다).
- C++의 `%`는 피연산자가 음수면 결과도 음수가 될 수 있다(파이썬은 항상 나누는 수의 부호). 여기서는 `mid + r`이 항상 0 이상이라 안전하지만, 왼쪽 회전·역매핑을 다룰 땐 `(x % n + n) % n`으로 감싸는 습관이 필요하다.
- 출력은 가상 인덱스가 아니라 실제 인덱스. 회전 0, n=1, 최솟값·최댓값이 질의인 경우(`5 1 2 3 4`에서 5 → 0, 4 → 4)로 검산.
```
