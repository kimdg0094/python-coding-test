## L3. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch4(이진탐색)의 핵심 — 정렬 배열에서의 이진탐색, Lower/Upper Bound, 그리고 "정답 후보 범위"에 이진탐색을 거는 파라메트릭 서치 — 를 **반복 훈련**하고, 코딩테스트 단골 이진탐색 유형으로 **확장**하는 연습 세트다. 모든 문제의 공통 질문은 "무엇에 이진탐색을 거는가(배열 인덱스인가, 답의 후보인가)"와 "단조 술어가 무엇인가"다.
- **반복 훈련 개념 1 — 닫힌 구간 이진탐색**: `lo, hi = 0, n-1` / `while lo <= hi` / `mid = (lo+hi)//2` / 세 갈래(같다·작다·크다)로 `lo=mid+1` 또는 `hi=mid-1`. 못 찾으면 -1을 루프 밖에서.
- **반복 훈련 개념 2 — Lower/Upper Bound 직접 구현**: 반열린 구간 `lo, hi = 0, n` / `while lo < hi` / lower는 `arr[mid] < x`일 때 `lo=mid+1`, upper는 `arr[mid] <= x`일 때 `lo=mid+1`, 아니면 `hi=mid`. 개수 = `upper - lower`.
- **반복 훈련 개념 3 — 답의 후보에 이진탐색(파라메트릭)**: 술어 `ok(mid)`가 한 지점에서 True↔False로 딱 한 번 바뀌면, 참인 최댓값은 `if ok(mid): ans=mid; lo=mid+1`, 참인 최솟값은 `if ok(mid): ans=mid; hi=mid-1`.
- **반복 훈련 개념 4 — 회전·봉우리 배열의 단조성 찾기**: 전체가 정렬돼 있지 않아도 `a[mid] > a[hi]`(회전) 또는 `a[mid] < a[mid+1]`(봉우리)처럼 "한쪽을 버릴 수 있는 판정"이 있으면 O(log n)이 성립한다.
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '이분 탐색' 단계(수 찾기·자르기류 파라메트릭), 프로그래머스 「코딩테스트 고득점 Kit」의 '이분탐색', NeetCode 150의 'Binary Search'(회전 배열·봉우리·용량 최소화), 『이것이 취업을 위한 코딩테스트다』의 '이진탐색' 파트.
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 탐색 경로 출력 | Easy | 닫힌 구간 이진탐색 과정 | 반복 훈련 |
| 2 | 회원 번호 조회 | Easy | 정렬 후 존재 여부 다중 질의 | 반복 훈련 (백준 '이분 탐색' 단계 스타일) |
| 3 | 정수 세제곱근 | Easy | 답 범위 이진탐색(단조 술어) | 반복 훈련 |
| 4 | 온도 구간 관측 횟수 | Medium | lower/upper bound 직접 구현·개수 세기 | 반복 훈련 |
| 5 | 가장 가까운 정류장 | Medium | lower bound + 이웃 비교 | 반복 훈련 |
| 6 | 두 상자 합 맞추기 | Medium | 정렬 배열 두 개 + 등장 횟수 | 유형 확장 (NeetCode 'Binary Search'·'Two Pointers' 스타일) |
| 7 | 가래떡 자르기 | Medium | 파라메트릭(참인 최댓값) | 유형 확장 (백준 '이분 탐색' 단계 자르기류 스타일) |
| 8 | 택배 배달원 배정 | Hard | 파라메트릭(참인 최솟값) + 탐욕 판정 | 유형 확장 (NeetCode 'Binary Search' 용량 최소화 스타일) |
| 9 | 산봉우리 배열 탐색 | Hard | 봉우리 찾기 + 양쪽 이진탐색 결합 | 유형 확장 (NeetCode 'Binary Search' 스타일) |
| 10 | 회전 배열 다중 질의 | Hard | 회전 횟수 + 인덱스 매핑 이진탐색 | 반복 훈련 |

**문제**

**1) 탐색 경로 출력** · Easy

- **요구사항**: 오름차순으로 정렬된 서로 다른 정수 배열과 목표값이 주어진다. 닫힌 구간 이진탐색(`lo=0`, `hi=n-1`, `mid=(lo+hi)//2`, 같으면 종료, 작으면 `lo=mid+1`, 크면 `hi=mid-1`)을 수행하며 확인한 `arr[mid]` 값들을 순서대로 출력하고, 다음 줄에 찾은 인덱스(없으면 -1)를 출력하라.
- **입력**: 첫 줄 n(1 ≤ n ≤ 1000), 둘째 줄 오름차순 정수 n개, 셋째 줄 목표값.
- **출력**: 첫 줄에 확인한 값들을 공백으로, 둘째 줄에 인덱스 또는 -1.
- **예제**: `7 / 2 5 8 12 16 23 38 / 23` → `12 23` / `5` · `7 / 2 5 8 12 16 23 38 / 7` → `12 5 8` / `-1`
- **셀프체크**: 둘째 예제 — mid=3(12)>7이라 hi=2, mid=1(5)<7이라 lo=2, mid=2(8)>7이라 hi=1, lo>hi로 종료. `mid`를 `(lo+hi+1)//2`로 쓰거나 반열린 구간으로 짜면 경로가 달라지니 규칙대로. 원소 1개(`1 / 4 / 4` → `4` / `0`)에서도 한 번은 확인한다.

```runner
@@SOLUTION
import sys
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    arr = [int(data[idx + i]) for i in range(n)]; idx += n
    target = int(data[idx]); idx += 1
    lo, hi = 0, n - 1
    path = []
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        path.append(arr[mid])            # 확인한 값 기록
        if arr[mid] == target:
            ans = mid
            break
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    print(" ".join(map(str, path)))
    print(ans)
main()
@@TESTS
--IN
7
2 5 8 12 16 23 38
23
--OUT
12 23
5
--IN
7
2 5 8 12 16 23 38
7
--OUT
12 5 8
-1
--IN
1
4
4
--OUT
4
0
--IN
8
1 2 3 4 5 6 7 8
8
--OUT
4 6 7 8
7
@@EXPL
(1) 접근·핵심 아이디어

- L1-1의 이진탐색을 그대로 돌리되 "무엇을 확인했는가"를 기록한다. 경로는 구간 규칙(닫힌 구간, `(lo+hi)//2`)에 의해 유일하게 정해지므로, 규칙을 한 글자도 바꾸지 않는 것이 정답의 조건이다.
- 확인 횟수는 최대 약 log₂n + 1이다. 경로를 눈으로 보면 "매번 절반을 버린다"는 감각과 off-by-one(`hi=mid-1`)의 의미가 명확해진다.

(2) 코드 단계별

- `n`, 배열, `target`을 읽고 `lo=0, hi=n-1`, `path=[]`, `ans=-1`.
- 루프 진입마다 `mid` 계산 후 즉시 `path.append(arr[mid])` — 비교 전에 기록해야 마지막(찾은/버린) 확인도 남는다.
- 같으면 `ans=mid`로 종료, 작으면 `lo=mid+1`, 크면 `hi=mid-1`.
- 경로와 인덱스를 두 줄로 출력. 시간 O(log n).

(3) 스스로 다시 짤 때 생각 순서

- 경계 유파(닫힌 구간)를 정하고 `mid` 식을 문제 규칙과 맞춘다 — 다른 유파는 결과 경로가 다르다.
- 기록 시점은 "값을 본 순간" = `mid` 계산 직후.
- 경계 검산: 원소 1개, 목표가 마지막 원소(`1..8`에서 8 → 경로 `4 6 7 8`), 없는 값(-1이지만 경로는 비어 있지 않음).
```

**2) 회원 번호 조회** · Easy

- **요구사항**: 회원 번호 N개(정렬되어 있지 않고 서로 다름)와 조회할 번호 M개가 주어진다. 각 조회 번호가 회원 번호에 있으면 1, 없으면 0을 출력하라. 집합(`set`)이나 `in` 검색을 쓰지 말고, 회원 번호를 정렬한 뒤 직접 구현한 이진탐색으로 각 조회를 O(log N)에 처리한다.
- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 회원 번호 N개, 셋째 줄 M(1 ≤ M ≤ 1000), 넷째 줄 조회 번호 M개(정수 범위 -10^9 ~ 10^9).
- **출력**: 조회 순서대로 1 또는 0을 공백으로 구분해 한 줄로.
- **예제**: `6 / 41 7 19 3 25 12 / 5 / 19 4 41 26 3` → `1 0 1 0 1` · `1 / 7 / 2 / 7 8` → `1 0`
- **셀프체크**: 정렬을 빼먹으면 이진탐색이 틀린 답을 낸다(정렬은 한 번만, 조회마다 하지 않는다). 최솟값보다 작거나 최댓값보다 큰 조회(`-4`, `101`)에서 0이 나오는가. 출력 순서는 조회 입력 순서 그대로.

```runner
@@SOLUTION
import sys
def exists(arr, x):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == x:
            return 1
        elif arr[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return 0
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    members = [int(data[idx + i]) for i in range(n)]; idx += n
    m = int(data[idx]); idx += 1
    queries = [int(data[idx + i]) for i in range(m)]; idx += m
    members.sort()                       # 이진탐색 전제: 정렬
    print(" ".join(str(exists(members, q)) for q in queries))
main()
@@TESTS
--IN
6
41 7 19 3 25 12
5
19 4 41 26 3
--OUT
1 0 1 0 1
--IN
1
7
2
7 8
--OUT
1 0
--IN
4
100 -3 50 0
4
-3 -4 101 100
--OUT
1 0 0 1
@@EXPL
(1) 접근·핵심 아이디어

- "여러 번 존재 여부를 묻는다"면 전처리 1회(정렬 O(N log N)) 후 질의마다 O(log N)으로 답하는 것이 정석이다. 질의마다 선형으로 훑으면 O(N·M)이라 둘 다 커지면 느리다.
- 이진탐색은 정렬을 전제로 하므로, 입력이 섞여 있으면 반드시 먼저 정렬한다. 이 문제는 값이 서로 다르므로 "찾았다/없다"만 판정하면 된다.

(2) 코드 단계별

- `exists(arr, x)`: 닫힌 구간 이진탐색으로 찾으면 1, 구간이 비면 0을 반환.
- 회원 번호를 읽어 `members.sort()`(한 번만).
- 각 질의에 `exists`를 적용해 결과를 공백으로 이어 출력.
- 시간 O(N log N + M log N), 공간 O(N).

(3) 스스로 다시 짤 때 생각 순서

- "다중 질의 + 존재 여부" 신호 → 정렬 1회 + 이진탐색 반복.
- 이진탐색 함수를 따로 빼면 질의 루프가 한 줄로 정리된다. 함수의 반환값(1/0)을 출력 형식에 맞춘다.
- 경계 검산: 회원 1명, 최솟값 미만·최댓값 초과 질의, 음수 번호가 섞인 경우의 정렬 순서.
```

**3) 정수 세제곱근** · Easy

- **요구사항**: 음이 아닌 정수 x가 주어질 때 `m³ ≤ x`를 만족하는 가장 큰 정수 m(세제곱근의 정수부)을 이진탐색으로 구하라. 부동소수 연산(`** (1/3)`, `math`)은 오차가 있으니 쓰지 말고 정수 곱만 사용한다.
- **입력**: 한 줄에 정수 x(0 ≤ x ≤ 10^18).
- **출력**: 세제곱근의 정수부.
- **예제**: `27` → `3` · `100` → `4`
- **셀프체크**: 술어 `mid*mid*mid <= x`는 mid가 커질수록 True→False로 한 번만 바뀐다(참인 최댓값 문제). 탐색 범위 `[0, x]`에서 x=0이면 답 0, x=1~7이면 1(`7` → `1`). x=10^18일 때 답이 정확히 10^6인가(부동소수로 풀면 999999.999…로 어긋날 수 있다).

```runner
@@SOLUTION
import sys
def main():
    x = int(sys.stdin.read().split()[0])
    lo, hi = 0, x
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid * mid <= x:         # 조건 참 → 답 후보, 더 큰 값 시도
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    print(ans)
main()
@@TESTS
--IN
27
--OUT
3
--IN
100
--OUT
4
--IN
0
--OUT
0
--IN
1000000000000000000
--OUT
1000000
@@EXPL
(1) 접근·핵심 아이디어

- L1-2(제곱근)와 같은 구조로, 배열이 아니라 "답의 후보 `[0, x]`"에 이진탐색을 건다. 술어 `mid³ <= x`는 단조(참…참 거짓…거짓)이므로 참인 가장 큰 mid가 답이다.
- 정수 곱만 쓰면 파이썬 정수는 임의 정밀도라 10^54 크기의 `mid³`도 정확하다. 부동소수 세제곱근은 완전세제곱수 근처에서 1 작게 나오는 오차가 흔하다.

(2) 코드 단계별

- `lo=0, hi=x`, `ans=0`.
- `mid³ <= x`면 `ans=mid`로 기록하고 `lo=mid+1`(더 큰 후보), 아니면 `hi=mid-1`.
- 루프 종료 후 `ans` 출력. 반복 횟수는 약 log₂(10^18) ≈ 60회.

(3) 스스로 다시 짤 때 생각 순서

- "무엇에 이진탐색?" → 정수 후보 m. "술어?" → `m³ <= x`. "참인 최댓값인가 최솟값인가?" → 최댓값.
- 참일 때 `ans` 갱신 + 오른쪽으로, 거짓일 때 왼쪽으로. 이 틀은 파라메트릭 서치 전부에 재사용된다.
- 경계: x=0(답 0), x=1(답 1), 완전세제곱수(27→3)와 그 직전 값(26→2).
```

**4) 온도 구간 관측 횟수** · Medium

- **요구사항**: 관측된 온도 N개(정렬되어 있지 않고 중복 가능)와 Q개의 구간 질의 `x y`가 주어진다. 각 질의에 대해 `x ≤ 온도 ≤ y`인 관측의 개수를 출력하라. `bisect` 모듈 없이 lower bound(`x` 이상 첫 위치)와 upper bound(`y` 초과 첫 위치)를 직접 구현해 `upper(y) - lower(x)`로 O(log N)에 답한다.
- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 온도 N개(정수), 셋째 줄 Q(1 ≤ Q ≤ 1000), 다음 Q줄에 `x y`(x ≤ y).
- **출력**: 질의마다 개수를 한 줄씩.
- **예제**: `8 / 23 19 31 25 19 28 22 31 / 3 / 19 25 / 30 40 / 26 27` → `5` / `2` / `0` · `3 / 5 5 5 / 2 / 5 5 / 6 9` → `3` / `0`
- **셀프체크**: 정렬하면 `19 19 22 23 25 28 31 31`. [19,25]는 lower(19)=0, upper(25)=5 → 5. 두 함수의 부등호(`<` vs `<=`) 하나 차이가 "이상/초과"를 가른다. `hi`를 `n-1`이 아니라 `n`으로 두어야 "전부 y 이하"일 때 upper가 n이 된다. 구간 안에 값이 하나도 없으면 두 경계가 같은 위치를 가리켜 0.

```runner
@@SOLUTION
import sys
def lower_bound(arr, x):                 # arr[i] >= x 인 첫 i
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo
def upper_bound(arr, x):                 # arr[i] > x 인 첫 i
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    temps = [int(data[idx + i]) for i in range(n)]; idx += n
    q = int(data[idx]); idx += 1
    temps.sort()
    out = []
    for _ in range(q):
        x = int(data[idx]); y = int(data[idx + 1]); idx += 2
        out.append(str(upper_bound(temps, y) - lower_bound(temps, x)))
    print("\n".join(out))
main()
@@TESTS
--IN
8
23 19 31 25 19 28 22 31
3
19 25
30 40
26 27
--OUT
5
2
0
--IN
3
5 5 5
2
5 5
6 9
--OUT
3
0
--IN
4
-2 0 3 9
2
-10 100
4 8
--OUT
4
0
@@EXPL
(1) 접근·핵심 아이디어

- 정렬 배열에서 "x 이상 y 이하"의 개수는 `(y 이하 개수) - (x 미만 개수)` = `upper_bound(y) - lower_bound(x)`다. 두 경계는 L2의 반열린 구간 골격으로 각각 O(log N)에 구한다.
- lower는 `arr[mid] < x`일 때 오른쪽으로(아직 부족), upper는 `arr[mid] <= x`일 때 오른쪽으로(같아도 넘어감). 이 등호 하나가 "이상"과 "초과"를 구분한다.

(2) 코드 단계별

- `lower_bound`/`upper_bound`를 반열린 구간 `[0, n)`, `while lo < hi`, `hi = mid`로 구현.
- 온도 배열을 읽어 한 번 정렬.
- 질의마다 `x, y`를 읽고 `upper_bound(temps, y) - lower_bound(temps, x)`를 기록.
- 줄 단위로 출력. 시간 O(N log N + Q log N).

(3) 스스로 다시 짤 때 생각 순서

- "구간 개수" → 두 경계의 차. 어느 쪽이 lower(x)이고 어느 쪽이 upper(y)인지 부등호 방향으로 확정한다.
- 반열린 구간을 쓰면 `hi=mid`가 안전하고, `hi`의 초기값 `n`이 "모두 조건 미달"을 자연스럽게 표현한다.
- 검산: 전부 같은 값에서 `[5,5]` → N, 배열 전체를 덮는 구간 → N, 값 사이 빈 구간 → 0.
```

**5) 가장 가까운 정류장** · Medium

- **요구사항**: 직선 도로 위 정류장 위치 N개가 오름차순(서로 다름)으로 주어진다. Q개의 질의 위치 p에 대해 |정류장 − p|가 가장 작은 정류장의 위치를 출력하라. 거리가 같으면 위치가 작은 쪽을 고른다. 각 질의를 O(log N)에 처리한다(lower bound로 삽입 위치를 찾고 양 이웃만 비교).
- **입력**: 첫 줄 N(1 ≤ N ≤ 1000), 둘째 줄 정류장 위치 N개(오름차순 정수), 셋째 줄 Q(1 ≤ Q ≤ 1000), 넷째 줄 질의 위치 Q개.
- **출력**: 질의 순서대로 정류장 위치를 공백으로 구분해 한 줄로.
- **예제**: `5 / 1 4 9 15 20 / 4 / 10 2 17 25` → `9 1 15 20` · `3 / 2 6 10 / 2 / 4 8` → `2 6`
- **셀프체크**: lower bound `k`가 0이면 왼쪽 이웃이 없고(`stops[0]`), `k == N`이면 오른쪽 이웃이 없다(`stops[N-1]`) — 이 두 경계를 먼저 처리해야 인덱스 오류가 없다. 동률(`4`는 2와 6에서 거리 2)은 `<=`로 왼쪽을 우선. p가 정류장과 정확히 같으면 그 정류장 자신(거리 0).

```runner
@@SOLUTION
import sys
def lower_bound(arr, x):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    stops = [int(data[idx + i]) for i in range(n)]; idx += n
    q = int(data[idx]); idx += 1
    out = []
    for _ in range(q):
        p = int(data[idx]); idx += 1
        k = lower_bound(stops, p)        # p 이상인 첫 정류장
        if k == 0:
            best = stops[0]              # 왼쪽 이웃 없음
        elif k == n:
            best = stops[n - 1]          # 오른쪽 이웃 없음
        else:
            left, right = stops[k - 1], stops[k]
            if p - left <= right - p:    # 동률이면 작은 위치(왼쪽)
                best = left
            else:
                best = right
        out.append(str(best))
    print(" ".join(out))
main()
@@TESTS
--IN
5
1 4 9 15 20
4
10 2 17 25
--OUT
9 1 15 20
--IN
3
2 6 10
2
4 8
--OUT
2 6
--IN
2
5 8
3
0 5 100
--OUT
5 5 8
@@EXPL
(1) 접근·핵심 아이디어

- 정렬 배열에서 p에 가장 가까운 값은 "p 이상인 첫 원소"(lower bound)와 "그 바로 왼쪽 원소" 둘 중 하나다. 그 사이에 p가 끼어 있으므로 다른 원소는 이 둘보다 멀 수밖에 없다. 따라서 lower bound 한 번 + 이웃 두 개 비교로 O(log N).
- 동률 규칙(작은 위치 우선)은 비교 연산자 `<=`로 왼쪽을 먼저 택하면 된다.

(2) 코드 단계별

- `lower_bound(stops, p)`로 `k`를 구한다.
- `k == 0`이면 왼쪽 이웃이 없으므로 `stops[0]`, `k == n`이면 오른쪽 이웃이 없으므로 `stops[n-1]`.
- 그 외엔 `stops[k-1]`, `stops[k]`의 거리를 비교해 `p - left <= right - p`면 왼쪽.
- 질의 순서대로 공백 출력. 시간 O(Q log N).

(3) 스스로 다시 짤 때 생각 순서

- "가장 가까운" = 삽입 위치의 양 이웃 후보 2개로 줄인다.
- 경계 두 개(`k==0`, `k==n`)를 먼저 분기해 인덱스 범위를 안전하게 만든 뒤 일반 경우를 쓴다.
- 동률 규칙을 부등호 하나로 표현하고, p가 정류장과 일치하는 경우(거리 0, 오른쪽 후보가 곧 정답이지만 `<=` 때문에 왼쪽이 뽑히지 않는지) 검산한다 — `p == stops[k]`면 `right - p = 0`이므로 `p - left <= 0`은 거짓, 오른쪽이 정확히 선택된다.
```

**6) 두 상자 합 맞추기** · Medium

- **요구사항**: 오름차순으로 정렬된 두 정수 배열 A(길이 N)와 B(길이 M)가 주어진다(각각 중복 가능). 목표합 S에 대해 `A[i] + B[j] == S`인 쌍 (i, j)의 개수를 출력하라. A의 각 원소마다 B에서 `S − A[i]`의 등장 횟수를 이진탐색(lower/upper bound 직접 구현)으로 구해 합산한다.
- **입력**: 첫 줄 N M S(1 ≤ N, M ≤ 1000, |S| ≤ 10^9), 둘째 줄 A의 원소 N개, 셋째 줄 B의 원소 M개.
- **출력**: 쌍의 개수 하나.
- **예제**: `4 5 7 / 1 2 3 4 / 3 3 4 5 6` → `5` · `3 3 100 / 1 2 3 / 1 2 3` → `0`
- **셀프체크**: 첫 예제 — 1은 6(1개), 2는 5(1개), 3은 4(1개), 4는 3(2개) → 5. B에 같은 값이 여러 개일 때 "존재 여부"만 세면 틀린다(등장 횟수 = upper − lower). S − A[i]가 B의 범위 밖이면 두 경계가 같아 0. 음수가 섞여도(`3 4 0 / -2 -1 0 / -2 0 1 2` → `3`) 정렬 순서만 맞으면 동작.

```runner
@@SOLUTION
import sys
def lower_bound(arr, x):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo
def upper_bound(arr, x):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); s = int(data[idx + 2]); idx += 3
    a = [int(data[idx + i]) for i in range(n)]; idx += n
    b = [int(data[idx + i]) for i in range(m)]; idx += m
    total = 0
    for x in a:
        need = s - x                     # b에서 찾을 값
        total += upper_bound(b, need) - lower_bound(b, need)   # 등장 횟수
    print(total)
main()
@@TESTS
--IN
4 5 7
1 2 3 4
3 3 4 5 6
--OUT
5
--IN
3 3 100
1 2 3
1 2 3
--OUT
0
--IN
1 1 4
2
2
--OUT
1
--IN
3 4 0
-2 -1 0
-2 0 1 2
--OUT
3
@@EXPL
(1) 접근·핵심 아이디어

- 합이 S인 쌍은 A의 원소 x를 고정하면 B에서 `S - x`를 찾는 문제로 바뀐다. B가 정렬돼 있으니 `S - x`의 등장 횟수를 `upper_bound - lower_bound`로 O(log M)에 얻고, A 전체에 대해 합산하면 O(N log M)이다. 이중 루프 O(N·M)보다 빠르다.
- 존재 여부(0/1)가 아니라 "횟수"를 세야 하는 이유: B에 같은 값이 여러 개면 각각이 서로 다른 쌍이기 때문이다.

(2) 코드 단계별

- L2 골격의 `lower_bound`, `upper_bound`를 정의.
- A의 각 `x`에 대해 `need = s - x`, `total += upper(b, need) - lower(b, need)`.
- `total` 출력. 공간 O(1) 추가.

(3) 스스로 다시 짤 때 생각 순서

- "두 배열 + 합" → 한쪽을 고정하고 다른 쪽에서 보수를 탐색한다.
- 정렬 배열에서 값의 개수는 두 경계의 차 — L2-1과 같은 도구를 그대로 쓴다.
- 경계: 답이 0인 경우(보수가 범위 밖), 원소 1개씩, 음수·0이 섞인 경우. 두 배열이 같은 배열일 때도 (i, j)는 서로 다른 배열의 인덱스이므로 그대로 센다.
```

**7) 가래떡 자르기** · Medium

- **요구사항**: 길이가 다른 가래떡 N개를 모두 같은 정수 길이 L로 잘라 조각을 만든다(각 가래떡에서 `길이 // L`개가 나오고 남는 부분은 버린다). 조각을 최소 M개 이상 얻을 수 있는 L의 최댓값을 구하라. 가래떡 길이의 합은 M 이상이라 L=1은 항상 가능하다.
- **입력**: 첫 줄 N M(1 ≤ N ≤ 1000, 1 ≤ M ≤ 10^9), 둘째 줄 가래떡 길이 N개(1 ≤ 길이 ≤ 10^9).
- **출력**: L의 최댓값.
- **예제**: `3 7 / 30 14 22` → `7` · `2 3 / 10 10` → `5`
- **셀프체크**: 첫 예제 — L=7이면 4+2+3=9 ≥ 7 가능, L=8이면 3+1+2=6 < 7 불가. 술어 "조각 수 ≥ M"은 L이 커질수록 True→False로 단조 감소하므로 참인 최댓값 문제. 탐색 범위는 `[1, max(길이)]`(0은 나눗셈 오류). `1 5 / 5` → 1, `1 1 / 1000` → 1000처럼 양 끝값이 답인 경우도 확인.

```runner
@@SOLUTION
import sys
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); idx += 2
    rice = [int(data[idx + i]) for i in range(n)]; idx += n
    lo, hi = 1, max(rice)
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        pieces = sum(r // mid for r in rice)    # 길이 mid로 잘랐을 때 조각 수
        if pieces >= m:                  # 충분 → 더 길게 시도
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    print(ans)
main()
@@TESTS
--IN
3 7
30 14 22
--OUT
7
--IN
2 3
10 10
--OUT
5
--IN
1 5
5
--OUT
1
--IN
1 1
1000
--OUT
1000
@@EXPL
(1) 접근·핵심 아이디어

- 답 L 자체를 후보 범위 `[1, max(길이)]`에서 이진탐색한다(파라메트릭 서치). 판정 `f(L) = (조각 수 ≥ M)`은 L이 길어질수록 조각이 줄어 True→False로 한 번만 바뀐다. 따라서 True를 유지하는 가장 큰 L을 찾는다 — L2-3(나무 자르기)과 같은 "참인 최댓값" 틀.
- 판정 비용은 O(N)이고 반복은 약 log₂(10^9) ≈ 30회라 전체 O(N log(max)).

(2) 코드 단계별

- `lo=1, hi=max(rice)`, `ans=0`.
- `mid`로 잘랐을 때 `pieces = sum(r // mid for r in rice)`.
- `pieces >= m`이면 `ans=mid`, `lo=mid+1`(더 긴 길이 시도), 아니면 `hi=mid-1`.
- `ans` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "최대 L을 구하되 조건은 조각 수" → 배열이 아니라 답에 이진탐색.
- 단조성 방향(L↑ ⇒ 조각↓)을 확인해 참일 때 오른쪽으로 간다.
- 경계: `lo`는 0이 아닌 1(0으로 나누기 방지), 답이 `max(길이)` 자체인 경우(가래떡 하나, M=1), 답이 1인 경우.
```

**8) 택배 배달원 배정** · Hard

- **요구사항**: 상자 N개의 무게가 배송 순서대로 주어진다. 이 순서를 유지한 채 연속 구간으로 나눠 K명의 배달원에게 배정한다(각 배달원은 1개 이상, 구간은 이어져야 한다). 배달원 중 가장 무거운 적재량(구간 무게 합)을 최소화할 때 그 값을 출력하라.
- **입력**: 첫 줄 N K(1 ≤ K ≤ N ≤ 1000), 둘째 줄 상자 무게 N개(1 ≤ 무게 ≤ 10^6).
- **출력**: 최대 적재량의 최솟값.
- **예제**: `5 2 / 7 2 5 10 8` → `18` · `5 3 / 1 2 3 4 5` → `6`
- **셀프체크**: 첫 예제 — 한도 18이면 `[7,2,5] [10,8]` 2명으로 가능, 17이면 `[7,2,5] [10] [8]` 3명 필요. 판정은 탐욕: 한도 C를 두고 앞에서부터 담다가 넘치면 새 배달원. 필요 인원이 K 이하면 가능(인원이 남으면 구간을 더 쪼개도 최대 적재량은 늘지 않는다). 탐색 범위 하한은 `max(무게)`(한 상자는 쪼갤 수 없음), 상한은 `sum(무게)`. K=N이면 답은 `max`, K=1이면 `sum`.

```runner
@@SOLUTION
import sys
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); k = int(data[idx + 1]); idx += 2
    w = [int(data[idx + i]) for i in range(n)]; idx += n
    lo, hi = max(w), sum(w)
    ans = hi
    while lo <= hi:
        mid = (lo + hi) // 2
        groups = 1                       # 적재 한도 mid로 필요한 배달원 수
        load = 0
        for x in w:
            if load + x > mid:
                groups += 1
                load = x
            else:
                load += x
        if groups <= k:                  # 가능 → 한도를 더 줄여 본다
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    print(ans)
main()
@@TESTS
--IN
5 2
7 2 5 10 8
--OUT
18
--IN
5 3
1 2 3 4 5
--OUT
6
--IN
3 3
4 9 2
--OUT
9
--IN
4 1
1 1 1 1
--OUT
4
@@EXPL
(1) 접근·핵심 아이디어

- "최대값을 최소화"는 파라메트릭 서치의 대표 신호다. 답(적재 한도 C)을 고정하면 "C로 K명 이하에 배정 가능한가"는 C가 커질수록 False→True로 단조 증가하므로, 참인 최솟값을 이진탐색한다 — 앞 문제들과 반대로 참일 때 `hi = mid - 1`.
- 판정은 탐욕이 최적이다: 순서를 유지해야 하므로 앞에서부터 한도까지 꽉 채우고 넘치면 새 사람에게 넘기는 것이 인원을 최소화한다. 인원이 K보다 적게 나와도 구간을 더 쪼개면 되니(최대 적재량은 줄거나 같음) `groups <= k`가 가능 조건이다.

(2) 코드 단계별

- `lo = max(w)`(한 상자보다 작은 한도는 불가능), `hi = sum(w)`(전부 한 명), `ans = hi`.
- `mid`에 대해 탐욕으로 `groups`를 센다: `load + x > mid`면 `groups += 1`, `load = x`.
- `groups <= k`면 `ans = mid`, `hi = mid - 1`; 아니면 `lo = mid + 1`.
- `ans` 출력. 시간 O(N log(sum)).

(3) 스스로 다시 짤 때 생각 순서

- "최대의 최소" → 답에 이진탐색, 술어는 "이 한도로 K명 안에 되는가".
- 단조성 방향이 앞 문제들과 반대(C↑ ⇒ 가능)이므로 참일 때 왼쪽으로 좁힌다.
- 하한을 0이나 1로 잡으면 판정에서 한 상자가 한도를 넘어 `load = x`가 한도 초과인 채로 진행되는 함정 — 반드시 `max(w)`. K=N(답 max), K=1(답 sum)로 양 끝 검산.
```

**9) 산봉우리 배열 탐색** · Hard

- **요구사항**: 배열이 어떤 위치(봉우리)까지는 순증가하고 그 뒤로는 순감소한다(봉우리가 맨 앞이나 맨 뒤일 수도 있고, 값은 모두 서로 다르다). 목표값이 주어질 때 봉우리의 인덱스와 목표값의 인덱스(없으면 -1)를 O(log n)에 구하라. 절차: (1) 봉우리를 이진탐색으로 찾고, (2) 오름 구간 `[0, peak]`에서 일반 이진탐색, (3) 없으면 내림 구간 `[peak+1, n-1]`에서 부등호를 뒤집은 이진탐색.
- **입력**: 첫 줄 n(1 ≤ n ≤ 1000), 둘째 줄 배열, 셋째 줄 목표값.
- **출력**: 첫 줄에 봉우리 인덱스, 둘째 줄에 목표값 인덱스 또는 -1.
- **예제**: `7 / 1 4 7 12 9 5 2 / 5` → `3` / `5` · `7 / 1 4 7 12 9 5 2 / 10` → `3` / `-1`
- **셀프체크**: 봉우리 탐색 술어는 `a[mid] < a[mid+1]`(참이면 봉우리는 오른쪽) — 반열린 구간 `while lo < hi`로 짜야 `mid+1`이 범위를 넘지 않는다. 내림 구간에서는 `a[mid] > target`일 때 오른쪽으로 가야 한다(부등호 반전 실수 주의). 순증가만 하는 배열(`1 2 3 4`)은 봉우리가 마지막 인덱스, 순감소만 하는 배열(`9 6 3 1`)은 0.

```runner
@@SOLUTION
import sys
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    a = [int(data[idx + i]) for i in range(n)]; idx += n
    target = int(data[idx]); idx += 1
    # 1) 봉우리 찾기: a[mid] < a[mid+1] 이면 봉우리는 오른쪽
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < a[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    peak = lo
    ans = -1
    # 2) 오름 구간 [0, peak]
    lo, hi = 0, peak
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            ans = mid
            break
        elif a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    # 3) 내림 구간 [peak+1, n-1] (부등호 반대)
    if ans == -1:
        lo, hi = peak + 1, n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if a[mid] == target:
                ans = mid
                break
            elif a[mid] > target:
                lo = mid + 1
            else:
                hi = mid - 1
    print(peak)
    print(ans)
main()
@@TESTS
--IN
7
1 4 7 12 9 5 2
5
--OUT
3
5
--IN
7
1 4 7 12 9 5 2
10
--OUT
3
-1
--IN
1
5
5
--OUT
0
0
--IN
4
9 6 3 1
9
--OUT
0
0
@@EXPL
(1) 접근·핵심 아이디어

- 배열 전체는 정렬돼 있지 않지만 "봉우리 왼쪽은 오름차순, 오른쪽은 내림차순"이라는 구조가 있다. 그래서 세 번의 이진탐색으로 나눈다: 봉우리 위치 찾기, 오름 구간 탐색, 내림 구간 탐색. 각각 O(log n)이므로 전체도 O(log n).
- 봉우리 찾기의 술어 `a[mid] < a[mid+1]`은 "아직 오르막" — 참이면 봉우리는 mid보다 오른쪽에 있고, 거짓이면 mid 자신이거나 왼쪽이다. 반열린 골격(`while lo < hi`, `hi = mid`)으로 첫 거짓 위치를 찾으면 그것이 봉우리다.

(2) 코드 단계별

- 봉우리: `lo=0, hi=n-1`, `a[mid] < a[mid+1]`면 `lo=mid+1`, 아니면 `hi=mid`. 종료 시 `peak = lo`.
- 오름 구간 `[0, peak]`에서 표준 이진탐색.
- 못 찾았으면 내림 구간 `[peak+1, n-1]`에서 `a[mid] > target`일 때 `lo=mid+1`(값이 오른쪽으로 갈수록 작아지므로).
- `peak`와 `ans`를 두 줄로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "부분적으로 정렬" → 정렬된 조각으로 쪼개서 각각 이진탐색. 먼저 경계(봉우리)를 이진탐색으로 찾는다.
- 봉우리 탐색은 `mid+1` 접근 때문에 `while lo < hi`가 안전하다(`lo <= hi`면 `mid = n-1`에서 범위 초과).
- 내림 구간은 부등호만 뒤집는다. n=1(봉우리 0, 내림 구간 없음), 순증가·순감소 배열로 경계 검산.
```

**10) 회전 배열 다중 질의** · Hard

- **요구사항**: 서로 다른 정수의 오름차순 배열을 오른쪽으로 r칸 회전한 배열이 주어진다(r은 알려지지 않았고 0 ≤ r < n). 먼저 회전 횟수 r(= 최솟값의 인덱스)을 이진탐색으로 구해 첫 줄에 출력하고, 이어지는 Q개의 목표값 각각에 대해 배열에서의 인덱스(없으면 -1)를 둘째 줄에 출력하라. 각 질의는 "가상의 정렬 배열 인덱스 k ↔ 실제 인덱스 (k + r) % n" 대응을 이용해 O(log n)에 처리한다.
- **입력**: 첫 줄 n(1 ≤ n ≤ 1000), 둘째 줄 회전된 배열, 셋째 줄 Q(1 ≤ Q ≤ 1000), 넷째 줄 목표값 Q개.
- **출력**: 첫 줄에 r, 둘째 줄에 질의 순서대로 인덱스(또는 -1)를 공백으로.
- **예제**: `7 / 15 18 2 3 6 12 14 / 3 / 6 15 7` → `2` / `4 0 -1` · `4 / 1 3 5 7 / 2 / 7 1` → `0` / `3 0`
- **셀프체크**: 최솟값 탐색 술어는 `a[mid] > a[hi]`(참이면 최솟값은 mid 오른쪽) — `a[lo]`와 비교하면 회전 0에서 틀리는 함정. 회전 0(`1 3 5 7`)이면 r=0이고 매핑은 항등. 질의 탐색에서는 비교 대상이 `a[(mid + r) % n]`이고, 답으로 출력할 것은 가상 인덱스 mid가 아니라 실제 인덱스라는 점에 주의. n=1은 r=0.

```runner
@@SOLUTION
import sys
def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    a = [int(data[idx + i]) for i in range(n)]; idx += n
    q = int(data[idx]); idx += 1
    # 1) 회전 횟수 = 최솟값 인덱스
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] > a[hi]:               # 최솟값은 mid 오른쪽
            lo = mid + 1
        else:
            hi = mid
    r = lo
    # 2) 가상의 정렬 배열 인덱스 k → 실제 인덱스 (k + r) % n
    out = []
    for _ in range(q):
        t = int(data[idx]); idx += 1
        lo, hi = 0, n - 1
        ans = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            real = (mid + r) % n
            if a[real] == t:
                ans = real
                break
            elif a[real] < t:
                lo = mid + 1
            else:
                hi = mid - 1
        out.append(str(ans))
    print(r)
    print(" ".join(out))
main()
@@TESTS
--IN
7
15 18 2 3 6 12 14
3
6 15 7
--OUT
2
4 0 -1
--IN
4
1 3 5 7
2
7 1
--OUT
0
3 0
--IN
1
9
1
9
--OUT
0
0
--IN
5
5 1 2 3 4
3
5 4 0
--OUT
1
0 4 -1
@@EXPL
(1) 접근·핵심 아이디어

- L1-3은 질의 하나를 "정렬된 절반 판정"으로 풀었다. 질의가 많으면 회전 횟수 r을 한 번만 구해 두고, 이후엔 "가상의 정렬 배열"에 표준 이진탐색을 거는 것이 깔끔하다. 가상 인덱스 k의 실제 위치는 `(k + r) % n`이므로 비교할 때만 이 매핑을 거치면 된다.
- r은 최솟값의 인덱스다. 술어 `a[mid] > a[hi]`가 참이면 mid는 회전된 앞부분(큰 값들)에 있어 최솟값이 오른쪽에 있고, 거짓이면 mid 이하 어딘가에 있다. 반열린 골격으로 첫 거짓 위치를 찾는다.

(2) 코드 단계별

- 최솟값: `lo=0, hi=n-1`, `a[mid] > a[hi]`면 `lo=mid+1`, 아니면 `hi=mid`. 종료 시 `r = lo`.
- 각 질의: 가상 구간 `[0, n-1]`에서 `real = (mid + r) % n`으로 실제 값을 읽어 표준 세 갈래 비교.
- 찾으면 `ans = real`(실제 인덱스), 못 찾으면 -1.
- `r`과 질의 결과를 두 줄로 출력. 시간 O((1 + Q) log n).

(3) 스스로 다시 짤 때 생각 순서

- "회전 배열 + 다중 질의" → 회전 횟수를 먼저 한 번 구하고 매핑으로 정렬 배열처럼 다룬다.
- 최솟값 탐색은 `a[hi]`와 비교해야 회전 0에서도 맞다(`a[lo]` 비교는 `1 3 5 7`에서 `a[mid] > a[lo]`가 참이라 오른쪽으로 잘못 간다).
- 출력은 가상 인덱스가 아니라 실제 인덱스. 회전 0, n=1, 최솟값·최댓값이 질의인 경우(`5 1 2 3 4`에서 5 → 0, 4 → 4)로 검산.
```
