## L5. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터는 도구 하나와 그 도구로 만든 알고리즘 둘로 되어 있다. **유니온-파인드**는 "이 둘이 이미 이어져 있나"를 거의 상수 시간에 답하는 부품이고, **크루스칼**은 그 부품에 정렬을 얹은 것, **프림**은 같은 컷 성질을 정점 쪽에서 적용한 것이다. 셋의 관계와 갈림길을 아래 지도로 못 박는다.

**개념 지도**

```text
  Ch02 map : connectivity first, spanning tree second

  disjoint set (union-find)
   |    parent[] + rank[] (or size[])
   |    find  : walk up to the root, then compress the path
   |    union : hang the shorter root under the taller one
   |    cost  : O(alpha(V)) amortized -> treat it as O(1)
   |
   +-- used alone
   |     same group ?        find(a) == find(b)
   |     group count         V minus the number of successful unions
   |     cycle detection     union(a, b) returns False
   |     offline queries     process merges in the given order
   |
   +-- used inside Kruskal
         "does this edge join two different components ?"

  minimum spanning tree : V-1 edges, no cycle, minimum total weight
   |    cut property : the cheapest edge crossing any cut is safe
   |
   +-- Kruskal      edge driven    sort + union-find    O(E log E)
   |                  edge list given, sparse graph
   |
   +-- Prim (heap)  vertex driven  one growing tree     O(E log V)
   |                  adjacency list, sparse to medium
   |
   +-- Prim (array) vertex driven  scan keys, no heap   O(V^2)
                      dense or complete graph built from points
```

MST 뼈대는 하나인데, 비교 방향과 멈추는 시점만 바꾸면 다른 문제가 된다.

```text
  same loop, different twist

  minimum spanning tree     sort ascending, stop at V-1 edges
  maximum spanning tree     sort descending, everything else same
  k clusters                keep only the first V-k accepted edges
  edges already built       union them first (cost 0), then run
  bottleneck path u..v      the w that first connects u and v
  is edge e in some MST ?   compare against the path max in the MST
```

두 알고리즘의 진행 모양이 다르다는 점이 선택의 감각을 만든다.

```text
  Kruskal : many islands appear first, then they merge

     step 1    {0,1}   {2}   {3}   {4}
     step 2    {0,1,2}   {3}   {4}
     step 4    {0,1,2,3,4}

  Prim : never more than one island, it only grows

     step 1    [0]   (1) (2) (3) (4)
     step 2    [0]=[1]   (2) (3) (4)
     step 5    [0]=[1]=[2]=[3]=[4]

  Both obey the cut property, so the total weight is always equal.
```

**뼈대 코드**

1) 유니온-파인드 — 경로 압축 + union by rank

```python
import sys

n = int(sys.stdin.readline())              # ← 원소 개수는 문제마다 바뀜
parent = list(range(n + 1))                # ← 0-based면 list(range(n))
rank_ = [0] * (n + 1)
groups = n                                 # 남은 그룹 수

def find(x):
    root = x
    while parent[root] != root:            # 1단계: 뿌리까지 올라간다
        root = parent[root]
    while parent[x] != root:               # 2단계: 지나온 길을 뿌리에 직결
        parent[x], x = root, parent[x]     # 대입해야 압축이 실제로 남는다
    return root

def union(a, b):
    global groups
    ra, rb = find(a), find(b)              # 반드시 '뿌리끼리' 붙인다
    if ra == rb:
        return False                       # 이미 같은 그룹 -> 붙이면 사이클
    if rank_[ra] < rank_[rb]:              # 낮은 트리를 높은 트리 밑으로
        ra, rb = rb, ra
    parent[rb] = ra
    if rank_[ra] == rank_[rb]:             # 높이가 같을 때만 1 올라간다
        rank_[ra] += 1
    groups -= 1
    return True                            # 실제로 합쳐졌다
```

2) 크루스칼 — 정렬 + 유니온-파인드

```python
edges = []
for _ in range(m):                         # ← 간선 수·입력 형식은 문제마다 바뀜
    a, b, w = map(int, sys.stdin.readline().split())
    edges.append((w, a, b))                # 가중치를 앞에 두면 sort()만으로 끝
edges.sort()                               # ← 최대 신장 트리면 reverse=True

total, cnt, used = 0, 0, []
for w, a, b in edges:
    if union(a, b):                        # 다른 컴포넌트일 때만 True
        total += w
        cnt += 1
        used.append((a, b, w))             # ← MST 간선 목록이 필요할 때만
        if cnt == n - 1:                   # V-1개 모으면 더 볼 필요 없음
            break
print(total if cnt == n - 1 else -1)       # 못 채우면 비연결
```

3) 프림 — heapq 버전(희소~중간 밀도)

```python
import heapq

def prim_heap(n, adj, start=1):            # adj[u] = [(v, w), ...]
    visited = [False] * (n + 1)
    heap = [(0, start)]                    # 시작 정점 진입 비용은 0
    total, cnt = 0, 0
    while heap and cnt < n:
        w, u = heapq.heappop(heap)
        if visited[u]:                     # 지연 삭제: 꺼낸 직후에 검사한다
            continue
        visited[u] = True
        total += w
        cnt += 1
        for v, wv in adj[u]:
            if not visited[v]:
                heapq.heappush(heap, (wv, v))   # 키는 w (dist + w 가 아니다)
    return total if cnt == n else -1       # 다 못 넣으면 비연결
```

4) 프림 — O(V²) 배열 버전(밀집·완전 그래프)

```python
INF = float('inf')

def prim_dense(n, cost):                   # cost[u][v] = 가중치, 없으면 INF
    key = [INF] * n                        # 트리에 붙이는 최소 간선 비용
    used = [False] * n
    key[0] = 0                             # ← 시작 정점은 아무거나
    total = 0
    for _ in range(n):
        u = -1
        for i in range(n):                 # 안 쓴 것 중 key 최소를 선형 탐색
            if not used[i] and (u == -1 or key[i] < key[u]):
                u = i
        if key[u] == INF:
            return -1                      # 닿을 수 있는 정점이 없다 = 비연결
        used[u] = True
        total += key[u]
        for v in range(n):                 # 새 정점 기준으로 key 갱신
            if not used[v] and cost[u][v] < key[v]:
                key[v] = cost[u][v]
    return total                           # 힙도 정렬도 필요 없다
```

5) 최소 병목 경로 — s에서 t까지 "가장 큰 간선"을 최소화

```python
edges.sort()                               # 가중치 오름차순
answer = -1
for w, a, b in edges:
    union(a, b)
    if find(s) == find(t):                 # ← 질의 쌍 (s, t)는 문제마다 바뀜
        answer = w                         # 처음 이어지는 순간의 간선이 답
        break
print(answer)                              # s == t 는 루프 전에 0으로 처리
```

6) k개 군집 분할 · 최대 신장 트리

```python
# (1) k개 군집: MST 간선을 오름차순으로 모으되 앞에서 n-k개만 더한다
edges.sort()
picked, total = 0, 0
for w, a, b in edges:
    if union(a, b):
        picked += 1
        if picked <= n - k:                # ← 군집 수 k는 문제마다 바뀜
            total += w                     # 비싼 k-1개는 자동으로 잘린다
print(total if picked == n - 1 else -1)    # n-1개를 못 채우면 비연결

# (2) 최대 신장 트리: 정렬 방향만 뒤집는다
edges.sort(reverse=True)                   # 내림차순
# 이후 채택 루프는 크루스칼과 한 글자도 다르지 않다

# (3) 일부 간선이 이미 건설됨: 그것부터 union 하고 시작
for a, b in prebuilt:                      # ← 비용 0으로 미리 합친 셈
    union(a, b)
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 연결 여부·그룹 수만 묻는다(간선 추가만) | 유니온-파인드 단독 | 신장 트리를 만들 이유가 없다 | O(m·α(V)) |
| 간선을 넣다가 사이클이 되는 순간을 찾는다 | 유니온-파인드 단독 | `union`이 False를 돌려주는 시점 | O(m·α(V)) |
| "합쳐라 / 같은 그룹인가"가 섞여 들어온다 | 유니온-파인드 단독 | 온라인 질의를 그대로 처리 | 질의당 사실상 O(1) |
| 간선 목록이 주어진 희소 그래프의 MST | 크루스칼 | 정렬 한 번이면 끝, 코드가 가장 짧다 | O(E log E) |
| 간선이 이미 가중치순으로 들어온다 | 크루스칼(정렬 생략) | 지배항인 정렬이 사라진다 | O(E·α(V)) |
| 인접 리스트가 주어진 중간 밀도 그래프 | 힙 프림 | 간선 전부를 정렬하지 않아도 된다 | O(E log V) |
| 좌표 V개로 만든 완전 그래프(E ≈ V²) | 배열 프림 | 간선 나열·정렬 비용 O(V² log V)를 피한다 | O(V²) |
| V ≤ 약 1000인 인접 행렬 입력 | 배열 프림 | 힙 없이도 충분히 빠르고 구현이 단순 | O(V²) |
| 일부 도로가 이미 놓여 있다 | 미리 union 후 크루스칼 | 비용 0 간선을 먼저 채택한 것과 같다 | O(E log E) |
| 최대 신장 트리 | 내림차순 크루스칼 | 컷 성질이 부호를 뒤집어도 성립 | O(E log E) |
| s–t 경로의 최대 간선을 최소화 | 오름차순 크루스칼 | 처음 이어지는 순간의 w가 곧 답 | O(E log E) |
| 정확히 k개 군집으로 나눈다 | MST 간선 앞 V-k개 | 비싼 간선 k-1개를 끊는 것과 동치 | O(E log E) |
| 그래프가 연결인지 함께 판정 | 채택 간선 수 검사 | V-1개를 못 채우면 비연결 | 추가 비용 없음 |
| 간선 "삭제"가 섞여 있다 | 질의를 역순으로 처리 | 유니온-파인드는 분리를 지원하지 않는다 | O((E+Q)·α(V)) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 유니온-파인드가 각 그룹을 "대표원소를 뿌리로 하는 트리"로 표현한다는 것과, 그래서 `find`가 무엇을 반환하는지.
- [ ] 설명할 수 있다: 경로 압축이 왜 "비싼 탐색이 스스로를 없애는" 최적화인지.
- [ ] 설명할 수 있다: union by rank/size만으로도 트리 높이가 왜 `log2 V` 이하인지.
- [ ] 설명할 수 있다: 두 최적화를 합쳤을 때의 α(V)가 무슨 뜻이고 왜 상수로 취급해도 되는지.
- [ ] 설명할 수 있다: 왜 원소끼리가 아니라 반드시 뿌리끼리 붙여야 하는지.
- [ ] 설명할 수 있다: MST의 간선이 왜 항상 정확히 V-1개인지.
- [ ] 설명할 수 있다: 컷 성질을 교환 논증으로. 그리고 그것이 왜 크루스칼과 프림 양쪽의 정당성 근거인지.
- [ ] 설명할 수 있다: 크루스칼이 간선을 채택하는 순간이 왜 "어떤 컷의 최소 간선"인지.
- [ ] 설명할 수 있다: 프림의 힙 키가 `w`이고 다익스트라는 `dist[u] + w`인 이유, 그리고 바꿔 쓰면 무엇이 나오는지.
- [ ] 설명할 수 있다: 프림의 지연 삭제가 왜 정당하고, 검사를 꺼낸 직후에 해야 하는 이유.
- [ ] 설명할 수 있다: `E log V`와 `V²`를 비교해 크루스칼·힙 프림·배열 프림을 고르는 기준.
- [ ] 설명할 수 있다: 시작 정점을 바꿔도 프림의 총합이 변하지 않는 이유.
- [ ] 설명할 수 있다: 최소 병목 경로의 답이 왜 MST 위 경로의 최대 간선과 같은지.
- [ ] 설명할 수 있다: k개 군집 문제가 왜 "MST에서 비싼 간선 k-1개 끊기"로 환원되는지.
- [ ] 설명할 수 있다: 비연결 그래프를 어떻게 감지하고, 크루스칼과 프림에서 각각 어느 값으로 판정하는지.

**⚠️ 자주 하는 실수**

**1) `find`에서 경로 압축 결과를 대입하지 않는다**

```python
# ❌ 틀린 코드
def find(x):
    if parent[x] == x:
        return x
    find(parent[x])        # 결과를 어디에도 대입하지 않는다
    return parent[x]       # parent[x]는 압축 전 값 그대로
```

왜: 재귀가 뿌리를 찾아 돌아오지만 `parent[x]`를 갱신하지 않으므로 트리가 조금도 납작해지지 않는다. 게다가 `return parent[x]`는 뿌리가 아니라 "한 칸 위"를 돌려주므로, 깊이 2 이상에서는 대표원소 자체가 틀린다. `find(a) == find(b)` 판정이 무너져 사이클을 못 잡는다.

```python
# ✅ 고친 코드
def find(x):
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:
        parent[x], x = root, parent[x]   # 지나온 노드를 뿌리에 직결
    return root                          # 반복형이라 재귀 깊이 걱정도 없다
```

**2) 크루스칼에서 정렬을 빠뜨리거나 엉뚱한 키로 정렬한다**

```python
# ❌ 틀린 코드
edges = []
for _ in range(m):
    a, b, w = map(int, input().split())
    edges.append((a, b, w))    # 가중치가 세 번째
edges.sort()                   # a 기준, 그다음 b 기준으로 정렬된다
for a, b, w in edges:
    if union(a, b):
        total += w
```

왜: 튜플 정렬은 앞 원소부터 비교하므로 위 코드는 정점 번호 순으로 정렬한다. 사이클은 여전히 걸러지므로 **신장 트리는 나오지만 최소가 아니다.** 오류 메시지도 없고 작은 예제에서는 우연히 맞기도 해서, 답이 조금 큰 이유를 한참 못 찾는다.

```python
# ✅ 고친 코드
edges.append((w, a, b))        # 가중치를 맨 앞으로
edges.sort()                   # 이제 sort() 한 줄이 곧 가중치 오름차순
for w, a, b in edges:
    if union(a, b):
        total += w
# 순서를 바꾸기 싫다면 edges.sort(key=lambda e: e[2]) 로 키를 지정한다
```

**3) 채택 간선이 V-1개인지 확인하지 않는다**

```python
# ❌ 틀린 코드
total = 0
for w, a, b in edges:
    if union(a, b):
        total += w
print(total)               # 비연결 그래프에서도 태연히 숫자를 출력한다
```

왜: 그래프가 두 덩어리로 끊겨 있으면 채택 간선이 V-2개 이하에서 멈춘다. 그런데 위 코드는 "각 덩어리의 MST 합"을 더한 값을 출력한다. 신장 트리가 아예 존재하지 않는데 그럴듯한 수가 나오므로 틀렸다는 사실조차 드러나지 않는다.

```python
# ✅ 고친 코드
total, cnt = 0, 0
for w, a, b in edges:
    if union(a, b):
        total += w
        cnt += 1
        if cnt == n - 1:       # 다 모았으면 조기 종료까지 덤으로
            break
print(total if cnt == n - 1 else -1)   # ← 비연결 표기는 문제마다 바뀜
```

**4) union by rank/size 없이 한쪽으로만 붙인다**

```python
# ❌ 틀린 코드
def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False
    parent[rb] = ra            # 항상 b 쪽을 a 밑으로만 붙인다
    return True
```

왜: `union(1,2), union(2,3), union(3,4), ...`처럼 한 방향으로 들어오는 입력에서 트리가 한 줄로 늘어난다. 경로 압축이 있으면 대체로 버티지만, 압축까지 빠지면 `find` 한 번이 O(V)가 되어 간선 20만 개짜리 크루스칼이 시간 초과로 죽는다.

```python
# ✅ 고친 코드
def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False
    if rank_[ra] < rank_[rb]:  # 낮은 트리를 높은 트리 밑으로
        ra, rb = rb, ra
    parent[rb] = ra
    if rank_[ra] == rank_[rb]: # 높이가 같았을 때만 1 증가
        rank_[ra] += 1
    return True                # 높이가 log2 V 이하로 묶인다
```

**5) 무방향 간선을 인접 리스트에 한 방향만 넣는다**

```python
# ❌ 틀린 코드
adj = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b, w = map(int, input().split())
    adj[a].append((b, w))      # b 쪽에서는 이 간선이 보이지 않는다
```

왜: 프림은 "지금 트리에서 나가는 간선"만 힙에 넣는다. 간선이 한 방향만 등록되어 있으면, 트리가 `b`를 먼저 흡수했을 때 `a`로 돌아오는 길을 찾지 못한다. 결과적으로 도달 못 한 정점이 남아 `cnt < n`이 되고, 멀쩡히 연결된 그래프를 비연결로 판정한다.

```python
# ✅ 고친 코드
for _ in range(m):
    a, b, w = map(int, input().split())
    adj[a].append((b, w))
    adj[b].append((a, w))      # 무방향은 반드시 양쪽 등록
```

**6) 프림에서 방문 검사를 push 시점에만 한다**

```python
# ❌ 틀린 코드
while heap:
    w, u = heapq.heappop(heap)
    visited[u] = True          # 꺼낸 뒤 검사 없이 바로 편입
    total += w
    for v, wv in adj[u]:
        if not visited[v]:     # push 시점 검사만으로 충분하다고 착각
            heapq.heappush(heap, (wv, v))
```

왜: 정점 `v`가 힙에 여러 번 들어간 뒤 그중 하나가 꺼내져 트리에 편입되면, 힙에 남은 나머지 `v` 항목들은 push된 시점에는 미방문이었으므로 걸러지지 않았다. 그것들이 다시 꺼내지면 같은 정점의 비용이 총합에 중복으로 더해져 답이 커진다.

```python
# ✅ 고친 코드
while heap and cnt < n:
    w, u = heapq.heappop(heap)
    if visited[u]:             # 지연 삭제: 반드시 꺼낸 직후에 검사
        continue
    visited[u] = True
    total += w
    cnt += 1
    for v, wv in adj[u]:
        if not visited[v]:
            heapq.heappush(heap, (wv, v))
```

**7) 프림의 힙 키를 다익스트라처럼 누적 거리로 넣는다**

```python
# ❌ 틀린 코드
for v, wv in adj[u]:
    if not visited[v]:
        heapq.heappush(heap, (w + wv, v))   # 시작점부터의 누적 거리
```

왜: 그 코드는 MST가 아니라 최단 경로 트리를 만든다. 두 트리는 다른 것이고, 최단 경로 트리의 간선 합은 MST보다 크거나 같다. 별 모양 그래프처럼 시작점에서 모두 직결된 경우에는 우연히 일치해 통과하기도 해서 더 헷갈린다.

```python
# ✅ 고친 코드
for v, wv in adj[u]:
    if not visited[v]:
        heapq.heappush(heap, (wv, v))       # 트리에 붙이는 간선 하나만 본다
# 최소화 대상이 다르다: 다익스트라는 경로 합, 프림은 뽑은 간선들의 총합
```

**8) 뿌리가 아닌 원소끼리 직접 연결한다**

```python
# ❌ 틀린 코드
def union(a, b):
    parent[a] = b          # find 없이 원소를 원소에 매단다
```

왜: `a`가 원래 속했던 트리의 나머지 노드들은 여전히 옛 뿌리를 가리킨다. 한 집합이 두 뿌리로 쪼개져 보여 `find` 결과가 서로 달라지고, "같은 그룹인가" 판정이 즉시 깨진다. 크루스칼에서는 이미 이어진 두 정점을 다시 채택해 사이클이 든 간선 집합이 나온다.

```python
# ✅ 고친 코드
def union(a, b):
    ra, rb = find(a), find(b)   # 먼저 양쪽 뿌리를 구하고
    if ra == rb:
        return False
    parent[rb] = ra             # 뿌리끼리 붙인다
    return True
```

**다음 챕터로**

- 프림의 뼈대는 다익스트라와 한 줄만 다르다. 힙 키를 `w`에서 `dist[u] + w`로 바꾸면 그대로 최단 경로가 되므로, 최단 경로 챕터에서 이 코드를 다시 꺼내 쓰게 된다.
- 유니온-파인드는 MST 밖에서도 계속 등장한다. "간선을 지우는 질의"를 역순으로 뒤집어 합치기로 바꾸는 오프라인 기법, 그리고 좌표·격자를 그룹으로 묶는 문제들이 모두 같은 부품 위에 서 있다.
