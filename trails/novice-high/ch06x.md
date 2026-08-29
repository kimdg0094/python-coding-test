## L6. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch06(트리)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. 부모 배열·간선 목록·자식 배열·1-based 배열 등 서로 다른 입력 형식으로 트리를 만들고, 순회·BST·힙을 소재만 바꿔 다시 쓴다.
- **반복 훈련 개념**:
  - 입력 → 트리 구성: 부모 배열은 `children[parent[v]].append(v)`, 간선 목록은 `adj[u].append(v); adj[v].append(u)`
  - 재귀 순회 뼈대: `if v == 0: return` 뒤에 "현재를 어디서 append하느냐"로 전위/중위/후위가 갈린다
  - 내려가며 누적 / 올라오며 합치기: `path[c] = path[v] + val[c]` vs `size[parent[v]] += size[v]`
  - BST 하강: `cur = left[cur] if x < cur else right[cur]`
  - 힙 인덱스(0-based): 부모 `(i-1)//2`, 자식 `2*i+1`·`2*i+2`; 우선순위 큐는 `heapq.heappush(h, (키, 부가정보))`
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '트리'·'우선순위 큐' 단계, 프로그래머스 「코딩테스트 고득점 Kit」의 '힙', NeetCode 150의 'Trees'·'Heap'.
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 간선 목록으로 노드별 깊이 | Easy | 인접 리스트 + 내려가며 깊이 | 반복 훈련 |
| 2 | 배열 완전 이진 트리의 전위·후위 순회 | Easy | 1-based 배열 자식 공식 + 순회 | 반복 훈련 |
| 3 | BST의 최솟값·최댓값·높이 | Easy | BST 삽입 하강 | 반복 훈련 |
| 4 | 최소 힙 삽입 후 배열 상태 | Easy | 힙 sift-up 직접 구현 | 반복 훈련 |
| 5 | 후위+중위로 전위 복원 | Medium | 순회 결과로 트리 분할 | 반복 훈련 |
| 6 | 루트에서 리프까지 경로 합 최댓값 | Medium | 부모 배열 + 내려가며 누적 | 반복 훈련 |
| 7 | 좌우 대칭 이진 트리 판정 | Medium | 두 노드 동시 재귀 | 유형 확장 (NeetCode 'Trees' 스타일) |
| 8 | k개 정렬 목록 합치기 | Medium | 튜플 우선순위 큐 | 유형 확장 (NeetCode 'Heap' 스타일) |
| 9 | 묶음 합치기 최소 비용 | Medium | 힙에서 최소 두 개 꺼내 합치기 | 유형 확장 (백준 '우선순위 큐' 단계 스타일) |
| 10 | BST 삭제 후 순회 | Hard | BST 삭제 세 경우 + 순회 | 유형 확장 (백준 '트리' 단계 스타일) |
| 11 | 배열 힙 직접 구현 — 삽입과 삭제 | Hard | sift-up + sift-down | 반복 훈련 |
| 12 | 트리의 지름 | Hard | 간선 목록 + BFS 두 번 | 유형 확장 (백준 '트리' 단계 스타일) |

**문제**

**1) 간선 목록으로 노드별 깊이** · Easy

- **요구사항**: 노드 1..N과 N−1개의 간선(방향 없음)으로 주어진 트리에서, 루트를 1번으로 두었을 때 각 노드의 깊이(루트 0)를 구하라.

- **입력**: 첫 줄 N(1 ≤ N ≤ 1000). 이후 N−1줄에 간선 `u v`.

- **출력**: 노드 1..N의 깊이를 공백으로 구분해 한 줄.

- **예제**:

  - `5 / 1 2 / 1 3 / 3 4 / 3 5` → `0 1 1 2 2`  (1의 자식 2,3; 3의 자식 4,5)

  - `4 / 2 1 / 3 2 / 4 3` → `0 1 2 3`  (간선이 `자식 부모` 순으로 적혀 있어도 1→2→3→4 사슬)

- **셀프체크**: 간선 `u v`를 양쪽 인접 리스트에 모두 넣었는가(한쪽만 넣으면 `2 1`처럼 자식이 먼저 적힌 간선에서 끊김). 방향이 없으니 부모로 되돌아가지 않도록 `depth == -1`(미방문) 검사를 했는가. N=1이면 간선 줄이 없고 `0`만 출력되는가.

```runner
@@SOLUTION
import sys
from collections import deque
data = sys.stdin.read().split()
idx = 0
n = int(data[idx]); idx += 1
adj = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u = int(data[idx]); v = int(data[idx + 1]); idx += 2
    adj[u].append(v)
    adj[v].append(u)          # 방향 없음 → 양쪽에 등록

depth = [-1] * (n + 1)
depth[1] = 0
q = deque([1])
while q:
    v = q.popleft()
    for w in adj[v]:
        if depth[w] == -1:    # 아직 안 간 곳만 (부모로 되돌아가기 방지)
            depth[w] = depth[v] + 1
            q.append(w)
print(' '.join(str(depth[v]) for v in range(1, n + 1)))
@@TESTS
--IN
5
1 2
1 3
3 4
3 5
--OUT
0 1 1 2 2
--IN
4
2 1
3 2
4 3
--OUT
0 1 2 3
--IN
1
--OUT
0
--IN
6
1 2
1 3
1 4
1 5
1 6
--OUT
0 1 1 1 1 1
@@EXPL
(1) 접근·핵심 아이디어

- 간선 목록에는 부모/자식 구분이 없으므로 양방향 인접 리스트로 만든 뒤, 루트 1에서 출발해 "만나는 순서대로" 깊이를 부모 깊이+1로 매긴다. 방향이 없으니 방금 온 부모로 되돌아갈 수 있는데, 깊이가 이미 정해진 노드는 건너뛰면 된다. 노드·간선을 한 번씩 보므로 O(N).

(2) 코드 단계별

- `adj[u]`, `adj[v]` 양쪽에 서로를 추가한다.
- `depth`를 -1로 초기화하고 루트만 0으로 둔 뒤 큐 BFS(L2·L3의 레벨 순회와 같은 골격).
- 이웃 w의 `depth`가 -1일 때만 `depth[v]+1`로 채우고 큐에 넣는다.
- 1..N 순서로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "부모 배열이 아니라 간선"이면 먼저 양방향 인접 리스트로 바꾼다는 습관.
- 깊이는 "내려가며 계산"이므로 BFS/DFS 어느 쪽이든 부모 값+1.
- 되돌아가기 방지(방문 표시)를 빠뜨리면 무한 루프. N=1(간선 0개) 경계값 확인.
```

**2) 배열 완전 이진 트리의 전위·후위 순회** · Easy

- **요구사항**: 1-based 배열 A[1..N]에 저장된 완전 이진 트리(노드 i의 왼쪽 자식 2i, 오른쪽 자식 2i+1)를 전위·후위 순회한 값을 출력하라.

- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 A[1..N].

- **출력**: 두 줄 — 전위 순회 결과, 후위 순회 결과(공백 구분).

- **예제**:

  - `6 / 1 2 3 4 5 6` → `1 2 4 5 3 6` / `4 5 2 6 3 1`  (1의 자식 2,3; 2의 자식 4,5; 3의 왼쪽 자식 6)

  - `3 / 9 8 7` → `9 8 7` / `8 7 9`

- **셀프체크**: 재귀 기저를 "인덱스가 N을 넘으면 반환"으로 두었는가(자식 배열 없이 인덱스 공식만으로 순회). 전위는 진입 시, 후위는 두 자식을 마친 뒤 append했는가. N=1이면 두 줄 모두 값 하나인가. 완전 이진 트리라 재귀 깊이는 log2(N) 수준임을 알고 있는가.

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
n = int(data[0])
a = [0] + [int(x) for x in data[1:1 + n]]   # 1-based

pre, post = [], []

def dfs(i):
    if i > n:              # 자식 인덱스가 N을 넘으면 없음
        return
    pre.append(a[i])       # 전위: 진입 시
    dfs(2 * i)
    dfs(2 * i + 1)
    post.append(a[i])      # 후위: 두 자식을 마친 뒤

dfs(1)
print(' '.join(map(str, pre)))
print(' '.join(map(str, post)))
@@TESTS
--IN
6
1 2 3 4 5 6
--OUT
1 2 4 5 3 6
4 5 2 6 3 1
--IN
3
9 8 7
--OUT
9 8 7
8 7 9
--IN
1
7
--OUT
7
7
--IN
4
10 20 30 40
--OUT
10 20 40 30
40 20 30 10
@@EXPL
(1) 접근·핵심 아이디어

- 완전 이진 트리는 자식 배열을 따로 만들 필요 없이 인덱스 공식(2i, 2i+1)만으로 내려갈 수 있다. 순회 뼈대는 L3과 같고, 기저가 `v == 0` 대신 `i > n`으로 바뀔 뿐이다. 각 노드를 한 번 방문하므로 O(N).

(2) 코드 단계별

- 값 배열을 앞에 0을 하나 붙여 1-based로 맞춘다.
- `dfs(i)`: `i > n`이면 반환, 전위 리스트에 `a[i]` 추가, `dfs(2i)`, `dfs(2i+1)`, 후위 리스트에 `a[i]` 추가.
- `dfs(1)` 후 두 리스트를 각각 한 줄로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "배열 표현"이면 자식은 계산으로 얻는다 — 1-based 공식 `2i`/`2i+1`(0-based `2i+1`/`2i+2`와 혼동 금지).
- 전위/후위의 append 위치만 다르다는 L3 원칙 그대로.
- 마지막 레벨이 덜 찬 경우(`N=6`, 3의 오른쪽 자식 7 없음)에도 `i > n` 기저가 자연스럽게 처리하는지 검산.
```

**3) BST의 최솟값·최댓값·높이** · Easy

- **요구사항**: 서로 다른 정수를 주어진 순서대로 빈 BST에 삽입한 뒤, 트리의 최솟값·최댓값·높이(간선 기준)를 구하라.

- **입력**: 첫 줄 N(1 ≤ N ≤ 500), 둘째 줄 정수 N개(삽입 순서).

- **출력**: 최솟값 최댓값 높이를 공백으로 구분해 한 줄.

- **예제**:

  - `5 / 4 2 6 1 3` → `1 6 2`  (4 아래 2·6, 2 아래 1·3 → 높이 2)

  - `4 / 1 2 3 4` → `1 4 3`  (오름차순 삽입 → 오른쪽 사슬, 높이 3)

- **셀프체크**: 최솟값은 루트에서 왼쪽으로만, 최댓값은 오른쪽으로만 끝까지 내려가 구했는가. 높이를 "삽입할 때 내려간 깊이의 최댓값"으로 잡았는가(새 노드는 항상 리프에 붙고 기존 노드의 깊이는 변하지 않음). N=1이면 높이 0인가. 같은 값 집합이라도 삽입 순서에 따라 높이가 달라짐을 이해했는가.

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
n = int(data[0])
nums = [int(data[1 + i]) for i in range(n)]

left = {}
right = {}
root = nums[0]
left[root] = None; right[root] = None
height = 0
for x in nums[1:]:
    cur = root
    d = 0
    while True:
        d += 1                       # 한 칸 내려감
        if x < cur:
            if left[cur] is None:
                left[cur] = x; left[x] = None; right[x] = None; break
            cur = left[cur]
        else:
            if right[cur] is None:
                right[cur] = x; left[x] = None; right[x] = None; break
            cur = right[cur]
    if d > height:
        height = d                   # 새 리프의 깊이가 곧 높이 후보

mn = root
while left[mn] is not None:
    mn = left[mn]
mx = root
while right[mx] is not None:
    mx = right[mx]
print(mn, mx, height)
@@TESTS
--IN
5
4 2 6 1 3
--OUT
1 6 2
--IN
4
1 2 3 4
--OUT
1 4 3
--IN
1
10
--OUT
10 10 0
--IN
6
50 30 70 20 40 60
--OUT
20 70 2
@@EXPL
(1) 접근·핵심 아이디어

- BST에서 최솟값은 "왼쪽으로만" 내려간 끝, 최댓값은 "오른쪽으로만" 내려간 끝이다. 높이는 별도 재귀 없이도 구할 수 있다: 새 노드는 항상 리프로 붙고 기존 노드의 깊이는 변하지 않으므로, 삽입하며 내려간 칸 수의 최댓값이 곧 트리 높이다. 삽입 N번 × O(높이).

(2) 코드 단계별

- 첫 값을 루트로 두고, 나머지는 L4와 같은 while 하강으로 빈 자리에 단다. 내려갈 때마다 `d`를 1씩 올려 삽입 깊이를 세고 `height`를 갱신한다.
- `mn`: 루트에서 `left`가 None이 될 때까지 왼쪽으로. `mx`: 오른쪽으로.
- 세 값을 한 줄로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "BST 최소/최대 = 한쪽 끝"이라는 성질을 먼저 떠올린다.
- 높이를 재귀로 다시 계산해도 되지만, "삽입 깊이 최댓값"이 더 짧고 같은 답임을 이해한다.
- 정렬 순 삽입(`1 2 3 4`)이 사슬이 되어 높이 N−1이 되는 최악 경우를 확인. N=1은 루프에 들어가지 않아 높이 0.
```

**4) 최소 힙 삽입 후 배열 상태** · Easy

- **요구사항**: 빈 배열(0-based)로 표현한 최소 힙에 정수를 순서대로 삽입하라. 삽입 규칙: 배열 끝에 붙인 뒤, "부모 값이 새 값보다 클 동안" 부모와 자리를 바꾸며 올라간다(같으면 멈춤). 모든 삽입이 끝난 배열을 출력하라. `heapq`를 쓰지 말고 직접 구현한다.

- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 정수 N개(중복 가능).

- **출력**: 최종 배열을 인덱스 0부터 공백으로 구분해 한 줄.

- **예제**:

  - `5 / 5 3 8 1 4` → `1 3 8 5 4`
    - 검산: `[5]` → `[3,5]` → `[3,5,8]` → 1 삽입 `[3,5,8,1]` → 부모(5)와 교환 `[3,1,8,5]` → 부모(3)와 교환 `[1,3,8,5]` → 4 삽입 `[1,3,8,5,4]`, 부모 3 ≤ 4라 멈춤

  - `4 / 9 7 5 3` → `3 5 7 9`

- **셀프체크**: 부모 인덱스를 `(j-1)//2`(0-based)로 썼는가(1-based 공식 `i//2`와 혼동 금지). 교환 조건이 `heap[p] > heap[j]`(엄격)라 같은 값끼리는 교환하지 않는가(`2 2 2` → `2 2 2`). j가 0(루트)에 도달하면 멈추는가.

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
n = int(data[0])
heap = []
for i in range(n):
    x = int(data[1 + i])
    heap.append(x)                 # 끝에 붙이고
    j = len(heap) - 1
    while j > 0:                   # 부모보다 작으면 올라간다 (sift-up)
        p = (j - 1) // 2
        if heap[p] > heap[j]:
            heap[p], heap[j] = heap[j], heap[p]
            j = p
        else:
            break
print(' '.join(map(str, heap)))
@@TESTS
--IN
5
5 3 8 1 4
--OUT
1 3 8 5 4
--IN
4
9 7 5 3
--OUT
3 5 7 9
--IN
3
2 2 2
--OUT
2 2 2
--IN
1
42
--OUT
42
@@EXPL
(1) 접근·핵심 아이디어

- 힙 삽입(sift-up)은 "끝에 붙이고 부모보다 작으면 부모와 바꾸며 올라가기"다. 완전 이진 트리를 배열로 두었으므로 부모는 `(j-1)//2` 한 줄로 찾는다. 한 번 올라갈 때마다 깊이가 1 줄어 삽입당 O(log N), 전체 O(N log N).

(2) 코드 단계별

- `heap.append(x)` 후 `j`를 마지막 인덱스로.
- `j > 0`인 동안 부모 `p`를 구해 `heap[p] > heap[j]`면 교환하고 `j = p`, 아니면 중단.
- 모든 삽입 후 배열을 그대로 출력.

(3) 스스로 다시 짤 때 생각 순서

- 0-based 부모 공식 `(j-1)//2`를 먼저 적어 두기(L5 개념표 참고).
- 비교를 엄격(`>`)으로 두어야 같은 값이 불필요하게 자리를 바꾸지 않아 답이 유일해진다.
- 내림차순 입력(`9 7 5 3`)은 매번 루트까지 올라가는 최악 경우 — 손으로 한 번 따라가 보기.
```

**5) 후위+중위로 전위 복원** · Medium

- **요구사항**: 어떤 이진 트리의 후위 순회와 중위 순회(노드 값은 서로 다른 정수)가 주어진다. 그 트리의 전위 순회를 출력하라.

- **입력**: 첫 줄 N(1 ≤ N ≤ 500), 둘째 줄 후위 수열, 셋째 줄 중위 수열.

- **출력**: 전위 순회 결과(공백 구분).

- **예제**:

  - `5 / 4 5 2 3 1 / 4 2 5 1 3` → `1 2 4 5 3`
    - 검산: 후위 마지막 1=루트. 중위에서 1의 왼쪽 `{4,2,5}`(3개)·오른쪽 `{3}`. 후위 앞 3개 `4 5 2`가 왼 서브트리(루트 2) → 전위 `2 4 5`. 전체 전위 = 1 + (2 4 5) + (3)

  - `4 / 1 2 3 4 / 1 2 3 4` → `4 3 2 1`  (왼쪽 사슬)

- **셀프체크**: 후위의 "마지막" 원소가 루트임을 썼는가(전위는 첫 원소). 왼 서브트리 크기 `mid - in_lo`로 후위 구간도 함께 잘랐는가(후위 구간 `[pl, pl+ls-1]`이 왼쪽, `[pl+ls, pr-1]`이 오른쪽). 값→중위 인덱스 dict로 분할 위치를 O(1)에 찾았는가. N=1이면 그 값 하나인가.

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
n = int(data[0])
post = [int(data[1 + i]) for i in range(n)]
ino = [int(data[1 + n + i]) for i in range(n)]

pos = {v: i for i, v in enumerate(ino)}   # 값 → 중위 인덱스
pre = []

def build(il, ir, pl, pr):
    # 중위 구간 [il, ir], 후위 구간 [pl, pr] 은 같은 서브트리
    if il > ir:
        return
    root = post[pr]                 # 후위의 마지막 = 루트
    pre.append(root)                # 전위: 루트 먼저
    mid = pos[root]
    ls = mid - il                   # 왼 서브트리 크기
    build(il, mid - 1, pl, pl + ls - 1)
    build(mid + 1, ir, pl + ls, pr - 1)

build(0, n - 1, 0, n - 1)
print(' '.join(map(str, pre)))
@@TESTS
--IN
5
4 5 2 3 1
4 2 5 1 3
--OUT
1 2 4 5 3
--IN
4
1 2 3 4
1 2 3 4
--OUT
4 3 2 1
--IN
3
2 3 1
2 1 3
--OUT
1 2 3
--IN
1
7
7
--OUT
7
@@EXPL
(1) 접근·핵심 아이디어

- 후위 순회는 "왼 → 오 → 루트"이므로 구간의 마지막 원소가 루트다. 중위에서 그 루트 위치로 좌/우를 나누면, 왼 서브트리 크기 `ls`만큼이 후위 구간 앞쪽, 나머지가 오른쪽이다. 중위·후위 구간을 쌍으로 넘기는 재귀로 전위(루트 → 왼 → 오)를 바로 만든다. dict로 위치를 찾으면 O(N).

(2) 코드 단계별

- `pos`로 값→중위 인덱스를 미리 만든다.
- `build(il, ir, pl, pr)`: 비었으면 반환. `root = post[pr]`를 전위에 추가, `mid = pos[root]`, `ls = mid - il`.
- 왼쪽: 중위 `[il, mid-1]`, 후위 `[pl, pl+ls-1]`. 오른쪽: 중위 `[mid+1, ir]`, 후위 `[pl+ls, pr-1]`.
- 왼쪽 → 오른쪽 순으로 재귀하면 append 순서가 전위가 된다.

(3) 스스로 다시 짤 때 생각 순서

- L3의 "전위+중위 → 후위"와 대칭: 이번엔 루트가 후위의 끝, 그리고 출력이 전위라 루트를 진입 시 append.
- 후위를 포인터 하나로 뒤에서 소비하면 오른쪽을 먼저 재귀해야 해서 전위 순서가 꼬인다 — 구간 쌍으로 넘기면 왼쪽 먼저 재귀가 가능해 이 함정을 피한다.
- 사슬(`4 3 2 1`)과 N=1로 구간 계산(`pl+ls-1`)이 어긋나지 않는지 검산.
```

**6) 루트에서 리프까지 경로 합 최댓값** · Medium

- **요구사항**: 부모 배열과 각 노드의 값(음수 가능)이 주어진 트리에서, 루트에서 어떤 리프까지 내려가는 경로 위 값들의 합이 최대가 되는 값을 구하라. 경로의 끝은 반드시 리프여야 한다.

- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 `parent[0..N-1]`(루트 -1), 셋째 줄 값 `V[0..N-1]`(−1000 ≤ V ≤ 1000).

- **출력**: 최대 경로 합.

- **예제**:

  - `5 / -1 0 0 1 1 / 1 2 3 -4 5` → `8`  (경로 0→1→4: 1+2+5=8; 0→2: 4; 0→1→3: −1)

  - `3 / -1 0 1 / 5 -2 -3` → `0`  (리프는 2뿐이라 경로 합 5−2−3=0. 루트 값 5가 더 크지만 리프가 아니므로 답이 아님)

- **셀프체크**: 누적합을 "내려가며" `path[c] = path[v] + V[c]`로 전달했는가. 최댓값 갱신을 리프에서만 했는가(음수가 있으면 내부 노드 합이 더 클 수 있음). 값이 모두 음수여도 답이 나오도록 초깃값을 0이 아니라 `None`(또는 매우 작은 수)으로 두었는가(`1 / -1 / -7` → `-7`). 루트가 0번이 아닐 수도 있는가.

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
n = int(data[0])
parent = [int(data[1 + i]) for i in range(n)]
val = [int(data[1 + n + i]) for i in range(n)]

children = [[] for _ in range(n)]
root = -1
for v in range(n):
    if parent[v] == -1:
        root = v
    else:
        children[parent[v]].append(v)

path = [0] * n                 # path[v] = 루트에서 v까지 값 합
path[root] = val[root]
best = None
stack = [root]
while stack:
    v = stack.pop()
    if not children[v]:        # 리프에서만 답 후보
        if best is None or path[v] > best:
            best = path[v]
    for c in children[v]:
        path[c] = path[v] + val[c]    # 내려가며 누적
        stack.append(c)
print(best)
@@TESTS
--IN
5
-1 0 0 1 1
1 2 3 -4 5
--OUT
8
--IN
3
-1 0 1
5 -2 -3
--OUT
0
--IN
1
-1
-7
--OUT
-7
--IN
3
2 2 -1
4 -9 1
--OUT
5
@@EXPL
(1) 접근·핵심 아이디어

- 깊이처럼 "내려가며 계산"하는 값이다. 루트의 경로 합은 자기 값, 자식의 경로 합은 부모 경로 합 + 자기 값. 이렇게 모든 노드의 경로 합을 한 번에 채우고, 리프의 경로 합 중 최댓값을 고른다. 노드마다 한 번씩 보므로 O(N). 재귀 대신 명시적 스택 DFS를 써서 깊은 사슬에도 안전하다.

(2) 코드 단계별

- 부모 배열을 자식 리스트로 바꾸고 루트를 찾는다(L1 패턴).
- `path[root] = val[root]`로 시작해 스택 DFS: 꺼낸 노드가 리프면 `best` 갱신, 자식마다 `path[c] = path[v] + val[c]` 후 push.
- `best`를 출력.

(3) 스스로 다시 짤 때 생각 순서

- "루트에서 내려오는 경로" → 내려가며 누적(깊이와 같은 방향). 서브트리 크기처럼 올라오며 합치는 게 아님을 구분.
- 리프 판정은 자식 리스트가 빈 것으로. 내부 노드 합을 답에 넣으면 두 번째 예제가 5로 틀린다.
- `best` 초깃값을 0으로 두면 전부 음수인 경우(-7)에 0이 나오는 함정 — `None`으로 시작.
```

**7) 좌우 대칭 이진 트리 판정** · Medium

- **요구사항**: 이진 트리가 루트를 기준으로 좌우 거울처럼 대칭인지 판정하라. 대칭이란 왼쪽 서브트리와 오른쪽 서브트리가 모양도 값도 서로 거울상이라는 뜻이다.

- **입력**: 첫 줄 N(1 ≤ N ≤ 500, 루트 1). 둘째 줄 노드 값 V[1..N]. 이후 N줄, i번째 줄 `left_i right_i`(없으면 0).

- **출력**: 대칭이면 `YES`, 아니면 `NO`.

- **예제**:

  - `7 / 1 2 2 3 4 4 3 / 2 3 / 4 5 / 6 7 / 0 0 / 0 0 / 0 0 / 0 0` → `YES`  (2(3,4)와 2(4,3)이 거울상)

  - `4 / 1 2 2 5 / 2 3 / 4 0 / 0 0 / 0 0` → `NO`  (왼쪽 2에는 왼쪽 자식 5가 있는데 오른쪽 2에는 오른쪽 자식이 없음)

- **셀프체크**: 노드 하나가 아니라 "두 노드 (a, b)"를 함께 재귀했는가 — a의 왼쪽은 b의 오른쪽과, a의 오른쪽은 b의 왼쪽과 짝지었는가. 둘 다 0이면 True, 하나만 0이면 False, 값이 다르면 False 순으로 기저를 두었는가. 값은 같지만 배치가 거울상이 아닌 경우(`3 4 / 3 4`)를 걸렀는가. N=1이면 YES인가.

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
idx = 0
n = int(data[idx]); idx += 1
val = [0] * (n + 1)
for i in range(1, n + 1):
    val[i] = int(data[idx]); idx += 1
left = [0] * (n + 1)
right = [0] * (n + 1)
for i in range(1, n + 1):
    left[i] = int(data[idx]); right[i] = int(data[idx + 1]); idx += 2

def mirror(a, b):
    if a == 0 and b == 0:
        return True
    if a == 0 or b == 0:          # 한쪽만 비면 모양이 다름
        return False
    if val[a] != val[b]:
        return False
    return mirror(left[a], right[b]) and mirror(right[a], left[b])

print("YES" if mirror(left[1], right[1]) else "NO")
@@TESTS
--IN
7
1 2 2 3 4 4 3
2 3
4 5
6 7
0 0
0 0
0 0
0 0
--OUT
YES
--IN
4
1 2 2 5
2 3
4 0
0 0
0 0
--OUT
NO
--IN
7
1 2 2 3 4 3 4
2 3
4 5
6 7
0 0
0 0
0 0
0 0
--OUT
NO
--IN
1
5
0 0
--OUT
YES
@@EXPL
(1) 접근·핵심 아이디어

- 대칭은 "왼 서브트리와 오른 서브트리가 서로 거울"이라는 뜻이므로, 노드 하나를 재귀하는 대신 노드 쌍 (a, b)를 재귀한다. a의 왼쪽 ↔ b의 오른쪽, a의 오른쪽 ↔ b의 왼쪽을 짝지어 내려가며 모양(둘 다 없음/하나만 없음)과 값을 비교한다. 각 노드가 한 번씩 짝지어지므로 O(N).

(2) 코드 단계별

- 값·자식 배열을 1-based로 읽는다.
- `mirror(a, b)`: 둘 다 0 → True, 하나만 0 → False, 값 다름 → False, 아니면 교차 재귀 두 개의 and.
- 루트의 왼쪽·오른쪽 자식 쌍으로 시작해 결과를 출력.

(3) 스스로 다시 짤 때 생각 순서

- "두 트리가 같은가" 유형의 변형 — 비교 대상을 교차(left↔right)시키는 것만 다르다.
- 기저 순서(둘 다 없음 → 하나만 없음 → 값 비교)를 지켜야 `val[0]` 같은 잘못된 접근이 없다.
- 값 배열이 좌우 대칭처럼 보여도(`3 4 3 4`) 배치가 거울이 아니면 NO — 값만 비교하면 안 되는 이유.
```

**8) k개 정렬 목록 합치기** · Medium

- **요구사항**: 오름차순으로 정렬된 목록 K개를 하나의 오름차순 목록으로 합쳐라. 힙에는 "각 목록의 현재 맨 앞 값"만 두어 매번 최솟값을 O(log K)에 뽑는다.

- **입력**: 첫 줄 K(1 ≤ K ≤ 100). 이후 K줄, 각 줄 첫 수는 목록 길이 L_i(0 ≤ L_i ≤ 100), 이어서 L_i개의 정수(오름차순). 총 원소 ≤ 5000.

- **출력**: 합친 결과를 공백으로 구분해 한 줄. 원소가 하나도 없으면 `EMPTY`.

- **예제**:

  - `3 / 3 1 4 9 / 2 2 8 / 1 5` → `1 2 4 5 8 9`

  - `2 / 0 / 2 3 3` → `3 3`  (빈 목록이 섞여 있음)

- **셀프체크**: 힙에 `(값, 목록 번호, 위치)` 튜플을 넣어 어느 목록에서 왔는지 알 수 있게 했는가. 하나를 꺼낼 때마다 같은 목록의 다음 원소를 넣었는가(끝이면 넣지 않음). 길이 0인 목록을 처음에 힙에 넣지 않도록 방어했는가. 값이 같을 때 튜플의 두 번째 원소(정수)로 비교되어 오류가 없는가. 전부 빈 목록이면 `EMPTY`인가.

```runner
@@SOLUTION
import sys
import heapq
data = sys.stdin.read().split()
idx = 0
k = int(data[idx]); idx += 1
lists = []
for _ in range(k):
    L = int(data[idx]); idx += 1
    lists.append([int(data[idx + j]) for j in range(L)]); idx += L

h = []
for i in range(k):
    if lists[i]:                              # 빈 목록은 넣지 않음
        heapq.heappush(h, (lists[i][0], i, 0))   # (값, 목록 번호, 위치)
out = []
while h:
    v, i, j = heapq.heappop(h)
    out.append(str(v))
    if j + 1 < len(lists[i]):                 # 같은 목록의 다음 원소
        heapq.heappush(h, (lists[i][j + 1], i, j + 1))
print(' '.join(out) if out else "EMPTY")
@@TESTS
--IN
3
3 1 4 9
2 2 8
1 5
--OUT
1 2 4 5 8 9
--IN
2
0
2 3 3
--OUT
3 3
--IN
1
0
--OUT
EMPTY
--IN
2
2 1 1
2 1 1
--OUT
1 1 1 1
@@EXPL
(1) 접근·핵심 아이디어

- 목록이 각각 정렬돼 있으므로 "전체 최솟값"은 반드시 어떤 목록의 맨 앞에 있다. 각 목록의 맨 앞 하나씩만 힙에 넣어 두고, 최솟값을 꺼낼 때마다 그 목록의 다음 원소를 넣으면 힙 크기가 K를 넘지 않는다. 원소 총 수 M에 대해 O(M log K).

(2) 코드 단계별

- 목록을 읽어 `lists`에 담고, 비어 있지 않은 목록의 첫 원소를 `(값, i, 0)`으로 push.
- 힙이 빌 때까지 pop → 출력 목록에 추가 → `j+1`이 범위 안이면 `(lists[i][j+1], i, j+1)` push.
- 결과가 없으면 `EMPTY`.

(3) 스스로 다시 짤 때 생각 순서

- "정렬된 것 여러 개 합치기" → 각각의 앞 원소만 경쟁시키는 힙.
- 튜플에 목록 번호·위치를 넣어야 다음 원소를 찾을 수 있고, 값이 같아도 정수끼리 비교되어 오류가 없다(L5 개념의 동점 주의).
- 빈 목록·전부 빈 경우·전부 같은 값을 경계값으로 검산.
```

**9) 묶음 합치기 최소 비용** · Medium

- **요구사항**: 크기가 각각 s_i인 묶음 N개가 있다. 두 묶음을 하나로 합치는 비용은 두 크기의 합이고, 합친 묶음의 크기도 그 합이다. 모든 묶음이 하나가 될 때까지 합칠 때 드는 총 비용의 최솟값을 구하라.

- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 s_1..s_N(1 ≤ s_i ≤ 1000).

- **출력**: 최소 총 비용. N=1이면 0.

- **예제**:

  - `3 / 10 20 40` → `100`  (10+20=30, 30+40=70 → 30+70=100. 40+20을 먼저 하면 60+70=130으로 손해)

  - `4 / 1 1 1 1` → `8`  (2, 2, 4 → 2+2+4=8)

- **셀프체크**: 매번 "가장 작은 두 개"를 골라 합쳤는가(먼저 합친 묶음은 뒤에서 계속 다시 더해지므로 작은 것부터). 합친 결과를 힙에 다시 넣었는가. `heapify`로 한 번에 힙을 만들었는가. N=1이면 루프에 안 들어가 0인가. N=2면 두 수의 합인가.

```runner
@@SOLUTION
import sys
import heapq
data = sys.stdin.read().split()
n = int(data[0])
h = [int(data[1 + i]) for i in range(n)]
heapq.heapify(h)
cost = 0
while len(h) > 1:
    a = heapq.heappop(h)        # 가장 작은 둘을
    b = heapq.heappop(h)
    cost += a + b               # 합치고
    heapq.heappush(h, a + b)    # 합친 묶음을 다시 넣는다
print(cost)
@@TESTS
--IN
3
10 20 40
--OUT
100
--IN
4
1 1 1 1
--OUT
8
--IN
1
5
--OUT
0
--IN
2
3 4
--OUT
7
@@EXPL
(1) 접근·핵심 아이디어

- 일찍 합쳐진 묶음은 이후 합칠 때마다 비용에 다시 포함된다. 그러므로 큰 묶음은 가능한 한 늦게, 작은 묶음은 먼저 합쳐야 총 비용이 최소가 된다. "현재 가장 작은 두 개"를 반복해서 꺼내려면 최소 힙이 딱 맞다. N−1번의 pop·pop·push로 O(N log N).

(2) 코드 단계별

- 크기 배열을 `heapify`로 O(N)에 힙으로 만든다.
- 힙에 2개 이상 남은 동안: 두 번 pop해 합을 비용에 더하고, 합을 다시 push.
- 누적 비용 출력.

(3) 스스로 다시 짤 때 생각 순서

- "합친 결과가 다시 후보가 된다" → 정렬 한 번으로는 부족하고 힙이 필요한 이유.
- 반례(`40+20` 먼저 → 130)로 "작은 것부터"가 왜 옳은지 확인.
- N=1은 루프 자체가 돌지 않아 0, N=2는 단 한 번 합침.
```

**10) BST 삭제 후 순회** · Hard

- **요구사항**: 서로 다른 정수 N개를 순서대로 BST에 삽입한 뒤, M개의 값을 순서대로 삭제하라(삭제할 값은 그 시점에 반드시 트리에 있고, 서로 다르다). 삭제 규칙: 자식이 없으면 그냥 제거, 하나면 그 자식으로 대체, 둘이면 오른쪽 서브트리의 최솟값(후계자)을 그 자리의 값으로 복사한 뒤 후계자 노드를 오른쪽 서브트리에서 삭제한다. 삭제가 끝난 트리의 전위·중위 순회를 출력하라.

- **입력**: 첫 줄 N M(1 ≤ M ≤ N ≤ 500), 둘째 줄 삽입 값 N개, 셋째 줄 삭제 값 M개.

- **출력**: 두 줄 — 전위 순회, 중위 순회(공백 구분). 트리가 비면 `EMPTY` 한 줄.

- **예제**:

  - `7 1 / 5 3 8 2 4 7 9 / 5` → `7 3 2 4 8 9` / `2 3 4 7 8 9`  (루트 5의 후계자 7을 루트로 복사, 리프 7 제거)

  - `7 2 / 5 3 8 2 4 7 9 / 2 8` → `5 3 4 9 7` / `3 4 5 7 9`  (2는 리프 제거; 8은 후계자 9로 대체)

- **셀프체크**: 삭제 함수가 "새 서브트리 루트"를 반환해 부모의 L/R에 다시 연결하는 구조인가(루트 자체가 삭제될 때도 `root = delete(root, x)`로 처리). 자식 둘인 경우 후계자를 "오른쪽으로 한 번, 그다음 왼쪽으로 끝까지"로 찾았는가. 후계자 값을 복사한 뒤 후계자를 오른쪽 서브트리에서 재귀 삭제했는가(후계자는 왼쪽 자식이 없어 0·1개 경우로 끝남). 값을 dict 키로 쓰면 "값 복사"가 곤란하니 노드 번호 배열(`val/L/R`)로 구현했는가. 전부 삭제되면 `EMPTY`인가. 중위 순회는 삭제 후에도 오름차순인가(BST 성질 검산).

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
idx = 0
n = int(data[idx]); m = int(data[idx + 1]); idx += 2
nums = [int(data[idx + i]) for i in range(n)]; idx += n
dels = [int(data[idx + i]) for i in range(m)]; idx += m

val, L, R = [], [], []           # 노드 번호 기반 저장

def new_node(x):
    val.append(x); L.append(-1); R.append(-1)
    return len(val) - 1

root = -1
for x in nums:
    if root == -1:
        root = new_node(x)
        continue
    cur = root
    while True:
        if x < val[cur]:
            if L[cur] == -1:
                L[cur] = new_node(x); break
            cur = L[cur]
        else:
            if R[cur] == -1:
                R[cur] = new_node(x); break
            cur = R[cur]

def delete(node, x):
    # x를 지운 뒤 이 서브트리의 새 루트를 반환
    if node == -1:
        return -1
    if x < val[node]:
        L[node] = delete(L[node], x)
    elif x > val[node]:
        R[node] = delete(R[node], x)
    else:
        if L[node] == -1:          # 자식 0개 또는 오른쪽만
            return R[node]
        if R[node] == -1:          # 왼쪽만
            return L[node]
        s = R[node]                # 자식 2개: 후계자(오른쪽 서브트리 최솟값)
        while L[s] != -1:
            s = L[s]
        val[node] = val[s]
        R[node] = delete(R[node], val[s])
    return node

for x in dels:
    root = delete(root, x)

pre, ino = [], []

def dfs(v):
    if v == -1:
        return
    pre.append(val[v])
    dfs(L[v])
    ino.append(val[v])
    dfs(R[v])

if root == -1:
    print("EMPTY")
else:
    dfs(root)
    print(' '.join(map(str, pre)))
    print(' '.join(map(str, ino)))
@@TESTS
--IN
7 1
5 3 8 2 4 7 9
5
--OUT
7 3 2 4 8 9
2 3 4 7 8 9
--IN
7 2
5 3 8 2 4 7 9
2 8
--OUT
5 3 4 9 7
3 4 5 7 9
--IN
3 3
2 1 3
2 1 3
--OUT
EMPTY
--IN
4 1
4 2 1 3
2
--OUT
4 3 1
1 3 4
@@EXPL
(1) 접근·핵심 아이디어

- BST 삭제는 세 경우로 나뉜다. 자식 0개·1개는 그 노드를 자식(또는 없음)으로 갈아 끼우면 끝이고, 자식 2개는 "오른쪽 서브트리의 최솟값(후계자)"이 BST 순서를 깨지 않고 그 자리에 올 수 있는 유일한 후보라 값을 복사한 뒤 후계자를 오른쪽에서 지운다. 후계자는 왼쪽 자식이 없으므로 그 삭제는 반드시 0·1개 경우로 끝난다. 각 삭제는 O(높이).

(2) 코드 단계별

- 값을 dict 키로 쓰지 않고 `val/L/R` 배열에 노드 번호로 저장한다 — "값 복사"가 필요하기 때문.
- 삽입은 L4와 같은 while 하강.
- `delete(node, x)`: x가 작으면 왼쪽, 크면 오른쪽으로 재귀하고 그 반환값을 자식 링크에 다시 대입. 찾으면 세 경우 처리 후 `node`(또는 대체 자식)를 반환.
- 모든 삭제 후 전위·중위를 한 DFS에서 만들어 출력, 루트가 -1이면 `EMPTY`.

(3) 스스로 다시 짤 때 생각 순서

- "재귀가 새 서브트리 루트를 반환"하는 구조를 먼저 잡으면 루트 삭제·자식 갈아 끼우기가 한 코드로 처리된다.
- 후계자 찾기는 "오른쪽 한 번, 그다음 왼쪽 끝까지"(왼쪽 서브트리 최댓값을 쓰는 방식도 있지만 문제가 후계자를 지정).
- 삭제 뒤 중위 순회가 여전히 오름차순인지가 가장 빠른 검산. 전부 삭제한 `EMPTY`와 루트 삭제 케이스를 꼭 돌려 볼 것.
```

**11) 배열 힙 직접 구현 — 삽입과 삭제** · Hard

- **요구사항**: 빈 배열(0-based) 최소 힙에 명령을 처리한다. `push x`: 끝에 붙인 뒤 부모가 더 클 동안 교환하며 올라간다. `pop`: 루트(최솟값)를 꺼내 출력하고, 마지막 원소를 루트로 옮긴 뒤 "두 자식 중 더 작은 쪽(같으면 왼쪽)이 현재 값보다 작은 동안" 그 자식과 교환하며 내려간다. 빈 힙에서 `pop`이면 `-1`을 출력. 모든 명령 뒤 배열 상태를 출력하라. `heapq`는 배열 배치가 이 규칙과 다를 수 있으므로 쓰지 않는다.

- **입력**: 첫 줄 Q(1 ≤ Q ≤ 1000), 이후 Q줄에 `push x`(−10^9 ≤ x ≤ 10^9) 또는 `pop`.

- **출력**: `pop`마다 결과를 한 줄씩, 마지막 줄에 최종 배열(인덱스 0부터 공백 구분; 비면 `EMPTY`).

- **예제**:

  - `7 / push 5 / push 3 / push 8 / push 1 / pop / pop / push 2` → `1` / `3` / `2 8 5`
    - 검산: 삽입 후 `[1,3,8,5]` → pop 1: 5를 루트로 `[5,3,8]`, 자식 3<5 교환 `[3,5,8]` → pop 3: `[8,5]` → `[5,8]` → push 2: `[5,8,2]` → 부모 5>2 교환 `[2,8,5]`

  - `2 / pop / push 4` → `-1` / `4`

- **셀프체크**: pop에서 마지막 원소를 먼저 떼어낸 뒤(`heap.pop()`) 힙이 비어 있지 않을 때만 루트에 덮어썼는가(원소 1개일 때 인덱스 오류 방지). sift-down에서 오른쪽 자식이 없을 수 있음을 `r < size`로 검사했는가. "더 작은 자식"을 고를 때 왼쪽을 먼저 후보로 두어 동점이면 왼쪽과 교환하는가. 비교가 엄격(`<`)이라 같은 값이면 멈추는가. 최종 배열이 힙 조건(부모 ≤ 자식)을 만족하는지 검산했는가.

```runner
@@SOLUTION
import sys
data = sys.stdin.read().split()
idx = 0
q = int(data[idx]); idx += 1
heap = []
out = []

def push(x):
    heap.append(x)
    j = len(heap) - 1
    while j > 0:                          # sift-up
        p = (j - 1) // 2
        if heap[p] > heap[j]:
            heap[p], heap[j] = heap[j], heap[p]
            j = p
        else:
            break

def pop():
    top = heap[0]
    last = heap.pop()                     # 마지막 원소를 떼어냄
    if heap:                              # 남은 게 있으면 루트에 덮고 내려간다
        heap[0] = last
        j = 0
        size = len(heap)
        while True:                       # sift-down
            l = 2 * j + 1
            r = 2 * j + 2
            small = j
            if l < size and heap[l] < heap[small]:
                small = l
            if r < size and heap[r] < heap[small]:
                small = r
            if small == j:
                break
            heap[j], heap[small] = heap[small], heap[j]
            j = small
    return top

for _ in range(q):
    cmd = data[idx]; idx += 1
    if cmd == 'push':
        push(int(data[idx])); idx += 1
    else:
        out.append(str(pop()) if heap else "-1")
out.append(' '.join(map(str, heap)) if heap else "EMPTY")
print('\n'.join(out))
@@TESTS
--IN
7
push 5
push 3
push 8
push 1
pop
pop
push 2
--OUT
1
3
2 8 5
--IN
2
pop
push 4
--OUT
-1
4
--IN
5
push 9
push 4
push 7
push 1
pop
--OUT
1
4 9 7
--IN
2
push 1
pop
--OUT
1
EMPTY
@@EXPL
(1) 접근·핵심 아이디어

- 힙의 두 기본 연산을 배열 위에서 직접 구현한다. push는 문제 4의 sift-up 그대로, pop은 "루트를 꺼내고 마지막 원소를 루트로 올린 뒤, 더 작은 자식과 바꾸며 내려가기(sift-down)"다. 두 연산 모두 트리 높이만큼만 움직이므로 O(log N). 출력 배열이 규칙에 따라 유일하게 정해지므로, 같은 값을 넣어도 배열 배치가 다를 수 있는 `heapq`를 쓰면 안 된다.

(2) 코드 단계별

- `push(x)`: append 후 `(j-1)//2` 부모와 비교·교환.
- `pop()`: `top = heap[0]`를 보관하고 `last = heap.pop()`. 힙이 남아 있으면 `heap[0] = last` 후 sift-down — 왼쪽 자식을 먼저 후보로, 오른쪽이 더 작을 때만 후보 교체, 후보가 자기 자신이면 종료.
- 명령을 토큰으로 읽어 `push`/`pop` 분기. `pop`은 빈 힙이면 `-1`.
- 마지막에 배열 상태 한 줄(비면 `EMPTY`).

(3) 스스로 다시 짤 때 생각 순서

- 0-based 인덱스 공식(부모 `(j-1)//2`, 자식 `2j+1`·`2j+2`)을 먼저 적는다.
- pop에서 "마지막 원소 떼기 → 비었는지 검사 → 루트 덮기" 순서가 원소 1개일 때의 오류를 막는다.
- 자식이 하나(오른쪽 없음)인 경우와 동점 시 왼쪽 우선 규칙을 `5 / push 9 4 7 1 / pop`(`4 9 7`)로 검산. 마지막 배열이 힙 조건을 만족하는지 눈으로 확인.
```

**12) 트리의 지름** · Hard

- **요구사항**: 노드 1..N과 가중치가 있는 간선 N−1개(방향 없음)로 주어진 트리에서, 두 노드 사이 거리(경로 위 가중치 합)의 최댓값(지름)을 구하라.

- **입력**: 첫 줄 N(1 ≤ N ≤ 1000). 이후 N−1줄에 `u v w`(1 ≤ w ≤ 100).

- **출력**: 지름.

- **예제**:

  - `5 / 1 2 3 / 1 3 2 / 3 4 5 / 3 5 1` → `10`  (2→1→3→4: 3+2+5)

  - `3 / 1 2 7 / 1 3 7` → `14`  (2→1→3)

- **셀프체크**: "아무 노드에서 가장 먼 노드 a를 찾고, a에서 가장 먼 거리"가 지름이라는 두 번 탐색 원리를 썼는가. BFS/DFS에서 거리 배열 `dist`를 -1로 초기화해 되돌아가기를 막았는가(방향 없는 간선). 가장 먼 노드가 여럿이라도 지름 값은 같은가. N=1이면 0인가. 모든 쌍을 다 재면 O(N²)인데 두 번 탐색은 O(N)임을 이해했는가.

```runner
@@SOLUTION
import sys
from collections import deque
data = sys.stdin.read().split()
idx = 0
n = int(data[idx]); idx += 1
adj = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
    adj[u].append((v, w))
    adj[v].append((u, w))

def farthest(start):
    # start에서 가장 먼 노드와 그 거리
    dist = [-1] * (n + 1)
    dist[start] = 0
    q = deque([start])
    far = start
    while q:
        v = q.popleft()
        if dist[v] > dist[far]:
            far = v
        for w, c in adj[v]:
            if dist[w] == -1:
                dist[w] = dist[v] + c
                q.append(w)
    return far, dist[far]

a, _ = farthest(1)        # 1번에서 가장 먼 노드 a
b, d = farthest(a)        # a에서 가장 먼 거리가 지름
print(d)
@@TESTS
--IN
5
1 2 3
1 3 2
3 4 5
3 5 1
--OUT
10
--IN
3
1 2 7
1 3 7
--OUT
14
--IN
1
--OUT
0
--IN
4
1 2 1
2 3 1
3 4 1
--OUT
3
@@EXPL
(1) 접근·핵심 아이디어

- 트리에서는 "임의의 노드에서 가장 먼 노드"가 항상 지름의 한쪽 끝이 된다. 그래서 1번에서 가장 먼 노드 a를 찾고, a에서 가장 먼 거리를 재면 그것이 지름이다. 모든 쌍을 재면 O(N²)이지만 이 방법은 탐색 두 번으로 O(N). 가중치가 있어도 트리는 경로가 유일하므로 BFS로 거리를 누적해도 된다.

(2) 코드 단계별

- 간선을 `(이웃, 가중치)`로 양쪽 인접 리스트에 넣는다.
- `farthest(start)`: `dist`를 -1로 초기화하고 BFS로 `dist[w] = dist[v] + c`를 채우며, 거리가 가장 큰 노드 `far`를 추적해 `(far, dist[far])` 반환.
- `farthest(1)`로 a를 얻고, `farthest(a)`의 거리를 출력.

(3) 스스로 다시 짤 때 생각 순서

- "가장 먼 두 노드" → 두 번 탐색 원리를 떠올린다(증명은 몰라도 결론은 외워 둘 것).
- 방향 없는 간선이므로 `dist == -1` 검사로 부모로 되돌아가지 않게 한다.
- N=1(간선 없음, 0)과 사슬(`3`)로 경계값 검산. 가장 먼 노드가 여럿이면 어느 것을 골라도 지름 값은 같다.
```
