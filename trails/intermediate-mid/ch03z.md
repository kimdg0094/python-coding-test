## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터는 "정렬된 배열에서 값 찾기"로 시작해 "정답 자체를 축에 놓고 이진탐색하기"로 끝났다. 두 레슨을 한 장으로 잇고, 바로 쓸 수 있는 골격과 실수 목록으로 마무리한다.

**개념 지도**

```text
   binary search on an INDEX            binary search on the ANSWER
   ------------------------            ---------------------------
   sorted array a[0..n-1]              answer range [LO, HI]
   test  : a[mid] < x ?                test  : ok(mid) ?
   result: a position                  result: the optimal value
                \                       /
                 \                     /
                  v                   v
        same engine : find where a monotone T/F strip flips

   ok(X) monotone ?
     |
     +-- no  -> parametric search does NOT apply  (DP / brute force)
     |
     +-- yes -> T..T F..F  ->  answer = LAST  T   (maximise)
                F..F T..T  ->  answer = FIRST T   (minimise)
                integer axis -> while lo <= hi
                real    axis -> repeat a fixed number of times
```

왼쪽 갈래(인덱스 이진탐색)는 lower_bound / upper_bound로 굳어졌고, 오른쪽 갈래(정답 이진탐색)가 파라메트릭 서치다. **엔진은 같고 축만 다르다.** 그래서 L1에서 익힌 경계 감각이 그대로 L2의 정확도가 된다.

**뼈대 코드**

경계 탐색 — 반열린 구간 `[lo, hi)`. 실전에서는 `bisect`를 쓰지만, 직접 짤 수 있어야 변형이 가능하다.

```python
def lower_bound(a, x):        # a[i] >= x 인 첫 인덱스
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:        # ← 문제마다 바뀜: 버릴 조건
            lo = mid + 1
        else:
            hi = mid
    return lo
# upper_bound는 조건만 a[mid] <= x 로 바꾼다
```

파라메트릭 — **최댓값**을 찾는 형태(`T..T F..F`, 마지막 T가 답).

```python
def feasible(X):              # ← 문제마다 바뀜: O(N) 정도의 예/아니오 판정
    ...
    return True

lo, hi = LO, HI               # ← 문제마다 바뀜: 답이 가질 수 있는 최소/최대
ans = -1                      # 한 번도 성공 못 할 수 있으면 실패값으로
while lo <= hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        ans = mid             # 성공 → 더 크게 노려본다
        lo = mid + 1
    else:
        hi = mid - 1
print(ans)
```

파라메트릭 — **최솟값**을 찾는 형태(`F..F T..T`, 첫 T가 답). 위와 딱 두 줄만 다르다.

```python
lo, hi = LO, HI               # ← 문제마다 바뀜
ans = HI                      # 전 구간이 실패면 남을 값
while lo <= hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        ans = mid             # 성공 → 더 작게 노려본다
        hi = mid - 1          # ← 최댓값 형태와 반대 방향
    else:
        lo = mid + 1
print(ans)
```

답이 실수일 때 — 경계가 없으므로 **고정 횟수**로 돌린다.

```python
lo, hi = 0.0, 1e9             # ← 문제마다 바뀜
for _ in range(100):          # 한 번에 오차가 절반 → 100회면 충분
    mid = (lo + hi) / 2
    if feasible(mid):
        lo = mid              # 최댓값 형태(성공이면 오른쪽을 남긴다)
    else:
        hi = mid
print("%.6f" % lo)            # ← 문제마다 바뀜: 요구 정밀도
```

정렬이 선행돼야 할 때 쓰는 최소 조합.

```python
a.sort()                      # 이진탐색의 전제: 단조성
import bisect
lo = bisect.bisect_left(a, x)     # lower_bound
up = bisect.bisect_right(a, x)    # upper_bound
cnt = up - lo                     # x의 등장 횟수
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 정렬된 배열에서 값의 존재·위치·개수 | `bisect_left` / `bisect_right` | 경계 두 개면 개수까지 나온다 | O(log N) |
| "x 이상이 처음 나오는 위치" 같은 경계 질문 | 반열린 `[lo, hi)` 이진탐색 | 불변식이 가장 단순해 off-by-one이 적다 | O(log N) |
| "조건을 만족하는 최댓값" | 닫힌 구간 + 성공 시 `lo = mid + 1` | `T..T F..F`의 마지막 T가 답 | O(N log R) |
| "조건을 만족하는 최솟값", "최대를 최소로" | 닫힌 구간 + 성공 시 `hi = mid - 1` | `F..F T..T`의 첫 T가 답 | O(N log R) |
| 답이 실수(소수점 정밀도 요구) | 고정 횟수 실수 이분 | 정수 경계가 없어 종료 조건을 못 만든다 | O(N · 100) |
| 판정이 O(N)보다 비싼데 N이 크다 | 판정을 먼저 최적화(누적합·그리디) | 판정 비용이 그대로 곱해진다 | 판정 × log R |
| `ok(X)`가 단조가 아니다 | 파라메트릭 금지 → 완전탐색·DP | 경계가 여러 개라 아무 데나 수렴한다 | 문제에 따름 |
| 배열이 회전·부분정렬 등 변형 | "어느 절반이 정렬됐나"를 먼저 판정 | 정렬된 절반에서만 범위 비교가 안전하다 | O(log N) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 이진탐색의 불변식("정답은 항상 현재 구간 안에 있다")이 무엇이고, `lo`·`hi` 갱신이 그것을 어떻게 지키는지.
- [ ] 설명할 수 있다: lower_bound와 upper_bound의 정의 차이와, 왜 `upper - lower`가 등장 횟수인지.
- [ ] 설명할 수 있다: 반열린 `[lo, hi)`와 닫힌 `[lo, hi]` 컨벤션의 차이, 그리고 왜 하나만 골라 써야 하는지.
- [ ] 설명할 수 있다: 왜 루프가 반드시 끝나는지(구간 길이가 매번 최소 1 줄어든다는 논증).
- [ ] 설명할 수 있다: 파라메트릭 서치가 "최적화 문제를 결정 문제로 바꾸는" 기법이라는 말의 뜻.
- [ ] 설명할 수 있다: 단조성이 무엇이고, 주어진 판정 함수가 단조인지 **직접 확인하는 절차**.
- [ ] 설명할 수 있다: 단조가 아닌 판정 함수의 예를 하나 만들고, 왜 이진탐색이 거기서 틀리는지.
- [ ] 설명할 수 있다: "최댓값의 최솟값", "적어도 K개" 같은 문구가 왜 파라메트릭 신호인지.
- [ ] 설명할 수 있다: 최댓값 패턴과 최솟값 패턴에서 성공 시 어느 쪽 경계를 미는지와 그 이유.
- [ ] 설명할 수 있다: `lo`, `hi` 초기값을 잡는 기준(답이 가질 수 있는 최소/최대)과, 좁게 잡으면 생기는 오류.
- [ ] 설명할 수 있다: 전체 복잡도가 왜 `판정 비용 × log(범위 크기)`인지.
- [ ] 설명할 수 있다: 실수 이분에서 `while hi - lo > eps` 대신 고정 횟수를 쓰는 이유.
- [ ] 설명할 수 있다: 판정 함수를 부작용 없는 순수 함수로 짜야 하는 이유.

**⚠️ 자주 하는 실수**

**1. 단조성을 확인하지 않고 파라메트릭을 적용한다**

```python
# ❌ 틀린 코드
def feasible(X):
    # "자투리 합이 정확히 X인 분할이 있는가?" — X에 대해 T/F가 들쭉날쭉
    return leftover_sum_exactly(X)

lo, hi, ans = 0, 10**9, -1
while lo <= hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        ans = mid; lo = mid + 1
    else:
        hi = mid - 1
```

왜: 이진탐색은 T/F가 **딱 한 번** 바뀐다는 전제 위에서 절반을 버린다. "정확히 같은가" 류의 판정은 경계가 여러 개라, 버린 절반에 진짜 답이 남아 있어도 알 수 없다.

```python
# ✅ 고친 코드
# 먼저 "X를 1 키우면 판정이 나빠지기만 하는가?"를 확인한다.
def feasible(X):
    # "자투리 합이 X 이상인가" 처럼 한 방향으로만 움직이는 형태로 재정의
    return leftover_sum_at_least(X)      # X가 커지면 T -> F 로만 이동
# 이 형태로 바꿀 수 없으면 파라메트릭이 아니라 DP/완전탐색으로 간다.
```

**2. "성공 시 `lo = mid`"에 내림 `mid`를 써서 무한 루프**

```python
# ❌ 틀린 코드
while lo < hi:
    mid = (lo + hi) // 2      # 내림
    if ok(mid):
        lo = mid              # lo=3, hi=4 이면 mid=3, lo=3 -> 영원히 그대로
    else:
        hi = mid - 1
```

왜: `lo = 3, hi = 4`에서 `mid = (3+4)//2 = 3`이고 성공하면 `lo = 3`. `lo`도 `hi`도 안 움직여 구간이 줄지 않는다.

```python
# ✅ 고친 코드
while lo < hi:
    mid = (lo + hi + 1) // 2  # 올림 — "성공 시 lo=mid"와 반드시 짝
    if ok(mid):
        lo = mid
    else:
        hi = mid - 1
# 또는 ans 변수를 쓰는 닫힌 구간 형태로 통일한다:
#   if ok(mid): ans = mid; lo = mid + 1
```

**3. 최댓값을 찾는데 성공 시 왼쪽으로 민다**

```python
# ❌ 틀린 코드
lo, hi, ans = 1, max(cables), 0
while lo <= hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        ans = mid
        hi = mid - 1          # 최솟값 패턴의 갱신
    else:
        lo = mid + 1
```

왜: `feasible`이 `T..T F..F`이므로 답은 **마지막 T**다. 성공했는데 왼쪽만 남기면 더 큰 T를 영영 못 보고, 답이 작게 나온다.

```python
# ✅ 고친 코드
lo, hi, ans = 1, max(cables), 0
while lo <= hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        ans = mid
        lo = mid + 1          # 최댓값 → 성공하면 더 크게
    else:
        hi = mid - 1
```

**4. `hi` 초기값을 답보다 작게 잡는다**

```python
# ❌ 틀린 코드
# "그룹 합의 최댓값을 최소화" 문제
lo, hi = 1, max(a)            # 한 그룹에 여러 원소가 들어가면 max(a)를 넘는다
```

왜: 답의 상한은 "전부 한 그룹"인 `sum(a)`다. `hi`를 `max(a)`로 두면 정답이 탐색 범위 밖이라, 전 구간이 실패하고 초기 `ans`가 그대로 출력된다.

```python
# ✅ 고친 코드
lo, hi = max(a), sum(a)       # 하한: 최대 원소 하나는 담아야 함
                              # 상한: 전부 한 그룹
```

**5. `lo = 0`으로 시작해 판정 안에서 0으로 나눈다**

```python
# ❌ 틀린 코드
lo, hi = 0, max(cables)
while lo <= hi:
    mid = (lo + hi) // 2
    if sum(c // mid for c in cables) >= k:   # mid가 0이면 ZeroDivisionError
        ...
```

왜: `mid = 0`이 반드시 한 번은 나온다(`lo = 0, hi = 0`인 순간). 판정 함수가 그 값을 다룰 수 없으면 예외로 죽는다.

```python
# ✅ 고친 코드
lo, hi = 1, max(cables)       # 길이는 최소 1
# 또는 판정 안에서 방어한다
def feasible(L):
    if L == 0:
        return True
    return sum(c // L for c in cables) >= k
```

**6. 판정 함수가 원본 데이터를 바꾼다**

```python
# ❌ 틀린 코드
def feasible(X):
    a.sort()                  # 매 호출마다 원본을 건드림
    while a and a[-1] > X:
        a.pop()               # 다음 호출 때는 데이터가 사라져 있다
    return len(a) >= k
```

왜: 이진탐색은 판정을 수십 번 호출한다. 첫 호출이 데이터를 바꿔 놓으면 두 번째 호출부터는 **다른 문제를 푸는 셈**이라 답이 매번 달라진다.

```python
# ✅ 고친 코드
a.sort()                      # 정렬 같은 전처리는 루프 밖에서 한 번만
def feasible(X):              # 읽기만 하는 순수 함수
    return sum(1 for v in a if v <= X) >= k
```

**7. 실수 이분에서 종료 조건을 오차로 준다**

```python
# ❌ 틀린 코드
while hi - lo > 1e-9:         # 부동소수 정밀도 한계에 걸리면 영원히 안 줄어든다
    mid = (lo + hi) / 2
    if feasible(mid):
        lo = mid
    else:
        hi = mid
```

왜: 값이 큰 구간(예: 10^9 근처)에서는 `hi - lo`가 `1e-9`까지 내려가기 전에 두 값이 표현 한계로 붙어 버려 갱신이 멈추고, 조건은 계속 참이라 무한 루프가 된다.

```python
# ✅ 고친 코드
for _ in range(100):          # 횟수 고정 — 오차는 초기 범위의 2^-100배
    mid = (lo + hi) / 2
    if feasible(mid):
        lo = mid
    else:
        hi = mid
print("%.6f" % lo)
```

**다음 챕터로**

파라메트릭 서치의 판정 함수 `feasible(X)`는 대개 **그리디**로 짠다("왼쪽부터 X를 넘지 않게 채우고 그룹 수를 센다"가 그 예다). 다음 챕터에서 그리디의 정당성을 교환 논증으로 증명하는 법을 배우면, 판정 함수가 정말 최적으로 세고 있는지를 스스로 검증할 수 있게 된다.
