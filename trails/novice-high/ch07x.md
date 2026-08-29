## L2. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch07(해싱)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. 모든 문제의 공통 질문은 하나다 — "무엇을 키로 잡아야 O(n) 탐색이 O(1) 조회로 바뀌는가".
- **반복 훈련 개념**:

- 존재 판정 — `seen = set()`을 두고 `if x in seen:` 확인 후 `seen.add(x)`. "확인 → 추가" 순서가 핵심.
- 빈도 세기 — `cnt = Counter(arr)` 또는 `d[x] = d.get(x, 0) + 1`. `Counter`끼리 빼면(`a - b`) 0 이하 항목은 자동으로 사라진다.
- 집합 연산 — `A & B`(교집합), `A - B`(차집합). 출력 순서는 `sorted()`로 고정한다.
- 키→값 매핑·그룹화 — `d[key] = value`로 명령을 처리하고, `defaultdict(list)`로 같은 키끼리 모은다.
- 불변 키 — 좌표는 `(x, y)` 튜플로 `set`에 넣는다. 리스트는 키가 될 수 없다.

- **코딩테스트 출제 맵**: 프로그래머스 「코딩테스트 고득점 Kit」의 '해시'(명단 대조·접두어 충돌·장르별 상위 곡 류), NeetCode 150의 'Arrays & Hashing'(두 수의 합·가장 긴 연속 수열·부분합 개수 류), solved.ac CLASS 2~3의 집합·맵 문제가 이 레슨 수준이다.
- **문제 구성표**:

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 두 번 찍힌 첫 출입 카드 | Easy | set 존재 판정(확인→추가) | 반복 훈련 |
| 2 | 두 동아리의 겹치는 회원과 단독 회원 | Easy | set 교집합·차집합 + 정렬 출력 | 반복 훈련 |
| 3 | 기준 횟수 이상 팔린 상품 | Easy | Counter 빈도 + 조건 필터 | 반복 훈련 |
| 4 | 청소 로봇이 밟은 칸 수 | Easy | 튜플 키 set(좌표 방문) | 반복 훈련 |
| 5 | 반납되지 않은 책 | Medium | Counter 뺄셈 | 유형 확장 (프로그래머스 Kit '해시' 스타일) |
| 6 | 명령 패턴과 단어 열의 일대일 대응 | Medium | dict 양방향 매핑 | 유형 확장 (NeetCode 'Arrays & Hashing' 스타일) |
| 7 | 합이 K인 카드 쌍의 개수 | Medium | dict 빈도로 짝 개수 누적 | 반복 훈련 |
| 8 | 서로 접두어가 되는 상품 코드 | Medium | set 존재 판정 × 접두어 순회 | 유형 확장 (프로그래머스 Kit '해시' 스타일) |
| 9 | 단어장 명령 처리 | Medium | dict 삽입·삭제·조회 | 반복 훈련 |
| 10 | 가장 긴 연속 정수 구간 | Hard | set 존재 판정으로 구간 시작점 찾기 | 유형 확장 (NeetCode 'Arrays & Hashing' 스타일) |
| 11 | 합이 K인 연속 구간의 개수 | Hard | 누적합 + dict 빈도 | 유형 확장 (NeetCode 'Arrays & Hashing' 스타일) |
| 12 | 장르별 인기곡 플레이리스트 | Hard | defaultdict 그룹화 + 다중 키 정렬 | 유형 확장 (프로그래머스 Kit '해시' 스타일) |

**문제**

**1) 두 번 찍힌 첫 출입 카드** · Easy

- **요구사항**: 출입문 기록에 카드 번호가 찍힌 순서대로 주어진다. 앞에서부터 읽을 때 처음으로 "이미 찍힌 적 있는" 번호가 다시 나오는 순간, 그 번호를 출력하라. 끝까지 그런 번호가 없으면 `-1`. 리스트에 `in`으로 매번 찾지 말고 `set`으로 평균 O(n)에 해결하라.
- **입력**: 첫 줄에 기록 수 `n`(1 ≤ n ≤ 1000), 둘째 줄에 카드 번호 `n`개(1 이상 10^9 이하 정수).
- **출력**: 번호 하나 또는 `-1`.
- **예제**: `6 / 3 1 4 1 5 3` → `1` · `4 / 7 8 9 10` → `-1`
- **셀프체크**: 3도 두 번 나오지만 "두 번째 등장 시점"이 더 빠른 1이 답이다 — 값 크기가 아니라 시점 기준임을 확인하라. 확인보다 추가를 먼저 하면 첫 원소가 곧바로 중복으로 잡히는 오류가 난다. n=1이면 항상 -1.

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = [int(x) for x in data[1:1 + n]]
    seen = set()
    for x in arr:
        if x in seen:
            print(x)
            return
        seen.add(x)
    print(-1)

main()
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

- "이미 나왔는가"는 존재 판정이므로 지나온 번호를 `set`에 담아 두면 각 조회가 평균 O(1), 전체 O(n)이다. 리스트 `in`은 매번 O(n)이라 전체 O(n^2)가 된다.
- 앞에서부터 훑다가 처음 `in`이 참이 되는 순간이 곧 "가장 빠른 두 번째 등장"이므로 바로 출력하고 끝내면 된다.

(2) 코드 단계별

- 입력을 한 번에 읽어 `n`과 번호 배열을 만든다.
- 빈 `seen`을 두고 각 `x`에 대해 먼저 `x in seen`을 확인 — 참이면 출력 후 `return`.
- 거짓이면 `seen.add(x)`로 등록하고 다음으로 넘어간다.
- 반복이 끝까지 가면 중복이 없었다는 뜻이므로 `-1`.

(3) 스스로 다시 짤 때 생각 순서

- "이전에 본 적 있나?"라는 질문이 나오면 자동으로 `set`을 떠올린다.
- 확인과 추가의 순서를 먼저 고정한다(확인 → 추가). 순서를 바꾸면 첫 원소부터 오답.
- 답이 "첫 번째 시점"인지 "가장 작은 값"인지 문제 문장을 다시 읽고 확인한다. n=1, 전부 같은 값 같은 경계로 검산한다.
```

**2) 두 동아리의 겹치는 회원과 단독 회원** · Easy

- **요구사항**: 동아리 A와 B의 회원 학번 목록이 주어진다. 첫 줄에 두 동아리에 모두 속한 학번을 오름차순으로, 둘째 줄에 A에만 속한 학번을 오름차순으로 출력하라. 해당 학번이 하나도 없으면 그 줄에 `NONE`을 출력한다. 한 목록 안에 같은 학번이 여러 번 적혀 있을 수 있으며 같은 사람으로 본다.
- **입력**: 첫 줄에 `n m`(1 ≤ n, m ≤ 200), 둘째 줄에 A의 학번 `n`개, 셋째 줄에 B의 학번 `m`개(1 이상 10^6 이하 정수).
- **출력**: 두 줄. 각 줄은 공백으로 구분된 오름차순 학번 또는 `NONE`.
- **예제**: `4 3 / 101 205 333 101 / 205 999 333` → `205 333 / 101` · `2 2 / 1 2 / 1 2` → `1 2 / NONE`
- **셀프체크**: 목록을 `set`으로 바꾸는 순간 중복이 사라짐을 확인하라(101이 두 번 있어도 한 번만). `A - B`는 "A에는 있고 B에는 없는 것"이지 대칭이 아니다. 빈 집합을 `" ".join`하면 빈 줄이 되므로 `NONE` 처리를 따로 해야 한다.

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    a = set(int(x) for x in data[2:2 + n])
    b = set(int(x) for x in data[2 + n:2 + n + m])
    both = sorted(a & b)
    only_a = sorted(a - b)
    print(" ".join(str(x) for x in both) if both else "NONE")
    print(" ".join(str(x) for x in only_a) if only_a else "NONE")

main()
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

- "양쪽 모두에 있는가 / 한쪽에만 있는가"는 집합 연산 그 자체다. 두 목록을 `set`으로 만들면 `&`(교집합)와 `-`(차집합)가 평균 O(n+m)에 끝난다. 이중 반복으로 비교하면 O(n·m).
- `set`은 순서를 보장하지 않으므로 출력 전에 `sorted()`로 오름차순을 고정한다 — 정답이 유일해야 하기 때문이다.

(2) 코드 단계별

- 입력을 통째로 읽어 앞 `n`개를 A, 다음 `m`개를 B로 잘라 각각 `set`으로 만든다(중복 자동 제거).
- `a & b`로 교집합, `a - b`로 A 단독을 구하고 각각 정렬한다.
- 비어 있으면 `NONE`, 아니면 `" ".join`으로 한 줄에 출력한다.

(3) 스스로 다시 짤 때 생각 순서

- "겹치는 것 / 한쪽에만 있는 것" 문장을 보면 `&`, `-`로 번역한다.
- 중복 입력이 있어도 `set`이 알아서 하나로 합친다는 점을 확인한다.
- 출력 순서 고정(`sorted`)과 빈 결과(`NONE`) 두 가지 마무리를 잊지 않는다. B가 A를 전부 포함하는 경우(둘째 줄 `NONE`)로 검산한다.
```

**3) 기준 횟수 이상 팔린 상품** · Easy

- **요구사항**: 하루 판매 기록이 상품 코드의 나열로 주어진다. `k`번 이상 팔린 상품 코드를 사전순으로 한 줄에 하나씩 `코드 판매횟수` 형식으로 출력하라. 하나도 없으면 `NONE`.
- **입력**: 첫 줄에 `n k`(1 ≤ k ≤ n ≤ 1000), 둘째 줄에 상품 코드 `n`개(소문자·숫자로 된 길이 1~10 문자열).
- **출력**: 조건을 만족하는 코드마다 한 줄 `코드 횟수`(사전순), 또는 `NONE`.
- **예제**: `7 2 / pen cup pen bag cup pen ink` → `cup 2 / pen 3` · `3 2 / a b c` → `NONE`
- **셀프체크**: `Counter`로 한 번에 빈도표를 만든 뒤 `>= k` 필터를 거는지 확인하라. 출력 순서는 빈도가 아니라 사전순이다(`pen 3`이 `cup 2`보다 뒤). k=1이면 모든 서로 다른 코드가 출력된다.

```runner
@@SOLUTION
import sys
from collections import Counter

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    codes = data[2:2 + n]
    cnt = Counter(codes)
    picked = sorted(code for code in cnt if cnt[code] >= k)
    if not picked:
        print("NONE")
        return
    for code in picked:
        print(code, cnt[code])

main()
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

- "몇 번 나왔는가"는 빈도 세기이므로 `Counter`(코드 → 횟수)를 O(n)에 만든다. 그 다음 횟수 조건으로 거르면 끝이다.
- 출력 규칙이 "사전순"이므로 필터링한 코드들을 `sorted()`로 정렬한다. 빈도순이 아님에 주의.

(2) 코드 단계별

- 입력에서 `n`, `k`, 코드 목록을 읽는다.
- `Counter(codes)`로 빈도표를 만든다.
- 빈도가 `k` 이상인 코드만 골라 정렬한 리스트 `picked`를 만든다.
- 비어 있으면 `NONE`, 아니면 각 코드와 그 빈도를 한 줄씩 출력한다.

(3) 스스로 다시 짤 때 생각 순서

- "k번 이상"이라는 조건을 보면 빈도표부터 만든다.
- 정렬 기준이 무엇인지(사전순 vs 빈도순) 문제에서 확인하고 `sorted`의 대상을 정한다.
- 조건을 만족하는 것이 없는 경우의 출력(`NONE`)을 별도로 처리한다. k=1(전부 출력), n=1 경계로 검산한다.
```

**4) 청소 로봇이 밟은 칸 수** · Easy

- **요구사항**: 로봇이 (0, 0)에서 출발해 명령 문자열을 따라 한 칸씩 움직인다(`U`: y+1, `D`: y-1, `L`: x-1, `R`: x+1). 로봇이 한 번이라도 밟은 서로 다른 칸의 수(출발 칸 포함)와, 이미 밟았던 칸을 다시 밟은 횟수를 공백으로 구분해 출력하라.
- **입력**: 한 줄에 명령 문자열(길이 1 이상 1000 이하, `U/D/L/R`만 포함).
- **출력**: `서로다른칸수 재방문횟수`.
- **예제**: `RRUULLDD` → `8 1` · `RLRL` → `2 3`
- **셀프체크**: 좌표를 리스트 `[x, y]`로 `set`에 넣으면 오류가 난다 — 튜플 `(x, y)`여야 한다. 출발 칸을 처음부터 방문 집합에 넣어야 `RLRL`에서 되돌아올 때 재방문으로 잡힌다. 명령 한 글자짜리 입력에서 `2 0`이 나오는지 확인하라.

```runner
@@SOLUTION
import sys

def main():
    cmds = sys.stdin.readline().strip()
    move = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}
    x, y = 0, 0
    visited = {(0, 0)}
    revisit = 0
    for ch in cmds:
        dx, dy = move[ch]
        x += dx
        y += dy
        if (x, y) in visited:
            revisit += 1
        else:
            visited.add((x, y))
    print(len(visited), revisit)

main()
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

- "이 칸을 밟은 적 있는가"는 좌표에 대한 존재 판정이다. 좌표 `(x, y)`는 튜플이라 불변이므로 `set`의 원소가 될 수 있다.
- 방향 문자 → 이동량도 dict `move`로 매핑하면 `if/elif` 네 갈래가 한 줄 조회로 줄어든다.

(2) 코드 단계별

- 명령 문자열을 읽고, 방향별 `(dx, dy)`를 dict에 준비한다.
- 현재 좌표 `(0, 0)`을 방문 집합 `visited`에 미리 넣는다(출발 칸 포함).
- 각 명령마다 좌표를 갱신하고, 새 좌표가 `visited`에 있으면 `revisit += 1`, 없으면 집합에 추가한다.
- `len(visited)`가 서로 다른 칸 수, `revisit`이 재방문 횟수.

(3) 스스로 다시 짤 때 생각 순서

- 좌표를 키로 쓰려면 튜플이어야 함을 먼저 떠올린다(리스트는 해시 불가).
- 출발 칸을 방문 집합에 넣을지 말지 문제 문장("출발 칸 포함")으로 확정한다.
- 갱신 순서(이동 → 확인 → 추가)를 정하고, `RLRL`처럼 같은 두 칸을 오가는 경계로 재방문 셈을 검산한다.
```

**5) 반납되지 않은 책** · Medium

- **요구사항**: 도서관의 대여 기록(책 제목 나열)과 반납 기록이 주어진다. 같은 제목의 책이 여러 권 있을 수 있다. 반납되지 않은 책을 `제목 권수` 형식으로 사전순으로 한 줄씩 출력하라. 전부 반납됐으면 `ALL RETURNED`. 반납 기록은 항상 대여 기록의 일부다(대여한 책만 반납된다).
- **입력**: 첫 줄에 `n m`(1 ≤ n ≤ 500, 0 ≤ m ≤ n), 둘째 줄에 대여된 제목 `n`개, 셋째 줄에 반납된 제목 `m`개(소문자 문자열, m=0이면 셋째 줄 없음).
- **출력**: 미반납 책마다 한 줄 `제목 권수`(사전순), 또는 `ALL RETURNED`.
- **예제**: `5 3 / dune dune emma hamlet dune / dune hamlet dune` → `dune 1 / emma 1` · `2 2 / odyssey iliad / iliad odyssey` → `ALL RETURNED`
- **셀프체크**: `set` 차집합으로 풀면 `dune`처럼 3권 대여·2권 반납인 경우를 놓친다 — 권수까지 세야 하므로 `Counter`가 필요하다. `Counter` 뺄셈은 결과가 0 이하인 항목을 자동으로 버린다는 성질을 확인하라. m=0이면 대여 목록 전체가 답이다.

```runner
@@SOLUTION
import sys
from collections import Counter

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    rented = data[2:2 + n]
    returned = data[2 + n:2 + n + m]
    left = Counter(rented) - Counter(returned)
    if not left:
        print("ALL RETURNED")
        return
    for title in sorted(left):
        print(title, left[title])

main()
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

- "명단 A에서 명단 B를 빼되 개수까지 고려"하는 문제다. 제목만 보면 `set` 차집합 같지만 같은 제목이 여러 권이라 개수를 세야 하므로 빈도표(`Counter`)를 두 개 만들어 뺀다.
- `Counter(rented) - Counter(returned)`는 각 제목의 (대여 수 - 반납 수)를 계산하고 0 이하인 항목은 제거한다. 남은 것이 곧 미반납 목록이다. 전체 O(n + m).

(2) 코드 단계별

- 입력을 통째로 읽어 `n`, `m`, 대여 목록, 반납 목록으로 자른다(m=0이면 반납 목록은 빈 리스트).
- 두 `Counter`를 만들어 뺀 결과를 `left`에 둔다.
- `left`가 비어 있으면 `ALL RETURNED`.
- 아니면 제목을 정렬해 `제목 권수`를 한 줄씩 출력한다.

(3) 스스로 다시 짤 때 생각 순서

- "빠진 것 찾기"에서 같은 이름이 여러 개 가능하면 `set`이 아니라 `Counter`임을 먼저 판단한다.
- `Counter` 뺄셈이 0 이하를 자동으로 지운다는 성질을 이용하면 필터 코드가 필요 없다.
- 반납이 하나도 없는 경우(m=0)와 전부 반납된 경우, 두 경계를 모두 검산한다.
```

**6) 명령 패턴과 단어 열의 일대일 대응** · Medium

- **요구사항**: 패턴 문자열(소문자)과 단어 열이 주어진다. 패턴의 각 글자가 단어 하나에 **일대일**로 대응하면(같은 글자는 항상 같은 단어, 다른 글자는 항상 다른 단어) `YES`, 아니면 `NO`를 출력하라. 패턴 길이와 단어 수가 다르면 `NO`. 질의가 여러 개 주어진다.
- **입력**: 첫 줄에 질의 수 `q`(1 ≤ q ≤ 100), 이후 `q`줄에 `패턴 단어1 단어2 ...`(패턴 길이 1~50, 단어는 소문자 문자열).
- **출력**: 질의마다 한 줄에 `YES` 또는 `NO`.
- **예제**: `3 / abba dog cat cat dog / abba dog cat cat fish / aaa go go go` → `YES / NO / YES`
- **셀프체크**: 글자→단어 dict 하나만 쓰면 `ab`와 `go go`(다른 글자가 같은 단어)를 `YES`로 잘못 판정한다 — 단어→글자 dict도 함께 검사해야 일대일이 된다. 길이가 다른 경우를 맨 앞에서 걸러라. 두 dict 모두 "없으면 등록, 있으면 일치 확인" 규칙이다.

```runner
@@SOLUTION
import sys

def main():
    lines = sys.stdin.read().split('\n')
    q = int(lines[0])
    for i in range(1, q + 1):
        parts = lines[i].split()
        pattern, words = parts[0], parts[1:]
        if len(pattern) != len(words):
            print("NO")
            continue
        p2w = {}
        w2p = {}
        ok = True
        for j in range(len(pattern)):
            ch, w = pattern[j], words[j]
            if ch in p2w and p2w[ch] != w:
                ok = False
                break
            if w in w2p and w2p[w] != ch:
                ok = False
                break
            p2w[ch] = w
            w2p[w] = ch
        print("YES" if ok else "NO")

main()
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

- "같은 글자는 같은 단어"는 글자→단어 매핑(dict)으로 검사할 수 있다. 그런데 "다른 글자는 다른 단어"까지 보장하려면 반대 방향 단어→글자 매핑도 필요하다. 두 dict를 동시에 유지하면 일대일(전단사) 대응이 된다.
- 각 위치에서 두 dict를 조회·등록하는 비용이 O(1)이므로 질의 하나당 O(패턴 길이).

(2) 코드 단계별

- 줄 단위로 읽어 첫 토큰을 패턴, 나머지를 단어 목록으로 나눈다.
- 길이가 다르면 즉시 `NO`.
- `p2w`, `w2p` 두 dict를 비우고 위치 j마다: 글자가 이미 등록돼 있는데 단어가 다르면 실패, 단어가 이미 등록돼 있는데 글자가 다르면 실패. 둘 다 통과하면 양쪽에 등록.
- 끝까지 실패가 없으면 `YES`.

(3) 스스로 다시 짤 때 생각 순서

- "대응"이 한 방향인지 양방향인지 문장에서 확인한다 — 일대일이면 dict 두 개.
- 길이 불일치를 먼저 처리해 인덱스 오류를 막는다.
- `ab go go`(단어 같음, 글자 다름)와 `abba ... fish`(글자 같음, 단어 다름) 두 종류의 반례로 양쪽 검사가 모두 필요함을 검산한다.
```

**7) 합이 K인 카드 쌍의 개수** · Medium

- **요구사항**: 정수가 적힌 카드 `n`장이 있다. 서로 다른 두 장(위치가 다르면 값이 같아도 다른 카드)을 골라 합이 `K`가 되는 쌍의 개수를 구하라. 같은 값의 카드가 여러 장이면 각각 별개의 쌍으로 센다. 이중 반복 없이 평균 O(n)에 해결하라.
- **입력**: 첫 줄에 `n K`(1 ≤ n ≤ 2000, -10^6 ≤ K ≤ 10^6), 둘째 줄에 카드 값 `n`개(-10^6 이상 10^6 이하 정수).
- **출력**: 쌍의 개수(정수).
- **예제**: `6 8 / 4 4 4 3 5 1` → `4` · `3 10 / 1 2 3` → `0`
- **셀프체크**: 존재 여부(YES/NO)가 아니라 개수이므로 `set`이 아니라 "값 → 지금까지 나온 횟수" dict가 필요하다. 카드 `x`를 볼 때 `K - x`가 **이미 나온 횟수**를 더한 뒤 `x`를 등록하는 순서가 자기 자신과 짝짓기(예: K=8에서 4 한 장을 4+4로 세는 오류)를 막는다. 4가 세 장이면 4+4 쌍은 3개(첫째-둘째, 첫째-셋째, 둘째-셋째)임을 손으로 확인하라.

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    n, K = int(data[0]), int(data[1])
    cards = [int(x) for x in data[2:2 + n]]
    seen = {}
    pairs = 0
    for x in cards:
        pairs += seen.get(K - x, 0)
        seen[x] = seen.get(x, 0) + 1
    print(pairs)

main()
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
- 횟수를 O(1)에 조회하려면 값 → 등장 횟수 dict를 유지한다. 전체 O(n). 이중 반복은 O(n^2).

(2) 코드 단계별

- 입력에서 `n`, `K`, 카드 배열을 읽는다.
- 빈 dict `seen`과 `pairs = 0`으로 시작.
- 각 `x`에 대해 `seen.get(K - x, 0)`을 `pairs`에 더한 **뒤** `seen[x]`를 1 늘린다.
- 끝나면 `pairs` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "합이 K인 쌍" → 짝이 `K - x`로 결정된다는 사실을 먼저 적는다.
- 존재 여부면 `set`, 개수면 dict(빈도)로 자료구조를 고른다.
- "조회 → 등록" 순서로 자기 자신 짝짓기를 막고, 전부 0인 배열(C(4,2)=6)과 음수 포함 배열로 검산한다.
```

**8) 서로 접두어가 되는 상품 코드** · Medium

- **요구사항**: 서로 다른 상품 코드 `n`개가 있다. 어떤 코드가 다른 코드의 **접두어**이면 바코드 판독기가 혼동하므로 "충돌 코드"라 부른다(예: `12`는 `123`의 접두어). 충돌 코드(다른 코드의 접두어가 되는 코드)를 사전순으로 한 줄에 공백으로 구분해 출력하라. 없으면 `OK`.
- **입력**: 첫 줄에 `n`(1 ≤ n ≤ 500), 이후 `n`줄에 코드 하나씩(숫자·소문자로 된 길이 1~20 문자열, 모두 서로 다름).
- **출력**: 충돌 코드들(사전순, 공백 구분) 또는 `OK`.
- **예제**: `4 / 12 / 123 / 45 / 4567` → `12 45` · `3 / ab / cd / ef` → `OK`
- **셀프체크**: 모든 쌍을 비교하면 O(n^2·길이)지만, 코드 전체를 `set`에 넣고 각 코드의 접두어(길이 1 ~ 길이-1)를 하나씩 조회하면 O(n·길이^2)로 줄어듦을 확인하라. 자기 자신은 접두어로 세지 않도록 길이 범위를 `len(code)` 미만으로 둔다. `a / ab / abc`처럼 사슬이면 `a`, `ab` 둘 다 충돌이다.

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    codes = data[1:1 + n]
    table = set(codes)
    bad = set()
    for code in codes:
        for L in range(1, len(code)):
            if code[:L] in table:
                bad.add(code[:L])
    print(" ".join(sorted(bad)) if bad else "OK")

main()
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

- "어떤 코드가 다른 코드의 접두어인가"를 뒤집어 "각 코드의 접두어 중에 실제 코드가 있는가"로 묻는다. 접두어는 길이별로 최대 19개뿐이므로, 코드 전체를 `set`에 넣어 두면 각 접두어 조회가 O(1)이다.
- 접두어로 발견된 코드를 또 다른 `set`에 모으면 중복 없이 한 번씩만 기록되고, 마지막에 정렬해 출력한다.

(2) 코드 단계별

- 코드 `n`개를 읽어 리스트와 `set`(조회용) 둘 다 만든다.
- 각 코드에 대해 길이 1부터 `len(code) - 1`까지의 접두어 `code[:L]`를 만들어 `set`에 있는지 확인한다.
- 있으면 그 접두어(= 충돌하는 다른 코드)를 `bad`에 추가한다.
- `bad`가 비면 `OK`, 아니면 정렬해 공백으로 이어 출력한다.

(3) 스스로 다시 짤 때 생각 순서

- 쌍 비교(O(n^2))를 "짧은 쪽 후보를 직접 생성해 조회"로 바꿀 수 있는지 먼저 본다 — 접두어는 후보 수가 작다.
- 자기 자신을 제외하려면 접두어 길이의 상한을 `len(code)` 미만으로 둔다.
- 사슬(`a`, `ab`, `abc`)과 코드 하나뿐인 경우로 검산한다.
```

**9) 단어장 명령 처리** · Medium

- **요구사항**: 단어장에 대한 명령 `q`개를 순서대로 처리하라. `add 단어 뜻`(이미 있으면 뜻을 덮어씀), `del 단어`(없으면 무시), `find 단어`(뜻 출력, 없으면 `?`), `count`(현재 단어 수 출력). `find`와 `count`만 출력을 낸다.
- **입력**: 첫 줄에 `q`(1 ≤ q ≤ 1000), 이후 `q`줄에 명령 하나씩(단어·뜻은 공백 없는 문자열).
- **출력**: `find`·`count` 명령마다 한 줄.
- **예제**: `6 / add sol sun / find sol / add sol sunlight / find sol / del sol / find sol` → `sun / sunlight / ?` · `5 / add a 1 / add b 2 / count / del c / count` → `2 / 2`
- **셀프체크**: 없는 단어를 `d[word]`로 읽으면 `KeyError` — `d.get(word, "?")`를 쓰는지 확인하라. 없는 단어를 `del`하면 역시 오류이므로 `in` 검사가 먼저다. 같은 단어를 `add`하면 개수는 늘지 않고 뜻만 바뀐다.

```runner
@@SOLUTION
import sys

def main():
    lines = sys.stdin.read().split('\n')
    q = int(lines[0])
    book = {}
    for i in range(1, q + 1):
        parts = lines[i].split()
        cmd = parts[0]
        if cmd == "add":
            book[parts[1]] = parts[2]
        elif cmd == "del":
            if parts[1] in book:
                del book[parts[1]]
        elif cmd == "find":
            print(book.get(parts[1], "?"))
        elif cmd == "count":
            print(len(book))

main()
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

- 단어 → 뜻 매핑이므로 dict가 정답이다. 삽입(`d[k] = v`), 삭제(`del d[k]`), 조회(`d.get(k)`), 크기(`len(d)`) 모두 평균 O(1)이라 명령 수만큼 O(q)에 끝난다.
- 오류가 나는 두 지점(없는 키 읽기, 없는 키 삭제)을 `get`과 `in`으로 미리 막는 것이 이 문제의 핵심이다.

(2) 코드 단계별

- 줄 단위로 읽어 첫 토큰을 명령으로 본다.
- `add`: `book[단어] = 뜻` — 기존 키면 값만 덮어써서 개수가 늘지 않는다.
- `del`: `단어 in book`일 때만 `del`.
- `find`: `book.get(단어, "?")` 출력. `count`: `len(book)` 출력.

(3) 스스로 다시 짤 때 생각 순서

- 명령별로 dict의 어떤 연산에 대응하는지 표로 적는다(add→대입, del→삭제, find→get, count→len).
- "없는 경우"가 있는 명령(del, find)에 방어 코드를 넣는다.
- 같은 단어를 두 번 `add`한 뒤 `count`가 1인지, 명령이 `count` 하나뿐일 때 0인지 검산한다.
```

**10) 가장 긴 연속 정수 구간** · Hard

- **요구사항**: 정수 `n`개(중복 가능)가 주어진다. 값들 중에서 `x, x+1, ..., x+L-1`이 모두 존재하는 가장 긴 구간의 길이 `L`과 시작값 `x`를 출력하라. 길이가 같은 구간이 여러 개면 시작값이 가장 작은 것. 정렬 없이 `set`만으로 평균 O(n)에 해결하라.
- **입력**: 첫 줄에 `n`(1 ≤ n ≤ 2000), 둘째 줄에 정수 `n`개(-10^9 이상 10^9 이하).
- **출력**: `길이 시작값`.
- **예제**: `8 / 100 4 200 1 3 2 101 102` → `4 1` · `5 / 7 7 7 7 7` → `1 7`
- **셀프체크**: 모든 원소에서 오른쪽으로 뻗어 나가면 같은 구간을 여러 번 훑어 O(n^2)가 된다 — `x - 1`이 집합에 없는 원소(구간의 시작점)에서만 뻗어야 각 원소가 총 O(1)번만 방문된다. 중복 값은 `set`이 지우므로 길이 계산에 영향이 없다. 동점 처리(시작값 최소)를 비교문에 넣었는가?

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    nums = set(int(x) for x in data[1:1 + n])
    best_len, best_start = 0, 0
    for x in nums:
        if x - 1 in nums:
            continue
        length = 1
        while x + length in nums:
            length += 1
        if length > best_len or (length == best_len and x < best_start):
            best_len, best_start = length, x
    print(best_len, best_start)

main()
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

- 정렬하면 O(n log n)이지만, `set`에 넣으면 "x+1이 있는가"를 O(1)에 물을 수 있어 정렬 없이 구간을 이어 갈 수 있다.
- 핵심 최적화: `x - 1`이 집합에 있으면 `x`는 구간의 중간이므로 건너뛴다. 시작점에서만 오른쪽으로 뻗으면 각 원소는 구간당 한 번씩만 방문되어 전체 O(n)이다.
- 동점 규칙은 `(길이가 더 길거나) 또는 (같고 시작값이 더 작으면)` 갱신으로 처리한다.

(2) 코드 단계별

- 입력을 `set`으로 만든다(중복 제거).
- 각 `x`에 대해 `x - 1 in nums`이면 `continue`(시작점 아님).
- 시작점이면 `x + length`가 있는 동안 `length`를 늘린다.
- 더 길거나, 같은 길이인데 시작값이 작으면 최적을 갱신하고, 마지막에 `길이 시작값` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "연속된 정수"라는 구조에서 이웃 조회(`x+1`)를 `set`으로 O(1)에 할 수 있음을 떠올린다.
- 왜 시작점에서만 뻗어야 O(n)인지(각 원소가 딱 한 구간에 속함) 스스로 설명한다.
- 전부 같은 값(길이 1), 길이가 같은 구간이 여러 개, 원소 하나뿐인 경우로 검산한다.
```

**11) 합이 K인 연속 구간의 개수** · Hard

- **요구사항**: 정수 배열에서 원소 합이 정확히 `K`인 연속 부분 배열(길이 1 이상)의 개수를 구하라. 음수가 포함될 수 있으므로 투 포인터는 쓸 수 없고, 누적합과 dict로 O(n)에 해결하라.
- **입력**: 첫 줄에 `n K`(1 ≤ n ≤ 2000, -10^6 ≤ K ≤ 10^6), 둘째 줄에 정수 `n`개(-1000 이상 1000 이하).
- **출력**: 구간의 개수(정수).
- **예제**: `5 3 / 1 2 1 2 1` → `4` · `4 0 / 0 0 0 0` → `10`
- **셀프체크**: 구간 `[i+1, j]`의 합은 `prefix[j] - prefix[i]`이므로, `prefix[j]`를 볼 때 "`prefix[j] - K`가 이전에 몇 번 나왔는가"를 세면 된다 — 문제 7과 같은 뼈대임을 확인하라. 빈 접두사(합 0)를 `{0: 1}`로 미리 넣지 않으면 배열 맨 앞에서 시작하는 구간을 놓친다. 전부 0이고 K=0이면 모든 구간 n(n+1)/2개가 답이다.

```runner
@@SOLUTION
import sys

def main():
    data = sys.stdin.read().split()
    n, K = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    freq = {0: 1}
    prefix = 0
    count = 0
    for x in a:
        prefix += x
        count += freq.get(prefix - K, 0)
        freq[prefix] = freq.get(prefix, 0) + 1
    print(count)

main()
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

- 누적합 `prefix[j]`를 두면 구간 합은 두 누적합의 차다. 따라서 "합이 K인 구간"은 "차가 K인 누적합 쌍"과 같고, 이는 문제 7(합이 K인 쌍)과 똑같이 dict 빈도로 센다: 현재 누적합 `p`에서 이전에 나온 `p - K`의 횟수를 더한다.
- 음수가 있어도 누적합의 차라는 관점은 변하지 않으므로 그대로 성립한다. 전체 O(n).

(2) 코드 단계별

- `freq = {0: 1}`로 시작 — 아무 원소도 안 더한 누적합 0이 한 번 있다는 뜻(맨 앞에서 시작하는 구간용).
- 원소를 하나씩 더해 `prefix`를 갱신하고, `freq.get(prefix - K, 0)`을 `count`에 더한다.
- 그 다음 `freq[prefix]`를 1 늘린다(조회 → 등록 순서).
- 끝나면 `count` 출력.

(3) 스스로 다시 짤 때 생각 순서

- "연속 구간의 합"을 보면 누적합으로 바꿔 "두 값의 차"로 만든다.
- 차가 K인 쌍 세기는 이미 아는 패턴(dict 빈도)임을 연결한다.
- `{0: 1}` 초기화를 빼먹으면 어떤 구간을 놓치는지(첫 원소부터 시작하는 구간) 예제 `1 2 1 2 1`로 확인하고, 전부 0 케이스(10개)로 검산한다.
```

**12) 장르별 인기곡 플레이리스트** · Hard

- **요구사항**: 곡 `n`개에 대해 장르와 재생 수가 주어진다(고유 번호는 입력 순서대로 0부터). 다음 규칙으로 플레이리스트를 만들어 고유 번호를 순서대로 출력하라. (a) 장르별 총 재생 수가 큰 장르부터(동점이면 장르 이름 사전순), (b) 각 장르 안에서는 재생 수가 큰 곡부터 최대 2곡(동점이면 고유 번호가 작은 곡 먼저).
- **입력**: 첫 줄에 `n`(1 ≤ n ≤ 200), 이후 `n`줄에 `장르 재생수`(장르는 소문자 문자열, 재생수는 0 이상 10^6 이하 정수).
- **출력**: 선택된 곡의 고유 번호를 공백으로 구분해 한 줄에.
- **예제**: `5 / pop 500 / rock 600 / pop 150 / rock 800 / jazz 2500` → `4 3 1 0 2` · `4 / a 10 / b 10 / a 5 / b 5` → `0 2 1 3`
- **셀프체크**: 장르 → 곡 목록은 `defaultdict(list)`, 장르 → 총합은 dict로 두 표를 한 번의 순회에서 함께 채우는지 확인하라. 정렬 키를 `(-총합, 장르명)`, `(-재생수, 번호)`로 두면 "큰 것 먼저 + 동점 규칙"이 한 번에 처리된다. 곡이 하나뿐인 장르는 1곡만 나온다(`[:2]`가 안전하게 처리).

```runner
@@SOLUTION
import sys
from collections import defaultdict

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    songs = defaultdict(list)
    total = {}
    idx = 1
    for i in range(n):
        genre, plays = data[idx], int(data[idx + 1])
        idx += 2
        songs[genre].append((plays, i))
        total[genre] = total.get(genre, 0) + plays
    order = sorted(total, key=lambda g: (-total[g], g))
    result = []
    for g in order:
        top = sorted(songs[g], key=lambda pi: (-pi[0], pi[1]))[:2]
        for plays, i in top:
            result.append(str(i))
    print(" ".join(result))

main()
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

- 두 단계 정렬 문제다: 장르를 총 재생 수로 줄 세우고, 장르 안에서 곡을 재생 수로 줄 세운다. 이를 위해 "장르 → 그 장르의 곡들"(그룹화)과 "장르 → 총합"(빈도 합) 두 해시 표가 필요하다.
- 그룹화는 `defaultdict(list)`가 제격이다 — 없는 장르에 처음 접근해도 빈 리스트가 자동으로 생겨 `if genre not in d` 분기가 필요 없다.
- 동점 규칙은 정렬 키 튜플로 표현한다: 큰 것 먼저는 음수로, 사전순·번호순은 그대로.

(2) 코드 단계별

- 곡을 읽으며 `songs[genre]`에 `(재생수, 번호)`를 추가하고 `total[genre]`에 재생 수를 누적한다.
- 장르들을 `(-총합, 장르명)` 키로 정렬해 순서를 정한다.
- 각 장르의 곡을 `(-재생수, 번호)` 키로 정렬한 뒤 앞 2개만 잘라(`[:2]`) 번호를 결과에 추가한다.
- 번호들을 공백으로 이어 출력.

(3) 스스로 다시 짤 때 생각 순서

- "장르별로 묶어서" → 그룹화 `defaultdict(list)`, "총합 큰 순" → 별도 합계 dict를 함께 채운다.
- 정렬 규칙을 문장에서 키 튜플로 번역한다(내림차순은 부호 반전, 동점 2차 기준을 두 번째 원소로).
- 총합 동점 장르, 재생 수 동점 곡, 곡 하나뿐인 장르 세 경계를 각각 검산한다.
```
