## L8. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터의 여섯 레슨은 서로 다른 자료구조를 배운 것처럼 보이지만, 실제로 던진 질문은 하나다. **"이 문제는 컬렉션에게 무엇을 요구하는가?"** 존재 여부만 물으면 해시로 충분하고, 정렬 순서를 계속 물으면 비교 기반 구조가 필요하며, 극단값 하나만 반복해서 꺼낸다면 전체를 정렬할 이유가 없다. C++는 이 갈림길마다 표준 컨테이너를 하나씩 마련해 두었다 — 파이썬이라면 외부 라이브러리를 가져오거나 직접 흉내 내야 하는 자리(TreeMap·TreeSet·최대 힙)까지 표준에 들어 있다. 아래에서 그 갈림길을 한 장으로 잇고, 바로 꺼내 쓸 뼈대와 자주 넘어지는 지점을 모은다.

**개념 지도**

챕터 전체는 "컬렉션에 무엇을 요구하는가"라는 한 질문에서 다섯 갈래로 갈라진다. 맨 아랫줄의 복잡도가 곧 그 선택의 가격표다.

```text
                    Ch01 : mid-level containers
                                |
         what does the problem need from the collection ?
                                |
 +-----------+-------------+-------------+-------------+
 |           |             |             |             |
 membership  order kept    one extreme   both ends     neighbors
 frequency   at all times  over and over only          of a node
 |           |             |             |             |
 unordered_  set / map     priority_     deque         list , or
 map / set   multiset      queue         (see L6)      nxt / prv
 L1 , L3     L2 , L4       L5                          L6
 |           |             |             |             |
 O(1) avg    O(log n)      O(log n)      O(1) ends     O(1) if the
 unordered   per op        top only      O(n) middle   node is held
```

같은 원소 다섯 개를 세 구조에 담아 보면 차이가 한눈에 보인다. **유지하는 순서가 많을수록 삽입이 비싸진다** — 이 한 문장이 위 지도의 가격표를 설명한다.

```text
  how much order does each structure actually keep ?

  unordered_set : none        bucket = hash(x) % bucket_count()
      +----+----+----+----+----+
      |  7 |  1 |  9 |  3 |  5 |
      +----+----+----+----+----+

  priority_queue : only "parent >= child"    // 기본은 최대 힙이다
              9                    root is the maximum
            /   \                  siblings have no order at all
           7     5                 the minimum is somewhere in a leaf
          / \
         3   1

  set : total order
      +----+----+----+----+----+
      |  1 |  3 |  5 |  7 |  9 |   lower_bound works here
      +----+----+----+----+----+

  more order kept   ->   more work per insert
  unordered_set O(1) avg  <  priority_queue O(log n)  <  set O(log n)
  sorted vector : O(log n) to find the slot, but O(n) to shift the tail
```

힙에는 "가운데 원소 하나만 지우기"가 없다. 그 구멍을 메우는 표준 우회가 지연 삭제이고, 이 챕터의 어려운 문제 대부분이 이 패턴 위에 서 있다.

```text
  a heap cannot delete an element in the middle -> lazy deletion

  pq.push({value, id})    and keep    alive = { ids that still count }

  delete id 2                         alive = { 1, 3, 4 }
      heap  [ (3,2) , (5,1) , (9,4) ]
              ^ top is a ghost : id 2 is no longer in alive

  peek : pop while the top id is missing from alive
      heap  [ (5,1) , (9,4) ]
              ^ real top = 5

  every element is pushed once and popped at most once
  -> the cleanup costs O(log n) amortized per operation
  // C++ 에서는 multiset 을 쓰면 ms.erase(ms.find(x)) 로 즉시 지울 수도 있다
```

**뼈대 코드**

1) `priority_queue` 5종 — 최대/최소, 우선순위 쌍, 상위 K 유지. **부호 반전이 필요 없다는 것이 파이썬 대비 이득이다.**

```cpp
#include <bits/stdc++.h>
using namespace std;

priority_queue<int> maxh;                     // 기본이 최대 힙
maxh.push(x);
int biggest = maxh.top(); maxh.pop();         // top()으로 읽고 pop()으로 지운다

priority_queue<int, vector<int>, greater<int>> minh;   // 최소 힙은 비교자 한 줄
minh.push(x);
int smallest = minh.top(); minh.pop();

vector<int> v = {5, 3, 8, 1};
priority_queue<int> pq(v.begin(), v.end());   // 배열이 이미 있으면 O(n)에 힙화

priority_queue<pair<long long,int>,
               vector<pair<long long,int>>,
               greater<>> pq2;                // <- 문제마다 바뀜: 우선순위 키
pq2.push({dist, node});                       // pair는 first 우선, 동점이면 second

priority_queue<int, vector<int>, greater<int>> topk;   // 상위 K개 유지
if ((int)topk.size() < K) topk.push(x);
else if (x > topk.top()) { topk.pop(); topk.push(x); } // top이 K개 중 최솟값
```

2) 두 힙으로 중앙값 — 작은 절반과 큰 절반의 경계 두 개를 O(1)에 본다.

```cpp
priority_queue<int> lo;                                 // 작은 절반 (최대 힙)
priority_queue<int, vector<int>, greater<int>> hi;      // 큰 절반 (최소 힙)

void addValue(int x) {
    lo.push(x);
    hi.push(lo.top()); lo.pop();          // lo의 최대를 hi로 넘겨 경계를 맞춘다
    if (hi.size() > lo.size()) {          // 불변식: lo.size() == hi.size() 또는 +1
        lo.push(hi.top()); hi.pop();
    }
}

double median() {
    if (lo.size() > hi.size()) return lo.top();
    return (lo.top() + hi.top()) / 2.0;   // <- 문제마다 바뀜: 짝수 개일 때의 규칙
}
```

3) 이분 경계 4종 — 정렬된 `vector` 위의 모든 경계 질의는 이 두 함수로 만든다.

```cpp
vector<int> a;                       // a는 항상 정렬 상태여야 한다
sort(a.begin(), a.end());

int i = lower_bound(a.begin(), a.end(), x) - a.begin();  // x 미만 개수
int j = upper_bound(a.begin(), a.end(), x) - a.begin();  // x 이하 개수

int cnt_x  = j - i;                                      // x의 등장 횟수
int cnt_LR = upper_bound(a.begin(), a.end(), R)
           - lower_bound(a.begin(), a.end(), L);         // [L, R] 개수
int ge = (i < (int)a.size()) ? a[i]   : -1;              // x 이상 최솟값
int le = (j > 0)             ? a[j-1] : -1;              // x 이하 최댓값
```

4) `set`/`multiset`으로 TreeSet — 삽입·삭제·pred·succ가 전부 O(log n)이다.

```cpp
set<int> s;
s.insert(v);                         // 중복은 자동으로 무시된다
s.erase(v);                          // 없으면 아무 일도 없다 (개수를 반환)

auto it = s.lower_bound(x);          // 반드시 멤버 함수! std::lower_bound는 O(n)
int succ = (it != s.end()) ? *it : -1;             // x 이상 최솟값
int pred = (it != s.begin()) ? *prev(it) : -1;     // x 미만 최댓값

multiset<int> ms;                    // 중복을 담아야 하면 multiset
ms.insert(v);
ms.erase(ms.find(v));                // <- 하나만 지운다. erase(v)는 전부 지운다
int mn = *ms.begin(), mx = *ms.rbegin();           // 최소·최대 O(1)
```

5) `deque` — 양끝만 쓴다면 직접 만들지 않는다.

```cpp
deque<int> dq;
dq.push_back(x);   dq.push_front(x);      // 양끝 삽입 O(1)
dq.pop_back();     dq.pop_front();        // 양끝 삭제 O(1)
int f = dq.front(), b = dq.back();        // 양끝 조회 O(1)

while (!dq.empty() && dq.front() <= r - W) dq.pop_front();   // 고정 크기 창
// dq[i] 도 O(1)이지만(vector와 달리 메모리가 연속은 아니다) 중간 삽입·삭제는 O(n)
```

6) 센티넬 이중 연결 리스트 — 삽입·삭제·복원의 세 줄짜리 정석(배열 링크 버전).

```cpp
const int H = 0, T = n + 1;               // 양끝 센티넬 두 칸(경계 분기를 없앤다)
vector<int> nxt(n + 2), prv(n + 2);
for (int i = 0; i <= n + 1; i++) { nxt[i] = i + 1; prv[i] = i - 1; }

void link(int p, int x, int q) {          // p와 q 사이에 x를 끼운다 (링크 네 개)
    nxt[p] = x; prv[x] = p;
    nxt[x] = q; prv[q] = x;
}
void unlink(int x) {                      // x를 뗀다 (링크 두 개, 짝으로 고친다)
    nxt[prv[x]] = nxt[x];
    prv[nxt[x]] = prv[x];                 // x의 prv/nxt는 지우지 않고 남겨 둔다
}
void restore(int x) {                     // 뗀 것을 제자리로 — 반드시 뗀 역순으로
    nxt[prv[x]] = x;
    prv[nxt[x]] = x;
}
```

**언제 무엇을 쓰나**

먼저 컨테이너를 한 표에 모은다. **왼쪽 열(무엇을 묻는 문제인가)을 문제에서 찾아내는 것이 실제로 하는 일의 전부**이고, 오른쪽 두 열이 그 선택의 가격표다.

| 컨테이너 | 무엇을 묻는 문제인가 | 주요 연산 복잡도 | 고르는 결정적 이유 |
| --- | --- | --- | --- |
| `vector` | 인덱스로 접근하고 순서대로 훑기만 함 | `a[i]` O(1), 탐색 O(n), 중간 삽입 O(n) | 메모리가 연속이라 상수배가 가장 작다 |
| 정렬한 `vector` + `lower_bound` | 삽입이 끝난 뒤 경계·개수 질의만 함 | 정렬 O(n log n), 질의 O(log n), 삽입 O(n) | 갱신이 없으면 `set`보다 몇 배 빠르다 |
| `unordered_set` | "이 값이 있는가"를 수없이 물음 | `count`·`insert`·`erase` 평균 O(1) | 해시가 버킷을 계산해 주므로 비교 한 번 |
| `unordered_map` | "키 → 값 대응을 읽고 고친다", 빈도 세기 | 조회·삽입·삭제 평균 O(1) | `m[k]++`가 없는 키 초기화까지 해 준다 |
| `set` | 정렬 순서 유지 + 삽입·삭제가 섞임 | 삽입·삭제·`lower_bound` O(log n), `begin`/`rbegin` O(1) | **파이썬에 없는 TreeSet이 표준으로 있다** |
| `multiset` | 같은 값이 여러 개, 최소·최대를 계속 지움 | 삽입·삭제·조회 O(log n) | 중복을 세지 않고 그대로 담을 수 있다 |
| `map` | 키를 정렬 순서로 순회·범위 질의 | 모든 연산 O(log n) | 순회 자체가 오름차순이라 재정렬이 없다 |
| `deque` | 양끝에서 넣고 뺀다(큐·슬라이딩 윈도우) | 양끝 O(1), 인덱스 O(1), 중간 O(n) | 블록 구조라 원소 이동이 없다 |
| `priority_queue` | "가장 큰(작은) 것을 반복해서 꺼낸다" | `push`·`pop` O(log n), `top` O(1) | 전체를 정렬하지 않고 극단만 유지 |
| `list` | 노드 참조를 들고 중간을 넣고 뺀다 | 삽입·삭제 O(1)(이터레이터 보유 시), 접근 O(n) | 다른 원소의 이터레이터가 무효화되지 않는다 |
| `nxt`/`prv` 배열 | 노드 번호가 `1..N`으로 정해진 연결 리스트 | 삽입·삭제·복원 O(1) | 동적 할당이 없어 `list`보다 상수배가 작다 |

같은 질문을 문제 문장 쪽에서 되짚으면 이렇게 갈린다.

| 무엇을 묻는 문제인가 | 고르는 것 | 이유 |
| --- | --- | --- |
| 중복을 없애고 개수만 세기 | `unordered_set` 또는 `sort` + `unique` | 정렬 순회가 필요 없으면 해시가 더 싸다 |
| "몇 번 나왔는가"(빈도) | `unordered_map<T,int>` | `m[x]++` 한 줄, 평균 O(1) |
| "키마다 목록을 모은다"(그룹핑) | `unordered_map<T, vector<U>>` | `m[k].push_back(v)`가 빈 벡터를 자동 생성 |
| "상위 K개만 계속 유지" | 크기 K 최소 힙 | top이 K개 중 최솟값 = 다음 탈락 후보 |
| "K번째로 작은 값" | 크기 K 최대 힙(`priority_queue<int>`) | 작은 K개의 최댓값이 곧 답 |
| "지금까지의 중앙값" | 최대 힙 + 최소 힙 | 절반씩 나누면 경계의 두 top이 중앙 |
| "최댓값과 최솟값을 둘 다 지운다" | `multiset` 또는 두 힙 + 지연 삭제 | 힙 하나로는 반대쪽 극단을 볼 수 없다 |
| "x 이하 최댓값 / x 이상 최솟값" | `set` 멤버 `lower_bound`/`upper_bound` | 트리를 타고 내려가 O(log n) |
| "[L, R] 안에 몇 개인가" | 정렬 `vector` + `upper_bound - lower_bound` | 두 경계의 차가 곧 개수 |
| 삽입·삭제가 정렬 질의와 대량으로 섞임 | `set`/`multiset` | 정렬 `vector`의 O(n) 이동이 병목이 된다 |
| "값으로 노드를 찾아 즉시 옮긴다"(LRU) | `unordered_map` + `list` + `splice` | 찾기와 잇기가 둘 다 O(1)이라야 전체가 O(1) |

헷갈리기 쉬운 짝들은 갈림 기준을 한 줄로 못 박아 둔다.

| 헷갈리는 짝 | 갈림 기준 | 결론 |
| --- | --- | --- |
| `set` vs `unordered_set` | 정렬 순회·경계 질의가 필요한가 | 필요하면 `set`, 존재 판정만이면 `unordered_set` |
| `map` vs `unordered_map` | n이 큰가, 순서가 필요한가 | 순서 필요하면 `map`, n이 수만 이하면 `map`도 빠르다 |
| `set` vs `multiset` | 같은 값이 여러 개 들어오는가 | 들어오면 `multiset`(단, `erase(x)`는 전부 지움) |
| 정렬 `vector` vs `set` | 삽입·삭제가 질의와 섞이는가 | 섞이면 `set`, 안 섞이면 정렬 `vector` |
| `priority_queue` vs `sort` | 전부 필요한가, 극단만 반복인가 | 전부면 `sort`, 반복 추출이면 힙 |
| `priority_queue` vs `multiset` | 중간 원소를 지워야 하는가 | 지워야 하면 `multiset`(또는 지연 삭제) |
| `deque` vs `list` | 중간을 건드리는가 | 양끝만이면 `deque`, 중간이면 `list`나 배열 링크 |
| `s.lower_bound(x)` vs `std::lower_bound` | 대상이 `set`인가 `vector`인가 | `set`이면 멤버(O(log n)), `vector`면 표준(O(log n)) |
| `lower_bound` vs `upper_bound` | 경계에 같은 값을 포함하는가 | "이상(≥)"은 lower, "초과(>)"는 upper |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: `unordered_map`의 평균 O(1)이 "적재율을 `max_load_factor` 이하로 유지하는 rehash" 위에 서 있다는 것과, 최악이 O(n)이 되는 조건.
- [ ] 설명할 수 있다: C++ 해시에 난수 시드가 없다는 사실이 왜 저격 입력의 빌미가 되는지와, 그때 무엇으로 갈아타는지.
- [ ] 설명할 수 있다: `unordered_map<pair<int,int>,T>`가 컴파일되지 않는 이유와, 좌표를 키로 쓰는 두 가지 우회.
- [ ] 설명할 수 있다: `m[k]`와 `m.find(k)`·`m.count(k)`가 없는 키에 각각 어떻게 반응하는지.
- [ ] 설명할 수 있다: `lower_bound`가 "x 미만 개수", `upper_bound`가 "x 이하 개수"라는 정의 하나에서 pred·succ·구간 개수 공식을 전부 다시 만들어 내기.
- [ ] 설명할 수 있다: 정렬 `vector` 삽입이 "위치 찾기 O(log n) + 자리 만들기 O(n)"이라 O(n)인 이유와, 그럼에도 `set`보다 정렬 `vector`를 고르는 상황.
- [ ] 설명할 수 있다: `s.lower_bound(x)`와 `std::lower_bound(s.begin(), s.end(), x)`의 복잡도가 다른 이유와, 그 차이가 왜 "틀린 답"이 아니라 "느린 답"으로만 나타나는지.
- [ ] 설명할 수 있다: 힙이 완전이진트리라 높이가 log n이고, 그래서 push·pop이 O(log n)이 되는 과정.
- [ ] 설명할 수 있다: 범위 생성자(`make_heap`)가 O(n)인데 하나씩 push하면 O(n log n)인 이유.
- [ ] 설명할 수 있다: 최대 힙에서 최솟값을 O(1)에 볼 수 없는 이유(형제 사이에 순서가 없다).
- [ ] 설명할 수 있다: `priority_queue`의 비교자가 `sort`의 비교자와 방향이 반대인 이유와, `less`가 왜 최대 힙인지.
- [ ] 설명할 수 있다: "K번째로 작은 값"은 최대 힙, "상위 K개의 합"은 최소 힙이라는 방향을 그림 없이 말로 설명하기.
- [ ] 설명할 수 있다: 힙에서 임의 원소를 지울 수 없는 이유와, 지연 삭제가 왜 분할상환 O(log n)인지, 그리고 `multiset`이 그 우회를 어떻게 없애는지.
- [ ] 설명할 수 있다: `set`의 원소가 `const`인 이유와, 값을 바꿔야 할 때의 정석 절차.
- [ ] 설명할 수 있다: 이중 연결 리스트의 삭제가 O(1)이려면 "노드를 이미 손에 쥐고 있어야 한다"는 전제와, LRU가 해시맵을 곁들이는 이유.
- [ ] 설명할 수 있다: `list`의 이터레이터가 다른 원소의 삽입·삭제에 무효화되지 않는 반면 `vector`는 왜 전부 무효화되는지.
- [ ] 설명할 수 있다: 센티넬 노드가 없애 주는 경계 분기가 정확히 어떤 코드였는지.
- [ ] 설명할 수 있다: `deque`와 `list`와 `nxt`/`prv` 배열 중 무엇을 고를지 한 문장으로.

**⚠️ 자주 하는 실수**

**1) 없는 키를 `m[key]`로 읽어 조용히 삽입한다**

```cpp
// ❌ 틀린 코드
unordered_map<int,int> cnt;
for (int q : queries) {
    if (cnt[q] > 0) { /* ... */ }   // 읽기만 하려 했는데 키가 생긴다
}
cout << cnt.size() << '\n';         // 실제로 센 것보다 훨씬 크다
```

왜: `operator[]`는 키가 없으면 **기본값으로 만들어 넣고** 그 참조를 돌려준다. 값 자체는 0이라 조건은 맞아 보이지만 맵이 조용히 부풀어 오르고, `size()`나 순회 결과가 전부 어긋난다. 파이썬 `dict[k]`가 `KeyError`로 그 자리에서 터지는 것과 달리 C++는 아무 신호도 주지 않는다.

```cpp
// ✅ 고친 코드 — 존재만 볼 땐 count/find, 누적할 때만 operator[]
if (cnt.count(q)) { /* ... */ }             // 키를 만들지 않는다
auto it = cnt.find(q);
int v = (it != cnt.end()) ? it->second : 0; // 값도 필요하면 find 한 번으로
for (int x : arr) cnt[x]++;                 // 누적은 operator[]가 맞는 자리
```

**2) `set`에 `std::lower_bound`를 써서 O(n)으로 만든다**

```cpp
// ❌ 틀린 코드
set<int> s(v.begin(), v.end());
for (int x : queries) {
    auto it = lower_bound(s.begin(), s.end(), x);   // 이터레이터를 한 칸씩 전진
    if (it != s.end()) cout << *it << '\n';         // 결과는 맞지만 O(n)
}
```

왜: `std::lower_bound`는 **랜덤 액세스 이터레이터**일 때만 이분탐색을 한다. `set`의 이터레이터는 양방향(bidirectional)이라 중간으로 점프할 수 없어 처음부터 한 칸씩 걷는다. 답이 맞기 때문에 예제는 통과하고 큰 입력에서만 시간 초과가 나므로 원인을 찾기가 가장 어려운 부류다.

```cpp
// ✅ 고친 코드 — set/map/multiset에서는 멤버 함수를 쓴다
auto it = s.lower_bound(x);        // 트리를 타고 내려간다, O(log n)
if (it != s.end()) cout << *it << '\n';
// std::lower_bound는 정렬된 vector·배열 전용이라고 외워 둔다
```

**3) `priority_queue`의 비교자 방향을 반대로 안다**

```cpp
// ❌ 틀린 코드 — 최소 힙을 만들려고 했다
priority_queue<int, vector<int>, less<int>> pq;   // less인데 최대 힙이 된다
for (int x : arr) pq.push(x);
cout << pq.top() << '\n';                          // 최솟값이 아니라 최댓값
```

왜: `priority_queue`의 비교자는 "먼저 나올 것"이 아니라 **"나중에 나올 것"**을 참으로 만든다. `less(a,b)`가 참이면 "a가 b보다 우선순위가 낮다"는 뜻이라 큰 값이 위로 올라온다. `sort`의 비교자(앞에 올 것을 참으로)와 방향이 정반대인 것이 실수의 근원이다.

```cpp
// ✅ 고친 코드
priority_queue<int, vector<int>, greater<int>> pq;   // 최소 힙
priority_queue<int> maxq;                            // 최대 힙(기본값)
// 커스텀 구조체도 같은 규칙: cmp(a,b)==true 이면 a가 나중에 나온다
struct Cmp { bool operator()(const Node& a, const Node& b) const {
    return a.cost > b.cost;      // 비용이 큰 쪽이 나중 -> 비용 작은 순으로 나온다
}};
```

**4) `pop()`이 값을 돌려준다고 생각하거나 빈 큐를 건드린다**

```cpp
// ❌ 틀린 코드
int x = pq.pop();            // 컴파일 에러: pop()의 반환형은 void
while (true) {
    int y = pq.top();        // 비었으면 미정의 동작 — 예외도 안 난다
    pq.pop();
    if (pq.empty()) break;
}
```

왜: C++ 컨테이너 어댑터는 예외 안전성 때문에 "읽기(`top`)"와 "지우기(`pop`)"를 분리했다. 그리고 빈 큐에 `top()`·`pop()`을 부르는 것은 예외가 아니라 **미정의 동작**이라, 쓰레기 값이 나오거나 그냥 죽는다. 파이썬 `heappop`이 `IndexError`를 던져 주는 것과 다르다.

```cpp
// ✅ 고친 코드 — 읽고 지운다, 그리고 비었는지 먼저 본다
while (!pq.empty()) {
    int y = pq.top();
    pq.pop();
    // ... y 사용
}
```

**5) 정렬 `vector`에 삽입을 반복해 O(N²)를 만든다**

```cpp
// ❌ 틀린 코드
vector<int> a;
for (int x : arr) {                                    // N = 200000
    a.insert(lower_bound(a.begin(), a.end(), x), x);   // 위치는 O(log n)
}                                                      // 밀기가 O(n)
cout << a[k-1] << '\n';
```

왜: 자리를 찾는 것과 자리를 만드는 것은 다른 비용이다. `vector`는 원소가 연속이라 중간에 끼우려면 뒤를 전부 한 칸씩 밀어야 하므로 한 번이 O(n)이고, N번 반복하면 O(N²)다. N=20만이면 200억 번이다.

```cpp
// ✅ 고친 코드 — 삽입이 다 끝난 뒤 조회만 한다면 한 번만 정렬한다
vector<int> a(arr.begin(), arr.end());
sort(a.begin(), a.end());              // O(N log N)
cout << a[k-1] << '\n';
// 삽입·삭제가 조회와 계속 섞인다면 set/multiset으로 간다 (연산당 O(log n))
```

**6) `multiset::erase(x)`로 하나만 지우려 한다**

```cpp
// ❌ 틀린 코드
multiset<int> ms = {5, 5, 5, 7};
ms.erase(5);                 // 5를 하나만 빼려던 의도
cout << ms.size() << '\n';   // 1 — 세 개가 한꺼번에 사라졌다
```

왜: 값을 받는 `erase(const key_type&)`는 **그 키와 같은 원소를 전부 지우고 지운 개수를 반환**한다. `set`에서는 원소가 유일하니 차이가 드러나지 않다가, `multiset`으로 바꾸는 순간 조용히 달라진다.

```cpp
// ✅ 고친 코드 — 하나만 지우려면 이터레이터로 지운다
auto it = ms.find(5);
if (it != ms.end()) ms.erase(it);   // 정확히 한 개
// 최소·최대를 하나씩 뺄 때도 같다: ms.erase(ms.begin()), ms.erase(prev(ms.end()))
```

**7) 순회하면서 원소를 지워 이터레이터를 무효화한다**

```cpp
// ❌ 틀린 코드
for (auto it = m.begin(); it != m.end(); ++it) {
    if (it->second == 0) m.erase(it);   // 지운 뒤 ++it -> 무효 이터레이터
}
for (int i = 0; i < (int)v.size(); i++) {
    if (v[i] < 0) v.erase(v.begin() + i);   // 뒤 원소가 당겨져 한 칸씩 건너뛴다
}
```

왜: `erase(it)` 이후 `it`는 무효라 `++it`가 미정의 동작이다. `vector`는 더 나쁘다 — 지우면 뒤가 전부 당겨지는데 `i`는 그대로 증가하므로 **연속된 원소를 건너뛰고**, 게다가 매번 O(n)이라 전체가 O(n²)다.

```cpp
// ✅ 고친 코드 — 반환된 이터레이터로 진행하거나, remove_if로 한 번에
for (auto it = m.begin(); it != m.end(); ) {
    if (it->second == 0) it = m.erase(it);   // erase가 다음 이터레이터를 준다
    else ++it;
}
v.erase(remove_if(v.begin(), v.end(),
                  [](int x){ return x < 0; }), v.end());   // O(n) 한 번
```

**8) 이중 연결 리스트에서 링크를 한쪽만 고친다**

```cpp
// ❌ 틀린 코드
void unlink(int x) {
    nxt[prv[x]] = nxt[x];        // 앞 -> 뒤 방향만 이어 붙였다
}
```

왜: 뒤에서 앞으로 가는 길은 여전히 x를 가리킨다. 앞에서부터 순회하면 멀쩡해 보이다가, 역방향 순회나 `prv[nxt[x]]`를 쓰는 순간 이미 지운 x로 되돌아간다. **삭제는 링크 두 개, 삽입은 네 개**를 반드시 짝으로 고쳐야 한다.

```cpp
// ✅ 고친 코드
void unlink(int x) {
    int p = prv[x], q = nxt[x];
    nxt[p] = q;
    prv[q] = p;                  // x의 prv/nxt는 남겨 둔다 -> restore(x)로 복원 가능
}
```

**다음 챕터로**

- 이 챕터의 도구들은 다음 챕터(Shorten time Technique)에서 **전처리의 재료**로 다시 나온다. 좌표 압축의 `sort` + `unique`는 여기서 배운 정렬 `vector` 그대로이고, "값 → 순위" 변환은 `lower_bound`의 전형적인 쓰임이다.
- 이분 경계 감각도 그대로 이어진다. 압축된 좌표에서 `[L, R]` 구간을 찾을 때, 누적합 위에서 조건을 만족하는 경계를 찾을 때 다시 등장하며, 그 다음 챕터의 이진탐색에서는 `lower_bound`가 하던 일을 직접 손으로 구현하게 된다.
- 반대로 "질의와 갱신이 번갈아 오는" 상황에서 `set`의 O(log n)조차 부족해지는 지점(구간 합·구간 최솟값을 통째로 물을 때)이 펜윅 트리·세그먼트 트리라는 다음 단계로 가는 정확한 이유가 된다.
