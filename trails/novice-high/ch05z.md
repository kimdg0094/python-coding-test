## L5. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 레슨은 Ch05(스택·큐·덱) 전체를 한 장으로 묶는 정리다. 세 자료구조는 서로 다른 발명품이 아니라 **"한 줄로 늘어선 데이터에서 어느 끝을 만질 수 있는가"** 하나의 질문에 대한 세 가지 답이다.
- 스택은 한쪽 끝만, 큐는 양 끝을 하나씩 나눠서, 덱은 양쪽 끝을 모두 쓴다. 그리고 "들어온 순서"가 아니라 **"값의 크기 순서"**로 꺼내야 하면 그때 힙(`heapq`)으로 넘어간다. 이 갈림길을 표로 못 박는 것이 이 레슨의 목적이다.

**개념 지도**

- 먼저 전체 지도다. 위에서 아래로 "어느 끝을 만지나 → 무슨 문제에 쓰나"로 읽는다.

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
  append / pop     append /         stack -> next greater
  a list is fine   popleft          deque -> window max
      |                |                |
  nesting          arrival order    "this one can never win
  undo / redo      BFS by layer      again"  ->  drop it now
  postfix eval     round robin
      |
      +-- order by PRIORITY, not by arrival  ->  heapq
            push / pop O(log n),  peek O(1)
```

- 덱의 그림 한 장이면 스택과 큐가 왜 그 특수한 경우인지 바로 보인다. 문은 네 개고, 어느 문을 쓰느냐가 이름을 정한다.

```text
       appendleft              append
           v                      v
        ┌──────┬──────┬──────┬──────┐
        │  10  │  20  │  30  │  40  │
        └──────┴──────┴──────┴──────┘
           ^                      ^
        popleft                  pop

  append + pop      -> STACK  (LIFO)   # 오른쪽 문 두 개만 쓴다
  append + popleft  -> QUEUE  (FIFO)   # 들어가는 문과 나오는 문이 반대
  all four doors    -> DEQUE           # 회문·회전·단조 덱
  list.pop(0)       -> O(n) trap       # 큐를 list 로 만들면 안 되는 이유
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

**뼈대 코드**

- (1) 괄호 검사 — 세 종류를 짝 사전으로 한꺼번에.

```python
def check(s):
    pair = {')': '(', ']': '[', '}': '{'}    # ← 괄호 종류는 문제마다 바뀜
    st = []
    for c in s:
        if c in '([{':
            st.append(c)
        elif c in pair:
            if not st or st[-1] != pair[c]:  # 빈 검사가 먼저! 종류까지 비교
                return False
            st.pop()
    return not st                            # 끝에 남아 있으면 안 닫힌 것
```

- (2) 후위 표기식 계산 — 피연산자는 쌓고, 연산자를 만나면 위에서 둘을 꺼낸다.

```python
def eval_postfix(tokens):
    st = []
    for t in tokens:
        if t not in '+-*/':
            st.append(int(t))                # ← 피연산자 판별 방식은 문제마다 바뀜
        else:
            b = st.pop()                     # 나중에 넣은 것이 오른쪽 피연산자
            a = st.pop()                     # 먼저 넣은 것이 왼쪽 피연산자
            if   t == '+': st.append(a + b)
            elif t == '-': st.append(a - b)  # 순서를 바꾸면 뺄셈·나눗셈이 틀린다
            elif t == '*': st.append(a * b)
            else:          st.append(a // b)
    return st[-1]                            # 마지막 하나가 최종 결과
```

- (3) 모노토닉 스택 — "다음으로 큰 수". **값이 아니라 인덱스를 담는다.**

```python
def next_greater(arr):
    n = len(arr)
    ans = [-1] * n                           # ← 없을 때의 값은 문제마다 바뀜
    st = []                                  # 답이 아직 안 정해진 '인덱스'
    for i in range(n):
        while st and arr[st[-1]] < arr[i]:   # ← 같을 때 pop 할지는 문제마다 바뀜
            ans[st.pop()] = arr[i]           # 밀려나는 순간 그 자리의 답이 확정
        st.append(i)
    return ans                               # 스택에 남은 것들은 -1 그대로
```

- (4) 큐와 덱의 기본 연산 — `list` 대신 `deque`.

```python
from collections import deque

q = deque()
q.append(x)          # 뒤에 넣기      O(1)
front = q[0]         # 맨 앞 엿보기   O(1)
x = q.popleft()      # 앞에서 빼기    O(1)   ← list 의 pop(0) 은 O(n)

dq = deque()
dq.appendleft(x)     # 앞에 넣기      O(1)
back = dq[-1]        # 맨 뒤 엿보기   O(1)
y = dq.pop()         # 뒤에서 빼기    O(1)

while q:             # 비었는지 검사는 반드시 꺼내기 '전에'
    cur = q.popleft()
```

- (5) 슬라이딩 윈도우 최댓값 — 단조 덱. 네 단계의 순서가 곧 불변식이다.

```python
def window_max(arr, k):
    dq, out = deque(), []                    # dq 에는 인덱스만, 값은 내림차순 유지
    for i, v in enumerate(arr):
        while dq and arr[dq[-1]] <= v:
            dq.pop()                         # (1) 뒤에서 못 이길 것들을 버린다
        dq.append(i)                         # (2) 새 인덱스를 넣는다
        if dq[0] <= i - k:
            dq.popleft()                     # (3) 앞에서 창을 벗어난 것을 버린다
        if i >= k - 1:
            out.append(arr[dq[0]])           # (4) 창이 다 찼으면 맨 앞이 최댓값
    return out
```

- (6) 회전 명령 처리 — 직접 옮기지 말고 `rotate`를 쓴다.

```python
dq = deque(range(1, n + 1))
dq.rotate(1)      # 오른쪽으로 1칸: 맨 뒤가 맨 앞으로       O(k)
dq.rotate(-1)     # 왼쪽으로 1칸 : 맨 앞이 맨 뒤로          O(k)

# 특정 값을 맨 앞으로 가져오는 최소 회전 수 (양방향 중 짧은 쪽)
i = dq.index(target)                         # ← 탐색은 O(n)
left_cost  = i                               # 왼쪽으로 i 번
right_cost = len(dq) - i                     # 오른쪽으로 n-i 번
dq.rotate(-i) if left_cost <= right_cost else dq.rotate(right_cost)
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 중첩된 짝을 맞춘다(괄호·태그) | 스택(`list`) | 닫는 것의 짝은 언제나 "가장 최근에 열린 것" | O(n) |
| 되돌리기·다시하기 | 스택 두 개 | 취소한 것을 다른 스택에 옮겨 두면 순서가 보존됨 | 연산당 O(1) |
| 후위 표기식 계산·수식 처리 | 스택 | 피연산자를 쌓다가 연산자에서 둘만 꺼내면 됨 | O(n) |
| 각 원소의 "다음(이전)으로 큰/작은 값" | 모노토닉 스택 | 밀려나는 순간 답이 확정돼 다시 볼 필요가 없음 | O(n) |
| 히스토그램·직사각형 넓이류 | 모노토닉 스택 + 파수꾼 | 높이가 낮아지는 지점이 곧 구간의 끝 | O(n) |
| 도착한 순서대로 공정하게 처리 | 큐(`deque`) | 먼저 들어온 것이 먼저 나가는 것이 곧 규칙 | 연산당 O(1) |
| 층·단계 단위로 퍼지는 탐색 | 큐(`deque`) | 큐 안의 원소가 항상 같은 층에 있음 | O(n) |
| 앞에서 꺼내 뒤로 보내는 회전 | 큐(`deque`) 또는 `rotate` | `popleft` + `append`가 한 바퀴를 그대로 표현 | 회전당 O(1) |
| 양 끝에서 넣고 빼야 한다(회문·앞뒤 줄서기) | 덱(`deque`) | 네 연산이 모두 O(1)이라 방향 전환이 공짜 | 연산당 O(1) |
| 고정 크기 창의 최댓값·최솟값 | 단조 덱 | 뒤로는 후보 정리, 앞으로는 만료 처리가 동시에 필요 | O(n) |
| 창마다 값이 바뀌고 크기도 바뀐다 | 힙 + 지연 삭제 | 만료를 위치로 판단할 수 없어 우선순위가 필요 | O(n log n) |
| 도착 순서가 아니라 **값의 크기** 순으로 꺼낸다 | `heapq` | 전체 정렬을 포기하는 대신 삽입·삭제를 싸게 만듦 | 연산당 O(log n) |
| 남은 것 중 항상 최소(또는 최대)만 필요 | `heapq` | 꼭대기 하나만 정확하면 되므로 O(1) 조회 | 조회 O(1) |
| 중간 원소를 자주 읽어야 한다 | `list` | 덱은 인덱스 접근이 O(n)이라 오히려 느려짐 | 읽기 O(1) |

- 연산별 비용을 한 표로 비교하면 선택이 더 분명해진다. **같은 코드 모양인데 비용이 다른 칸**이 함정이다.

| 연산 | `list` | `deque` | `heapq`(list 기반) |
|---|---|---|---|
| 뒤에 넣기 | O(1) 평균 | O(1) | 삽입 O(log n) |
| 뒤에서 빼기 | O(1) | O(1) | — |
| 앞에 넣기 | **O(n)** | O(1) | — |
| 앞에서 빼기 | **O(n)** | O(1) | 최솟값 제거 O(log n) |
| 양 끝 엿보기 | O(1) | O(1) | 최솟값 조회 O(1) |
| i번째 읽기 | O(1) | **O(n)** | 의미 없음 |
| 회전 k칸 | O(n) | O(k) | — |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: LIFO와 FIFO의 차이를, 같은 입력을 넣고 꺼낸 결과로 보여 주며.
- [ ] 설명할 수 있다: 중첩 구조(괄호·호출)의 짝이 왜 항상 "가장 최근에 열린 것"인지.
- [ ] 설명할 수 있다: 괄호 검사에서 개수만 세면 왜 `([)]`가 통과해 버리는지.
- [ ] 설명할 수 있다: 파이썬 `list`의 `append`/`pop()`이 평균 O(1)인 이유(상환 분석).
- [ ] 설명할 수 있다: `list.pop(0)`이 O(n)이고 큐로 쓰면 전체가 O(n²)이 되는 과정.
- [ ] 설명할 수 있다: `deque.popleft()`가 O(1)인 구조적 이유와, 그 대가로 `dq[i]`가 O(n)인 이유.
- [ ] 설명할 수 있다: 후위 표기식에서 괄호가 필요 없는 이유와, 두 피연산자를 꺼내는 순서.
- [ ] 설명할 수 있다: 모노토닉 스택이 겹루프처럼 보이는데도 전체 O(n)인 근거.
- [ ] 설명할 수 있다: 모노토닉 스택에 값이 아니라 인덱스를 담아야 하는 이유.
- [ ] 설명할 수 있다: 단조 덱의 불변식 두 줄(창 안의 인덱스만, 값은 내림차순)과 그로부터 "맨 앞 = 최댓값"이 따라오는 이유.
- [ ] 설명할 수 있다: 단조 덱에서 뒤쪽 원소를 `<=`로 버려도 안전한 근거.
- [ ] 설명할 수 있다: 슬라이딩 윈도우를 창마다 다시 계산하면 O(n·k), 단조 덱이면 O(n)인 차이.
- [ ] 설명할 수 있다: 큐를 스택으로 바꾸면 "가장 먼저 도달"이라는 성질이 왜 깨지는지.
- [ ] 설명할 수 있다: 스택·큐·덱으로 안 되고 힙이 필요해지는 순간(도착 순서 대 값 순서).

**⚠️ 자주 하는 실수**

**1) `list.pop(0)`으로 큐를 만든다**

```python
# ❌ 틀린 코드
q = [start]
while q:
    cur = q.pop(0)          # 앞을 뺄 때마다 뒤의 원소가 전부 한 칸씩 이사
    for nxt in nexts(cur):
        q.append(nxt)
```

왜: `list`는 원소를 연속된 칸에 붙여 두므로 0번을 빼면 뒤의 n-1개를 전부 앞으로 당긴다. n번 반복하면 이동 횟수가 `n(n-1)/2`, 즉 **O(n²)**다. n = 100,000이면 약 50억 번이라 시간 초과가 확정이다.

```python
# ✅ 고친 코드
from collections import deque

q = deque([start])
while q:
    cur = q.popleft()       # 앞쪽 표시만 한 칸 옮긴다 -> O(1)
    for nxt in nexts(cur):
        q.append(nxt)
```

**2) 빈 스택에서 pop하거나 top을 본다**

```python
# ❌ 틀린 코드
for c in s:
    if c == '(':
        st.append(c)
    else:
        st.pop()            # 입력이 ")(" 면 첫 글자에서 IndexError 로 죽는다
```

왜: 닫는 괄호가 여는 괄호보다 먼저 나오는 입력은 **"실패로 판정해야 할 정상 입력"**이지 예외 상황이 아니다. 검사를 빼면 오답이 아니라 런타임 에러가 나서 채점이 0점이 된다. `st[-1]`도 같은 위험이 있다.

```python
# ✅ 고친 코드
for c in s:
    if c == '(':
        st.append(c)
    else:
        if not st:          # 빈 검사가 항상 먼저
            return False    # 짝이 없는 닫는 괄호 -> 실패로 판정
        st.pop()
```

**3) 덱의 양 끝 메서드를 뒤바꾼다**

```python
# ❌ 틀린 코드
from collections import deque
q = deque()
q.append(1); q.append(2); q.append(3)
print(q.pop())              # 3 — 큐를 만들려 했는데 스택이 되었다
```

왜: `append`와 `pop`은 **둘 다 오른쪽 끝**이다. 이 조합은 LIFO, 즉 스택이다. 큐로 쓰려면 넣는 끝과 빼는 끝이 반대여야 하므로 `append` + `popleft`(또는 `appendleft` + `pop`)로 짝을 맞춰야 한다. 예제가 작으면 우연히 같은 답이 나와 더 늦게 발각된다.

```python
# ✅ 고친 코드
q.append(1); q.append(2); q.append(3)
print(q.popleft())          # 1 — 넣는 끝(뒤)과 빼는 끝(앞)이 반대여야 FIFO
# 규칙: 큐는 append + popleft, 스택은 append + pop 으로 짝을 고정한다
```

**4) 모노토닉 스택에 값만 담아 위치를 잃는다**

```python
# ❌ 틀린 코드
st = []
for i in range(n):
    while st and st[-1] < arr[i]:
        st.pop()            # 어느 '자리'의 답이 정해진 것인지 알 수 없다
    st.append(arr[i])       # 값만 담았다
```

왜: 밀려나는 순간 확정되는 것은 "그 원소의 답"인데, 그 원소가 배열의 몇 번째였는지를 모르면 `ans[?] = arr[i]`를 쓸 수가 없다. 값이 중복되면 어느 쪽이 밀려난 것인지 구별조차 안 된다. 거리(`i - j`)를 묻는 문제도 인덱스가 없으면 손도 못 댄다.

```python
# ✅ 고친 코드
st = []
for i in range(n):
    while st and arr[st[-1]] < arr[i]:
        ans[st.pop()] = arr[i]      # 인덱스를 담았으므로 자리를 지정할 수 있다
    st.append(i)                    # 값이 아니라 인덱스를 담는다
```

**5) 괄호를 종류 구분 없이 개수만 센다**

```python
# ❌ 틀린 코드
depth = 0
for c in s:
    if c in '([{':
        depth += 1
    else:
        depth -= 1
        if depth < 0:
            return False
return depth == 0           # "([)]" 가 통과해 버린다
```

왜: 개수 세기는 "몇 개가 열려 있나"만 알 뿐 **무엇이 열려 있나**를 모른다. `([)]`는 열림·닫힘 개수가 맞아 통과하지만, 3번째 `)`의 짝은 가장 최근에 열린 `[`여야 하므로 실제로는 틀린 문자열이다. 종류가 하나뿐일 때만 쓸 수 있는 방법이다.

```python
# ✅ 고친 코드
pair = {')': '(', ']': '[', '}': '{'}
st = []
for c in s:
    if c in '([{':
        st.append(c)
    elif c in pair:
        if not st or st[-1] != pair[c]:   # 종류까지 비교해야 한다
            return False
        st.pop()
return not st
```

**6) 단조 덱에서 창 만료를 값으로 판단한다**

```python
# ❌ 틀린 코드
dq = deque()                # 값을 담았다
for i, v in enumerate(arr):
    while dq and dq[-1] <= v:
        dq.pop()
    dq.append(v)
    if dq[0] == arr[i - k]:  # 창을 벗어난 값과 같은지로 만료를 판단
        dq.popleft()
```

왜: 값이 같은 원소가 둘 이상이면 "지금 나가는 그 원소"인지 "아직 창 안에 있는 다른 원소"인지 구별할 수 없다. 멀쩡히 창 안에 있는 최댓값을 지워 버리거나, 만료된 값을 계속 답으로 내놓는다. 만료는 **위치의 문제**라서 위치로만 판단할 수 있다.

```python
# ✅ 고친 코드
dq = deque()                # 인덱스를 담는다
for i, v in enumerate(arr):
    while dq and arr[dq[-1]] <= v:
        dq.pop()
    dq.append(i)
    if dq[0] <= i - k:      # 맨 앞 인덱스가 창 왼쪽 밖이면 만료
        dq.popleft()
```

**7) 덱을 인덱스로 훑거나, 회전을 슬라이싱으로 처리한다**

```python
# ❌ 틀린 코드
for i in range(len(dq)):
    if dq[i] == target:     # dq[i] 하나가 O(n) -> 전체 O(n²)
        break

lst = lst[1:] + lst[:1]     # 회전할 때마다 리스트를 통째로 새로 만든다
```

왜: `deque`는 작은 블록을 이어 붙인 구조라 중간 인덱스 접근이 O(n)이다. 양 끝이 O(1)이라는 장점만 보고 인덱스로 훑으면 `list`보다 느려진다. 슬라이싱 회전도 매번 n칸을 복사하므로 회전 m번이면 O(n·m)이다.

```python
# ✅ 고친 코드
i = dq.index(target)        # 탐색은 한 번만 O(n)
dq.rotate(-i)               # 회전은 옮길 칸 수 k 에만 비례한다

from collections import deque
dq = deque(lst)
dq.rotate(-1)               # 왼쪽으로 한 칸: 맨 앞이 맨 뒤로
```

**다음 챕터로**

- Ch06(트리)의 순회는 이 챕터의 두 도구를 그대로 쓴다. 깊이 우선(DFS)은 스택, 너비 우선(BFS)은 큐이며, "층 단위로 퍼진다"는 성질은 `deque`가 FIFO를 지켜 주기 때문에 성립한다.
- 그리고 "도착 순서가 아니라 값의 크기 순으로 꺼내야 한다"는 갈림길의 끝에 힙이 있다. Ch06의 `heapq`는 이 챕터의 선택 기준표에서 마지막 두 줄을 담당하는 자료구조다.
