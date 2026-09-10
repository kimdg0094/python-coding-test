## L5. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 레슨은 Ch05(스택·큐·덱) 전체를 한 장으로 묶는 정리다. 세 자료구조는 서로 다른 발명품이 아니라 **"한 줄로 늘어선 데이터에서 어느 끝을 만질 수 있는가"** 하나의 질문에 대한 세 가지 답이다.
- 스택은 한쪽 끝만, 큐는 양 끝을 하나씩 나눠서, 덱은 양쪽 끝을 모두 쓴다. 그리고 "들어온 순서"가 아니라 **"값의 크기 순서"**로 꺼내야 하면 그때 힙(`priority_queue`)으로 넘어간다. 이 갈림길을 표로 못 박는 것이 이 레슨의 목적이다.
- C++에서 이들은 전부 **컨테이너 어댑터**다. `stack`·`queue`·`priority_queue`는 스스로 데이터를 담지 않고 `vector`나 `deque` 위에 얹혀 "쓸 수 있는 문"만 제한한다. 그래서 세 가지 공통 규칙이 따라붙는다 — (1) `pop()`은 값을 돌려주지 않는다, (2) 빈 컨테이너에 `top()`/`front()`를 부르면 미정의 동작이다, (3) 반복자가 없어 중간을 훑을 수 없다.

**개념 지도**

- 먼저 전체 지도다. 위에서 아래로 "어느 끝을 만지나 -> 무슨 문제에 쓰나"로 읽는다.

```text
  Ch05 map : linear containers -- which END may I touch ?

                     deque  (both ends, O(1) each)
                       |
      +----------------+----------------+
      |                |                |
    STACK            QUEUE         MONOTONIC use
    one end          two ends      keep it sorted inside
    LIFO             FIFO          front = current answer
      |                |                |
  push_back /      push /           stack -> next greater
  pop_back         front + pop      deque -> window max
  a vector is fine                       |
      |                |                |
  nesting          arrival order    "this one can never win
  undo / redo      BFS by layer      again"  ->  drop it now
  postfix eval     round robin
      |
      +-- order by PRIORITY, not by arrival  ->  priority_queue
            push / pop O(log n),  top O(1)
            default is a MAX heap            # python heapq 와 반대
```

- 덱의 그림 한 장이면 스택과 큐가 왜 그 특수한 경우인지 바로 보인다. 문은 네 개고, 어느 문을 쓰느냐가 이름을 정한다.

```text
      push_front              push_back
           v                      v
        +------+------+------+------+
        |  10  |  20  |  30  |  40  |
        +------+------+------+------+
           ^                      ^
        pop_front               pop_back

  push_back + pop_back   -> STACK  (LIFO)   # 오른쪽 문 두 개만 쓴다
  push_back + pop_front  -> QUEUE  (FIFO)   # 넣는 문과 나오는 문이 반대
  all four doors         -> DEQUE           # 회문.회전.단조 덱
  v.erase(v.begin())     -> O(n) trap       # 큐를 vector 로 만들면 안 되는 이유
```

- 단조 스택은 "밀려나는 순간 답이 확정된다"는 한 문장이 전부다. 스택에는 **답이 아직 안 정해진 인덱스**만 남는다.

```text
  monotonic stack : "next greater" is settled at the moment of pop

  arr = [2, 1, 5, 3, 4]
  i=0  push 0                     stack : 0
  i=1  push 1  (1 < 2)            stack : 0 1
  i=2  5 pops 1 then 0            ans[1]=5, ans[0]=5    stack : 2
  i=3  push 3  (3 < 5)            stack : 2 3
  i=4  4 pops 3                   ans[3]=4              stack : 2 4
  end  leftovers 2 and 4          ans[2]=-1, ans[4]=-1
  # 각 원소는 평생 한 번 push, 많아야 한 번 pop -> 전체 O(n)
```

- C++만의 공통 규칙 하나는 따로 그려 둘 값어치가 있다. **읽는 문과 버리는 문이 다르다.**

```text
  read and discard are two separate calls
  ---------------------------------------------------------
   container        peek            remove
   vector           v.back()        v.pop_back()
   stack            st.top()        st.pop()
   queue            q.front()       q.pop()
   deque            dq.front()      dq.pop_front()
   priority_queue   pq.top()        pq.pop()
   int x = st.pop();      # 컴파일 에러 : pop 의 반환형은 void
   int x = st.top(); st.pop();      # 항상 이 2 단계로 쓴다
```

**뼈대 코드**

- (1) 괄호 검사 — 세 종류를 짝 표로 한꺼번에.

```cpp
bool check(const string& s) {
    unordered_map<char, char> pair_of = {{')', '('}, {']', '['}, {'}', '{'}};
    vector<char> st;                              // 스택 = vector
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            st.push_back(c);
        } else if (pair_of.count(c)) {            // count 로 확인 (find 도 가능)
            if (st.empty() || st.back() != pair_of[c]) return false;
            st.pop_back();                        // 빈 검사가 먼저! 종류까지 비교
        }
    }
    return st.empty();                            // 끝에 남아 있으면 안 닫힌 것
}
```

- (2) 후위 표기식 계산 — 피연산자는 쌓고, 연산자를 만나면 위에서 둘을 꺼낸다.

```cpp
long long evalPostfix(const vector<string>& tokens) {
    vector<long long> st;                         // 오버플로 대비로 long long
    for (const string& t : tokens) {
        if (t != "+" && t != "-" && t != "*" && t != "/") {
            st.push_back(stoll(t));               // 피연산자 판별은 문제마다 바뀜
        } else {
            long long b = st.back(); st.pop_back();  // 나중에 넣은 것이 오른쪽
            long long a = st.back(); st.pop_back();  // 먼저 넣은 것이 왼쪽
            if      (t == "+") st.push_back(a + b);
            else if (t == "-") st.push_back(a - b);  // 순서를 바꾸면 뺄셈이 틀린다
            else if (t == "*") st.push_back(a * b);
            else               st.push_back(a / b);
        }
    }
    return st.back();                             // 마지막 하나가 최종 결과
}
```

- (3) 모노토닉 스택 — "다음으로 큰 수". **값이 아니라 인덱스를 담는다.**

```cpp
vector<int> nextGreater(const vector<int>& arr) {  // 참조로 받아 복사를 막는다
    int n = (int)arr.size();
    vector<int> ans(n, -1);                        // 없을 때의 값은 문제마다 바뀜
    vector<int> st;                                // 답이 아직 안 정해진 '인덱스'
    for (int i = 0; i < n; i++) {
        while (!st.empty() && arr[st.back()] < arr[i]) {  // 같을 때 pop 할지는 문제마다
            ans[st.back()] = arr[i];               // 밀려나는 순간 답이 확정
            st.pop_back();                         // 읽고 나서 버린다
        }
        st.push_back(i);
    }
    return ans;                                    // 스택에 남은 것들은 -1 그대로
}
```

- (4) 큐와 덱의 기본 연산 — `vector`의 앞 삭제 대신 `queue`/`deque`.

```cpp
queue<int> q;
q.push(x);               // 뒤에 넣기      O(1)
int front = q.front();   // 맨 앞 엿보기   O(1)
q.pop();                 // 앞에서 빼기    O(1)   <- vector 의 erase(begin()) 은 O(n)

deque<int> dq;
dq.push_front(x);        // 앞에 넣기      O(1)
int back = dq.back();    // 맨 뒤 엿보기   O(1)
dq.pop_back();           // 뒤에서 빼기    O(1)
int mid = dq[3];         // 임의 접근      O(1)   <- 파이썬 deque 는 O(n)

while (!q.empty()) {     // 비었는지 검사는 반드시 꺼내기 '전에'
    int cur = q.front(); q.pop();
}
```

- (5) 슬라이딩 윈도우 최댓값 — 단조 덱. 네 단계의 순서가 곧 불변식이다.

```cpp
vector<int> windowMax(const vector<int>& arr, int k) {
    deque<int> dq;                                 // 인덱스만, 값은 내림차순 유지
    vector<int> out;
    for (int i = 0; i < (int)arr.size(); i++) {
        while (!dq.empty() && arr[dq.back()] <= arr[i])
            dq.pop_back();                         // (1) 뒤에서 못 이길 것들을 버린다
        dq.push_back(i);                           // (2) 새 인덱스를 넣는다
        if (dq.front() <= i - k) dq.pop_front();   // (3) 앞에서 창을 벗어난 것을 버린다
        if (i >= k - 1) out.push_back(arr[dq.front()]);  // (4) 맨 앞이 최댓값
    }
    return out;
}
```

- (6) 회전 명령 처리 — 한 칸씩 옮기거나 `std::rotate`를 쓴다.

```cpp
deque<int> dq;
for (int i = 1; i <= n; i++) dq.push_back(i);

int frontVal = dq.front(); dq.pop_front(); dq.push_back(frontVal);  // 왼쪽 1칸 O(1)
int backVal  = dq.back();  dq.pop_back();  dq.push_front(backVal);  // 오른쪽 1칸 O(1)

// 특정 값을 맨 앞으로 가져오는 최소 회전 수 (양방향 중 짧은 쪽)
int idx = (int)(find(dq.begin(), dq.end(), target) - dq.begin());   // 탐색은 O(n)
int leftCost = idx, rightCost = (int)dq.size() - idx;
if (leftCost <= rightCost) rotate(dq.begin(), dq.begin() + idx, dq.end());
else                       rotate(dq.begin(), dq.end() - rightCost, dq.end());
```

- (7) 우선순위 큐 — 도착 순서가 아니라 값의 크기로 꺼낸다.

```cpp
priority_queue<int> maxh;                                     // 기본은 최대 힙
maxh.push(5); maxh.push(1);
int biggest = maxh.top(); maxh.pop();                         // 5

priority_queue<int, vector<int>, greater<int>> minh;          // 최소 힙
minh.push(5); minh.push(1);
int smallest = minh.top(); minh.pop();                        // 1

using P = pair<int,int>;                                      // (비용, 번호)
priority_queue<P, vector<P>, greater<P>> pq;                  // 비용이 작은 것부터
pq.push({7, 3});
pq.push({2, 5});
P best = pq.top(); pq.pop();                                  // {2, 5}
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 중첩된 짝을 맞춘다(괄호·태그) | `vector` 또는 `stack` | 닫는 것의 짝은 언제나 "가장 최근에 열린 것" | O(n) |
| 되돌리기·다시하기 | 스택 두 개 | 취소한 것을 다른 스택에 옮겨 두면 순서가 보존됨 | 연산당 O(1) |
| 후위 표기식 계산·수식 처리 | `vector`(스택) | 피연산자를 쌓다가 연산자에서 둘만 꺼내면 됨 | O(n) |
| 각 원소의 "다음(이전)으로 큰/작은 값" | 모노토닉 스택 | 밀려나는 순간 답이 확정돼 다시 볼 필요가 없음 | O(n) |
| 히스토그램·직사각형 넓이류 | 모노토닉 스택 + 파수꾼 | 높이가 낮아지는 지점이 곧 구간의 끝 | O(n) |
| 도착한 순서대로 공정하게 처리 | `queue` | 먼저 들어온 것이 먼저 나가는 것이 곧 규칙 | 연산당 O(1) |
| 층·단계 단위로 퍼지는 탐색(BFS) | `queue` | 큐 안의 원소가 항상 같은 층에 있음 | O(n) |
| 앞에서 꺼내 뒤로 보내는 회전 | `deque` 또는 `std::rotate` | `pop_front` + `push_back`이 한 바퀴를 그대로 표현 | 회전당 O(1) |
| 양 끝에서 넣고 빼야 한다(회문·앞뒤 줄서기) | `deque` | 네 연산이 모두 O(1)이라 방향 전환이 공짜 | 연산당 O(1) |
| 고정 크기 창의 최댓값·최솟값 | 단조 `deque` | 뒤로는 후보 정리, 앞으로는 만료 처리가 동시에 필요 | O(n) |
| 창마다 값이 바뀌고 크기도 바뀐다 | `priority_queue` + 지연 삭제 | 만료를 위치로 판단할 수 없어 우선순위가 필요 | O(n log n) |
| 도착 순서가 아니라 **값의 크기** 순으로 꺼낸다 | `priority_queue` | 전체 정렬을 포기하는 대신 삽입·삭제를 싸게 만듦 | 연산당 O(log n) |
| 남은 것 중 항상 최대만 필요 | `priority_queue<T>` | 기본이 최대 힙이라 그대로 쓰면 된다 | 조회 O(1) |
| 남은 것 중 항상 최소만 필요 | `priority_queue<T, vector<T>, greater<T>>` | 비교자를 바꿔야 최소 힙이 된다 | 조회 O(1) |
| 중간 원소를 자주 읽어야 한다 | `vector` | 어댑터(`stack`/`queue`)는 반복자가 아예 없다 | 읽기 O(1) |
| 컨테이너를 순회하며 출력해야 한다 | `vector`/`deque` | `stack`/`queue`/`priority_queue`는 순회가 불가능 | O(n) |

- 연산별 비용을 한 표로 비교하면 선택이 더 분명해진다. **같은 코드 모양인데 비용이 다른 칸**이 함정이다.

| 연산 | `vector` | `deque` | `stack`/`queue` | `priority_queue` |
|---|---|---|---|---|
| 뒤에 넣기 | 분할상환 O(1) | O(1) | `push` O(1) | 삽입 O(log n) |
| 뒤에서 빼기 | O(1) | O(1) | `stack::pop` O(1) | — |
| 앞에 넣기 | **O(n)** | O(1) | 불가 | — |
| 앞에서 빼기 | **O(n)** | O(1) | `queue::pop` O(1) | 극값 제거 O(log n) |
| 양 끝 엿보기 | `front`/`back` O(1) | O(1) | `top`/`front` O(1) | 극값 조회 O(1) |
| i번째 읽기 | O(1) | O(1) | **불가**(반복자 없음) | 의미 없음 |
| 순회 | O(n) | O(n) | **불가** | **불가** |
| 회전 k칸 | O(n) | 한 칸당 O(1) | 불가 | — |

- 파이썬에서 옮겨 올 때 특히 어긋나는 칸만 따로 모으면 이렇다.

| 파이썬 | C++ | 어긋나는 지점 |
|---|---|---|
| `st.pop()`이 값을 반환 | `st.pop()`은 `void` | `top()`으로 읽고 `pop()`으로 버리는 2단계 |
| 빈 스택 `pop()` → `IndexError` | 빈 스택 `pop()` → **미정의 동작** | 예외가 안 나니 직접 `empty()` 검사 |
| `heapq`는 **최소** 힙 | `priority_queue`는 **최대** 힙 | 그대로 옮기면 정반대 답 |
| `deque[i]`가 O(n) | `deque[i]`가 O(1) | C++ 덱은 임의 접근이 싸다 |
| `list.pop(0)`이 O(n) | `vector::erase(begin())`이 O(n) | 여기만 같다 — 둘 다 쓰면 안 된다 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: LIFO와 FIFO의 차이를, 같은 입력을 넣고 꺼낸 결과로 보여 주며.
- [ ] 설명할 수 있다: 중첩 구조(괄호·호출)의 짝이 왜 항상 "가장 최근에 열린 것"인지.
- [ ] 설명할 수 있다: 괄호 검사에서 개수만 세면 왜 `([)]`가 통과해 버리는지.
- [ ] 설명할 수 있다: `vector`의 `push_back`/`pop_back`이 분할상환 O(1)인 이유(용량 2배 증가).
- [ ] 설명할 수 있다: `vector::erase(begin())`이 O(n)이고 큐로 쓰면 전체가 O(n²)이 되는 과정.
- [ ] 설명할 수 있다: `deque::pop_front()`가 O(1)인 구조적 이유(블록 배열)와, 그런데도 `dq[i]`가 O(1)인 이유.
- [ ] 설명할 수 있다: `pop()`이 값을 돌려주지 않는 이유와, 그래서 코드가 왜 항상 2단계인지.
- [ ] 설명할 수 있다: 빈 컨테이너에 `top()`/`front()`를 부르는 것이 왜 예외가 아니라 미정의 동작인지.
- [ ] 설명할 수 있다: 후위 표기식에서 괄호가 필요 없는 이유와, 두 피연산자를 꺼내는 순서.
- [ ] 설명할 수 있다: 모노토닉 스택이 겹루프처럼 보이는데도 전체 O(n)인 근거.
- [ ] 설명할 수 있다: 모노토닉 스택에 값이 아니라 인덱스를 담아야 하는 이유.
- [ ] 설명할 수 있다: 단조 덱의 불변식 두 줄(창 안의 인덱스만, 값은 내림차순)과 그로부터 "맨 앞 = 최댓값"이 따라오는 이유.
- [ ] 설명할 수 있다: 단조 덱에서 뒤쪽 원소를 `<=`로 버려도 안전한 근거.
- [ ] 설명할 수 있다: 슬라이딩 윈도우를 창마다 다시 계산하면 O(n·k), 단조 덱이면 O(n)인 차이.
- [ ] 설명할 수 있다: 큐를 스택으로 바꾸면 "가장 먼저 도달"이라는 성질이 왜 깨지는지.
- [ ] 설명할 수 있다: `priority_queue`의 기본이 최대 힙인 이유와 최소 힙으로 바꾸는 방법.
- [ ] 설명할 수 있다: 스택·큐·덱으로 안 되고 힙이 필요해지는 순간(도착 순서 대 값 순서).

**⚠️ 자주 하는 실수**

**1) `pop()`의 반환값을 쓰려 한다**

```cpp
// ❌ 틀린 코드
stack<int> st;
st.push(3);
int x = st.pop();          // 컴파일 에러 : void 를 int 에 대입할 수 없다
```

왜: C++ 표준은 예외 안전성 때문에 "읽기"와 "제거"를 분리했다. 값을 복사해 반환하는 도중 복사 생성자가 예외를 던지면 원소는 이미 지워졌는데 값도 잃어버린다. 그래서 `pop()`의 반환형은 `void`다. 파이썬 `pop()`이 값을 돌려주던 습관을 그대로 옮기면 여기서 걸린다.

```cpp
// ✅ 고친 코드
int x = st.top();          // (1) 꼭대기를 읽는다
st.pop();                  // (2) 꼭대기를 버린다
// queue 는 front(), deque 는 front()/back(), priority_queue 는 top()
```

**2) 빈 컨테이너에서 `top()`/`front()`를 부른다**

```cpp
// ❌ 틀린 코드
for (char c : s) {
    if (c == '(') st.push_back(c);
    else st.pop_back();    // 입력이 ")(" 면 빈 vector 에서 pop_back -> 미정의 동작
}
```

왜: 파이썬이라면 `IndexError`로 즉시 죽어 원인을 알려 준다. C++은 **아무 신호도 주지 않는다.** 쓰레기 값을 읽고 조용히 틀린 답을 내거나, 로컬에서는 우연히 통과했다가 채점 서버에서만 죽는다. 닫는 괄호가 먼저 나오는 입력은 "실패로 판정할 정상 입력"이지 예외 상황이 아니므로, 검사를 직접 넣어야 한다.

```cpp
// ✅ 고친 코드
for (char c : s) {
    if (c == '(') st.push_back(c);
    else {
        if (st.empty()) return false;   // 빈 검사가 항상 먼저
        st.pop_back();
    }
}
// 조건식에서는 && 의 단축 평가를 이용한다
// if (!st.empty() && st.back() == '(') st.pop_back();
```

**3) `priority_queue`가 최소 힙인 줄 안다**

```cpp
// ❌ 틀린 코드
priority_queue<int> pq;                 // 파이썬 heapq 감각으로 최소 힙이라 생각
for (int x : {5, 1, 3}) pq.push(x);
cout << pq.top() << "\n";               // 5 가 나온다 (기대한 1 이 아니다)
```

왜: `priority_queue`의 셋째 인자는 비교자이고 기본값이 `less<T>`라 **큰 값이 위로 올라온다.** 파이썬 `heapq`는 정반대인 최소 힙이라, 코드를 그대로 옮기면 컴파일도 되고 실행도 되는데 **답만 정반대**로 나온다. 에러가 없어서 발견이 가장 늦는 함정이다.

```cpp
// ✅ 고친 코드
priority_queue<int, vector<int>, greater<int>> pq;   // 최소 힙
for (int x : {5, 1, 3}) pq.push(x);
cout << pq.top() << "\n";                            // 1
// 최대 힙이 필요하면 priority_queue<int> 를 그냥 쓰면 된다
```

**4) `vector`의 앞 삭제로 큐를 만든다**

```cpp
// ❌ 틀린 코드
vector<int> q = {start};
while (!q.empty()) {
    int cur = q.front();
    q.erase(q.begin());     // 앞을 뺄 때마다 뒤의 원소가 전부 한 칸씩 이사
    for (int nxt : nexts(cur)) q.push_back(nxt);
}
```

왜: `vector`는 원소를 연속된 칸에 붙여 두므로 맨 앞을 빼면 뒤의 n-1개를 전부 앞으로 당긴다. n번 반복하면 이동 횟수가 `n(n-1)/2`, 즉 **O(n²)**다. n = 100,000이면 약 50억 번이라 시간 초과가 확정이다.

```cpp
// ✅ 고친 코드
queue<int> q;
q.push(start);
while (!q.empty()) {
    int cur = q.front(); q.pop();   // 앞쪽 표시만 한 칸 옮긴다 -> O(1)
    for (int nxt : nexts(cur)) q.push(nxt);
}
```

**5) 덱의 양 끝 메서드를 뒤바꾼다**

```cpp
// ❌ 틀린 코드
deque<int> q;
q.push_back(1); q.push_back(2); q.push_back(3);
int x = q.back(); q.pop_back();     // 3 — 큐를 만들려 했는데 스택이 되었다
```

왜: `push_back`과 `pop_back`은 **둘 다 오른쪽 끝**이다. 이 조합은 LIFO, 즉 스택이다. 큐로 쓰려면 넣는 끝과 빼는 끝이 반대여야 하므로 `push_back` + `pop_front`(또는 `push_front` + `pop_back`)로 짝을 맞춰야 한다. 예제가 작으면 우연히 같은 답이 나와 더 늦게 발각된다.

```cpp
// ✅ 고친 코드
int x = q.front(); q.pop_front();   // 1 — 넣는 끝(뒤)과 빼는 끝(앞)이 반대여야 FIFO
// 규칙: 큐는 push_back + pop_front, 스택은 push_back + pop_back 으로 짝을 고정
```

**6) 모노토닉 스택에 값만 담아 위치를 잃는다**

```cpp
// ❌ 틀린 코드
vector<int> st;
for (int i = 0; i < n; i++) {
    while (!st.empty() && st.back() < arr[i]) st.pop_back();  // 어느 '자리'인지 모른다
    st.push_back(arr[i]);                                     // 값만 담았다
}
```

왜: 밀려나는 순간 확정되는 것은 "그 원소의 답"인데, 그 원소가 배열의 몇 번째였는지를 모르면 `ans[?] = arr[i]`를 쓸 수가 없다. 값이 중복되면 어느 쪽이 밀려난 것인지 구별조차 안 된다. 거리(`i - j`)를 묻는 문제도 인덱스가 없으면 손도 못 댄다.

```cpp
// ✅ 고친 코드
vector<int> st;
for (int i = 0; i < n; i++) {
    while (!st.empty() && arr[st.back()] < arr[i]) {
        ans[st.back()] = arr[i];      // 인덱스를 담았으므로 자리를 지정할 수 있다
        st.pop_back();
    }
    st.push_back(i);                  // 값이 아니라 인덱스를 담는다
}
```

**7) 단조 덱에서 창 만료를 값으로 판단한다**

```cpp
// ❌ 틀린 코드
deque<int> dq;                        // 값을 담았다
for (int i = 0; i < n; i++) {
    while (!dq.empty() && dq.back() <= arr[i]) dq.pop_back();
    dq.push_back(arr[i]);
    if (i >= k && dq.front() == arr[i - k]) dq.pop_front();  // 값으로 만료를 판단
}
```

왜: 값이 같은 원소가 둘 이상이면 "지금 나가는 그 원소"인지 "아직 창 안에 있는 다른 원소"인지 구별할 수 없다. 멀쩡히 창 안에 있는 최댓값을 지워 버리거나, 만료된 값을 계속 답으로 내놓는다. 만료는 **위치의 문제**라서 위치로만 판단할 수 있다.

```cpp
// ✅ 고친 코드
deque<int> dq;                        // 인덱스를 담는다
for (int i = 0; i < n; i++) {
    while (!dq.empty() && arr[dq.back()] <= arr[i]) dq.pop_back();
    dq.push_back(i);
    if (dq.front() <= i - k) dq.pop_front();   // 맨 앞 인덱스가 창 왼쪽 밖이면 만료
}
```

**8) `stack`/`queue`를 순회하려 한다**

```cpp
// ❌ 틀린 코드
stack<int> st;
for (int x : st) cout << x << ' ';        // 컴파일 에러 : begin()/end() 가 없다
cout << st[0] << "\n";                    // 컴파일 에러 : operator[] 도 없다
```

왜: `stack`·`queue`·`priority_queue`는 컨테이너가 아니라 **어댑터**다. "쓸 수 있는 문"을 일부러 좁혀 놓은 것이라 반복자도 인덱스 접근도 제공하지 않는다. 내용을 보려면 전부 꺼내야 하고, 그러면 컨테이너가 비어 버린다.

```cpp
// ✅ 고친 코드
vector<int> st;                           // 순회가 필요하면 처음부터 vector 로
st.push_back(1); st.push_back(2);
for (int x : st) cout << x << ' ';        // 스택으로 쓰면서 순회도 된다
// 이미 stack 을 쓰고 있다면 복사본을 만들어 비우며 읽는다
// stack<int> tmp = st; while (!tmp.empty()) { use(tmp.top()); tmp.pop(); }
```

**9) 큰 컨테이너를 값으로 넘긴다**

```cpp
// ❌ 틀린 코드
vector<int> nextGreater(vector<int> arr) {   // 부를 때마다 배열 전체가 복사된다
    // ...
}
```

왜: C++은 인자를 **값으로 복사**하는 것이 기본이다. 원소 10만 개짜리 `vector`를 값으로 받으면 호출마다 10만 칸을 새로 만들어 옮긴다. 파이썬은 리스트를 참조로 넘기므로 이런 비용이 없어, 코드를 옮기다 보면 놓치기 쉽다.

```cpp
// ✅ 고친 코드
vector<int> nextGreater(const vector<int>& arr) {   // 주소 하나만 넘어간다
    // const 를 붙이면 실수로 고치는 것까지 막아 준다
}
// 함수 안에서 내용을 바꿔야 하면 const 를 떼고 vector<int>& 로 받는다
```

**다음 챕터로**

- Ch06(트리)의 순회는 이 챕터의 두 도구를 그대로 쓴다. 깊이 우선(DFS)은 스택, 너비 우선(BFS)은 큐이며, "층 단위로 퍼진다"는 성질은 `queue`가 FIFO를 지켜 주기 때문에 성립한다.
- 그리고 "도착 순서가 아니라 값의 크기 순으로 꺼내야 한다"는 갈림길의 끝에 힙이 있다. Ch06의 `priority_queue`는 이 챕터의 선택 기준표에서 마지막 세 줄을 담당하는 자료구조다. 기본이 최대 힙이라는 것만 잊지 않으면 된다.
