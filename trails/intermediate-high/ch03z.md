## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터는 두 문장으로 요약된다. **"의존 관계가 있으면 순서를 먼저 만든다"**(L1), **"그 순서가 곧 DP를 채우는 안전한 순서다"**(L2). 위상 정렬 자체는 코드가 짧지만, 실제 문제는 거의 항상 "순서를 만든 다음 그 위에서 무언가를 계산하는" 두 단계로 온다. 아래에서 두 단계를 한 장으로 잇고, 뼈대와 실수 목록으로 마무리한다.

**개념 지도**

```text
                  Ch03 : topological sort
                            |
            edge u -> v means "u must come before v"
                            |
        +-------------------+--------------------+
        |                                        |
   BUILD THE ORDER                          USE THE ORDER
        |                                        |
   Kahn : indeg == 0 -> queue           DAG DP : dp[v] <- dp[pred]
   DFS  : post-order, then reverse        op = max -> longest path
        |                                  op = min -> cheapest path
   len(order) < N       -> cycle          op = +   -> path count
   deque                -> any order      op = max -> finish time
   heapq                -> smallest one        |
   queue size always 1  -> unique              |
        |                                      |
        +--------------------------------------+
                       |
        the order must exist before the DP can run
```

DAG DP가 위상 순서를 요구하는 이유는 한 장면이면 충분하다. 순서를 어기면 **아직 비어 있는 값을 읽고**, 그 값이 나중에 커져도 아무도 되돌아오지 않는다.

```text
   (1)--3-->(2)--4-->(4)--2-->(5)      # numbers on edges are weights
    |                 ^
    2                 1
    +----->(3)--------+

   order respected 1,2,3,4,5      order violated : 4 computed first
   dp[2] = 0 + 3 = 3              dp[4] reads dp[2] = 0, dp[3] = 0
   dp[3] = 0 + 2 = 2              dp[4] = 0
   dp[4] = max(3+4, 2+1) = 7      later dp[2] becomes 3, but nobody
   dp[5] = 7 + 2 = 9              ever revisits 4 -> dp[5] = 2  WRONG
```

큐에 몇 개가 들어 있는지는 그 자체로 정보다. 사이클 판정도, 순서의 유일성 판정도 여기서 읽는다.

```text
   the queue holds every vertex that is ready RIGHT NOW

   size 1 at every step           size >= 2 at some step
   1 -> 2 -> 3 -> 4               1 -> 3 ,  2 -> 3
   queue : [1] [2] [3] [4]        queue : [1, 2] [3]
   -> the order is UNIQUE         -> "1 2 3" and "2 1 3" both valid

   cycle :  1 -> 2 -> 3 -> 4 -> 2
   pop 1, indeg[2] goes 2 -> 1, so 2 never reaches 0
   the queue dries up, len(order) = 1 < 4      -> cycle detected
```

**뼈대 코드**

1) Kahn — 진입차수 큐. 이 챕터의 기본형이다.

```python
from collections import deque

graph = [[] for _ in range(n + 1)]
indeg = [0] * (n + 1)
for u, v in edges:                 # u 를 먼저, 그다음 v
    graph[u].append(v)
    indeg[v] += 1                  # 화살표가 '들어오는' 쪽에 센다

q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
order = []
while q:
    u = q.popleft()
    order.append(u)
    for v in graph[u]:
        indeg[v] -= 1              # 먼저 깎고
        if indeg[v] == 0:          # 그다음에 0인지 본다
            q.append(v)

if len(order) < n:                 # 사이클 판정은 항상 이 한 줄
    print(-1)
```

2) 사전순 최소 — 큐를 최소 힙으로 바꾸기만 한다.

```python
import heapq

h = [v for v in range(1, n + 1) if indeg[v] == 0]
heapq.heapify(h)
order = []
while h:
    u = heapq.heappop(h)           # 지금 놓을 수 있는 것 중 가장 작은 번호
    order.append(u)
    for v in graph[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            heapq.heappush(h, v)   # ← 사전순 최대면 -v 를 넣고 꺼낼 때 -를 뗀다
```

3) 사이클 판정 — 못 꺼낸 정점이 곧 사이클에 얽힌 정점이다.

```python
# 위 Kahn 을 그대로 돌린 뒤
if len(order) < n:
    stuck = [v for v in range(1, n + 1) if indeg[v] > 0]
    # stuck = 사이클에 속하거나, 사이클에 의존해 영영 못 하는 작업들
    print("CYCLE", *stuck)
else:
    print(*order)
```

4) DAG DP — 위상 순서로 밀면서(Push) 값을 확정한다. `op`만 갈아 끼운다.

```python
from collections import deque

dp = [0] * (n + 1)                 # ← 문제마다 바뀜: 아래 세 갈래 참고
q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
while q:
    u = q.popleft()                # u 를 꺼낸 순간 dp[u] 는 확정
    for v, w in graph[u]:
        # (A) 최장 경로  : dp[v] = max(dp[v], dp[u] + w)
        # (B) 경로 수    : dp[v] = (dp[v] + dp[u]) % MOD      (dp[start] = 1)
        # (C) 완료 시각  : dp[v] = max(dp[v], dp[u] + t[v])   (병렬이라 max)
        if dp[u] + w > dp[v]:
            dp[v] = dp[u] + w
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

print(max(dp[1:]))                 # ← 끝점이 자유면 max, 고정이면 dp[goal]
```

도달 불가를 값 0과 구분해야 하면 초기값을 바꾼다.

```python
NEG = float('-inf')
dp = [NEG] * (n + 1)
for v in range(1, n + 1):
    if indeg[v] == 0:              # 시작 후보만 base 를 갖는다
        dp[v] = 0
# 출발점이 하나로 고정이면 dp[start] = 0 하나만 두고 나머지는 NEG
```

5) 위상 순서 유일성 판정 — 매 단계 큐 크기를 본다.

```python
from collections import deque

q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
order, unique = [], True
while q:
    if len(q) > 1:                 # 지금 놓을 수 있는 후보가 둘 이상
        unique = False             # → 다른 순서도 가능하다
    u = q.popleft()
    order.append(u)
    for v in graph[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

if len(order) < n:
    print("IMPOSSIBLE")            # 사이클 — 순서가 아예 없음
elif not unique:
    print("AMBIGUOUS")             # 순서가 여러 개 — 확정 불가
else:
    print(*order)
```

**언제 무엇을 쓰나**

먼저 "이 문제가 위상 정렬인가"를 신호로 판정한다.

| 문제 문장의 신호 | 그래프로 옮기면 | 다음 단계 |
|---|---|---|
| "A를 들어야 B를 들을 수 있다"(선수과목) | `A → B` | Kahn + 레벨 DP(최소 학기) |
| "A가 끝나야 B를 시작한다"(작업·공정) | `A → B` | 완료 시각 DP(`max` + 소요 시간) |
| "A가 B보다 앞선다"(순위·경기 결과) | `A → B` | 순서 생성 + 유일성 판정 |
| "이 모듈은 저 모듈을 필요로 한다"(빌드) | `필요한 것 → 쓰는 것` | 사전순 최소가 요구되면 heapq-Kahn |
| "규칙이 서로 모순인지 확인하라" | 방향 그래프 전체 | 사이클 판정(`len(order) < N`) |
| "가능한 순서가 몇 가지인가" | DAG | N이 작으면 백트래킹·비트마스크 DP |

판정을 통과했으면 아래에서 도구를 고른다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 순서 하나만 아무거나 | Kahn(`deque`) | 재귀가 없어 깊이 걱정이 없다 | O(V+E) |
| 사전순 가장 앞선 순서 | Kahn의 큐를 `heapq`로 | 매번 "지금 가능한 것 중 최소"를 확정 | O((V+E) log V) |
| 사전순 가장 뒤인 순서·역방향 조건 | 역그래프 + 최대 힙 Kahn | 뒤에서부터 채우면 같은 그리디가 성립 | O((V+E) log V) |
| 사이클 존재 여부 | Kahn 후 `len(order) < N` | 사이클 정점은 진입차수가 0이 될 수 없다 | O(V+E) |
| 사이클에 얽힌 정점 목록 | Kahn 후 `indeg[v] > 0`인 정점 | 못 꺼낸 것이 곧 못 하는 작업 | O(V) |
| 사이클의 증거 정점 하나 | DFS 3색(회색 재방문) | 되돌아가는 간선을 만나는 그 순간이 증거 | O(V+E) |
| 순서가 유일한지 판정 | Kahn 중 매 단계 큐 크기 | 후보가 둘 이상인 순간이 곧 분기점 | O(V+E) |
| 각 정점의 최소 단계·학기 | Kahn + 레벨 전파 | `level[v] = max(level[pred]) + 1` | O(V+E) |
| DAG 최장·최단 경로, 경로 수 | 위상 순서 Push DP | 선행이 전부 확정된 뒤에만 v를 계산 | O(V+E) |
| 병렬 작업의 총 완료 시각 | 완료 시각 DP(`max`) | 선행이 동시에 진행되므로 합이 아니라 최대 | O(V+E) |
| 각 작업의 여유 시간(slack) | 정방향 최이른 + 역방향 최늦 | 두 값의 차가 곧 늦출 수 있는 여유 | O(V+E) |

**위상 정렬만으로 끝나는가, DP까지 필요한가**는 이 표로 가른다.

| 묻는 것 | 필요한 것 | 이유 |
|---|---|---|
| 순서 자체 / 가능한지 여부 | 위상 정렬만 | 정점을 세우는 것이 곧 답 |
| 순서가 유일한지 | 위상 정렬 + 큐 크기 관찰 | 분기 여부는 순서를 만들며 알 수 있다 |
| 각 정점의 "몇 번째 층인가" | 위상 정렬 + 레벨 전파 | 값이 선행의 최댓값에만 의존 |
| 최대/최소/개수/시각을 정점마다 | 위상 정렬 + DAG DP | 값이 선행들의 값에 의존 |
| 두 정점을 잇는 조건부 경로 수 | 정방향 DP × 역방향 DP | 경유 강제는 두 조각의 곱으로 읽는다 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 사이클이 하나라도 있으면 위상 순서가 존재할 수 없는 이유를 모순으로.
- [ ] 설명할 수 있다: 진입차수를 `u → v`에서 왜 `v` 쪽에 세는지, 방향을 뒤집으면 무슨 일이 생기는지.
- [ ] 설명할 수 있다: Kahn이 사이클을 감지하는 원리와, 못 꺼낸 정점들이 무엇을 뜻하는지.
- [ ] 설명할 수 있다: 위상 정렬의 답이 여러 개일 수 있는 이유와, 유일해지는 정확한 조건.
- [ ] 설명할 수 있다: 사전순 최소를 왜 `deque` 대신 `heapq`로 얻는지, 그 그리디가 옳은 이유와 함께.
- [ ] 설명할 수 있다: DFS 후위 순서를 뒤집으면 위상 순서가 되는 이유와, 3색 칠하기에서 회색 정점 재방문이 사이클의 증거인 이유.
- [ ] 설명할 수 있다: Kahn과 DFS 중 무엇을 고를지, 사전순·레벨·재귀 깊이를 근거로.
- [ ] 설명할 수 있다: 위상 정렬의 복잡도가 O(V+E)인 이유를, 정점·간선이 각각 몇 번 처리되는지 세면서.
- [ ] 설명할 수 있다: "위상 순서 = DP를 채우는 안전한 순서"라는 문장의 뜻과, 어겼을 때 생기는 증상.
- [ ] 설명할 수 있다: DAG DP에서 `op`를 `max`/`min`/`+`로 바꾸면 무엇이 계산되는지, 뼈대는 왜 그대로인지.
- [ ] 설명할 수 있다: Push(전방 갱신)와 Pull(재귀+메모)이 같은 계산인 이유.
- [ ] 설명할 수 있다: 병렬 작업의 완료 시각이 선행들의 "합"이 아니라 "최대"인 이유.
- [ ] 설명할 수 있다: DP 초기값에서 "도달 불가"와 "값 0"을 구분해야 하는 상황과 그 방법.
- [ ] 설명할 수 있다: 역그래프를 언제 만들어야 하는지, 그리고 그것이 어떤 질문을 뒤집어 주는지.

**⚠️ 자주 하는 실수**

**1) 진입차수를 깎지 않고 검사만 한다**

```python
# ❌ 틀린 코드
while q:
    u = q.popleft()
    order.append(u)
    for v in graph[u]:
        if indeg[v] == 0:        # 깎기 전에 검사한다
            q.append(v)
```

왜: `indeg[v]`가 줄지 않으니 선행이 있는 정점은 영영 0이 되지 못하고, 출력이 시작 정점들에서 끊긴다. 반대로 진입차수가 원래 0이던 정점은 조건을 계속 만족해 **여러 번 큐에 들어가** 같은 정점이 중복 출력되기도 한다. 순서는 "깎기 → 0인지 보기"다.

```python
# ✅ 고친 코드
for v in graph[u]:
    indeg[v] -= 1                # 먼저 깎고
    if indeg[v] == 0:            # 0이 되는 그 순간에만 넣는다
        q.append(v)
```

**2) 진입차수를 화살표 반대쪽에 센다**

```python
# ❌ 틀린 코드
for u, v in edges:               # u 를 먼저 해야 v 를 할 수 있다
    graph[u].append(v)
    indeg[u] += 1                # 나가는 쪽에 세었다
```

왜: 진입차수는 "나보다 먼저 끝나야 할 것이 몇 개 남았는가"다. 나가는 쪽에 세면 의미가 뒤집혀, 선행이 없는 정점이 큐에 못 들어가고 선행이 많은 정점이 곧바로 들어간다. 결과는 순서가 통째로 거꾸로 나오거나, 사이클이 없는데도 `len(order) < N`이 뜬다.

```python
# ✅ 고친 코드
for u, v in edges:
    graph[u].append(v)
    indeg[v] += 1                # 화살표가 들어오는 v 쪽에 센다
```

**3) 사이클을 감지하지 않고 나온 것만 출력한다**

```python
# ❌ 틀린 코드
while q:
    u = q.popleft()
    order.append(u)
    ...
print(*order)                    # 사이클이면 앞부분만 출력된다
```

왜: 사이클이 있으면 큐가 먼저 마르고 `order`에는 사이클 바깥의 정점만 담긴다. 이 값은 "짧은 정답"이 아니라 **애초에 존재하지 않는 답의 조각**이다. 작은 예제에서는 사이클이 없어 통과하고, 사이클이 섞인 입력에서만 조용히 틀린다. 판정은 언제나 담긴 개수와 N의 비교다.

```python
# ✅ 고친 코드
if len(order) < n:
    print(-1)                    # ← 문제 규칙에 맞게: -1 / IMPOSSIBLE / 0
else:
    print(*order)
```

**4) 사전순 최소를 요구하는데 `deque`를 쓴다**

```python
# ❌ 틀린 코드
q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
while q:
    u = q.popleft()              # 들어온 순서대로 나온다
```

왜: `deque`는 FIFO라 "먼저 준비된 것"을 꺼낼 뿐, "번호가 가장 작은 것"을 꺼내지 않는다. 두 정점이 동시에 준비되면 입력 순서가 답을 좌우해 사전순이 깨진다. 정점 `1, 2`가 함께 준비되고 간선을 `2`부터 읽었다면 `2 1 …`이 나온다. **정렬 기준이 붙는 순간 큐는 힙이 된다.**

```python
# ✅ 고친 코드
import heapq
h = [v for v in range(1, n + 1) if indeg[v] == 0]
heapq.heapify(h)
while h:
    u = heapq.heappop(h)         # 지금 가능한 것 중 최소 번호
    ...
    heapq.heappush(h, v)         # 큐 연산 세 군데를 모두 힙으로 바꾼다
```

**5) DAG DP를 위상 순서 없이 계산한다**

```python
# ❌ 틀린 코드
for u in range(1, n + 1):        # 정점 번호 순으로 그냥 훑는다
    for v, w in graph[u]:
        dp[v] = max(dp[v], dp[u] + w)
```

왜: `dp[u]`가 확정되기 전에 `u`를 꺼내 미완성 값을 이웃에 퍼뜨린다. 번호 순이 우연히 위상 순서와 같으면 맞고 아니면 틀리므로, **입력 번호 붙이기 방식에 답이 좌우되는** 최악의 버그가 된다. 앞의 도식에서 `4`를 먼저 계산하면 `dp[5]`가 9가 아니라 2로 굳는 것이 정확히 이 증상이다.

```python
# ✅ 고친 코드
q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
while q:
    u = q.popleft()              # 꺼낸 순간 dp[u] 는 확정돼 있다
    for v, w in graph[u]:
        if dp[u] + w > dp[v]:
            dp[v] = dp[u] + w
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
```

**6) 도달 불가를 값 0과 구분하지 않는다**

```python
# ❌ 틀린 코드
dp = [0] * (n + 1)               # 출발점이 s 하나로 고정인 문제
dp[s] = 0
...
print(dp[t])                     # s 에서 못 가는 t 도 0 을 출력한다
```

왜: 모든 칸을 0으로 두면 "출발점에서 도달했고 비용이 0"과 "아예 도달 못 함"이 같은 값이 된다. 가중치에 음수가 섞이면 더 나빠져서, 도달 불가 정점이 0이라는 이유로 다른 정점의 최댓값을 오염시킨다. 출발이 고정이면 base는 **출발점 하나뿐**이다.

```python
# ✅ 고친 코드
NEG = float('-inf')
dp = [NEG] * (n + 1)
dp[s] = 0                        # base 는 출발점만
...
for v, w in graph[u]:
    if dp[u] != NEG and dp[u] + w > dp[v]:   # 미도달에서는 밀지 않는다
        dp[v] = dp[u] + w
print(dp[t] if dp[t] != NEG else -1)
```

**7) 유일성 판정을 처음 한 번만 한다**

```python
# ❌ 틀린 코드
q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
unique = len(q) == 1             # 시작할 때만 검사한다
while q:
    u = q.popleft()
    ...
```

왜: 분기는 중간에도 얼마든지 생긴다. 시작 정점이 하나여도, 그 정점을 꺼낸 뒤 두 개가 한꺼번에 준비되면 순서는 두 가지가 된다. `1 → 2`, `1 → 3`만 있는 그래프가 그렇다 — 시작 큐는 `[1]` 하나지만 답은 `1 2 3`과 `1 3 2` 둘이다. **매 반복마다** 후보 수를 봐야 한다.

```python
# ✅ 고친 코드
unique = True
while q:
    if len(q) > 1:               # 루프 안에서 매번 확인
        unique = False
    u = q.popleft()
    ...
# 사이클(len(order) < n) 판정과 유일성 판정은 서로 다른 검사다 — 둘 다 한다
```

**다음 챕터로**

- 위상 순서는 "의존이 한 방향으로만 흐를 때 DP를 안전하게 채우는 순서"였다. 다음 단계의 DP들은 이 순서를 그래프가 아니라 **인덱스·부분집합**에서 찾는다. 배열 DP의 `for i in range(n)`, 비트마스크 DP의 "비트 수가 적은 마스크부터"가 모두 같은 요구를 다른 모양으로 만족시키는 것이다.
- 사이클이 있어서 위상 정렬이 실패하는 그래프도, 강한 연결 요소로 뭉치면 다시 DAG가 된다. "먼저 DAG로 만든 뒤 그 위에서 DP"라는 이 챕터의 두 단계 구조가 그대로 재사용된다.
