## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터는 "정렬된 배열에서 값 찾기"로 시작해 "정답 자체를 축에 놓고 이진탐색하기"로 끝났다. 두 레슨을 한 장으로 잇고, 바로 쓸 수 있는 골격과 실수 목록으로 마무리한다. C++로 옮길 때 새로 생기는 위험은 두 가지뿐이다 — **`mid` 계산의 오버플로**와 **판정 함수 안에서의 오버플로**다. 둘 다 예외가 아니라 "조용히 틀린 답"으로 나타나므로, 골격에 아예 박아 두고 시작하는 편이 낫다.

**개념 지도**

```text
   binary search on an INDEX            binary search on the ANSWER
   ------------------------            ---------------------------
   sorted array a[0..n-1]              answer range [LO, HI]
   test  : a[mid] < x ?                test  : feasible(mid) ?
   result: a position                  result: the optimal value
                \                       /
                 \                     /
                  v                   v
        same engine : find where a monotone T/F strip flips

   feasible(X) monotone ?
     |
     +-- no  -> parametric search does NOT apply  (DP / brute force)
     |
     +-- yes -> T..T F..F  ->  answer = LAST  T   (maximise)
                F..F T..T  ->  answer = FIRST T   (minimise)
                integer axis -> while (lo <= hi)
                real    axis -> repeat a fixed number of times
```

왼쪽 갈래(인덱스 이진탐색)는 `lower_bound` / `upper_bound`로 굳어졌고, 오른쪽 갈래(정답 이진탐색)가 파라메트릭 서치다. **엔진은 같고 축만 다르다.** 그래서 L1에서 익힌 경계 감각이 그대로 L2의 정확도가 된다.

C++에서 이 엔진이 깨지는 자리는 딱 두 곳이고, 둘 다 타입 문제다.

```text
   where a C++ binary search silently breaks

   1) mid = (lo + hi) / 2
        lo = 2e9 , hi = 2e9   ->  lo + hi overflows int -> mid < 0
        a[mid] reads out of bounds                    // 예외가 아니라 UB
      fix : mid = lo + (hi - lo) / 2                  // 차이는 넘치지 않는다

   2) inside feasible(X) :  int cnt = 0; cnt += c / X;
        n = 1e5 , c = 2e9   ->  cnt overflows -> becomes negative
        cnt >= K is false everywhere -> every probe fails -> ans stays LO
      fix : long long cnt , or stop early : if (cnt >= K) return true;

   symptom of (2) : the sample passes, the big case prints the initial ans
```

**뼈대 코드**

경계 탐색 — 반열린 구간 `[lo, hi)`. 실전에서는 `std::lower_bound`를 쓰지만, 직접 짤 수 있어야 변형이 가능하다.

```cpp
#include <bits/stdc++.h>
using namespace std;

int lowerBound(const vector<int>& a, int x) {   // a[i] >= x 인 첫 인덱스
    int lo = 0, hi = (int)a.size();
    // 불변식: 답은 항상 [lo, hi] 안에 있다 (hi = size 는 "없음"을 뜻한다)
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;   // (lo+hi)/2 로 쓰지 않는다 — 오버플로
        if (a[mid] < x) lo = mid + 1;   // <- 문제마다 바뀜: 버릴 조건
        else            hi = mid;       // mid 자신도 답일 수 있으므로 포함해 줄인다
    }
    return lo;                          // 종료 시 lo == hi
}
// upperBound는 조건만 a[mid] <= x 로 바꾼다
```

파라메트릭 — **최댓값**을 찾는 형태(`T..T F..F`, 마지막 T가 답).

```cpp
bool feasible(long long X) {      // <- 문제마다 바뀜: O(N) 정도의 예/아니오 판정
    long long cnt = 0;            // 누적은 반드시 long long
    for (long long c : a) {
        cnt += c / X;
        if (cnt >= K) return true;   // 넘칠 일도 없애는 조기 종료
    }
    return false;
}

long long lo = LO, hi = HI;       // <- 문제마다 바뀜: 답이 가질 수 있는 최소/최대
long long ans = -1;               // 한 번도 성공 못 할 수 있으면 실패값으로
// 불변식: ans 는 "지금까지 성공한 X 중 가장 큰 값", 답은 [lo, hi] 안에 남아 있다
while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;
    if (feasible(mid)) {
        ans = mid;                // 성공 -> 더 크게 노려본다
        lo = mid + 1;             // [mid+1, hi] 로 줄어든다 (길이가 반드시 감소)
    } else {
        hi = mid - 1;             // 실패 -> mid 이상은 전부 실패이므로 버린다
    }
}
cout << ans << '\n';
```

파라메트릭 — **최솟값**을 찾는 형태(`F..F T..T`, 첫 T가 답). 위와 딱 두 줄만 다르다.

```cpp
long long lo = LO, hi = HI;       // <- 문제마다 바뀜
long long ans = HI;               // 전 구간이 실패면 남을 값
// 불변식: ans 는 "지금까지 성공한 X 중 가장 작은 값"
while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;
    if (feasible(mid)) {
        ans = mid;                // 성공 -> 더 작게 노려본다
        hi = mid - 1;             // <- 최댓값 형태와 반대 방향
    } else {
        lo = mid + 1;
    }
}
cout << ans << '\n';
```

답이 실수일 때 — 경계가 없으므로 **고정 횟수**로 돌린다.

```cpp
double lo = 0.0, hi = 1e9;        // <- 문제마다 바뀜
for (int it = 0; it < 100; it++) {   // 한 번에 오차가 절반 -> 100회면 충분
    double mid = (lo + hi) / 2;      // double 이라 오버플로 걱정은 없다
    if (feasible(mid)) lo = mid;     // 최댓값 형태(성공이면 오른쪽을 남긴다)
    else               hi = mid;
}
cout << fixed << setprecision(6) << lo << '\n';   // <- 문제마다 바뀜: 요구 정밀도
```

정렬이 선행돼야 할 때 쓰는 최소 조합.

```cpp
sort(a.begin(), a.end());         // 이진탐색의 전제: 단조성
int lo = lower_bound(a.begin(), a.end(), x) - a.begin();   // x 미만 개수
int up = upper_bound(a.begin(), a.end(), x) - a.begin();   // x 이하 개수
int cnt = up - lo;                                          // x의 등장 횟수
// set/map 이라면 s.lower_bound(x) 처럼 멤버 함수를 쓴다 (std::lower_bound는 O(n))
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 정렬된 `vector`에서 값의 존재·위치·개수 | `std::lower_bound` / `upper_bound` | 경계 두 개면 개수까지 나온다 | O(log N) |
| `set`/`map`에서 같은 질문 | **멤버** `s.lower_bound(x)` | `std::lower_bound`는 이터레이터를 걸어 O(N) | O(log N) |
| "x 이상이 처음 나오는 위치" 같은 경계 질문 | 반열린 `[lo, hi)` 이진탐색 | 불변식이 가장 단순해 off-by-one이 적다 | O(log N) |
| "조건을 만족하는 최댓값" | 닫힌 구간 + 성공 시 `lo = mid + 1` | `T..T F..F`의 마지막 T가 답 | O(N log R) |
| "조건을 만족하는 최솟값", "최대를 최소로" | 닫힌 구간 + 성공 시 `hi = mid - 1` | `F..F T..T`의 첫 T가 답 | O(N log R) |
| 답의 범위가 10⁹을 넘음 | `lo`·`hi`·`mid`·판정 누적을 `long long` | `int` 오버플로가 조용히 답을 뒤집는다 | 동일 |
| 답이 실수(소수점 정밀도 요구) | 고정 횟수(100회) 실수 이분 | 정수 경계가 없어 종료 조건을 못 만든다 | O(N · 100) |
| 판정이 O(N)보다 비싼데 N이 크다 | 판정을 먼저 최적화(누적합·그리디) | 판정 비용이 그대로 곱해진다 | 판정 × log R |
| `feasible(X)`가 단조가 아니다 | 파라메트릭 금지 → 완전탐색·DP | 경계가 여러 개라 아무 데나 수렴한다 | 문제에 따름 |
| 배열이 회전·부분정렬 등 변형 | "어느 절반이 정렬됐나"를 먼저 판정 | 정렬된 절반에서만 범위 비교가 안전하다 | O(log N) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 이진탐색의 불변식("정답은 항상 현재 구간 안에 있다")이 무엇이고, `lo`·`hi` 갱신이 그것을 어떻게 지키는지.
- [ ] 설명할 수 있다: `lower_bound`와 `upper_bound`의 정의 차이와, 왜 `upper - lower`가 등장 횟수인지.
- [ ] 설명할 수 있다: 반열린 `[lo, hi)`와 닫힌 `[lo, hi]` 컨벤션의 차이, 그리고 왜 하나만 골라 써야 하는지.
- [ ] 설명할 수 있다: 왜 루프가 반드시 끝나는지(구간 길이가 매번 최소 1 줄어든다는 논증).
- [ ] 설명할 수 있다: `mid = (lo + hi) / 2`가 왜 위험하고 `lo + (hi - lo) / 2`가 왜 안전한지, 그리고 그 차이가 음수 구간에서도 왜 이득인지.
- [ ] 설명할 수 있다: C++의 정수 나눗셈이 0 방향 절삭이라 파이썬의 내림과 다르다는 것과, 그것이 음수 구간 이진탐색에서 어떤 증상으로 나타나는지.
- [ ] 설명할 수 있다: 파라메트릭 서치가 "최적화 문제를 결정 문제로 바꾸는" 기법이라는 말의 뜻.
- [ ] 설명할 수 있다: 단조성이 무엇이고, 주어진 판정 함수가 단조인지 **직접 확인하는 절차**.
- [ ] 설명할 수 있다: 단조가 아닌 판정 함수의 예를 하나 만들고, 왜 이진탐색이 거기서 틀리는지.
- [ ] 설명할 수 있다: "최댓값의 최솟값", "적어도 K개" 같은 문구가 왜 파라메트릭 신호인지.
- [ ] 설명할 수 있다: 최댓값 패턴과 최솟값 패턴에서 성공 시 어느 쪽 경계를 미는지와 그 이유.
- [ ] 설명할 수 있다: `lo`, `hi` 초기값을 잡는 기준(답이 가질 수 있는 최소/최대)과, 좁게 잡으면 생기는 오류.
- [ ] 설명할 수 있다: 판정 함수 안의 누적을 `int`로 받으면 왜 "전 구간 실패"라는 증상으로 나타나는지.
- [ ] 설명할 수 있다: 전체 복잡도가 왜 `판정 비용 × log(범위 크기)`인지.
- [ ] 설명할 수 있다: 실수 이분에서 `while (hi - lo > eps)` 대신 고정 횟수를 쓰는 이유.
- [ ] 설명할 수 있다: 판정 함수를 부작용 없는 순수 함수로 짜야 하는 이유.

**⚠️ 자주 하는 실수**

**1) 단조성을 확인하지 않고 파라메트릭을 적용한다**

```cpp
// ❌ 틀린 코드
bool feasible(long long X) {
    // "자투리 합이 정확히 X인 분할이 있는가?" — X에 대해 T/F가 들쭉날쭉
    return leftoverSumExactly(X);
}

long long lo = 0, hi = 1000000000LL, ans = -1;
while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;
    if (feasible(mid)) { ans = mid; lo = mid + 1; }
    else hi = mid - 1;
}
```

왜: 이진탐색은 T/F가 **딱 한 번** 바뀐다는 전제 위에서 절반을 버린다. "정확히 같은가" 류의 판정은 경계가 여러 개라, 버린 절반에 진짜 답이 남아 있어도 알 수 없다.

```cpp
// ✅ 고친 코드
// 먼저 "X를 1 키우면 판정이 나빠지기만 하는가?"를 확인한다.
bool feasible(long long X) {
    // "자투리 합이 X 이상인가" 처럼 한 방향으로만 움직이는 형태로 재정의
    return leftoverSumAtLeast(X);     // X가 커지면 T -> F 로만 이동한다
}
// 이 형태로 바꿀 수 없으면 파라메트릭이 아니라 DP/완전탐색으로 간다.
```

**2) "성공 시 `lo = mid`"에 내림 `mid`를 써서 무한 루프**

```cpp
// ❌ 틀린 코드
while (lo < hi) {
    long long mid = lo + (hi - lo) / 2;   // 내림
    if (ok(mid)) lo = mid;                // lo=3, hi=4 이면 mid=3, lo=3 -> 그대로
    else         hi = mid - 1;
}
```

왜: `lo = 3, hi = 4`에서 `mid = 3 + (4-3)/2 = 3`이고 성공하면 `lo = 3`. `lo`도 `hi`도 안 움직여 구간이 줄지 않는다. C++에서는 이 루프가 그냥 멈추지 않아 채점에서 시간 초과로만 보인다.

```cpp
// ✅ 고친 코드
while (lo < hi) {
    long long mid = lo + (hi - lo + 1) / 2;   // 올림 — "성공 시 lo=mid"와 반드시 짝
    if (ok(mid)) lo = mid;
    else         hi = mid - 1;
}
// 또는 ans 변수를 쓰는 닫힌 구간 형태로 통일한다:
//   if (ok(mid)) { ans = mid; lo = mid + 1; } else hi = mid - 1;
```

**3) 최댓값을 찾는데 성공 시 왼쪽으로 민다**

```cpp
// ❌ 틀린 코드
long long lo = 1, hi = *max_element(cables.begin(), cables.end()), ans = 0;
while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;
    if (feasible(mid)) {
        ans = mid;
        hi = mid - 1;              // 최솟값 패턴의 갱신
    } else {
        lo = mid + 1;
    }
}
```

왜: `feasible`이 `T..T F..F`이므로 답은 **마지막 T**다. 성공했는데 왼쪽만 남기면 더 큰 T를 영영 못 보고, 답이 작게 나온다(대개 `lo`의 초기값 근처가 출력된다).

```cpp
// ✅ 고친 코드
while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;
    if (feasible(mid)) {
        ans = mid;
        lo = mid + 1;              // 최댓값 -> 성공하면 더 크게
    } else {
        hi = mid - 1;
    }
}
```

**4) `hi` 초기값을 답보다 작게 잡는다**

```cpp
// ❌ 틀린 코드 — "그룹 합의 최댓값을 최소화" 문제
long long lo = 1;
long long hi = *max_element(a.begin(), a.end());   // 한 그룹에 여러 원소가 들어가면
                                                    // max(a)를 넘는다
```

왜: 답의 상한은 "전부 한 그룹"인 `sum(a)`다. `hi`를 `max(a)`로 두면 정답이 탐색 범위 밖이라, 전 구간이 실패하고 초기 `ans`가 그대로 출력된다.

```cpp
// ✅ 고친 코드
long long lo = *max_element(a.begin(), a.end());          // 하한: 최대 원소 하나는 담아야
long long hi = accumulate(a.begin(), a.end(), 0LL);       // 상한: 전부 한 그룹
// accumulate의 초깃값을 0 이 아니라 0LL 로 주는 것도 중요하다 — 0이면 int로 누적된다
```

**5) `lo = 0`으로 시작해 판정 안에서 0으로 나눈다**

```cpp
// ❌ 틀린 코드
long long lo = 0, hi = *max_element(cables.begin(), cables.end());
while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;
    long long cnt = 0;
    for (long long c : cables) cnt += c / mid;   // mid가 0이면 정수 0 나눗셈
    ...
}
```

왜: `mid = 0`이 반드시 한 번은 나온다(`lo = 0, hi = 0`인 순간). 파이썬이라면 `ZeroDivisionError`로 그 자리에서 멈추지만, **C++의 정수 0 나눗셈은 미정의 동작**이라 대개 그대로 프로세스가 죽는다(x86에서는 SIGFPE). 채점에서는 "런타임 에러"로만 보여 원인을 짚기 어렵다.

```cpp
// ✅ 고친 코드
long long lo = 1;                 // 길이는 최소 1
// 또는 판정 안에서 방어한다
bool feasible(long long L) {
    if (L == 0) return true;
    long long cnt = 0;
    for (long long c : cables) cnt += c / L;
    return cnt >= K;
}
```

**6) `mid`와 판정 누적을 `int`로 두어 조용히 뒤집는다**

```cpp
// ❌ 틀린 코드
int lo = 1, hi = 2000000000;      // hi가 이미 int 상한(약 2.147e9)에 가깝다
while (lo <= hi) {
    int mid = (lo + hi) / 2;      // lo+hi 가 int를 넘어 음수 -> mid < 0
    int cnt = 0;
    for (int c : cables) cnt += c / mid;   // cnt도 넘칠 수 있다
    ...
}
```

왜: C++의 부호 있는 정수 오버플로는 **예외도 경고도 없이** 값이 뒤집힌다. `mid`가 음수가 되면 나눗셈 결과가 엉뚱해지고, `cnt`가 음수가 되면 `cnt >= K`가 어디서도 참이 되지 않아 **전 구간 실패**로 나타난다. 그러면 초기 `ans`가 그대로 출력되므로 "경계를 반대로 밀었나?"를 의심하며 엉뚱한 곳을 고치게 된다. 파이썬은 임의 정밀도라 이 증상 자체가 없다.

```cpp
// ✅ 고친 코드 — lo·hi·mid·판정 누적을 전부 long long으로
long long lo = 1, hi = 2000000000LL, ans = -1;
while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;     // 차이는 절대 넘치지 않는다
    long long cnt = 0;
    for (long long c : cables) {
        cnt += c / mid;
        if (cnt >= K) break;                // 조기 종료로 누적 자체를 줄인다
    }
    if (cnt >= K) { ans = mid; lo = mid + 1; }
    else hi = mid - 1;
}
```

**7) 판정 함수가 원본 데이터를 바꾼다**

```cpp
// ❌ 틀린 코드
vector<long long> a;              // 전역
bool feasible(long long X) {
    sort(a.begin(), a.end());     // 매 호출마다 원본을 건드림
    while (!a.empty() && a.back() > X) a.pop_back();   // 데이터가 사라진다
    return (long long)a.size() >= K;
}
```

왜: 이진탐색은 판정을 수십 번 호출한다. 첫 호출이 데이터를 바꿔 놓으면 두 번째 호출부터는 **다른 문제를 푸는 셈**이라 답이 매번 달라진다. C++에서는 인자를 `const vector<long long>&`로 받는 습관을 들이면 컴파일러가 이 실수를 막아 준다(값으로 받으면 매 호출마다 전체 복사가 일어나 느려진다는 별도의 함정도 있다).

```cpp
// ✅ 고친 코드
sort(a.begin(), a.end());         // 정렬 같은 전처리는 루프 밖에서 한 번만
bool feasible(const vector<long long>& a, long long X) {   // 읽기만 하는 순수 함수
    long long cnt = 0;
    for (long long v : a) if (v <= X) cnt++;
    return cnt >= K;
}
```

**8) 실수 이분에서 종료 조건을 오차로 준다**

```cpp
// ❌ 틀린 코드
while (hi - lo > 1e-9) {          // 부동소수 정밀도 한계에 걸리면 영원히 안 줄어든다
    double mid = (lo + hi) / 2;
    if (feasible(mid)) lo = mid;
    else               hi = mid;
}
```

왜: 값이 큰 구간(예: 10⁹ 근처)에서는 `hi - lo`가 `1e-9`까지 내려가기 전에 두 `double`이 표현 한계로 붙어 버려 갱신이 멈추고, 조건은 계속 참이라 무한 루프가 된다. `double`의 유효숫자는 약 15~16자리뿐이라 10⁹ 근처에서 표현 가능한 최소 간격이 이미 1e-7 수준이다.

```cpp
// ✅ 고친 코드
for (int it = 0; it < 100; it++) {   // 횟수 고정 — 오차는 초기 범위의 2^-100배
    double mid = (lo + hi) / 2;
    if (feasible(mid)) lo = mid;
    else               hi = mid;
}
cout << fixed << setprecision(6) << lo << '\n';
// 기본 cout은 유효숫자 6자리라 fixed 없이 큰 값을 내면 지수 표기가 나온다
```

**다음 챕터로**

파라메트릭 서치의 판정 함수 `feasible(X)`는 대개 **그리디**로 짠다("왼쪽부터 X를 넘지 않게 채우고 그룹 수를 센다"가 그 예다). 다음 챕터에서 그리디의 정당성을 교환 논증으로 증명하는 법을 배우면, 판정 함수가 정말 최적으로 세고 있는지를 스스로 검증할 수 있게 된다. 그때도 누적 변수의 타입은 `long long`부터 확인하는 습관이 그대로 유효하다.
