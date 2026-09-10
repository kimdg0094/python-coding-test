> 언어 C++

> 개요: 이 챕터에서는 문자(글자)들이 이어진 "문자열"을 입력받고, 하나씩 살펴보고, 이어 붙이거나 찾고 바꾸는 기본기를 배운다. C++에서는 `std::string`을 쓰며, 문자열도 배열처럼 인덱스로 다룰 수 있다는 감각을 익히는 것이 핵심이다.

## L1. 공백없는 문자열 입력받아 출력하기

**개념**

- 문자열(string)은 글자들이 순서대로 이어진 자료형이다. 예: `"apple"`, `"hello123"`
- C++에서는 `#include <string>` 후 `string` 타입을 쓴다. `getline(cin, s)`로 한 줄을 읽으면 그 자체가 이미 문자열이다. 정수처럼 `int`로 받을 필요가 없다.
- `getline(cin, s)`은 한 줄 전체를 읽되, 맨 끝의 줄바꿈(엔터)은 문자열에 넣지 않고 떼어낸다.
- 이번 레슨의 입력은 "공백이 없는" 한 덩어리 문자열이다. 즉 중간에 띄어쓰기가 없다.
- 문자열 리터럴은 큰따옴표 `"..."`로 적는다. 작은따옴표 `'...'`는 글자(문자, `char`) 하나를 뜻하므로 구분해야 한다.

```cpp
string s;
getline(cin, s);   // 예: 사용자가 apple 을 입력
cout << s << endl; // apple
```

**문제**

**1) 그대로 따라 말하기** · Easy

- **요구사항**: 공백 없는 문자열 한 개를 입력받아 그대로 한 줄에 출력한다.
- **입력**: 첫 줄에 공백이 없는 문자열 하나
- **출력**: 입력받은 문자열을 그대로 출력
- **예제**: `banana` → `banana` / `Code2024` → `Code2024`
- **셀프체크**: `int`가 아니라 `string`으로 받았는지 확인. 문자열에 숫자가 섞여 있어도 그냥 문자열이다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    cout << s << endl;
    return 0;
}
@@TESTS
--IN
banana
--OUT
banana
--IN
Code2024
--OUT
Code2024
@@EXPL
접근: `getline(cin, s)`로 읽은 한 줄은 그 자체가 문자열이다. 정수처럼 `int`로 받을 필요가 없다. 받은 값을 그대로 출력한다.

코드 진행:

- `string s;`로 문자열 변수를 선언한다.
- `getline(cin, s)`로 한 줄을 문자열로 받는다.
- `cout << s << endl;`로 그대로 출력한다.

재작성 사고 순서: (1) 입력을 문자열로 받기(`int` 사용 안 함) → (2) 그대로 출력. `Code2024`처럼 숫자가 섞여 있어도 이것은 계산할 수가 아니라 그냥 문자열이므로 변환하지 않는다.
```

**2) 두 번 외치기** · Easy

- **요구사항**: 공백 없는 문자열 한 개를 입력받아 두 줄에 걸쳐 두 번 출력한다.
- **입력**: 첫 줄에 문자열 하나
- **출력**: 첫 줄과 둘째 줄에 각각 같은 문자열
- **예제**: `hi` → `hi`(줄바꿈)`hi` / `dog` → `dog`(줄바꿈)`dog`
- **셀프체크**: 입력은 한 번만 받는다. `cout ... << endl`을 두 번 하면 자동으로 줄이 나뉜다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    cout << s << endl;
    cout << s << endl;
    return 0;
}
@@TESTS
--IN
hi
--OUT
hi
hi
--IN
dog
--OUT
dog
dog
@@EXPL
접근: 같은 문자열을 두 줄에 두 번 출력하는 문제다. 입력은 한 번만 받고, 그 값을 `cout`으로 두 번 찍으면 된다.

코드 진행:

- `getline(cin, s)`으로 문자열을 한 번만 받는다.
- `cout << s << endl;`을 두 번 쓴다.
- `endl`은 매번 줄을 바꾸므로 같은 값이 두 줄에 나온다.

재작성 사고 순서: (1) 입력 한 번 받기 → (2) 같은 변수를 두 번 출력 → 두 줄 출력. 입력을 두 번 받으려 하지 말 것(엔터가 하나뿐이라 둘째 `getline`은 빈 줄을 읽는다).
```

**3) 인사 붙이기** · Medium

- **요구사항**: 이름(공백 없는 문자열)을 입력받아 `Hello, ` 뒤에 이름을 붙이고 마지막에 `!`를 붙여 출력한다.
- **입력**: 첫 줄에 이름 하나
- **출력**: `Hello, {이름}!` 형태의 한 줄
- **예제**: `Sua` → `Hello, Sua!` / `min123` → `Hello, min123!`
- **셀프체크**: 쉼표 뒤 공백, 느낌표 위치가 예제와 정확히 같은지. 이름 앞뒤에 불필요한 공백이 붙지 않았는지.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    cout << "Hello, " << s << "!" << endl;
    return 0;
}
@@TESTS
--IN
Sua
--OUT
Hello, Sua!
--IN
min123
--OUT
Hello, min123!
@@EXPL
접근: 고정된 문구 `Hello, `와 입력받은 이름, 그리고 `!`를 이어 붙이는(concat) 문제다. C++에서는 `cout <<`로 여러 조각을 차례로 흘려보내도 되고, `+`로 붙여도 된다.

코드 진행:

- 이름 `s`를 `getline(cin, s)`으로 받는다.
- `cout << "Hello, " << s << "!" << endl;`로 앞 문구, 이름, 느낌표를 순서대로 내보낸다. 쉼표 뒤 공백은 문자열 안에 미리 넣어 둔다.
- 결과가 한 줄에 출력된다.

재작성 사고 순서: (1) 이름 입력 → (2) 인사말, 이름, 느낌표를 순서대로 출력 → (3) 줄바꿈. `"Hello, "`의 끝 공백과 `!`의 위치가 예제와 정확히 같아야 하고, 이름 앞뒤에 여분 공백이 붙지 않도록 한다.
```

## L2. 공백있는 문자열 한번에 입력받기

**개념**

- 문장처럼 중간에 띄어쓰기(공백)가 들어간 문자열도 있다. 예: `I love code`
- `getline(cin, s)`은 한 줄 전체를 읽으므로, 중간 공백이 있어도 한 번에 그대로 받는다. 공백도 문자열의 일부다.
- 주의: `cin >> s`는 공백을 만나면 거기서 끊는다. 그래서 공백 있는 문장은 반드시 `getline`으로 받아야 한 줄이 통째로 들어온다.
- 문자열의 길이를 세면 공백도 한 글자로 센다. 길이는 `s.length()`(또는 `s.size()`)로 구한다.

```cpp
string s;
getline(cin, s);        // 예: I love code
cout << s << endl;      // I love code
cout << s.length() << endl;  // 11  (공백 2개 포함)
```

> 선행: `s.length()`는 문자열의 글자 수(길이)를 돌려주는 기능이다. 배열의 길이를 재던 것과 같은 개념이다.

**문제**

**1) 문장 그대로 출력** · Easy

- **요구사항**: 공백이 포함될 수 있는 문장 한 줄을 입력받아 그대로 출력한다.
- **입력**: 첫 줄에 문장 하나 (중간에 공백이 있을 수 있음)
- **출력**: 입력 문장을 그대로 한 줄에 출력
- **예제**: `good morning` → `good morning` / `I am here` → `I am here`
- **셀프체크**: `cin >> s`가 아니라 `getline`으로 받는다. 공백을 기준으로 잘라 받지 않도록 주의.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    cout << s << endl;
    return 0;
}
@@TESTS
--IN
good morning
--OUT
good morning
--IN
I am here
--OUT
I am here
@@EXPL
접근: `getline(cin, s)`은 한 줄 전체를 읽으므로 중간에 공백이 있어도 한 번에 통째로 받는다. 받은 그대로 출력하면 된다.

코드 진행:

- `getline(cin, s)`으로 한 줄 문장을 받는다. 공백도 문자열의 일부로 함께 들어온다.
- `cout << s << endl;`로 받은 문장을 그대로 출력한다.

재작성 사고 순서: (1) 한 줄 입력 받기(`getline`) → (2) 그대로 출력. `cin >> s`는 공백에서 끊기므로 쓰지 않는다. 한 줄 통째로 받는다는 점만 지키면 된다.
```

**2) 문장 길이 세기** · Medium

- **요구사항**: 공백이 포함될 수 있는 문장을 입력받아, 그 문장의 전체 길이(공백 포함)를 출력한다.
- **입력**: 첫 줄에 문장 하나
- **출력**: 문장의 길이(정수) 한 줄
- **예제**: `a b` → `3` / `hello world` → `11`
- **셀프체크**: `a b`는 `a`, 공백, `b`로 3글자. `hello world`는 5+1+5=11. 공백을 빼먹지 않았는지 검산.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    cout << s.length() << endl;
    return 0;
}
@@TESTS
--IN
a b
--OUT
3
--IN
hello world
--OUT
11
@@EXPL
접근: 문장의 전체 길이는 공백까지 포함해서 센다. `s.length()`가 문자열의 글자 수를 그대로 돌려준다.

코드 진행:

- 문장 한 줄을 `getline(cin, s)`으로 받는다(중간 공백도 함께 받는다).
- `s.length()`로 글자 수를 구한다.
- 그 값을 한 줄에 출력한다.

재작성 사고 순서: (1) 문장 입력(`getline`) → (2) `s.length()`로 길이 구하기 → (3) 출력. `a b`는 `a`, 공백, `b`로 3, `hello world`는 5+1+5=11처럼 공백도 한 글자로 세는지 검산한다.
```

**3) 앞뒤로 감싸기** · Medium

- **요구사항**: 문장 한 줄을 입력받아 `[` 와 `]` 사이에 넣어 출력한다. 문장 안 공백은 그대로 둔다.
- **입력**: 첫 줄에 문장 하나
- **출력**: `[{문장}]` 한 줄
- **예제**: `hi there` → `[hi there]` / `end` → `[end]`
- **셀프체크**: 대괄호와 문장 사이에 불필요한 공백이 들어가지 않았는지. 문장 내부 공백은 유지되어야 함.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    cout << "[" << s << "]" << endl;
    return 0;
}
@@TESTS
--IN
hi there
--OUT
[hi there]
--IN
end
--OUT
[end]
@@EXPL
접근: 입력 문장의 앞뒤에 대괄호를 붙이는 문제다. `cout`으로 `"["`, 문장, `"]"`를 차례로 내보내면 된다.

코드 진행:

- 한 줄 문장을 `getline(cin, s)`으로 받는다(공백이 있어도 통째로 받는다).
- `cout << "[" << s << "]" << endl;`로 앞뒤에 대괄호를 붙여 출력한다.

재작성 사고 순서: (1) 문장 한 줄 입력(`getline`) → (2) 여는 괄호, 문장, 닫는 괄호를 순서대로 출력 → (3) 줄바꿈. 괄호와 문장 사이에 공백을 넣지 않아야 하고, 문장 내부의 공백은 그대로 유지된다.
```

## L3. 문자열 배열 관리

**개념**

- 여러 개의 문자열을 함께 다루려면 문자열 배열에 담는다. 예: `string words[100];`
- 개수가 정해지면 인덱스로 하나씩 채운다. 예: `words[i] = ...;`
- 배열은 넉넉한 크기로 미리 잡아 둔다. 예: `string words[100];`(최대 100개까지 담을 수 있게).
- 배열 안의 문자열은 인덱스로 꺼낸다. 첫 번째는 `words[0]`, 두 번째는 `words[1]`.
- 배열에 담긴 문자열들을 하나씩 처리할 때는 `for`로 돈다.
- 주의: `cin >> n`으로 개수를 읽은 뒤 `getline`으로 문자열을 읽으려면, 사이에 `cin.ignore();`로 개수 뒤에 남은 줄바꿈을 버려야 한다. 그렇지 않으면 첫 `getline`이 빈 줄을 읽는다.

```cpp
int n;
cin >> n;          // 문자열 개수
cin.ignore();      // 개수 뒤 줄바꿈 버리기
string words[100];
for (int i = 0; i < n; i++) {
    getline(cin, words[i]);   // 한 줄씩 읽어 담기
}
cout << words[0] << endl;      // 첫 번째 문자열
```

**문제**

**1) 첫 번째와 마지막** · Easy

- **요구사항**: 문자열 여러 개를 입력받아 배열에 담고, 첫 번째 문자열과 마지막 문자열을 각각 한 줄씩 출력한다.
- **입력**: 첫 줄에 개수 `n`. 이어서 `n`개의 줄에 각각 공백 없는 문자열 하나
- **출력**: 첫 번째 문자열, 그다음 줄에 마지막 문자열
- **예제**: `3`/`red`/`green`/`blue` → `red`(줄바꿈)`blue`
- **셀프체크**: 마지막 원소 인덱스는 `n-1`. `words[n]`은 범위를 벗어난다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    int n;
    cin >> n;
    cin.ignore();
    string words[100];
    for (int i = 0; i < n; i++) {
        getline(cin, words[i]);
    }
    cout << words[0] << endl;
    cout << words[n - 1] << endl;
    return 0;
}
@@TESTS
--IN
3
red
green
blue
--OUT
red
blue
--IN
2
up
down
--OUT
up
down
@@EXPL
접근: 문자열들을 배열에 담고 첫 번째와 마지막을 꺼낸다. 첫 번째는 인덱스 0, 마지막은 인덱스 `n-1`이다.

코드 진행:

- 개수 `n`을 `cin >> n`으로 받고, `cin.ignore()`로 남은 줄바꿈을 버린다. 그다음 배열 `words`를 준비한다.
- `for (int i = 0; i < n; i++)`로 `n`줄을 읽어 `getline(cin, words[i])`로 담는다.
- `words[0]`(첫 번째)을 출력하고, 다음 줄에 `words[n-1]`(마지막)을 출력한다.

재작성 사고 순서: (1) 개수 읽고 줄바꿈 버리기 → (2) 반복으로 배열 채우기 → (3) 인덱스 0과 `n-1`을 각각 출력. 마지막 원소는 `words[n]`이 아니라 `words[n-1]`임에 주의.
```

**2) 거꾸로 나열** · Medium

- **요구사항**: 문자열 `n`개를 입력받아 입력의 역순으로 한 줄씩 출력한다.
- **입력**: 첫 줄에 `n`. 이어서 `n`개의 문자열이 각 줄에
- **출력**: 마지막에 입력된 것부터 처음 것까지 한 줄씩
- **예제**: `3`/`one`/`two`/`three` → `three`(줄바꿈)`two`(줄바꿈)`one`
- **셀프체크**: 인덱스 `n-1`부터 `0`까지 1씩 줄이며 접근했는지. 순서가 뒤집혔는지 눈으로 확인.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    int n;
    cin >> n;
    cin.ignore();
    string words[100];
    for (int i = 0; i < n; i++) {
        getline(cin, words[i]);
    }
    for (int i = n - 1; i >= 0; i--) {
        cout << words[i] << endl;
    }
    return 0;
}
@@TESTS
--IN
3
one
two
three
--OUT
three
two
one
--IN
2
cat
dog
--OUT
dog
cat
@@EXPL
접근: 입력을 배열에 순서대로 담은 뒤, 마지막 인덱스부터 첫 인덱스까지 거꾸로 훑으며 출력하면 역순이 된다.

코드 진행:

- 개수 `n`을 받고(줄바꿈 버리기), 배열에 `n`개의 문자열을 `getline`으로 담는다.
- `for (int i = n - 1; i >= 0; i--)`는 `n-1`에서 시작해 `-1`씩 줄여 `0`까지 돈다.
- 그 인덱스 `i`로 `words[i]`를 한 줄씩 출력한다.

재작성 사고 순서: (1) 배열 채우기 → (2) 마지막 인덱스 `n-1`부터 `0`까지 감소 반복 → (3) 각 원소 출력. 감소 반복은 `for (i = n-1; i >= 0; i--)` 꼴이다.
```

**3) 특정 순번만 출력** · Medium

- **요구사항**: 문자열 `n`개를 배열에 담은 뒤, 정수 `k`를 입력받아 `k`번째(1부터 셈) 문자열을 출력한다.
- **입력**: 첫 줄에 `n`. 다음 `n`줄에 문자열들. 마지막 줄에 정수 `k` (1 이상 `n` 이하)
- **출력**: `k`번째 문자열 한 줄
- **예제**: `3`/`cat`/`dog`/`fox`/`2` → `dog` / `3`/`cat`/`dog`/`fox`/`1` → `cat`
- **셀프체크**: "1부터 세는 k"와 "0부터 세는 인덱스"의 차이. `k`번째는 인덱스 `k-1`이다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    int n;
    cin >> n;
    cin.ignore();
    string words[100];
    for (int i = 0; i < n; i++) {
        getline(cin, words[i]);
    }
    int k;
    cin >> k;
    cout << words[k - 1] << endl;
    return 0;
}
@@TESTS
--IN
3
cat
dog
fox
2
--OUT
dog
--IN
3
cat
dog
fox
1
--OUT
cat
@@EXPL
접근: 문자열들을 배열에 담은 뒤, "1부터 세는 k번째"를 꺼낸다. 배열 인덱스는 0부터 세므로, k번째는 인덱스 `k-1`에 해당한다.

코드 진행:

- 개수 `n`을 받고(줄바꿈 버리기), 배열 `words`를 준비한다.
- `for (int i = 0; i < n; i++)`로 `n`개의 줄을 읽어 `getline(cin, words[i])`로 담는다.
- 마지막 줄에서 `cin >> k`로 `k`를 받는다(문자열은 이미 다 읽었으므로 `>>`로 정수를 받아도 된다).
- `words[k-1]`을 출력한다.

재작성 사고 순서: (1) 개수 읽기 → (2) 반복으로 배열 채우기 → (3) `k` 읽기 → (4) 1부터 세는 순번을 인덱스로 바꾸려 `k-1` 사용해 출력. `k=2`면 인덱스 1, 즉 두 번째 원소 `dog`.
```

## L4. 문자열 순회하기

**개념**

- 문자열은 글자 하나하나가 순서대로 들어 있어, 하나씩 꺼내 볼 수 있다.
- 인덱스로 접근: `s[0]`은 첫 글자, `s[1]`은 두 번째 글자. 배열과 똑같다. 각 글자는 `char`(문자) 타입이다.
- `for (int i = 0; i < s.length(); i++)` 로 돌며 `s[i]`로 각 글자에 접근한다.
- 순회하며 개수 세기(cnt)나 조건 검사를 할 수 있다.
- 문자 하나를 비교할 때는 작은따옴표를 쓴다. 예: `if (s[i] == 'a')`.

```cpp
string s;
getline(cin, s);
for (int i = 0; i < s.length(); i++) {
    cout << s[i] << endl;   // 글자를 한 줄에 하나씩
}

string t = "abc";
cout << t[0] << " " << t[2] << endl;   // a c
```

**문제**

**1) 한 글자씩 세로로** · Easy

- **요구사항**: 공백 없는 문자열을 입력받아, 한 글자씩 각 줄에 하나씩 출력한다.
- **입력**: 첫 줄에 공백 없는 문자열 하나
- **출력**: 각 글자를 한 줄에 하나씩
- **예제**: `sky` → `s`(줄바꿈)`k`(줄바꿈)`y`
- **셀프체크**: 글자 수만큼 줄이 나오는지. 마지막 글자 뒤에 빈 줄이 더 붙지 않았는지.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    for (int i = 0; i < s.length(); i++) {
        cout << s[i] << endl;
    }
    return 0;
}
@@TESTS
--IN
sky
--OUT
s
k
y
--IN
ab
--OUT
a
b
@@EXPL
접근: 문자열의 각 글자를 한 줄에 하나씩 출력하는 문제다. `for`로 인덱스 `0`부터 끝까지 돌며 `s[i]`를 하나씩 꺼낸다.

코드 진행:

- 문자열 `s`를 받는다.
- `for (int i = 0; i < s.length(); i++)`로 인덱스를 하나씩 돈다.
- 매 반복에서 `cout << s[i] << endl;`로 한 글자를 한 줄에 출력한다.

재작성 사고 순서: (1) 문자열 입력 → (2) 인덱스로 순회 → (3) 각 글자를 `endl`과 함께 출력. `endl`이 줄을 바꾸므로 글자 수만큼 줄이 나오고, 마지막 뒤에 여분의 빈 줄은 생기지 않는다.
```

**2) 특정 글자 개수 세기** · Medium

- **요구사항**: 문자열과 찾을 글자 하나를 입력받아, 문자열 안에 그 글자가 몇 번 나오는지 센다.
- **입력**: 첫 줄에 공백 없는 문자열, 둘째 줄에 찾을 글자 한 개
- **출력**: 등장 횟수(정수) 한 줄
- **예제**: `banana`/`a` → `3` / `apple`/`z` → `0`
- **셀프체크**: 없으면 0이 나와야 함. 대소문자는 서로 다른 글자로 취급한다(`A`와 `a`는 다름).

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    char target;
    cin >> target;
    int cnt = 0;
    for (int i = 0; i < s.length(); i++) {
        if (s[i] == target) {
            cnt = cnt + 1;
        }
    }
    cout << cnt << endl;
    return 0;
}
@@TESTS
--IN
banana
a
--OUT
3
--IN
apple
z
--OUT
0
@@EXPL
접근: 특정 글자가 몇 번 나오는지 세는 문제다. 문자열을 한 글자씩 돌며, 찾는 글자와 같을 때마다 세는 변수를 1씩 늘린다.

코드 진행:

- 문자열 `s`를 `getline`으로 받고, 찾을 글자 `target`을 `char`로 `cin >> target`으로 받는다. `>>`는 공백/줄바꿈을 건너뛰고 글자 하나만 읽는다.
- `cnt = 0`으로 개수 세는 변수를 준비한다.
- `for`로 각 글자를 하나씩 꺼내며, `s[i] == target`이면 `cnt = cnt + 1`로 센다.
- 순회가 끝나면 `cnt`를 출력한다.

재작성 사고 순서: (1) 카운터 `cnt = 0` → (2) 문자열을 글자 단위로 순회 → (3) 찾는 글자와 같으면 카운터 +1 → (4) 출력. 한 번도 안 나오면 `cnt`가 0인 채로 남는다. 대소문자는 다른 글자로 센다.
```

**3) 앞뒤가 같은지 확인** · Hard

- **요구사항**: 공백 없는 문자열을 입력받아, 앞에서 읽으나 뒤에서 읽으나 같은지(회문인지) 판별해 `YES`/`NO`를 출력한다.
- **입력**: 첫 줄에 공백 없는 문자열 하나
- **출력**: 회문이면 `YES`, 아니면 `NO`
- **예제**: `level` → `YES` / `hello` → `NO` / `a` → `YES`
- **셀프체크**: `i`번째 글자와 `len-1-i`번째 글자를 비교. 길이가 1이면 항상 회문. 하나라도 다르면 즉시 회문 아님.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    bool ok = true;
    int len = s.length();
    for (int i = 0; i < len; i++) {
        if (s[i] != s[len - 1 - i]) {
            ok = false;
        }
    }
    if (ok) {
        cout << "YES" << endl;
    } else {
        cout << "NO" << endl;
    }
    return 0;
}
@@TESTS
--IN
level
--OUT
YES
--IN
hello
--OUT
NO
--IN
a
--OUT
YES
@@EXPL
접근: 회문이면 앞에서 `i`번째 글자와 뒤에서 같은 거리에 있는 글자(`len-1-i`번째)가 서로 같아야 한다. 하나라도 다르면 회문이 아니다. 그래서 "일단 회문(`true`)"으로 가정하고, 다른 짝이 발견되면 거짓으로 뒤집는다.

코드 진행:

- 문자열 `s`를 받고 `bool ok = true;`로 시작한다. 길이는 `len`에 담아 둔다.
- `for (int i = 0; i < len; i++)`로 각 자리를 돌며, `s[i]`와 `s[len-1-i]`를 비교한다.
- 두 글자가 다르면 `ok = false;`로 표시한다.
- 순회가 끝난 뒤 `ok`가 참이면 `YES`, 아니면 `NO`를 출력한다.

재작성 사고 순서: (1) `ok = true` 가정 → (2) 앞 글자와 대칭 위치 뒤 글자를 비교 → (3) 다르면 `ok = false` → (4) 최종 판정 출력. 길이가 1이면 자기 자신과만 비교되어 항상 YES.
```

## L5. 문자열 Concat

**개념**

- 문자열끼리 `+`로 이어 붙이는 것을 concat(연결)이라고 한다. 예: `string("ab") + "cd"` → `"abcd"`
- `+`는 두 문자열을 순서대로 붙일 뿐, 사이에 공백을 넣지 않는다. 공백이 필요하면 `" "`를 직접 넣는다.
- 반복문 안에서 결과 문자열에 한 조각씩 계속 더해 나갈 수도 있다. 빈 문자열 `""`에서 시작한다. `result = result + s`처럼 쓴다.
- `char` 하나도 `string`에 `+`로 붙일 수 있다. 예: `result = result + s[i];` (한 글자를 이어 붙임)
- 주의: C++에서 `"ab" + "cd"`처럼 문자열 리터럴끼리 바로 `+`하면 안 된다. 최소 한쪽이 `string` 타입이어야 한다. 그래서 결과 변수를 `string result = "";`로 두고 거기에 붙여 나가는 방식이 안전하다.

```cpp
string a, b;
getline(cin, a);
getline(cin, b);
cout << a + b << endl;         // 두 문자열을 붙여 출력
cout << a + " " + b << endl;   // 사이에 공백을 넣어 붙임

string result = "";
for (int i = 0; i < 3; i++) {
    result = result + "ha";
}
cout << result << endl;        // hahaha
```

- 인덱스로 부분 글자를 꺼내 붙일 수도 있다. `s[i]`는 `i`번째 글자(char)이며, `result + s[i]`로 결과에 한 글자를 이어 붙인다. 이렇게 앞에서부터 한 글자씩 쌓으면 부분 문자열을 만들어 갈 수 있다.

```cpp
string s = "apple";
string part = "";
part = part + s[0];   // "a"
part = part + s[1];   // "ap"
cout << part << endl; // ap
```

**문제**

**1) 두 단어 붙이기** · Easy

- **요구사항**: 공백 없는 두 문자열을 각 줄에서 입력받아, 사이에 공백 하나를 넣어 이어 출력한다.
- **입력**: 첫째 줄과 둘째 줄에 각각 공백 없는 문자열
- **출력**: `{첫째} {둘째}` 형태 한 줄
- **예제**: `good`/`job` → `good job` / `hello`/`world` → `hello world`
- **셀프체크**: 두 단어 사이에 공백이 정확히 하나인지. 앞뒤에 여분 공백이 없는지.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string a, b;
    getline(cin, a);
    getline(cin, b);
    cout << a + " " + b << endl;
    return 0;
}
@@TESTS
--IN
good
job
--OUT
good job
--IN
hello
world
--OUT
hello world
@@EXPL
접근: 두 문자열 사이에 공백 하나를 넣어 붙이는 문제다. `+`는 사이에 아무것도 넣지 않으므로, 공백이 필요하면 `" "`를 직접 끼워 concat한다.

코드 진행:

- 첫째 줄과 둘째 줄에서 문자열 `a`, `b`를 각각 `getline`으로 받는다.
- `a + " " + b`로 두 단어 사이에 공백 하나를 넣어 이어 붙인다. `a`가 `string`이라 리터럴 `" "`와도 `+`가 된다.
- 그 결과를 한 줄에 출력한다.

재작성 사고 순서: (1) 두 문자열 입력 받기 → (2) `a`, 공백, `b`를 차례로 concat → (3) 출력. 앞뒤에 여분 공백이 붙지 않도록 공백은 두 단어 사이에만 넣는다.
```

**2) n번 반복 문자열** · Medium

- **요구사항**: 문자열 `s`와 정수 `n`을 입력받아 `s`를 `n`번 이어 붙인 결과를 출력한다.
- **입력**: 첫 줄에 공백 없는 문자열 `s`, 둘째 줄에 정수 `n` (`n`은 0 이상)
- **출력**: `s`가 `n`번 반복된 문자열 한 줄
- **예제**: `ab`/`3` → `ababab` / `x`/`0` → (빈 줄)
- **셀프체크**: `n`이 0이면 아무 글자도 없는 빈 줄이 출력되어야 함. 반복문으로 `s`를 계속 이어 붙인다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    int n;
    cin >> n;
    string result = "";
    for (int i = 0; i < n; i++) {
        result = result + s;
    }
    cout << result << endl;
    return 0;
}
@@TESTS
--IN
ab
3
--OUT
ababab
--IN
x
0
--OUT

@@EXPL
접근: 같은 문자열을 여러 번 이어 붙이려면, 빈 결과 문자열에서 시작해 `n`번 반복하며 `s`를 계속 concat한다.

코드 진행:

- 문자열 `s`를 `getline`으로 받고, 반복 횟수 `n`은 `cin >> n`으로 받는다(정수).
- `string result = "";`로 빈 문자열을 준비한다.
- `for (int i = 0; i < n; i++)`로 `n`번 돌며 `result = result + s;`로 `s`를 이어 붙인다.
- `cout << result << endl;`로 결과를 한 줄에 출력한다.

재작성 사고 순서: (1) 문자열과 정수 입력 받기 → (2) 빈 결과에서 시작해 `n`번 concat → (3) 출력. `n`이 0이면 반복이 한 번도 돌지 않아 `result`가 빈 문자열이고, `endl`만 찍혀 빈 줄이 나온다.
```

**3) 점점 길어지는 계단** · Hard

- **요구사항**: 공백 없는 문자열 `s`를 입력받아, 첫 줄엔 `s`의 앞 1글자, 둘째 줄엔 앞 2글자 ... 마지막 줄엔 `s` 전체를 출력한다.
- **입력**: 첫 줄에 공백 없는 문자열 `s`
- **출력**: 길이 1부터 `len(s)`까지, 앞에서부터의 부분을 한 줄씩
- **예제**: `code` → `c`(줄바꿈)`co`(줄바꿈)`cod`(줄바꿈)`code`
- **셀프체크**: 각 줄은 이전 줄에 글자를 하나씩 더한 것. 빈 문자열에서 시작해 `s[i]`를 차례로 붙여 나가면 편하다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    string result = "";
    for (int i = 0; i < s.length(); i++) {
        result = result + s[i];
        cout << result << endl;
    }
    return 0;
}
@@TESTS
--IN
code
--OUT
c
co
cod
code
--IN
hi
--OUT
h
hi
@@EXPL
접근: 각 줄이 이전 줄에 글자 하나를 더한 모양이다. 그래서 결과 문자열을 계속 쌓아 나가면서, 한 글자를 붙일 때마다 그 상태를 출력한다.

코드 진행:

- 문자열 `s`를 받고 `string result = "";`로 시작한다.
- `for (int i = 0; i < s.length(); i++)`로 앞에서부터 인덱스를 돈다.
- 매 반복에서 `result = result + s[i];`로 다음 글자(char)를 이어 붙인다.
- 붙인 직후 `cout << result << endl;`로 현재까지의 조각을 한 줄 출력한다.

재작성 사고 순서: (1) 빈 결과 문자열 준비 → (2) 앞에서부터 한 글자씩 concat → (3) 붙일 때마다 바로 출력 → 반복. 출력이 `for` 안에 있어야 매 단계가 한 줄씩 찍힌다. `code`면 `c`, `co`, `cod`, `code` 순.
```

## L6. 문자열 찾기

**개념**

- 어떤 글자가 문자열 안에 있는지 확인하려면, 문자열을 순회하며 하나라도 같은 글자가 있는지 검사한다. 있으면 표시 변수를 켠다.
- 있으면 `true`, 없으면 `false`인 표시 변수(`bool found`)를 만들어 두면 `if` 조건에 바로 쓸 수 있다.
- 몇 번째 위치에 있는지(인덱스)까지 알고 싶으면, 문자열을 순회하며 처음 일치하는 위치를 직접 찾는다.
- 위치는 0부터 센다. 첫 글자에서 찾으면 0, 없으면 흔히 `-1`로 표시한다(직접 그렇게 정하기).
- 찾을 때 대소문자는 서로 다른 글자로 취급한다.

```cpp
string s = "banana";
char target = 'n';

// 포함 여부
bool found = false;
for (int i = 0; i < s.length(); i++) {
    if (s[i] == target) {
        found = true;
    }
}
if (found) cout << "found" << endl;

// 첫 등장 위치를 직접 찾기
int pos = -1;
for (int i = 0; i < s.length(); i++) {
    if (s[i] == target) {
        pos = i;
        break;
    }
}
cout << pos << endl;   // 2
```

> 선행: `bool`이 돌려주는 `true`/`false`는 조건문에서 배운 참/거짓 값이다. `if` 뒤에 그대로 쓸 수 있다.

**문제**

**1) 포함 여부 확인** · Easy

- **요구사항**: 공백 없는 문자열과 찾을 글자 하나를 입력받아, 그 글자가 문자열에 있으면 `YES`, 없으면 `NO`를 출력한다.
- **입력**: 첫 줄에 문자열, 둘째 줄에 찾을 글자 한 개
- **출력**: 있으면 `YES`, 없으면 `NO`
- **예제**: `apple`/`p` → `YES` / `apple`/`z` → `NO`
- **셀프체크**: 대소문자 구분에 주의(`A`와 `a`는 다름). 순회하며 하나라도 같으면 표시 변수를 켠다.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    char c;
    cin >> c;
    bool found = false;
    for (int i = 0; i < s.length(); i++) {
        if (s[i] == c) {
            found = true;
        }
    }
    if (found) {
        cout << "YES" << endl;
    } else {
        cout << "NO" << endl;
    }
    return 0;
}
@@TESTS
--IN
apple
p
--OUT
YES
--IN
apple
z
--OUT
NO
@@EXPL
접근: 어떤 글자가 문자열 안에 있는지만 판별하면 되므로, 순회하며 하나라도 같은 글자가 나오면 표시 변수 `found`를 켠다.

코드 진행:

- 문자열 `s`를 `getline`으로, 찾을 글자 `c`를 `cin >> c`로 받는다.
- `bool found = false;`로 시작한다.
- `for`로 각 글자를 돌며 `s[i] == c`이면 `found = true;`로 켠다.
- 순회 후 `found`가 참이면 `YES`, 아니면 `NO`를 출력한다.

재작성 사고 순서: (1) `found = false` 준비 → (2) 순회하며 같은 글자 찾으면 켜기 → (3) 참이면 YES, 거짓이면 NO 출력. 대소문자는 다른 글자로 취급되니 `apple`에서 대문자 `P`를 찾으면 NO가 된다.
```

**2) 처음 등장 위치** · Medium

- **요구사항**: 문자열과 찾을 글자를 입력받아, 그 글자가 처음 나타나는 위치(0부터 셈)를 출력한다. 없으면 `-1`을 출력한다.
- **입력**: 첫 줄에 문자열, 둘째 줄에 찾을 글자 한 개
- **출력**: 처음 등장 인덱스, 없으면 `-1`
- **예제**: `banana`/`a` → `1` / `banana`/`n` → `2` / `banana`/`z` → `-1`
- **셀프체크**: `banana`에서 `a`는 인덱스 1이 첫 등장(0은 `b`). 첫 등장을 찾으면 바로 멈춰야 함.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    char target;
    cin >> target;
    int pos = -1;
    for (int i = 0; i < s.length(); i++) {
        if (s[i] == target) {
            pos = i;
            break;
        }
    }
    cout << pos << endl;
    return 0;
}
@@TESTS
--IN
banana
a
--OUT
1
--IN
banana
n
--OUT
2
--IN
banana
z
--OUT
-1
@@EXPL
접근: "처음" 등장을 찾는 것이므로, 앞에서부터 순회하다가 처음 일치하는 순간 그 인덱스를 기록하고 `break`로 바로 멈춘다. 끝까지 못 찾으면 `-1`.

코드 진행:

- 문자열 `s`와 찾을 글자 `target`을 받는다.
- `int pos = -1;`로 시작한다(못 찾을 때의 값).
- `for`로 앞에서부터 돌며, `s[i] == target`이면 `pos = i;`로 기록하고 `break;`로 즉시 멈춘다.
- 반복이 끝나면 `pos`를 출력한다.

재작성 사고 순서: (1) `pos = -1` 준비 → (2) 앞에서부터 순회 → (3) 처음 일치하면 위치 기록 후 `break` → (4) 출력. `banana`의 `a`는 인덱스 0(`b`) 다음인 1에서 처음 만나므로 1이 나온다.
```

**3) 마지막 등장 위치** · Hard

- **요구사항**: 문자열과 찾을 글자를 입력받아, 그 글자가 마지막으로 나타나는 위치(0부터 셈)를 출력한다. 없으면 `-1`.
- **입력**: 첫 줄에 문자열, 둘째 줄에 찾을 글자 한 개
- **출력**: 마지막 등장 인덱스, 없으면 `-1`
- **예제**: `banana`/`a` → `5` / `banana`/`b` → `0` / `banana`/`z` → `-1`
- **셀프체크**: 순회 중 일치할 때마다 위치를 계속 갱신하면 마지막 값이 남는다(멈추지 않는다).

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    char target;
    cin >> target;
    int pos = -1;
    for (int i = 0; i < s.length(); i++) {
        if (s[i] == target) {
            pos = i;
        }
    }
    cout << pos << endl;
    return 0;
}
@@TESTS
--IN
banana
a
--OUT
5
--IN
banana
b
--OUT
0
--IN
banana
z
--OUT
-1
@@EXPL
접근: "마지막" 등장을 찾으려면 처음 찾았다고 멈추면 안 된다. 앞에서부터 끝까지 다 돌면서, 일치할 때마다 위치를 계속 갱신한다. 그러면 최종적으로 마지막 위치가 남는다.

코드 진행:

- 문자열 `s`와 찾을 글자 `target`을 받는다.
- `int pos = -1;`로 시작한다(못 찾으면 그대로 `-1`).
- `for`로 모든 인덱스를 돌며, `s[i] == target`이면 `pos = i;`로 덮어쓴다. `break`는 하지 않는다.
- 순회가 끝나면 마지막으로 갱신된 `pos`를 출력한다.

재작성 사고 순서: (1) 결과 `pos = -1` 준비 → (2) 처음부터 끝까지 순회 → (3) 일치할 때마다 위치 갱신(멈추지 않음) → (4) 출력. `banana`의 `a`는 인덱스 1,3,5에서 만나므로 마지막 값 5가 남는다.
```

## L7. 문자 수정

**개념**

- C++ 문자열은 `s[p] = 'x'`처럼 특정 위치의 글자를 직접 바꿀 수도 있다. 하지만 이 레슨에서는 "원본을 보고 새 문자열을 만드는" 방식으로 익힌다(다른 언어와 사고가 통하고, 조건에 따라 다른 글자를 넣기 좋기 때문).
- 방법: 문자열을 순회하면서, 바꿀 위치면 새 글자를, 아니면 원래 글자를 골라 하나씩 이어 붙인다.
- 빈 문자열 `""`에서 시작해 `for`로 돌며 조건에 따라 다른 글자를 concat하면 된다.
- 특정 위치를 바꾸려면 인덱스 `i`를 함께 봐야 하므로 `for (int i = 0; i < s.length(); i++)` 형태가 편하다.

```cpp
string s = "cat";
// 0번 글자를 h로 바꾼 새 문자열 만들기
string result = "";
for (int i = 0; i < s.length(); i++) {
    if (i == 0) {
        result = result + "h";
    } else {
        result = result + s[i];
    }
}
cout << result << endl;   // hat
```

**문제**

**1) 한 자리 바꾸기** · Medium

- **요구사항**: 문자열 `s`, 위치 `p`(0부터), 새 글자 `c`를 입력받아, `s`의 `p`번째 글자를 `c`로 바꾼 결과를 출력한다.
- **입력**: 첫 줄에 문자열 `s`, 둘째 줄에 정수 `p`, 셋째 줄에 글자 `c`
- **출력**: 바뀐 문자열 한 줄
- **예제**: `cat`/`0`/`h` → `hat` / `code`/`3`/`a` → `coda`
- **셀프체크**: `p` 위치만 바뀌고 나머지는 그대로여야 함.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    int p;
    cin >> p;
    cin.ignore();
    char c;
    cin >> c;
    string result = "";
    for (int i = 0; i < s.length(); i++) {
        if (i == p) {
            result = result + c;
        } else {
            result = result + s[i];
        }
    }
    cout << result << endl;
    return 0;
}
@@TESTS
--IN
cat
0
h
--OUT
hat
--IN
code
3
a
--OUT
coda
@@EXPL
접근: 원본을 보고 새 문자열을 만든다. 이번엔 위치 `p` 하나만 바꾸는 경우다. 순회 중 `i == p`인 자리에서만 새 글자를 넣고, 나머지는 원래 글자를 넣는다.

코드 진행:

- 문자열 `s`를 `getline`으로, 위치 `p`를 `cin >> p`로 받는다. `p` 뒤에는 `cin.ignore()`로 줄바꿈을 버린 뒤 새 글자 `c`를 `cin >> c`로 받는다.
- `string result = "";`로 시작해 `for`로 모든 자리를 돈다.
- `i == p`인 자리에서만 `c`를 붙이고, 나머지 자리는 원래 글자 `s[i]`를 붙인다.
- 순회 후 `result`를 출력한다.

재작성 사고 순서: (1) 세 입력 받기(위치는 정수) → (2) 빈 결과 문자열 → (3) 인덱스로 돌며 `i == p`면 새 글자, 아니면 원래 글자 concat → (4) 출력. `cat`의 0번을 `h`로 → `hat`.
```

**2) 특정 글자 모두 바꾸기** · Medium

- **요구사항**: 문자열과 바꿀 대상 글자 `a`, 새 글자 `b`를 입력받아, 문자열 속 모든 `a`를 `b`로 바꾼 결과를 출력한다.
- **입력**: 첫 줄에 문자열, 둘째 줄에 글자 `a`, 셋째 줄에 글자 `b`
- **출력**: 바뀐 문자열 한 줄
- **예제**: `banana`/`a`/`o` → `bonono` / `hello`/`z`/`x` → `hello`
- **셀프체크**: 대상 글자가 없으면 원본 그대로 나와야 함. 하나만 바꾸고 멈추면 안 된다(모두 바꾼다).

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    char a, b;
    cin >> a;
    cin >> b;
    string result = "";
    for (int i = 0; i < s.length(); i++) {
        if (s[i] == a) {
            result = result + b;
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
o
--OUT
bonono
--IN
hello
z
x
--OUT
hello
@@EXPL
접근: "모든" 대상 글자를 바꾸는 것이므로 순회 중 멈추지 않는다. 각 글자를 하나씩 검사해, 대상이면 새 글자를, 아니면 원래 글자를 새 문자열에 이어 붙인다.

코드 진행:

- 문자열 `s`를 `getline`으로 받고, 바꿀 대상 `a`와 새 글자 `b`를 각각 `cin >> a; cin >> b;`로 받는다. `>>`는 공백/줄바꿈을 건너뛰므로 두 글자를 순서대로 읽는다.
- `string result = "";`로 시작하고 `for`로 모든 자리를 돈다.
- `s[i] == a`이면 `result`에 `b`를 붙이고, 아니면 원래 글자 `s[i]`를 붙인다.
- 순회가 끝난 뒤 `result`를 출력한다.

재작성 사고 순서: (1) 세 입력 받기 → (2) 빈 결과 문자열 → (3) 각 글자 검사: 대상이면 새 글자, 아니면 그대로 concat(멈추지 않음) → (4) 출력. 대상이 하나도 없으면 모든 글자가 그대로 붙어 원본이 나온다.
```

**3) 짝수 자리만 대체** · Hard

- **요구사항**: 문자열을 입력받아, 인덱스가 짝수(0, 2, 4, ...)인 자리의 글자를 모두 `*`로 바꾼 결과를 출력한다.
- **입력**: 첫 줄에 공백 없는 문자열 하나
- **출력**: 짝수 인덱스가 `*`로 바뀐 문자열 한 줄
- **예제**: `abcde` → `*b*d*` / `hi` → `*i`
- **셀프체크**: 인덱스 0도 짝수라 첫 글자부터 바뀐다. `i % 2 == 0` 판별을 사용. 홀수 자리는 원래 글자 유지.

```runner
@@SOLUTION
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    string result = "";
    for (int i = 0; i < s.length(); i++) {
        if (i % 2 == 0) {
            result = result + "*";
        } else {
            result = result + s[i];
        }
    }
    cout << result << endl;
    return 0;
}
@@TESTS
--IN
abcde
--OUT
*b*d*
--IN
hi
--OUT
*i
@@EXPL
접근: 새 결과 문자열을 처음부터 만들어 나간다. 이번엔 글자 값이 아니라 "자리 번호(인덱스)"가 조건이므로 인덱스 `i`가 필요하다.

코드 진행:

- `string result = "";`로 빈 문자열에서 시작한다.
- `for (int i = 0; i < s.length(); i++)`로 0번부터 끝 번호까지 인덱스를 하나씩 돈다.
- `i % 2 == 0`이면 짝수 자리이므로 `"*"`를 붙이고, 아니면 원래 글자 `s[i]`를 붙인다.
- 다 돌면 `result`를 한 번 출력한다.

재작성 사고 순서: (1) 빈 결과 문자열 준비 → (2) 인덱스로 순회 → (3) 짝수 인덱스면 `*`, 홀수면 원래 글자를 concat → (4) 마지막에 출력. `abcde`는 인덱스 0,2,4가 `*`가 되어 `*b*d*`.
```
