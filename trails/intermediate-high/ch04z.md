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
         cnt[v] = words passing v , end[v] = words ending at v
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

  X + '#' + Y     pi[-1] = longest prefix of X that is a suffix of Y
     P + '#' + S     -> where does P sit inside S
     B + '#' + A     -> overlap when gluing A then B
     S + '#' + rev(S)-> longest palindromic prefix of S
  A + A           search B here -> rotation, first hit = smallest k
  # '#' must appear in neither side, or a match leaks across the seam
```

**뼈대 코드**

1) KMP — 실패 함수 + 매칭 + 주기

```python
def failure(p):                              # 실패 함수(LPS) 배열, O(m)
    m = len(p)
    pi = [0] * m
    j = 0                                    # 지금까지 맞은 접두사 길이
    for i in range(1, m):
        while j > 0 and p[i] != p[j]:
            j = pi[j - 1]                    # pi[j]가 아니다 — 한 칸 왼쪽
        if p[i] == p[j]:
            j += 1
        pi[i] = j
    return pi

def kmp_all(s, p):                           # 겹치는 등장까지 전부, O(n + m)
    pi = failure(p)
    m = len(p)
    res, j = [], 0
    for i in range(len(s)):
        while j > 0 and s[i] != p[j]:
            j = pi[j - 1]                    # 텍스트 포인터 i는 그대로
        if s[i] == p[j]:
            j += 1
        if j == m:
            res.append(i - m + 1)            # ← 1-indexed 출력이면 +1
            j = pi[j - 1]                    # 0이 아니다 — 겹침을 보존
    return res

pi = failure(s)                              # 문자열 자신에게 쓰면 주기가 나온다
n = len(s)
period = n - pi[-1]                          # 밀어도 포개지는 최소 칸 수
is_repeat = (period < n and n % period == 0) # 온전한 반복인가
```

2) 롤링 해시 — 접두사 전처리 + 구간 해시 + 이중 해시

```python
MOD1, MOD2 = (1 << 61) - 1, 1000000007
B1, B2 = 131, 137                            # ← 알파벳 크기보다 큰 서로 다른 소수

def build(s, base, mod):
    n = len(s)
    H = [0] * (n + 1)
    pw = [1] * (n + 1)
    for i in range(n):
        H[i + 1] = (H[i] * base + ord(s[i])) % mod
        pw[i + 1] = (pw[i] * base) % mod
    return H, pw

def rng(H, pw, mod, l, r):                   # s[l..r] 해시 (r 포함)
    return (H[r + 1] - H[l] * pw[r - l + 1]) % mod   # % 를 반드시 붙인다

H1, pw1 = build(s, B1, MOD1)
H2, pw2 = build(s, B2, MOD2)

def key(l, r):                               # 이중 해시 튜플 = 사실상 충돌 없음
    return (rng(H1, pw1, MOD1, l, r), rng(H2, pw2, MOD2, l, r))

# 창을 밀며 갱신하는 라빈-카프(패턴 하나만 찾을 때)
top = pow(B1, m, MOD1)                       # 나가는 문자의 자릿값
cur = 0
for i in range(len(s)):
    cur = (cur * B1 + ord(s[i])) % MOD1
    if i >= m:
        cur = (cur - ord(s[i - m]) * top) % MOD1
    if i >= m - 1 and cur == ph and s[i - m + 1:i + 1] == p:   # 실제 비교로 확인
        ...                                  # ← 기록할 내용은 문제마다 바뀜
```

3) 트라이 — 삽입·단어 검색·접두어 카운트

```python
ch = [{}]                                    # ch[node][글자] = 자식 노드 번호
cnt = [0]                                    # 이 노드를 지나간 단어 수
end = [0]                                    # 이 노드에서 끝나는 단어 수

def add(w):
    cur = 0
    for c in w:
        nxt = ch[cur].get(c)
        if nxt is None:
            nxt = len(ch)
            ch[cur][c] = nxt
            ch.append({})                    # 세 배열을 항상 함께 늘린다
            cnt.append(0)
            end.append(0)
        cur = nxt
        cnt[cur] += 1
    end[cur] += 1                            # ← 중복을 무시하려면 1로 고정

def count_prefix(p):                         # p로 시작하는 단어 수
    cur = 0
    for c in p:
        nxt = ch[cur].get(c)
        if nxt is None:
            return 0                         # 경로가 끊기면 0
        cur = nxt
    return cnt[cur]

def has_word(w):                             # '단어가 있나'는 도달만으로 부족
    cur = 0
    for c in w:
        nxt = ch[cur].get(c)
        if nxt is None:
            return False
        cur = nxt
    return end[cur] > 0                      # 접두어 존재와 단어 존재는 다르다
```

4) Manacher — 구분자 + 반지름 배열 + 구간 회문 O(1) 판정

```python
def manacher(s):
    t = '#' + '#'.join(s) + '#'              # 구분자 필수 — 짝수 길이 회문 통일
    n = len(t)
    p = [0] * n
    c = r = 0                                # 최우측 회문의 중심 c, 오른끝 r
    for i in range(n):
        if i < r:
            p[i] = min(r - i, p[2 * c - i])  # min 클램프 필수
        while (i - p[i] - 1 >= 0 and i + p[i] + 1 < n
               and t[i - p[i] - 1] == t[i + p[i] + 1]):
            p[i] += 1
        if i + p[i] > r:
            c, r = i, i + p[i]
    return p                                 # p[i] = 원본에서의 회문 길이

p = manacher(s)

def is_pal(l, r):                            # s[l..r]가 회문인가 — O(1)
    return p[l + r + 1] >= r - l + 1         # 중심 인덱스는 l + r + 1

best = max(p)                                # ← 길이만 필요하면 여기까지
i = p.index(best)                            # ← 문자열 자체가 필요하면
start = (i - best) // 2                      #    s[start:start + best]
```

5) 비트 트라이 — XOR 최대

```python
BITS = 30                                    # ← 값의 상한에 맞춰 조정
bt = [[-1, -1]]                              # bt[node] = [자식0, 자식1]

def bt_insert(x):
    cur = 0
    for b in range(BITS - 1, -1, -1):        # 반드시 상위 비트부터
        d = (x >> b) & 1
        if bt[cur][d] == -1:
            bt[cur][d] = len(bt)
            bt.append([-1, -1])
        cur = bt[cur][d]

def bt_max_xor(x):                           # 트라이 안의 값과 x의 XOR 최댓값
    cur, val = 0, 0
    for b in range(BITS - 1, -1, -1):
        d = (x >> b) & 1
        if bt[cur][1 - d] != -1:             # 반대 비트를 최우선으로
            val |= 1 << b
            cur = bt[cur][1 - d]
        else:
            cur = bt[cur][d]                 # 없으면 어쩔 수 없이 같은 비트
    return val

bt_insert(0)                                 # 빈 접두사 — 빼먹으면 [0..r] 누락
acc = best = 0
for x in nums:                               # ← 누적 XOR로 구간을 두 점 문제로
    acc ^= x
    best = max(best, bt_max_xor(acc))        # 질의를 먼저, 삽입을 나중에
    bt_insert(acc)
```

**언제 무엇을 쓰나**

| 문제가 묻는 것 | 고르는 것 | 이유 | 전처리·질의 복잡도 |
| --- | --- | --- | --- |
| 한 패턴의 등장 위치 전부 | KMP | 텍스트 포인터를 되돌리지 않아 최악에도 선형 | 전처리 O(m), 검색 O(n) |
| 부분 문자열 동일 여부를 반복 질의 | 접두사(롤링) 해시 | 임의 구간이 정수 하나로 압축돼 비교가 상수 시간 | 전처리 O(n), 질의 O(1) |
| 접두어로 시작하는 단어 수 | 트라이 + `cnt` | 접두어 경로 끝 노드의 카운터를 읽기만 하면 끝 | 삽입 O(총 길이), 질의 O(\|p\|) |
| 단어가 사전에 있나 | 트라이 + `end` | 도달 여부가 아니라 끝 표시로 판정해야 정확 | 삽입 O(총 길이), 질의 O(\|w\|) |
| 가장 긴 회문 부분 문자열 | Manacher | 모든 중심의 반지름을 한 번에 얻는다 | 전처리 O(n), 조회 O(1) |
| 임의 구간이 회문인가(반복) | Manacher 반지름 배열 | `p[l+r+1] >= r-l+1` 한 줄로 판정 | 전처리 O(n), 질의 O(1) |
| 최소 주기·접두=접미 | KMP 실패 함수 `pi[-1]` | 최장 경계가 곧 주기 `n - pi[-1]` | 전처리 O(n), 질의 O(1) |
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
- [ ] 설명할 수 있다: `pi[-1]`에서 최소 주기 `n - pi[-1]`이 나오는 이유와, 나눠떨어짐 검사가 왜 필요한지.
- [ ] 설명할 수 있다: 구간 해시 식 `H[r+1] - H[l]*pw[r-l+1]`을 자리 이동으로 유도하는 과정.
- [ ] 설명할 수 있다: 왜 모듈러를 취하는지, 그리고 모듈러가 작으면 무엇이 깨지는지.
- [ ] 설명할 수 있다: 해시 `N`개를 모을 때 충돌 확률이 왜 `N²/(2M)` 규모인지(생일 문제)와, 이중 해시가 그것을 어떻게 낮추는지.
- [ ] 설명할 수 있다: 트라이의 `cnt`가 왜 정확히 "그 접두어를 가진 단어 수"인지.
- [ ] 설명할 수 있다: 트라이의 모든 연산이 왜 사전 크기와 무관하게 O(문자열 길이)인지.
- [ ] 설명할 수 있다: "접두어가 있다"와 "단어가 있다"가 어떻게 다르고, 어느 값으로 구분하는지.
- [ ] 설명할 수 있다: Manacher가 왜 구분자를 넣고, 그 덕에 `p[i]`가 왜 곧 원본 회문 길이인지.
- [ ] 설명할 수 있다: Manacher에서 `min(r-i, p[2c-i])` 클램프가 왜 필요한지.
- [ ] 설명할 수 있다: Manacher가 왜 O(n)인지를 `r`이 줄지 않는다는 사실로.
- [ ] 설명할 수 있다: 비트 트라이의 "반대 비트 우선" 그리디가 왜 최적인지를 `2^b > 2^b - 1`로.
- [ ] 설명할 수 있다: 같은 문제를 KMP로 풀지 해시로 풀지 고를 때 무엇을 근거로 삼는지.

**⚠️ 자주 하는 실수**

**1) 실패 함수 점프를 `pi[j]`로 쓴다 (인덱스 off-by-one)**

```python
# ❌ 틀린 코드
def failure(p):
    pi = [0] * len(p)
    j = 0
    for i in range(1, len(p)):
        while j > 0 and p[i] != p[j]:
            j = pi[j]            # 한 칸 오른쪽을 읽는다
        if p[i] == p[j]:
            j += 1
        pi[i] = j
    return pi
```

왜: `pi`의 인덱스는 "접두사의 마지막 위치"다. 지금 맞아 있는 길이가 `j`면 그 접두사는 `P[0..j-1]`이고 마지막 위치는 `j-1`이다. `pi[j]`를 읽으면 아직 비교조차 하지 않은 `P[j]`까지 포함한 값을 쓰는 셈이라 전부 한 칸씩 밀린다. 더 나쁜 것은 `P = "aaab"`처럼 같은 문자가 이어지다 다른 문자가 오는 입력이다. `i = 3`에서 `j = 2`인 채 불일치가 나는데 `pi[2] = 2`라 `j = pi[j]`가 `j`를 조금도 줄이지 못해 `while`이 영원히 돈다.

```python
# ✅ 고친 코드
        while j > 0 and p[i] != p[j]:
            j = pi[j - 1]        # 맞은 길이 j -> 마지막 위치 j-1
# pi[j-1] < j 가 항상 보장되므로 while 은 반드시 끝난다
```

**2) 완전 일치 후 `j`를 0으로 되돌려 겹치는 등장을 놓친다**

```python
# ❌ 틀린 코드
if j == m:
    res.append(i - m + 1)
    j = 0                        # 방금 맞은 정보를 통째로 버린다
```

왜: `s = "aaaaa"`, `p = "aa"`의 정답은 `0 1 2 3`인데 이 코드는 `0`과 `2`만 찾는다. 패턴 전체가 맞은 직후에도, 그 접미사 중 패턴의 접두사이기도 한 길이 `pi[m-1]`만큼은 다음 등장에 그대로 재사용할 수 있다. 0으로 리셋하면 그 재사용분이 사라져 겹치는 등장이 통째로 빠진다. 겹치지 않는 예제만 있으면 통과해 버려서 발견이 늦다.

```python
# ✅ 고친 코드
if j == m:
    res.append(i - m + 1)
    j = pi[j - 1]                # = pi[m-1], 재사용 가능한 만큼만 남긴다
```

**3) 단일 모듈러 해시로 대량 비교를 한다**

```python
# ❌ 틀린 코드
MOD = 1000000007
seen = set()
for l in range(n - L + 1):
    seen.add((H[l + L] - H[l] * pw[L]) % MOD)   # 값 하나만 저장
print(len(seen))
```

왜: 한 쌍이 충돌할 확률은 `L/MOD` 정도로 작지만, 값 `N`개를 한 집합에 넣으면 비교되는 쌍이 `N²/2`개다. `N = 10⁶`, `MOD ≈ 10⁹`이면 충돌 기댓값이 `N²/(2·MOD) ≈ 500`이라 사실상 확정이다(생일 문제). 서로 다른 문자열이 한 칸을 공유해 개수가 줄어드는데, 예제는 전부 맞아서 원인 추적이 어렵다.

```python
# ✅ 고친 코드
M1, M2 = (1 << 61) - 1, 1000000007
B1, B2 = 131, 137
seen = set()
for l in range(n - L + 1):
    k1 = (H1[l + L] - H1[l] * P1[L]) % M1
    k2 = (H2[l + L] - H2[l] * P2[L]) % M2
    seen.add((k1, k2))           # 유효 모듈러가 M1*M2 규모로 커진다
```

**4) 뺄셈 결과에 `% MOD`를 한쪽만 붙여 비교한다**

```python
# ❌ 틀린 코드
h1 = H[b + 1] - H[a] * pw[b - a + 1]              # % MOD 없음
h2 = (H[d + 1] - H[c] * pw[d - c + 1]) % MOD
print("YES" if h1 == h2 else "NO")                # 같은 구간인데 NO
```

왜: 두 값은 `MOD`로 나눈 나머지가 같을 뿐 정수로서는 다르다. `h1`은 음수이거나 `MOD`의 배수만큼 어긋난 큰 수라 `==` 비교에서 어긋난다. 파이썬의 `%`는 음수 입력에도 0 이상을 돌려주니 문제는 부호가 아니라 **정규화를 한쪽만 했다**는 점이다.

```python
# ✅ 고친 코드
def rng(l, r):                                    # 항상 같은 경로로 만든다
    return (H[r + 1] - H[l] * pw[r - l + 1]) % MOD

print("YES" if rng(a, b) == rng(c, d) else "NO")
```

**5) 트라이 노드를 만들며 병렬 배열을 함께 늘리지 않는다**

```python
# ❌ 틀린 코드
ch = [{}]
cnt = [0]
cur = 0
for c in w:
    if c not in ch[cur]:
        ch[cur][c] = len(ch)
        ch.append({})            # cnt 는 안 늘렸다
    cur = ch[cur][c]
    cnt[cur] += 1                # IndexError, 또는 남의 칸을 건드림
```

왜: 노드 번호를 `len(ch)`로 발급하는데 `cnt`의 길이는 그대로라, 새 노드 번호가 `cnt`의 범위를 벗어난다. 운 나쁘게 예외가 안 나는 순서로 진행되면 다른 노드의 카운터를 올려 답만 조용히 틀린다. 같은 이유로 `ch = [{}] * k`도 금물이다 — 모든 칸이 **같은 dict 하나**를 가리켜 모든 노드가 자식을 공유한다.

```python
# ✅ 고친 코드
ch, cnt, end = [{}], [0], [0]
cur = 0
for c in w:
    nxt = ch[cur].get(c)
    if nxt is None:
        nxt = len(ch)
        ch[cur][c] = nxt
        ch.append({})            # 세 배열을 한 묶음으로 늘린다
        cnt.append(0)
        end.append(0)
    cur = nxt
    cnt[cur] += 1
end[cur] += 1
```

**6) Manacher에서 구분자를 넣지 않아 짝수 길이 회문을 놓친다**

```python
# ❌ 틀린 코드
n = len(s)
p = [0] * n
for i in range(n):               # 원본 위에서 중심을 문자로만 잡는다
    while (i - p[i] - 1 >= 0 and i + p[i] + 1 < n
           and s[i - p[i] - 1] == s[i + p[i] + 1]):
        p[i] += 1
print(max(2 * x + 1 for x in p))
```

왜: `abba`의 회문 중심은 두 `b` **사이**에 있고, `cbbd`의 `bb`도 마찬가지다. 원본 위에서 중심을 문자 위로만 잡으면 이런 중심은 후보에조차 들어오지 않아 짝수 길이 회문이 통째로 빠진다. `cbbd`의 답이 `2`가 아니라 `1`로 나오는 순간이 바로 이 증상이다.

```python
# ✅ 고친 코드
t = '#' + '#'.join(s) + '#'      # 길이가 항상 홀수 2n+1, 중심은 늘 문자 위
n = len(t)
p = [0] * n
c = r = 0
for i in range(n):
    if i < r:
        p[i] = min(r - i, p[2 * c - i])
    while (i - p[i] - 1 >= 0 and i + p[i] + 1 < n
           and t[i - p[i] - 1] == t[i + p[i] + 1]):
        p[i] += 1
    if i + p[i] > r:
        c, r = i, i + p[i]
print(max(p))                    # p[i]가 곧 원본 회문 길이라 환산도 필요 없다
```

**7) 해시가 같으면 같은 문자열이라고 단정한다**

```python
# ❌ 틀린 코드
for i in range(m - 1, n):
    if cur == ph:                # 해시만 보고 등장으로 확정
        res.append(i - m + 1)
    cur = roll(cur, i)
```

왜: 해시는 임의 길이 문자열을 고정 크기 정수로 눌러 담은 압축이라, 서로 다른 문자열이 같은 값을 가질 수 있다. 패턴 검색처럼 후보가 몇 개 안 되는 상황이면 슬라이스 비교 한 번이 O(m)이고 그런 후보 자체가 드물어 총비용이 거의 늘지 않는다. 검증 한 줄을 아껴서 얻는 것보다 잃는 것이 훨씬 크다.

```python
# ✅ 고친 코드
for i in range(m - 1, n):
    if cur == ph and s[i - m + 1:i + 1] == p:   # 후보일 때만 실제 비교
        res.append(i - m + 1)
    cur = roll(cur, i)
# 후보가 너무 많아 실제 비교가 부담이면, 검증 대신 (h1, h2) 이중 해시를 쓴다
```

**다음 챕터로**

- 이 챕터에서 "구간 하나를 O(1)에 판정하는 표"(Manacher 반지름, 접두사 해시)를 만들어 두면, 다음 챕터의 **구간 DP**에서 그 판정을 그대로 비용 함수로 꽂아 쓸 수 있다. 회문 분할 문제가 O(n³)에서 O(n²)로 내려가는 지점이 정확히 거기다.
- 비트 트라이에서 정수를 "상위 비트부터 읽는 이진 문자열"로 본 시각은, 다음 챕터의 **비트마스크**에서 정수를 "집합"으로 보는 시각으로 이어진다. 둘 다 정수 하나를 자료구조처럼 다루는 훈련이다.
