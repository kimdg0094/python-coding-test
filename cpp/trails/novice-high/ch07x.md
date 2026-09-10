## L2. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch07(해싱)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. 모든 문제의 공통 질문은 하나다 — "무엇을 키로 잡아야 O(n) 탐색이 O(1) 조회로 바뀌는가".
- **반복 훈련 개념**:

- 존재 판정 — `unordered_set<int> seen;`을 두고 `if (seen.count(x))` 확인 후 `seen.insert(x)`. "확인 → 추가" 순서가 핵심.
- 빈도 세기 — `unordered_map<T,int> cnt; for (auto &x : arr) cnt[x]++;`. C++의 `[]`는 없는 키를 **값 0으로 자동 생성**하므로 `cnt[x]++`가 그대로 동작한다.
- 집합 연산 — 교집합·차집합 전용 연산자가 없다. `set`을 돌며 `other.count(x)`로 직접 가른다. `set`은 오름차순 순회라 출력 순서가 저절로 고정된다.
- 키→값 매핑·그룹화 — `m[key] = value`로 명령을 처리하고, `map<string, vector<T>>`에 `m[key].push_back(...)`로 같은 키끼리 모은다(빈 `vector`가 자동 생성된다).
- 복합 키 — 좌표는 `pair<int,int>`로 `set`에 넣거나 `x * 10000LL + y`처럼 하나의 정수로 접어 넣는다. `unordered_set<pair<int,int>>`는 표준 해시가 없어 그대로는 컴파일되지 않는다.

- **코딩테스트 출제 맵**: 프로그래머스 「코딩테스트 고득점 Kit」의 '해시'(명단 대조·접두어 충돌·장르별 상위 곡 류), NeetCode 150의 'Arrays & Hashing'(두 수의 합·가장 긴 연속 수열·부분합 개수 류), solved.ac CLASS 2~3의 집합·맵 문제가 이 레슨 수준이다.
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 두 번 찍힌 첫 출입 카드 | Easy | unordered_set 존재 판정(확인→추가) | 반복 훈련 |
| 2 | 두 동아리의 겹치는 회원과 단독 회원 | Easy | set 순회 + count()로 교집합·차집합 | 반복 훈련 |
| 3 | 기준 횟수 이상 팔린 상품 | Easy | map 빈도 + 조건 필터(정렬 순회) | 반복 훈련 |
| 4 | 청소 로봇이 밟은 칸 수 | Easy | set<pair<int,int>>(좌표 방문) | 반복 훈련 |
| 5 | 반납되지 않은 책 | Medium | map 빈도 더하고 빼기 | 유형 확장 (프로그래머스 Kit '해시' 스타일) |
| 6 | 명령 패턴과 단어 열의 일대일 대응 | Medium | map 양방향 매핑 | 유형 확장 (NeetCode 'Arrays & Hashing' 스타일) |
| 7 | 합이 K인 카드 쌍의 개수 | Medium | unordered_map 빈도로 짝 개수 누적 | 반복 훈련 |
| 8 | 서로 접두어가 되는 상품 코드 | Medium | unordered_set 존재 판정 × 접두어 순회 | 유형 확장 (프로그래머스 Kit '해시' 스타일) |
| 9 | 단어장 명령 처리 | Medium | map 삽입·삭제·조회(find vs []) | 반복 훈련 |
| 10 | 가장 긴 연속 정수 구간 | Hard | unordered_set 존재 판정으로 구간 시작점 찾기 | 유형 확장 (NeetCode 'Arrays & Hashing' 스타일) |
| 11 | 합이 K인 연속 구간의 개수 | Hard | 누적합 + unordered_map 빈도 | 유형 확장 (NeetCode 'Arrays & Hashing' 스타일) |
| 12 | 장르별 인기곡 플레이리스트 | Hard | map 그룹화 + 다중 키 비교 함수 정렬 | 유형 확장 (프로그래머스 Kit '해시' 스타일) |

**문제**

**1) 두 번 찍힌 첫 출입 카드** · Easy

- **요구사항**: 출입문 기록에 카드 번호가 찍힌 순서대로 주어진다. 앞에서부터 읽을 때 처음으로 "이미 찍힌 적 있는" 번호가 다시 나오는 순간, 그 번호를 출력하라. 끝까지 그런 번호가 없으면 `-1`. `vector`를 매번 선형 탐색하지 말고 `unordered_set`으로 평균 O(n)에 해결하라.
- **입력**: 첫 줄에 기록 수 `n`(1 ≤ n ≤ 1000), 둘째 줄에 카드 번호 `n`개(1 이상 10^9 이하 정수).
- **출력**: 번호 하나 또는 `-1`.
- **예제**: `6 / 3 1 4 1 5 3` → `1` · `4 / 7 8 9 10` → `-1`
- **셀프체크**: 3도 두 번 나오지만 "두 번째 등장 시점"이 더 빠른 1이 답이다 — 값 크기가 아니라 시점 기준임을 확인하라. 확인보다 추가를 먼저 하면 첫 원소가 곧바로 중복으로 잡히는 오류가 난다. n=1이면 항상 -1.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    unordered_set<int> seen;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        if (seen.count(x)) {          // 확인 먼저
            cout << x << "\n";
            return 0;
        }
        seen.insert(x);               // 그 다음 추가
    }
    cout << -1 << "\n";
    return 0;
}
@@TESTS
--IN
6
3 1 4 1 5 3
--OUT
1
--IN
4
7 8 9 10
--OUT
-1
--IN
1
5
--OUT
-1
--IN
5
2 2 2 2 2
--OUT
2
@@EXPL
(1) 접근·핵심 아이디어

- "이미 나왔는가"는 존재 판정이므로 지나온 번호를 `unordered_set`에 담아 두면 각 조회가 평균 O(1), 전체 O(n)이다. `vector`를 `find`로 뒤지면 매번 O(n)이라 전체 O(n^2)가 된다.
- 앞에서부터 훑다가 처음 `count(x)`가 1이 되는 순간이 곧 "가장 빠른 두 번째 등장"이므로 바로 출력하고 끝내면 된다.

(2) 코드 단계별

- `n`을 읽고, 번호를 하나씩 읽으며 즉시 판정한다(배열에 다 담아 둘 필요가 없다).
- 빈 `seen`을 두고 각 `x`에 대해 먼저 `seen.count(x)`를 확인 — 1이면 출력 후 `return 0`.
- 0이면 `seen.insert(x)`로 등록하고 다음으로 넘어간다.
- 반복이 끝까지 가면 중복이 없었다는 뜻이므로 `-1`.

(3) 스스로 다시 짤 때 생각 순서

- "이전에 본 적 있나?"라는 질문이 나오면 자동으로 `unordered_set`을 떠올린다.
- 확인과 추가의 순서를 먼저 고정한다(확인 → 추가). 순서를 바꾸면 첫 원소부터 오답.
- **C++ 함정**: 존재 판정에 `unordered_map`의 `[]`를 쓰면 없는 키가 값 0으로 **조용히 생성**된다(파이썬 `KeyError`와 정반대). 판정에는 `count()`나 `find()`를 쓴다. 여기서는 값이 필요 없으니 `unordered_set`이 맞다.
- 답이 "첫 번째 시점"인지 "가장 작은 값"인지 문제 문장을 다시 읽고 확인한다. n=1, 전부 같은 값 같은 경계로 검산한다.
```

**2) 두 동아리의 겹치는 회원과 단독 회원** · Easy

- **요구사항**: 동아리 A와 B의 회원 학번 목록이 주어진다. 첫 줄에 두 동아리에 모두 속한 학번을 오름차순으로, 둘째 줄에 A에만 속한 학번을 오름차순으로 출력하라. 해당 학번이 하나도 없으면 그 줄에 `NONE`을 출력한다. 한 목록 안에 같은 학번이 여러 번 적혀 있을 수 있으며 같은 사람으로 본다.
- **입력**: 첫 줄에 `n m`(1 ≤ n, m ≤ 200), 둘째 줄에 A의 학번 `n`개, 셋째 줄에 B의 학번 `m`개(1 이상 10^6 이하 정수).
- **출력**: 두 줄. 각 줄은 공백으로 구분된 오름차순 학번 또는 `NONE`.
- **예제**: `4 3 / 101 205 333 101 / 205 999 333` → `205 333 / 101` · `2 2 / 1 2 / 1 2` → `1 2 / NONE`
- **셀프체크**: 목록을 `set`에 넣는 순간 중복이 사라짐을 확인하라(101이 두 번 있어도 `insert`가 무시한다). "A에는 있고 B에는 없는 것"은 대칭이 아니다. 결과가 비었을 때 그냥 출력하면 빈 줄이 되므로 `NONE` 처리를 따로 해야 한다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

void emit(const vector<int> &v) {
    if (v.empty()) {
        cout << "NONE" << "\n";
        return;
    }
    for (size_t i = 0; i < v.size(); i++) {
        if (i) cout << ' ';
        cout << v[i];
    }
    cout << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    set<int> a, b;                    // set 은 오름차순 순회 -> 정렬이 공짜
    for (int i = 0; i < n; i++) { int x; cin >> x; a.insert(x); }
    for (int i = 0; i < m; i++) { int x; cin >> x; b.insert(x); }

    vector<int> both, onlyA;
    for (int x : a) {
        if (b.count(x)) both.push_back(x);   // 교집합
        else onlyA.push_back(x);             // 차집합 A - B
    }
    emit(both);
    emit(onlyA);
    return 0;
}
@@TESTS
--IN
4 3
101 205 333 101
205 999 333
--OUT
205 333
101
--IN
2 2
1 2
1 2
--OUT
1 2
NONE
--IN
3 1
5 6 7
9
--OUT
NONE
5 6 7
@@EXPL
(1) 접근·핵심 아이디어

- "양쪽 모두에 있는가 / 한쪽에만 있는가"는 집합 연산이다. C++에는 파이썬의 `&`, `-` 같은 집합 연산자가 없으므로 A를 한 번 순회하며 `b.count(x)`로 두 갈래로 가른다. 순회 O(n), 조회 O(log m) — 전체 O(n log m)이고 이중 반복 O(n·m)보다 훨씬 빠르다.
- `unordered_set`을 쓰면 조회는 O(1)이지만 **순회 순서가 보장되지 않는다**. 출력이 오름차순이어야 하므로 `set`(균형 이진 탐색 트리)을 골라 정렬을 공짜로 얻는다.

(2) 코드 단계별

- `n`, `m`을 읽고 각각 `set<int>`에 `insert` — 같은 값을 다시 넣으면 조용히 무시되어 중복이 자동 제거된다.
- A를 오름차순으로 돌며 `b.count(x)`가 1이면 `both`에, 0이면 `onlyA`에 담는다. 이미 오름차순이라 따로 `sort`할 필요가 없다.
- `emit`으로 비었으면 `NONE`, 아니면 공백으로 이어 출력한다.

(3) 스스로 다시 짤 때 생각 순서

- "겹치는 것 / 한쪽에만 있는 것" 문장을 보면 두 컨테이너와 `count()` 한 번의 순회로 번역한다.
- **C++ 함정**: `unordered_set`/`unordered_map`은 순회 순서가 구현 정의다. 출력 순서가 답에 영향을 주면 `set`/`map`을 쓰거나 `vector`에 담아 `sort`한다.
- 공백 구분 출력은 "첫 원소 앞에는 공백 없음"을 `if (i) cout << ' ';`로 처리한다. 줄 끝에 공백을 남기지 않는다.
- 출력 순서 고정과 빈 결과(`NONE`) 두 가지 마무리를 잊지 않는다. B가 A를 전부 포함하는 경우(둘째 줄 `NONE`)로 검산한다.
```

**3) 기준 횟수 이상 팔린 상품** · Easy

- **요구사항**: 하루 판매 기록이 상품 코드의 나열로 주어진다. `k`번 이상 팔린 상품 코드를 사전순으로 한 줄에 하나씩 `코드 판매횟수` 형식으로 출력하라. 하나도 없으면 `NONE`.
- **입력**: 첫 줄에 `n k`(1 ≤ k ≤ n ≤ 1000), 둘째 줄에 상품 코드 `n`개(소문자·숫자로 된 길이 1~10 문자열).
- **출력**: 조건을 만족하는 코드마다 한 줄 `코드 횟수`(사전순), 또는 `NONE`.
- **예제**: `7 2 / pen cup pen bag cup pen ink` → `cup 2 / pen 3` · `3 2 / a b c` → `NONE`
- **셀프체크**: `map<string,int>`로 한 번에 빈도표를 만든 뒤 `>= k` 필터를 거는지 확인하라. 출력 순서는 빈도가 아니라 사전순이다(`pen 3`이 `cup 2`보다 뒤). `map`은 키 오름차순 순회이므로 사전순이 공짜다. k=1이면 모든 서로 다른 코드가 출력된다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    map<string, int> cnt;             // 키 오름차순 = 사전순
    for (int i = 0; i < n; i++) {
        string s;
        cin >> s;
        cnt[s]++;                     // 없는 키는 0으로 자동 생성된 뒤 1이 된다
    }

    bool any = false;
    for (const auto &kv : cnt) {
        if (kv.second >= k) {
            cout << kv.first << ' ' << kv.second << "\n";
            any = true;
        }
    }
    if (!any) cout << "NONE" << "\n";
    return 0;
}
@@TESTS
--IN
7 2
pen cup pen bag cup pen ink
--OUT
cup 2
pen 3
--IN
3 2
a b c
--OUT
NONE
--IN
1 1
z
--OUT
z 1
@@EXPL
(1) 접근·핵심 아이디어

- "몇 번 나왔는가"는 빈도 세기이므로 `map<string,int>`(코드 → 횟수)를 O(n log n)에 만든다. 그 다음 횟수 조건으로 거르면 끝이다.
- 출력 규칙이 "사전순"이므로 `map`을 고른다. `map`은 키 오름차순으로 순회하므로 정렬 단계가 필요 없다. `unordered_map`을 썼다면 키를 `vector`에 뽑아 `sort` 해야 한다.

(2) 코드 단계별

- `n`, `k`를 읽고 코드를 하나씩 읽으며 `cnt[s]++`.
- `map`을 처음부터 끝까지 돌며 `kv.second >= k`인 것만 `코드 횟수`로 출력한다.
- 하나도 출력하지 않았으면(`any == false`) `NONE`.

(3) 스스로 다시 짤 때 생각 순서

- "k번 이상"이라는 조건을 보면 빈도표부터 만든다.
- **C++ 함정이자 편의**: `cnt[s]++`는 없는 키를 값 0으로 만든 뒤 증가시킨다. 파이썬이라면 `KeyError`가 났을 코드가 C++에서는 조용히 동작한다 — 세기에는 편하지만, 단순히 "있는지 보려고" `if (cnt[s] > 0)`라고 쓰면 그 순간 키가 생겨 `map`이 커진다. 조회만 할 때는 `count()`/`find()`.
- 정렬 기준이 무엇인지(사전순 vs 빈도순) 확인하고 컨테이너를 고른다.
- 조건을 만족하는 것이 없는 경우의 출력(`NONE`)을 별도로 처리한다. k=1(전부 출력), n=1 경계로 검산한다.
```

**4) 청소 로봇이 밟은 칸 수** · Easy

- **요구사항**: 로봇이 (0, 0)에서 출발해 명령 문자열을 따라 한 칸씩 움직인다(`U`: y+1, `D`: y-1, `L`: x-1, `R`: x+1). 로봇이 한 번이라도 밟은 서로 다른 칸의 수(출발 칸 포함)와, 이미 밟았던 칸을 다시 밟은 횟수를 공백으로 구분해 출력하라.
- **입력**: 한 줄에 명령 문자열(길이 1 이상 1000 이하, `U/D/L/R`만 포함).
- **출력**: `서로다른칸수 재방문횟수`.
- **예제**: `RRUULLDD` → `8 1` · `RLRL` → `2 3`
- **셀프체크**: 좌표를 `unordered_set<pair<int,int>>`에 넣으면 표준 해시 함수가 없어 **컴파일 오류**가 난다 — `set<pair<int,int>>`를 쓰거나 좌표를 하나의 정수로 접어야 한다. 출발 칸을 처음부터 방문 집합에 넣어야 `RLRL`에서 되돌아올 때 재방문으로 잡힌다. 명령 한 글자짜리 입력에서 `2 0`이 나오는지 확인하라.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string cmds;
    cin >> cmds;

    map<char, pair<int, int>> move;   // 방향 문자 -> (dx, dy)
    move['U'] = make_pair(0, 1);
    move['D'] = make_pair(0, -1);
    move['L'] = make_pair(-1, 0);
    move['R'] = make_pair(1, 0);

    int x = 0, y = 0, revisit = 0;
    set<pair<int, int>> visited;      // pair 는 < 연산자가 있어 set 에 바로 들어간다
    visited.insert(make_pair(0, 0));  // 출발 칸 포함

    for (char ch : cmds) {
        pair<int, int> d = move[ch];
        x += d.first;
        y += d.second;
        pair<int, int> cur = make_pair(x, y);
        if (visited.count(cur)) revisit++;
        else visited.insert(cur);
    }
    cout << visited.size() << ' ' << revisit << "\n";
    return 0;
}
@@TESTS
--IN
RRUULLDD
--OUT
8 1
--IN
RLRL
--OUT
2 3
--IN
U
--OUT
2 0
@@EXPL
(1) 접근·핵심 아이디어

- "이 칸을 밟은 적 있는가"는 좌표에 대한 존재 판정이다. `pair<int,int>`는 사전식 `<` 비교 연산자를 갖고 있어 `set`의 원소가 될 수 있다.
- 방향 문자 → 이동량도 `map<char, pair<int,int>>`로 매핑하면 `if/else if` 네 갈래가 한 줄 조회로 줄어든다.

(2) 코드 단계별

- 명령 문자열을 읽고, 방향별 `(dx, dy)`를 `map`에 준비한다.
- 현재 좌표 `(0, 0)`을 방문 집합 `visited`에 미리 넣는다(출발 칸 포함).
- 각 명령마다 좌표를 갱신하고, 새 좌표가 `visited`에 있으면 `revisit++`, 없으면 집합에 추가한다.
- `visited.size()`가 서로 다른 칸 수, `revisit`이 재방문 횟수.

(3) 스스로 다시 짤 때 생각 순서

- 좌표를 키로 쓰려면 "비교 가능(`set`용)" 또는 "해시 가능(`unordered_set`용)"이어야 함을 먼저 떠올린다.
- **C++ 함정**: `unordered_set<pair<int,int>>`는 `std::hash<pair<...>>`가 표준에 없어 컴파일되지 않는다. 해법은 세 가지 — (a) `set<pair<int,int>>`를 쓴다, (b) `x * 4000LL + y`처럼 좌표를 하나의 `long long`으로 접어 `unordered_set<long long>`에 넣는다(음수 좌표는 오프셋을 더한다), (c) 해시 구조체를 직접 써서 템플릿 인자로 넘긴다.
- 출발 칸을 방문 집합에 넣을지 말지 문제 문장("출발 칸 포함")으로 확정한다.
- 갱신 순서(이동 → 확인 → 추가)를 정하고, `RLRL`처럼 같은 두 칸을 오가는 경계로 재방문 셈을 검산한다.
```

**5) 반납되지 않은 책** · Medium

- **요구사항**: 도서관의 대여 기록(책 제목 나열)과 반납 기록이 주어진다. 같은 제목의 책이 여러 권 있을 수 있다. 반납되지 않은 책을 `제목 권수` 형식으로 사전순으로 한 줄씩 출력하라. 전부 반납됐으면 `ALL RETURNED`. 반납 기록은 항상 대여 기록의 일부다(대여한 책만 반납된다).
- **입력**: 첫 줄에 `n m`(1 ≤ n ≤ 500, 0 ≤ m ≤ n), 둘째 줄에 대여된 제목 `n`개, 셋째 줄에 반납된 제목 `m`개(소문자 문자열, m=0이면 셋째 줄 없음).
- **출력**: 미반납 책마다 한 줄 `제목 권수`(사전순), 또는 `ALL RETURNED`.
- **예제**: `5 3 / dune dune emma hamlet dune / dune hamlet dune` → `dune 1 / emma 1` · `2 2 / odyssey iliad / iliad odyssey` → `ALL RETURNED`
- **셀프체크**: 제목을 `set`에 넣어 "대여에 있고 반납에 없는 것"만 찾으면 `dune`처럼 3권 대여·2권 반납인 경우를 놓친다 — 권수까지 세야 하므로 빈도표가 필요하다. 대여에서 `+1`, 반납에서 `-1`을 한 뒤 **0이 된 항목이 `map`에 그대로 남아 있다**는 점을 확인하라(파이썬 `Counter` 뺄셈처럼 자동으로 사라지지 않는다). m=0이면 대여 목록 전체가 답이다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    map<string, int> left;            // 제목 -> (대여 수 - 반납 수)
    for (int i = 0; i < n; i++) { string t; cin >> t; left[t]++; }
    for (int i = 0; i < m; i++) { string t; cin >> t; left[t]--; }

    bool any = false;
    for (const auto &kv : left) {
        if (kv.second > 0) {          // 0 이 된 항목은 지워지지 않으므로 직접 거른다
            cout << kv.first << ' ' << kv.second << "\n";
            any = true;
        }
    }
    if (!any) cout << "ALL RETURNED" << "\n";
    return 0;
}
@@TESTS
--IN
5 3
dune dune emma hamlet dune
dune hamlet dune
--OUT
dune 1
emma 1
--IN
2 2
odyssey iliad
iliad odyssey
--OUT
ALL RETURNED
--IN
3 0
x y x
--OUT
x 2
y 1
@@EXPL
(1) 접근·핵심 아이디어

- "명단 A에서 명단 B를 빼되 개수까지 고려"하는 문제다. 제목만 보면 집합 차집합 같지만 같은 제목이 여러 권이라 개수를 세야 하므로 빈도표 하나에 대여는 `+1`, 반납은 `-1`을 누적한다.
- 결과가 양수인 제목이 곧 미반납 목록이다. 출력이 사전순이므로 `map`을 써서 순회 순서를 공짜로 얻는다. 전체 O((n + m) log n).

(2) 코드 단계별

- `n`, `m`을 읽는다(m=0이면 반납 루프가 한 번도 돌지 않는다 — 셋째 줄이 없어도 문제없다).
- 대여 제목마다 `left[t]++`, 반납 제목마다 `left[t]--`.
- `map`을 순회하며 값이 0보다 큰 항목만 `제목 권수`로 출력한다.
- 하나도 출력하지 않았으면 `ALL RETURNED`.

(3) 스스로 다시 짤 때 생각 순서

- "빠진 것 찾기"에서 같은 이름이 여러 개 가능하면 집합이 아니라 빈도표임을 먼저 판단한다.
- **C++ 함정**: 파이썬 `Counter`의 뺄셈은 0 이하 항목을 자동으로 버리지만, C++ `map`은 값이 0이 되어도 **키가 남는다**. `left.empty()`로 "전부 반납"을 판정하면 예제 2에서 틀린다 — 반드시 값이 양수인지 직접 검사해야 한다.
- `left[t]--`가 없는 키에 대해서도 동작한다는 점(0을 만든 뒤 -1)도 기억해 둔다. 여기서는 "반납은 대여의 일부"라는 조건 덕에 음수가 나오지 않는다.
- 반납이 하나도 없는 경우(m=0)와 전부 반납된 경우, 두 경계를 모두 검산한다.
```

**6) 명령 패턴과 단어 열의 일대일 대응** · Medium

- **요구사항**: 패턴 문자열(소문자)과 단어 열이 주어진다. 패턴의 각 글자가 단어 하나에 **일대일**로 대응하면(같은 글자는 항상 같은 단어, 다른 글자는 항상 다른 단어) `YES`, 아니면 `NO`를 출력하라. 패턴 길이와 단어 수가 다르면 `NO`. 질의가 여러 개 주어진다.
- **입력**: 첫 줄에 질의 수 `q`(1 ≤ q ≤ 100), 이후 `q`줄에 `패턴 단어1 단어2 ...`(패턴 길이 1~50, 단어는 소문자 문자열).
- **출력**: 질의마다 한 줄에 `YES` 또는 `NO`.
- **예제**: `3 / abba dog cat cat dog / abba dog cat cat fish / aaa go go go` → `YES / NO / YES`
- **셀프체크**: 글자→단어 `map` 하나만 쓰면 `ab`와 `go go`(다른 글자가 같은 단어)를 `YES`로 잘못 판정한다 — 단어→글자 `map`도 함께 검사해야 일대일이 된다. 길이가 다른 경우를 맨 앞에서 걸러라. 두 `map` 모두 "없으면 등록, 있으면 일치 확인" 규칙이며, 이때 `find()`로 확인해야지 `[]`로 읽으면 없는 키가 생겨 버린다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    string rest;
    getline(cin, rest);               // 첫 줄에 남은 개행 소비

    for (int t = 0; t < q; t++) {
        string line;
        getline(cin, line);
        istringstream iss(line);
        string pattern, w;
        iss >> pattern;
        vector<string> words;
        while (iss >> w) words.push_back(w);

        if (pattern.size() != words.size()) {   // 길이 불일치는 즉시 NO
            cout << "NO" << "\n";
            continue;
        }
        map<char, string> p2w;
        map<string, char> w2p;
        bool ok = true;
        for (size_t j = 0; j < pattern.size(); j++) {
            char ch = pattern[j];
            const string &word = words[j];
            auto it1 = p2w.find(ch);
            if (it1 != p2w.end() && it1->second != word) { ok = false; break; }
            auto it2 = w2p.find(word);
            if (it2 != w2p.end() && it2->second != ch) { ok = false; break; }
            p2w[ch] = word;
            w2p[word] = ch;
        }
        cout << (ok ? "YES" : "NO") << "\n";
    }
    return 0;
}
@@TESTS
--IN
3
abba dog cat cat dog
abba dog cat cat fish
aaa go go go
--OUT
YES
NO
YES
--IN
2
ab go go
abc x y
--OUT
NO
NO
@@EXPL
(1) 접근·핵심 아이디어

- "같은 글자는 같은 단어"는 글자→단어 매핑으로 검사할 수 있다. 그런데 "다른 글자는 다른 단어"까지 보장하려면 반대 방향 단어→글자 매핑도 필요하다. 두 `map`을 동시에 유지하면 일대일(전단사) 대응이 된다.
- 각 위치에서 두 `map`을 조회·등록하는 비용이 O(log n)이므로 질의 하나당 O(패턴 길이 · log). `unordered_map`으로 바꾸면 평균 O(1)이다(출력 순서와 무관하므로 어느 쪽이든 된다).

(2) 코드 단계별

- `q`를 `cin >>`로 읽은 뒤 `getline`으로 **남은 개행을 반드시 버린다**. 이 한 줄을 빼면 첫 질의가 빈 문자열이 되어 전부 어긋난다.
- 줄 하나를 `getline`으로 읽어 `istringstream`에 넣고, 첫 토큰을 패턴, 나머지를 단어 목록으로 나눈다.
- `pattern.size() != words.size()`면 즉시 `NO`. 두 값 모두 `size_t`(부호 없음)라 안심하고 비교할 수 있다.
- 위치 j마다: 글자가 이미 등록돼 있는데 단어가 다르면 실패, 단어가 이미 등록돼 있는데 글자가 다르면 실패. 둘 다 통과하면 양쪽에 등록.

(3) 스스로 다시 짤 때 생각 순서

- "대응"이 한 방향인지 양방향인지 문장에서 확인한다 — 일대일이면 `map` 두 개.
- **C++ 함정**: 확인할 때 `if (p2w[ch] != word)`라고 쓰면 없는 글자에 대해 **빈 문자열 항목이 새로 생기고** 조건도 참이 되어 오답이다. 반드시 `find()`로 존재를 먼저 확인한다.
- `cin >>`와 `getline`을 섞을 때는 개행 처리를 먼저 정한다.
- `ab go go`(단어 같음, 글자 다름)와 `abba ... fish`(글자 같음, 단어 다름) 두 종류의 반례로 양쪽 검사가 모두 필요함을 검산한다.
```

**7) 합이 K인 카드 쌍의 개수** · Medium

- **요구사항**: 정수가 적힌 카드 `n`장이 있다. 서로 다른 두 장(위치가 다르면 값이 같아도 다른 카드)을 골라 합이 `K`가 되는 쌍의 개수를 구하라. 같은 값의 카드가 여러 장이면 각각 별개의 쌍으로 센다. 이중 반복 없이 평균 O(n)에 해결하라.
- **입력**: 첫 줄에 `n K`(1 ≤ n ≤ 2000, -10^6 ≤ K ≤ 10^6), 둘째 줄에 카드 값 `n`개(-10^6 이상 10^6 이하 정수).
- **출력**: 쌍의 개수(정수).
- **예제**: `6 8 / 4 4 4 3 5 1` → `4` · `3 10 / 1 2 3` → `0`
- **셀프체크**: 존재 여부(YES/NO)가 아니라 개수이므로 집합이 아니라 "값 → 지금까지 나온 횟수" 맵이 필요하다. 카드 `x`를 볼 때 `K - x`가 **이미 나온 횟수**를 더한 뒤 `x`를 등록하는 순서가 자기 자신과 짝짓기(예: K=8에서 4 한 장을 4+4로 세는 오류)를 막는다. 4가 세 장이면 4+4 쌍은 3개(첫째-둘째, 첫째-셋째, 둘째-셋째)임을 손으로 확인하라.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long K;
    cin >> n >> K;
    unordered_map<long long, int> seen;   // 값 -> 지금까지 등장 횟수
    long long pairs = 0;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        auto it = seen.find(K - x);       // [] 대신 find: 없는 키를 만들지 않는다
        if (it != seen.end()) pairs += it->second;
        seen[x]++;                        // 조회 뒤에 등록
    }
    cout << pairs << "\n";
    return 0;
}
@@TESTS
--IN
6 8
4 4 4 3 5 1
--OUT
4
--IN
3 10
1 2 3
--OUT
0
--IN
4 0
0 0 0 0
--OUT
6
--IN
4 0
-2 2 -2 2
--OUT
4
@@EXPL
(1) 접근·핵심 아이디어

- 카드 `x`의 짝은 `K - x`로 유일하게 정해진다. 앞에서부터 훑으며 "지금까지 `K - x`가 몇 번 나왔는가"를 더하면, 각 쌍은 뒤쪽 카드를 볼 때 정확히 한 번씩 세어진다(중복·누락 없음).
- 횟수를 O(1)에 조회하려면 값 → 등장 횟수 `unordered_map`을 유지한다. 전체 평균 O(n). 이중 반복은 O(n^2).

(2) 코드 단계별

- `n`, `K`를 읽고 카드를 하나씩 처리한다.
- `seen.find(K - x)`로 짝의 등장 횟수를 조회해 `pairs`에 더한 **뒤** `seen[x]++`로 자기 자신을 등록한다.
- 끝나면 `pairs` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "합이 K인 쌍" → 짝이 `K - x`로 결정된다는 사실을 먼저 적는다.
- 존재 여부면 `unordered_set`, 개수면 `unordered_map`(빈도)로 자료구조를 고른다.
- **C++ 함정 1**: 조회를 `pairs += seen[K - x];`로 쓰면 답은 맞지만 없는 키가 값 0으로 **매번 새로 생성**되어 맵이 최대 두 배로 부풀고 느려진다. 파이썬 `d.get(k, 0)`에 해당하는 것은 `[]`가 아니라 `find()`(또는 `count(k) ? m[k] : 0`)다.
- **C++ 함정 2**: n=2000이면 쌍의 개수는 최대 C(2000,2) ≈ 2×10^6이라 `int`로도 되지만, 같은 뼈대를 n이 큰 문제에 재사용하면 곧 넘친다. 개수를 세는 변수는 습관적으로 `long long`으로 둔다. 또 `K - x`는 두 값이 모두 `int`면 `int`로 계산된 뒤에야 넓혀지므로, 범위가 큰 문제에서는 `x`와 `K`를 애초에 `long long`으로 받는다.
- "조회 → 등록" 순서로 자기 자신 짝짓기를 막고, 전부 0인 배열(C(4,2)=6)과 음수 포함 배열로 검산한다.
```

**8) 서로 접두어가 되는 상품 코드** · Medium

- **요구사항**: 서로 다른 상품 코드 `n`개가 있다. 어떤 코드가 다른 코드의 **접두어**이면 바코드 판독기가 혼동하므로 "충돌 코드"라 부른다(예: `12`는 `123`의 접두어). 충돌 코드(다른 코드의 접두어가 되는 코드)를 사전순으로 한 줄에 공백으로 구분해 출력하라. 없으면 `OK`.
- **입력**: 첫 줄에 `n`(1 ≤ n ≤ 500), 이후 `n`줄에 코드 하나씩(숫자·소문자로 된 길이 1~20 문자열, 모두 서로 다름).
- **출력**: 충돌 코드들(사전순, 공백 구분) 또는 `OK`.
- **예제**: `4 / 12 / 123 / 45 / 4567` → `12 45` · `3 / ab / cd / ef` → `OK`
- **셀프체크**: 모든 쌍을 비교하면 O(n^2·길이)지만, 코드 전체를 `unordered_set<string>`에 넣고 각 코드의 접두어(길이 1 ~ 길이-1)를 하나씩 조회하면 O(n·길이^2)로 줄어듦을 확인하라. 자기 자신은 접두어로 세지 않도록 `substr` 길이 상한을 `code.size()` 미만으로 둔다. `a / ab / abc`처럼 사슬이면 `a`, `ab` 둘 다 충돌이다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<string> codes(n);
    unordered_set<string> table;      // 조회용: 평균 O(1)
    for (int i = 0; i < n; i++) {
        cin >> codes[i];
        table.insert(codes[i]);
    }

    set<string> bad;                  // set: 중복 제거 + 사전순 정렬
    for (const string &code : codes) {
        for (size_t L = 1; L < code.size(); L++) {   // 자기 자신(L == size)은 제외
            string pre = code.substr(0, L);
            if (table.count(pre)) bad.insert(pre);
        }
    }

    if (bad.empty()) {
        cout << "OK" << "\n";
        return 0;
    }
    bool first = true;
    for (const string &s : bad) {
        if (!first) cout << ' ';
        cout << s;
        first = false;
    }
    cout << "\n";
    return 0;
}
@@TESTS
--IN
4
12
123
45
4567
--OUT
12 45
--IN
3
ab
cd
ef
--OUT
OK
--IN
3
a
ab
abc
--OUT
a ab
--IN
1
a
--OUT
OK
@@EXPL
(1) 접근·핵심 아이디어

- "어떤 코드가 다른 코드의 접두어인가"를 뒤집어 "각 코드의 접두어 중에 실제 코드가 있는가"로 묻는다. 접두어는 길이별로 최대 19개뿐이므로, 코드 전체를 `unordered_set<string>`에 넣어 두면 각 접두어 조회가 평균 O(길이)다.
- 접두어로 발견된 코드를 `set<string>`에 모으면 중복 없이 한 번씩만 기록되고 순회 순서가 사전순이라 그대로 출력하면 된다.

(2) 코드 단계별

- 코드 `n`개를 읽어 `vector`(순회용)와 `unordered_set`(조회용) 둘 다 만든다.
- 각 코드에 대해 길이 1부터 `code.size() - 1`까지의 접두어 `code.substr(0, L)`을 만들어 `table`에 있는지 확인한다.
- 있으면 그 접두어(= 충돌하는 다른 코드)를 `bad`에 추가한다.
- `bad`가 비면 `OK`, 아니면 공백으로 이어 출력한다.

(3) 스스로 다시 짤 때 생각 순서

- 쌍 비교(O(n^2))를 "짧은 쪽 후보를 직접 생성해 조회"로 바꿀 수 있는지 먼저 본다 — 접두어는 후보 수가 작다.
- **C++ 함정**: `code.size()`는 `size_t`(부호 없는 정수)다. `for (int L = 1; L < code.size(); L++)`처럼 `int`와 비교하면 컴파일 경고가 나고, 더 위험하게는 `for (size_t L = code.size() - 1; L >= 0; L--)` 같은 역순 루프가 **절대 끝나지 않는다**(부호 없는 값은 0에서 1을 빼면 거대한 수가 된다). 여기서는 `size_t L`로 정순만 쓴다.
- 자기 자신을 제외하려면 접두어 길이의 상한을 `code.size()` 미만으로 둔다.
- 사슬(`a`, `ab`, `abc`)과 코드 하나뿐인 경우로 검산한다.
```

**9) 단어장 명령 처리** · Medium

- **요구사항**: 단어장에 대한 명령 `q`개를 순서대로 처리하라. `add 단어 뜻`(이미 있으면 뜻을 덮어씀), `del 단어`(없으면 무시), `find 단어`(뜻 출력, 없으면 `?`), `count`(현재 단어 수 출력). `find`와 `count`만 출력을 낸다.
- **입력**: 첫 줄에 `q`(1 ≤ q ≤ 1000), 이후 `q`줄에 명령 하나씩(단어·뜻은 공백 없는 문자열).
- **출력**: `find`·`count` 명령마다 한 줄.
- **예제**: `6 / add sol sun / find sol / add sol sunlight / find sol / del sol / find sol` → `sun / sunlight / ?` · `5 / add a 1 / add b 2 / count / del c / count` → `2 / 2`
- **셀프체크**: 없는 단어를 `book[word]`로 읽으면 **빈 문자열이 반환되면서 그 키가 새로 생긴다** — 파이썬의 `KeyError`처럼 알려 주지 않으므로 `count`가 조용히 늘어난다. `find`에는 `find()`를, `del`에는 `erase()`(없는 키를 지워도 안전하다)를 쓴다. 같은 단어를 `add`하면 개수는 늘지 않고 뜻만 바뀐다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    unordered_map<string, string> book;
    for (int i = 0; i < q; i++) {
        string cmd;
        cin >> cmd;
        if (cmd == "add") {
            string w, meaning;
            cin >> w >> meaning;
            book[w] = meaning;        // 이미 있으면 값만 덮어쓴다
        } else if (cmd == "del") {
            string w;
            cin >> w;
            book.erase(w);            // 없는 키를 지워도 아무 일도 일어나지 않는다
        } else if (cmd == "find") {
            string w;
            cin >> w;
            auto it = book.find(w);   // [] 로 읽으면 없는 키가 생겨 count 가 틀어진다
            cout << (it == book.end() ? string("?") : it->second) << "\n";
        } else {                      // count
            cout << book.size() << "\n";
        }
    }
    return 0;
}
@@TESTS
--IN
6
add sol sun
find sol
add sol sunlight
find sol
del sol
find sol
--OUT
sun
sunlight
?
--IN
5
add a 1
add b 2
count
del c
count
--OUT
2
2
--IN
1
count
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 단어 → 뜻 매핑이므로 `unordered_map<string,string>`이 정답이다. 삽입(`m[k] = v`), 삭제(`m.erase(k)`), 조회(`m.find(k)`), 크기(`m.size()`) 모두 평균 O(1)이라 명령 수만큼 O(q)에 끝난다.
- 출력 순서가 명령 순서로 이미 정해져 있으므로 `map`의 정렬이 필요 없다 — `unordered_map`이 더 빠르다.

(2) 코드 단계별

- 명령 이름을 `cin >>`로 읽고, 명령마다 필요한 토큰 수만큼 더 읽는다(`add`는 2개, `del`·`find`는 1개, `count`는 0개).
- `add`: `book[w] = meaning` — 기존 키면 값만 덮어써서 개수가 늘지 않는다.
- `del`: `book.erase(w)` — 없는 키여도 안전하다(지워진 개수 0을 반환할 뿐).
- `find`: `book.find(w)`가 `end()`면 `?`, 아니면 `it->second`. `count`: `book.size()`.

(3) 스스로 다시 짤 때 생각 순서

- 명령별로 맵의 어떤 연산에 대응하는지 표로 적는다(add→대입, del→erase, find→find, count→size).
- **C++ 함정(이 문제의 핵심)**: `cout << book[w]`는 없는 단어에 대해 빈 문자열을 출력하면서 **그 키를 값 빈 문자열로 삽입한다**. 그러면 뒤따르는 `count`가 1 커진다. 파이썬은 `KeyError`로 즉시 알려 주지만 C++은 조용히 틀린 답을 낸다 — 읽기 전용 조회에는 항상 `find()`나 `count()`를 쓴다. `const unordered_map`에 `[]`가 아예 없는 것도 같은 이유다(`at()`은 없으면 예외를 던진다).
- 같은 단어를 두 번 `add`한 뒤 `count`가 1인지, 명령이 `count` 하나뿐일 때 0인지 검산한다.
```

**10) 가장 긴 연속 정수 구간** · Hard

- **요구사항**: 정수 `n`개(중복 가능)가 주어진다. 값들 중에서 `x, x+1, ..., x+L-1`이 모두 존재하는 가장 긴 구간의 길이 `L`과 시작값 `x`를 출력하라. 길이가 같은 구간이 여러 개면 시작값이 가장 작은 것. 정렬 없이 `unordered_set`만으로 평균 O(n)에 해결하라.
- **입력**: 첫 줄에 `n`(1 ≤ n ≤ 2000), 둘째 줄에 정수 `n`개(-10^9 이상 10^9 이하).
- **출력**: `길이 시작값`.
- **예제**: `8 / 100 4 200 1 3 2 101 102` → `4 1` · `5 / 7 7 7 7 7` → `1 7`
- **셀프체크**: 모든 원소에서 오른쪽으로 뻗어 나가면 같은 구간을 여러 번 훑어 O(n^2)가 된다 — `x - 1`이 집합에 없는 원소(구간의 시작점)에서만 뻗어야 각 원소가 총 O(1)번만 방문된다. 중복 값은 `unordered_set`이 지우므로 길이 계산에 영향이 없다. `unordered_set`의 순회 순서는 보장되지 않으므로 동점 처리(시작값 최소)를 비교문에 반드시 넣어야 답이 결정적으로 나온다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    unordered_set<long long> nums;
    for (int i = 0; i < n; i++) { long long x; cin >> x; nums.insert(x); }

    long long bestLen = 0, bestStart = 0;
    for (long long x : nums) {
        if (nums.count(x - 1)) continue;      // 구간의 시작점에서만 뻗는다
        long long len = 1;
        while (nums.count(x + len)) len++;
        if (len > bestLen || (len == bestLen && x < bestStart)) {
            bestLen = len;
            bestStart = x;
        }
    }
    cout << bestLen << ' ' << bestStart << "\n";
    return 0;
}
@@TESTS
--IN
8
100 4 200 1 3 2 101 102
--OUT
4 1
--IN
5
7 7 7 7 7
--OUT
1 7
--IN
6
10 11 3 4 20 21
--OUT
2 3
--IN
1
-5
--OUT
1 -5
@@EXPL
(1) 접근·핵심 아이디어

- 정렬하면 O(n log n)이지만, `unordered_set`에 넣으면 "x+1이 있는가"를 평균 O(1)에 물을 수 있어 정렬 없이 구간을 이어 갈 수 있다.
- 핵심 최적화: `x - 1`이 집합에 있으면 `x`는 구간의 중간이므로 건너뛴다. 시작점에서만 오른쪽으로 뻗으면 각 원소는 구간당 한 번씩만 방문되어 전체 평균 O(n)이다.
- 동점 규칙은 `(길이가 더 길거나) 또는 (같고 시작값이 더 작으면)` 갱신으로 처리한다.

(2) 코드 단계별

- 입력을 `unordered_set<long long>`으로 만든다(중복 제거).
- 각 `x`에 대해 `nums.count(x - 1)`이 1이면 `continue`(시작점 아님).
- 시작점이면 `x + len`이 있는 동안 `len`을 늘린다.
- 더 길거나, 같은 길이인데 시작값이 작으면 최적을 갱신하고, 마지막에 `길이 시작값` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "연속된 정수"라는 구조에서 이웃 조회(`x+1`)를 해시 집합으로 평균 O(1)에 할 수 있음을 떠올린다.
- 왜 시작점에서만 뻗어야 O(n)인지(각 원소가 딱 한 구간에 속함) 스스로 설명한다.
- **C++ 함정 1**: 값이 최대 10^9이고 `x + len`을 계산한다. `int`로 두면 10^9 + 2000은 아직 `int` 범위 안이지만 여유가 거의 없다 — 값 범위가 10^9급이면 `long long`으로 받아 두는 편이 안전하다.
- **C++ 함정 2**: `unordered_set`의 순회 순서는 구현 정의라 실행마다 달라질 수 있다. 동점 비교 `(len == bestLen && x < bestStart)`가 없으면 "먼저 만난 것"이 답이 되어 결과가 불안정해진다. 순회 순서에 의존하지 않는 갱신 규칙을 반드시 쓴다.
- 전부 같은 값(길이 1), 길이가 같은 구간이 여러 개, 원소 하나뿐인 경우로 검산한다.
```

**11) 합이 K인 연속 구간의 개수** · Hard

- **요구사항**: 정수 배열에서 원소 합이 정확히 `K`인 연속 부분 배열(길이 1 이상)의 개수를 구하라. 음수가 포함될 수 있으므로 투 포인터는 쓸 수 없고, 누적합과 해시 맵으로 O(n)에 해결하라.
- **입력**: 첫 줄에 `n K`(1 ≤ n ≤ 2000, -10^6 ≤ K ≤ 10^6), 둘째 줄에 정수 `n`개(-1000 이상 1000 이하).
- **출력**: 구간의 개수(정수).
- **예제**: `5 3 / 1 2 1 2 1` → `4` · `4 0 / 0 0 0 0` → `10`
- **셀프체크**: 구간 `[i+1, j]`의 합은 `prefix[j] - prefix[i]`이므로, `prefix[j]`를 볼 때 "`prefix[j] - K`가 이전에 몇 번 나왔는가"를 세면 된다 — 문제 7과 같은 뼈대임을 확인하라. 빈 접두사(합 0)를 `freq[0] = 1`로 미리 넣지 않으면 배열 맨 앞에서 시작하는 구간을 놓친다. 전부 0이고 K=0이면 모든 구간 n(n+1)/2개가 답이다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long K;
    cin >> n >> K;
    unordered_map<long long, int> freq;
    freq[0] = 1;                      // 아무것도 안 더한 누적합 0 이 한 번 있다
    long long prefix = 0, count = 0;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        prefix += x;
        auto it = freq.find(prefix - K);
        if (it != freq.end()) count += it->second;   // 조회 먼저
        freq[prefix]++;                              // 등록은 그 다음
    }
    cout << count << "\n";
    return 0;
}
@@TESTS
--IN
5 3
1 2 1 2 1
--OUT
4
--IN
4 0
0 0 0 0
--OUT
10
--IN
6 2
3 -1 2 -2 2 0
--OUT
7
--IN
3 100
1 2 3
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 누적합 `prefix[j]`를 두면 구간 합은 두 누적합의 차다. 따라서 "합이 K인 구간"은 "차가 K인 누적합 쌍"과 같고, 이는 문제 7(합이 K인 쌍)과 똑같이 해시 맵 빈도로 센다: 현재 누적합 `p`에서 이전에 나온 `p - K`의 횟수를 더한다.
- 음수가 있어도 누적합의 차라는 관점은 변하지 않으므로 그대로 성립한다. 전체 평균 O(n).

(2) 코드 단계별

- `freq[0] = 1`로 시작 — 아무 원소도 안 더한 누적합 0이 한 번 있다는 뜻(맨 앞에서 시작하는 구간용).
- 원소를 하나씩 더해 `prefix`를 갱신하고, `freq.find(prefix - K)`로 이전 등장 횟수를 `count`에 더한다.
- 그 다음 `freq[prefix]++`로 현재 누적합을 등록한다(조회 → 등록 순서).
- 끝나면 `count` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "연속 구간의 합"을 보면 누적합으로 바꿔 "두 값의 차"로 만든다.
- 차가 K인 쌍 세기는 이미 아는 패턴(해시 빈도)임을 연결한다.
- **C++ 함정**: 누적합과 답을 `long long`으로 둔다. 여기서는 n=2000, 값 ≤1000이라 누적합이 ±2×10^6, 개수도 최대 약 2×10^6이라 `int`로도 되지만, 같은 뼈대를 n이 10^5인 문제에 쓰면 개수가 곧 5×10^9이 되어 `int`를 넘는다. 누적합·개수는 습관적으로 `long long`.
- `freq[0] = 1` 초기화를 빼먹으면 어떤 구간을 놓치는지(첫 원소부터 시작하는 구간) 예제 `1 2 1 2 1`로 확인하고, 전부 0 케이스(10개)로 검산한다.
```

**12) 장르별 인기곡 플레이리스트** · Hard

- **요구사항**: 곡 `n`개에 대해 장르와 재생 수가 주어진다(고유 번호는 입력 순서대로 0부터). 다음 규칙으로 플레이리스트를 만들어 고유 번호를 순서대로 출력하라. (a) 장르별 총 재생 수가 큰 장르부터(동점이면 장르 이름 사전순), (b) 각 장르 안에서는 재생 수가 큰 곡부터 최대 2곡(동점이면 고유 번호가 작은 곡 먼저).
- **입력**: 첫 줄에 `n`(1 ≤ n ≤ 200), 이후 `n`줄에 `장르 재생수`(장르는 소문자 문자열, 재생수는 0 이상 10^6 이하 정수).
- **출력**: 선택된 곡의 고유 번호를 공백으로 구분해 한 줄에.
- **예제**: `5 / pop 500 / rock 600 / pop 150 / rock 800 / jazz 2500` → `4 3 1 0 2` · `4 / a 10 / b 10 / a 5 / b 5` → `0 2 1 3`
- **셀프체크**: 장르 → 곡 목록은 `map<string, vector<pair<int,int>>>`, 장르 → 총합은 `map<string, long long>`으로 두 표를 한 번의 순회에서 함께 채우는지 확인하라. C++에는 정렬 키 함수가 없으므로 **비교 함수**로 "총합 내림차순, 이름 오름차순"을 직접 쓴다. 곡이 하나뿐인 장르는 1곡만 나온다 — 자를 개수를 `v.size() < 2 ? v.size() : 2`로 정한다(`min(2, v.size())`는 `int`와 `size_t`가 섞여 컴파일되지 않는다).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    map<string, vector<pair<int, int>>> songs;   // 장르 -> (재생수, 번호) 목록
    map<string, long long> total;                // 장르 -> 총 재생수

    for (int i = 0; i < n; i++) {
        string g;
        int plays;
        cin >> g >> plays;
        songs[g].push_back(make_pair(plays, i)); // 없는 키면 빈 vector 가 자동 생성
        total[g] += plays;                       // 없는 키면 0 에서 시작
    }

    vector<string> order;
    for (const auto &kv : total) order.push_back(kv.first);
    sort(order.begin(), order.end(),
         [&](const string &p, const string &q) {
             if (total[p] != total[q]) return total[p] > total[q];  // 총합 큰 순
             return p < q;                                          // 동점이면 이름 사전순
         });

    vector<int> result;
    for (const string &g : order) {
        vector<pair<int, int>> &v = songs[g];
        sort(v.begin(), v.end(),
             [](const pair<int, int> &p, const pair<int, int> &q) {
                 if (p.first != q.first) return p.first > q.first;  // 재생수 큰 순
                 return p.second < q.second;                        // 동점이면 번호 작은 순
             });
        size_t take = v.size() < 2 ? v.size() : 2;
        for (size_t i = 0; i < take; i++) result.push_back(v[i].second);
    }

    for (size_t i = 0; i < result.size(); i++) {
        if (i) cout << ' ';
        cout << result[i];
    }
    cout << "\n";
    return 0;
}
@@TESTS
--IN
5
pop 500
rock 600
pop 150
rock 800
jazz 2500
--OUT
4 3 1 0 2
--IN
4
a 10
b 10
a 5
b 5
--OUT
0 2 1 3
--IN
1
k 7
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 두 단계 정렬 문제다: 장르를 총 재생 수로 줄 세우고, 장르 안에서 곡을 재생 수로 줄 세운다. 이를 위해 "장르 → 그 장르의 곡들"(그룹화)과 "장르 → 총합"(누적) 두 해시/정렬 표가 필요하다.
- 그룹화는 C++ `map`의 `[]`가 그대로 해준다 — 없는 장르에 `songs[g].push_back(...)`을 하면 빈 `vector`가 자동으로 만들어져 삽입된다. 파이썬 `defaultdict(list)`에 해당하는 동작이 기본 제공이다.
- 동점 규칙은 파이썬의 키 튜플 대신 **비교 함수(람다)**로 쓴다. "큰 것 먼저"는 `>`, "사전순"은 `<`로 각각 표현한다.

(2) 코드 단계별

- 곡을 읽으며 `songs[g]`에 `(재생수, 번호)`를 추가하고 `total[g]`에 재생 수를 누적한다.
- 장르 이름을 `vector`에 뽑아 `(총합 내림차순, 이름 오름차순)` 비교 함수로 `sort`한다.
- 각 장르의 곡을 `(재생수 내림차순, 번호 오름차순)`으로 `sort`한 뒤 앞 2개(모자라면 있는 만큼)만 결과에 추가한다.
- 번호들을 공백으로 이어 출력.

(3) 스스로 다시 짤 때 생각 순서

- "장르별로 묶어서" → `map<string, vector<...>>`, "총합 큰 순" → 별도 합계 맵을 같은 순회에서 함께 채운다.
- 정렬 규칙을 문장에서 비교 함수로 번역한다. **비교 함수는 "엄격한 약한 순서"여야 한다** — 동점일 때 `true`를 반환하면(`return total[p] >= total[q];` 같은 실수) `sort`가 정의되지 않은 동작에 빠져 실행 중 죽을 수 있다. 그래서 "다를 때만 1차 기준으로 판정, 같으면 2차 기준"이라는 형태로 쓴다.
- **C++ 함정**: `sort`는 파이썬 `sorted`와 달리 **안정 정렬이 아니다**. 동점 순서를 값에 기대면 안 되고, 이 문제처럼 2차 기준(번호)을 비교 함수에 명시해야 한다(안정성이 꼭 필요하면 `stable_sort`).
- 총합은 `long long`으로 둔다. 재생수 10^6 × 곡 200 = 2×10^8이라 `int`로도 되지만, 곡 수가 늘면 곧 넘치는 자리다.
- 총합 동점 장르, 재생 수 동점 곡, 곡 하나뿐인 장르 세 경계를 각각 검산한다.
```
