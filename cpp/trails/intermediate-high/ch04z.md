## L6. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터의 네 도구는 겉모습이 달라도 뼈대가 같다. **문자열을 한 번 훑어 배열 하나를 만들어 두고**, 그다음부터는 질의를 O(1)이나 O(길이)에 답한다. Manacher는 반지름 배열, 해시는 접두사 배열, KMP는 실패 함수 배열, 트라이는 경로 위에 얹은 카운터가 그 "한 번 만든 표"다. 그러니 도구 선택은 곧 **"무엇을 묻는 질의가 반복되는가"**를 정하는 일이다.

**개념 지도**

```text
  Ch04 map : build one table first, then answer fast

  a string  s
   |
   +-- compare two pieces by value    ->  polynomial hash
   |     H[i+1] = H[i]*B + s[i]           prefix table, O(1) per range
   |     sub(l,r) = H[r+1] - H[l]*pw[r-l+1]
   |     one modulus collides -> pair (h1, h2), or verify the text
   |
   +-- locate one fixed pattern       ->  KMP failure function
   |     pi[i] = longest proper border of p[0..i]
   |     the text pointer never moves back  ->  O(n + m)
   |     same array gives period = m - pi[m-1]
   |
   +-- palindrome radius everywhere   ->  Manacher
   |     '#' between characters makes every center odd
   |     p[l+r+1] >= r-l+1  answers "is s[l..r] a palindrome ?"
   |
   +-- many words sharing prefixes    ->  Trie
         cnt[v] = words passing v , endc[v] = words ending at v
         an integer is a 30-bit string -> binary trie, XOR greedy
```

질의의 모양이 도구를 정한다. 아래 한 줄씩이 그대로 판단 규칙이다.

```text
  what does the problem ask, and how many times ?

  one pattern, every occurrence           -> KMP           O(n + m)
  "are these two ranges equal ?" x 1e5    -> rolling hash   O(1) each
  "how many words start with p ?"         -> trie + cnt     O(|p|)
  longest palindromic substring           -> Manacher       O(n)
  "is s[l..r] a palindrome ?" x 1e5       -> Manacher radii  O(1) each
  shortest period, prefix == suffix       -> KMP pi[m-1]
  is B a rotation of A ?                  -> find B in A + A
  max XOR of a pair                       -> binary trie    O(n * B)
  k-th word in lexicographic order        -> trie subtree counts
```

실패 함수와 구분자를 붙이는 한 가지 재주가 서로 달라 보이는 문제를 하나로 묶는다.

```text
  separator trick : one failure function, many questions

  X + '#' + Y     pi.back() = longest prefix of X that is a suffix of Y
     P + '#' + S     -> where does P sit inside S
     B + '#' + A     -> overlap when gluing A then B
     S + '#' + rev(S)-> longest palindromic prefix of S
  A + A           search B here -> rotation, first hit = smallest k
  # '#' must appear in neither side, or a match leaks across the seam
```

C++로 옮길 때 문자열 쪽에서 새로 생기는 함정은 네 갈래다.

```text
  what C++ adds on top of the string algorithms

  s.size()      unsigned : i - 1 < s.size() is ALWAYS true when i == 0
  f[-1]         no negative index : use f.back() or f[m-1]
  overflow      h*B+c overflows int ; signed overflow is UB
                unsigned long long overflow is fine : it IS mod 2^64
  a % b         keeps the sign of a : add MOD before taking %
```

**뼈대 코드**

1) KMP — 실패 함수 + 매칭 + 주기

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> failure(const string& p) {          // 실패 함수(LPS) 배열, O(m)
    int m = (int)p.size();
    vector<int> pi(m, 0);
    int j = 0;                                  // 지금까지 맞은 접두사 길이
    for (int i = 1; i < m; i++) {
        while (j > 0 && p[i] != p[j]) j = pi[j - 1];   // pi[j]가 아니다
        if (p[i] == p[j]) j++;
        pi[i] = j;
    }
    return pi;
}

vector<int> kmpAll(const string& s, const string& p) {   // 겹치는 등장까지 전부
    vector<int> pi = failure(p), res;
    int n = (int)s.size(), m = (int)p.size(), j = 0;
    for (int i = 0; i < n; i++) {
        while (j > 0 && s[i] != p[j]) j = pi[j - 1];     // 텍스트 포인터 i는 그대로
        if (s[i] == p[j]) j++;
        if (j == m) {
            res.push_back(i - m + 1);            // 1-indexed 출력이면 +1
            j = pi[j - 1];                       // 0이 아니다 — 겹침을 보존
        }
    }
    return res;
}

// 문자열 자신에게 쓰면 주기가 나온다
vector<int> pi = failure(s);
int len = (int)s.size();
int period = len - pi.back();                    // 밀어도 포개지는 최소 칸 수
bool isRepeat = (period < len && len % period == 0);   // 온전한 반복인가
```

2) 롤링 해시 — 접두사 전처리 + 구간 해시 + 이중 해시

```cpp
typedef unsigned long long u64;
typedef __uint128_t u128;
const u64 MOD1 = (1ULL << 61) - 1, MOD2 = 1000000007ULL;
const u64 B1 = 131, B2 = 137;                   // 알파벳 크기보다 큰 서로 다른 소수

u64 mulmod61(u64 a, u64 b) {                    // 61비트 메르센 소수 전용 곱
    u128 c = (u128)a * b;
    u64 r = (u64)(c & MOD1) + (u64)(c >> 61);
    return r >= MOD1 ? r - MOD1 : r;
}

void build(const string& s, u64 base, u64 mod, vector<u64>& H, vector<u64>& pw) {
    int n = (int)s.size();
    H.assign(n + 1, 0);
    pw.assign(n + 1, 1);
    for (int i = 0; i < n; i++) {
        u64 c = (u64)(unsigned char)s[i];        // char 의 부호에 휘둘리지 않게
        H[i + 1] = (mod == MOD1 ? (mulmod61(H[i], base) + c) % mod
                                : (H[i] * base + c) % mod);
        pw[i + 1] = (mod == MOD1 ? mulmod61(pw[i], base) : (pw[i] * base) % mod);
    }
}

u64 rng(const vector<u64>& H, const vector<u64>& pw, u64 mod, int l, int r) {
    u64 back = (mod == MOD1 ? mulmod61(H[l], pw[r - l + 1])
                            : (H[l] * pw[r - l + 1]) % mod);
    return (H[r + 1] + mod - back) % mod;        // + mod 로 음수를 미리 막는다
}

// 이중 해시 키 = 사실상 충돌 없음. set/map 에 넣을 때는 pair 로 묶는다
pair<u64,u64> key(int l, int r) {
    return {rng(H1, pw1, MOD1, l, r), rng(H2, pw2, MOD2, l, r)};
}
```

3) 트라이 — 배열 인덱스 노드로 삽입·검색·접두어 카운트

```cpp
struct Trie {
    vector<array<int,26>> nxt;                   // 자식을 '인덱스'로 가리킨다
    vector<int> cnt, endc;                       // 지나간 수 / 여기서 끝난 수
    Trie() { newNode(); }                        // 0번이 루트
    int newNode() {
        array<int,26> a; a.fill(-1);
        nxt.push_back(a);
        cnt.push_back(0);
        endc.push_back(0);                       // 세 배열을 항상 함께 늘린다
        return (int)nxt.size() - 1;
    }
    void add(const string& w) {
        int cur = 0;
        for (char c : w) {
            int idx = c - 'a';                   // 입력이 소문자라는 보장이 필요
            if (nxt[cur][idx] == -1) {
                int nn = newNode();              // 먼저 만들고
                nxt[cur][idx] = nn;              // 그다음에 대입 (재할당 안전)
            }
            cur = nxt[cur][idx];
            cnt[cur]++;
        }
        endc[cur]++;                             // 중복을 무시하려면 1로 고정
    }
    int countPrefix(const string& p) {           // p로 시작하는 단어 수
        int cur = 0;
        for (char c : p) {
            int idx = c - 'a';
            if (nxt[cur][idx] == -1) return 0;   // 경로가 끊기면 0
            cur = nxt[cur][idx];
        }
        return cnt[cur];
    }
    bool hasWord(const string& w) {              // '단어가 있나'는 도달만으론 부족
        int cur = 0;
        for (char c : w) {
            int idx = c - 'a';
            if (nxt[cur][idx] == -1) return false;
            cur = nxt[cur][idx];
        }
        return endc[cur] > 0;                    // 접두어 존재와 단어 존재는 다르다
    }
};
```

4) Manacher — 구분자 + 반지름 배열 + 구간 회문 O(1) 판정

```cpp
vector<int> manacher(const string& s, string& t) {
    t.clear();
    t.reserve(2 * s.size() + 1);
    t.push_back('#');
    for (char ch : s) { t.push_back(ch); t.push_back('#'); }   // 구분자 필수
    int n = (int)t.size();                       // 부호 있는 int 로 고정
    vector<int> p(n, 0);
    int c = 0, r = 0;                            // 최우측 회문의 중심 c, 오른끝 r
    for (int i = 0; i < n; i++) {
        if (i < r) p[i] = min(r - i, p[2 * c - i]);            // min 클램프 필수
        while (i - p[i] - 1 >= 0 && i + p[i] + 1 < n
               && t[i - p[i] - 1] == t[i + p[i] + 1])
            p[i]++;
        if (i + p[i] > r) { c = i; r = i + p[i]; }
    }
    return p;                                    // p[i] = 원본에서의 회문 길이
}

string t;
vector<int> p = manacher(s, t);

bool isPal(int l, int r) {                       // s[l..r]가 회문인가 — O(1)
    return p[l + r + 1] >= r - l + 1;            // 중심 인덱스는 l + r + 1
}

int best = *max_element(p.begin(), p.end());     // 길이만 필요하면 여기까지
int i = (int)(find(p.begin(), p.end(), best) - p.begin());
int start = (i - best) / 2;                      // s.substr(start, best)
```

5) 비트 트라이 — XOR 최대

```cpp
const int BITS = 30;                             // 값의 상한에 맞춰 조정
vector<array<int,2>> bt(1, {-1, -1});            // bt[node] = {자식0, 자식1}

void btInsert(int x) {
    int cur = 0;
    for (int b = BITS - 1; b >= 0; b--) {        // 반드시 상위 비트부터
        int d = (x >> b) & 1;                    // 괄호 필수 (& 가 == 보다 약함)
        if (bt[cur][d] == -1) {
            bt.push_back({-1, -1});
            bt[cur][d] = (int)bt.size() - 1;
        }
        cur = bt[cur][d];
    }
}

int btMaxXor(int x) {                            // 트라이 안의 값과 x의 XOR 최댓값
    int cur = 0, val = 0;
    for (int b = BITS - 1; b >= 0; b--) {
        int d = (x >> b) & 1;
        if (bt[cur][1 - d] != -1) {              // 반대 비트를 최우선으로
            val |= 1 << b;
            cur = bt[cur][1 - d];
        } else {
            cur = bt[cur][d];                    // 없으면 어쩔 수 없이 같은 비트
        }
    }
    return val;
}

btInsert(0);                                     // 빈 접두사 — 빼먹으면 [0..r] 누락
int acc = 0, ans = 0;
for (int x : nums) {                             // 누적 XOR로 구간을 두 점 문제로
    acc ^= x;
    ans = max(ans, btMaxXor(acc));               // 질의를 먼저, 삽입을 나중에
    btInsert(acc);
}
```

**언제 무엇을 쓰나**

먼저 **네 도구 중 무엇인가**를 이 표 하나로 가른다.

| 판단 기준 | KMP | 롤링 해시 | 트라이 | Manacher |
| --- | --- | --- | --- | --- |
| 한 문장 요약 | 패턴 하나를 되돌림 없이 훑는다 | 임의 구간을 정수 하나로 압축 | 접두사를 경로로 공유 | 모든 중심의 회문 반지름 |
| 전처리 | O(m) 실패 함수 | O(n) 접두사·거듭제곱 | O(총 글자 수) | O(n) 반지름 |
| 질의 | O(n) 한 번 훑기 | O(1) 구간 비교 | O(길이) | O(1) 구간 판정 |
| 대상 개수 | 패턴 **하나** | 구간 **여러 개** | 문자열 **여러 개** | 회문 **전부** |
| 결과의 확실성 | 항상 정확 | 확률적(충돌 가능) | 항상 정확 | 항상 정확 |
| 메모리 | O(m) | O(n) | O(총 글자 수 × 26) | O(n) |
| 대표 응용 | 등장 위치, 최소 주기, 경계 | 서로 다른 부분 문자열, 이분 탐색 | 자동완성, 접두사 개수, XOR 최대 | 최장 회문, 회문 개수 |
| 패턴이 여러 개 | 패턴마다 다시 돌려야 함 | 해시 집합으로 한 번에 | **가장 유리**(사전으로 담음) | 해당 없음 |
| C++ 주의점 | `f.back()`, `size()`가 unsigned | 곱셈 오버플로·음수 나머지 | `vector` 재할당, `c-'a'` 범위 | `int n`으로 경계 비교 |
| 못 하는 것 | 임의 구간 비교 | 100% 보장 | 회문·주기 | 일반 패턴 검색 |

도구를 정했으면 아래에서 구체적인 형태를 고른다.

| 문제가 묻는 것 | 고르는 것 | 이유 | 전처리·질의 복잡도 |
| --- | --- | --- | --- |
| 한 패턴의 등장 위치 전부 | KMP | 텍스트 포인터를 되돌리지 않아 최악에도 선형 | 전처리 O(m), 검색 O(n) |
| 부분 문자열 동일 여부를 반복 질의 | 접두사(롤링) 해시 | 임의 구간이 정수 하나로 압축돼 비교가 상수 시간 | 전처리 O(n), 질의 O(1) |
| 접두어로 시작하는 단어 수 | 트라이 + `cnt` | 접두어 경로 끝 노드의 카운터를 읽기만 하면 끝 | 삽입 O(총 길이), 질의 O(\|p\|) |
| 단어가 사전에 있나 | 트라이 + `endc` | 도달 여부가 아니라 끝 표시로 판정해야 정확 | 삽입 O(총 길이), 질의 O(\|w\|) |
| 가장 긴 회문 부분 문자열 | Manacher | 모든 중심의 반지름을 한 번에 얻는다 | 전처리 O(n), 조회 O(1) |
| 임의 구간이 회문인가(반복) | Manacher 반지름 배열 | `p[l+r+1] >= r-l+1` 한 줄로 판정 | 전처리 O(n), 질의 O(1) |
| 최소 주기·접두=접미 | KMP 실패 함수 `pi.back()` | 최장 경계가 곧 주기 `m - pi.back()` | 전처리 O(n), 질의 O(1) |
| 회전 동치 판정(최소 회전량) | `A + A`에서 `B` 매칭 | 회전 결과는 전부 `A+A`의 길이 n 창 | O(n) |
| 앞에 붙여 만드는 최단 회문 | `S + '#' + rev(S)` 실패 함수 | 최장 회문 접두사 길이가 곧 남길 부분 | O(n) |
| 한쪽 접미사 = 다른 쪽 접두사 | `X + '#' + Y` 실패 함수 | 결합 문자열의 최장 경계가 정확히 그 값 | O(\|X\| + \|Y\|) |
| 최장 반복 부분 문자열 | 길이 이분 탐색 + 구간 해시 `set` | 길이에 단조성이 있고 판정이 O(n) | O(n log n) |
| 서로 다른 부분 문자열 개수(n ≤ 3000) | 길이별 해시 `set` 크기 합 | 구간 해시가 O(1)이라 O(n²)이 감당된다 | O(n²) |
| XOR 최대 쌍 | 비트 트라이 | 상위 비트에서 1을 얻는 쪽이 항상 이득 | 삽입·질의 각 O(BITS) |
| 사전순 k번째 단어(삽입이 섞임) | 트라이 서브트리 카운트 하강 | 자식 서브트리를 통째로 건너뛴다 | 삽입 O(\|w\|), 질의 O(\|답\| × 분기) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 실패 함수 `pi[i]`의 정의(접두사이면서 접미사인 최장 진부분문자열)를 예시 하나로.
- [ ] 설명할 수 있다: 불일치 시 점프량이 왜 `pi[j-1]`이고 `pi[j]`가 아닌지.
- [ ] 설명할 수 있다: KMP에서 텍스트 포인터가 왜 되돌아가지 않아도 되는지, 건너뛴 시작 위치가 왜 안전한지.
- [ ] 설명할 수 있다: KMP가 왜 O(n+m)인지를 `j`의 증가 총량과 감소 총량으로.
- [ ] 설명할 수 있다: `pi.back()`에서 최소 주기 `m - pi.back()`이 나오는 이유와, 나눠떨어짐 검사가 왜 필요한지.
- [ ] 설명할 수 있다: 구간 해시 식 `H[r+1] - H[l]*pw[r-l+1]`을 자리 이동으로 유도하는 과정.
- [ ] 설명할 수 있다: C++에서 왜 모듈러를 취해야 하는지(파이썬과 이유가 어떻게 다른지)와, 모듈러가 작으면 무엇이 깨지는지.
- [ ] 설명할 수 있다: 해시 `N`개를 모을 때 충돌 확률이 왜 `N²/(2M)` 규모인지(생일 문제)와, 이중 해시가 그것을 어떻게 낮추는지.
- [ ] 설명할 수 있다: `unsigned long long`의 자연 오버플로가 왜 안전하고, 같은 짓을 `long long`으로 하면 왜 위험한지.
- [ ] 설명할 수 있다: 트라이의 `cnt`가 왜 정확히 "그 접두어를 가진 단어 수"인지.
- [ ] 설명할 수 있다: 트라이의 모든 연산이 왜 사전 크기와 무관하게 O(문자열 길이)인지.
- [ ] 설명할 수 있다: "접두어가 있다"와 "단어가 있다"가 어떻게 다르고, 어느 값으로 구분하는지.
- [ ] 설명할 수 있다: 왜 포인터 노드보다 배열 인덱스 노드가 빠른지, 그리고 `vector` 재할당이 왜 위험한지.
- [ ] 설명할 수 있다: Manacher가 왜 구분자를 넣고, 그 덕에 `p[i]`가 왜 곧 원본 회문 길이인지.
- [ ] 설명할 수 있다: Manacher에서 `min(r-i, p[2c-i])` 클램프가 왜 필요한지.
- [ ] 설명할 수 있다: Manacher가 왜 O(n)인지를 `r`이 줄지 않는다는 사실로.
- [ ] 설명할 수 있다: 비트 트라이의 "반대 비트 우선" 그리디가 왜 최적인지를 `2^b > 2^b - 1`로.
- [ ] 설명할 수 있다: 같은 문제를 KMP로 풀지 해시로 풀지 고를 때 무엇을 근거로 삼는지.

**⚠️ 자주 하는 실수**

**1) 실패 함수 점프를 `pi[j]`로 쓴다 (인덱스 off-by-one)**

```cpp
// ❌ 틀린 코드
vector<int> failure(const string& p) {
    int m = (int)p.size();
    vector<int> pi(m, 0);
    int j = 0;
    for (int i = 1; i < m; i++) {
        while (j > 0 && p[i] != p[j]) j = pi[j];   // 한 칸 오른쪽을 읽는다
        if (p[i] == p[j]) j++;
        pi[i] = j;
    }
    return pi;
}
```

왜: `pi`의 인덱스는 "접두사의 마지막 위치"다. 지금 맞아 있는 길이가 `j`면 그 접두사는 `P[0..j-1]`이고 마지막 위치는 `j-1`이다. `pi[j]`를 읽으면 아직 비교조차 하지 않은 `P[j]`까지 포함한 값을 쓰는 셈이라 전부 한 칸씩 밀린다. 더 나쁜 것은 `P = "aaab"`처럼 같은 문자가 이어지다 다른 문자가 오는 입력이다. `i = 3`에서 `j = 2`인 채 불일치가 나는데 `pi[2] = 2`라 `j = pi[j]`가 `j`를 조금도 줄이지 못해 `while`이 영원히 돈다.

```cpp
// ✅ 고친 코드
while (j > 0 && p[i] != p[j]) j = pi[j - 1];      // 맞은 길이 j -> 마지막 위치 j-1
// pi[j-1] < j 가 항상 보장되므로 while 은 반드시 끝난다
```

**2) 마지막 원소를 파이썬처럼 `pi[-1]`로 읽는다**

```cpp
// ❌ 틀린 코드
vector<int> pi = failure(s);
int period = (int)s.size() - pi[-1];              // 음수 인덱스
```

왜: 파이썬의 `pi[-1]`은 "마지막 원소"지만 C++의 `vector::operator[]`는 **범위 검사를 전혀 하지 않는다**. `pi[-1]`은 배열 시작보다 앞 메모리를 읽어 쓰레기 값이 나오거나, 운이 나쁘면 그 자리에서 죽는다. 값이 그럴듯한 숫자로 나오면 원인 추적이 극도로 어렵다. 파이썬 코드를 옮길 때 가장 먼저 훑어야 할 패턴이다.

```cpp
// ✅ 고친 코드
int m = (int)s.size();
int border = pi.back();                            // 또는 pi[m - 1]
int period = m - border;
bool isRepeat = (period < m && m % period == 0);
// 빈 문자열이면 pi 가 비어 있으니 pi.back() 도 위험하다 — m == 0 을 먼저 거른다
```

**3) 완전 일치 후 `j`를 0으로 되돌려 겹치는 등장을 놓친다**

```cpp
// ❌ 틀린 코드
if (j == m) {
    res.push_back(i - m + 1);
    j = 0;                                         // 방금 맞은 정보를 통째로 버린다
}
```

왜: `s = "aaaaa"`, `p = "aa"`의 정답은 `0 1 2 3`인데 이 코드는 `0`과 `2`만 찾는다. 패턴 전체가 맞은 직후에도, 그 접미사 중 패턴의 접두사이기도 한 길이 `pi[m-1]`만큼은 다음 등장에 그대로 재사용할 수 있다. 0으로 리셋하면 그 재사용분이 사라져 겹치는 등장이 통째로 빠진다. 겹치지 않는 예제만 있으면 통과해 버려서 발견이 늦다.

```cpp
// ✅ 고친 코드
if (j == m) {
    res.push_back(i - m + 1);
    j = pi[j - 1];                                 // = pi[m-1], 재사용분만 남긴다
}
// "겹치지 않는 등장만" 세라는 문제면 그때만 j = 0 으로 둔다 — 조건을 먼저 확인
```

**4) 해시 곱셈을 `int`나 `long long`에서 넘치게 둔다**

```cpp
// ❌ 틀린 코드
const long long MOD = 1000000007LL;
long long h = 0;
for (char c : s) h = h * 131 + c;                  // MOD 를 안 취한다
// 또는
int h2 = 0;
for (char c : s) h2 = (h2 * 131 + c) % 1000000007; // int 곱셈이 먼저 넘친다
```

왜: `h`가 `10^9`급이면 `h * 131`만으로 `10^11`이라 `int`를 즉시 넘고, 모듈러를 아예 안 취하면 `long long`도 20글자 남짓에서 넘친다. **부호 있는 정수의 오버플로는 정의되지 않은 동작(UB)**이라 값이 감기는 것으로 끝나지 않고, 컴파일러가 "넘칠 리 없다"고 가정해 최적화 빌드에서만 답이 달라지기도 한다. 파이썬은 정수가 무한 자릿수라 이 실수 자체가 없었다.

```cpp
// ✅ 고친 코드
long long h = 0;
for (char c : s)
    h = (h * 131 + (unsigned char)c) % MOD;        // 매 단계 MOD (MOD 가 32비트급)
// MOD = (1<<61)-1 이면 __uint128_t 로 곱해 접는 mulmod61 을 쓴다
// 의도적으로 mod 2^64 를 쓰려면 반드시 unsigned long long :
unsigned long long uh = 0;
for (char c : s) uh = uh * 131ULL + (unsigned long long)(unsigned char)c;
// unsigned 의 넘침은 UB 가 아니라 표준이 정한 mod 2^64 연산이라 안전하다
```

**5) 뺄셈 결과의 음수를 그대로 둔다**

```cpp
// ❌ 틀린 코드
long long sub(int l, int r) {
    return (H[r + 1] - H[l] * pw[r - l + 1]) % MOD;   // 음수가 나올 수 있다
}
if (sub(a, b) == sub(c, d)) ...                       // 같은 구간인데 다르게 나온다
```

왜: 파이썬의 `%`는 음수 입력에도 0 이상을 돌려주지만, **C++의 `%`는 피연산자의 부호를 따라 음수를 낸다**. `-3 % 7`이 파이썬에서는 `4`, C++에서는 `-3`이다. 그래서 같은 구간의 해시가 한 번은 `-3`, 한 번은 `4`로 나와 `==` 비교가 어긋난다. 심지어 대부분의 입력에서는 우연히 양수라 통과하고, 특정 입력에서만 틀린다.

```cpp
// ✅ 고친 코드
long long sub(int l, int r) {
    long long v = (H[r + 1] - H[l] % MOD * pw[r - l + 1]) % MOD;
    return (v + MOD) % MOD;                           // 항상 0 이상으로 정규화
}
// 또는 애초에 빼기 전에 더한다: (H[r+1] + MOD - back) % MOD
// 규칙: C++ 에서 모듈러 뺄셈은 언제나 "+MOD 하고 %MOD"
```

**6) `s.size()`를 그대로 부호 있는 식에 섞는다**

```cpp
// ❌ 틀린 코드
for (int i = 0; i + m <= s.size(); i++) ...        // int 가 unsigned 로 승격
if (i - p[i] - 1 < s.size()) ...                   // 음수가 거대한 양수가 된다
for (int i = 0; i < s.size() - m; i++) ...         // m > s.size() 면 폭주
```

왜: `size()`의 반환 타입은 `size_t`(부호 없음)다. `int`와 비교하면 `int` 쪽이 부호 없는 값으로 바뀌므로, `-1`은 `18446744073709551615`가 되어 어떤 상한 검사든 통과해 버린다. 세 번째 줄은 더 나쁘다 — `s.size() - m`이 음수여야 할 상황에서 거대한 양수가 되어 루프가 배열 밖을 끝없이 훑는다. 컴파일러가 경고(`-Wsign-compare`)를 주지만 채점 환경에서는 보이지 않는다.

```cpp
// ✅ 고친 코드
int n = (int)s.size(), m = (int)p.size();          // 한 번 받아 두고 이것만 쓴다
for (int i = 0; i + m <= n; i++) ...
if (i - p[i] - 1 >= 0) ...                         // 부호 있는 정수끼리 비교
if (m > n) { /* 패턴이 더 길면 등장 없음 */ }
```

**7) 단일 모듈러 해시로 대량 비교를 한다**

```cpp
// ❌ 틀린 코드
const long long MOD = 1000000007LL;
set<long long> seen;
for (int l = 0; l + L <= n; l++)
    seen.insert(sub(l, l + L - 1));                // 값 하나만 저장
cout << seen.size() << "\n";
```

왜: 한 쌍이 충돌할 확률은 `L/MOD` 정도로 작지만, 값 `N`개를 한 집합에 넣으면 비교되는 쌍이 `N²/2`개다. `N = 10^6`, `MOD ≈ 10^9`이면 충돌 기댓값이 `N²/(2·MOD) ≈ 500`이라 사실상 확정이다(생일 문제). 서로 다른 문자열이 한 칸을 공유해 개수가 줄어드는데, 예제는 전부 맞아서 원인 추적이 어렵다.

```cpp
// ✅ 고친 코드
set<pair<u64,u64>> seen;                           // 서로 다른 (B, M) 두 쌍
for (int l = 0; l + L <= n; l++)
    seen.insert({rng(H1, pw1, MOD1, l, l + L - 1),
                 rng(H2, pw2, MOD2, l, l + L - 1)});
cout << seen.size() << "\n";                       // 유효 모듈러가 M1*M2 규모
// 또는 MOD 하나를 (1ULL<<61)-1 로 키운다
```

**8) 트라이에서 새 노드를 만들며 병렬 배열을 함께 늘리지 않는다**

```cpp
// ❌ 틀린 코드
vector<array<int,26>> nxt(1);
vector<int> cnt(1, 0);
int cur = 0;
for (char c : w) {
    int idx = c - 'a';
    if (nxt[cur][idx] == -1) {
        array<int,26> a; a.fill(-1);
        nxt.push_back(a);                          // cnt 는 안 늘렸다
        nxt[cur][idx] = (int)nxt.size() - 1;
    }
    cur = nxt[cur][idx];
    cnt[cur]++;                                    // 범위 밖 쓰기 — 메모리를 깬다
}
```

왜: 노드 번호를 `nxt.size()`로 발급하는데 `cnt`의 길이는 그대로라, 새 노드 번호가 `cnt`의 범위를 벗어난다. `vector::operator[]`는 검사를 하지 않으므로 예외 대신 **남의 메모리를 조용히 덮어쓴다**. 운이 좋으면 즉시 죽고, 나쁘면 다른 값이 망가진 채 계속 돌아 원인 추적이 불가능해진다. 파이썬이었다면 `IndexError`로 즉시 알려 줬을 자리다.

```cpp
// ✅ 고친 코드 — 노드 생성을 함수 하나로 묶어 세 배열을 항상 함께 늘린다
int newNode() {
    array<int,26> a; a.fill(-1);
    nxt.push_back(a);
    cnt.push_back(0);
    endc.push_back(0);
    return (int)nxt.size() - 1;
}
...
if (nxt[cur][idx] == -1) {
    int nn = newNode();                            // 먼저 만들고
    nxt[cur][idx] = nn;                            // 그다음 대입 (재할당 안전)
}
```

**9) Manacher에서 구분자를 넣지 않아 짝수 길이 회문을 놓친다**

```cpp
// ❌ 틀린 코드
int n = (int)s.size();
vector<int> p(n, 0);
for (int i = 0; i < n; i++) {                      // 원본 위에서 중심을 문자로만
    while (i - p[i] - 1 >= 0 && i + p[i] + 1 < n
           && s[i - p[i] - 1] == s[i + p[i] + 1])
        p[i]++;
}
int best = 0;
for (int x : p) best = max(best, 2 * x + 1);
```

왜: `abba`의 회문 중심은 두 `b` **사이**에 있고, `cbbd`의 `bb`도 마찬가지다. 원본 위에서 중심을 문자 위로만 잡으면 이런 중심은 후보에조차 들어오지 않아 짝수 길이 회문이 통째로 빠진다. `cbbd`의 답이 `2`가 아니라 `1`로 나오는 순간이 바로 이 증상이다.

```cpp
// ✅ 고친 코드
string t;
t.reserve(2 * s.size() + 1);
t.push_back('#');
for (char ch : s) { t.push_back(ch); t.push_back('#'); }   // 길이가 항상 홀수
int n = (int)t.size();
vector<int> p(n, 0);
int c = 0, r = 0;
for (int i = 0; i < n; i++) {
    if (i < r) p[i] = min(r - i, p[2 * c - i]);
    while (i - p[i] - 1 >= 0 && i + p[i] + 1 < n
           && t[i - p[i] - 1] == t[i + p[i] + 1])
        p[i]++;
    if (i + p[i] > r) { c = i; r = i + p[i]; }
}
int best = *max_element(p.begin(), p.end());       // p[i]가 곧 원본 회문 길이
```

**10) 해시가 같으면 같은 문자열이라고 단정한다**

```cpp
// ❌ 틀린 코드
for (int i = m - 1; i < n; i++) {
    if (cur == ph) res.push_back(i - m + 1);       // 해시만 보고 등장으로 확정
    cur = roll(cur, i);
}
```

왜: 해시는 임의 길이 문자열을 고정 크기 정수로 눌러 담은 압축이라, 서로 다른 문자열이 같은 값을 가질 수 있다. 패턴 검색처럼 후보가 몇 개 안 되는 상황이면 실제 비교 한 번이 O(m)이고 그런 후보 자체가 드물어 총비용이 거의 늘지 않는다. 검증 한 줄을 아껴서 얻는 것보다 잃는 것이 훨씬 크다.

```cpp
// ✅ 고친 코드
for (int i = m - 1; i < n; i++) {
    if (cur == ph && s.compare(i - m + 1, m, p) == 0)   // 후보일 때만 실제 비교
        res.push_back(i - m + 1);
    cur = roll(cur, i);
}
// 후보가 너무 많아 실제 비교가 부담이면, 검증 대신 (h1, h2) 이중 해시를 쓴다
```

**다음 챕터로**

- 이 챕터에서 "구간 하나를 O(1)에 판정하는 표"(Manacher 반지름, 접두사 해시)를 만들어 두면, 다음 챕터의 **구간 DP**에서 그 판정을 그대로 비용 함수로 꽂아 쓸 수 있다. 회문 분할 문제가 O(n³)에서 O(n²)로 내려가는 지점이 정확히 거기다.
- 비트 트라이에서 정수를 "상위 비트부터 읽는 이진 문자열"로 본 시각은, 다음 챕터의 **비트마스크**에서 정수를 "집합"으로 보는 시각으로 이어진다. 둘 다 정수 하나를 자료구조처럼 다루는 훈련이다.
- C++ 쪽에서 이 챕터가 남긴 습관은 세 가지다. **길이는 `int n = (int)s.size();`로 한 번에**, **모듈러 뺄셈은 `+MOD` 후 `%MOD`**, **음수 인덱스 대신 `back()`**.
