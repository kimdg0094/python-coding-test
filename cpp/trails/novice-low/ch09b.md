## L8. 문자 삭제

**개념**

- 문자열에서 특정 위치나 특정 문자를 "지운" 새 문자열을 만든다. C++의 `std::string`은 바꿀 수 있지만(가변), 이 레슨에서는 조각을 잘라 이어 붙이거나 한 글자씩 골라 담아 "지운 결과"를 만드는 방식으로 다룬다.

- `s.substr(pos, len)` 로 부분 문자열을 잘라낸다. `pos`부터 `len`글자를 가져오며, `len`을 생략하면 `pos`부터 끝까지다. 앞부분과 뒷부분을 이어 붙이면 가운데 한 글자를 뺄 수 있다. 인덱스 `i`의 글자를 지우려면 `s.substr(0, i) + s.substr(i + 1)` 을 쓴다.

- `s.substr(0, i)` 는 처음부터 `i`글자(즉 인덱스 0..i-1), `s.substr(i + 1)` 은 `i` 다음부터 끝까지를 뜻한다. 두 조각을 합치면 `i`번째 글자만 빠진다.

- "특정 문자를 모두 지우기"는 한 글자씩 훑으며 지울 문자가 아닌 것만 결과에 담으면 된다. `for` 순회로 직접 만든다.

- "처음 나온 하나만 지우기"는 이미 지웠는지 표시하는 `bool` 플래그를 두고, 아직 안 지웠고 대상 문자를 만나면 그때 한 번만 건너뛴다.

```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s = "apple";
    cout << s.substr(0, 1) + s.substr(2) << endl;  // index 1(p) 삭제 -> "aple"
    // "banana"에서 'a' 모두 삭제
    string t = "banana", r = "";
    for (int i = 0; i < t.size(); i++)
        if (t[i] != 'a') r = r + t[i];
    cout << r << endl;  // "bnn"
    return 0;
}
```

> 선행: 부분 문자열(`substr`)과 인덱싱 `s[i]`, `+` 연결, `s.size()` 는 앞 레슨(문자열 순회·Concat)에서 배웠다.

**문제**

**1) 가운데 글자 빼기** · Easy

- **요구사항**: 공백 없는 문자열과 정수 인덱스를 받아, 그 인덱스의 글자 하나만 지운 문자열을 출력한다.
- **입력**: 첫 줄에 문자열 `s`, 둘째 줄에 정수 `i` (0 ≤ i < s.size())
- **출력**: `i`번째 글자를 지운 문자열
- **예제**:
  - `apple` / `0` → `pple`
  - `apple` / `4` → `appl`
  - `hello` / `2` → `helo`
- **셀프체크**: 인덱스는 0부터 센다. `i`가 마지막 글자일 때 `s.substr(i + 1)` 은 빈 문자열이 되어야 정상이다(에러 아님).

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    int i;
    getline(cin, s);
    cin >> i;
    cout << s.substr(0, i) + s.substr(i + 1) << endl;
    return 0;
}
@@TESTS
--IN
apple
0
--OUT
pple
--IN
hello
2
--OUT
helo
@@EXPL
지울 인덱스 `i`를 기준으로 문자열을 두 조각으로 나눠 다시 이어 붙이는 문제다. `i`번째 글자만 빼면 되므로, `i` 앞부분과 `i` 뒷부분을 합친다.

- `getline(cin, s)` 으로 첫 줄의 문자열을, `cin >> i` 로 둘째 줄의 인덱스를 정수로 받는다.
- `s.substr(0, i)` 는 처음부터 `i`글자(인덱스 0..i-1)이므로 `i`번째 글자는 포함하지 않는다.
- `s.substr(i + 1)` 은 `i` 다음 글자부터 끝까지다(길이 생략 시 끝까지).
- 두 조각을 `+` 로 이어 붙이면 `i`번째 글자만 빠진 문자열이 된다.

스스로 다시 짤 때 생각 순서: (1) `substr`은 (시작, 길이) 규칙이라는 걸 떠올린다. (2) 남길 앞부분은 `substr(0, i)`, 남길 뒷부분은 `substr(i + 1)` 로 정한다. (3) 마지막 글자를 지울 때 `substr(i + 1)` 가 빈 문자열이 되어도 문제없이 동작하는지 머릿속으로 확인한다.
```

**2) 특정 문자 모두 지우기** · Easy

- **요구사항**: 문자열과 지울 문자 한 개를 받아, 그 문자를 전부 없앤 결과를 출력한다.
- **입력**: 첫 줄에 문자열 `s`, 둘째 줄에 지울 문자 `c`
- **출력**: `s`에서 `c`를 모두 지운 문자열
- **예제**:
  - `banana` / `a` → `bnn`
  - `mississippi` / `s` → `miiippi`
  - `hello` / `z` → `hello`
- **셀프체크**: 지울 문자가 없으면 원본이 그대로 나와야 한다. 원본을 직접 바꾸는 대신, 남길 글자만 새 문자열에 담는 방식이 안전하다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s, c;
    getline(cin, s);
    getline(cin, c);
    string result = "";
    for (int i = 0; i < s.size(); i++) {
        if (s[i] != c[0]) result = result + s[i];
    }
    cout << result << endl;
    return 0;
}
@@TESTS
--IN
banana
a
--OUT
bnn
--IN
hello
z
--OUT
hello
@@EXPL
문자열에서 특정 문자를 모두 없애는 문제다. 한 글자씩 훑으면서 지울 문자가 아닌 것만 결과에 담는다.

- `getline(cin, s)`, `getline(cin, c)` 으로 원본 문자열과 지울 문자 한 개를 받는다. `c`는 문자열이지만 첫 글자 `c[0]` 만 쓴다.
- `result` 를 빈 문자열로 두고 시작한다.
- `for` 로 `s`의 글자를 하나씩 본다. `s[i]` 가 지울 문자 `c[0]` 와 다르면 결과에 이어 붙이고, 같으면 건너뛴다. 그러면 지울 문자만 빠진다.
- 지울 문자가 없으면 모든 글자가 조건을 통과해 원본이 그대로 나온다.

스스로 다시 짤 때 생각 순서: (1) "지우기 = 남길 것만 골라 담기"라는 아이디어를 떠올린다. (2) 빈 결과 문자열을 준비한다. (3) 순회하며 대상 문자가 아닌 것만 `+` 로 이어 붙인다. (4) 원본은 건드리지 않으므로 지울 게 없으면 원본이 그대로 재구성된다.
```

**3) 처음 나온 하나만 지우기** · Medium

- **요구사항**: 문자열과 문자 한 개를 받아, 그 문자가 처음 등장하는 곳 딱 하나만 지운 결과를 출력한다. 없으면 원본을 그대로 출력한다.
- **입력**: 첫 줄에 문자열 `s`, 둘째 줄에 문자 `c`
- **출력**: `c`의 첫 등장 하나만 지운 문자열
- **예제**:
  - `banana` / `a` → `bnana`
  - `aabbcc` / `b` → `aabcc`
  - `hello` / `x` → `hello`
- **셀프체크**: "모두 지우기"와 다르게 한 번만 지운다. 이미 지웠는지 표시하는 플래그를 쓴다. 없는 문자를 줘도 에러 없이 원본이 나와야 한다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s, c;
    getline(cin, s);
    getline(cin, c);
    string result = "";
    bool removed = false;
    for (int i = 0; i < s.size(); i++) {
        if (!removed && s[i] == c[0]) {
            removed = true;
        } else {
            result = result + s[i];
        }
    }
    cout << result << endl;
    return 0;
}
@@TESTS
--IN
banana
a
--OUT
bnana
--IN
hello
x
--OUT
hello
@@EXPL
특정 문자가 처음 등장하는 곳 딱 하나만 지우는 문제다. "이미 지웠는가"를 기억하는 `bool` 플래그로 한 번만 건너뛴다.

- `getline` 으로 문자열 `s`와 지울 문자 `c`를 받는다.
- `removed` 를 `false` 로 두어 아직 지우지 않았음을 표시한다.
- `for` 로 글자를 하나씩 본다. 아직 안 지웠고(`!removed`) 지금 글자가 대상(`s[i] == c[0]`)이면, 이번 한 번만 건너뛰고 `removed = true` 로 표시한다.
- 그 외의 글자는 모두 결과에 이어 붙인다. 두 번째 이후의 같은 문자는 `removed` 가 이미 `true` 라 그대로 남는다.
- 대상 문자가 없으면 건너뛸 일이 없어 원본이 그대로 나온다.

스스로 다시 짤 때 생각 순서: (1) "모두 지우기"와 달리 개수를 1로 제한해야 함을 인식한다. (2) "한 번 했는가"를 기억할 `bool` 플래그를 둔다. (3) 아직 안 지웠고 대상 문자일 때만 건너뛰고 플래그를 켠다. (4) 나머지는 전부 결과에 담는다.
```


## L9. 문자열 밀기

**개념**

- "문자열 밀기(회전)"는 글자들을 통째로 왼쪽이나 오른쪽으로 옮기고, 밀려나간 글자를 반대편 끝으로 되돌려 붙이는 것이다.

- 왼쪽으로 한 칸 밀기: 맨 앞 글자를 떼어 맨 뒤로 보낸다. `s.substr(1) + s.substr(0, 1)`.

- 오른쪽으로 한 칸 밀기: 맨 뒤 글자를 떼어 맨 앞으로 보낸다. `n = s.size()` 일 때 `s.substr(n - 1) + s.substr(0, n - 1)`.

- `k`칸 밀기는 자를 위치를 계산해서 한 번에 나눈다. 왼쪽으로 `k`칸: `s.substr(k) + s.substr(0, k)`. 문자열 길이 `n`보다 큰 `k`는 `k % n` 으로 줄여 쓴다(한 바퀴 돌면 제자리이므로).

```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s = "abcde";
    cout << s.substr(1) + s.substr(0, 1) << endl;   // 왼쪽 1칸 -> "bcdea"
    int n = s.size();
    cout << s.substr(n - 1) + s.substr(0, n - 1) << endl;  // 오른쪽 1칸 -> "eabcd"
    int k = 2;
    cout << s.substr(k) + s.substr(0, k) << endl;   // 왼쪽 2칸 -> "cdeab"
    return 0;
}
```

> 선행: 부분 문자열(`substr`, L5 문자열 Concat에서 배움)과 나머지 연산자 `%`(Ch3), `s.size()` 를 사용한다.

**문제**

**1) 왼쪽으로 한 칸** · Easy

- **요구사항**: 공백 없는 문자열을 받아 왼쪽으로 한 칸 민 결과를 출력한다.
- **입력**: 한 줄에 문자열 `s` (길이 1 이상)
- **출력**: 왼쪽으로 한 칸 민 문자열
- **예제**:
  - `abcde` → `bcdea`
  - `hello` → `elloh`
  - `x` → `x`
- **셀프체크**: 길이가 1이면 밀어도 그대로다. 맨 앞 글자가 맨 뒤로 갔는지 확인한다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    cout << s.substr(1) + s.substr(0, 1) << endl;
    return 0;
}
@@TESTS
--IN
abcde
--OUT
bcdea
--IN
x
--OUT
x
@@EXPL
문자열을 왼쪽으로 한 칸 미는 문제다. 맨 앞 글자를 떼어 맨 뒤로 옮기면 된다.

- `getline(cin, s)` 으로 문자열을 받는다.
- `s.substr(1)` 은 두 번째 글자부터 끝까지(맨 앞 글자를 뺀 나머지)다.
- `s.substr(0, 1)` 은 맨 앞 글자 하나다.
- 이 둘을 `s.substr(1) + s.substr(0, 1)` 순서로 이어 붙이면 앞 글자가 맨 뒤로 간 결과가 된다.

스스로 다시 짤 때 생각 순서: (1) 왼쪽 밀기는 "앞 글자를 뒤로 보내기"임을 떠올린다. (2) 남길 뒷부분은 `substr(1)`, 뒤로 보낼 앞 글자는 `substr(0, 1)` 로 잘라낸다. (3) 뒷부분 + 앞 글자 순서로 합친다. 길이가 1이면 `substr(1)` 이 빈 문자열이라 원본 그대로 나오는 것도 확인한다.
```

**2) 오른쪽으로 K칸** · Medium

- **요구사항**: 문자열과 정수 `k`를 받아 오른쪽으로 `k`칸 민 결과를 출력한다.
- **입력**: 첫 줄에 문자열 `s`, 둘째 줄에 정수 `k` (0 ≤ k)
- **출력**: 오른쪽으로 `k`칸 민 문자열
- **예제**:
  - `abcde` / `1` → `eabcd`
  - `abcde` / `2` → `deabc`
  - `abcde` / `0` → `abcde`
- **셀프체크**: 오른쪽 `k`칸은 왼쪽 `n-k`칸과 같다. `k`가 0일 때 원본이 그대로 나오는지 확인한다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    int k;
    getline(cin, s);
    cin >> k;
    int n = s.size();
    k = k % n;
    cout << s.substr(n - k) + s.substr(0, n - k) << endl;
    return 0;
}
@@TESTS
--IN
abcde
1
--OUT
eabcd
--IN
abcde
0
--OUT
abcde
@@EXPL
문자열을 오른쪽으로 `k`칸 미는 문제다. 오른쪽으로 `k`칸 미는 것은 뒤쪽 `k`글자를 통째로 앞으로 가져오는 것과 같다.

- `getline` 으로 문자열을, `cin >> k` 로 이동 칸 수를 받는다.
- `n = s.size()` 로 길이를 구하고, `k = k % n` 으로 `k`를 길이 범위 안으로 줄인다(한 바퀴 돌면 제자리이므로).
- `s.substr(n - k)` 는 뒤쪽 `k`글자, `s.substr(0, n - k)` 는 그 앞부분이다. `뒤쪽 + 앞부분` 순서로 이어 붙이면 오른쪽으로 `k`칸 민 결과가 된다.
- `k`가 0이면 `s.substr(n)` 은 빈 문자열, `s.substr(0, n)` 은 원본 전체라 원본이 그대로 나온다.

스스로 다시 짤 때 생각 순서: (1) 오른쪽 밀기는 "뒤 글자들을 앞으로"라고 정리한다. (2) 가져올 뒤쪽 글자 수가 `k`이므로 자르는 기준은 `n-k` 위치다. (3) `substr(n - k)`(뒤)와 `substr(0, n - k)`(앞)를 뒤·앞 순서로 합친다. (4) `k`가 커도 안전하게 `k % n` 을 먼저 적용한다.
```

**3) 한 바퀴 넘게 밀기** · Hard

- **요구사항**: 문자열과 정수 `k`를 받아 왼쪽으로 `k`칸 민 결과를 출력한다. 단 `k`가 문자열 길이보다 클 수 있다.
- **입력**: 첫 줄에 문자열 `s`, 둘째 줄에 정수 `k` (0 ≤ k, 매우 클 수 있음)
- **출력**: 왼쪽으로 `k`칸 민 문자열
- **예제**:
  - `abcde` / `7` → `cdeab`
  - `abcde` / `5` → `abcde`
  - `abcde` / `12` → `cdeab`
- **셀프체크**: 길이가 `n`이면 `n`칸 밀 때마다 제자리로 돌아온다. `k`를 `k % n` 으로 줄여서 다뤄야 큰 값에서도 정확하다. (`k`가 `n`의 배수면 원본 그대로)

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    int k;
    getline(cin, s);
    cin >> k;
    int n = s.size();
    k = k % n;
    cout << s.substr(k) + s.substr(0, k) << endl;
    return 0;
}
@@TESTS
--IN
abcde
7
--OUT
cdeab
--IN
abcde
5
--OUT
abcde
@@EXPL
왼쪽으로 `k`칸 미는데, `k`가 문자열 길이보다 클 수 있는 문제다. 핵심은 큰 `k`를 나머지 연산으로 줄이는 것이다.

- `getline` 으로 문자열을, `cin >> k` 로 이동 칸 수를 받는다.
- `n = s.size()` 로 길이를 구한다. `n`칸을 밀면 제자리로 돌아오므로, 실제 이동은 `k = k % n` 만큼이면 충분하다.
- 왼쪽으로 `k`칸: 앞쪽 `k`글자를 떼어 뒤로 보낸다. `s.substr(k)`(앞 `k`글자 제외한 나머지) + `s.substr(0, k)`(떼어낸 앞 `k`글자).
- 예: `k=7`, `n=5` 이면 `7 % 5 = 2` 라 왼쪽 2칸과 같다.

스스로 다시 짤 때 생각 순서: (1) `n`칸마다 원래대로 돌아온다는 주기성을 떠올린다. (2) 그래서 `k`를 `k % n` 으로 먼저 줄인다. (3) 왼쪽 밀기는 `s.substr(k) + s.substr(0, k)` 로 앞부분을 뒤로 보낸다. (4) `k`가 `n`의 배수면 `k % n` 이 0이 되어 원본이 그대로 나온다.
```


## L10. 아스키 코드

**개념**

- 컴퓨터는 문자를 숫자로 저장한다. 각 문자에 정해진 번호를 아스키 코드(ASCII)라고 한다.

- C++에서 `char` 는 사실상 작은 정수다. `(int)문자` 로 캐스팅하면 그 문자의 아스키 코드(정수)를 얻는다. 예: `(int)'A'` 는 `65`, `(int)'a'` 는 `97`.

- 반대로 `(char)정수` 로 캐스팅하면 아스키 코드에 해당하는 문자가 된다. 예: `(char)66` 은 `'B'`.

- 알아두면 좋은 기준값: `'A'`=65 ~ `'Z'`=90, `'a'`=97 ~ `'z'`=122, `'0'`=48 ~ `'9'`=57. 대문자와 소문자는 정확히 32 차이가 난다.

- 같은 종류의 글자는 순서대로 번호가 이어진다. `char` 끼리 빼면 정수 차이가 나오므로 `'c' - 'a'` 는 `'a'`부터 몇 칸 떨어졌는지(=2)를 알려준다.

```cpp
#include <iostream>
using namespace std;
int main() {
    cout << (int)'A' << endl;         // 65
    cout << (char)97 << endl;         // 'a'
    cout << 'c' - 'a' << endl;        // 2
    cout << (char)('a' + 3) << endl;  // 'a'에서 3칸 뒤 -> 'd'
    return 0;
}
```

> 선행: 정수 사칙연산(Ch3)과 반복문으로 문자열을 순회(L4)하는 방법을 사용한다. `char` 를 `cout` 으로 내면 문자로, `(int)` 로 캐스팅해 내면 숫자로 출력된다는 차이에 유의한다.

**문제**

**1) 코드로 바꾸기** · Easy

- **요구사항**: 대문자 한 글자를 받아 그 아스키 코드를 출력한다.
- **입력**: 한 줄에 대문자 한 글자
- **출력**: 그 글자의 아스키 코드(정수)
- **예제**:
  - `A` → `65`
  - `Z` → `90`
  - `C` → `67`
- **셀프체크**: 출력은 숫자여야 한다. `char` 를 그냥 `cout` 하면 글자가 나오므로, 반드시 `(int)` 로 캐스팅해 정수로 출력한다.

```runner
@@SOLUTION
#include <iostream>
using namespace std;
int main() {
    char c;
    cin >> c;
    cout << (int)c << endl;
    return 0;
}
@@TESTS
--IN
A
--OUT
65
--IN
Z
--OUT
90
@@EXPL
문자 한 개의 아스키 코드를 그대로 출력하는 문제다. `char` 를 정수로 캐스팅하면 코드 값이 된다.

- `char c;` 를 두고 `cin >> c` 로 대문자 한 글자를 받는다.
- `(int)c` 는 그 글자의 아스키 코드(정수)다. 예: `(int)'A'` 는 65.
- `cout` 으로 정수를 출력하면 글자가 아니라 숫자로 나온다. 캐스팅 없이 `cout << c` 하면 문자 `A` 가 그대로 나오니 주의한다.

스스로 다시 짤 때 생각 순서: (1) "문자 -> 코드"는 `(int)` 캐스팅임을 떠올린다. (2) 입력받은 `char` 를 `(int)` 로 바꾼다. (3) 정수로 출력해야 숫자가 나온다는 점을 확인한다.
```

**2) 순서 번호 매기기** · Medium

- **요구사항**: 소문자 한 글자를 받아, 그 글자가 알파벳에서 몇 번째인지(a=1, b=2, …, z=26) 출력한다.
- **입력**: 한 줄에 소문자 한 글자
- **출력**: 알파벳 순서 번호(정수)
- **예제**:
  - `a` → `1`
  - `c` → `3`
  - `z` → `26`
- **셀프체크**: `c - 'a'` 는 0부터 시작하므로 1을 더해야 한다. 기준을 `'a'` 로 맞췄는지 확인한다.

```runner
@@SOLUTION
#include <iostream>
using namespace std;
int main() {
    char c;
    cin >> c;
    cout << (int)c - (int)'a' + 1 << endl;
    return 0;
}
@@TESTS
--IN
a
--OUT
1
--IN
z
--OUT
26
@@EXPL
소문자가 알파벳에서 몇 번째인지(a=1 … z=26) 구하는 문제다. 기준 글자 `'a'` 와의 코드 차이를 이용한다.

- `cin >> c` 로 소문자 한 글자를 받는다.
- 소문자는 코드가 순서대로 이어지므로 `(int)c - (int)'a'` 는 `'a'`부터 몇 칸 떨어졌는지를 준다. `'a'` 면 0, `'b'` 면 1 …
- 순서는 1부터 세므로 여기에 `+ 1` 을 해서 `a=1`, `z=26` 으로 맞춘다. (`char` 끼리 빼면 정수가 되므로 `c - 'a' + 1` 로도 같은 결과다.)

스스로 다시 짤 때 생각 순서: (1) "몇 번째"는 기준으로부터의 거리 문제임을 인식한다. (2) 기준은 `'a'`, 거리는 `c - 'a'` 다. (3) 이 값이 0부터 시작하니, 1부터 세는 순서 번호로 맞추려고 1을 더한다.
```

**3) 문자열 코드 합** · Medium

- **요구사항**: 공백 없는 문자열을 받아, 모든 글자의 아스키 코드를 더한 값을 출력한다.
- **입력**: 한 줄에 문자열 `s` (길이 1 이상)
- **출력**: 아스키 코드의 총합(정수)
- **예제**:
  - `ABC` → `198`  (65+66+67)
  - `abc` → `294`  (97+98+99)
  - `Z` → `90`
- **셀프체크**: 문자열을 한 글자씩 돌며 `(int)` 값을 합 변수에 더한다. 대문자와 소문자를 섞으면 값이 달라진다(같은 글자라도 코드가 다름).

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    int total = 0;
    for (int i = 0; i < s.size(); i++) {
        total = total + (int)s[i];
    }
    cout << total << endl;
    return 0;
}
@@TESTS
--IN
ABC
--OUT
198
--IN
Z
--OUT
90
@@EXPL
문자열 안 모든 글자의 아스키 코드를 더하는 문제다. 한 글자씩 돌면서 코드를 누적한다.

- `getline(cin, s)` 으로 문자열을 받는다.
- `total = 0` 으로 합을 담을 변수를 준비한다.
- `for` 로 인덱스 `i`를 0부터 `s.size()` 전까지 돌며 `s[i]` 를 하나씩 본다. 각 글자마다 `total = total + (int)s[i]` 로 그 글자의 코드를 더한다.
- 반복이 끝나면 `total` 에 모든 코드의 합이 들어 있으므로 출력한다.

스스로 다시 짤 때 생각 순서: (1) "총합"이므로 0으로 시작하는 누적 변수를 떠올린다. (2) 문자열을 `for` 로 인덱스 순회하며 글자를 하나씩 본다. (3) 각 글자를 `(int)` 로 코드로 바꿔 누적 변수에 더한다. (4) 순회가 끝난 뒤 누적 변수를 출력한다.
```


## L11. 대소문자 변환

**개념**

- C++ 기초 도구로는 문자열을 한 글자씩 돌며 직접 바꾼다. 소문자→대문자는 아스키 코드에서 32를 빼고(`c - 32`), 대문자→소문자는 32를 더한다(`c + 32`). 대·소문자 코드 차이가 정확히 32이기 때문이다.

- 알파벳이 아닌 글자(숫자, 공백, 기호)는 그대로 둔다. 이미 대문자인 글자를 또 바꾸지 않으려면, 바꿀 때 "소문자 범위인지"를 먼저 검사한다.

- 소문자인지 검사: `'a' <= c && c <= 'z'`. 대문자인지 검사: `'A' <= c && c <= 'Z'`. `char` 는 정수처럼 비교할 수 있어 범위 판별이 그대로 된다.

- 대소문자 뒤집기는 소문자면 32를 빼고, 대문자면 32를 더하고, 나머지는 그대로 두면 된다.

```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s = "Hello, World! 7";
    for (int i = 0; i < s.size(); i++)
        if ('a' <= s[i] && s[i] <= 'z') s[i] = s[i] - 32;  // 소문자 -> 대문자
    cout << s << endl;                 // "HELLO, WORLD! 7"
    cout << (char)('a' - 32) << endl;  // 'A'
    return 0;
}
```

> 선행: 아스키 코드 캐스팅(L10), 조건문(Ch4), 문자열 순회(L4)를 함께 쓴다. `char` 는 정수처럼 비교되므로 `'a' <= c && c <= 'z'` 로 소문자인지 검사할 수 있다.

**문제**

**1) 전부 대문자로** · Easy

- **요구사항**: 문자열을 받아 모두 대문자로 바꿔 출력한다.
- **입력**: 한 줄에 문자열 `s`(공백 포함 가능)
- **출력**: 모두 대문자로 바꾼 문자열
- **예제**:
  - `Hello World` → `HELLO WORLD`
  - `abc123` → `ABC123`
  - `PYTHON` → `PYTHON`
- **셀프체크**: 숫자·공백은 그대로 유지되어야 한다. 소문자만 32를 빼고, 이미 대문자인 부분은 건드리지 않는다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    for (int i = 0; i < s.size(); i++) {
        if ('a' <= s[i] && s[i] <= 'z') s[i] = s[i] - 32;
    }
    cout << s << endl;
    return 0;
}
@@TESTS
--IN
Hello World
--OUT
HELLO WORLD
--IN
abc123
--OUT
ABC123
@@EXPL
문자열을 전부 대문자로 바꾸는 문제다. 소문자만 골라 코드에서 32를 빼면 대문자가 된다.

- `getline(cin, s)` 으로 공백이 포함될 수 있는 문자열을 받는다.
- `for` 로 글자를 하나씩 보며 `'a' <= s[i] && s[i] <= 'z'` 로 소문자인지 검사한다.
- 소문자면 `s[i] = s[i] - 32` 로 대문자로 바꾼다(코드 차이가 32이므로).
- 소문자가 아닌 글자(숫자·공백·이미 대문자)는 조건을 통과하지 못해 그대로 남는다. 그래서 `abc123` -> `ABC123` 처럼 숫자는 유지된다.

스스로 다시 짤 때 생각 순서: (1) "전부 대문자"는 소문자만 32를 빼는 것임을 떠올린다. (2) 순회하며 소문자 범위인지 검사한다. (3) 소문자면 -32, 아니면 그대로 둔다. (4) 원본 문자열을 직접 고친 뒤 출력한다.
```

**2) 대소문자 뒤집기** · Medium

- **요구사항**: 문자열을 받아 대문자는 소문자로, 소문자는 대문자로 서로 바꿔 출력한다.
- **입력**: 한 줄에 문자열 `s`(공백 포함 가능)
- **출력**: 대소문자를 뒤바꾼 문자열
- **예제**:
  - `Hello` → `hELLO`
  - `aBcD` → `AbCd`
  - `Python 3` → `pYTHON 3`
- **셀프체크**: 알파벳이 아닌 글자(공백·숫자)는 그대로 두어야 한다. 소문자면 32를 빼고, 대문자면 32를 더한다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    for (int i = 0; i < s.size(); i++) {
        if ('a' <= s[i] && s[i] <= 'z') s[i] = s[i] - 32;
        else if ('A' <= s[i] && s[i] <= 'Z') s[i] = s[i] + 32;
    }
    cout << s << endl;
    return 0;
}
@@TESTS
--IN
Hello
--OUT
hELLO
--IN
Python 3
--OUT
pYTHON 3
@@EXPL
대문자는 소문자로, 소문자는 대문자로 서로 뒤바꾸는 문제다. 각 글자의 종류를 판별해 32를 빼거나 더한다.

- `getline(cin, s)` 으로 문자열을 받는다.
- `for` 로 글자를 하나씩 보며 두 경우로 나눈다.
- 소문자(`'a' <= s[i] && s[i] <= 'z'`)면 `s[i] - 32` 로 대문자로 바꾼다.
- 그렇지 않고 대문자(`'A' <= s[i] && s[i] <= 'Z'`)면 `s[i] + 32` 로 소문자로 바꾼다.
- 두 조건에 모두 해당하지 않는 글자(공백·숫자)는 손대지 않아 그대로 남는다. `Python 3` -> `pYTHON 3`.

스스로 다시 짤 때 생각 순서: (1) "서로 뒤바꾸기"는 소문자·대문자 두 경우를 각각 처리해야 함을 인식한다. (2) 소문자면 -32, 대문자면 +32 임을 떠올린다. (3) `if / else if` 로 둘을 구분하고, 나머지는 건드리지 않는다. (4) 원본을 고쳐 출력한다.
```

**3) 아스키로 직접 바꾸기** · Hard

- **요구사항**: 표준 라이브러리 변환 함수를 쓰지 않고, 아스키 코드와 조건문만으로 문자열의 소문자를 대문자로 바꿔 출력한다. 소문자가 아닌 글자는 그대로 둔다.
- **입력**: 한 줄에 문자열 `s`(공백 포함 가능)
- **출력**: 소문자만 대문자로 바꾼 문자열
- **예제**:
  - `abc XYZ` → `ABC XYZ`
  - `Hello 7` → `HELLO 7`
  - `12ab` → `12AB`
- **셀프체크**: 소문자인지 판별하려면 `'a' <= c && c <= 'z'` 를 확인한다. 소문자면 코드에서 32를 빼고, 아니면 원래 글자를 그대로 이어 붙인다. 대문자를 실수로 또 바꾸면 안 된다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    string result = "";
    for (int i = 0; i < s.size(); i++) {
        char c = s[i];
        if ('a' <= c && c <= 'z') {
            result = result + (char)(c - 32);
        } else {
            result = result + c;
        }
    }
    cout << result << endl;
    return 0;
}
@@TESTS
--IN
abc XYZ
--OUT
ABC XYZ
--IN
12ab
--OUT
12AB
@@EXPL
편의 함수 없이 아스키 코드만으로 소문자를 대문자로 바꾸는 문제다. 소문자와 대문자의 코드 차이가 정확히 32라는 사실을 쓴다.

- `getline(cin, s)` 으로 문자열을, `result = ""` 로 결과를 담을 빈 문자열을 준비한다.
- `for` 로 글자를 하나씩 꺼내 `char c` 에 담는다.
- `if ('a' <= c && c <= 'z')` 로 소문자인지 판별한다. 소문자면 코드에서 32를 빼야 대문자가 되므로 `(char)(c - 32)` 를 이어 붙인다. `(char)` 캐스팅을 해야 정수가 아니라 문자로 붙는다.
- 소문자가 아니면(대문자·숫자·공백) 바꾸지 않고 원래 글자 `c`를 그대로 이어 붙인다.

스스로 다시 짤 때 생각 순서: (1) 글자마다 다르게 처리해야 하니 순회 + 조건이 필요함을 인식한다. (2) 소문자 판별은 `'a' <= c && c <= 'z'` 비교로 한다. (3) 소문자->대문자는 코드 -32(`(char)(c - 32)`)임을 떠올린다. (4) 아닌 글자는 손대지 않고 그대로 이어 붙여, 대문자를 또 바꾸는 실수를 피한다.
```


## L12. 문자열을 정수로 변환하기

**개념**

- 사용자 입력이나 숫자 모양의 문자열은 그냥은 계산할 수 없다. `"12"` 는 글자들일 뿐이라 `string` 끼리 `+` 하면 `"12" + "3"` 은 `"123"`(이어붙이기)이 된다.

- C++에서 숫자를 계산으로 다루려면 정수 변수로 받으면 된다. `int a; cin >> a;` 처럼 하면 입력의 숫자 문자열을 자동으로 정수로 읽어 준다. 음수 부호(`-7`)도 인식하고, 앞의 공백은 건너뛴다.

- 이미 `string` 으로 들고 있는 값을 정수로 바꾸려면 `stoi(문자열)` 를 쓴다. 예: `stoi("12") + 3` 은 `15`. `stoi("007")` 은 `7`(앞의 0은 사라짐).

- 한 글자 숫자 문자를 그 값으로 바꾸는 다른 방법도 있다: `'7' - '0'` 는 `7`. `'0'`=48부터 순서대로이기 때문이다. 문자열의 각 자리 숫자를 다룰 때 유용하다.

```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
    cout << stoi("12") + 3 << endl;   // 15
    cout << stoi("-7") << endl;       // -7
    string a = "12", b = "3";
    cout << a + b << endl;            // "123"  (변환 안 하면 이어붙이기)
    cout << '7' - '0' << endl;        // 7
    return 0;
}
```

> 선행: 앞서 배운 아스키 코드(L10)와 정수 연산(Ch3)을 함께 활용한다. `#include <string>` 을 하면 `stoi`, `to_string` 을 쓸 수 있다.

**문제**

**1) 두 수의 합** · Easy

- **요구사항**: 숫자 모양의 입력 두 개를 받아 정수로 합을 출력한다.
- **입력**: 두 줄에 각각 숫자 `a`, `b`
- **출력**: 두 수의 합(정수)
- **예제**:
  - `12` / `3` → `15`
  - `100` / `200` → `300`
  - `-5` / `8` → `3`
- **셀프체크**: 정수 변수로 받으면 자동으로 숫자로 계산된다. 음수 부호가 있는 입력도 올바르게 계산되는지 확인한다.

```runner
@@SOLUTION
#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}
@@TESTS
--IN
12
3
--OUT
15
--IN
-5
8
--OUT
3
@@EXPL
숫자 모양의 입력 두 개를 진짜 숫자로 받아 더하는 문제다. `int` 로 받으면 문자열이 아니라 정수로 읽혀 산술 합이 된다.

- `int a, b;` 로 정수 변수 두 개를 두고 `cin >> a >> b` 로 입력을 받는다. `cin >>` 은 공백·줄바꿈으로 값을 구분하므로 두 줄에 나눠 있어도 각각 읽힌다.
- `a + b` 는 두 정수의 산술 합이다. 만약 `string` 으로 받아 `+` 했다면 `"12" + "3"` = `"123"` 처럼 글자가 이어붙었을 것이다.
- `cin >> int` 는 음수 부호도 인식하므로 `-5` 도 올바른 정수 -5가 된다.

스스로 다시 짤 때 생각 순서: (1) 계산하려면 문자열이 아니라 정수로 받아야 함을 떠올린다. (2) `int` 변수에 `cin >>` 로 값을 넣는다. (3) 정수끼리 `+` 로 더해 출력한다.
```

**2) 각 자리 숫자의 합** · Medium

- **요구사항**: 숫자로만 이루어진 문자열을 받아, 각 자리 숫자를 모두 더한 값을 출력한다.
- **입력**: 한 줄에 숫자 문자열 `s`(길이 1 이상, 음수 부호 없음)
- **출력**: 자릿수들의 합(정수)
- **예제**:
  - `123` → `6`
  - `9999` → `36`
  - `7` → `7`
- **셀프체크**: 문자열을 한 글자씩 돌며 각 글자를 숫자로 바꿔 더한다. `s[i] - '0'` 로 한 글자를 그 값(0~9)으로 만든다. 전체를 한 번에 `stoi` 하는 것과 헷갈리지 않는다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    int total = 0;
    for (int i = 0; i < s.size(); i++) {
        total = total + (s[i] - '0');
    }
    cout << total << endl;
    return 0;
}
@@TESTS
--IN
123
--OUT
6
--IN
9999
--OUT
36
@@EXPL
숫자 문자열의 각 자리 숫자를 모두 더하는 문제다. 전체를 하나의 수로 보는 게 아니라 글자를 하나씩 떼어 더하는 것이 핵심이다.

- `getline(cin, s)` 으로 숫자 문자열을 받고, `total = 0` 으로 합 변수를 준비한다.
- `for` 로 글자를 한 개씩 본다. 각 글자 `s[i]` 는 `'1'`, `'2'` 같은 문자다.
- `s[i] - '0'` 로 그 한 글자를 정수 값(0~9)으로 바꿔 `total` 에 더한다. `'0'`부터 코드가 순서대로라 문자에서 `'0'` 을 빼면 그 자릿값이 된다.
- 모든 글자를 더하면 자릿수 합이 된다. `123` -> 1+2+3 = 6.

스스로 다시 짤 때 생각 순서: (1) "자릿수 합"이니 전체를 한 번에 `stoi` 하지 말고 글자별로 봐야 함을 인식한다. (2) 0으로 시작하는 누적 변수를 둔다. (3) 문자열을 순회하며 각 글자를 `s[i] - '0'` 로 바꿔 누적한다. (4) 순회 후 누적 변수를 출력한다.
```

**3) 앞의 0 무시** · Medium

- **요구사항**: 앞자리에 0이 붙어 있을 수 있는 숫자 문자열을 받아, 그 수에 1을 더한 값을 출력한다.
- **입력**: 한 줄에 숫자 문자열 `s`
- **출력**: 정수로 바꾼 값 + 1
- **예제**:
  - `007` → `8`
  - `0100` → `101`
  - `0` → `1`
- **셀프체크**: `stoi("007")` 은 `7`이 된다(앞의 0은 사라짐). 출력은 정수라서 `007` 같은 형태가 남지 않는다. 결과가 문자열이 아닌 숫자로 나오는지 확인한다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    int n = stoi(s);
    cout << n + 1 << endl;
    return 0;
}
@@TESTS
--IN
007
--OUT
8
--IN
0100
--OUT
101
@@EXPL
앞에 0이 붙은 숫자 문자열을 정수로 바꾼 뒤 1을 더하는 문제다. `stoi` 로 바꾸면 앞자리 0이 자연히 사라진다는 점이 핵심이다.

- `getline(cin, s)` 으로 `007` 처럼 앞에 0이 있을 수 있는 문자열을 받는다.
- `stoi(s)` 는 이 문자열을 정수로 바꾼다. 정수에는 의미 없는 앞자리 0이 없으므로 `007` -> 7, `0100` -> 100 이 된다.
- 여기에 `+ 1` 을 해서 출력한다. 결과는 정수라 `008` 같은 형태가 아니라 `8` 로 나온다.

스스로 다시 짤 때 생각 순서: (1) 앞자리 0 문제는 정수로 바꾸면 저절로 해결됨을 떠올린다. (2) `stoi(s)` 로 변환한다. (3) 요구대로 1을 더해 출력하면, 정수라서 앞의 0이 남지 않는다.
```


## L13. 정수를 문자열로 변환하기

**개념**

- 숫자를 문자열처럼 다루고 싶을 때(글자 수 세기, 이어붙이기, 뒤집기 등) `to_string(정수)` 로 문자열로 바꾼다. 예: `to_string(123)` 은 `"123"`.

- 문자열로 바꾸면 인덱싱·`substr`·`size()`·`+` 이어붙이기 같은 문자열 도구를 그대로 쓸 수 있다. 예: `to_string(12345).size()` 는 `5`(자릿수).

- 정수와 `string` 은 `+` 로 바로 합칠 수 없다. `"번호: " + 7` 은 뜻이 달라지거나 에러이고, `"번호: " + to_string(7)` 은 `"번호: 7"` 이 된다.

- 음수도 부호까지 문자열이 된다: `to_string(-7)` 은 `"-7"` (맨 앞 글자가 `'-'`).

```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
    cout << to_string(123) + to_string(45) << endl;   // "12345"
    cout << to_string(9999).size() << endl;           // 4  (자릿수)
    cout << string("점수: ") + to_string(90) << endl; // "점수: 90"
    return 0;
}
```

> 선행: 인덱싱·`substr`·역순 순회는 L5(문자열 Concat)에서, `size()`는 문자열 순회에서, `+` 이어붙이기는 Concat에서 배웠다. `to_string` 은 `#include <string>` 이 필요하다.

**문제**

**1) 자릿수 세기** · Easy

- **요구사항**: 정수를 받아 그 수가 몇 자리인지 출력한다.
- **입력**: 한 줄에 정수 `n` (0 이상)
- **출력**: 자릿수(정수)
- **예제**:
  - `12345` → `5`
  - `7` → `1`
  - `1000` → `4`
- **셀프체크**: `to_string(n)` 으로 바꾼 뒤 `size()` 를 쓴다. `0`은 한 자리다. 나눗셈으로 세지 않아도 문자열 길이로 간단히 구할 수 있다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    int n;
    cin >> n;
    string s = to_string(n);
    cout << s.size() << endl;
    return 0;
}
@@TESTS
--IN
12345
--OUT
5
--IN
1000
--OUT
4
@@EXPL
정수가 몇 자리인지 구하는 문제다. 숫자를 문자열로 바꾸면 자릿수가 곧 문자열의 길이가 된다.

- `cin >> n` 으로 정수를 받는다.
- `to_string(n)` 은 그 정수를 문자열로 바꾼다. 예: 12345 -> `"12345"`.
- `s.size()` 는 문자열의 글자 수를 세므로, 이것이 곧 자릿수다. `12345` -> 5, `1000` -> 4.

스스로 다시 짤 때 생각 순서: (1) "자릿수 = 글자 수"라는 아이디어를 떠올린다. (2) 숫자를 `to_string` 으로 문자열로 바꾼다. (3) `size()` 로 길이를 재서 출력한다. 나눗셈으로 하나씩 세지 않아도 된다.
```

**2) 두 수 이어붙이기** · Medium

- **요구사항**: 정수 두 개를 받아 그대로 이어 붙인 문자열을 출력한다(더하는 것이 아님).
- **입력**: 두 줄에 각각 정수 `a`, `b`
- **출력**: 두 수를 이어 붙인 문자열
- **예제**:
  - `12` / `34` → `1234`
  - `7` / `100` → `7100`
  - `0` / `5` → `05`
- **셀프체크**: 더하기(`+` 산술)와 이어붙이기(문자열 `+`)는 다르다. `12`와 `34`를 더하면 `46`이지만 이어붙이면 `1234`다. 각 정수를 먼저 `to_string` 으로 바꿔야 한다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << to_string(a) + to_string(b) << endl;
    return 0;
}
@@TESTS
--IN
12
34
--OUT
1234
--IN
0
5
--OUT
05
@@EXPL
두 정수를 더하지 않고 글자 그대로 이어 붙이는 문제다. 정수를 문자열로 바꾼 뒤 문자열 `+` 로 합치는 것이 핵심이다.

- `cin >> a >> b` 로 두 정수를 받는다.
- `to_string(a)` 와 `to_string(b)` 로 각각 문자열로 바꾼다. 예: 12 -> `"12"`, 34 -> `"34"`.
- 문자열끼리 `+` 하면 산술 합이 아니라 이어붙이기가 된다. `"12" + "34"` = `"1234"`.
- `0` 과 `5` 를 이어 붙이면 `"0" + "5"` = `"05"` 처럼 앞의 0도 그대로 남는다.

스스로 다시 짤 때 생각 순서: (1) "더하기"가 아니라 "붙이기"임을 분명히 구분한다. (2) 이어붙이기는 문자열의 `+` 이므로 각 정수를 `to_string` 으로 바꾼다. (3) 두 문자열을 `+` 로 합쳐 출력한다.
```

**3) 팰린드롬 숫자** · Hard

- **요구사항**: 정수를 받아, 자릿수를 뒤집어도 같은 수(팰린드롬)면 `YES`, 아니면 `NO`를 출력한다.
- **입력**: 한 줄에 정수 `n` (0 이상)
- **출력**: 팰린드롬이면 `YES`, 아니면 `NO`
- **예제**:
  - `12321` → `YES`
  - `123` → `NO`
  - `7` → `YES`
- **셀프체크**: `to_string(n)` 으로 바꾼 뒤 뒤집은 문자열과 원래 문자열이 같은지 비교한다. 한 자리 수는 항상 팰린드롬이다. `1000` 처럼 뒤집으면 `0001`(=`"0001"`)이 되어 원본과 다르므로 `NO`다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    int n;
    cin >> n;
    string s = to_string(n);
    string rev = "";
    for (int i = s.size() - 1; i >= 0; i--) {
        rev = rev + s[i];
    }
    if (s == rev) cout << "YES" << endl;
    else cout << "NO" << endl;
    return 0;
}
@@TESTS
--IN
12321
--OUT
YES
--IN
123
--OUT
NO
@@EXPL
숫자를 뒤집어도 같은지(팰린드롬) 판별하는 문제다. 숫자를 문자열로 바꾼 뒤, 원래 문자열과 뒤집은 문자열을 비교한다.

- `cin >> n` 으로 정수를 받고, `to_string(n)` 으로 문자열 `s`로 바꾼다.
- 뒤집은 문자열 `rev` 를 만든다. 인덱스를 마지막(`s.size() - 1`)부터 0까지 거꾸로 돌며 글자를 이어 붙이면 `s`의 역순이 된다. 예: `"12321"` -> `"12321"`, `"123"` -> `"321"`.
- `if (s == rev)` 로 원래와 뒤집은 것이 같은지 비교한다. `string` 끼리 `==` 는 내용이 완전히 같은지 본다. 같으면 팰린드롬이므로 `YES`, 아니면 `NO` 를 출력한다.

스스로 다시 짤 때 생각 순서: (1) 팰린드롬은 "뒤집어도 같은가"의 문제임을 떠올린다. (2) 뒤집기·비교는 문자열이 편하므로 `to_string(n)` 으로 바꾼다. (3) 인덱스를 거꾸로 돌며 뒤집은 문자열을 만든다. (4) 원본과 `==` 로 비교해 결과에 따라 YES/NO 를 낸다.
```


## L14. 문자열 비교

**개념**

- 두 문자열이 완전히 같은지는 `==` 로, 다른지는 `!=` 로 비교한다. 결과는 `true`/`false` 다. 대소문자도 구분한다: `"Apple" == "apple"` 은 `false`.

- 크기 비교(`<`, `>`, `<=`, `>=`)도 된다. 이는 사전 순서(사전에서 먼저 나오면 작다)로 정해진다. 실제로는 앞 글자부터 아스키 코드를 하나씩 비교한다.

- 첫 글자의 코드가 다르면 거기서 승부가 난다: `"apple" < "banana"` 는 `'a'`(97) < `'b'`(98) 이라 `true`. 앞이 같으면 다음 글자로 넘어간다: `"apple" < "apply"` 는 넷째 글자 `'e'`(101) < `'y'`(121) 이라 `true`.

- 한 문자열이 다른 문자열의 앞부분과 똑같고 길이만 짧으면, 짧은 쪽이 작다: `"app" < "apple"` 은 `true`.

- 주의: 대문자는 소문자보다 코드가 작다(`'Z'`=90 < `'a'`=97). 그래서 `"Zoo" < "apple"` 은 `true`. 대소문자를 무시하고 비교하려면 양쪽을 소문자로 맞춘 뒤 비교한다.

```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
    cout << (string("apple") == "apple") << endl;   // 1 (true)
    cout << (string("apple") < "banana") << endl;   // 1
    cout << (string("app") < "apple") << endl;      // 1  (앞부분 같고 더 짧음)
    cout << (string("Zoo") < "apple") << endl;      // 1  ('Z'=90 < 'a'=97)
    return 0;
}
```

> 선행: 비교 연산자와 조건문(Ch4), 아스키 코드(L10), 소문자로 맞추기(L11)를 함께 쓴다. C++에서 `bool` 을 `cout` 하면 `true`/`false` 가 아니라 `1`/`0` 으로 나온다는 점에 유의한다.

**문제**

**1) 같은지 확인** · Easy

- **요구사항**: 두 문자열을 받아 완전히 같으면 `SAME`, 다르면 `DIFF`를 출력한다.
- **입력**: 두 줄에 각각 문자열 `a`, `b`(공백 없음)
- **출력**: 같으면 `SAME`, 다르면 `DIFF`
- **예제**:
  - `apple` / `apple` → `SAME`
  - `Apple` / `apple` → `DIFF`
  - `cat` / `dog` → `DIFF`
- **셀프체크**: 대소문자가 다르면 다른 문자열이다. `==` 의 결과에 따라 서로 다른 문자열을 출력하는지 확인한다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string a, b;
    getline(cin, a);
    getline(cin, b);
    if (a == b) cout << "SAME" << endl;
    else cout << "DIFF" << endl;
    return 0;
}
@@TESTS
--IN
apple
apple
--OUT
SAME
--IN
Apple
apple
--OUT
DIFF
@@EXPL
두 문자열이 완전히 같은지 판별하는 문제다. `==` 로 비교하고 결과에 따라 다른 말을 출력한다.

- `getline(cin, a)`, `getline(cin, b)` 로 두 문자열을 받는다.
- `if (a == b)` 로 두 문자열이 완전히 같은지 확인한다. `string` 의 `==` 는 대소문자까지 구분하므로 `Apple` 과 `apple` 은 다르다고 본다.
- 같으면 `SAME`, 아니면(`else`) `DIFF` 를 출력한다.

스스로 다시 짤 때 생각 순서: (1) "같은지"는 `==` 비교라는 걸 떠올린다. (2) 대소문자도 구분된다는 점을 기억한다. (3) `if / else` 로 두 경우에 각각 `SAME` / `DIFF` 를 출력한다.
```

**2) 사전순으로 앞선 것** · Medium

- **요구사항**: 서로 다른 두 문자열을 받아 사전 순으로 더 앞에 오는 것을 출력한다.
- **입력**: 두 줄에 각각 문자열 `a`, `b`(공백 없음, 서로 다름)
- **출력**: 사전 순으로 앞선 문자열
- **예제**:
  - `banana` / `apple` → `apple`
  - `app` / `apple` → `app`
  - `Zoo` / `apple` → `Zoo`
- **셀프체크**: `<` 로 비교하면 사전 순으로 작은(앞선) 쪽을 알 수 있다. 대문자는 소문자보다 앞선다는 점(코드가 작음)을 잊지 않는다. 앞부분이 같으면 짧은 쪽이 앞선다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string a, b;
    getline(cin, a);
    getline(cin, b);
    if (a < b) cout << a << endl;
    else cout << b << endl;
    return 0;
}
@@TESTS
--IN
banana
apple
--OUT
apple
--IN
Zoo
apple
--OUT
Zoo
@@EXPL
서로 다른 두 문자열 중 사전 순으로 앞선 것을 고르는 문제다. `string` 의 `<` 비교가 사전 순서를 그대로 따른다.

- `getline` 으로 두 문자열 `a`, `b`를 받는다.
- `a < b` 는 `a`가 사전 순으로 `b`보다 앞이면 참이다. 비교는 앞 글자부터 아스키 코드를 하나씩 견주는 방식이다.
- 참이면 `a`가 앞서므로 `a`를, 아니면 `b`를 출력한다.
- 주의: 대문자는 소문자보다 코드가 작아 앞선다. 그래서 `Zoo` vs `apple` 에서는 `'Z'`(90) < `'a'`(97) 라 `Zoo` 가 앞선다.

스스로 다시 짤 때 생각 순서: (1) "사전 순 앞"은 문자열 `<` 비교로 알 수 있음을 떠올린다. (2) `a < b` 면 `a`, 아니면 `b`를 고른다. (3) 대문자가 소문자보다 앞선다는 코드 순서를 잊지 않는다.
```

**3) 대소문자 무시 비교** · Hard

- **요구사항**: 두 문자열을 받아 대소문자를 무시했을 때 같으면 `EQUAL`, 그렇지 않으면 사전 순(대소문자 무시)으로 앞선 문자열을 출력한다.
- **입력**: 두 줄에 각각 문자열 `a`, `b`(공백 없음)
- **출력**: 대소문자 무시하고 같으면 `EQUAL`, 아니면 앞선 쪽 문자열(원래 대소문자 그대로)
- **예제**:
  - `Apple` / `apple` → `EQUAL`
  - `Banana` / `apple` → `apple`
  - `cat` / `Car` → `Car`
- **셀프체크**: 비교는 양쪽을 소문자로 바꿔서 하되, 출력은 입력받은 원래 문자열을 그대로 낸다. `cat` 과 `Car` 는 소문자로 보면 `cat` vs `car` → 셋째 글자 `t`(116) > `r`(114) 이라 `car` 쪽(`Car`)이 앞선다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
string toLower(string s) {
    for (int i = 0; i < s.size(); i++) {
        if ('A' <= s[i] && s[i] <= 'Z') s[i] = s[i] + 32;
    }
    return s;
}
int main() {
    string a, b;
    getline(cin, a);
    getline(cin, b);
    string la = toLower(a);
    string lb = toLower(b);
    if (la == lb) cout << "EQUAL" << endl;
    else if (la < lb) cout << a << endl;
    else cout << b << endl;
    return 0;
}
@@TESTS
--IN
Apple
apple
--OUT
EQUAL
--IN
cat
Car
--OUT
Car
@@EXPL
**이 풀이의 새 문법**

- `string toLower(string s) { ... return s; }`: `main` 밖에 별도로 정의한 함수. 괄호 안 `s`는 전달받은 문자열을 담는 매개변수이고, `return`은 계산한 값을 호출한 곳으로 돌려준다. `toLower(a)`처럼 이름과 괄호로 호출해 쓴다.

대소문자를 무시하고 두 문자열을 비교하는 문제다. 비교는 소문자로 맞춰서 하되, 출력은 원래 대소문자 그대로 내는 것이 핵심이다.

- `getline` 으로 원래 문자열 `a`, `b`를 받아 둔다.
- `toLower` 함수로 각 문자열의 대문자를 소문자로 바꾼 비교용 버전을 만든다. 대문자면 코드에 32를 더해 소문자로 바꾼다. 원본 `a`, `b`는 그대로 남긴다.
- `la = toLower(a)`, `lb = toLower(b)` 로 소문자 버전을 얻는다.
- `if (la == lb)` 로 대소문자 무시하고 같은지 먼저 확인한다. 같으면 `EQUAL`.
- 아니면 `else if (la < lb)` 로 소문자 기준 사전 순을 비교해, 앞선 쪽의 **원본**(`a` 또는 `b`)을 출력한다.
- 예: `cat` vs `Car` -> 소문자로 `cat` vs `car`, 셋째 글자 `t` > `r` 이라 `car` 쪽인 원본 `Car` 가 앞선다.

스스로 다시 짤 때 생각 순서: (1) "대소문자 무시"이므로 비교 전에 양쪽을 소문자로 맞춰야 함을 떠올린다. (2) 소문자 버전을 만드는 함수를 두고, 원본과 비교용을 분리한다(출력은 원본). (3) 같으면 EQUAL, 아니면 소문자끼리 `<` 로 앞선 쪽을 정한다. (4) 정한 쪽은 소문자 버전이 아니라 대응하는 원본을 출력한다.
```
