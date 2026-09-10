## L20. 정리 — 반복문 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터에서 배운 것을 한자리에 모은다. 새 문법은 없다. `for`와 `while`, 누적 변수, `continue`/`break`, 깃발 변수가 사실은 **하나의 뼈대**를 공유한다는 것을 확인하고, 입문자가 실제로 넘어지는 지점을 미리 밟아 보는 자리다.

**개념 지도**

반복문을 고르는 갈림길은 딱 하나다. "반복을 시작하기 전에 총 횟수를 적을 수 있는가?"

```text
   +-------------------------------------------------------+
   |  repeat the same work                                 |
   +---------------------------+---------------------------+
                               |
          can you count the passes in advance ?
                 yes |                    | no
                     v                    v
   +--------------------------+  +--------------------------+
   |  for (init; cond; step)  |  |  while (cond)            |
   |  i=0; i<n      : n times |  |  init / check / update   |
   |  i=a; i<b      : b - a   |  |  while (true) + break    |
   |  i=a; i<b; i+=s: step s  |  |  sentinel value          |
   +--------------------------+  +--------------------------+
```

둘은 같은 일을 다른 방식으로 적은 것이다. `for`가 괄호 하나에 뭉쳐 둔 세 정보가 `while`에서는 세 줄로 흩어진다.

```text
   for (int i = 1; i <= N; i++) {    int i = 1;          // start
       body                          while (i <= N) {    // stop
   }                                     body
                                         i = i + 1;      // step
                                     }
```

반복의 껍데기가 정해지면, 남는 것은 "본문에 무엇을 두는가"뿐이다.

```text
   inside the loop body
   ------------------------------------------------------------
   accumulate   int cnt = 0        ->  cnt++        // how many
                long long total = 0 -> total += x   // sum
                long long prod  = 1 -> prod *= x    // product
   filter       if (cond) { ... }  ->  only the ones that pass
   jump         continue           ->  skip the rest of THIS pass
                break              ->  leave the loop right now
   decide       bool found  = false -> true  , 'at least one'
                bool all_ok = true  -> false , 'all of them'
```

C++에서 하나 더 챙겨야 하는 것이 있다. 누적 값이 담기는 그릇의 크기다.

```text
   how big before int breaks ?     int max = 2147483647
   ------------------------------------------------------------
   sum 1..n      n = 65000    ->  about 2.1e9    borderline
   sum 1..n      n = 100000   ->  about 5.0e9    OVERFLOW
   n!            n = 12       ->  479001600      ok
   n!            n = 13       ->  6227020800     OVERFLOW
   long long     holds about 9.2e18  ( 20! is the limit )
```

**뼈대 코드**

**1) 정해진 횟수만큼 반복**

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    for (int i = 0; i < n; i++) {   // 문제마다 바뀜 (횟수)
        cout << "Hello" << endl;    // 문제마다 바뀜 (매번 할 일)
    }
    return 0;
}
```

**2) 구간 훑으며 누적하기 (합·개수·곱)**

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    long long total = 0;            // 합은 0, 곱이면 1, 개수도 0 (반복 밖!)
    for (int i = 1; i <= n; i++) {  // 문제마다 바뀜 (구간, 끝은 <=)
        total = total + i;          // 문제마다 바뀜 (+1 / +i / *i)
    }
    cout << total << endl;          // 반복이 끝난 뒤 한 번만
    return 0;
}
```

**3) 훑으면서 조건에 맞는 것만 고르기**

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int cnt = 0;
    for (int i = 1; i <= n; i++) {
        if (i % 5 == 0) {           // 문제마다 바뀜 (고르는 기준)
            cnt = cnt + 1;          // 문제마다 바뀜 (고른 것으로 할 일)
        }
    }
    cout << cnt << endl;
    return 0;
}
```

**4) 개수를 먼저 받고, 값을 하나씩 받기**

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;                       // 몇 개가 오는지
    long long total = 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;                   // 매 회차마다 하나씩 읽는다
        total = total + x;          // 문제마다 바뀜 (읽은 값으로 할 일)
    }
    cout << total << endl;
    return 0;
}
```

**5) 언제 끝날지 모를 때 — 무한 루프와 감시 값**

```cpp
#include <iostream>
using namespace std;

int main() {
    long long total = 0;
    while (true) {
        int n;
        cin >> n;
        if (n == 0) {               // 문제마다 바뀜 (종료 신호)
            break;                  // 신호 값은 처리하지 않고 빠져나온다
        }
        total = total + n;          // 문제마다 바뀜 (신호가 아닐 때 할 일)
    }
    cout << total << endl;
    return 0;
}
```

**6) 판정하기 — "하나라도" 와 "모두"**

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    bool found = false;             // '하나라도' : 없다고 가정하고 시작
    for (int i = 2; i < n; i++) {
        if (n % i == 0) {           // 문제마다 바뀜 (찾는 조건)
            found = true;
            break;                  // 하나 찾으면 결론이 나므로 멈춘다
        }
    }

    bool all_ok = true;             // '모두' : 다 만족한다고 가정하고 시작
    for (int i = 2; i < n; i++) {
        if (n % i == 0) {           // 문제마다 바뀜 (어기는 조건)
            all_ok = false;
            break;
        }
    }

    cout << (found ? "YES" : "NO") << endl;
    cout << (all_ok ? "YES" : "NO") << endl;
    return 0;
}
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 횟수를 미리 셀 수 있다 | `for` | 시작·조건·증감을 괄호 하나에 적을 수 있다 | 반복 n회 |
| 그냥 n번만 하면 된다 | `for (int i = 0; i < n; i++)` | 값이 필요 없고 횟수만 필요하다 | 반복 n회 |
| a부터 b까지 값이 필요하다 | `i = a; i <= b` | 끝값이 빠지지 않게 `<=` | 반복 (b − a + 1)회 |
| 거꾸로 내려간다 | `i = b; i >= a; i--` | 방향과 함께 부등호도 뒤집는다 | 반복 (b − a + 1)회 |
| 홀수·짝수만 훑는다 | 증감식 `i += 2` | 판별 조건 없이 시작값이 홀짝을 정한다 | 반복 약 n/2회 |
| 끝나는 시점이 입력에 달렸다 | `while` 또는 `while (true)` + `break` | 횟수를 미리 적을 수 없다 | 입력 개수에 비례 |
| 한 번은 반드시 실행해야 한다 | `while (true)` + `break` | 종료 판단을 본문 아무 자리로 옮길 수 있다 | 상황에 따라 |
| 입력이 끝날 때까지 읽는다 | `while (cin >> x)` | 더 읽을 것이 없으면 조건이 거짓이 된다 | 입력 개수에 비례 |
| 개수를 센다 | `int cnt = 0;`, `cnt++` | 조건이 참인 회차에만 1씩 | 반복 n회 |
| 값을 더한다 | `long long total = 0;`, `total += x` | 덧셈의 시작은 0, 그릇은 넉넉히 | 반복 n회 |
| 값을 곱한다 | `long long prod = 1;`, `prod *= x` | 곱셈의 시작은 1 (0이면 전부 0) | 반복 n회 |
| 특정 회차만 건너뛴다 | `continue` | 반복은 계속하고 이번 회차만 생략 | 반복 n회 |
| 찾으면 더 볼 필요가 없다 | `break` | 남은 값은 만들어지지도 않는다 | 최악 n회, 보통 더 적음 |
| "하나라도 있는가" | `bool found = false;` + `break` | 하나만 찾으면 결론이 난다 | 최악 n회 |
| "모두 그러한가" | `bool all_ok = true;` + `break` | 어기는 것 하나만 찾으면 결론이 난다 | 최악 n회 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: `for`의 세 칸(초기식·조건식·증감식)이 각각 언제 몇 번 실행되는지.
- [ ] 설명할 수 있다: `i < b`가 `b`를 포함하지 않는데도 그 규칙이 왜 편한지(회차 수 = `b - a`).
- [ ] 설명할 수 있다: `i = 0; i < n`의 마지막 값과 반복 횟수가 왜 다른지.
- [ ] 설명할 수 있다: 감소 반복에서 시작값·조건 부호·증감식 셋이 왜 함께 바뀌어야 하는지.
- [ ] 설명할 수 있다: `for`의 세 칸이 `while`의 어느 세 줄에 각각 대응되는지.
- [ ] 설명할 수 있다: `while`의 조건이 언제 검사되는지, 검사 횟수가 반복 횟수보다 왜 하나 더 많은지.
- [ ] 설명할 수 있다: 반복문 괄호 안에서 선언한 `int i`가 반복이 끝난 뒤 왜 사라지는지(스코프).
- [ ] 설명할 수 있다: 누적 변수의 선언을 반복 밖에 두어야 하는 이유를, 반복 안에 뒀을 때 나는 컴파일 오류와 함께.
- [ ] 설명할 수 있다: 합은 0, 곱은 1로 시작하는 이유와, 반복이 0번 돌 때 그 값이 왜 정답인지.
- [ ] 설명할 수 있다: `int`가 몇까지 담는지와, 합·곱을 `long long`으로 바꿔야 하는 시점.
- [ ] 설명할 수 있다: 초기화하지 않은 변수(`int total;`)를 누적에 쓰면 왜 답이 매번 달라질 수 있는지.
- [ ] 설명할 수 있다: `continue`와 `break`가 각각 어디로 점프하는지, 그림으로 그려서.
- [ ] 설명할 수 있다: `for`의 `continue`와 `while`의 `continue`가 뛰는 자리가 어떻게 다른지.
- [ ] 설명할 수 있다: `while (true)`를 안전하게 쓰는 조건("반드시 도달하는 `break`").
- [ ] 설명할 수 있다: 종료 조건을 `==`가 아니라 부등호로 써야 하는 이유.
- [ ] 설명할 수 있다: 감시 값(센티넬)이 왜 처리 대상이 아닌지.
- [ ] 설명할 수 있다: "하나라도"와 "모두"에서 깃발의 초기값이 서로 반대인 이유.
- [ ] 설명할 수 있다: 출력 줄을 반복 안(중괄호 안)에 둘 때와 밖에 둘 때 결과가 어떻게 달라지는지.

**⚠️ 자주 하는 실수**

**1) 조건을 `i < n`으로 써서 마지막 값이 빠짐**

```cpp
// ❌ 틀린 코드
int n = 5;
int total = 0;
for (int i = 1; i < n; i++) {   // 1, 2, 3, 4 까지만 (5가 빠진다)
    total = total + i;
}
cout << total << endl;
// 출력: 10   (기대한 값은 15)
```

왜: `i < n`은 `n` 바로 앞에서 멈춘다. "1부터 n까지"라는 말은 n을 포함하므로 조건을 `i <= n`으로 둬야 한다.

```cpp
// ✅ 고친 코드
int n = 5;
int total = 0;
for (int i = 1; i <= n; i++) {  // 1, 2, 3, 4, 5
    total = total + i;
}
cout << total << endl;
// 출력: 15
```

**2) 누적 변수를 반복 안에서 선언함**

```cpp
// ❌ 틀린 코드
int n = 10;
for (int i = 1; i <= n; i++) {
    int cnt = 0;                // 매 회차 새로 태어나 0으로 되돌아간다
    if (i % 2 == 0) {
        cnt = cnt + 1;
    }
}
cout << cnt << endl;
// error: 'cnt' was not declared in this scope
```

왜: 중괄호 안에서 선언한 변수는 그 블록을 벗어나는 순간 사라진다. 회차를 넘어 살아남아야 하는 변수는 반복 밖에서 만든다. C++에서는 이 실수가 컴파일 오류로 잡히니 오류 메시지가 곧 힌트다.

```cpp
// ✅ 고친 코드
int n = 10;
int cnt = 0;                    // 반복 밖(위)에서 딱 한 번
for (int i = 1; i <= n; i++) {
    if (i % 2 == 0) {
        cnt = cnt + 1;
    }
}
cout << cnt << endl;
// 출력: 5
```

**3) 누적 변수를 초기화하지 않음**

```cpp
// ❌ 틀린 코드
int total;                      // 안에 쓰레기 값이 들어 있다 (0이 아니다)
for (int i = 1; i <= 5; i++) {
    total = total + i;
}
cout << total << endl;
// 출력: 실행할 때마다 달라질 수 있다
```

왜: C++는 지역 변수를 자동으로 0으로 채워 주지 않는다. 초기값을 주지 않으면 그 자리에 남아 있던 값으로 계산이 시작된다. 오류도 경고도 없이 답만 흔들리는 가장 잡기 어려운 버그다.

```cpp
// ✅ 고친 코드
int total = 0;                  // 누적 변수는 반드시 초기값을 준다
for (int i = 1; i <= 5; i++) {
    total = total + i;
}
cout << total << endl;
// 출력: 15
```

**4) `while`에서 값을 바꾸는 줄을 빼먹어 무한 반복**

```cpp
// ❌ 틀린 코드
int n = 5;
int i = 1;
while (i <= n) {
    cout << i << endl;
    // i 를 늘리는 줄이 없다 -> 조건이 영원히 참
}
// 출력: 1 이 끝없이 반복된다
```

왜: `while`은 조건이 거짓이 될 때까지 돈다. 조건에 쓰인 변수(`i`)를 본문에서 바꾸지 않으면 조건이 절대 거짓이 되지 않는다. `while`을 쓸 때는 "무엇이 이 조건을 거짓으로 만드는가"를 한 줄로 답할 수 있어야 한다.

```cpp
// ✅ 고친 코드
int n = 5;
int i = 1;
while (i <= n) {
    cout << i << endl;
    i = i + 1;                  // 조건을 거짓으로 만드는 줄
}
```

**5) 반복문 뒤에 세미콜론을 찍음**

```cpp
// ❌ 틀린 코드
int total = 0;
for (int i = 1; i <= 5; i++);   // 세미콜론 하나 - 본문이 빈 반복문이 된다
{
    total = total + i;          // error: 'i' was not declared in this scope
}
cout << total << endl;
```

왜: `for (...);`는 "아무것도 하지 않는 문장을 5번 반복"이라는 완전한 코드다. 아래 중괄호는 반복과 무관한 그냥 블록이 되어 한 번만 실행된다. `while (cond);`이면 조건이 참인 채로 멈춰 무한 반복이 된다.

```cpp
// ✅ 고친 코드
int total = 0;
for (int i = 1; i <= 5; i++) {  // 세미콜론 없이 바로 중괄호
    total = total + i;
}
cout << total << endl;
// 출력: 15
```

**6) 감소 반복에서 방향과 부호가 어긋남**

```cpp
// ❌ 틀린 코드
int n = 5;
for (int i = n; i > 0; i++) {   // 증감이 i++ 라 값이 커지기만 한다
    cout << i << endl;
}
// 출력: 5, 6, 7, ... 끝나지 않는다
```

왜: 방향을 바꾸려면 세 자리가 함께 바뀌어야 한다. 시작값, 조건 부호, 증감식. 하나만 고치면 조건이 처음부터 거짓이라 한 번도 안 돌거나, 영원히 참이라 무한 반복이 된다.

```cpp
// ✅ 고친 코드
int n = 5;
for (int i = n; i >= 1; i--) {  // 5, 4, 3, 2, 1
    cout << i << endl;
}
```

**7) 곱을 모으는 변수를 0으로 시작함**

```cpp
// ❌ 틀린 코드
int n = 5;
int prod = 0;                   // 곱셈의 시작이 0이면
for (int i = 1; i <= n; i++) {
    prod = prod * i;            // 무엇을 곱해도 0
}
cout << prod << endl;
// 출력: 0   (기대한 값은 120)
```

왜: 초기값은 "그 연산에서 아무 영향을 주지 않는 값"이어야 한다. 덧셈은 0, 곱셈은 1이다. 이 실수는 오류 없이 답만 틀리므로 발견이 늦다.

```cpp
// ✅ 고친 코드
int n = 5;
int prod = 1;
for (int i = 1; i <= n; i++) {
    prod = prod * i;
}
cout << prod << endl;
// 출력: 120
```

**8) `int`로 누적하다 조용히 넘침**

```cpp
// ❌ 틀린 코드
int prod = 1;
for (int i = 1; i <= 13; i++) {
    prod = prod * i;            // 13! 은 int 범위(약 21억)를 넘는다
}
cout << prod << endl;
// 출력: 1932053504   (기대한 값은 6227020800)
```

왜: `int`가 담을 수 있는 한계를 넘어도 오류가 나지 않는다. 넘친 값은 잘려서 엉뚱한 수(때로는 음수)가 되고, 테스트만 조용히 틀린다. 합은 10만 개만 더해도, 곱은 13!만 되어도 넘친다.

```cpp
// ✅ 고친 코드
long long prod = 1;             // 큰 수는 처음부터 long long
for (int i = 1; i <= 13; i++) {
    prod = prod * i;
}
cout << prod << endl;
// 출력: 6227020800
```

**9) 결과 출력을 반복 안에 두어 여러 번 찍힘**

```cpp
// ❌ 틀린 코드
int n = 3;
int total = 0;
for (int i = 1; i <= n; i++) {
    total = total + i;
    cout << total << endl;      // 중괄호 안 -> 매 회차 출력
}
// 출력: 1 / 3 / 6 (세 줄)
```

왜: C++에서 소속을 정하는 것은 중괄호다. 최종 결과를 한 번만 내려면 출력 줄이 반복문의 닫는 중괄호 **밖**에 있어야 한다.

```cpp
// ✅ 고친 코드
int n = 3;
int total = 0;
for (int i = 1; i <= n; i++) {
    total = total + i;
}
cout << total << endl;          // 반복이 끝난 뒤 한 번
// 출력: 6
```

**10) `while`에서 `continue`가 증감 줄보다 위에 있음**

```cpp
// ❌ 틀린 코드
int i = 0;
while (i < 5) {
    if (i == 3) {
        continue;               // i 를 안 바꾼 채 조건 검사로 돌아간다
    }
    cout << i << endl;
    i = i + 1;
}
// i 가 3이 되는 순간 같은 회차가 영원히 반복된다
```

왜: `continue`는 이번 회차의 남은 줄을 전부 건너뛴다. `for`는 그래도 증감식이 자동으로 실행되지만, `while`은 그렇지 않다. 값을 바꾸는 줄이 아래에 있으면 실행되지 않아 조건이 영원히 그대로다.

```cpp
// ✅ 고친 코드
int i = 0;
while (i < 5) {
    i = i + 1;                  // 값을 먼저 바꿔 두고
    if (i == 3) {
        continue;               // 그다음 건너뛴다
    }
    cout << i << endl;
}
// 출력: 1 / 2 / 4 / 5
```

**11) "모두" 판정의 깃발 초기값을 뒤집어 둠**

```cpp
// ❌ 틀린 코드
int n = 3;
bool all_ok = false;            // "모두 짝수"인데 거짓으로 시작
for (int i = 0; i < n; i++) {
    int x;
    cin >> x;
    if (x % 2 != 0) {
        all_ok = true;          // 방향까지 반대로 섞였다
    }
}
cout << (all_ok ? "YES" : "NO") << endl;
// 2 4 6 을 넣어도 NO 가 나온다
```

왜: "모두 만족"은 "어기는 것이 하나도 없다"와 같은 말이다. 아직 아무것도 검사하지 않은 상태에서는 어긴 것이 하나도 없으므로 참에서 출발해야 한다. 어기는 값을 만났을 때 거짓으로 뒤집는다.

```cpp
// ✅ 고친 코드
int n = 3;
bool all_ok = true;             // 모두 만족한다고 가정하고 시작
for (int i = 0; i < n; i++) {
    int x;
    cin >> x;
    if (x % 2 != 0) {           // 어기는 값(홀수)을 만나면
        all_ok = false;
    }
}
cout << (all_ok ? "YES" : "NO") << endl;
```

**다음 챕터로**

여기까지가 "값을 하나씩 만들어 내며 훑는" 반복이다. 다음 단계에서는 반복 안에 반복을 넣어(중첩 반복) 격자나 표를 다루고, 값들을 변수 하나하나가 아니라 배열·`vector`로 모아 두는 방법을 배운다. 이 챕터의 누적 변수와 깃발 변수는 그대로 쓰이므로, `cnt`/`total`/`prod`의 초기값과 선언 위치, 그리고 `int`가 넘치는 지점을 손에 익혀 두면 그 뒤가 훨씬 수월하다.
