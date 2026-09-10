## L4. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch05(스택·큐·덱)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. 스택의 "짝 맞추기·단조 스택", 큐의 "앞에서 꺼내 뒤로 보내는 시뮬레이션", 덱의 "양 끝 접근·단조 덱"을 소재만 바꿔 여러 번 다시 쓴다.
- **C++에서 가장 먼저 몸에 붙여야 할 차이**: `stack::pop()`·`queue::pop()`·`deque::pop_front()`는 **값을 돌려주지 않는다**. 파이썬의 `x = st.pop()`은 C++에서 `int x = st.top(); st.pop();` **두 줄**이다. 그리고 빈 컨테이너에 `top()`·`front()`·`back()`을 부르면 파이썬처럼 예외가 나는 게 아니라 **정의되지 않은 동작**(쓰레기 값이거나 프로그램이 죽음)이므로, 모든 접근 앞에 `if (!st.empty())`가 붙어야 한다.
- **반복 훈련 개념**:
  - 스택 짝 맞추기 — top과 비교해 짝이면 pop, 아니면 push: `if (!st.empty() && st.top() == c) st.pop();` / `else st.push(c);`
  - 단조 스택 — 새 값이 top을 "이기면" top을 pop하며 답을 확정: `while (!st.empty() && a[st.top()] <= a[i]) st.pop();`
  - 두 스택 되돌리기 — 취소한 것을 다른 스택에 보관: `redo.push(text.top()); text.pop();`. 스택을 통째로 비울 땐 `clear()`가 없으므로 `redo = stack<char>();`처럼 빈 것을 대입한다.
  - 큐 회전 시뮬레이션 — 앞에서 꺼내 뒤로 보내기: `q.push(q.front()); q.pop();`
  - 단조 덱 창 만료 — 인덱스를 담아 위치로 만료: `if (dq.front() <= i - k) dq.pop_front();`
- **컨테이너 고르기**: `stack<T>`·`queue<T>`는 순회가 안 된다(반복자가 없다). 마지막에 내용을 순서대로 출력해야 한다면 전부 꺼내 `reverse`하거나, 애초에 순회가 되는 `vector<T>`/`string`/`deque<T>`를 스택처럼(`back()`/`pop_back()`) 쓰면 된다.
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '스택·큐·덱' 단계, 프로그래머스 「코딩테스트 고득점 Kit」의 '스택/큐', NeetCode 150의 'Stack'.
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 짝지어 문자 지우기 | Easy | 스택 짝 맞추기 (`top()`+`pop()` 2단계) | 반복 훈련 |
| 2 | 첫 번째 괄호 오류 위치 | Easy | 스택 짝 맞추기(`pair`로 위치 저장) | 반복 훈련 |
| 3 | 원탁 술래 뽑기 | Easy | 큐 회전 시뮬레이션 | 반복 훈련 |
| 4 | 앞뒤 줄서기 | Easy | 덱 양 끝 삽입 | 반복 훈련 |
| 5 | 타자 되돌리기와 다시하기 | Medium | 두 스택 되돌리기 + 스택 비우기 | 반복 훈련 |
| 6 | 주가 스팬 | Medium | 단조 스택(왼쪽 방향) | 반복 훈련 |
| 7 | 중위 표기식을 후위 표기식으로 | Medium | 연산자 스택 | 유형 확장 (백준 '스택' 단계 스타일) |
| 8 | 라운드 로빈 작업 처리 | Medium | 큐 시뮬레이션(`pair` 원소) | 유형 확장 (프로그래머스 Kit '스택/큐' 스타일) |
| 9 | 회전 명령 최소 횟수 | Medium | 덱 양방향 회전 + `find` | 유형 확장 (백준 '덱' 단계 스타일) |
| 10 | 창 안 온도 변동폭 | Hard | 단조 덱 두 개 | 반복 훈련 |
| 11 | 히스토그램 최대 직사각형 | Hard | 단조 스택 + 파수꾼 + `long long` | 유형 확장 (NeetCode 'Stack' 스타일) |
| 12 | 카드 전쟁 | Hard | 큐 두 개 시뮬레이션 | 유형 확장 (백준 '큐' 단계 스타일) |

**문제**

**1) 짝지어 문자 지우기** · Easy

- **요구사항**: 소문자 문자열에서 "서로 인접한 같은 문자 두 개"를 찾아 지운다. 지운 뒤 양옆이 붙어 새로 인접한 같은 문자 쌍이 생기면 그것도 계속 지운다. 더 지울 쌍이 없을 때 남는 문자열을 구하라.
- **입력**: 한 줄에 소문자 문자열 S(1 ≤ |S| ≤ 100000).
- **출력**: 남은 문자열. 전부 지워졌으면 `EMPTY`.
- **예제**: `baabcc` → `EMPTY`  ·  `abbac` → `c`  ·  `abcab` → `abcab`
- **셀프체크**: `baabcc`를 손으로 — `aa` 지움 → `bbcc` → `bb` 지움 → `cc` → 지움 → 빈 문자열이 맞는가. 지운 뒤 "새로 붙는 쌍"을 다시 처음부터 훑지 않고, 스택 top과 새 문자를 비교하는 것만으로 처리했는가(문자열을 매번 `replace`/`erase`하면 O(n²)). 빈 스택에서 `st.top()`을 읽지 않도록 `!st.empty()`를 **먼저** 검사했는가(C++에서 이 실수는 예외가 아니라 정의되지 않은 동작이다). `aaa`처럼 홀수 개가 연속이면 한 글자가 남는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;

    stack<char> st;
    for (char c : s) {
        if (!st.empty() && st.top() == c) {
            st.pop();                    // 짝이 맞으면 둘 다 사라짐 (pop 은 값을 안 준다)
        } else {
            st.push(c);
        }
    }

    // stack 은 순회가 안 되므로 전부 꺼낸 뒤 뒤집는다
    string res;
    while (!st.empty()) {
        res += st.top();
        st.pop();
    }
    reverse(res.begin(), res.end());

    if (res.empty()) cout << "EMPTY" << '\n';
    else cout << res << '\n';
    return 0;
}
@@TESTS
--IN
baabcc
--OUT
EMPTY
--IN
abbac
--OUT
c
--IN
abcab
--OUT
abcab
--IN
aaa
--OUT
a
@@EXPL
(1) 접근·핵심 아이디어

- "지운 뒤 새로 붙는 쌍"은 결국 스택 top과 새 문자의 관계다. 왼쪽부터 문자를 쌓다가 top과 같은 문자가 오면 둘을 함께 없애면, 그 순간 top 아래 문자가 자동으로 다음 비교 대상이 되어 연쇄 삭제가 저절로 처리된다. 각 문자는 최대 한 번 push·한 번 pop이므로 O(n).

(2) 코드 단계별

- 빈 `stack<char> st`를 두고 문자열을 `for (char c : s)`로 한 글자씩 훑는다.
- `!st.empty() && st.top() == c`면 `st.pop()`(짝 제거), 아니면 `st.push(c)`. 조건의 순서가 중요하다 — `&&`는 왼쪽이 거짓이면 오른쪽을 아예 평가하지 않으므로(단락 평가), 빈 스택에서 `top()`이 호출되는 일이 없다.
- 끝나면 스택에 남은 문자가 곧 결과. 다만 `stack`은 반복자가 없어 `for`로 훑을 수 없으므로 전부 꺼내 문자열에 담고 `reverse`한다. `string`을 그대로 스택처럼(`push_back`/`back()`/`pop_back()`) 써도 되고, 그러면 뒤집을 필요가 없다.
- 비었으면 `EMPTY`. 삼항 연산자로 `res.empty() ? "EMPTY" : res`를 쓰면 `const char*`와 `string`의 타입이 달라 컴파일 오류가 나므로 `if`/`else`로 나눈다.

(3) 스스로 다시 짤 때 생각 순서

- "인접 쌍 제거의 연쇄"를 "top과 비교"로 바꿀 수 있는지 먼저 확인(문자열 `erase` 반복은 O(n²)로 시간 초과).
- 빈 스택에서 `st.top()`을 보지 않도록 `!st.empty() && ...` 순서를 지키기.
- 홀수 개 연속(`aaa`)은 한 글자가 남는다는 경계값으로 검산.
```

**2) 첫 번째 괄호 오류 위치** · Easy

- **요구사항**: `()[]{}` 세 종류 괄호로 된 문자열을 왼쪽부터 읽으며, 처음으로 잘못된 괄호의 위치(1-based)를 찾아라. "잘못됨"은 (a) 닫는 괄호를 만났는데 열린 괄호가 없거나 종류가 다른 경우 — 그 닫는 괄호의 위치, (b) 끝까지 (a)가 없었지만 닫히지 않은 여는 괄호가 남은 경우 — 남은 것 중 가장 나중에 열린 여는 괄호의 위치. 올바른 문자열이면 0.
- **입력**: 한 줄에 괄호 문자열 S(1 ≤ |S| ≤ 100000).
- **출력**: 위치 정수 하나(올바르면 0).
- **예제**: `([)]` → `3`  ·  `{(` → `2`  ·  `{[()]}` → `0`
- **셀프체크**: `([)]`에서 3번째 `)`가 top `[`와 종류가 달라 3인가. `{(`는 끝까지 오류가 없지만 위치 1·2가 남고, "가장 나중에 열린" 것은 top인 2인가. `(()`는 3번째 `)`가 2번째 `(`와 짝지어져 빠지고 1번째만 남으므로 답이 2가 아니라 1인가. 스택에 문자만 넣으면 위치를 알 수 없으니 `pair<char, int>`를 넣었는가(파이썬 튜플의 대응물). `]` 한 글자면 1인가. 문자열 인덱스 루프에서 `s.size()`는 부호 없는 타입이라 `int i`와 비교하면 경고가 나니 `(int)s.size()`로 캐스팅했는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;

    stack<pair<char, int>> st;           // (여는 괄호, 위치)
    for (int i = 0; i < (int)s.size(); i++) {
        char c = s[i];
        if (c == '(' || c == '[' || c == '{') {
            st.push(make_pair(c, i + 1));
        } else {
            char need = (c == ')') ? '(' : (c == ']' ? '[' : '{');
            if (st.empty() || st.top().first != need) {
                cout << i + 1 << '\n';   // 닫기 실패 지점
                return 0;
            }
            st.pop();
        }
    }

    cout << (st.empty() ? 0 : st.top().second) << '\n';
    return 0;
}
@@TESTS
--IN
([)]
--OUT
3
--IN
{(
--OUT
2
--IN
{[()]}
--OUT
0
--IN
]
--OUT
1
--IN
(()
--OUT
1
@@EXPL
(1) 접근·핵심 아이디어

- 괄호 검사의 스택 뼈대는 그대로 두고, "어디서 실패했는가"를 답하기 위해 스택에 문자와 함께 위치를 저장한다. 닫는 괄호가 실패하면 그 자리가 답이고, 다 훑고도 스택이 남으면 top의 위치(가장 나중에 열린 것)가 답이다. O(n).

(2) 코드 단계별

- 파이썬의 `enumerate(s, 1)` 대신 인덱스 `for (int i = 0; i < (int)s.size(); i++)`로 돌고 위치는 `i + 1`을 쓴다.
- 여는 괄호면 `st.push(make_pair(c, i + 1))`. C++17이면 `st.push({c, i + 1})`도 된다.
- 닫는 괄호면 스택이 비었거나 `st.top().first`가 대응 짝이 아니면 즉시 `i + 1`을 출력하고 `return 0`, 아니면 `st.pop()`.
- 루프가 끝나면 스택이 남았을 때 `st.top().second`, 아니면 0. 여기서는 두 갈래 모두 `int`라 삼항 연산자를 그대로 쓸 수 있다.

(3) 스스로 다시 짤 때 생각 순서

- 기존 YES/NO 검사에서 "실패 시점"을 반환하도록 바꾸는 것이 핵심이므로, 실패 지점 두 종류(닫기 실패 / 남은 열기)를 먼저 나눈다.
- 위치를 답해야 하니 스택 원소를 `pair<char, int>`로 확장(파이썬 튜플 → C++ `pair`). 값이 셋 이상이면 `tuple`이나 작은 `struct`.
- `st.empty() || st.top().first != need`의 순서를 지켜야 빈 스택에서 `top()`을 부르지 않는다 — `||`도 단락 평가라 왼쪽이 참이면 오른쪽을 보지 않는다.
- `{(`처럼 남은 여는 괄호가 여럿일 때 "맨 위"를 답한다는 정의를 정확히 따르기. `(()`는 짝이 맞은 2번이 이미 빠져 1번이 남는다.
```

**3) 원탁 술래 뽑기** · Easy

- **요구사항**: 1번부터 N번까지 N명이 원탁에 시계 방향으로 앉아 있다. 1번부터 세기 시작해 K번째 사람을 술래로 뽑아 원탁에서 내보내고, 그다음 사람부터 다시 1로 세어 K번째를 내보낸다. 모두 나갈 때까지 반복했을 때 내보낸 순서를 구하라.
- **입력**: 한 줄에 N과 K(1 ≤ K ≤ N ≤ 1000).
- **출력**: 내보낸 사람 번호 N개를 공백으로 구분해 한 줄.
- **예제**: `7 3` → `3 6 2 7 5 1 4`  ·  `5 1` → `1 2 3 4 5`
- **셀프체크**: `7 3`을 손으로 — 3 나감 → 4부터 세어 6 → 7부터 세어 2(7,1,2) → 4,5,7 중 7 → 1,4,5 중 5 → 1,4,1 중 1 → 4. 순서가 `3 6 2 7 5 1 4`가 맞는가. "K번째"는 앞의 K-1명을 뒤로 보낸 뒤(`q.push(q.front()); q.pop();`) 맨 앞을 꺼내는 것으로 구현했는가. C++ `queue::pop()`은 값을 돌려주지 않으므로 내보낼 사람을 기록할 땐 `q.front()`로 먼저 읽고 그다음 `q.pop()`을 하는 2단계인가. K=1이면 회전 없이 순서대로 나가는가. N=1이면 `1` 하나만 출력되는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;

    queue<int> q;
    for (int i = 1; i <= n; i++) q.push(i);

    vector<int> out;
    while (!q.empty()) {
        for (int t = 0; t < k - 1; t++) {
            q.push(q.front());           // K-1명은 뒤로 보냄
            q.pop();
        }
        out.push_back(q.front());        // K번째를 내보냄 (읽고 → 버리고)
        q.pop();
    }

    for (size_t i = 0; i < out.size(); i++) {
        if (i) cout << ' ';
        cout << out[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
7 3
--OUT
3 6 2 7 5 1 4
--IN
5 1
--OUT
1 2 3 4 5
--IN
1 1
--OUT
1
--IN
4 4
--OUT
4 1 3 2
@@EXPL
(1) 접근·핵심 아이디어

- 원탁은 "맨 앞을 맨 뒤로 보내는" 큐 회전으로 표현된다. K번째를 뽑는다는 것은 앞의 K-1명을 차례로 뒤로 보내고 맨 앞을 꺼내는 것과 같다. 한 명 내보낼 때마다 K번 이하의 O(1) 연산이므로 전체 O(NK).

(2) 코드 단계별

- `queue<int> q`에 1..N을 순서대로 `push`해 1번이 맨 앞이 되게 만든다.
- 큐가 빌 때까지: `k - 1`번 `q.push(q.front()); q.pop();`으로 회전하고, `q.front()`를 결과에 담은 뒤 `q.pop()`.
- 결과를 공백으로 이어 출력한다.
- `q.push(q.front())`는 "읽어서 뒤에 넣기"이고 그 뒤의 `q.pop()`이 "앞에서 지우기"다. 파이썬의 `q.append(q.popleft())` 한 줄이 C++에선 두 줄이 되는 이유가 `pop()`의 무반환이다.

(3) 스스로 다시 짤 때 생각 순서

- "K번째 = K-1번 회전 + 1번 제거"로 규칙을 분해.
- 카드 버리기(L2)와 달리 "마지막 한 명"이 아니라 "나가는 순서 전체"를 모아야 하므로 꺼낸 값을 `vector`에 누적.
- K=1(회전 0회), N=1(즉시 종료) 경계값을 확인. 사람 수가 줄어도 K가 큐 길이보다 클 수 있는데, 회전은 길이에 상관없이 그대로 돌리면 된다(`4 4` → 마지막 한 명도 3번 회전 후 자기 자신).
```

**4) 앞뒤 줄서기** · Easy

- **요구사항**: 처음에 줄은 비어 있다. 명령 `F 이름`은 그 사람이 줄 맨 앞에 서고, `B 이름`은 맨 뒤에 선다. 단, 이미 줄에 서 있는 이름이 또 오면 그 명령은 무시한다. 모든 명령을 처리한 뒤 줄을 앞에서부터 출력하라.
- **입력**: 첫 줄에 명령 수 Q(1 ≤ Q ≤ 100000), 이후 Q줄에 `F 이름` 또는 `B 이름`(이름은 소문자, 길이 ≤ 10).
- **출력**: 줄에 선 이름을 앞에서부터 공백으로 구분해 한 줄.
- **예제**: `4 / B kim / F lee / B park / F choi` → `choi lee kim park`  ·  `3 / B a / B a / F a` → `a`
- **셀프체크**: `F`는 `push_front`, `B`는 `push_back`으로 대응했는가(`vector`의 앞 삽입 `insert(v.begin(), x)`는 O(n)). 중복 판정을 덱을 훑어서(`find`, O(n)) 하지 않고 `set`/`unordered_set`으로 O(log n)·O(1)에 했는가. 첫 예제에서 `F`가 두 번이면 나중 명령(`choi`)이 더 앞에 서는가. 명령 문자를 `char`로 읽으면 공백 처리에 걸리니 `string`으로 읽고 `cmd == "F"`로 비교했는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;

    deque<string> line;
    set<string> seen;                    // 중복 판정 O(log n)
    for (int i = 0; i < q; i++) {
        string cmd, name;
        cin >> cmd >> name;
        if (seen.count(name)) continue;  // 이미 줄에 있으면 무시
        seen.insert(name);
        if (cmd == "F") line.push_front(name);
        else line.push_back(name);
    }

    bool first = true;
    for (const string& s : line) {       // deque 는 순회가 된다
        if (!first) cout << ' ';
        cout << s;
        first = false;
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
4
B kim
F lee
B park
F choi
--OUT
choi lee kim park
--IN
3
B a
B a
F a
--OUT
a
--IN
5
F b
F a
B c
F a
B d
--OUT
a b c d
--IN
1
F z
--OUT
z
@@EXPL
(1) 접근·핵심 아이디어

- 줄의 "맨 앞에 서기"와 "맨 뒤에 서기"는 `deque`의 `push_front`/`push_back`에 1:1로 대응한다. 둘 다 O(1)이라 명령 Q개를 O(Q)에 처리한다. 중복 이름 검사는 덱을 훑으면 O(n)이므로 별도 `set`으로 처리한다.

(2) 코드 단계별

- 빈 `deque<string> line`과 빈 `set<string> seen`을 준비한다.
- 명령마다 `seen.count(name)`이 1이면 건너뛰고, 아니면 `insert`한 뒤 `F`는 `push_front`, `B`는 `push_back`.
- 끝나면 덱을 앞에서부터 순회하며 공백으로 이어 출력한다. `stack`·`queue`와 달리 `deque`는 반복자가 있어 범위 기반 `for`로 훑을 수 있다.
- 순회에서 원소를 `const string&`로 받아 이름 문자열이 매번 복사되지 않게 한다.

(3) 스스로 다시 짤 때 생각 순서

- "양 끝 삽입"이라는 단어에서 `deque`를 고르고, `vector`의 앞 삽입(O(n))을 피한다.
- 중복 판정은 자료구조를 하나 더(`set`) 두는 게 정석 — 덱은 검색이 느리다. 순서가 필요 없으니 `unordered_set`으로 O(1)까지 줄여도 된다.
- `F`가 연속되면 나중 사람이 더 앞에 선다는 점을 첫 예제로 검산.
```

**5) 타자 되돌리기와 다시하기** · Medium

- **요구사항**: 빈 문서에 세 가지 명령을 순서대로 적용한다. `T c`는 문자 c를 문서 끝에 입력, `U`는 마지막으로 입력한 문자를 취소(문서에서 제거; 취소할 게 없으면 무시), `R`은 가장 최근에 취소한 문자를 다시 입력(다시 할 게 없으면 무시). 새 `T` 명령이 실행되면 그동안의 취소 기록은 모두 사라져 이후 `R`을 해도 아무 일도 일어나지 않는다. 최종 문서를 출력하라.
- **입력**: 첫 줄에 명령 수 Q(1 ≤ Q ≤ 100000), 이후 Q줄에 명령(`T c`의 c는 소문자 한 글자).
- **출력**: 최종 문서 문자열. 비어 있으면 `EMPTY`.
- **예제**: `5 / T a / T b / U / R / T c` → `abc`  ·  `6 / T a / T b / T c / U / U / R` → `ab`
- **셀프체크**: 문서 스택과 취소 스택 두 개를 두고, `U`는 문서→취소, `R`은 취소→문서로 옮겼는가(옮길 때마다 `top()`으로 읽고 `pop()`으로 버리는 2단계). 두 번째 예제에서 `U` 두 번으로 취소 스택이 `c` 아래 `b`가 top인 상태가 되어 `R` 한 번에 `b`가 돌아오는가. `T`가 오면 취소 스택을 비웠는가 — C++ `stack`에는 `clear()`가 없으니 `redo = stack<char>();`로 빈 스택을 대입한다(`T a / T b / U / T c / R` → `ac`). 빈 문서에서 `U`, 빈 취소 스택에서 `R`이 `empty()` 검사 덕에 조용히 무시되는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;

    stack<char> text;                    // 문서
    stack<char> redo;                    // 취소된 문자
    for (int i = 0; i < q; i++) {
        string cmd;
        cin >> cmd;
        if (cmd == "T") {
            string ch;
            cin >> ch;
            text.push(ch[0]);
            redo = stack<char>();        // 새 입력 → 다시하기 기록 소멸 (clear() 가 없다)
        } else if (cmd == "U") {
            if (!text.empty()) {
                redo.push(text.top());   // 읽고
                text.pop();              // 버리고
            }
        } else {                         // "R"
            if (!redo.empty()) {
                text.push(redo.top());
                redo.pop();
            }
        }
    }

    string res;
    while (!text.empty()) {
        res += text.top();
        text.pop();
    }
    reverse(res.begin(), res.end());

    if (res.empty()) cout << "EMPTY" << '\n';
    else cout << res << '\n';
    return 0;
}
@@TESTS
--IN
5
T a
T b
U
R
T c
--OUT
abc
--IN
6
T a
T b
T c
U
U
R
--OUT
ab
--IN
5
T a
T b
U
T c
R
--OUT
ac
--IN
2
U
R
--OUT
EMPTY
@@EXPL
(1) 접근·핵심 아이디어

- 되돌리기(undo)는 "가장 최근 것부터 되돌린다"라 스택이고, 다시하기(redo)는 "가장 최근에 취소한 것부터 복구한다"라 역시 스택이다. 문서 스택에서 pop한 것을 취소 스택에 push하고, redo는 반대로 옮기면 된다. 명령당 O(1), 전체 O(Q).

(2) 코드 단계별

- `stack<char> text`(문서)와 `stack<char> redo`(취소 기록) 두 개를 쓴다.
- `T c`: `text.push(ch[0])` 후 `redo = stack<char>();` — 새 입력이 들어오면 이전 취소 기록은 더 이상 유효하지 않다. C++ 컨테이너 어댑터인 `stack`은 `clear()`가 없어서 빈 임시 객체를 대입해 비운다(`while (!redo.empty()) redo.pop();`도 같은 뜻이지만 한 줄이 더 짧다).
- `U`: `text`가 비어 있지 않을 때만 `redo.push(text.top()); text.pop();`.
- `R`: `redo`가 비어 있지 않을 때만 `text.push(redo.top()); redo.pop();`.
- 끝나면 `text`를 꺼내 `reverse`해 출력, 비면 `EMPTY`.
- 명령을 `cin >> cmd`로 읽으면 공백·개행이 자동으로 넘어가므로 줄 단위 파싱이 필요 없다. `T`의 인자도 `string`으로 받아 첫 글자를 쓰면 안전하다.

(3) 스스로 다시 짤 때 생각 순서

- "취소한 것을 어디에 두면 다시 할 수 있나" → 두 번째 스택.
- 세 명령 중 어느 것이 어느 스택을 비우는지(`T`가 `redo`를 비움)를 규칙에서 먼저 확인 — 이걸 빠뜨리면 `ac`가 `acb`가 된다.
- 빈 스택 방어(`if (!text.empty())` / `if (!redo.empty())`)를 각 명령에 넣기. 파이썬이라면 `IndexError`로 즉시 드러나지만 C++에선 조용히 망가진다.
```

**6) 주가 스팬** · Medium

- **요구사항**: N일 동안의 주가가 순서대로 주어진다. i번째 날의 "스팬"은 그 날을 포함해, 그 날 바로 앞으로 거슬러 올라가며 주가가 i번째 날 이하였던 날이 연속해서 며칠인지다(자기보다 높은 날을 만나면 멈춤). 모든 날의 스팬을 구하라.
- **입력**: 첫 줄에 N(1 ≤ N ≤ 100000), 둘째 줄에 N개의 주가(1 ≤ 값 ≤ 10^9).
- **출력**: 스팬 N개를 공백으로 구분해 한 줄.
- **예제**: `7 / 100 80 60 70 60 75 85` → `1 1 1 2 1 4 6`  ·  `4 / 5 5 5 5` → `1 2 3 4`
- **셀프체크**: 6번째 날(75)을 손으로 — 60, 70, 60은 75 이하이고 80에서 멈추니 3+1=4가 맞는가. 매일 왼쪽으로 되짚으면 O(N²)이니, "왼쪽에서 처음으로 자기보다 높은 날"만 `stack<int>`(인덱스)로 찾아 `i - st.top()`을 답으로 했는가. 스택에서 뺄 조건이 `<=`(이하)라 같은 값(5 5 5 5)도 스팬에 포함되는가. 왼쪽에 더 높은 날이 없으면(`st.empty()`) `i + 1`(첫날부터 전부)인가. 주가가 10^9까지지만 비교만 하므로 `int`로 충분한가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> p(n);
    for (int i = 0; i < n; i++) cin >> p[i];

    stack<int> st;                       // 가격이 엄격히 내림차순인 인덱스 스택
    vector<int> out(n);
    for (int i = 0; i < n; i++) {
        while (!st.empty() && p[st.top()] <= p[i]) {
            st.pop();                    // 오늘 이하인 날은 앞으로도 벽이 못 됨
        }
        out[i] = st.empty() ? (i + 1) : (i - st.top());
        st.push(i);
    }

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << out[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
7
100 80 60 70 60 75 85
--OUT
1 1 1 2 1 4 6
--IN
4
5 5 5 5
--OUT
1 2 3 4
--IN
3
3 2 1
--OUT
1 1 1
--IN
5
1 2 3 4 5
--OUT
1 2 3 4 5
@@EXPL
(1) 접근·핵심 아이디어

- 스팬은 "왼쪽에서 처음으로 나보다 높은 날(벽)"까지의 거리다. 다음으로 큰 원소(L1)가 오른쪽을 봤다면 이 문제는 왼쪽을 본다. 스택에 "아직 벽이 될 가능성이 있는 날"의 인덱스를 가격 내림차순으로 유지하면, 오늘 이하인 날들은 pop해도 되고(오늘이 그 날들보다 높으니 이후 누구에게도 그 날들이 벽이 되지 못함) 남은 top이 곧 벽이다. 각 인덱스가 한 번 push·pop이라 O(N).

(2) 코드 단계별

- i를 0..n-1로 훑으며 `!st.empty() && p[st.top()] <= p[i]`인 동안 `st.pop()`.
- 스택이 남았으면 벽은 `st.top()`, 스팬은 `i - st.top()`; 비었으면 왼쪽에 벽이 없으니 `i + 1`.
- 오늘 인덱스 i를 `st.push(i)`.
- 삼항 연산자의 두 갈래가 모두 `int`라 그대로 쓸 수 있다.

(3) 스스로 다시 짤 때 생각 순서

- "연속해서 이하인 날 수" → "처음으로 초과인 날까지 거리"로 문제를 뒤집는다.
- 스택에 값이 아니라 **인덱스**를 넣어야 거리를 계산할 수 있다. C++ `stack`은 값을 꺼낼 때 `top()`/`pop()` 2단계지만, 여기선 `pop()` 전에 `st.top()`을 읽을 필요가 없어 while 루프가 깔끔하다.
- pop 조건 `<=` vs `<`: 같은 값도 스팬에 포함("이하")이므로 `<=`로 pop. 전부 같은 값이면 `1 2 3 4`가 나오는지로 검산.
```

**7) 중위 표기식을 후위 표기식으로** · Medium

- **요구사항**: 대문자 알파벳 한 글자짜리 피연산자, 연산자 `+ - * /`, 소괄호로 이루어진 중위 표기식을 후위 표기식으로 바꿔라. `*`,`/`가 `+`,`-`보다 우선하고, 우선순위가 같으면 왼쪽부터 계산한다(좌결합). 입력은 항상 올바른 식이며 공백이 없다.
- **입력**: 한 줄에 중위 표기식(길이 ≤ 100).
- **출력**: 후위 표기식 문자열(공백 없이).
- **예제**: `A+B*C` → `ABC*+`  ·  `(A+B)*C` → `AB+C*`  ·  `A-B-C` → `AB-C-`
- **셀프체크**: 연산자를 만나면 "스택 top의 우선순위가 지금 것 이상인 동안" 꺼내 출력했는가(`>=`라서 `A-B-C`가 `AB-C-`로 좌결합이 되는가; `>`로 쓰면 `ABC--`가 되어 틀림). `(`는 무조건 push하고, `)`를 만나면 `(`가 나올 때까지 꺼낸 뒤 `(`는 버렸는가. 스택 top이 `(`일 때는 우선순위 비교를 멈추는가. 끝나면 스택에 남은 연산자를 전부 꺼냈는가. 우선순위 표를 파이썬 `dict` 대신 작은 함수나 `map<char,int>`로 옮겼는가(문자 4종뿐이라 `if`로 충분하다).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int prec(char c) {                       // '+','-' 는 1, '*','/' 는 2
    if (c == '+' || c == '-') return 1;
    return 2;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;

    stack<char> st;                      // 연산자·여는 괄호 스택
    string out;
    for (char c : s) {
        if (isalpha((unsigned char)c)) {
            out += c;
        } else if (c == '(') {
            st.push(c);
        } else if (c == ')') {
            while (!st.empty() && st.top() != '(') {
                out += st.top();
                st.pop();
            }
            if (!st.empty()) st.pop();   // '(' 버림
        } else {
            while (!st.empty() && st.top() != '(' && prec(st.top()) >= prec(c)) {
                out += st.top();
                st.pop();
            }
            st.push(c);
        }
    }
    while (!st.empty()) {
        out += st.top();
        st.pop();
    }

    cout << out << '\n';
    return 0;
}
@@TESTS
--IN
A+B*C
--OUT
ABC*+
--IN
(A+B)*C
--OUT
AB+C*
--IN
A-B-C
--OUT
AB-C-
--IN
A*(B+C)/D
--OUT
ABC+*D/
--IN
A
--OUT
A
@@EXPL
(1) 접근·핵심 아이디어

- 피연산자는 순서가 바뀌지 않으므로 그대로 출력하고, 연산자만 스택에 "미뤄 두었다가" 자기보다 우선순위가 낮은 연산자가 오거나 괄호가 닫힐 때 내보낸다. 후위식에서는 먼저 계산될 연산자가 먼저 나와야 하므로, 새 연산자보다 우선순위가 같거나 높은 top들을 먼저 출력한다. 문자 하나당 push/pop 최대 한 번이라 O(n).

(2) 코드 단계별

- 알파벳이면 즉시 `out += c`. 판정은 `isalpha`인데 인자를 `(unsigned char)`로 캐스팅한다 — `char`가 음수일 수 있는 플랫폼에서 `isalpha`에 음수를 넘기면 정의되지 않은 동작이다.
- `(`는 무조건 push(괄호 안은 새로 시작).
- `)`는 `(`가 나올 때까지 pop해 출력하고 `(`는 버린다.
- 연산자면 `st.top()`이 `(`가 아니고 우선순위가 `>=`인 동안 pop해 출력한 뒤 push.
- 끝나면 남은 연산자를 전부 pop.
- 파이썬 원본은 `while st[-1] != '('`처럼 `empty()` 검사 없이 써도 `IndexError`로 드러나지만, C++에서는 조용히 망가지므로 모든 `top()` 앞에 `!st.empty()`를 둔다.

(3) 스스로 다시 짤 때 생각 순서

- "피연산자는 바로, 연산자는 미루기"라는 틀을 먼저 세운다.
- 좌결합을 위해 비교를 `>=`로 두어야 `A-B-C`가 `(A-B)-C` 순서로 나온다 — `>`면 오른쪽부터 계산되는 식이 된다.
- `(`는 우선순위 함수의 대상이 아니므로 비교 전에 `st.top() != '('` 검사를 반드시 앞에 둔다.
```

**8) 라운드 로빈 작업 처리** · Medium

- **요구사항**: 1번부터 N번 작업이 순서대로 큐에 들어 있고, 각 작업은 처리에 t_i 시간이 필요하다. 시각 0부터 다음을 반복한다 — 큐 맨 앞 작업을 꺼내 최대 Q만큼 실행하고(남은 시간이 Q보다 작으면 남은 만큼만), 아직 남았으면 큐 맨 뒤로 보내고 끝났으면 완료 처리한다. 각 작업이 완료되는 시각을 구하라.
- **입력**: 첫 줄에 N과 Q(1 ≤ N ≤ 1000, 1 ≤ Q ≤ 100), 둘째 줄에 t_1..t_N(1 ≤ t_i ≤ 1000).
- **출력**: 1번 작업부터 N번 작업까지의 완료 시각을 공백으로 구분해 한 줄.
- **예제**: `3 2 / 5 2 3` → `10 4 9`  ·  `2 10 / 3 4` → `3 7`
- **셀프체크**: 첫 예제를 손으로 — 1번 2실행(남3, t=2) → 2번 2실행(완료 t=4) → 3번 2실행(남1, t=6) → 1번 2실행(남1, t=8) → 3번 1실행(완료 t=9) → 1번 1실행(완료 t=10)이 맞는가. 큐에 `pair<int,int>`(작업 번호, 남은 시간)를 넣어야 어느 작업이 끝났는지 기록할 수 있는데 그렇게 했는가. 꺼낼 때 `q.front()`를 **복사해 두고** `q.pop()`을 했는가 — 참조로 받아 두고 `pop()`을 부르면 그 참조는 이미 사라진 원소를 가리켜 정의되지 않은 동작이 된다. 실행량은 `min(Q, 남은 시간)`인가. Q가 모든 t보다 크면 그냥 순서대로 누적합이 되는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, quantum;
    cin >> n >> quantum;
    vector<int> t(n);
    for (int i = 0; i < n; i++) cin >> t[i];

    queue<pair<int, int>> dq;            // (작업 번호, 남은 시간)
    for (int i = 0; i < n; i++) dq.push(make_pair(i, t[i]));

    vector<int> done(n, 0);
    int now = 0;
    while (!dq.empty()) {
        pair<int, int> cur = dq.front(); // 참조가 아니라 복사본으로 받고
        dq.pop();                        // 그 뒤에 버린다
        int i = cur.first, rem = cur.second;
        int run = min(quantum, rem);
        now += run;
        rem -= run;
        if (rem > 0) dq.push(make_pair(i, rem));   // 아직 남았으면 뒤로
        else done[i] = now;                        // 완료 시각 기록
    }

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << done[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
3 2
5 2 3
--OUT
10 4 9
--IN
2 10
3 4
--OUT
3 7
--IN
1 1
5
--OUT
5
--IN
3 1
1 1 1
--OUT
1 2 3
@@EXPL
(1) 접근·핵심 아이디어

- 라운드 로빈은 "앞에서 꺼내 조금 처리하고, 안 끝났으면 뒤로 보내는" 큐 시뮬레이션의 전형이다. 프린터 큐(L2)와 같은 골격이지만 이번엔 "우선순위"가 아니라 "남은 시간"이 재삽입 조건이다. 한 번 꺼낼 때마다 시각이 `min(Q, 남은)`만큼 흐르고, 총 반복 횟수는 `sum(t)/Q` 정도라 작다.

(2) 코드 단계별

- 큐에 `pair<int,int>`로 `(작업 번호, 남은 시간)`을 순서대로 넣는다(파이썬 튜플 → C++ `pair`).
- `pair<int,int> cur = dq.front();`로 **복사**한 뒤 `dq.pop()`. `const auto& cur = dq.front();`처럼 참조로 받고 `pop()`을 부르면 참조가 죽은 원소를 가리켜 값이 깨진다 — C++에서 자주 나오는 함정이다.
- `run = min(quantum, rem)`만큼 실행: `now += run`, `rem -= run`.
- `rem > 0`이면 뒤로 재삽입, 아니면 `done[i] = now`.
- 변수 이름을 `q`가 아니라 `quantum`으로 둔 이유는, 큐 변수와 이름이 헷갈리지 않게 하려는 것이다.

(3) 스스로 다시 짤 때 생각 순서

- "공평하게 조금씩 돌아가며"는 큐, "누가 끝났는지"는 번호를 함께 담아 해결.
- 시간이 흐르는 양을 `Q`가 아니라 `min(Q, 남은)`으로 두어야 마지막 조각에서 시각이 과다 증가하지 않는다.
- Q가 충분히 크면 재삽입이 한 번도 없고 답이 누적합(`3 7`)이 되는지로 검산.
```

**9) 회전 명령 최소 횟수** · Medium

- **요구사항**: 1..N이 순서대로 든 덱(맨 앞이 1)이 있다. 세 가지 연산을 쓸 수 있다 — (1) 맨 앞 원소를 뽑아 버린다, (2) 왼쪽 회전: 맨 앞 원소를 맨 뒤로 보낸다, (3) 오른쪽 회전: 맨 뒤 원소를 맨 앞으로 보낸다. 주어진 M개의 목표 원소를 그 순서대로 (1)번 연산으로 뽑아내고 싶다. 필요한 (2)·(3)번 연산 횟수의 합의 최솟값을 구하라.
- **입력**: 첫 줄에 N과 M(1 ≤ M ≤ N ≤ 50), 둘째 줄에 서로 다른 목표 M개.
- **출력**: 회전 횟수의 최솟값.
- **예제**: `10 3 / 2 9 5` → `8`  ·  `5 2 / 1 5` → `1`
- **셀프체크**: 첫 예제를 손으로 — 2는 왼쪽 1회, 뽑으면 `3..10 1`에서 9는 왼쪽 6회 vs 오른쪽 3회 → 3회, 뽑으면 `10 1 3 4 5 6 7 8`에서 5는 왼쪽 4회 vs 오른쪽 4회 → 4회, 합 8이 맞는가. C++ `deque`에는 파이썬의 `index()`가 없으니 `<algorithm>`의 `find(dq.begin(), dq.end(), x) - dq.begin()`으로 위치를 구했는가. 목표의 현재 위치 idx를 구한 뒤 `min(idx, len - idx)`로 방향을 골랐는가(뽑을 때마다 길이가 줄어 위치가 바뀌므로 매번 다시 찾기). 오른쪽 회전은 `push_front(back()); pop_back();`인가. 목표가 이미 맨 앞이면 0회인가. `dq.size()`는 부호 없는 타입이라 `(int)`로 캐스팅해 빼야 음수 계산이 어긋나지 않는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<int> targets(m);
    for (int i = 0; i < m; i++) cin >> targets[i];

    deque<int> dq;
    for (int i = 1; i <= n; i++) dq.push_back(i);

    int total = 0;
    for (int t = 0; t < m; t++) {
        int x = targets[t];
        // deque 에는 index() 가 없다 → find 로 위치를 구한다
        int idx = (int)(find(dq.begin(), dq.end(), x) - dq.begin());
        int left = idx;                          // 왼쪽 회전으로 앞까지 오는 횟수
        int right = (int)dq.size() - idx;        // 오른쪽 회전으로 앞까지 오는 횟수
        if (left <= right) {
            for (int c = 0; c < left; c++) {
                dq.push_back(dq.front());
                dq.pop_front();
            }
            total += left;
        } else {
            for (int c = 0; c < right; c++) {
                dq.push_front(dq.back());
                dq.pop_back();
            }
            total += right;
        }
        dq.pop_front();                          // 목표를 뽑아 버림
    }

    cout << total << '\n';
    return 0;
}
@@TESTS
--IN
10 3
2 9 5
--OUT
8
--IN
5 2
1 5
--OUT
1
--IN
3 3
1 2 3
--OUT
0
--IN
4 2
3 4
--OUT
2
@@EXPL
(1) 접근·핵심 아이디어

- 목표 하나를 맨 앞으로 데려오는 방법은 두 가지뿐이다: 왼쪽 회전을 idx번 하거나, 오른쪽 회전을 `len - idx`번 하거나. 각 목표마다 둘 중 작은 쪽을 택하는 것이 전체 최솟값이다(뽑는 순서가 고정돼 있어 목표마다 독립적으로 결정 가능). N ≤ 50이라 매번 `find`로 위치를 찾아도 충분하다.

(2) 코드 단계별

- `deque<int>`를 1..N으로 초기화.
- 목표 x마다 `find(dq.begin(), dq.end(), x)`로 반복자를 얻고 `- dq.begin()`으로 인덱스로 바꾼다. 파이썬의 `dq.index(x)`에 해당하는 C++ 관용구다.
- `left = idx`, `right = (int)dq.size() - idx`. `size()`가 부호 없는 타입이라 캐스팅 없이 빼면 결과 타입이 부호 없는 값이 되어 비교가 뒤틀릴 수 있다.
- 작은 쪽 방향으로 실제 회전(왼쪽은 `push_back(front()); pop_front();`, 오른쪽은 `push_front(back()); pop_back();`)하고 횟수를 더한다.
- 맨 앞에 온 목표를 `pop_front()`로 제거.

(3) 스스로 다시 짤 때 생각 순서

- "양방향 회전"이라는 말에서 `deque`의 네 연산(양 끝 넣기/빼기)을 떠올린다.
- 길이는 뽑을 때마다 줄어드니 위치와 오른쪽 횟수를 매번 다시 계산.
- 동률(`4 2 / 3 4`에서 idx=2, len=4)이면 어느 쪽이든 횟수는 같으므로 답에 영향이 없음을 확인.
```

**10) 창 안 온도 변동폭** · Hard

- **요구사항**: N개의 기온이 시간 순으로 주어진다. 연속한 K개를 묶은 창을 왼쪽 끝에서 오른쪽 끝까지 한 칸씩 옮기며, 각 창의 변동폭(창 안 최고 기온 − 최저 기온)을 구하라(창은 N−K+1개).
- **입력**: 첫 줄에 N과 K(1 ≤ K ≤ N ≤ 200000), 둘째 줄에 N개의 정수 기온(−100 ≤ 값 ≤ 100).
- **출력**: 창별 변동폭 N−K+1개를 공백으로 구분해 한 줄.
- **예제**: `6 3 / 4 2 7 1 5 3` → `5 6 6 4`  ·  `4 1 / 9 9 9 9` → `0 0 0 0`
- **셀프체크**: 첫 예제를 손으로 — `[4,2,7]`=7−2=5, `[2,7,1]`=6, `[7,1,5]`=6, `[1,5,3]`=4가 맞는가. 최댓값용 내림차순 덱과 최솟값용 오름차순 덱 두 개를 함께 굴렸는가(창마다 `max_element`·`min_element`를 부르면 O(NK)). 두 덱 모두 인덱스를 담아 `dq.front() <= i - k`로 만료시켰는가. 최솟값 덱은 뒤에서 빼는 조건이 `>=`(새 값 이상인 것 제거)로 방향이 반대인가. `dq.front()`·`dq.back()` 앞에 `!dq.empty()`를 붙였는가. K=1이면 전부 0인가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    deque<int> mx;                       // 값 내림차순 인덱스 → 앞이 최댓값
    deque<int> mn;                       // 값 오름차순 인덱스 → 앞이 최솟값
    vector<int> out;
    for (int i = 0; i < n; i++) {
        while (!mx.empty() && a[mx.back()] <= a[i]) mx.pop_back();
        mx.push_back(i);
        while (!mn.empty() && a[mn.back()] >= a[i]) mn.pop_back();
        mn.push_back(i);

        if (mx.front() <= i - k) mx.pop_front();   // 창을 벗어난 앞쪽 만료
        if (mn.front() <= i - k) mn.pop_front();

        if (i >= k - 1) out.push_back(a[mx.front()] - a[mn.front()]);
    }

    for (size_t i = 0; i < out.size(); i++) {
        if (i) cout << ' ';
        cout << out[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
6 3
4 2 7 1 5 3
--OUT
5 6 6 4
--IN
4 1
9 9 9 9
--OUT
0 0 0 0
--IN
3 3
-2 0 -5
--OUT
5
--IN
5 2
1 2 3 4 5
--OUT
1 1 1 1
@@EXPL
(1) 접근·핵심 아이디어

- 슬라이딩 윈도우 최댓값(L3)의 단조 덱을 "최솟값용"으로 한 번 더 만들어 두 덱을 같은 i에 대해 동시에 굴린다. 최댓값 덱은 값이 내림차순, 최솟값 덱은 오름차순이 되도록 뒤에서 정리하고, 앞은 창 범위로 만료시킨다. 각 인덱스가 각 덱에 한 번씩 들어갔다 나오므로 O(N).

(2) 코드 단계별

- `mx`: `a[mx.back()] <= a[i]`인 동안 `pop_back()` 후 `push_back(i)` → 앞이 최댓값.
- `mn`: `a[mn.back()] >= a[i]`인 동안 `pop_back()` 후 `push_back(i)` → 앞이 최솟값.
- 두 덱 모두 `front() <= i - k`면 `pop_front()`(창 밖 인덱스 제거). 이 시점엔 방금 `push_back(i)`을 했으므로 덱이 비어 있지 않음이 보장되지만, 습관적으로 `!dq.empty()`를 함께 두어도 좋다.
- `i >= k - 1`부터 `a[mx.front()] - a[mn.front()]`를 기록.
- 기온 범위가 −100..100이라 차이는 최대 200 — `int`로 충분하다. 값 범위가 컸다면 뺄셈에서 오버플로를 먼저 따져야 한다.

(3) 스스로 다시 짤 때 생각 순서

- "최대와 최소가 동시에 필요" → 단조 덱을 두 개, 부등호 방향만 반대로.
- 덱에 값이 아니라 인덱스를 담아야 두 덱이 같은 만료 규칙을 공유할 수 있다.
- `deque`는 `stack`·`queue`와 달리 `[]`와 반복자가 있어 `dq.front()` 대신 `dq[0]`으로도 읽을 수 있다 — 파이썬 원본의 `dq[0]`에 가장 가까운 표현이다.
- K=1(모든 창이 원소 하나 → 0), 전부 같은 값(0), 음수 포함 창(`-2 0 -5` → 5)으로 검산.
```

**11) 히스토그램 최대 직사각형** · Hard

- **요구사항**: 너비가 1인 막대 N개가 나란히 서 있고 각 막대의 높이가 주어진다. 막대들 안에 완전히 들어가는 직사각형(연속한 막대 구간 × 그 구간의 최소 높이) 중 가장 넓은 것의 넓이를 구하라.
- **입력**: 첫 줄에 N(1 ≤ N ≤ 100000), 둘째 줄에 높이 N개(0 ≤ 높이 ≤ 10^9).
- **출력**: 최대 넓이 정수 하나.
- **예제**: `7 / 2 1 4 5 1 3 3` → `8`  ·  `4 / 3 3 3 3` → `12`
- **셀프체크**: 첫 예제 — 높이 4·5 두 막대로 4×2=8, 3·3으로 3×2=6, 전체를 높이 1로 1×7=7 → 8이 맞는가. "각 막대를 높이로 하는 가장 넓은 직사각형"은 왼쪽·오른쪽에서 처음으로 자기보다 낮은 막대 사이 구간인데, 이를 단조(오름차순) 스택으로 O(N)에 구했는가. 배열 끝에 높이 0 파수꾼을 붙여 마지막에 스택에 남은 막대도 모두 정산되게 했는가. 너비는 `i - (스택의 새 top) - 1`(스택이 비면 `i`)인가. **넓이가 최대 10^9 × 10^5 = 10^14라 `int`로 두면 조용히 넘친다 — `long long`으로 두었는가.** 높이 0 막대 하나면 0인가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> h(n + 1);
    for (int i = 0; i < n; i++) cin >> h[i];
    h[n] = 0;                            // 끝에 높이 0 파수꾼

    stack<int> st;                       // 높이가 오름차순인 인덱스 스택
    long long best = 0;                  // 최대 1e9 * 1e5 = 1e14 → long long
    for (int i = 0; i <= n; i++) {
        while (!st.empty() && h[st.top()] >= h[i]) {
            int top = st.top();          // 읽고
            st.pop();                    // 버리고 (pop 은 값을 안 준다)
            long long left = st.empty() ? -1 : (long long)st.top();
            long long width = (long long)i - left - 1;
            long long area = h[top] * width;
            if (area > best) best = area;
        }
        st.push(i);
    }

    cout << best << '\n';
    return 0;
}
@@TESTS
--IN
7
2 1 4 5 1 3 3
--OUT
8
--IN
4
3 3 3 3
--OUT
12
--IN
1
0
--OUT
0
--IN
5
1 2 3 4 5
--OUT
9
@@EXPL
(1) 접근·핵심 아이디어

- 어떤 막대 t를 "높이"로 삼는 최대 직사각형은, t의 왼쪽·오른쪽에서 처음으로 t보다 낮은 막대 직전까지 뻗는다. 스택에 높이 오름차순으로 인덱스를 쌓아 두면, 새 막대 i가 top보다 낮아지는 순간 top의 오른쪽 경계는 i, 왼쪽 경계는 스택의 그 아래 원소로 확정된다. 끝에 높이 0을 붙이면 마지막엔 모든 막대가 pop되어 정산된다. 각 막대가 한 번 push·pop이므로 O(N).

(2) 코드 단계별

- `vector<long long> h(n + 1)`에 높이를 읽고 `h[n] = 0`으로 파수꾼을 둔다. 크기를 `n + 1`로 잡아 두면 파수꾼 자리를 따로 `push_back`할 필요가 없다.
- i를 0..n까지 훑으며 `h[st.top()] >= h[i]`인 동안: `int top = st.top(); st.pop();`으로 두 단계로 꺼내고, `left`(남은 top 또는 -1)로 너비 `i - left - 1`을 구해 `h[top] * width`를 `best`와 비교.
- i를 push.
- **타입이 이 문제의 정답을 가른다.** 높이 10^9, 너비 10^5이면 곱이 10^14로 `int`(약 2.1×10^9)를 훌쩍 넘는다. 넘쳐도 예외가 없고 음수 쓰레기가 나올 뿐이라 테스트가 조용히 틀린다. `h`를 `long long`으로 두면 `h[top] * width`가 자동으로 `long long` 곱셈이 된다.

(3) 스스로 다시 짤 때 생각 순서

- 완전 탐색(모든 구간의 최소 높이)은 O(N²) → "막대마다 자기가 최소인 최대 구간"으로 관점을 바꾼다.
- 오름차순 스택에서 "내려가는 순간"이 경계 확정 시점.
- 파수꾼 없이 끝내면 오름차순으로만 이어진 `1 2 3 4 5`에서 아무것도 정산되지 않아 0이 나온다 — 반드시 마지막에 0을 붙일 것. 같은 높이(`3 3 3 3`)는 `>=`로 pop되어도 마지막 막대가 전체 너비를 정산하므로 12가 맞게 나온다.
```

**12) 카드 전쟁** · Hard

- **요구사항**: A와 B가 각자 카드 더미를 들고 있다(맨 위부터 순서대로 주어짐). 매 라운드 두 사람이 더미 맨 위 카드를 한 장씩 낸다. 숫자가 큰 쪽이 이기고, 이긴 사람은 두 카드를 "자기 카드 먼저, 상대 카드 나중" 순서로 자기 더미 맨 아래에 넣는다. 숫자가 같으면 두 카드 모두 버린다. 한쪽의 더미가 비거나 R라운드를 채우면 게임이 끝난다. 끝났을 때 카드가 더 많은 사람이 승자다.
- **입력**: 첫 줄에 A의 카드 수 n, B의 카드 수 m, 최대 라운드 R(1 ≤ n, m ≤ 50, 1 ≤ R ≤ 10000), 둘째 줄에 A의 카드 n개, 셋째 줄에 B의 카드 m개(카드 값 1~100).
- **출력**: 승자(`A` 또는 `B`, 카드 수가 같으면 `DRAW`)와 진행된 라운드 수를 공백으로 구분해 한 줄.
- **예제**: `2 2 10 / 5 1 / 3 8` → `B 6`  ·  `1 1 5 / 4 / 4` → `DRAW 1`
- **셀프체크**: 첫 예제를 손으로 — (5 vs 3) A: `1 5 3`, B: `8` → (1 vs 8) A: `5 3`, B: `8 1` → (5 vs 8) A: `3`, B: `1 8 5` → (3 vs 1) A: `3 1`, B: `8 5` → (3 vs 8) A: `1`, B: `5 8 3` → (1 vs 5) A 빔 → B가 6라운드에 승리가 맞는가. 이긴 카드를 먼저 넣고 진 카드를 나중에 넣는 순서를 지켰는가(순서가 바뀌면 이후 전개가 달라짐). 카드를 꺼낼 때 `front()`로 읽고 `pop()`으로 버리는 2단계인가. 종료 조건 세 가지(A 빔, B 빔, R 도달)를 `while` 조건 하나로 묶었는가. 비긴 라운드도 라운드 수에 세는가. 마지막 승자 판정에서 `a.size() > b.size()`는 부호 없는 값끼리의 비교라 안전하지만, `a.size() - b.size()`처럼 빼면 음수가 거대한 양수가 되니 쓰지 않았는가. R에 걸려 끝났을 때 카드 수가 같으면 `DRAW`인가(`2 2 2 / 5 1 / 3 8` → `DRAW 2`).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, r;
    cin >> n >> m >> r;
    queue<int> a, b;
    for (int i = 0; i < n; i++) { int x; cin >> x; a.push(x); }
    for (int i = 0; i < m; i++) { int x; cin >> x; b.push(x); }

    int rounds = 0;
    while (!a.empty() && !b.empty() && rounds < r) {
        int x = a.front(); a.pop();      // 읽고 → 버리고
        int y = b.front(); b.pop();
        rounds++;
        if (x > y) {
            a.push(x); a.push(y);        // 이긴 카드 먼저, 진 카드 나중
        } else if (y > x) {
            b.push(y); b.push(x);
        }
        // 같으면 두 장 모두 버림
    }

    if (a.size() > b.size()) cout << "A " << rounds << '\n';
    else if (b.size() > a.size()) cout << "B " << rounds << '\n';
    else cout << "DRAW " << rounds << '\n';
    return 0;
}
@@TESTS
--IN
2 2 10
5 1
3 8
--OUT
B 6
--IN
1 1 5
4
4
--OUT
DRAW 1
--IN
2 1 1
9 9
1
--OUT
A 1
--IN
2 2 2
5 1
3 8
--OUT
DRAW 2
@@EXPL
(1) 접근·핵심 아이디어

- 카드 더미는 "위에서 내고 아래로 넣는" 큐다. 두 더미를 `queue<int>` 두 개로 두고, 라운드마다 앞에서 한 장씩 빼 비교한 뒤 승자 큐에 두 장을 순서대로 `push`한다. 규칙만 정확히 옮기면 되는 시뮬레이션이며, 라운드 수 R이 상한이라 최대 R번 반복으로 종료가 보장된다. O(R).

(2) 코드 단계별

- 두 큐 `a`, `b`를 입력 순서(맨 위가 앞)로 만든다.
- `while (!a.empty() && !b.empty() && rounds < r)`: 둘 다 카드가 있고 라운드가 남았을 때만 진행. 이 조건 하나가 빈 큐에서 `front()`를 부르는 정의되지 않은 동작을 원천 차단한다.
- `int x = a.front(); a.pop();`로 한 장씩 꺼내 비교: 큰 쪽이 `자기 카드, 상대 카드` 순으로 뒤에 넣고, 같으면 아무 곳에도 넣지 않는다(버림).
- 루프가 끝나면 `a.size()`와 `b.size()`를 비교해 승자와 `rounds`를 출력. `size()`는 부호 없는 타입이라 크기 **비교**는 안전하지만 뺄셈은 위험하다.

(3) 스스로 다시 짤 때 생각 순서

- "맨 위에서 내고 맨 아래로 넣기" → 큐 두 개.
- 종료 조건 세 가지를 `while` 조건 하나로 묶으면 빈 큐 접근이 원천 차단된다 — 파이썬은 `IndexError`로 알려 주지만 C++은 알려 주지 않으므로 이 습관이 더 중요하다.
- 이긴 카드/진 카드의 삽입 순서와 "비기면 버림"이 이후 전개를 바꾸는 함정. R 상한에 걸려 끝나는 경우(`DRAW 2`)와 첫 라운드에 끝나는 경우(`A 1`)로 검산.
```
