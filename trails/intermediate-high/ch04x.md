## L5. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch04(String)의 네 무기 — Manacher(팰린드롬 반지름), String Hashing(구간 해시 O(1) 비교), KMP(실패함수), Trie(접두사 트리·비트 트라이) — 를 소재만 바꿔 **반복 훈련**하고, 코딩테스트 단골 문자열 유형으로 **확장**하는 연습 세트다.
- **반복 훈련 개념**:
  - Manacher: `t = '#' + '#'.join(s) + '#'`로 홀·짝 통일 → `p[i]`는 원본 팰린드롬 길이. 원본 구간 `s[l..r]`이 팰린드롬인지는 `p[l + r + 1] >= r - l + 1`로 O(1) 판정.
  - 접두사 해시: `H[i+1] = (H[i]*B + ord(c)) % M`, 구간 해시 `(H[r+1] - H[l]*pw[r-l+1]) % M`. 충돌 방지는 `(h1, h2)` 이중 해시 튜플.
  - 라빈-카프 롤링: `cur = (cur*B + ord(new)) % M` → 윈도가 넘치면 `cur -= ord(old) * B^m`.
  - KMP 실패함수: `while k > 0 and p[i] != p[k]: k = f[k-1]` → `f[-1]`은 최장 경계, 최소 주기는 `n - f[-1]`. `A + '#' + B` 결합으로 접두·접미 문제를 푼다.
  - Trie: `ch[cur].get(c)`로 내려가며 `cnt[node] += 1`(지나는 단어 수) / `end[node]`(끝나는 단어 수). 정수는 상위 비트부터 `ch[node] = [자식0, 자식1]`.
- **코딩테스트 출제 맵**: 백준 「단계별로 풀어보기」의 '문자열 알고리즘' 단계, NeetCode 150의 'Tries'·'Bit Manipulation' 유형, 프로그래머스 「코딩테스트 고득점 Kit」의 '해시'가 이 챕터 유형과 맞닿아 있다.
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 가장 긴 팰린드롬 부분문자열 복원 | Easy | Manacher + 원본 인덱스 복원 | 반복 훈련 |
| 2 | 회전 동치 판정 | Medium | 라빈-카프 롤링 해시(A+A) | 반복 훈련 |
| 3 | 최장 반복 부분문자열 | Medium | 이진탐색 + 구간 해시 set | 유형 확장 (백준 '문자열 알고리즘' 단계 스타일) |
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
- **셀프체크**: 변환 문자열 `t`에서 반지름 `p[i]`가 최대인 중심 `i`를 찾으면 원본 시작은 `(i - p[i]) // 2`, 길이는 `p[i]`다. "가장 왼쪽"은 `p`를 앞에서부터 훑으며 **더 클 때만**(`>`) 갱신하면 자동으로 지켜진다(`>=`로 쓰면 오른쪽 것이 선택된다). 짝수 길이 `bb`(`cbbd`)도 잡히는지 확인.

```runner
@@SOLUTION
import sys

def main():
    s = sys.stdin.read().split()[0]
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    c = r = 0
    best_len = 0
    best_i = 0
    for i in range(n):
        if i < r:
            p[i] = min(r - i, p[2 * c - i])
        while i - p[i] - 1 >= 0 and i + p[i] + 1 < n and t[i - p[i] - 1] == t[i + p[i] + 1]:
            p[i] += 1
        if i + p[i] > r:
            c, r = i, i + p[i]
        if p[i] > best_len:       # 같은 길이면 먼저 나온(왼쪽) 중심을 유지
            best_len = p[i]
            best_i = i
    start = (best_i - best_len) // 2
    print(s[start:start + best_len])

main()
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

- Manacher로 변환 문자열의 반지름 `p`를 O(N)에 구하면 `p[i]`가 곧 원본에서의 팰린드롬 길이다. 최댓값 위치 `i`에서 원본 시작 인덱스는 `(i - p[i]) // 2`.
- "같은 길이면 가장 왼쪽"은 중심 `i`가 작을수록 시작 인덱스도 작으므로, 앞에서부터 훑으며 **더 클 때만** 갱신하면 첫 번째 최댓값(가장 왼쪽)이 남는다.

(2) 코드 단계별

- `t = '#' + '#'.join(s) + '#'`로 홀·짝 팰린드롬을 통일한다.
- 표준 Manacher 루프(`min(r - i, p[2c - i])` 재활용 → 확장 → `c, r` 갱신)로 `p[i]`를 계산하면서 `p[i] > best_len`일 때만 `best_len, best_i`를 갱신.
- `start = (best_i - best_len) // 2`, `s[start:start + best_len]` 출력.

(3) 스스로 다시 짤 때 생각 순서

- 길이만 묻던 문제에서 "문자열 자체 + 동률 규칙"으로 바뀌었다 → 인덱스 복원 공식을 먼저 확정한다.
- 동률 처리는 비교 연산자 하나(`>` vs `>=`)로 갈린다. `babad`(`bab` vs `aba`)로 확인.
- 길이 1 문자열, 전부 같은 문자 등 경계에서도 공식이 맞는지 손검산.
```

**2) 회전 동치 판정** · Medium

- **요구사항**: 두 문자열 `A`, `B`가 주어진다. `A`를 왼쪽으로 `k`칸 회전한 것(앞 k글자를 뒤로 보낸 것)이 `B`와 같아지는 **가장 작은 k**(0 ≤ k < |A|)를 출력하라. 그런 k가 없으면 `-1`.
- **입력**: 첫 줄 `A`, 둘째 줄 `B` (소문자, 1 ≤ |A|, |B| ≤ 100,000).
- **출력**: 최소 회전량 k 또는 `-1`.
- **예제**: `abcde / cdeab` → `2` · `abc / acb` → `-1`
- **셀프체크**: 길이가 다르면 즉시 `-1`. `A + A`의 길이 |A| 윈도를 왼쪽부터 밀며 롤링 해시로 `B`의 해시와 비교하면 첫 일치 위치가 곧 최소 k다(`A+A`를 실제로 만들어도 길이가 2배일 뿐이니 괜찮다). 해시 일치 시 실제 슬라이스 비교로 충돌을 거르고, `k`는 `|A| - 1`까지만 본다(그 이상은 같은 회전의 반복). `aaaa / aaaa`는 `0`.

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    a = data[0]
    b = data[1] if len(data) > 1 else ''
    n = len(a)
    if n != len(b):
        print(-1)
        return
    MOD = (1 << 61) - 1
    BASE = 131
    hb = 0
    for ch in b:
        hb = (hb * BASE + ord(ch)) % MOD
    top = pow(BASE, n, MOD)         # 윈도에서 나가는 문자의 자릿값
    aa = a + a
    cur = 0
    for i in range(len(aa)):
        cur = (cur * BASE + ord(aa[i])) % MOD
        if i >= n:
            cur = (cur - ord(aa[i - n]) * top) % MOD
        if i >= n - 1:
            k = i - n + 1            # 윈도 시작 = 회전량
            if k >= n:
                break
            if cur == hb and aa[k:k + n] == b:
                print(k)
                return
    print(-1)

main()
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

- `B`의 다항식 해시 `hb`와 `top = BASE^n`을 준비한다.
- `aa = a + a`를 왼쪽부터 훑으며 `cur = cur*BASE + ord(c)`, 윈도가 n을 넘으면 나가는 문자 `aa[i-n]`에 `top`을 곱해 뺀다.
- `i >= n-1`부터 윈도 시작 `k = i - n + 1`. `k`가 n 이상이면 중단(0..n-1만 의미 있음). 해시가 같고 슬라이스도 같으면 `k` 출력.
- 끝까지 없으면 `-1`.

(3) 스스로 다시 짤 때 생각 순서

- "회전"을 보면 `A + A` 트릭을 먼저 떠올린다. 그다음은 그냥 패턴 검색이다(라빈-카프든 KMP든).
- 롤링에서 빼는 항의 자릿값이 `BASE^n`인지 `BASE^(n-1)`인지 곱하는 순서에 따라 정해진다 — 여기선 곱한 뒤 빼므로 `BASE^n`.
- `k = 0`(같은 문자열)과 길이 불일치, 전부 같은 문자 케이스를 확인.
```

**3) 최장 반복 부분문자열** · Medium

- **요구사항**: 문자열 `S`에서 **두 번 이상 등장하는**(겹쳐도 됨) 부분문자열 중 가장 긴 것의 길이를 구하라. 없으면 `0`.
- **입력**: 첫 줄에 `S` (소문자, 1 ≤ |S| ≤ 5,000).
- **출력**: 최장 반복 부분문자열의 길이.
- **예제**: `banana` → `3` · `abcd` → `0`
- **셀프체크**: "길이 L짜리 반복이 있으면 길이 L-1짜리도 있다"는 단조성이 있으므로 **길이에 대해 이진탐색**하고, 각 길이 검사는 모든 시작 위치의 구간 해시를 `set`에 넣어 중복이 나오는지로 O(N)에 한다. 총 O(N log N). 겹치는 등장(`aaaa` → `aaa`)도 허용되므로 시작 위치만 다르면 된다. 충돌 방지를 위해 이중 해시 튜플을 넣어라.

```runner
@@SOLUTION
import sys

def main():
    s = sys.stdin.read().split()[0]
    n = len(s)
    M1 = (1 << 61) - 1
    M2 = 1000000007
    B1, B2 = 131, 137
    H1 = [0] * (n + 1); P1 = [1] * (n + 1)
    H2 = [0] * (n + 1); P2 = [1] * (n + 1)
    for i in range(n):
        H1[i + 1] = (H1[i] * B1 + ord(s[i])) % M1
        P1[i + 1] = (P1[i] * B1) % M1
        H2[i + 1] = (H2[i] * B2 + ord(s[i])) % M2
        P2[i + 1] = (P2[i] * B2) % M2

    def repeats(L):                 # 길이 L 부분문자열이 두 번 이상 나오는가
        seen = set()
        for l in range(0, n - L + 1):
            r = l + L
            key = ((H1[r] - H1[l] * P1[L]) % M1, (H2[r] - H2[l] * P2[L]) % M2)
            if key in seen:
                return True
            seen.add(key)
        return False

    lo, hi = 0, n - 1               # 답의 범위 [0, n-1]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if repeats(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

main()
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
- 각 L의 판정: 모든 시작 위치의 구간 해시를 O(1)에 뽑아 `set`에 넣고 이미 있으면 반복. 접두사 해시 전처리 O(N) 후 판정 O(N), 전체 O(N log N).
- 해시만 같고 문자열이 다른 충돌을 막으려 서로 다른 (BASE, MOD) 두 쌍의 튜플을 키로 쓴다.

(2) 코드 단계별

- 두 세트의 접두사 해시 `H1/P1`, `H2/P2`를 만든다.
- `repeats(L)`: `l`을 0..n-L로 돌며 `(H[l+L] - H[l]*P[L]) % M` 두 값을 튜플로 `seen`에 넣고 중복 시 True.
- `lo=0, hi=n-1`에서 "참이면 lo=mid, 거짓이면 hi=mid-1"의 상한 탐색(`mid = (lo+hi+1)//2`로 무한 루프 방지).
- `lo` 출력(반복이 전혀 없으면 0).

(3) 스스로 다시 짤 때 생각 순서

- "최장 + 조건이 단조" → 답을 이진탐색하고 판정 함수를 빠르게 만드는 구도. 판정을 O(N)으로 만드는 도구가 구간 해시.
- 전체 문자열은 한 번밖에 못 나오므로 상한은 n-1. 길이 1 문자열은 0.
- 이진탐색 방향(상한 찾기)에 맞춰 `mid` 올림을 잊지 않는다. 겹침 허용 여부는 시작 위치 범위에 아무 제한도 안 두는 것으로 반영된다.
```

**4) 접두사·접미사 최장 겹침** · Medium

- **요구사항**: 두 문자열 `A`, `B`가 있다. `A`의 **접미사**이면서 `B`의 **접두사**인 가장 긴 문자열의 길이 `L`을 구하고, 그 겹침을 한 번만 쓰도록 이어붙인 문자열 `A + B[L:]`을 출력하라.
- **입력**: 첫 줄 `A`, 둘째 줄 `B` (소문자, 1 ≤ |A|, |B| ≤ 100,000).
- **출력**: 첫 줄에 `L`, 둘째 줄에 이어붙인 문자열.
- **예제**: `abcxyz / xyzabc` → `3 / abcxyzabc` · `hello / world` → `0 / helloworld`
- **셀프체크**: `B + '#' + A`의 실패함수 마지막 값이 답이다 — 결합 문자열 전체의 "접두사 = 접미사" 최장 길이는 곧 "B의 접두사 = A의 접미사" 최장 길이이며, 구분자 `#` 덕분에 B의 길이를 넘어가지 못한다. 순서를 `A + '#' + B`로 하면 다른 문제(A의 접두사 = B의 접미사)를 풀게 된다. `aaa / aa`처럼 B 전체가 A의 접미사인 경우 L=|B|가 나오는지 확인.

```runner
@@SOLUTION
import sys

def failure(p):
    n = len(p)
    f = [0] * n
    k = 0
    for i in range(1, n):
        while k > 0 and p[i] != p[k]:
            k = f[k - 1]
        if p[i] == p[k]:
            k += 1
        f[i] = k
    return f

def main():
    data = sys.stdin.read().split()
    a = data[0]
    b = data[1] if len(data) > 1 else ''
    f = failure(b + '#' + a)        # '#'은 두 문자열에 없는 구분자
    L = f[-1]                       # B의 접두사 == A의 접미사 최장 길이
    print(L)
    print(a + b[L:])

main()
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

- 실패함수 `f[i]`는 "그 위치까지의 접두사에서 접두사이자 접미사인 최장 길이"다. `B + '#' + A`를 만들면 이 문자열의 접두사는 B의 접두사, 접미사는 A의 접미사이므로 `f[-1]`이 정확히 "B의 접두사 = A의 접미사" 최장 길이가 된다.
- 구분자 `#`은 두 문자열에 없는 문자라, 일치 길이가 |B|를 넘어 `#`을 포함하는 일이 없다(그래서 `L ≤ min(|A|, |B|)`가 자동으로 보장된다).
- 시간 O(|A| + |B|).

(2) 코드 단계별

- 표준 `failure` 함수(`while k > 0 and 불일치: k = f[k-1]`)를 준비한다.
- `f = failure(b + '#' + a)`, `L = f[-1]`.
- `L`과 `a + b[L:]`(겹친 부분을 한 번만 쓴 결합)을 출력.

(3) 스스로 다시 짤 때 생각 순서

- "한쪽의 접미사 = 다른 쪽의 접두사" → 결합 문자열의 실패함수 마지막 값. 어느 쪽이 앞에 오는지(접두사가 되어야 하는 쪽이 앞)를 먼저 정한다.
- 구분자가 없으면 일치가 경계를 넘어 잘못된 값이 나올 수 있다 — 반드시 넣는다.
- 예제 `aaa / aa`로 B 전체가 겹치는 경계, `hello / world`로 겹침 0을 확인.
```

**5) 주기적인 접두사 나열** · Medium

- **요구사항**: 문자열 `S`의 각 접두사(길이 2 이상)에 대해, 그 접두사가 **더 짧은 문자열을 2번 이상 온전히 반복한 형태**이면 `접두사 길이 최소반복단위길이`를 한 줄에 출력하라. 접두사 길이 오름차순. 해당하는 접두사가 하나도 없으면 `NONE`.
- **입력**: 첫 줄에 `S` (소문자, 1 ≤ |S| ≤ 100,000).
- **출력**: 조건을 만족하는 접두사마다 `i p` 한 줄씩, 또는 `NONE`.
- **예제**: `aabaabaa` → `2 1 / 6 3` · `abcd` → `NONE`
- **셀프체크**: 길이 `i`인 접두사의 최소 주기 후보는 `p = i - f[i-1]`이고, `p < i`이면서 `i % p == 0`일 때만 온전한 반복이다. 실패함수는 **한 번만** 계산하면 모든 접두사의 답이 나온다(접두사마다 다시 계산하면 O(N^2)). `aaaa`는 `2 1`, `3 1`, `4 1` 세 줄이 모두 나오는지 확인.

```runner
@@SOLUTION
import sys

def main():
    s = sys.stdin.read().split()[0]
    n = len(s)
    f = [0] * n
    k = 0
    for i in range(1, n):
        while k > 0 and s[i] != s[k]:
            k = f[k - 1]
        if s[i] == s[k]:
            k += 1
        f[i] = k
    out = []
    for i in range(2, n + 1):       # 길이 i인 접두사
        p = i - f[i - 1]            # 최소 주기 후보
        if p < i and i % p == 0:
            out.append(str(i) + ' ' + str(p))
    print('\n'.join(out) if out else "NONE")

main()
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
- `i`를 2..n으로 돌며 `p = i - f[i-1]`, 조건 `p < i and i % p == 0`이면 `"i p"`를 모은다.
- 모은 것이 없으면 `NONE`, 있으면 줄바꿈으로 이어 출력.

(3) 스스로 다시 짤 때 생각 순서

- "접두사마다 주기" → 실패함수는 원래 접두사별 정보이므로 재계산 없이 한 번에 끝남을 인식한다.
- 최소 주기 공식 `n - f[-1]`과 온전한 반복 조건(나눠떨어짐)을 접두사 길이 `i`에 맞춰 옮겨 쓴다.
- 길이 1 문자열(출력할 접두사 없음 → `NONE`)과 전부 같은 문자(모든 길이가 해당) 경계 확인.
```

**6) 가장 짧은 고유 접두어** · Medium

- **요구사항**: 서로 다른 단어 `N`개가 주어진다. 각 단어에 대해, **그 단어만의 접두어**(다른 어떤 단어의 접두어도 아닌 가장 짧은 접두어)를 출력하라. 어떤 단어가 다른 단어의 접두어이면(끝까지 가도 유일해지지 않으면) 단어 전체를 출력한다.
- **입력**: 첫 줄 `N` (1 ≤ N ≤ 10,000), 이후 N줄에 소문자 단어(총 길이 합 ≤ 1,000,000).
- **출력**: 입력 순서대로 단어마다 한 줄.
- **예제**: `4 / apple / apply / banana / bandana` → `apple / apply / bana / band` · `2 / car / card` → `car / card`
- **셀프체크**: 삽입 때 지나는 노드마다 `cnt += 1` 해 두면, 단어를 따라 내려가다 **처음으로 `cnt == 1`이 되는 노드**까지가 고유 접두어다. `car`는 `card` 때문에 끝까지 `cnt`가 2라 단어 전체가 답이고, `card`는 `d`에서 1이 되어 `card`. 단어가 하나뿐이면 첫 글자에서 바로 유일해진다(`zoo` → `z`).

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    words = data[1:1 + n]
    ch = [{}]
    cnt = [0]
    for w in words:
        cur = 0
        for c in w:
            nxt = ch[cur].get(c)
            if nxt is None:
                nxt = len(ch)
                ch[cur][c] = nxt
                ch.append({})
                cnt.append(0)
            cur = nxt
            cnt[cur] += 1            # 이 접두어를 가진 단어 수
    out = []
    for w in words:
        cur = 0
        ans = w                      # 끝까지 유일해지지 않으면 단어 전체
        for i, c in enumerate(w):
            cur = ch[cur][c]
            if cnt[cur] == 1:
                ans = w[:i + 1]
                break
        out.append(ans)
    print('\n'.join(out))

main()
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

- 배열 Trie(`ch`: 노드별 `{글자: 자식}`, `cnt`: 노드별 통과 단어 수)에 모든 단어를 넣는다.
- 각 단어를 다시 따라 내려가며 `cnt[cur] == 1`인 첫 위치 `i`에서 `w[:i+1]`을 답으로 확정하고 중단.
- 끝까지 못 찾으면 초기값 `w`(전체)를 그대로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "고유 접두어" → 접두어별 개수가 필요 → Trie `cnt`. 두 패스(삽입 → 조회)로 나눈다.
- 유일해지지 않는 경우의 규칙(단어 전체)을 초기값으로 두면 분기가 줄어든다.
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
import sys

def main():
    s = sys.stdin.read().split()[0]
    n = len(s)
    t = '#' + '#'.join(s) + '#'
    m = len(t)
    p = [0] * m
    c = r = 0
    for i in range(m):
        if i < r:
            p[i] = min(r - i, p[2 * c - i])
        while i - p[i] - 1 >= 0 and i + p[i] + 1 < m and t[i - p[i] - 1] == t[i + p[i] + 1]:
            p[i] += 1
        if i + p[i] > r:
            c, r = i, i + p[i]

    def is_pal(lo, hi):             # s[lo..hi]가 팰린드롬인가 (O(1))
        return p[lo + hi + 1] >= hi - lo + 1

    ans = 0
    for i in range(n - 1):          # 앞 조각 s[0..i], 뒤 조각 s[i+1..n-1]
        if is_pal(0, i) and is_pal(i + 1, n - 1):
            ans += 1
    print(ans)

main()
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
- `is_pal(lo, hi)`: `p[lo + hi + 1] >= hi - lo + 1`.
- `i`를 0..n-2로 돌며 `is_pal(0, i) and is_pal(i+1, n-1)`이면 카운트.

(3) 스스로 다시 짤 때 생각 순서

- "여러 구간의 팰린드롬 판정" → 구간 DP O(N^2) 대신 Manacher + 중심 공식 O(1)을 떠올린다.
- 중심 인덱스 공식은 `s[l]→2l+1`, `s[r]→2r+1`의 평균으로 직접 유도해 둔다.
- 두 조각 모두 비어 있지 않아야 하므로 `i`의 범위는 `n-2`까지. `ab`(`a|b` → 1)와 `abc`(0)로 확인.
```

**8) 앞에 붙여 만드는 최단 팰린드롬** · Hard

- **요구사항**: 문자열 `S`의 **앞에만** 문자를 붙여 팰린드롬으로 만들 때, 만들 수 있는 가장 짧은 팰린드롬을 출력하라.
- **입력**: 첫 줄에 `S` (소문자, 1 ≤ |S| ≤ 100,000).
- **출력**: 가장 짧은 결과 팰린드롬.
- **예제**: `aacecaaa` → `aaacecaaa` · `abcd` → `dcbabcd`
- **셀프체크**: 앞에 붙이는 문자는 S의 뒷부분을 뒤집은 것이어야 하므로, S의 **가장 긴 팰린드롬 접두사** 길이 `L`을 찾으면 답은 `S[L:]을 뒤집은 것 + S`다. 팰린드롬 접두사 = "S의 접두사이면서 rev(S)의 접미사"이므로 `S + '#' + rev(S)`의 실패함수 마지막 값이 `L`이다. 구분자가 없으면 `L`이 |S|를 넘을 수 있어 틀린다. `aba`처럼 이미 팰린드롬이면 그대로 나오는지 확인.

```runner
@@SOLUTION
import sys

def main():
    s = sys.stdin.read().split()[0]
    combo = s + '#' + s[::-1]
    n = len(combo)
    f = [0] * n
    k = 0
    for i in range(1, n):
        while k > 0 and combo[i] != combo[k]:
            k = f[k - 1]
        if combo[i] == combo[k]:
            k += 1
        f[i] = k
    L = f[-1]                       # s의 가장 긴 팰린드롬 접두사 길이
    print(s[L:][::-1] + s)

main()
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
- "팰린드롬 접두사"는 "S의 접두사 = rev(S)의 접미사"와 같으므로 `S + '#' + rev(S)`의 실패함수 마지막 값 `L`이 최장 팰린드롬 접두사 길이다. 답은 `rev(S[L:]) + S`. 시간 O(N).
- `aacecaaa`는 접두사 `aacecaa`(7)가 팰린드롬 → 남은 `a`를 뒤집어 앞에 붙여 `aaacecaaa`.

(2) 코드 단계별

- `combo = s + '#' + s[::-1]`를 만들고 실패함수를 계산한다.
- `L = f[-1]`.
- `s[L:][::-1] + s` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "앞에 붙여 팰린드롬" → 최장 팰린드롬 접두사 문제로 바꾼다.
- 팰린드롬 접두사 = 접두사와 뒤집은 문자열의 접미사 일치 → 결합 + 실패함수. 구분자 필수.
- 이미 팰린드롬인 경우(`L = n`, 아무것도 안 붙임)와 길이 1을 확인.
```

**9) 부분 배열 XOR 최댓값** · Hard

- **요구사항**: 음이 아닌 정수 배열에서 **연속 부분 배열**(길이 1 이상)의 원소들을 모두 XOR한 값의 최댓값을 구하라.
- **입력**: 첫 줄 `N` (1 ≤ N ≤ 100,000), 둘째 줄에 정수 N개(각 0 ≤ x < 2^31).
- **출력**: 부분 배열 XOR의 최댓값.
- **예제**: `4 / 8 1 2 12` → `15` · `3 / 5 5 5` → `5`
- **셀프체크**: 누적 XOR `px[i] = a[0] ^ … ^ a[i-1]`을 두면 부분 배열 `[l, r]`의 XOR는 `px[r+1] ^ px[l]`이다. 즉 "누적값들 중 두 개를 골라 XOR 최대"로 바뀌고, 이는 비트 트라이로 O(N·31)에 푼다. **`px[0] = 0`을 먼저 트라이에 넣어야** 배열 처음부터 시작하는 부분 배열이 포함된다. 모든 원소가 0이면 답 0.

```runner
@@SOLUTION
import sys

BITS = 31

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = [int(x) for x in data[1:1 + n]]
    ch = [[-1, -1]]

    def insert(x):
        cur = 0
        for b in range(BITS - 1, -1, -1):
            bit = (x >> b) & 1
            if ch[cur][bit] == -1:
                ch[cur][bit] = len(ch)
                ch.append([-1, -1])
            cur = ch[cur][bit]

    def query(x):                   # 트라이 안의 값과 x의 XOR 최댓값
        cur = 0
        val = 0
        for b in range(BITS - 1, -1, -1):
            bit = (x >> b) & 1
            want = 1 - bit
            if ch[cur][want] != -1:
                val |= (1 << b)
                cur = ch[cur][want]
            else:
                cur = ch[cur][bit]
        return val

    insert(0)                       # 빈 접두사의 누적 XOR
    px = 0
    best = 0
    for x in nums:
        px ^= x
        q = query(px)
        if q > best:
            best = q
        insert(px)
    print(best)

main()
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

- 배열 트라이 `ch[node] = [자식0, 자식1]`, `insert`/`query`는 최대 XOR 쌍과 동일.
- `insert(0)` 후 원소를 순회하며 `px ^= x`, `query(px)`로 최댓값 갱신, `insert(px)`.
- `best` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "연속 부분 배열의 XOR" → 누적 XOR로 두 점 문제로 변환(누적합 사고를 XOR에 이식).
- 두 점 XOR 최대 → 비트 트라이 그리디. 삽입 전 질의 순서로 중복 없이 쌍을 센다.
- 함정: 0을 미리 넣지 않으면 첫 원소부터 시작하는 구간을 놓친다. 전부 0이면 답 0.
```

**10) 사전순 k번째 단어** · Hard

- **요구사항**: 처음엔 비어 있는 단어 집합에 대해 다음 두 종류의 명령을 순서대로 처리하라. `+ w`: 단어 `w`를 집합에 넣는다(이미 있으면 무시). `? k`: 현재 집합의 단어들을 사전순으로 나열했을 때 `k`번째(1부터) 단어를 출력한다. 단어가 `k`개 미만이면 `-1`.
- **입력**: 첫 줄 `Q` (1 ≤ Q ≤ 100,000), 이후 Q줄에 명령(단어는 소문자, 총 길이 합 ≤ 1,000,000).
- **출력**: `?` 명령마다 한 줄.
- **예제**: `7 / + banana / + apple / ? 1 / + app / ? 1 / ? 3 / ? 4` → `apple / app / banana / -1` · `4 / + b / + a / + a / ? 2` → `b`
- **셀프체크**: 삽입이 질의 사이에 섞이므로 매번 정렬하면 느리다. Trie에 노드별 **서브트리 단어 수 `cnt`**를 두면, 루트에서 내려가며 "이 노드에서 끝나는 단어가 있으면 그것이 1번째", 그다음 자식을 **글자 순으로** 보며 `k <= cnt[자식]`이면 들어가고 아니면 `k -= cnt[자식]`으로 건너뛴다. 중복 삽입을 무시하지 않으면 `cnt`가 부풀어 틀린다. 루트의 `cnt`가 전체 단어 수이므로 `k > cnt[0]`이면 `-1`.

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split('\n')
    q = int(data[0])
    ch = [{}]
    cnt = [0]        # 이 노드 아래(자기 포함)에서 끝나는 단어 수
    end = [0]        # 이 노드에서 끝나는 단어가 있는가
    out = []
    for i in range(1, q + 1):
        parts = data[i].split()
        if parts[0] == '+':
            w = parts[1]
            cur = 0
            exists = True
            for c in w:
                nxt = ch[cur].get(c)
                if nxt is None:
                    exists = False
                    break
                cur = nxt
            if exists and end[cur]:
                continue              # 이미 있는 단어는 무시
            cur = 0
            cnt[0] += 1
            for c in w:
                nxt = ch[cur].get(c)
                if nxt is None:
                    nxt = len(ch)
                    ch[cur][c] = nxt
                    ch.append({})
                    cnt.append(0)
                    end.append(0)
                cur = nxt
                cnt[cur] += 1
            end[cur] = 1
        else:
            k = int(parts[1])
            if k > cnt[0]:
                out.append("-1")
                continue
            cur = 0
            res = []
            while True:
                if end[cur]:
                    if k == 1:
                        break         # 이 노드에서 끝나는 단어가 답
                    k -= 1
                for c in sorted(ch[cur]):
                    nxt = ch[cur][c]
                    if k <= cnt[nxt]:
                        res.append(c)
                        cur = nxt
                        break
                    k -= cnt[nxt]
            out.append(''.join(res))
    print('\n'.join(out))

main()
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

- `+ w`: 먼저 따라 내려가 이미 끝 표시가 있으면 무시. 아니면 루트 `cnt` 포함 지나는 모든 노드의 `cnt`를 1 올리고 마지막 노드에 `end = 1`.
- `? k`: `k > cnt[0]`이면 `-1`. 아니면 루트에서 시작해 `end[cur]`이면 `k == 1`일 때 종료·아니면 `k -= 1`, 자식을 글자 순으로 보며 들어가거나 건너뛴다. 내려가며 모은 글자가 답.
- 결과를 모아 한 번에 출력.

(3) 스스로 다시 짤 때 생각 순서

- "동적 집합 + 순위(k번째)" → 서브트리 크기를 들고 있는 트리에서 하강. 문자열이므로 Trie + `cnt`.
- 노드에서 끝나는 단어를 먼저 처리한 뒤 자식으로 가는 순서가 사전순임을 확인(`app` < `apple`).
- 함정: 중복 삽입 시 `cnt`가 부풀지 않게 존재 확인 먼저. 빈 집합 질의는 `-1`.
```
