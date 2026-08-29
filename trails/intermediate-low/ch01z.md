## L7. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터는 "격자 위에서 규칙을 그대로 옮긴다"는 하나의 기술을 다섯 갈래로 펼친 것이다.
L1이 좌표계·방향·경계라는 바닥을 깔고, L2~L3이 "값들이 움직인다", L4~L5가 "객체가
움직인다"로 갈라진다. 마지막 절의 실수 목록은 실제 채점에서 오답을 만드는 것들만 모았다.

**개념 지도**

```text
 L1  grid scan
     coords (r,c) / dir vectors dr,dc / in_range()
       |
       +---> L2  push & gravity
       |         one-line function + transpose / reverse  ==> 4 dirs
       |           |
       |           +---> L3  clear & fall
       |                 mark all -> clear once -> fall -> repeat
       |
       +---> L4  a single actor
                 state = (r, c, dir) + turn / reflect / wrap
                   |
                   +---> L5  many actors
                         simultaneous vs sequential update
                           |
                           +---> collision: group by destination cell
```

위쪽 두 줄(좌표계·경계 검사)이 무너지면 아래 전부가 무너진다. 왼쪽 가지(L2·L3)는
"칸에 담긴 값"이 주인공이고, 오른쪽 가지(L4·L5)는 "칸 위를 걷는 물체"가 주인공이다.

```text
 what is actually moving?
   nothing, only counting          -> L1  double for loop + in_range
   a whole row or column of values -> L2  push_left + rotate trick
   values vanish, then refill      -> L3  mark -> clear -> fall -> loop
   exactly one actor               -> L4  (r, c, dir) state machine
   many actors at the same time    -> L5  new board / dest grouping
```

문제를 읽고 이 다섯 줄 중 하나를 고르는 것이 첫 번째 결정이다. 고르고 나면 아래 뼈대를
그대로 꺼내 쓰면 된다.

**뼈대 코드**

(1) 격자 입력 · 순회 · 경계 검사 — 모든 문제의 첫 20줄

```python
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    R = int(data[idx]); idx += 1
    C = int(data[idx]); idx += 1
    g = []
    for r in range(R):
        g.append([int(data[idx + c]) for c in range(C)])   # ← 문제마다 바뀜(정수/문자)
        idx += C

    DR = [-1, 0, 1, 0]          # 북 동 남 서 (시계 방향)
    DC = [0, 1, 0, -1]

    def in_range(r, c):
        return 0 <= r < R and 0 <= c < C

    for r in range(R):
        for c in range(C):
            for d in range(4):                  # ← 문제마다 바뀜(4방향/8방향)
                nr, nc = r + DR[d], c + DC[d]
                if in_range(nr, nc):
                    pass                        # ← 문제마다 바뀜(세기/최댓값/표시)
main()
```

(2) 한 줄 밀기 + 전치·회전 유틸 — 좌 밀기 하나로 네 방향을 만든다

```python
def push_left(row):
    vals = [x for x in row if x != 0]      # 빈칸 제거, 순서 유지
    res, i = [], 0
    while i < len(vals):
        if i + 1 < len(vals) and vals[i] == vals[i + 1]:
            res.append(vals[i] * 2)        # ← 문제마다 바뀜(합치기 규칙)
            i += 2                         # 2씩 건너뛰어 이중 합치기 차단
        else:
            res.append(vals[i])
            i += 1
    return res + [0] * (len(row) - len(res))

def transpose(g):
    return [list(col) for col in zip(*g)]

def flip_h(g):                              # 각 행을 좌우 반전
    return [row[::-1] for row in g]

def move(g, d):
    if d == 'L':
        return [push_left(row) for row in g]
    if d == 'R':
        return flip_h([push_left(row) for row in flip_h(g)])
    if d == 'U':
        return transpose([push_left(row) for row in transpose(g)])
    if d == 'D':
        t = transpose(g)
        return transpose(flip_h([push_left(row) for row in flip_h(t)]))
```

`push_left` 하나만 테스트해 두면 네 방향이 자동으로 옳다. 방향마다 따로 짜지 않는다.

(3) 연쇄 제거 · 낙하 루프 — 표시 → 종료 판정 → 일괄 제거 → 낙하

```python
def mark(g, R, C, K):
    boom = [[False] * C for _ in range(R)]
    hit = False
    for r in range(R):                       # 가로 런
        run = 1
        for c in range(1, C + 1):
            same = c < C and g[r][c] != 0 and g[r][c] == g[r][c - 1]
            if same:
                run += 1
            else:
                if run >= K:                 # ← 문제마다 바뀜(K, 판정 방식)
                    for k in range(c - run, c):
                        boom[r][k] = True
                    hit = True
                run = 1
    return boom, hit                          # 세로 런도 같은 모양으로 추가

def fall(g, R, C):
    for c in range(C):
        vals = [g[r][c] for r in range(R) if g[r][c] != 0]
        for r in range(R):
            i = r - (R - len(vals))
            g[r][c] = vals[i] if i >= 0 else 0

def run_until_stable(g, R, C, K):
    while True:
        boom, hit = mark(g, R, C, K)
        if not hit:                           # 종료 조건: 이번 라운드에 아무것도 안 터짐
            break
        for r in range(R):
            for c in range(C):
                if boom[r][c]:
                    g[r][c] = 0               # 표시된 것을 한꺼번에 제거
        fall(g, R, C)
```

(4) 단일 객체 이동 — 상태 (r, c, d) + 회전 · 반사 · 래핑

```python
DR = [-1, 0, 1, 0]
DC = [0, 1, 0, -1]

def simulate(R, C, sr, sc, sd, cmds):
    r, c, d = sr, sc, sd
    for ch in cmds:                            # ← 문제마다 바뀜(명령 집합)
        if ch == 'R':
            d = (d + 1) % 4
        elif ch == 'L':
            d = (d + 3) % 4
        elif ch == 'F':
            nr, nc = r + DR[d], c + DC[d]
            if 0 <= nr < R and 0 <= nc < C:
                r, c = nr, nc
            else:
                pass          # ← 문제마다 바뀜(무시 / 반사 / 회전 / 래핑)
    return r, c, d

def reflect(dr, dc, r, c, R, C):
    if not (0 <= r < R):
        dr = -dr             # 위/아래 벽: 행 성분만 부호 반전
    if not (0 <= c < C):
        dc = -dc             # 좌/우 벽: 열 성분만 부호 반전
    return dr, dc
```

명령 수 T가 매우 크면 상태 `(r, c, d)`를 집합에 넣어 사이클을 찾는다. 상태가
`R*C*4`개뿐이라 반드시 반복되고, 주기를 찾으면 T를 나머지 연산으로 줄일 수 있다.

(5) 여러 객체 동시 이동 + 충돌 — 도착 칸으로 그룹핑

```python
from collections import defaultdict

def one_turn(objs, R, C):                      # objs: [(r, c, size, d), ...]
    dest = defaultdict(list)
    for (r, c, s, d) in objs:
        nr, nc = r + DR[d], c + DC[d]
        if not (0 <= nr < R and 0 <= nc < C):
            nr, nc, d = r, c, (d + 2) % 4      # ← 문제마다 바뀜(벽 처리)
        dest[(nr, nc)].append((s, d))
    new_objs = []
    for pos, group in dest.items():
        if len(group) == 1:
            s, d = group[0]
            new_objs.append((pos[0], pos[1], s, d))
        else:
            group.sort(key=lambda x: -x[0])    # ← 문제마다 바뀜(생존/합체 규칙)
            total = sum(s for s, _ in group)
            new_objs.append((pos[0], pos[1], total, group[0][1]))
    return new_objs
```

동시 갱신이면 **원본을 읽고 결과는 새 리스트/새 격자에** 쓴다. 순차 갱신이면 정렬 키를
문제 문장 그대로 못 박은 뒤 하나씩 즉시 반영한다.

(6) 시간 순 이벤트 루프 — "T초 동안" 류 문제의 바깥 틀

```python
def solve(T, state):
    for t in range(1, T + 1):                  # ← 문제마다 바뀜(초/턴/명령 개수)
        state = phase_move(state)              # 1단계: 이동
        state = phase_collide(state)           # 2단계: 충돌/합체
        state = phase_spawn(state, t)          # 3단계: 생성/소멸
        if is_done(state):                     # ← 문제마다 바뀜(조기 종료 조건)
            return t
    return -1
```

한 턴 안의 단계 순서를 문제 문장에서 그대로 베껴 함수 이름으로 남기면, 순서를
바꿔 끼우는 실수가 사라진다.

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 각 칸에서 이웃만 보면 되는 세기/판정 | 이중 for + 방향 벡터 | 상태가 없고 순서도 무관 | O(R·C) |
| 고정 크기 K×K 창을 전부 훑기 | 시작점 범위를 `R-K+1`로 제한 | 경계 넘침을 원천 차단 | O(R·C·K²) |
| K가 커서 창 합산이 무거움 | 2차원 누적합 | 창 하나를 O(1)로 계산 | O(R·C) |
| 한 방향으로 값 몰기(합치기 포함) | `push_left` + 전치·반전 | 함수 하나만 검증하면 4방향이 옳다 | O(R·C) / 회 |
| 합치기 없는 단순 낙하 | 열마다 개수 세고 바닥부터 채우기 | 이동을 시뮬레이션할 필요가 없다 | O(R·C) |
| "가로·세로 K개 연속" 소거 | 런(run) 스캔 | 연결성이 아니라 연속성 조건 | O(R·C) / 라운드 |
| "상하좌우로 이어진 덩어리 K개" 소거 | 큐 기반 BFS + `visited` | 연결 요소 크기를 재야 함 | O(R·C) / 라운드 |
| 연쇄가 안정될 때까지 | 표시→제거→낙하 while 루프 | 종료 조건이 명확해야 무한 루프가 없다 | 최악 O((R·C)²) |
| 주인공이 정확히 하나 | `(r, c, d)` 상태 + 모듈러 회전 | 격자를 갱신할 필요 없이 상태만 | O(T) |
| 명령 수 T가 10⁸ 수준 | 상태 사이클 탐지 후 나머지 연산 | 상태가 `R·C·4`개뿐이라 반드시 반복 | O(R·C) |
| 여러 객체가 동시에 이동 | 새 격자/새 리스트에 쓰기 | 이미 움직인 값이 다시 읽히는 오염 차단 | O(K + R·C) / 턴 |
| 같은 칸에 여럿이 도착 | `defaultdict(list)`로 도착 칸 그룹핑 | 충돌 규칙을 한 곳에서 처리 | O(K) / 턴 |
| 객체가 정해진 순서로 하나씩 | 정렬 키 고정 후 즉시 반영 | 문제가 "순차"라고 못 박은 경우 | O(K log K) / 턴 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: `board[r][c]`에서 r과 c가 각각 어느 방향으로 증가하는지, 그리고 방향 벡터 `dr/dc`의 순서를 회전 규칙과 어떻게 맞추는지.
- [ ] 설명할 수 있다: 경계 검사를 "이동 후 접근 전"에 넣어야 하는 이유와, 파이썬에서 음수 인덱스가 에러 없이 반대편을 읽는다는 사실.
- [ ] 설명할 수 있다: K×K 창의 시작점 범위가 왜 `range(R-K+1)`인지 오프바이원까지.
- [ ] 설명할 수 있다: 한 줄 좌 밀기가 "빈칸 제거 → 합치기 → 0으로 채우기" 세 단계로 쪼개지는 이유.
- [ ] 설명할 수 있다: 인덱스를 2씩 건너뛰는 것이 왜 "한 번 합쳐진 타일의 재합치기"를 막는지.
- [ ] 설명할 수 있다: 전치와 좌우 반전이 좌표 `(r,c)`를 각각 어디로 보내는지, 그리고 그 조합으로 시계·반시계 회전이 어떻게 만들어지는지.
- [ ] 설명할 수 있다: 좌 밀기 함수 하나만 검증해도 네 방향이 옳은 이유, 그리고 그것이 버그를 왜 줄이는지.
- [ ] 설명할 수 있다: 제자리(in-place) 밀기가 값을 복제하는 구체적 과정과, 새 리스트를 반환하면 왜 안전해지는지.
- [ ] 설명할 수 있다: "표시 후 일괄 제거"가 필요한 이유를 가로·세로 매치가 겹치는 예로.
- [ ] 설명할 수 있다: "연속 K개"와 "연결 덩어리 K개"의 차이, 각각에 런 스캔과 BFS 중 무엇을 쓰는지.
- [ ] 설명할 수 있다: 연쇄 루프의 종료 조건을 무엇으로 잡아야 무한 루프가 나지 않는지.
- [ ] 설명할 수 있다: 동시 갱신과 순차 갱신이 같은 입력에서 다른 답을 내는 상황 하나.
- [ ] 설명할 수 있다: 충돌 처리를 도착 칸 그룹핑으로 하는 이유와, 두 객체가 자리를 맞바꾸는 경우가 왜 따로 다뤄야 하는지.
- [ ] 설명할 수 있다: 명령 수 T가 매우 클 때 상태 사이클을 찾아 시간을 줄이는 논리.

**⚠️ 자주 하는 실수**

(1) 2차원 배열을 `*`로 복제 — 모든 행이 같은 리스트

```python
# ❌ 틀린 코드
g = [[0] * C] * R
g[0][0] = 1
print(g[1][0])        # 1 이 나온다
```

왜: `[X] * R`은 X를 R번 **복사**하는 게 아니라 같은 객체를 R번 **참조**한다. 한 행을
고치면 모든 행이 같이 바뀐다.

```python
# ✅ 고친 코드
g = [[0] * C for _ in range(R)]
g[0][0] = 1
print(g[1][0])        # 0
```

(2) 제자리 밀기로 값이 유령처럼 복제됨

```python
# ❌ 틀린 코드
def push_left(row):
    for i in range(len(row)):
        if row[i] != 0:
            j = i
            while j > 0 and row[j - 1] == 0:
                row[j - 1] = row[j]     # 앞으로 옮기고
                j -= 1                  # 원래 자리를 지우지 않았다
    return row
```

왜: 값을 앞 칸에 쓰면서 원래 칸을 비우지 않으면, 뒤이어 그 칸을 다시 읽어 같은 값이
두 번 등장한다. `[0,2,0,0]`이 `[2,2,0,0]`이 되는 식이다.

```python
# ✅ 고친 코드
def push_left(row):
    vals = [x for x in row if x != 0]        # 읽기 전용으로 모으고
    return vals + [0] * (len(row) - len(vals))   # 새 리스트를 만들어 반환
```

(3) 이중 합치기 — 방금 합친 타일을 또 합친다

```python
# ❌ 틀린 코드
res, i = [], 0
while i < len(vals):
    if res and res[-1] == vals[i]:
        res[-1] *= 2                 # 이미 합쳐진 결과와 또 합친다
    else:
        res.append(vals[i])
    i += 1
```

왜: `vals = [4, 4, 8]`이면 `4+4=8`이 되고, 다음 `8`이 그 결과와 다시 합쳐져 `16`이
된다. 실제 규칙은 한 이동에서 각 타일이 최대 한 번만 합쳐지는 것이다.

```python
# ✅ 고친 코드
res, i = [], 0
while i < len(vals):
    if i + 1 < len(vals) and vals[i] == vals[i + 1]:
        res.append(vals[i] * 2)
        i += 2                       # 소비한 두 칸을 건너뛴다
    else:
        res.append(vals[i])
        i += 1
```

(4) 전치 후에도 R, C를 그대로 쓴다

```python
# ❌ 틀린 코드
t = [list(col) for col in zip(*g)]      # 이제 t는 C행 R열
for r in range(R):
    for c in range(C):
        t[r][c] = 0                     # R != C 이면 IndexError
```

왜: 전치는 `(r,c) → (c,r)`이라 모양이 `R×C`에서 `C×R`로 바뀐다. 행·열 개수를 그대로
두면 정사각 격자에서만 우연히 통과하고 직사각에서 터진다.

```python
# ✅ 고친 코드
t = [list(col) for col in zip(*g)]
TR, TC = C, R                           # 전치된 격자의 크기를 새로 잡는다
for r in range(TR):
    for c in range(TC):
        t[r][c] = 0
```

(5) 표시 없이 발견 즉시 제거 — 겹친 매치가 사라진다

```python
# ❌ 틀린 코드
for r in range(R):
    for c in range(C - 2):
        if g[r][c] == g[r][c+1] == g[r][c+2] != 0:
            g[r][c] = g[r][c+1] = g[r][c+2] = 0    # 바로 지운다
# 이어서 세로 런을 검사하면, 이미 0이 되어 세로 매치를 놓친다
```

왜: 가로 매치와 세로 매치가 한 칸을 공유할 때, 가로를 먼저 지우면 그 칸이 0이 되어
세로 런이 끊긴다. 같은 라운드에서 터져야 할 칸이 살아남는다.

```python
# ✅ 고친 코드
boom = [[False] * C for _ in range(R)]
# 가로 스캔에서 boom 표시, 세로 스캔에서도 boom 표시 (격자는 그대로 둔다)
for r in range(R):
    for c in range(C):
        if boom[r][c]:
            g[r][c] = 0                 # 다 표시한 뒤 한꺼번에 제거
```

(6) 동시 갱신인데 원본 격자를 고쳐가며 읽는다

```python
# ❌ 틀린 코드
for r in range(R):
    for c in range(C):
        if g[r][c] == 1 and c + 1 < C:
            g[r][c] = 0
            g[r][c + 1] = 1        # 다음 c 반복에서 이 1을 또 읽는다
```

왜: 방금 오른쪽으로 옮긴 값을 같은 스캔이 다시 만나 또 옮긴다. 한 턴에 한 칸만
움직여야 할 객체가 줄 끝까지 흘러간다.

```python
# ✅ 고친 코드
nxt = [[0] * C for _ in range(R)]
for r in range(R):
    for c in range(C):
        if g[r][c] == 1 and c + 1 < C:
            nxt[r][c + 1] = 1      # 읽기는 g, 쓰기는 nxt
g = nxt
```

(7) 경계 검사를 이동 후 접근 뒤에 둔다

```python
# ❌ 틀린 코드
nr, nc = r + dr, c + dc
val = g[nr][nc]                    # 먼저 읽고
if 0 <= nr < R and 0 <= nc < C:    # 나중에 검사
    total += val
```

왜: `nr = -1`이면 예외가 나지 않고 마지막 행을 조용히 읽는다. 값이 그럴듯해서 오답의
원인을 찾기가 매우 어렵다.

```python
# ✅ 고친 코드
nr, nc = r + dr, c + dc
if 0 <= nr < R and 0 <= nc < C:    # 검사 먼저
    total += g[nr][nc]
```

(8) 회전 규칙과 방향 배열 순서가 어긋난다

```python
# ❌ 틀린 코드
DR = [-1, 1, 0, 0]      # 북 남 서 동 (시계 순서가 아님)
DC = [0, 0, -1, 1]
d = (d + 1) % 4         # "우회전"이라고 썼지만 북 -> 남 이 된다
```

왜: `(d+1) % 4`가 우회전이 되려면 배열이 시계 방향(북·동·남·서)으로 정렬돼 있어야
한다. 완전탐색용 4방향 배열을 그대로 재사용하면 회전이 뒤엉킨다.

```python
# ✅ 고친 코드
DR = [-1, 0, 1, 0]      # 북 동 남 서 (시계 방향)
DC = [0, 1, 0, -1]
d = (d + 1) % 4         # 우회전: 북 -> 동
# 검산: d=0(북)에서 우회전 한 번이 동쪽인지 작은 예제로 반드시 확인
```

**다음 챕터로**

여기서 만든 "격자를 상태로 들고 규칙대로 갱신한다"는 감각은 다음 챕터의 백트래킹에서
"선택을 상태로 들고 되돌린다"로 이어진다. 특히 L5의 "새 격자에 쓰기 vs 제자리 수정"은
백트래킹의 "복사본 저장 vs 되돌리기"와 정확히 같은 고민이다. 또 L3의 BFS 덩어리 세기는
이후 그래프 탐색 챕터에서 방문 배열과 큐를 다루는 기초가 된다.
