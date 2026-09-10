## L14. 정리 — 조건문 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터에서 배운 것을 한자리에 모은다. 새 문법은 없다. 흩어져 있던 조각이 어떻게 하나로 이어지는지 확인하고, 입문자가 실제로 넘어지는 지점을 미리 밟아 보는 자리다.

**개념 지도**

조건문의 재료는 딱 하나, **참·거짓 값**이다. 비교 연산자가 그 값을 만들고, `&&`/`||`가 여러 개를 하나로 합치고, `if` 계열 문법이 그 값을 보고 갈 길을 정한다.

```text
   +----------+  +---------------+   +----------------------------+
   |  values  |->|  comparison   |-->|  true / false              |
   |  a , b   |  |  ==  !=  >    |   |  ( this is what if reads ) |
   +----------+  |  <   >=  <=   |   +--------------+-------------+
                 +---------------+                  |
                 +---------------+                  |
                 |  &&  ||  !  ( )  |---------------+
                 |  join several    |               |
                 +------------------+               v
```

참·거짓 값 하나가 만들어지면, 그다음은 "갈래를 어떤 모양으로 놓을 것인가"만 남는다.

```text
   branch shapes                        how many run
   ---------------------------------    ----------------------------
   if                                   0 or 1
   if / else                            exactly 1
   if / else if / else                  exactly 1  (order matters)
   if  +  if   (side by side)           0 .. n
   nested if   (if inside if)           stage by stage
   switch (v) { case c: ... break; }    one case  (break or it flows)
   cond ? a : b                         picks a VALUE, not code
```

위 표의 마지막 줄만 성격이 다르다. 삼항 연산자는 "실행할 코드"가 아니라 "값"을 고른다.

C++에서 조건 자리에 놓인 값이 어떻게 읽히는지도 한 번 못박아 두자. 이 규칙이 이 챕터 함정의 절반을 설명한다.

```text
   what the condition really means in C++
   ------------------------------------------------------
   0                       ->  false
   any other number        ->  true      ( 1, -1, 7, ... )

   if (x == 5)   compare : x stays, result is true / false
   if (x = 5)    assign  : x becomes 5, then 5 -> true
                           ^ compiles fine, silently wrong
```

**뼈대 코드**

**1) 두 갈래 — 결과가 정확히 둘일 때**

```cpp
#include <iostream>
using namespace std;

int main() {
    int x;
    cin >> x;                       // 문제마다 바뀜 (입력 형태)
    if (x >= 60) {                  // 문제마다 바뀜 (가르는 기준)
        cout << "Pass" << endl;     // 문제마다 바뀜 (참일 때 할 일)
    } else {
        cout << "Fail" << endl;     // 문제마다 바뀜 (거짓일 때 할 일)
    }
    return 0;
}
```

**2) 구간 나누기 — 겹치는 범위를 순서로 푼다**

```cpp
#include <iostream>
using namespace std;

int main() {
    int score;
    cin >> score;
    if (score >= 90) {              // 큰 기준부터 내려간다
        cout << "A" << endl;
    } else if (score >= 80) {       // 여기 왔다는 건 이미 90 미만이라는 뜻
        cout << "B" << endl;
    } else if (score >= 70) {       // 기준 개수만큼 else if 를 늘린다
        cout << "C" << endl;
    } else {                        // 남은 전부
        cout << "D" << endl;
    }
    return 0;
}
```

**3) 독립 판정 여러 개 — 동시에 참일 수 있을 때**

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    if (n % 2 == 0) {               // 판정 1
        cout << "two" << endl;
    }
    if (n % 3 == 0) {               // 판정 2 (앞 결과와 무관하게 다시 검사)
        cout << "three" << endl;
    }
    return 0;
}
```

**4) 깃발 변수 — "아무것도 안 했는가"를 기억하기**

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    bool done = false;              // 아직 아무 일도 하지 않았다
    if (n % 3 == 0) {
        cout << "Fizz" << endl;
        done = true;                // 뭔가 했다고 표시
    }
    if (n % 5 == 0) {
        cout << "Buzz" << endl;
        done = true;
    }
    if (!done) {                    // 위에서 하나도 안 걸렸을 때만
        cout << n << endl;          // 문제마다 바뀜 (기본 동작)
    }
    return 0;
}
```

**5) 단계형 분기 — 통과한 것만 다시 나눌 때**

```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    if (a > 0) {                    // 1단계: 큰 갈래
        if (b > 0) {                // 2단계: 1단계를 통과한 경우에만 검사
            cout << "both" << endl;
        } else {
            cout << "only a" << endl;
        }
    } else {
        cout << "none" << endl;     // 1단계에서 떨어진 경우
    }
    return 0;
}
```

**6) 값 하나 고르기 — 삼항 연산자**

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    string label = (n % 2 == 0) ? "even" : "odd";   // 조건과 두 값만 바뀜
    cout << label << endl;
    return 0;
}
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 조건이 참일 때만 뭔가 한다 | `if` | 거짓일 때 할 일이 아예 없다 | 비교 1회 |
| 결과가 정확히 두 가지 | `if / else` | 반대 조건을 컴파일러가 만들어 준다 | 비교 1회 |
| 결과가 셋 이상, 그중 하나만 | `if / else if / else` | 위에서 처음 참인 하나만 실행 | 비교 최대 (갈래 수 − 1)회 |
| 정수·문자를 상수 여러 개와 견준다 | `switch` | 갈래가 `n == 상수` 꼴로만 이루어졌을 때 | 비교 최대 갈래 수 |
| 판정이 여러 개이고 동시에 참일 수 있다 | `if`를 나란히 | 서로 막지 않고 각각 검사 | 비교 (판정 수)회 |
| 두 조건이 동시에 참이어야 한다 | `&&` | 통과 구간의 겹치는 부분만 남긴다 | 비교 2회 |
| 둘 중 하나만 참이면 된다 | `\|\|` | 통과 구간을 합친다 | 비교 2회 |
| 양쪽이 막힌 범위(이상 그리고 이하) | `&&`로 두 경계 | 아래 경계와 위 경계는 별개 조건 | 비교 2회 |
| 통과한 대상만 다시 나눈다 | 중첩 `if` | 바깥이 거짓일 때 따로 할 일이 있다 | 단계마다 1회 |
| 값 하나만 고르면 끝난다 | 삼항 연산자 | 결과가 값이라 변수·`cout`에 바로 들어간다 | 비교 1회 |
| 구간 경계가 겹친다 | `else if` + 큰 기준부터 | 위 갈래가 상한을 대신 잘라 준다 | 비교 최대 (구간 수 − 1)회 |
| 참·거짓을 변수에 담아 둔다 | `bool` | `int` 대신 쓰면 `=`/`==` 실수를 줄인다 | 저장 1칸 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 조건이 참일 때와 거짓일 때 중괄호 `{ }` 안팎의 줄이 각각 언제 실행되는지.
- [ ] 설명할 수 있다: C++에서 소속을 정하는 것이 들여쓰기가 아니라 중괄호라는 것과, 중괄호를 생략하면 몇 줄이 묶이는지.
- [ ] 설명할 수 있다: `if / else`의 두 갈래가 절대 동시에 실행되지 않는 이유.
- [ ] 설명할 수 있다: `else if` 사슬이 "처음 참인 갈래 하나만" 실행한다는 것과, 그래서 순서가 답을 바꾼다는 것.
- [ ] 설명할 수 있다: 성적 등급을 `>=`로 쓸 때 왜 큰 점수부터 검사해야 하는지, 순서를 뒤집으면 무슨 일이 생기는지.
- [ ] 설명할 수 있다: 나란한 `if` 두 개와 `if / else if`가 어떤 입력에서 결과가 갈리는지, 예를 하나 들어서.
- [ ] 설명할 수 있다: `>=`와 `>`가 경계값에서 어떻게 다른지, 지문의 "이상·초과"가 각각 어느 쪽인지.
- [ ] 설명할 수 있다: `=`와 `==`의 역할 차이, 그리고 조건 자리에 `=`를 써도 C++가 왜 오류를 내지 않는지.
- [ ] 설명할 수 있다: 조건 자리에서 `0`은 거짓, 나머지 정수는 참이라는 규칙과 그것이 만드는 함정 하나.
- [ ] 설명할 수 있다: `&&`와 `||`의 참·거짓 표를 보지 않고 말로.
- [ ] 설명할 수 있다: `&&`가 `||`보다 먼저 계산된다는 것과, 괄호가 꼭 필요한 상황의 예 하나.
- [ ] 설명할 수 있다: 단축 평가가 무엇이고, 그것이 0으로 나누기를 어떻게 막아 주는지.
- [ ] 설명할 수 있다: 중첩 `if`와 `&&`로 합친 조건이 언제 같고 언제 다른지.
- [ ] 설명할 수 있다: 중괄호를 생략했을 때 `else`가 어느 `if`에 붙는지(dangling else).
- [ ] 설명할 수 있다: 삼항 연산자가 고르는 것이 "코드"가 아니라 "값"이라는 뜻.
- [ ] 설명할 수 있다: 어떤 조건 코드를 보고 경계 검산용 입력 세 개(기준, 기준−1, 기준+1)를 즉시 만드는 법.

**⚠️ 자주 하는 실수**

**1) `else if` 대신 `if`를 나열해 여러 갈래가 함께 실행됨**

```cpp
// ❌ 틀린 코드
int score = 95;
if (score >= 70) {
    cout << "C" << endl;
}
if (score >= 80) {
    cout << "B" << endl;
}
if (score >= 90) {
    cout << "A" << endl;
}
// 출력: C / B / A 세 줄
```

왜: 세 `if`는 서로 독립이라 앞이 참이어도 뒤가 다시 검사된다. 95는 세 조건에 모두 걸려 세 줄이 나온다. 등급을 하나만 내려면 갈래가 배타적이어야 한다.

```cpp
// ✅ 고친 코드
int score = 95;
if (score >= 90) {
    cout << "A" << endl;
} else if (score >= 80) {
    cout << "B" << endl;
} else if (score >= 70) {
    cout << "C" << endl;
}
// 출력: A 한 줄
```

**2) `else if` 사슬의 순서가 거꾸로**

```cpp
// ❌ 틀린 코드
int score = 95;
if (score >= 70) {
    cout << "C" << endl;
} else if (score >= 80) {
    cout << "B" << endl;
} else if (score >= 90) {
    cout << "A" << endl;
}
// 출력: C   (A는 영원히 나오지 않는다)
```

왜: `score >= 70`은 95에도 참이다. `else if` 사슬은 처음 참인 갈래에서 끝나므로 아래 두 줄은 도달조차 하지 못한다. 겹치는 범위는 **좁은 조건(큰 기준)부터** 써야 한다.

```cpp
// ✅ 고친 코드
int score = 95;
if (score >= 90) {
    cout << "A" << endl;
} else if (score >= 80) {
    cout << "B" << endl;
} else if (score >= 70) {
    cout << "C" << endl;
}
```

**3) 비교 자리에 `=`를 씀 — C++에서 가장 위험한 함정**

```cpp
// ❌ 틀린 코드
int n = 3;
if (n = 5) {                    // 오류가 아니다! n 에 5를 넣고 5를 조건으로 쓴다
    cout << "five" << endl;     // 언제나 출력되고, n 도 5로 바뀐다
}
// 출력: five   (n 이 3인데도)
```

왜: `=`는 값을 넣는 기호이고, 넣은 결과가 그대로 식의 값이 된다. `5`는 0이 아니므로 조건은 언제나 참이다. 컴파일러는 경고를 줄 수는 있어도 **오류로 막지 않는다.** 조건 자리에 `=`가 하나만 있으면 100% 실수라고 보면 된다.

```cpp
// ✅ 고친 코드
int n = 3;
if (n == 5) {                   // 비교는 언제나 == 두 개
    cout << "five" << endl;
}
// 출력: (없음)
```

**4) 경계값에서 `>`와 `>=`를 바꿔 씀**

```cpp
// ❌ 틀린 코드
int score = 60;
if (score > 60) {               // 지문은 "60점 이상 합격"인데 60이 빠진다
    cout << "Pass" << endl;
} else {
    cout << "Fail" << endl;
}
// 출력: Fail
```

왜: "이상"은 경계 포함이라 `>=`, "초과"가 `>`다. 지문의 두 글자가 부등호의 `=` 한 글자를 결정한다. 기준값과 기준값 ±1, 세 개를 넣어 보면 바로 드러난다.

```cpp
// ✅ 고친 코드
int score = 60;
if (score >= 60) {
    cout << "Pass" << endl;
} else {
    cout << "Fail" << endl;
}
// 출력: Pass
```

**5) `||` 양쪽에 비교식을 온전히 쓰지 않음**

```cpp
// ❌ 틀린 코드
int day = 3;
if (day == 6 || 7) {
    cout << "weekend" << endl;
}
// 출력: weekend   (평일 3인데도 나온다)
```

왜: C++는 이 식을 `(day == 6) || (7)`로 읽는다. `7`은 0이 아닌 수라 그 자체로 참 취급이므로 전체가 항상 참이 된다. 오류가 나지 않아 더 위험하다.

```cpp
// ✅ 고친 코드
int day = 3;
if (day == 6 || day == 7) {
    cout << "weekend" << endl;
} else {
    cout << "weekday" << endl;
}
// 출력: weekday
```

**6) 수학처럼 `3 < x < 7`이라고 씀**

```cpp
// ❌ 틀린 코드
int x = 100;
if (3 < x < 7) {                // (3 < 100) -> true -> 1, 그리고 1 < 7 -> 참
    cout << "between" << endl;
}
// 출력: between   (x 가 100인데도)
```

왜: 비교는 왼쪽부터 두 개씩 계산된다. 앞의 비교 결과가 `1` 또는 `0`이 되고, 그 수를 다시 `7`과 비교하므로 사실상 언제나 참이다. 범위는 조건 두 개로 나눠 `&&`로 묶는다.

```cpp
// ✅ 고친 코드
int x = 100;
if (x > 3 && x < 7) {
    cout << "between" << endl;
} else {
    cout << "out" << endl;
}
// 출력: out
```

**7) 괄호 없이 `&&`와 `||`를 섞음**

```cpp
// ❌ 틀린 코드
int x = 1;
if (x > 0 || x > 10 && x < 0) {
    cout << "hit" << endl;
}
// 의도: (x > 0 || x > 10) && x < 0  ->  아무것도 안 나와야 함
// 실제: x > 0 || (x > 10 && x < 0)  ->  hit 이 나온다
```

왜: `&&`가 `||`보다 먼저 계산된다. 사칙연산에서 `*`가 `+`보다 먼저인 것과 같다. `||` 쪽을 먼저 묶고 싶으면 직접 괄호를 쳐야 한다.

```cpp
// ✅ 고친 코드
int x = 1;
if ((x > 0 || x > 10) && x < 0) {
    cout << "hit" << endl;
}
// 아무것도 출력되지 않는다
```

**8) 중괄호를 생략해 한 줄만 조건에 묶임**

```cpp
// ❌ 틀린 코드
int score = 40;
if (score >= 60)
    cout << "Pass" << endl;
    cout << "done" << endl;     // 들여썼지만 if 와 무관하다
// 출력: done   (Pass 없이 done 만)
```

왜: C++에서 소속을 정하는 것은 들여쓰기가 아니라 중괄호다. 중괄호를 생략하면 **바로 다음 한 문장만** 조건에 묶인다. 두 번째 줄은 조건과 상관없는 독립 문장이 된다.

```cpp
// ✅ 고친 코드
int score = 40;
if (score >= 60) {
    cout << "Pass" << endl;
    cout << "done" << endl;     // 둘 다 조건 안
}
// 출력: (없음)
```

**9) `else`에 조건을 붙이거나, `else`의 짝을 놓침**

```cpp
// ❌ 틀린 코드
int n = 5;
if (n > 0) {
    cout << "plus" << endl;
} else (n < 0) {                // 컴파일 오류: else 는 조건을 받지 않는다
    cout << "minus" << endl;
}
```

왜: `else`는 "위 조건들이 전부 거짓인 나머지 전부"라서 조건을 받지 않는다. 조건을 더 걸고 싶으면 `else if`다. 그리고 중괄호를 생략하면 `else`가 가장 가까운 짝 없는 `if`에 붙어(dangling else) 뜻이 조용히 바뀐다.

```cpp
// ✅ 고친 코드
int n = 5;
if (n > 0) {
    cout << "plus" << endl;
} else if (n < 0) {
    cout << "minus" << endl;
} else {
    cout << "zero" << endl;
}
// 출력: plus
```

**10) `switch`에서 `break`를 빠뜨려 아래로 흘러내림**

```cpp
// ❌ 틀린 코드
int n = 2;
switch (n) {
    case 1: cout << "one" << endl;
    case 2: cout << "two" << endl;
    case 3: cout << "three" << endl;
    default: cout << "many" << endl;
}
// 출력: two / three / many 세 줄
```

왜: `case`는 "여기서부터 시작"이라는 표시일 뿐 "여기만"이라는 뜻이 아니다. `break`를 만나기 전까지 아래 `case`들을 그대로 통과한다(fall-through). `else if` 사슬과 달리 배타적이지 않다.

```cpp
// ✅ 고친 코드
int n = 2;
switch (n) {
    case 1: cout << "one" << endl;   break;
    case 2: cout << "two" << endl;   break;
    case 3: cout << "three" << endl; break;
    default: cout << "many" << endl;
}
// 출력: two 한 줄
```

**다음 챕터로**

조건문은 "한 번 갈라지는" 문법이다. 다음 챕터의 반복문은 같은 판단을 **여러 번** 반복하면서 값이 매번 바뀌는 상황을 다룬다. 여기서 익힌 `if`가 반복문 안으로 들어가면 "훑으면서 조건에 맞는 것만 고르기"가 되고, `&&`/`||`와 `bool` 깃발 변수는 "하나라도 있는가·모두 그런가"를 판정하는 도구로 그대로 이어진다. 중괄호로 소속을 정하는 감각도 반복문에서 그대로 다시 쓰인다.
