## L5. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch1(함수)의 핵심 — 반환 없는/있는 함수, 여러 값 반환, 기본 인자, 값 전달 vs 참조 전달, 변수의 영역 — 을 **반복 훈련**하고, 코딩테스트 단골 유형을 "함수로 쪼개서 푸는" 연습으로 **확장**하는 세트다.
- **반복 훈련 개념**
- 반환 없는 함수(부수 효과만): `void show(int x) { cout << x << '\n'; }` — 반환 타입 자리에 `void`를 적고, 호출한 쪽은 반환값을 쓰지 않는다.
- 반환 있는 함수: C++은 **반환 타입을 반드시 명시**한다. `int`, `bool`, `string`, `long long` 중 무엇을 돌려줄지 먼저 정하고 함수 머리에 적는다.
- 여러 값 반환: C++에는 파이썬의 튜플 언패킹이 없다. `pair<int,int>` / `tuple<int,int,int>`를 반환하고 `auto [a, b, c] = f(...);`(C++17 구조적 바인딩)로 받거나, 참조 인자 `void f(int x, int& q, int& r)`로 채워 준다.
- 기본 인자: `int discounted(int price, int rate = 10)` — 인자를 생략하면 `10`이 쓰인다. 기본값이 있는 매개변수는 없는 매개변수보다 **뒤**에 둬야 한다.
- 값 전달 vs 참조 전달: **C++은 값 전달이 기본**이다. `void f(vector<int> v)`처럼 받으면 벡터가 통째로 복사되어 함수 안에서 `v[i] = ...`를 해도 바깥은 그대로다. 원본을 바꾸려면 `vector<int>& v`, 바꾸지 않고 복사만 피하려면 `const vector<int>& v`.
- 변수의 영역: 전역 변수는 함수 안에서 그냥 대입할 수 있다(파이썬의 `global` 선언 같은 것이 없다). 대신 함수 안에 같은 이름의 지역 변수를 선언하면 전역이 **가려져서**(shadowing) 조용히 엉뚱한 값이 갱신된다.
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '함수' 단계(자기 자신을 만드는 수, 자릿수 규칙 판정 유형), 프로그래머스 「코딩테스트 고득점 Kit」의 '완전탐색'(모든 쌍 검사), 『이것이 취업을 위한 코딩테스트다』의 '구현' 파트(명령 처리 시뮬레이션) — 모두 "판정/계산 부품을 함수로 떼어낸 뒤 메인에서 조립"하는 형태로 풀린다.
- **문제 구성표**

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 막대 그래프 출력기 | Easy | `void` 함수(출력 부수 효과) | 반복 훈련 |
| 2 | 초를 시·분·초로 | Easy | `tuple` 반환 + 구조적 바인딩 | 반복 훈련 |
| 3 | 기본 할인율 계산기 | Easy | 기본 인자 | 반복 훈련 |
| 4 | 가위바위보 전적 집계 | Medium | 판정 함수(값 반환) + `tuple` 반환 | 반복 훈련 |
| 5 | 구간 뒤집기 명령 처리 | Medium | 참조 인자 `vector<int>&`로 제자리 수정 | 반복 훈련 |
| 6 | 우박수 단계 수 세기 | Medium | 전역 호출 카운터 + 초기화 함정 + `long long` | 반복 훈련 |
| 7 | 가장 가까운 두 점 | Medium | 거리 함수 부품 + `const&`로 복사 방지 | 유형 확장 (프로그래머스 Kit '완전탐색' 스타일) |
| 8 | 이웃 합이 가장 큰 칸 | Medium | 범위 판정 함수 + 연쇄 비교 함정 | 유형 확장 (이코테 '구현' 스타일) |
| 9 | 계좌 이체 시뮬레이션 | Hard | 참조 인자 + `bool` 반환 + 전역 실패 카운터 | 유형 확장 (이코테 '구현' 스타일) |
| 10 | 생성자 없는 수 | Hard | 계산 함수 + 표시 함수(참조 인자) 조립 | 유형 확장 (백준 단계별 '함수' 단계 스타일) |

**문제**

**1) 막대 그래프 출력기** · Easy

- **요구사항**: 항목 이름 `label`과 값 `value`를 받아 `label|` 뒤에 `#`을 `value`개 이어 붙인 한 줄을 출력하는, 값을 반환하지 않는 함수 `void print_bar(const string& label, int value)`를 만들어라. 메인은 입력 줄마다 이 함수를 호출만 한다.
- **입력**: 첫 줄에 항목 수 `n`(1 ≤ n ≤ 20). 다음 `n`개 줄에 `label value`(`label`은 공백 없는 알파벳 1~10자, 0 ≤ value ≤ 30).
- **출력**: 항목마다 한 줄씩 `label|####` 형식(`#`은 `value`개). `value`가 0이면 `label|`만 출력한다.
- **예제**: `3 / mon 3 / tue 0 / wed 5` → `mon|### / tue| / wed|#####`
- **셀프체크**: C++에는 문자열 반복 연산자가 없다 — `string(value, '#')`(문자 `'#'`을 `value`개 채운 문자열)을 썼는가? 인자 순서를 `string('#', value)`로 바꿔 쓰지 않았는가? `value`가 0일 때 `string(0, '#')`이 빈 문자열이 되어 `label|`만 나오는가? 반환 타입이 `void`인데 메인이 `int x = print_bar(...)`처럼 반환값을 기대하지 않았는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

void print_bar(const string& label, int value) {
    cout << label << '|' << string(value, '#') << '\n';
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 0; i < n; i++) {
        string label;
        int value;
        cin >> label >> value;
        print_bar(label, value);
    }
    return 0;
}
@@TESTS
--IN
3
mon 3
tue 0
wed 5
--OUT
mon|###
tue|
wed|#####
--IN
1
x 0
--OUT
x|
--IN
2
a 1
b 30
--OUT
a|#
b|##############################
@@EXPL
(1) 접근·핵심 아이디어

- "한 항목을 한 줄로 그리는 일"은 결과값이 필요 없는 순수한 출력 작업이므로 반환 타입 `void`인 함수 `print_bar`가 자연스럽다. 메인은 무엇을 그릴지(입력 파싱)만 맡고, 어떻게 그릴지는 함수에 위임한다.
- 막대는 `string(value, '#')` 생성자로 만든다. 첫 인자가 개수, 둘째 인자가 채울 **문자**다. `value == 0`이면 빈 문자열이 되어 `label|`만 남는 것이 경계값이다.

(2) 코드 단계별

- `print_bar(const string& label, int value)`: 문자열 매개변수를 `const string&`로 받아 복사를 피한다. 값으로 받아도 답은 같지만 큰 문자열이 오갈 때 손해다.
- 출력은 `cout << label << '|' << string(value, '#') << '\n'` 한 줄. `<<`로 이어 붙이면 사이에 공백이 끼지 않는다.
- `main`: `cin >> label >> value`로 공백 구분 토큰을 그대로 읽어 함수에 전달. 반환값은 받지 않는다.
- `endl` 대신 `'\n'`을 쓰면 매번 버퍼를 비우지 않아 빠르다.

(3) 스스로 다시 짤 때 생각 순서

- "출력만 하는 일"인지 확인 → 반환 타입을 `void`로 결정 → 달라지는 부분(이름·값)을 매개변수로 뽑는다 → 값 0인 경계를 손으로 찍어 형식(`label|`)을 확인.
```

**2) 초를 시·분·초로** · Easy

- **요구사항**: 초 단위 정수 `sec`를 받아 `(시, 분, 초)` 세 값을 **한 번에 반환**하는 함수 `tuple<int,int,int> to_hms(int sec)`를 만들어라. 메인은 반환된 튜플을 `auto [h, m, s] = to_hms(sec);`로 받아 출력한다. 시는 24를 넘어도 그대로 둔다(날짜로 넘기지 않는다).
- **입력**: 첫 줄에 질의 수 `n`(1 ≤ n ≤ 100). 다음 `n`개 줄에 정수 `sec`(0 ≤ sec ≤ 1,000,000).
- **출력**: 질의마다 한 줄에 `h m s`(공백 구분).
- **예제**: `2 / 3661 / 59` → `1 1 1 / 0 0 59` · `1 / 0` → `0 0 0`
- **셀프체크**: 분은 `(sec % 3600) / 60`처럼 "시를 뗀 나머지"에서 구했는가(`sec / 60`을 그대로 쓰면 분이 60을 넘는다)? `sec = 0`에서 `0 0 0`이 나오는가? 세 값을 `make_tuple(h, m, s)`로 묶어 돌려주고 메인이 구조적 바인딩으로 받는가(값이 두 개뿐이면 `pair`, 세 개 이상이면 `tuple`)?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

tuple<int, int, int> to_hms(int sec) {
    int h = sec / 3600;
    int m = (sec % 3600) / 60;
    int s = sec % 60;
    return make_tuple(h, m, s);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 0; i < n; i++) {
        int sec;
        cin >> sec;
        auto [h, m, s] = to_hms(sec);
        cout << h << ' ' << m << ' ' << s << '\n';
    }
    return 0;
}
@@TESTS
--IN
2
3661
59
--OUT
1 1 1
0 0 59
--IN
1
0
--OUT
0 0 0
--IN
3
90000
3600
86399
--OUT
25 0 0
1 0 0
23 59 59
@@EXPL
**이 풀이의 새 문법**

- `tuple<int,int,int>`와 구조적 바인딩 `auto [h, m, s] = f(...);`(C++17): 값 여러 개를 한 번에 반환하고 한 번에 풀어 받는다. 두 개면 `pair<int,int>`와 `auto [a, b] = ...`로 충분하다. 옛 방식은 `int h, m, s; tie(h, m, s) = to_hms(sec);`.

(1) 접근·핵심 아이디어

- 시·분·초는 하나의 계산에서 동시에 나오는 세 결과다. C++ 함수는 값을 하나만 반환하므로 세 값을 `tuple`로 묶어 돌려주고 호출한 쪽에서 풀어 받는다. 참조 인자 `void to_hms(int sec, int& h, int& m, int& s)`로 채워 주는 방식도 똑같이 쓰인다.
- 함정은 분 계산이다. `sec / 60`은 "전체 분"이라 60을 넘을 수 있다. 시(3600초)를 먼저 떼어낸 나머지 `sec % 3600`에서 분을 구해야 0~59 범위가 된다.

(2) 코드 단계별

- `to_hms`: `h = sec / 3600`, `m = (sec % 3600) / 60`, `s = sec % 60`. C++의 `/`는 정수끼리면 자동으로 몫(버림)이라 파이썬의 `//`에 해당한다.
- `main`: 질의마다 정수를 읽어 `auto [h, m, s] = to_hms(sec)`로 세 값을 한꺼번에 받고 `cout << h << ' ' << m << ' ' << s << '\n'`.
- `90000`처럼 하루(86400)를 넘는 값도 `h = 25`로 그대로 두는 것이 요구사항이다. 입력 상한이 100만이라 `int`로 충분하다.

(3) 스스로 다시 짤 때 생각 순서

- "결과가 여러 개"이면 `pair`/`tuple`/참조 인자 중 하나를 고른다 → 시/분/초 공식을 세우고 분에서 `% 3600`을 먼저 적용하는지 확인 → `0`과 `86399`(23 59 59)로 경계를 검산.
```

**3) 기본 할인율 계산기** · Easy

- **요구사항**: 가격 `price`와 할인율 `rate`(%)를 받아 할인 후 가격을 반환하는 함수 `int discounted(int price, int rate = 10)`을 만들어라. 할인율이 입력에 없으면 **기본 인자** `10`이 적용되어야 한다. 할인액은 `price * rate / 100`(정수 나눗셈, 소수점 버림)으로 계산한다.
- **입력**: 첫 줄에 질의 수 `n`(1 ≤ n ≤ 100). 다음 `n`개 줄에 `price` 하나만 있거나 `price rate` 두 값(1 ≤ price ≤ 1,000,000, 0 ≤ rate ≤ 100).
- **출력**: 질의마다 할인 후 가격을 한 줄에 하나씩.
- **예제**: `3 / 1000 / 1000 25 / 999` → `900 / 750 / 900` · `2 / 500 0 / 500 100` → `500 / 0`
- **셀프체크**: 토큰이 하나뿐인 줄에서 `discounted(price)`처럼 두 번째 인자를 생략해 기본값이 쓰이게 했는가? 줄마다 값의 개수가 다르므로 `cin >>`만으로는 줄 경계를 알 수 없다 — `getline`으로 한 줄을 통째로 받아 `istringstream`으로 다시 읽었는가? `cin >> n` 직후 남은 개행을 `cin.ignore(...)`로 버렸는가(안 버리면 첫 `getline`이 빈 줄을 읽는다)? `999`의 10%는 `99`(버림)이라 `900`이 되는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int discounted(int price, int rate = 10) {
    return price - price * rate / 100;
}

int main() {
    int n;
    cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    for (int i = 0; i < n; i++) {
        string line;
        getline(cin, line);
        istringstream iss(line);
        int price, rate;
        iss >> price;
        if (iss >> rate) cout << discounted(price, rate) << '\n';
        else cout << discounted(price) << '\n';
    }
    return 0;
}
@@TESTS
--IN
3
1000
1000 25
999
--OUT
900
750
900
--IN
2
500 0
500 100
--OUT
500
0
--IN
1
7
--OUT
7
@@EXPL
**이 풀이의 새 문법**

- 기본 인자 `int discounted(int price, int rate = 10)`: 매개변수에 `= 값`을 붙이면 호출할 때 그 인자를 생략할 수 있고, 생략하면 적힌 기본값이 들어간다. 기본값이 있는 매개변수는 없는 매개변수보다 뒤에 둬야 한다. 선언과 정의를 나눠 쓸 때는 기본값을 **선언 쪽에만** 적는다(양쪽에 적으면 컴파일 오류).
- `istringstream iss(line); iss >> price;` — 문자열 한 줄을 스트림처럼 다시 읽는다. `if (iss >> rate)`는 "읽기에 성공했는가"를 그대로 조건으로 쓰는 관용구다.

(1) 접근·핵심 아이디어

- "대부분은 10% 할인, 가끔만 다른 할인율"이라는 상황은 기본 인자의 전형적 쓰임이다. 호출하는 쪽은 특별한 경우에만 `rate`를 넘기고, 나머지는 함수가 알아서 기본값을 쓴다.
- 줄마다 토큰 수가 다르므로 줄 단위로 읽어야 한다. `cin >> price >> rate`를 그냥 쓰면 다음 줄의 값을 `rate`로 빨아들여 전부 어긋난다.
- 할인액을 `price * rate / 100`으로 곱셈을 먼저 한 뒤 정수 나눗셈을 해야 버림 오차가 작다(`price / 100 * rate`는 결과가 달라진다).

(2) 코드 단계별

- `cin >> n` 뒤에는 개행이 스트림에 남아 있다. `cin.ignore(numeric_limits<streamsize>::max(), '\n')`으로 그 줄의 끝까지 버려야 첫 `getline`이 정상적으로 첫 데이터 줄을 읽는다.
- 줄을 `istringstream`에 넣고 `iss >> price`로 먼저 읽는다. 이어서 `iss >> rate`가 성공하면 두 인자 호출, 실패하면(토큰이 하나뿐) 기본 인자를 쓰는 한 인자 호출.
- 경계: `rate = 0`이면 할인액 0, `rate = 100`이면 가격 전액이 할인되어 `0`, `price = 7`이면 `7 * 10 / 100 = 0`이라 그대로 `7`.
- 오버플로 점검: `price * rate`는 최대 `1,000,000 * 100 = 1억`이라 `int`(약 21억) 안이다. 가격 상한이 한 자리만 커져도 `long long`으로 올려야 한다.

(3) 스스로 다시 짤 때 생각 순서

- "생략 가능한 인자"가 보이면 기본 인자를 떠올린다 → 줄마다 토큰 수가 다르면 `getline` + `istringstream` → 곱셈 먼저·나눗셈 나중 순서를 확인하고 `999`, `7`로 버림 경계를 검산.
```

**4) 가위바위보 전적 집계** · Medium

- **요구사항**: 한 판의 결과를 판정하는 값 반환 함수 `int judge(char a, char b)`(A가 이기면 `1`, 지면 `-1`, 비기면 `0`)와, 전체 판을 훑어 `(승, 패, 무)` 세 값을 `tuple`로 반환하는 함수 `tuple<int,int,int> tally(const string& A, const string& B)`를 만들어라. 메인은 전적을 출력한 뒤 승이 많으면 `A`, 패가 많으면 `B`, 같으면 `DRAW`를 출력한다. `R`(바위)은 `S`(가위)를, `S`는 `P`(보)를, `P`는 `R`을 이긴다.
- **입력**: 첫 줄에 A의 손 문자열, 둘째 줄에 B의 손 문자열(각각 `R`/`P`/`S`로만 구성, 길이 1~1000, 두 줄의 길이는 같다).
- **출력**: 첫 줄에 A 기준 `승 패 무`(공백 구분), 둘째 줄에 `A`/`B`/`DRAW` 중 하나.
- **예제**: `RPS / SPR` → `1 1 1 / DRAW` · `RRPS / SSSS` → `2 1 1 / A`
- **셀프체크**: `judge`의 매개변수 타입이 `char`인가(문자 하나는 `'R'`처럼 작은따옴표, 문자열은 `"R"`처럼 큰따옴표 — 둘은 다른 타입이다)? `judge`가 같은 손일 때 `0`을 가장 먼저 반환하는가? `tally`가 문자열을 `const string&`로 받아 1000자 복사를 피하는가? `for (int i = 0; i < (int)A.size(); i++)`처럼 `size()`를 `int`로 캐스팅했는가(`size()`는 unsigned라 부호 있는 값과 섞으면 경고·함정이 생긴다)?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int judge(char a, char b) {
    if (a == b) return 0;
    if ((a == 'R' && b == 'S') || (a == 'S' && b == 'P') || (a == 'P' && b == 'R')) return 1;
    return -1;
}

tuple<int, int, int> tally(const string& A, const string& B) {
    int win = 0, lose = 0, draw = 0;
    for (int i = 0; i < (int)A.size(); i++) {
        int r = judge(A[i], B[i]);
        if (r == 1) win++;
        else if (r == -1) lose++;
        else draw++;
    }
    return make_tuple(win, lose, draw);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    string A, B;
    cin >> A >> B;
    auto [w, l, d] = tally(A, B);
    cout << w << ' ' << l << ' ' << d << '\n';
    if (w > l) cout << "A" << '\n';
    else if (l > w) cout << "B" << '\n';
    else cout << "DRAW" << '\n';
    return 0;
}
@@TESTS
--IN
RPS
SPR
--OUT
1 1 1
DRAW
--IN
RRPS
SSSS
--OUT
2 1 1
A
--IN
RRR
RRR
--OUT
0 0 3
DRAW
--IN
P
S
--OUT
0 1 0
B
@@EXPL
(1) 접근·핵심 아이디어

- 문제를 두 층으로 쪼갠다. 아래층 `judge(char a, char b)`는 "한 판의 승패"라는 작은 질문에 `1/-1/0`으로 답하고, 위층 `tally`는 이 부품을 판마다 호출해 세 카운터를 누적한 뒤 `tuple`로 돌려준다. 메인은 튜플을 풀어 받아 출력·판정만 한다.
- 이기는 조합은 딱 세 가지뿐이므로, 같은 손(무승부)을 먼저 걸러낸 뒤 세 조합만 `1`, 나머지는 자동으로 `-1`이 되게 조기 반환으로 짧게 쓴다.

(2) 코드 단계별

- `judge`: 문자 비교이므로 매개변수 타입은 `char`. `a == b`면 `0`, 세 가지 이기는 조합이면 `1`, 그 외 `-1`.
- `tally`: `const string&`로 받아 복사를 피한다. 값으로 받으면 호출할 때마다 최대 1000자 문자열이 통째로 복사된다. 인덱스 `i`로 두 문자열을 같은 위치끼리 짝지어 `judge` 결과에 따라 `win/lose/draw`를 늘린다.
- `A.size()`의 타입은 `size_t`(부호 없음)다. `i < (int)A.size()`로 캐스팅해 두면 부호 섞임 경고와 "빈 문자열에서 `size() - 1`이 거대한 값이 되는" 부류의 함정을 피할 수 있다.
- `main`: `auto [w, l, d]`로 풀어 받아 첫 줄 출력, `w`와 `l`의 대소로 둘째 줄 출력. 같으면(전부 무승부 포함) `DRAW`.

(3) 스스로 다시 짤 때 생각 순서

- "한 판 판정"과 "전체 집계"를 분리 → 판정 함수는 `char` 인자에 무승부부터 조기 반환 → 집계 함수는 문자열을 `const&`로 받고 세 값을 `tuple`로 반환 → `RRR/RRR`(전부 무) 같은 경계로 `DRAW` 분기를 검산.
```

**5) 구간 뒤집기 명령 처리** · Medium

- **요구사항**: 벡터 `arr`와 구간 `[l, r]`을 받아 그 구간의 원소 순서를 **제자리에서** 뒤집는, 값을 반환하지 않는 함수 `void reverse_range(vector<int>& arr, int l, int r)`를 만들어라. 매개변수를 반드시 참조 `&`로 받아 원본이 바뀌게 한다. 새 벡터를 만들어 반환하지 않는다. 메인은 명령마다 함수를 호출하고 마지막에 벡터를 출력한다.
- **입력**: 첫 줄에 `n q`(1 ≤ n ≤ 100, 1 ≤ q ≤ 100). 둘째 줄에 정수 `n`개. 다음 `q`개 줄에 `l r`(0-based, 0 ≤ l ≤ r < n).
- **출력**: 모든 명령을 적용한 뒤의 벡터를 공백으로 구분해 한 줄에.
- **예제**: `5 2 / 1 2 3 4 5 / 0 4 / 1 3` → `5 2 3 4 1` · `3 1 / 7 8 9 / 1 1` → `7 8 9`
- **셀프체크**: 매개변수에 `&`를 빠뜨리면 벡터가 **복사**되어 함수 안 수정이 바깥에 전혀 반영되지 않는다 — `vector<int>& arr`로 적었는가(파이썬은 리스트가 자동 공유되지만 C++은 정반대로 값 전달이 기본이다)? `l == r`이면 아무 일도 안 일어나는가? 같은 구간을 두 번 뒤집으면 원래대로 돌아오는가(검산용)? 출력 줄 끝에 공백이 남지 않는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

void reverse_range(vector<int>& arr, int l, int r) {
    while (l < r) {
        swap(arr[l], arr[r]);
        l++;
        r--;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];
    for (int i = 0; i < q; i++) {
        int l, r;
        cin >> l >> r;
        reverse_range(arr, l, r);
    }
    for (int i = 0; i < n; i++) {
        if (i > 0) cout << ' ';
        cout << arr[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
5 2
1 2 3 4 5
0 4
1 3
--OUT
5 2 3 4 1
--IN
3 1
7 8 9
1 1
--OUT
7 8 9
--IN
4 2
1 2 3 4
0 3
0 3
--OUT
1 2 3 4
@@EXPL
(1) 접근·핵심 아이디어

- 이 문제의 핵심은 `vector<int>& arr`의 `&` 한 글자다. C++은 **값 전달이 기본**이라 `&`가 없으면 함수에 들어가는 순간 벡터 전체가 복사되고, 함수 안에서 아무리 원소를 바꿔도 복사본만 바뀌었다가 함수가 끝나며 버려진다. 파이썬은 리스트를 넘기면 자동으로 같은 객체를 공유하므로 이 지점이 **정반대**다.
- 알고리즘 자체는 두 포인터다. 양 끝 인덱스 `l`, `r`을 안쪽으로 좁혀 가며 `arr[l]`과 `arr[r]`을 `swap`으로 맞바꾼다.

(2) 코드 단계별

- `reverse_range(vector<int>& arr, int l, int r)`: `l`과 `r`은 값으로 받아도 된다(안에서 바뀌어도 바깥에 영향이 없어야 하는 인덱스이므로). 벡터만 참조로 받는다.
- `l < r`인 동안 `swap(arr[l], arr[r])` 후 `l++`, `r--`. `l == r`(가운데 원소 또는 길이 1 구간)이면 반복이 한 번도 돌지 않아 자연히 아무 변화가 없다.
- `swap(a, b)`는 표준 함수다. 파이썬의 `a, b = b, a`(동시 대입)는 C++에 없으므로 `swap`을 쓰거나 임시 변수 `int t = arr[l]; arr[l] = arr[r]; arr[r] = t;`로 세 줄을 써야 한다. `arr[l] = arr[r]; arr[r] = arr[l];`처럼 두 줄만 쓰면 첫 줄에서 값이 덮여 둘 다 같은 값이 된다.
- 출력은 `i > 0`일 때만 공백을 먼저 찍어 줄 끝 공백을 남기지 않는다. 표준 라이브러리 `reverse(arr.begin() + l, arr.begin() + r + 1)`로도 같은 일을 할 수 있다(끝이 열린 구간이라 `+1`).

(3) 스스로 다시 짤 때 생각 순서

- "함수로 원본을 바꾼다" → 컨테이너 매개변수에 `&`를 붙였는지부터 확인 → 두 포인터를 안쪽으로 좁히는 `swap` 루프 → `l == r`과 "두 번 뒤집기" 경계로 검산.
```

**6) 우박수 단계 수 세기** · Medium

- **요구사항**: 전역 정수 `steps`(호출 횟수)를 두고, 다음 값을 돌려주는 함수 `next_value(x)`가 호출될 때마다 `steps`를 1 늘리게 하라. 규칙은 짝수면 `x / 2`, 홀수면 `3x + 1`. 함수 `count_steps(x)`는 `steps`를 0으로 초기화한 뒤 `x`가 1이 될 때까지 `next_value`를 반복 호출하고 최종 `steps`를 반환한다. 질의가 여러 개이므로 **질의마다 전역을 초기화**해야 한다.
- **입력**: 첫 줄에 질의 수 `n`(1 ≤ n ≤ 20). 다음 `n`개 줄에 정수 `x`(1 ≤ x ≤ 1,000,000).
- **출력**: 질의마다 1에 도달하기까지 `next_value`가 호출된 횟수를 한 줄에 하나씩.
- **예제**: `3 / 6 / 1 / 27` → `8 / 0 / 111` · `2 / 6 / 1` → `8 / 0`
- **셀프체크**: 중간값이 `int` 범위를 넘는다 — `x = 837799`는 도중에 약 29억까지 올라가 `int`(약 21억)로는 음수로 뒤집힌다. `x`와 계산을 `long long`으로 잡았는가? 두 번째 질의 전에 `steps`를 0으로 되돌리지 않으면 앞 질의의 값이 누적된다(예제 `6` 다음 `1`에서 `0`이 나와야 한다)? 함수 안에서 `long long steps = 0;`처럼 **같은 이름의 지역 변수를 새로 선언하면 전역이 가려져** 바깥 값이 그대로 0으로 남는다는 것을 확인했는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

long long steps = 0;

long long next_value(long long x) {
    steps++;
    if (x % 2 == 0) return x / 2;
    return 3 * x + 1;
}

long long count_steps(long long x) {
    steps = 0;
    while (x != 1) x = next_value(x);
    return steps;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        cout << count_steps(x) << '\n';
    }
    return 0;
}
@@TESTS
--IN
3
6
1
27
--OUT
8
0
111
--IN
2
6
1
--OUT
8
0
--IN
1
837799
--OUT
524
@@EXPL
(1) 접근·핵심 아이디어

- "함수가 몇 번 불렸는가"는 함수 밖에서 살아남는 상태가 필요하므로 전역 변수 `steps`로 관리한다. C++에서는 파이썬의 `global steps` 같은 선언이 필요 없다 — 전역 이름을 함수 안에서 그냥 읽고 쓰면 된다.
- 함정 세 가지: (a) 함수 안에 `long long steps = 0;`을 다시 선언하면 그 지역 변수가 전역을 가려(shadowing) 전역은 영원히 0이다. (b) 질의가 여러 개이므로 `count_steps` 시작 시 `steps = 0`으로 초기화하지 않으면 이전 질의의 횟수가 더해진다. (c) 콜라츠 수열의 중간값은 입력보다 훨씬 커진다.

(2) 코드 단계별

- `long long steps = 0;`을 함수 밖(전역)에 둔다. 전역 변수는 자동으로 0으로 초기화되지만, 의도를 드러내려고 명시했다.
- `next_value(long long x)`: `steps++` 후 짝수면 `x / 2`, 홀수면 `3 * x + 1`을 반환. `x`가 `long long`이므로 `3 * x`도 `long long`으로 계산된다.
- `count_steps(long long x)`: `steps = 0` 초기화 → `x != 1`인 동안 `x = next_value(x)` → 최종 `steps` 반환. `x = 1`이면 루프가 돌지 않아 `0`.
- 오버플로 실측: `x = 837799`의 수열 최댓값은 2,974,984,576으로 `int` 상한(2,147,483,647)을 넘는다. `int`로 짰다면 값이 음수로 뒤집혀 `x % 2 == 0` 판정이 어긋나고 루프가 영영 끝나지 않거나 엉뚱한 답이 나온다. 이런 오버플로는 예외를 던지지 않고 **조용히** 틀린다.

(3) 스스로 다시 짤 때 생각 순서

- "호출 횟수"는 전역 상태 → 전역 이름을 함수 안에서 다시 선언하지 않는지 확인 → 질의 단위로 초기화 지점을 정한다 → 중간값의 최대 크기를 어림해 `int`/`long long`을 고른다 → `6`(8단계) 다음 `1`(0단계)을 넣어 초기화가 되는지 검산.
```

**7) 가장 가까운 두 점** · Medium

- **요구사항**: 두 점의 거리 제곱을 반환하는 함수 `int dist2(const pair<int,int>& p, const pair<int,int>& q)`와, 점 벡터에서 모든 두 점 쌍을 검사해 가장 작은 거리 제곱을 반환하는 함수 `int closest_pair(const vector<pair<int,int>>& points)`를 만들어라. 제곱근을 쓰지 않고 정수인 거리 제곱으로만 비교한다.
- **입력**: 첫 줄에 점의 수 `n`(2 ≤ n ≤ 100). 다음 `n`개 줄에 좌표 `x y`(−1000 ≤ x, y ≤ 1000, 같은 점이 두 번 나올 수 있다).
- **출력**: 가장 가까운 두 점 사이 거리의 제곱.
- **예제**: `4 / 0 0 / 3 4 / 1 1 / 10 10` → `2` · `2 / 5 5 / 5 5` → `0`
- **셀프체크**: 점 벡터를 `const vector<pair<int,int>>&`로 받아 호출마다 복사되지 않게 했는가(값으로 받으면 함수를 부를 때마다 점 100개가 통째로 복사된다)? 쌍을 `j = i + 1`부터 돌려 같은 쌍을 두 번 세거나 자기 자신과 비교하지 않았는가? "최솟값" 초기값을 0으로 두면 어떤 쌍도 갱신되지 않는다 — 첫 쌍으로 초기화하거나 `-1` 같은 표식을 썼는가? 좌표 차가 최대 2000이라 `dx*dx + dy*dy ≤ 8,000,000`으로 `int` 안임을 확인했는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int dist2(const pair<int, int>& p, const pair<int, int>& q) {
    int dx = p.first - q.first;
    int dy = p.second - q.second;
    return dx * dx + dy * dy;
}

int closest_pair(const vector<pair<int, int>>& points) {
    int best = -1;
    int m = (int)points.size();
    for (int i = 0; i < m; i++) {
        for (int j = i + 1; j < m; j++) {
            int d = dist2(points[i], points[j]);
            if (best == -1 || d < best) best = d;
        }
    }
    return best;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int, int>> points(n);
    for (int i = 0; i < n; i++) cin >> points[i].first >> points[i].second;
    cout << closest_pair(points) << '\n';
    return 0;
}
@@TESTS
--IN
4
0 0
3 4
1 1
10 10
--OUT
2
--IN
2
5 5
5 5
--OUT
0
--IN
3
0 0
0 5
12 0
--OUT
25
@@EXPL
(1) 접근·핵심 아이디어

- "가장 가까운 쌍"은 모든 쌍을 다 재 보면 확실하다(완전탐색). 점이 100개면 쌍은 약 5,000개라 충분히 빠르다.
- 거리 계산을 `dist2` 부품으로 분리하면 메인 루프는 "모든 쌍을 돌며 최솟값 갱신"이라는 뼈대만 남아 읽기 쉽다. 제곱근 없이 거리 제곱으로 비교해도 대소 관계는 같으므로 정수만으로 정확하게 푼다(`sqrt`는 `double`이라 오차가 끼어든다).

(2) 코드 단계별

- 점은 `pair<int,int>`로 담는다. `p.first`가 x, `p.second`가 y. 필드가 셋 이상이거나 이름이 중요하면 `struct`를 쓴다.
- `dist2`는 두 점을 `const pair<int,int>&`로 받는다. `pair` 하나는 작아서 값 전달해도 손해가 크지 않지만, "컨테이너·구조체는 `const&`로 받는다"를 습관으로 굳히는 편이 낫다.
- `closest_pair`는 벡터를 반드시 `const vector<pair<int,int>>&`로 받는다. 값으로 받으면 함수 호출 한 번에 원소 100개가 복사된다. `const`를 붙였으므로 함수 안에서 실수로 원본을 수정할 수도 없다.
- `best = -1`(아직 없음 표식)에서 시작해 `i < j`인 모든 쌍을 돌며 더 작은 거리가 나오면 갱신. 초기값을 0으로 두면 어떤 양수도 갱신되지 않으니 주의.
- `points.size()`는 부호 없는 `size_t`이므로 `int m`에 한 번 받아 두고 비교에 쓴다.

(3) 스스로 다시 짤 때 생각 순서

- "모든 쌍"이면 이중 루프 `j = i + 1`부터 → 거리 부품을 먼저 완성해 `(0,0)-(3,4) = 25`로 검산 → 큰 컨테이너 매개변수에 `const&`를 붙였는지 확인 → 최솟값 초기값 표식 방식을 정하고 같은 점 두 개(`0`)로 경계 확인.
```

**8) 이웃 합이 가장 큰 칸** · Medium

- **요구사항**: 격자 안 좌표인지 판정하는 함수 `bool in_range(int r, int c, int R, int C)`와, 어떤 칸의 상·하·좌·우 이웃 값 합을 반환하는 함수 `int neighbor_sum(const vector<vector<int>>& grid, int r, int c)`를 만들어라. 격자 밖 이웃은 없는 것으로 친다. 모든 칸에 대해 이웃 합을 구해 최댓값과 그 칸의 위치를 출력한다. 최댓값이 여러 칸이면 행 번호가 작은 칸, 같으면 열 번호가 작은 칸을 고른다.
- **입력**: 첫 줄에 `R C`(1 ≤ R, C ≤ 20). 다음 `R`개 줄에 격자 값(각 0 ≤ v ≤ 100, 공백 구분).
- **출력**: 첫 줄에 최대 이웃 합, 둘째 줄에 그 칸의 `r c`(0-based).
- **예제**: `3 3 / 1 2 3 / 4 5 6 / 7 8 9` → `21 / 2 1` · `1 1 / 5` → `0 / 0 0`
- **셀프체크**: 범위 판정을 `0 <= r < R`라고 이어 쓰지 않았는가 — C++에서 이 식은 `(0 <= r) < R`로 해석되어 `true/false(1/0)`를 `R`과 비교하므로 **거의 항상 참**이 된다. `0 <= r && r < R`처럼 `&&`로 이어야 한다. 네 방향 각각을 `in_range`로 걸렀는가(파이썬의 음수 인덱스와 달리 C++ `vector`의 `grid[-1]`은 범위 밖 접근이라 쓰레기 값을 읽거나 프로그램이 죽는다)? 최댓값 동률일 때 먼저 만난 칸(행 우선 순회)을 유지하려면 `>`로만 갱신해야 한다(`>=`면 뒤 칸으로 바뀐다)? 1×1 격자는 이웃이 없어 `0`인가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

bool in_range(int r, int c, int R, int C) {
    return 0 <= r && r < R && 0 <= c && c < C;
}

int neighbor_sum(const vector<vector<int>>& grid, int r, int c) {
    int R = (int)grid.size();
    int C = (int)grid[0].size();
    int total = 0;
    if (in_range(r - 1, c, R, C)) total += grid[r - 1][c];
    if (in_range(r + 1, c, R, C)) total += grid[r + 1][c];
    if (in_range(r, c - 1, R, C)) total += grid[r][c - 1];
    if (in_range(r, c + 1, R, C)) total += grid[r][c + 1];
    return total;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int R, C;
    cin >> R >> C;
    vector<vector<int>> grid(R, vector<int>(C));
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) cin >> grid[r][c];
    int best = -1, br = 0, bc = 0;
    for (int r = 0; r < R; r++) {
        for (int c = 0; c < C; c++) {
            int s = neighbor_sum(grid, r, c);
            if (s > best) {
                best = s;
                br = r;
                bc = c;
            }
        }
    }
    cout << best << '\n';
    cout << br << ' ' << bc << '\n';
    return 0;
}
@@TESTS
--IN
3 3
1 2 3
4 5 6
7 8 9
--OUT
21
2 1
--IN
1 1
5
--OUT
0
0 0
--IN
1 3
5 5 5
--OUT
10
0 1
--IN
2 2
1 1
1 1
--OUT
2
0 0
@@EXPL
**이 풀이의 함정 하나**

- 파이썬은 `0 <= r < R`처럼 비교를 이어 쓸 수 있지만 **C++은 안 된다**. `0 <= r < R`은 먼저 `0 <= r`을 계산해 `true`(1) 또는 `false`(0)를 얻고, 그 값을 `R`과 비교한다. `R`이 2 이상이면 `1 < R`도 `0 < R`도 참이라 어떤 `r`이든 통과한다. 반드시 `0 <= r && r < R`로 쓴다.

(1) 접근·핵심 아이디어

- 격자 문제의 단골 부품은 "이 좌표가 격자 안인가"를 답하는 `in_range`다. 이 판정을 한 곳에 모아 두면 네 방향 이웃 검사가 모두 같은 함수를 재사용해 실수가 줄어든다.
- 함정: 파이썬에서 `grid[-1]`은 에러 없이 마지막 행을 읽어 조용히 틀린 답을 냈지만, C++ `vector`의 `operator[]`에 음수를 넣으면 아예 **할당되지 않은 메모리**를 읽는다(범위 검사가 없다). 쓰레기 값이 나오거나 그 자리에서 죽는다. 어느 쪽이든 범위 검사를 빠뜨리면 안 된다.
- 동률 처리는 행 우선으로 순회하면서 `>`일 때만 갱신하면, 먼저 만난(행·열이 작은) 칸이 자연히 남는다.

(2) 코드 단계별

- `in_range`: 반환 타입은 `bool`. `0 <= r && r < R && 0 <= c && c < C`를 그대로 반환한다.
- `neighbor_sum`: 격자를 `const vector<vector<int>>&`로 받는다(값으로 받으면 칸마다 400칸 격자를 통째로 복사한다). 크기는 `grid.size()`, `grid[0].size()`로 얻고 `int`로 캐스팅한다.
- 상·하·좌·우 네 좌표를 각각 `in_range`로 검사해 안쪽일 때만 값을 더해 반환.
- `main`: `vector<vector<int>> grid(R, vector<int>(C))`로 2차원 격자를 만들고 모든 칸을 행 우선으로 돌며 `best`를 `>`로만 갱신. 값이 0 이상이므로 초기값 `-1`이면 첫 칸에서 반드시 갱신된다.

(3) 스스로 다시 짤 때 생각 순서

- "격자 밖 처리"를 판정 함수로 먼저 고정하되 `&&`로 이어 쓴다 → 이웃 합 함수는 그 판정만 믿고 네 방향을 더한다 → 메인은 최댓값 갱신 조건(`>`)과 순회 순서로 동률 규칙을 만족시킨다 → 1×1과 전부 같은 값 격자로 검산.
```

**9) 계좌 이체 시뮬레이션** · Hard

- **요구사항**: 잔액 벡터 `balance`를 여러 함수가 **참조로 공유**하며 갱신하는 시뮬레이션을 설계하라. `void deposit(vector<int>& balance, int a, int x)`는 계좌 `a`에 `x`를 입금하고, `bool transfer(vector<int>& balance, int a, int b, int x)`는 `a`의 잔액이 `x` 이상일 때만 `a`에서 `b`로 옮기고 `true`를, 부족하면 아무 변화 없이 전역 `fail_count`를 1 늘리고 `false`를 반환한다. 메인은 성공한 이체 수를 반환값으로 세고, 실패 수는 전역에서 읽는다.
- **입력**: 첫 줄에 계좌 수 `n`과 명령 수 `q`(1 ≤ n ≤ 50, 1 ≤ q ≤ 100). 둘째 줄에 초기 잔액 `n`개(0 ≤ 잔액 ≤ 10,000). 다음 `q`개 줄에 `D a x`(입금) 또는 `T a b x`(이체, `a ≠ b`). 계좌 번호는 0-based, 1 ≤ x ≤ 10,000.
- **출력**: 첫 줄에 최종 잔액 `n`개(공백 구분), 둘째 줄에 `성공한 이체 수 실패한 이체 수`.
- **예제**: `3 4 / 100 50 0 / T 0 1 30 / T 1 2 100 / D 2 5 / T 2 0 10` → `70 80 5 / 1 2` · `2 1 / 10 0 / T 0 1 10` → `0 10 / 1 0`
- **셀프체크**: 잔액이 정확히 `x`인 경우 이체가 성공하는가(`<` 와 `<=` 경계)? 실패 시 잔액이 전혀 바뀌지 않는가(빼기 전에 검사)? 두 함수 모두 `vector<int>& balance`로 참조를 받았는가 — `&`를 빠뜨리면 복사본만 바뀌어 잔액이 초기값 그대로 출력된다. 전역 `fail_count`는 `global` 같은 선언 없이 그냥 대입하면 되고, 반대로 `balance`는 전역이 아니라 **참조 인자**로 공유된다는 차이를 설명할 수 있는가? 명령의 첫 토큰을 `string`으로 읽어 `op == "D"`처럼 비교했는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int fail_count = 0;

void deposit(vector<int>& balance, int a, int x) {
    balance[a] += x;
}

bool transfer(vector<int>& balance, int a, int b, int x) {
    if (balance[a] < x) {
        fail_count++;
        return false;
    }
    balance[a] -= x;
    balance[b] += x;
    return true;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> balance(n);
    for (int i = 0; i < n; i++) cin >> balance[i];
    int ok = 0;
    for (int i = 0; i < q; i++) {
        string op;
        cin >> op;
        if (op == "D") {
            int a, x;
            cin >> a >> x;
            deposit(balance, a, x);
        } else {
            int a, b, x;
            cin >> a >> b >> x;
            if (transfer(balance, a, b, x)) ok++;
        }
    }
    for (int i = 0; i < n; i++) {
        if (i > 0) cout << ' ';
        cout << balance[i];
    }
    cout << '\n';
    cout << ok << ' ' << fail_count << '\n';
    return 0;
}
@@TESTS
--IN
3 4
100 50 0
T 0 1 30
T 1 2 100
D 2 5
T 2 0 10
--OUT
70 80 5
1 2
--IN
2 1
10 0
T 0 1 10
--OUT
0 10
1 0
--IN
2 2
0 0
D 1 3
T 1 0 4
--OUT
0 3
0 1
@@EXPL
(1) 접근·핵심 아이디어

- 세 가지 상태 전달 방식을 한 문제에서 함께 쓴다. 잔액 벡터는 **참조 인자** `vector<int>&`로 넘겨 제자리 수정, 이체 성공 여부는 `bool` 반환값으로, 실패 횟수는 전역 변수 `fail_count`로 갱신한다.
- 파이썬 버전과 결정적으로 다른 점: 파이썬은 리스트를 넘기기만 하면 자동으로 공유되지만 C++은 `&`를 명시해야 한다. `void deposit(vector<int> balance, ...)`처럼 `&`를 빠뜨리면 함수 안에서 잔액이 늘었다가 함수가 끝나며 복사본과 함께 사라지고, 최종 출력은 초기 잔액 그대로가 된다.
- 경계: "잔액이 `x` 이상이면 성공"이므로 실패 조건은 `balance[a] < x`다. `<=`로 쓰면 잔액이 딱 맞는 경우가 실패로 잘못 처리된다. 또 검사를 빼기 **전에** 해야 실패 시 잔액이 그대로 남는다.

(2) 코드 단계별

- `deposit`: `balance[a] += x`로 제자리 수정. 반환 타입은 `void`.
- `transfer`: 부족하면 `fail_count++` 후 `false` 조기 반환. 충분하면 `a`에서 빼고 `b`에 더한 뒤 `true`. 전역 변수를 쓰기 위한 별도 선언은 필요 없다.
- `main`: 명령 첫 토큰을 `string op`로 읽는다. `char`로 읽어도 되지만 명령이 여러 글자로 늘어날 때를 대비해 문자열이 안전하다. `op == "D"`면 인자 두 개, 아니면 세 개를 읽는다.
- 이체 반환값이 `true`일 때만 `ok`를 늘리고, 마지막에 잔액과 `ok fail_count`를 출력.
- 오버플로 점검: 잔액 최대 10,000, 명령 100건이라 한 계좌가 최대 100만 정도. `int`로 충분하다.

(3) 스스로 다시 짤 때 생각 순서

- 상태별로 "참조 인자 / 반환값 / 전역" 중 무엇으로 전달할지 먼저 정한다 → 컨테이너 인자에 `&`가 붙었는지 눈으로 확인 → 실패 검사를 갱신보다 앞에 두고 부등호 경계(`<`)를 확정 → 잔액이 정확히 `x`인 케이스와 잔액 0에서의 실패 케이스로 검산.
```

**10) 생성자 없는 수** · Hard

- **요구사항**: 양의 정수 `m`에 대해 `gen(m) = m + (m의 각 자릿수 제곱의 합)`을 "m이 만드는 수"라 하자. 예를 들어 `gen(12) = 12 + 1 + 4 = 17`이다. `1` 이상 `N` 이하의 수 중 **어떤 `m`으로도 만들어지지 않는 수**의 개수와, 그런 수 중 가장 작은 것과 가장 큰 것을 출력하라. 자릿수 제곱합을 반환하는 함수 `int digit_square_sum(int m)`, `gen(m)`을 반환하는 함수, 그리고 "만들어진 수" 표시 벡터를 **참조 인자**로 받아 제자리에서 표시하는 반환 없는 함수 `void mark(vector<bool>& made, int m, int N)`으로 나눠 구현한다.
- **입력**: 한 줄에 정수 `N`(1 ≤ N ≤ 5000).
- **출력**: 첫 줄에 개수, 둘째 줄에 `가장 작은 수 가장 큰 수`(공백 구분). `1`은 어떤 수로도 만들어지지 않으므로 답이 없는 경우는 없다.
- **예제**: `10` → `8 / 1 10` · `30` → `19 / 1 29`
- **셀프체크**: `gen(m)`이 `N`을 넘으면 벡터 범위를 벗어나므로 `mark`에서 `g <= N`일 때만 표시했는가(C++ `vector`의 `[]`는 범위 검사를 하지 않아 조용히 남의 메모리를 덮어쓴다)? `made`를 크기 `N + 1`로 잡아 인덱스 `N`까지 쓸 수 있는가? `mark`의 매개변수가 `vector<bool>&`(참조)인가 — `&`가 없으면 표시가 전부 사라진다? `N = 30`에서 30은 `gen(5) = 30`으로 만들어지므로 가장 큰 답이 29임을 손으로 확인했는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int digit_square_sum(int m) {
    int s = 0;
    while (m > 0) {
        int d = m % 10;
        s += d * d;
        m /= 10;
    }
    return s;
}

int gen(int m) {
    return m + digit_square_sum(m);
}

void mark(vector<bool>& made, int m, int N) {
    int g = gen(m);
    if (g <= N) made[g] = true;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int N;
    cin >> N;
    vector<bool> made(N + 1, false);
    for (int m = 1; m <= N; m++) mark(made, m, N);
    int cnt = 0, smallest = -1, largest = -1;
    for (int x = 1; x <= N; x++) {
        if (!made[x]) {
            cnt++;
            if (smallest == -1) smallest = x;
            largest = x;
        }
    }
    cout << cnt << '\n';
    cout << smallest << ' ' << largest << '\n';
    return 0;
}
@@TESTS
--IN
10
--OUT
8
1 10
--IN
30
--OUT
19
1 29
--IN
1
--OUT
1
1 1
--IN
5000
--OUT
1697
1 5000
@@EXPL
(1) 접근·핵심 아이디어

- "만들어지지 않는 수"를 직접 찾기는 어렵지만, 반대로 "만들어지는 수"는 `m = 1..N`을 돌며 `gen(m)`을 계산해 표시하면 전부 알 수 있다. 표시되지 않은 수가 답이다. `gen(m) > m`이므로 `N`보다 큰 `m`은 볼 필요가 없다.
- 세 함수의 책임: `digit_square_sum`(계산 부품, `int` 반환) → `gen`(부품 조립, `int` 반환) → `mark`(표시 벡터를 참조로 받아 제자리 수정, `void`). 메인은 이 부품들을 순서대로 호출하고 집계만 한다.
- 함정 둘: `mark`의 매개변수에 `&`가 없으면 표시가 복사본에만 남아 전부 사라진다. 그리고 `gen(m)`이 `N`을 넘을 수 있으므로 `g <= N` 검사가 없으면 벡터 범위 밖을 쓴다 — 파이썬처럼 `IndexError`가 나는 게 아니라 **조용히 남의 메모리를 덮어쓰고** 나중에 엉뚱한 곳에서 터진다.

(2) 코드 단계별

- `digit_square_sum`: `m % 10`으로 한 자리씩 떼어 제곱을 더하고 `m /= 10`으로 줄인다. `m`은 값 전달이라 안에서 부숴도 호출한 쪽 값은 그대로다 — 여기서는 그게 오히려 편하다.
- `mark(vector<bool>& made, int m, int N)`: `g = gen(m)`이 `N` 이하일 때만 `made[g] = true`. 참조로 받았으므로 반환값도 전역도 필요 없다.
- `main`: `vector<bool> made(N + 1, false)`로 인덱스 `N`까지 확보 → 모든 `m`에 `mark` → `1..N`을 훑으며 표시 안 된 수를 세고, 처음 만난 것을 `smallest`, 마지막으로 만난 것을 `largest`로 기록.
- `vector<bool>`은 비트 단위로 압축된 특수한 컨테이너라 `bool& b = made[i];`처럼 원소의 참조를 뽑을 수 없다. 여기서는 대입과 읽기만 하므로 문제없지만, 참조가 필요하면 `vector<char>`를 쓴다.
- `N = 5000`이어도 `gen` 계산은 5,000번뿐이라 즉시 끝난다.

(3) 스스로 다시 짤 때 생각 순서

- "없는 것을 세기"를 "있는 것을 표시하기"로 뒤집는다 → 계산 함수·조립 함수·표시 함수로 책임을 나눈다 → 표시 함수 매개변수에 `&`를 붙이고 벡터 크기와 `g <= N` 경계를 못 박는다 → `N = 10`을 손으로(2와 6만 만들어짐 → 8개) 검산.
```
