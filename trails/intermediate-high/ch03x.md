## L3. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch03(위상정렬)의 핵심 — Kahn(진입차수)·DFS 위상 정렬, 사이클 판정, 그리고 위상 순서를 뼈대로 삼는 DAG DP — 를 소재만 바꿔 **반복 훈련**하고, 코딩테스트 단골 그래프 유형으로 **확장**하는 연습 세트다.
- **반복 훈련 개념**:
  - Kahn 뼈대: `u→v`면 `indeg[v] += 1` → `q = deque(v for v in range(1, n+1) if indeg[v] == 0)` → 꺼내며 이웃의 `indeg[v] -= 1`, 0이 되는 순간 `q.append(v)`.
  - 사전순 최소: 큐를 힙으로 — `heapq.heappop(h)` / `heapq.heappush(h, v)`. 최대 힙이 필요하면 `-v`를 넣는다.
  - 사이클 판정: 꺼낸 정점 수가 N 미만이면 사이클 — `if len(order) < n`. 못 꺼낸 정점이 곧 "사이클에 속하거나 사이클에 의존하는" 정점이다.
  - 위상 순서 Push DP: `u`를 꺼낸 순간 `dp[u]`는 확정 → `dp[v] = op(dp[v], dp[u] + w)`. `op`가 `max`면 최장·완료 시각, `min`이면 최단, 덧셈이면 경로 수.
  - 역그래프: 간선을 뒤집어 `rgraph[v].append(u)` — "끝에서부터" 계산하거나 순서를 뒤에서부터 채울 때 쓴다.
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '위상 정렬' 단계, 프로그래머스 「코딩테스트 고득점 Kit」의 '그래프', 『이것이 취업을 위한 코딩테스트다』의 '그래프이론' 파트가 이 챕터 유형을 그대로 낸다.
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 선수과목과 최소 학기 | Easy | Kahn + 레벨(층) DP | 반복 훈련 |
| 2 | 이름으로 주어진 모듈 빌드 순서 | Medium | heapq-Kahn 사전순 최소(문자열 키) | 반복 훈련 |
| 3 | 완료할 수 없는 작업 찾기 | Medium | Kahn 사이클 판정(못 꺼낸 정점) | 반복 훈련 |
| 4 | 순위 확정 여부 판정 | Medium | Kahn 큐 크기로 유일성 판정 | 유형 확장 (백준 '위상 정렬' 단계 스타일) |
| 5 | 출발점에서 각 정점까지 최소 비용 | Medium | 위상 순서 Push DP(min, 음수 가중치) | 반복 훈련 |
| 6 | 필수 경유 정점을 지나는 경로 수 | Hard | 정방향·역방향 경로 수 DP 결합 | 유형 확장 (백준 '위상 정렬' 단계 스타일) |
| 7 | 작업의 여유 시간 | Hard | 완료 시각 DP + 역순 최늦 시각 | 유형 확장 (이코테 '그래프이론' 스타일) |
| 8 | 작은 번호를 최대한 앞으로 | Hard | 역그래프 + 최대 힙 Kahn | 유형 확장 (백준 '위상 정렬' 단계 스타일) |

**문제**

**1) 선수과목과 최소 학기** · Easy

- **요구사항**: 과목 `N`개(1..N)와 선수 관계 `M`개가 있다. `a b`는 "a를 이수해야 b를 들을 수 있다"는 뜻이다. 한 학기에 듣는 과목 수에는 제한이 없다. 각 과목을 들을 수 있는 **가장 빠른 학기**(1학기부터)를 과목 번호 순서로 출력하라. 선수 관계에 순환은 없다.
- **입력**: 첫 줄 `N M` (1 ≤ N ≤ 1,000, 0 ≤ M ≤ 5,000), 이후 M줄 `a b`.
- **출력**: 과목 1..N의 최소 학기를 공백으로 구분해 한 줄에.
- **예제**: `6 5 / 1 2 / 1 3 / 2 4 / 3 4 / 5 6` → `1 2 2 3 1 2` · `4 0` → `1 1 1 1`
- **셀프체크**: 선수가 여럿이면 "선수들의 학기 중 **최댓값** + 1"이지 합이 아니다. 진입차수 0인 과목이 전부 1학기로 시작하는가? Kahn으로 꺼내는 순간 그 과목의 학기가 확정되어 있는지(선행이 모두 먼저 처리됨) 확인하라. 위상 순서를 안 지키고 번호 순으로 채우면 `5 6`처럼 뒤 번호가 선수인 경우에 틀린다.

```runner
@@SOLUTION
import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for _ in range(m):
        a = int(data[idx]); idx += 1
        b = int(data[idx]); idx += 1
        graph[a].append(b)
        indeg[b] += 1
    sem = [1] * (n + 1)          # 선수 없는 과목은 1학기
    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    while q:
        u = q.popleft()          # 이 순간 sem[u]는 확정
        for v in graph[u]:
            if sem[u] + 1 > sem[v]:
                sem[v] = sem[u] + 1
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    print(' '.join(str(sem[v]) for v in range(1, n + 1)))

main()
@@TESTS
--IN
6 5
1 2
1 3
2 4
3 4
5 6
--OUT
1 2 2 3 1 2
--IN
4 0
--OUT
1 1 1 1
--IN
4 3
1 2
2 3
3 4
--OUT
1 2 3 4
@@EXPL
(1) 접근·핵심 아이디어

- `sem[v]` = v를 들을 수 있는 최소 학기. 선수들이 병렬로 이수되므로 `sem[v] = max(sem[선수]) + 1`, 선수가 없으면 1이다. 이것은 "DAG에서 각 정점까지의 최장 경로(간선 수)"와 같은 구조다.
- 이 점화식은 v의 선수가 모두 확정된 뒤에만 계산할 수 있으므로 위상 순서(Kahn)로 채운다. Kahn에서 정점 u를 꺼내는 순간은 u의 선행이 전부 처리된 뒤이므로 `sem[u]`가 확정돼 있고, 그 값을 이웃으로 밀어(Push) 갱신하면 된다.
- 시간 O(N + M): 정점·간선을 상수 번만 본다.

(2) 코드 단계별

- 인접 리스트와 진입차수를 만든다(`a b`면 `b`의 진입차수 증가).
- `sem`을 전부 1로 초기화하고 진입차수 0인 과목을 큐에 넣는다.
- 큐에서 `u`를 꺼내 각 이웃 `v`에 `sem[v] = max(sem[v], sem[u] + 1)`을 적용하고 진입차수를 깎아 0이 되면 큐에 넣는다.
- 1..N 순서로 `sem`을 공백 구분 출력.

(3) 스스로 다시 짤 때 생각 순서

- "선수 과목 + 최소 학기" → 레벨(층)을 세는 위상 정렬 = DAG 최장 경로(간선 수) DP.
- 합이 아니라 최댓값임을 먼저 확인(병렬 이수). base는 진입차수 0 = 1학기.
- Kahn 뼈대를 그대로 쓰고, 꺼내는 순간 값을 이웃으로 미는 Push 형태로 짠다. 번호 순 채우기는 함정.
```

**2) 이름으로 주어진 모듈 빌드 순서** · Medium

- **요구사항**: 소문자 이름을 가진 모듈 `N`개와 의존 관계 `M`개가 있다. `A B`는 "A를 먼저 빌드해야 B를 빌드할 수 있다"는 뜻이다. 가능한 빌드 순서 중 **문자열 사전순으로 가장 앞선 순서**를 출력하라. 순환 의존이 있으면 `CYCLE`을 출력한다.
- **입력**: 첫 줄 `N M` (1 ≤ N ≤ 500, 0 ≤ M ≤ 5,000). 둘째 줄에 서로 다른 모듈 이름 N개(공백 구분, 길이 ≤ 20). 이후 M줄 `A B`.
- **출력**: 사전순 최소 빌드 순서(공백 구분 한 줄) 또는 `CYCLE`.
- **예제**: `4 3 / net core ui db / core net / core ui / db ui` → `core db net ui` · `3 3 / a b c / a b / b c / c a` → `CYCLE`
- **셀프체크**: 정점이 번호가 아니라 **문자열**이다 — 인접 리스트와 진입차수를 `dict`로 잡거나 이름→번호 매핑을 만들어라. 파이썬 `heapq`는 문자열도 그대로 비교하므로 이름을 바로 힙에 넣을 수 있다. 사전순 최소는 "지금 넣을 수 있는 것 중 가장 작은 이름"을 매번 꺼내는 heap-Kahn이며, 꺼낸 개수가 N 미만이면 `CYCLE`이다.

```runner
@@SOLUTION
import sys
import heapq

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    names = data[idx:idx + n]; idx += n
    graph = {name: [] for name in names}
    indeg = {name: 0 for name in names}
    for _ in range(m):
        a = data[idx]; b = data[idx + 1]; idx += 2
        graph[a].append(b)
        indeg[b] += 1
    # 사전순 최소 → 큐를 최소 힙으로(문자열 비교 그대로 사용)
    h = [name for name in names if indeg[name] == 0]
    heapq.heapify(h)
    order = []
    while h:
        u = heapq.heappop(h)
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(h, v)
    if len(order) == n:
        print(' '.join(order))
    else:
        print("CYCLE")

main()
@@TESTS
--IN
4 3
net core ui db
core net
core ui
db ui
--OUT
core db net ui
--IN
3 3
a b c
a b
b c
c a
--OUT
CYCLE
--IN
1 0
solo
--OUT
solo
@@EXPL
(1) 접근·핵심 아이디어

- 위상 순서 중 사전순 최소는 Kahn의 큐를 **최소 힙**으로 바꾸면 그리디하게 얻어진다. 매 순간 "진입차수 0인 후보 중 가장 작은 것"을 확정하는 선택이 항상 최선이기 때문이다(작은 것을 미룰 이유가 없다).
- 정점 식별자가 문자열이라는 점만 다르다. 파이썬 `heapq`는 문자열 비교를 그대로 지원하므로 이름을 바로 힙에 넣으면 사전순이 자동으로 지켜진다.
- 사이클이면 진입차수 0 후보가 도중에 마르므로 꺼낸 개수가 N 미만 → `CYCLE`.

(2) 코드 단계별

- 이름 목록을 읽어 `graph`(이름→후행 이름 리스트)와 `indeg`(이름→진입차수)를 `dict`로 만든다.
- `A B`마다 `graph[A].append(B)`, `indeg[B] += 1`.
- 진입차수 0인 이름을 힙에 넣고 `heapify`. 꺼낸 이름을 `order`에 추가하고 후행들의 진입차수를 깎아 0이 되면 힙에 push.
- `len(order) == n`이면 공백으로 이어 출력, 아니면 `CYCLE`.

(3) 스스로 다시 짤 때 생각 순서

- "빌드 순서 + 사전순" → heap-Kahn. 번호 대신 문자열이므로 자료구조를 `dict`로 바꾸는 것만 결정하면 된다.
- 방향 실수 주의: `A B`는 A→B, 진입차수는 B에 센다.
- 사이클 판정은 "꺼낸 개수 < N" 그대로. M=0이면 모든 이름이 처음부터 힙에 들어가 정렬 결과와 같아진다.
```

**3) 완료할 수 없는 작업 찾기** · Medium

- **요구사항**: 작업 `N`개와 의존 관계 `M`개(`u v`: u가 끝나야 v를 시작할 수 있음)가 있다. 순환 의존에 직접 속한 작업뿐 아니라, 그런 작업에 (직접·간접으로) 의존하는 작업도 영원히 끝낼 수 없다. **완료 가능한 작업 수**와 **완료 불가능한 작업 번호**(오름차순)를 출력하라.
- **입력**: 첫 줄 `N M` (1 ≤ N ≤ 1,000, 0 ≤ M ≤ 5,000), 이후 M줄 `u v`.
- **출력**: 첫 줄에 완료 가능한 작업 수. 둘째 줄에 완료 불가능한 작업 번호를 오름차순 공백 구분, 하나도 없으면 `NONE`.
- **예제**: `6 6 / 1 2 / 2 3 / 3 2 / 3 4 / 5 4 / 5 6` → `3 / 2 3 4` · `3 2 / 1 2 / 2 3` → `3 / NONE`
- **셀프체크**: Kahn에서 **끝까지 큐에 못 들어온 정점**이 곧 "사이클에 속하거나 사이클에 의존하는" 정점이다 — 사이클을 따로 찾을 필요가 없다. 예제에서 4는 사이클에 속하지 않지만 3에 의존하므로 불가능이다. 5는 4를 선행으로 두지 않고 4의 선행이므로 완료 가능. 전부 사이클(`2 2 / 1 2 / 2 1`)이면 첫 줄이 `0`인지 확인.

```runner
@@SOLUTION
import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for _ in range(m):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        graph[u].append(v)
        indeg[v] += 1
    done = [False] * (n + 1)
    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    cnt = 0
    while q:
        u = q.popleft()
        done[u] = True           # 큐에서 꺼낸 정점 = 완료 가능
        cnt += 1
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    blocked = [str(v) for v in range(1, n + 1) if not done[v]]
    print(cnt)
    print(' '.join(blocked) if blocked else "NONE")

main()
@@TESTS
--IN
6 6
1 2
2 3
3 2
3 4
5 4
5 6
--OUT
3
2 3 4
--IN
3 2
1 2
2 3
--OUT
3
NONE
--IN
2 2
1 2
2 1
--OUT
0
1 2
@@EXPL
(1) 접근·핵심 아이디어

- Kahn 알고리즘은 "선행이 모두 완료된 정점"만 큐에 넣는다. 사이클에 속한 정점은 진입차수가 절대 0이 되지 않고, 그 정점에 의존하는 정점도 마찬가지로 진입차수가 남는다. 따라서 **끝까지 꺼내지 못한 정점 집합 = 완료 불가능한 작업**이다.
- 사이클을 명시적으로 찾을 필요 없이, 완료 가능 여부를 `done` 배열 하나로 얻는다. 시간 O(N + M).

(2) 코드 단계별

- 인접 리스트와 진입차수를 만든다.
- 진입차수 0인 정점으로 큐를 시작. 꺼낼 때마다 `done[u] = True`, 개수 증가, 이웃 진입차수 감소.
- 끝난 뒤 `done`이 False인 번호를 오름차순으로 모아 둘째 줄에 출력(없으면 `NONE`).

(3) 스스로 다시 짤 때 생각 순서

- "사이클 + 그에 의존하는 것까지" → Kahn에서 못 꺼낸 정점이 정확히 그 집합임을 떠올린다.
- 정답이 유일하도록 오름차순으로 출력하는 요구를 지킨다(`range(1, n+1)` 순회면 자동).
- 경계: M=0이면 전부 완료 가능(`NONE`), 전부 사이클이면 `0`과 전체 목록.
```

**4) 순위 확정 여부 판정** · Medium

- **요구사항**: 선수 `N`명의 순위를 정하려 한다. 비교 결과 `M`개가 `a b`(a가 b보다 순위가 높다) 형태로 주어진다. 비교 결과에 **모순**(순환)이 있으면 `IMPOSSIBLE`, 모순은 없지만 전체 순위가 **한 가지로 정해지지 않으면** `?`, 유일하게 정해지면 그 순위를 1위부터 출력하라.
- **입력**: 첫 줄 `N M` (1 ≤ N ≤ 1,000, 0 ≤ M ≤ 5,000), 이후 M줄 `a b`(같은 쌍이 여러 번 나올 수 있다).
- **출력**: `IMPOSSIBLE`, `?`, 또는 순위 순서(공백 구분).
- **예제**: `4 3 / 1 3 / 3 2 / 2 4` → `1 3 2 4` · `3 1 / 1 2` → `?`
- **셀프체크**: 유일성 판정은 Kahn을 돌리며 **꺼내는 순간 큐에 정점이 2개 이상이면** 그 시점에 서로 순서를 정할 수 없는 두 정점이 있다는 뜻이다(→ 순서가 여러 개). 단, 사이클 판정이 우선이므로 `?`로 조기 종료하지 말고 끝까지 돌려 꺼낸 개수를 확인하라. 같은 쌍이 반복되어도 진입차수를 그만큼 올리고 그만큼 깎으면 문제없다.

```runner
@@SOLUTION
import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for _ in range(m):
        a = int(data[idx]); idx += 1
        b = int(data[idx]); idx += 1
        graph[a].append(b)
        indeg[b] += 1
    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    order = []
    unique = True
    while q:
        if len(q) > 1:           # 동시에 놓을 수 있는 정점이 둘 이상 → 순서 불확정
            unique = False
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) < n:
        print("IMPOSSIBLE")
    elif not unique:
        print("?")
    else:
        print(' '.join(map(str, order)))

main()
@@TESTS
--IN
4 3
1 3
3 2
2 4
--OUT
1 3 2 4
--IN
3 1
1 2
--OUT
?
--IN
3 3
1 2
2 3
3 1
--OUT
IMPOSSIBLE
--IN
1 0
--OUT
1
@@EXPL
(1) 접근·핵심 아이디어

- 위상 순서가 유일하려면 매 단계에 "지금 놓을 수 있는 정점"이 정확히 하나여야 한다. 둘 이상이면 그 둘의 상대 순서를 바꾼 다른 위상 순서가 존재한다. 그래서 Kahn에서 정점을 꺼내는 순간 `len(q) > 1`이면 유일하지 않다.
- 모순(사이클)은 꺼낸 정점 수가 N 미만인 것으로 판정하고, 이것이 `?`보다 우선한다. 큐가 한때 2개였더라도 끝에 사이클이 드러나면 `IMPOSSIBLE`이어야 하므로 조기 종료하지 않는다.
- 시간 O(N + M).

(2) 코드 단계별

- 인접 리스트·진입차수 구성(같은 쌍이 중복돼도 그대로 누적).
- 진입차수 0인 정점을 큐에 넣고, 꺼내기 직전에 `len(q) > 1`이면 `unique = False`.
- 꺼낸 정점을 `order`에 넣고 이웃 진입차수를 깎는다.
- 결과 판정 순서: 개수 부족 → `IMPOSSIBLE`, `unique`가 False → `?`, 아니면 `order` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "순서가 유일한가" → 큐 크기 관찰이라는 한 줄 추가로 Kahn이 답한다.
- 세 결과의 우선순위(사이클 > 불확정 > 유일)를 먼저 정해두고 마지막에 판정한다.
- N=1, M=0은 큐에 하나만 들어가 유일(`1`). 중복 간선은 진입차수 누적으로 자연 처리됨을 확인.
```

**5) 출발점에서 각 정점까지 최소 비용** · Medium

- **요구사항**: 가중 DAG와 출발점 `S`가 주어진다. 정점 1..N 각각에 대해 `S`에서 그 정점까지의 **최소 비용**을 구하라. 간선 가중치는 **음수일 수 있다**. 도달할 수 없는 정점은 `X`로 표시한다.
- **입력**: 첫 줄 `N M S` (1 ≤ N ≤ 1,000, 0 ≤ M ≤ 5,000), 이후 M줄 `u v w`(u→v, -100 ≤ w ≤ 100). 사이클은 없다.
- **출력**: 정점 1..N의 최소 비용(도달 불가는 `X`)을 공백 구분 한 줄에.
- **예제**: `5 6 1 / 1 2 4 / 1 3 1 / 3 2 -3 / 2 4 2 / 3 4 5 / 5 4 1` → `0 -2 1 0 X` · `3 1 2 / 1 2 5` → `X 0 X`
- **셀프체크**: 음수 가중치가 있으면 다익스트라는 못 쓰지만 DAG에서는 위상 순서 DP가 그대로 통한다(각 정점을 한 번만 확정하므로 음수도 문제없음). `dist`를 `float('inf')`로 초기화하고 **`dist[u]`가 inf인 정점에서는 완화하지 말 것**(inf + w는 여전히 inf지만 습관적으로 막아라). 출발점이 아닌 진입차수 0 정점(예제의 5)도 Kahn 큐에는 넣어야 위상 순서가 완성된다.

```runner
@@SOLUTION
import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    s = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for _ in range(m):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        w = int(data[idx]); idx += 1
        graph[u].append((v, w))
        indeg[v] += 1
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[s] = 0
    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    while q:
        u = q.popleft()
        for v, w in graph[u]:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    print(' '.join('X' if dist[v] == INF else str(dist[v]) for v in range(1, n + 1)))

main()
@@TESTS
--IN
5 6 1
1 2 4
1 3 1
3 2 -3
2 4 2
3 4 5
5 4 1
--OUT
0 -2 1 0 X
--IN
3 1 2
1 2 5
--OUT
X 0 X
--IN
1 0 1
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- `dist[v]` = S에서 v까지의 최소 비용. u→v(w)마다 `dist[v] = min(dist[v], dist[u] + w)`로 완화하되, `dist[u]`가 최종값일 때만 밀어야 한다. DAG에서는 위상 순서로 u를 처리하면 u로 들어오는 간선이 모두 먼저 처리되어 `dist[u]`가 확정돼 있다.
- 다익스트라는 "확정된 정점은 다시 안 본다"는 가정 때문에 음수 간선에서 깨지지만, 위상 순서 DP는 순서 자체가 의존성을 보장하므로 음수 가중치도 그대로 된다. 시간 O(N + M).
- 도달 불가와 비용 0은 다르다 — `inf`로 초기화해 구분하고 출력 시 `X`로 바꾼다.

(2) 코드 단계별

- `N M S`를 읽고 `graph[u] = [(v, w), ...]`와 진입차수를 만든다.
- `dist[S] = 0`, 나머지 `inf`. 진입차수 0인 모든 정점(출발점이 아니어도)을 큐에 넣는다.
- Kahn으로 `u`를 꺼내며 `dist[u]`가 inf가 아닐 때만 이웃을 완화하고, 진입차수를 깎아 0이 되면 큐에.
- 1..N 순서로 `dist`를 출력하되 inf는 `X`.

(3) 스스로 다시 짤 때 생각 순서

- "DAG + 음수 가중치 + 출발점 고정" → 다익스트라 대신 위상 순서 DP(min). 최장 경로 문제에서 max를 min으로 바꾼 대칭형.
- 출발점이 고정이므로 seed는 `dist[S] = 0` 하나뿐이고 나머지는 inf(자유 시작인 최장 경로와 다름).
- 예제의 5처럼 S에서 못 가는 진입차수 0 정점도 Kahn에는 참여시키고, 그 정점에서는 완화하지 않는다.
```

**6) 필수 경유 정점을 지나는 경로 수** · Hard

- **요구사항**: DAG에서 정점 `S`에서 `T`로 가는 경로 중 **정점 `K`를 반드시 지나는** 경로의 수를 `1,000,000,007`로 나눈 나머지로 구하라. `K`가 `S`나 `T`와 같을 수도 있다.
- **입력**: 첫 줄 `N M S T K` (1 ≤ N ≤ 1,000, 0 ≤ M ≤ 5,000), 이후 M줄 `u v`.
- **출력**: 경로 수 mod 1e9+7.
- **예제**: `6 8 1 6 3 / 1 2 / 1 3 / 2 3 / 3 4 / 3 5 / 4 6 / 5 6 / 2 6` → `4` · `5 6 1 5 3 / 1 2 / 1 3 / 2 4 / 3 4 / 4 5 / 2 5` → `1`
- **셀프체크**: K를 지나는 경로는 "S→K 경로" 하나와 "K→T 경로" 하나의 이어붙임이고, DAG라 K를 두 번 지날 수 없으므로 **곱**으로 센다: `paths(S→K) × paths(K→T)`. 후자는 역그래프에서 T를 출발점으로 삼은 경로 수 DP로 얻는다. 두 번의 Kahn은 각각 **별도의 진입차수 배열**을 써야 한다(첫 번째가 깎아 버린 배열을 재사용하면 큐가 비어 있다). K가 S에서 도달 불가면 0, K=T면 `paths(K→T)=1`.

```runner
@@SOLUTION
import sys
from collections import deque

MOD = 1_000_000_007

def count_from(n, graph, indeg, src):
    # dp[v] = src에서 v로 가는 경로 수 (graph 방향 기준)
    dp = [0] * (n + 1)
    dp[src] = 1
    deg = indeg[:]                 # 원본 진입차수는 보존
    q = deque(v for v in range(1, n + 1) if deg[v] == 0)
    while q:
        u = q.popleft()
        for v in graph[u]:
            dp[v] = (dp[v] + dp[u]) % MOD
            deg[v] -= 1
            if deg[v] == 0:
                q.append(v)
    return dp

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    s = int(data[idx]); idx += 1
    t = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    rgraph = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    rindeg = [0] * (n + 1)
    for _ in range(m):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        graph[u].append(v)
        indeg[v] += 1
        rgraph[v].append(u)        # 역그래프
        rindeg[u] += 1
    f = count_from(n, graph, indeg, s)      # f[v] = S→v 경로 수
    g = count_from(n, rgraph, rindeg, t)    # g[v] = v→T 경로 수
    print(f[k] * g[k] % MOD)

main()
@@TESTS
--IN
6 8 1 6 3
1 2
1 3
2 3
3 4
3 5
4 6
5 6
2 6
--OUT
4
--IN
5 6 1 5 3
1 2
1 3
2 4
3 4
4 5
2 5
--OUT
1
--IN
3 2 1 3 2
1 3
2 3
--OUT
0
--IN
3 2 1 3 3
1 2
2 3
--OUT
1
@@EXPL
(1) 접근·핵심 아이디어

- DAG에서는 어떤 경로도 같은 정점을 두 번 지나지 않으므로, K를 지나는 S→T 경로는 "S→K 경로"와 "K→T 경로"를 하나씩 골라 이은 것과 일대일 대응한다. 따라서 답은 `f[K] × g[K]` (f = S에서 시작한 경로 수, g = T에서 끝나는 경로 수).
- `g`는 간선을 뒤집은 역그래프에서 T를 seed로 같은 경로 수 DP를 돌리면 된다. 역그래프에서 "T→v 경로 수"가 원그래프의 "v→T 경로 수"다.
- 경로 수는 폭발하므로 매 덧셈마다 mod를 유지하고, 마지막 곱셈에도 mod.
- 첫 예제: `f[3] = 2`(1→3, 1→2→3), `g[3] = 2`(3→4→6, 3→5→6) → 4. 1→2→6은 3을 안 지나므로 제외.

(2) 코드 단계별

- 간선을 읽으며 `graph`/`indeg`와 `rgraph`/`rindeg`를 동시에 만든다.
- `count_from(graph, indeg, S)`: `dp[S]=1`, Kahn Push로 `dp[v] += dp[u]`. 진입차수 배열은 복사본을 써서 원본을 남긴다.
- 같은 함수를 `rgraph`, `rindeg`, `T`로 다시 호출해 `g`를 얻는다.
- `f[K] * g[K] % MOD` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "반드시 지나는" → 경유 정점에서 경로를 둘로 쪼개 곱한다(DAG라 중복 통과 없음).
- 뒤쪽 절반은 역그래프 DP라는 도구를 떠올린다. 경로 수 DP 함수를 하나 만들어 두 번 재사용.
- 함정: 두 Kahn이 진입차수 배열을 공유하면 두 번째가 동작하지 않는다. K 도달 불가(0), K=T(g=1) 같은 경계도 곱셈 공식이 그대로 처리한다.
```

**7) 작업의 여유 시간** · Hard

- **요구사항**: 작업 `N`개가 있고 각 작업 v는 `t[v]` 시간이 걸린다. 선행 관계 `u v`는 "u가 끝나야 v를 시작할 수 있다"는 뜻이고 선행이 없는 작업은 0시에 시작할 수 있다(모든 작업은 병렬 가능). 전체를 **가장 빨리 끝내는 시각** `T`를 구하고, 각 작업에 대해 **전체 완료를 늦추지 않으면서 시작을 미룰 수 있는 최대 시간(여유 시간)**을 구하라.
- **입력**: 첫 줄 `N M` (1 ≤ N ≤ 1,000, 0 ≤ M ≤ 5,000), 둘째 줄 `t[1..N]` (1 ≤ t ≤ 1,000), 이후 M줄 `u v`. 사이클은 없다.
- **출력**: 첫 줄에 `T`, 둘째 줄에 작업 1..N의 여유 시간을 공백 구분.
- **예제**: `5 4 / 3 2 4 1 2 / 1 3 / 2 3 / 3 4 / 2 5` → `8 / 0 1 0 0 4` · `3 0 / 5 2 9` → `9 / 4 7 0`
- **셀프체크**: 두 번 훑는다. (a) 정방향(위상 순서)으로 가장 빠른 시작 `ES[v] = max(ES[u] + t[u])`, `T = max(ES[v] + t[v])`. (b) 역순(위상 순서를 뒤집어)으로 가장 늦은 완료 `LF[v] = min(LF[w] - t[w])`(후행 w), 후행이 없으면 `T`. 여유 = `(LF[v] - t[v]) - ES[v]`. 여유가 0인 작업들이 임계 경로다. 정방향 결과인 위상 순서 리스트를 저장해 두고 **뒤집어** 쓰면 역그래프를 따로 만들 필요가 없다.

```runner
@@SOLUTION
import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    t = [0] * (n + 1)
    for i in range(1, n + 1):
        t[i] = int(data[idx]); idx += 1
    graph = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for _ in range(m):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        graph[u].append(v)
        indeg[v] += 1
    # (a) 정방향: 가장 빠른 시작 ES, 위상 순서 order
    es = [0] * (n + 1)
    order = []
    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            if es[u] + t[u] > es[v]:
                es[v] = es[u] + t[u]
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    total = max(es[v] + t[v] for v in range(1, n + 1))
    # (b) 역순: 가장 늦은 완료 LF (후행이 없으면 total)
    lf = [total] * (n + 1)
    for u in reversed(order):
        for v in graph[u]:
            if lf[v] - t[v] < lf[u]:
                lf[u] = lf[v] - t[v]
    print(total)
    print(' '.join(str(lf[v] - t[v] - es[v]) for v in range(1, n + 1)))

main()
@@TESTS
--IN
5 4
3 2 4 1 2
1 3
2 3
3 4
2 5
--OUT
8
0 1 0 0 4
--IN
3 0
5 2 9
--OUT
9
4 7 0
--IN
1 0
7
--OUT
7
0
@@EXPL
(1) 접근·핵심 아이디어

- 가장 빠른 시작 `ES[v]`는 선행들의 완료 시각 최댓값이다(병렬이라 합이 아님): `ES[v] = max(ES[u] + t[u])`. 위상 순서로 Push하면 채워지고, 전체 완료 `T = max(ES[v] + t[v])`.
- 가장 늦은 완료 `LF[v]`는 "후행들이 각자 가장 늦은 시작 시각(`LF[w] - t[w]`)에 시작하려면 v는 언제까지 끝나야 하나"의 최솟값이다. 후행이 없으면 `T`. 후행이 먼저 확정돼야 하므로 **위상 순서의 역순**으로 채운다.
- 여유 시간 = 가장 늦은 시작 − 가장 빠른 시작 = `(LF[v] - t[v]) - ES[v]`. 이 값이 0인 작업이 하나라도 늦으면 전체가 늦는다(임계 경로). 시간 O(N + M).

(2) 코드 단계별

- `t`, 그래프, 진입차수를 읽는다.
- Kahn으로 `es`를 채우면서 꺼낸 순서를 `order`에 기록한다. `total = max(es + t)`.
- `lf`를 `total`로 초기화하고 `order`를 뒤집어 순회: `u`의 각 후행 `v`에 대해 `lf[u] = min(lf[u], lf[v] - t[v])`. 뒤집은 순서에서는 `v`가 `u`보다 먼저 처리되어 `lf[v]`가 확정돼 있다.
- `total`과 `lf[v] - t[v] - es[v]`를 출력.

(3) 스스로 다시 짤 때 생각 순서

- "완료 시각 + 미룰 수 있는 여유" → 정방향 DP(최댓값) 하나와 역방향 DP(최솟값) 하나, 두 값의 차이.
- 역방향은 역그래프를 새로 만들어도 되지만, 정방향에서 얻은 `order`를 뒤집어 쓰면 코드가 짧다.
- base 확인: 선행 없음 → ES=0, 후행 없음 → LF=T. 첫 예제의 작업 5(2시 완료, 8시까지 여유 4)로 손검산.
```

**8) 작은 번호를 최대한 앞으로** · Hard

- **요구사항**: 작업 `N`개와 선후 관계 `M`개(`u v`: u가 v보다 먼저)가 있다. 가능한 순서 중 다음 조건을 만족하는 순서를 출력하라: **1번 작업이 가능한 한 앞에** 오고, 그 조건을 지키는 순서들 중 **2번 작업이 가능한 한 앞에** 오고, … 이런 식으로 번호 순으로 위치를 최대한 앞당긴다. 사이클이 있으면 `-1`.
- **입력**: 첫 줄 `N M` (1 ≤ N ≤ 1,000, 0 ≤ M ≤ 5,000), 이후 M줄 `u v`.
- **출력**: 조건을 만족하는 순서(공백 구분) 또는 `-1`.
- **예제**: `3 1 / 3 1` → `3 1 2` · `5 4 / 4 1 / 4 2 / 5 3 / 3 2` → `4 1 5 3 2`
- **셀프체크**: 이 문제는 **사전순 최소와 다르다**. 첫 예제의 사전순 최소는 `2 3 1`이지만, 1번을 최대한 앞으로 보내려면 3을 먼저 처리하고 바로 1을 놓는 `3 1 2`가 답이다. 정석은 **역그래프에서 최대 힙 Kahn을 돌려 얻은 순서를 뒤집는 것**: 뒤에서부터 "지금 마지막에 놓을 수 있는 것 중 가장 큰 번호"를 고르면 큰 번호가 뒤로 밀리고, 결과적으로 작은 번호가 앞당겨진다. 사이클 판정은 역그래프에서도 "꺼낸 개수 < N"으로 동일하다.

```runner
@@SOLUTION
import sys
import heapq

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    rgraph = [[] for _ in range(n + 1)]   # 역그래프: v -> u
    rindeg = [0] * (n + 1)
    for _ in range(m):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        rgraph[v].append(u)
        rindeg[u] += 1
    # 역그래프에서 최대 힙 Kahn: "맨 뒤에 놓을 수 있는 것 중 가장 큰 번호"부터
    h = [-v for v in range(1, n + 1) if rindeg[v] == 0]
    heapq.heapify(h)
    order = []
    while h:
        u = -heapq.heappop(h)
        order.append(u)
        for v in rgraph[u]:
            rindeg[v] -= 1
            if rindeg[v] == 0:
                heapq.heappush(h, -v)
    if len(order) < n:
        print(-1)
    else:
        print(' '.join(map(str, order[::-1])))   # 뒤에서부터 채운 것을 뒤집는다

main()
@@TESTS
--IN
3 1
3 1
--OUT
3 1 2
--IN
5 4
4 1
4 2
5 3
3 2
--OUT
4 1 5 3 2
--IN
2 2
1 2
2 1
--OUT
-1
--IN
4 0
--OUT
1 2 3 4
@@EXPL
(1) 접근·핵심 아이디어

- "1번을 최대한 앞으로"는 사전순 최소와 다르다. 사전순 최소 힙-Kahn은 "지금 놓을 수 있는 것 중 가장 작은 것"을 앞에서부터 고르는데, 그러면 1의 선행이 큰 번호일 때(예: 3→1) 1을 뒤로 미루고 2를 먼저 놓아 버린다.
- 대신 순서를 **뒤에서부터** 만든다. 역그래프(간선을 뒤집은 그래프)에서 진입차수가 0인 정점은 원그래프에서 "후행이 없는 = 맨 뒤에 놓아도 되는" 정점이다. 그중 **가장 큰 번호**를 뒤에 놓는 선택을 반복하면 큰 번호가 최대한 뒤로 밀리고, 그 결과 작은 번호가 번호 순으로 최대한 앞당겨진다. 마지막에 뒤집으면 답.
- 둘째 예제: 역그래프 최대 힙 순서는 `2 3 5 1 4`, 뒤집으면 `4 1 5 3 2`. 1은 선행 4 바로 뒤(2번째)라 더 앞당길 수 없고, 그 상태에서 2는 5·3 뒤인 5번째가 최선이다. 사전순 최소인 `4 1 2 5 3`과 다르다.

(2) 코드 단계별

- 간선 `u v`를 읽되 **역방향**으로 저장한다: `rgraph[v].append(u)`, `rindeg[u] += 1`.
- 역그래프 진입차수 0인 정점을 음수로 힙에 넣어 최대 힙을 만든다.
- 꺼낸 정점을 `order`에 추가하고, 역그래프 이웃의 진입차수를 깎아 0이 되면 push.
- 꺼낸 개수가 N 미만이면 `-1`, 아니면 `order`를 뒤집어 출력.

(3) 스스로 다시 짤 때 생각 순서

- "작은 번호를 최대한 앞으로"라는 문장을 보면 사전순 최소가 아닌지 먼저 의심한다. `3→1` 한 개짜리 반례를 손으로 만들어 확인.
- "앞에서 작은 것 고르기"가 안 되면 "뒤에서 큰 것 고르기"로 뒤집어 본다 = 역그래프 + 최대 힙 + 결과 반전.
- 사이클 판정은 그대로. M=0이면 큰 번호부터 뒤에 놓여 `1 2 … N`이 나오는지 확인.
```
