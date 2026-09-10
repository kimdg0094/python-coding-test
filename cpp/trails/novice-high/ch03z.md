## L12. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 레슨은 Ch3(정렬) 전체를 하나의 선택 절차로 접는다. 정렬 알고리즘을 외우는 것이 목적이 아니라, **"이 문제에서 무엇을 보장해야 하는가"**를 세 축(안정성·공간·최악 보장)으로 읽고 도구를 고르는 것이 목적이다.

- C++에서는 결론이 더 단순하다. **실전 정답은 거의 항상 `std::sort`(또는 안정성이 필요하면 `std::stable_sort`)이고, 직접 구현하는 것은 원리를 묻거나 정렬 과정 자체가 답일 때다.** 대신 `sort`를 쓸 때 지켜야 할 규칙(비교자의 strict weak ordering, 안정성 미보장)이 새로 생긴다.

**개념 지도**

```text
                               sorting
                                  |
                +-----------------+-----------------+
         comparison based                     non-comparison
                |                                   |
         +------+------------+               radix (LSD)
   O(n^2) family     O(n log n) family       bucket by digit
   bubble : swap     merge : split + merge   stable = correctness
   select : pick min quick : partition       O(d * n), space O(n)
   insert : shift    heap  : tree in array   # 키가 고정폭 정수일 때만
   space O(1)        merge stable + O(n)
   n <= 3000         quick, heap : in-place
                |                                   |
                +-----------------+-----------------+
                                  |
   lower bound : n! leaves -> height >= log2(n!) = Omega(n log n)
 -------------------------------------------------------------
   std::sort        = introsort ( quick + heap + insertion )
                      average O(n log n) , worst O(n log n) , UNSTABLE
   std::stable_sort = merge based , STABLE , O(n log n) with buffer
   std::partial_sort / nth_element  = top-k / k-th only
```

이 챕터의 갈림길은 두 번 열린다.

- 첫 갈림길은 **"값을 서로 비교할 것인가"**다. 비교하는 순간 결정 트리 논증에 걸려 최악 비교 횟수가 n log n 아래로 못 내려간다. 기수 정렬만 이 문을 피해 가는데, 대신 "키가 자릿수를 가진 고정폭"이어야 한다는 값을 치른다.
- 두 번째 갈림길은 비교 정렬 안에서 **"한 번에 얼마나 멀리 보내는가"**다. 인접한 것만 바꾸면(거품·삽입) 한 번에 역위 하나를 지워 O(n²)이 되고, 반씩 쪼개거나(병합·퀵) 트리 높이만큼 뛰면(힙) 한 번에 여러 개를 정리해 O(n log n)이 된다.
- 그 아래에서 실전 선택을 가르는 축은 셋뿐이다 — **안정성**(동점 순서를 지키나), **공간**(임시 배열을 쓰나), **최악 보장**(순수 퀵만 O(n²)로 무너질 수 있다).
- `std::sort`는 세 알고리즘을 섞은 introsort다. 기본은 퀵(상수가 작다), 재귀가 `2·log₂n`보다 깊어지면 힙으로 갈아타 최악을 O(n log n)으로 묶고, 구간이 16 이하로 짧아지면 삽입 정렬로 마무리한다. 그래서 **평균은 퀵만큼 빠르고 최악은 힙만큼 안전**하지만, **안정성은 주지 않는다.** 동점 순서가 답에 영향을 준다면 `std::stable_sort`로 바꾼다.

**뼈대 코드**

```cpp
// 1) O(n^2) 3형제 - 최소 골격
void bubble(vector<int>& a) {
    int n = (int)a.size();
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < n - 1 - i; j++) {  // 뒤쪽 i 개는 확정 -> 범위를 줄인다
            if (a[j] > a[j + 1]) {             // '>' 만. '>=' 면 안정성이 깨짐
                swap(a[j], a[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;                   // 교환 0 -> 이미 정렬됨
    }
}

void selection(vector<int>& a) {
    int n = (int)a.size();
    for (int i = 0; i < n - 1; i++) {
        int m = i;
        for (int j = i + 1; j < n; j++)
            if (a[j] < a[m]) m = j;            // 인덱스만 갱신
        if (m != i) swap(a[i], a[m]);          // 교환은 밖에서 한 번
    }
}

void insertion(vector<int>& a) {
    int n = (int)a.size();
    for (int i = 1; i < n; i++) {
        int key = a[i];                        // 먼저 꺼내 둬야 덮어써도 안 잃는다
        int j = i - 1;
        while (j >= 0 && a[j] > key) {         // j >= 0 을 앞에 둬야 a[-1] 회피
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = key;
    }
}
```

```cpp
// 2) 병합 정렬 - 항상 O(n log n), 안정, 공간 O(n)
void merge_part(vector<int>& a, vector<int>& buf, int lo, int mid, int hi) {
    int i = lo, j = mid + 1, k = lo;
    while (i <= mid && j <= hi)
        buf[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];   // '<=' 왼쪽 우선이라 안정
    while (i <= mid) buf[k++] = a[i++];
    while (j <= hi)  buf[k++] = a[j++];                // 남은 꼬리 (빠뜨리기 쉬움)
    for (int t = lo; t <= hi; t++) a[t] = buf[t];
}

void merge_sort(vector<int>& a, vector<int>& buf, int lo, int hi) {
    if (lo >= hi) return;
    int mid = lo + (hi - lo) / 2;              // (lo+hi)/2 는 오버플로 위험
    merge_sort(a, buf, lo, mid);
    merge_sort(a, buf, mid + 1, hi);
    merge_part(a, buf, lo, mid, hi);
}
// 호출 : vector<int> buf(a.size()); merge_sort(a, buf, 0, (int)a.size()-1);
```

```cpp
// 3) 퀵 정렬 - 제자리 분할과 최악 방어
int partition(vector<int>& a, int lo, int hi) {   // Lomuto, 피벗 = a[hi]
    int pivot = a[hi];
    int i = lo - 1;
    for (int j = lo; j < hi; j++) {
        if (a[j] <= pivot) { i++; swap(a[i], a[j]); }
    }
    swap(a[i + 1], a[hi]);                  // i 가 아니라 i+1 (대표적 off-by-one)
    return i + 1;
}

static mt19937 rng(12345);                  // 저격 입력 방어용 무작위 피벗

void quick_sort(vector<int>& a, int lo, int hi) {
    while (lo < hi) {
        int p = lo + (int)(rng() % (unsigned)(hi - lo + 1));   // 문제마다 바뀜
        swap(a[p], a[hi]);
        int q = partition(a, lo, hi);
        if (q - lo < hi - q) { quick_sort(a, lo, q - 1); lo = q + 1; }
        else                 { quick_sort(a, q + 1, hi); hi = q - 1; }
        // 작은 쪽만 재귀 -> 스택 깊이가 최악에도 O(log n)
    }
}
```

```cpp
// 4) 힙 - 전체 정렬보다 '극값 반복 추출'에 쓴다
vector<int> heap_sort(vector<int> a) {      // 값 복사본을 정렬해 돌려준다
    make_heap(a.begin(), a.end());          // O(n) 에 최대 힙 구성
    sort_heap(a.begin(), a.end());          // O(n log n) 에 오름차순
    return a;
}

vector<int> top_k(const vector<int>& a, int k) {   // 상위 k 개를 O(n log k) 에
    priority_queue<int, vector<int>, greater<int>> pq;   // 최소 힙
    for (int x : a) {
        pq.push(x);                         // 문제마다 바뀜(비교 기준)
        if ((int)pq.size() > k) pq.pop();   // 가장 작은 것을 버려 크기를 k 로
    }
    vector<int> out;
    while (!pq.empty()) { out.push_back(pq.top()); pq.pop(); }
    reverse(out.begin(), out.end());        // 큰 값부터
    return out;
}
```

```cpp
// 5) 실전 - sort 비교자 패턴 모음
struct Row { string name; int score, id; };
vector<Row> rows = {{"kim",90,3}, {"lee",85,1}, {"park",90,2}};

// 제자리 정렬. 반환값이 없다 (파이썬의 list.sort 처럼 원본을 고친다)
sort(rows.begin(), rows.end(),
     [](const Row& a, const Row& b){ return a.score < b.score; });

// 다중 기준 : 순위대로, 방향은 부등호로. 모두 같으면 반드시 false 여야 한다
sort(rows.begin(), rows.end(), [](const Row& a, const Row& b){
    if (a.score != b.score) return a.score > b.score;   // 1순위 : 점수 내림
    return a.name < b.name;                             // 2순위 : 이름 오름
});                                                     // 문제마다 바뀜

// 방향이 뒤섞여 한 식으로 쓰기 싫을 때 : 낮은 순위부터 여러 번 안정 정렬
stable_sort(rows.begin(), rows.end(),
            [](const Row& a, const Row& b){ return a.name < b.name; });
stable_sort(rows.begin(), rows.end(),
            [](const Row& a, const Row& b){ return a.score > b.score; });

// 동점 순서를 라이브러리에 맡기지 않고 못 박는 가장 안전한 방법
vector<tuple<int, string, int>> t;          // (-score, name, id)
for (auto& r : rows) t.emplace_back(-r.score, r.name, r.id);
sort(t.begin(), t.end());                   // tuple 의 사전식 비교 - 완전 결정적

// 중복 제거 후 정렬
vector<int> v = {3, 1, 3};
sort(v.begin(), v.end());
v.erase(unique(v.begin(), v.end()), v.end());   // unique 는 정렬 후에만 옳다
```

**언제 무엇을 쓰나**

정렬 알고리즘 비교표 (n = 원소 수, d = 자릿수)

| 알고리즘 | 평균 | 최악 | 최선 | 추가 공간 | 안정성 | `std::sort` 대비 | 언제 쓰나 |
|---|---|---|---|---|---|---|---|
| 거품 | O(n²) | O(n²) | O(n) | O(1) | 안정 | 압도적으로 느림 | 학습용. 조기 종료가 있어 거의 정렬된 입력에만 |
| 선택 | O(n²) | O(n²) | O(n²) | O(1) | 불안정 | 압도적으로 느림 | 교환·쓰기 비용이 비교보다 훨씬 비쌀 때(교환 ≤ n-1) |
| 삽입 | O(n²) | O(n²) | O(n) | O(1) | 안정 | 짧은 구간(≤16)에서는 오히려 빠름 | n이 작거나 거의 정렬됨. `sort` 내부에서도 쓰인다 |
| 병합 | O(n log n) | O(n log n) | O(n log n) | O(n) | 안정 | `stable_sort`가 이것 | 최악 보장 + 안정성 필요, 역순쌍 세기 |
| 퀵 | O(n log n) | O(n²) | O(n log n) | O(log n) | 불안정 | `sort`의 기본 경로 | 평균이 가장 빠름. k번째 값만 필요하면 `nth_element` |
| 힙 | O(n log n) | O(n log n) | O(n log n) | O(1) | 불안정 | `sort`의 최악 방어 경로 | 최악 보장 + 제자리. 상위 k개, 우선순위 처리 |
| 기수 | O(d·n) | O(d·n) | O(d·n) | O(n) | 안정 | n이 크고 d가 작으면 더 빠름 | 키가 좁은 범위의 고정폭 정수 |
| `std::sort` | O(n log n) | O(n log n) | O(n log n) | O(log n) | **불안정** | 기준 | 특별한 이유가 없으면 이것 |
| `std::stable_sort` | O(n log n) | O(n log n)* | O(n log n) | O(n) | 안정 | 약간 느리고 메모리를 씀 | 동점 순서를 지켜야 할 때 |

`*` 버퍼를 얻지 못하면 O(n log² n)으로 떨어진다(대신 공간을 아낀다).

상황별 선택 기준

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 그냥 정렬해야 한다 | `sort(v.begin(), v.end())` | 최악 보장 + 가장 빠른 실측 | O(n log n) |
| 동점 순서를 입력대로 지켜야 한다 | `stable_sort` | `sort`는 동점 순서를 보장하지 않는다 | O(n log n) |
| 동점 규칙을 라이브러리에 안 맡기고 싶다 | 인덱스를 비교자 마지막 기준으로 | 구현과 무관하게 결정적 | O(n log n) |
| 기준이 여러 개고 방향이 뒤섞임 | `tuple` 사전식 또는 다단 `stable_sort` | 부호 반전과 안정성으로 방향을 맞춘다 | O(k·n log n) |
| 정렬 과정 자체를 출력해야 한다 | 그 알고리즘을 직접 구현 | 패스별 스냅샷은 `sort`로 못 뽑음 | 알고리즘에 따름 |
| n ≤ 수천이고 거의 정렬돼 있다 | 삽입 정렬 | 역위가 적어 실측이 O(n)에 근접 | 최선 O(n) |
| 교환 비용이 압도적으로 크다 | 인덱스 배열을 대신 정렬 | 실제 데이터를 옮기지 않는다 | 이동 O(n) |
| 최악에도 시간이 보장돼야 한다 | `sort` 또는 병합·힙 | 손으로 짠 퀵은 피벗이 치우치면 O(n²) | O(n log n) |
| 메모리가 빠듯하다 | `sort`(제자리) | `stable_sort`는 O(n) 버퍼를 씀 | 공간 O(log n) |
| 전체가 아니라 상위 k개만 필요 | `partial_sort` 또는 크기 k 최소 힙 | 정렬 전체를 만들 필요가 없음 | O(n log k) |
| k번째 값 하나만 필요 | `nth_element` | 한쪽 구간만 재귀 | 평균 O(n) |
| 키가 0~999999 같은 정수 | 기수·계수 정렬 | 비교를 아예 안 해 하한을 우회 | O(d·n) |
| 정렬된 배열에서 중복 제거 | `sort` 후 `unique` + `erase` | `unique`는 인접 중복만 지운다 | O(n log n) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 거품·선택·삽입이 왜 O(n²)인가 — (n-1)+(n-2)+…+1의 합으로 유도할 수 있다.
- [ ] 설명할 수 있다: 거품 정렬 안쪽 범위가 왜 `n-1-i`인가.
- [ ] 설명할 수 있다: 선택 정렬만 최선도 O(n²)인 이유(조기 종료가 불가능한 이유).
- [ ] 설명할 수 있다: 삽입 정렬의 이동 횟수가 왜 역위(inversion) 개수와 같은가.
- [ ] 설명할 수 있다: 안정 정렬이 무엇이고, 왜 다단 정렬을 여러 번의 단일 정렬로 쪼갤 수 있게 해 주는가.
- [ ] 설명할 수 있다: 선택·퀵·힙이 왜 불안정한가 — 각각 최소 반례를 하나씩 들 수 있다.
- [ ] 설명할 수 있다: 병합 정렬이 왜 O(n log n)인가 — 레벨당 O(n) × log n 레벨로 유도할 수 있다.
- [ ] 설명할 수 있다: 병합에서 `<=`와 `<`의 차이가 안정성에 미치는 영향.
- [ ] 설명할 수 있다: 퀵 정렬의 최악 O(n²)이 어떤 입력·피벗 조합에서 나오고, 어떻게 피하는가.
- [ ] 설명할 수 있다: 힙이 완전 이진 트리를 배열 하나로 표현하는 방식(부모·자식 인덱스 공식).
- [ ] 설명할 수 있다: 힙 배열이 왜 "정렬된 배열"이 아닌가.
- [ ] 설명할 수 있다: 기수 정렬에서 안정성이 왜 성능이 아니라 정확성의 문제인가.
- [ ] 설명할 수 있다: 비교 기반 정렬의 하한이 왜 Ω(n log n)인가 — 결정 트리의 잎이 n!개라는 논증으로.
- [ ] 설명할 수 있다: 기수 정렬이 그 하한을 어떻게 피해 가고, 대신 무엇을 전제하는가.
- [ ] 설명할 수 있다: `std::sort`가 introsort로 세 알고리즘을 언제 갈아타는가.
- [ ] 설명할 수 있다: `sort`와 `stable_sort`의 차이(안정성·공간·속도)와 각각을 고를 기준.
- [ ] 설명할 수 있다: 비교자가 strict weak ordering이어야 하는 이유와, `<=`를 쓰면 왜 프로그램이 죽는가.
- [ ] 설명할 수 있다: `nth_element`·`partial_sort`가 전체 정렬보다 싼 이유.

**⚠️ 자주 하는 실수**

**1) 비교자에 `<=`를 써서 프로그램을 죽인다**

```cpp
// ❌ 틀린 코드
sort(v.begin(), v.end(), [](int a, int b){ return a <= b; });
// 또는 구조체에서
sort(rs.begin(), rs.end(), [](const Row& a, const Row& b){
    return a.score >= b.score;      // 같을 때도 true 를 돌려준다
});
```

왜: `sort`의 비교자는 **strict weak ordering**이어야 한다 — 핵심은 "같은 원소끼리는 반드시 `false`"다. `<=`는 `cmp(a, a)`가 참이라 이 규칙을 깨고, 표준 구현의 분할 루프가 **경계 검사 없이 배열 밖으로 넘어간다.** 결과는 오답이 아니라 대개 런타임 오류이고, 원소가 적을 때는 우연히 통과해 더 헷갈린다.

```cpp
// ✅ 고친 코드
sort(v.begin(), v.end(), [](int a, int b){ return a < b; });   // 순수 부등호
sort(rs.begin(), rs.end(), [](const Row& a, const Row& b){
    if (a.score != b.score) return a.score > b.score;
    return a.name < b.name;         // 모든 필드가 같으면 false 가 된다
});
```

**2) `sort`가 안정하다고 가정한다**

```cpp
// ❌ 틀린 코드
// "점수 내림차순, 동점이면 입력 순서" 라는 요구
sort(rows.begin(), rows.end(),
     [](const Row& a, const Row& b){ return a.score > b.score; });
// 로컬에서는 맞게 나왔는데 채점에서 틀린다
```

왜: `std::sort`는 introsort라 **동점 원소의 순서를 보장하지 않는다.** 원소 수·라이브러리 버전·컴파일 옵션에 따라 결과가 달라질 수 있어, 로컬 통과가 아무 증거가 되지 않는다.

```cpp
// ✅ 고친 코드
stable_sort(rows.begin(), rows.end(),
            [](const Row& a, const Row& b){ return a.score > b.score; });
// 또는 입력 순서를 비교자에 명시해 sort 로도 결정적으로 만든다
sort(rows.begin(), rows.end(), [](const Row& a, const Row& b){
    if (a.score != b.score) return a.score > b.score;
    return a.id < b.id;             // id = 입력 순서
});
```

**3) 거품 정렬의 안쪽 루프 범위를 잘못 잡는다**

```cpp
// ❌ 틀린 코드
for (int i = 0; i < n - 1; i++)
    for (int j = 0; j < n; j++)
        if (a[j] > a[j + 1])        // j 가 n-1 일 때 a[n] 을 읽는다
            swap(a[j], a[j + 1]);
```

왜: 안쪽 루프는 `a[j]`와 `a[j+1]` 두 칸을 보므로 `j`의 상한이 `n-2`여야 한다. C++의 `[]`는 범위를 검사하지 않으므로 **예외 없이 남의 메모리를 읽고 쓴다** — 우연히 통과했다가 다른 입력에서 터지는 유형이다. 게다가 패스 `i`가 끝나면 뒤쪽 `i`개는 이미 확정이라 다시 볼 필요도 없다.

```cpp
// ✅ 고친 코드
for (int i = 0; i < n - 1; i++)
    for (int j = 0; j < n - 1 - i; j++)   // -1 은 a[j+1], -i 는 확정 구간 때문
        if (a[j] > a[j + 1])
            swap(a[j], a[j + 1]);
```

**4) 순회하면서 그 컨테이너의 길이를 바꾼다**

```cpp
// ❌ 틀린 코드
for (int i = 0; i < (int)a.size(); i++)
    if (a[i] < 0) a.erase(a.begin() + i);   // 뒤가 당겨져 다음 원소를 건너뜀
// 범위 기반 for 라면 더 나쁘다 - 반복자가 통째로 무효가 된다
for (int x : a) if (x < 0) a.erase(find(a.begin(), a.end(), x));
```

왜: 원소를 지우면 뒤가 앞으로 당겨져 `i`가 이미 다음 원소를 지나쳐 버린다. `{-1, -2, 3}`에서 `-2`가 살아남는다. 범위 기반 `for` 중에 `erase`나 `push_back`을 하면 반복자가 무효가 되어 미정의 동작이 된다.

```cpp
// ✅ 고친 코드
a.erase(remove_if(a.begin(), a.end(),
                  [](int x){ return x < 0; }), a.end());   // 한 번에 O(n)
// 직접 쓴다면 지웠을 때 i 를 늘리지 않는다
for (int i = 0; i < (int)a.size(); ) {
    if (a[i] < 0) a.erase(a.begin() + i);
    else i++;
}
```

**5) 제자리 분할에서 피벗 인덱스를 하나 잘못 쓴다**

```cpp
// ❌ 틀린 코드
int partition(vector<int>& a, int lo, int hi) {
    int pivot = a[hi];
    int i = lo - 1;
    for (int j = lo; j < hi; j++)
        if (a[j] <= pivot) { i++; swap(a[i], a[j]); }
    swap(a[i], a[hi]);        // i 는 '피벗 이하 구간의 마지막'이다
    return i;
}
```

왜: 루프가 끝난 시점에 `a[lo..i]`는 피벗 이하, `a[i+1..hi-1]`은 피벗 초과다. 피벗이 들어갈 경계 자리는 `i`가 아니라 `i+1`이다. `i`와 바꾸면 피벗보다 작은 값이 오른쪽 구간으로 넘어가 분할이 깨지고, 정렬 결과가 조용히 틀린다.

```cpp
// ✅ 고친 코드
    swap(a[i + 1], a[hi]);
    return i + 1;
```

**6) 비교에 등호를 넣어 안정성을 깬다**

```cpp
// ❌ 틀린 코드
while (j >= 0 && a[j] >= key) {   // 같은 값도 넘어가 버린다
    a[j + 1] = a[j];
    j--;
}
```

왜: `key`와 값이 같은 원소까지 밀어내면 `key`가 그 앞으로 가서 동점 원소의 입력 순서가 뒤집힌다. 다단 정렬의 전제가 무너져, 2순위 기준으로 맞춰 둔 순서가 사라진다. 병합에서 `a[i] <= a[j]`의 등호를 빼는 것도 같은 결과를 낳는다.

```cpp
// ✅ 고친 코드
while (j >= 0 && a[j] > key) {    // 같은 값을 만나면 멈춰 뒤에 놓는다
    a[j + 1] = a[j];
    j--;
}
```

**7) 오름차순 정렬 후 `reverse`로 내림차순을 만든다**

```cpp
// ❌ 틀린 코드
stable_sort(rows.begin(), rows.end(),
            [](const Row& a, const Row& b){ return a.score < b.score; });
reverse(rows.begin(), rows.end());     // 동점의 순서까지 뒤집힌다
```

왜: `reverse`는 결과 전체를 뒤집으므로 값이 같은 원소들의 상대 순서도 함께 뒤집힌다. "점수 내림차순, 동점이면 입력 순서"라는 요구를 만족하지 못한다. 파이썬의 `sorted(...)[::-1]`이 `reverse=True`와 다른 것과 정확히 같은 이유다.

```cpp
// ✅ 고친 코드
stable_sort(rows.begin(), rows.end(),
            [](const Row& a, const Row& b){ return a.score > b.score; });
// 숫자 하나가 기준이면 키의 부호를 뒤집어도 된다
sort(v.begin(), v.end(), greater<int>());
```

**8) 힙 배열을 정렬된 배열로 착각한다**

```cpp
// ❌ 틀린 코드
vector<int> h = {5, 3, 8, 1};
make_heap(h.begin(), h.end());
for (int x : h) cout << x << ' ';     // 8 3 5 1 - 정렬돼 있지 않다
```

왜: 힙이 보장하는 것은 "부모 ≥ 자식"(기본은 최대 힙)뿐이고, 형제끼리의 대소는 아무 규칙이 없다. 루트만 최댓값이다. `priority_queue`도 마찬가지로 `top()` 하나만 의미가 있다.

```cpp
// ✅ 고친 코드
vector<int> h = {5, 3, 8, 1};
make_heap(h.begin(), h.end());
sort_heap(h.begin(), h.end());        // 하나씩 꺼내야 정렬 순서 : 1 3 5 8
for (int x : h) cout << x << ' ';
```

**9) `unique`를 정렬 없이 쓰거나 `erase`를 빼먹는다**

```cpp
// ❌ 틀린 코드
vector<int> v = {3, 1, 3, 1};
unique(v.begin(), v.end());           // 인접 중복만 지운다 + 크기가 안 변한다
cout << v.size() << '\n';             // 여전히 4
```

왜: `unique`는 **인접한** 중복만 앞으로 몰아 없애고, 실제로 크기를 줄이지 않는다. "남길 구간의 끝" 반복자를 돌려줄 뿐이다. 정렬하지 않으면 떨어져 있는 중복이 그대로 남고, `erase`를 빼먹으면 뒤쪽에 옛 값이 남는다.

```cpp
// ✅ 고친 코드
vector<int> v = {3, 1, 3, 1};
sort(v.begin(), v.end());                          // 먼저 정렬해 중복을 붙이고
v.erase(unique(v.begin(), v.end()), v.end());      // 반환값부터 끝까지 지운다
cout << v.size() << '\n';                          // 2
```

**다음 챕터로**

- 힙에서 잠깐 만난 "완전 이진 트리 + 배열 인덱스"는 이후 트리·우선순위 큐 챕터에서 본격적으로 다룬다. `sift-up`/`sift-down`을 직접 구현하면 `priority_queue`가 무엇을 대신해 줬는지 보인다.
- 분할 정복(병합·퀵)의 사고 틀은 다음 챕터의 이분 탐색으로 이어진다. "절반씩 줄인다 → log n"이라는 감각이 그대로 재사용되고, `mid = lo + (hi - lo) / 2`라는 오버플로 방어 습관도 그대로 이어진다.
- 정렬은 그 자체보다 전처리로 더 자주 쓰인다. 정렬해 두면 `lower_bound`, 투 포인터, 그리디의 교환 논증이 모두 가능해진다는 것이 이 챕터의 실전 결론이다. `lower_bound`가 "정렬된 범위에서만 옳다"는 전제도 여기서 나온다.
