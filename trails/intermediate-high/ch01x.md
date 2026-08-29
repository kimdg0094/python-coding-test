## L5. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch01(트리)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. 루트 고정 순회·서브트리 누적·지름·이진 트리 스택 순회·Tree DP·LCA를 소재와 입력 형식을 바꿔 여러 번 다시 짜 본다.
- **반복 훈련 개념**:
  - 루트 고정 BFS로 `parent/depth/order`를 채우고, 서브트리 값은 `for u in reversed(order): acc[parent[u]] += acc[u]`로 아래→위 누적
  - 지름은 BFS 두 번(`a = far(1)`, `b = far(a)`), 그리고 "임의 정점의 최원점은 지름 끝점 중 하나"라 `ecc[v] = max(dA[v], dB[v])`
  - 이진 트리는 `left/right/value` 배열 + 명시적 스택(`stack.pop()`)으로 재귀 없이 순회, 레벨은 `q = nxt`로 한 층씩 교체
  - Tree DP는 정점당 상태 2개(`dp0[u]`, `dp1[u]`)를 두고 자식→부모로 `min`/`max`/`+` 누적
  - LCA는 깊이 맞춘 뒤 같이 올리기(`while a != b: a, b = par[a], par[b]`) 또는 `up[k][v] = up[k-1][up[k-1][v]]` 희소 표
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '트리'·'최소 공통 조상' 단계, solved.ac CLASS 4~5의 트리 DP·LCA 문제, NeetCode 150의 'Trees'(지그재그 레벨 순회·BST 유효성·k번째 원소).
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 루트를 바꾼 부모 표 | Easy | 루트 고정 BFS·parent | 반복 훈련 |
| 2 | 지그재그 레벨 순회 | Medium | 레벨별 큐 교체·홀수 층 뒤집기 | 유형 확장 (NeetCode 'Trees' 스타일) |
| 3 | BST 유효성 검사 | Medium | 스택 순회 + (lo, hi) 범위 전파 | 유형 확장 (NeetCode 'Trees' 스타일) |
| 4 | 임계값 이상 서브트리 수 | Medium | order 역순 서브트리 합 | 반복 훈련 |
| 5 | 트리 센트로이드 찾기 | Medium | 서브트리 크기 → 제거 후 최대 조각 | 반복 훈련 |
| 6 | 부모 배열로 경로 위 정점 수 | Medium | 단순 상승 LCA + 거리 공식 | 반복 훈련 |
| 7 | BST k번째 작은 값 질의 | Hard | BST 삽입 + 서브트리 크기 + 순위 탐색 | 반복 훈련 |
| 8 | 경비 초소 최소 비용 | Hard | Tree DP 두 상태(min 버전) | 유형 확장 (백준 '트리' 단계 스타일) |
| 9 | 모든 정점의 최원거리 | Hard | 지름 끝점 BFS 3회 | 반복 훈련 |
| 10 | 경로 위 최대 간선 가중치 질의 | Hard | 희소 표 + 점프별 최댓값 | 유형 확장 (백준 '최소 공통 조상' 단계 스타일) |

**문제**

**1) 루트를 바꾼 부모 표** · Easy

- **요구사항**: 트리와 루트 정점 r이 주어진다. r을 루트로 잡았을 때 각 정점의 부모를 구하라. 루트의 부모는 0으로 둔다.
- **입력**: 첫 줄에 `N r` (1 ≤ N ≤ 300, 1 ≤ r ≤ N). 다음 N-1줄에 간선 `a b` (1-indexed).
- **출력**: 정점 1부터 N까지의 부모를 공백으로 구분해 한 줄에.
- **예제**:
  `7 3 / 1 2 / 1 3 / 3 4 / 3 5 / 5 6 / 5 7` → `3 1 0 3 3 5 5`
  (3이 루트이므로 1의 부모는 3, 2의 부모는 1)
  `4 4 / 1 2 / 2 3 / 3 4` → `2 3 4 0`
- **셀프체크**: 루트가 1이 아닐 때 BFS 시작점을 r로 바꿨는가? 방문 표시를 `parent == -1`로 대신하면 루트(부모 0)와 미방문(-1)이 구분되는가? N=1이면 `0` 하나만 출력되는가?

```runner
@@SOLUTION
import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); r = int(data[idx + 1]); idx += 2
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        g[a].append(b)
        g[b].append(a)

    parent = [-1] * (n + 1)   # -1: 아직 방문 안 함
    parent[r] = 0             # 루트의 부모는 0
    q = deque([r])
    while q:
        u = q.popleft()
        for v in g[u]:
            if parent[v] == -1:
                parent[v] = u
                q.append(v)
    print(*parent[1:])

main()
@@TESTS
--IN
7 3
1 2
1 3
3 4
3 5
5 6
5 7
--OUT
3 1 0 3 3 5 5
--IN
4 4
1 2
2 3
3 4
--OUT
2 3 4 0
--IN
1 1
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 트리는 루트를 어디로 잡느냐에 따라 부모 관계가 완전히 달라진다. "루트 고정 → BFS로 방향 주기"가 모든 트리 문제의 첫 단계이며, 여기서는 시작점만 1 대신 r로 바꾸면 된다.
- 무방향 인접 리스트에서 되돌아가는 간선을 막아야 하므로 방문 여부가 필요한데, `parent`를 -1로 초기화하면 방문 배열을 따로 두지 않아도 된다(루트는 0, 미방문은 -1로 구분).

(2) 코드 단계별

- 인접 리스트를 양방향으로 채운다.
- `parent[r] = 0`으로 두고 r부터 BFS. 이웃 v가 -1(미방문)이면 `parent[v] = u`로 기록하고 큐에 넣는다.
- `parent[1..N]`을 공백으로 출력한다.

(3) 스스로 다시 짤 때 생각 순서

- 루트 r 확인 → BFS 시작점을 r로 → 방문 체크를 parent 값으로 대신 → 출력. N=1이면 간선이 없어 BFS가 바로 끝나고 `0`만 출력된다.
- 시간 O(N), 공간 O(N). 재귀가 없으므로 일자 트리에서도 안전하다.
```

**2) 지그재그 레벨 순회** · Medium

- **요구사항**: 1번을 루트로 하는 이진 트리가 각 노드의 왼쪽/오른쪽 자식으로 주어진다. 레벨(깊이)별로 노드 번호를 출력하되, 깊이 0은 왼쪽→오른쪽, 깊이 1은 오른쪽→왼쪽, 깊이 2는 다시 왼쪽→오른쪽 … 처럼 방향을 번갈아 가며 출력하라.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 다음 N줄: `node left right` (자식이 없으면 0). 노드 번호는 1..N.
- **출력**: 깊이 0부터 한 줄에 한 레벨씩, 노드 번호를 공백으로 구분.
- **예제**:
  `7 / 1 2 3 / 2 4 5 / 3 6 7 / 4 0 0 / 5 0 0 / 6 0 0 / 7 0 0` → `1` `3 2` `4 5 6 7`
  `4 / 1 0 2 / 2 3 0 / 3 0 4 / 4 0 0` → `1` `2` `3` `4`
- **셀프체크**: 다음 레벨을 만들 때는 반드시 **원래(왼→오) 순서**의 현재 레벨을 훑어야 한다 — 뒤집은 리스트로 자식을 모으면 다음 레벨 순서가 꼬인다. 자식 0을 큐에 넣지 않았는가? 한쪽으로 치우친 트리에서 각 레벨이 한 개씩 출력되는가?

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    left = [0] * (n + 1)
    right = [0] * (n + 1)
    for _ in range(n):
        node = int(data[idx]); l = int(data[idx + 1]); r = int(data[idx + 2]); idx += 3
        left[node] = l
        right[node] = r

    out = []
    cur = [1]          # 현재 레벨(항상 왼→오 순서로 유지)
    level = 0
    while cur:
        nxt = []
        for u in cur:  # 원래 순서로 자식을 모아야 다음 레벨 순서가 맞다
            if left[u]:
                nxt.append(left[u])
            if right[u]:
                nxt.append(right[u])
        row = cur if level % 2 == 0 else cur[::-1]
        out.append(' '.join(map(str, row)))
        cur = nxt
        level += 1
    print('\n'.join(out))

main()
@@TESTS
--IN
7
1 2 3
2 4 5
3 6 7
4 0 0
5 0 0
6 0 0
7 0 0
--OUT
1
3 2
4 5 6 7
--IN
4
1 0 2
2 3 0
3 0 4
4 0 0
--OUT
1
2
3
4
--IN
1
1 0 0
--OUT
1
--IN
6
1 2 3
2 0 4
3 5 0
4 6 0
5 0 0
6 0 0
--OUT
1
3 2
4 5
6
@@EXPL
(1) 접근·핵심 아이디어

- 레벨 순회(BFS)를 "한 층 전체를 리스트로 들고 다음 층 리스트로 교체"하는 형태로 쓰면 레벨 경계가 자연스럽게 생긴다. 지그재그는 출력할 때만 홀수 층을 뒤집으면 된다.
- 함정: 다음 층을 만들 때 뒤집힌 순서로 자식을 모으면 그 다음 층의 "왼→오" 기준이 깨진다. 내부 상태(`cur`)는 항상 왼→오로 유지하고, 뒤집기는 출력 시점에만 적용한다.

(2) 코드 단계별

- `left/right` 배열을 입력대로 채운다(자식 없음은 0).
- `cur = [1]`, `level = 0`에서 시작. `cur`를 원래 순서로 돌며 0이 아닌 자식만 `nxt`에 추가.
- `level`이 홀수면 `cur[::-1]`, 짝수면 그대로 출력 줄에 추가. `cur = nxt`, `level += 1`.
- `cur`가 비면 종료.

(3) 스스로 다시 짤 때 생각 순서

- 레벨 단위 BFS 골격(현재 층 → 다음 층) → 홀수 층만 출력 방향 반전 → 자식 0 걸러내기. 시간 O(N), 공간 O(가장 넓은 층).
- 재귀 DFS로 깊이별 리스트를 모아도 되지만, 치우친 트리에서 깊이가 N까지 커질 수 있으므로 반복형이 안전하다.
```

**3) BST 유효성 검사** · Medium

- **요구사항**: 1번을 루트로 하는 이진 트리가 각 노드의 값과 자식으로 주어진다. 모든 노드에서 "왼쪽 서브트리의 모든 값 < 노드 값 < 오른쪽 서브트리의 모든 값"이 성립하면(같은 값도 허용하지 않음) `YES`, 아니면 `NO`를 출력하라.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 다음 N줄: `node value left right` (자식 없으면 0, -10^9 ≤ value ≤ 10^9).
- **출력**: `YES` 또는 `NO`.
- **예제**:
  `5 / 1 8 2 3 / 2 3 4 5 / 3 10 0 0 / 4 1 0 0 / 5 6 0 0` → `YES`
  `4 / 1 10 2 0 / 2 5 3 4 / 3 1 0 0 / 4 12 0 0` → `NO`
  (노드 4(값 12)는 부모 5보다는 크지만 조상 10의 왼쪽에 있으므로 10보다 작아야 한다)
- **셀프체크**: 부모와만 비교하면 둘째 예제를 잡지 못한다 — 각 노드가 가질 수 있는 **허용 범위 (lo, hi)** 를 위에서 아래로 전파했는가? 같은 값이 나오면 NO로 판정했는가(부등호가 엄격한가)? 노드 하나뿐인 트리는 YES인가?

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    val = [0] * (n + 1)
    left = [0] * (n + 1)
    right = [0] * (n + 1)
    for _ in range(n):
        node = int(data[idx]); v = int(data[idx + 1])
        l = int(data[idx + 2]); r = int(data[idx + 3]); idx += 4
        val[node] = v
        left[node] = l
        right[node] = r

    NEG = -10 ** 18
    POS = 10 ** 18
    stack = [(1, NEG, POS)]   # (노드, 허용 하한, 허용 상한) — 열린 구간
    ok = True
    while stack:
        u, lo, hi = stack.pop()
        if not (lo < val[u] < hi):
            ok = False
            break
        if left[u]:
            stack.append((left[u], lo, val[u]))
        if right[u]:
            stack.append((right[u], val[u], hi))
    print("YES" if ok else "NO")

main()
@@TESTS
--IN
5
1 8 2 3
2 3 4 5
3 10 0 0
4 1 0 0
5 6 0 0
--OUT
YES
--IN
4
1 10 2 0
2 5 3 4
3 1 0 0
4 12 0 0
--OUT
NO
--IN
1
1 5 0 0
--OUT
YES
--IN
2
1 5 2 0
2 5 0 0
--OUT
NO
@@EXPL
(1) 접근·핵심 아이디어

- BST 조건은 "부모와 자식의 비교"가 아니라 "조상 전체가 만드는 범위"다. 루트는 (-∞, ∞), 왼쪽 자식으로 내려가면 상한이 부모 값으로, 오른쪽으로 내려가면 하한이 부모 값으로 좁아진다. 각 노드 값이 자기 범위 안에 있으면 유효하다.
- 이렇게 "부모 정보를 자식에 전파"하는 것은 전위 순회 패턴이며, 명시적 스택으로 반복 구현하면 깊은 트리에서도 안전하다.

(2) 코드 단계별

- `val/left/right` 배열을 채운다.
- 스택에 `(1, NEG, POS)`를 넣고 시작. pop한 노드가 `lo < val < hi`를 어기면 즉시 NO.
- 왼쪽 자식은 `(left, lo, val[u])`, 오른쪽 자식은 `(right, val[u], hi)`로 범위를 좁혀 push.
- 스택이 빌 때까지 위반이 없으면 YES.

(3) 스스로 다시 짤 때 생각 순서

- "범위 전파" 아이디어 확정 → 스택 원소를 (노드, lo, hi) 튜플로 → 열린 구간 비교로 중복 값 배제 → 위반 즉시 종료. 시간 O(N), 공간 O(높이).
- 대안: 중위 순회가 엄격히 증가하는지 확인해도 된다(값이 -10^9~10^9라 초기 비교값은 그보다 작게 잡을 것). 어느 쪽이든 "부모하고만 비교"는 오답임을 기억하자.
```

**4) 임계값 이상 서브트리 수** · Medium

- **요구사항**: 정점 1을 루트로 하는 트리의 각 정점에 정수 가중치(음수 가능)가 있다. 서브트리(자신 포함) 가중치 합이 T 이상인 정점의 개수를 세고, 그 정점 번호들을 오름차순으로 출력하라.
- **입력**: 첫 줄 `N T` (1 ≤ N ≤ 300, -10^6 ≤ T ≤ 10^6). 둘째 줄 정점 1..N의 가중치(-100 ≤ w ≤ 100). 다음 N-1줄 간선 `a b`.
- **출력**: 첫 줄에 개수. 개수가 1 이상이면 둘째 줄에 해당 정점 번호를 오름차순으로 공백 구분.
- **예제**:
  `7 20 / 10 5 20 8 15 -6 9 / 1 2 / 1 3 / 3 4 / 3 5 / 5 6 / 5 7` → `2` `1 3`
  (정점 5의 서브트리 합은 15-6+9=18로 미달, 3은 46, 1은 61)
  `3 100 / 1 2 3 / 1 2 / 2 3` → `0`
- **셀프체크**: 가중치에 음수가 있으면 "부모 합 ≥ 자식 합"이 성립하지 않는다 — 조상이 미달이어도 자식이 조건을 만족할 수 있음을 반영했는가? 리프의 합은 자기 가중치 그대로인가? 개수 0일 때 둘째 줄을 출력하지 않는가?

```runner
@@SOLUTION
import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); t = int(data[idx + 1]); idx += 2
    w = [0] * (n + 1)
    for i in range(1, n + 1):
        w[i] = int(data[idx]); idx += 1
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        g[a].append(b)
        g[b].append(a)

    parent = [0] * (n + 1)
    seen = [False] * (n + 1)
    order = []
    seen[1] = True
    q = deque([1])
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                q.append(v)

    ssum = w[:]                      # 자기 가중치로 초기화
    for u in reversed(order):        # 자식이 먼저 확정
        if parent[u]:
            ssum[parent[u]] += ssum[u]

    res = [i for i in range(1, n + 1) if ssum[i] >= t]
    print(len(res))
    if res:
        print(*res)

main()
@@TESTS
--IN
7 20
10 5 20 8 15 -6 9
1 2
1 3
3 4
3 5
5 6
5 7
--OUT
2
1 3
--IN
3 100
1 2 3
1 2
2 3
--OUT
0
--IN
4 0
-5 3 -2 4
1 2
1 3
3 4
--OUT
4
1 2 3 4
--IN
1 5
5
--OUT
1
1
@@EXPL
(1) 접근·핵심 아이디어

- 서브트리 합은 "자식들의 서브트리 합 + 자기 가중치"라는 Tree DP의 가장 기본형이다. 루트에서 BFS로 방문순서를 얻고 역순으로 누적하면 재귀 없이 아래→위로 채워진다.
- 함정: 음수 가중치가 있으면 서브트리 합이 위로 갈수록 커진다는 보장이 없다. 셋째 테스트에서 루트 합은 0인데 자식 합은 3, 4처럼 더 크다. 따라서 "루트가 미달이면 전부 미달"같은 가지치기는 오답이다. 모든 정점을 개별로 검사한다.

(2) 코드 단계별

- 가중치와 무방향 인접 리스트를 읽는다.
- 루트 1에서 BFS로 `parent`, `order`를 만든다.
- `ssum = w[:]`로 초기화한 뒤 `order` 역순으로 `ssum[parent[u]] += ssum[u]`.
- `ssum[i] >= t`인 i를 오름차순으로 모아 개수를 출력하고, 비어 있지 않으면 목록도 출력한다.

(3) 스스로 다시 짤 때 생각 순서

- BFS로 parent/order → 합 배열을 가중치로 초기화 → 역순 누적 → 조건 필터. 시간 O(N), 공간 O(N).
- 검산: 루트의 `ssum[1]`은 모든 가중치의 총합과 같아야 한다. N=1이면 order가 [1]뿐이고 누적이 없어 `ssum[1] = w[1]`이다.
```

**5) 트리 센트로이드 찾기** · Medium

- **요구사항**: 트리에서 정점 하나를 제거하면 여러 조각(연결 요소)으로 나뉜다. "제거했을 때 남는 가장 큰 조각의 크기"가 최소가 되는 정점(센트로이드)을 찾아, 그 정점 번호와 그때의 최대 조각 크기를 출력하라. 후보가 여럿이면 번호가 가장 작은 것을 고른다.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 다음 N-1줄 간선 `a b`.
- **출력**: `정점번호 최대조각크기` 한 줄.
- **예제**:
  `7 / 1 2 / 1 3 / 3 4 / 3 5 / 5 6 / 5 7` → `3 3`
  (3을 제거하면 {1,2}, {4}, {5,6,7}로 나뉘어 최대 3. 1을 제거하면 {3,4,5,6,7}=5)
  `4 / 1 2 / 2 3 / 3 4` → `2 2`
  (2와 3 모두 최대 조각 2, 번호가 작은 2)
- **셀프체크**: 정점 u를 제거할 때 조각은 "각 자식의 서브트리"들과 "위쪽 나머지(N - size[u])" 이렇게 두 종류임을 모두 고려했는가? 서브트리 크기를 자식→부모 순으로 누적했는가? N=1이면 제거 후 남는 게 없어 `1 0`이 나오는가?

```runner
@@SOLUTION
import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        g[a].append(b)
        g[b].append(a)

    parent = [0] * (n + 1)
    seen = [False] * (n + 1)
    order = []
    seen[1] = True
    q = deque([1])
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                q.append(v)

    size = [1] * (n + 1)
    for u in reversed(order):
        if parent[u]:
            size[parent[u]] += size[u]

    best_u, best_w = 1, n
    for u in range(1, n + 1):
        worst = n - size[u]            # 위쪽 나머지 조각
        for v in g[u]:
            if parent[v] == u and size[v] > worst:
                worst = size[v]        # 자식 서브트리 조각
        if worst < best_w:             # 같으면 작은 번호 유지
            best_w = worst
            best_u = u
    print(best_u, best_w)

main()
@@TESTS
--IN
7
1 2
1 3
3 4
3 5
5 6
5 7
--OUT
3 3
--IN
4
1 2
2 3
3 4
--OUT
2 2
--IN
1
--OUT
1 0
--IN
5
1 2
1 3
1 4
1 5
--OUT
1 1
@@EXPL
(1) 접근·핵심 아이디어

- 정점 u를 지우면 트리는 (a) u의 각 자식 c가 이끄는 서브트리(크기 `size[c]`)와 (b) u의 위쪽에 남는 나머지(크기 `N - size[u]`)로 나뉜다. 이 조각들 중 최댓값이 u의 "나쁨"이고, 그 값이 최소인 정점이 센트로이드다.
- 서브트리 크기만 있으면 모든 정점의 값을 O(N)에 한 번에 구할 수 있다. 센트로이드는 항상 존재하며 최대 조각이 N/2 이하가 됨이 알려져 있다(분할 정복의 기초).

(2) 코드 단계별

- 루트 1에서 BFS로 `parent`, `order`를 만들고 역순 누적으로 `size`를 채운다.
- 각 u에 대해 `worst = n - size[u]`로 시작하고, 자식(`parent[v] == u`)의 `size[v]`와 비교해 최댓값을 갱신.
- `worst < best_w`일 때만 갱신하면(엄격 부등호) 같은 값에서 먼저 본 작은 번호가 유지된다.
- `best_u best_w` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "제거 후 조각 = 자식 서브트리들 + 위쪽 나머지" 분해를 먼저 떠올린다 → size 누적 → 정점마다 max 조각 계산 → 최소 선택(동률은 작은 번호). 시간 O(N).
- 경계: 루트는 위쪽 나머지가 0이고, N=1이면 자식도 없어 worst=0 → `1 0`. 별 모양(둘째 예제 참고)에서는 중심만 값 1, 나머지는 N-1이다.
```

**6) 부모 배열로 경로 위 정점 수** · Medium

- **요구사항**: 트리가 간선 목록이 아니라 **부모 배열**로 주어진다(루트의 부모는 0). Q개의 질의 `u v`에 대해 u에서 v로 가는 경로 위에 있는 정점의 개수(양 끝 포함)를 출력하라.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 둘째 줄 정점 1..N의 부모(정확히 하나가 0). 셋째 줄 Q (1 ≤ Q ≤ 100). 다음 Q줄 `u v`.
- **출력**: 질의마다 정점 개수를 한 줄에 하나씩.
- **예제**:
  `7 / 3 1 0 3 3 5 5 / 3 / 4 6 / 2 7 / 3 3` → `4` `5` `1`
  (루트는 3. 4-3-5-6은 정점 4개, 2-1-3-5-7은 5개, 같은 정점이면 1개)
  `1 / 0 / 1 / 1 1` → `1`
- **셀프체크**: 깊이를 구하려면 부모 배열에서 자식 목록을 만들어 루트부터 BFS해야 한다(부모 배열 순서가 깊이 순이라는 보장은 없다). 정점 수 = 간선 수 + 1 = `depth[u] + depth[v] - 2*depth[lca] + 1`인가? u=v면 1인가?

```runner
@@SOLUTION
import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    par = [0] * (n + 1)
    children = [[] for _ in range(n + 1)]
    root = 0
    for i in range(1, n + 1):
        p = int(data[idx]); idx += 1
        par[i] = p
        if p == 0:
            root = i
        else:
            children[p].append(i)

    depth = [0] * (n + 1)
    q = deque([root])
    while q:
        u = q.popleft()
        for v in children[u]:
            depth[v] = depth[u] + 1
            q.append(v)

    Q = int(data[idx]); idx += 1
    out = []
    for _ in range(Q):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        a, b = u, v
        while depth[a] > depth[b]:     # 깊은 쪽을 먼저 올려 깊이 맞추기
            a = par[a]
        while depth[b] > depth[a]:
            b = par[b]
        while a != b:                  # 같이 한 칸씩 올리기
            a = par[a]
            b = par[b]
        out.append(str(depth[u] + depth[v] - 2 * depth[a] + 1))
    print('\n'.join(out))

main()
@@TESTS
--IN
7
3 1 0 3 3 5 5
3
4 6
2 7
3 3
--OUT
4
5
1
--IN
1
0
1
1 1
--OUT
1
--IN
5
0 1 2 3 4
2
5 1
5 3
--OUT
5
3
@@EXPL
(1) 접근·핵심 아이디어

- 부모 배열이 곧 "위로 올라가는 포인터"이므로 LCA를 가장 단순한 방식으로 구할 수 있다: 두 정점의 깊이를 맞춘 뒤 같아질 때까지 함께 한 칸씩 올린다. N ≤ 300, Q ≤ 100이면 질의당 O(깊이)로 충분하다.
- 경로 위 정점 수는 간선 수 + 1이고, 간선 수는 `depth[u] + depth[v] - 2*depth[lca]`다.

(2) 코드 단계별

- 부모 배열을 읽으며 루트(부모 0)를 찾고 `children` 목록을 만든다.
- 루트부터 BFS로 `depth`를 채운다. 입력 순서가 깊이 순이 아닐 수 있으므로 한 줄씩 `depth[i] = depth[par[i]] + 1`로 채우면 틀릴 수 있다.
- 질의마다 깊은 쪽을 올려 깊이를 맞추고, 다르면 둘 다 부모로 올린다. 만나는 정점이 LCA.
- 거리 공식 + 1을 출력.

(3) 스스로 다시 짤 때 생각 순서

- 입력 형식(부모 배열)에서 자식 리스트·루트 복원 → BFS depth → 단순 상승 LCA → 정점 수 공식. 전처리 O(N), 질의당 O(N) 최악(일자 트리).
- 경계: u=v면 깊이 맞추기·상승 루프가 모두 0번 돌고 공식이 `0 + 1 = 1`을 준다. 한쪽이 다른 쪽의 조상이면 깊이 맞추기만으로 같아진다.
```

**7) BST k번째 작은 값 질의** · Hard

- **요구사항**: 값을 주어진 순서대로 BST에 삽입한 뒤(중복 없음), Q개의 질의 k에 대해 "k번째로 작은 값"을 출력하라. 질의마다 중위 순회를 처음부터 다시 하지 말고, 각 노드의 **서브트리 크기**를 미리 구해 루트에서 한 번 내려가며 찾아라.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 둘째 줄 삽입할 N개의 서로 다른 정수. 셋째 줄 Q (1 ≤ Q ≤ 100). 넷째 줄 Q개의 k (1 ≤ k ≤ N).
- **출력**: 질의마다 k번째 작은 값을 한 줄에 하나씩.
- **예제**:
  `7 / 5 3 8 1 4 7 9 / 3 / 1 4 7` → `1` `5` `9`
  `5 / 10 20 30 40 50 / 2 / 5 1` → `50` `10`
  (오름차순 삽입이라 오른쪽으로만 치우친 트리)
- **셀프체크**: 노드 u에서 왼쪽 서브트리 크기를 L이라 할 때, `k ≤ L`이면 왼쪽으로, `k == L+1`이면 u가 답, 아니면 `k -= L+1` 후 오른쪽으로 가는 분기를 정확히 썼는가? 서브트리 크기는 자식이 먼저 확정되는 순서(후위)로 누적했는가? 치우친 트리에서도 재귀 없이 동작하는가?

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    vals = [int(data[idx + i]) for i in range(n)]; idx += n
    Q = int(data[idx]); idx += 1

    left = [0] * (n + 1)
    right = [0] * (n + 1)
    value = [0] * (n + 1)
    root = 0
    cnt = 0
    for v in vals:                      # 반복형 삽입
        cnt += 1
        value[cnt] = v
        if root == 0:
            root = cnt
            continue
        cur = root
        while True:
            if v < value[cur]:
                if left[cur] == 0:
                    left[cur] = cnt
                    break
                cur = left[cur]
            else:
                if right[cur] == 0:
                    right[cur] = cnt
                    break
                cur = right[cur]

    # 서브트리 크기: 전위 방문 순서의 역순 = 자식이 먼저 확정
    order = []
    stack = [root]
    while stack:
        u = stack.pop()
        order.append(u)
        if left[u]:
            stack.append(left[u])
        if right[u]:
            stack.append(right[u])
    size = [0] * (n + 1)
    for u in reversed(order):
        size[u] = 1 + size[left[u]] + size[right[u]]   # size[0] = 0

    out = []
    for _ in range(Q):
        k = int(data[idx]); idx += 1
        cur = root
        while True:
            ls = size[left[cur]]
            if k <= ls:
                cur = left[cur]
            elif k == ls + 1:
                out.append(str(value[cur]))
                break
            else:
                k -= ls + 1
                cur = right[cur]
    print('\n'.join(out))

main()
@@TESTS
--IN
7
5 3 8 1 4 7 9
3
1 4 7
--OUT
1
5
9
--IN
5
10 20 30 40 50
2
5 1
--OUT
50
10
--IN
1
42
1
1
--OUT
42
--IN
6
40 20 60 10 30 50
3
3 4 6
--OUT
30
40
60
@@EXPL
(1) 접근·핵심 아이디어

- BST에서 노드 u의 왼쪽 서브트리에는 u보다 작은 값만 있다. 왼쪽 크기를 L이라 하면 u는 자기 서브트리 안에서 정확히 L+1번째다. 따라서 k와 L을 비교해 한쪽으로만 내려가면 O(높이)에 k번째를 찾는다(순위 통계 트리의 기본 아이디어).
- 서브트리 크기는 Ch01 L1의 "order 역순 누적"을 이진 트리에 그대로 적용한다. 인덱스 0을 "빈 노드"로 두고 `size[0] = 0`으로 놓으면 자식 유무 분기가 사라진다.

(2) 코드 단계별

- L2와 같은 배열 기반 반복형 삽입으로 BST를 만든다.
- 스택으로 전위 방문 순서 `order`를 얻고, 역순으로 `size[u] = 1 + size[left[u]] + size[right[u]]`.
- 질의: `ls = size[left[cur]]`. `k <= ls`면 왼쪽으로, `k == ls+1`이면 현재 값이 답, 아니면 `k -= ls+1` 하고 오른쪽으로.
- 결과를 줄마다 출력.

(3) 스스로 다시 짤 때 생각 순서

- BST 삽입(반복형) → 서브트리 크기(전위 역순) → 순위 탐색 분기 3가지. 전처리 O(N), 질의당 O(높이)이며 최악(치우침) O(N).
- 경계: 둘째 예제처럼 오름차순 삽입이면 왼쪽 크기가 항상 0이라 `k -= 1`을 반복하며 오른쪽으로 내려간다. k=1은 항상 최솟값, k=N은 최댓값이 나와야 한다.
```

**8) 경비 초소 최소 비용** · Hard

- **요구사항**: 트리의 각 정점에 초소를 세우는 비용이 있다. 모든 간선은 양 끝점 중 **적어도 하나**에 초소가 있어야 감시된다. 모든 간선을 감시하는 데 드는 최소 총비용을 구하라(트리의 최소 가중 정점 커버).
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 둘째 줄 정점 1..N의 비용(1 ≤ c ≤ 1000). 다음 N-1줄 간선 `a b`.
- **출력**: 최소 총비용.
- **예제**:
  `7 / 10 5 20 8 15 6 9 / 1 2 / 1 3 / 3 4 / 3 5 / 5 6 / 5 7` → `33`
  (예: {1, 4, 5} = 10+8+15. 1이 1-2·1-3을, 4가 3-4를, 5가 3-5·5-6·5-7을 감시)
  `3 / 4 1 4 / 1 2 / 2 3` → `1`
  (가운데 2 하나로 두 간선 모두 감시)
- **셀프체크**: 상태를 "u에 초소를 세움(dp1)/안 세움(dp0)"으로 나눴을 때, u에 안 세우면 **모든 자식에 반드시** 세워야 하고(`dp0[u] += dp1[c]`), u에 세우면 자식은 자유(`dp1[u] += min(dp0[c], dp1[c])`)라는 점화식이 맞는가? L3의 독립 집합(max)과 방향이 어떻게 다른지 설명할 수 있는가? N=1이면 간선이 없어 0인가?

```runner
@@SOLUTION
import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    c = [0] * (n + 1)
    for i in range(1, n + 1):
        c[i] = int(data[idx]); idx += 1
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        g[a].append(b)
        g[b].append(a)

    if n == 1:
        print(0)
        return

    parent = [0] * (n + 1)
    seen = [False] * (n + 1)
    order = []
    seen[1] = True
    q = deque([1])
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                q.append(v)

    dp0 = [0] * (n + 1)   # u에 초소 없음 → 자식 전부 필수
    dp1 = [0] * (n + 1)   # u에 초소 있음 → 자식 자유
    for u in reversed(order):
        dp1[u] += c[u]
        p = parent[u]
        if p:
            dp0[p] += dp1[u]
            dp1[p] += min(dp0[u], dp1[u])
    print(min(dp0[1], dp1[1]))

main()
@@TESTS
--IN
7
10 5 20 8 15 6 9
1 2
1 3
3 4
3 5
5 6
5 7
--OUT
33
--IN
3
4 1 4
1 2
2 3
--OUT
1
--IN
1
7
--OUT
0
--IN
2
3 5
1 2
--OUT
3
@@EXPL
(1) 접근·핵심 아이디어

- 간선 (u, c)를 감시하려면 u 또는 c에 초소가 있어야 한다. 그래서 u에 초소가 없으면 모든 자식 c에는 반드시 있어야 하고, u에 있으면 자식은 있어도 없어도 된다. 이를 두 상태 Tree DP로 쓴다: `dp0[u] = Σ dp1[c]`, `dp1[u] = c[u] + Σ min(dp0[c], dp1[c])`.
- L3의 최대 독립 집합과 골격은 같지만 "고르면 자식은 못 고름(max)"이 "안 고르면 자식은 반드시 골라야 함(min)"으로 뒤집힌 구조다. 독립 집합의 여집합이 정점 커버라는 사실과도 맞물린다.

(2) 코드 단계별

- 비용과 인접 리스트를 읽는다. N=1이면 감시할 간선이 없으므로 0을 출력하고 끝낸다.
- 루트 1에서 BFS로 `parent`, `order`를 만든다.
- `order` 역순으로: `dp1[u] += c[u]`로 자기 비용을 더한 뒤 부모 p에 `dp0[p] += dp1[u]`, `dp1[p] += min(dp0[u], dp1[u])`를 누적한다(u를 처리하는 시점에 u의 두 값은 완성돼 있다).
- 답은 `min(dp0[1], dp1[1])`.

(3) 스스로 다시 짤 때 생각 순서

- 상태 정의(초소 있음/없음) → 간선 조건을 점화식으로 번역 → BFS order 역순 누적 → 루트에서 min. 시간 O(N), 공간 O(N).
- 경계: 리프는 자식이 없어 `dp0 = 0`, `dp1 = c`로 자연 초기화된다. 정점 2개 트리에서는 싼 쪽 하나만 세우면 되므로 `min(c1, c2)`가 나와야 한다(넷째 테스트).
```

**9) 모든 정점의 최원거리** · Hard

- **요구사항**: 트리의 **모든 정점 v**에 대해, v에서 가장 먼 정점까지의 거리(간선 수)를 구하라. 정점마다 BFS를 돌리는 O(N²) 대신, 지름의 두 끝점만 이용해 BFS 세 번으로 해결하라.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 다음 N-1줄 간선 `a b`.
- **출력**: 정점 1..N의 최원거리를 공백으로 구분해 한 줄에.
- **예제**:
  `7 / 1 2 / 1 3 / 3 4 / 3 5 / 5 6 / 5 7` → `3 4 2 3 3 4 4`
  (3에서 가장 먼 정점은 2·6·7로 거리 2. 지름 끝점 2와 6(또는 7)까지의 거리 중 큰 쪽)
  `4 / 1 2 / 1 3 / 1 4` → `1 2 2 2`
- **셀프체크**: "임의의 정점 v에서 가장 먼 정점은 반드시 지름의 한 끝점"이라는 성질을 설명할 수 있는가(아니라면 v에서의 최원 경로와 지름을 이어 더 긴 경로를 만들 수 있어 모순)? 첫 BFS로 끝점 A, A에서 BFS로 끝점 B와 `dA`, B에서 BFS로 `dB`를 얻은 뒤 `max(dA[v], dB[v])`를 썼는가? N=1이면 0인가?

```runner
@@SOLUTION
import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        g[a].append(b)
        g[b].append(a)

    def bfs(src):
        dist = [-1] * (n + 1)
        dist[src] = 0
        q = deque([src])
        far = src
        while q:
            u = q.popleft()
            for v in g[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    if dist[v] > dist[far]:
                        far = v
                    q.append(v)
        return far, dist

    a, _ = bfs(1)          # 아무 정점에서 가장 먼 정점 A = 지름의 한 끝
    b, da = bfs(a)         # A에서 가장 먼 정점 B = 반대쪽 끝, da = A로부터 거리
    _, db = bfs(b)         # db = B로부터 거리
    print(*[max(da[i], db[i]) for i in range(1, n + 1)])

main()
@@TESTS
--IN
7
1 2
1 3
3 4
3 5
5 6
5 7
--OUT
3 4 2 3 3 4 4
--IN
4
1 2
1 3
1 4
--OUT
1 2 2 2
--IN
1
--OUT
0
--IN
2
1 2
--OUT
1 1
@@EXPL
(1) 접근·핵심 아이디어

- 정점마다 BFS를 돌리면 O(N²)다. 대신 지름 성질을 한 단계 확장한다: 트리에서 임의 정점 v의 최원점은 항상 지름의 두 끝점 A, B 중 하나다. 따라서 `ecc[v] = max(dist(A, v), dist(B, v))`이고, A·B로부터의 거리 배열 두 개만 있으면 모든 정점의 답이 O(N)에 나온다.
- 왜 성립하나: v의 최원점 X가 A, B 어느 쪽도 아니라고 하자. v에서 지름 경로로 가는 갈림 지점을 P라 하면, X까지의 경로와 A 또는 B까지의 경로를 P에서 이어 붙여 지름보다 긴 경로가 만들어져 모순이다(L1의 "BFS 두 번" 증명과 같은 논리).

(2) 코드 단계별

- 인접 리스트를 만들고, `bfs(src)`가 "(가장 먼 정점, 거리 배열)"을 반환하도록 작성한다.
- `bfs(1)`로 끝점 A, `bfs(A)`로 끝점 B와 `da`, `bfs(B)`로 `db`를 얻는다.
- 정점마다 `max(da[i], db[i])`를 출력한다.

(3) 스스로 다시 짤 때 생각 순서

- 지름 BFS 2회 골격 재사용 → 세 번째 BFS로 반대 끝점 거리 확보 → 정점별 max. 시간 O(N), 공간 O(N).
- 경계: N=1이면 세 BFS 모두 자기 자신만 방문해 0. 별 모양에서는 중심 1, 나머지 2가 나와야 한다. 지름 끝점 선택이 여러 개(예: 6과 7)여도 어느 쪽을 골라도 답은 같다.
```

**10) 경로 위 최대 간선 가중치 질의** · Hard

- **요구사항**: 각 간선에 양의 가중치가 있는 트리에서 Q개의 질의 `u v`에 대해, u에서 v로 가는 경로 위 간선 가중치의 **최댓값**을 출력하라. u = v이면 0이다. 희소 표(binary lifting)에 "2^k칸 위로 가는 동안의 최대 가중치"를 함께 저장해 질의당 O(log N)에 답하라.
- **입력**: 첫 줄 N (1 ≤ N ≤ 300). 다음 N-1줄 간선 `a b w` (1 ≤ w ≤ 10^9). 다음 줄 Q (1 ≤ Q ≤ 100). 다음 Q줄 `u v`.
- **출력**: 질의마다 최댓값을 한 줄에 하나씩.
- **예제**:
  `5 / 1 2 2 / 1 3 3 / 3 4 4 / 3 5 1 / 3 / 2 4 / 4 5 / 5 5` → `4` `4` `0`
  (2-1-3-4는 2,3,4 중 4; 4-3-5는 4,1 중 4)
  `2 / 1 2 7 / 1 / 2 1` → `7`
- **셀프체크**: `mx[k][v] = max(mx[k-1][v], mx[k-1][up[k-1][v]])`처럼 점프를 반으로 쪼개 최댓값도 합쳤는가? 깊이 맞추기 단계에서 올라가며 지나간 간선의 최댓값을 잊지 않았는가? 마지막에 LCA 바로 아래에서 멈춘 두 정점에서 **한 칸 더**(`mx[0][u]`, `mx[0][v]`)를 반영했는가?

```runner
@@SOLUTION
import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a = int(data[idx]); b = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        g[a].append((b, w))
        g[b].append((a, w))
    Q = int(data[idx]); idx += 1

    parent = [0] * (n + 1)
    pw = [0] * (n + 1)          # 부모로 가는 간선의 가중치
    depth = [0] * (n + 1)
    seen = [False] * (n + 1)
    seen[1] = True
    q = deque([1])
    while q:
        u = q.popleft()
        for v, w in g[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                pw[v] = w
                depth[v] = depth[u] + 1
                q.append(v)

    LOG = max(1, n.bit_length())
    up = [[0] * (n + 1) for _ in range(LOG)]
    mx = [[0] * (n + 1) for _ in range(LOG)]
    up[0] = parent[:]
    mx[0] = pw[:]
    for k in range(1, LOG):
        for v in range(1, n + 1):
            mid = up[k - 1][v]
            up[k][v] = up[k - 1][mid]
            mx[k][v] = max(mx[k - 1][v], mx[k - 1][mid])

    def query(u, v):
        res = 0
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        for k in range(LOG):                 # 깊이 맞추기 — 지나간 최대도 반영
            if (diff >> k) & 1:
                res = max(res, mx[k][u])
                u = up[k][u]
        if u == v:
            return res
        for k in range(LOG - 1, -1, -1):     # 큰 점프부터, 조상이 다를 때만
            if up[k][u] != up[k][v]:
                res = max(res, mx[k][u], mx[k][v])
                u = up[k][u]
                v = up[k][v]
        return max(res, mx[0][u], mx[0][v])  # 마지막 한 칸(LCA 직전)

    out = []
    for _ in range(Q):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        out.append(str(query(u, v)))
    print('\n'.join(out))

main()
@@TESTS
--IN
5
1 2 2
1 3 3
3 4 4
3 5 1
3
2 4
4 5
5 5
--OUT
4
4
0
--IN
2
1 2 7
1
2 1
--OUT
7
--IN
4
1 2 5
2 3 3
3 4 9
2
1 4
1 3
--OUT
9
5
@@EXPL
(1) 접근·핵심 아이디어

- LCA 희소 표의 점화식 `up[k][v] = up[k-1][up[k-1][v]]`는 "2^k칸 = 2^(k-1)칸 두 번"이다. 같은 분해로 "그 구간의 최대 간선"도 `mx[k][v] = max(mx[k-1][v], mx[k-1][up[k-1][v]])`로 합칠 수 있다. 최댓값은 결합법칙을 만족하므로 점프를 쪼개 합쳐도 결과가 같다(합·최소·gcd 등도 같은 방식).
- 질의는 LCA 알고리즘과 동일하게 진행하되, 실제로 점프할 때마다 그 점프 구간의 `mx`를 답에 반영한다. LCA 자체를 반환할 필요는 없고 경로를 두 조각(u→LCA, v→LCA)으로 훑는 셈이다.

(2) 코드 단계별

- BFS로 `parent`, `depth`, 그리고 각 정점이 부모로 올라가는 간선 가중치 `pw`를 채운다.
- `up[0] = parent`, `mx[0] = pw`로 두고 k를 키우며 표를 채운다(가상 루트 0은 가중치 0이라 넘쳐도 무해).
- 질의: (1) 깊은 쪽을 올리며 지나간 `mx[k][u]`를 `res`에 반영. (2) 같아졌으면 반환. (3) 큰 k부터 조상이 다를 때만 두 정점을 함께 올리며 `mx`를 반영. (4) 마지막에 LCA 바로 아래에 멈춘 두 정점의 부모 간선 `mx[0]`을 더한다.

(3) 스스로 다시 짤 때 생각 순서

- LCA 골격 복사 → 표에 `mx` 추가 → 질의의 세 단계마다 "점프 = 답 갱신" 한 줄씩 삽입 → 마지막 한 칸 잊지 않기. 전처리 O(N log N), 질의 O(log N).
- 경계: u=v는 깊이 차 0·즉시 같음으로 0 반환. 한쪽이 조상이면 깊이 맞추기 단계만으로 끝나므로 그 단계에서도 `mx`를 반영해야 한다(셋째 테스트의 1-4처럼 일자 경로).
```
