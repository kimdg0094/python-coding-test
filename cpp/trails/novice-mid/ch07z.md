## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 챕터는 완전탐색의 **축(axis)** 을 두 갈래로 갈라서 배웠다. 하나는 "무엇을 고를까"(부분집합)를 훑는 것이고, 다른 하나는 "정답이 될 값이 얼마일까"를 훑는 것이다.
- 두 갈래는 서로 배타적이지 않다. 같은 문제를 양쪽으로 다 풀 수 있는 경우도 있으니, **후보 개수가 더 작은 축**을 고르면 된다.

**개념 지도**

```text
                      exhaustive search
                              |
          +-------------------+-------------------+
          |                                       |
    axis = CHOICE                           axis = VALUE
    "what do I pick?"                       "what is the answer?"
          |                                       |
    subset of n items                       candidate v in [lo, hi]
    mask = 0 .. (1<<n)-1                    for (v = lo; v <= hi; v++)
          |                                       |
    evaluate(mask) : sum / count            check(v) : one O(n) scan
          |                                       |
    O(2^n * n),  n <= 20                    O(V * n),  V = hi-lo+1
          |                                       |
    +-----+------+                          is check monotone?
    |            |                          O O O X X X  -> yes
  pick/skip    split in two                       |
  (knapsack)   (two teams)                  binary search on answer
                                            (a later chapter)
```

- 왼쪽 갈래는 **답이 "조합"** 일 때, 오른쪽 갈래는 **답이 "하나의 수"** 일 때 쓴다.
- 두 갈래가 만나는 자리가 "두 그룹으로 나누기"다. 한쪽을 고르면 반대쪽이 자동으로 결정되므로 부분집합 하나 = 배정 하나가 된다.

- 비트 연산 관용구는 이 표 하나로 정리된다. C++에서는 **괄호**가 생명이다.

```text
   idiom                         meaning
   ---------------------------   ----------------------------------
   1 << i                        only bit i is on  ( = 2^i )
   (1 << n) - 1                  all n bits on     (full set)
   (mask & (1 << i)) != 0        is item i chosen ?   // parens!
   mask | (1 << i)               add item i
   mask & ~(1 << i)              remove item i
   mask ^ (1 << i)               toggle item i
   __builtin_popcount(mask)      how many bits are on
   1LL << n                      needed when n >= 31
```

**뼈대 코드**

부분집합 완전탐색 — 비트마스크 골격.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n = 4;
    vector<int> w = {3, 7, 4, 9};       // 문제마다 바뀜(물체의 속성)
    int C = 13;                         // 문제마다 바뀜(제약)

    long long best = 0;                 // 답이 음수일 수 있으면 LLONG_MIN
    for (int mask = 0; mask < (1 << n); mask++) {   // 0 .. 2^n - 1
        long long total = 0;
        int cnt = 0;
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {           // i번 물체를 골랐는가
                total += w[i];
                cnt++;
            }
        }
        if (total <= C) {               // 문제마다 바뀜(제약 통과 조건)
            best = max(best, total);    // 문제마다 바뀜(최대/최소/개수)
        }
    }
    cout << best << '\n';
    return 0;
}
```

부분집합 완전탐색 — 재귀 골격(비트 연산이 낯설 때 같은 일을 한다).

```cpp
int n = 3;
vector<int> a = {5, 2, 8};
long long best = 0;

void go(int i, long long total) {   // i번째까지 결정했고, 현재 합은 total
    if (i == n) {                   // 끝까지 결정 -> 여기서 평가
        best = max(best, total);    // 문제마다 바뀜
        return;
    }
    go(i + 1, total + a[i]);        // i번을 고른다
    go(i + 1, total);               // i번을 고르지 않는다
}
// 호출: go(0, 0);
```

두 그룹으로 나누기 골격 — 한쪽만 고르면 반대쪽은 자동이다.

```cpp
int n = 4;
vector<int> a = {1, 6, 11, 5};
long long total = accumulate(a.begin(), a.end(), 0LL);   // 0LL 로 누적

long long best = LLONG_MAX;
for (int mask = 1; mask < (1 << n) - 1; mask++) {   // 양 끝 제외
    long long s = 0;                                // 두 그룹 모두 최소 1개
    for (int i = 0; i < n; i++)
        if ((mask & (1 << i)) != 0) s += a[i];
    long long d = llabs(s - (total - s));           // 문제마다 바뀜(평가식)
    best = min(best, d);
}
```

값 기준 완전탐색 골격 — 후보 값을 하나씩 대입해 판정한다.

```cpp
vector<long long> a = {20, 15, 10, 17};
long long M = 7;                        // 문제마다 바뀜(목표치)

long long lo = 0;
long long hi = *max_element(a.begin(), a.end());   // 문제마다 바뀜(후보 범위)
long long ans = -1;                     // 한 번도 만족 못 하면 그대로 -1
for (long long v = lo; v <= hi; v++) {  // hi 자신도 후보이므로 <= 필수
    long long got = 0;
    for (long long x : a)
        if (x > v) got += x - v;        // 문제마다 바뀜(판정용 계산)
    if (got >= M) ans = v;              // "만족하는 v 중 최대" -> 계속 덮어쓰기
}
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| "몇 개를 골라서 …", 각 물체가 독립적으로 포함/제외 | 부분집합(비트마스크) | 탐색의 축이 물체 그 자체 | O(2^n · n), n ≤ 20 |
| "두 팀/두 그룹으로 남김없이 나눠라" | 부분집합 + 나머지는 자동 | 한쪽을 정하면 반대편이 결정됨 | O(2^n · n) |
| 비트 연산이 헷갈리거나 도중에 가지치기하고 싶다 | 재귀(포함/제외) | 부분 상태를 인자로 들고 다닐 수 있음 | O(2^n) 노드 |
| 고른 개수가 필요하다 | `__builtin_popcount(mask)` | 직접 세는 루프보다 짧고 빠름 | O(1) |
| "조건을 만족하는 가장 큰/작은 값 X를 구하라" | 값 기준 완전탐색 | 답 자체가 하나의 수 | O(V · n) |
| 값 범위 V가 매우 크고 check가 단조 | (다음 단계) 답에 대한 이분탐색 | 참/거짓 경계가 딱 한 곳 | O(n log V) |
| 물체 n개 중 **정확히 2개**만 고른다 | 이중 for `j = i + 1` | 순서가 무의미해 절반만 보면 됨 | O(n²) |
| n이 20을 넘는데 답이 조합 | 부분집합 포기 → DP·그리디 재검토 | 2^n이 폭발함 | — |
| n이 31 이상인 시프트가 필요 | `1LL << n` | `int` 시프트는 오버플로 | — |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 부분집합의 개수가 왜 정확히 2^n인지(각 물체마다 두 갈래 × n번 → 곱의 법칙).
- [ ] 설명할 수 있다: 0 ~ 2^n-1의 정수 하나가 왜 부분집합 하나와 일대일로 대응하는지.
- [ ] 설명할 수 있다: `1 << i`가 무엇이고, `mask & (1 << i)`가 왜 "i번 물체를 골랐는가"를 뜻하는지.
- [ ] 설명할 수 있다: C++에서 `&`가 `==`보다 우선순위가 낮다는 사실과, 그래서 괄호가 필요한 이유.
- [ ] 설명할 수 있다: `(1 << n) - 1`과 `1 << (n - 1)`이 왜 다른 값인지.
- [ ] 설명할 수 있다: `1 << n`이 `int` 연산이라는 사실과, `n ≥ 31`에서 `1LL << n`이 필요한 이유.
- [ ] 설명할 수 있다: "두 그룹으로 나누기"가 왜 부분집합 하나를 고르는 문제와 같은지.
- [ ] 설명할 수 있다: 두 그룹이 모두 비지 않아야 할 때 mask 범위를 `1 .. 2^n-2`로 두는 이유.
- [ ] 설명할 수 있다: 부분집합 완전탐색이 O(2^n · n)이고, 그래서 n ≤ 20이 실전 기준선인 이유.
- [ ] 설명할 수 있다: "값 기준 완전탐색"이 조합 대신 무엇을 훑는지, 언제 그 발상이 가능한지.
- [ ] 설명할 수 있다: 후보 값의 범위 [lo, hi]를 어떻게 정하고, 왜 `v <= hi`여야 하는지.
- [ ] 설명할 수 있다: 판정 함수 check(v)가 단조라는 말이 무슨 뜻이고, 그게 왜 나중에 이분탐색으로 이어지는지.
- [ ] 설명할 수 있다: 최댓값을 담는 변수를 0으로 초기화하면 어떤 입력에서 틀리는지.
- [ ] 설명할 수 있다: n개 중 2개를 고를 때 `i < j`로 두면 왜 중복이 사라지고 개수가 n(n-1)/2가 되는지.

**⚠️ 자주 하는 실수**

**1) 전체 집합 마스크를 `1 << n - 1`로 계산**

```cpp
// ❌ 틀린 코드
int n = 4;
int full = 1 << n - 1;              // "2^n - 1"을 만들려던 의도
for (int mask = 0; mask <= full; mask++) { }
```

왜: `-`가 `<<`보다 먼저 계산되어 `1 << (n - 1)` = 8이 된다. 원하던 `2^n - 1` = 15의 절반만 훑어 부분집합의 절반을 통째로 놓친다. C++의 시프트는 산술 연산자보다 우선순위가 **낮다**는 점을 기억하자.

```cpp
// ✅ 고친 코드
int n = 4;
int full = (1 << n) - 1;            // 15 = 0b1111
for (int mask = 0; mask <= full; mask++) { }
```

**2) 비트 검사에 괄호를 안 씌우고 `== 1`을 붙이기**

```cpp
// ❌ 틀린 코드
for (int i = 0; i < n; i++)
    if (mask & (1 << i) == 1)       // i번 비트가 켜졌는지 보려던 의도
        total += w[i];
```

왜: 두 가지가 동시에 틀렸다. 첫째, C++에서 `&`는 `==`보다 우선순위가 **낮아** 식이 `mask & ((1 << i) == 1)`로 묶인다(파이썬은 반대라 그대로 옮기면 안 된다). 둘째, `mask & (1 << i)`의 값은 켜져 있을 때 `1`이 아니라 `2^i`다.

```cpp
// ✅ 고친 코드
for (int i = 0; i < n; i++)
    if ((mask & (1 << i)) != 0)     // 괄호로 묶고 0 과 비교
        total += w[i];
```

**3) 최댓값 변수를 0으로 초기화**

```cpp
// ❌ 틀린 코드
long long best = 0;
for (int mask = 0; mask < (1 << n); mask++) {
    long long s = 0;
    for (int i = 0; i < n; i++)
        if ((mask & (1 << i)) != 0) s += v[i];
    best = max(best, s);
}
```

왜: "반드시 1개 이상 골라야 한다"인데 모든 가치가 음수라면 정답도 음수다. 그런데 `best = 0`은 한 번도 갱신되지 않아 0이 출력된다.

```cpp
// ✅ 고친 코드
long long best = LLONG_MIN;
for (int mask = 1; mask < (1 << n); mask++) {   // 최소 1개 -> mask=0 제외
    long long s = 0;
    for (int i = 0; i < n; i++)
        if ((mask & (1 << i)) != 0) s += v[i];
    best = max(best, s);
}
```

**4) 같은 쌍을 두 번 세기(`i < j` 누락)**

```cpp
// ❌ 틀린 코드
int cnt = 0;
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        if (i != j && a[i] + a[j] == target) cnt++;
```

왜: `(i, j)`와 `(j, i)`가 서로 다른 반복에서 각각 세어져 답이 정확히 2배가 된다. `i != j`는 "같은 원소 두 번"만 막을 뿐 순서 중복은 못 막는다.

```cpp
// ✅ 고친 코드
int cnt = 0;
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)     // 항상 i < j -> 각 쌍을 정확히 한 번
        if (a[i] + a[j] == target) cnt++;
```

**5) 값 후보의 상한을 빠뜨리기**

```cpp
// ❌ 틀린 코드
long long ans = -1;
for (long long v = lo; v < hi; v++)     // hi 자신은 한 번도 검사되지 않는다
    if (check(v)) ans = v;
```

왜: `v < hi`는 `hi - 1`에서 멈춘다. 정답이 딱 `hi`인 입력(예: 가장 높은 나무 높이가 그대로 답)에서만 틀려, 예제로는 잘 안 잡힌다.

```cpp
// ✅ 고친 코드
long long ans = -1;
for (long long v = lo; v <= hi; v++)    // 상한 포함
    if (check(v)) ans = v;
```

**6) 판정 계산을 `int`로 하다 넘치기**

```cpp
// ❌ 틀린 코드
int got = 0;
for (int x : h)
    if (x > H) got += x - H;            // 나무 100만 그루 x 높이 10^9
```

왜: 얻는 양의 총합은 쉽게 `int`(약 21억)를 넘는다. 넘치면 음수로 돌아가 `got >= M` 판정이 거짓이 되고, "가능한데 불가능하다"는 답이 나온다. 게다가 `H` 이하인 나무의 기여를 0으로 막지 않으면 음수가 더해져 총량이 깎인다.

```cpp
// ✅ 고친 코드
long long got = 0;
for (int x : h)
    if (x > H) got += (long long)(x - H);   // 또는 got += max(0LL, (long long)x - H);
```

**7) 두 그룹으로 나눌 때 빈 그룹을 허용**

```cpp
// ❌ 틀린 코드
for (int mask = 0; mask < (1 << n); mask++) {   // mask = 0 이면 한 그룹이 빈다
    long long s = 0;
    for (int i = 0; i < n; i++)
        if ((mask & (1 << i)) != 0) s += a[i];
}
```

왜: "두 팀 모두 최소 1명"이라는 조건이 있으면 mask가 `0`(한 팀이 빔)이나 `2^n - 1`(반대 팀이 빔)인 경우는 유효한 분할이 아니다. 그대로 두면 항상 "전부 한 팀"이 최적으로 뽑힌다.

```cpp
// ✅ 고친 코드
for (int mask = 1; mask < (1 << n) - 1; mask++) {   // 양 끝을 배제
    long long s = 0;
    for (int i = 0; i < n; i++)
        if ((mask & (1 << i)) != 0) s += a[i];
}
```

**8) `mask`는 `long long`인데 `1 << i`로 검사하기**

```cpp
// ❌ 틀린 코드
for (long long mask = 0; mask < (1LL << n); mask++)
    for (int i = 0; i < n; i++)
        if ((mask & (1 << i)) != 0) s += a[i];   // i >= 31 이면 못 읽는다
```

왜: 루프 상한만 `1LL`로 고치고 검사식을 그대로 두면, `1 << i`는 여전히 `int` 연산이라 `i ≥ 31`에서 오버플로한다. 위쪽 비트를 못 읽어 큰 부분집합의 원소가 통째로 빠진다.

```cpp
// ✅ 고친 코드
for (long long mask = 0; mask < (1LL << n); mask++)
    for (int i = 0; i < n; i++)
        if ((mask & (1LL << i)) != 0) s += a[i];  // 검사식도 1LL 로
```

**다음 챕터로**

- 다음 챕터는 "고를 대상"이 뚜렷하지 않은 문제를 다룬다. **미지수 하나를 가정**하고 나머지를 규칙대로 전개하거나, 아예 **탐색의 축을 다른 것으로 갈아끼워** 경우의 수를 줄인다.
- 여기서 익힌 "탐색의 축을 의식한다"는 습관이 그대로 이어진다. 지금은 축이 물체/값 두 가지였다면, 다음에는 가정·기준점·시각 같은 축이 추가된다.
