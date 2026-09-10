## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

**개념 지도**

재귀는 문법이 아니라 **구조**다. 아래 한 장에 이 챕터의 전부가 들어 있다 — 반드시 필요한 세 부분, 값을 돌려주느냐 마느냐, 그리고 한 번에 얼마나 줄이느냐.

```text
                    +---------------------+
                    |      recursion      |
                    +----------+----------+
             +-----------------+-----------------+
             |                                   |
       3 required parts                    2 return shapes
             |                                   |
   1. base case : stop here            void  : print / update
   2. shrink    : get closer           value : return + combine
   3. combine   : build the answer     both  : same 3 parts
             |                                   |
             +-----------------+-----------------+
                               |
              +----------------+----------------+
              |                |                |
        shrink by 1      shrink by half    two branches
        depth n          depth log n       depth n, 2^n calls
        n-1, n/10        b/2, (lo+hi)/2    f(n-1) + f(n-2)
        O(n)             O(log n)          O(2^n) without memo
```

세 부분 중 하나라도 빠지면 재귀는 성립하지 않는다. 그리고 "한 번에 얼마나 줄이는가"가 곧 복잡도와 재귀 깊이를 결정한다. 값을 돌려주는 재귀는 언제나 아래 두 방향 운동으로 읽는다.

```text
   unfold  f(4) -> f(3) -> f(2) -> f(1)          // shrink each step
                                     |
                                     v base case
   fold    24  <-   6  <-   2  <-   1            // combine on the way back
```

C++에서 재귀를 쓸 때 추가로 봐야 할 축이 하나 더 있다 — **프레임 하나의 크기**다. 깊이 × 프레임 크기가 스택 한도를 넘으면 아무 경고 없이 죽는다.

```text
   stack budget  ~ 1 MB  (typical)

   frame = few ints        --> depth 100000 is fine
   frame = int tmp[100000] --> 400 KB each : dies at depth 3
   pass vector<int> by value -> a full copy in EVERY frame
   pass const vector<int>&   -> one address, frame stays tiny
```

**뼈대 코드**

재귀 문제를 만나면 아래 골격 중 하나를 고른 뒤, 종료 조건·축소·결합 세 자리만 채운다.

```cpp
// 1) 값을 반환하지 않는 재귀 — 출력·상태 변경이 목적
void rec(int cur, int n) {
    if (cur > n) return;            // <- 문제마다 바뀜: 종료 조건
    cout << cur << "\n";            // <- 재귀 '앞'에 두면 정방향(작은 것부터)
    rec(cur + 1, n);                // <- 문제마다 바뀜: 축소 규칙
    // cout << cur << "\n";         // <- 여기로 옮기면 역방향(큰 것부터)
}
```

```cpp
// 2) 값을 반환하는 재귀(한 갈래) — 부분 답 하나를 받아 조합
long long rec(int n) {
    if (n <= 1) return 1;           // <- 가장 작은 경우의 정확한 답
    long long sub = rec(n - 1);     // <- 문제마다 바뀜: 축소
    return (long long)n * sub;      // <- 문제마다 바뀜: 결합 연산
}
```

```cpp
// 3) 두 갈래 재귀 — 부분 답 둘을 합친다
long long ways(int n) {
    if (n < 0) return 0;            // <- 범위를 벗어난 갈래는 0으로 막는다
    if (n == 0) return 1;           // <- 도착 한 가지
    return ways(n - 1) + ways(n - 3);   // <- 결합: 더하기·최댓값·논리합 등
}
```

```cpp
// 4) 절반 축소(분할 정복) — 깊이가 log n 이라 안전하다
int solve(const vector<int>& arr, int lo, int hi) {   // const& : 복사하지 않는다
    if (lo == hi) return arr[lo];                     // <- 원소 하나면 답이 명백
    int mid = (lo + hi) / 2;
    int left = solve(arr, lo, mid);                   // [lo, mid], [mid+1, hi]
    int right = solve(arr, mid + 1, hi);
    return left > right ? left : right;               // <- 결합 연산
}
```

```cpp
// 5) 문자열·자릿수 축소 — 한 조각을 떼고 나머지를 맡긴다
string rev(const string& s, int i) {    // 슬라이스 대신 인덱스를 줄인다
    if (i >= (int)s.size()) return "";  // <- 종료 조건
    return rev(s, i + 1) + s[i];        // <- 축소 + 결합
}

int digit_sum(long long n) {
    if (n < 10) return (int)n;          // <- 한 자리만 남으면 그것이 답
    return (int)(n % 10) + digit_sum(n / 10);
}
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 출력·전역 갱신만 하면 된다 | `void` 재귀 | 위로 올릴 값이 없다 | 시간 O(호출 수), 공간 O(깊이) |
| 작은 것부터 처리·출력 | 일 처리를 재귀 호출 **앞**에 | 펼치며 처리된다 | O(n) |
| 큰 것부터 처리·출력 | 일 처리를 재귀 호출 **뒤**에 | 접히며 처리된다 | O(n) |
| 부분 답을 모아 답을 만든다 | 반환 타입 있는 재귀 | 결합 연산으로 조립 | O(호출 수) |
| 한 걸음씩 줄어든다 | `n-1`, `n/10`, 인덱스 `i+1` | 자연스러운 축소 | O(n), 깊이 n |
| 절반씩 줄어든다 | `b/2`, `(lo+hi)/2` | 깊이가 log n으로 얕다 | O(log n) 또는 O(n) 방문 |
| 갈래가 둘이고 겹친다 | 재귀만으로는 위험 | 같은 부분 문제를 반복 계산 | O(2^n) — 이후 메모이제이션 |
| 축소 인자가 배열의 일부다 | 컨테이너가 아니라 `lo`, `hi` 인덱스 | 부분 벡터를 새로 만들면 매번 복사 | 인덱스 O(1) vs 복사 O(n) |
| 큰 컨테이너를 재귀에 넘긴다 | `const vector<T>&` | 프레임마다 복사하면 스택·시간 폭발 | 전달 O(1) |
| 결과가 21억을 넘을 수 있다 | `long long` 반환 | `int`는 조용히 음수로 뒤집힌다 | O(1) |
| 깊이가 수십만을 넘을 것 같다 | 반복문 또는 절반 축소 | 스택 한도에 걸린다 | — |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 재귀의 세 요소(종료 조건·문제 축소·결합)와, 각각을 빼면 무엇이 깨지는지.
- [ ] 설명할 수 있다: 종료 조건이 없으면 왜 멈추는 게 아니라 스택 오버플로로 프로그램이 죽는지.
- [ ] 설명할 수 있다: C++에는 파이썬의 `RecursionError` 같은 경고가 없어 증상이 왜 더 불친절한지.
- [ ] 설명할 수 있다: 종료 조건이 있어도 축소가 없으면 왜 여전히 무한 재귀인지.
- [ ] 설명할 수 있다: 호출이 쌓이는 펼침과 값이 되돌아오는 접힘을 그림으로.
- [ ] 설명할 수 있다: 일 처리를 재귀 호출 앞에 두느냐 뒤에 두느냐로 출력 순서가 뒤집히는 이유.
- [ ] 설명할 수 있다: 반환 타입이 있는 함수에서 `return`을 빠뜨리면 왜 미정의 동작인지.
- [ ] 설명할 수 있다: 종료 조건의 반환값이 틀리면 왜 최종 답 전체가 무너지는지.
- [ ] 설명할 수 있다: "부분 답을 이미 안다고 가정한다"는 사고가 수학적 귀납법과 같은 구조라는 것.
- [ ] 설명할 수 있다: `fact(4)`를 (깊이, 인자, 반환값) 표로 끝까지 손으로 추적하는 과정.
- [ ] 설명할 수 있다: 한 갈래 재귀가 O(n)이고 두 갈래 재귀가 왜 O(2^n)에 가까워지는지.
- [ ] 설명할 수 있다: 매번 절반으로 줄이면 왜 호출 횟수가 O(log n)이 되는지.
- [ ] 설명할 수 있다: 재귀가 반복문보다 O(깊이)만큼 추가 공간을 쓰는 이유.
- [ ] 설명할 수 있다: 재귀 프레임에 큰 지역 배열이나 값 전달 컨테이너를 두면 왜 스택이 터지는지.
- [ ] 설명할 수 있다: 재귀로 누적하는 값에 `long long`이 필요한 경우를 판단하는 기준.

**⚠️ 자주 하는 실수**

**1) 종료 조건을 아예 빠뜨린다**

```cpp
// ❌ 틀린 코드
void count_up(int cur, int n) {
    cout << cur << "\n";
    count_up(cur + 1, n);       // 멈출 조건이 없다
}
```

왜: 호출마다 스택 프레임이 쌓이는데 되돌아올 지점이 없다. 파이썬은 깊이 1000쯤에서 `RecursionError`로 알려 줬지만, C++은 스택이 넘치는 순간 아무 메시지 없이 강제 종료된다(대개 Segmentation fault). 원인 불명으로 죽으면 종료 조건부터 의심한다.

```cpp
// ✅ 고친 코드
void count_up(int cur, int n) {
    if (cur > n) return;        // 종료 조건 먼저
    cout << cur << "\n";
    count_up(cur + 1, n);
}
```

**2) 종료 조건은 있는데 인자가 줄지 않는다**

```cpp
// ❌ 틀린 코드
int s(int n) {
    if (n == 1) return 1;
    return n + s(n);            // 같은 n 을 다시 넘긴다 -> 종료 조건에 영영 못 닿음
}
```

왜: 종료 조건과 축소는 짝이다. 매 호출이 종료 조건 쪽으로 한 걸음이라도 다가가지 않으면, 조건이 있어도 그 자리를 지나칠 수 없다.

```cpp
// ✅ 고친 코드
int s(int n) {
    if (n == 1) return 1;
    return n + s(n - 1);        // 매 호출마다 1씩 작아진다
}
```

**3) 재귀 호출 앞에 `return`을 빠뜨린다**

```cpp
// ❌ 틀린 코드
long long fact(int n) {
    if (n <= 1) return 1;
    (long long)n * fact(n - 1);   // 계산만 하고 돌려주지 않는다
}
```

왜: 파이썬은 이럴 때 `None`을 돌려줘 다음 줄에서 바로 터졌지만, C++에서 반환 타입이 있는 함수가 값 없이 끝나는 것은 **미정의 동작**이다. 컴파일이 통과할 수도 있고, 쓰레기 값이 답인 척 흘러나온다. `g++ -Wall`의 `control reaches end of non-void function` 경고를 반드시 켜 둔다.

```cpp
// ✅ 고친 코드
long long fact(int n) {
    if (n <= 1) return 1;
    return (long long)n * fact(n - 1);
}
```

**4) 종료 조건의 반환값이 틀렸다**

```cpp
// ❌ 틀린 코드
long long fact(int n) {
    if (n <= 1) return 0;       // 0! = 1 인데 0 을 돌려준다
    return (long long)n * fact(n - 1);
}
// fact(4) -> 0
```

왜: 최종 답은 종료 조건의 값 위에 연산을 쌓아 만든 것이다. `4 * 3 * 2 * 0`은 무조건 0이 된다. 가장 작은 사례를 손으로 검산하는 이유가 이것이다.

```cpp
// ✅ 고친 코드
long long fact(int n) {
    if (n <= 1) return 1;       // 0! = 1! = 1
    return (long long)n * fact(n - 1);
}
```

**5) 재귀로 누적하면서 `int`를 쓴다**

```cpp
// ❌ 틀린 코드
int fact(int n) {               // 반환 타입이 int
    if (n <= 1) return 1;
    return n * fact(n - 1);     // int * int 는 32비트로 계산된다
}
// fact(13) -> 1932053504  (실제 값은 6227020800)
```

왜: `13!`은 약 62억이라 `int` 한계(약 21억)를 넘는데, C++은 오버플로를 알려 주지 않고 조용히 뒤집는다. 반환 타입을 `long long`으로 바꿔도 `n * fact(n-1)`에서 한쪽이 `int`면 곱셈 자체가 32비트로 끝난 뒤 대입되므로, **곱셈 전에** 캐스팅해야 한다.

```cpp
// ✅ 고친 코드
long long fact(int n) {
    if (n <= 1) return 1;
    return (long long)n * fact(n - 1);   // 곱하기 전에 64비트로 올린다
}
```

**6) 역방향 출력인데 일 처리를 재귀 앞에 둔다**

```cpp
// ❌ 틀린 코드
void stars(int cur, int n) {
    if (cur > n) return;
    cout << string(cur, '*') << "\n";   // 재귀보다 먼저 출력 -> 1개짜리가 맨 위
    stars(cur + 1, n);
}
```

왜: 재귀 앞의 코드는 펼치며(작은 인자부터) 실행되고, 뒤의 코드는 접히며(큰 인자부터) 실행된다. 출력 순서를 뒤집고 싶으면 코드의 위치를 바꾸면 된다.

```cpp
// ✅ 고친 코드
void stars(int cur, int n) {
    if (cur > n) return;
    stars(cur + 1, n);                  // 끝까지 내려간 뒤
    cout << string(cur, '*') << "\n";   // 돌아오면서 출력 -> n개짜리가 맨 위
}
```

**7) 큰 컨테이너를 값으로 받아 프레임마다 복사한다**

```cpp
// ❌ 틀린 코드
int find_max(vector<int> arr, int lo, int hi) {   // 값 전달 : 프레임마다 통째 복사
    if (lo == hi) return arr[lo];
    int mid = (lo + hi) / 2;
    int left = find_max(arr, lo, mid);
    int right = find_max(arr, mid + 1, hi);
    return left > right ? left : right;
}
```

왜: 파이썬에서 리스트를 넘기면 참조만 가서 공짜였지만, C++은 `&`가 없으면 원소 n개를 **호출할 때마다** 복사한다. 비교 자체는 O(n)인데 복사 때문에 시간이 O(n log n)으로 불어나고, 프레임마다 벡터를 하나씩 들고 있어 스택도 함께 위험해진다.

```cpp
// ✅ 고친 코드
int find_max(const vector<int>& arr, int lo, int hi) {  // 복사 0
    if (lo == hi) return arr[lo];
    int mid = (lo + hi) / 2;
    int left = find_max(arr, lo, mid);
    int right = find_max(arr, mid + 1, hi);
    return left > right ? left : right;
}
```

**8) 재귀 함수 안에 큰 지역 배열을 잡는다**

```cpp
// ❌ 틀린 코드
void dfs(int depth) {
    int buf[100000];            // 프레임 하나가 400KB
    if (depth == 0) return;
    buf[0] = depth;
    dfs(depth - 1);
}
```

왜: 스택은 보통 1MB 남짓이라 깊이 3만 되어도 넘친다. 재귀에서는 **프레임 하나의 크기 × 깊이**가 곧 스택 사용량이라, 지역 변수를 최소한으로 두는 것이 곧 안전이다.

```cpp
// ✅ 고친 코드
int buf_g[100000];              // 전역: 스택이 아니라 별도 영역에 잡힌다

void dfs(int depth) {
    if (depth == 0) return;
    buf_g[0] = depth;
    dfs(depth - 1);
}
```

**9) 절반 축소인데 같은 재귀를 두 번 부른다**

```cpp
// ❌ 틀린 코드
long long power(long long a, int b) {
    if (b == 0) return 1;
    if (b % 2 == 0) return power(a, b / 2) * power(a, b / 2);  // 두 번 계산
    return a * power(a, b - 1);
}
```

왜: 호출이 매 단계 두 갈래로 갈라지므로 절반으로 줄인 이득이 사라진다. 호출 트리의 노드 수가 다시 b에 비례해 O(b)가 된다.

```cpp
// ✅ 고친 코드
long long power(long long a, int b) {
    if (b == 0) return 1;
    if (b % 2 == 0) {
        long long half = power(a, b / 2);   // 한 번만 계산해 변수에 담는다
        return half * half;
    }
    return a * power(a, b - 1);
}
```

**다음 챕터로**

- Ch3의 정렬은 "절반으로 나눠 각각 풀고 합친다"는 이 챕터의 분할 정복 골격 위에 서 있다. `std::sort`가 O(N log N)인 이유도 "절반씩 log N번 나눈다"는 같은 셈에서 나오며, 재귀가 너무 깊어지면 힙소트로 갈아타는 안전장치까지 들어 있다.
- 값을 반환하는 재귀에서 "부분 답을 어떤 연산으로 합칠지" 정하던 감각은, 정렬에서 "두 원소 중 무엇을 앞에 둘지(비교 함수)"를 정하는 감각으로 이어진다.
