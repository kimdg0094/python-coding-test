## L6. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 레슨은 Ch04(시뮬레이션 I) 전체를 한 장으로 묶는 정리다. 새 유형을 배우는 대신, 네 레슨이 사실은 **같은 한 가지 습관**의 변형이었음을 확인하고, 바로 꺼내 쓸 수 있는 뼈대와 자주 넘어지는 지점을 모아 둔다.

**개념 지도**

- Ch04는 크게 "사람이 읽는 형태를 정수 하나로 펴는 쪽"과 "표시를 남기고 세는 쪽" 두 갈래다. 두 갈래 모두 바닥에는 `/`와 `%`, 그리고 "직접 계산하지 말고 기록하라"는 태도가 깔려 있다.

```text
                       Ch04 : simulation I
                                |
         +----------------------+----------------------+
         |                                             |
   UNIT CONVERSION                                  PAINTING
   flatten into one integer                   mark first, count later
         |                                             |
    +----+------+                           +----------+----------+
    |           |                           |                     |
  L1 date/time  L2 base N                 L3 range 1D           L4 rect 2D
  h:m:s -> sec  s -> 10 -> b              cnt[x]++              grid[r][c]++
  y/m/d -> doy  horner / div-mod          sweep events          color assign
    |           |                           |                     |
    +-----------+---------------------------+---------------------+
                                |
                    div-mod ( / and % ) is the engine
```

- 그리고 챕터 전체를 관통하는 파이프라인은 이 한 줄이다. 어떤 문제를 만나든 "지금 나는 A·B·C 중 어디에 있나"를 물으면 길을 잃지 않는다.

```text
   human form         integer form          human form
  +-----------+  A   +------------+   C   +-----------+
  | 23:50     | ---> | 1430       | ----> | 00:15 d+1 |
  | 2024-03-01|      | doy = 61   |       | FRI       |
  | "1010" b2 |      | 10         |       | "12" b8   |
  +-----------+      +------------+       +-----------+
                          | B
                          v
                    + - / % compare
  // A = 환산   B = 정수 연산   C = 복원
```

- C++에서는 이 파이프라인 위에 언어 고유의 지뢰가 세 개 얹힌다. 이 챕터의 오답 대부분이 여기서 나온다.

```text
   C++ traps on top of the pipeline

   1. negative %      -10 % 1440  ==  -10   (NOT 1430)
                      fix : ((t % M) + M) % M
   2. overflow        int holds about 2.1e9 only
                      fix : long long for coords and sums
   3. no bound check  v[i] out of range does NOT throw
                      fix : size R+2, or use v.at(i) while debugging
```

**뼈대 코드**

- (1) 시각·날짜: 환산 → 정수 연산 → 복원.

```cpp
#include <bits/stdc++.h>
using namespace std;

const int DAY = 24 * 3600;              // <- 문제마다 바뀜 (분 단위면 24*60)

int to_unit(int h, int m, int s) {      // 사람이 읽는 형태 -> 정수 하나
    return h * 3600 + m * 60 + s;
}

void from_unit(int t, int& days, int& h, int& m, int& s) {  // 참조로 여러 값 반환
    days = t / DAY;                     // 며칠 넘어갔나
    int rest = t % DAY;                 // 그날의 시각
    h = rest / 3600;
    m = (rest % 3600) / 60;
    s = rest % 60;
}

int wrap(int t, int M) {                // 음수까지 안전한 나머지
    return ((t % M) + M) % M;
}

bool is_leap(int y) {
    return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
}

const int MDAYS[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

int day_of_year(int y, int m, int d) {
    int doy = d;
    for (int mm = 1; mm < m; mm++) {    // 앞선 달들을 통째로 더한다
        int add = MDAYS[mm - 1];        // 1월이 index 0
        if (mm == 2 && is_leap(y)) add = 29;
        doy += add;
    }
    return doy;
}
```

- (2) 진법: 10진을 다리로 삼는 두 함수.

```cpp
const string DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";

long long to_decimal(const string& s, int b) {   // b진 문자열 -> 10진 정수
    long long val = 0;
    for (char ch : s) {
        size_t pos = DIGITS.find(ch);
        if (pos == string::npos) return -1;      // 잘못된 문자는 조용히 넘기지 않는다
        val = val * b + (long long)pos;
    }
    return val;
}

string to_base(long long n, int b) {             // 10진 정수 -> b진 문자열
    if (n == 0) return "0";                      // 0은 반드시 특수 처리
    string res = "";
    while (n > 0) {
        res.push_back(DIGITS[n % b]);            // 뒤에 붙이고
        n /= b;
    }
    reverse(res.begin(), res.end());             // 마지막에 한 번 뒤집는다 : O(L)
    return res;
}
```

- (3) 칠하기: 1차원 칸 배열과 2차원 카운트 격자.

```cpp
// 1D : 좌표 1..L, 닫힌 구간 [a, b]
vector<int> cnt(L + 2, 0);              // 여유 칸 2개(1-based + 오른쪽 여유)
for (auto& iv : intervals) {
    for (int x = iv.first; x <= iv.second; x++) cnt[x]++;   // <- 닫힌 구간이라 <=
}
int painted = 0, exact_k = 0;
for (int x = 1; x <= L; x++) {
    if (cnt[x] > 0) painted++;
    if (cnt[x] == k) exact_k++;         // <- 문제마다 바뀜
}

// 2D : 행 1..N, 열 1..M
vector<vector<int>> grid(N + 1, vector<int>(M + 1, 0));
for (auto& rc : rects) {
    for (int r = rc.r1; r <= rc.r2; r++)
        for (int c = rc.c1; c <= rc.c2; c++)
            grid[r][c]++;               // <- 색 문제면 grid[r][c] = color (last wins)
}
```

- (4) 이벤트 스위핑: 좌표가 커서 칸을 못 만들 때.

```cpp
vector<pair<long long,int>> events;     // 좌표가 크므로 long long
for (auto& iv : intervals) {            // 반열림 [a, b)
    events.push_back({iv.first,  +1});  // 시작: 두께 +1
    events.push_back({iv.second, -1});  // 끝  : 두께 -1
}
sort(events.begin(), events.end());     // pair 기본 비교 : 같은 좌표면 -1 이 먼저

long long cover = 0, prev = 0, covered = 0;
bool started = false;
for (auto& e : events) {
    long long x = e.first;
    if (cover > 0 && started) covered += x - prev;  // 길이는 두께 갱신 '전'에
    cover += e.second;
    prev = x;
    started = true;
}
```

- (5) 시뮬레이션 루프의 일반형: 상태 → 한 스텝 → 종료 조건.

```cpp
int t = 0;                              // 진행량(턴 수, 시각 ...)
State state = start;                    // <- 문제마다 바뀜: 위치·격자·남은 양

while (true) {
    if (done(state, t)) break;          // <- 종료 조건: 목표 도달 / 시간 끝 / 변화 없음
    step(state);                        // <- 규칙 한 번 적용. 참조로 받아 제자리 수정
    t++;
    if (t > LIMIT) break;               // 무한 루프 안전장치(규칙이 순환할 때)
}
cout << answer(state) << "\n";
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 시각의 덧셈·차이·비교 | 총 초(또는 총 분)로 환산 | 자릿수 올림을 `/`와 `%`가 대신 처리 | O(1) |
| 결과가 음수가 될 수 있다 | `((t % M) + M) % M` | C++ `%`는 음수를 그대로 남긴다 | O(1) |
| 며칠 뒤 요일 | day-of-year 뒤 `% 7` | 요일은 7주기라 나머지가 곧 답 | O(달 수) |
| 총 근무시간 누적 | 구간마다 초 차이를 합산 | 빌림이 없어 실수가 안 생김 | O(기록 수) |
| 임의의 두 진법 변환 | 10진을 다리로 | 두 함수 조합이면 모든 쌍을 처리 | O(자리 수) |
| k진 자릿수 합·판정 | `% k`, `/ k` 반복 | 표기 문자열을 만들 필요가 없음 | O(log_k n) |
| 진법 결과가 커질 수 있다 | `long long` | 36진 7자리면 이미 `int`를 넘는다 | O(1) |
| 좌표가 작은 구간 칠하기 | 1차원 칸 배열 `vector<int>` | 짧고, 어떤 질문에도 한 번 훑어 답함 | O(구간 수 × 길이) |
| 좌표가 10^9까지 큰 덮임 길이 | 이벤트 스위핑 + `long long` | 두께가 변하는 지점만 보면 충분 | O(n log n) |
| 격자가 수백 규모인 사각형 칠하기 | `vector<vector<int>>` 카운트 격자 | 겹침·색을 같은 코드로 처리 | O(n × 넓이) |
| 격자를 함수에 넘긴다 | `vector<vector<int>>&` | 값 전달은 O(R·C) 복사 | 전달 O(1) |
| 사각형 두 개의 겹침만 필요 | max/min 교집합 공식 | 격자를 만들지 않아도 됨 | 쌍마다 O(1) |
| 나중에 칠한 색이 이겨야 함 | 순서대로 대입(last wins) | 대입 자체가 덮어쓰기라 공짜 | O(n × 넓이) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 시:분:초를 총 초로 바꾸면 왜 계산이 쉬워지는지, `/`와 `%`가 각각 무엇을 뜻하는지.
- [ ] 설명할 수 있다: 총 분에서 "며칠 넘어갔는지"와 "그날의 시각"을 분리하는 두 식과, 그 둘이 유일하게 정해지는 이유.
- [ ] 설명할 수 있다: C++의 `%`가 음수에서 음수를 준다는 것과, `((t % M) + M) % M`이 왜 안전한지.
- [ ] 설명할 수 있다: `-7 / 2`가 파이썬의 `-4`가 아니라 `-3`인 이유(0쪽 절삭).
- [ ] 설명할 수 있다: 윤년 조건 `(y%4==0 && y%100!=0) || y%400==0`의 세 규칙이 각각 무엇을 보정하는지.
- [ ] 설명할 수 있다: day-of-year를 구한 뒤 `(doy - 1) % 7`로 요일을 얻는 이유(왜 1을 빼는가).
- [ ] 설명할 수 있다: 호너 방식 `val = val*b + 자릿값`이 왜 자리값 거듭제곱과 같은 결과를 주는지.
- [ ] 설명할 수 있다: `n % b`가 왜 마지막 자리이고, 결과 문자열을 앞에 붙이는 것과 뒤에 붙였다 뒤집는 것의 비용 차이.
- [ ] 설명할 수 있다: `to_base`에서 `n == 0`을 특수 처리하지 않으면 무슨 일이 벌어지는지.
- [ ] 설명할 수 있다: `string::find`가 못 찾으면 예외가 아니라 `npos`를 준다는 것과 그 위험.
- [ ] 설명할 수 있다: 칸 배열이 겹침을 자동으로 한 번만 세는 이유(포함-배제를 왜 안 해도 되는지).
- [ ] 설명할 수 있다: 닫힌 구간 `[a,b]`와 반열림 구간 `[a,b)`의 길이·순회 범위 차이.
- [ ] 설명할 수 있다: 좌표가 10^9일 때 칸 배열이 불가능한 이유와, 스위핑이 왜 가능한지.
- [ ] 설명할 수 있다: 스위핑에서 길이를 더하는 시점이 두께 갱신 "전"이어야 하는 이유.
- [ ] 설명할 수 있다: `pair` 정렬에서 같은 좌표일 때 `-1`이 먼저 오는 이유와, 그것이 맞닿는 구간에 주는 효과.
- [ ] 설명할 수 있다: 두 사각형의 교집합이 `[max(시작), min(끝)]`인 이유와, 언제 겹침이 없는지.
- [ ] 설명할 수 있다: 색칠에서 `++`(누적)과 `= color`(대입)의 결과가 어떻게 달라지는지.
- [ ] 설명할 수 있다: 격자를 함수에 값으로 넘길 때의 비용과, `&`·`const&`를 언제 쓰는지.

**⚠️ 자주 하는 실수**

**1) 닫힌 구간인데 끝을 빼먹는다**

```cpp
// ❌ 틀린 코드
for (int x = a; x < b; x++) {    // b 칸이 칠해지지 않는다
    cnt[x]++;
}
```

왜: 문장이 "`a`부터 `b`까지"(양 끝 포함)인데 `x < b`는 `b-1`에서 멈춘다. 구간 하나마다 정확히 한 칸씩 모자라 답이 조용히 작아진다.

```cpp
// ✅ 고친 코드
for (int x = a; x <= b; x++) {   // 닫힌 구간 [a, b] 는 <= 로
    cnt[x]++;
}
```

**2) 반열림 구간의 길이를 닫힌 구간처럼 센다**

```cpp
// ❌ 틀린 코드
covered += (b - a + 1);          // [a, b) 인데 +1 을 붙였다
```

왜: `[a, b)`는 `b`를 포함하지 않으므로 길이가 `b - a`다. `+1`을 붙이면 구간마다 1씩 부풀고, `[0,5)`와 `[5,10)`처럼 맞닿는 경우 경계 좌표가 두 번 세어진다.

```cpp
// ✅ 고친 코드
covered += (b - a);              // 반열림 [a, b) 의 길이
```

**3) 음수가 나오는데 `%` 보정을 빠뜨린다**

```cpp
// ❌ 틀린 코드
int minutes_before(int t, int k) {
    return (t - k) % 1440;       // t-k 가 음수면 결과도 음수
}
// minutes_before(10, 20) -> -10   (원하는 값은 1430)
```

왜: 파이썬의 `%`는 결과가 항상 0 이상이라 이 코드가 그대로 동작했지만, C++은 몫을 0 쪽으로 자르므로 나머지에 음수가 남는다. 그 값으로 시각을 복원하면 `-1:50` 같은 값이 나오고, 배열 인덱스로 쓰면 범위 밖 접근이 된다.

```cpp
// ✅ 고친 코드
int minutes_before(int t, int k) {
    int M = 1440;
    return (((t - k) % M) + M) % M;   // 한 번 보정하면 항상 0..M-1
}
```

**4) 윤년 조건을 `||`로 뭉뚱그린다**

```cpp
// ❌ 틀린 코드
bool is_leap(int y) {
    return y % 4 == 0 || y % 400 == 0;    // 1900년을 윤년으로 판정
}
```

왜: 100의 배수를 제외하는 규칙이 빠졌다. 1900은 4의 배수라 이 식에서는 윤년이 되지만 실제로는 평년이라, 2월 일수가 하루 어긋나고 그 뒤 모든 날짜·요일이 틀어진다.

```cpp
// ✅ 고친 코드
bool is_leap(int y) {
    return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
}
```

**5) 누적 시간에 하루 나머지를 적용한다**

```cpp
// ❌ 틀린 코드
int h = (total / 3600) % 24;     // 총 근무 26시간이 2시간으로 줄어든다
```

왜: `% 24`는 "그날의 시각"을 구할 때 쓰는 연산이다. 여러 날에 걸친 누적 시간(길이)에 쓰면 하루를 넘긴 만큼이 통째로 사라진다. 시각(위치)과 시간(길이)은 다른 값이다.

```cpp
// ✅ 고친 코드
int h = total / 3600;            // 누적 길이이므로 24로 감싸지 않는다
int m = (total % 3600) / 60;
int s = total % 60;
```

**6) 진법 변환에서 0을 빠뜨린다**

```cpp
// ❌ 틀린 코드
string to_base(long long n, int b) {
    string res = "";
    while (n > 0) {              // n 이 0이면 루프를 한 번도 안 돈다
        res = string(1, DIGITS[n % b]) + res;
        n /= b;
    }
    return res;                  // "" 가 반환된다
}
```

왜: `n = 0`이면 `while` 조건이 처음부터 거짓이라 빈 문자열이 나온다. 출력이 비어 버리거나, 이어붙인 결과가 통째로 어긋난다.

```cpp
// ✅ 고친 코드
string to_base(long long n, int b) {
    if (n == 0) return "0";      // 0은 자리 하나짜리 예외
    string res = "";
    while (n > 0) {
        res.push_back(DIGITS[n % b]);
        n /= b;
    }
    reverse(res.begin(), res.end());
    return res;
}
```

**7) 스위핑에서 길이를 두께 갱신 뒤에 더한다**

```cpp
// ❌ 틀린 코드
for (auto& e : events) {
    cover += e.second;                       // 두께를 먼저 바꿔 버렸다
    if (cover > 0 && started) covered += e.first - prev;
    prev = e.first;
    started = true;
}
```

왜: `prev`부터 `x`까지 구간을 덮고 있었는지는 **이 이벤트가 일어나기 직전의 두께**로 판단해야 한다. 먼저 갱신하면 구간이 끝나는 순간(`-1`)에 그 구간의 길이를 잃고, 시작하는 순간(`+1`)에는 덮이지 않았던 앞 구간을 더해 버린다.

```cpp
// ✅ 고친 코드
for (auto& e : events) {
    if (cover > 0 && started) covered += e.first - prev;  // 먼저 정산하고
    cover += e.second;                                    // 그 다음 두께 갱신
    prev = e.first;
    started = true;
}
```

**8) 좌표·누적을 `int`로 잡아 오버플로를 낸다**

```cpp
// ❌ 틀린 코드
int covered = 0;
for (auto& iv : intervals) covered += iv.second - iv.first;   // 좌표가 1e9 급
// covered 가 21억을 넘는 순간 음수로 뒤집힌다
```

왜: `int`는 약 21억까지다. 좌표가 10^9이고 구간이 여러 개면 길이 합이 그 한계를 쉽게 넘는데, C++은 경고 없이 음수로 감아 버린다. 답이 크게 틀리지만 프로그램은 멀쩡히 끝나서 원인을 찾기 어렵다.

```cpp
// ✅ 고친 코드
long long covered = 0;
for (auto& iv : intervals) covered += (long long)iv.second - iv.first;
```

**9) 1-based 격자를 크기 그대로 잡는다**

```cpp
// ❌ 틀린 코드
vector<vector<int>> grid(N, vector<int>(M, 0));   // 1..N, 1..M 로 쓸 계획인데
grid[N][M]++;                                     // 범위 밖 : 오류도 안 난다
```

왜: 인덱스는 0부터 시작하므로 `1..N`을 쓰려면 칸이 `N+1`개 필요하다. 파이썬이라면 `IndexError`로 즉시 알려 줬겠지만, C++ `operator[]`는 범위를 검사하지 않아 남의 메모리를 조용히 망가뜨리고 한참 뒤에 엉뚱한 곳에서 터진다.

```cpp
// ✅ 고친 코드
vector<vector<int>> grid(N + 1, vector<int>(M + 1, 0));   // 0번 줄은 버리고 1..N
grid[N][M]++;
```

**10) 격자를 함수에 값으로 넘긴다**

```cpp
// ❌ 틀린 코드
void paint(vector<vector<int>> g, int r1, int c1, int r2, int c2) {
    for (int r = r1; r <= r2; r++)
        for (int c = c1; c <= c2; c++) g[r][c]++;   // 복사본만 바뀐다
}
```

왜: 값 전달이라 호출마다 R×C 원소가 통째로 복사되고, 그러고도 바깥 격자는 하나도 안 바뀐다. 파이썬에서는 격자를 넘기면 저절로 공유돼 이 코드가 동작했기 때문에 특히 걸려 넘어지기 쉽다.

```cpp
// ✅ 고친 코드
void paint(vector<vector<int>>& g, int r1, int c1, int r2, int c2) {
    for (int r = r1; r <= r2; r++)
        for (int c = c1; c <= c2; c++) g[r][c]++;   // 원본이 바뀐다, 복사도 없다
}
```

**다음 챕터로**

- Ch05는 같은 "표시하고 센다"를 **한 번 훑기(one pass)** 로 압축한다. 배열을 한 번 지나며 현재 상태(cur)와 최댓값(best)을 굴리는 기법, 값을 인덱스로 삼아 기록하는 기법이 이어진다.
- 특히 Ch04 L4의 격자 순회는 Ch05 L3의 dx/dy 이동으로 확장된다. "격자에 찍는다"에서 "격자 위를 걷는다"로 한 걸음 나아가는 것이다. 그때 이 챕터에서 본 음수 `%` 함정이 `(d - 1) % 4` 형태로 다시 나타난다.
