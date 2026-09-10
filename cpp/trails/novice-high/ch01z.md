## L8. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 레슨은 Ch1(시간·공간복잡도) 전체를 하나의 판단 절차로 접는다. 이 챕터의 도구는 결국 **하나의 질문에 답하기 위한 것**이다 — "내가 지금 떠올린 방법이 주어진 입력 크기에서 제한 시간 안에 끝나는가?"

- 그 질문에 답하는 순서는 항상 같다. **수도코드로 설계하고 → 줄별 실행 횟수를 세어 `T(n)`을 만들고 → 지배항만 남겨 Big-O로 줄이고 → 입력 크기와 대조한다.** 아래 지도가 그 흐름 전체다.

- C++에서는 여기에 **한 가지 검산이 더 붙는다** — "복잡도가 맞아도 자료형이 넘치지 않는가". 등급이 옳은데 `int` 오버플로로 틀리는 답이 파이썬에는 없던 새로운 실패 유형이다.

**개념 지도**

```text
 how to price an algorithm
 -------------------------------------------------------------
   problem  ->  pseudocode  ->  count  ->  T(n)  ->  O( . )
                    L1           L3        L3        L2
                                  |
                +-----------------+-----------------+
                |                                   |
             LOOPS   (L4)                     RECURSION  (L5)
                |                                   |
      nesting   -> multiply             T(n) = a T(n/b) + f(n)
      sequence  -> add                  unroll , or sum levels
      i += 1    -> n steps              -1 shrink -> depth n
      i *= 2    -> log n steps          /2 shrink -> depth log n
                |                                   |
                +-----------------+-----------------+
                                  |
                        drop constants and
                        keep the top term
                                  |
                +--------+--------+--------+
             TIME              SPACE (L6)      TYPE   ( c++ only )
      compare with limit    extra containers   int overflow ?
      ops per sec ~ 1e8     + max stack depth  narrowing ?
 -------------------------------------------------------------
 one call tree , two prices : nodes = time , height = space
```

- 지도의 마지막 줄이 이 챕터에서 가장 자주 놓치는 지점이다. **같은 재귀 트리를 놓고 시간은 "노드 수"로, 공간은 "높이"로 읽는다.** 나이브 피보나치가 시간 `O(2ⁿ)`인데 공간은 `O(n)`인 이유가 여기 있다.

- 세 번째 갈래(TYPE)는 C++에서만 붙는 칸이다. `int`는 약 21억, `long long`은 약 9.2×10¹⁸까지다. 입력 제한을 읽는 순간 "이 값들의 **합·곱**이 어디까지 가는가"를 함께 계산해 자료형을 정한다.

- 등급 판정이 막히면 **배율 테스트**로 돌아온다. `n`을 2배로 했을 때 비용이 `×1`이면 `O(1)`, `+1`이면 `O(log n)`, `×2`면 `O(n)`, `×2.2`면 `O(n log n)`, `×4`면 `O(n²)`, 제곱이 되면 `O(2ⁿ)`이다.

```text
 max n for a 1-second budget  ( c++ : about 1e8 .. 1e9 simple ops )
 -------------------------------------------------------------
 n                1e8   1e6   1e5   1e4  2000   100    20    10
 O(1)              ok    ok    ok    ok    ok    ok    ok    ok
 O(log n)          ok    ok    ok    ok    ok    ok    ok    ok
 O(n)              ok    ok    ok    ok    ok    ok    ok    ok
 O(n log n)        --    ok    ok    ok    ok    ok    ok    ok
 O(n^2)            --    --    --    ok    ok    ok    ok    ok
 O(n^3)            --    --    --    --    --    ok    ok    ok
 O(2^n)            --    --    --    --    --    --    ok    ok
 O(n!)             --    --    --    --    --    --    --    ok
 -------------------------------------------------------------
 read it backwards : the given n tells you which line to aim at
```

- 이 표를 **거꾸로 읽는 것**이 실전 사용법이다. 지문에서 `n ≤ 10⁵`를 보면 `O(n²)` 줄이 이미 막혀 있으므로, 설계를 시작하기도 전에 "`O(n log n)` 이하로 짜야 한다"는 목표가 정해진다.

**뼈대 코드**

```cpp
// 뼈대 1(before) - vector 멤버십 : 한 줄처럼 보이지만 O(n)
vector<int> seen;
for (int x : a)                                    // n번
    if (find(seen.begin(), seen.end(), x) == seen.end())  // 선형 스캔 O(n)
        seen.push_back(x);                         // -> 전체 O(n^2)
```

```cpp
// 뼈대 1(after) - 해시 집합으로 바꾸면 검사 한 번이 평균 O(1)
unordered_set<int> seen;
vector<int> out;
for (int x : a) {                                  // n번
    if (seen.insert(x).second)                     // 새로 들어갔으면 true
        out.push_back(x);                          // 순서 보존이 필요할 때만
}                                                  // -> 전체 O(n)
```

```cpp
// 뼈대 2(before) - 출력마다 endl : 매번 버퍼를 강제로 비운다
for (int i = 0; i < n; i++)
    cout << a[i] << endl;      // flush 가 n번 -> 디스크/파이프 왕복 n번
```

```cpp
// 뼈대 2(after) - '\n' 과 동기화 해제 : 같은 O(n) 인데 실측이 몇 배 빠르다
ios_base::sync_with_stdio(false);
cin.tie(nullptr);              // cin 앞에서 cout 을 flush 하지 않게
for (int i = 0; i < n; i++)
    cout << a[i] << '\n';      // 버퍼에 쌓았다가 한 번에 나간다
```

```cpp
// 뼈대 3(before) - 구간 합을 질의마다 다시 계산
for (auto [lo, hi] : queries) {          // q개의 질의
    long long s = 0;
    for (int i = lo; i <= hi; i++) s += a[i];   // 구간 길이만큼 O(n)
    cout << s << '\n';                          // -> 전체 O(q*n)
}
```

```cpp
// 뼈대 3(after) - 누적합을 한 번 만들어 두고 뺄셈으로 답한다
vector<long long> pre(n + 1, 0);                 // long long ! int 는 넘친다
for (int i = 0; i < n; i++)                      // 전처리 O(n)
    pre[i + 1] = pre[i] + a[i];                  // pre[k] = a[0]+...+a[k-1]
for (auto [lo, hi] : queries)
    cout << pre[hi + 1] - pre[lo] << '\n';       // 질의당 O(1) -> O(n + q)
```

```cpp
// 뼈대 4(before) - vector 앞에서 빼기 : 뒤 원소를 전부 한 칸씩 당긴다
vector<int> q = {start};
while (!q.empty()) {
    int cur = q.front();
    q.erase(q.begin());        // O(n)  ->  전체 O(n^2)
    q.push_back(nxt);          // 문제마다 바뀜
}
```

```cpp
// 뼈대 4(after) - 양끝 큐를 쓰면 앞에서 빼기도 O(1)
deque<int> q = {start};        // queue<int> 도 같다
while (!q.empty()) {
    int cur = q.front();
    q.pop_front();             // O(1)  ->  전체 O(n)
    q.push_back(nxt);
}
```

```cpp
// 뼈대 5(before) - 컨테이너를 값으로 받기 : 호출마다 통째로 복사
long long solve(vector<int> a, int lo, int hi) {   // 복사 O(n)
    if (lo >= hi) return 0;
    int mid = lo + (hi - lo) / 2;
    return solve(a, lo, mid) + solve(a, mid + 1, hi);   // 레벨마다 O(n) 추가
}                                                  // T(n)=2T(n/2)+O(n)
```

```cpp
// 뼈대 5(after) - 참조 + 인덱스 : 복사가 사라진다
long long solve(const vector<int>& a, int lo, int hi) {  // 복사 0
    if (lo >= hi) return 0;
    int mid = lo + (hi - lo) / 2;
    return solve(a, lo, mid) + solve(a, mid + 1, hi);    // T(n)=2T(n/2)+O(1)
}
```

```cpp
// 뼈대 6(before) - 깊이가 n 에 비례하는 재귀 : 스택 오버플로 위험
long long rec_sum(const vector<int>& a, int i) {
    if (i == (int)a.size()) return 0;
    return a[i] + rec_sum(a, i + 1);      // 깊이 n -> n=1e6 이면 즉사
}
```

```cpp
// 뼈대 6(after) - 꼬리가 단순한 재귀는 반복문으로 : 공간 O(1)
long long iter_sum(const vector<int>& a) {
    long long s = 0;                      // int 로 두면 합이 넘친다
    for (int x : a) s += x;               // 시간은 그대로 O(n)
    return s;                             // 깊이 항상 1, 스택과 무관
}
```

**언제 무엇을 쓰나**

**(1) 입력 크기 `n`이 알려주는 목표 복잡도** — 지문의 제한을 보고 설계 방향을 먼저 정한다.

| 입력 크기 `n` | 노려야 할 복잡도 | 대표 알고리즘·기법 | 대략 연산 수 |
|---|---|---|---|
| `n ≤ 10` | `O(n!)`, `O(2ⁿ·n)` | 순열 전부 나열(`next_permutation`), 완전탐색 | ~10⁷ |
| `n ≤ 20` | `O(2ⁿ)` | 부분집합 전부, 비트마스크 DP | ~10⁶ |
| `n ≤ 100` | `O(n³)` | 3중 반복, 플로이드-워셜 | ~10⁶ |
| `n ≤ 2 000` | `O(n²)` | 2중 반복, 2차원 DP, 모든 쌍 비교 | ~4·10⁶ |
| `n ≤ 10⁵` | `O(n log n)` | `sort`, 이분 탐색, `priority_queue`, 분할정복 | ~1.7·10⁶ |
| `n ≤ 10⁶` | `O(n)` / `O(n log n)` | 한 번 훑기, 누적합, 투 포인터, 해시 | ~10⁷ |
| `n ≤ 10⁸` | `O(n)` | 단순 순회만(입출력 자체가 병목) | ~10⁸ |
| `n`이 10⁹ 이상 | `O(log n)` / `O(1)` | 이분 탐색, 수식·닫힌 식, 거듭제곱 분할 | ~30 |

- 기준선은 **1초에 대략 10⁸번의 단순 연산**이다. C++는 컴파일 언어라 같은 알고리즘에서 파이썬보다 대략 **10~100배 빠르므로**, 단순 산술 루프라면 10⁸~10⁹까지도 1초에 들어간다. 그래서 위 표에서 **한 칸 더 공격적으로** 잡아도 통과하는 경우가 있다(예: `n = 10⁴`의 `O(n²)`는 10⁸이라 C++에서는 대개 통과, 파이썬에서는 대개 실패).
- 하지만 **한 등급 차이는 언어로 메워지지 않는다.** `n = 10⁵`에서 `O(n²)`은 10¹⁰ 연산이므로, 100배 빨라져도 10⁸에 해당하는 시간이 남는다. 언어 속도는 Big-O 정의의 상수 `c`를 줄일 뿐 `g(n)`을 바꾸지 못한다.
- 반대 방향으로도 쓴다. `n ≤ 20`처럼 유난히 작으면 그것은 **"지수 시간을 써도 된다"는 신호**다. 억지로 다항식 해법을 찾느라 시간을 버릴 필요가 없다.
- 표에 나오지 않는 C++ 고유 병목이 하나 있다 — **입출력**. `n = 10⁶`을 `cin`/`cout`으로 그냥 읽고 쓰면 알고리즘보다 입출력이 오래 걸린다. `ios_base::sync_with_stdio(false); cin.tie(nullptr);`은 선택이 아니라 기본값으로 둔다.

**(2) 복잡도를 한 칸 낮추는 정석 치환** — 코드에서 바로 갈아 끼우는 판단표다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 반복 안에서 `find(v.begin(), v.end(), x)` | `unordered_set` / `set` | 벡터는 선형 스캔, 해시는 즉시 조회 | `O(n²)` → `O(n)` |
| 같은 구간 합을 여러 번 | 누적합 배열 전처리 | 뺄셈 한 번으로 임의 구간 합을 얻음 | `O(qn)` → `O(n+q)` |
| 앞에서 빼는 큐(`v.erase(v.begin())`) | `deque` / `queue` | 벡터는 앞을 빼면 뒤를 전부 당김 | `O(n²)` → `O(n)` |
| 중간 삽입 `v.insert(v.begin()+i, x)` 반복 | `list` 또는 설계 변경 | 벡터의 중간 삽입은 매번 O(n) | `O(n²)` → `O(n)` |
| 컨테이너를 값으로 넘기는 함수 | `const vector<T>&` | 값 전달은 호출마다 O(n) 복사 | 호출당 `O(n)` → `O(1)` |
| 재귀에 부분 벡터를 새로 만들어 넘김 | 인덱스 `lo, hi`를 넘김 | 복사가 시간·공간 양쪽을 먹음 | 공간 `O(n log n)` → `O(log n)` |
| 같은 부분문제를 반복 계산 | 메모이제이션·DP | 비용 = 상태 수 × 전이 비용 | `O(2ⁿ)` → `O(n)` |
| 정렬된 배열에서 값 찾기 | `lower_bound` / `binary_search` | 매번 후보가 절반으로 줄어듦 | `O(n)` → `O(log n)` |
| 개수 세기를 `count(b, e, x)`로 | `map<int,int>` / `unordered_map` 누적 | `count`는 호출마다 전체를 훑음 | `O(n²)` → `O(n)` |
| 깊이가 `n`인 재귀 | 반복문 또는 명시적 `stack` | 스택 오버플로(1MB~8MB)를 피함 | 공간 `O(n)` → `O(1)` |
| 출력이 많은데 `endl` | `'\n'` + 동기화 해제 | `endl`은 매번 버퍼를 flush | 상수를 수 배 개선 |
| 메모리 제한이 병목 | 롤링 배열·제자리 갱신 | 이전 한두 줄만 있으면 되는 DP가 많음 | 공간 `O(n²)` → `O(n)` |
| 합·곱이 21억을 넘을 수 있음 | `long long` / `1LL *` | `int` 오버플로는 조용히 틀린 답을 냄 | 정확성 문제 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: Big-O의 정의를 `c`와 `n₀`를 써서, 그리고 왜 그 정의가 상수·저차항을 버리게 만드는지를.
- [ ] 설명할 수 있다: 실행 시간(초)이 아니라 연산 횟수를 세는 이유와, 그 모델이 표준 라이브러리 한 줄짜리 호출에서 깨지는 자리들을.
- [ ] 설명할 수 있다: `O`·`Ω`·`Θ`의 차이와, `O(n)`인 코드를 `O(n²)`이라 말해도 거짓은 아니지만 쓸모없는 이유를.
- [ ] 설명할 수 있다: `n`을 2배로 했을 때의 배율만 보고 복잡도 등급을 역산하는 법을.
- [ ] 설명할 수 있다: `1+2+…+n = n(n+1)/2`를 가우스 짝짓기로 유도하고, 왜 그것이 `O(n²)`인지를.
- [ ] 설명할 수 있다: 절반씩 줄이면 `log₂n`번인 이유를 `2^k = n`에서 시작해서.
- [ ] 설명할 수 있다: 중첩 반복이 곱, 순차 반복이 합이 되는 이유를.
- [ ] 설명할 수 있다: 이중 반복인데도 `O(n²)`이 아닌 경우(안쪽이 `log n`번, 또는 조화급수)를 예와 함께.
- [ ] 설명할 수 있다: 점화식을 세우는 세 요소(분기 수·크기 감소·호출 밖 비용)와 반복 대입법으로 푸는 절차를.
- [ ] 설명할 수 있다: 네 가지 대표 점화식의 결과를 유도까지 곁들여서.
- [ ] 설명할 수 있다: 레벨 합이 평평할 때·위로 기울 때·아래로 기울 때 결과가 어떻게 달라지는지를.
- [ ] 설명할 수 있다: 나이브 피보나치가 시간 `O(2ⁿ)`인데 공간은 `O(n)`인 이유를(노드 수 대 높이).
- [ ] 설명할 수 있다: 재귀 호출에서 형제 프레임이 공간에 더해지지 않는 이유를.
- [ ] 설명할 수 있다: 메모이제이션의 비용이 "상태 수 × 전이 비용"인 이유를.
- [ ] 설명할 수 있다: `int`와 `long long`의 한계를 숫자로 말하고, 입력 제한만 보고 필요한 자료형을 고를 수 있다.
- [ ] 설명할 수 있다: 컨테이너를 값으로 넘길 때와 `const` 참조로 넘길 때의 비용 차이를.
- [ ] 설명할 수 있다: C++ 재귀가 깊어질 때 무슨 일이 일어나는지와, 대략 몇 단계에서 위험해지는지를.
- [ ] 설명할 수 있다: 주어진 `n`만 보고 노려야 할 복잡도 등급을 즉시 말할 수 있다.

**⚠️ 자주 하는 실수**

**1) `int`로 합·곱을 담아 조용히 넘친다**

```cpp
// ❌ 틀린 코드
int n;                      // n <= 100000 , a[i] <= 100000
cin >> n;
vector<int> a(n);
int total = 0;
for (int i = 0; i < n; i++) { cin >> a[i]; total += a[i]; }
cout << total << '\n';      // 최대 1e10 -> int(약 21억) 를 넘어 음수가 나온다
```

왜: `int`의 범위는 약 −21억 ~ +21억이다. 넘는 순간 예외도 경고도 없이 **값이 뒤로 돌아간다**(부호 있는 정수의 오버플로는 미정의 동작이다). 복잡도는 `O(n)`으로 맞는데 답만 틀리므로 원인을 찾기 어렵다. `n * (n + 1) / 2`, `mid * mid`, 좌표의 곱 같은 식이 전형적인 발화점이다.

```cpp
// ✅ 고친 코드
long long total = 0;              // 약 9.2e18 까지
for (int i = 0; i < n; i++) { cin >> a[i]; total += a[i]; }
cout << total << '\n';
// 곱셈은 계산 '전에' 승격해야 한다
long long area = 1LL * w * h;     // (long long)(w * h) 는 이미 늦다
```

**2) `vector`에서의 선형 탐색을 `O(1)`로 착각한다**

```cpp
// ❌ 틀린 코드
vector<int> seen;
for (int x : a)                                          // n번
    if (find(seen.begin(), seen.end(), x) == seen.end())  // O(n)
        seen.push_back(x);
// "한 번 훑었으니 O(n)" 이라고 분석한다
```

왜: `find`는 앞에서부터 하나씩 비교하는 **선형 탐색**이다. 원소가 모두 유일하면 비교가 `0+1+2+…+(n-1) = n(n-1)/2`번 일어나 실제로는 **`O(n²)`**이다. `n = 10⁵`이면 50억 번이라 시간 초과다. `count(b, e, x)`도 같다.

```cpp
// ✅ 고친 코드
unordered_set<int> seen;          // 평균 O(1) 조회 (최악 O(n) 이라 set 도 후보)
vector<int> out;
for (int x : a)
    if (seen.insert(x).second)    // 삽입 성공 = 처음 보는 값
        out.push_back(x);
// 전체 O(n)
```

**3) `vector`의 앞에서 원소를 빼거나 넣는다**

```cpp
// ❌ 틀린 코드
vector<int> q = {0};
while (!q.empty()) {
    int cur = q.front();
    q.erase(q.begin());           // 뒤의 모든 원소를 한 칸씩 당긴다 -> O(n)
    for (int nxt : graph[cur]) q.push_back(nxt);
}
// 또는 v.insert(v.begin(), x) 로 앞에 계속 끼워 넣기
```

왜: `vector`는 원소가 메모리에 나란히 놓인 구조라, **앞에서 빼면 뒤의 모든 원소를 한 칸씩 이동**해야 한다. `erase(begin())`과 `insert(begin(), x)`는 각각 `O(n)`이므로 `n`번 반복하면 `O(n²)`이 된다.

```cpp
// ✅ 고친 코드
queue<int> q;                     // 또는 deque<int> - 양끝 연산이 O(1)
q.push(0);
while (!q.empty()) {
    int cur = q.front(); q.pop();       // O(1)
    for (int nxt : graph[cur]) q.push(nxt);
}
// 앞에 쌓는 것이 목적이라면 push_back 후 마지막에 reverse() 해도 된다
```

**4) 컨테이너를 값으로 받아 매 호출마다 복사한다**

```cpp
// ❌ 틀린 코드
long long best(vector<int> a, int lo, int hi) {   // 호출마다 a 를 통째로 복사
    if (lo >= hi) return a[lo];
    int mid = lo + (hi - lo) / 2;
    return max(best(a, lo, mid), best(a, mid + 1, hi));
}
// "인덱스만 넘기니까 O(log n) 이겠지" 라고 분석한다
```

왜: `vector<int> a`는 **값 전달**이라 호출마다 원소 `n`개가 복사된다. 호출이 `O(n)`개이므로 복사만 `O(n²)`이고, 동시에 살아 있는 사본 때문에 공간도 `O(n log n)`으로 부푼다. `&` 한 글자가 빠졌을 뿐인데 등급이 통째로 달라지며, 컴파일러는 아무 경고도 하지 않는다.

```cpp
// ✅ 고친 코드
long long best(const vector<int>& a, int lo, int hi) {   // 복사 0
    if (lo >= hi) return a[lo];
    int mid = lo + (hi - lo) / 2;
    return max(best(a, lo, mid), best(a, mid + 1, hi));
}
// 고쳐야 하면 const 를 빼고 vector<int>& 로, 읽기만 하면 const 를 붙인다
```

**5) `.size()`가 부호 없는 타입임을 잊는다**

```cpp
// ❌ 틀린 코드
vector<int> v;                    // 비어 있을 수 있다
for (size_t i = 0; i < v.size() - 1; i++)   // v.size()==0 이면 0-1 = 거대한 수
    if (v[i] > v[i + 1]) { /* ... */ }
// 빈 입력에서만 터지는, 재현이 어려운 버그
```

왜: `v.size()`의 타입은 부호 없는 `size_t`다. `0 - 1`은 `-1`이 아니라 **`size_t`의 최댓값(약 1.8×10¹⁹)**이 되어 루프가 사실상 끝나지 않고 범위 밖을 계속 읽는다. `int`와 비교할 때도 `int`가 부호 없는 쪽으로 승격되어 같은 사고가 난다.

```cpp
// ✅ 고친 코드
int n = (int)v.size();            // 부호 있는 정수로 먼저 못 박는다
for (int i = 0; i + 1 < n; i++)   // 뺄셈 대신 덧셈으로 비교하면 더 안전
    if (v[i] > v[i + 1]) { /* ... */ }
```

**6) 같은 구간 합을 질의마다 다시 계산한다**

```cpp
// ❌ 틀린 코드
for (int t = 0; t < q; t++) {          // q개의 질의
    int lo, hi; cin >> lo >> hi;
    long long s = 0;
    for (int i = lo; i <= hi; i++) s += a[i];   // 구간 길이만큼 -> 최악 O(n)
    cout << s << '\n';
}
// 전체 O(q * n)
```

왜: 질의가 `q`개이고 각 질의가 최악 `n`개를 더하므로 `O(qn)`이다. `n = q = 10⁵`이면 100억 번이다. 구간 합은 **미리 한 번 계산해 두면 질의마다 뺄셈 한 번**으로 끝난다.

```cpp
// ✅ 고친 코드
vector<long long> pre(n + 1, 0);            // 누적합은 반드시 long long
for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + a[i];   // 전처리 O(n)
for (int t = 0; t < q; t++) {
    int lo, hi; cin >> lo >> hi;
    cout << pre[hi + 1] - pre[lo] << '\n';  // 질의당 O(1) -> 전체 O(n + q)
}
```

**7) 깊이가 `n`인 재귀를 그대로 제출한다**

```cpp
// ❌ 틀린 코드
long long rec_sum(const vector<int>& a, int i) {
    if (i == (int)a.size()) return 0;
    return a[i] + rec_sum(a, i + 1);        // 깊이가 n 에 비례
}
// n = 1000000 을 넣으면 오류 메시지도 없이 프로세스가 죽는다
```

왜: C++에는 파이썬 같은 "재귀 깊이 1000" 제한이 없지만, 대신 **운영체제가 잡아 준 스택(보통 1MB~8MB)을 넘는 순간 스택 오버플로**로 프로그램이 종료된다. 프레임 하나가 32~64바이트면 1MB에 2~3만 프레임이 한계이고, 함수 안에 지역 배열이 있으면 그보다 훨씬 빨리 터진다. 예외가 아니라 **비정상 종료**라 원인을 찾기 어렵다.

```cpp
// ✅ 고친 코드
long long iter_sum(const vector<int>& a) {
    long long s = 0;
    for (int x : a) s += x;      // 시간 O(n), 공간 O(1), 깊이 항상 1
    return s;
}
// 재귀 구조가 본질적이면 stack<...> 에 상태를 쌓아 힙에서 관리한다
```

**8) 출력마다 `endl`을 쓴다**

```cpp
// ❌ 틀린 코드
int main() {
    int n; cin >> n;
    for (int i = 0; i < n; i++) cout << i << endl;   // n = 1e6
    return 0;
}
// 복잡도는 O(n) 인데 시간 초과가 난다
```

왜: `endl`은 줄바꿈 **더하기 버퍼 flush**다. 출력이 100만 줄이면 flush가 100만 번 일어나 매번 운영체제 호출을 한다. 등급은 `O(n)` 그대로지만 상수가 수십 배로 커진다. 또 `cin`과 `cout`이 C 표준 입출력과 동기화돼 있는 것도 큰 비용이다.

```cpp
// ✅ 고친 코드
int main() {
    ios_base::sync_with_stdio(false);   // C 입출력과의 동기화 해제
    cin.tie(nullptr);                   // cin 앞에서 cout 을 flush 하지 않음
    int n; cin >> n;
    for (int i = 0; i < n; i++) cout << i << '\n';   // 버퍼에 쌓았다 한 번에
    return 0;
}
```

**9) 등급이 아니라 상수만 최적화한다**

```cpp
// ❌ 틀린 코드  ( n = 100000 )
long long cnt = 0;
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)      // 삼각형이라 절반이지만 여전히 O(n^2)
        if (a[i] + a[j] == target) cnt++;
// "j 를 i+1 부터 돌려 절반 줄였으니 괜찮겠지"
```

왜: 절반으로 줄여도 `n(n-1)/2 ≈ 5·10⁹`번이라 등급은 `O(n²)` 그대로다. **계수 `1/2`는 Big-O가 흡수한다.** 필요한 것은 상수 개선이 아니라 **등급을 한 칸 낮추는 구조 변경**이다. C++가 파이썬보다 빠르다는 사실도 여기서는 도움이 되지 않는다.

```cpp
// ✅ 고친 코드
unordered_map<int, int> cntMap;
long long cnt = 0;
for (int x : a) {                        // 한 번만 훑는다
    auto it = cntMap.find(target - x);
    if (it != cntMap.end()) cnt += it->second;   // 짝이 왼쪽에 몇 개 있었나
    cntMap[x]++;
}
// 전체 평균 O(n)
```

**다음 챕터로**

- 이 챕터의 결론은 하나다. **알고리즘 선택은 지문의 `n`을 읽는 순간 이미 절반이 끝난다.** 앞으로 어떤 문제를 만나든 "이 `n`에서 허용되는 등급은 무엇인가"를 먼저 적고 설계를 시작하면, 잘못된 방향으로 구현을 끝까지 밀고 가는 사고를 막을 수 있다.

- 이어지는 챕터들의 자료구조·알고리즘은 사실상 **"복잡도를 한 칸 낮추는 도구 상자"**다. 정렬과 이분 탐색은 `O(n)`을 `O(log n)`으로, 해시는 탐색을 `O(1)`로, 누적합·투 포인터는 반복 계산을 한 번 훑기로, DP는 지수를 다항식으로 끌어내린다. 이 챕터에서 만든 "상태 수 × 전이 비용" 공식이 그중 DP의 계산을 그대로 담당한다.

- 공간복잡도 감각도 계속 쓰인다. 2차원 DP 표를 `n = 10⁵`에 잡으려다 메모리가 먼저 터지는 일, 재귀 깊이가 스택을 넘어 프로세스가 죽는 일은 모두 이 챕터에서 배운 이유로 일어난다.

- C++만의 마지막 당부: **복잡도 검산 옆에 자료형 검산을 나란히 두라.** 등급이 맞는데 틀리는 답의 대부분은 `int` 오버플로이고, 그것은 채점 결과가 "시간 초과"가 아니라 "오답"으로 나오기 때문에 복잡도를 다시 들여다보느라 시간을 버리게 만든다.
