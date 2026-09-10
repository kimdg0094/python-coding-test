## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 레슨은 Ch10(Ad-Hoc) 전체를 한 장으로 접는 정리다. 새 내용은 없고, **흩어진 관찰들을 하나의 판단 절차로 묶는** 것이 목적이다. 애드혹의 정체는 "알고리즘을 고르는 문제"가 아니라 **"그 문제만의 성질을 증명하는 문제"**다.

**개념 지도**

```text
 Ad-Hoc : read the problem , not the algorithm list
 -------------------------------------------------------------
                    "max / min / optimal ?"
                              |
              +---------------+---------------+
              |                               |
        L1 : the BEST MOVE              L2 : the CANDIDATE SET
             is forced                       is tiny
              |                               |
        greedy loop                     narrow , then check
        - largest unit first            - neighbours only
        - earliest end time             - both ends
        - most urgent first             - the median
              |                               |
        proof : exchange arg            proof : nothing outside
                ( swap is safe )                can be optimal
              |                               |
              +---------------+---------------+
                              |
                  sort O(n log n) + one scan O(n)
 -------------------------------------------------------------
 no proof works  ->  it is NOT ad-hoc  ->  brute force / DP
```

- 왼쪽 갈래(L1)와 오른쪽 갈래(L2)는 **묻는 것이 다르다.** L1은 "매 순간 무엇을 할까", L2는 "답이 어디에 있을까"를 묻는다. 그런데 두 갈래 모두 **정렬 한 번 + 훑기 한 번**으로 끝난다는 점, 그리고 **증명 없이는 쓰면 안 된다**는 점이 같다.

- 정렬이 두 갈래에 공통으로 등장하는 이유가 애드혹의 핵심이다. 정렬은 **순서라는 구조를 만들어 내는 도구**다. 순서가 생기면 "가장 급한 것부터"라는 규칙이 정의되고(L1), "인접한 것끼리만 비교하면 된다"는 성질이 생긴다(L2).

- C++에서 이 골격을 쓸 때 반복해서 등장하는 초기값·정렬 관용구는 다음과 같다.

```text
   goal                     init value        note
   ----------------------   ---------------   -----------------------
   max of long long         LLONG_MIN         never 0
   min of long long         LLONG_MAX         never 0
   "not found yet"          -1                keep it out of range
   last_end (activity)      INT_MIN           times may be negative
   sort by end time         pair{end, start}  default sort just works
   comparator               use < , never <=  <= crashes std::sort
```

**뼈대 코드**

```cpp
// 뼈대 1 — 그리디 루프 : "정렬 → 순서대로 확정"
sort(items.begin(), items.end(), [](const auto& x, const auto& y) {
    return x.second < y.second;      // 문제마다 바뀜 (정렬 기준이 전부다)
});
int answer = 0;
long long state = LLONG_MIN;         // 문제마다 바뀜 (들고 다닐 최소한의 상태)
for (auto& it : items) {
    if (is_ok(it, state)) {          // 문제마다 바뀜 (지금 고를 수 있는가)
        answer++;
        state = update(it);          // 문제마다 바뀜 (고른 뒤 상태 갱신)
    }
}
cout << answer << '\n';
```

```cpp
// 뼈대 2 — 활동 선택 : 겹치지 않게 최대 개수 (종료 시각 기준)
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int,int>> meets(n);              // {end, start} 로 담는다
    for (int i = 0; i < n; i++) {
        int s, e;
        cin >> s >> e;
        meets[i] = {e, s};
    }
    sort(meets.begin(), meets.end());            // 종료 오름차순(기본 정렬)
    int count = 0, last_end = INT_MIN;           // 어떤 시작 시각보다도 작은 값
    for (auto& m : meets) {
        if (m.second >= last_end) {              // 등호 허용 여부는 지문 확인
            count++;
            last_end = m.first;
        }
    }
    cout << count << '\n';
    return 0;
}
```

```cpp
// 뼈대 3 — 후보 좁히기 : 정렬하면 인접한 것끼리만 보면 된다
sort(xs.begin(), xs.end());
long long best = xs[1] - xs[0];          // 최솟값 초기화는 '첫 후보'로
for (int i = 0; i + 1 < (int)xs.size(); i++) {
    long long gap = xs[i + 1] - xs[i];   // 문제마다 바뀜 (인접 두 개의 값)
    best = min(best, gap);
}
cout << best << '\n';
```

```cpp
// 뼈대 4 — 정렬 + 투 포인터 : 양 끝에서 좁혀 오기
sort(xs.begin(), xs.end());
int i = 0, j = (int)xs.size() - 1;
long long best = LLONG_MAX;
bool found = false;
while (i < j) {
    long long cur = (long long)xs[i] + xs[j];    // 문제마다 바뀜 (평가할 값)
    if (!found || better(cur, best)) {           // 동점 규칙까지 넣을 것
        best = cur;
        found = true;
    }
    if (cur == target) break;
    else if (cur > target) j--;                  // 크면 오른쪽을 줄인다
    else i++;                                    // 작으면 왼쪽을 키운다
}
cout << best << '\n';
```

```cpp
// 뼈대 5 — 대표값 하나로 답이 정해지는 유형
sort(xs.begin(), xs.end());
long long m = xs[xs.size() / 2];         // 절댓값 거리 합 -> 중앙값
long long total = 0;
for (long long x : xs) total += llabs(x - m);
cout << total << '\n';
// 제곱 거리 합이 목표라면 중앙값이 아니라 평균이 답 (문제마다 바뀜)
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 겹치지 않게 최대 개수 고르기 | 종료 시각 오름차순 그리디 | 빨리 끝낼수록 뒤에 남는 시간이 길다(교환 논증) | `O(n log n)` |
| 마감이 있는 작업 최대 처리 | 마감 이른 순 정렬 후 배치 | 급한 것을 미루면 못 하게 될 위험만 커진다 | `O(n log n)` |
| 배수 관계 동전으로 최소 개수 | 큰 단위부터 그리디 | 큰 단위 1개를 쪼개면 개수가 늘기만 함 | `O(t log t)` |
| 배수 관계가 **아닌** 동전 | 그리디 금지 → DP | 반례: 단위 `1,3,4`로 `6`은 `4+1+1`(3개)보다 `3+3`(2개) | `O(money·t)` |
| 가장 가까운 두 수의 차 | 정렬 후 인접 쌍만 비교 | 떨어진 쌍의 차 = 사이 인접 차들의 합 ≥ 각 조각 | `O(n log n)` |
| 합이 목표에 가장 가까운 쌍 | 정렬 후 투 포인터 | 단조성 덕에 한쪽을 통째로 버려도 손해 없음 | `O(n log n)` |
| 한 점으로 모을 때 거리 합 최소 | 정렬 후 중앙값 `xs[n/2]` | 좌우 점 개수가 균형을 이루는 지점 | `O(n log n)` |
| 제곱 거리 합 최소 | 평균 | 제곱 합은 평균에서 최소가 됨(중앙값 아님) | `O(n)` |
| `k`개 지워 가장 큰 수 만들기 | 단조 스택(`vector`를 스택처럼) | 앞자리를 키우는 이득이 항상 지배적 | `O(n)` |
| 정렬 기준이 두 축 이상 | 비교 람다에서 `<`만 사용 | `<=`는 정렬이 범위를 벗어나 죽는다 | `O(n log n)` |
| 앞의 선택이 뒤 선택지를 망가뜨림 | 완전탐색·DP로 전환 | 교환 논증이 깨지면 그리디는 틀린다 | 유형별 |

- 표의 마지막 줄이 이 챕터에서 가장 중요하다. **그리디를 못 쓰는 상황을 알아보는 것**이 그리디를 쓰는 것보다 실전에서 더 자주 점수를 지킨다.

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 애드혹이 "알고리즘 선택"이 아니라 "성질 증명"인 이유를.
- [ ] 설명할 수 있다: 교환 논증이 무엇이고, 왜 그것으로 그리디의 정당성이 증명되는지를.
- [ ] 설명할 수 있다: 탐욕적 선택 속성과 최적 부분구조가 각각 무엇을 보장하는지를.
- [ ] 설명할 수 있다: 회의실 배정에서 기준이 시작 시각도 길이도 아닌 **종료 시각**인 이유를.
- [ ] 설명할 수 있다: `pair`를 `{end, start}`로 담으면 왜 기본 정렬만으로 종료 시각 기준이 되는지를.
- [ ] 설명할 수 있다: 배수 관계 동전에서 그리디가 최적인 이유와, 단위 `1,3,4`에서 깨지는 이유를.
- [ ] 설명할 수 있다: 정렬 후 "최소 차이는 반드시 인접 쌍"인 이유를 합으로 논증해서.
- [ ] 설명할 수 있다: 절댓값 거리 합의 최적점이 평균이 아니라 중앙값인 이유를 좌우 개수로.
- [ ] 설명할 수 있다: 짝수 개일 때 가운데 두 값 사이가 모두 같은 최소인 이유를.
- [ ] 설명할 수 있다: 투 포인터가 후보를 버려도 되는 근거(단조성)와 `while (i < j)`인 이유를.
- [ ] 설명할 수 있다: `sort`의 비교 함수에 `<=`를 쓰면 왜 프로그램이 죽는지를.
- [ ] 설명할 수 있다: 최솟값·최댓값 변수를 0으로 초기화하면 각각 어떤 입력에서 틀리는지를.
- [ ] 설명할 수 있다: 애드혹 문제 대부분이 왜 `O(n log n)`으로 끝나는지를.
- [ ] 설명할 수 있다: 그리디가 틀린다는 것을 보이려면 무엇을 제시해야 하는지(반례 하나면 충분한 이유)를.
- [ ] 설명할 수 있다: 경계 조건(끝 시각 == 시작 시각, 동점 처리)이 답을 바꾸는 구체적 예를.

**⚠️ 자주 하는 실수**

**1) 활동 선택을 시작 시각 기준으로 정렬한다**

```cpp
// ❌ 틀린 코드
sort(meets.begin(), meets.end());        // {start, end} 로 담아 시작 기준 정렬
int count = 0, last_end = INT_MIN;
for (auto& m : meets)
    if (m.first >= last_end) { count++; last_end = m.second; }
```

왜: 시작이 이른 회의가 아주 늦게 끝날 수 있다. `(0, 6)`을 먼저 잡으면 `(1, 3)`과 `(3, 5)` 두 개를 동시에 잃는다. 남는 자유 시간을 결정하는 것은 시작이 아니라 **종료 시각**이다.

```cpp
// ✅ 고친 코드
// meets 를 {end, start} 로 담으면 기본 정렬이 곧 종료 오름차순
sort(meets.begin(), meets.end());
int count = 0, last_end = INT_MIN;
for (auto& m : meets)
    if (m.second >= last_end) { count++; last_end = m.first; }
```

**2) 겹침 판정에서 등호를 빼먹는다**

```cpp
// ❌ 틀린 코드
if (s > last_end) {          // 앞 회의가 끝나는 순간 시작하는 회의를 버린다
    count++;
    last_end = e;
}
```

왜: 지문이 "종료 시각과 시작 시각이 같으면 겹치지 않는다"고 하면 `s == last_end`도 선택 가능해야 한다. `>`로 쓰면 `(1,3) → (3,5) → (5,7)`에서 뒤 두 개를 놓쳐 답이 3이 아니라 1이 된다.

```cpp
// ✅ 고친 코드
if (s >= last_end) {         // 등호 허용 여부는 지문에서 확인해 결정
    count++;
    last_end = e;
}
```

**3) 비교 함수에 `<=`를 쓴다**

```cpp
// ❌ 틀린 코드
sort(items.begin(), items.end(), [](const auto& x, const auto& y) {
    return x.second <= y.second;         // 같을 때 true 를 돌려준다
});
```

왜: `std::sort`는 비교 함수가 "엄격한 약순서"임을 가정한다. 같은 값에 `true`가 나오면 정렬 내부에서 범위를 벗어나 읽어 프로그램이 죽거나(segfault) 메모리를 망가뜨린다. 원소가 적을 땐 멀쩡히 돌다가 커지는 순간 터져서 원인을 찾기 어렵다.

```cpp
// ✅ 고친 코드
sort(items.begin(), items.end(), [](const auto& x, const auto& y) {
    if (x.second != y.second) return x.second < y.second;
    return x.first < y.first;            // 동점은 다른 축으로, 항상 <
});
```

**4) 배수 관계가 아닌 동전에 그리디를 쓴다**

```cpp
// ❌ 틀린 코드
int coins[] = {4, 3, 1};
int money = 6, count = 0;
for (int c : coins) {
    count += money / c;
    money %= c;                          // 4 한 개 + 1 두 개 = 3개
}
```

왜: 큰 단위를 쓰는 순간 남은 금액을 작은 단위로 메울 수밖에 없어 손해가 난다. `6 = 3 + 3`으로 2개가 최적인데 그리디는 3개를 낸다. **큰 단위가 작은 단위의 배수**라는 전제가 없으면 교환 논증이 성립하지 않는다.

```cpp
// ✅ 고친 코드 (배수 성질이 없으면 DP)
const int INF = 1e9;
vector<int> dp(money + 1, INF);
dp[0] = 0;
for (int x = 1; x <= money; x++)
    for (int c : coins)
        if (x >= c && dp[x - c] + 1 < dp[x]) dp[x] = dp[x - c] + 1;
cout << dp[money] << '\n';               // 6 -> 2
```

**5) 최소 차이를 모든 쌍으로 구한다**

```cpp
// ❌ 틀린 코드
long long best = LLONG_MAX;
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)
        best = min(best, llabs((long long)xs[i] - xs[j]));   // 쌍이 n(n-1)/2 개
```

왜: 쌍의 개수가 `n(n-1)/2`라 `O(n²)`다. `n = 10⁵`이면 50억 번이라 C++로도 시간 초과다. 정렬해 두면 **최소 차이는 반드시 인접 쌍에서 나오므로** `n-1`번만 보면 된다.

```cpp
// ✅ 고친 코드
sort(xs.begin(), xs.end());
long long best = LLONG_MAX;
for (int i = 0; i + 1 < n; i++)
    best = min(best, (long long)xs[i + 1] - xs[i]);          // O(n log n)
```

**6) 거리 합 최소 지점으로 평균을 쓴다**

```cpp
// ❌ 틀린 코드
long long sum = accumulate(xs.begin(), xs.end(), 0LL);
long long m = sum / (long long)xs.size();    // 평균으로 모은다
long long total = 0;
for (long long x : xs) total += llabs(x - m);
```

왜: 절댓값 거리 합은 **점이 좌우에 몇 개 있는지**만 보고, 값이 얼마나 큰지는 보지 않는다. `{1, 2, 9}`에서 평균은 4라 합이 `3+2+5=10`이지만, 중앙값 2로 모으면 `1+0+7=8`로 더 작다. 평균이 답인 것은 **제곱** 거리 합일 때다.

```cpp
// ✅ 고친 코드
sort(xs.begin(), xs.end());
long long m = xs[xs.size() / 2];             // 중앙값
long long total = 0;
for (long long x : xs) total += llabs(x - m);
```

**7) 후보를 좁혀 놓고 정렬을 빠뜨린다**

```cpp
// ❌ 틀린 코드
long long m = xs[xs.size() / 2];             // 정렬 안 한 벡터의 '가운데 인덱스'
long long total = 0;
for (long long x : xs) total += llabs(x - m);
```

왜: `xs[n/2]`가 중앙값이 되는 것은 **정렬된 상태에서만**이다. `{1, 2, 9, 4, 5}`의 `xs[2]`는 9이지 중앙값 4가 아니다. "인접 쌍만 보면 된다", "가운데가 답이다" 같은 성질은 모두 정렬을 전제로 한다.

```cpp
// ✅ 고친 코드
sort(xs.begin(), xs.end());                  // 성질을 쓰기 전에 반드시 정렬
long long m = xs[xs.size() / 2];
long long total = 0;
for (long long x : xs) total += llabs(x - m);
```

**8) 최솟값 변수를 0으로 초기화한다**

```cpp
// ❌ 틀린 코드
long long best = 0;                          // 최솟값을 찾는데 0에서 시작
for (int i = 0; i + 1 < n; i++)
    best = min(best, (long long)xs[i + 1] - xs[i]);
```

왜: 정렬 후 인접 차는 항상 0 이상이라, `min`이 절대 `0` 아래로 못 내려가 답이 무조건 `0`이 된다. 최솟값의 초기값은 **첫 후보** 또는 `LLONG_MAX`여야 한다. 반대로 최댓값을 `0`으로 두면 음수 답을 놓친다.

```cpp
// ✅ 고친 코드
long long best = (long long)xs[1] - xs[0];   // 첫 후보로 초기화
for (int i = 0; i + 1 < n; i++)
    best = min(best, (long long)xs[i + 1] - xs[i]);
```

**다음 챕터로**

- 이 챕터에서 익힌 "**증명이 서면 탐색을 건너뛴다**"는 감각은 이후 모든 최적화 문제의 첫 관문이 된다. 문제를 받으면 항상 (1) 그리디로 되는가 → (2) 후보를 상수 개로 좁힐 수 있는가 → (3) 둘 다 아니면 탐색·DP 순으로 묻게 된다.

- 반대로 여기서 배운 **반례 만들기**는 다음 단계로 넘어가는 신호다. 교환 논증이 깨지는 예를 하나라도 찾으면, 그때부터는 "모든 경우를 어떻게 빠짐없이·중복 없이 볼 것인가"라는 완전탐색·DP의 언어로 문제를 다시 읽어야 한다.

- 정렬을 전처리로 깔고 한 번 훑는 `O(n log n)` 골격은 투 포인터·이분 탐색·스위핑으로 그대로 확장된다. 이 챕터의 뼈대 코드 4번(투 포인터)이 그 다리 역할을 한다.
