## L3. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터의 내용은 문장 하나로 압축된다 — **키를 계산해서 자리를 만들면, 찾는 일이 세는 일이 아니라 뛰어가는 일이 된다.** `vector`를 처음부터 훑던 O(n)이 `unordered_set`/`unordered_map`에서 평균 O(1)로 바뀌는 이유가 전부 여기 있다.

C++에는 이 갈림길이 하나 더 있다. **순서를 버리고 속도를 얻는 해시 컨테이너**(`unordered_set`/`unordered_map`)와 **순서를 지키는 대신 항상 O(log n)인 트리 컨테이너**(`set`/`map`)가 둘 다 표준에 들어 있다. 파이썬에는 후자가 없어 고민할 일이 없었지만, C++에서는 "정렬된 순회나 범위 질의가 필요한가"를 먼저 묻고 컨테이너를 고른다. 아래 지도와 종합 선택표가 그 판단을 대신해 준다.

**개념 지도**

```text
  Ch07 map : key -> number -> slot

  hash(key) % m  ->  bucket index    # 계산 한 번으로 자리가 정해진다
   |
   +-- collision : two keys, one slot
   |     chaining        : hang a list on that slot
   |     open addressing : probe the next free slot
   |
   +-- load factor  a = n / m
   |     a stays small  -> average O(1)
   |     a grows        -> rehash (bigger m, insert everything again)
   |     all in one slot -> worst O(n)
   |
   +-- C++ hash containers        (no order at all)
   |     unordered_set  : membership only    s.count(x)
   |     unordered_map  : key -> value       m[k],  m.find(k)
   |     counting       : m[x]++             # [] auto-creates the key
   |     grouping       : m[k].push_back(v)  # [] makes an empty vector
   |
   +-- C++ ordered containers     (balanced binary search tree)
   |     set / map      : always O(log n),  iteration is sorted
   |     lower_bound / upper_bound : "first key >= x"
   |
   +-- key must be hashable and comparable
         ok  : int, long long, string, pair via std::map
         no  : pair / vector in unordered_map without a custom hash
```

같은 질문을 자료구조만 바꿔 물으면 비용이 이렇게 달라진다.

```text
  same question, different cost

  "is x in here ?"     vector        : scan every item        O(n)
                       unordered_set : one hash jump          O(1) average
                       set           : walk down the tree     O(log n)

  "how many x ?"       vector        : count() each time      O(n) each
                       unordered_map : cnt[x]                 O(1) average

  "what maps to x ?"   two vectors + find()                   O(n)
                       unordered_map : m[x]                   O(1) average

  "sorted order ?"     unordered_*   : no order at all        # 순서를 버린다
                       set / map     : iteration is sorted    O(log n) per op

  "first key >= x ?"   unordered_*   : impossible             # 근접 질의 불가
                       set / map     : lower_bound(x)         O(log n)
```

C++에서만 밟는 함정 하나는 그림으로 못 박아 둘 값어치가 있다.

```text
  operator[] on a map : reading can WRITE
  ---------------------------------------------------------
   m[k]++              # 없으면 0 을 만들고 1 로  -> 빈도 세기엔 편하다
   if (m[k] > 0)       # 없으면 0 을 '만들어' 놓고 비교 -> 표가 커진다
   m.count(k)          # 있는지만 본다 (삽입 없음)
   m.find(k) != m.end()  # 값까지 꺼내려면 이쪽
   # 파이썬 d[k] 는 KeyError, C++ m[k] 는 조용한 삽입 -- 정반대다
```

**뼈대 코드**

1) 존재 판정 — `unordered_set`으로 "확인 → 추가"

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];   // 파싱은 문제마다 바뀜

    unordered_set<int> seen;
    bool found = false;
    for (int x : arr) {
        if (seen.count(x)) {          // 확인이 먼저
            cout << x << "\n";        // 찾았을 때 할 일은 문제마다 바뀜
            found = true;
            break;
        }
        seen.insert(x);               // 추가는 나중
    }
    if (!found) cout << -1 << "\n";
    return 0;
}
```

2) 빈도 세기 — `unordered_map`의 `[]`가 0을 자동 생성한다

```cpp
unordered_map<int,int> cnt;
for (int x : arr) cnt[x]++;           // 없는 키는 0 으로 생겨 1 이 된다

// 없는 키를 '읽기만' 할 때는 count/find 로 (m[k] 는 키를 만들어 버린다)
int c = cnt.count(999) ? cnt[999] : 0;

// 최빈값: 빈도 내림차순, 동점이면 키 오름차순
int bestKey = 0, bestCnt = -1;
for (auto& [k, v] : cnt) {            // 순회 순서는 보장되지 않는다
    if (v > bestCnt || (v == bestCnt && k < bestKey)) { bestCnt = v; bestKey = k; }
}
cout << bestKey << "\n";              // 정렬 기준은 문제마다 바뀜
```

3) 그룹화 — `unordered_map<string, vector<string>>`과 정규화 키

```cpp
unordered_map<string, vector<string>> groups;
for (const string& s : words) {
    string key = s;
    sort(key.begin(), key.end());     // 정규화 키는 문제마다 바뀜
    groups[key].push_back(s);         // [] 가 빈 vector 를 자동 생성한다
}

cout << groups.size() << "\n";        // 그룹 개수

vector<string> keys;                  // 출력 순서가 필요하면 반드시 정렬
for (auto& [k, v] : groups) keys.push_back(k);
sort(keys.begin(), keys.end());
for (const string& k : keys) {
    vector<string> g = groups[k];
    sort(g.begin(), g.end());
    cout << k;
    for (const string& w : g) cout << ' ' << w;
    cout << "\n";
}
```

4) 매핑·명령 처리와 집합 연산

```cpp
unordered_map<string,string> book;
book["apple"] = "red";                            // 삽입과 수정이 같은 문법
if (book.count("apple")) book.erase("apple");     // 없는 키를 지워도 에러는 없다(0 반환)
auto it = book.find("apple");
cout << (it != book.end() ? it->second : "none") << "\n";   // 없을 때 기본값

set<int> a(listA.begin(), listA.end());           // 정렬된 집합
set<int> b(listB.begin(), listB.end());
vector<int> inter, diff, uni;
set_intersection(a.begin(), a.end(), b.begin(), b.end(), back_inserter(inter));
set_difference  (a.begin(), a.end(), b.begin(), b.end(), back_inserter(diff));
set_union       (a.begin(), a.end(), b.begin(), b.end(), back_inserter(uni));
// set_* 알고리즘은 '정렬된' 범위를 요구한다 -> unordered_set 에는 쓸 수 없다
```

5) 여러 값이 한 키일 때와 누적합 + `map` 조합

```cpp
set<pair<int,int>> visited;                       // 좌표처럼 값 여러 개가 한 키일 때
int x = 0, y = 0;
visited.insert({x, y});
// unordered_set<pair<int,int>> 는 기본 해시가 없어 컴파일되지 않는다.
// 해시가 꼭 필요하면 키를 하나의 수로 접는다:
unordered_set<long long> vis2;
vis2.insert((long long)x * 1000000 + y);          // 좌표 범위에 맞춰 곱수를 정한다

unordered_map<long long, int> freq;               // 합이 K인 연속 구간의 개수
freq[0] = 1;                                      // 누적합 0을 한 번 본 것으로 시작
long long total = 0;
long long ans = 0;
for (int v : arr) {
    total += v;
    if (freq.count(total - K)) ans += freq[total - K];   // 찾을 값은 문제마다 바뀜
    freq[total]++;
}
cout << ans << "\n";
```

**언제 무엇을 쓰나**

- 이 챕터의 핵심 표다. 왼쪽 열의 **질문 모양**을 보고 컨테이너를 고른다.

| 무엇을 묻는 문제인가 | 무엇을 쓰나 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 순서가 의미를 갖고 인덱스로 접근한다 | `vector` | 위치 정보를 가진 유일한 자료구조 | 인덱스 O(1) · 탐색 O(n) |
| "이 값이 있었나?"만 반복해서 묻는다 | `unordered_set` | 값에서 자리를 계산해 한 칸만 본다 | 평균 O(1) · 최악 O(n) |
| 존재 확인이 필요한데 **정렬 순회도** 해야 한다 | `set` | 순회가 곧 오름차순이다 | O(log n) |
| 중복을 없애고 종류의 개수만 센다 | `unordered_set` + `size()` | 같은 값은 한 번만 저장된다 | O(n) |
| 중복을 없애고 **정렬된 결과**로 출력한다 | `set` | 넣는 즉시 정렬 상태가 유지된다 | O(n log n) |
| 두 모음의 교집합·차집합을 구한다 | `set` + `set_intersection` 등 | 알고리즘이 정렬된 범위를 요구한다 | O(n + m) |
| "이 키에 딸린 값"이 필요하다 | `unordered_map` | 키→값 한 방향 매핑이 정확히 그 일 | 평균 O(1) |
| 키→값이 필요하고 **키 순서대로 출력**해야 한다 | `map` | 순회가 키 오름차순이라 정렬이 불필요 | O(log n) |
| 각 값이 몇 번 나왔는지 센다 | `unordered_map<T,int>` + `cnt[x]++` | `[]`가 0을 자동 생성해 초기화가 사라진다 | O(n) |
| 최빈값·상위 k개 빈도를 뽑는다 | `unordered_map` + `vector`로 옮겨 `sort` | 빈도표를 만든 뒤 기준만 정하면 끝 | O(n log n) |
| 같은 기준의 원소들을 묶는다 | `unordered_map<K, vector<V>>` | `[]`가 빈 벡터를 자동 생성한다 | O(n) |
| 키가 좌표처럼 값 여러 개의 조합이다 | `map<pair<int,int>, V>` 또는 접은 정수 키 | `unordered_map`은 `pair` 기본 해시가 없다 | O(log n) / 평균 O(1) |
| "x 이상인 첫 값"·범위 질의(x 이상 y 이하) | `set`/`map`의 `lower_bound` | 해시는 순서 정보를 아예 버린다 | O(log n) |
| 값이 고정이고 순위·범위만 묻는다 | `sort` + `lower_bound`(vector) | 갱신이 없으면 정렬 배열이 가장 빠르다 | O(log n) |
| 최악 시간까지 보장돼야 한다 | `set`/`map` | 해시는 최악 O(n), 트리는 항상 O(log n) | O(log n) |
| 키가 0..N 범위의 작은 정수다 | `vector<int>` 카운팅 배열 | 해시 계산조차 필요 없이 곧바로 인덱스 | O(1) |

- 다섯 컨테이너를 연산별로 나란히 놓으면 표가 하나로 정리된다.

| 연산 | `vector` | `set` | `unordered_set` | `map` | `unordered_map` |
| --- | --- | --- | --- | --- | --- |
| 삽입 | 뒤에 O(1) | O(log n) | 평균 O(1) | O(log n) | 평균 O(1) |
| 존재 확인 | **O(n)** | O(log n) | 평균 O(1) | O(log n) | 평균 O(1) |
| 값 조회 | 인덱스 O(1) | — | — | O(log n) | 평균 O(1) |
| 삭제 | 중간 O(n) | O(log n) | 평균 O(1) | O(log n) | 평균 O(1) |
| 최악 보장 | O(n) | **O(log n)** | **O(n)** | **O(log n)** | **O(n)** |
| 순회 순서 | 삽입 순서 | **오름차순** | 미정 | **키 오름차순** | 미정 |
| 범위·근접 질의 | 정렬 후 가능 | `lower_bound` | **불가** | `lower_bound` | **불가** |
| 상수(같은 O끼리) | 가장 작다 | 중간 | 작다 | 중간 | 작다 |

- 파이썬에서 옮겨 올 때 어긋나는 칸만 따로 모으면 이렇다.

| 파이썬 | C++ | 어긋나는 지점 |
| --- | --- | --- |
| `d[k]` 없는 키 → `KeyError` | `m[k]` 없는 키 → **조용히 생성** | 확인만 할 땐 `count`/`find` |
| `set`/`dict`만 있다 | 해시형과 정렬형이 따로 있다 | 순서가 필요하면 `set`/`map` |
| 리스트는 키가 될 수 없다 | `vector`/`pair`는 기본 해시가 없다 | `map`을 쓰거나 키를 정수로 접는다 |
| `Counter(arr)` 한 줄 | `for (x : arr) cnt[x]++;` | 표준 Counter가 없다 |
| `d.get(k, 0)` | `m.count(k) ? m[k] : 0` | 기본값 조회 문법이 없다 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 해시 함수가 키를 어떻게 버킷 번호로 바꾸는지, 그 계산이 왜 한 번이면 되는지.
- [ ] 설명할 수 있다: 충돌이 무엇이고, 체이닝과 개방 주소법이 각각 어떻게 처리하는지.
- [ ] 설명할 수 있다: 적재율 α가 무엇이고, 커지면 왜 느려지는지, `max_load_factor`가 무엇을 막는지.
- [ ] 설명할 수 있다: 해시가 왜 평균 O(1)이고 최악 O(n)인지, 그 둘을 가르는 조건이 무엇인지.
- [ ] 설명할 수 있다: `vector` 선형 탐색이 O(n)인데 `unordered_set` 조회가 평균 O(1)인 차이가 어디서 오는지.
- [ ] 설명할 수 있다: `unordered_map`과 `map`의 내부 구조가 어떻게 다르고, 그래서 무엇이 달라지는지.
- [ ] 설명할 수 있다: 최악 시간을 보장해야 할 때 왜 `map`이 더 안전한 선택인지.
- [ ] 설명할 수 있다: `m[k]`가 없는 키를 자동 생성하는 이유(`T&` 반환)와 그것이 언제 버그가 되는지.
- [ ] 설명할 수 있다: `count`·`find`·`[]` 셋의 차이와 각각을 언제 쓰는지.
- [ ] 설명할 수 있다: 왜 키가 불변이어야 하는지, C++이 그것을 `const Key`로 어떻게 강제하는지.
- [ ] 설명할 수 있다: `unordered_map`의 순회 순서가 보장되지 않는 이유와, 출력 시 무엇을 해야 하는지.
- [ ] 설명할 수 있다: `pair`를 `unordered_map`의 키로 바로 쓸 수 없는 이유와 우회 방법 두 가지.
- [ ] 설명할 수 있다: 애너그램 묶기처럼 "정규화 키"를 만드는 발상이 왜 해시 문제의 핵심인지.
- [ ] 설명할 수 있다: 정렬·이진탐색이 필요한 문제와 해시로 충분한 문제를 어떻게 구분하는지.
- [ ] 설명할 수 있다: `vector` / `set` / `unordered_set` / `map` / `unordered_map` 중 무엇을 고를지, 문제 문장에서 어떤 단어를 보고 판단하는지.

**⚠️ 자주 하는 실수**

**1) 존재 확인을 `m[k]`로 해서 키를 만들어 버린다**

```cpp
// ❌ 틀린 코드
unordered_map<int,int> m;
for (int q : queries) {
    if (m[q] > 0) cout << "YES\n";      // 없는 키가 0으로 '생성'된다
    else          cout << "NO\n";
}
// 질의 10만 개면 표에 없던 키 10만 개가 새로 쌓인다
```

왜: `operator[]`의 반환형이 `T&`, 즉 참조다. `m[k] = 5`처럼 대입할 수 있어야 하므로 없는 키라도 돌려줄 실체가 필요하고, 그래서 값 초기화된 원소(정수면 0)를 **만들어** 그 참조를 준다. 파이썬 `d[k]`가 `KeyError`로 즉시 알려 주는 자리에서 C++은 아무 말 없이 표를 키운다. 메모리가 늘 뿐 아니라 이후 `m.size()`나 순회 결과까지 틀어진다.

```cpp
// ✅ 고친 코드
if (m.count(q)) cout << "YES\n"; else cout << "NO\n";     // 삽입 없이 확인만

auto it = m.find(q);                                       // 값까지 필요하면 find
if (it != m.end()) cout << it->second << "\n";
```

**2) `pair`나 `vector`를 `unordered_map`의 키로 쓴다**

```cpp
// ❌ 틀린 코드
unordered_set<pair<int,int>> visited;      // 컴파일 에러
visited.insert({1, 2});                    // std::hash<pair<...>> 가 없다
```

왜: 표준은 기본 타입과 `string`에만 `std::hash` 특수화를 제공한다. `pair`나 `vector`에는 기본 해시가 없어 컴파일 자체가 안 된다. 파이썬은 튜플이 자동으로 해시 가능하므로 그 감각으로 옮기면 여기서 막힌다.

```cpp
// ✅ 고친 코드
set<pair<int,int>> visited;                // 정렬 컨테이너는 비교만 하면 되니 OK
visited.insert({1, 2});                    // O(log n)

unordered_set<long long> vis;              // 또는 두 수를 하나로 접는다
vis.insert((long long)x * 1000000 + y);    // 곱수는 좌표 범위보다 크게 잡는다
```

**3) `unordered_map`의 순회 순서를 답으로 쓴다**

```cpp
// ❌ 틀린 코드
unordered_map<string,int> cnt;
for (const string& s : words) cnt[s]++;
for (auto& [k, v] : cnt) cout << k << ' ' << v << "\n";   // 순서가 보장되지 않는다
```

왜: 순회는 **버킷 배열을 훑는 순서**라 해시값·버킷 수·삽입 이력에 따라 달라진다. 삽입 순서도 정렬 순서도 아니고, 리해싱이 한 번 일어나면 통째로 뒤바뀐다. 로컬에서 우연히 맞아 보여도 컴파일러나 입력이 조금만 달라지면 순서가 바뀐다.

```cpp
// ✅ 고친 코드
map<string,int> cnt;                        // 키 오름차순이 필요하면 정렬 컨테이너
for (const string& s : words) cnt[s]++;
for (auto& [k, v] : cnt) cout << k << ' ' << v << "\n";   // 항상 사전순

// 또는 결과를 벡터로 옮겨 정렬한다
// vector<pair<string,int>> v(cnt.begin(), cnt.end());
// sort(v.begin(), v.end());
```

**4) `vector`에 선형 탐색을 반복해 O(n²)을 만든다**

```cpp
// ❌ 틀린 코드
vector<int> seen;
for (int x : arr) {
    if (find(seen.begin(), seen.end(), x) != seen.end()) {   // 한 번이 O(n)
        cout << x << "\n";
        break;
    }
    seen.push_back(x);
}
```

왜: `find` 한 번이 O(n)인데 루프가 n번 돈다. 전체가 O(n²)이라 n이 10만이면 100억 번 비교로 시간 초과가 난다. 자료구조만 바꾸면 전체가 O(n)이 된다.

```cpp
// ✅ 고친 코드
unordered_set<int> seen;                    // push_back -> insert, 나머지는 그대로
for (int x : arr) {
    if (seen.count(x)) { cout << x << "\n"; break; }
    seen.insert(x);
}
```

**5) "추가 → 확인" 순서로 뒤집어 쓴다**

```cpp
// ❌ 틀린 코드
unordered_set<int> seen;
for (int x : arr) {
    seen.insert(x);                         // 먼저 넣어 버렸다
    if (seen.count(T - x)) { cout << "YES\n"; break; }   // T=8, x=4면 혼자 YES
}
```

왜: 자기 자신을 짝으로 세게 된다. 배열에 4가 하나뿐인데 `T - 4 = 4`가 방금 넣은 자기 값과 맞아떨어져 잘못된 YES가 나온다. 예제 입력에서는 대개 통과하고 특정 입력에서만 틀려 원인을 찾기 어렵다.

```cpp
// ✅ 고친 코드
unordered_set<int> seen;
for (int x : arr) {
    if (seen.count(T - x)) { cout << "YES\n"; break; }   // 확인이 먼저
    seen.insert(x);                                      // 추가는 나중
}
```

**6) 순회 중에 원소를 지우고 반복자를 계속 쓴다**

```cpp
// ❌ 틀린 코드
for (auto it = m.begin(); it != m.end(); ++it) {
    if (it->second == 0) m.erase(it);      // 지운 반복자를 ++ 한다 -> 미정의 동작
}
```

왜: `erase`가 그 원소의 반복자를 무효화하는데, 무효가 된 반복자를 `++`하면 어디로 갈지 알 수 없다. 파이썬은 "순회 중 크기 변경"을 `RuntimeError`로 즉시 잡아 주지만 C++은 **아무 신호 없이** 원소를 건너뛰거나 프로그램을 죽인다.

```cpp
// ✅ 고친 코드
for (auto it = m.begin(); it != m.end(); ) {
    if (it->second == 0) it = m.erase(it);   // erase 가 '다음' 반복자를 돌려준다
    else                 ++it;
}
// C++20 이상이면 한 줄로: erase_if(m, [](auto& kv){ return kv.second == 0; });
```

**7) 키가 작은 정수인데 굳이 해시를 쓴다**

```cpp
// ❌ 틀린 코드
unordered_map<int,int> cnt;                 // 키가 0..100 뿐인데
for (int x : arr) cnt[x]++;                 // 해시 계산 + 버킷 탐색 + 리해싱
```

왜: 틀린 답이 나오지는 않지만 **불필요하게 느리다.** 키가 이미 작은 정수라면 그것이 곧 배열 인덱스이므로, 해시를 계산할 이유가 없다. `unordered_map`은 노드를 하나씩 힙에 할당하느라 캐시도 나쁘다. 큰 입력에서 배열 대비 수 배 차이가 난다.

```cpp
// ✅ 고친 코드
vector<int> cnt(101, 0);                    // 키 범위만큼 잡는다
for (int x : arr) cnt[x]++;                 // 해시 없이 곧바로 인덱스 O(1)
// 값 범위가 음수를 포함하면 offset 을 더해 인덱스로 옮긴다
```

**8) `int`로 키를 접다가 오버플로를 낸다**

```cpp
// ❌ 틀린 코드
unordered_set<int> vis;
vis.insert(x * 1000000 + y);                // x 가 10만이면 10^11 -> int 를 넘는다
```

왜: C++ `int`는 약 21억까지다. 넘으면 예외 없이 **조용히 음수로 감겨** 서로 다른 좌표가 같은 키가 되어 버린다. 방문 표시가 엉키면서 답만 틀리고 에러는 나지 않는다. 파이썬 정수는 자리수 제한이 없어 이 사고가 없으므로 옮겨 온 코드에서 특히 위험하다.

```cpp
// ✅ 고친 코드
unordered_set<long long> vis;
vis.insert((long long)x * 1000000 + y);     // 캐스팅은 곱하기 '전에' 해야 한다
// (long long)(x * 1000000 + y) 는 이미 int 로 넘친 뒤라 소용이 없다
```

**다음 챕터로**

- 해시는 "값 → 자리"를 계산하는 도구라 순서 정보를 버린다. 그래서 정렬된 순서·범위 질의가 필요한 순간 `set`/`map`과 `lower_bound`가 다시 등장한다. 두 도구는 경쟁 관계가 아니라 묻는 질문이 다르다.
- 좌표를 하나의 정수 키로 접어 `unordered_set`에 담는 패턴은 그래프·탐색 챕터에서 격자 방문 배열과 같은 역할을 한다. 좌표 범위가 아주 넓거나 음수까지 나오는 문제에서는 배열 대신 이 방식이 답이 된다. 그때 접는 계산을 `long long`으로 하는 것이 정확성의 조건이다.
