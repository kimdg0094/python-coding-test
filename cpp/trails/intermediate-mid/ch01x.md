## L7. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch1(중급 자료구조)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. 새 문법은 없다. `unordered_map`·`unordered_set`·`map`/`set`(정렬 유지)·`multiset`·`priority_queue`·prev/next 포인터 배열(이중 연결 리스트)만으로 12문제를 푼다.

- **반복 훈련 개념**
- HashMap 명령 처리·그룹핑: 없는 키를 **읽기만** 할 때는 `find`로 확인하고(`operator[]`는 없는 키를 0으로 **만들어 넣는다**), 누적할 때는 그 성질을 역이용해 `m[k] += v`. 그룹은 `map<string, vector<T>>`에 `push_back`
- TreeMap/TreeSet 직행: 파이썬은 없어서 `sorted + bisect`로 흉내 냈지만 C++에는 `map`/`set`이 있다. "x 이하 마지막"은 `it = m.upper_bound(x); --it`, "x 이상 첫"은 `m.lower_bound(x)`. 삽입·삭제·탐색 모두 O(log n)
- HashSet 존재 판정·증감: `s.insert(x)`, `s.erase(x)`(없어도 조용히 0을 반환), `s.size()`
- 힙 세 패턴: 크기 K 힙(`pop` 후 `push`), 최대·최소 동시 접근(`multiset`의 `*begin()` / `*rbegin()`), 지연 삭제(`priority_queue`에서 중간 원소를 못 지울 때)
- 이중 연결 리스트: 센티넬 HEAD/TAIL 사이에 `nxt`/`prv`로 잇고, 삭제는 `nxt[prv[x]] = nxt[x]; prv[nxt[x]] = prv[x]`, 복원은 그 반대 `nxt[prv[x]] = x; prv[nxt[x]] = x`

- **코딩테스트 출제 맵**: 이 챕터의 유형은 프로그래머스 「코딩테스트 고득점 Kit」의 '힙'(스코빌 합치기·작업 스케줄러·양끝 삭제 큐 류), 백준 「단계별로 풀어보기」의 '우선순위 큐'·'집합과 맵' 단계, NeetCode 150의 'Heap / Priority Queue'·'Linked List'에 그대로 등장한다. 이 레슨의 유형 확장 문제는 그 대표 유형의 소재·수치·조건을 새로 만들어 재구성한 것이다.

- **문제 구성표**

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 재고 명령 처리 | Easy | unordered_map 명령 처리 + find/operator[] 구분 | 반복 훈련 |
| 2 | 동시 접속 최대 인원 | Easy | unordered_set insert/erase + 최댓값 갱신 | 반복 훈련 |
| 3 | 시각별 요금 조회 | Medium | map::upper_bound로 floor 키(TreeMap 직행) | 반복 훈련 |
| 4 | 정렬 집합 k번째와 이하 최대 | Medium | set 유지 + k번째 순회·이하 탐색(TreeSet 직행) | 반복 훈련 |
| 5 | 부서별 인원과 최고 득점자 | Medium | map 그룹핑(정렬 순회 공짜) + 동점 규칙 | 반복 훈련 |
| 6 | 카드 합성 최소 횟수 | Medium | 최소 힙 두 개 pop → 하나 push | 유형 확장 (프로그래머스 Kit '힙' 스타일) |
| 7 | 상위 K개 합 스트리밍 | Medium | 크기 K 최소 힙 + 합 유지 | 반복 훈련 |
| 8 | 줄 세우기 명령 | Medium | 센티넬 이중 연결 리스트 앞뒤 삽입·삭제 | 반복 훈련 |
| 9 | 주문 처리 총 소요 시간 | Hard | 정렬 + 힙 스케줄링(가장 짧은 작업 우선) | 유형 확장 (프로그래머스 Kit '힙' 스타일) |
| 10 | 양끝 삭제 우선순위 큐 | Hard | multiset 하나로 최대·최소 동시 삭제 | 유형 확장 (프로그래머스 Kit '힙' 스타일) |
| 11 | 막대 절단 후 가장 긴 조각 | Hard | set 이웃 탐색 + multiset 최댓값 | 유형 확장 (NeetCode 'Heap' 스타일) |
| 12 | 카드 지우기와 되돌리기 | Hard | 이중 연결 리스트 삭제·복원 + 커서 | 유형 확장 (NeetCode 'Linked List' 스타일) |

**문제**

**1) 재고 명령 처리** · Easy

- **요구사항**: 창고 재고를 해시맵으로 관리한다. `in x k`(품목 x를 k개 입고), `out x k`(k개 출고 — 재고가 k 미만이면 출고하지 않고 `fail` 출력), `ask x`(현재 재고 출력, 한 번도 입고된 적 없으면 0) 세 명령을 순서대로 처리한다.
- **입력**: 첫 줄 Q(1 ≤ Q ≤ 200). 이후 Q줄에 명령. 품목명은 소문자 10자 이하, k는 1 이상 1000 이하.
- **출력**: `out` 실패 시 `fail`, `ask`마다 재고를 줄마다.
- **예제**: `6 / in apple 5 / in pear 2 / out apple 3 / ask apple / out pear 5 / ask pear` → `2 / fail / 2` · `2 / ask kiwi / out kiwi 1` → `0 / fail`
- **셀프체크**: C++의 `stock[x]`는 없는 키를 예외 없이 **0으로 만들어 삽입**한다 — 읽기만 할 때는 `find`를 써서 맵을 오염시키지 않았는가? 재고가 정확히 k개일 때 출고는 성공(≥)이어야 한다. `out` 실패 시 재고를 건드리지 않는지 확인.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    unordered_map<string, long long> stock;
    string out;
    for (int i = 0; i < q; i++) {
        string op, name;
        cin >> op >> name;
        if (op == "in") {
            long long k;
            cin >> k;
            stock[name] += k;            // 없던 키는 0에서 시작해 누적된다
        } else if (op == "out") {
            long long k;
            cin >> k;
            auto it = stock.find(name);  // 읽기만 하므로 find (operator[]는 키를 만든다)
            if (it != stock.end() && it->second >= k) it->second -= k;
            else out += "fail\n";
        } else {
            auto it = stock.find(name);
            out += to_string(it == stock.end() ? 0LL : it->second);
            out += '\n';
        }
    }
    cout << out;
    return 0;
}
@@TESTS
--IN
6
in apple 5
in pear 2
out apple 3
ask apple
out pear 5
ask pear
--OUT
2
fail
2
--IN
2
ask kiwi
out kiwi 1
--OUT
0
fail
--IN
4
in box 3
out box 3
ask box
out box 1
--OUT
0
fail
@@EXPL
(1) 접근·핵심 아이디어

- "품목명 → 수량"이라는 키·값 대응이 필요하고, 명령마다 특정 품목만 평균 O(1)에 읽고 고쳐야 하므로 `unordered_map`이 정답이다. `vector`에서 품목을 찾으면 명령마다 O(품목 수)라 Q가 커지면 느려진다.
- 존재하지 않는 키를 읽는 경우(`ask`, `out`)가 정상 입력에 포함된다. C++은 파이썬처럼 예외를 던지지 않고 `operator[]`가 조용히 값 0인 항목을 **만들어 넣으므로**, 읽기 전용 경로는 `find`로 분리하는 것이 이 문제의 습관이다.

(2) 코드 단계별

- 명령·품목명을 먼저 읽고, 수량이 필요한 명령에서만 셋째 토큰을 읽는다(`ask`는 토큰이 둘뿐이므로 무조건 세 개를 읽으면 입력이 어긋난다).
- `in`: `stock[name] += k` — 없던 키가 0으로 생기고 바로 누적된다. 여기서는 키를 만드는 동작이 곧 원하는 동작이다.
- `out`: `find`로 찾아 `it != end() && it->second >= k`일 때만 빼고, 아니면 `fail`을 기록(재고는 그대로).
- `ask`: `find` 결과가 `end()`면 0, 아니면 값을 기록. 출력은 문자열 하나에 모아 마지막에 한 번에 내보낸다.

(3) 스스로 다시 짤 때 생각 순서

- "이름으로 찾아 수량을 고친다" → 해시맵. 명령 종류를 먼저 나열하고 각각이 맵을 **읽기만 하는지 쓰기도 하는지** 표로 정리한다. 읽기만 하는 자리에는 `find`(또는 `count`), 쓰기 자리에는 `operator[]`.
- 값 타입을 `long long`으로 두면 누적 합이 커져도 안전하다(이 문제는 최대 20만이라 `int`로도 되지만, 습관을 들여 두면 오버플로 사고가 줄어든다).
- 경계: 딱 맞게 출고(k == 재고)는 성공, 0개가 되어도 키는 남아 있어도 무방하다.
```

**2) 동시 접속 최대 인원** · Easy

- **요구사항**: 접속 로그가 순서대로 주어진다. `+ id`는 접속, `- id`는 종료다. 이미 접속 중인 id의 `+`와 접속 중이 아닌 id의 `-`는 무시한다. 로그를 모두 처리하면서 "어느 순간의 최대 동시 접속 인원"과 "마지막 시점의 접속 인원"을 출력한다.
- **입력**: 첫 줄 N(1 ≤ N ≤ 500). 이후 N줄에 `+ id` 또는 `- id`(id는 영문 소문자·숫자 20자 이하).
- **출력**: 최대 동시 접속 인원과 최종 접속 인원을 공백으로.
- **예제**: `5 / + a / + b / - a / + c / + b` → `2 2` · `3 / - x / + x / + x` → `1 1`
- **셀프체크**: `vector`로 관리하면 포함 판정이 O(N)이라 O(N^2)이 된다 — `unordered_set`을 썼는가? `insert`는 이미 있으면 아무 일도 하지 않고, `erase(key)`는 없으면 0을 반환할 뿐 예외를 던지지 않는다(문제의 "무시" 규칙과 그대로 맞아떨어진다). 최댓값은 매 로그 처리 직후 갱신해야 한다(마지막에 한 번만 재면 틀림).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    unordered_set<string> online;
    int best = 0;
    for (int i = 0; i < n; i++) {
        string op, uid;
        cin >> op >> uid;
        if (op == "+") online.insert(uid);   // 이미 있으면 아무 일도 없음
        else online.erase(uid);              // 없으면 0을 반환할 뿐
        int cur = (int)online.size();        // size()는 unsigned이므로 int로 받아 비교
        if (cur > best) best = cur;
    }
    cout << best << " " << (int)online.size() << "\n";
    return 0;
}
@@TESTS
--IN
5
+ a
+ b
- a
+ c
+ b
--OUT
2 2
--IN
3
- x
+ x
+ x
--OUT
1 1
--IN
1
- q
--OUT
0 0
@@EXPL
(1) 접근·핵심 아이디어

- "지금 접속 중인 id의 집합"만 있으면 되고, 같은 id의 중복 `+`는 집합이 자동으로 흡수한다. 존재 판정·추가·삭제가 평균 O(1)인 `unordered_set`이 적합해 전체 O(N)이다.
- 최대 동시 접속은 상태가 바뀔 때마다 `online.size()`를 재서 최댓값을 갱신하면 된다.

(2) 코드 단계별

- 각 줄을 `op`, `uid` 두 토큰으로 읽는다.
- `+`면 `insert`(이미 있으면 변화 없음), `-`면 `erase`(없으면 변화 없음) — 문제의 "무시" 규칙이 두 멤버 함수의 성질과 정확히 일치하므로 분기를 더 둘 필요가 없다.
- 처리 직후 크기를 `best`와 비교해 갱신. 마지막에 `best`와 현재 크기를 출력.

(3) 스스로 다시 짤 때 생각 순서

- "누가 접속 중인가"는 순서·횟수가 아닌 존재 여부 → 집합. 정렬된 순회가 전혀 필요 없으므로 `set`이 아니라 `unordered_set`을 고른다.
- 무시 규칙을 `insert`/`erase`의 기본 동작으로 흡수할 수 있는지 확인해 분기를 줄인다.
- 함정: `size()`의 반환형은 `size_t`(부호 없음)다. `if (online.size() - 1 > best)`처럼 뺄셈을 섞으면 0에서 1을 뺀 값이 거대한 양수가 되어 조건이 항상 참이 된다. 비교 전에 `(int)`로 받아 두는 습관이 안전하다.
- 경계: 첫 로그가 `-`이면 0명, 아무도 접속하지 않으면 `0 0`.
```

**3) 시각별 요금 조회** · Medium

- **요구사항**: 요금이 바뀐 기록 N개 `(t, p)`(시각 t에 요금이 p로 바뀜)가 순서 없이 주어진다. 각 질의 시각 x에 대해 "x 이하인 가장 늦은 변경 시각"의 요금을 출력한다. x보다 이른 변경이 하나도 없으면 -1.
- **입력**: 첫 줄 N Q(1 ≤ N, Q ≤ 200). 이후 N줄에 `t p`(0 ≤ t ≤ 10^9, 시각은 서로 다름). 이후 Q줄에 질의 시각 x.
- **출력**: 질의마다 요금을 줄마다.
- **예제**: `3 3 / 10 500 / 0 300 / 20 800 / 15 / 20 / 5` → `500 / 800 / 300` · `2 2 / 5 100 / 9 200 / 4 / 9` → `-1 / 200`
- **셀프체크**: C++의 `map`은 키 오름차순을 항상 유지하므로 정렬을 따로 하지 않는다. "x 이하 마지막"은 `it = m.upper_bound(x)` 뒤 `--it`(x와 같은 시각도 적용되어야 하므로 `lower_bound`가 아니라 `upper_bound`). `it == m.begin()`이면 x 이하가 하나도 없다는 뜻이니 -1. 삽입 O(log N), 질의 O(log N).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    map<long long, long long> price;     // 키(시각) 오름차순이 자동 유지된다
    for (int i = 0; i < n; i++) {
        long long t, p;
        cin >> t >> p;
        price[t] = p;
    }
    string out;
    for (int i = 0; i < q; i++) {
        long long x;
        cin >> x;
        auto it = price.upper_bound(x);  // x 초과 첫 원소 (멤버 함수라 O(log N))
        if (it == price.begin()) {
            out += "-1\n";               // x 이하인 변경이 없다
        } else {
            --it;                        // 한 칸 뒤로 = x 이하 마지막
            out += to_string(it->second);
            out += '\n';
        }
    }
    cout << out;
    return 0;
}
@@TESTS
--IN
3 3
10 500
0 300
20 800
15
20
5
--OUT
500
800
300
--IN
2 2
5 100
9 200
4
9
--OUT
-1
200
--IN
1 2
0 7
0
1000000000
--OUT
7
7
@@EXPL
(1) 접근·핵심 아이디어

- "x 이하인 가장 큰 키의 값"은 TreeMap의 floorEntry다. 파이썬에는 TreeMap이 없어 `(시각, 요금)`을 정렬한 뒤 별도 키 배열에 `bisect`를 걸어야 했지만, **C++의 `std::map`이 곧 TreeMap이다.** 넣는 순간 정렬이 유지되고 `upper_bound`가 O(log N)이므로 중간 단계가 통째로 사라진다.
- `upper_bound(x)`는 "x 초과 첫 원소"를 가리킨다. 여기서 한 칸 뒤로 물러나면 "x 이하 마지막"이다. `lower_bound(x)`를 쓰면 x와 같은 시각의 변경을 건너뛰게 되어 예제의 `20 → 800`이 틀린다.

(2) 코드 단계별

- 기록을 `price[t] = p`로 넣는다. 입력 순서가 뒤섞여 있어도 `map`이 알아서 정렬한다.
- 질의 x마다 `it = price.upper_bound(x)`.
- `it == price.begin()`이면 x 이하 키가 하나도 없으므로 -1. 아니면 `--it` 후 `it->second`가 답.

(3) 스스로 다시 짤 때 생각 순서

- "정렬 순서상 x 바로 아래 키" → `map` + `upper_bound` + `--`. 세 줄짜리 관용구로 외워 둔다.
- 함정 — **멤버 함수를 써야 한다.** `std::lower_bound(price.begin(), price.end(), ...)`처럼 전역 알고리즘을 `map`/`set`에 걸면 반복자가 임의 접근이 아니라서 **O(n)**으로 한 칸씩 걸어간다. 컴파일은 되고 답도 맞지만 로그 시간이 선형 시간이 되어 조용히 시간 초과가 난다. `map`/`set`에서는 항상 `m.lower_bound(x)`, `m.upper_bound(x)` 멤버 함수를 쓴다(`vector`처럼 임의 접근인 컨테이너에서만 전역 `std::lower_bound`가 O(log n)이다).
- 경계: 모든 변경보다 이른 질의는 `begin()`이 나오므로 반드시 검사한다. 마지막 변경 이후의 질의는 마지막 요금이 계속 적용된다. 시각이 10^9까지이므로 키 타입은 `long long`(또는 `int`)로 충분하다.
```

**4) 정렬 집합 k번째와 이하 최대** · Medium

- **요구사항**: 처음엔 빈 정수 집합이다. `1 v`(v 삽입, 이미 있으면 무시), `2 k`(작은 쪽에서 k번째 원소 출력, 원소 수가 k 미만이면 -1), `3 x`(x 이하인 가장 큰 원소 출력, 없으면 -1)를 순서대로 처리한다.
- **입력**: 첫 줄 Q(1 ≤ Q ≤ 300). 이후 Q줄에 연산. v, x는 -10^9 이상 10^9 이하, k는 1 이상 Q 이하.
- **출력**: `2`, `3` 연산마다 결과를 줄마다.
- **예제**: `7 / 1 5 / 1 2 / 1 5 / 2 2 / 3 4 / 3 1 / 2 3` → `5 / 2 / -1 / -1` · `2 / 2 1 / 3 100` → `-1 / -1`
- **셀프체크**: `std::set`이 곧 TreeSet이다 — 중복 삽입은 `insert`가 알아서 무시하고, "x 이하 최대"는 `upper_bound(x)` 뒤 `--`. 다만 k번째 원소는 `set`이 O(log n)으로 주지 못한다(반복자가 양방향이라 `next(s.begin(), k-1)`이 O(k)). Q가 300이라 그대로 두어도 되지만, 왜 O(k)인지 설명할 수 있는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    set<long long> s;                     // TreeSet: 정렬 유지 + O(log n) 삽입/탐색
    string out;
    for (int i = 0; i < q; i++) {
        int op;
        long long v;
        cin >> op >> v;
        if (op == 1) {
            s.insert(v);                  // 이미 있으면 조용히 무시된다
        } else if (op == 2) {
            long long k = v;
            if ((long long)s.size() >= k) {
                auto it = next(s.begin(), (long long)(k - 1));  // 양방향 반복자라 O(k)
                out += to_string(*it);
                out += '\n';
            } else {
                out += "-1\n";
            }
        } else {
            auto it = s.upper_bound(v);   // v 초과 첫 원소
            if (it == s.begin()) {
                out += "-1\n";
            } else {
                --it;                     // v 이하 마지막
                out += to_string(*it);
                out += '\n';
            }
        }
    }
    cout << out;
    return 0;
}
@@TESTS
--IN
7
1 5
1 2
1 5
2 2
3 4
3 1
2 3
--OUT
5
2
-1
-1
--IN
2
2 1
3 100
--OUT
-1
-1
--IN
5
1 -3
1 10
3 -3
2 1
3 -4
--OUT
-3
-3
-1
@@EXPL
(1) 접근·핵심 아이디어

- 삽입과 "k번째", "x 이하 최대" 질의가 섞여 있으므로 항상 정렬된 상태를 유지하는 TreeSet이 필요하다. 파이썬은 이것을 "정렬 리스트 + bisect"로 흉내 내야 했고 그 대가로 **삽입이 O(n)**(원소 이동)이었지만, C++의 `set`은 균형 이진 탐색 트리라 삽입·삭제·탐색이 모두 O(log n)이다. 중복 방지도 `set`의 정의에 포함되어 있어 삽입 전 검사 코드가 통째로 사라진다.
- "x 이하 최대"는 문제 3과 같은 `upper_bound` 후 `--` 관용구다.

(2) 코드 단계별

- `1 v`: `s.insert(v)` 한 줄. 반환값 `pair<iterator,bool>`의 `bool`이 "새로 들어갔는지"를 알려 주지만 여기서는 볼 필요가 없다.
- `2 k`: 크기가 k 이상이면 `next(s.begin(), k-1)`로 k번째를 얻는다. 아니면 -1.
- `3 x`: `it = s.upper_bound(x)`. `begin()`이면 -1, 아니면 `--it` 후 `*it`.

(3) 스스로 다시 짤 때 생각 순서

- "정렬 순서 기반 질의 + 삽입 혼합" → `set`. 파이썬 풀이를 그대로 옮겨 `vector`를 정렬 상태로 유지하려 들지 말 것 — C++에는 그럴 이유가 없다.
- 함정 — **`set`은 "k번째"를 O(log n)에 주지 않는다.** `std::set`의 반복자는 양방향(bidirectional)이라 `it + k`가 불가능하고 `next`/`advance`는 한 칸씩 걷는다. 즉 `next(s.begin(), k-1)`은 O(k)다. 이 문제는 Q ≤ 300이라 무시해도 되지만, 질의가 10^5개면 이것만으로 시간 초과가 난다. 진짜 O(log n) k번째가 필요하면 값 범위에 펜윅 트리를 얹거나(좌표 압축 후 부분합 이분탐색) GNU 확장 `__gnu_pbds::tree`의 order-statistic 트리를 쓴다.
- 함정 2 — 여기서도 `std::upper_bound(s.begin(), s.end(), x)`가 아니라 멤버 `s.upper_bound(x)`다. 전역 버전은 양방향 반복자에서 O(n)으로 퇴화한다.
- 경계: 빈 집합에서의 질의, x가 최솟값보다 작을 때(-1), 음수 값(`set`은 부호를 신경 쓰지 않는다), 같은 값 재삽입(무시되어 k번째가 밀리지 않는다).
```

**5) 부서별 인원과 최고 득점자** · Medium

- **요구사항**: 직원 N명의 `부서 이름 점수`가 주어진다. 부서별로 인원수와 최고 점수를 받은 사람의 이름을 출력한다. 최고 점수가 여러 명이면 이름이 사전순으로 앞선 사람. 부서는 부서명 사전순으로 출력한다.
- **입력**: 첫 줄 N(1 ≤ N ≤ 300). 이후 N줄에 `부서 이름 점수`(부서·이름은 소문자 15자 이하, 이름은 전체에서 유일, 0 ≤ 점수 ≤ 100).
- **출력**: 부서마다 `부서 인원수 이름`을 줄마다.
- **예제**: `5 / dev kim 80 / ops lee 90 / dev park 95 / ops choi 90 / hr yoon 70` → `dev 2 park / hr 1 yoon / ops 2 choi` · `1 / qa a 0` → `qa 1 a`
- **셀프체크**: `map<string, vector<...>>`은 키가 정렬된 채 유지되므로 출력 전에 부서명을 따로 정렬할 필요가 없다(`unordered_map`을 썼다면 반드시 정렬해야 한다). 없는 키에 `groups[dept].push_back(...)`을 하면 빈 `vector`가 자동으로 만들어지는가? 동점 규칙은 "점수 더 큼 또는 (점수 같고 이름 더 작음)"을 한 조건식으로 적는다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    // map은 키(부서명) 사전순을 유지한다 -> 출력 전 정렬이 필요 없다
    map<string, vector<pair<string, int>>> groups;
    for (int i = 0; i < n; i++) {
        string dept, name;
        int score;
        cin >> dept >> name >> score;
        groups[dept].push_back({name, score});   // 없던 키는 빈 vector가 생긴다
    }
    string out;
    for (const auto& g : groups) {
        const string& dept = g.first;
        const vector<pair<string, int>>& mem = g.second;
        pair<string, int> best = mem[0];
        for (size_t i = 1; i < mem.size(); i++) {
            if (mem[i].second > best.second ||
                (mem[i].second == best.second && mem[i].first < best.first)) {
                best = mem[i];
            }
        }
        out += dept + " " + to_string(mem.size()) + " " + best.first + "\n";
    }
    cout << out;
    return 0;
}
@@TESTS
--IN
5
dev kim 80
ops lee 90
dev park 95
ops choi 90
hr yoon 70
--OUT
dev 2 park
hr 1 yoon
ops 2 choi
--IN
1
qa a 0
--OUT
qa 1 a
--IN
3
x bob 50
x amy 50
x cat 50
--OUT
x 3 amy
@@EXPL
(1) 접근·핵심 아이디어

- "부서별로 묶어서 각 묶음의 통계"는 그룹핑 문제다. 부서명을 키로 하는 `map<string, vector<pair<string,int>>>`에 `(이름, 점수)`를 밀어 넣으면 한 번의 순회로 그룹이 완성되고, 그룹마다 최댓값을 한 번 더 훑으면 총 O(N log N)이다.
- **여기서 `map`을 고르는 이유가 성능이 아니라 출력 순서다.** 출력이 부서명 사전순이므로 `map`이면 순회가 곧 정답 순서고, `unordered_map`이면 키를 모아 따로 정렬하는 코드가 더 필요하다. 파이썬은 `defaultdict` + `sorted(groups)` 두 단계였지만 C++은 컨테이너 선택 한 번으로 끝난다.

(2) 코드 단계별

- 각 줄을 부서, 이름, 점수로 읽어 `groups[dept].push_back({name, score})`. C++의 `operator[]`가 없는 키에 기본 생성된 빈 `vector`를 만들어 주므로 파이썬 `defaultdict(list)`와 같은 역할을 한다.
- `map`을 앞에서부터 순회하면 부서명 사전순이다. 첫 구성원을 `best`로 두고 나머지를 비교: 점수가 더 크거나, 같으면서 이름이 사전순으로 앞서면 교체.
- `dept + " " + to_string(mem.size()) + " " + best.first` 형식으로 이어 붙여 출력.

(3) 스스로 다시 짤 때 생각 순서

- "~별로"라는 단어가 보이면 키 → `vector` 그룹핑을 떠올린다. 그다음 **출력 순서를 확인해 `map`과 `unordered_map` 중 하나를 고른다** — 정렬 순회가 필요하면 `map`, 아니면 `unordered_map`.
- 동점 규칙을 비교식에 명시한다(점수 내림, 이름 오름). 셋째 테스트처럼 전원 동점이면 이름이 가장 앞선 사람.
- 함정: 큰 `vector`를 담은 `map`을 순회할 때 `for (auto g : groups)`처럼 값으로 받으면 그룹마다 통째로 복사된다. `const auto&`로 받아 복사를 없앤다.
- 경계: 부서가 하나뿐이거나 N=1인 경우, 점수 0. `mem.size()`는 `size_t`지만 `to_string`이 그대로 받아 준다.
```

**6) 카드 합성 최소 횟수** · Medium

- **요구사항**: 카드 N장의 공격력이 주어진다. 가장 약한 두 장 a ≤ b를 합성하면 공격력 `a + 2*b`인 카드 한 장이 된다. 모든 카드의 공격력이 K 이상이 될 때까지 합성을 반복할 때 최소 합성 횟수를 출력한다. 불가능하면 -1.
- **입력**: 첫 줄 N K(1 ≤ N ≤ 300, 1 ≤ K ≤ 10^9). 둘째 줄 N개의 공격력(1 이상 10^9 이하).
- **출력**: 최소 합성 횟수 또는 -1.
- **예제**: `5 7 / 1 2 3 9 10` → `2` · `1 5 / 3` → `-1`
- **셀프체크**: `priority_queue`는 기본이 **최대 힙**이므로 최소 힙을 만들려면 `priority_queue<long long, vector<long long>, greater<long long>>`처럼 비교자를 바꿔야 한다(파이썬처럼 `-x`로 부호를 뒤집을 필요가 없다). `top()`이 K 이상이 될 때까지 두 번 pop, 한 번 push. 카드가 한 장만 남았는데 K 미만이면 -1 — "pop하기 전에" 장수를 검사했는가? 합성값 `a + 2*b`는 최대 3·10^9이라 `int`로는 넘친다. 검산: {1,2,3,9,10} → 1+2·2=5 → {3,5,9,10} → 3+2·5=13 → {9,10,13} 전부 7 이상, 2회.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long k;
    cin >> n >> k;
    vector<long long> v(n);
    for (int i = 0; i < n; i++) cin >> v[i];

    // greater<> 를 주어야 최소 힙. 범위 생성자는 O(N)으로 힙을 만든다.
    priority_queue<long long, vector<long long>, greater<long long>> pq(v.begin(), v.end());

    long long cnt = 0;
    while (pq.top() < k) {
        if ((int)pq.size() < 2) {        // pop 하기 전에 검사
            cout << -1 << "\n";
            return 0;
        }
        long long a = pq.top(); pq.pop();
        long long b = pq.top(); pq.pop();
        pq.push(a + 2 * b);              // long long 이 아니면 3e9에서 넘친다
        cnt++;
    }
    cout << cnt << "\n";
    return 0;
}
@@TESTS
--IN
5 7
1 2 3 9 10
--OUT
2
--IN
1 5
3
--OUT
-1
--IN
3 1
1 1 1
--OUT
0
--IN
2 100
1 1
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- "가장 약한 두 장"을 매번 꺼내야 하는데, 합성 결과가 다시 후보로 들어오므로 정렬을 매번 다시 할 수 없다. 최소 힙이면 pop 2회 + push 1회가 O(log N)이고 합성은 최대 N-1회라 전체 O(N log N)이다(매번 정렬하면 O(N^2 log N)).
- 종료 조건은 "현재 최솟값이 K 이상"이며, 최솟값은 `pq.top()`으로 O(1)에 볼 수 있다.

(2) 코드 단계별

- 값을 `vector`에 읽어 `priority_queue`의 **범위 생성자**에 넘긴다. 이러면 내부에서 `make_heap`이 불려 O(N)에 힙이 만들어진다(하나씩 `push`하면 O(N log N)).
- `pq.top() < K`인 동안 반복: 카드가 2장 미만이면 더 합성할 수 없으므로 -1을 출력하고 종료.
- 두 장을 pop해 `a + 2*b`를 push하고 횟수를 1 늘린다. 루프가 정상 종료되면 횟수를 출력.

(3) 스스로 다시 짤 때 생각 순서

- "반복해서 최소 두 개를 꺼내 합친다" → 최소 힙 정석 패턴(밧줄 잇기와 같은 골격, 종료 조건만 다름).
- 함정 1 — **`priority_queue`의 기본은 최대 힙이다.** 파이썬 `heapq`는 최소 힙이 기본이라 최대 힙을 쓰려면 값에 `-`를 붙였지만, C++은 그 반대다. 최소 힙이 필요하면 `greater<long long>`을 세 번째 인자로 준다. 부호 뒤집기는 필요 없고, 뒤집으면 오히려 오버플로 위험만 늘어난다.
- 함정 2 — **오버플로.** 공격력이 10^9까지이므로 첫 합성만으로도 `a + 2*b`가 3·10^9이 되어 `int`(약 21억)를 넘는다. 게다가 합성 결과가 다시 합성되며 값이 몇 배로 불어난다(합칠 때마다 개수가 절반씩 줄어드니 깊이는 log2(300) ≈ 9단, 최대 3^9배 정도까지). `long long`으로 두면 안전하고, `int`로 두면 음수가 되어 루프가 영원히 끝나지 않거나 조용히 오답이 난다.
- 함정 3 — `pq.size()`는 `size_t`다. `pq.size() - 1 < 1` 같은 식을 쓰면 빈 큐에서 거대한 양수가 나온다. `(int)`로 캐스팅해 비교한다.
- 경계: 처음부터 조건을 만족하면 0회(루프에 안 들어감), 마지막 한 장이 K 미만이면 -1.
```

**7) 상위 K개 합 스트리밍** · Medium

- **요구사항**: 정수가 하나씩 들어온다. 값이 들어올 때마다 "지금까지 들어온 값 중 가장 큰 K개의 합"을 출력한다. 아직 K개 미만이면 들어온 값 전체의 합.
- **입력**: 첫 줄 N K(1 ≤ K ≤ N ≤ 500). 둘째 줄 N개의 정수(-10^6 이상 10^6 이하).
- **출력**: 각 값이 들어온 직후의 합을 공백으로 N개.
- **예제**: `5 2 / 3 1 4 1 5` → `3 4 7 7 9` · `3 5 / -1 -2 -3` → `-1 -3 -6`
- **셀프체크**: 크기 K인 **최소 힙**에 가장 큰 K개만 남긴다 — `top()`이 K개 중 최솟값이므로 새 값이 `top()`보다 클 때만 교체. C++에는 파이썬 `heapreplace` 같은 "pop+push 한 번에" 함수가 없으니 `pq.pop(); pq.push(x);` 두 줄로 쓴다. 합은 매번 다시 더하지 말고 `합 += 새 값 - 쫓겨난 값`으로 O(1) 갱신. 상위 K는 최소 힙, 하위 K는 최대 힙이라는 방향을 헷갈리지 말 것.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    priority_queue<long long, vector<long long>, greater<long long>> pq;  // 최소 힙
    long long total = 0;
    string out;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        if ((int)pq.size() < k) {
            pq.push(x);
            total += x;
        } else if (x > pq.top()) {
            total += x - pq.top();   // 합은 차이만큼만 갱신
            pq.pop();
            pq.push(x);
        }
        if (i) out += ' ';
        out += to_string(total);
    }
    cout << out << "\n";
    return 0;
}
@@TESTS
--IN
5 2
3 1 4 1 5
--OUT
3 4 7 7 9
--IN
3 5
-1 -2 -3
--OUT
-1 -3 -6
--IN
4 1
2 2 1 3
--OUT
2 2 2 3
@@EXPL
(1) 접근·핵심 아이디어

- "가장 큰 K개"만 유지하면 되므로 크기를 K로 제한한 최소 힙을 쓴다. 힙의 `top()`은 K개 중 가장 작은 값이라, 새 값이 그보다 크면 `top()`을 버리고 새 값을 넣는 것이 "상위 K 갱신"이다. 삽입마다 O(log K), 전체 O(N log K)(매번 정렬하면 O(N^2 log N)).
- 합은 교체될 때 "새 값 - 쫓겨난 값"만큼만 변하므로 누적 변수 하나로 O(1)에 유지한다.

(2) 코드 단계별

- 힙이 K개 미만이면 무조건 `push`하고 합에 더한다.
- K개가 찼으면 `x > pq.top()`일 때만 `total += x - pq.top()` 후 `pop(); push(x);`. **`total`을 먼저 갱신해야 한다** — `pop()`을 먼저 하면 쫓겨난 값을 읽을 수 없다.
- 매 값 처리 직후 `total`을 기록해 공백으로 이어 붙인다. 첫 항목 앞에는 공백을 붙이지 않아 꼬리 공백이 생기지 않게 한다.

(3) 스스로 다시 짤 때 생각 순서

- "상위 K개의 합을 계속" → 크기 K 힙 + 합 누적. 전체 정렬 재계산을 피하는 것이 목적임을 먼저 인식한다.
- 방향 확인: 상위 K를 지키려면 "K개 중 최솟값"을 빨리 봐야 하므로 최소 힙(`greater<>`).
- 함정: `priority_queue`에는 파이썬 `heapreplace`에 해당하는 원자적 연산이 없다. `pop` 다음 `push` 두 번의 힙 연산이 들어가지만 복잡도는 그대로 O(log K)다. `top()`을 참조로 잡아 두고 `pop()`한 뒤 읽으면 이미 파괴된 원소를 읽는 것이므로, 값으로 복사해 두거나 `pop` 전에 다 쓴다.
- 경계: K > 현재 개수일 때(그냥 전체 합), 음수만 들어올 때(교체 조건 `x > pq.top()`은 음수여도 그대로 성립), 같은 값 반복(교체되지 않아 합 불변). 합은 최대 500·10^6 = 5·10^8이라 `int` 경계에 가까우니 `long long`으로 둔다.
```

**8) 줄 세우기 명령** · Medium

- **요구사항**: 빈 줄에서 시작해 사람들을 세운다. `front x`(맨 앞에 x), `back x`(맨 뒤에 x), `before y x`(y 바로 앞에 x), `after y x`(y 바로 뒤에 x), `out x`(x를 줄에서 뺌) 명령을 처리하고 최종 줄을 앞에서부터 출력한다. 아무도 없으면 `empty`.
- **입력**: 첫 줄 M(1 ≤ M ≤ 300). 이후 M줄에 명령. 이름은 영숫자 10자 이하이며, 삽입되는 x는 줄에 없고 기준 y와 `out`의 x는 반드시 줄에 있다.
- **출력**: 최종 줄의 이름들을 공백으로, 비어 있으면 `empty`.
- **예제**: `5 / back 3 / front 1 / after 1 2 / before 3 9 / out 1` → `2 9 3` · `2 / front 7 / out 7` → `empty`
- **셀프체크**: `vector`의 중간 삽입·삭제는 원소 이동 때문에 O(n)이다 — 이름 → 이웃을 `unordered_map`으로 두면 모든 명령이 평균 O(1). HEAD/TAIL 센티넬을 두면 `front`는 "HEAD 뒤 삽입", `back`은 "TAIL 앞 삽입"으로 통일된다. 삽입 시 네 개의 링크를 모두 갱신했는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

unordered_map<string, string> nxt, prv;

// 인자를 값으로 받는다: 참조로 받으면 본문의 nxt[p]=x 가 인자 q 자신을 바꿔 버린다.
void link(string p, string x, string q) {
    nxt[p] = x; prv[x] = p;
    nxt[x] = q; prv[q] = x;
}

void unlink(const string& x) {
    string p = prv[x], q = nxt[x];
    nxt[p] = q; prv[q] = p;
    nxt.erase(x); prv.erase(x);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int m;
    cin >> m;
    const string HEAD = "__H__", TAIL = "__T__";
    nxt[HEAD] = TAIL; prv[TAIL] = HEAD;

    for (int i = 0; i < m; i++) {
        string op;
        cin >> op;
        if (op == "front") {
            string x; cin >> x;
            link(HEAD, x, nxt[HEAD]);
        } else if (op == "back") {
            string x; cin >> x;
            link(prv[TAIL], x, TAIL);
        } else if (op == "before") {
            string y, x; cin >> y >> x;
            link(prv[y], x, y);
        } else if (op == "after") {
            string y, x; cin >> y >> x;
            link(y, x, nxt[y]);
        } else {
            string x; cin >> x;
            unlink(x);
        }
    }

    string res;
    string cur = nxt[HEAD];
    while (cur != TAIL) {
        if (!res.empty()) res += ' ';
        res += cur;
        cur = nxt[cur];
    }
    cout << (res.empty() ? "empty" : res) << "\n";
    return 0;
}
@@TESTS
--IN
5
back 3
front 1
after 1 2
before 3 9
out 1
--OUT
2 9 3
--IN
2
front 7
out 7
--OUT
empty
--IN
3
front 5
front 6
back 4
--OUT
6 5 4
@@EXPL
(1) 접근·핵심 아이디어

- 명령이 전부 "어떤 사람의 바로 앞/뒤"를 기준으로 하므로, 이름으로 노드를 바로 찾아 이웃 링크만 고치는 이중 연결 리스트가 맞다. `unordered_map` 두 개(`nxt`, `prv`)를 쓰면 이름 → 이웃이 평균 O(1)이라 명령당 O(1), 전체 O(M)이다(`vector`의 `insert`/`erase`는 명령당 O(n)).
- HEAD/TAIL 센티넬 덕에 "맨 앞/맨 뒤"도 일반 삽입과 같은 코드로 처리되고, 빈 줄 검사가 사라진다.

(2) 코드 단계별

- `link(p, x, q)`: p와 q 사이에 x를 끼운다(네 링크 갱신). `unlink(x)`: x의 양 이웃을 서로 이어 붙이고 x의 항목을 지운다.
- `front x` = `link(HEAD, x, nxt[HEAD])`, `back x` = `link(prv[TAIL], x, TAIL)`, `before y x` = `link(prv[y], x, y)`, `after y x` = `link(y, x, nxt[y])`, `out x` = `unlink(x)`.
- 끝나면 HEAD 다음부터 TAIL 전까지 따라가며 이름을 모은다. 비어 있으면 `empty`.

(3) 스스로 다시 짤 때 생각 순서

- "이름 기준 앞/뒤 삽입·삭제 반복" → 이름 → 이웃 해시맵(이중 연결 리스트). 인덱스 기반 `vector` 조작은 O(n)임을 상기한다.
- 함정 — **`link`의 인자를 `const string&`로 받으면 안 된다.** `link(HEAD, x, nxt[HEAD])`에서 셋째 인자가 참조라면 그것은 `nxt[HEAD]`라는 맵 원소 자체를 가리킨다. 본문 첫 줄 `nxt[p] = x`(p == HEAD)가 바로 그 원소를 덮어쓰므로, 그다음 줄에서 읽는 `q`는 이미 `x`로 바뀐 값이다 — 자기 자신을 가리키는 고리가 생겨 출력 루프가 무한히 돈다. 값으로 받으면 호출 시점의 복사본이 남아 안전하다. 덧붙여 `unordered_map`은 삽입 때 재해시가 일어나면 기존 참조가 무효화되므로, 컨테이너를 바꾸는 함수에 그 컨테이너의 원소 참조를 넘기지 않는 것이 원칙이다.
- 삽입·삭제를 함수 하나씩으로 묶고, 네 명령을 그 함수의 인자 차이로 표현해 분기를 줄인다.
- 경계: 사람이 한 명일 때 `out`하면 HEAD-TAIL만 남아 `empty`. 삭제한 이름의 맵 항목을 지워 두면 잘못된 참조를 예방한다.
```

**9) 주문 처리 총 소요 시간** · Hard

- **요구사항**: 주방에 요리사가 한 명이다. 주문 N개가 `(도착 시각 a, 조리 시간 d)`로 주어진다. 요리사는 한 번에 한 주문만 처리하며, 손이 비는 순간 "이미 도착한 주문 중 조리 시간이 가장 짧은 것"(같으면 도착이 빠른 것, 그것도 같으면 입력 순서가 앞선 것)을 고른다. 도착한 주문이 없으면 다음 도착까지 쉰다. 각 주문의 소요 시간은 `완료 시각 - 도착 시각`이다. 모든 주문의 소요 시간 합을 출력한다.
- **입력**: 첫 줄 N(1 ≤ N ≤ 300). 이후 N줄에 `a d`(0 ≤ a ≤ 10^6, 1 ≤ d ≤ 10^4).
- **출력**: 소요 시간의 합.
- **예제**: `4 / 0 5 / 1 2 / 2 4 / 10 1` → `22` · `1 / 5 3` → `3`
- **셀프체크**: 도착 시각으로 정렬한 뒤, 현재 시각 t 이하로 도착한 주문을 힙에 `(d, a, 번호)`로 밀어 넣고 top을 꺼내 처리. 우선순위 규칙 세 단계는 `array<long long,3>`의 사전순 비교로 그대로 표현되고, 최소 힙이 필요하므로 `greater<>`를 준다. 힙이 비었으면 t를 다음 도착 시각으로 "점프"해야 한다(1씩 증가시키면 시간 초과). 검산: t=0에 (0,5) 처리→5, t=5에 도착한 (1,2),(2,4) 중 2→7(소요 6), (2,4)→11(소요 9), (10,1)→12(소요 2), 합 5+6+9+2=22.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<array<long long, 3>> jobs(n);          // (도착, 조리, 입력순서)
    for (int i = 0; i < n; i++) {
        long long a, d;
        cin >> a >> d;
        jobs[i] = {a, d, (long long)i};
    }
    sort(jobs.begin(), jobs.end());               // array는 사전순 비교

    // (조리, 도착, 입력순서) 최소 힙 -> 우선순위 규칙 세 단계가 그대로 표현된다
    priority_queue<array<long long, 3>,
                   vector<array<long long, 3>>,
                   greater<array<long long, 3>>> pq;

    long long t = 0, total = 0;
    int i = 0, done = 0;
    while (done < n) {
        while (i < n && jobs[i][0] <= t) {
            pq.push({jobs[i][1], jobs[i][0], jobs[i][2]});
            i++;
        }
        if (pq.empty()) {
            t = jobs[i][0];                       // 1씩이 아니라 다음 도착 시각으로 점프
            continue;
        }
        array<long long, 3> cur = pq.top();
        pq.pop();
        t += cur[0];
        total += t - cur[1];
        done++;
    }
    cout << total << "\n";
    return 0;
}
@@TESTS
--IN
4
0 5
1 2
2 4
10 1
--OUT
22
--IN
1
5 3
--OUT
3
--IN
2
0 1
10 1
--OUT
2
--IN
3
0 4
0 4
0 4
--OUT
24
@@EXPL
(1) 접근·핵심 아이디어

- "손이 빌 때마다 도착한 주문 중 가장 짧은 것"을 고르는 스케줄링이다. 후보 집합에 주문이 계속 추가되면서 최솟값을 반복해서 꺼내므로 힙이 필요하고, 도착 순서대로 후보에 넣기 위해 도착 시각 정렬이 선행된다. 정렬 O(N log N) + 힙 연산 O(N log N).
- 우선순위 규칙 "짧은 조리 → 이른 도착 → 앞선 입력"은 `array<long long,3>`의 사전순 비교로 그대로 표현된다. `std::array`는 `operator<`가 원소를 앞에서부터 비교하도록 정의되어 있어 파이썬 튜플과 똑같이 동작한다(`pair`는 두 값까지, 세 값 이상은 `array`나 `tuple`).

(2) 코드 단계별

- 주문을 `{a, d, 번호}`로 모아 정렬한다. 첫 원소가 도착 시각이므로 사전순 정렬이 곧 도착순이다.
- 현재 시각 t에서, 아직 안 넣은 주문 중 `a <= t`인 것을 모두 힙에 `{d, a, 번호}`로 넣는다(넣는 순서를 바꾸는 것이 핵심 — 정렬 키와 우선순위 키가 다르다).
- 힙이 비어 있으면(도착한 주문이 없음) `t`를 다음 주문의 도착 시각으로 점프하고 다시 시도.
- 힙 top을 꺼내 `t += d`, 소요 시간 `t - a`를 합산. 처리한 개수가 N이 되면 종료.

(3) 스스로 다시 짤 때 생각 순서

- "빌 때마다 최선을 고른다 + 후보가 시간에 따라 열린다" → 정렬(도착) + 힙(선택)의 2단 구조를 먼저 그린다.
- 함정 — `priority_queue`의 기본은 최대 힙이므로 세 번째 템플릿 인자에 `greater<...>`를 반드시 준다. 이때 둘째 인자(내부 컨테이너 `vector<...>`)도 같이 적어야 한다. 이 세 인자 형태를 통째로 외워 두면 매번 헤맬 일이 없다.
- 시간 진행을 1씩 돌리지 말고 "처리 완료 시각" 또는 "다음 도착 시각"으로만 점프시켜야 도착 시각이 커도 안전하다.
- 함정 — `pq.top()`은 참조를 반환한다. `pop()` 뒤에 그 참조를 읽으면 이미 사라진 원소를 읽는 것이다. 위 코드처럼 값으로 복사해 두고 `pop()`한다.
- 경계: 주문 사이에 공백이 있는 경우(셋째 테스트), 전원 동시에 도착하고 조리 시간이 같은 경우(넷째 테스트: 4+8+12=24, 입력 순서 규칙). 우선순위를 `d`만으로 두면 동점 시 순서가 불정(不定)이 되니 세 값을 다 넣는다.
```

**10) 양끝 삭제 우선순위 큐** · Hard

- **요구사항**: 정수 다중집합에 `I v`(v 삽입), `D 1`(최댓값 하나 삭제), `D -1`(최솟값 하나 삭제), `Q`(현재 최댓값과 최솟값 출력, 비어 있으면 `EMPTY`) 연산을 순서대로 적용한다. 빈 상태의 `D`는 무시한다. 같은 값이 여러 개면 하나만 지운다.
- **입력**: 첫 줄 Q(1 ≤ Q ≤ 500). 이후 Q줄에 연산(v는 -10^9 이상 10^9 이하).
- **출력**: `Q` 연산마다 `최댓값 최솟값` 또는 `EMPTY`를 줄마다.
- **예제**: `7 / I 5 / I 3 / I 8 / D 1 / Q / D -1 / Q` → `5 3 / 5 5` · `3 / D 1 / I 4 / Q` → `4 4`
- **셀프체크**: `multiset`은 중복을 허용하면서 정렬을 유지하고 **양끝을 동시에 준다** — 최솟값 `*ms.begin()`, 최댓값 `*ms.rbegin()`, 중간 원소 삭제 O(log n). 파이썬처럼 힙 두 개 + 지연 삭제를 만들 이유가 없다. 단, "하나만 지우기"는 `ms.erase(반복자)`여야 한다 — `ms.erase(값)`은 같은 값을 **전부** 지운다(넷째 테스트에서 바로 드러난다).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    multiset<long long> ms;              // 중복 허용 + 정렬 유지 + 양끝 O(1) 조회
    string out;
    for (int i = 0; i < q; i++) {
        string op;
        cin >> op;
        if (op == "I") {
            long long v;
            cin >> v;
            ms.insert(v);
        } else if (op == "D") {
            int dir;
            cin >> dir;
            if (ms.empty()) continue;    // 빈 상태의 D는 무시
            if (dir == 1) ms.erase(prev(ms.end()));  // 최댓값 '하나'만
            else ms.erase(ms.begin());               // 최솟값 '하나'만
        } else {
            if (ms.empty()) {
                out += "EMPTY\n";
            } else {
                out += to_string(*ms.rbegin());
                out += ' ';
                out += to_string(*ms.begin());
                out += '\n';
            }
        }
    }
    cout << out;
    return 0;
}
@@TESTS
--IN
7
I 5
I 3
I 8
D 1
Q
D -1
Q
--OUT
5 3
5 5
--IN
3
D 1
I 4
Q
--OUT
4 4
--IN
4
I 1
D -1
D 1
Q
--OUT
EMPTY
--IN
5
I 2
I 2
D 1
Q
D -1
--OUT
2 2
@@EXPL
(1) 접근·핵심 아이디어

- 최댓값 삭제와 최솟값 삭제가 모두 필요하다. 파이썬에는 "정렬을 유지하는 다중집합"이 없어서 최소 힙과 최대 힙에 같은 원소를 넣고, 고유번호로 `alive` 집합을 관리하고, top이 죽은 원소면 걷어내는 **지연 삭제**를 직접 구현해야 했다. C++에는 `std::multiset`이 있으므로 그 우회가 통째로 사라진다.
- `multiset`은 균형 이진 탐색 트리라 정렬을 유지하면서 중복을 허용한다. 최솟값은 `*ms.begin()`, 최댓값은 `*ms.rbegin()`으로 O(1)에 보고, 그 자리에서 O(log n)에 지운다. 연산당 O(log n)으로 두 힙 풀이와 복잡도는 같지만 코드가 3분의 1로 줄고 버그 여지가 없다.

(2) 코드 단계별

- `I v`: `ms.insert(v)`. 같은 값이 여러 개 들어와도 각각 보존된다.
- `D 1`: `ms.erase(prev(ms.end()))` — `end()`는 마지막 다음이므로 한 칸 앞이 최댓값이다. `D -1`: `ms.erase(ms.begin())`.
- 삭제 전에 `ms.empty()`를 검사한다. 빈 `multiset`에서 `prev(ms.end())`나 `ms.begin()`을 지우면 정의되지 않은 동작이다.
- `Q`: 비어 있으면 `EMPTY`, 아니면 `*ms.rbegin()`과 `*ms.begin()`을 공백으로 이어 출력.

(3) 스스로 다시 짤 때 생각 순서

- "최댓값과 최솟값을 둘 다, 그리고 중복도 유지" → `multiset` 한 줄이면 끝난다. 힙 두 개를 떠올렸다면 그것은 파이썬의 사고 습관이다. `priority_queue`가 필요한 자리는 "중간 원소를 지울 일이 없고 극단값만 반복해서 꺼낼 때"다.
- 함정 — **`ms.erase(값)`은 그 값을 가진 원소를 전부 지운다.** 넷째 테스트처럼 2가 두 개 있을 때 `ms.erase(2)`를 부르면 둘 다 사라져 그다음 `Q`가 `EMPTY`를 내며 오답이 난다. 하나만 지우려면 반드시 반복자를 넘긴다: `ms.erase(ms.find(2))`, 또는 위치를 이미 알고 있으면 `ms.erase(it)`. `erase(값)`이 지운 개수를 반환한다는 것도 이 성질의 흔적이다.
- 함정 2 — `ms.rbegin()`은 역방향 반복자라 `ms.erase(ms.rbegin())`처럼 그대로 넘길 수 없다. `prev(ms.end())`를 쓰거나 `ms.erase(--ms.end())`를 쓴다.
- 함정 3 — `*ms.end()`나 빈 컨테이너의 `*ms.begin()`은 읽으면 안 된다. 모든 삭제·조회 앞에 `empty()` 검사를 둔다.
- 경계: 빈 상태의 D(무시), 원소 하나일 때 최대=최소, 전부 지운 뒤 `EMPTY`, 같은 값 2개 중 하나만 삭제.
```

**11) 막대 절단 후 가장 긴 조각** · Hard

- **요구사항**: 길이 L의 막대가 좌표 0부터 L까지 놓여 있다. 절단 위치 x가 하나씩 주어질 때마다(이미 잘린 위치는 다시 주어지지 않음) 그 위치를 자르고, 현재 남아 있는 조각 중 가장 긴 조각의 길이를 출력한다.
- **입력**: 첫 줄 L Q(2 ≤ L ≤ 10^9, 1 ≤ Q ≤ 300). 이후 Q줄에 절단 위치 x(0 < x < L, 서로 다름).
- **출력**: 절단마다 가장 긴 조각의 길이를 줄마다.
- **예제**: `10 3 / 4 / 8 / 2` → `6 / 4 / 4` · `5 1 / 1` → `4`
- **셀프체크**: 절단점은 `set<long long>`에 넣고 좌우 이웃을 `it = pts.lower_bound(x)`(오른쪽 이웃)와 `prev(it)`(왼쪽 이웃)로 얻는다. 조각 길이는 `multiset<long long>`에 담아 최댓값을 `*rbegin()`으로 본다 — 조각 `b-a` 하나를 `erase(find(b-a))`로 지우고 `x-a`, `b-x` 둘을 넣는다. `erase(b-a)`라고 쓰면 같은 길이의 조각이 **전부** 사라진다. 검산: 10 → {4,6} → 6; 8 절단 → {4,4,2} → 4; 2 절단 → {2,2,4,2} → 4.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    long long L;
    int q;
    cin >> L >> q;

    set<long long> pts;                 // 절단점(양끝 포함): 이웃 탐색용
    pts.insert(0);
    pts.insert(L);
    multiset<long long> len;            // 조각 길이: 최댓값 조회용
    len.insert(L);

    string out;
    for (int i = 0; i < q; i++) {
        long long x;
        cin >> x;
        auto it = pts.lower_bound(x);   // 멤버 함수! x 이상 첫 점 = 오른쪽 이웃
        long long b = *it;
        long long a = *prev(it);        // 왼쪽 이웃
        pts.insert(x);

        len.erase(len.find(b - a));     // '하나만' 지운다 (erase(b-a)는 전부 지움)
        len.insert(x - a);
        len.insert(b - x);

        out += to_string(*len.rbegin());
        out += '\n';
    }
    cout << out;
    return 0;
}
@@TESTS
--IN
10 3
4
8
2
--OUT
6
4
4
--IN
5 1
1
--OUT
4
--IN
7 2
3
6
--OUT
4
3
@@EXPL
(1) 접근·핵심 아이디어

- 이 문제는 두 가지를 동시에 요구한다. (가) 새 절단점 x의 **좌우 이웃 찾기**, (나) 조각 길이의 **최댓값 조회 + 하나 삭제**. 파이썬에는 둘 다 표준이 없어 (가)는 정렬 리스트 + `bisect`(삽입 O(n)), (나)는 최대 힙 + "길이 → 개수" 딕셔너리 + 지연 삭제로 흉내 냈다.
- C++에서는 (가)는 `set`, (나)는 `multiset` 하나씩이면 끝난다. `set::lower_bound(x)`는 O(log n)에 오른쪽 이웃을 주고 `prev`가 왼쪽 이웃을 준다. `multiset`은 최댓값이 `*rbegin()`, 중간 원소 삭제가 O(log n)이라 "이미 사라진 최댓값"이라는 개념 자체가 생기지 않는다 — 지연 삭제도 개수 딕셔너리도 필요 없다.

(2) 코드 단계별

- `pts = {0, L}`, `len = {L}`로 시작한다. 양끝을 절단점 취급하면 첫 절단도 특별 취급 없이 처리된다.
- 절단 x마다 `it = pts.lower_bound(x)` → `b = *it`(오른쪽 이웃), `a = *prev(it)`(왼쪽 이웃). x는 아직 집합에 없으므로 `lower_bound`와 `upper_bound` 중 무엇을 써도 같은 곳을 가리킨다.
- `pts.insert(x)`로 절단점 등록.
- 사라진 조각 `b-a`를 `len.erase(len.find(b-a))`로 하나만 지우고, 새 조각 `x-a`, `b-x`를 넣는다.
- `*len.rbegin()`이 현재 최댓값.

(3) 스스로 다시 짤 때 생각 순서

- "이웃을 찾아 조각을 쪼갠다" → `set`. "최댓값을 계속 보되 중간 원소도 지운다" → `multiset`. 요구를 두 줄로 적고 각각에 컨테이너를 하나씩 배정하면 설계가 끝난다.
- 함정 1 — **`len.erase(b - a)`는 그 길이의 조각을 전부 지운다.** 셋째 절단에서 길이 4짜리가 두 개일 때 이렇게 쓰면 둘 다 사라져 이후 최댓값이 틀린다. 반드시 `erase(find(값))`으로 반복자 하나를 넘긴다.
- 함정 2 — **`pts.lower_bound(x)`는 멤버 함수여야 한다.** `std::lower_bound(pts.begin(), pts.end(), x)`도 컴파일되고 같은 답을 내지만, `set`의 반복자는 임의 접근이 아니라 한 칸씩만 움직여서 **O(n)**이 된다. 절단이 10^5번이면 O(n^2)으로 시간 초과다. `map`/`set`/`multiset`에서는 항상 멤버 `lower_bound`/`upper_bound`를 쓴다.
- 함정 3 — `prev(it)`을 부르기 전에 `it != pts.begin()`인지 확인해야 하는 게 원칙이다. 이 문제는 0을 미리 넣어 두었고 `0 < x`가 보장되므로 `it`이 절대 `begin()`이 아니지만, 양끝 센티넬을 안 넣었다면 그 검사가 반드시 필요하다.
- 경계: 첫 절단에서 이웃이 0과 L, 정확히 절반 절단(같은 길이 두 개), 최댓값이 바뀌지 않는 절단(셋째 테스트 첫 줄). 좌표가 10^9까지이므로 `long long`으로 받아 둔다.
```

**12) 카드 지우기와 되돌리기** · Hard

- **요구사항**: 1부터 N까지 번호가 적힌 카드가 순서대로 놓여 있고 커서는 1번 카드 위에 있다. 명령은 네 가지다. `L`: 커서를 왼쪽 카드로(맨 왼쪽이면 무시). `R`: 오른쪽 카드로(맨 오른쪽이면 무시). `D`: 커서 위 카드를 지운다. 커서는 오른쪽 이웃으로 가고, 오른쪽이 없으면 왼쪽 이웃으로 간다(카드가 1장뿐일 때 `D`는 주어지지 않는다). `U`: 가장 최근에 지운 카드를 원래 자리(지울 당시의 양 이웃 사이)에 되돌리고 커서를 그 카드로 옮긴다(되돌릴 카드가 없으면 무시). 모든 명령 후 남은 카드를 순서대로 출력하고, 둘째 줄에 커서가 가리키는 카드 번호를 출력한다.
- **입력**: 첫 줄 N M(2 ≤ N ≤ 500, 1 ≤ M ≤ 500). 둘째 줄에 M개의 명령이 공백으로.
- **출력**: 첫 줄에 남은 카드 번호들을 공백으로, 둘째 줄에 커서 카드 번호.
- **예제**: `5 5 / R D D U L` → `1 3 4 5 / 1` · `3 4 / D U U D` → `2 3 / 2`
- **셀프체크**: 카드 번호가 1..N이므로 해시맵이 아니라 `vector<int> prv, nxt`(0과 N+1을 센티넬)면 충분하다 — 삭제는 `nxt[prv[x]] = nxt[x]; prv[nxt[x]] = prv[x]`, 되돌리기는 x의 포인터를 건드리지 않고 `nxt[prv[x]] = x; prv[nxt[x]] = x`. 되돌리기는 지운 순서의 역순(스택)으로만 정확하다. 검산(첫 예제): R→커서2, D→2 삭제·커서3, D→3 삭제·커서4, U→3 복원·커서3, L→커서1.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    // 번호가 1..N이므로 해시맵이 아니라 배열로 둔다 (0과 N+1이 센티넬)
    vector<int> nxt(n + 2), prv(n + 2);
    for (int i = 0; i <= n + 1; i++) {
        nxt[i] = i + 1;
        prv[i] = i - 1;
    }
    int cur = 1;
    vector<int> st;                       // 지운 순서 스택

    for (int i = 0; i < m; i++) {
        string op;
        cin >> op;
        if (op == "L") {
            if (prv[cur] != 0) cur = prv[cur];
        } else if (op == "R") {
            if (nxt[cur] != n + 1) cur = nxt[cur];
        } else if (op == "D") {
            int p = prv[cur], q = nxt[cur];
            nxt[p] = q; prv[q] = p;       // cur의 prv/nxt는 그대로 남겨 둔다
            st.push_back(cur);
            cur = (q != n + 1) ? q : p;
        } else {
            if (!st.empty()) {
                int x = st.back();
                st.pop_back();
                nxt[prv[x]] = x;          // 보존해 둔 포인터로 제자리 복귀
                prv[nxt[x]] = x;
                cur = x;
            }
        }
    }

    string res;
    for (int v = nxt[0]; v != n + 1; v = nxt[v]) {
        if (!res.empty()) res += ' ';
        res += to_string(v);
    }
    cout << res << "\n" << cur << "\n";
    return 0;
}
@@TESTS
--IN
5 5
R D D U L
--OUT
1 3 4 5
1
--IN
3 4
D U U D
--OUT
2 3
2
--IN
4 5
R R R D D
--OUT
1 2
2
--IN
4 5
R D D U U
--OUT
1 2 3 4
2
@@EXPL
(1) 접근·핵심 아이디어

- 커서 이동·삭제·복원이 모두 "이웃"만으로 정의되므로 이중 연결 리스트가 자연스럽다. 카드 번호가 1..N이라 문제 8처럼 해시맵을 쓸 필요가 없다 — `vector<int> prv, nxt`로 두면 조회가 진짜 O(1)이고(해시 계산조차 없다) 캐시 지역성도 좋다. 0과 N+1을 센티넬로 쓰면 끝 검사가 `prv[cur] != 0`, `nxt[cur] != n+1`로 단순해진다. 명령당 O(1), 전체 O(N + M).
- 복원의 핵심은 삭제된 노드 x의 `prv[x]`, `nxt[x]`를 **지우지 않고 남겨 두는 것**이다. 그 두 값이 "지울 당시의 이웃"이므로 `nxt[prv[x]] = x; prv[nxt[x]] = x;`만으로 제자리에 돌아간다. 단, 이웃들이 그 사이에 바뀌지 않았어야 하므로 지운 역순(스택)으로만 복원한다.

(2) 코드 단계별

- `nxt[i] = i+1`, `prv[i] = i-1`로 0..N+1을 잇고 커서는 1. 배열 크기는 N+2다(인덱스 N+1까지 쓰므로 N+1로 잡으면 범위를 벗어난다).
- `L`/`R`: 이웃이 센티넬이 아니면 이동.
- `D`: 양 이웃 `p, q`를 서로 잇고 `cur`를 스택에 push. 커서는 `q`가 센티넬이 아니면 `q`, 아니면 `p`.
- `U`: 스택이 비어 있지 않으면 pop한 x를 자기 포인터로 재연결하고 커서를 x로.
- 끝나면 `nxt[0]`부터 N+1 전까지 따라가 출력하고, 커서 번호를 둘째 줄에 출력.

(3) 스스로 다시 짤 때 생각 순서

- "지운 것을 원래 자리에 되돌린다"를 보면, 삭제 시 노드의 포인터를 보존하고 스택(`vector` + `push_back`/`pop_back`, 또는 `std::stack`)으로 순서를 기억하는 패턴을 떠올린다.
- 함정 — `vector<int> nxt(n + 2)`처럼 크기를 정확히 잡는다. `vector`의 `operator[]`는 범위를 검사하지 않으므로 `nxt[n+1]`을 크기 `n+1`짜리에 쓰면 조용히 메모리를 망가뜨린다(파이썬처럼 IndexError가 나지 않는다). 디버깅할 때는 `.at()`으로 바꿔 보면 예외가 잡힌다.
- 함정 2 — `st.back()`은 비어 있을 때 부르면 정의되지 않은 동작이다. `!st.empty()` 검사를 먼저 한다("되돌릴 카드가 없으면 무시"라는 규칙이 곧 그 검사다).
- 삭제 후 커서 규칙(오른쪽 우선, 없으면 왼쪽)을 센티넬 비교로 정확히 옮긴다(셋째 테스트: 맨 끝 삭제).
- 경계: 되돌릴 것이 없는 `U`(무시), 연속 두 번 삭제 후 두 번 복원(넷째 테스트: 3을 먼저 되돌려야 2가 1과 3 사이로 정확히 돌아간다), 커서가 복원된 카드로 이동하는지 확인.
```
