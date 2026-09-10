## L6. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

**개념 지도**

Ch1은 "함수 하나를 어떻게 만드는가"에서 출발해, "값이 어떻게 오가는가"와 "이름이 어디까지 살아 있는가"로 갈라진다. 이 세 갈래가 한 장에 들어가면 챕터가 끝난 것이다.

```text
                        +-------------+
                        |  function   |
                        +------+------+
                 +-------------+-------------+
                 |                           |
          void : no value              returns a value
          (side effect only)           (a reusable part)
                 |                           |
          cout / draw / log            return x | return {a, b}
                 |                           |
                 +-------------+-------------+
                               |
                    +----------+----------+
                    |                     |
            argument passing         name scope
                    |                     |
        T  x     -> copy, safe       local  : dies at return
        T& x     -> alias, edits     global : seen everywhere
        const T& -> no copy, no edit shadow : inner decl hides it
```

왼쪽 갈래(L1·L2)는 "무엇을 돌려줄까", 오른쪽 아래 갈래(L3·L4)는 "무엇이 바깥에 남을까"의 문제다. C++에서는 그 답이 **매개변수 선언 한 글자**로 정해진다.

```text
   want the function to change the caller's data?
        |
        +-- parameter is  T x        --> impossible : x is a COPY
        |                                return a new value instead
        +-- parameter is  T& x       --> edits in place, no return
        |
        +-- only reading a big T     --> const T& : no copy, no risk
```

파이썬은 "무엇을 넘겼는가"(불변/가변)가 결과를 갈랐지만, C++은 "어떻게 받겠다고 적었는가"가 갈린다. 호출부만 봐서는 알 수 없고, 함수 선언을 봐야 안다.

**뼈대 코드**

문제를 만나면 아래 골격 중 하나를 골라 빈칸만 채운다.

```cpp
// 1) 함수 분해 골격 — 판정/계산 부품을 위에, 조립은 아래에
#include <bits/stdc++.h>
using namespace std;

bool check(int x) {                 // <- 문제마다 바뀜: 판정 규칙
    if (x < 0) return false;        // 안 되는 경우를 조기 반환으로 먼저 걸러냄
    return true;
}

int transform(int x) {              // <- 문제마다 바뀜: 값 변환 규칙
    return x * 2;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    long long answer = 0;           // 누적은 long long 이 기본
    for (int i = 0; i < n; i++) {
        int v;
        cin >> v;
        if (check(v)) answer += transform(v);   // <- 무엇을 세고 무엇을 모을지
    }
    cout << answer << "\n";
    return 0;
}
```

```cpp
// 2) 반환 없는 출력 함수 — 함수가 함수를 부른다
void show_row(const vector<int>& row) {   // <- 한 줄의 출력 형식. const& 로 복사 방지
    for (int i = 0; i < (int)row.size(); i++) {
        if (i) cout << ' ';
        cout << row[i];
    }
    cout << "\n";
}

void show_all(const vector<vector<int>>& grid) {
    for (const auto& row : grid) show_row(row);   // 반환값을 쓰지 않는다
}
```

```cpp
// 3) 여러 값 한 번에 돌려주기
pair<int,int> min_max(const vector<int>& arr) {
    int lo = *min_element(arr.begin(), arr.end());
    int hi = *max_element(arr.begin(), arr.end());
    return {lo, hi};                // <- 돌려줄 값들. pair 하나로 묶여 올라간다
}

// 받는 쪽 (C++17 구조적 바인딩)
// auto [lo, hi] = min_max(v);
```

```cpp
// 4) 원본 보존 vs 원본 갱신 — 둘을 절대 섞지 않는다
vector<int> apply_copy(vector<int> arr) {   // 보존형: 값으로 받아 복사본을 고쳐 반환
    arr[0] += 1;                            // <- 연산. 호출자의 원본은 그대로
    return arr;
}

void apply_inplace(vector<int>& arr) {      // 갱신형: 참조로 받아 제자리 수정
    arr[0] += 1;                            // <- 연산. 반환 없이 호출자가 바뀐다
}
```

```cpp
// 5) 여러 함수가 상태를 공유할 때 — 전역은 0 으로 자동 초기화된다
int cnt = 0;
vector<bool> visited;

void mark(int v) {
    if (!visited[v]) {              // C++ 은 global 선언 없이 전역을 바로 갱신한다
        visited[v] = true;
        cnt += 1;
    }
}

void reset(int m) {
    cnt = 0;                        // <- 질의마다 초기화하는 것을 잊기 쉽다
    visited.assign(m + 1, false);
}
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 결과를 출력하고 끝난다 | `void` 함수 | 위로 올릴 값이 없다 | 호출 O(1) + 내부 작업 |
| 그 값을 나중에 또 쓴다 | 반환 타입 있는 함수 | 부품으로 조립할 수 있다 | 호출 O(1) + 내부 작업 |
| 안 되는 경우를 먼저 쳐낸다 | 조기 반환 | 중첩 `if`가 사라진다 | 평균 실행량이 줄어듦 |
| 값 두 개를 돌려준다 | `pair` 반환 + 구조적 바인딩 | 한 덩어리로 올라간다 | O(1) |
| 값 세 개 이상을 돌려준다 | `struct` 정의 후 반환 | 필드에 이름이 붙어 안 헷갈린다 | O(1) |
| 큰 배열을 함수가 갱신한다 | `vector<T>&` 참조 매개변수 | 복사가 없고 바깥에 반영된다 | 전달 O(1) |
| 큰 배열을 읽기만 한다 | `const vector<T>&` | 복사 0, 실수로 수정 불가 | 전달 O(1) |
| 호출자의 원본을 지켜야 한다 | 값으로 받기(`vector<T>`) | 복사본만 고친다 | 복사 O(n) |
| 2차원 격자를 복사한다 | `auto b = a;` (깊은 복사) | 안쪽 행까지 새로 만들어진다 | O(R·C) |
| 여러 함수가 카운터를 공유 | 전역 변수 | C++은 선언 없이 바로 갱신 | O(1) |
| 함수마다 값이 독립이어야 한다 | 지역 변수(인자로 받고 반환) | 간섭이 원천 차단된다 | O(1) |
| 큰 배열이 필요하다 | 전역 배열 또는 `vector` | 지역 배열은 스택을 넘긴다 | 선언 O(1)~O(n) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 함수를 부를 때 스택 프레임이 쌓였다가 반환과 함께 사라지는 과정.
- [ ] 설명할 수 있다: `void`가 "올려 보낼 값이 없다"는 선언이라는 것과, `return;`·`return` 생략이 같은 뜻인 이유.
- [ ] 설명할 수 있다: 반환 타입이 있는데 `return`을 빠뜨리면 왜 오류가 아니라 미정의 동작인지.
- [ ] 설명할 수 있다: 조기 반환이 코드를 왜 짧고 안전하게 만드는지, 그리고 왜 정답을 바꾸지 않는지.
- [ ] 설명할 수 있다: `pair` 반환과 구조적 바인딩 `auto [a, b] = f();`가 하는 일.
- [ ] 설명할 수 있다: C++의 매개변수 전달이 기본적으로 **복사**라는 것과, 그래서 `vector`도 통째로 복사된다는 것.
- [ ] 설명할 수 있다: `void f(vector<int> v)`와 `void f(vector<int>& v)`가 호출자에게 어떻게 다르게 보이는지.
- [ ] 설명할 수 있다: 읽기 전용인데도 `const T&`로 받는 두 가지 이유(복사 비용, 수정 방지).
- [ ] 설명할 수 있다: 값 전달의 비용이 O(n)이고 격자는 O(R·C)라는 것, 그것을 반복문 안에 두면 왜 위험한지.
- [ ] 설명할 수 있다: 이름 찾기가 안쪽 블록에서 바깥으로 올라가며 첫 선언에서 멈춘다는 규칙.
- [ ] 설명할 수 있다: 전역과 같은 이름의 지역을 선언하면 왜 전역이 안 바뀌는지(shadowing).
- [ ] 설명할 수 있다: 전역은 0으로 자동 초기화되는데 지역은 왜 초기화되지 않는지.
- [ ] 설명할 수 있다: 함수 안에 큰 배열을 선언하면 왜 스택이 넘치는지, 대안이 무엇인지.
- [ ] 설명할 수 있다: 함수로 잘게 나눈다고 시간 복잡도가 나빠지지 않는 이유.

**⚠️ 자주 하는 실수**

**1) 반환 타입이 있는데 `return`을 빠뜨린다**

```cpp
// ❌ 틀린 코드
int total(const vector<int>& arr) {
    int s = 0;
    for (int x : arr) s += x;
    // return 이 없다 — 컴파일은 통과할 수도 있다
}

// int t = total(v);   // t 에 쓰레기 값이 들어온다
```

왜: `void`가 아닌 함수가 값을 돌려주지 않고 끝나는 것은 C++에서 **미정의 동작**이다. 파이썬처럼 `None`이 들어오는 것도 아니고 실행이 멈추지도 않는다. 레지스터에 남아 있던 값이 답인 척 흘러나와, 어떤 입력에서는 맞고 어떤 입력에서는 틀린다. `g++ -Wall`을 켜면 `control reaches end of non-void function` 경고로 잡힌다.

```cpp
// ✅ 고친 코드
int total(const vector<int>& arr) {
    int s = 0;
    for (int x : arr) s += x;
    return s;                   // 모든 갈래가 값을 반환해야 한다
}
```

**2) 바깥을 바꿔야 하는데 `&`를 빠뜨린다 (파이썬 습관의 함정)**

```cpp
// ❌ 틀린 코드
void push(vector<int> v, int x) {   // 값 전달 : v 는 복사본이다
    v.push_back(x);
}

// vector<int> arr = {1, 2};
// push(arr, 3);                    // arr 는 여전히 {1, 2}
```

왜: 파이썬에서는 리스트를 넘기면 저절로 공유돼 `append`가 바깥에 반영됐다. C++은 정반대로, `&`가 없으면 원소를 전부 복사한 새 벡터를 만들어 그것만 고친다. O(n)을 내고도 바깥은 하나도 안 바뀌는 최악의 조합이다.

```cpp
// ✅ 고친 코드
void push(vector<int>& v, int x) {  // 참조 전달 : v 는 arr 의 다른 이름
    v.push_back(x);
}
```

**3) 읽기만 하는 큰 컨테이너를 값으로 받는다**

```cpp
// ❌ 틀린 코드
long long sum_all(vector<int> v) {  // 호출할 때마다 원소 n 개를 통째로 복사
    long long s = 0;
    for (int x : v) s += x;
    return s;
}

// for (int q = 0; q < Q; q++) ans += sum_all(big);   // 복사가 Q 번
```

왜: 답은 맞는데 시간만 초과되는 전형적인 원인이다. 값 전달은 길이 n에 O(n), 격자면 O(R·C)이고, 반복문 안에 두면 O(반복 횟수 × n)으로 조용히 커진다. 파이썬에서는 없던 비용이라 눈에 잘 안 띈다.

```cpp
// ✅ 고친 코드
long long sum_all(const vector<int>& v) {   // 복사 0, 수정도 불가
    long long s = 0;
    for (int x : v) s += x;
    return s;
}
```

**4) 지역 변수를 초기화하지 않는다**

```cpp
// ❌ 틀린 코드
int count_positive(const vector<int>& v) {
    int c;                      // 초기화되지 않았다 — 쓰레기 값
    for (int x : v) if (x > 0) c++;
    return c;
}
```

왜: 전역 변수는 프로그램 시작 시 0으로 자동 초기화되지만, 함수 안의 지역 변수는 그렇지 않다. 그 자리에 남아 있던 값에서 세기 시작하므로 실행할 때마다 답이 달라진다. 파이썬에는 아예 없던 종류의 버그다.

```cpp
// ✅ 고친 코드
int count_positive(const vector<int>& v) {
    int c = 0;                  // 세는 변수는 반드시 0 으로 시작
    for (int x : v) if (x > 0) c++;
    return c;
}
```

**5) 전역과 같은 이름의 지역을 선언해 전역을 가린다 (shadowing)**

```cpp
// ❌ 틀린 코드
int total = 0;                  // 전역

void add(int x) {
    int total = 0;              // 같은 이름의 지역이 전역을 가린다
    total += x;                 // 지역만 바뀌고 함수가 끝나면 사라진다
}
```

왜: C++ 이름 찾기는 가장 안쪽 블록부터 올라가며 **첫 선언에서 멈춘다.** 함수 안에 `int total`이 있으면 그 함수의 모든 `total`은 지역을 뜻한다. 파이썬처럼 `global` 키워드를 빠뜨린 게 아니라, **선언을 하나 더 쓴 것**이 원인이다.

```cpp
// ✅ 고친 코드
int total = 0;

void add(int x) {
    total += x;                 // 선언하지 않으면 전역이 그대로 쓰인다
}
```

**6) 지역 변수의 참조를 돌려준다**

```cpp
// ❌ 틀린 코드
vector<int>& make_row(int m) {
    vector<int> row(m, 0);      // 이 함수의 프레임에서 태어난 지역 변수
    return row;                 // 함수가 끝나면 사라지는 것을 가리키게 된다
}
```

왜: `row`는 `return` 직후 소멸한다. 그 자리를 가리키는 참조를 받아 쓰면 이미 없어진 메모리를 읽는 것이라, 처음 몇 번은 멀쩡히 동작하다가 나중에 엉뚱하게 터진다. 참조로 돌려도 되는 것은 **호출자보다 오래 사는 것**(전역, 인자로 받은 참조)뿐이다.

```cpp
// ✅ 고친 코드
vector<int> make_row(int m) {   // 값으로 돌려준다 (컴파일러가 복사를 없애 준다)
    vector<int> row(m, 0);
    return row;
}
```

**7) 함수 안에 큰 배열을 선언해 스택을 터뜨린다**

```cpp
// ❌ 틀린 코드
void solve() {
    int grid[2000][2000];       // 약 16MB — 스택은 보통 1MB 남짓이다
    grid[0][0] = 1;
}
```

왜: 지역 변수는 스택에 잡힌다. 스택 한도를 넘는 순간 아무 메시지 없이 프로그램이 강제 종료되는데, 파이썬에는 이런 실패 방식 자체가 없어 원인을 짐작하기 어렵다.

```cpp
// ✅ 고친 코드
int grid_g[2000][2000];         // 전역: 별도 영역에 잡히고 0 으로 초기화된다

void solve() {
    vector<vector<int>> grid(2000, vector<int>(2000, 0));  // 또는 힙에 잡기
    grid[0][0] = 1;
}
```

**8) 여러 질의를 처리하며 전역을 초기화하지 않는다**

```cpp
// ❌ 틀린 코드
int cnt = 0;

int run(const vector<int>& vals) {
    for (int v : vals) cnt += 1;
    return cnt;
}

// run({1, 2});        // 2
// run({1, 2, 3});     // 5  <- 앞 질의의 2 가 그대로 남아 있다
```

왜: 전역은 프로그램이 끝날 때까지 살아 있다. 함수가 끝나도 값이 사라지지 않으므로, 질의마다 새로 세려면 명시적으로 되돌려야 한다.

```cpp
// ✅ 고친 코드
int cnt = 0;

int run(const vector<int>& vals) {
    cnt = 0;                    // 질의 시작마다 초기화
    for (int v : vals) cnt += 1;
    return cnt;
}
```

**다음 챕터로**

- Ch2에서는 함수가 **자기 자신**을 부른다. 그러면 L1에서 본 스택 프레임이 한 겹이 아니라 깊이만큼 여러 겹으로 쌓이고, "언제 멈추는가"가 곧 생사를 가르는 문제가 된다. C++에는 파이썬의 `RecursionError` 같은 안전장치가 없어 그냥 죽는다는 점도 함께 기억한다.
- L2의 "값을 돌려주는 부품" 감각은 재귀의 반환값 조합으로, L3의 "큰 것은 참조로" 감각은 재귀 프레임을 가볍게 유지하는 습관으로 그대로 이어진다.
