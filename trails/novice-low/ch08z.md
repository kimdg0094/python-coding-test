## L7. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 레슨은 새 문제를 풀지 않는다. Ch8에서 배운 것들이 서로 어떻게 이어지는지 한 장으로 정리하고, 다음 문제에서 바로 꺼내 쓸 뼈대와 자주 밟는 지뢰를 모아 둔다.

- 2차원 배열 문제는 겉모습이 아무리 달라도 결국 세 가지 질문으로 갈린다. (1) 표를 어디서 얻는가(입력/직접 생성), (2) 칸의 값을 무엇으로 정하는가(입력값/좌표 규칙/방문 순서), (3) 이웃을 보는가(격자).

**개념 지도**

세 갈래가 모두 같은 엔진(모든 칸을 도는 이중 반복)으로 모인다. 갈라지는 곳과 다시 만나는 곳을 함께 보자.

```text
                 2D array : a list whose items are lists
                                   |
     +----------------+------------+------------+----------------+
     |                |                         |                |
  L1 input        L2 create              L3 / L4 fill        L5 grid
  read n lines    [[0]*m                 i, j -> value       cell (r, c)
  append rows      for _ in range(n)]    pattern / order     4 neighbors
     |                |                         |                |
     +----------------+------------+------------+----------------+
                                   |
                   every branch ends at the same engine
                      for i in range(n):
                          for j in range(m):
                              ... board[i][j] ...
                                   |
                  +----------------+----------------+
                  |                                 |
            read a cell                       write a cell
            total / cnt / max                 board[i][j] = value
            find a position                   new board : T , rotate
```

읽기만 하면 원본 한 장으로 충분하고, 쓰기가 섞이면 결과를 담을 **새 표**가 필요할 때가 많다. 특히 이웃을 보며 값을 갱신하는 문제는 원본을 덮어쓰면 안 된다.

격자(L5)에서만 추가로 필요한 것이 이웃 좌표와 경계 검사다.

```text
  neighbor offsets              bounds check (n rows, m cols)
   dr = [-1, 1, 0, 0]            0 <= nr < n and 0 <= nc < m
   dc = [ 0, 0,-1, 1]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^ check FIRST
         up dn lt rt             then read board[nr][nc]

        (r-1, c)                 r - 1 = -1  -> reads the LAST row, no error
            |                    r + 1 = n   -> IndexError, it does crash
  (r, c-1)-(r, c)-(r, c+1)       so one side fails loudly, the other quietly
            |
        (r+1, c)
```

**뼈대 코드**

```python
# 1) 격자 입력 + 모든 칸 순회 (합·개수·최댓값)
n, m = map(int, input().split())
board = []
for i in range(n):
    row = list(map(int, input().split()))
    board.append(row)

total = 0
cnt = 0
mx = board[0][0]          # 0이 아니라 첫 칸에서 시작 (음수 대비)
for i in range(n):
    for j in range(m):
        v = board[i][j]
        total += v
        if v >= 5:        # ← 문제마다 바뀜 (세는 조건)
            cnt += 1
        if v > mx:        # ← 문제마다 바뀜 (> 는 첫 등장, >= 는 마지막 등장)
            mx = v
print(total, cnt, mx)
```

```python
# 2) 새 표를 만들어 칸 규칙대로 채우기 (패턴)
n, m = map(int, input().split())
board = [[0] * m for _ in range(n)]     # 행마다 독립된 리스트
for i in range(n):
    for j in range(m):
        if (i + j) % 2 == 0:            # ← 문제마다 바뀜 (칸 조건)
            board[i][j] = 1             # ← 문제마다 바뀜 (넣을 값)
for i in range(n):
    print(*board[i])
```

```python
# 3) 순서대로 채우기 (행 우선 / 지그재그)
board = [[0] * m for _ in range(n)]
num = 1
for i in range(n):
    if i % 2 == 0:                      # ← 지그재그가 아니면 이 분기를 없앤다
        for j in range(m):
            board[i][j] = num
            num += 1
    else:
        for j in range(m - 1, -1, -1):  # 거꾸로: 시작 m-1, 끝 -1(미포함), 걸음 -1
            board[i][j] = num
            num += 1
```

```python
# 4) 4방향 이웃 보기 (경계 검사 포함)
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]
res = [[0] * m for _ in range(n)]       # 결과는 반드시 새 표에
for r in range(n):
    for c in range(m):
        cnt = 0
        for d in range(4):
            nr = r + dr[d]
            nc = c + dc[d]
            # 0 <= nr < n 은 nr >= 0 and nr < n 을 한 번에 쓴 것이다
            if 0 <= nr < n and 0 <= nc < m:
                if board[nr][nc] == 1:  # ← 문제마다 바뀜 (이웃 판정)
                    cnt += 1
        res[r][c] = cnt
```

```python
# 5) 크기가 바뀌는 변환 (전치 / 시계 90도 회전)
t = [[0] * n for _ in range(m)]         # 결과는 m행 n열 (n, m 자리 교환)
for i in range(n):
    for j in range(m):
        t[j][i] = board[i][j]                # 전치
        # t[j][n - 1 - i] = board[i][j]      # ← 시계 90도 회전이면 이 줄
for i in range(m):                      # 출력 줄 수도 m으로 바뀐다
    print(*t[i])
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 표 전체의 합·개수 | 이중 반복 1회 + 누적 변수 | 모든 칸을 한 번씩만 보면 충분 | O(n·m) |
| 행마다 결과가 하나씩 | 바깥 `i`, 안쪽 `j`, 합 초기화는 바깥 반복 **안** | 합의 수명이 "행 하나" | O(n·m) |
| 열마다 결과가 하나씩 | 바깥 `j`, 안쪽 `i` (대입은 여전히 `board[i][j]`) | 열 단위로 훑어야 함 | O(n·m) |
| 칸 값이 좌표로 정해짐 | 0 표 생성 + `if` 조건식 | 한 칸 기준 질문으로 환원 | O(n·m) |
| 채우는 순서가 문제 | 카운터 `num` + 방문 순서 반복 | 값은 순서대로, 순서만 설계 | O(n·m) |
| 이웃을 봐야 함 | `dr`/`dc` 방향표 + 경계 검사 | 네 방향을 한 반복으로 처리 | O(4·n·m) |
| 결과 크기가 달라짐(전치·회전) | 새 표 `[[0]*n for _ in range(m)]` | 행·열 수가 뒤바뀜 | O(n·m) |
| 회전을 `k`번 | `k % 4`로 줄인 뒤 반복 | 4번이면 제자리 | O(n·m) |
| 이웃 값으로 표를 갱신 | 결과 전용 새 표 | 원본을 덮으면 뒷 칸이 오염됨 | O(n·m) |
| 나선(달팽이) 채우기 | 방향표 + "밖이거나 이미 채움" 판정 | 막히면 시계로 한 번 꺾기 | O(n·m) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: `board[i][j]`에서 `i`가 행이고 `j`가 열인 이유와, `board[i]`가 값이 아니라 리스트인 이유.
- [ ] 설명할 수 있다: `[[0]*m for _ in range(n)]`과 `[[0]*m]*n`이 만드는 모양의 차이, 그리고 후자에서 한 칸만 바꿔도 모든 행이 바뀌는 이유.
- [ ] 설명할 수 있다: 행 우선과 열 우선 순회의 차이, 그리고 무엇을 바깥 반복으로 두면 어느 순서가 되는지.
- [ ] 설명할 수 있다: `range(m-1, -1, -1)`이 왜 `m-1`부터 `0`까지 주는지(끝값 미포함 규칙).
- [ ] 설명할 수 있다: 체스판·대각선·테두리·십자를 각각 어떤 한 칸 조건식으로 쓰는지.
- [ ] 설명할 수 있다: 반대 대각선 조건이 `i + j == n - 1`인 이유.
- [ ] 설명할 수 있다: 격자 밖 좌표를 읽었을 때 파이썬이 한쪽은 조용히 반대편을 주고 다른 쪽은 오류를 내는 이유.
- [ ] 설명할 수 있다: `and`로 조건을 이을 때 범위 검사를 왼쪽에 두어야 하는 이유.
- [ ] 설명할 수 있다: 전치·회전에서 새 표의 크기가 `m행 n열`이 되는 이유와, 출력 줄 수가 함께 바뀌는 이유.
- [ ] 설명할 수 있다: 회전 `k`번을 `k % 4`로 줄여도 되는 이유.
- [ ] 설명할 수 있다: 이웃 개수 지도를 만들 때 원본을 덮어쓰면 왜 틀리는지.
- [ ] 설명할 수 있다: 최댓값 후보의 시작값을 0이 아니라 `board[0][0]`으로 두는 이유.
- [ ] 설명할 수 있다: 모든 칸을 한 번씩 보는 코드의 비용이 왜 `n × m`에 비례하는지.

**⚠️ 자주 하는 실수**

**(1) 행과 열을 뒤바꿔 쓴다**

```python
# ❌ 틀린 코드
n, m = map(int, input().split())
board = [[0] * n for _ in range(m)]   # 행이 m개, 열이 n개가 되어 버림
for i in range(n):
    for j in range(m):
        board[i][j] = 0               # n != m 이면 IndexError
```

왜: 대괄호 순서는 `[행][열]`인데 생성식은 `[[0] * (열 수) for _ in range(행 수)]`다. `n`(행)과 `m`(열)의 자리가 서로 반대라 헷갈리기 쉽다. 정사각형 입력으로만 시험하면 이 실수가 드러나지 않는다.

```python
# ✅ 고친 코드
board = [[0] * m for _ in range(n)]   # 행 n개, 각 행의 길이 m
for i in range(n):
    for j in range(m):
        board[i][j] = 0
```

**(2) `[[0]*m]*n`으로 표를 만든다**

```python
# ❌ 틀린 코드
board = [[0] * m] * n
board[0][0] = 9
print(board)      # 모든 행의 첫 칸이 9가 된다
```

왜: `* n`은 리스트를 `n`번 복사하지 않는다. `[0]*m`이 한 번만 계산되어 리스트 **하나**가 만들어지고, `n`개의 자리가 모두 그 하나를 가리킨다. 그래서 어느 행을 고쳐도 전부 같이 바뀐다.

```python
# ✅ 고친 코드
board = [[0] * m for _ in range(n)]   # 반복마다 [0]*m 을 다시 계산 → 독립된 리스트
board[0][0] = 9
```

**(3) 이웃을 볼 때 경계를 확인하지 않는다**

```python
# ❌ 틀린 코드
total = 0
total += board[r - 1][c]     # r == 0 이면 board[-1] = 맨 아랫줄을 더한다
total += board[r][c - 1]     # c == 0 이면 맨 오른쪽 칸을 더한다
```

왜: 파이썬의 음수 인덱스는 "뒤에서부터 세기"다. `board[-1]`은 오류가 아니라 마지막 행이므로, 프로그램이 멈추지도 않고 값만 조용히 틀린다. 반대로 `r + 1`이 `n`이 되면 그때는 `IndexError`가 난다.

```python
# ✅ 고친 코드
total = 0
if r - 1 >= 0:
    total += board[r - 1][c]
if c - 1 >= 0:
    total += board[r][c - 1]
```

**(4) 범위 검사와 값 검사의 순서를 뒤집는다**

```python
# ❌ 틀린 코드
if board[nr][nc] == 1 and 0 <= nr < n and 0 <= nc < m:
    cnt += 1
```

왜: `and`는 왼쪽부터 계산한다. 왼쪽에서 이미 `board[nr][nc]`를 읽어 버리므로, `nr`이 `n`이면 범위 검사에 닿기도 전에 `IndexError`가 난다. 검사는 접근보다 **먼저** 해야 의미가 있다.

```python
# ✅ 고친 코드
if 0 <= nr < n and 0 <= nc < m and board[nr][nc] == 1:
    cnt += 1
```

**(5) 행별 합인데 합 변수를 반복 밖에 둔다**

```python
# ❌ 틀린 코드
total = 0
for i in range(n):
    for j in range(m):
        total += board[i][j]
    print(total)      # 앞 행의 합이 계속 얹혀 누적된다
```

왜: `total`의 수명이 "표 전체"가 되어 버렸다. 행마다 답을 내려면 수명도 "행 하나"여야 하므로, 초기화가 바깥 반복 **안쪽**으로 들어가야 한다.

```python
# ✅ 고친 코드
for i in range(n):
    total = 0            # 행이 바뀔 때마다 다시 0
    for j in range(m):
        total += board[i][j]
    print(total)
```

**(6) 이웃 계산 결과를 원본에 바로 덮어쓴다**

```python
# ❌ 틀린 코드
for r in range(n):
    for c in range(m):
        board[r][c] = count_neighbors(board, r, c)   # 원본을 갱신
```

왜: `(0,0)`을 갱신한 뒤 `(0,1)`을 계산할 때, 이미 바뀐 `(0,0)`의 값을 "원래 값"으로 착각해 읽는다. 앞 칸의 결과가 뒤 칸의 입력을 오염시킨다.

```python
# ✅ 고친 코드
res = [[0] * m for _ in range(n)]
for r in range(n):
    for c in range(m):
        res[r][c] = count_neighbors(board, r, c)     # 원본은 그대로 둔다
```

**(7) 회전한 뒤 크기를 그대로 둔다**

```python
# ❌ 틀린 코드
for t in range(k):
    new = [[0] * n for _ in range(m)]
    for i in range(n):
        for j in range(m):
            new[j][n - 1 - i] = board[i][j]
    board = new           # n, m 을 안 바꿔 다음 회전에서 어긋난다
```

왜: 한 번 회전하면 표가 `n행 m열`에서 `m행 n열`이 된다. `n`과 `m`을 바꾸지 않으면 두 번째 회전의 반복 범위가 실제 크기와 달라져 `IndexError`가 나거나 값이 뒤엉킨다.

```python
# ✅ 고친 코드
for t in range(k % 4):        # 4번이면 제자리이므로 미리 줄인다
    new = [[0] * n for _ in range(m)]
    for i in range(n):
        for j in range(m):
            new[j][n - 1 - i] = board[i][j]
    board = new
    tmp = n
    n = m
    m = tmp                   # 크기도 함께 교환
```

**다음 챕터로**

- 격자 위에서 "이웃을 보고 조건에 따라 움직이는" 사고는 이후 시뮬레이션·탐색 문제의 공통 뼈대다. `dr`/`dc` 방향표와 경계 검사는 그대로 재사용된다.

- 표를 새로 만들어 결과를 담는 습관은 누적합·DP 표처럼 "칸에 계산 결과를 저장하는" 유형으로 이어진다.

- 다음 챕터의 문자열도 "인덱스로 접근하는 한 줄짜리 칸"이라는 점에서 여기의 격자와 같은 감각을 쓴다.
