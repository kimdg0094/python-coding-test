## L4. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch02(MST)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. Union-Find의 집합 크기·그룹 수 추적, Kruskal의 "정렬 + 사이클 판정" 골격, Prim의 힙·배열 두 버전을 소재만 바꿔 여러 번 다시 짜 본다.
- **반복 훈련 개념**:
  - Union-Find 뼈대: 반복형 `find`(경로 압축) + `union`(크기/랭크 기준). 합치기 성공 여부를 `True/False`로 돌려주면 사이클 판정·그룹 수 감소(`comp -= 1`)·크기 갱신(`size[ra] += size[rb]`)이 한 줄로 끝난다
  - Kruskal: `edges.sort()` 후 `for w, a, b in edges: if union(a, b): total += w; cnt += 1`. 채택 간선 수 `cnt == n-1`로 완성/비연결 판정
  - Kruskal 변형: 내림차순 정렬이면 최대 신장 트리, "u와 v가 처음 같은 집합이 되는 순간의 w"가 최소 병목, 채택을 `n-k`개에서 멈추면 k개 군집
  - 컷 성질(cut property): 어떤 절단이든 그 절단을 건너는 최소 간선은 반드시 어떤 MST에 들어간다 — Kruskal·Prim 정당성과 "이 간선이 MST에 들어갈 수 있는가" 판정의 근거
  - Prim: 힙 버전은 `heappush(heap, (w, v))`에 누적이 아닌 간선 가중치만, 배열 버전은 `key[v] = min(key[v], cost(u, v))`를 O(V²)로 — 좌표 완전 그래프처럼 간선을 미리 나열하기 어려울 때 유리
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '최소 신장 트리'·'유니온 파인드' 단계, 프로그래머스 「코딩테스트 고득점 Kit」의 '그래프', NeetCode 150의 'Advanced Graphs'(Min Cost to Connect Points·병목 경로).
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 집합 크기 질의 | Easy | union by size·`size[find(a)]` | 반복 훈련 |
| 2 | 친구 그룹 수와 최대 그룹 추적 | Medium | union 성공 시 `comp -= 1`·크기 갱신 | 반복 훈련 |
| 3 | 최소 병목 경로 | Medium | Kruskal 진행 중 두 정점이 처음 연결되는 순간 | 유형 확장 (NeetCode 'Advanced Graphs' 스타일) |
| 4 | k개 군집으로 나누기 | Medium | MST 간선 중 큰 k-1개 제거 | 유형 확장 (백준 '최소 신장 트리' 단계 스타일) |
| 5 | 맨해튼 완전 그래프 MST | Medium | O(V²) 배열 Prim, 간선을 즉석 계산 | 반복 훈련 |
| 6 | 트리로 만들기 위한 최소 제거 비용 | Medium | 내림차순 Kruskal(최대 신장 숲) | 반복 훈련 |
| 7 | 차선 최소 신장 트리 | Hard | MST 간선 하나씩 제외하고 Kruskal 재실행 | 유형 확장 (백준 '최소 신장 트리' 단계 스타일) |
| 8 | 간선의 MST 소속 판정 | Hard | 컷 성질 + 가중치 기준 Union-Find 두 번 | 유형 확장 (solved.ac CLASS 5 MST 응용 스타일) |
| 9 | 간선 철거 후 연결 질의 | Hard | 역순(오프라인) Union-Find·union by rank | 유형 확장 (백준 '유니온 파인드' 단계 스타일) |
| 10 | 길이 제한과 기존 배선이 있는 전력망 | Hard | 힙 Prim + 즉석 인접 리스트 + 0비용 간선 | 반복 훈련 |

**문제**

**1) 집합 크기 질의** · Easy

- **요구사항**: 원소 0..n-1에 대해 연산이 순서대로 주어진다. `1 a b`는 a와 b가 속한 집합을 합치고, `2 a`는 a가 속한 집합의 원소 수를 출력한다. Union-Find(크기 기준 합치기)로 처리하라.
- **입력**: 첫 줄 `n q` (1 ≤ n ≤ 300, 1 ≤ q ≤ 500). 다음 q줄에 `1 a b` 또는 `2 a`. `2` 연산은 1개 이상 있다.
- **출력**: 각 `2` 연산마다 집합 크기를 한 줄에 하나씩.
- **예제**:
  `6 6 / 1 0 1 / 1 2 3 / 2 0 / 1 1 3 / 2 2 / 2 5` → `2` `4` `1`
  `3 2 / 2 0 / 2 2` → `1` `1`
- **셀프체크**: 크기는 **뿌리**에만 유지되므로 `size[a]`가 아니라 `size[find(a)]`를 읽었는가? 이미 같은 집합인 쌍을 다시 합칠 때 크기를 두 번 더하지 않았는가(셋째 테스트)? 연산 종류에 따라 읽는 정수 개수가 다른 입력을 올바르게 파싱했는가?

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); q = int(data[idx + 1]); idx += 2
    parent = list(range(n))
    size = [1] * n

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:          # 경로 압축
            parent[x], x = root, parent[x]
        return root

    out = []
    for _ in range(q):
        t = int(data[idx]); idx += 1
        if t == 1:
            a = int(data[idx]); b = int(data[idx + 1]); idx += 2
            ra, rb = find(a), find(b)
            if ra != rb:                  # 같은 집합이면 크기 변화 없음
                if size[ra] < size[rb]:
                    ra, rb = rb, ra
                parent[rb] = ra
                size[ra] += size[rb]
        else:
            a = int(data[idx]); idx += 1
            out.append(str(size[find(a)]))
    print('\n'.join(out))

main()
@@TESTS
--IN
6 6
1 0 1
1 2 3
2 0
1 1 3
2 2
2 5
--OUT
2
4
1
--IN
3 2
2 0
2 2
--OUT
1
1
--IN
4 4
1 0 1
1 0 1
1 1 0
2 1
--OUT
2
@@EXPL
(1) 접근·핵심 아이디어

- "합쳐라/크기는?" 질의가 섞여 반복되므로 Union-Find가 정석이다. 크기 기준 합치기(union by size)를 쓰면 `size` 배열이 부산물로 생기고, 그 값은 항상 **뿌리 원소**에서만 정확하다.
- 따라서 크기 질의는 `size[find(a)]`. 이미 같은 집합인 쌍을 합치면 아무것도 하지 않아야 크기가 중복 가산되지 않는다.

(2) 코드 단계별

- `parent[i] = i`, `size[i] = 1`로 초기화한다.
- `find`는 반복형 + 경로 압축.
- 연산 종류 `t`를 먼저 읽고, `1`이면 두 정수를 더 읽어 뿌리가 다를 때만 작은 쪽을 큰 쪽 아래에 붙이며 크기를 합산. `2`면 정수 하나를 읽어 `size[find(a)]`를 기록.
- 결과를 줄바꿈으로 모아 출력.

(3) 스스로 다시 짤 때 생각 순서

- Union-Find 뼈대 → 연산별 읽는 정수 개수가 다름에 주의해 파싱 → 크기는 뿌리에서 읽기. 총 O((n + q)·α(n)).
- 경계: 아무 합치기도 없으면 모든 크기가 1(둘째 테스트). 같은 쌍을 여러 번 합쳐도 크기는 2를 유지해야 한다(셋째 테스트).
```

**2) 친구 그룹 수와 최대 그룹 추적** · Medium

- **요구사항**: 학생 n명이 있고, 처음에는 모두 서로 모른다. 친구 관계 `a b`가 하나씩 추가될 때마다 "현재 친구 그룹(연결 요소)의 수"와 "가장 큰 그룹의 인원 수"를 출력하라. 이미 같은 그룹인 두 사람의 관계가 추가되면 아무 변화도 없다.
- **입력**: 첫 줄 `n m` (1 ≤ n ≤ 300, 1 ≤ m ≤ 500). 다음 m줄 관계 `a b` (0-based, a = b일 수 있음).
- **출력**: 관계마다 `그룹수 최대인원`을 한 줄에.
- **예제**:
  `5 4 / 0 1 / 2 3 / 1 2 / 0 3` → `4 2` `3 2` `2 4` `2 4`
  (마지막 0-3은 이미 같은 그룹이라 변화 없음)
  `4 2 / 0 1 / 2 3` → `3 2` `2 2`
- **셀프체크**: 그룹 수는 n에서 시작해 union이 **실제로** 성공할 때만 1 줄였는가? 최대 인원은 합쳐진 뒤의 뿌리 크기와 비교해 갱신하면 되고, 절대 줄어들지 않는다는 점을 이용했는가? `a == b`인 자기 관계에서 그룹 수가 줄지 않는가?

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); idx += 2
    parent = list(range(n))
    size = [1] * n

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    comp = n
    largest = 1
    out = []
    for _ in range(m):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        ra, rb = find(a), find(b)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            comp -= 1
            if size[ra] > largest:
                largest = size[ra]
        out.append(f"{comp} {largest}")
    print('\n'.join(out))

main()
@@TESTS
--IN
5 4
0 1
2 3
1 2
0 3
--OUT
4 2
3 2
2 4
2 4
--IN
4 2
0 1
2 3
--OUT
3 2
2 2
--IN
1 1
0 0
--OUT
1 1
--IN
3 3
0 1
1 2
2 0
--OUT
2 2
1 3
1 3
@@EXPL
(1) 접근·핵심 아이디어

- 관계가 추가될 때마다 연결 요소 수를 다시 세면 O(m·(n+m))이지만, Union-Find로 "실제로 두 그룹이 합쳐질 때만 `comp -= 1`"로 추적하면 관계당 거의 상수 시간이다.
- 최대 그룹 크기는 단조 증가한다(합치기만 있고 분리가 없으므로). 그래서 합쳐진 직후의 뿌리 크기 `size[ra]`와만 비교하면 된다.

(2) 코드 단계별

- `comp = n`, `largest = 1`로 시작한다(모두 혼자인 상태).
- 관계 `(a, b)`의 두 뿌리가 다르면 크기 기준으로 합치고 `comp -= 1`, `largest = max(largest, size[ra])`.
- 뿌리가 같으면(이미 친구 그룹이거나 `a == b`) 아무 변화 없이 현재 값을 그대로 출력.
- 관계마다 `f"{comp} {largest}"`를 기록해 출력.

(3) 스스로 다시 짤 때 생각 순서

- "그룹 수 = n - 성공한 union 수"라는 관계를 먼저 잡는다 → 크기 갱신을 union 성공 지점에 넣는다 → 최대는 단조라 갱신만 한다. 총 O(m·α(n)).
- 경계: n=1에 `0 0` 하나면 `1 1`. 삼각형(넷째 테스트)에서 세 번째 관계는 사이클이라 그룹 수·최대 모두 그대로다.
```

**3) 최소 병목 경로** · Medium

- **요구사항**: 무방향 가중 그래프에서 정점 s에서 t로 가는 경로들 중 "경로 위 가장 큰 간선 가중치"가 최소가 되는 값을 구하라(트럭이 지나야 하는 다리 중 가장 낮은 하중 제한을 최대한 높이는 문제와 같은 구조). 도달할 수 없으면 -1, s = t이면 0을 출력한다.
- **입력**: 첫 줄 `n m` (1 ≤ n ≤ 300, 0 ≤ m ≤ 500). 다음 m줄 간선 `a b w` (0-based, 1 ≤ w ≤ 10^6, 다중 간선 가능). 마지막 줄 `s t`.
- **출력**: 최소 병목 값(또는 -1).
- **예제**:
  `5 6 / 0 1 4 / 1 2 8 / 0 2 10 / 2 3 3 / 3 4 6 / 1 4 9 / 0 4` → `8`
  (0-1-2-3-4는 최대 8, 0-1-4는 9, 0-2-3-4는 10)
  `3 1 / 0 1 5 / 0 2` → `-1`
- **셀프체크**: 간선을 오름차순으로 넣다가 s와 t가 **처음** 같은 집합이 되는 순간의 가중치가 답인 이유(그 전까지는 더 작은 간선만으로 못 이었고, 그 순간 이은 경로는 최대가 현재 w)를 설명할 수 있는가? 사이클 간선(이미 같은 집합)도 그냥 건너뛰면 되는가? s = t를 정렬 전에 먼저 처리했는가?

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); idx += 2
    edges = []
    for _ in range(m):
        a = int(data[idx]); b = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        edges.append((w, a, b))
    s = int(data[idx]); t = int(data[idx + 1]); idx += 2
    if s == t:
        print(0)
        return
    edges.sort()

    parent = list(range(n))
    size = [1] * n

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for w, a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            if find(s) == find(t):     # 처음 연결되는 순간의 w가 답
                print(w)
                return
    print(-1)

main()
@@TESTS
--IN
5 6
0 1 4
1 2 8
0 2 10
2 3 3
3 4 6
1 4 9
0 4
--OUT
8
--IN
3 1
0 1 5
0 2
--OUT
-1
--IN
2 2
0 1 7
0 1 2
0 1
--OUT
2
--IN
3 2
0 1 1
1 2 1
1 1
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- "경로의 최댓값을 최소화"는 Kruskal이 자연스럽다. 간선을 가중치 오름차순으로 하나씩 켜 나가면, 가중치 w 이하의 간선만으로 s와 t가 이어지는 최초의 w가 답이다. 그 전에는 더 작은 간선들만으로는 연결이 불가능했고, 그 순간에는 최대 가중치가 w인 경로가 존재하기 때문이다.
- 이 값은 MST 위의 s-t 경로의 최대 간선과도 같다(MST의 병목 성질). 그래서 "최소 병목 경로 = MST 위 경로"라는 결과를 기억해 두면 다른 문제에서도 쓰인다.

(2) 코드 단계별

- 간선을 `(w, a, b)`로 담고 정렬한다. s = t는 정렬 전에 0으로 처리.
- Union-Find를 초기화하고 정렬 순서대로 union. 실제로 합쳐진 뒤 `find(s) == find(t)`가 되면 그 w를 출력하고 종료.
- 끝까지 이어지지 않으면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "최대의 최소" 구조를 보면 정렬 + Union-Find → 연결 시점 체크. O(m log m + m·α(n)).
- 경계: 다중 간선은 작은 것이 먼저 오므로 자연히 유리한 쪽이 선택된다(셋째 테스트). 사이클 간선은 union이 실패하므로 연결 상태가 바뀌지 않아 체크를 건너뛰어도 된다.
```

**4) k개 군집으로 나누기** · Medium

- **요구사항**: 연결 무방향 가중 그래프의 정점들을 정확히 k개의 군집으로 나누되, "군집 내부를 잇는 데 쓴 간선 비용의 합"을 최소로 하고 싶다. MST를 구한 뒤 가중치가 큰 간선 k-1개를 끊으면 되는 것으로 알려져 있다. 남은 간선 비용의 합을 출력하라. 그래프가 연결되어 있지 않으면 -1을 출력한다.
- **입력**: 첫 줄 `n m k` (1 ≤ n ≤ 300, 0 ≤ m ≤ 500, 1 ≤ k ≤ n). 다음 m줄 간선 `a b w` (0-based, 1 ≤ w ≤ 10^6).
- **출력**: 남은 간선 비용의 합(또는 -1).
- **예제**:
  `6 7 2 / 0 1 1 / 1 2 5 / 2 3 2 / 3 4 7 / 4 5 1 / 0 5 9 / 1 4 6` → `9`
  (MST 간선 1,1,2,5,6 중 가장 큰 6을 끊으면 1+1+2+5=9)
  `6 7 1 / 0 1 1 / 1 2 5 / 2 3 2 / 3 4 7 / 4 5 1 / 0 5 9 / 1 4 6` → `15`
- **셀프체크**: MST 간선을 오름차순으로 모았을 때 앞에서 `n-k`개만 더하면 "큰 k-1개 제거"와 같은가? k = n이면 아무 간선도 남지 않아 0인가? MST가 여러 개여도 간선 가중치의 **정렬된 목록**은 항상 같으므로 답이 유일함을 이해했는가? 비연결이면 채택 간선이 n-1개 미만이다.

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); k = int(data[idx + 2]); idx += 3
    edges = []
    for _ in range(m):
        a = int(data[idx]); b = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        edges.append((w, a, b))
    edges.sort()

    parent = list(range(n))
    size = [1] * n

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    chosen = []                      # MST 간선 가중치(오름차순으로 쌓임)
    for w, a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            continue
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        chosen.append(w)
        if len(chosen) == n - 1:
            break

    if len(chosen) < n - 1:
        print(-1)
        return
    print(sum(chosen[:n - k]))       # 큰 k-1개 제거 = 작은 n-k개만 남김

main()
@@TESTS
--IN
6 7 2
0 1 1
1 2 5
2 3 2
3 4 7
4 5 1
0 5 9
1 4 6
--OUT
9
--IN
6 7 1
0 1 1
1 2 5
2 3 2
3 4 7
4 5 1
0 5 9
1 4 6
--OUT
15
--IN
3 3 3
0 1 1
1 2 2
0 2 3
--OUT
0
--IN
4 2 2
0 1 1
2 3 1
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- MST는 "전체를 가장 싸게 잇는 트리"다. 트리에서 간선 하나를 끊으면 조각이 하나 늘어나므로, k개 조각을 만들려면 k-1개를 끊어야 하고, 남는 비용을 최소로 하려면 가장 비싼 k-1개를 끊는 것이 최적이다(MST 간선 집합에서 부분 집합을 고르는 셈이고, 어떤 다른 신장 숲도 이보다 싸지 않다는 것이 Kruskal의 탐욕 근거로 보장된다).
- 구현은 Kruskal에서 채택 간선을 오름차순으로 모아 두고 앞의 `n-k`개만 더하면 된다 — Kruskal은 오름차순으로 채택하므로 따로 정렬할 필요가 없다.

(2) 코드 단계별

- 간선을 정렬하고 Union-Find로 Kruskal을 돌리며 채택 가중치를 `chosen`에 쌓는다.
- 채택 개수가 n-1 미만이면 비연결 → -1.
- `sum(chosen[:n-k])` 출력. k = 1이면 전체 MST, k = n이면 빈 합 0.

(3) 스스로 다시 짤 때 생각 순서

- Kruskal 골격 → 채택 가중치 리스트화 → 조각 수와 끊는 간선 수의 관계(k개 조각 = k-1개 절단) → 앞에서 n-k개 합. O(m log m).
- 경계: MST가 유일하지 않아도 채택 가중치의 정렬 목록은 같으므로 답은 유일하다. 비연결 그래프는 이미 조각이 나뉘어 있어 문제 정의가 애매하므로 -1로 규정했다.
```

**5) 맨해튼 완전 그래프 MST** · Medium

- **요구사항**: 평면 위 n개의 점이 있고, 두 점을 잇는 비용은 맨해튼 거리 `|x1-x2| + |y1-y2|`다. 모든 점을 연결하는 최소 총비용을 구하라. 모든 쌍이 간선이므로 간선 목록을 만들지 말고, O(V²) 배열 기반 Prim으로 거리를 즉석에서 계산하라.
- **입력**: 첫 줄 n (1 ≤ n ≤ 300). 다음 n줄 `x y` (-10^4 ≤ x, y ≤ 10^4, 같은 좌표가 반복될 수 있음).
- **출력**: 최소 총비용.
- **예제**:
  `4 / 0 0 / 0 3 / 4 0 / 4 3` → `10`
  (3 + 3 + 4)
  `3 / 1 1 / 3 5 / 6 2` → `12`
- **셀프체크**: 간선 수가 n(n-1)/2라 Kruskal은 정렬 비용 O(n² log n)이 들지만, 배열 Prim은 O(n²)로 끝난다는 비교를 할 수 있는가? `key[v]`를 "현재 트리에서 v까지의 최소 거리"로 유지하고 정점이 편입될 때마다 나머지 정점의 key를 갱신했는가? 같은 좌표의 점은 비용 0으로 이어지는가? n = 1이면 0인가?

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    xs = [0] * n
    ys = [0] * n
    for i in range(n):
        xs[i] = int(data[idx]); ys[i] = int(data[idx + 1]); idx += 2

    INF = float('inf')
    key = [INF] * n          # 트리까지의 최소 연결 비용
    used = [False] * n
    key[0] = 0
    total = 0
    for _ in range(n):
        u = -1
        best = INF
        for v in range(n):   # 아직 안 넣은 정점 중 key 최소
            if not used[v] and key[v] < best:
                best = key[v]; u = v
        used[u] = True
        total += key[u]
        ux, uy = xs[u], ys[u]
        for v in range(n):   # 새 정점 기준으로 나머지 key 갱신(거리 즉석 계산)
            if not used[v]:
                d = abs(ux - xs[v]) + abs(uy - ys[v])
                if d < key[v]:
                    key[v] = d
    print(total)

main()
@@TESTS
--IN
4
0 0
0 3
4 0
4 3
--OUT
10
--IN
3
1 1
3 5
6 2
--OUT
12
--IN
1
5 5
--OUT
0
--IN
3
2 2
2 2
9 9
--OUT
14
@@EXPL
(1) 접근·핵심 아이디어

- 좌표 완전 그래프는 간선이 O(n²)개다. Kruskal은 그 간선을 전부 만들어 정렬해야 하므로 O(n² log n)인 반면, 배열 Prim은 "매 단계 key 최소 정점 선택 + 이웃 key 갱신"을 n번 반복해 O(n²)로 끝나고 간선을 저장할 필요도 없다. 밀집 그래프에서 배열 Prim이 유리한 전형적인 사례다.
- 정당성은 컷 성질: 현재 트리와 바깥을 가르는 절단에서 가장 싼 간선(= key 최소 정점의 연결 간선)은 항상 어떤 MST에 포함된다.

(2) 코드 단계별

- 좌표를 `xs`, `ys`에 담는다.
- `key[0] = 0`으로 시작. n번 반복: 미편입 정점 중 key 최소 `u`를 선형 탐색으로 고르고 편입(`total += key[u]`).
- `u`와 나머지 미편입 정점 v 사이 맨해튼 거리를 계산해 `key[v]`를 더 작으면 갱신.
- `total` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "간선을 미리 못 만들겠다/너무 많다" → 배열 Prim → 거리 함수를 갱신 루프 안에서 직접 호출. 완전 그래프라 항상 연결되므로 비연결 판정이 필요 없다.
- 경계: n = 1이면 첫 반복에서 0번만 편입하고 끝(0). 같은 좌표 점은 거리 0으로 이어진다(넷째 테스트: 0 + 14).
```

**6) 트리로 만들기 위한 최소 제거 비용** · Medium

- **요구사항**: 무방향 가중 그래프에서 간선을 몇 개 제거해 **사이클이 하나도 없게** 만들되, 원래 연결되어 있던 정점 쌍은 여전히 연결되어 있어야 한다(각 연결 요소를 트리로 만든다). 제거한 간선 가중치 합의 최솟값을 구하라.
- **입력**: 첫 줄 `n m` (1 ≤ n ≤ 300, 0 ≤ m ≤ 500). 다음 m줄 간선 `a b w` (0-based, 1 ≤ w ≤ 10^6, 다중 간선 가능).
- **출력**: 제거 비용의 최솟값.
- **예제**:
  `4 5 / 0 1 3 / 1 2 4 / 2 0 5 / 2 3 2 / 3 0 6` → `5`
  (6, 5, 4를 남기고 3과 2를 제거)
  `3 2 / 0 1 1 / 1 2 1` → `0`
- **셀프체크**: "제거 비용 최소 = 남기는 비용 최대 = 최대 신장 숲"으로 뒤집었는가? 내림차순 정렬한 Kruskal에서 채택되지 않은(사이클을 만드는) 간선의 합이 곧 답인가? 그래프가 비연결이어도 각 컴포넌트마다 독립적으로 동작하므로 -1 처리가 필요 없는가? 같은 쌍의 다중 간선 중 큰 것 하나만 남는가?

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); idx += 2
    edges = []
    for _ in range(m):
        a = int(data[idx]); b = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        edges.append((w, a, b))
    edges.sort(reverse=True)         # 최대 신장 숲: 비싼 간선부터 채택

    parent = list(range(n))
    size = [1] * n

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    removed = 0
    for w, a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            removed += w             # 사이클을 만드는 간선 = 제거 대상
            continue
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
    print(removed)

main()
@@TESTS
--IN
4 5
0 1 3
1 2 4
2 0 5
2 3 2
3 0 6
--OUT
5
--IN
3 2
0 1 1
1 2 1
--OUT
0
--IN
5 4
0 1 2
1 2 3
2 0 4
3 4 1
--OUT
2
--IN
2 3
0 1 5
0 1 1
0 1 3
--OUT
4
@@EXPL
(1) 접근·핵심 아이디어

- 각 연결 요소를 트리로 만들 때 남는 간선 수는 정해져 있다(정점 수 - 1). 제거 비용을 최소화하려면 **남기는** 간선 비용을 최대화하면 되고, 그것이 최대 신장 숲(maximum spanning forest)이다. Kruskal에서 정렬 방향만 내림차순으로 바꾸면 된다.
- Kruskal이 건너뛰는 간선(이미 같은 집합)은 정확히 "사이클을 만드는 간선"이며, 내림차순이므로 그 사이클에서 가장 싼 쪽이 버려진다. 따라서 건너뛴 가중치의 합이 답이다. 비연결 그래프도 컴포넌트별로 독립이라 그대로 동작한다.

(2) 코드 단계별

- 간선을 `(w, a, b)`로 담고 `sort(reverse=True)`.
- Union-Find로 순서대로 처리: 뿌리가 같으면 `removed += w`, 다르면 합친다.
- `removed` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "제거 최소 ↔ 유지 최대" 변환 → 최대 신장 숲 = 내림차순 Kruskal → 건너뛴 간선 합. O(m log m).
- 경계: 이미 숲이면 0(둘째 테스트). 다중 간선은 가장 비싼 것만 남고 나머지는 전부 제거된다(넷째 테스트: 1 + 3). 검산: `총합 - 채택합 = removed`.
```

**7) 차선 최소 신장 트리** · Hard

- **요구사항**: 연결 무방향 가중 그래프에서 MST 비용을 C라 하자. 간선 집합이 MST와 **다른** 신장 트리 중 비용이 가장 작은 것(차선 MST)의 비용을 구하라. 비용이 C와 같아도 간선 집합이 다르면 인정한다. 그런 트리가 없거나(신장 트리가 하나뿐) 그래프가 비연결이면 -1을 출력한다.
- **입력**: 첫 줄 `n m` (2 ≤ n ≤ 50, 1 ≤ m ≤ 200). 다음 m줄 간선 `a b w` (0-based, 1 ≤ w ≤ 10^6, 다중 간선 가능).
- **출력**: 차선 MST 비용(또는 -1).
- **예제**:
  `4 5 / 0 1 1 / 1 2 2 / 2 3 3 / 0 3 4 / 0 2 5` → `7`
  (MST {1,2,3}=6. 간선 3을 빼면 {1,2,4}=7이 최소)
  `3 2 / 0 1 1 / 1 2 1` → `-1`
- **셀프체크**: 차선 트리는 MST에서 간선 **정확히 하나**를 빼고 하나를 넣은 형태로 항상 얻을 수 있다는 사실(교환 논증)을 근거로, "MST의 각 간선을 하나씩 제외하고 Kruskal을 다시 돌린 결과의 최솟값"을 취했는가? 제외 후 신장 트리가 안 만들어지면 그 후보는 버렸는가? 가중치가 같은 간선이 여럿이면 답이 C와 같을 수 있는가(셋째 테스트)?

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); idx += 2
    edges = []
    for i in range(m):
        a = int(data[idx]); b = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        edges.append((w, a, b, i))
    edges.sort()

    def kruskal(skip):
        # skip 번호 간선을 제외하고 MST → (비용, 채택 간선 번호 목록) 또는 None
        parent = list(range(n))
        size = [1] * n

        def find(x):
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:
                parent[x], x = root, parent[x]
            return root

        total = 0
        used = []
        for w, a, b, i in edges:
            if i == skip:
                continue
            ra, rb = find(a), find(b)
            if ra == rb:
                continue
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            total += w
            used.append(i)
            if len(used) == n - 1:
                break
        if len(used) < n - 1:
            return None
        return total, used

    base = kruskal(-1)
    if base is None:
        print(-1)
        return
    best = -1
    for e in base[1]:                  # MST 간선을 하나씩 제외
        r = kruskal(e)
        if r is not None and (best == -1 or r[0] < best):
            best = r[0]
    print(best)

main()
@@TESTS
--IN
4 5
0 1 1
1 2 2
2 3 3
0 3 4
0 2 5
--OUT
7
--IN
3 2
0 1 1
1 2 1
--OUT
-1
--IN
3 3
0 1 1
1 2 1
0 2 1
--OUT
2
--IN
4 2
0 1 1
2 3 1
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- 교환 논증: 어떤 신장 트리 T'가 MST T와 다르면 T에는 있고 T'에는 없는 간선 e가 존재한다. 그러면 T'는 "e를 제외한 그래프"의 신장 트리이므로, 비용은 `MST(G - e)` 이상이다. 따라서 차선 비용은 T의 간선 e를 하나씩 제외하며 구한 `MST(G - e)`들의 최솟값과 같다(그 최솟값을 주는 트리는 e를 안 쓰므로 T와 다르다).
- n ≤ 50, m ≤ 200이므로 Kruskal을 최대 n번(=MST 간선 수) 다시 돌려도 O(n·m·α)로 충분하다. 간선 정렬은 한 번만 하고 `skip`만 바꿔 재사용한다.

(2) 코드 단계별

- 간선에 원래 번호 `i`를 붙여 `(w, a, b, i)`로 정렬한다.
- `kruskal(skip)`: 번호 `skip`을 건너뛰며 Kruskal. 채택 간선이 n-1개 미만이면 `None`, 아니면 `(비용, 채택 번호 목록)`.
- `kruskal(-1)`로 기준 MST를 얻는다(없으면 -1).
- MST의 각 채택 간선을 제외하고 다시 돌려 유효한 결과 중 최솟값을 취한다. 하나도 없으면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "MST와 다른 트리"를 "MST의 어떤 간선을 안 쓰는 트리"로 바꿔 생각 → 그 간선 제외 후 MST → 최소. 제외 시 비연결이면 후보에서 제거.
- 경계: 그래프 자체가 트리면 어떤 간선을 빼도 끊기므로 -1(둘째 테스트). 동일 가중치 삼각형은 어느 간선을 빼도 비용 2가 나와 C와 같다(셋째 테스트). 다중 간선도 번호로 구분되므로 같은 쌍의 다른 간선으로 대체할 수 있다.
```

**8) 간선의 MST 소속 판정** · Hard

- **요구사항**: 연결 무방향 가중 그래프(자기 루프·다중 간선 없음)의 각 간선에 대해, 그 간선이 **모든** MST에 들어가면 `ALL`, 일부 MST에만 들어가면 `SOME`, 어떤 MST에도 들어가지 않으면 `NONE`을 출력하라. 가중치가 같은 간선이 여럿일 수 있다.
- **입력**: 첫 줄 `n m` (2 ≤ n ≤ 50, 1 ≤ m ≤ 200). 다음 m줄 간선 `a b w` (0-based, 1 ≤ w ≤ 10^6).
- **출력**: 입력 순서대로 간선마다 `ALL`/`SOME`/`NONE`을 한 줄에 하나씩.
- **예제**:
  `4 5 / 0 1 1 / 1 2 2 / 2 3 2 / 0 3 2 / 0 2 3` → `ALL` `SOME` `SOME` `SOME` `NONE`
  (가중치 2인 세 간선은 0-1과 함께 사이클을 이루므로 그중 둘만 쓰인다. 0-2(3)는 더 싼 경로로 이미 연결되어 있어 불필요)
  `3 3 / 0 1 1 / 1 2 2 / 0 2 3` → `ALL` `ALL` `NONE`
- **셀프체크**: 간선 e=(u,v,w)가 어떤 MST에 들어갈 수 있는 조건은 "가중치 **w 미만**인 간선만으로 u와 v가 이어지지 않는다"(컷 성질)이고, 모든 MST에 들어갈 조건은 "e를 제외한 가중치 **w 이하**인 간선만으로도 u와 v가 이어지지 않는다"(같은 무게의 대체 경로가 없음)라는 두 판정을 순서대로 적용했는가? 각 판정마다 Union-Find를 새로 만들었는가?

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); idx += 2
    edges = []
    for _ in range(m):
        a = int(data[idx]); b = int(data[idx + 1]); w = int(data[idx + 2]); idx += 3
        edges.append((a, b, w))

    def connected(u, v, limit, strict, skip):
        # 가중치가 limit 미만(strict) 또는 이하(not strict)인 간선만 union
        parent = list(range(n))
        size = [1] * n

        def find(x):
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:
                parent[x], x = root, parent[x]
            return root

        for j in range(m):
            if j == skip:
                continue
            a, b, w = edges[j]
            if (w < limit) if strict else (w <= limit):
                ra, rb = find(a), find(b)
                if ra != rb:
                    if size[ra] < size[rb]:
                        ra, rb = rb, ra
                    parent[rb] = ra
                    size[ra] += size[rb]
        return find(u) == find(v)

    out = []
    for i in range(m):
        u, v, w = edges[i]
        if connected(u, v, w, True, -1):        # 더 싼 간선만으로 이미 연결
            out.append("NONE")
        elif connected(u, v, w, False, i):      # 같은 무게 이하의 대체 경로 존재
            out.append("SOME")
        else:
            out.append("ALL")
    print('\n'.join(out))

main()
@@TESTS
--IN
4 5
0 1 1
1 2 2
2 3 2
0 3 2
0 2 3
--OUT
ALL
SOME
SOME
SOME
NONE
--IN
3 3
0 1 1
1 2 2
0 2 3
--OUT
ALL
ALL
NONE
--IN
2 1
0 1 5
--OUT
ALL
--IN
4 4
0 1 7
1 2 7
2 3 7
3 0 7
--OUT
SOME
SOME
SOME
SOME
@@EXPL
(1) 접근·핵심 아이디어

- Kruskal의 관점에서 간선 e=(u,v,w)를 볼 차례가 왔을 때, 이미 w 미만 간선들로 u-v가 이어져 있으면 e는 어떤 순서로 돌려도 사이클이 되어 절대 채택되지 않는다 → `NONE`. 반대로 이어져 있지 않으면 컷 성질에 의해 e를 포함하는 MST가 존재한다.
- 그 경우, e를 빼고 w 이하 간선(같은 무게 포함)만으로 u-v가 이어진다면 e 대신 그 경로의 간선을 써도 비용이 같은 MST가 되므로 e 없는 MST가 존재 → `SOME`. 이어지지 않으면 어떤 MST도 e 없이는 u-v를 w 이하로 못 잇는다 → `ALL`(e는 "가중치 w 이하 부분 그래프"의 다리).

(2) 코드 단계별

- 간선 목록을 저장한다.
- `connected(u, v, limit, strict, skip)`: 조건(미만/이하)에 맞는 간선만 Union-Find로 합친 뒤 u, v가 같은 집합인지 반환. `skip`은 자기 자신 제외용.
- 간선마다 (1) `strict=True, skip=-1`로 NONE 판정, (2) 아니면 `strict=False, skip=i`로 SOME/ALL 판정.
- 결과를 순서대로 출력.

(3) 스스로 다시 짤 때 생각 순서

- 컷 성질에서 "w 미만으로 연결됐는가"를 먼저, 그다음 "동점 대체 경로가 있는가"를 확인하는 2단계 판정으로 정리. 간선당 Union-Find 2회 → O(m²·α(n)).
- 경계: 모든 가중치가 같은 사이클(넷째 테스트)은 어느 간선이든 빼도 나머지 셋으로 이어지므로 전부 SOME. 정점 2개·간선 1개면 대체 경로가 없어 ALL. 가중치가 전부 다르면 MST가 유일해 SOME은 나오지 않는다.
```

**9) 간선 철거 후 연결 질의** · Hard

- **요구사항**: 무방향 그래프의 간선이 입력 순서대로 1번부터 하나씩 철거된다. 질의 `t u v`는 "앞에서부터 t개의 간선을 철거한 시점에 u와 v가 연결되어 있는가"를 묻는다. 질의는 임의의 순서로 주어지며 원래 순서대로 답하라. Union-Find는 삭제를 지원하지 않으므로, 질의를 t 내림차순으로 정렬해 **간선을 거꾸로 되살리며** 처리하라(오프라인 역순 처리). 랭크 기준 합치기를 사용한다.
- **입력**: 첫 줄 `n m` (1 ≤ n ≤ 300, 0 ≤ m ≤ 500). 다음 m줄 간선 `a b` (0-based). 다음 줄 q (1 ≤ q ≤ 300). 다음 q줄 `t u v` (0 ≤ t ≤ m).
- **출력**: 질의마다 입력 순서대로 `YES` 또는 `NO`.
- **예제**:
  `5 5 / 0 1 / 1 2 / 2 3 / 3 4 / 0 4 / 5 / 0 0 3 / 2 0 3 / 4 0 3 / 5 2 2 / 1 0 1` → `YES` `YES` `NO` `YES` `YES`
  (t=4면 간선 0-4만 남아 0-3은 NO. t=5는 간선이 없지만 u=v라 YES)
  `2 1 / 0 1 / 2 / 0 0 1 / 1 0 1` → `YES` `NO`
- **셀프체크**: 시각 t에 남아 있는 간선은 번호 t+1..m이며, 큰 t부터 처리하면서 포인터 p를 m에서 t까지 내리며 간선 p를 union하면 되는가? 답을 원래 질의 순서로 되돌려 놓았는가(질의에 번호를 붙여 저장)? t=m(전부 철거)에서 u=v면 YES인가? 같은 t의 질의가 여럿이어도 문제없는가?

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); idx += 2
    edges = []
    for _ in range(m):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        edges.append((a, b))
    q = int(data[idx]); idx += 1
    queries = []
    for i in range(q):
        t = int(data[idx]); u = int(data[idx + 1]); v = int(data[idx + 2]); idx += 3
        queries.append((t, u, v, i))
    queries.sort(key=lambda x: -x[0])       # 많이 철거된 시점부터

    parent = list(range(n))
    rank = [0] * n

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:             # 낮은 트리를 높은 트리 밑에
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    ans = [""] * q
    p = m                                   # 간선 p+1..m 이 되살아난 상태
    for t, u, v, i in queries:
        while p > t:                        # 시각 t까지 간선을 거꾸로 복구
            a, b = edges[p - 1]
            union(a, b)
            p -= 1
        ans[i] = "YES" if find(u) == find(v) else "NO"
    print('\n'.join(ans))

main()
@@TESTS
--IN
5 5
0 1
1 2
2 3
3 4
0 4
5
0 0 3
2 0 3
4 0 3
5 2 2
1 0 1
--OUT
YES
YES
NO
YES
YES
--IN
2 1
0 1
2
0 0 1
1 0 1
--OUT
YES
NO
--IN
3 0
1
0 0 2
--OUT
NO
--IN
4 3
0 1
1 2
2 3
3
3 0 3
3 1 1
2 2 3
--OUT
NO
YES
YES
@@EXPL
(1) 접근·핵심 아이디어

- Union-Find는 합치기만 되고 분리는 안 된다. 그런데 "철거"를 시간을 거꾸로 보면 "설치"가 된다. 모든 질의를 미리 받아(오프라인) t가 큰 순서로 처리하면, 시각 t로 갈수록 남은 간선이 늘어나므로 union만으로 상태를 유지할 수 있다.
- 시각 t에 남은 간선은 번호 t+1..m이다. 포인터 p를 m에서 시작해 `p > t`인 동안 간선 p를 union하고 p를 내린다. 질의는 t 내림차순이라 p는 단조 감소하며 각 간선은 정확히 한 번만 union된다.

(2) 코드 단계별

- 간선과 질의를 읽고, 질의에 원래 번호 i를 붙여 t 내림차순으로 정렬한다.
- 랭크 기준 union(높이가 낮은 트리를 높은 트리 밑에, 같으면 랭크 +1)과 경로 압축 find를 준비한다.
- 정렬된 질의를 돌며 필요한 간선을 되살린 뒤 `find(u) == find(v)`를 `ans[i]`에 기록.
- `ans`를 원래 순서로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "삭제 질의 → 시간 역순 삽입"이라는 변환을 먼저 떠올린다 → 질의 정렬(번호 보존) → 포인터로 간선 복구 → 답을 원래 순서로 복원. O((m + q)·α(n) + q log q).
- 경계: t=m이면 간선이 하나도 없지만 u=v면 같은 집합이라 YES. m=0이면 복구할 간선이 없고 모든 다른 두 정점은 NO. 같은 t의 질의가 연속되어도 `while p > t`가 0번 돌 뿐이다.
```

**10) 길이 제한과 기존 배선이 있는 전력망** · Hard

- **요구사항**: 평면 위 n개의 건물이 있고, 두 건물을 직접 잇는 전선 비용은 맨해튼 거리다. 단, 한 전선의 길이는 L을 넘을 수 없다(거리가 L보다 크면 직접 연결 불가). 또 일부 건물 쌍은 이미 배선되어 있어 비용 0으로 연결된 것으로 본다(길이 제한과 무관). 모든 건물을 연결하는 최소 총비용을 구하고, 불가능하면 -1을 출력하라. 힙 기반 Prim으로 풀되, 인접 리스트를 직접 만들어 사용한다.
- **입력**: 첫 줄 `n L` (1 ≤ n ≤ 100, 0 ≤ L ≤ 10^5). 다음 n줄 `x y` (0 ≤ x, y ≤ 10^4). 다음 줄 f (0 ≤ f ≤ 100). 다음 f줄 기존 배선 `a b` (0-based).
- **출력**: 최소 총비용(또는 -1).
- **예제**:
  `5 5 / 0 0 / 3 0 / 3 4 / 10 10 / 12 10 / 1 / 2 3` → `9`
  (0-1(3), 1-2(4), 2-3(기존 0), 3-4(2). 2-3은 거리 13이지만 기존 배선)
  `5 5 / 0 0 / 3 0 / 3 4 / 10 10 / 12 10 / 0` → `-1`
  (건물 3, 4까지 5 이하 전선으로 닿을 수 없음)
- **셀프체크**: 모든 쌍 중 거리가 L 이하인 것만 인접 리스트에 양방향으로 넣고, 기존 배선은 거리와 무관하게 비용 0 간선으로 추가했는가? 힙에서 꺼낸 정점이 이미 편입됐으면 건너뛰는 지연 삭제를 했는가? 편입 정점이 n개 미만이면 -1인가? L=0이면 같은 좌표끼리만 직접 연결되는가?

```runner
@@SOLUTION
import sys
import heapq

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); L = int(data[idx + 1]); idx += 2
    xs = [0] * n
    ys = [0] * n
    for i in range(n):
        xs[i] = int(data[idx]); ys[i] = int(data[idx + 1]); idx += 2
    f = int(data[idx]); idx += 1

    adj = [[] for _ in range(n)]
    for i in range(n):                       # 길이 제한 이하인 쌍만 간선으로
        for j in range(i + 1, n):
            d = abs(xs[i] - xs[j]) + abs(ys[i] - ys[j])
            if d <= L:
                adj[i].append((j, d))
                adj[j].append((i, d))
    for _ in range(f):                       # 기존 배선: 비용 0, 제한 무관
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        adj[a].append((b, 0))
        adj[b].append((a, 0))

    visited = [False] * n
    heap = [(0, 0)]
    total, cnt = 0, 0
    while heap and cnt < n:
        w, u = heapq.heappop(heap)
        if visited[u]:                       # 지연 삭제
            continue
        visited[u] = True
        total += w
        cnt += 1
        for v, wv in adj[u]:
            if not visited[v]:
                heapq.heappush(heap, (wv, v))
    print(total if cnt == n else -1)

main()
@@TESTS
--IN
5 5
0 0
3 0
3 4
10 10
12 10
1
2 3
--OUT
9
--IN
5 5
0 0
3 0
3 4
10 10
12 10
0
--OUT
-1
--IN
1 1
0 0
0
--OUT
0
--IN
3 0
1 1
1 1
2 2
1
0 2
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 좌표 완전 그래프에 두 가지 변형이 붙었다: (a) 길이 제한 — 거리 > L인 쌍은 간선이 아예 없다(그래프가 비연결이 될 수 있음). (b) 기존 배선 — 비용 0 간선을 제한과 무관하게 추가. 이 두 조건을 인접 리스트를 만드는 단계에서 처리하면, 그 뒤는 표준 힙 Prim이다.
- 기존 배선을 "미리 union"으로 처리하는 Kruskal 방식도 되지만, 여기서는 비용 0 간선으로 넣어 Prim이 자연스럽게 먼저 꺼내게 한다(힙에서 0이 가장 먼저 나오므로).

(2) 코드 단계별

- 좌표를 읽고, 모든 쌍 (i, j)에 대해 맨해튼 거리 d가 L 이하일 때만 양방향으로 `adj`에 추가한다(n ≤ 100이라 O(n²) 간선이 부담 없다).
- 기존 배선 f개를 `(상대, 0)`으로 양방향 추가.
- 힙에 `(0, 0)`을 넣고 Prim: 꺼낸 정점이 이미 편입이면 건너뛰고, 아니면 편입해 비용 누적 후 이웃을 push.
- 편입 수가 n이면 `total`, 아니면 -1.

(3) 스스로 다시 짤 때 생각 순서

- 조건을 "간선 생성 규칙"으로 번역(제한 → 필터, 기존 배선 → 0비용) → 인접 리스트 → 힙 Prim + 지연 삭제 + `cnt == n` 판정. O(n² log n).
- 경계: n=1이면 시작 정점만 편입해 0. L=0이면 같은 좌표(거리 0)끼리만 이어지고 나머지는 기존 배선에 의존한다(넷째 테스트). 둘째 테스트처럼 멀리 떨어진 건물은 기존 배선이 없으면 -1.
```
