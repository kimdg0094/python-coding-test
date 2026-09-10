## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 챕터의 질문은 하나다. **"나는 지금 무엇을 하나씩 바꿔가며 보고 있는가?"** 그 축이 잘못되면 완전탐색은 느려지고, 축을 바꾸면 같은 답을 훨씬 적은 경우로 센다.
- L1은 **축을 새로 만든다**(정하면 나머지가 줄줄이 결정되는 미지수 하나를 가정). L2는 **축을 갈아끼운다**(쌍·조합 대신 값·기준점·시각을 훑는다).

**개념 지도**

```text
                     brute force is too slow
                               |
                   "which axis am I looping over?"
                               |
           +-------------------+-------------------+
           |                                       |
     ASSUME  (L1)                            RE-AXIS  (L2)
     fix ONE unknown, derive the rest        swap the loop axis
           |                                       |
     for (x = lo; x <= hi; x++)              pair (i, j)    O(n^2)
         build the rest by the rule                | replace with
         contradiction? -> drop                    v
         survived?      -> candidate         sorted ends    O(n log n)
           |                                 threshold val  O(n log n)
           v                                 pivot index    O(n) x O(1)
     O(V * n)                                time event     O(n log n)
           |                                       |
           +-------------------+-------------------+
                               |
                    keep the best / count survivors
```

- 두 갈래의 공통 원리: **자유도(free variable)를 1개로 줄인다.** 자유도가 2개면 후보가 V²개로 늘어난다.
- 축을 잘 고르는 것이 그대로 복잡도 개선이다. `O(n²) → O(n log n)`은 대개 정렬·이벤트 스캔으로 축을 바꾼 결과다.

- 축을 바꿀 때 함께 바뀌는 것이 **값의 크기**다. C++에서는 이 표를 함께 외워 두어야 한다.

```text
   what you accumulate        safe type
   ------------------------   -----------------------------------
   index, count (n <= 1e6)    int
   sum of n values (1e9)      long long      // 1e5 * 1e9 = 1e14
   product of two values      long long      // 1e9 * 1e9 = 1e18
   x + d * (n - 1)            long long      // cast BEFORE the mul
   "no answer yet" flag       -1 or LLONG_MIN, never 0
```

**뼈대 코드**

가정 하나 고정 → 규칙 전개 → 검증 골격.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n = 4, d = 2, H = 10;           // 문제마다 바뀜(입력)

    int cnt = 0;
    int best = -1;                      // 못 찾으면 -1 로 남는다
    for (int x = 1; x <= H; x++) {      // 문제마다 바뀜(가정할 값의 범위)
        bool ok = true;                 // 가정마다 반드시 새로 초기화
        long long cur = x;
        for (int i = 1; i < n; i++) {
            cur = cur + d;              // 문제마다 바뀜(전개 규칙)
            if (cur < 1 || cur > H) {   // 문제마다 바뀜(모순 조건)
                ok = false;
                break;
            }
        }
        if (ok) {                       // 끝까지 살아남은 가정만 후보
            cnt++;
            best = max(best, x);
        }
    }
    cout << cnt << ' ' << best << '\n';
    return 0;
}
```

단조 수열이면 양 끝만 검사한다 — 위 골격의 안쪽 루프를 O(1)로 줄인 형태.

```cpp
int n = 4, d = 2, H = 10;
int cnt = 0;
for (int x = 1; x <= H; x++) {
    long long lo = x;                           // d >= 0 이므로 맨 앞이 최솟값
    long long hi = (long long)x + (long long)d * (n - 1);   // 맨 뒤가 최댓값
    if (lo >= 1 && hi <= H) cnt++;              // 양 끝이 범위 안 -> 중간은 자동
}
```

기준점 하나를 고정하고 나머지를 훑는 골격.

```cpp
int n = 5;
vector<int> a = {3, 1, 4, 1, 5};

long long best = LLONG_MIN;
for (int i = 0; i < n; i++) {           // i를 기준점으로 고정
    for (int j = 0; j < n; j++) {       // 문제에 따라 O(1) 계산으로 대체 가능
        if (j == i) continue;
        long long v = (long long)a[i] - a[j];   // 문제마다 바뀜(평가식)
        best = max(best, v);
    }
}
```

쌍을 정확히 한 번씩 보는 골격 — 순서가 무의미하면 `j = i + 1`.

```cpp
int n = 4;
vector<int> a = {3, 1, 4, 2};

long long best = LLONG_MIN;
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++) {   // (i, j)를 한 번만, 총 n(n-1)/2회
        long long v = (long long)a[i] * a[j];   // 문제마다 바뀜
        best = max(best, v);
    }
```

시각(이벤트)을 축으로 스캔하는 골격 — 구간 겹침 개수를 셀 때의 정석.

```cpp
vector<pair<int,int>> segs = {{1, 4}, {2, 5}, {6, 8}};   // 반열린 구간 [s, e)

vector<pair<int,int>> events;           // {시각, 델타}
for (auto& sg : segs) {
    events.push_back({sg.first,  1});   // 시작: +1
    events.push_back({sg.second, -1});  // 끝: -1
}
sort(events.begin(), events.end());     // 시각 같으면 -1 이 먼저(기본 정렬)

int cur = 0, best = 0;
for (auto& ev : events) {
    cur += ev.second;
    best = max(best, cur);
}
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 규칙은 명확한데 시작값·기준값 하나가 안 정해짐 | 그 값을 가정하고 전개(L1) | 하나만 정하면 나머지가 도미노처럼 결정 | O(V · n) |
| 가정 위에서 만들어지는 수열이 단조 | 양 끝값만 검사 | 최솟값·최댓값이 범위 안이면 중간은 자동 | O(V) |
| 두 수를 골라 최대/최소를 구함 | `sort` 후 양 끝 상수 개만 비교 | 극단값에서만 답이 나옴 | O(n log n) |
| "정확히 k명이 넘는 문턱" 류 | 값(문턱)을 축으로 | 후보 값이 입력에 등장하는 수뿐 | O(n log n) |
| 모든 쌍을 봐야만 하는 작은 n | 이중 for `j = i + 1` | 중복 없이 n(n-1)/2회 | O(n²) |
| 구간이 동시에 몇 개 겹치는지 | 시작 +1 / 끝 −1 이벤트 스캔 | 축을 "쌍"에서 "시각"으로 | O(n log n) |
| 누적합 값을 키로 개수를 셈 | `unordered_map<long long,int>` | 평균 O(1) 조회 | O(n) 평균 |
| 가정할 미지수가 둘 이상으로 보임 | 하나를 다른 하나로 표현해 1개로 줄임 | V² → V | O(V · n) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: "무엇을 가정할지" 고를 때 왜 "정하면 나머지가 결정되는 값"이 좋은 후보인지.
- [ ] 설명할 수 있다: 가정을 두 개 겹치면 복잡도가 왜 O(V·n)에서 O(V²·n)로 커지는지.
- [ ] 설명할 수 있다: 가정한 값이 만드는 수열이 단조일 때, 왜 양 끝값만 검사해도 되는지.
- [ ] 설명할 수 있다: 가정마다 `ok` 같은 상태 변수를 다시 초기화해야 하는 이유.
- [ ] 설명할 수 있다: `x + d * (n - 1)`에서 캐스팅을 곱셈 앞에 놓아야 하는 이유.
- [ ] 설명할 수 있다: "축을 갈아끼운다"는 말이 구체적으로 무엇을 무엇으로 바꾸는 것인지 예를 들어.
- [ ] 설명할 수 있다: n개 중 2개를 고를 때 `j = i + 1`로 두면 중복이 왜 사라지고 개수가 왜 n(n-1)/2인지.
- [ ] 설명할 수 있다: 두 수의 곱을 최대로 만들 때 왜 "가장 작은 두 수"도 후보여야 하는지.
- [ ] 설명할 수 있다: 문턱(합격선) 문제에서 후보 값이 왜 입력에 등장하는 수 근처뿐인지.
- [ ] 설명할 수 있다: 동점이 있으면 "정확히 k명"이 왜 불가능해질 수 있는지.
- [ ] 설명할 수 있다: 구간 겹침 최대 개수를 시작 +1 / 끝 −1 이벤트로 세는 원리.
- [ ] 설명할 수 있다: 반열린 구간 `[s, e)`에서 같은 시각의 끝을 시작보다 먼저 처리해야 하는 이유와, `pair`의 기본 정렬이 왜 그것을 공짜로 해 주는지.
- [ ] 설명할 수 있다: 답이 없을 수 있는 문제에서 `best = 0`이 아니라 `-1`·`LLONG_MIN`으로 시작해야 하는 이유.

**⚠️ 자주 하는 실수**

**1) 가정마다 상태 변수를 초기화하지 않기**

```cpp
// ❌ 틀린 코드
vector<int> res;
bool ok = true;                       // 반복 바깥에서 한 번만 초기화
for (int x = 1; x <= H; x++) {
    for (int i = 1; i < n; i++)
        if (x + d * i > H) ok = false;
    if (ok) res.push_back(x);
}
```

왜: 한 번이라도 `ok`가 false가 되면 그 뒤의 모든 가정이 무조건 실패로 처리된다. 앞쪽 가정이 통과하는 입력에서는 답이 맞아 보여서 더 위험하다.

```cpp
// ✅ 고친 코드
vector<int> res;
for (int x = 1; x <= H; x++) {
    bool ok = true;                   // 가정 하나마다 새로 초기화
    for (int i = 1; i < n; i++)
        if (x + d * i > H) { ok = false; break; }
    if (ok) res.push_back(x);
}
```

**2) 전개식이 `int`에서 넘쳐 검사를 통과해 버린다**

```cpp
// ❌ 틀린 코드
int last = x + d * (n - 1);           // d, n 이 크면 int 를 넘는다
if (last <= H) cnt++;                 // 음수로 돌아가면 조건을 통과한다
```

왜: `d * (n - 1)`이 먼저 `int`로 계산되므로, 넘치는 순간 값이 음수가 되어 `last <= H`가 **참**이 된다. 즉 탈락해야 할 가정이 후보로 채택된다. 오버플로는 예외를 던지지 않으니 원인을 찾기 매우 어렵다.

```cpp
// ✅ 고친 코드
long long last = (long long)x + (long long)d * (n - 1);   // 곱하기 '전에' 캐스팅
if (last <= H) cnt++;
```

**3) 같은 쌍을 두 번 세기(`i < j` 누락)**

```cpp
// ❌ 틀린 코드
int cnt = 0;
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        if (i != j && a[i] + a[j] == target) cnt++;
```

왜: `(i, j)`와 `(j, i)`가 각각 세어져 답이 정확히 2배가 된다. `i != j`는 "같은 원소를 두 번 고르는 것"만 막을 뿐 순서 중복은 못 막는다.

```cpp
// ✅ 고친 코드
int cnt = 0;
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)   // 항상 i < j -> n(n-1)/2회, 중복 없음
        if (a[i] + a[j] == target) cnt++;
```

**4) 정렬 후 "큰 쪽 끝"만 후보로 보기**

```cpp
// ❌ 틀린 코드
sort(a.begin(), a.end());
cout << (long long)a[n-1] * a[n-2] << '\n';   // 가장 큰 두 수의 곱만 본다
```

왜: 음수 두 개의 곱은 양수라 더 클 수 있다. `{-10, -9, 1, 2}`에서 정답은 90인데 이 코드는 2를 출력한다. 극단값을 볼 때는 **양쪽 끝**을 모두 후보로 둬야 한다.

```cpp
// ✅ 고친 코드
sort(a.begin(), a.end());
long long best = max((long long)a[n-1] * a[n-2], (long long)a[0] * a[1]);
cout << best << '\n';
```

**5) 이벤트 정렬에서 동시각 처리 순서를 지정하지 않기**

```cpp
// ❌ 틀린 코드
sort(events.begin(), events.end(), [](const auto& x, const auto& y) {
    return x.first < y.first;          // 같은 시각의 순서를 정하지 않았다
});
```

왜: 반열린 구간 `[s, e)`에서는 `e` 시점에 이미 끝난 것으로 본다. 같은 시각에 시작(+1)이 먼저 처리되면 `[1,2)`와 `[2,5)`를 겹친 것으로 세어 답이 1 커진다. `sort`는 안정 정렬이 아니라서 순서를 지정하지 않으면 **실행마다 결과가 달라질 수도** 있다.

```cpp
// ✅ 고친 코드
sort(events.begin(), events.end());    // pair 기본 정렬: 시각 -> 델타 순
                                       // 델타 -1 < +1 이라 끝이 먼저 처리된다
```

**6) 최댓값 변수를 0으로 초기화**

```cpp
// ❌ 틀린 코드
long long best = 0;
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)
        best = max(best, (long long)a[i] * a[j]);
```

왜: 모든 곱이 음수인 입력(예: `{-3, 2}` → 정답 −6)에서는 한 번도 갱신되지 않아 0이 출력된다. 0은 실제 후보가 아닌데 답이 되어 버린다.

```cpp
// ✅ 고친 코드
long long best = LLONG_MIN;            // <climits>, bits/stdc++.h 에 포함
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)
        best = max(best, (long long)a[i] * a[j]);
```

**7) "불가능"과 "답이 0"을 구별하지 않기**

```cpp
// ❌ 틀린 코드
int ans = 0;                           // 조건을 만족하는 x가 없어도 0을 출력
for (int x = 0; x <= C; x++)
    if (x - k * (n - 1) >= 0 && x <= C) ans = x;
cout << ans << '\n';
```

왜: 어떤 가정도 통과하지 못하는 입력에서 `-1`을 내야 하는데, 초기값 0이 그대로 출력되어 "가능하고 답은 0"으로 오해된다.

```cpp
// ✅ 고친 코드
int ans = -1;                          // 한 번도 갱신 안 되면 불가능
for (int x = 0; x <= C; x++)
    if (x - k * (n - 1) >= 0 && x <= C) ans = x;
cout << ans << '\n';
```

**8) 가정을 두 개 겹쳐서 훑기**

```cpp
// ❌ 틀린 코드
for (int x = 0; x <= V; x++)
    for (int y = 0; y <= V; y++)       // y는 x가 정해지면 이미 결정되는데도 훑는다
        if (ok(x, y)) best = pick(best, x, y);
```

왜: `y`가 규칙으로 `x`에서 계산되는 값이라면 두 번째 반복은 전부 낭비다. `O(V·n)`이면 되는 것이 `O(V²·n)`이 되어 시간 초과가 난다.

```cpp
// ✅ 고친 코드
for (int x = 0; x <= V; x++) {
    int y = derive(x);                 // 규칙으로 바로 계산 -> 자유도 1개
    if (ok(x, y)) best = pick(best, x, y);
}
```

**다음 챕터로**

- 다음 챕터는 "탐색"보다 **"분류"** 에 초점이 있다. 하나의 문제를 서로 겹치지 않고 빠짐없는 케이스로 쪼개는 법을 배운다.
- 이번 챕터의 이벤트 스캔·구간 겹침은 다음 챕터의 "구간 겹침 정리·포함-배제"로 곧장 이어진다. 경계에서 `<`를 쓸지 `<=`를 쓸지 정하는 습관을 그대로 가져가면 된다.
