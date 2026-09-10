## L6. 병합 정렬

**개념**

- 병합 정렬(merge sort)은 "분할 정복(divide & conquer)"으로 정렬하는 대표 알고리즘이다. 배열을 절반씩 계속 쪼개(divide) 크기 1까지 내려간 뒤, 이미 정렬된 두 조각을 하나로 "합치며(merge)" 올라온다.

- 핵심은 "이미 정렬된 두 배열을 합치는" 병합 단계다. 두 배열의 맨 앞을 가리키는 인덱스 두 개를 두고, 더 작은 쪽을 결과에 꺼내 담고 그 인덱스만 한 칸 전진한다. 한쪽이 끝나면 나머지를 통째로 붙인다. 이 과정은 두 배열 길이 합에 비례해 선형이다.

- 동작 단계: (1) 배열을 가운데에서 좌·우로 나눈다 → (2) 좌·우를 각각 재귀로 정렬한다 → (3) 정렬된 좌·우를 병합해 하나로 만든다. 크기 1 이하이면 이미 정렬된 것으로 보고 그대로 반환한다.

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> merge(const vector<int>& a, const vector<int>& b) { // 정렬된 두 배열을 합쳐 정렬된 하나로
    vector<int> res;
    int i = 0, j = 0;
    while (i < (int)a.size() && j < (int)b.size()) {
        if (a[i] <= b[j]) res.push_back(a[i++]); // '<=' 로 왼쪽 우선 → 안정성 유지
        else res.push_back(b[j++]);
    }
    while (i < (int)a.size()) res.push_back(a[i++]); // 남은 꼬리를 통째로
    while (j < (int)b.size()) res.push_back(b[j++]);
    return res;
}

vector<int> merge_sort(vector<int> arr) {
    if ((int)arr.size() <= 1) return arr;
    int m = arr.size() / 2;
    vector<int> left(arr.begin(), arr.begin() + m);
    vector<int> right(arr.begin() + m, arr.end());
    return merge(merge_sort(left), merge_sort(right));
}
```

**그림으로 보기**

```text
 merge sort on [38, 27, 43, 3, 9, 82, 10]      # 위로 쪼개고 아래로 합친다
 split                                              depth
   [38 27 43 3 9 82 10]                               0
   [38 27 43 3]   [9 82 10]                           1
   [38 27] [43 3]   [9 82] [10]                       2
   [38] [27] [43] [3]   [9] [82] [10]                 3
 merge
   [27 38] [3 43]   [9 82] [10]                       2
   [3 27 38 43]   [9 10 82]                           1
   [3 9 10 27 38 43 82]                               0
```

```text
 merge [3 27 38 43] and [9 10 82]      # <= 로 비교해 왼쪽 우선
   left  right   take           result
   3     9       3 (left)       3
   27    9       9 (right)      3 9
   27    10      10 (right)     3 9 10
   27    82      27 (left)      3 9 10 27
   38    82      38 (left)      3 9 10 27 38
   43    82      43 (left)      3 9 10 27 38 43
   -     82      tail           3 9 10 27 38 43 82
```

**손으로 따라가기**

`{5, 2, 4, 1}`을 병합 정렬한다. 재귀 호출이 언제 반환되는지에 주목한다.

| 단계 | 호출 | 반환 |
|---|---|---|
| 1 | `ms(0,3)` → 좌 `[5,2]` 우 `[4,1]` | 대기 |
| 2 | `ms(0,1)` → `ms(0,0)`, `ms(1,1)` | `[5]`, `[2]` |
| 3 | `merge(0,0,1)` | `[2,5]` |
| 4 | `ms(2,3)` → `ms(2,2)`, `ms(3,3)` | `[4]`, `[1]` |
| 5 | `merge(2,2,3)` | `[1,4]` |
| 6 | `merge(0,1,3)` | `[1,2,4,5]` |

크기 1인 조각은 "이미 정렬됨"이라 바로 반환된다(재귀의 바닥). 그 위로는 오직 병합만 일어난다.

C++에서는 조각을 **잘라 넘기지 않고 인덱스 구간으로 넘긴다.** 복사가 사라지고, 임시 배열도 병합 안에서만 쓰인다.

```cpp
void merge_part(vector<int>& a, int lo, int mid, int hi) {
    vector<int> tmp;
    tmp.reserve(hi - lo + 1);
    int i = lo, j = mid + 1;
    while (i <= mid && j <= hi)
        tmp.push_back(a[i] <= a[j] ? a[i++] : a[j++]);  // <= 가 안정성의 근거
    while (i <= mid) tmp.push_back(a[i++]);             // 남은 꼬리
    while (j <= hi)  tmp.push_back(a[j++]);
    for (int k = 0; k < (int)tmp.size(); k++) a[lo + k] = tmp[k];
}

void merge_sort(vector<int>& a, int lo, int hi) {
    if (lo >= hi) return;                      // 크기 0 또는 1 = 이미 정렬됨
    int mid = lo + (hi - lo) / 2;              // (lo+hi)/2 는 오버플로 위험
    merge_sort(a, lo, mid);
    merge_sort(a, mid + 1, hi);
    merge_part(a, lo, mid, hi);
}
```

**왜 이렇게 되는가**

n log n이 어디서 나오는지 레벨별로 합산해 보자(n = 8로 두면 세기 쉽다).

```text
 work per level (n = 8)
   level 0 : 1 merge  x 8 elems = 8
   level 1 : 2 merges x 4 elems = 8
   level 2 : 4 merges x 2 elems = 8
   level 3 : 8 pieces x 1 elem  = 8
   levels  = log2(8) + 1 = 4      total = 8 x 4 = 32
```

- 어느 레벨에서든 그 레벨의 병합들이 다루는 원소 수를 모두 더하면 정확히 n이다. 조각이 잘게 쪼개져도 원소 총수는 변하지 않기 때문이다.
- 병합은 두 구간을 한 번씩 훑는 선형 연산이므로 한 레벨의 비용은 O(n).
- 레벨 수는 n을 절반씩 나눠 1이 될 때까지의 횟수, 즉 log2 n이다.
- 따라서 전체 = (레벨당 O(n)) × (log2 n 레벨) = O(n log n). 입력이 어떤 모양이든 쪼개는 방식이 같으므로 최선·평균·최악이 모두 O(n log n)이다.
- 공간 O(n)인 이유: 병합 결과를 담을 배열이 필요하다. 재귀 깊이는 log n이지만, 한 시점에 살아 있는 임시 공간의 최대치가 n에 비례한다. 이 때문에 병합 정렬은 제자리 정렬이 아니다.
- 안정성: `a[i] <= a[j]`에서 등호가 왼쪽을 먼저 꺼내게 한다. 같은 값이면 왼쪽 조각(=원래 앞쪽)이 항상 먼저 나가므로 입력 순서가 보존된다. `<`로 바꾸면 오른쪽이 먼저 나가 안정성이 깨진다.

- **C++ 함정 — `mid = (lo + hi) / 2`의 오버플로**: `lo`와 `hi`가 각각 20억에 가까우면 그 합이 `int` 범위(약 21억)를 넘어 **음수**가 된다. 그러면 `mid`가 구간 밖을 가리켜 무한 재귀나 범위 밖 접근이 된다. 정석은 `mid = lo + (hi - lo) / 2`다 — 뺄셈이 먼저라 합이 절대 커지지 않는다. 배열 인덱스라면 실제로 터질 일은 드물지만, **이진탐색과 파라메트릭 서치에서 `lo`·`hi`가 값의 범위(10¹⁸)일 때는 반드시 터진다.** 습관으로 굳혀 둔다.

- **C++ 함정 — 임시 배열을 매 호출마다 새로 만들면**: `merge_part` 안의 `vector<int> tmp;`는 호출마다 힙 할당을 한다. 호출이 `2n` 번이므로 할당만 `2n` 번이다. 큰 입력에서는 **함수 밖에 크기 n짜리 버퍼를 한 번만 잡아 두고 재사용**하는 편이 몇 배 빠르다.

- **`std::stable_sort`가 곧 병합 정렬이다**: libstdc++의 `stable_sort`는 추가 버퍼를 얻을 수 있으면 병합 정렬로 O(n log n), 못 얻으면 제자리 병합으로 O(n log² n)에 동작한다. **"안정성이 필요하면 `stable_sort`"**라는 규칙의 내부가 바로 이 레슨의 알고리즘이다.

- **꼬리 처리 두 줄을 빼먹으면**: `while (i <= mid && j <= hi)`가 끝난 시점에는 한쪽이 반드시 남아 있다. 그 꼬리를 옮기지 않으면 결과 배열의 뒤쪽이 예전 값 그대로 남아 조용히 틀린다. 이 유형은 **작은 예제에서는 우연히 맞는 경우가 많아** 발견이 늦다.

**접근 전략**

- 핵심 아이디어: "쪼갠다 → 각각 정렬한다 → 합친다". 어려운 문제(정렬)를 절반짜리 같은 문제 두 개로 줄이고, 마지막에 병합이라는 쉬운 연산으로 합쳐 올린다. "정렬된 두 열을 훑으며 비교"하는 병합 패턴은 두 배열 교집합/합집합, "정렬된 상태로 개수 세기" 같은 문제에도 그대로 재사용된다.

- 언제 쓰나: 항상 O(N log N)이 보장돼야 할 때(퀵 정렬은 최악 O(N²)), 그리고 "안정 정렬"이 필요할 때. 또 병합 단계를 살짝 고치면 "정렬하면서 뒤바뀐 쌍(역순쌍, inversion) 개수 세기" 같은 부가 정보를 O(N log N)에 뽑아낼 수 있다 — 오른쪽 원소를 먼저 꺼낼 때 왼쪽에 남아 있는 개수만큼 역순쌍을 더하면 된다.

- 시간 O(N log N)(항상), 공간 O(N)(병합용 임시 배열 필요 → 제자리 정렬 아님). 흔한 실수: 병합에서 남은 꼬리를 붙이는 것을 잊거나, 비교를 `<`로 써서 동일 원소의 원래 순서가 뒤집혀 안정성이 깨지는 것(왼쪽 우선을 위해 `<=`를 쓴다).

**문제**

**1) 두 정렬 배열 병합** · Easy

- **요구사항**: 이미 오름차순으로 정렬된 두 배열을 하나의 오름차순 배열로 합쳐 출력한다. 정렬 함수를 새로 부르지 말고 "병합"만으로 O(N+M)에 처리한다.
- **입력**: 첫 줄에 N과 M. 둘째 줄에 정렬된 정수 N개. 셋째 줄에 정렬된 정수 M개.
- **출력**: 합쳐진 정렬 배열을 한 줄에 공백으로 구분해 출력.
- **예제**: `3 3 / 1 3 5 / 2 4 6` → `1 2 3 4 5 6`
- **예제**: `2 3 / 1 2 / 3 4 5` → `1 2 3 4 5`
- **셀프체크**: 인덱스 두 개로 훑었는가(두 배열을 합쳐 `sort`로 얼버무리면 병합의 핵심을 놓친 것). 한쪽이 먼저 끝났을 때 남은 꼬리를 붙였는가. 양쪽에 같은 값이 있을 때 둘 다 빠짐없이 들어가는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<int> a(n), b(m);
    for (int i = 0; i < n; i++) cin >> a[i];
    for (int i = 0; i < m; i++) cin >> b[i];
    vector<int> res;
    int i = 0, j = 0;
    while (i < n && j < m) {
        if (a[i] <= b[j]) res.push_back(a[i++]);
        else res.push_back(b[j++]);
    }
    while (i < n) res.push_back(a[i++]);
    while (j < m) res.push_back(b[j++]);
    for (int k = 0; k < (int)res.size(); k++) {
        if (k) cout << ' ';
        cout << res[k];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
3 3
1 3 5
2 4 6
--OUT
1 2 3 4 5 6
--IN
2 3
1 2
3 4 5
--OUT
1 2 3 4 5
@@EXPL
(1) 접근·핵심 아이디어

- 두 배열이 이미 정렬돼 있으므로, 각 배열의 맨 앞을 가리키는 인덱스 i, j를 두고 더 작은 쪽을 결과에 꺼내 그 인덱스만 전진시키면 O(N+M)에 합쳐진다. 둘을 이어붙여 다시 `sort`하면 병합의 핵심(두 정렬열을 훑는 것)을 놓친다.
- 한쪽이 먼저 끝나면 남은 쪽 꼬리를 통째로 붙인다. 비교를 `<=`로 하면 같은 값도 둘 다 순서대로 들어간다.

(2) 코드 단계별

- n, m과 두 정렬 배열 a, b를 읽는다.
- i=j=0에서 시작해 `i<n && j<m` 동안: `a[i] <= b[j]`면 a[i]를 꺼내고 i++, 아니면 b[j]를 꺼내고 j++.
- 루프가 끝나면 남은 `a`의 꼬리와 `b`의 꼬리를 각각 while로 결과에 붙인다.
- 결과를 공백으로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "두 개의 정렬열 합치기 = 투 포인터 병합"을 떠올린다(정렬 함수 재호출 금지).
- 작은 쪽을 꺼내고 그 인덱스만 전진, 같으면 왼쪽 우선(`<=`)으로 처리한다.
- 루프 종료 후 남은 꼬리 붙이기를 잊지 않는다. 한쪽이 훨씬 짧거나 값이 겹치는 케이스로 검산한다.
```

**2) 역순쌍 개수 세기** · Hard

- **요구사항**: 배열에서 `i < j` 이면서 `a[i] > a[j]`인 쌍(뒤에 더 작은 값이 오는 쌍)의 개수를 센다. N이 커도(수만) 동작하도록 병합 정렬을 변형해 O(N log N)에 구한다.
- **입력**: 첫 줄에 N. 둘째 줄에 정수 N개.
- **출력**: 역순쌍의 개수 하나.
- **예제**: `5 / 2 4 1 3 5` → `3`  ((2,1),(4,1),(4,3))
- **예제**: `5 / 5 4 3 2 1` → `10`  (모든 쌍이 역순, 5C2 = 10)
- **셀프체크**: 이중 반복 O(N²)는 큰 N에서 시간 초과다 — 병합 단계에서 "오른쪽 원소를 꺼낼 때 왼쪽에 남은 개수"를 누적했는가. 이미 정렬된 배열(`1 2 3 4`)에서 0이 나오는가. 카운트 변수의 자료형 범위(값이 매우 커질 수 있음 → `long long`)를 신경 썼는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

long long inv = 0;

vector<int> sortCount(vector<int> a) {
    if ((int)a.size() <= 1) return a;
    int m = a.size() / 2;
    vector<int> left(a.begin(), a.begin() + m);
    vector<int> right(a.begin() + m, a.end());
    left = sortCount(left);
    right = sortCount(right);
    vector<int> merged;
    int i = 0, j = 0;
    int L = left.size(), R = right.size();
    while (i < L && j < R) {
        if (left[i] <= right[j]) {
            merged.push_back(left[i++]);
        } else {
            merged.push_back(right[j++]);
            inv += L - i; // 오른쪽을 먼저 꺼냄 → 왼쪽에 남은 수만큼 역순쌍
        }
    }
    while (i < L) merged.push_back(left[i++]);
    while (j < R) merged.push_back(right[j++]);
    return merged;
}

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];
    sortCount(arr);
    cout << inv << '\n';
    return 0;
}
@@TESTS
--IN
5
2 4 1 3 5
--OUT
3
--IN
5
5 4 3 2 1
--OUT
10
@@EXPL
(1) 접근·핵심 아이디어

- 역순쌍(i<j, a[i]>a[j]) 개수를 병합 정렬에 얹어 O(N log N)에 센다. 핵심은 병합 단계: 왼쪽·오른쪽이 각각 정렬돼 있을 때, 오른쪽 원소를 결과로 먼저 꺼낸다는 것은 "그 오른쪽 값보다 큰(=아직 남은) 왼쪽 원소들 전부"와 역순쌍을 이룬다는 뜻이다. 그러니 오른쪽을 꺼낼 때 왼쪽에 남은 개수 `L - i`를 누적한다.
- 왼쪽 내부/오른쪽 내부의 역순쌍은 재귀 호출에서 이미 전역 `inv`에 누적된다.

(2) 코드 단계별

- n, 배열을 읽는다.
- `sortCount(a)`는 정렬된 벡터를 반환하며, 병합 도중 발생한 역순쌍을 전역 `inv`에 더한다. 크기<=1이면 그대로 반환.
- 절반씩 재귀해 left, right를 정렬한다.
- 병합하며 `left[i] <= right[j]`면 왼쪽을 꺼내고, 아니면 오른쪽을 꺼내며 `inv += L - i`.
- 남은 꼬리를 붙이고 정렬 결과를 반환. 최종 `inv`를 출력. (합이 커질 수 있으니 `long long`으로 센다.)

(3) 스스로 다시 짤 때 생각 순서

- "정렬하면서 부가 정보 세기 = 병합 변형"을 떠올린다.
- 병합에서 `<=`는 왼쪽 우선(안정)이라 역순쌍을 세지 않고, 오른쪽을 먼저 꺼낼 때만 "남은 왼쪽 수"를 더한다는 규칙을 세운다.
- 좌/우 내부 + 병합 단계를 모두 합산하도록 카운트를 누적한다. 정렬된 입력에서 0이, 역정렬에서 nC2가 나오는지 검산한다.
```

**3) 재귀 깊이 추적** · Medium

- **요구사항**: 병합 정렬로 배열을 정렬하는 과정에서, 재귀가 도달하는 "최대 깊이"를 출력한다(맨 처음 호출을 깊이 1로 센다). 배열을 절반씩 나눌 때의 트리 높이를 확인하는 문제다.
- **입력**: 첫 줄에 N. 둘째 줄에 정수 N개.
- **출력**: 정렬된 배열(한 줄)과 최대 재귀 깊이(다음 줄).
- **예제**: `4 / 3 1 2 4` → `1 2 3 4` / `3`  (4→2→1, 깊이 1,2,3)
- **예제**: `1 / 7` → `7` / `1`  (쪼갤 게 없어 깊이 1)
- **셀프체크**: 최대 깊이는 대략 `ceil(log2 N) + 1`이다 — N=4면 3, N=1이면 1. 재귀 함수에 현재 깊이를 인자로 넘겨 최댓값을 갱신했는가. 크기 1에서 더 내려가지 않고 멈추는가(무한 재귀 방지).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int best = 0;

vector<int> msort(vector<int> a, int depth) {
    if (depth > best) best = depth;
    if ((int)a.size() <= 1) return a;
    int m = a.size() / 2;
    vector<int> left(a.begin(), a.begin() + m);
    vector<int> right(a.begin() + m, a.end());
    left = msort(left, depth + 1);
    right = msort(right, depth + 1);
    vector<int> res;
    int i = 0, j = 0;
    int L = left.size(), R = right.size();
    while (i < L && j < R) {
        if (left[i] <= right[j]) res.push_back(left[i++]);
        else res.push_back(right[j++]);
    }
    while (i < L) res.push_back(left[i++]);
    while (j < R) res.push_back(right[j++]);
    return res;
}

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];
    vector<int> sorted_arr = msort(arr, 1);
    for (int k = 0; k < (int)sorted_arr.size(); k++) {
        if (k) cout << ' ';
        cout << sorted_arr[k];
    }
    cout << '\n';
    cout << best << '\n';
    return 0;
}
@@TESTS
--IN
4
3 1 2 4
--OUT
1 2 3 4
3
--IN
1
7
--OUT
7
1
@@EXPL
(1) 접근·핵심 아이디어

- 병합 정렬을 정상적으로 수행하되, 재귀 함수에 "현재 깊이"를 인자로 넘기고 전역 최댓값 best를 갱신한다. 맨 첫 호출을 깊이 1로 세고, 자식 호출은 depth+1로 넘긴다.
- 크기 1 이하이면 더 쪼개지 않고 그대로 반환하므로 재귀가 반드시 멈춘다. 최대 깊이는 트리 높이라 대략 ceil(log2 N)+1이다.

(2) 코드 단계별

- n, 배열을 읽는다. best=0으로 초기화(전역).
- `msort(a, depth)`: 진입할 때 best를 depth로 갱신. size<=1이면 반환.
- 반으로 나눠 `msort(왼쪽, depth+1)`, `msort(오른쪽, depth+1)` 재귀 후 두 정렬 결과를 병합.
- 최종 정렬 배열을 첫 줄, best를 둘째 줄에 출력.

(3) 스스로 다시 짤 때 생각 순서

- 평범한 병합 정렬을 먼저 떠올리고, "깊이 추적"을 위해 함수 인자에 depth를 추가한다.
- 첫 호출을 깊이 1로, 자식은 +1로 넘기며 매 진입 시 최댓값을 갱신한다.
- N=1이면 깊이 1, N=4면 3이 나오는지 손으로 트리를 그려 검산한다(종료 조건 size<=1을 잊지 않는다).
```


## L7. 퀵 정렬

**개념**

- 퀵 정렬(quick sort)도 분할 정복이지만, 병합 정렬과 반대로 "먼저 나누는 데 힘을 쓰고, 합칠 때는 아무 일도 안 한다". 기준값 하나(피벗, pivot)를 골라, 피벗보다 작은 것은 왼쪽, 큰 것은 오른쪽으로 몰아 놓는다(분할, partition). 이러면 피벗은 이미 "최종 자리"에 놓인다. 그다음 왼쪽 구간과 오른쪽 구간을 각각 같은 방식으로 정렬한다.

- 분할이 끝나면 피벗을 경계로 좌·우가 서로 섞일 일이 없으므로, 좌·우를 재귀로 정렬하기만 하면 전체가 정렬된다. 병합 같은 별도 합치기 단계가 없다.

- 성능은 "피벗이 구간을 얼마나 반반으로 가르느냐"에 달렸다. 균형 있게 갈리면 O(N log N), 항상 한쪽으로 치우치면(예: 이미 정렬된 배열에서 맨 끝을 피벗으로) 최악 O(N²)이 된다. 그래서 피벗을 무작위로 고르거나 "첫·중간·끝의 중앙값(median-of-three)"으로 고르는 기법을 쓴다.

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> quick_sort(vector<int> arr) {
    if ((int)arr.size() <= 1) return arr;
    int pivot = arr[arr.size() / 2];    // 가운데를 피벗으로 (치우침 완화)
    vector<int> less, equal, greater;
    for (int x : arr) {
        if (x < pivot) less.push_back(x);
        else if (x == pivot) equal.push_back(x);
        else greater.push_back(x);
    }
    vector<int> res = quick_sort(less);
    res.insert(res.end(), equal.begin(), equal.end());
    vector<int> g = quick_sort(greater);
    res.insert(res.end(), g.begin(), g.end());
    return res;
    // 참고: 위는 이해용(추가 벡터 사용). 제자리 분할은 L10에서.
}
```

**그림으로 보기**

```text
 quick sort on [7, 2, 9, 4, 1, 8, 5]      pivot = 4
   less        equal      greater
   [2 1]        [4]       [7 9 8 5]
     |                        |
     v                        v            # 각 구간을 같은 방식으로 재귀
   [1 2]                  [5 7 8 9]
   result = [1 2] + [4] + [5 7 8 9] = 1 2 4 5 7 8 9
 # 분할이 끝나면 피벗은 이미 최종 자리. 합치는 단계가 필요 없다
```

```text
 balanced split                 skewed split (worst)
   n                              n
   +-- n/2                        +-- 1
   |    +-- n/4                   +-- n-1
   |    +-- n/4                        +-- 1
   +-- n/2                             +-- n-2
        +-- n/4                              +-- 1
        +-- n/4                              +-- n-3
   depth = log2(n)                depth = n-1
   total = n * log2(n)            total = n + (n-1) + ... = n^2/2
```

**손으로 따라가기**

제자리 분할(Lomuto)을 `a = {3, 6, 2, 5, 4}`, 피벗 `a[hi] = 4`로 추적한다. `i`는 "피벗 이하인 값들의 마지막 자리"다.

| j | `a[j]` | `a[j] <= 4` | i | 실행 | 배열 |
|---|---|---|---|---|---|
| - | - | - | -1 | 시작 | `3 6 2 5 4` |
| 0 | 3 | O | 0 | `swap(0,0)` | `3 6 2 5 4` |
| 1 | 6 | X | 0 | 없음 | `3 6 2 5 4` |
| 2 | 2 | O | 1 | `swap(1,2)` | `3 2 6 5 4` |
| 3 | 5 | X | 1 | 없음 | `3 2 6 5 4` |
| 끝 | - | - | 1 | `swap(i+1, hi)` = `swap(2,4)` | `3 2 4 5 6` |

반환값은 `i + 1 = 2`. 피벗 4가 인덱스 2에 확정되고 왼쪽 `[3, 2]`는 모두 4 이하, 오른쪽 `[5, 6]`은 모두 4 초과다. 마지막 교환에서 `i`가 아니라 `i + 1`을 쓰는 것이 이 코드의 유일한 함정이다 — `i`를 쓰면 피벗이 자기보다 작은 값과 자리를 바꿔 분할이 깨진다.

```cpp
int partition(vector<int>& a, int lo, int hi) {
    int pivot = a[hi];                 // 값을 복사해 둔다 (자리가 곧 바뀐다)
    int i = lo - 1;                    // '피벗 이하 구간'의 마지막 자리
    for (int j = lo; j < hi; j++)      // 불변식 : a[lo..i] <= pivot < a[i+1..j-1]
        if (a[j] <= pivot) swap(a[++i], a[j]);
    swap(a[i + 1], a[hi]);             // i 가 아니라 i+1
    return i + 1;                      // 피벗의 최종 자리
}
```

**왜 이렇게 되는가**

- 분할 한 번의 비용은 구간을 한 번 훑는 O(구간 길이)다. 병합 정렬과 달리 합치는 비용은 0이므로, 전체 비용은 "모든 분할 비용의 합"이다.
- 균형 있게 갈리면 레벨마다 총 n칸을 훑고 레벨이 log2 n개 → O(n log n). 병합 정렬과 같은 계산이다.
- 한쪽으로 완전히 치우치면 구간 길이가 n, n-1, n-2, … 로만 줄어든다. 합이 n(n+1)/2 = O(n²)이고 재귀 깊이도 n이 되어 스택까지 위험해진다. C++에서는 이 "스택까지 위험"이 곧 **스택 오버플로로 인한 즉사**를 뜻한다 — n = 10⁵의 역순 입력에서 실제로 일어난다.
- 최악이 실제로 나오는 상황: 피벗을 항상 맨 앞(또는 맨 뒤)으로 고정한 채 이미 정렬된(또는 역순인) 입력을 받을 때다. 매번 최솟값/최댓값이 피벗이 되어 한쪽이 비어 버린다.
- 대책은 피벗을 데이터에 의존하지 않게 고르는 것이다. 무작위 선택, 또는 첫·중간·끝 세 값의 중앙값(median-of-three)을 쓰면 "정렬된 입력"이라는 흔한 패턴에서 최악이 사라진다.
- 중복이 많은 배열에서는 같은 값을 따로 모으는 3-way 분할이 결정적이다. 2-way로 처리하면 같은 값들이 한쪽에 몰려 구간이 줄지 않고, 최악이면 재귀가 끝나지 않는다.
- quickselect: 원하는 k가 어느 구간에 있는지 보고 그쪽만 재귀하면 비용이 n + n/2 + n/4 + … < 2n이라 평균 O(n)이다. 전체 정렬 없이 k번째 값만 필요할 때 쓴다. C++에는 이것이 `nth_element(v.begin(), v.begin() + k, v.end())`로 이미 들어 있다(평균 O(n)).

- **C++ 함정 — 무작위 피벗은 `rand()`보다 `mt19937`**: `rand() % n`은 주기가 짧고 하위 비트의 품질이 나빠 저격 입력에 뚫린다. 경쟁 프로그래밍에서 `std::sort`를 O(n²)로 몰아넣는 안티-퀵정렬 테스트가 실제로 존재한다. 필요하면 다음처럼 쓴다.

```cpp
static mt19937 rng((unsigned)chrono::steady_clock::now()
                       .time_since_epoch().count());
int p = lo + (int)(rng() % (unsigned)(hi - lo + 1));   // 균등한 무작위 피벗
swap(a[p], a[hi]);                                     // 맨 뒤로 옮긴 뒤 분할
```

- **C++ 함정 — 재귀 깊이를 로그로 묶는 관용구**: 두 구간 중 **작은 쪽만 재귀하고 큰 쪽은 루프로 처리**하면 스택 깊이가 최악에도 `O(log n)`으로 고정된다. `std::sort`의 introsort가 깊이 제한을 두는 것과 같은 동기다.

```cpp
while (lo < hi) {
    int p = partition(a, lo, hi);
    if (p - lo < hi - p) { quick(a, lo, p - 1); lo = p + 1; }  // 작은 쪽만 재귀
    else                 { quick(a, p + 1, hi); hi = p - 1; }
}
```

- **`swap(a[++i], a[j])`에서 부작용의 순서**: 한 식 안에서 같은 변수를 고치고 읽는 코드는 읽기 어렵고, 예전 C++에서는 미정의 동작이기도 했다. C++17부터는 이 형태가 안전하지만, 읽는 사람을 위해 `i++; swap(a[i], a[j]);` 두 줄로 쓰는 편이 낫다.

**접근 전략**

- 핵심 아이디어: "피벗 기준으로 세 무리(작다/같다/크다)로 가른다". 같은 값을 따로 모으면(3-way partition) 중복이 많은 배열에서도 빠르고, "피벗보다 작은 것 몇 개?" 같은 질문에 바로 답할 수 있다. 이 분할 아이디어는 정렬뿐 아니라 "전체 정렬 없이 k번째 값만 구하기(quickselect)"로 확장된다 — 원하는 k가 어느 쪽 구간에 있는지 보고 그쪽만 재귀하면 평균 O(N)이다.

- 언제 쓰나: 평균적으로 가장 빠른 비교 정렬이 필요하고 안정성이 필요 없을 때(C++ `std::sort`는 인트로소트라 안정성을 보장하지 않는다. 안정성이 필요하면 `std::stable_sort`를 쓴다). "정렬 전체는 필요 없고 k번째/상위 k개만" 같은 상황엔 quickselect(또는 `std::nth_element`)가 딱이다.

- 시간 평균 O(N log N), 최악 O(N²)(피벗 선택으로 완화). 공간은 재귀 스택 O(log N)(제자리 분할 기준). 흔한 실수: 피벗을 항상 맨 끝/맨 앞으로 고정하면 정렬된 입력에서 최악이 된다. 분할 시 피벗과 같은 값 처리를 빠뜨려 무한 재귀에 빠지는 것도 주의.

**문제**

**1) k번째로 작은 수 (quickselect)** · Medium

- **요구사항**: 정수 N개에서 정렬했을 때 k번째로 작은 값을 구한다(중복도 한 자리로 센다). 전체를 정렬하지 말고 분할 아이디어로 원하는 쪽 구간만 재귀해 구한다.
- **입력**: 첫 줄에 N과 k. 둘째 줄에 정수 N개.
- **출력**: k번째로 작은 값 하나.
- **예제**: `6 3 / 7 2 9 4 4 1` → `4`  (정렬: 1 2 4 4 7 9, 3번째는 4)
- **예제**: `5 2 / 3 1 2 5 4` → `2`
- **셀프체크**: 피벗으로 "작다/같다/크다"로 가른 뒤, k가 "작다" 구간 크기 이하면 왼쪽만, "작다+같다" 크기 이하면 답이 피벗, 그보다 크면 오른쪽만 재귀했는가(양쪽 다 재귀하면 그냥 정렬이다). k의 1-기반/0-기반 인덱스를 헷갈리지 않았는가. 중복이 많을 때도 무한 재귀 없이 끝나는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int quickselect(vector<int> a, int k) {
    int pivot = a[a.size() / 2];
    vector<int> less, equal, greater;
    for (int x : a) {
        if (x < pivot) less.push_back(x);
        else if (x == pivot) equal.push_back(x);
        else greater.push_back(x);
    }
    if (k <= (int)less.size()) return quickselect(less, k);
    else if (k <= (int)less.size() + (int)equal.size()) return pivot;
    else return quickselect(greater, k - less.size() - equal.size());
}

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];
    cout << quickselect(arr, k) << '\n';
    return 0;
}
@@TESTS
--IN
6 3
7 2 9 4 4 1
--OUT
4
--IN
5 2
3 1 2 5 4
--OUT
2
@@EXPL
(1) 접근·핵심 아이디어

- 전체 정렬 없이 k번째로 작은 값만 구한다. 피벗을 골라 "작다/같다/크다" 세 무리로 나누면, k(1-기반)가 어느 무리에 속하는지 바로 판정된다.
  - k <= less.size(): 답은 작은 무리 안에 있으니 그쪽만 재귀.
  - k <= less.size()+equal.size(): 답이 곧 피벗값.
  - 그 밖: 큰 무리에서 찾되, 앞 무리 크기만큼 k를 줄여 재귀.
- 한쪽만 재귀하므로 평균 O(N). 같은 값을 equal로 따로 빼서 중복이 많아도 무한 재귀에 빠지지 않는다.

(2) 코드 단계별

- n, k, 배열을 읽는다.
- `quickselect(a, k)`: 가운데 값을 피벗으로 삼아 less/equal/greater로 분할.
- 세 무리 크기로 k의 위치를 판정해 해당 방향만 재귀(또는 피벗 반환).
- 결과를 출력.

(3) 스스로 다시 짤 때 생각 순서

- "정렬 전체는 필요 없고 k번째만" 신호에서 quickselect를 떠올린다(C++ 표준 `std::nth_element`도 같은 목적).
- less/equal/greater 세 무리로 나눠 k와 무리 크기를 비교해 한 방향만 재귀한다(양쪽 재귀는 그냥 정렬).
- k가 1-기반임을 지키고, greater로 갈 때 `k - less.size() - equal.size()`로 k를 조정하는지 확인한다. 중복 값을 equal로 분리해 종료성을 보장한다.
```

**2) 피벗 기준 세 무리 개수** · Easy

- **요구사항**: 배열과 피벗값 p가 주어질 때, p보다 작은 원소 수 / p와 같은 원소 수 / p보다 큰 원소 수를 순서대로 출력한다(퀵 정렬의 분할 단계 자체를 확인).
- **입력**: 첫 줄에 N과 p. 둘째 줄에 정수 N개.
- **출력**: `작음 같음 큼` 세 수를 공백으로 구분해 한 줄에 출력.
- **예제**: `6 3 / 3 1 2 3 5 3` → `2 3 1`  (작음: 1,2 / 같음: 3,3,3 / 큼: 5)
- **예제**: `4 10 / 1 2 3 4` → `4 0 0`
- **셀프체크**: 세 조건(`<`, `==`, `>`)이 배타적이며 합이 N인가. 피벗과 같은 값이 "같음"으로만 세어지는가(작음이나 큼으로 새지 않게). 이 세 개수가 quickselect에서 방향을 결정하는 근거임을 이해했는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, p;
    cin >> n >> p;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];
    int less = 0, equal = 0, greater = 0;
    for (int x : arr) {
        if (x < p) less++;
        else if (x == p) equal++;
        else greater++;
    }
    cout << less << ' ' << equal << ' ' << greater << '\n';
    return 0;
}
@@TESTS
--IN
6 3
3 1 2 3 5 3
--OUT
2 3 1
--IN
4 10
1 2 3 4
--OUT
4 0 0
@@EXPL
(1) 접근·핵심 아이디어

- 퀵 정렬의 분할 단계 그 자체다. 배열을 피벗 p 기준으로 "작다/같다/크다" 세 무리로 나눌 때 각 무리의 크기를 센다. 세 조건은 서로 배타적이고(한 원소는 정확히 한 무리) 합은 N이다.

(2) 코드 단계별

- n, 피벗 p, 배열을 읽는다.
- `less = (x < p 개수)`, `equal = (x == p 개수)`, `greater = (x > p 개수)`를 각각 센다.
- 세 수를 공백으로 한 줄에 출력.

(3) 스스로 다시 짤 때 생각 순서

- `<`, `==`, `>` 세 조건으로만 분류하고, 세 카운트의 합이 N인지로 자기 검증한다.
- 피벗과 같은 값이 "같음"에만 들어가는지(작음/큼으로 새지 않게) 확인한다.
- 이 세 개수가 quickselect에서 "k가 어느 구간에 있나"를 정하는 근거임을 연결해 이해한다.
```

**3) 피벗 선택 비교** · Medium

- **요구사항**: 같은 배열에 대해 "맨 끝을 피벗"으로 쓸 때와 "중간값(첫·중간·끝의 median-of-three)을 피벗"으로 쓸 때, 첫 분할에서 좌측 구간의 크기가 각각 얼마인지 출력한다. 피벗 선택이 균형에 주는 영향을 관찰하는 문제다.
- **입력**: 첫 줄에 N. 둘째 줄에 정수 N개(서로 다르다고 가정).
- **출력**: `끝피벗_좌측크기 중앙값피벗_좌측크기` 를 공백으로 구분해 출력.
- **예제**: `5 / 1 2 3 4 5` → `4 2`  (끝=5 피벗이면 좌측에 1,2,3,4 → 4 / median(1,3,5)=3 피벗이면 좌측에 1,2 → 2)
- **예제**: `5 / 3 1 4 5 2` → `1 2`  (끝=2 피벗이면 좌측에 1 → 1 / median(3,4,2)=3 피벗이면 좌측에 1,2 → 2)
- **셀프체크**: "좌측 크기 = 피벗보다 작은 원소 수"로 정의했는가. 끝 피벗이 배열 최솟값이면 좌측이 0이 되는 극단이 왜 나쁜지(정렬된/역정렬된 입력에서 끝 피벗의 편향) 스스로 값을 넣어 체감해 보라. median-of-three가 왜 더 균형 잡히는지 설명할 수 있는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];

    int end_pivot = arr[n - 1];
    int end_left = 0;
    for (int x : arr) if (x < end_pivot) end_left++;

    int first = arr[0];
    int mid = arr[n / 2];
    int last = arr[n - 1];
    vector<int> three = {first, mid, last};
    sort(three.begin(), three.end());
    int median_pivot = three[1];
    int median_left = 0;
    for (int x : arr) if (x < median_pivot) median_left++;

    cout << end_left << ' ' << median_left << '\n';
    return 0;
}
@@TESTS
--IN
5
1 2 3 4 5
--OUT
4 2
--IN
5
3 1 4 5 2
--OUT
1 2
@@EXPL
(1) 접근·핵심 아이디어

- "첫 분할에서 좌측 구간 크기"를 "피벗보다 작은 원소 수"로 정의하고, 두 가지 피벗 선택으로 각각 그 수를 센다.
- 끝 피벗: `arr[n-1]`. median-of-three 피벗: 첫·중간·끝 세 값을 정렬한 중앙값(세 값을 담은 벡터를 `sort`한 뒤 `[1]`). 각 피벗에 대해 "그보다 작은 원소 수"를 세면 된다.
- 정렬된 입력(`1 2 3 4 5`)에서 끝=5 피벗은 좌측이 4로 크게 치우치는 반면, median 피벗은 좌측이 2로 반반에 가깝다 → median-of-three가 더 균형적임을 관찰한다.

(2) 코드 단계별

- n, 배열을 읽는다(원소는 서로 다르다고 가정).
- `end_pivot = arr[n-1]`, `end_left = (end_pivot보다 작은 원소 수)`.
- 중앙값 피벗: first=arr[0], mid=arr[n/2], last=arr[n-1]의 median을 세 원소 벡터를 `sort`해 `[1]`로 구하고 그보다 작은 원소 수를 센다.
- `end_left median_left`를 공백으로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "좌측 크기 = 피벗보다 작은 원소 수"라는 정의를 못 박는다(이게 quickselect 방향 결정 근거와 같다).
- 두 피벗을 각각 구하고, 각 피벗에 대해 카운트만 세면 끝. 정렬된 입력에서 끝 피벗이 왜 한쪽으로 쏠려 나쁜지, median-of-three가 왜 더 반반에 가까운지 손으로 확인한다.
```


## L8. 힙 정렬

**개념**

- 힙 정렬(heap sort)은 "힙"이라는 자료구조를 이용한 정렬이다. 힙은 완전 이진 트리 형태로, "부모가 항상 자식보다 작다(최소 힙)" 또는 "크다(최대 힙)"는 규칙만 지킨다. 그래서 루트(맨 위)에는 항상 최소(또는 최대)값이 있고, 그 값을 O(log N)에 꺼내고 다시 채울 수 있다.

> 선행: 트리와 힙의 내부 구조·`sift-up`/`sift-down`은 Ch6에서 자세히 다룬다. 여기서는 "정렬 도구로서의 힙"과 C++ `<queue>`의 `priority_queue` 사용에 집중한다.

- 정렬 아이디어: 모든 원소를 힙에 넣고(build), 루트(극값)를 하나씩 꺼내면 순서대로 나온다. 꺼낼 때마다 힙이 규칙을 회복하는 데 O(log N)이 들고, N번 꺼내므로 전체 O(N log N)이다.

- C++는 `<queue>`의 `priority_queue`로 힙을 제공한다. 기본은 최대 힙이라 `top()`이 최댓값이다. 최소 힙이 필요하면 `priority_queue<int, vector<int>, greater<int>>`처럼 비교자를 바꾼다. `push`로 넣고 `pop`으로 꺼낸다. 이미 있는 배열은 생성자에 반복자 범위를 넘겨 O(N)에 힙으로 만들 수 있다.

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> heap_sort(const vector<int>& arr) {
    priority_queue<int, vector<int>, greater<int>> h(arr.begin(), arr.end()); // 최소 힙, O(N)
    vector<int> res;
    while (!h.empty()) {           // 작은 것부터 나옴
        res.push_back(h.top());
        h.pop();
    }
    return res;
}

// 상위 k개는 굳이 전체 정렬 없이 "크기 k 최소 힙"을 유지해 O(N log k)에 구한다.
// (partial_sort / nth_element 같은 표준 알고리즘으로도 가능하다.)
```

**그림으로 보기**

```text
 min-heap           # 완전 이진 트리로 보되 실제 저장은 배열 한 줄
                  [0] 1
                 /       \
            [1] 3         [2] 5
           /     \       /
      [3] 7   [4] 4   [5] 9

   array : idx  0  1  2  3  4  5
                1  3  5  7  4  9
   parent(i) = (i - 1) / 2        child(i) = 2i + 1, 2i + 2
 # 포인터가 없다. 부모/자식은 인덱스 산술로 즉시 계산된다
 # 규칙은 '부모 <= 자식' 하나뿐. 형제끼리는 아무 관계도 없다
```

```text
 pop                # 루트를 꺼내고 마지막 잎을 올린 뒤 내려보낸다
   1  3  5  7  4  9      take root = 1
   9  3  5  7  4         move last leaf 9 to root
   9 vs min(3, 5) = 3    swap  ->  3  9  5  7  4
   9 vs min(7, 4) = 4    swap  ->  3  4  5  7  9
 # 내려간 거리 = 트리 높이 = log2(n) -> pop 한 번이 O(log n)
```

**손으로 따라가기**

`{5, 3, 8, 1}`을 힙으로 만들고 하나씩 꺼낸다.

| 단계 | 힙(배열) | 꺼낸 값 | 출력 |
|---|---|---|---|
| 0 | `1 3 8 5` | - | - |
| 1 | `3 5 8` | 1 | `1` |
| 2 | `5 8` | 3 | `1 3` |
| 3 | `8` | 5 | `1 3 5` |
| 4 | (빈 힙) | 8 | `1 3 5 8` |

주의: 1단계의 힙 상태 `3 5 8`은 정렬된 것처럼 보이지만 우연이다. 힙은 "루트만 최솟값"을 보장할 뿐 배열 전체가 정렬돼 있지 않다. `make_heap` 직후 배열을 그냥 출력하면 정렬 결과가 아니다.

C++에서 같은 일을 하는 도구가 두 층으로 있다.

```cpp
// (1) 컨테이너 어댑터 - 실전에서 거의 항상 이쪽
priority_queue<int> maxq;                                   // 기본은 최대 힙
priority_queue<int, vector<int>, greater<int>> minq;        // 최소 힙
minq.push(5); minq.push(1);
int x = minq.top();   // 1 - 꺼내는 게 아니라 보기만 한다
minq.pop();           // 반환값이 없다! top() 으로 먼저 읽어야 한다

// (2) 알고리즘 - vector 를 직접 힙으로 다룰 때
vector<int> v = {5, 3, 8, 1};
make_heap(v.begin(), v.end());     // O(n) - 최대 힙
pop_heap(v.begin(), v.end());      // 루트를 맨 뒤로 보낸다
int top = v.back(); v.pop_back();  // 그다음 실제로 뺀다
sort_heap(v.begin(), v.end());     // 힙 정렬 - 전부 꺼내 오름차순으로
```

- **`priority_queue`의 기본이 최대 힙**이라는 점이 파이썬 `heapq`(최소 힙)와 정반대다. 최소 힙이 필요하면 `greater<int>`를 세 번째 인자로 주거나, 넣을 때 부호를 뒤집어 `-x`로 넣고 꺼낼 때 다시 뒤집는다.
- **`pop()`은 값을 돌려주지 않는다.** `int x = pq.pop();`은 컴파일 오류이고, `top()`으로 읽은 뒤 `pop()`으로 지우는 두 줄이 정석이다.

**왜 이렇게 되는가**

- 완전 이진 트리라 높이가 floor(log2 n)이다. 부모·자식 관계를 인덱스 산술로 계산하니 트리를 배열 하나에 빈틈없이 담을 수 있고, 노드 링크에 쓸 메모리가 0이다. 흩어진 노드를 포인터로 잇는 구조보다 **캐시 지역성도 훨씬 좋다.**
- `pop` 한 번의 비용: 마지막 잎을 루트에 올린 뒤 규칙이 회복될 때까지 아래로 내려간다. 최악이 트리 높이만큼이므로 O(log n).
- n개를 모두 꺼내면 O(n log n)이다. 정확히는 log n + log(n-1) + … + log 1 = log(n!) ≈ n log n이라 비교 정렬 하한과 딱 맞는다.
- `make_heap`이 O(n log n)이 아니라 O(n)인 이유: 아래에서 위로 내려보내기를 하면 대부분의 노드가 잎 근처라 거의 안 움직인다. 깊이 d의 노드는 최대 (h-d)칸 내려가고 그런 노드가 2^d개이므로, 총 비용이 n · Σ(k / 2^k) ≤ 2n이다.
- 상위 k개를 O(n log k)에 구하는 법: 크기 k짜리 최소 힙을 유지하며, 새 값이 힙의 최소보다 크면 최소를 버리고 넣는다. 힙 크기가 k로 고정이라 연산 하나가 O(log k)이고 n번 반복한다. n이 크고 k가 작을 때 전체 정렬보다 훨씬 싸다. C++에는 `partial_sort(v.begin(), v.begin() + k, v.end())`도 있어 같은 목적에 쓸 수 있다.
- 힙 정렬은 제자리로 구현할 수 있지만 안정 정렬이 아니다. 멀리 떨어진 원소끼리 교환하며 내려보내기 때문에 같은 값의 순서가 보존되지 않는다.

- **C++ 함정 — 부모 인덱스 `(i - 1) / 2`에서 `i = 0`**: `i`가 `int`면 `(0 - 1) / 2 == 0`이라 우연히 안전하지만, `i`가 `size_t`(부호 없음)면 `0 - 1`이 거대한 수가 되어 배열 밖을 읽는다. 힙 인덱스는 항상 `int`로 두고, 올려보내기 루프의 조건에 `i > 0`을 먼저 건다.

- **C++ 함정 — 비교자의 방향이 직관과 반대**: `priority_queue<T, vector<T>, Cmp>`에서 `Cmp`가 참을 돌려주는 쪽이 **먼저 나오는 것이 아니라 나중에 나온다.** `greater<int>`를 주면 최소 힙이 되는 것이 그래서다. 사용자 정의 비교자도 같은 규칙을 따른다.

```cpp
struct Task { int pri, id; };
struct Cmp {                          // pri 가 작은 것이 먼저 나오게 하려면
    bool operator()(const Task& a, const Task& b) const {
        return a.pri > b.pri;         // '>' 를 써야 최소 힙이 된다
    }
};
priority_queue<Task, vector<Task>, Cmp> pq;
```

- **C++ 함정 — 빈 힙에서 `top()`·`pop()`**: 예외를 던지지 않고 미정의 동작이 된다. 다익스트라나 BFS 루프에서 `while (!pq.empty())`를 조건으로 두는 것은 스타일이 아니라 필수다.

- **`priority_queue`에는 반복자가 없다**: 안을 훑어보거나 특정 원소를 지우는 연산이 없다. "이미 처리한 원소를 무시하는" 관용구(다익스트라의 `if (d > dist[u]) continue;`)가 필요한 이유가 이것이다. 임의 원소 삭제가 정말 필요하면 `set`을 힙 대신 쓰거나, 삭제 표시용 힙을 하나 더 둔다.

**접근 전략**

- 핵심 아이디어: "매번 최소(또는 최대)값이 바로 필요하다"면 힙이다. 전체를 정렬해 두는 대신, 필요할 때마다 극값을 O(log N)에 꺼낸다. 특히 "상위 k개"나 "스트림에서 계속 들어오는 값의 k번째"처럼 데이터가 계속 흐르거나 일부만 필요할 때 강력하다. 상위 k개는 "크기 k짜리 최소 힙"을 유지해 O(N log k)에 구한다(새 값이 힙 최소보다 크면 최소를 버리고 넣는다).

- 언제 쓰나: (1) 여러 정렬된 리스트를 합칠 때(각 리스트 머리를 힙에 넣고 최소를 반복해 꺼냄), (2) 우선순위가 있는 처리(작은 것/급한 것 먼저), (3) k번째 값·상위 k개. 완전한 정렬 결과가 통째로 필요하면 그냥 `std::sort`가 더 간단하고 빠른 경우가 많다.

- 시간: 힙 구성 O(N), 전체 정렬 O(N log N). 상위 k개는 O(N log k). 공간 O(N)(또는 상위 k만 유지하면 O(k)). 주의점: `priority_queue`는 기본이 최대 힙이라 최소 힙이 필요하면 `greater` 비교자를 지정한다. 힙은 "정렬된 상태"가 아니라 "루트만 극값"임을 혼동하지 말 것(내부 배열을 그대로 출력하면 정렬돼 있지 않다).

**문제**

**1) 상위 k개 큰 수** · Easy

- **요구사항**: 정수 N개에서 가장 큰 k개를 큰 순서대로 출력한다. 전체 정렬 대신 크기 k 힙을 유지하는 방식으로 풀어 본다.
- **입력**: 첫 줄에 N과 k. 둘째 줄에 정수 N개.
- **출력**: 상위 k개를 내림차순으로 한 줄에 공백으로 구분해 출력.
- **예제**: `6 3 / 10 20 5 8 30 15` → `30 20 15`
- **예제**: `3 2 / 3 1 2` → `3 2`
- **셀프체크**: 크기 k 최소 힙을 유지하면(새 값이 힙 최소보다 크면 교체) 힙 안에 늘 상위 k개가 남는가. 출력은 내림차순으로 정렬했는가(힙에서 꺼내면 작은 것부터 나온다). k = N이면 전체가 내림차순으로 나오는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];
    // 크기 k 최소 힙
    priority_queue<int, vector<int>, greater<int>> h;
    for (int x : arr) {
        h.push(x);
        if ((int)h.size() > k) h.pop(); // 최소값을 버림
    }
    vector<int> res;
    while (!h.empty()) {
        res.push_back(h.top());
        h.pop();
    }
    sort(res.rbegin(), res.rend()); // 내림차순
    for (int i = 0; i < (int)res.size(); i++) {
        if (i) cout << ' ';
        cout << res[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
6 3
10 20 5 8 30 15
--OUT
30 20 15
--IN
3 2
3 1 2
--OUT
3 2
@@EXPL
(1) 접근·핵심 아이디어

- "가장 큰 k개"는 전체 정렬 없이 "크기 k짜리 최소 힙"으로 구한다. 힙에 값을 넣되 크기가 k를 넘으면 최소값을 버린다. 그러면 힙에는 항상 지금까지 본 값들 중 큰 k개만 남는다(가장 작은 것이 계속 밀려나므로).
- 힙 최소가 곧 "현재 상위 k개 중 가장 작은 값(=경계)"이라, 새 값이 그보다 크면 자연히 최소가 밀려난다. O(N log k).

(2) 코드 단계별

- n, k, 배열을 읽는다.
- 각 x를 힙에 push, `size() > k`면 pop으로 최소를 제거 → 힙 크기 k 유지.
- 끝나면 힙에 상위 k개가 남는다. 힙을 비우며 벡터에 담는다(작은 것부터).
- 출력은 내림차순이 요구이므로 `sort(res.rbegin(), res.rend())`로 정렬해 공백 출력.

(3) 스스로 다시 짤 때 생각 순서

- "상위 k개 = 크기 k 최소 힙"을 공식처럼 기억한다(작은 것을 버려 큰 것만 남긴다).
- 힙에서 꺼내면 작은 것부터 나오므로, 최종 출력은 반드시 내림차순으로 정렬한다.
- k=N이면 전체가 내림차순으로 나오는지 경계 검산한다.
```

**2) k개의 정렬된 리스트 병합** · Medium

- **요구사항**: 이미 각각 오름차순으로 정렬된 k개의 리스트가 있다. 이들을 하나의 오름차순 리스트로 병합해 출력한다. 힙을 이용해 매번 "현재 후보들 중 최소"를 골라 담는다.
- **입력**: 첫 줄에 k. 다음 k줄에 각 리스트(맨 앞에 길이, 그 뒤 정렬된 원소들).
- **출력**: 병합된 전체 오름차순 리스트를 한 줄에 공백으로 구분해 출력.
- **예제**: `3 / 2 1 4 / 2 2 5 / 2 3 6` → `1 2 3 4 5 6`
- **예제**: `2 / 3 1 2 3 / 2 2 4` → `1 2 2 3 4`
- **셀프체크**: 힙에는 "값과 그 값이 어느 리스트의 몇 번째인지"를 함께 넣어, 최소를 꺼낼 때마다 같은 리스트의 다음 값을 밀어 넣었는가. 힙 크기는 항상 k 이하로 유지되는가(전체를 한 번에 넣지 않는다). 어떤 리스트가 먼저 소진돼도 나머지가 계속 병합되는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    int k;
    cin >> k;
    vector<vector<int>> lists(k);
    for (int i = 0; i < k; i++) {
        int length;
        cin >> length;
        lists[i].resize(length);
        for (int j = 0; j < length; j++) cin >> lists[i][j];
    }
    // (값, 리스트번호, 위치) 최소 힙
    using T = tuple<int, int, int>;
    priority_queue<T, vector<T>, greater<T>> heap;
    for (int li = 0; li < k; li++) {
        if (!lists[li].empty())
            heap.push({lists[li][0], li, 0});
    }
    vector<int> res;
    while (!heap.empty()) {
        auto [val, li, pos] = heap.top();
        heap.pop();
        res.push_back(val);
        if (pos + 1 < (int)lists[li].size())
            heap.push({lists[li][pos + 1], li, pos + 1});
    }
    for (int i = 0; i < (int)res.size(); i++) {
        if (i) cout << ' ';
        cout << res[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
3
2 1 4
2 2 5
2 3 6
--OUT
1 2 3 4 5 6
--IN
2
3 1 2 3
2 2 4
--OUT
1 2 2 3 4
@@EXPL
**이 풀이의 새 문법**

- `tuple<T1,T2,T3>`: 서로 다른 타입 몇 개를 하나로 묶는 컨테이너(`pair`의 3개 이상 버전). 비교는 첫 원소부터 사전식으로 이뤄진다.
- `using T = tuple<int,int,int>;`: 타입에 별명을 붙이는 또 다른 문법(`typedef tuple<int,int,int> T;`와 같은 뜻).
- `auto [val, li, pos] = heap.top();`: 구조적 바인딩(structured binding). `pair`/`tuple`/`struct`의 각 원소를 이름 붙은 변수로 한 번에 풀어 받는다.

(1) 접근·핵심 아이디어

- 각 리스트가 이미 정렬돼 있으므로, "지금 각 리스트의 맨 앞 후보들" 중 최소만 반복해 꺼내면 전체가 오름차순으로 나온다. 이 "후보들 중 최소"를 O(log k)에 주는 것이 최소 힙이다.
- 힙에는 값만이 아니라 (값, 리스트번호, 그 리스트 내 위치)를 튜플로 넣어, 최소를 꺼내면 같은 리스트의 다음 원소를 힙에 밀어 넣는다. 힙 크기는 항상 살아있는 리스트 수(<= k) 이하다.

(2) 코드 단계별

- k와 각 리스트(맨 앞 길이 + 원소들)를 읽어 lists에 담는다.
- 각 리스트의 첫 원소를 (값, li, 0)으로 힙에 넣는다.
- 힙이 빌 때까지: 최소 (val, li, pos)를 꺼내 결과에 담고, 그 리스트에 다음 원소가 있으면 (다음값, li, pos+1)을 넣는다.
- 결과를 공백으로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "여러 정렬 리스트 병합 = 매번 후보 최소 꺼내기"를 떠올려 힙을 선택한다.
- 힙 원소에 리스트 식별자와 위치를 함께 넣어야 "다음 값"을 밀어 넣을 수 있음을 기억한다(튜플은 첫 원소부터 비교되므로 값이 최소 기준이 된다).
- 어떤 리스트가 소진돼도 나머지가 계속 처리되는지(빈 리스트/짧은 리스트) 작은 예제로 확인한다.
```

**3) 스트림에서 k번째 작은 값** · Medium

- **요구사항**: 정수들이 순서대로 들어온다. 매 순간이 아니라 전부 들어온 뒤, 전체에서 k번째로 작은 값을 출력한다. 힙으로 처리해 본다.
- **입력**: 첫 줄에 N과 k. 둘째 줄에 정수 N개.
- **출력**: k번째로 작은 값 하나.
- **예제**: `6 4 / 5 3 8 1 9 2` → `5`  (정렬: 1 2 3 5 8 9, 4번째는 5)
- **예제**: `5 1 / 4 2 7 1 3` → `1`
- **셀프체크**: 최소 힙에서 k번 `pop`한 마지막 값이 답인가. k = 1이면 전체 최소가 나오는가. `k`가 1-기반임을 기억하고 딱 k번만 꺼냈는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];
    priority_queue<int, vector<int>, greater<int>> h(arr.begin(), arr.end());
    int val = 0;
    for (int i = 0; i < k; i++) {
        val = h.top();
        h.pop();
    }
    cout << val << '\n';
    return 0;
}
@@TESTS
--IN
6 4
5 3 8 1 9 2
--OUT
5
--IN
5 1
4 2 7 1 3
--OUT
1
@@EXPL
(1) 접근·핵심 아이디어

- 최소 힙에서 top/pop을 하면 항상 남은 것 중 최소값이 나온다. 따라서 k번 꺼내면 꺼낸 순서가 곧 작은 순서이고, k번째로 꺼낸 값이 "k번째로 작은 값"이다.
- 전체를 정렬(O(N log N))해도 되지만, 힙은 범위 생성자로 build가 O(N)이고 pop k번이 O(k log N)이라 k가 작을 때 유리하다.

(2) 코드 단계별

- n, k, 배열을 읽는다.
- `priority_queue<int, vector<int>, greater<int>> h(arr.begin(), arr.end())`로 O(N)에 최소 힙 구성.
- k번 top/pop하며 마지막에 꺼낸 값을 `val`에 보관.
- `val` 출력 = k번째로 작은 값.

(3) 스스로 다시 짤 때 생각 순서

- "매번 최소값"이 필요하니 최소 힙(`greater` 비교자)을 떠올린다.
- 범위 생성자로 힙을 만들고, k가 1-기반임을 기억해 정확히 k번만 pop한다.
- k=1이면 전체 최소가 나오는지, `nth_element`로도 같은 답인지 교차 검산한다.
```


## L9. Stable Sort

**개념**

- "안정 정렬(stable sort)"은 값이 같은 원소들의 "원래(입력) 순서"를 정렬 후에도 그대로 유지하는 정렬이다. 예를 들어 점수가 같은 두 학생이 입력에서 A, B 순이었다면, 점수로 정렬한 뒤에도 A가 B보다 앞에 있어야 안정 정렬이다. 반대로 순서가 뒤집힐 수 있으면 "불안정 정렬"이다.

- 왜 중요한가: "여러 기준으로 차례차례" 정렬할 때 결정적이다. 안정 정렬이면 "약한 기준으로 먼저 정렬 → 강한 기준으로 다시 정렬"해도, 강한 기준이 같은 그룹 안에서는 이전(약한) 기준 순서가 살아남는다. 이 성질 덕분에 복잡한 다중 정렬을 여러 번의 단일 정렬로 쪼갤 수 있다.

- C++의 `std::sort`는 안정성을 보장하지 않는다(인트로소트). 안정성이 필요하면 `std::stable_sort`를 써야 한다. `stable_sort`는 값이 같은 원소들 사이의 입력 순서를 반드시 유지한다. 대신 이 성질을 "의식적으로 활용"하는 법을 아는 게 중요하다.

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<pair<string,int>> data = {{"kim",90},{"lee",85},{"park",90},{"choi",85}};

// 점수 내림차순만 지정 → 같은 점수끼리는 입력 순서 그대로 유지(안정)
stable_sort(data.begin(), data.end(),
            [](const auto& a, const auto& b){ return a.second > b.second; });
// 결과: kim(90), park(90), lee(85), choi(85)  ← 90끼리 kim→park, 85끼리 lee→choi

// 다단 정렬: 2순위 먼저, 1순위 나중 (안정성 덕분에 성립)
stable_sort(data.begin(), data.end(),
            [](const auto& a, const auto& b){ return a.first < b.first; });   // 2순위: 이름 오름차순
stable_sort(data.begin(), data.end(),
            [](const auto& a, const auto& b){ return a.second > b.second; }); // 1순위: 점수 내림차순
```

**그림으로 보기**

```text
 sort by score only            # 동점(85) 두 명의 순서에 주목
   input  : A(90)  B(85)  C(90)  D(85)
   stable : A(90)  C(90)  B(85)  D(85)   # B 가 D 보다 앞 = 입력 순서 유지
   unstab : A(90)  C(90)  D(85)  B(85)   # 뒤집혀도 '정렬'로는 통과한다
 # 두 결과 모두 점수 내림차순이다. 동점 처리만 다르다
 # std::sort 는 위 둘 중 어느 쪽을 줄지 보장하지 않는다
```

```text
 two-pass stable sort         # 2순위 먼저, 1순위 나중
   input        : kim90  lee85  park90  choi85
   pass1 (name) : choi85 kim90  lee85   park90
   pass2 (-score): kim90 park90 choi85  lee85
 # pass2 에서 90 끼리, 85 끼리는 pass1 의 순서가 그대로 살아남는다
 # 결과 = 점수 내림차순, 동점이면 이름 오름차순
```

**손으로 따라가기**

같은 데이터를 한 번에(복합 비교자) 정렬한 것과 두 번에 나눠 정렬한 것을 비교한다.

| 방식 | 코드 | 결과 |
|---|---|---|
| 복합 비교자 | `sort(d.begin(), d.end(), [](auto& a, auto& b){ return a.score != b.score ? a.score > b.score : a.name < b.name; })` | kim90, park90, choi85, lee85 |
| 2단 안정 정렬 | `stable_sort(... name <)` 후 `stable_sort(... score >)` | kim90, park90, choi85, lee85 |
| 동점 규칙 없음 | `stable_sort(... score >)` 한 번만 | kim90, park90, lee85, choi85 |

앞의 둘은 같은 답을 준다. 세 번째는 동점 규칙을 지정하지 않았으므로 입력 순서(lee가 choi보다 먼저 입력됨)가 그대로 남는다. 어느 쪽이 "맞는" 답인지는 문제가 정한다.

- 세 번째 줄을 `sort`로 바꾸면 **결과가 매번 달라질 수 있다.** `sort`는 동점의 순서를 보장하지 않으므로, 로컬에서 통과한 코드가 채점 서버의 다른 라이브러리 버전에서 틀릴 수 있다. **동점 순서가 답에 영향을 준다면 `sort`를 쓰면 안 된다.**

**왜 이렇게 되는가**

- 안정성의 정의를 그대로 쓰면 2단 정렬의 정당성이 증명된다. 안정 정렬은 "비교에서 같다고 판정된 두 원소"의 상대 순서를 바꾸지 않는다.
- pass2는 점수만 비교하므로 점수가 같은 두 원소는 "같다"고 판정된다. 따라서 그 둘의 순서는 pass2 이전 상태, 즉 pass1이 만든 이름 순서 그대로다.
- 이 논증은 순위가 셋 이상이어도 반복된다. k순위부터 1순위까지 거꾸로 안정 정렬하면 최종 결과가 "1순위, 같으면 2순위, …" 규칙과 일치한다.
- 방향이 뒤섞일 때(점수는 내림차순, 이름은 오름차순) 2단 정렬이 특히 편하다. 복합 비교자로 하려면 `a.score != b.score ? a.score > b.score : a.name < b.name`처럼 방향이 다른 두 비교를 한 식에 섞어야 해서 실수하기 쉽다.
- 어떤 정렬이 안정인가: 삽입·병합·기수는 안정, 선택·퀵·힙은 불안정이다. 안정인 쪽은 공통점이 있다 — 원소를 "이웃과만" 옮기거나(삽입) "같으면 왼쪽 먼저" 규칙을 명시한다(병합). 그래서 병합 정렬 기반인 `std::stable_sort`는 안정이고, 퀵+힙 기반인 `std::sort`는 불안정이다.

- **C++ 함정(가장 중요) — 비교자는 strict weak ordering이어야 한다**: `sort`에 넘기는 비교 함수는 "`a`가 `b`보다 **엄격히** 앞이면 참"을 돌려줘야 한다. 즉 **같을 때는 반드시 거짓**이어야 한다. `<=`를 쓰면 `cmp(a, a)`가 참이 되어 이 규칙이 깨지고, 표준 구현은 **배열 밖을 넘어가며 프로그램이 죽거나 조용히 메모리를 망가뜨린다.**

```cpp
// 틀림 - cmp(a, a) 가 true 라 범위 밖 접근이 일어난다
sort(v.begin(), v.end(), [](int a, int b){ return a <= b; });

// 맞음
sort(v.begin(), v.end(), [](int a, int b){ return a < b; });
```

  같은 이유로 **동점을 아무렇게나 처리하는 비교자**도 위험하다. 복합 비교자를 쓸 때는 "모든 필드가 같으면 반드시 `false`"가 되는지 확인한다. `pair`나 `tuple`의 기본 `<`는 이 성질을 자동으로 만족하므로, 가능하면 `sort(v.begin(), v.end())`처럼 기본 비교를 쓰는 편이 안전하다.

- **내림차순을 만드는 세 가지 방법과 동점 처리**: 결과가 미묘하게 다르다.

| 방법 | 코드 | 동점 순서 |
|---|---|---|
| 비교자 뒤집기 | `stable_sort(b, e, greater<int>())` | 입력 순서 유지 |
| 값 부호 뒤집기 | `-x`를 키로 오름차순 | 입력 순서 유지 |
| 오름차순 후 `reverse` | `stable_sort(b, e); reverse(b, e);` | **동점 순서까지 뒤집힘** |

  세 번째만 다르다. 파이썬의 `sorted(...)[::-1]`이 `reverse=True`와 다른 결과를 내는 것과 정확히 같은 이유다. **"내림차순으로 정렬하고 싶다"는 이유로 `reverse`를 쓰면 안 된다.**

- **동점 순서를 명시적으로 못 박는 법**: 안정성에 기대는 대신 원래 인덱스를 데이터에 넣어 비교자에 마지막 기준으로 추가하면, `sort`를 써도 결과가 결정적이 된다. 라이브러리 구현에 의존하지 않으므로 가장 안전한 방식이다.

```cpp
vector<tuple<int, string, int>> v;   // (-점수, 이름, 입력순서)
for (int i = 0; i < n; i++) v.emplace_back(-score[i], name[i], i);
sort(v.begin(), v.end());            // tuple 의 기본 사전식 비교 - 완전 결정적
```

**접근 전략**

- 핵심 아이디어: "동점일 때 입력 순서를 지켜야 한다"는 요구가 보이면 안정 정렬이다. C++에선 `stable_sort`가 동점의 입력 순서를 보장하므로, 비교자(comparator)에 "동점 처리 규칙"을 아예 넣지 않고 두면 입력 순서가 그대로 유지된다 — 굳이 등장 인덱스를 비교자에 넣을 필요가 없다(단, 넣어도 결과는 같다).

- 다단 정렬 패턴: 규칙이 "1순위 …, 같으면 2순위 …, 같으면 원래 순서"처럼 복잡하면, (a) 비교자에서 여러 기준을 순서대로 비교하는 방법과 (b) 낮은 순위부터 차례로 여러 번 `stable_sort`하는 방법 둘 다 가능하다. 방향이 뒤섞이거나 문자열을 내림차순으로 다뤄야 해 비교자가 까다로울 때 (b)가 편하다.

- 시간 O(N log N), 공간 O(N)(`stable_sort`는 추가 버퍼를 쓸 수 있다). 흔한 실수: 안정성이 "정렬 결과가 유일하다"는 뜻이라 착각하는 것 — 값이 같으면 순서가 입력에 따라 달라진다. 또 `std::sort`를 쓰면 동점의 입력 순서가 보장되지 않으니, 안정성이 필요한 문제에서는 반드시 `stable_sort`를 쓴다는 점을 정확히 알아 두면 함정을 피한다.

**문제**

**1) 안정 정렬 확인** · Easy

- **요구사항**: (값, 원래인덱스) 쌍들이 주어진다. 값 기준 오름차순으로 정렬하되, 값이 같으면 원래 인덱스가 작은 것이 앞에 오도록(=안정) 출력한다. 정렬이 안정적으로 동작하는지 눈으로 확인하는 문제다.
- **입력**: 첫 줄에 N. 둘째 줄에 정수 N개(왼쪽부터 원래 인덱스 0,1,2,…).
- **출력**: 정렬된 순서대로 각 원소의 "값 원래인덱스"를 한 줄씩 출력.
- **예제**: `5 / 2 1 2 1 3` → `1 1` / `1 3` / `2 0` / `2 2` / `3 4`  (값 1은 인덱스 1,3 순 / 값 2는 0,2 순)
- **예제**: `3 / 5 5 5` → `5 0` / `5 1` / `5 2`
- **셀프체크**: (값, 인덱스)를 만들고 값만 비교자로 `stable_sort`했을 때 인덱스가 오름차순으로 따라오는가(안정 정렬이라 그렇다). 값을 정수로 읽었는가. 모두 같은 값일 때 입력 순서가 그대로 유지되는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];
    vector<pair<int, int>> pairs;
    for (int i = 0; i < n; i++) pairs.push_back({arr[i], i});
    // 값만 기준으로 안정 정렬 -> 동점은 원래 인덱스 순서 유지
    stable_sort(pairs.begin(), pairs.end(),
                [](const pair<int, int>& a, const pair<int, int>& b) {
                    return a.first < b.first;
                });
    for (int i = 0; i < n; i++) {
        cout << pairs[i].first << ' ' << pairs[i].second << '\n';
    }
    return 0;
}
@@TESTS
--IN
5
2 1 2 1 3
--OUT
1 1
1 3
2 0
2 2
3 4
--IN
3
5 5 5
--OUT
5 0
5 1
5 2
@@EXPL
(1) 접근·핵심 아이디어

- 각 값에 "원래 인덱스"를 붙여 (값, 인덱스) 쌍을 만든다. 그다음 값만 비교 기준으로 `stable_sort`한다. `stable_sort`는 안정 정렬이라, 값이 같은 쌍들은 벡터에 들어온 순서(=인덱스 오름차순)를 그대로 유지한다. 그래서 동점 그룹 안에서 인덱스가 자동으로 오름차순으로 따라온다.

(2) 코드 단계별

- n과 정수 배열을 읽는다.
- (값 v, 인덱스 i) 쌍 벡터를 만든다.
- `stable_sort(..., a.first < b.first)` — 값만 기준. 인덱스는 비교자에 넣지 않아도 안정성 덕에 오름차순 유지.
- 정렬 순서대로 "값 인덱스"를 한 줄씩 출력.

(3) 스스로 다시 짤 때 생각 순서

- "동점일 때 입력 순서 유지" 요구를 보면 `stable_sort`를 떠올린다(`sort`는 보장 안 함).
- 값에 인덱스를 붙이되, 비교자에는 값만 넣는다(인덱스를 넣어도 결과는 같지만 불필요).
- 모두 같은 값인 케이스로 "인덱스가 0,1,2… 순으로 나오는지" 검산한다.
```

**2) 다단 정렬로 랭킹표** · Medium

- **요구사항**: 학생들의 (이름, 반, 점수)가 주어진다. "점수 내림차순, 점수가 같으면 반 오름차순, 반도 같으면 입력 순서 유지"로 정렬해 출력한다. 안정 정렬로 규칙을 구현해 본다.
- **입력**: 첫 줄에 N. 다음 N줄에 이름 반 점수.
- **출력**: 정렬된 순서대로 각 줄에 "이름 반 점수".
- **예제**: `4 / kim 2 90 / lee 1 90 / park 1 90 / amy 2 85` → `lee 1 90` / `park 1 90` / `kim 2 90` / `amy 2 85`  (90점 중 반 1: lee,park(입력순), 반 2: kim / 그 뒤 85점 amy)
- **예제**: `2 / a 1 70 / b 1 70` → `a 1 70` / `b 1 70`
- **셀프체크**: "가장 약한 기준(입력 순서는 그대로) → 반 오름 → 점수 내림" 순으로 정렬을 겹쳤는가, 혹은 비교자에서 `(점수 내림, 반 오름)`을 한 번에 처리했는가. 반이 같은 lee·park가 입력 순서대로 유지되는가(안정성의 핵심). 점수·반을 정수로 읽었는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<string> names(n);
    vector<int> cls(n), score(n);
    for (int i = 0; i < n; i++) cin >> names[i] >> cls[i] >> score[i];
    vector<int> idx(n);
    for (int i = 0; i < n; i++) idx[i] = i;
    // 점수 내림차순, 같으면 반 오름차순, 같으면 입력 순서(안정)
    stable_sort(idx.begin(), idx.end(), [&](int a, int b) {
        if (score[a] != score[b]) return score[a] > score[b];
        return cls[a] < cls[b];
    });
    for (int i = 0; i < n; i++) {
        int r = idx[i];
        cout << names[r] << ' ' << cls[r] << ' ' << score[r] << '\n';
    }
    return 0;
}
@@TESTS
--IN
4
kim 2 90
lee 1 90
park 1 90
amy 2 85
--OUT
lee 1 90
park 1 90
kim 2 90
amy 2 85
--IN
2
a 1 70
b 1 70
--OUT
a 1 70
b 1 70
@@EXPL
(1) 접근·핵심 아이디어

- 규칙이 "1순위 점수 내림 → 2순위 반 오름 → 3순위 입력 순서 유지"다. `stable_sort`는 안정이므로 비교자에 점수·반만 넣으면 두 값이 모두 같은 원소는 입력 순서가 저절로 보존된다(3순위를 따로 넣을 필요 없음).
- 인덱스 배열을 정렬해 "안정성"을 명확히 한다. 비교자에서 점수가 다르면 큰 쪽(내림), 같으면 반이 작은 쪽(오름)을 앞으로 보낸다.

(2) 코드 단계별

- 줄 단위로 (이름, 반=int, 점수=int)를 읽는다.
- 0..n-1 인덱스 배열을 만들고 `stable_sort`로 정렬(점수 내림 → 반 오름 → 나머지는 안정).
- 정렬된 인덱스 순서대로 각 행을 "이름 반 점수" 형식으로 줄마다 출력.

(3) 스스로 다시 짤 때 생각 순서

- 각 정렬 기준의 방향(내림/오름)을 확인한다: 점수 내림 → `>`, 반 오름 → `<`.
- 동점 시 입력 순서 유지는 `stable_sort`가 공짜로 준다는 점을 믿고 비교자에 그것을 넣지 않는다.
- 비교자는 강한 기준부터 순서대로 판정한다. 약한 기준부터 여러 번 `stable_sort`를 겹치는 방식으로도 같은 결과가 나오는지 떠올려 검산한다.
```

**3) 안정 vs 불안정 차이 만들기** · Medium

- **요구사항**: (값, 라벨) 쌍들을 값 기준으로 정렬한다. "안정 정렬" 결과와, "동점이면 라벨 사전 역순으로 뒤집는 불안정한 규칙"을 적용한 결과가 서로 다른 첫 위치(0-기반 인덱스)를 출력한다. 두 결과가 완전히 같으면 -1을 출력한다.
- **입력**: 첫 줄에 N. 다음 N줄에 값 라벨.
- **출력**: 두 정렬 결과가 처음으로 달라지는 인덱스(없으면 -1).
- **예제**: `3 / 1 a / 1 b / 2 c` → `0`  (안정: a,b,c / 불안정(동점 라벨 역순): b,a,c → 인덱스 0에서 다름)
- **예제**: `2 / 5 x / 6 y` → `-1`  (동점이 없어 두 결과가 동일)
- **셀프체크**: 안정 결과는 값만 기준으로 `stable_sort`해 동점의 입력 순서를 유지한다. "불안정 규칙"은 동점일 때 라벨 내림차순을 추가로 적용한 것 — 두 벡터를 앞에서부터 비교해 처음 다른 위치를 찾았는가. 동점이 하나도 없으면 왜 항상 -1인지 설명할 수 있는가(동점이 없으면 정렬 결과가 유일하다).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<int, string>> items(n);
    for (int i = 0; i < n; i++) cin >> items[i].first >> items[i].second;

    // 안정 정렬: 값만 key -> 동점은 입력 순서 유지
    vector<pair<int, string>> stable = items;
    stable_sort(stable.begin(), stable.end(),
                [](const auto& a, const auto& b) { return a.first < b.first; });

    // 불안정 규칙: 동점이면 라벨 사전 역순
    // (1) 라벨 내림차순으로 먼저 안정 정렬 -> (2) 값 오름차순으로 안정 정렬
    vector<pair<int, string>> unstable = items;
    stable_sort(unstable.begin(), unstable.end(),
                [](const auto& a, const auto& b) { return a.second > b.second; });
    stable_sort(unstable.begin(), unstable.end(),
                [](const auto& a, const auto& b) { return a.first < b.first; });

    int ans = -1;
    for (int i = 0; i < n; i++) {
        if (stable[i] != unstable[i]) {
            ans = i;
            break;
        }
    }
    cout << ans << '\n';
    return 0;
}
@@TESTS
--IN
3
1 a
1 b
2 c
--OUT
0
--IN
2
5 x
6 y
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- 두 정렬 결과를 만들어 앞에서부터 비교해 처음 달라지는 인덱스를 찾는다.
- "안정" 결과: 값만 기준으로 `stable_sort` → 동점은 입력 순서를 그대로 지킨다.
- "불안정" 규칙: 동점일 때만 라벨 사전 역순을 추가로 적용. 이를 안정 정렬 2단으로 구현한다 — 먼저 라벨 내림차순으로 정렬해 두고, 그 위에 값 오름차순으로 `stable_sort`하면 같은 값 안에서는 라벨 내림차순이 남는다.

(2) 코드 단계별

- 줄 단위로 (값, 라벨)을 읽는다(라벨은 문자열).
- `stable = items`를 값 기준으로 `stable_sort`.
- `unstable = items`를 라벨 내림차순으로 `stable_sort`한 뒤, 값 오름차순으로 다시 `stable_sort`.
- 두 벡터를 인덱스 0부터 비교해 처음 다른 위치를 `ans`에 담고, 끝까지 같으면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "동점이 없으면 정렬 결과가 유일 → 항상 -1"을 먼저 떠올리면 왜 동점 위치에서만 차이가 나는지 이해된다.
- 안정 결과는 값만 기준. 불안정은 "동점 내 라벨 내림차순"을 다단 안정 정렬(약한 기준 먼저, 강한 기준 나중)로 얹는다.
- 두 벡터를 앞에서 비교해 첫 불일치 인덱스를 반환한다.
```


## L10. In-Place Sort

**개념**

- "제자리 정렬(in-place sort)"은 입력 배열 "그 자체"를 자리만 바꿔 정렬해, 추가 메모리를 거의(상수 수준으로) 쓰지 않는 정렬이다. 병합 정렬처럼 크기 N짜리 임시 배열을 따로 만들면 제자리가 아니다. 선택·삽입·거품 정렬, 그리고 제자리 분할을 쓴 퀵 정렬·힙 정렬이 제자리 계열이다.

- 왜 중요한가: 메모리가 빠듯하거나(수백만 원소), "새 배열을 만들지 말고 원본을 바꾸라"는 제약이 있을 때 필요하다. 핵심 도구는 "두 원소의 교환(swap)"과 "인덱스로 경계 관리"다. C++에선 `swap(a[i], a[j])` 한 줄로 교환한다. `std::sort`는 제자리로 원본 컨테이너를 정렬한다.

- 대표 제자리 기법: (1) 투 포인터로 조건 만족 원소를 앞쪽으로 모으기(예: 0이 아닌 값 앞으로), (2) 세 구간 경계로 나누기(Dutch national flag), (3) 뒤집기(reverse)를 조합해 회전(rotate)하기. 모두 "원본 위에서 자리만 바꾼다".

```cpp
#include <bits/stdc++.h>
using namespace std;

// 0이 아닌 값을 앞으로 모으고 0을 뒤로 (순서 유지, 제자리)
void move_zeros(vector<int>& a) {
    int pos = 0;                          // 다음에 넣을 자리
    for (int i = 0; i < (int)a.size(); i++) {
        if (a[i] != 0) {
            swap(a[pos], a[i]);
            pos++;
        }
    }
    // 원본 a가 바뀜
}

// a = {0, 1, 0, 3, 12}; move_zeros(a); → a == {1, 3, 12, 0, 0}
```

**그림으로 보기**

```text
 move_zeros([0, 1, 0, 3, 12])      # pos = 0 이 아닌 값을 채울 다음 자리
   i=0  a[0]=0   skip          pos=0    0  1  0  3 12
   i=1  a[1]=1   swap(0,1)     pos=1    1  0  0  3 12
   i=2  a[2]=0   skip          pos=1    1  0  0  3 12
   i=3  a[3]=3   swap(1,3)     pos=2    1  3  0  0 12
   i=4  a[4]=12  swap(2,4)     pos=3    1  3 12  0  0
 # 새 배열 없이 원본 위에서 자리만 바꿨다 -> 추가 공간 O(1)
```

```text
 rotate left by k=2 with three reversals
   start           : 1 2 3 4 5
   reverse(0, k-1) : 2 1 3 4 5
   reverse(k, n-1) : 2 1 5 4 3
   reverse(0, n-1) : 3 4 5 1 2
 # 새 vector 를 만들어 이어 붙이면 O(n) 공간. 뒤집기 3번은 O(1) 공간
```

**손으로 따라가기**

C++에서 "원본이 바뀌는가"를 네 가지 방식으로 비교한다. 파이썬처럼 "이름이 객체를 가리킨다"가 아니라 **"값이냐 참조냐"**가 갈림길이다.

| 코드 | 함수 안 `a` | 바깥 원본 | 제자리인가 |
|---|---|---|---|
| `void f(vector<int>& a) { sort(a.begin(), a.end()); }` | 정렬됨 | 정렬됨 | O — 원본을 그 자리에서 고침 |
| `void f(vector<int> a) { sort(a.begin(), a.end()); }` | 정렬됨 | **그대로** | X — 복사본만 정렬됨 |
| `vector<int> b = a; sort(b.begin(), b.end());` | – | 그대로 | X — 사본 O(n)을 만듦 |
| `void f(const vector<int>& a) { sort(a.begin(), ...); }` | – | – | **컴파일 오류** — const 는 못 고침 |

두 번째가 가장 흔한 함정이다. 함수 안에서는 정렬된 것처럼 보이는데 호출한 쪽의 벡터는 하나도 안 바뀐다. **`&` 한 글자**가 차이의 전부이고, 컴파일러는 아무 경고도 하지 않는다. 게다가 값 전달은 `O(n)` 복사까지 덤으로 얹으므로, 큰 컨테이너는 **고칠 거면 `&`, 읽기만 할 거면 `const &`**가 규칙이다.

```cpp
void move_zeros(vector<int>& a) {           // & 가 있어야 원본이 바뀐다
    int pos = 0;                            // 불변식 : a[0..pos-1] 은 0 이 아님
    for (int i = 0; i < (int)a.size(); i++)
        if (a[i] != 0) swap(a[pos++], a[i]);
}

void rotate_left(vector<int>& a, int k) {
    int n = (int)a.size();
    if (n == 0) return;
    k %= n;                                 // k >= n 이어도 안전하게
    reverse(a.begin(), a.begin() + k);      // [0, k)
    reverse(a.begin() + k, a.end());        // [k, n)
    reverse(a.begin(), a.end());            // 전체
}
```

**왜 이렇게 되는가**

- 제자리 정렬의 정의는 "추가 공간이 입력 크기와 무관하게 상수"다. 재귀 스택처럼 O(log n)만 쓰는 경우도 관례상 제자리로 친다.
- 정렬별 추가 공간: 거품·선택·삽입 O(1), 힙 O(1), 퀵 O(log n)(재귀 스택), 병합 O(n)(임시 배열), 기수 O(n + b)(버킷). 병합·기수가 제자리가 아닌 이유가 여기 있다.
- `std::sort`는 퀵+힙+삽입의 혼합이라 추가 공간이 O(log n)뿐이고, 컨테이너를 **그 자리에서** 정렬한다. 반면 `std::stable_sort`는 병합 기반이라 O(n) 버퍼를 얻으려 시도하고, 못 얻으면 시간을 O(n log² n)으로 내주며 공간을 아낀다. **"제자리인가"를 묻는 문제에서 `stable_sort`는 답이 아니다.**
- 투 포인터가 O(1) 공간으로 도는 원리: 배열을 "확정 구간 / 검사 구간 / 미확인 구간"으로 나누고 그 경계를 인덱스 몇 개로만 기억한다. 상태가 인덱스뿐이라 입력이 커져도 추가 메모리가 늘지 않는다.
- `move_zeros`의 불변식: 루프 앞에서 항상 `a[0..pos-1]`은 0이 아닌 값들이 원래 순서대로 들어 있고, `a[pos..i-1]`은 전부 0이다. 이 불변식이 루프 끝까지 유지되므로 종료 시 답이 맞는다. 제자리 알고리즘은 이렇게 불변식 한 줄을 잡아 두면 검증이 쉬워진다.
- 회전을 뒤집기 3번으로 하는 이유: 새 벡터를 만들어 뒤쪽·앞쪽을 이어 붙이면 O(n) 공간을 쓴다. 뒤집기는 양끝에서 교환만 하므로 O(1) 공간에 끝난다. 시간은 둘 다 O(n)이지만 메모리 제약이 있을 때 차이가 난다. (표준 `std::rotate(b, b + k, e)`도 O(1) 공간에 같은 일을 한다.)

- **C++ 함정 — 반복자 산술의 경계**: `a.begin() + k`에서 `k > n`이면 유효 범위를 벗어난 반복자가 만들어져 `reverse`가 남의 메모리를 뒤집는다. 회전 전에 `k %= n`을 반드시 하고, `n == 0`을 먼저 걸러야 0으로 나누기도 피할 수 있다.

- **C++ 함정 — 지우면서 순회하기**: "조건에 맞는 원소를 제자리에서 제거"는 `for` 안에서 `erase`를 부르면 인덱스가 어긋나고 O(n²)이 된다. 정석은 **erase-remove 관용구**다.

```cpp
// 0 을 전부 제거 (순서 유지, O(n))
a.erase(remove(a.begin(), a.end(), 0), a.end());
// remove 는 지우지 않는다 - 남길 값을 앞으로 몰고 '새 끝'을 돌려줄 뿐이다
```

  `remove`만 부르고 `erase`를 빼먹으면 크기가 그대로라 뒤쪽에 옛 값이 남는다. 이름과 동작이 어긋나는 대표적인 API다.

- **원소가 무거우면 `swap`도 공짜가 아니다**: `vector<string>`의 `swap(a[i], a[j])`는 내부 포인터만 맞바꾸므로 사실상 O(1)이지만, 고정 크기 `struct`라면 통째 복사가 일어난다. 그런 경우 **인덱스 배열을 대신 정렬**하고 마지막에 한 번만 재배치하면 이동량이 최소가 된다.

**접근 전략**

- 핵심 아이디어: "새 배열을 만들지 말고 원본 위에서 해결"이라는 신호가 오면 투 포인터와 swap을 떠올린다. 대개 "이미 처리·확정된 구간"과 "아직 볼 구간"의 경계를 인덱스로 관리하고, 조건을 만족하는 원소를 경계 자리로 swap해 확정 구간을 키운다. 정렬된 배열에서 중복 제거, 특정 값 앞으로 몰기, 0/1/2 세 값 한 번에 분류(DNF)가 전형이다.

- 언제 쓰나: 메모리 제약, "원본을 그 자리에서 바꿔라"는 요구, 혹은 새 배열을 만들면 O(N) 추가 공간이 아까울 때. 회전은 "전체 뒤집기 → 부분 두 번 뒤집기"로 O(1) 추가 공간에 처리하는 고전 기법이 있다.

- 시간은 기법마다 다르지만 투 포인터/한 번 훑기는 보통 O(N), 공간 O(1) 추가. 흔한 실수: `sort`한 새 컨테이너를 만들거나 부분 배열을 복사해 "제자리"가 깨지는 것. 함수 안에서 원본을 바꾸려면 참조(`vector<int>&`)로 받아 인덱스 swap을 써야 한다(값으로 받으면 복사본만 바뀌고 바깥 원본은 그대로다).

**문제**

**1) 정렬된 배열 제자리 중복 제거** · Easy

- **요구사항**: 오름차순으로 정렬된 배열에서 중복을 제거해, 서로 다른 값들만 앞쪽에 몰아 둔다. 새 배열을 만들지 말고 원본 위에서 처리하고, "서로 다른 값의 개수"와 그 앞부분을 출력한다.
- **입력**: 첫 줄에 N. 둘째 줄에 정렬된 정수 N개.
- **출력**: 서로 다른 값의 개수(첫 줄)와 그 값들을 앞에서부터 공백 구분해 출력(둘째 줄).
- **예제**: `6 / 1 1 2 2 2 3` → `3` / `1 2 3`
- **예제**: `8 / 0 0 1 1 1 2 3 3` → `4` / `0 1 2 3`
- **셀프체크**: "쓰기 위치" 인덱스 하나로, 직전에 쓴 값과 다를 때만 그 자리에 써 넣었는가(정렬돼 있으니 바로 앞 값과만 비교하면 된다). 새 배열을 만들지 않고 `a[write]=a[i]` 식으로 원본을 갱신했는가. 모두 같은 값이면 개수가 1인가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    if (n == 0) {
        cout << 0 << '\n';
        cout << '\n';
        return 0;
    }
    int write = 1;
    for (int i = 1; i < n; i++) {
        if (a[i] != a[write - 1]) {
            a[write] = a[i];
            write++;
        }
    }
    cout << write << '\n';
    for (int i = 0; i < write; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
6
1 1 2 2 2 3
--OUT
3
1 2 3
--IN
8
0 0 1 1 1 2 3 3
--OUT
4
0 1 2 3
@@EXPL
(1) 접근·핵심 아이디어

- 배열이 이미 오름차순이므로 같은 값은 반드시 연속으로 몰려 있다. 따라서 "직전에 확정한 값"과 현재 값만 비교하면 새 값인지 알 수 있다.
- `write`는 "다음에 유일한 값을 써 넣을 자리"다. 현재 값이 직전에 쓴 값(`a[write-1]`)과 다르면 새 값이므로 `a[write]`에 써 넣고 `write`를 늘린다. 새 배열 없이 원본 앞부분을 덮어써서 제자리로 처리한다.

(2) 코드 단계별

- n과 배열 a를 읽는다. (n=0 방어는 있어도 되고 없어도 되지만, 첫 값은 항상 유일하므로 `write=1`로 시작.)
- i를 1..n-1로 훑으며 `a[i] != a[write-1]`일 때만 `a[write] = a[i]`, `write++`.
- 첫 줄에 유일한 값의 개수 `write`, 둘째 줄에 앞부분 `a[0..write-1]`을 공백으로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "정렬돼 있으니 중복은 이웃끼리만 발생"을 먼저 인식한다.
- 쓰기 인덱스 write를 1로 두고(첫 원소는 확정), 이후 원소를 직전 확정값과 비교한다.
- 다를 때만 앞으로 당겨 쓰고 write를 늘린다. 마지막에 개수와 앞부분을 출력한다. 모두 같은 값이면 write가 1로 끝나는지 확인한다.
```

**2) 0 뒤로 보내기(순서 유지)** · Easy

- **요구사항**: 배열에서 0이 아닌 값들의 상대 순서를 유지한 채 앞으로 모으고, 0은 모두 뒤로 보낸다. 제자리로 처리한다.
- **입력**: 첫 줄에 N. 둘째 줄에 정수 N개.
- **출력**: 변환된 배열을 한 줄에 공백 구분해 출력.
- **예제**: `5 / 0 1 0 3 12` → `1 3 12 0 0`
- **예제**: `6 / 1 0 2 0 0 3` → `1 2 3 0 0 0`
- **셀프체크**: 0이 아닌 값들의 원래 순서가 유지되는가(안정적인 이동). "다음에 넣을 자리" 인덱스로 swap 또는 덮어쓰기 했는가. 0이 전혀 없거나 전부 0인 경우도 맞게 나오는가.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    int pos = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] != 0) {
            swap(a[pos], a[i]);
            pos++;
        }
    }
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
5
0 1 0 3 12
--OUT
1 3 12 0 0
--IN
6
1 0 2 0 0 3
--OUT
1 2 3 0 0 0
@@EXPL
(1) 접근·핵심 아이디어

- "0이 아닌 값의 상대 순서 유지 + 0은 뒤로"는 투 포인터 제자리 기법의 전형이다. `pos`는 "다음에 0 아닌 값을 놓을 자리"를 가리킨다. 배열을 왼쪽부터 훑다가 0이 아닌 값을 만나면 그 값을 `pos` 자리로 swap하고 `pos`를 한 칸 전진시킨다.
- 이렇게 하면 0 아닌 값들은 만난 순서대로 앞쪽에 채워져 상대 순서가 보존되고, 0들은 자연히 뒤로 밀린다.

(2) 코드 단계별

- n과 배열 a를 읽는다.
- `pos = 0`으로 시작해 i를 0..n-1로 훑는다.
- `a[i] != 0`이면 `swap(a[pos], a[i])`하고 `pos++`. (i가 pos보다 앞서 있어 앞쪽에 남은 0과 교환되거나, 0이 없었다면 자기 자신과 교환된다.)
- 새 배열을 만들지 않고 원본 a 위에서만 자리를 바꾼다 → 제자리.
- 완성된 a를 공백으로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "쓸 자리 인덱스 pos" 하나를 떠올린다.
- 0이 아닌 값을 만날 때만 pos 자리로 보내고 pos를 늘린다는 규칙을 세운다.
- 덮어쓰기(그 뒤 나머지를 0으로 채우기) 대신 swap을 쓰면 한 번의 훑기로 끝난다는 점을 확인한다. 전부 0이거나 0이 없는 경계 케이스를 머릿속으로 돌려 본다.
```

**3) 배열 오른쪽으로 k칸 회전** · Medium

- **요구사항**: 배열을 오른쪽으로 k칸 회전한다(맨 뒤 k개가 앞으로 온다). 가능하면 "전체 뒤집기 → 앞 k개 뒤집기 → 나머지 뒤집기"의 제자리 뒤집기 기법으로 O(1) 추가 공간에 처리한다.
- **입력**: 첫 줄에 N과 k. 둘째 줄에 정수 N개.
- **출력**: 회전된 배열을 한 줄에 공백 구분해 출력.
- **예제**: `5 2 / 1 2 3 4 5` → `4 5 1 2 3`
- **예제**: `7 3 / 1 2 3 4 5 6 7` → `5 6 7 1 2 3 4`
- **셀프체크**: `k`가 N보다 클 수 있으니 `k %= N`으로 줄였는가(k가 N의 배수면 그대로). 뒤집기를 세 번 조합했을 때 결과가 맞는지 예제로 검산했는가. 투 포인터로 구간을 제자리에서 뒤집었는가(부분 배열을 복사해 만들면 추가 공간이 O(N)이 됨).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

void reverseRange(vector<int>& a, int lo, int hi) {
    while (lo < hi) {
        swap(a[lo], a[hi]);
        lo++;
        hi--;
    }
}

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    k %= n;
    reverseRange(a, 0, n - 1);
    reverseRange(a, 0, k - 1);
    reverseRange(a, k, n - 1);
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n';
    return 0;
}
@@TESTS
--IN
5 2
1 2 3 4 5
--OUT
4 5 1 2 3
--IN
7 3
1 2 3 4 5 6 7
--OUT
5 6 7 1 2 3 4
@@EXPL
(1) 접근·핵심 아이디어

- 오른쪽 k칸 회전은 "맨 뒤 k개가 앞으로 오는" 변환이다. 뒤집기 3번으로 O(1) 추가 공간에 처리하는 고전 기법을 쓴다: 전체를 뒤집으면 뒤 k개가 앞으로 오지만 각 구간의 내부 순서가 거꾸로다. 그래서 앞 k개와 나머지를 각각 다시 뒤집어 내부 순서를 복원한다.
- `k`는 N보다 클 수 있으므로 먼저 `k %= n`으로 실제 이동량으로 줄인다(k가 N의 배수면 0이 되어 그대로).

(2) 코드 단계별

- 입력에서 n, k, 배열 a를 읽고 `k %= n`.
- `reverseRange(a, lo, hi)`: 투 포인터로 lo와 hi를 안쪽으로 좁히며 swap → 구간을 제자리에서 뒤집는다(복사 안 씀).
- 전체 뒤집기 `reverseRange(a, 0, n-1)` → 앞 k개 뒤집기 `reverseRange(a, 0, k-1)` → 나머지 뒤집기 `reverseRange(a, k, n-1)`.
- 결과를 공백으로 이어 출력.

(3) 스스로 다시 짤 때 생각 순서

- 먼저 `k %= n`으로 정규화한다(안 하면 k가 클 때 인덱스가 어긋난다).
- 제자리 뒤집기 헬퍼(투 포인터 swap)를 만든다.
- "전체 → 앞 k → 뒤 n-k" 세 번 뒤집기 순서를 작은 예제(`1 2 3 4 5`, k=2)로 손으로 따라가며 확인한다.
```
