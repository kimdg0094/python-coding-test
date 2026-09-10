## L5. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

**개념 지도**

Ch3은 "어떤 도구로 정렬하나"와 "무엇을 기준으로 정렬하나"라는 두 축으로 이루어져 있다. 도구는 두 개뿐이고, 기준은 비교 함수가 전부다.

```text
                   +---------------------+
                   |       sorting       |
                   +----------+----------+
            +-----------------+-----------------+
            |                                   |
      which tool                          which order
            |                                   |
   sort(b, e)        : in place       default   : operator <
   stable_sort(b, e) : keeps ties     cmp/lambda: you decide
            |                                   |
            +-----------------+-----------------+
                              |
             +----------------+----------------+
             |                |                |
       single value    object (pair)     many criteria
       v[0], v[n-1]    (name, score)     if (a.x != b.x)
       v[k-1], v[n/2]  fields stay glued   return a.x > b.x;
             |                |            return a.y < b.y;
             +----------------+----------------+
                              |
                              v
                 sort is NOT stable : ties may move
```

비교 함수를 어떻게 쓸지는 "기준이 몇 개이고 방향이 무엇인가"만 물으면 정해진다.

```text
   how many criteria?
        |
        +-- one, ascending   --> sort(b, e)
        +-- one, descending  --> sort(b, e, greater<T>())
        +-- two or more      --> sort(b, e, cmp) with a lambda
        |                        1st : if (a.k1 != b.k1) return a.k1 < b.k1;
        |                        2nd : return a.k2 > b.k2;
        +-- ties must keep input order --> stable_sort, or add an index
```

방향은 부등호가 정한다. `<`면 오름차순, `>`면 내림차순 — 숫자든 문자열이든 규칙이 같다. 파이썬처럼 값에 `-`를 붙이는 우회가 필요 없다.

```text
   cmp(a, b) answers ONE question : should a come before b ?

   return a.score < b.score;   // small first  -> ascending
   return a.score > b.score;   // big first    -> descending
   return a.score <= b.score;  // FORBIDDEN : not a strict ordering
                               // sort may run off the array and crash
```

**뼈대 코드**

```cpp
// 1) 기본 — 정렬해 두면 원하는 값이 인덱스에 고정된다
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    sort(a.begin(), a.end());                 // 제자리 오름차순
    cout << a[0] << ' ' << a[n-1] << ' ' << a[n/2] << "\n";  // <- 최소·최대·중앙값

    vector<int> b = a;                        // 중복 제거는 정렬 후 unique + erase
    b.erase(unique(b.begin(), b.end()), b.end());
    for (int i = 0; i < (int)b.size(); i++) cout << b[i] << " \n"[i + 1 == (int)b.size()];
    return 0;
}
```

```cpp
// 2) 객체(pair) 다중 기준 정렬 — 실전 정렬 문제의 대부분
struct Item { string name; int score; };      // <- 문제마다 바뀜: 필드 구성

void solve(vector<Item>& items) {
    sort(items.begin(), items.end(), [](const Item& a, const Item& b) {
        if (a.score != b.score) return a.score > b.score;  // <- 1순위 점수 내림
        return a.name < b.name;                            // <- 2순위 이름 오름
    });
    for (const auto& it : items) cout << it.name << ' ' << it.score << "\n";
}
```

```cpp
// 3) 비교 함수 패턴 모음 — 규칙을 말로 적은 뒤 그대로 옮긴다
// 한 필드 오름차순
// sort(v.begin(), v.end(), [](const P& a, const P& b){ return a.second < b.second; });
// 한 필드 내림차순 (문자열도 그대로 됨)
// sort(v.begin(), v.end(), [](const P& a, const P& b){ return a.second > b.second; });
// 1순위 오름 -> 2순위 오름 : pair 기본 비교로 충분
// sort(v.begin(), v.end());
// 1순위 내림 -> 2순위 오름
// sort(v.begin(), v.end(), [](const P& a, const P& b){
//     if (a.second != b.second) return a.second > b.second;
//     return a.first < b.first;
// });
// 계산 키(길이 먼저, 같으면 사전순) — 무거운 계산은 미리 필드로 만들어 둔다
// sort(w.begin(), w.end(), [](const string& a, const string& b){
//     if (a.size() != b.size()) return a.size() < b.size();
//     return a < b;
// });
int dummy_pattern_marker = 0;
```

```cpp
// 4) 정렬 후 인접 비교 — 이웃끼리만 보면 O(N)에 끝난다
int min_gap(vector<int>& a) {
    sort(a.begin(), a.end());
    int n = a.size();                     // size()는 부호 없는 수라 int 로 받아 둔다
    int best = a[1] - a[0];               // <- 문제마다 바뀜: 초깃값
    for (int i = 0; i + 1 < n; i++)       // i+1 을 읽으므로 경계에 주의
        best = min(best, a[i + 1] - a[i]);
    return best;
}
```

```cpp
// 5) 동점 순서를 지켜야 할 때 — C++ sort 는 안정 정렬이 아니다
struct Rec { int key; int idx; };         // idx = 입력 순서

void keep_input_order(vector<Rec>& v) {
    // 방법 A : stable_sort 에 맡긴다
    stable_sort(v.begin(), v.end(), [](const Rec& a, const Rec& b) {
        return a.key > b.key;
    });
    // 방법 B : 입력 순서를 최하위 기준으로 명시한다 (권장)
    sort(v.begin(), v.end(), [](const Rec& a, const Rec& b) {
        if (a.key != b.key) return a.key > b.key;
        return a.idx < b.idx;
    });
}
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 원본 순서를 나중에 또 쓴다 | 사본을 떠서 정렬 | `sort`는 원본을 덮어쓴다 | O(N log N) + O(N) 공간 |
| 원본이 더 이상 필요 없다 | `sort(v.begin(), v.end())` | 제자리라 추가 공간이 거의 없다 | O(N log N) |
| 기준이 하나고 내림차순이다 | `greater<T>()` 또는 `>` 람다 | 부등호 하나로 끝난다 | O(N log N) |
| 기준마다 방향이 다르다 | 람다에서 순위별로 부등호 지정 | 순위마다 독립적으로 정할 수 있다 | O(N log N) |
| 문자열을 내림차순으로 | `return a > b;` | C++은 문자열도 부등호를 뒤집으면 된다 | O(N log N) |
| 비교값을 계산해야 한다 | 미리 필드에 넣어 두고 비교 | 비교 함수는 N log N 번 호출된다 | 계산 N회 + O(N log N) |
| 동점은 입력 순서 유지 | `stable_sort` 또는 인덱스 필드 | `sort`는 안정 정렬이 아니다 | O(N log N) |
| k번째로 작은 값 | 정렬 후 `v[k-1]` | 자리가 고정된다 | O(N log N) + O(1) |
| 중복을 없앤 뒤 줄 세운다 | `sort` → `unique` → `erase` | `unique`는 이웃 중복만 없앤다 | O(N log N) |
| 가장 가까운 두 값 | 정렬 후 인접 차이 최소 | 정렬하면 후보가 이웃뿐 | O(N log N) + O(N) |
| 필드 2개, 둘 다 오름차순 | 비교 함수 없이 `sort`만 | `pair`는 기본이 사전식 비교 | O(N log N) |
| 상위 k개만 필요하다 | `partial_sort` / `nth_element` | 전부 정렬할 필요가 없다 | O(N log k) / O(N) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: `std::sort`가 제자리 정렬이라 원본을 덮어쓴다는 것과, 원본을 지키는 방법.
- [ ] 설명할 수 있다: `sort`가 반복자 구간 `[begin, end)`를 받고 끝이 포함되지 않는 이유.
- [ ] 설명할 수 있다: 비교 기반 정렬이 왜 O(N log N)보다 빨라질 수 없는지.
- [ ] 설명할 수 있다: 정렬 뒤 `v[0]`, `v[n-1]`, `v[k-1]`, `v[n/2]`가 각각 무엇이 되는지.
- [ ] 설명할 수 있다: `unique` 앞에 왜 반드시 정렬이 필요하고, 왜 `erase`까지 해야 크기가 주는지.
- [ ] 설명할 수 있다: 비교 함수가 "a가 b보다 앞이냐"는 한 질문에만 답한다는 것.
- [ ] 설명할 수 있다: 부등호 방향이 곧 정렬 방향이라는 것과, 그래서 문자열 내림차순도 자유롭다는 것.
- [ ] 설명할 수 있다: 다중 기준에서 "1순위가 다르면 즉시 return"이 왜 동점 처리로 이어지는지.
- [ ] 설명할 수 있다: 비교 함수에 `<=`를 쓰면 왜 답이 틀리는 정도가 아니라 프로그램이 죽는지.
- [ ] 설명할 수 있다: `std::sort`가 안정 정렬이 아니라는 것과, 입력 순서를 지키는 두 가지 방법.
- [ ] 설명할 수 있다: `pair`의 기본 비교가 사전식이라 두 기준 오름차순이 공짜라는 것.
- [ ] 설명할 수 있다: 비교 함수 인자를 `const T&`로 받아야 하는 이유(복사 비용·수정 방지).
- [ ] 설명할 수 있다: 파이썬 `key`는 원소당 한 번, C++ 비교 함수는 비교할 때마다 실행된다는 차이.
- [ ] 설명할 수 있다: `map`이 키를 정렬해 보관한다는 성질을 동점 처리에 활용하는 방법.

**⚠️ 자주 하는 실수**

**1) 비교 함수에 `<=`를 써서 순서를 모순되게 만든다**

```cpp
// ❌ 틀린 코드
sort(v.begin(), v.end(), [](const P& a, const P& b) {
    return a.second <= b.second;    // 같아도 true 를 돌려준다
});
```

왜: `std::sort`는 비교 함수가 **엄격한 약한 순서**(같으면 반드시 `false`)를 지킨다고 믿고 경계 검사를 생략한다. `<=`면 `cmp(a,b)`와 `cmp(b,a)`가 동시에 참이 되어 순서가 모순되고, 정렬기가 구간 밖으로 뛰쳐나가 런타임에 죽거나 메모리를 조용히 망가뜨린다. 답이 조금 틀리는 수준이 아니다.

```cpp
// ✅ 고친 코드
sort(v.begin(), v.end(), [](const P& a, const P& b) {
    return a.second < b.second;     // 비교 함수에는 < 와 > 만 쓴다
});
```

**2) 동점 순서를 `std::sort`가 지켜 줄 것으로 믿는다**

```cpp
// ❌ 틀린 코드
// 규칙: 점수 내림차순, 같으면 입력 순서
sort(v.begin(), v.end(), [](const Rec& a, const Rec& b) {
    return a.key > b.key;           // 동점의 순서는 보장되지 않는다
});
```

왜: 파이썬 `sorted`는 안정 정렬이라 "동점이면 입력 순서"가 공짜였지만, `std::sort`는 안정 정렬이 아니다. 같은 코드가 환경에 따라 다른 순서를 낼 수 있어, 로컬에서는 맞고 채점에서는 틀리는 일이 생긴다.

```cpp
// ✅ 고친 코드
sort(v.begin(), v.end(), [](const Rec& a, const Rec& b) {
    if (a.key != b.key) return a.key > b.key;
    return a.idx < b.idx;           // 입력 순서를 최하위 기준으로 명시
});
// 또는 stable_sort(v.begin(), v.end(), cmp);
```

**3) `unique` 앞에 정렬을 빠뜨리거나 `erase`를 잊는다**

```cpp
// ❌ 틀린 코드
vector<int> a = {5, 3, 3, 1, 5, 2};
unique(a.begin(), a.end());     // 정렬도 안 했고 반환값도 안 썼다
// a 의 크기는 그대로고, 떨어져 있는 5 는 중복이 살아남는다
```

왜: `unique`는 **바로 앞 원소와만** 비교하므로 정렬돼 있어야 같은 값이 이웃한다. 게다가 원소를 실제로 지우지 않고 "남길 구간의 끝" 반복자만 돌려주므로, 그것으로 꼬리를 잘라야 크기가 줄어든다.

```cpp
// ✅ 고친 코드
vector<int> a = {5, 3, 3, 1, 5, 2};
sort(a.begin(), a.end());
a.erase(unique(a.begin(), a.end()), a.end());   // 1 2 3 5
```

**4) 비교 함수 인자를 값으로 받는다**

```cpp
// ❌ 틀린 코드
sort(v.begin(), v.end(), [](pair<string,int> a, pair<string,int> b) {
    return a.second < b.second;     // 비교할 때마다 문자열이 두 개씩 복사된다
});
```

왜: 정렬 한 번에 비교가 약 N log N 번 일어난다. 그때마다 `pair<string,int>`가 통째로 복사되면 정렬 본체보다 복사가 더 비싸진다. 파이썬 `key`는 원소당 한 번만 계산됐지만 C++ 비교 함수는 매 비교마다 실행된다는 차이가 여기서 드러난다.

```cpp
// ✅ 고친 코드
sort(v.begin(), v.end(), [](const pair<string,int>& a, const pair<string,int>& b) {
    return a.second < b.second;     // 복사 0, 실수로 수정도 불가
});
```

**5) k번째 값의 인덱스를 하나 어긋나게 잡는다**

```cpp
// ❌ 틀린 코드
sort(a.begin(), a.end());
cout << a[k] << "\n";           // k번째로 작은 값을 원했는데 (k+1)번째가 나온다
```

왜: `k`는 1부터 세지만 인덱스는 0부터 센다. `k = 1`일 때 최솟값은 `a[0]`이다. 게다가 `k == n`이면 `a[n]`은 범위 밖인데, C++은 파이썬처럼 오류를 내지 않고 남의 메모리를 조용히 읽는다.

```cpp
// ✅ 고친 코드
sort(a.begin(), a.end());
cout << a[k - 1] << "\n";       // k=1 -> a[0](최소), k=N -> a[N-1](최대)
```

**6) 숫자를 문자열인 채로 정렬한다**

```cpp
// ❌ 틀린 코드
vector<pair<string,string>> v;
v.push_back({name, scoreStr});          // 점수가 문자열 그대로다
sort(v.begin(), v.end(), [](const auto& a, const auto& b) {
    return a.second < b.second;         // "100" < "9" 로 비교된다
});
```

왜: `std::string`의 `<`는 사전식이라 첫 글자가 먼저다. `"100"`은 `"9"`보다 앞이 되어 숫자 크기와 결과가 어긋난다.

```cpp
// ✅ 고친 코드
vector<pair<string,int>> v;
v.push_back({name, stoi(scoreStr)});    // 비교 전에 정수로 변환
sort(v.begin(), v.end(), [](const auto& a, const auto& b) {
    return a.second < b.second;
});
```

**7) 원본을 지켜야 하는데 그냥 정렬해 버린다**

```cpp
// ❌ 틀린 코드
int median(vector<int>& a) {
    sort(a.begin(), a.end());   // 호출자가 넘긴 바로 그 벡터가 정렬된다
    return a[a.size() / 2];
}
// 호출 후 a 의 입력 순서가 사라진다
```

왜: `&`로 받으면 `a`는 호출자의 벡터 그 자체다. `std::sort`는 제자리 정렬이라 원본을 덮어쓴다. 파이썬에서 `sorted(a)`가 새 리스트를 만들어 주던 것과 달리, C++에는 "정렬된 새 것을 돌려주는" 표준 함수가 없다.

```cpp
// ✅ 고친 코드
int median(const vector<int>& a) {
    vector<int> s = a;          // 사본을 떠서 그것만 정렬한다 (O(n) 복사)
    sort(s.begin(), s.end());
    return s[s.size() / 2];
}
```

**8) `map`의 `operator[]`로 존재만 확인하려다 원소를 만든다**

```cpp
// ❌ 틀린 코드
map<string,int> cnt;
for (const string& w : words) cnt[w]++;
for (const string& q : queries)
    if (cnt[q] > 0) ans++;      // 없는 q 도 이 순간 0 으로 삽입된다
// 이후 cnt 를 순회하면 넣은 적 없는 키가 튀어나온다
```

왜: `std::map::operator[]`는 키가 없으면 기본값 원소를 **삽입한 뒤** 참조를 돌려준다. 세는 데는 편하지만, 읽기만 하려는 자리에서는 크기를 부풀리는 함정이 된다.

```cpp
// ✅ 고친 코드
for (const string& q : queries)
    if (cnt.count(q) && cnt.at(q) > 0) ans++;   // 삽입 없이 확인만
```

**다음 챕터로**

- 정렬은 그 자체가 답인 경우보다 "정렬해 두면 다음 단계가 쉬워지는" 전처리인 경우가 훨씬 많다. 앞으로 만날 이분 탐색, 구간 문제, 탐욕적 선택은 모두 "정렬된 상태"를 전제로 출발한다. 당장 Ch4의 이벤트 스위핑이 `pair` 정렬 위에 서 있다.
- 정렬 뒤 이웃끼리만 비교하면 O(N)에 끝나는 패턴은, 나중에 두 포인터·투 포인터류 기법으로 그대로 확장된다.
