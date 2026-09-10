## L5. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch04(String)의 네 무기 — Manacher(팰린드롬 반지름), String Hashing(구간 해시 O(1) 비교), KMP(실패함수), Trie(접두사 트리·비트 트라이) — 를 소재만 바꿔 **반복 훈련**하고, 코딩테스트 단골 문자열 유형으로 **확장**하는 연습 세트다.
- **반복 훈련 개념**:
  - Manacher: `t = "#"`에서 시작해 `for (char c : s) { t += c; t += '#'; }`로 홀·짝을 통일 → `p[i]`는 원본 팰린드롬 길이. 원본 구간 `s[l..r]`이 팰린드롬인지는 `p[l + r + 1] >= r - l + 1`로 O(1) 판정.
  - 접두사 해시: `H[i+1] = (H[i]*B + s[i]) % M`, 구간 해시 `((H[r+1] - H[l]*pw[r-l+1]) % M + M) % M`. **C++의 `%`는 음수를 그대로 음수로 돌려주므로** 파이썬과 달리 `+ M`을 한 번 더 해야 한다. 충돌 방지는 서로 다른 (B, M) 두 쌍을 한 키로 묶는 이중 해시.
  - 라빈-카프 롤링: `cur = cur*B + s[i]` → 윈도가 넘치면 `cur -= s[i-m] * B^m`. 값 타입을 **`unsigned long long`**으로 두면 2^64 자연 오버플로가 곧 모듈러가 되어 나눗셈이 없다. 부호 있는 정수의 오버플로는 **정의되지 않은 동작**이므로 반드시 `unsigned`여야 한다.
  - KMP 실패함수: `while (k > 0 && p[i] != p[k]) k = f[k-1];` → `f.back()`은 최장 경계, 최소 주기는 `n - f.back()`. `A + "#" + B` 결합으로 접두·접미 문제를 푼다.
  - Trie: `struct Node { int nxt[26]; }` 배열 기반(빈 자식은 `-1`)이 포인터·`map`보다 빠르다. 노드마다 `cnt`(지나는 단어 수) / `isEnd`(여기서 끝나는 단어)를 함께 든다. 정수는 상위 비트부터 `nxt[2]`.
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '문자열 알고리즘' 단계, NeetCode 150의 'Tries'·'Bit Manipulation' 유형, 프로그래머스 「코딩테스트 고득점 Kit」의 '해시'가 이 챕터 유형과 맞닿아 있다.
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 가장 긴 팰린드롬 부분문자열 복원 | Easy | Manacher + 원본 인덱스 복원 | 반복 훈련 |
| 2 | 회전 동치 판정 | Medium | 라빈-카프 롤링 해시(A+A) | 반복 훈련 |
| 3 | 최장 반복 부분문자열 | Medium | 이진탐색 + 구간 해시 집합 | 유형 확장 (백준 '문자열 알고리즘' 단계 스타일) |
| 4 | 접두사·접미사 최장 겹침 | Medium | KMP 실패함수 결합 문자열 | 반복 훈련 |
| 5 | 주기적인 접두사 나열 | Medium | 실패함수로 접두사별 최소 주기 | 반복 훈련 |
| 6 | 가장 짧은 고유 접두어 | Medium | Trie 통과 카운트 | 반복 훈련 |
| 7 | 팰린드롬 두 조각 분할 | Hard | Manacher O(1) 구간 판정 | 유형 확장 (백준 '문자열 알고리즘' 단계 스타일) |
| 8 | 앞에 붙여 만드는 최단 팰린드롬 | Hard | KMP 실패함수 + 뒤집은 문자열 결합 | 유형 확장 (NeetCode 스타일) |
| 9 | 부분 배열 XOR 최댓값 | Hard | 누적 XOR + 비트 트라이 | 유형 확장 (NeetCode 'Tries'·'Bit Manipulation' 스타일) |
| 10 | 사전순 k번째 단어 | Hard | Trie 서브트리 카운트로 하강 | 반복 훈련 |

**문제**

**1) 가장 긴 팰린드롬 부분문자열 복원** · Easy

- **요구사항**: 소문자 문자열 `S`에서 팰린드롬인 가장 긴 연속 부분문자열 **자체**를 출력하라. 같은 길이가 여럿이면 **가장 왼쪽에서 시작하는 것**을 고른다.
- **입력**: 첫 줄에 `S` (1 ≤ |S| ≤ 100,000).
- **출력**: 최장 팰린드롬 부분문자열 하나.
- **예제**: `babad` → `bab` · `abcd` → `a`
- **셀프체크**: 변환 문자열 `t`에서 반지름 `p[i]`가 최대인 중심 `i`를 찾으면 원본 시작은 `(i - p[i]) / 2`, 길이는 `p[i]`이고, 출력은 `s.substr(start, len)`이다(파이썬의 `s[a:b]`와 달리 **둘째 인자가 길이**다). "가장 왼쪽"은 `p`를 앞에서부터 훑으며 **더 클 때만**(`>`) 갱신하면 자동으로 지켜진다(`>=`로 쓰면 오른쪽 것이 선택된다). 짝수 길이 `bb`(`cbbd`)도 잡히는지 확인.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    string t = "#";                       // '#' + '#'.join(s) + '#' 과 같은 결과
    for (char c : s) { t += c; t += '#'; }
    int n = (int)t.size();
    vector<int> p(n, 0);
    int c = 0, r = 0;
    int bestLen = 0, bestI = 0;
    for (int i = 0; i < n; i++) {
        if (i < r) p[i] = min(r - i, p[2 * c - i]);
        while (i - p[i] - 1 >= 0 && i + p[i] + 1 < n && t[i - p[i] - 1] == t[i + p[i] + 1])
            p[i]++;
        if (i + p[i] > r) { c = i; r = i + p[i]; }
        if (p[i] > bestLen) {             // 같은 길이면 먼저 나온(왼쪽) 중심을 유지
            bestLen = p[i];
            bestI = i;
        }
    }
    int start = (bestI - bestLen) / 2;
    cout << s.substr(start, bestLen) << '\n';
    return 0;
}
@@TESTS
--IN
babad
--OUT
bab
--IN
abcd
--OUT
a
--IN
cbbd
--OUT
bb
@@EXPL
(1) 접근·핵심 아이디어

- Manacher로 변환 문자열의 반지름 `p`를 O(N)에 구하면 `p[i]`가 곧 원본에서의 팰린드롬 길이다. 최댓값 위치 `i`에서 원본 시작 인덱스는 `(i - p[i]) / 2`.
- "같은 길이면 가장 왼쪽"은 중심 `i`가 작을수록 시작 인덱스도 작으므로, 앞에서부터 훑으며 **더 클 때만** 갱신하면 첫 번째 최댓값(가장 왼쪽)이 남는다.

(2) 코드 단계별

- `t`를 `#`로 시작해 원본 글자와 `#`를 번갈아 붙여 만든다. 길이는 `2|S| + 1`로 항상 홀수라 중심이 언제나 한 칸이다.
- 표준 Manacher 루프(`min(r - i, p[2c - i])` 재활용 → 확장 → `c, r` 갱신)로 `p[i]`를 계산하면서 `p[i] > bestLen`일 때만 갱신.
- `start = (bestI - bestLen) / 2`, `s.substr(start, bestLen)` 출력.

(3) 스스로 다시 짤 때 생각 순서

- 길이만 묻던 문제에서 "문자열 자체 + 동률 규칙"으로 바뀌었다 → 인덱스 복원 공식을 먼저 확정한다.
- C++ 함정: 확장 조건에서 `i - p[i] - 1 >= 0`을 빠뜨리면 음수 인덱스로 `t[-1]`을 읽는다. `std::string::operator[]`는 범위를 확인하지 않아 조용히 쓰레기를 읽고 결과만 이상해진다. 또 `t.size()`는 부호 없는 `size_t`라 `i + p[i] + 1 < t.size()`처럼 `int`와 직접 비교하면 경고가 나므로 `n`을 `int`로 받아 두었다.
- 동률 처리는 비교 연산자 하나(`>` vs `>=`)로 갈린다. `babad`(`bab` vs `aba`)로 확인.
```

**2) 회전 동치 판정** · Medium

- **요구사항**: 두 문자열 `A`, `B`가 주어진다. `A`를 왼쪽으로 `k`칸 회전한 것(앞 k글자를 뒤로 보낸 것)이 `B`와 같아지는 **가장 작은 k**(0 ≤ k < |A|)를 출력하라. 그런 k가 없으면 `-1`.
- **입력**: 첫 줄 `A`, 둘째 줄 `B` (소문자, 1 ≤ |A|, |B| ≤ 100,000).
- **출력**: 최소 회전량 k 또는 `-1`.
- **예제**: `abcde / cdeab` → `2` · `abc / acb` → `-1`
- **셀프체크**: 길이가 다르면 즉시 `-1`. `A + A`의 길이 |A| 윈도를 왼쪽부터 밀며 롤링 해시로 `B`의 해시와 비교하면 첫 일치 위치가 곧 최소 k다. 해시 값을 `unsigned long long`으로 두어 2^64 자연 오버플로를 **의도적으로** 모듈러 대신 쓰는가(부호 있는 정수였다면 오버플로가 UB라 최적화에 따라 결과가 달라진다)? 해시 일치 시 `aa.compare(k, n, b) == 0`으로 실제 비교해 충돌을 거르는가? `k`는 `|A| - 1`까지만 본다. `aaaa / aaaa`는 `0`.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string a, b;
    cin >> a;
    if (!(cin >> b)) b = "";
    int n = (int)a.size();
    if (n != (int)b.size()) {
        cout << -1 << '\n';
        return 0;
    }
    const unsigned long long BASE = 131;    // 자연 오버플로(mod 2^64)를 모듈러로 쓴다
    unsigned long long hb = 0;
    for (char ch : b) hb = hb * BASE + (unsigned char)ch;
    unsigned long long top = 1;             // 윈도에서 나가는 문자의 자릿값 BASE^n
    for (int i = 0; i < n; i++) top *= BASE;

    string aa = a + a;
    unsigned long long cur = 0;
    for (int i = 0; i < (int)aa.size(); i++) {
        cur = cur * BASE + (unsigned char)aa[i];
        if (i >= n) cur -= (unsigned long long)(unsigned char)aa[i - n] * top;
        if (i >= n - 1) {
            int k = i - n + 1;              // 윈도 시작 = 회전량
            if (k >= n) break;
            if (cur == hb && aa.compare(k, n, b) == 0) {
                cout << k << '\n';
                return 0;
            }
        }
    }
    cout << -1 << '\n';
    return 0;
}
@@TESTS
--IN
abcde
cdeab
--OUT
2
--IN
abc
acb
--OUT
-1
--IN
aaaa
aaaa
--OUT
0
--IN
ab
abc
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- `A`를 k칸 회전한 문자열은 `A + A`의 `[k, k + n)` 구간과 같다. 따라서 "B가 A의 회전인가"는 "`A + A`에서 B가 등장하는가"이고, 최소 k는 첫 등장 위치다.
- 등장 위치 탐색은 라빈-카프 롤링 해시로 O(N): 길이 n 윈도를 한 칸씩 밀며 해시를 갱신하고 `B`의 해시와 같을 때만 실제 비교해 충돌을 거른다.
- 길이가 다르면 회전일 수 없으므로 먼저 `-1`.

(2) 코드 단계별

- `B`의 다항식 해시 `hb`와 `top = BASE^n`을 `unsigned long long`으로 준비한다. 곱셈이 2^64를 넘으면 자동으로 하위 64비트만 남는데, 그것이 곧 "mod 2^64"라서 나눗셈 한 번 없이 모듈러 해시가 된다.
- `aa = a + a`를 왼쪽부터 훑으며 `cur = cur*BASE + aa[i]`, 윈도가 n을 넘으면 나가는 문자 `aa[i-n]`에 `top`을 곱해 뺀다. 뺄셈도 `unsigned`에서는 감싸 돌기(wrap)가 표준으로 정의된 동작이라 안전하다.
- `i >= n-1`부터 윈도 시작 `k = i - n + 1`. `k`가 n 이상이면 중단(0..n-1만 의미 있음). 해시가 같고 `aa.compare(k, n, b) == 0`이면 `k` 출력.
- 끝까지 없으면 `-1`.

(3) 스스로 다시 짤 때 생각 순서

- "회전"을 보면 `A + A` 트릭을 먼저 떠올린다. 그다음은 그냥 패턴 검색이다(라빈-카프든 KMP든).
- C++ 함정: 같은 코드를 `long long`으로 쓰면 오버플로가 **정의되지 않은 동작**이라 컴파일러가 "오버플로는 일어나지 않는다"고 가정하고 최적화해 버려 `-O2`에서만 답이 달라지는 일이 생긴다. 오버플로를 의도적으로 쓰는 해시는 **반드시 `unsigned`**. 또 `char`가 부호 있는 플랫폼에서는 한글·이진 데이터를 넣으면 음수가 되므로 `(unsigned char)`로 캐스팅해 두는 습관이 좋다.
- 롤링에서 빼는 항의 자릿값이 `BASE^n`인지 `BASE^(n-1)`인지 곱하는 순서에 따라 정해진다 — 여기선 곱한 뒤 빼므로 `BASE^n`. `k = 0`(같은 문자열)과 길이 불일치를 확인.
```

**3) 최장 반복 부분문자열** · Medium

- **요구사항**: 문자열 `S`에서 **두 번 이상 등장하는**(겹쳐도 됨) 부분문자열 중 가장 긴 것의 길이를 구하라. 없으면 `0`.
- **입력**: 첫 줄에 `S` (소문자, 1 ≤ |S| ≤ 5,000).
- **출력**: 최장 반복 부분문자열의 길이.
- **예제**: `banana` → `3` · `abcd` → `0`
- **셀프체크**: "길이 L짜리 반복이 있으면 길이 L-1짜리도 있다"는 단조성이 있으므로 **길이에 대해 이진탐색**하고, 각 길이 검사는 모든 시작 위치의 구간 해시를 집합에 넣어 중복이 나오는지로 O(N)에 한다. 총 O(N log N). 겹치는 등장(`aaaa` → `aaa`)도 허용되므로 시작 위치만 다르면 된다. 충돌 방지를 위해 두 개의 (BASE, MOD) 쌍을 하나의 `unsigned long long` 키로 합쳐 넣어라. 구간 해시의 뺄셈 결과가 음수일 수 있으니 `((x % M) + M) % M`으로 보정했는가?

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    int n = (int)s.size();
    const long long M1 = 1000000007, M2 = 998244353;
    const long long B1 = 131, B2 = 137;
    vector<long long> H1(n + 1, 0), P1(n + 1, 1), H2(n + 1, 0), P2(n + 1, 1);
    for (int i = 0; i < n; i++) {
        H1[i + 1] = (H1[i] * B1 + s[i]) % M1;
        P1[i + 1] = (P1[i] * B1) % M1;
        H2[i + 1] = (H2[i] * B2 + s[i]) % M2;
        P2[i + 1] = (P2[i] * B2) % M2;
    }
    // 길이 L 부분문자열이 두 번 이상 나오는가
    auto repeats = [&](int L) {
        unordered_set<unsigned long long> seen;
        seen.reserve(n * 2);
        for (int l = 0; l + L <= n; l++) {
            int r = l + L;
            // C++ %는 음수를 음수로 돌려주므로 + M 보정이 필요하다
            long long h1 = ((H1[r] - H1[l] * P1[L]) % M1 + M1) % M1;
            long long h2 = ((H2[r] - H2[l] * P2[L]) % M2 + M2) % M2;
            unsigned long long key = (unsigned long long)h1 * 1000000009ULL + (unsigned long long)h2;
            if (!seen.insert(key).second) return true;   // 이미 있던 값
        }
        return false;
    };

    int lo = 0, hi = n - 1;               // 답의 범위 [0, n-1]
    while (lo < hi) {
        int mid = (lo + hi + 1) / 2;
        if (repeats(mid)) lo = mid;
        else hi = mid - 1;
    }
    cout << lo << '\n';
    return 0;
}
@@TESTS
--IN
banana
--OUT
3
--IN
abcd
--OUT
0
--IN
aaaa
--OUT
3
--IN
z
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- 길이 L의 반복 부분문자열이 있으면 그 앞 L-1글자도 반복이므로 "길이 L에 반복이 존재하는가"는 L이 커질수록 참→거짓으로 한 번만 바뀐다. 이 단조성 위에서 **가장 큰 참 L**을 이진탐색한다.
- 각 L의 판정: 모든 시작 위치의 구간 해시를 O(1)에 뽑아 집합에 넣고 이미 있으면 반복. 접두사 해시 전처리 O(N) 후 판정 O(N), 전체 O(N log N).
- 해시만 같고 문자열이 다른 충돌을 막으려 서로 다른 (BASE, MOD) 두 쌍을 계산해 하나의 64비트 키로 합쳐 쓴다.

(2) 코드 단계별

- 두 세트의 접두사 해시 `H1/P1`, `H2/P2`를 만든다. `H[i]*B`가 최대 (1e9)·137 ≈ 1.4e11이라 `long long`이면 넉넉하지만 `int`면 즉시 오버플로다.
- `repeats(L)`: `l`을 0..n-L로 돌며 두 해시를 계산해 키로 합치고 `unordered_set::insert`의 반환 `pair<iterator, bool>`에서 `.second`가 false면 이미 있던 값 → 반복.
- `lo=0, hi=n-1`에서 "참이면 lo=mid, 거짓이면 hi=mid-1"의 상한 탐색(`mid = (lo+hi+1)/2`로 무한 루프 방지).
- `lo` 출력(반복이 전혀 없으면 0).

(3) 스스로 다시 짤 때 생각 순서

- "최장 + 조건이 단조" → 답을 이진탐색하고 판정 함수를 빠르게 만드는 구도. 판정을 O(N)으로 만드는 도구가 구간 해시.
- C++ 함정: 파이썬의 `%`는 결과 부호가 **나누는 수**를 따라가 항상 양수지만, C++의 `%`는 **나눠지는 수**의 부호를 따라간다. `H[r] - H[l]*P[L]`은 음수가 될 수 있으므로 `(x % M + M) % M`이 필수다. 이걸 빠뜨리면 같은 문자열이 다른 키를 받아 조용히 답이 작아진다.
- 전체 문자열은 한 번밖에 못 나오므로 상한은 n-1. 길이 1 문자열은 이진탐색 루프가 돌지 않고 0.
```

**4) 접두사·접미사 최장 겹침** · Medium

- **요구사항**: 두 문자열 `A`, `B`가 있다. `A`의 **접미사**이면서 `B`의 **접두사**인 가장 긴 문자열의 길이 `L`을 구하고, 그 겹침을 한 번만 쓰도록 이어붙인 문자열 `A + (B의 L번째 이후)`를 출력하라.
- **입력**: 첫 줄 `A`, 둘째 줄 `B` (소문자, 1 ≤ |A|, |B| ≤ 100,000).
- **출력**: 첫 줄에 `L`, 둘째 줄에 이어붙인 문자열.
- **예제**: `abcxyz / xyzabc` → `3 / abcxyzabc` · `hello / world` → `0 / helloworld`
- **셀프체크**: `B + "#" + A`의 실패함수 마지막 값이 답이다 — 결합 문자열 전체의 "접두사 = 접미사" 최장 길이는 곧 "B의 접두사 = A의 접미사" 최장 길이이며, 구분자 `#` 덕분에 B의 길이를 넘어가지 못한다. 순서를 `A + "#" + B`로 하면 다른 문제(A의 접두사 = B의 접미사)를 풀게 된다. 이어붙이기는 `a + b.substr(L)`이고 `L == b.size()`일 때 빈 문자열이 되는지 확인. `aaa / aa`처럼 B 전체가 A의 접미사인 경우 L=|B|가 나오는지 확인.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

vector<int> failure(const string &p) {   // 큰 문자열은 const 참조로 받아 복사를 막는다
    int n = (int)p.size();
    vector<int> f(n, 0);
    int k = 0;
    for (int i = 1; i < n; i++) {
        while (k > 0 && p[i] != p[k]) k = f[k - 1];
        if (p[i] == p[k]) k++;
        f[i] = k;
    }
    return f;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string a, b;
    cin >> a;
    if (!(cin >> b)) b = "";
    vector<int> f = failure(b + "#" + a);   // '#'은 두 문자열에 없는 구분자
    int L = f.back();                       // B의 접두사 == A의 접미사 최장 길이
    cout << L << '\n';
    cout << a + b.substr(L) << '\n';
    return 0;
}
@@TESTS
--IN
abcxyz
xyzabc
--OUT
3
abcxyzabc
--IN
hello
world
--OUT
0
helloworld
--IN
aaa
aa
--OUT
2
aaa
--IN
ab
abab
--OUT
2
abab
@@EXPL
(1) 접근·핵심 아이디어

- 실패함수 `f[i]`는 "그 위치까지의 접두사에서 접두사이자 접미사인 최장 길이"다. `B + "#" + A`를 만들면 이 문자열의 접두사는 B의 접두사, 접미사는 A의 접미사이므로 `f.back()`이 정확히 "B의 접두사 = A의 접미사" 최장 길이가 된다.
- 구분자 `#`은 두 문자열에 없는 문자라, 일치 길이가 |B|를 넘어 `#`을 포함하는 일이 없다(그래서 `L ≤ min(|A|, |B|)`가 자동으로 보장된다).
- 시간 O(|A| + |B|).

(2) 코드 단계별

- `failure`를 자유 함수로 빼되 인자는 `const string &`로 받는다. 값으로 받으면 10만 글자짜리 문자열이 호출마다 통째로 복사된다.
- `f = failure(b + "#" + a)`, `L = f.back()`.
- `L`과 `a + b.substr(L)`(겹친 부분을 한 번만 쓴 결합)을 출력. `substr`의 첫 인자가 시작 위치이고 생략된 둘째 인자는 "끝까지"를 뜻한다.

(3) 스스로 다시 짤 때 생각 순서

- "한쪽의 접미사 = 다른 쪽의 접두사" → 결합 문자열의 실패함수 마지막 값. 어느 쪽이 앞에 오는지(접두사가 되어야 하는 쪽이 앞)를 먼저 정한다.
- C++ 함정: `b.substr(L)`에서 `L`이 `b.size()`와 같으면 빈 문자열을 돌려주지만, `b.size()`보다 크면 `std::out_of_range` 예외가 던져진다. 구분자를 넣어 `L ≤ |B|`를 보장했기 때문에 안전한 것이지, `substr`이 알아서 잘라 주는 것이 아니다.
- 예제 `aaa / aa`로 B 전체가 겹치는 경계, `hello / world`로 겹침 0을 확인.
```

**5) 주기적인 접두사 나열** · Medium

- **요구사항**: 문자열 `S`의 각 접두사(길이 2 이상)에 대해, 그 접두사가 **더 짧은 문자열을 2번 이상 온전히 반복한 형태**이면 `접두사 길이 최소반복단위길이`를 한 줄에 출력하라. 접두사 길이 오름차순. 해당하는 접두사가 하나도 없으면 `NONE`.
- **입력**: 첫 줄에 `S` (소문자, 1 ≤ |S| ≤ 100,000).
- **출력**: 조건을 만족하는 접두사마다 `i p` 한 줄씩, 또는 `NONE`.
- **예제**: `aabaabaa` → `2 1 / 6 3` · `abcd` → `NONE`
- **셀프체크**: 길이 `i`인 접두사의 최소 주기 후보는 `p = i - f[i-1]`이고, `p < i`이면서 `i % p == 0`일 때만 온전한 반복이다. 실패함수는 **한 번만** 계산하면 모든 접두사의 답이 나온다(접두사마다 다시 계산하면 O(N^2)). 출력이 최대 10만 줄이므로 `cout << ... << endl`을 줄마다 쓰면 매번 버퍼를 비워 느려진다 — `'\n'`이나 문자열 버퍼를 쓰는가? `aaaa`는 `2 1`, `3 1`, `4 1` 세 줄이 모두 나오는지 확인.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    int n = (int)s.size();
    vector<int> f(n, 0);
    int k = 0;
    for (int i = 1; i < n; i++) {
        while (k > 0 && s[i] != s[k]) k = f[k - 1];
        if (s[i] == s[k]) k++;
        f[i] = k;
    }
    string out;
    for (int i = 2; i <= n; i++) {       // 길이 i인 접두사
        int p = i - f[i - 1];            // 최소 주기 후보
        if (p < i && i % p == 0) {
            out += to_string(i);
            out += ' ';
            out += to_string(p);
            out += '\n';
        }
    }
    if (out.empty()) cout << "NONE" << '\n';
    else cout << out;
    return 0;
}
@@TESTS
--IN
aabaabaa
--OUT
2 1
6 3
--IN
abcd
--OUT
NONE
--IN
aaaa
--OUT
2 1
3 1
4 1
@@EXPL
(1) 접근·핵심 아이디어

- 접두사 `S[0..i-1]`의 최장 경계(접두사=접미사)는 `f[i-1]`이고, 문자열을 `i - f[i-1]`칸 밀어도 자기 자신과 포개지므로 `p = i - f[i-1]`이 최소 주기다. 길이가 주기로 나눠떨어질 때(`i % p == 0`)만 온전한 반복이고, `p == i`면 반복이 아니다.
- 실패함수 배열 하나가 **모든 접두사의 최장 경계**를 담고 있으므로 한 번 계산으로 모든 접두사를 O(1)씩 판정한다. 총 O(N).
- `aabaabaa`: 길이 2 `aa`(주기 1), 길이 6 `aabaab`(주기 3)만 온전한 반복. 길이 8은 `f=5`, `p=3`, `8 % 3 != 0`이라 제외.

(2) 코드 단계별

- 표준 실패함수 루프로 `f`를 만든다.
- `i`를 2..n으로 돌며 `p = i - f[i-1]`, 조건 `p < i && i % p == 0`이면 `"i p"`를 문자열 버퍼에 붙인다.
- 버퍼가 비었으면 `NONE`, 아니면 한 번에 출력.

(3) 스스로 다시 짤 때 생각 순서

- "접두사마다 주기" → 실패함수는 원래 접두사별 정보이므로 재계산 없이 한 번에 끝남을 인식한다.
- C++ 함정: 출력이 많을 때 `endl`은 줄바꿈에 더해 **버퍼 flush**까지 하므로 10만 줄이면 눈에 띄게 느려진다. `'\n'`을 쓰고, `ios_base::sync_with_stdio(false); cin.tie(nullptr);`로 C 표준 입출력과의 동기화를 끊어 두는 것이 기본 세팅이다.
- 최소 주기 공식 `n - f.back()`과 온전한 반복 조건(나눠떨어짐)을 접두사 길이 `i`에 맞춰 옮겨 쓴다. 길이 1 문자열(출력할 접두사 없음 → `NONE`)과 전부 같은 문자 경계 확인.
```

**6) 가장 짧은 고유 접두어** · Medium

- **요구사항**: 서로 다른 단어 `N`개가 주어진다. 각 단어에 대해, **그 단어만의 접두어**(다른 어떤 단어의 접두어도 아닌 가장 짧은 접두어)를 출력하라. 어떤 단어가 다른 단어의 접두어이면(끝까지 가도 유일해지지 않으면) 단어 전체를 출력한다.
- **입력**: 첫 줄 `N` (1 ≤ N ≤ 10,000), 이후 N줄에 소문자 단어(총 길이 합 ≤ 1,000,000).
- **출력**: 입력 순서대로 단어마다 한 줄.
- **예제**: `4 / apple / apply / banana / bandana` → `apple / apply / bana / band` · `2 / car / card` → `car / card`
- **셀프체크**: 삽입 때 지나는 노드마다 `cnt++` 해 두면, 단어를 따라 내려가다 **처음으로 `cnt == 1`이 되는 노드**까지가 고유 접두어다. `car`는 `card` 때문에 끝까지 `cnt`가 2라 단어 전체가 답이고, `card`는 `d`에서 1이 되어 `card`. 배열 트라이는 자식 슬롯을 `-1`(빈 자식)로 채워 시작했는가? 노드를 `push_back`하면 벡터가 재할당돼 **이전에 잡아 둔 참조·포인터가 전부 무효**가 되므로, 새 노드 번호를 부모 슬롯에 적을 때 `ch[cur][x]`를 다시 인덱싱했는가? 단어가 하나뿐이면 첫 글자에서 바로 유일해진다(`zoo` → `z`).

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<string> words(n);
    for (int i = 0; i < n; i++) cin >> words[i];

    array<int, 26> emptyNode;
    emptyNode.fill(-1);                       // 빈 자식은 -1
    vector<array<int, 26>> ch;
    vector<int> cnt;
    ch.push_back(emptyNode);
    cnt.push_back(0);                         // 0번 = 루트

    for (const string &w : words) {
        int cur = 0;
        for (char c : w) {
            int x = c - 'a';
            if (ch[cur][x] == -1) {
                ch.push_back(emptyNode);
                cnt.push_back(0);
                // push_back 뒤에 ch[cur]을 다시 인덱싱한다(재할당으로 참조가 무효화되므로)
                ch[cur][x] = (int)ch.size() - 1;
            }
            cur = ch[cur][x];
            cnt[cur]++;                       // 이 접두어를 가진 단어 수
        }
    }

    string out;
    for (const string &w : words) {
        int cur = 0;
        string ans = w;                       // 끝까지 유일해지지 않으면 단어 전체
        for (int i = 0; i < (int)w.size(); i++) {
            cur = ch[cur][w[i] - 'a'];
            if (cnt[cur] == 1) {
                ans = w.substr(0, i + 1);
                break;
            }
        }
        out += ans;
        out += '\n';
    }
    cout << out;
    return 0;
}
@@TESTS
--IN
4
apple
apply
banana
bandana
--OUT
apple
apply
bana
band
--IN
2
car
card
--OUT
car
card
--IN
1
zoo
--OUT
z
@@EXPL
(1) 접근·핵심 아이디어

- Trie 노드의 `cnt`는 "이 접두어로 시작하는 단어 수"다. 어떤 접두어가 한 단어만의 것이라는 뜻은 그 노드의 `cnt`가 1이라는 뜻이므로, 단어를 따라 내려가다 처음 `cnt == 1`을 만나는 깊이까지가 답이다.
- 다른 단어의 접두어인 단어(`car` ⊂ `card`)는 끝까지 `cnt ≥ 2`라 유일한 접두어가 없다 → 규칙대로 단어 전체.
- 삽입 O(총 길이), 질의 O(단어 길이).

(2) 코드 단계별

- 배열 트라이를 `vector<array<int,26>> ch`(노드별 자식 번호, 빈 자식 -1)와 `vector<int> cnt`로 만든다. 포인터로 노드를 하나씩 `new` 하는 방식보다 캐시 지역성이 좋고 해제도 필요 없다.
- 모든 단어를 넣으며 지나는 노드의 `cnt`를 1씩 올린다.
- 각 단어를 다시 따라 내려가며 `cnt[cur] == 1`인 첫 위치 `i`에서 `w.substr(0, i + 1)`을 답으로 확정하고 중단.
- 끝까지 못 찾으면 초기값 `w`(전체)를 그대로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "고유 접두어" → 접두어별 개수가 필요 → Trie `cnt`. 두 패스(삽입 → 조회)로 나눈다.
- C++ 함정: `int &slot = ch[cur][x]; ch.push_back(...); slot = ch.size()-1;` 처럼 쓰면 `push_back`이 벡터를 재할당하는 순간 `slot`이 해제된 메모리를 가리켜 정의되지 않은 동작이 된다. `vector`에 원소를 추가한 뒤에는 이전 참조·반복자·포인터를 모두 버리고 다시 인덱싱해야 한다.
- 메모리도 계산해 둔다: 노드 하나가 `26 × 4 = 104`바이트라 총 길이가 백만이면 100MB에 육박한다. 알파벳이 크거나 노드가 많으면 `unordered_map<char,int>`나 자식 연결 리스트로 바꾼다.
- 단어가 하나뿐일 때, 한 단어가 다른 단어의 접두어일 때를 경계로 확인.
```

**7) 팰린드롬 두 조각 분할** · Hard

- **요구사항**: 문자열 `S`를 **비어 있지 않은 두 조각**으로 잘라 두 조각이 모두 팰린드롬이 되게 하는 자르는 위치의 개수를 구하라.
- **입력**: 첫 줄에 `S` (소문자, 2 ≤ |S| ≤ 100,000).
- **출력**: 조건을 만족하는 분할 위치의 수.
- **예제**: `abacc` → `1` · `aaaa` → `3`
- **셀프체크**: 분할마다 두 구간의 팰린드롬 여부를 매번 확인하면 O(N^2)이다. Manacher `p`를 한 번 구해 두면 원본 구간 `s[l..r]`이 팰린드롬인지가 **`p[l + r + 1] >= r - l + 1`**로 O(1)에 판정된다(변환 문자열에서 `s[l]`은 `2l+1`, `s[r]`은 `2r+1`에 있고 그 중심이 `l + r + 1`). `aaaa`는 `a|aaa`, `aa|aa`, `aaa|a` 세 곳, `abacc`는 `aba|cc` 한 곳.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    int n = (int)s.size();
    string t = "#";
    for (char c : s) { t += c; t += '#'; }
    int m = (int)t.size();
    vector<int> p(m, 0);
    int c = 0, r = 0;
    for (int i = 0; i < m; i++) {
        if (i < r) p[i] = min(r - i, p[2 * c - i]);
        while (i - p[i] - 1 >= 0 && i + p[i] + 1 < m && t[i - p[i] - 1] == t[i + p[i] + 1])
            p[i]++;
        if (i + p[i] > r) { c = i; r = i + p[i]; }
    }
    // s[lo..hi]가 팰린드롬인가 (O(1))
    auto isPal = [&](int lo, int hi) { return p[lo + hi + 1] >= hi - lo + 1; };

    int ans = 0;
    for (int i = 0; i < n - 1; i++)      // 앞 조각 s[0..i], 뒤 조각 s[i+1..n-1]
        if (isPal(0, i) && isPal(i + 1, n - 1)) ans++;
    cout << ans << '\n';
    return 0;
}
@@TESTS
--IN
abacc
--OUT
1
--IN
aaaa
--OUT
3
--IN
abc
--OUT
0
--IN
ab
--OUT
1
@@EXPL
(1) 접근·핵심 아이디어

- 변환 문자열 `t`에서 원본 `s[l..r]`의 중심은 인덱스 `l + r + 1`이고, 그 중심의 반지름 `p`가 원본 길이 `r - l + 1` 이상이면 그 구간은 팰린드롬이다. 즉 Manacher 한 번으로 **임의 구간의 팰린드롬 여부를 O(1)**에 답할 수 있다.
- 분할 위치 `i`(앞 조각 `s[0..i]`, 뒤 조각 `s[i+1..n-1]`)마다 두 번의 O(1) 판정 → 전체 O(N).
- 반지름이 구간 길이보다 **크거나 같으면** 된다(더 큰 팰린드롬의 가운데 부분도 팰린드롬이므로 `>=`).

(2) 코드 단계별

- 표준 Manacher로 `p`를 계산한다.
- `isPal`을 람다로 두면 `[&]` 캡처로 `p`를 그대로 쓰면서 함수처럼 부를 수 있다.
- `i`를 0..n-2로 돌며 `isPal(0, i) && isPal(i+1, n-1)`이면 카운트.

(3) 스스로 다시 짤 때 생각 순서

- "여러 구간의 팰린드롬 판정" → 구간 DP O(N^2) 대신 Manacher + 중심 공식 O(1)을 떠올린다.
- 중심 인덱스 공식은 `s[l]→2l+1`, `s[r]→2r+1`의 평균으로 직접 유도해 둔다.
- C++ 함정: `&&`는 왼쪽이 거짓이면 오른쪽을 아예 평가하지 않는 단축 평가라, 위험한 인덱싱을 오른쪽에 두는 방어 코드가 성립한다. 다만 **비트 연산 `&`는 단축 평가가 없고 우선순위도 `==`보다 낮다** — 논리 조건에 `&`를 잘못 쓰면 `a & b == c`가 `a & (b == c)`로 묶여 조용히 다른 뜻이 된다.
- 두 조각 모두 비어 있지 않아야 하므로 `i`의 범위는 `n-2`까지. `ab`(`a|b` → 1)와 `abc`(0)로 확인.
```

**8) 앞에 붙여 만드는 최단 팰린드롬** · Hard

- **요구사항**: 문자열 `S`의 **앞에만** 문자를 붙여 팰린드롬으로 만들 때, 만들 수 있는 가장 짧은 팰린드롬을 출력하라.
- **입력**: 첫 줄에 `S` (소문자, 1 ≤ |S| ≤ 100,000).
- **출력**: 가장 짧은 결과 팰린드롬.
- **예제**: `aacecaaa` → `aaacecaaa` · `abcd` → `dcbabcd`
- **셀프체크**: 앞에 붙이는 문자는 S의 뒷부분을 뒤집은 것이어야 하므로, S의 **가장 긴 팰린드롬 접두사** 길이 `L`을 찾으면 답은 `S의 L번째 이후를 뒤집은 것 + S`다. 팰린드롬 접두사 = "S의 접두사이면서 rev(S)의 접미사"이므로 `S + "#" + rev(S)`의 실패함수 마지막 값이 `L`이다. 구분자가 없으면 `L`이 |S|를 넘을 수 있어 틀린다. 뒤집기는 `string rs(s.rbegin(), s.rend())`나 `reverse(v.begin(), v.end())`로 하는가? `aba`처럼 이미 팰린드롬이면 그대로 나오는지 확인.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    string rev(s.rbegin(), s.rend());       // 역방향 반복자로 뒤집은 사본을 만든다
    string combo = s + "#" + rev;
    int n = (int)combo.size();
    vector<int> f(n, 0);
    int k = 0;
    for (int i = 1; i < n; i++) {
        while (k > 0 && combo[i] != combo[k]) k = f[k - 1];
        if (combo[i] == combo[k]) k++;
        f[i] = k;
    }
    int L = f.back();                       // s의 가장 긴 팰린드롬 접두사 길이
    string head = s.substr(L);
    reverse(head.begin(), head.end());
    cout << head + s << '\n';
    return 0;
}
@@TESTS
--IN
aacecaaa
--OUT
aaacecaaa
--IN
abcd
--OUT
dcbabcd
--IN
aba
--OUT
aba
--IN
a
--OUT
a
@@EXPL
(1) 접근·핵심 아이디어

- 앞에 문자를 붙여 팰린드롬을 만들면 결과는 `X + S` 꼴이고, 뒤집어도 같아야 하므로 `X`는 `S`의 어떤 접미사를 뒤집은 것이다. 붙이는 양을 최소로 하려면 `S`에서 **팰린드롬인 접두사를 최대한 길게** 남기고 그 뒤 나머지만 뒤집어 앞에 붙이면 된다.
- "팰린드롬 접두사"는 "S의 접두사 = rev(S)의 접미사"와 같으므로 `S + "#" + rev(S)`의 실패함수 마지막 값 `L`이 최장 팰린드롬 접두사 길이다. 답은 `rev(S[L:]) + S`. 시간 O(N).
- `aacecaaa`는 접두사 `aacecaa`(7)가 팰린드롬 → 남은 `a`를 뒤집어 앞에 붙여 `aaacecaaa`.

(2) 코드 단계별

- `string rev(s.rbegin(), s.rend());`로 뒤집은 사본을 만든다. 반복자 쌍 생성자는 "이 범위를 순서대로 담아라"는 뜻이라 역방향 반복자를 주면 뒤집힌 사본이 된다.
- `combo = s + "#" + rev`의 실패함수를 계산하고 `L = f.back()`.
- `head = s.substr(L)`를 `reverse`로 제자리 뒤집어 `head + s`를 출력한다. `std::reverse`는 값을 돌려주지 않고 원본을 고치는 함수라 `cout << reverse(...)`처럼 쓸 수 없다.

(3) 스스로 다시 짤 때 생각 순서

- "앞에 붙여 팰린드롬" → 최장 팰린드롬 접두사 문제로 바꾼다.
- 팰린드롬 접두사 = 접두사와 뒤집은 문자열의 접미사 일치 → 결합 + 실패함수. 구분자 필수.
- C++ 함정: 파이썬의 `s[::-1]`은 새 문자열을 만들어 돌려주지만 C++의 `reverse`는 제자리(in-place) 연산이다. 원본을 보존해야 하면 먼저 복사한 뒤 뒤집어야 한다. 이미 팰린드롬인 경우(`L = n`, 아무것도 안 붙임)와 길이 1을 확인.
```

**9) 부분 배열 XOR 최댓값** · Hard

- **요구사항**: 음이 아닌 정수 배열에서 **연속 부분 배열**(길이 1 이상)의 원소들을 모두 XOR한 값의 최댓값을 구하라.
- **입력**: 첫 줄 `N` (1 ≤ N ≤ 100,000), 둘째 줄에 정수 N개(각 0 ≤ x < 2^31).
- **출력**: 부분 배열 XOR의 최댓값.
- **예제**: `4 / 8 1 2 12` → `15` · `3 / 5 5 5` → `5`
- **셀프체크**: 누적 XOR `px[i] = a[0] ^ … ^ a[i-1]`을 두면 부분 배열 `[l, r]`의 XOR는 `px[r+1] ^ px[l]`이다. 즉 "누적값들 중 두 개를 골라 XOR 최대"로 바뀌고, 이는 비트 트라이로 O(N·31)에 푼다. **`px[0] = 0`을 먼저 트라이에 넣어야** 배열 처음부터 시작하는 부분 배열이 포함된다. 비트를 뽑는 `(x >> b) & 1`에 **괄호를 제대로 쳤는가** — C++에서 `&`는 `==`보다 우선순위가 **낮아** `x >> b & 1 == 1`이 `x >> b & (1 == 1)`로 묶여 완전히 다른 뜻이 된다(파이썬과 정반대다). 모든 원소가 0이면 답 0.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

const int BITS = 31;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];

    vector<array<int, 2>> ch;
    ch.push_back({-1, -1});                    // 0번 = 루트

    auto insert = [&](int x) {
        int cur = 0;
        for (int b = BITS - 1; b >= 0; b--) {
            int bit = (x >> b) & 1;            // 괄호 필수: & 가 == 보다 우선순위가 낮다
            if (ch[cur][bit] == -1) {
                ch.push_back({-1, -1});
                ch[cur][bit] = (int)ch.size() - 1;   // push_back 뒤 다시 인덱싱
            }
            cur = ch[cur][bit];
        }
    };
    // 트라이 안의 값과 x의 XOR 최댓값
    auto query = [&](int x) {
        int cur = 0, val = 0;
        for (int b = BITS - 1; b >= 0; b--) {
            int bit = (x >> b) & 1;
            int want = 1 - bit;
            if (ch[cur][want] != -1) {
                val |= (1 << b);
                cur = ch[cur][want];
            } else {
                cur = ch[cur][bit];
            }
        }
        return val;
    };

    insert(0);                                 // 빈 접두사의 누적 XOR
    int px = 0, best = 0;
    for (int x : nums) {
        px ^= x;
        int q = query(px);
        if (q > best) best = q;
        insert(px);
    }
    cout << best << '\n';
    return 0;
}
@@TESTS
--IN
4
8 1 2 12
--OUT
15
--IN
3
5 5 5
--OUT
5
--IN
1
0
--OUT
0
@@EXPL
(1) 접근·핵심 아이디어

- XOR는 자기 자신과 하면 0이 되므로 누적 XOR `px`로 구간 XOR를 `px[r+1] ^ px[l]`로 바꿀 수 있다(누적합의 XOR 판). 그러면 문제는 "누적값 집합에서 두 값의 XOR 최대"가 된다.
- 두 수의 XOR 최대는 이진 트라이에 값을 넣고, 상위 비트부터 **반대 비트 자식을 우선** 내려가는 그리디로 O(31)에 찾는다. 누적값을 왼쪽부터 하나씩 "질의 후 삽입"하면 `l < r+1`인 모든 쌍을 정확히 한 번씩 고려한다.
- `px[0] = 0`을 먼저 넣어야 `[0, r]` 구간이 포함된다. 첫 예제는 `1 ^ 2 ^ 12 = 15`.

(2) 코드 단계별

- 배열 트라이 `vector<array<int,2>> ch`(자식 0/1, 빈 자식 -1)를 만든다.
- `insert`/`query`는 최대 XOR 쌍과 동일. 상위 비트(30)부터 0까지 내려간다. 값이 2^31 미만이므로 비트 0..30만 있으면 충분하고, `1 << 30`은 `int` 안에 들어간다.
- `insert(0)` 후 원소를 순회하며 `px ^= x`, `query(px)`로 최댓값 갱신, `insert(px)`.

(3) 스스로 다시 짤 때 생각 순서

- "연속 부분 배열의 XOR" → 누적 XOR로 두 점 문제로 변환(누적합 사고를 XOR에 이식).
- 두 점 XOR 최대 → 비트 트라이 그리디. 삽입 전 질의 순서로 중복 없이 쌍을 센다.
- C++ 함정 둘. (a) **비트 연산 우선순위**: C++의 우선순위는 `<<`·`>>` > 비교(`<`, `==`) > `&` > `^` > `|` 순이라, `mask & 1 == 0`은 `mask & (1 == 0)` 즉 `mask & 0`으로 묶여 항상 0이 된다. 파이썬은 비교가 비트 연산보다 **낮아** 정반대이므로, 파이썬 코드를 옮길 때 비트 조건에는 무조건 괄호를 친다. (b) **`1 << b`의 타입**: `1`은 `int`라 `b`가 31 이상이면 오버플로다. 64비트 마스크가 필요하면 `1LL << b`로 써야 한다.
- 함정: 0을 미리 넣지 않으면 첫 원소부터 시작하는 구간을 놓친다. 전부 0이면 답 0.
```

**10) 사전순 k번째 단어** · Hard

- **요구사항**: 처음엔 비어 있는 단어 집합에 대해 다음 두 종류의 명령을 순서대로 처리하라. `+ w`: 단어 `w`를 집합에 넣는다(이미 있으면 무시). `? k`: 현재 집합의 단어들을 사전순으로 나열했을 때 `k`번째(1부터) 단어를 출력한다. 단어가 `k`개 미만이면 `-1`.
- **입력**: 첫 줄 `Q` (1 ≤ Q ≤ 100,000), 이후 Q줄에 명령(단어는 소문자, 총 길이 합 ≤ 1,000,000).
- **출력**: `?` 명령마다 한 줄.
- **예제**: `7 / + banana / + apple / ? 1 / + app / ? 1 / ? 3 / ? 4` → `apple / app / banana / -1` · `4 / + b / + a / + a / ? 2` → `b`
- **셀프체크**: 삽입이 질의 사이에 섞이므로 매번 정렬하면 느리다. Trie에 노드별 **서브트리 단어 수 `cnt`**를 두면, 루트에서 내려가며 "이 노드에서 끝나는 단어가 있으면 그것이 1번째", 그다음 자식을 **글자 순으로**(배열 트라이면 인덱스 0..25 순서가 곧 사전순) 보며 `k <= cnt[자식]`이면 들어가고 아니면 `k -= cnt[자식]`으로 건너뛴다. 중복 삽입을 무시하지 않으면 `cnt`가 부풀어 틀린다. 루트의 `cnt`가 전체 단어 수이므로 `k > cnt[0]`이면 `-1`. 끝 표시 배열을 `end`로 이름 짓지 마라 — `using namespace std;` 아래에서 `std::end`와 헷갈린다.

```runner
@@SOLUTION
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    array<int, 26> emptyNode;
    emptyNode.fill(-1);
    vector<array<int, 26>> ch;
    vector<int> cnt, isEnd;                   // isEnd: std::end와 헷갈리지 않게 이름을 바꿈
    ch.push_back(emptyNode);
    cnt.push_back(0);                         // 서브트리(자기 포함)에서 끝나는 단어 수
    isEnd.push_back(0);

    string out;
    for (int t = 0; t < q; t++) {
        string op;
        cin >> op;
        if (op == "+") {
            string w;
            cin >> w;
            int cur = 0;
            bool exists = true;
            for (char c : w) {                // 이미 있는 단어인지 먼저 확인
                int x = c - 'a';
                if (ch[cur][x] == -1) { exists = false; break; }
                cur = ch[cur][x];
            }
            if (exists && isEnd[cur]) continue;
            cur = 0;
            cnt[0]++;
            for (char c : w) {
                int x = c - 'a';
                if (ch[cur][x] == -1) {
                    ch.push_back(emptyNode);
                    cnt.push_back(0);
                    isEnd.push_back(0);
                    ch[cur][x] = (int)ch.size() - 1;
                }
                cur = ch[cur][x];
                cnt[cur]++;
            }
            isEnd[cur] = 1;
        } else {
            int k;
            cin >> k;
            if (k > cnt[0]) { out += "-1\n"; continue; }
            int cur = 0;
            string res;
            while (true) {
                if (isEnd[cur]) {
                    if (k == 1) break;        // 이 노드에서 끝나는 단어가 답
                    k--;
                }
                bool moved = false;
                for (int c = 0; c < 26; c++) {   // 인덱스 순서가 곧 사전순
                    int nx = ch[cur][c];
                    if (nx == -1) continue;
                    if (k <= cnt[nx]) {
                        res += char('a' + c);
                        cur = nx;
                        moved = true;
                        break;
                    }
                    k -= cnt[nx];
                }
                if (!moved) break;
            }
            out += res;
            out += '\n';
        }
    }
    cout << out;
    return 0;
}
@@TESTS
--IN
7
+ banana
+ apple
? 1
+ app
? 1
? 3
? 4
--OUT
apple
app
banana
-1
--IN
4
+ b
+ a
+ a
? 2
--OUT
b
--IN
1
? 1
--OUT
-1
@@EXPL
(1) 접근·핵심 아이디어

- Trie에서 단어들은 루트로부터의 경로이고, 자식을 글자 순으로 방문하면 사전순이 된다. 어떤 노드에서 끝나는 단어는 그 서브트리의 다른 모든 단어보다 사전순으로 앞선다(짧은 접두어가 먼저).
- 노드별로 `cnt`(서브트리에서 끝나는 단어 수)를 유지하면, k번째 단어를 찾을 때 자식 서브트리를 통째로 건너뛸 수 있다: `k <= cnt[자식]`이면 그 자식으로 들어가고, 아니면 `k -= cnt[자식]`. 질의 O(단어 길이 × 알파벳).
- 삽입이 질의 사이에 섞여도 `cnt` 갱신만으로 동적 집합을 유지한다(정렬 재계산 불필요).

(2) 코드 단계별

- `+ w`: 먼저 따라 내려가 이미 끝 표시가 있으면 무시. 아니면 루트 `cnt` 포함 지나는 모든 노드의 `cnt`를 1 올리고 마지막 노드에 `isEnd = 1`.
- `? k`: `k > cnt[0]`이면 `-1`. 아니면 루트에서 시작해 `isEnd[cur]`이면 `k == 1`일 때 종료·아니면 `k--`, 자식을 0..25 순으로 보며 들어가거나 건너뛴다. 배열 트라이는 인덱스 순서가 그대로 사전순이라 `map`처럼 따로 정렬할 필요가 없다.
- 명령 토큰은 `cin >> op`로 읽고 종류에 따라 뒤를 문자열 또는 정수로 읽는다. 결과를 버퍼에 모아 한 번에 출력.

(3) 스스로 다시 짤 때 생각 순서

- "동적 집합 + 순위(k번째)" → 서브트리 크기를 들고 있는 트리에서 하강. 문자열이므로 Trie + `cnt`.
- 노드에서 끝나는 단어를 먼저 처리한 뒤 자식으로 가는 순서가 사전순임을 확인(`app` < `apple`).
- C++ 함정: 변수 이름을 `end`, `size`, `count`, `data`, `distance`처럼 지으면 `using namespace std;` 아래에서 표준 함수와 이름이 겹쳐, 지역에서는 가려지지만 읽는 사람에게는 함정이고 전역에서는 실제로 모호해질 수 있다. `isEnd` 같은 이름으로 피한다.
- 함정: 중복 삽입 시 `cnt`가 부풀지 않게 존재 확인 먼저. 빈 집합 질의는 `-1`.
```
