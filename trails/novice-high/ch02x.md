## L7. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch2(배열·연결 리스트)의 핵심 — 배열의 "밀기" 비용, 동적 배열의 뒤쪽 O(1), 단일·이중·원형 연결 리스트의 링크 재배선, Iterator로 순회 감추기 — 를 소재만 바꿔 **반복 훈련**하고, 코딩테스트 단골 연결 리스트 유형(중간 노드·사이클·뒤에서 k번째·재배열)으로 **확장**하는 연습 세트다.
- **반복 훈련 개념**:
  - 배열 삽입·삭제는 밀기: 삽입은 뒤에서부터 `a[j] = a[j-1]`, 삭제는 앞에서부터 `a[j] = a[j+1]` — 이동 횟수가 곧 O(n) 비용.
  - 배열로 표현한 연결 리스트: `nxt[i]`, `prv[i]` 인덱스 배열과 `-1`(끝) 표시로 `cur = nxt[cur]` 순회.
  - 링크 재배선 4줄: `nxt = cur.next; cur.next = prev; prev = cur; cur = nxt` — 뒤집기의 뼈대.
  - 더미(센티넬) 노드: `dummy.next = head`로 "맨 앞 삭제"와 "중간 삭제"를 한 코드로 통일.
  - 두 포인터: 느린/빠른 포인터(`slow`, `fast = fast.next.next`)로 길이를 세지 않고 중간·뒤에서 k번째를 찾는다.
- **코딩테스트 출제 맵**: NeetCode 150의 'Linked List' 유형(Reverse Linked List, Middle/Remove Nth Node, Linked List Cycle, Reorder List), 백준 「단계별로 풀어보기」의 '1차원 배열'·'큐, 덱' 단계(요세푸스류), 프로그래머스 「코딩테스트 고득점 Kit」의 '스택/큐'가 이 챕터 사고를 그대로 쓴다.
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 명단 삽입과 삭제 밀기 비용 | Easy | 배열 밀기 방향·이동 횟수 세기 | 반복 훈련 |
| 2 | 쪽지 따라가기 | Easy | next 인덱스 배열로 순회 | 반복 훈련 |
| 3 | 기차 중간 칸 찾기 | Easy | 느린/빠른 포인터 | 유형 확장 (NeetCode 'Linked List' 스타일) |
| 4 | 순간이동 포털 사이클 판정 | Medium | next 배열 + 방문 순서 기록 | 유형 확장 (NeetCode 'Linked List' 스타일) |
| 5 | 뒤에서 k번째 손님 빼기 | Medium | 더미 헤드 + 간격 두 포인터 | 유형 확장 (NeetCode 'Linked List' 스타일) |
| 6 | 카드 줄 부분 뒤집기 | Medium | 구간 링크 뒤집기 + 양끝 재연결 | 반복 훈련 |
| 7 | 브라우저 방문 기록 | Medium | 이중 연결 리스트 커서 이동·가지치기 | 반복 훈련 |
| 8 | 돌림판 선물 뽑기 | Medium | 원형 next/prev 배열 + `% remain` | 반복 훈련 |
| 9 | 무대 등장 순서 재배열 | Hard | 중간 찾기 + 뒤집기 + 번갈아 잇기 | 유형 확장 (NeetCode 'Linked List' 스타일) |
| 10 | 줄 서기 명령 처리 | Hard | 센티넬 이중 리스트 + dict + `__iter__` | 반복 훈련 |

**문제**

**1) 명단 삽입과 삭제 밀기 비용** · Easy

- **요구사항**: 빈 동적 배열에서 시작해 명령을 처리하라. `ins i x`는 인덱스 `i` 자리에 `x`를 삽입(원래 `i` 이후 원소들은 한 칸씩 뒤로 밀림), `del i`는 인덱스 `i`의 원소를 삭제(뒤 원소들이 한 칸씩 앞으로 당겨짐)한다. 각 명령에서 "자리를 옮긴 원소 수"를 세어, 최종 배열과 총 이동 횟수를 출력하라. `list.insert`/`del` 대신 직접 밀어라.
- **입력**: 첫 줄에 명령 수 `q`. 다음 `q`줄에 명령. 인덱스는 항상 유효하다(`ins`는 `0 ≤ i ≤ 현재 길이`, `del`은 `0 ≤ i < 현재 길이`). (`1 ≤ q ≤ 100`)
- **출력**: 첫 줄에 최종 배열(공백 구분, 비면 `empty`), 둘째 줄에 총 이동 횟수.
- **예제**: `5 / ins 0 5 / ins 0 3 / ins 2 9 / del 0 / ins 1 7` → `5 7 9` / `4` · `2 / ins 0 1 / del 0` → `empty` / `0`
- **셀프체크**: 삽입은 **뒤에서부터** 밀어야 값이 덮이지 않는가(`for j in range(len-1, i, -1)`)? 맨 뒤 삽입(`i == 길이`)과 맨 뒤 삭제는 이동 0번인가? 첫 예제에서 이동이 `0+1+0+2+1 = 4`로 나오는가?

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split('\n')
q = int(data[0])
arr = []
moves = 0
for line in data[1:q + 1]:
    parts = line.split()
    if not parts:
        continue
    if parts[0] == 'ins':
        i = int(parts[1]); x = int(parts[2])
        arr.append(0)                              # 칸 하나 확보
        for j in range(len(arr) - 1, i, -1):       # 뒤에서부터 한 칸씩 밀기
            arr[j] = arr[j - 1]
            moves += 1
        arr[i] = x
    else:
        i = int(parts[1])
        for j in range(i, len(arr) - 1):           # 앞으로 한 칸씩 당기기
            arr[j] = arr[j + 1]
            moves += 1
        arr.pop()                                  # 마지막 빈 칸 제거
print(' '.join(map(str, arr)) if arr else 'empty')
print(moves)
@@TESTS
--IN
5
ins 0 5
ins 0 3
ins 2 9
del 0
ins 1 7
--OUT
5 7 9
4
--IN
2
ins 0 1
del 0
--OUT
empty
0
--IN
4
ins 0 1
ins 1 2
ins 2 3
del 2
--OUT
1 2
0
@@EXPL
(1) 접근·핵심 아이디어

- 배열의 중간 삽입·삭제 비용이 O(n)인 이유는 "뒤쪽 원소를 전부 한 칸씩 옮기기" 때문이다. 이 문제는 그 이동을 직접 구현해 횟수를 세게 한다 — 삽입 위치 뒤에 원소가 `m`개면 이동도 `m`번.
- 삽입은 뒤에서부터 밀어야 아직 안 옮긴 값을 덮지 않고, 삭제는 앞에서부터 당겨야 한다. 방향이 반대면 같은 값이 복제된다.

(2) 코드 단계별

- `ins i x`: `append(0)`으로 칸을 늘리고, 마지막 인덱스부터 `i+1`까지 `arr[j] = arr[j-1]`로 밀며 `moves`를 센 뒤 `arr[i] = x`.
- `del i`: `i`부터 끝 직전까지 `arr[j] = arr[j+1]`로 당기며 세고, 마지막 칸을 `pop()`(뒤 제거는 O(1)).
- 맨 뒤 삽입/삭제는 반복이 0번이라 이동이 없다 — 동적 배열의 "뒤쪽은 싸다"는 성질이 그대로 보인다.

(3) 스스로 다시 짤 때 생각 순서

- "삽입 = 칸 확보 + 뒤에서부터 밀기", "삭제 = 앞에서부터 당기기 + 마지막 칸 제거"를 먼저 정한다.
- 이동 횟수는 밀기/당기기 루프 안에서만 센다(대입 `arr[i] = x`는 이동이 아님).
- 경계: 빈 배열에 `ins 0`, 마지막 원소 `del`, 결과가 비면 `empty`.
```

**2) 쪽지 따라가기** · Easy

- **요구사항**: 방 `n`개(번호 `0..n-1`)마다 쪽지가 있다. 쪽지에는 값과 "다음에 갈 방 번호"가 적혀 있고, 다음 방이 `-1`이면 거기서 끝난다. 시작 방 `h`부터 쪽지를 따라가며 읽은 값들을 순서대로 출력하고, 방문한 방의 수도 출력하라. 연결 리스트를 `next` 인덱스 배열로 표현하는 연습이다(도달하지 못하는 방은 무시).
- **입력**: 첫 줄에 `n h`. 이어서 `n`개의 줄에 방 `0..n-1`의 `값 다음방` 순서로. (`1 ≤ n ≤ 100`, 사이클 없음 보장)
- **출력**: 첫 줄에 읽은 값들(공백 구분), 둘째 줄에 방문한 방 수.
- **예제**: `4 2 / 10 -1 / 20 0 / 30 1 / 40 -1` → `30 20 10` / `3` · `1 0 / 7 -1` → `7` / `1`
- **셀프체크**: 값 배열 `val`과 링크 배열 `nxt`를 따로 두고 `cur = nxt[cur]`로 따라갔는가? 종료 조건이 `cur != -1`인가? 시작 방이 곧바로 `-1`을 가리키면 값 하나만 출력되는가? 도달 못 하는 방(예제의 40)은 출력에 없는가?

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
n, h = int(data[0]), int(data[1])
val = [0] * n
nxt = [0] * n
for i in range(n):
    val[i] = int(data[2 + 2 * i])
    nxt[i] = int(data[3 + 2 * i])
out = []
cur = h
while cur != -1:            # -1 이 곧 None(끝) 역할
    out.append(str(val[cur]))
    cur = nxt[cur]
print(' '.join(out))
print(len(out))
@@TESTS
--IN
4 2
10 -1
20 0
30 1
40 -1
--OUT
30 20 10
3
--IN
1 0
7 -1
--OUT
7
1
--IN
3 1
5 -1
6 -1
8 1
--OUT
6
1
@@EXPL
(1) 접근·핵심 아이디어

- 연결 리스트는 꼭 클래스로만 만드는 게 아니다. 값 배열 `val`과 "다음 인덱스" 배열 `nxt`를 두면 `nxt[i]`가 곧 `node.next`이고, `-1`이 `None`(끝) 역할을 한다. 인덱스 배열 표현은 노드 생성 비용이 없고 코딩테스트에서 자주 쓰인다.
- 순회는 `cur = h`에서 시작해 `cur != -1`인 동안 값을 읽고 `cur = nxt[cur]`로 한 칸씩 이동 — 클래스 버전의 `while cur: ... cur = cur.next`와 같은 모양이다.

(2) 코드 단계별

- `n, h`를 읽고 방마다 `값, 다음방`을 `val`, `nxt`에 채운다(한 방이 두 토큰이라 `2 + 2*i`, `3 + 2*i`).
- `cur = h`부터 `-1`을 만날 때까지 값을 모으고, 마지막에 개수 `len(out)`을 함께 출력.
- 셋째 테스트처럼 시작 방이 바로 `-1`을 가리키면 값 하나, 나머지 방은 도달 불가라 무시된다.

(3) 스스로 다시 짤 때 생각 순서

- "노드 = 인덱스, next = 정수 배열, 끝 = -1"로 표현을 정한다.
- 순회 루프의 종료 조건을 `-1`로 두고, 값과 링크를 각각 다른 배열에서 읽는다.
- 시작 방 자체가 끝인 경우와 도달 불가 방이 있는 경우를 예제로 확인한다.
```

**3) 기차 중간 칸 찾기** · Easy

- **요구사항**: 기차 칸 `n`개의 번호를 단일 연결 리스트(클래스)로 이어 만든 뒤, **길이를 세지 않고** 느린 포인터(한 칸)와 빠른 포인터(두 칸)로 한 번만 순회해 중간 칸의 번호를 출력하라. `n`이 짝수면 두 중간 칸 중 **뒤쪽**을 답으로 한다.
- **입력**: 첫 줄에 `n`. 둘째 줄에 칸 번호 `n`개. (`1 ≤ n ≤ 100`)
- **출력**: 중간 칸의 번호.
- **예제**: `5 / 1 2 3 4 5` → `3` · `4 / 10 20 30 40` → `30`
- **셀프체크**: 반복 조건이 `while fast and fast.next`인가(이 조건이 짝수일 때 뒤쪽 중간을 준다)? `fast`가 두 칸 갈 때 `None`을 참조하지 않는가? `n=1`이면 반복이 0번이라 첫 칸이 답인가? 길이를 먼저 세는 두 번 순회보다 왜 한 번 순회가 유리한지(스트림처럼 길이를 모를 때) 짚었는가?

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
n = int(data[0])
vals = [int(data[1 + i]) for i in range(n)]

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

head = None
tail = None
for v in vals:                  # 뒤에 이어 붙이기
    node = Node(v)
    if head is None:
        head = tail = node
    else:
        tail.next = node
        tail = node

slow = fast = head
while fast and fast.next:       # fast 가 두 칸 갈 수 있는 동안
    slow = slow.next
    fast = fast.next.next
print(slow.val)
@@TESTS
--IN
5
1 2 3 4 5
--OUT
3
--IN
4
10 20 30 40
--OUT
30
--IN
1
9
--OUT
9
--IN
2
3 4
--OUT
4
@@EXPL
(1) 접근·핵심 아이디어

- 느린 포인터가 1칸 갈 때 빠른 포인터가 2칸 가면, 빠른 포인터가 끝에 닿았을 때 느린 포인터는 정확히 절반 지점에 있다. 길이를 세는 순회 한 번을 아끼고, 길이를 모르는 스트림에서도 쓸 수 있다.
- 조건 `while fast and fast.next`는 홀수 길이면 정중앙, 짝수 길이면 두 중간 중 뒤쪽에서 멈춘다. 앞쪽을 원하면 `fast.next and fast.next.next`로 바꾼다(9번 문제에서 그 형태를 쓴다).

(2) 코드 단계별

- 입력값을 뒤에 이어 붙여 단일 연결 리스트를 만든다.
- `slow = fast = head`에서 시작해 `fast`가 두 칸 갈 수 있는 동안 `slow`는 한 칸, `fast`는 두 칸 이동.
- `n=4`: `fast`가 1→3→None, `slow`가 1→2→3번째 노드(30). `n=1`: 반복 0번이라 head.

(3) 스스로 다시 짤 때 생각 순서

- "두 배 속도 포인터"라는 그림을 먼저 떠올린다.
- `fast.next.next`를 참조하기 전에 `fast`와 `fast.next`가 모두 있는지 조건에 넣는다.
- 짝수/홀수/길이 1 세 경우에서 멈추는 위치를 손으로 확인한다.
```

**4) 순간이동 포털 사이클 판정** · Medium

- **요구사항**: 방 `n`개(`0..n-1`)마다 포털이 하나씩 있어 다른 방으로 보낸다(`-1`이면 출구). 시작 방 `s`에서 포털을 계속 타면 결국 출구로 나가는지, 아니면 영원히 도는지 판정하라. 출구로 나가면 `exit k`(`k`는 방문한 방의 수), 영원히 돌면 `cycle k`(`k`는 사이클에 포함된 방의 수)를 출력하라. 방마다 "처음 방문한 순서"를 배열에 기록해 판정하라.
- **입력**: 첫 줄에 `n s`. 둘째 줄에 방 `0..n-1`의 포털 목적지 `n`개(`-1`은 출구). (`1 ≤ n ≤ 100`)
- **출력**: `exit k` 또는 `cycle k`.
- **예제**: `5 0 / 1 2 3 1 -1` → `cycle 3` · `4 3 / 1 2 -1 0` → `exit 4`
- **셀프체크**: 이미 방문한 방에 다시 도착하면 사이클이고, 사이클 길이는 "지금 시각 − 그 방을 처음 방문한 시각"인가? 시작 방으로 돌아오지 않고 중간(예제의 방 1)으로 돌아오는 경우도 맞는가? 자기 자신을 가리키는 방(`cycle 1`)과 시작하자마자 출구(`exit 1`) 경계를 확인했는가?

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
n, s = int(data[0]), int(data[1])
nxt = [int(data[2 + i]) for i in range(n)]
step = [-1] * n          # 처음 방문한 시각(0부터), 미방문은 -1
cur = s
t = 0
while cur != -1 and step[cur] == -1:
    step[cur] = t
    t += 1
    cur = nxt[cur]
if cur == -1:
    print('exit', t)
else:
    print('cycle', t - step[cur])   # 재방문 지점부터 지금까지가 사이클
@@TESTS
--IN
5 0
1 2 3 1 -1
--OUT
cycle 3
--IN
4 3
1 2 -1 0
--OUT
exit 4
--IN
1 0
0
--OUT
cycle 1
--IN
2 0
-1 0
--OUT
exit 1
@@EXPL
(1) 접근·핵심 아이디어

- `next`가 하나뿐인 구조에서 경로는 한 갈래다. 그래서 출구를 만나거나(끝), 이미 본 방을 다시 만나거나(사이클) 둘 중 하나로 반드시 끝난다 — 최대 `n`번 이동이면 판정된다.
- 방문 시각을 기록해 두면, 재방문 순간 "그 방을 처음 본 시각부터 지금까지"가 정확히 사이클의 길이다. 시작 방이 사이클 밖(꼬리)에 있어도 이 식이 맞다.

(2) 코드 단계별

- `step[i] = -1`로 초기화하고, `cur`가 출구가 아니며 미방문인 동안 시각을 찍고 `cur = nxt[cur]`.
- 루프가 끝난 이유가 `cur == -1`이면 `exit`와 방문 수 `t`. 아니면 `cycle`과 `t - step[cur]`.
- 첫 예제: `0→1→2→3→1`, 1을 시각 1에 처음 봤고 지금 `t=4`라 사이클 `3`(방 1,2,3).

(3) 스스로 다시 짤 때 생각 순서

- "경로가 한 갈래 → 끝나거나 되돌아오거나"를 먼저 확인해 종료를 보장한다.
- 방문 여부만이 아니라 "언제" 방문했는지를 기록해야 길이를 구할 수 있음을 떠올린다.
- 경계: 자기 자신 포털(`cycle 1`), 시작 방이 출구(`exit 1`), 시작 방이 사이클 밖 꼬리인 경우.
```

**5) 뒤에서 k번째 손님 빼기** · Medium

- **요구사항**: 줄 선 손님 `n`명의 이름을 단일 연결 리스트로 만든 뒤, **뒤에서** `k`번째 손님을 줄에서 뺀 결과를 출력하라. 길이를 세지 말고, 앞 포인터를 `k`칸 먼저 보낸 뒤 두 포인터를 함께 전진시키는 한 번의 순회로 처리하라. 첫 손님이 빠지는 경우도 더미 헤드로 분기 없이 처리하라.
- **입력**: 첫 줄에 `n k`. 둘째 줄에 이름 `n`개(공백 구분). (`1 ≤ k ≤ n ≤ 100`)
- **출력**: 남은 줄(공백 구분). 비면 `empty`.
- **예제**: `5 2 / ann bob cat dan eve` → `ann bob cat eve` · `3 3 / x y z` → `y z`
- **셀프체크**: 두 포인터의 간격을 `k`로 두고, 앞 포인터가 마지막 노드에 닿았을 때 뒤 포인터가 "삭제할 노드의 직전"에 있는가? 더미에서 출발하면 `k == n`(첫 노드 삭제)도 같은 코드로 처리되는가? `n = 1`이면 `empty`인가?

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
n, k = int(data[0]), int(data[1])
names = data[2:2 + n]

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

dummy = Node(None)
tail = dummy
for v in names:
    tail.next = Node(v)
    tail = tail.next

fast = dummy
for _ in range(k):              # 앞 포인터를 k칸 먼저 보낸다
    fast = fast.next
slow = dummy
while fast.next:                # fast 가 마지막 노드에 닿을 때까지 함께 전진
    slow = slow.next
    fast = fast.next
slow.next = slow.next.next      # slow 는 삭제 대상의 직전

out = []
cur = dummy.next
while cur:
    out.append(cur.val)
    cur = cur.next
print(' '.join(out) if out else 'empty')
@@TESTS
--IN
5 2
ann bob cat dan eve
--OUT
ann bob cat eve
--IN
3 3
x y z
--OUT
y z
--IN
1 1
solo
--OUT
empty
--IN
3 1
a b c
--OUT
a b
@@EXPL
(1) 접근·핵심 아이디어

- 뒤에서 `k`번째는 "앞에서 `n-k+1`번째"지만 길이 `n`을 모른다고 치자. 두 포인터의 간격을 `k`로 고정하고 함께 전진하면, 앞 포인터가 끝에 닿는 순간 뒤 포인터가 뒤에서 `k+1`번째 — 즉 삭제할 노드의 직전 — 에 서 있다.
- 단일 리스트 삭제는 직전 노드가 필요하므로, 더미 헤드에서 출발해 "직전"이 항상 존재하게 만든다. 그러면 첫 노드 삭제(`k == n`)도 특별 취급이 없다.

(2) 코드 단계별

- 더미 뒤에 이름들을 이어 리스트를 만든다.
- `fast`를 더미에서 `k`칸 전진. `slow`는 더미에서 시작해 `fast.next`가 있는 동안 둘 다 한 칸씩.
- `slow.next = slow.next.next`로 건너뛰어 삭제. 이후 더미 다음부터 순회해 출력.
- `3 3`: `fast`가 z에 닿아 있어 루프가 0번, `slow`는 더미 → 더미.next(x)를 삭제.

(3) 스스로 다시 짤 때 생각 순서

- "간격 k인 두 포인터"라는 그림을 먼저 그리고, 멈추는 조건(`fast.next`가 None)에서 `slow` 위치를 확인한다.
- 삭제에는 직전 노드가 필요하니 더미에서 출발한다.
- 경계: 첫 노드 삭제, 마지막 노드 삭제(`k = 1`), 노드 하나뿐인 경우.
```

**6) 카드 줄 부분 뒤집기** · Medium

- **요구사항**: 카드 `n`장을 단일 연결 리스트로 이은 뒤, `l`번째부터 `r`번째(1-based, 양 끝 포함)까지의 구간만 링크를 뒤집어 출력하라. 값 배열을 만들어 뒤집는 방식이 아니라, 노드는 그대로 두고 `next` 링크만 바꿔야 한다.
- **입력**: 첫 줄에 `n l r`. 둘째 줄에 정수 `n`개. (`1 ≤ l ≤ r ≤ n ≤ 100`)
- **출력**: 결과 리스트(공백 구분).
- **예제**: `6 2 4 / 1 2 3 4 5 6` → `1 4 3 2 5 6` · `5 1 5 / 1 2 3 4 5` → `5 4 3 2 1`
- **셀프체크**: 구간 직전 노드 `prev`를 잡기 위해 더미에서 `l-1`칸 갔는가? 구간 안에서 `r-l+1`개 노드를 표준 4줄로 뒤집은 뒤, `prev.next`는 뒤집힌 구간의 새 앞(`p`)에, 구간의 원래 첫 노드 `first.next`는 구간 뒤 첫 노드 `cur`에 이었는가? `l == r`이면 변화가 없는가? `l = 1`(더미 덕에 분기 없음)과 `r = n`(뒤가 `None`) 경계가 맞는가?

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
n, l, r = int(data[0]), int(data[1]), int(data[2])
vals = [int(data[3 + i]) for i in range(n)]

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

dummy = Node(0)
tail = dummy
for v in vals:
    tail.next = Node(v)
    tail = tail.next

prev = dummy
for _ in range(l - 1):          # 구간 직전 노드
    prev = prev.next
cur = prev.next
first = cur                     # 구간의 원래 첫 노드 (뒤집힌 뒤엔 마지막이 됨)
p = None
for _ in range(r - l + 1):      # 구간 안 r-l+1 개 뒤집기
    nxt = cur.next
    cur.next = p
    p = cur
    cur = nxt
prev.next = p                   # 앞쪽을 뒤집힌 구간의 새 앞에 연결
first.next = cur                # 뒤집힌 구간의 끝을 구간 뒤 노드에 연결

out = []
cur = dummy.next
while cur:
    out.append(str(cur.val))
    cur = cur.next
print(' '.join(out))
@@TESTS
--IN
6 2 4
1 2 3 4 5 6
--OUT
1 4 3 2 5 6
--IN
5 1 5
1 2 3 4 5
--OUT
5 4 3 2 1
--IN
3 2 2
7 8 9
--OUT
7 8 9
--IN
4 3 4
1 2 3 4
--OUT
1 2 4 3
@@EXPL
(1) 접근·핵심 아이디어

- 전체 뒤집기(L3)의 4줄 뼈대를 "구간 안에서 정해진 개수만" 돌리고, 끝난 뒤 양쪽 경계를 다시 잇는 문제다. 뒤집기 자체보다 재연결 두 줄(`prev.next = p`, `first.next = cur`)이 핵심이다.
- 더미 헤드를 두면 `l = 1`(구간이 맨 앞)이어도 "직전 노드"가 존재해 코드가 갈라지지 않는다.

(2) 코드 단계별

- 더미에서 `l-1`칸 전진해 `prev`를 잡고, `cur = prev.next`가 구간 첫 노드. 이 노드를 `first`로 기억한다(뒤집힌 뒤 구간의 마지막이 됨).
- `r-l+1`번 표준 뒤집기(`nxt` 백업 → 화살표 반대 → 두 포인터 전진). 끝나면 `p`가 구간의 새 앞, `cur`가 구간 뒤 첫 노드(없으면 `None`).
- `prev.next = p`, `first.next = cur`로 앞뒤를 잇는다. `r = n`이면 `cur`가 `None`이라 자연히 끝 처리가 된다.

(3) 스스로 다시 짤 때 생각 순서

- "구간 직전, 구간 첫, 구간 뒤 첫" 세 위치를 그림에 표시한다.
- 뒤집기 루프를 "개수로" 돌리고, 루프 후 `p`와 `cur`가 무엇을 가리키는지 확인한다.
- 재연결 두 줄을 쓰고 `l == r`, `l = 1`, `r = n`에서 검산한다.
```

**7) 브라우저 방문 기록** · Medium

- **요구사항**: 브라우저는 처음 `home` 페이지에 있다. 명령은 세 가지다. `visit x`: 현재 페이지 뒤의 "앞으로 가기" 기록을 모두 버리고 `x`로 이동. `back`: 이전 페이지로(없으면 무시). `forward`: 다음 페이지로(없으면 무시). `back`/`forward` 명령마다 (무시된 경우도 포함해) 이동 후 현재 페이지를 출력하고, 모든 명령 후 마지막 줄에 남아 있는 전체 기록을 처음부터 끝까지 출력하라. 이중 연결 리스트의 노드 참조를 "현재 페이지"로 들고 다녀라.
- **입력**: 첫 줄에 명령 수 `q`. 다음 `q`줄에 명령. (`1 ≤ q ≤ 100`)
- **출력**: `back`/`forward`마다 현재 페이지 한 줄씩, 마지막 줄에 전체 기록(공백 구분).
- **예제**: `6 / visit a / visit b / back / visit c / forward / back` → `a` / `c` / `a` / `home a c` · `3 / back / visit x / back` → `home` / `home` / `home x`
- **셀프체크**: `visit`가 `cur.next = node`로 덮어써서 뒤쪽 기록(첫 예제의 `b`)이 통째로 잘리는가? `back`은 `cur.prev`가 `None`이 아닐 때만, `forward`는 `cur.next`가 `None`이 아닐 때만 이동하는가? 전체 기록은 현재 위치에서 `prev`로 맨 앞까지 간 뒤 `next`로 순회했는가?

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split('\n')
q = int(data[0])

class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

cur = Node('home')
out = []
for line in data[1:q + 1]:
    parts = line.split()
    if not parts:
        continue
    cmd = parts[0]
    if cmd == 'visit':
        node = Node(parts[1])
        node.prev = cur
        cur.next = node          # 기존 앞쪽 기록은 여기서 잘려 나간다
        cur = node
    elif cmd == 'back':
        if cur.prev is not None:
            cur = cur.prev
        out.append(cur.val)
    elif cmd == 'forward':
        if cur.next is not None:
            cur = cur.next
        out.append(cur.val)

first = cur
while first.prev is not None:    # prev 링크로 맨 앞까지
    first = first.prev
hist = []
node = first
while node is not None:          # next 링크로 끝까지
    hist.append(node.val)
    node = node.next
out.append(' '.join(hist))
print('\n'.join(out))
@@TESTS
--IN
6
visit a
visit b
back
visit c
forward
back
--OUT
a
c
a
home a c
--IN
3
back
visit x
back
--OUT
home
home
home x
--IN
5
visit a
visit b
back
back
forward
--OUT
a
home
a
home a b
@@EXPL
(1) 접근·핵심 아이디어

- 방문 기록은 "현재 위치를 중심으로 양쪽으로 움직이는" 구조라 이중 연결 리스트가 딱 맞다. 현재 페이지를 노드 참조 `cur`로 들고 있으면 `back`은 `cur.prev`, `forward`는 `cur.next`로 O(1)이다.
- `visit`의 핵심은 가지치기다. 새 노드를 `cur.next`에 덮어쓰면 그 뒤에 매달려 있던 기록이 더 이상 도달 불가능해져 자연히 버려진다 — 따로 삭제 루프가 필요 없다.

(2) 코드 단계별

- `home` 노드에서 시작한다(센티넬 없이 실제 페이지가 첫 노드).
- `visit x`: 새 노드의 `prev`를 `cur`로, `cur.next`를 새 노드로 걸고 `cur`를 옮긴다.
- `back`/`forward`: 이동 가능할 때만 옮기고, 어느 쪽이든 현재 페이지를 기록한다.
- 마지막에 `prev`로 맨 앞까지 되돌아간 뒤 `next`로 훑어 전체 기록을 만든다.

(3) 스스로 다시 짤 때 생각 순서

- "커서 = 노드 참조"로 두고 세 명령을 각각 `prev`/`next`/덮어쓰기로 대응시킨다.
- `visit`가 앞쪽 기록을 버린다는 규칙이 코드에서 어떻게 구현되는지(`cur.next = node`) 확인한다.
- 경계: 맨 앞에서 `back`, 맨 뒤에서 `forward`는 무시하되 출력은 해야 한다.
```

**8) 돌림판 선물 뽑기** · Medium

- **요구사항**: `1..n`번이 원형으로 앉아 있다. 처음 "현재 사람"은 `s`번이다. 라운드 `r`(1부터)마다 현재 사람에서 시계 방향으로 `m + r - 1`칸 이동한 사람이 선물을 받고 원에서 빠진다(0칸이면 현재 사람 자신). 빠진 사람의 시계 방향 바로 다음 사람이 새 "현재 사람"이 된다. 모두 빠질 때까지의 선물 받는 순서를 출력하라. `deque` 대신 `next`/`prev` 인덱스 배열로 원형 이중 연결 리스트를 직접 만들어 풀어라.
- **입력**: 한 줄에 `n s m`. (`1 ≤ s ≤ n ≤ 100`, `0 ≤ m ≤ 100`)
- **출력**: 선물 받는 순서 `n`개(공백 구분).
- **예제**: `5 1 1` → `2 5 1 3 4` · `4 3 0` → `3 1 2 4`
- **셀프체크**: 원형 초기화가 `nxt[i] = i % n + 1`, `prv[i] = (i-2) % n + 1`로 `n → 1`, `1 → n`이 이어지는가? 이동 칸 수를 남은 인원으로 나눈 나머지(`% remain`)로 줄여 헛도는 순회를 막았는가? 삭제 시 `nxt[prv[cur]]`와 `prv[nxt[cur]]` 두 링크를 모두 고쳤는가? 첫 예제 1라운드에서 `1`번에서 1칸 이동한 `2`번이 빠지고 현재가 `3`번이 되는지 손으로 확인했는가?

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
n, s, m = int(data[0]), int(data[1]), int(data[2])
nxt = [0] * (n + 1)
prv = [0] * (n + 1)
for i in range(1, n + 1):           # 원형 초기화 (1..n, n 의 다음은 1)
    nxt[i] = i % n + 1
    prv[i] = (i - 2) % n + 1
cur = s
remain = n
order = []
r = 1
while remain > 0:
    steps = (m + r - 1) % remain    # 남은 인원만큼만 돌면 충분
    for _ in range(steps):
        cur = nxt[cur]
    order.append(str(cur))
    nxt[prv[cur]] = nxt[cur]        # 원에서 빼기: 이웃끼리 잇기
    prv[nxt[cur]] = prv[cur]
    cur = nxt[cur]                  # 다음 사람이 새 현재
    remain -= 1
    r += 1
print(' '.join(order))
@@TESTS
--IN
5 1 1
--OUT
2 5 1 3 4
--IN
4 3 0
--OUT
3 1 2 4
--IN
1 1 5
--OUT
1
--IN
6 2 3
--OUT
5 4 1 2 6 3
@@EXPL
(1) 접근·핵심 아이디어

- 원형 리스트를 인덱스 배열 두 개로 만든다. `nxt`는 시계 방향, `prv`는 반시계 방향이며 끝이 없으므로 `n`의 다음은 `1`, `1`의 이전은 `n`으로 초기화한다.
- 요세푸스와 같은 "돌면서 하나씩 빼기"지만 이동 칸 수가 라운드마다 늘어난다. 한 바퀴는 남은 인원 수이므로 `steps % remain`으로 줄이면 100칸을 실제로 돌지 않아도 된다(`remain = 1`이면 항상 0칸).
- 빼기는 이중 링크라 직전 노드를 찾지 않고 `nxt[prv[cur]]`, `prv[nxt[cur]]` 두 줄로 O(1).

(2) 코드 단계별

- `nxt[i] = i % n + 1`(n이면 1), `prv[i] = (i-2) % n + 1`(1이면 n)로 원을 만든다.
- 라운드마다 `steps = (m + r - 1) % remain`만큼 `cur = nxt[cur]`로 이동한 뒤 기록.
- 이웃끼리 이어 `cur`를 빼고, `cur = nxt[cur]`(방금 뺀 사람의 다음)를 새 현재로. `remain`, `r` 갱신.
- `5 1 1`: 1라운드 `1→2`(2 제거, 현재 3), 2라운드 2칸 `3→4→5`(5 제거, 현재 1), 3라운드 3칸 `1→3→4→1`(1 제거) … → `2 5 1 3 4`.

(3) 스스로 다시 짤 때 생각 순서

- 원형 초기화 공식을 `n=1`(자기 자신을 가리킴)에서도 검산한다.
- "몇 칸 이동 → 기록 → 빼기 → 현재 갱신"의 4단계 루프를 세우고, 이동 칸 수를 `% remain`으로 줄인다.
- 삭제가 두 링크를 모두 고치는지, 빼고 난 뒤 현재 사람이 누구인지(뺀 사람의 다음) 규칙대로 맞추는지 확인한다.
```

**9) 무대 등장 순서 재배열** · Hard

- **요구사항**: 출연자 `a1, a2, …, an`이 단일 연결 리스트로 이어져 있다. 등장 순서를 `a1, an, a2, a(n-1), a3, …`처럼 앞과 뒤에서 번갈아 뽑는 순서로 **링크만 바꿔** 재배열하라. 값 배열을 새로 만들지 말고 (1) 느린/빠른 포인터로 중간을 찾아 둘로 자르고 (2) 뒷부분을 뒤집은 뒤 (3) 두 리스트를 한 노드씩 번갈아 잇는다.
- **입력**: 첫 줄에 `n`. 둘째 줄에 정수 `n`개. (`1 ≤ n ≤ 100`)
- **출력**: 재배열된 리스트(공백 구분).
- **예제**: `5 / 1 2 3 4 5` → `1 5 2 4 3` · `4 / 1 2 3 4` → `1 4 2 3`
- **셀프체크**: 중간 찾기 조건을 `while fast.next and fast.next.next`로 두어 홀수 길이면 앞부분이 한 개 더 길게 잘리는가(그래야 마지막에 앞부분 꼬리가 자연스럽게 남는다)? 자른 뒤 `slow.next = None`으로 앞부분을 끊었는가? 번갈아 잇기에서 두 리스트의 다음 노드를 **먼저 백업**한 뒤 링크를 바꾸는가? `n = 1`, `n = 2`에서 변화 없이 나오는가?

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
n = int(data[0])
vals = [int(data[1 + i]) for i in range(n)]

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

head = None
tail = None
for v in vals:
    node = Node(v)
    if head is None:
        head = tail = node
    else:
        tail.next = node
        tail = node

# (1) 중간 찾기: 홀수면 앞부분이 하나 더 길게
slow = fast = head
while fast.next and fast.next.next:
    slow = slow.next
    fast = fast.next.next
second = slow.next
slow.next = None                 # 앞부분 끊기

# (2) 뒷부분 뒤집기
prev = None
cur = second
while cur:
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt
second = prev

# (3) 번갈아 잇기
first = head
while second:
    n1 = first.next              # 다음 노드들을 먼저 백업
    n2 = second.next
    first.next = second
    second.next = n1
    first = n1
    second = n2

out = []
cur = head
while cur:
    out.append(str(cur.val))
    cur = cur.next
print(' '.join(out))
@@TESTS
--IN
5
1 2 3 4 5
--OUT
1 5 2 4 3
--IN
4
1 2 3 4
--OUT
1 4 2 3
--IN
1
9
--OUT
9
--IN
2
1 2
--OUT
1 2
@@EXPL
(1) 접근·핵심 아이디어

- "앞에서 하나, 뒤에서 하나"를 단일 리스트에서 직접 하면 뒤 노드를 매번 끝까지 찾아야 해 O(n^2)이다. 대신 뒷부분을 뒤집어 두면 두 리스트 모두 앞에서부터 꺼내면 되므로 O(n)으로 떨어진다.
- 그래서 세 도구가 결합된다: 중간 찾기(3번 문제), 뒤집기(L3), 두 리스트 교대로 잇기(병합의 변형). 각 단계가 끝날 때 어떤 포인터가 무엇을 가리키는지가 전부다.

(2) 코드 단계별

- 중간 찾기에서 `fast.next and fast.next.next` 조건을 쓰면 `n=5`일 때 `slow`가 3에서 멈춰 앞 `1 2 3`, 뒤 `4 5`가 된다. `slow.next = None`으로 끊는 걸 빼먹으면 순환이 생긴다.
- 뒷부분을 표준 4줄로 뒤집어 `5 4`를 만든다.
- 교대 잇기: `first`의 다음(`n1`)과 `second`의 다음(`n2`)을 먼저 저장한 뒤 `first → second → n1` 순으로 잇고 둘을 전진. 뒷부분이 먼저 소진되면 앞부분의 남은 꼬리(홀수일 때 가운데 노드)가 그대로 끝에 남는다.
- `n=1`: `second`가 `None`이라 (2)(3)이 모두 건너뛰어진다. `n=2`: 앞 `1`, 뒤 `2` → `1 2`.

(3) 스스로 다시 짤 때 생각 순서

- "뒤에서 꺼내기가 비싸다 → 뒷부분을 뒤집어 앞에서 꺼내자"는 전환을 먼저 떠올린다.
- 세 단계의 입력/출력 포인터(`head`, `second`, 끊긴 자리)를 종이에 적는다.
- 교대 잇기에서는 "백업 먼저, 연결 나중"을 지키고, `n = 1, 2`와 홀수/짝수로 검산한다.
```

**10) 줄 서기 명령 처리** · Hard

- **요구사항**: 처음에 줄은 비어 있다. 명령을 처리하라. `push x`(맨 뒤에 `x`), `after x y`(`x` 바로 뒤에 `y` 삽입), `before x y`(`x` 바로 앞에 `y` 삽입), `remove x`(`x` 제거). 이름은 모두 서로 다르고, 기준이 되는 `x`는 항상 줄에 있다. 모든 명령 후 줄을 앞→뒤로 한 줄, 뒤→앞으로 한 줄 출력하라. 이름→노드 `dict`와 양끝 센티넬을 둔 이중 연결 리스트로 모든 명령을 O(1)에 처리하고, 앞→뒤 순회는 클래스의 `__iter__`(제너레이터)로 구현하라.
- **입력**: 첫 줄에 명령 수 `q`. 다음 `q`줄에 명령. (`1 ≤ q ≤ 100`)
- **출력**: 첫 줄에 앞→뒤 순서, 둘째 줄에 뒤→앞 순서(각각 공백 구분, 비면 `empty`).
- **예제**: `6 / push a / push b / after a c / before a d / remove b / push e` → `d a c e` / `e c a d` · `2 / push x / remove x` → `empty` / `empty`
- **셀프체크**: `push`는 `tail.prev` 뒤에, `before x y`는 `x.prev` 뒤에 삽입하는 식으로 모든 삽입을 "노드 `a` 바로 뒤에 넣기" 하나로 통일했는가? 삽입에서 링크 4개(새 노드의 prev/next, 양쪽 이웃의 next/prev)를 모두 세팅했는가? `remove`가 `dict`에서도 지우는가? 역방향은 배열 뒤집기가 아니라 `prev` 링크를 따라 만들었는가? `for name in line:`이 동작하도록 `__iter__`가 값을 `yield`하는가?

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split('\n')
q = int(data[0])

class Node:
    def __init__(self, val=None):
        self.val = val
        self.prev = None
        self.next = None

class Line:
    def __init__(self):
        self.head = Node()             # 센티넬
        self.tail = Node()             # 센티넬
        self.head.next = self.tail
        self.tail.prev = self.head
        self.pos = {}                  # 이름 -> 노드
    def insert_after(self, a, name):   # 모든 삽입을 이 하나로 통일
        node = Node(name)
        b = a.next
        node.prev = a
        node.next = b
        a.next = node
        b.prev = node
        self.pos[name] = node
    def remove(self, name):
        node = self.pos.pop(name)
        node.prev.next = node.next
        node.next.prev = node.prev
    def __iter__(self):                # 앞 -> 뒤 (for name in line)
        cur = self.head.next
        while cur is not self.tail:
            yield cur.val
            cur = cur.next
    def backward(self):                # 뒤 -> 앞 (prev 링크)
        cur = self.tail.prev
        while cur is not self.head:
            yield cur.val
            cur = cur.prev

line = Line()
for raw in data[1:q + 1]:
    parts = raw.split()
    if not parts:
        continue
    cmd = parts[0]
    if cmd == 'push':
        line.insert_after(line.tail.prev, parts[1])
    elif cmd == 'after':
        line.insert_after(line.pos[parts[1]], parts[2])
    elif cmd == 'before':
        line.insert_after(line.pos[parts[1]].prev, parts[2])
    elif cmd == 'remove':
        line.remove(parts[1])

fwd = list(line)
bwd = list(line.backward())
print(' '.join(fwd) if fwd else 'empty')
print(' '.join(bwd) if bwd else 'empty')
@@TESTS
--IN
6
push a
push b
after a c
before a d
remove b
push e
--OUT
d a c e
e c a d
--IN
2
push x
remove x
--OUT
empty
empty
--IN
4
push a
before a b
before b c
after a d
--OUT
c b a d
d a b c
@@EXPL
(1) 접근·핵심 아이디어

- "이름으로 노드를 찾아 그 앞뒤에 넣거나 빼기"는 배열이면 매번 O(n) 탐색·밀기가 든다. 이중 연결 리스트 + `dict`(이름→노드)를 결합하면 찾기 O(1), 삽입·삭제 O(1)이다 — LRU(L4)와 같은 뼈대.
- 양끝 센티넬을 두면 `push`(맨 뒤), `before`(맨 앞이 될 수도 있음), `remove`(첫/마지막 노드일 수도 있음)가 전부 경계 분기 없이 같은 코드로 처리된다. 삽입은 "노드 `a` 바로 뒤에 넣기" 하나로 통일하고, `push`는 `a = tail.prev`, `before x`는 `a = x.prev`로 바꿔 부른다.
- 순회를 `__iter__`에 숨기면 사용하는 쪽은 노드나 링크를 몰라도 `for name in line:`으로 값만 받는다.

(2) 코드 단계별

- `Line.__init__`: 센티넬 두 개를 서로 잇고 빈 `dict`를 둔다.
- `insert_after(a, name)`: 이웃 `b = a.next`를 확보한 뒤 새 노드의 `prev/next`, 그리고 `a.next`, `b.prev` 네 링크를 세팅하고 `dict`에 등록.
- `remove(name)`: `dict`에서 꺼내며 지우고 이웃끼리 직접 잇는다(링크 2개).
- 명령 루프에서 네 명령을 위 두 메서드로 옮기고, 마지막에 `list(line)`(앞→뒤)과 `list(line.backward())`(뒤→앞)을 출력.
- 첫 예제: `a b` → `a c b` → `d a c b` → `d a c` → `d a c e`.

(3) 스스로 다시 짤 때 생각 순서

- "찾기는 dict, 순서는 이중 링크"라는 두 축을 먼저 세운다.
- 삽입 함수를 하나로 통일하고 나머지 명령을 그 호출로 표현할 수 있는지 확인한다.
- 링크 4개/2개를 빠짐없이 쓰고, 빈 줄(`empty`)·맨 앞 삽입·마지막 노드 제거를 예제로 검산한다.
```
