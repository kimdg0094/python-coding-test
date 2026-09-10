## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 레슨은 Ch04(이진탐색) 전체를 한 장으로 묶는 정리다. 새 유형을 배우는 대신, 두 레슨이 사실은 **하나의 질문**의 변형이었음을 확인하고, 바로 꺼내 쓸 수 있는 뼈대와 자주 넘어지는 지점을 모아 둔다.
- 그 하나의 질문은 이것이다. **"F가 죽 이어지다 T로 딱 한 번 바뀌는 줄에서, 그 경계는 어디인가?"** 값 찾기도, lower/upper bound도, 파라메트릭 서치도 전부 이 질문의 다른 얼굴이다. 배열이 정렬돼 있어야 한다는 조건은 이 질문을 만들기 위한 수단일 뿐, 진짜 조건은 **단조성**이다.
- C++에서는 여기에 **자료형 검산**이 하나 더 붙는다. 파라메트릭 서치의 `lo`·`hi`는 인덱스가 아니라 **답의 값**이라 10⁹이나 10¹⁸까지 갈 수 있고, 그 순간 `mid = (lo + hi) / 2`가 오버플로로 무너진다. `mid = lo + (hi - lo) / 2`를 습관으로 굳혀야 하는 진짜 이유가 이것이다.

**개념 지도**

- 문제를 만나면 가장 먼저 "탐색 공간이 인덱스인가, 답 자체인가"를 정한다. 여기서 갈라진 뒤로는 골격이 거의 같다.

```text
  Ch04 map : binary search = find the first T in a monotone line

  predicate over the search space :  F F F F F T T T T T
                                              ^ the boundary
   |
   +-- (A) search space = INDEX of a sorted array
   |     |
   |     +-- "is x here ?"         closed [lo, hi]   while lo <= hi
   |     |                         hit -> mid,  empty range -> -1
   |     |                         stl : binary_search(b, e, x)
   |     |
   |     +-- "first i, a[i] >= x"  lower_bound(b, e, x) - b
   |     +-- "first i, a[i] >  x"  upper_bound(b, e, x) - b
   |           count(x)     = upper(x) - lower(x)
   |           count(a..b)  = upper(b) - lower(a)
   |
   +-- (B) search space = THE ANSWER itself   (parametric search)
         |
         +-- ok() looks like T T T F F F  ->  largest True
         +-- ok() looks like F F F T T T  ->  smallest True
               cost = O( log(range) * cost of ok )
               lo, hi may be up to 1e18  ->  use long long
```

- 왜 답이 `lo`인지는 **불변식** 한 줄에서 나온다. 구간 밖은 이미 판정이 끝났고, 구간 안만 모른다.

```text
  half-open form  [lo, hi)  :  what each region means

  index    0 ........ lo-1 | lo ........ hi-1 | hi ........ n
  status   all FALSE       | UNKNOWN          | all TRUE
           already settled | still shrinking  | already settled

  start : lo = 0, hi = n            # 양쪽 끝이 비어 있어 처음부터 참
  a[mid] is FALSE -> lo = mid + 1   # mid 까지 FALSE 로 확정
  a[mid] is TRUE  -> hi = mid       # mid 부터 TRUE 로 확정
  end   : lo == hi                  # UNKNOWN 이 비면 그 자리가 첫 TRUE
  # 이 규약이 곧 STL 의 [first, last) 구간이다
```

- 네 가지 형태의 차이는 표 한 장이면 끝난다. **구간의 종류·루프 조건·갱신식·답의 출처는 한 묶음으로 움직인다.** 이 묶음을 섞는 순간 버그가 난다.

```text
  form         range       loop cond   move on F/T     answer
  ----------   ---------   ---------   -------------   ------------
  exists       [lo, hi]    lo <= hi    mid+1 / mid-1   mid  or  -1
  boundary     [lo, hi)    lo <  hi    mid+1 / mid     lo
  param max    [LO, HI]    lo <= hi    mid+1 / mid-1   ans (saved)
  param min    [LO, HI]    lo <= hi    mid-1 / mid+1   ans (saved)
  # 마지막 두 줄은 갱신 방향만 서로 반대다
```

**뼈대 코드**

- (1) 존재 판정 — 닫힌 구간 `[lo, hi]`.

```cpp
// arr 는 오름차순. 있으면 인덱스, 없으면 -1
int bsearch_exists(const vector<int>& arr, int x) {
    int lo = 0, hi = (int)arr.size() - 1;   // 닫힌 구간 : hi 도 후보다
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;       // (lo+hi)/2 는 오버플로 위험
        // 불변식 : 답이 있다면 반드시 [lo, hi] 안에 있다
        if (arr[mid] == x) return mid;      // 여러 개면 어느 것이 나올지 모른다
        if (arr[mid] < x) lo = mid + 1;     // mid 이하는 전부 탈락
        else              hi = mid - 1;     // mid 이상은 전부 탈락
    }
    return -1;                              // 구간이 비었다(lo > hi) = 없음
}
```

- (2) 경계 찾기 — 반열린 구간 `[lo, hi)`. 두 함수는 **부등호 한 글자**만 다르다.

```cpp
// arr[i] >= x 인 첫 i  (없으면 n)
int lower_bd(const vector<int>& arr, int x) {
    int lo = 0, hi = (int)arr.size();       // hi = n 이어야 "없음(=n)"이 후보에 남는다
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        // 불변식 : i < lo 는 전부 arr[i] < x , i >= hi 는 전부 arr[i] >= x
        if (arr[mid] < x) lo = mid + 1;
        else              hi = mid;         // mid 도 후보라 버리지 않는다
    }
    return lo;                              // 불변식 + (lo==hi) => 첫 TRUE
}

// arr[i] > x 인 첫 i  (없으면 n)
int upper_bd(const vector<int>& arr, int x) {
    int lo = 0, hi = (int)arr.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        // 불변식 : i < lo 는 전부 arr[i] <= x , i >= hi 는 전부 arr[i] > x
        if (arr[mid] <= x) lo = mid + 1;    // lower 와의 유일한 차이 : '=' 를 왼쪽에
        else               hi = mid;
    }
    return lo;
}
```

- (3) 같은 일을 표준 라이브러리로. 대회·시험에서는 이쪽이 안전하다. **범위가 정렬돼 있어야 한다는 전제는 그대로다.**

```cpp
sort(arr.begin(), arr.end());               // 전제 : 정렬된 범위에서만 옳다

int lo = (int)(lower_bound(arr.begin(), arr.end(), x) - arr.begin());
int up = (int)(upper_bound(arr.begin(), arr.end(), x) - arr.begin());

bool found     = binary_search(arr.begin(), arr.end(), x);   // 존재 여부만
int  count_x   = up - lo;                                    // x 의 개수
int  first_pos = found ? lo : -1;                            // 첫 위치
int  last_pos  = found ? up - 1 : -1;                        // 마지막 위치
int  count_ab  = (int)(upper_bound(arr.begin(), arr.end(), b)
                     - lower_bound(arr.begin(), arr.end(), a));  // [a,b] 개수

int le_idx = up - 1;    // x 이하 최댓값의 위치 (-1 이면 없음)
int ge_idx = lo;        // x 이상 최솟값의 위치 (n 이면 없음)

auto pr = equal_range(arr.begin(), arr.end(), x);   // lower/upper 를 한 번에

// 정렬을 유지한 삽입 : 탐색 O(log n) + 이동 O(n)
arr.insert(lower_bound(arr.begin(), arr.end(), x), x);

// set / map 은 반드시 멤버 함수를 쓴다 (알고리즘 버전은 O(n) 이 된다)
set<int> s;
auto it = s.lower_bound(x);   // O(log n)
```

- (4) 파라메트릭 서치 — **참인 최댓값**(`ok`가 `T T T F F F` 모양).

```cpp
// 판정 함수가 문제의 본체. 예 : 높이 mid 로 잘라 얻는 나무의 양
bool ok_max(long long mid, const vector<long long>& arr, long long need) {
    long long got = 0;
    for (long long x : arr)
        if (x > mid) got += x - mid;        // 누적은 long long (int 는 넘친다)
    return got >= need;                     // mid 가 커지면 got 은 줄어든다 = 단조
}

long long solve_max(const vector<long long>& arr, long long need) {
    long long lo = 0, hi = *max_element(arr.begin(), arr.end());  // 답의 후보 범위
    long long ans = -1;                     // "가능한 답이 하나도 없음"을 뜻하는 값
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2; // 값 범위가 크면 반드시 이 형태로
        // 불변식 : ans = 지금까지 본 것 중 ok 가 참인 가장 큰 값
        //          [lo, hi] 밖은 판정이 이미 끝났다
        if (ok_max(mid, arr, need)) {
            ans = mid;                      // mid 자신도 답 후보 -> 반드시 기록
            lo = mid + 1;                   // 더 큰 쪽을 노린다
        } else {
            hi = mid - 1;
        }
    }
    return ans;
}
```

- (5) 파라메트릭 서치 — **참인 최솟값**(`ok`가 `F F F T T T` 모양). 골격은 같고 방향만 뒤집는다.

```cpp
// 예 : 한 묶음에 mid 만큼 담으면 k 묶음 안에 끝나는가
bool ok_min(long long mid, const vector<long long>& arr, int k) {
    long long groups = 1, cur = 0;
    for (long long x : arr) {
        if (x > mid) return false;          // 하나도 못 담으면 애초에 불가능
        if (cur + x > mid) { groups++; cur = 0; }
        cur += x;
    }
    return groups <= k;                     // mid 가 커지면 groups 는 줄어든다 = 단조
}

long long solve_min(const vector<long long>& arr, int k) {
    long long lo = 1;
    long long hi = accumulate(arr.begin(), arr.end(), 0LL);  // 0LL ! 0 이면 int 합
    long long ans = hi;                     // 항상 참인 값으로 초기화(= 안전한 상한)
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        // 불변식 : ans = 지금까지 본 것 중 ok 가 참인 가장 작은 값
        if (ok_min(mid, arr, k)) {
            ans = mid;
            hi = mid - 1;                   // 더 작은 쪽을 노린다
        } else {
            lo = mid + 1;
        }
    }
    return ans;
}
```

- (6) 답이 실수일 때 — 종료 조건을 값이 아니라 **횟수**로 건다.

```cpp
double solve_real(double LO, double HI) {
    double lo = LO, hi = HI;
    for (int iter = 0; iter < 100; iter++) {   // 100회면 2^-100 배까지 좁혀진다
        double mid = lo + (hi - lo) / 2;       // 불변식 : 답은 항상 [lo, hi] 안
        if (ok_real(mid)) lo = mid;            // 문제마다 방향이 바뀜
        else              hi = mid;
    }
    return lo;                                 // lo 와 hi 의 차이는 이미 무시 가능
}
// while (lo < hi) 는 부동소수점에서 끝나지 않을 수 있다 - 절대 쓰지 않는다
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 정렬 배열에 값이 있는지만 필요 | `binary_search(b, e, x)` | 경계 실수가 원천 봉쇄된다 | O(log n) |
| 정렬 배열에서 위치 하나만 필요 | 닫힌 구간 이진탐색 | 찾는 즉시 반환해 가장 짧다 | O(log n) |
| 중복 값의 **첫** 위치 | `lower_bound` | "x 이상인 첫 자리"가 곧 정의 | O(log n) |
| 중복 값의 **마지막** 위치 | `upper_bound - 1` | "x 초과인 첫 자리"의 바로 왼쪽 | O(log n) |
| 특정 값의 개수 | `upper_bound - lower_bound` | 두 경계 사이가 곧 그 값의 구간 | O(log n) |
| 두 경계가 모두 필요 | `equal_range` | 한 번에 pair 로 받는다 | O(log n) |
| 구간 `[a, b]` 안의 원소 개수 | `upper_bound(b) - lower_bound(a)` | 양 끝을 각각 다른 경계로 잡는다 | O(log n) |
| x 이하 최댓값 / x 이상 최솟값 | `upper_bound(x)-1` / `lower_bound(x)` | 경계 바로 옆 칸이 답이다 | O(log n) |
| `set`·`map`에서 경계 찾기 | `s.lower_bound(x)` (**멤버 함수**) | 알고리즘 버전은 O(n)이 된다 | O(log n) |
| 정렬이 안 된 배열에서 딱 한 번 찾기 | 그냥 선형 탐색 | 정렬 O(n log n)이 탐색보다 비싸다 | O(n) |
| 정렬 안 된 배열에 질의가 q번 | 한 번 `sort` 후 이진탐색 | 정렬 비용을 q번에 나눠 갚는다 | O(n log n + q log n) |
| "최대 얼마까지 가능한가" | 파라메트릭(참인 최댓값) | 판정이 단조면 답도 이분 가능 | O(log R × 판정) |
| "최소 얼마면 충분한가" | 파라메트릭(참인 최솟값) | 같은 골격, 갱신 방향만 반대 | O(log R × 판정) |
| 답의 범위가 10⁹을 넘는다 | `long long` + `lo + (hi-lo)/2` | `int` 오버플로로 mid가 음수가 된다 | O(log R × 판정) |
| 답이 실수이고 오차가 허용된다 | 고정 횟수 반복(100회 정도) | `lo < hi`가 부동소수점에서 안 끝난다 | O(100 × 판정) |
| 삽입·삭제가 섞이며 순위를 계속 물어봄 | 이진탐색만으로는 부족 | 정렬 유지에 O(n) 이동이 든다 | 삽입 O(n) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 이진탐색의 진짜 전제가 "정렬"이 아니라 "단조성"인 이유.
- [ ] 설명할 수 있다: `arr[mid] < x`를 확인한 순간 왼쪽 절반 **전체**를 버려도 되는 근거.
- [ ] 설명할 수 있다: 후보가 n → n/2 → … 로 줄어 왜 정확히 약 log₂n번에 끝나는지.
- [ ] 설명할 수 있다: 닫힌 구간 `[lo, hi]`와 반열린 구간 `[lo, hi)`에서 초기값·루프 조건·갱신식이 어떻게 한 묶음으로 달라지는지.
- [ ] 설명할 수 있다: 반열린 구간 구현의 불변식 두 줄과, 그로부터 답이 `lo`인 이유.
- [ ] 설명할 수 있다: `lower_bound`의 `hi`를 `n-1`이 아니라 `n`으로 두어야 하는 이유.
- [ ] 설명할 수 있다: lower와 upper가 부등호 한 글자(`<` vs `<=`)로 갈리는 이유.
- [ ] 설명할 수 있다: `upper - lower`가 왜 등장 횟수이고, 값이 없으면 왜 0이 되는지.
- [ ] 설명할 수 있다: `lower_bound` 결과만으로 존재 여부를 판정하면 안 되는 이유와 필요한 두 검사.
- [ ] 설명할 수 있다: 내림 mid에서 `lo = mid`가 왜 무한 루프이고, 올림 mid로 바꾸면 왜 안전한지.
- [ ] 설명할 수 있다: `mid = (lo + hi) / 2`가 언제 오버플로하고, `lo + (hi - lo) / 2`가 왜 안전한지.
- [ ] 설명할 수 있다: `set`·`map`에서 알고리즘 버전 `lower_bound`를 쓰면 왜 O(n)이 되는지.
- [ ] 설명할 수 있다: 파라메트릭 서치에서 "단조 술어"가 무엇이고, 그것이 없으면 왜 답이 틀리는지.
- [ ] 설명할 수 있다: 참인 최댓값과 참인 최솟값 두 형태의 갱신식 차이와, 각각의 `ans` 초기값을 정하는 기준.
- [ ] 설명할 수 있다: 파라메트릭의 전체 복잡도가 왜 `log(답 범위) × 판정 비용`인지.
- [ ] 설명할 수 있다: 실수 이진탐색에서 `while (lo < hi)`를 쓰면 안 되는 이유.
- [ ] 설명할 수 있다: 정렬 후 이진탐색이 유리해지는 질의 수의 기준(언제부터 정렬이 이득인지).

**⚠️ 자주 하는 실수**

**1) `mid = (lo + hi) / 2`로 써서 오버플로를 낸다**

```cpp
// ❌ 틀린 코드
long long lo = 1, hi = 1000000000000000000LL;   // 답의 범위가 1e18
while (lo <= hi) {
    int mid = (lo + hi) / 2;      // int 에 담는 것부터 틀렸고
    if (ok(mid)) lo = mid + 1;    // lo+hi 가 long long 범위도 위협한다
    else hi = mid - 1;
}
// 인덱스 탐색에서도 lo, hi 가 각각 20억에 가까우면 int 합이 음수가 된다
```

왜: 두 값을 먼저 더하면 합이 자료형의 최댓값을 넘을 수 있다. 넘는 순간 `mid`가 음수가 되어 배열 접근이면 즉사하고, 값 탐색이면 조용히 틀린 답이 나온다. **뺄셈을 먼저 하면 합이 커지지 않는다.**

```cpp
// ✅ 고친 코드
long long lo = 1, hi = 1000000000000000000LL;
while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;   // 타입도 범위도 안전
    if (ok(mid)) lo = mid + 1;
    else hi = mid - 1;
}
```

**2) 내림 mid를 쓰면서 `lo = mid`로 갱신한다**

```cpp
// ❌ 틀린 코드
while (lo < hi) {
    int mid = lo + (hi - lo) / 2;
    if (ok(mid)) lo = mid;        // 구간이 [3, 4] 가 되면 영원히 멈추지 않는다
    else         hi = mid - 1;
}
```

왜: C++의 정수 나눗셈은 양수에서 내림이라 `lo < hi`일 때 `lo <= mid < hi`다. `lo = 3, hi = 4`면 `mid = 3`이고, `lo = mid`는 `lo = 3`으로 **아무것도 바꾸지 않는다.** 같은 상태가 무한히 반복되어 시간 초과로만 보인다.

```cpp
// ✅ 고친 코드
while (lo < hi) {
    int mid = lo + (hi - lo + 1) / 2;   // 올림 mid : lo < mid <= hi 가 보장된다
    if (ok(mid)) lo = mid;              // 이제 lo 가 반드시 늘어난다
    else         hi = mid - 1;
}
```

**3) 닫힌 구간에 `hi = mid`를 쓴다**

```cpp
// ❌ 틀린 코드
int lo = 0, hi = n - 1;
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    if (arr[mid] < x) lo = mid + 1;
    else              hi = mid;   // 닫힌 구간인데 mid 를 남겼다
}
```

왜: `lo == hi`가 되면 `mid == lo == hi`인데, `hi = mid`는 구간을 전혀 줄이지 못한다. 그런데 루프 조건은 `lo <= hi`라 계속 참이다. 즉 **구간이 비는 순간이 영원히 오지 않는다.** 구간의 종류와 갱신식은 한 묶음이라 섞으면 안 된다.

```cpp
// ✅ 고친 코드
int lo = 0, hi = n - 1;
while (lo <= hi) {                // 닫힌 구간이면 mid 를 반드시 버린다
    int mid = lo + (hi - lo) / 2;
    if (arr[mid] < x) lo = mid + 1;
    else              hi = mid - 1;
}
// 경계가 필요하면 반열린 구간(hi = n / while lo < hi / hi = mid)으로 통째로 바꾼다
```

**4) 두 유파를 섞어 `hi`를 `n-1`로 시작한다**

```cpp
// ❌ 틀린 코드
int lower_bd(const vector<int>& arr, int x) {
    int lo = 0, hi = (int)arr.size() - 1;   // 반열린 골격인데 hi 를 마지막 인덱스로
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] < x) lo = mid + 1;
        else              hi = mid;
    }
    return lo;
}
```

왜: 답의 후보에는 "조건을 만족하는 원소가 하나도 없다"는 뜻의 **인덱스 n**도 들어 있다. `hi = n - 1`로 시작하면 이 후보가 처음부터 빠져, `x`가 배열 최댓값보다 클 때 `n` 대신 `n-1`이 나온다. `arr = {1, 2, 3}`, `x = 9`면 3이어야 할 답이 2가 된다. STL이 이때 `end()`를 돌려주는 것도 같은 이유다.

```cpp
// ✅ 고친 코드
int lower_bd(const vector<int>& arr, int x) {
    int lo = 0, hi = (int)arr.size();       // 반열린 구간은 hi = n 에서 시작
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] < x) lo = mid + 1;
        else              hi = mid;
    }
    return lo;
}
```

**5) 정렬되지 않은 범위에 `lower_bound`를 건다**

```cpp
// ❌ 틀린 코드
vector<int> arr(n);
for (int i = 0; i < n; i++) cin >> arr[i];   // 입력 순서 그대로
auto it = lower_bound(arr.begin(), arr.end(), x);   // 값이 있어도 못 찾는다
cout << (it != arr.end() && *it == x ? "YES" : "NO") << '\n';
```

왜: `arr[mid] < x`라는 사실이 "왼쪽 전부가 x가 아니다"를 보장하는 것은 **오름차순일 때뿐**이다. 정렬돼 있지 않으면 버린 절반에 답이 숨어 있어도 알 길이 없다. 더 나쁜 것은 **표준 함수가 오류를 내지 않고 의미 없는 값을 조용히 돌려준다**는 점이다. 예제만으로는 버그가 안 보인다.

```cpp
// ✅ 고친 코드
sort(arr.begin(), arr.end());                       // 이진탐색 전에 반드시 정렬
auto it = lower_bound(arr.begin(), arr.end(), x);
cout << (it != arr.end() && *it == x ? "YES" : "NO") << '\n';
// 질의가 한 번뿐이라면 정렬 O(n log n) 보다 find() O(n) 이 오히려 싸다
```

**6) `lower_bound` 결과를 존재 여부로 그대로 쓴다**

```cpp
// ❌ 틀린 코드
auto it = lower_bound(arr.begin(), arr.end(), x);
if (*it == x) cout << "YES\n";     // x 가 최댓값보다 크면 it == end() -> 미정의 동작
// 인덱스로 받아도 같다
int i = (int)(lower_bound(arr.begin(), arr.end(), x) - arr.begin());
if (arr[i] == x) { /* i == n 이면 범위 밖 */ }
```

왜: `lower_bound`는 "x를 넣을 자리"를 돌려줄 뿐, x가 있다고 말해 주지 않는다. x가 없으면 그 자리에는 x보다 큰 값이 있고, x가 모든 원소보다 크면 그 자리는 배열 **밖**인 `end()`(= 인덱스 n)다. 파이썬이라면 `IndexError`로 즉시 알려 주지만, **C++에서는 남의 메모리를 읽어 우연히 통과하기도 한다.**

```cpp
// ✅ 고친 코드
auto it = lower_bound(arr.begin(), arr.end(), x);
if (it != arr.end() && *it == x) cout << "YES\n";   // 범위 먼저, 값 비교는 그다음
else                             cout << "NO\n";
// 존재 여부만 필요하면 이 두 조건을 합친 binary_search 가 읽기 쉽다
```

**7) 중복 값에서 첫/마지막 위치를 잘못 집는다**

```cpp
// ❌ 틀린 코드
// arr = {1, 2, 2, 2, 3} 에서 2의 마지막 위치를 구한다
int last  = (int)(upper_bound(arr.begin(), arr.end(), 2) - arr.begin());  // 4
int first = last - 1;                                                     // 3
// 4번 칸은 이미 3이고, 3번 칸은 첫 위치가 아니라 마지막 위치다
```

왜: `upper_bound`는 "2보다 **큰** 첫 자리", 즉 2의 구간이 **끝난 다음 칸**을 가리킨다. 그 칸 자체는 2가 아니다. 두 경계는 원소가 아니라 **원소 사이의 틈**을 가리킨다고 기억하면 헷갈리지 않는다.

```cpp
// ✅ 고친 코드
int lo  = (int)(lower_bound(arr.begin(), arr.end(), 2) - arr.begin());  // 1 : 시작
int up  = (int)(upper_bound(arr.begin(), arr.end(), 2) - arr.begin());  // 4 : 끝 다음
int last = up - 1;                                                      // 3 : 끝
int cnt  = up - lo;                                                     // 3 개
```

**8) 파라메트릭에서 답을 저장하지 않고 `lo`를 그대로 쓴다**

```cpp
// ❌ 틀린 코드
long long lo = 1, hi = 1000000;
while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;
    if (ok(mid)) lo = mid + 1;
    else         hi = mid - 1;
}
cout << lo << '\n';        // 참인 최댓값을 원했는데 그보다 1 큰 값이 나온다
```

왜: 루프가 끝나면 `lo`는 항상 "처음으로 거짓이 되는 값"에 서 있다. 참인 최댓값은 그 하나 왼쪽인 `lo - 1`이다. `lo - 1`을 외워 쓰는 것보다 **참일 때마다 `ans`에 기록**하는 편이 두 형태(최댓값·최솟값) 모두에 그대로 통해 안전하다.

```cpp
// ✅ 고친 코드
long long lo = 1, hi = 1000000;
long long ans = -1;                 // 참인 후보가 하나도 없을 때의 값
while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;
    if (ok(mid)) { ans = mid; lo = mid + 1; }   // 참인 순간마다 갱신
    else         { hi = mid - 1; }
}
cout << ans << '\n';
```

**9) 판정 함수 안에서 누적을 `int`로 받는다**

```cpp
// ❌ 틀린 코드
bool ok(int mid) {
    int got = 0;                    // 나무 길이 합이 최대 1e14 까지 간다
    for (int x : arr) if (x > mid) got += x - mid;
    return got >= need;             // int 가 넘쳐 음수가 되면 판정이 뒤집힌다
}
```

왜: 복잡도는 `O(log R × n)`으로 맞는데 **판정이 틀려** 이분탐색이 엉뚱한 방향으로 간다. 오버플로가 판정 함수 안에서 일어나면 단조성 자체가 깨져 보이므로, "단조가 아닌가?" 하고 알고리즘을 의심하게 되어 원인을 찾기 더 어렵다. `accumulate(v.begin(), v.end(), 0)`의 `0`도 같은 함정이다 — `0LL`로 써야 한다.

```cpp
// ✅ 고친 코드
bool ok(long long mid) {
    long long got = 0;              // 누적은 항상 long long
    for (long long x : arr) if (x > mid) got += x - mid;
    return got >= need;
}
// 합계 초기값도 타입을 못 박는다
long long total = accumulate(arr.begin(), arr.end(), 0LL);
```

**10) 파라메트릭에서 단조성을 확인하지 않는다**

```cpp
// ❌ 틀린 코드
bool ok(int mid) {
    return count_of_divisors(mid) == 6;   // 참·거짓이 들쭉날쭉하다
}
// ok 가 F T F F T ... 처럼 흩어져 있으면 절반을 버릴 근거가 없다
```

왜: 이진탐색이 성립하려면 술어가 **한 번만** 뒤집혀야 한다(`T…TF…F` 또는 `F…FT…T`). `ok`가 오르내리면 `ok(mid)`가 거짓이라는 사실이 "오른쪽 전부 거짓"을 뜻하지 않으므로, 버린 절반에 답이 남는다. 판정 함수를 쓰기 전에 **"mid를 키우면 ok가 한 방향으로만 변하는가"**를 반드시 말로 확인한다.

```cpp
// ✅ 고친 코드
bool ok(long long mid) {
    return count_up_to(mid) >= k;   // mid 가 커지면 개수는 절대 줄지 않는다 = 단조
}
// 단조가 아니면 이진탐색을 포기하고 다른 접근(완전탐색·투 포인터 등)으로 바꾼다
```

**다음 챕터로**

- Ch05(스택·큐·덱)는 "구간을 반으로 줄인다"가 아니라 **"한 번 훑으면서 후보를 담아 둔다"**로 방향을 바꾼다. 이진탐색이 정렬이라는 사전 조건을 요구했다면, 스택·덱은 조건 없이 한 번의 순회로 답을 확정한다.
- 다만 둘의 뿌리는 같다. 단조 스택·단조 덱의 정당성은 "이 값은 앞으로 절대 답이 될 수 없다"는 **버려도 되는 근거**에서 나오는데, 이는 이진탐색이 절반을 버릴 때 쓴 논리와 정확히 같은 형태다.
- C++로 넘어가며 얻은 습관 둘은 계속 쓰인다 — **`mid = lo + (hi - lo) / 2`**, 그리고 **누적·합계는 `long long`**. 앞으로 만날 누적합, 구간 트리, 파라메트릭 문제에서 이 둘이 오답의 절반을 막아 준다.
