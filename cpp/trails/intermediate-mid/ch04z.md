## L4. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터의 두 레슨은 소재가 달랐지만 던진 질문은 하나다. **"지금 이 선택을 확정해도 나중에 후회하지 않는가?"** L1은 그 답을 *정렬 기준 + 교환 논증*으로 얻었고, L2는 *애초에 선택지가 하나뿐*이라는 사실로 얻었다. 아래에서 두 갈래를 한 장으로 잇고, 바로 꺼내 쓸 뼈대와 자주 넘어지는 지점을 모은다.

**개념 지도**

```text
                          Ch04 : greedy
                                |
          +---------------------+---------------------+
          |                                           |
     SORT AND TAKE                              FORCED FLIP
     pick an order, decide once                 zero freedom left
     lesson 1                                   lesson 2
          |                                           |
   what is the sort key ?                    leftmost cell has
   exchange argument decides                 exactly one fixer
          |                                           |
   +------+------+------+------+             press or skip is
   |      |      |      |      |             forced by its value
  end   ratio  value   pair  stack           -> the run is unique
  time   v/w   desc    lo,hi  mono           -> unique => minimal
```

두 갈래의 정당성 근거가 다르다는 점이 중요하다. 왼쪽은 "바꿔치기해도 손해가 아니다"를 **증명해야** 하고, 오른쪽은 "다른 길이 없다"라서 **증명할 게 없다**. 그래서 왼쪽에서만 반례를 찾는 절차가 필요하다.

```text
   how to decide if greedy is valid

   step 1   list candidate keys
            end / start / length / ratio / value / count
   step 2   kill each key with a tiny counterexample
            (0,10) (1,2) (3,4)   kills "earliest start"
            (0,5) (4,6) (5,10)   kills "shortest length"
   step 3   for the survivor run the exchange argument
            take any OPT, swap its first pick for the greedy pick,
            show the answer never gets worse
   step 4   no key survives  ->  it is a DP problem, not a greedy one
```

3단계를 건너뛰면 어떻게 되는지는 동전 문제가 가장 짧게 보여 준다.

```text
   coins {1, 6, 10}   target 12
   greedy   10 + 1 + 1   = 3 coins
   best      6 + 6       = 2 coins        <- greedy is WRONG here

   coins {1, 5, 10, 50}  target 12        # each value divides the next
   greedy   10 + 1 + 1   = 3 coins = best <- divisibility rescues it
```

정렬 기준과 힙 방향은 이 챕터에서 언어가 개입하는 두 지점이다. 둘 다 컴파일은 되고 답만 틀리므로 미리 못 박아 둔다.

```text
   two language traps, both compile fine

   sort(v.begin(), v.end())          -> pair compares first, then second
                                        i.e. by START time , not by END

   priority_queue<int>               -> MAX heap  (top() is the largest)
   priority_queue<int, vector<int>,
                  greater<int>>      -> MIN heap  (top() is the smallest)

   comparator must be strict :   return a < b;      # OK
                                 return a <= b;     # UB, may crash
```

**뼈대 코드**

1) 정렬 후 순차 선택 — 모든 그리디의 공통 골격.

```cpp
sort(items.begin(), items.end(), cmp);   // ← 문제마다 바뀜: 이 한 줄이 문제의 90%
vector<Item> result;
State state = INIT;                      // ← 문제마다 바뀜: last_end / 잔여 용량 ...

for (auto& x : items) {                  // 참조로 받아 복사 비용을 없앤다
    if (feasible(state, x)) {            // 지금 확정해도 규칙을 안 깨는가
        result.push_back(x);
        state = update(state, x);        // 확정, 되돌아보지 않음
    }
}
cout << result.size() << '\n';
```

2) 구간 스케줄링 — 겹치지 않게 **최대 개수**. 기준은 **종료 시각**.

```cpp
// mt: vector<pair<int,int>>, (시작, 종료)
sort(mt.begin(), mt.end(), [](const pair<int,int>& a, const pair<int,int>& b) {
    if (a.second != b.second) return a.second < b.second;  // 종료 오름차순
    return a.first < b.first;                              // 동점은 시작 순
});

int cnt = 0, last_end = INT_MIN;         // ← 시각이 음수일 수 있으면 INT_MIN
for (auto& [s, e] : mt) {
    if (s >= last_end) {                 // ← 맞닿음을 겹침으로 보면 >
        cnt++;
        last_end = e;
    }
}
cout << cnt << '\n';
```

3) `priority_queue` 교체형 — 마감이 있고 **넣었다가 넘치면 가장 나쁜 것을 버린다**.

```cpp
// tasks: vector<pair<int,int>>, (마감, 점수)
sort(tasks.begin(), tasks.end());                        // 마감 오름차순
priority_queue<int, vector<int>, greater<int>> chosen;   // 최소 힙(기본은 최대 힙!)

for (auto& [d, p] : tasks) {
    chosen.push(p);                                      // 일단 넣고
    if ((int)chosen.size() > d) chosen.pop();            // ← 문제마다 바뀜: 용량 조건
}
long long sum = 0;                                       // 합은 int를 쉽게 넘긴다
while (!chosen.empty()) { sum += chosen.top(); chosen.pop(); }
cout << sum << '\n';
```

4) 두 배열 짝짓기 — 정렬 후 한 방향 투 포인터.

```cpp
sort(boxes.begin(), boxes.end());
sort(goods.begin(), goods.end());
int i = 0, j = 0, cnt = 0;

while (i < (int)goods.size() && j < (int)boxes.size()) {
    if (boxes[j] >= goods[i]) {          // ← 문제마다 바뀜: 매칭 조건
        cnt++;
        i++;                             // 담았을 때만 물건을 넘긴다
    }
    j++;                                 // 상자는 성공/실패와 무관하게 소진
}
cout << cnt << '\n';
```

양끝에서 좁혀 오는 변형(무거운 사람 + 가벼운 사람 짝짓기)은 `lo`/`hi`를 양끝에 두고 `w[lo] + w[hi] <= LIMIT`이면 둘 다, 아니면 `hi`만 당기는 같은 틀이다.

5) 단조 스택 그리디 — K개를 지워 **사전순(수치) 최소** 만들기.

```cpp
string num;  int k;                      // 입력: 숫자 문자열과 지울 개수
string stk;                              // 문자 스택은 string으로 충분
for (char ch : num) {
    while (!stk.empty() && k > 0 && stk.back() > ch) {   // ← 최대를 원하면 부등호 반대
        stk.pop_back();
        k--;
    }
    stk.push_back(ch);
}
if (k > 0) stk.resize(stk.size() - k);   // 오름차순이라 한 번도 못 지운 경우

int p = 0;
while (p + 1 < (int)stk.size() && stk[p] == '0') p++;   // 선행 0 제거
string ans = stk.substr(p);
cout << (ans.empty() ? "0" : ans) << '\n';
```

6) 구간 커버 최소 개수 — `[0, L]`을 왼쪽부터 덮어 나간다.

```cpp
sort(iv.begin(), iv.end());              // 시작점 오름차순(pair 기본 비교)
int covered = 0, cnt = 0, idx = 0, m = iv.size();
bool ok = true;

while (covered < L) {
    int best = covered;
    while (idx < m && iv[idx].first <= covered) {   // 끊김 없이 이을 수 있는 것들
        best = max(best, iv[idx].second);           // 그중 가장 멀리 뻗는 것
        idx++;
    }
    if (best == covered) { ok = false; break; }     // 한 칸도 못 뻗음 = 구멍
    covered = best;
    cnt++;
}
cout << (ok ? cnt : -1) << '\n';
```

**언제 무엇을 쓰나**

먼저 "이 문제가 그리디인가"를 절차로 판정한다. 순서를 지키면 감으로 찍는 일이 없어진다.

| 단계 | 하는 일 | 통과 기준 | 실패하면 |
|---|---|---|---|
| 1 | 후보 정렬 기준을 3~4개 적는다 | 끝·시작·길이·비율·값 등 | 기준이 안 떠오르면 DP 의심 |
| 2 | 각 기준을 죽일 반례를 원소 3개로 만든다 | 반례가 나오면 그 기준 폐기 | 전부 죽으면 DP |
| 3 | 살아남은 기준에 교환 논증을 적용 | 첫 선택을 바꿔도 답이 안 나빠짐 | 안 되면 DP |
| 4 | 되돌아보기가 필요한지 확인 | 확정 후 취소가 없으면 그리디 | 취소가 필요하면 DP |

판정을 통과했다면 아래 표에서 도구를 고른다.

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 겹치지 않게 최대 개수 | 종료 시각 비교 람다 + 순차 선택 | 일찍 끝날수록 뒤에 남는 자리가 넓다 | O(N log N) |
| 전부 배정할 최소 자원 수 | 시작 시각 정렬 + 종료 시각 최소 힙 | 힙 크기가 곧 동시 진행 수 | O(N log N) |
| 마감이 있고 이득 최대 | 마감 정렬 + `priority_queue` 교체 | 넘칠 때 가장 낮은 것만 버리면 손해가 없다 | O(N log N) |
| 한쪽을 한 번씩만 쓰는 크기 매칭 | 양쪽 정렬 + 투 포인터 | 작은 것에 작은 것을 붙이면 자원이 남는다 | O(N log N) |
| 무게 제한 아래 2명씩 묶기 | 정렬 + 양끝 투 포인터 | 가장 무거운 쪽의 짝은 가장 가벼운 쪽이면 충분 | O(N log N) |
| K개 지워 사전순 최소·최대 | 단조 스택(`string`/`vector`) | 내림(오름) 지점의 앞자리를 지우는 게 유일한 개선 | O(N) |
| 선분 전체를 구간으로 덮기 | 시작점 정렬 + 가장 멀리 뻗기 | 더 멀리 뻗는 선택이 이후 후보를 줄이지 않는다 | O(N log N) |
| 각 칸을 바꿀 조작이 유일 | 왼→오 강제 확정 + imos(XOR) | 자유도가 0이라 해가 유일하고, 유일하면 최소 | O(N) |
| 앞쪽 한두 칸만 자유도가 남음 | 그 자유도만 완전탐색 + 강제 | 상수배 비용으로 강제성을 복구한다 | O(c·N) |

마지막으로, **그리디처럼 생겼지만 실제로는 DP**인 대표 문제들을 미리 표시해 둔다.

| 문제 | 그리디가 내는 답 | 실제 최적 | 왜 깨지는가 |
|---|---|---|---|
| 임의 액면 동전 최소 개수 `{1,6,10}`, 12 | 10+1+1 = 3개 | 6+6 = 2개 | 배수 관계가 없어 "큰 것부터"의 교환이 손해 |
| 0/1 배낭(쪼갤 수 없음) | 비율 큰 것부터 담기 | 조합을 봐야 함 | 남는 공간이 버려져 교환이 성립 안 함 |
| 계단·격자 최소 비용 경로 | 매 칸 싼 쪽으로 | 전체를 봐야 함 | 지금 싼 칸이 뒤에서 비싼 길로 이어짐 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 그리디와 DP의 차이를 "버린 선택을 다시 보는가"로 한 문장에 정리하기.
- [ ] 설명할 수 있다: 탐욕적 선택 속성과 최적 부분 구조가 각각 무엇을 보장하는지.
- [ ] 설명할 수 있다: 교환 논증의 형식(임의의 최적해 → 첫 선택 교체 → 값이 안 나빠짐 → 귀납).
- [ ] 설명할 수 있다: 구간 스케줄링에서 종료 시각이 정답 기준이고 시작 시각·길이는 왜 아닌지, 각각의 반례와 함께.
- [ ] 설명할 수 있다: 같은 구간 입력인데 "최대 개수"는 종료 정렬, "최소 자원 수"는 시작 정렬 + 힙인 이유.
- [ ] 설명할 수 있다: `priority_queue`가 기본으로 최대 힙인 이유와, 최소 힙을 만드는 세 번째 템플릿 인자의 역할.
- [ ] 설명할 수 있다: 비교자가 strict weak ordering이어야 하는 이유와, `<=`를 넣으면 무슨 일이 생기는지.
- [ ] 설명할 수 있다: 마감 있는 작업에서 "일단 넣고 넘치면 최소를 버린다"가 왜 "자리 있을 때만 넣는다"보다 강한지.
- [ ] 설명할 수 있다: 투 포인터 매칭에서 실패했을 때 어느 포인터만 전진해야 하는지와 그 근거.
- [ ] 설명할 수 있다: 단조 스택으로 사전순 최소를 만들 때 "내림 지점의 앞자리를 지운다"가 최적인 이유와, 지울 몫이 남으면 왜 뒤에서 지워야 하는지.
- [ ] 설명할 수 있다: 구간 커버에서 "가장 멀리 뻗는 것"을 고르는 그리디의 정당성과 구멍 판정 조건.
- [ ] 설명할 수 있다: 동전 문제에서 배수 조건이 그리디를 살리는 정확한 지점.
- [ ] 설명할 수 있다: 상태 반전 유형에서 "선택"이 아니라 "계산"이라는 말의 뜻과, 그래서 교환 논증이 필요 없는 이유.
- [ ] 설명할 수 있다: 왼쪽부터 강제 확정한 뒤 **마지막 몇 칸을 반드시 검증**해야 하는 이유와, 자유도가 남는 변형(원형·양끝)을 완전탐색으로 복구하는 방법.
- [ ] 설명할 수 있다: 그리디 문제의 복잡도가 대개 O(N log N)이고 그 지배항이 정렬인 이유.
- [ ] 설명할 수 있다: 누적 합·최댓값에서 `int` 대신 `long long`을 써야 하는 기준과, 최댓값 초기값을 0으로 두면 안 되는 경우.

**⚠️ 자주 하는 실수**

**1) 검증 없이 그리디를 적용한다**

```cpp
// ❌ 틀린 코드
sort(coins.rbegin(), coins.rend());      // coins = {1, 6, 10}, m = 12
int cnt = 0;
for (int c : coins) {
    cnt += m / c;
    m %= c;
}
cout << cnt << '\n';                     // 3 을 출력 (실제 최소는 2)
```

왜: "큰 것부터"가 옳으려면 큰 액면을 하나 덜 쓰고 작은 액면 여럿으로 바꿨을 때 **반드시 개수가 늘어야** 한다. 배수 관계가 없는 `{1, 6, 10}`에서는 `10`을 포기하고 `6`을 두 개 쓰는 교환이 이득이라 그 전제가 깨진다. 그리디는 문제 구조가 허락할 때만 옳고, 그 허락 여부는 반례를 만들어 확인해야 한다.

```cpp
// ✅ 고친 코드 — 반례가 나오면 DP로 내려간다
const int INF = 1e9;
vector<int> dp(m + 1, INF);
dp[0] = 0;
for (int x = 1; x <= m; x++)
    for (int c : coins)
        if (c <= x && dp[x - c] + 1 < dp[x]) dp[x] = dp[x - c] + 1;
cout << (dp[m] == INF ? -1 : dp[m]) << '\n';
```

**2) 구간 문제를 시작 시각으로 정렬한다**

```cpp
// ❌ 틀린 코드
sort(mt.begin(), mt.end());              // pair는 first부터 비교 = 시작 시각 기준
int cnt = 0, last_end = INT_MIN;
for (auto& [s, e] : mt) {
    if (s >= last_end) { cnt++; last_end = e; }
}
```

왜: `pair`의 기본 비교는 first(시작 시각) → second 순이다. `(0,10) (1,2) (3,4)`에서 시작이 가장 이른 `(0,10)`을 먼저 확정하면 나머지 둘이 통째로 막혀 답이 1이 된다. 실제 최대는 `(1,2) (3,4)` 두 개다. **긴 구간 하나가 뒤를 다 막는 것**이 시작 시각 정렬의 고정 실패 패턴이고, `sort`에 비교자를 안 넘긴 순간 조용히 그렇게 된다.

```cpp
// ✅ 고친 코드
sort(mt.begin(), mt.end(), [](const pair<int,int>& a, const pair<int,int>& b) {
    if (a.second != b.second) return a.second < b.second;   // 종료 시각 오름차순
    return a.first < b.first;
});
int cnt = 0, last_end = INT_MIN;
for (auto& [s, e] : mt) {
    if (s >= last_end) { cnt++; last_end = e; }
}
```

**3) 비교 람다에 등호를 넣는다**

```cpp
// ❌ 틀린 코드
sort(v.begin(), v.end(), [](const Item& a, const Item& b) {
    return a.end <= b.end;               // 같은 값끼리 "서로 앞선다"가 된다
});
```

왜: `sort`는 비교자가 **strict weak ordering**(같은 값이면 반드시 `false`)이라고 가정하고 최적화한다. `<=`를 쓰면 `cmp(a,a)`가 참이 되어, 내부 퀵소트가 경계 검사를 생략한 채 배열 밖을 짚는다. 결과는 "정렬이 이상하다"가 아니라 **런타임 크래시**이고, 입력이 작으면 우연히 통과해서 원인을 찾기 어렵다.

```cpp
// ✅ 고친 코드 — 반드시 <(또는 >)만, 동점은 2차 키로 가른다
sort(v.begin(), v.end(), [](const Item& a, const Item& b) {
    if (a.end != b.end) return a.end < b.end;
    return a.start < b.start;
});
```

**4) `priority_queue`가 최소 힙이라고 착각한다**

```cpp
// ❌ 틀린 코드
priority_queue<int> chosen;              // 기본은 최대 힙이다
for (auto& [d, p] : tasks) {
    chosen.push(p);
    if ((int)chosen.size() > d) chosen.pop();   // 가장 "좋은" 것을 버린다
}
```

왜: C++의 `priority_queue`는 기본 비교자가 `less`라 `top()`이 **최댓값**이다. 위 코드는 넘칠 때마다 가장 점수가 높은 작업을 버려, 답이 최솟값 쪽으로 몰린다. 컴파일도 되고 실행도 되며 작은 테스트는 통과하기도 해서 발견이 늦다.

```cpp
// ✅ 고친 코드
priority_queue<int, vector<int>, greater<int>> chosen;   // 최소 힙
for (auto& [d, p] : tasks) {
    chosen.push(p);
    if ((int)chosen.size() > d) chosen.pop();            // 가장 낮은 것을 버린다
}
```

**5) 힙 교체형에서 "자리 있을 때만" 넣는다**

```cpp
// ❌ 틀린 코드
for (auto& [d, p] : tasks) {             // 마감 오름차순
    if ((int)chosen.size() < d) chosen.push(p);   // 자리가 있을 때만 담는다
}
```

왜: 자리가 꽉 찼을 때 "지금 것이 힙 최솟값보다 나으면 바꿔치기"하는 기회를 통째로 버린다. `(1, 10) (1, 90)`이면 먼저 들어온 10만 남고 90을 놓쳐 답이 10이 된다. 이 패턴의 정확한 형태는 **일단 넣고, 넘치면 최솟값을 버린다**이다.

```cpp
// ✅ 고친 코드
for (auto& [d, p] : tasks) {
    chosen.push(p);
    if ((int)chosen.size() > d) chosen.pop();     // 지금까지 중 가장 낮은 것만 포기
}
```

**6) 투 포인터 매칭에서 실패했는데 양쪽을 다 전진시킨다**

```cpp
// ❌ 틀린 코드
while (i < m && j < n) {
    if (boxes[j] >= goods[i]) cnt++;
    i++;                                 // 못 담았는데 물건도 넘겨 버린다
    j++;
}
```

왜: 상자가 작아 못 담았다면 **버릴 것은 상자뿐**이고 물건은 다음 상자를 기다려야 한다. 둘 다 전진시키면 담을 수 있었던 조합이 사라진다. 상자 `1 5 6`, 물건 `5 6`이면 정답이 2인데 0이 나온다.

```cpp
// ✅ 고친 코드
while (i < m && j < n) {
    if (boxes[j] >= goods[i]) {
        cnt++;
        i++;                             // 담았을 때만 물건을 넘긴다
    }
    j++;                                 // 상자는 어느 쪽이든 소진
}
```

**7) 누적 합을 `int`로 받고 최댓값을 0으로 시작한다**

```cpp
// ❌ 틀린 코드
int sum = 0, best = 0;                   // N = 1e5, 값 = 1e9 이면 합이 1e14
for (int v : values) {
    sum += v;                            // int는 약 21억에서 조용히 뒤집힌다
    if (v > best) best = v;              // 전부 음수면 존재하지 않는 답 0이 남는다
}
cout << sum << ' ' << best << '\n';
```

왜: `int`는 약 ±21억이라 `10^5 × 10^9 = 10^14`를 담지 못하고 **오버플로가 예외 없이 조용히** 값을 뒤집는다. 그리디는 값을 계속 누적하는 구조라 특히 잘 걸린다. 또 `best = 0`은 "아무것도 안 고르면 0"이라는 뜻이라, 반드시 하나는 골라야 하는 문제에서 후보가 전부 음수면 틀린 0을 내놓는다.

```cpp
// ✅ 고친 코드
long long sum = 0;
long long best = LLONG_MIN;              // 또는 best = values[0] 로 시작
for (int v : values) {
    sum += v;
    if (v > best) best = v;
}
cout << sum << ' ' << best << '\n';
```

**8) 스택 그리디에서 남은 삭제 몫을 버려둔다**

```cpp
// ❌ 틀린 코드
for (char ch : num) {
    while (!stk.empty() && k > 0 && stk.back() > ch) { stk.pop_back(); k--; }
    stk.push_back(ch);
}
cout << stk << '\n';                     // num="12345", k=2 면 5자리가 그대로 나온다
```

왜: 입력이 오름차순이면 내림 지점이 없어 `pop_back`이 한 번도 일어나지 않는다. 지워야 할 `k`개가 남은 채 끝나 결과의 길이가 틀린다. 오름차순 문자열에서는 **뒤쪽 자리가 가장 크므로 뒤에서** 지워야 최소가 된다.

```cpp
// ✅ 고친 코드
if (k > 0) stk.resize(stk.size() - k);   // 남은 몫은 뒤에서 잘라낸다
int p = 0;
while (p + 1 < (int)stk.size() && stk[p] == '0') p++;   // 선행 0 제거
string ans = stk.substr(p);
cout << (ans.empty() ? "0" : ans) << '\n';              // 전부 지워지면 0
```

**다음 챕터로**

- 여기서 익힌 `priority_queue` 패턴 — "가장 좋은 것을 꺼내 확정하고 되돌아보지 않는다" — 는 다음 챕터(최단 경로)의 Dijkstra에서 그대로 재등장한다. Dijkstra는 사실 **거리에 대한 그리디**이고, "음수 간선이 없다"가 이 챕터의 교환 논증에 해당하는 전제다. `greater<>`로 최소 힙을 만드는 습관도 그대로 이어진다.
- 반대로 그리디가 깨져 DP로 내려간 자리(0/1 배낭, 임의 액면 동전)는 DP 챕터에서 "상태를 정의하고 표를 채우는" 방식으로 다시 만난다. 그리디에서 반례를 만들어 본 경험이 그때 상태 정의를 빠르게 해 준다.
