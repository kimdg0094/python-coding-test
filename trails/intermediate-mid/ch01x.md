## L7. 추가 연습 — 핵심 반복 × 유형 확장

**개념**

- 이 레슨은 Ch1(중급 자료구조)의 핵심을 **반복 훈련**하고, 코딩테스트 단골 유형으로 **확장**하는 연습 세트다. 새 문법은 없다. `dict`·`set`·정렬 리스트+`bisect`·`heapq`·prev/next 포인터 배열(이중 연결 리스트)만으로 12문제를 푼다.

- **반복 훈련 개념**
- HashMap 명령 처리·그룹핑: 없는 키는 기본값으로 안전하게 읽고, 그룹은 리스트로 모은다 — `d.get(k, 0)`, `defaultdict(list)`
- TreeMap/TreeSet 대체(정렬 리스트 + bisect): "x 이하 마지막"은 `bisect_right(a, x) - 1`, "x 이상 첫"은 `bisect_left(a, x)`, k번째는 `a[k-1]`
- HashSet 존재 판정·증감: `s.add(x)`, `s.discard(x)`(없어도 조용히 통과), `len(s)`
- 힙 세 패턴: 크기 K 힙(`heapreplace`), 두 힙(최대 힙은 부호 반전), 지연 삭제(`(값, id)`를 넣고 살아 있는 id만 인정)
- 이중 연결 리스트: 센티넬 HEAD/TAIL 사이에 `nxt`/`prv`로 잇고, 삭제는 `nxt[prv[x]] = nxt[x]; prv[nxt[x]] = prv[x]`, 복원은 그 반대 `nxt[prv[x]] = x; prv[nxt[x]] = x`

- **코딩테스트 출제 맵**: 이 챕터의 유형은 프로그래머스 「코딩테스트 고득점 Kit」의 '힙'(스코빌 합치기·작업 스케줄러·양끝 삭제 큐 류), 백준 「단계별로 풀어보기」의 '우선순위 큐'·'집합과 맵' 단계, NeetCode 150의 'Heap / Priority Queue'·'Linked List'에 그대로 등장한다. 이 레슨의 유형 확장 문제는 그 대표 유형의 소재·수치·조건을 새로 만들어 재구성한 것이다.

- **문제 구성표**

| # | 문제 | 난이도 | 반복 개념 | 유형 |
|---|------|--------|-----------|------|
| 1 | 재고 명령 처리 | Easy | dict 명령 처리 + get 기본값 | 반복 훈련 |
| 2 | 동시 접속 최대 인원 | Easy | set add/discard + 최댓값 갱신 | 반복 훈련 |
| 3 | 시각별 요금 조회 | Medium | 정렬 + bisect_right로 floor 키(TreeMap 대체) | 반복 훈련 |
| 4 | 정렬 집합 k번째와 이하 최대 | Medium | 정렬 리스트 유지 + k번째·이하 탐색(TreeSet 대체) | 반복 훈련 |
| 5 | 부서별 인원과 최고 득점자 | Medium | defaultdict 그룹핑 + 동점 규칙 | 반복 훈련 |
| 6 | 카드 합성 최소 횟수 | Medium | 최소 힙 두 개 pop → 하나 push | 유형 확장 (프로그래머스 Kit '힙' 스타일) |
| 7 | 상위 K개 합 스트리밍 | Medium | 크기 K 최소 힙 + 합 유지 | 반복 훈련 |
| 8 | 줄 세우기 명령 | Medium | 센티넬 이중 연결 리스트 앞뒤 삽입·삭제 | 반복 훈련 |
| 9 | 주문 처리 총 소요 시간 | Hard | 정렬 + 힙 스케줄링(가장 짧은 작업 우선) | 유형 확장 (프로그래머스 Kit '힙' 스타일) |
| 10 | 양끝 삭제 우선순위 큐 | Hard | 두 힙 + 지연 삭제 | 유형 확장 (프로그래머스 Kit '힙' 스타일) |
| 11 | 막대 절단 후 가장 긴 조각 | Hard | 정렬 리스트 이웃 탐색 + 개수 dict + 최대 힙 지연 삭제 | 유형 확장 (NeetCode 'Heap' 스타일) |
| 12 | 카드 지우기와 되돌리기 | Hard | 이중 연결 리스트 삭제·복원 + 커서 | 유형 확장 (NeetCode 'Linked List' 스타일) |

**문제**

**1) 재고 명령 처리** · Easy

- **요구사항**: 창고 재고를 dict로 관리한다. `in x k`(품목 x를 k개 입고), `out x k`(k개 출고 — 재고가 k 미만이면 출고하지 않고 `fail` 출력), `ask x`(현재 재고 출력, 한 번도 입고된 적 없으면 0) 세 명령을 순서대로 처리한다.
- **입력**: 첫 줄 Q(1 ≤ Q ≤ 200). 이후 Q줄에 명령. 품목명은 소문자 10자 이하, k는 1 이상 1000 이하.
- **출력**: `out` 실패 시 `fail`, `ask`마다 재고를 줄마다.
- **예제**: `6 / in apple 5 / in pear 2 / out apple 3 / ask apple / out pear 5 / ask pear` → `2 / fail / 2` · `2 / ask kiwi / out kiwi 1` → `0 / fail`
- **셀프체크**: 없는 키를 `stock[x]`로 읽으면 KeyError — `get(x, 0)`으로 읽었는가? 재고가 정확히 k개일 때 출고는 성공(≥)이어야 한다. `out` 실패 시 재고를 건드리지 않는지 확인.

```runner
@@SOLUTION
import sys
def main():
    lines=sys.stdin.read().split("\n")
    q=int(lines[0])
    stock={}
    out=[]
    for i in range(1,q+1):
        parts=lines[i].split()
        op=parts[0]; name=parts[1]
        if op=="in":
            stock[name]=stock.get(name,0)+int(parts[2])
        elif op=="out":
            k=int(parts[2])
            if stock.get(name,0)>=k:
                stock[name]-=k
            else:
                out.append("fail")
        else:
            out.append(str(stock.get(name,0)))
    print("\n".join(out))
main()
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

- "품목명 → 수량"이라는 키·값 대응이 필요하고, 명령마다 특정 품목만 O(1)에 읽고 고쳐야 하므로 dict가 정답이다. 리스트로 품목을 찾으면 명령마다 O(품목 수)라 Q가 커지면 느려진다.
- 존재하지 않는 키를 읽는 경우(`ask`, `out`)가 정상 입력에 포함되므로 `get(name, 0)`으로 기본값을 주는 것이 핵심 습관이다.

(2) 코드 단계별

- 줄 단위로 읽어 첫 토큰을 명령, 둘째를 품목명으로 뗀다.
- `in`: `stock[name] = stock.get(name, 0) + k`로 없던 품목도 안전하게 누적.
- `out`: `stock.get(name, 0) >= k`일 때만 빼고, 아니면 `fail`을 기록(재고는 그대로).
- `ask`: `get(name, 0)`을 문자열로 기록. 마지막에 줄바꿈으로 합쳐 출력.

(3) 스스로 다시 짤 때 생각 순서

- "이름으로 찾아 수량을 고친다" → dict. 명령 종류를 먼저 나열하고 각각이 dict를 읽는지 쓰는지 표로 정리한다.
- 없는 키 접근이 언제 생기는지 찾아 `get` 기본값으로 막는다.
- 경계: 딱 맞게 출고(k == 재고)는 성공, 0개가 되어도 키는 남아 있어도 무방하다.
```

**2) 동시 접속 최대 인원** · Easy

- **요구사항**: 접속 로그가 순서대로 주어진다. `+ id`는 접속, `- id`는 종료다. 이미 접속 중인 id의 `+`와 접속 중이 아닌 id의 `-`는 무시한다. 로그를 모두 처리하면서 "어느 순간의 최대 동시 접속 인원"과 "마지막 시점의 접속 인원"을 출력한다.
- **입력**: 첫 줄 N(1 ≤ N ≤ 500). 이후 N줄에 `+ id` 또는 `- id`(id는 영문 소문자·숫자 20자 이하).
- **출력**: 최대 동시 접속 인원과 최종 접속 인원을 공백으로.
- **예제**: `5 / + a / + b / - a / + c / + b` → `2 2` · `3 / - x / + x / + x` → `1 1`
- **셀프체크**: 리스트로 관리하면 `in` 판정이 O(N)이라 O(N^2)이 된다 — set을 썼는가? `remove`는 없는 원소에 KeyError를 내지만 `discard`는 조용히 통과한다. 최댓값은 매 로그 처리 직후 갱신해야 한다(마지막에 한 번만 재면 틀림).

```runner
@@SOLUTION
import sys
def main():
    lines=sys.stdin.read().split("\n")
    n=int(lines[0])
    online=set()
    best=0
    for i in range(1,n+1):
        op,uid=lines[i].split()
        if op=="+":
            online.add(uid)
        else:
            online.discard(uid)
        if len(online)>best:
            best=len(online)
    print(best, len(online))
main()
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

- "지금 접속 중인 id의 집합"만 있으면 되고, 같은 id의 중복 `+`는 집합이 자동으로 흡수한다. 존재 판정·추가·삭제가 평균 O(1)인 set이 적합해 전체 O(N)이다.
- 최대 동시 접속은 상태가 바뀔 때마다 `len(online)`을 재서 최댓값을 갱신하면 된다.

(2) 코드 단계별

- 각 줄을 `op, uid`로 나눈다.
- `+`면 `add`(이미 있으면 변화 없음), `-`면 `discard`(없으면 변화 없음) — 문제의 "무시" 규칙이 두 메서드의 성질과 정확히 일치한다.
- 처리 직후 `len(online)`이 `best`보다 크면 갱신. 마지막에 `best`와 현재 크기를 출력.

(3) 스스로 다시 짤 때 생각 순서

- "누가 접속 중인가"는 순서·횟수가 아닌 존재 여부 → set.
- 무시 규칙을 add/discard의 기본 동작으로 흡수할 수 있는지 확인해 분기를 줄인다.
- 경계: 첫 로그가 `-`이면 0명, 아무도 접속하지 않으면 `0 0`.
```

**3) 시각별 요금 조회** · Medium

- **요구사항**: 요금이 바뀐 기록 N개 `(t, p)`(시각 t에 요금이 p로 바뀜)가 순서 없이 주어진다. 각 질의 시각 x에 대해 "x 이하인 가장 늦은 변경 시각"의 요금을 출력한다. x보다 이른 변경이 하나도 없으면 -1.
- **입력**: 첫 줄 N Q(1 ≤ N, Q ≤ 200). 이후 N줄에 `t p`(0 ≤ t ≤ 10^9, 시각은 서로 다름). 이후 Q줄에 질의 시각 x.
- **출력**: 질의마다 요금을 줄마다.
- **예제**: `3 3 / 10 500 / 0 300 / 20 800 / 15 / 20 / 5` → `500 / 800 / 300` · `2 2 / 5 100 / 9 200 / 4 / 9` → `-1 / 200`
- **셀프체크**: 시각으로 정렬한 뒤 `bisect_right(times, x) - 1`이 "x 이하 마지막" 위치다(x와 같은 시각의 변경도 적용되어야 하므로 left가 아니라 right). 위치가 -1이면 답 -1. 정렬 O(N log N), 질의당 O(log N).

```runner
@@SOLUTION
import sys, bisect
def main():
    data=sys.stdin.read().split()
    idx=0
    n=int(data[idx]); q=int(data[idx+1]); idx+=2
    changes=[]
    for _ in range(n):
        t=int(data[idx]); p=int(data[idx+1]); idx+=2
        changes.append((t,p))
    changes.sort()
    times=[t for t,_ in changes]
    prices=[p for _,p in changes]
    out=[]
    for _ in range(q):
        x=int(data[idx]); idx+=1
        i=bisect.bisect_right(times,x)-1
        out.append(str(prices[i]) if i>=0 else "-1")
    print("\n".join(out))
main()
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

- "x 이하인 가장 큰 키의 값"은 TreeMap의 floorEntry에 해당한다. 파이썬에는 없으므로 (시각, 요금)을 시각으로 정렬한 뒤 시각 배열에 이분탐색을 건다. 질의마다 전체를 훑으면 O(NQ)지만 정렬 한 번 + 질의당 O(log N)으로 줄어든다.
- `bisect_right(times, x)`는 "x 이하 원소 개수"이므로 그 값에서 1을 뺀 인덱스가 x 이하 마지막 변경이다.

(2) 코드 단계별

- 기록을 `(t, p)` 튜플로 모아 정렬하면 시각 오름차순이 된다.
- 시각만 뽑은 `times`와 같은 순서의 `prices`를 만든다(bisect는 키 배열이 따로 필요).
- 질의 x마다 `i = bisect_right(times, x) - 1`. `i >= 0`이면 `prices[i]`, 아니면 -1.

(3) 스스로 다시 짤 때 생각 순서

- "정렬 순서상 x 바로 아래 키" → 정렬 + bisect(TreeMap 대체)임을 알아차린다.
- 같은 시각(x == t)을 포함해야 하므로 right를 쓴다는 것을 예제 `20 → 800`으로 확인한다.
- 경계: 모든 변경보다 이른 질의는 인덱스 -1이 나오므로 반드시 검사한다. 마지막 변경 이후의 질의는 마지막 요금이 계속 적용된다.
```

**4) 정렬 집합 k번째와 이하 최대** · Medium

- **요구사항**: 처음엔 빈 정수 집합이다. `1 v`(v 삽입, 이미 있으면 무시), `2 k`(작은 쪽에서 k번째 원소 출력, 원소 수가 k 미만이면 -1), `3 x`(x 이하인 가장 큰 원소 출력, 없으면 -1)를 순서대로 처리한다.
- **입력**: 첫 줄 Q(1 ≤ Q ≤ 300). 이후 Q줄에 연산. v, x는 -10^9 이상 10^9 이하, k는 1 이상 Q 이하.
- **출력**: `2`, `3` 연산마다 결과를 줄마다.
- **예제**: `7 / 1 5 / 1 2 / 1 5 / 2 2 / 3 4 / 3 1 / 2 3` → `5 / 2 / -1 / -1` · `2 / 2 1 / 3 100` → `-1 / -1`
- **셀프체크**: 정렬 리스트를 유지하면 k번째는 `a[k-1]`로 O(1), "x 이하 최대"는 `bisect_right(a, x) - 1`. 삽입 전에 `bisect_left` 위치의 값이 v와 같은지 확인해 중복을 막았는가(집합이므로)? 중복 삽입을 허용하면 k번째가 밀린다.

```runner
@@SOLUTION
import sys, bisect
def main():
    data=sys.stdin.read().split()
    idx=0
    q=int(data[idx]); idx+=1
    a=[]
    out=[]
    for _ in range(q):
        op=int(data[idx]); v=int(data[idx+1]); idx+=2
        if op==1:
            i=bisect.bisect_left(a,v)
            if i==len(a) or a[i]!=v:
                a.insert(i,v)
        elif op==2:
            out.append(str(a[v-1]) if v<=len(a) else "-1")
        else:
            i=bisect.bisect_right(a,v)-1
            out.append(str(a[i]) if i>=0 else "-1")
    print("\n".join(out))
main()
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

- 삽입과 "k번째", "x 이하 최대" 질의가 섞여 있으므로 항상 정렬된 상태를 유지하는 TreeSet이 필요하다. 표준 라이브러리만 쓰면 정렬 리스트 + bisect로 대체한다: 위치 찾기 O(log n), 삽입은 원소 이동 때문에 O(n)이지만 Q가 작아 충분하다.
- k번째 원소는 정렬 리스트 인덱스 `k-1`이고, "x 이하 최대"는 `bisect_right(a, x) - 1` 위치다.

(2) 코드 단계별

- `1 v`: `i = bisect_left(a, v)`. `i`가 끝이거나 `a[i] != v`일 때만 `a.insert(i, v)` — 집합이므로 중복을 걸러낸다.
- `2 k`: `k <= len(a)`면 `a[k-1]`, 아니면 -1.
- `3 x`: `i = bisect_right(a, x) - 1`. `i >= 0`이면 `a[i]`, 아니면 -1(x가 모든 원소보다 작음).

(3) 스스로 다시 짤 때 생각 순서

- "정렬 순서 기반 질의 + 삽입 혼합" → 정렬 리스트 유지(TreeSet 대체).
- 각 질의를 bisect 표현으로 번역한다: 이하(≤)의 마지막은 right - 1, 이상(≥)의 처음은 left.
- 경계: 빈 집합에서의 질의, x가 최솟값보다 작을 때(-1), 음수 값. 중복 삽입 방지를 빠뜨리면 셋째 테스트처럼 같은 값이 두 번 들어가 k번째가 어긋난다.
```

**5) 부서별 인원과 최고 득점자** · Medium

- **요구사항**: 직원 N명의 `부서 이름 점수`가 주어진다. 부서별로 인원수와 최고 점수를 받은 사람의 이름을 출력한다. 최고 점수가 여러 명이면 이름이 사전순으로 앞선 사람. 부서는 부서명 사전순으로 출력한다.
- **입력**: 첫 줄 N(1 ≤ N ≤ 300). 이후 N줄에 `부서 이름 점수`(부서·이름은 소문자 15자 이하, 이름은 전체에서 유일, 0 ≤ 점수 ≤ 100).
- **출력**: 부서마다 `부서 인원수 이름`을 줄마다.
- **예제**: `5 / dev kim 80 / ops lee 90 / dev park 95 / ops choi 90 / hr yoon 70` → `dev 2 park / hr 1 yoon / ops 2 choi` · `1 / qa a 0` → `qa 1 a`
- **셀프체크**: `defaultdict(list)`로 부서 → 구성원 목록을 모았는가? 동점 규칙은 "점수 더 큼 또는 (점수 같고 이름 더 작음)"을 한 조건식으로 적는다. 출력 순서는 dict 삽입 순서가 아니라 `sorted(groups)`로 부서명 정렬.

```runner
@@SOLUTION
import sys
from collections import defaultdict
def main():
    lines=sys.stdin.read().split("\n")
    n=int(lines[0])
    groups=defaultdict(list)
    for i in range(1,n+1):
        dept,name,score=lines[i].split()
        groups[dept].append((name,int(score)))
    out=[]
    for dept in sorted(groups):
        members=groups[dept]
        best=members[0]
        for name,score in members[1:]:
            if score>best[1] or (score==best[1] and name<best[0]):
                best=(name,score)
        out.append(f"{dept} {len(members)} {best[0]}")
    print("\n".join(out))
main()
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

- "부서별로 묶어서 각 묶음의 통계"는 그룹핑 문제다. 부서명을 키로 하는 `defaultdict(list)`에 (이름, 점수)를 밀어 넣으면 한 번의 순회 O(N)으로 그룹이 완성되고, 그룹마다 최댓값을 한 번 더 훑으면 총 O(N)이다.
- 정렬로도 풀 수 있지만(부서, -점수, 이름 키로 정렬) 그룹핑이 "인원수"까지 자연스럽게 준다.

(2) 코드 단계별

- 각 줄을 부서, 이름, 점수로 나눠 `groups[dept].append((name, score))`.
- `sorted(groups)`로 부서명 사전순 순회. 첫 구성원을 `best`로 두고 나머지를 비교: 점수가 더 크거나, 같으면서 이름이 사전순으로 앞서면 교체.
- `f"{dept} {len(members)} {best[0]}"` 형식으로 기록해 출력.

(3) 스스로 다시 짤 때 생각 순서

- "~별로" 라는 단어가 보이면 키 → 리스트 그룹핑을 떠올린다.
- 동점 규칙을 비교식에 명시한다(점수 내림, 이름 오름). 셋째 테스트처럼 전원 동점이면 이름이 가장 앞선 사람.
- 경계: 부서가 하나뿐이거나 N=1인 경우, 점수 0. dict 순회 순서는 삽입 순이므로 출력 전 반드시 정렬한다.
```

**6) 카드 합성 최소 횟수** · Medium

- **요구사항**: 카드 N장의 공격력이 주어진다. 가장 약한 두 장 a ≤ b를 합성하면 공격력 `a + 2*b`인 카드 한 장이 된다. 모든 카드의 공격력이 K 이상이 될 때까지 합성을 반복할 때 최소 합성 횟수를 출력한다. 불가능하면 -1.
- **입력**: 첫 줄 N K(1 ≤ N ≤ 300, 1 ≤ K ≤ 10^9). 둘째 줄 N개의 공격력(1 이상 10^9 이하).
- **출력**: 최소 합성 횟수 또는 -1.
- **예제**: `5 7 / 1 2 3 9 10` → `2` · `1 5 / 3` → `-1`
- **셀프체크**: 최소 힙에서 두 번 pop, 합성 결과를 push하며 `h[0] >= K`가 될 때까지 반복. 처음부터 전부 K 이상이면 0회. 카드가 한 장만 남았는데 K 미만이면 -1 — "pop하기 전에" 장수를 검사했는가? 검산: {1,2,3,9,10} → 1+2·2=5 → {3,5,9,10} → 3+2·5=13 → {9,10,13} 전부 7 이상, 2회.

```runner
@@SOLUTION
import sys, heapq
def main():
    data=sys.stdin.read().split()
    n=int(data[0]); k=int(data[1])
    h=[int(data[2+i]) for i in range(n)]
    heapq.heapify(h)
    cnt=0
    while h[0]<k:
        if len(h)<2:
            print(-1); return
        a=heapq.heappop(h)
        b=heapq.heappop(h)
        heapq.heappush(h, a+2*b)
        cnt+=1
    print(cnt)
main()
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
- 종료 조건은 "현재 최솟값이 K 이상"이며, 최솟값은 `h[0]`으로 O(1)에 볼 수 있다.

(2) 코드 단계별

- 배열을 `heapify`로 O(N)에 힙화한다.
- `h[0] < K`인 동안 반복: 카드가 2장 미만이면 더 합성할 수 없으므로 -1을 출력하고 종료.
- 두 장을 pop해 `a + 2*b`를 push하고 횟수를 1 늘린다. 루프가 정상 종료되면 횟수를 출력.

(3) 스스로 다시 짤 때 생각 순서

- "반복해서 최소 두 개를 꺼내 합친다" → 최소 힙 정석 패턴(밧줄 잇기와 같은 골격, 종료 조건만 다름).
- 불가능 판정을 어디에 둘지 정한다: pop 전에 장수를 검사해야 IndexError 없이 -1을 낼 수 있다.
- 경계: 처음부터 조건을 만족하면 0회(루프에 안 들어감), 마지막 한 장이 K 미만이면 -1.
```

**7) 상위 K개 합 스트리밍** · Medium

- **요구사항**: 정수가 하나씩 들어온다. 값이 들어올 때마다 "지금까지 들어온 값 중 가장 큰 K개의 합"을 출력한다. 아직 K개 미만이면 들어온 값 전체의 합.
- **입력**: 첫 줄 N K(1 ≤ K ≤ N ≤ 500). 둘째 줄 N개의 정수(-10^6 이상 10^6 이하).
- **출력**: 각 값이 들어온 직후의 합을 공백으로 N개.
- **예제**: `5 2 / 3 1 4 1 5` → `3 4 7 7 9` · `3 5 / -1 -2 -3` → `-1 -3 -6`
- **셀프체크**: 크기 K인 "최소 힙"에 가장 큰 K개만 남긴다 — top이 K개 중 최솟값이므로 새 값이 top보다 클 때만 교체. 합은 매번 다시 더하지 말고 `합 += 새 값 - 쫓겨난 값`으로 O(1) 갱신. 상위 K는 최소 힙, 하위 K는 최대 힙이라는 방향을 헷갈리지 말 것.

```runner
@@SOLUTION
import sys, heapq
def main():
    data=sys.stdin.read().split()
    n=int(data[0]); k=int(data[1])
    h=[]
    total=0
    out=[]
    for i in range(n):
        x=int(data[2+i])
        if len(h)<k:
            heapq.heappush(h,x); total+=x
        elif x>h[0]:
            total+=x-h[0]
            heapq.heapreplace(h,x)
        out.append(str(total))
    print(" ".join(out))
main()
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

- "가장 큰 K개"만 유지하면 되므로 크기를 K로 제한한 최소 힙을 쓴다. 힙의 top은 K개 중 가장 작은 값이라, 새 값이 top보다 크면 top을 버리고 새 값을 넣는 것이 "상위 K 갱신"이다. 삽입마다 O(log K), 전체 O(N log K)(매번 정렬하면 O(N^2 log N)).
- 합은 교체될 때 "새 값 - 쫓겨난 값"만큼만 변하므로 누적 변수 하나로 O(1)에 유지한다.

(2) 코드 단계별

- 힙이 K개 미만이면 무조건 push하고 합에 더한다.
- K개가 찼으면 `x > h[0]`일 때만 `total += x - h[0]` 후 `heapreplace(h, x)`(pop과 push를 한 번에).
- 매 값 처리 직후 `total`을 기록해 공백으로 출력.

(3) 스스로 다시 짤 때 생각 순서

- "상위 K개의 합을 계속" → 크기 K 힙 + 합 누적. 전체 정렬 재계산을 피하는 것이 목적임을 먼저 인식한다.
- 방향 확인: 상위 K를 지키려면 "K개 중 최솟값"을 빨리 봐야 하므로 최소 힙.
- 경계: K > 현재 개수일 때(그냥 전체 합), 음수만 들어올 때(교체 조건 `x > h[0]`은 음수여도 그대로 성립), 같은 값 반복(교체되지 않아 합 불변).
```

**8) 줄 세우기 명령** · Medium

- **요구사항**: 빈 줄에서 시작해 사람들을 세운다. `front x`(맨 앞에 x), `back x`(맨 뒤에 x), `before y x`(y 바로 앞에 x), `after y x`(y 바로 뒤에 x), `out x`(x를 줄에서 뺌) 명령을 처리하고 최종 줄을 앞에서부터 출력한다. 아무도 없으면 `empty`.
- **입력**: 첫 줄 M(1 ≤ M ≤ 300). 이후 M줄에 명령. 이름은 영숫자 10자 이하이며, 삽입되는 x는 줄에 없고 기준 y와 `out`의 x는 반드시 줄에 있다.
- **출력**: 최종 줄의 이름들을 공백으로, 비어 있으면 `empty`.
- **예제**: `5 / back 3 / front 1 / after 1 2 / before 3 9 / out 1` → `2 9 3` · `2 / front 7 / out 7` → `empty`
- **셀프체크**: 리스트의 `insert`/`remove`는 위치 탐색과 이동 때문에 O(n)이다 — 이름 → 이웃을 dict `nxt`/`prv`로 두면 모든 명령이 O(1). HEAD/TAIL 센티넬을 두면 `front`는 "HEAD 뒤 삽입", `back`은 "TAIL 앞 삽입"으로 통일된다. 삽입 시 네 개의 링크를 모두 갱신했는가?

```runner
@@SOLUTION
import sys
def main():
    lines=sys.stdin.read().split("\n")
    m=int(lines[0])
    HEAD="__H__"; TAIL="__T__"
    nxt={HEAD:TAIL}; prv={TAIL:HEAD}
    def link(p,x,q):
        nxt[p]=x; prv[x]=p
        nxt[x]=q; prv[q]=x
    def unlink(x):
        p=prv[x]; q=nxt[x]
        nxt[p]=q; prv[q]=p
        del nxt[x]; del prv[x]
    for i in range(1,m+1):
        parts=lines[i].split()
        op=parts[0]
        if op=="front":
            link(HEAD,parts[1],nxt[HEAD])
        elif op=="back":
            link(prv[TAIL],parts[1],TAIL)
        elif op=="before":
            y,x=parts[1],parts[2]
            link(prv[y],x,y)
        elif op=="after":
            y,x=parts[1],parts[2]
            link(y,x,nxt[y])
        else:
            unlink(parts[1])
    res=[]
    cur=nxt[HEAD]
    while cur!=TAIL:
        res.append(cur); cur=nxt[cur]
    print(" ".join(res) if res else "empty")
main()
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

- 명령이 전부 "어떤 사람의 바로 앞/뒤"를 기준으로 하므로, 이름으로 노드를 바로 찾아 이웃 링크만 고치는 이중 연결 리스트가 맞다. dict 두 개(`nxt`, `prv`)를 쓰면 이름 → 이웃이 O(1)이라 명령당 O(1), 전체 O(M)이다(리스트 insert는 명령당 O(n)).
- HEAD/TAIL 센티넬 덕에 "맨 앞/맨 뒤"도 일반 삽입과 같은 코드로 처리되고, 빈 줄 검사가 사라진다.

(2) 코드 단계별

- `link(p, x, q)`: p와 q 사이에 x를 끼운다(네 링크 갱신). `unlink(x)`: x의 양 이웃을 서로 이어 붙이고 x의 항목을 지운다.
- `front x` = `link(HEAD, x, nxt[HEAD])`, `back x` = `link(prv[TAIL], x, TAIL)`, `before y x` = `link(prv[y], x, y)`, `after y x` = `link(y, x, nxt[y])`, `out x` = `unlink(x)`.
- 끝나면 HEAD 다음부터 TAIL 전까지 따라가며 이름을 모은다. 비어 있으면 `empty`.

(3) 스스로 다시 짤 때 생각 순서

- "이름 기준 앞/뒤 삽입·삭제 반복" → 이름 → 이웃 dict(이중 연결 리스트). 인덱스 기반 리스트 조작은 O(n)임을 상기한다.
- 삽입·삭제를 함수 하나씩으로 묶고, 네 명령을 그 함수의 인자 차이로 표현해 분기를 줄인다.
- 경계: 사람이 한 명일 때 `out`하면 HEAD-TAIL만 남아 `empty`. 삭제한 이름의 dict 항목을 지워 두면 잘못된 참조를 예방한다.
```

**9) 주문 처리 총 소요 시간** · Hard

- **요구사항**: 주방에 요리사가 한 명이다. 주문 N개가 `(도착 시각 a, 조리 시간 d)`로 주어진다. 요리사는 한 번에 한 주문만 처리하며, 손이 비는 순간 "이미 도착한 주문 중 조리 시간이 가장 짧은 것"(같으면 도착이 빠른 것, 그것도 같으면 입력 순서가 앞선 것)을 고른다. 도착한 주문이 없으면 다음 도착까지 쉰다. 각 주문의 소요 시간은 `완료 시각 - 도착 시각`이다. 모든 주문의 소요 시간 합을 출력한다.
- **입력**: 첫 줄 N(1 ≤ N ≤ 300). 이후 N줄에 `a d`(0 ≤ a ≤ 10^6, 1 ≤ d ≤ 10^4).
- **출력**: 소요 시간의 합.
- **예제**: `4 / 0 5 / 1 2 / 2 4 / 10 1` → `22` · `1 / 5 3` → `3`
- **셀프체크**: 도착 시각으로 정렬한 뒤, 현재 시각 t 이하로 도착한 주문을 힙에 `(d, a, 번호)`로 밀어 넣고 top을 꺼내 처리. 힙이 비었으면 t를 다음 도착 시각으로 "점프"해야 한다(1씩 증가시키면 시간 초과). 검산: t=0에 (0,5) 처리→5, t=5에 도착한 (1,2),(2,4) 중 2→7(소요 6), (2,4)→11(소요 9), (10,1)→12(소요 2), 합 5+6+9+2=22.

```runner
@@SOLUTION
import sys, heapq
def main():
    data=sys.stdin.read().split()
    n=int(data[0])
    jobs=[]
    for i in range(n):
        a=int(data[1+2*i]); d=int(data[2+2*i])
        jobs.append((a,d,i))
    jobs.sort()
    h=[]
    t=0; i=0; total=0; done=0
    while done<n:
        while i<n and jobs[i][0]<=t:
            a,d,j=jobs[i]
            heapq.heappush(h,(d,a,j)); i+=1
        if not h:
            t=jobs[i][0]
            continue
        d,a,j=heapq.heappop(h)
        t+=d
        total+=t-a
        done+=1
    print(total)
main()
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
- 우선순위 규칙 "짧은 조리 → 이른 도착 → 앞선 입력"은 튜플 `(d, a, 번호)`의 사전순 비교로 그대로 표현된다.

(2) 코드 단계별

- 주문을 `(a, d, 번호)`로 모아 도착 시각순 정렬한다.
- 현재 시각 t에서, 아직 안 넣은 주문 중 `a <= t`인 것을 모두 힙에 `(d, a, 번호)`로 넣는다.
- 힙이 비어 있으면(도착한 주문이 없음) `t`를 다음 주문의 도착 시각으로 점프하고 다시 시도.
- 힙 top을 꺼내 `t += d`, 소요 시간 `t - a`를 합산. 처리한 개수가 N이 되면 종료.

(3) 스스로 다시 짤 때 생각 순서

- "빌 때마다 최선을 고른다 + 후보가 시간에 따라 열린다" → 정렬(도착) + 힙(선택)의 2단 구조를 먼저 그린다.
- 시간 진행을 1씩 돌리지 말고 "처리 완료 시각" 또는 "다음 도착 시각"으로만 점프시켜야 도착 시각이 커도 안전하다.
- 경계: 주문 사이에 공백이 있는 경우(셋째 테스트), 전원 동시에 도착하고 조리 시간이 같은 경우(넷째 테스트: 4+8+12=24, 입력 순서 규칙). 우선순위를 `d`만으로 두면 동점 시 다음 원소 비교에서 규칙이 어긋날 수 있으니 튜플 전체를 설계한다.
```

**10) 양끝 삭제 우선순위 큐** · Hard

- **요구사항**: 정수 다중집합에 `I v`(v 삽입), `D 1`(최댓값 하나 삭제), `D -1`(최솟값 하나 삭제), `Q`(현재 최댓값과 최솟값 출력, 비어 있으면 `EMPTY`) 연산을 순서대로 적용한다. 빈 상태의 `D`는 무시한다. 같은 값이 여러 개면 하나만 지운다.
- **입력**: 첫 줄 Q(1 ≤ Q ≤ 500). 이후 Q줄에 연산(v는 -10^9 이상 10^9 이하).
- **출력**: `Q` 연산마다 `최댓값 최솟값` 또는 `EMPTY`를 줄마다.
- **예제**: `7 / I 5 / I 3 / I 8 / D 1 / Q / D -1 / Q` → `5 3 / 5 5` · `3 / D 1 / I 4 / Q` → `4 4`
- **셀프체크**: 최소 힙과 최대 힙에 같은 원소를 `(값, 고유번호)`로 넣고, 한쪽에서 지운 번호를 `alive` 집합에서 빼면 반대쪽 힙에는 "유령"이 남는다 — top을 볼 때마다 유령을 pop으로 걷어내는 지연 삭제를 했는가? 원소가 하나면 최댓값 = 최솟값. 같은 값 2개 중 하나만 지워지는지(넷째 테스트).

```runner
@@SOLUTION
import sys, heapq
def main():
    lines=sys.stdin.read().split("\n")
    q=int(lines[0])
    mx=[]; mn=[]
    alive=set()
    seq=0
    out=[]
    for i in range(1,q+1):
        parts=lines[i].split()
        op=parts[0]
        if op=="I":
            v=int(parts[1]); seq+=1
            heapq.heappush(mn,(v,seq))
            heapq.heappush(mx,(-v,seq))
            alive.add(seq)
        elif op=="D":
            h=mx if parts[1]=="1" else mn
            while h and h[0][1] not in alive:
                heapq.heappop(h)
            if h:
                _,sid=heapq.heappop(h)
                alive.discard(sid)
        else:
            while mx and mx[0][1] not in alive:
                heapq.heappop(mx)
            while mn and mn[0][1] not in alive:
                heapq.heappop(mn)
            if not alive:
                out.append("EMPTY")
            else:
                out.append(f"{-mx[0][0]} {mn[0][0]}")
    print("\n".join(out))
main()
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

- 최댓값 삭제와 최솟값 삭제가 모두 필요하므로 힙 하나로는 부족하다. 최소 힙과 최대 힙(부호 반전)에 같은 원소를 넣고, 한쪽에서 삭제된 원소를 다른 쪽에서도 "삭제된 것으로 취급"해야 한다. 힙은 중간 원소를 O(log n)에 못 지우므로, 원소마다 고유번호를 붙여 살아 있는 번호 집합 `alive`로 관리하고 top이 죽은 번호면 그때 걷어내는 지연 삭제(lazy deletion)를 쓴다. 연산당 평균 O(log n).
- 같은 값이 여러 개여도 고유번호가 다르므로 정확히 하나만 지워진다.

(2) 코드 단계별

- `I v`: 번호 `seq`를 올리고 `(v, seq)`를 최소 힙에, `(-v, seq)`를 최대 힙에 넣고 `alive`에 번호 추가.
- `D 1`/`D -1`: 대상 힙의 top이 `alive`에 없는 동안 pop(유령 제거). 남아 있으면 top을 pop하고 그 번호를 `alive`에서 제거.
- `Q`: 두 힙 모두 유령을 걷어낸 뒤, `alive`가 비었으면 `EMPTY`, 아니면 `-mx[0][0]`과 `mn[0][0]`을 출력.

(3) 스스로 다시 짤 때 생각 순서

- "양끝 삭제" → 두 힙. 그다음 "한쪽에서 지운 것을 반대쪽이 모르는" 문제를 인식하고 지연 삭제를 설계한다.
- 값이 아니라 고유번호로 생사를 판단해야 중복 값이 섞여도 정확히 하나만 지워진다.
- 경계: 빈 상태의 D(무시), 원소 하나일 때 최대=최소, 전부 지운 뒤 `EMPTY`. 유령 제거를 `Q`에서도 해야 top이 죽은 원소를 가리키지 않는다.
```

**11) 막대 절단 후 가장 긴 조각** · Hard

- **요구사항**: 길이 L의 막대가 좌표 0부터 L까지 놓여 있다. 절단 위치 x가 하나씩 주어질 때마다(이미 잘린 위치는 다시 주어지지 않음) 그 위치를 자르고, 현재 남아 있는 조각 중 가장 긴 조각의 길이를 출력한다.
- **입력**: 첫 줄 L Q(2 ≤ L ≤ 10^9, 1 ≤ Q ≤ 300). 이후 Q줄에 절단 위치 x(0 < x < L, 서로 다름).
- **출력**: 절단마다 가장 긴 조각의 길이를 줄마다.
- **예제**: `10 3 / 4 / 8 / 2` → `6 / 4 / 4` · `5 1 / 1` → `4`
- **셀프체크**: 정렬 리스트에 절단 위치를 `insort`하면 좌우 이웃 `a, b`는 삽입 위치의 양옆이다. 조각 `b-a` 하나가 사라지고 `x-a`, `b-x` 둘이 생긴다. 최댓값은 "조각 길이 → 개수" dict와 최대 힙으로 유지하되, 힙 top의 개수가 0이면 걷어내는 지연 삭제. 검산: 10 → {4,6} → 6; 8 절단 → {4,4,2} → 4; 2 절단 → {2,2,4,2} → 4.

```runner
@@SOLUTION
import sys, bisect, heapq
from collections import defaultdict
def main():
    data=sys.stdin.read().split()
    L=int(data[0]); q=int(data[1])
    pts=[0,L]
    cnt=defaultdict(int)
    cnt[L]=1
    h=[-L]
    out=[]
    for k in range(q):
        x=int(data[2+k])
        i=bisect.bisect_left(pts,x)
        a=pts[i-1]; b=pts[i]
        pts.insert(i,x)
        cnt[b-a]-=1
        for g in (x-a, b-x):
            cnt[g]+=1
            heapq.heappush(h,-g)
        while cnt[-h[0]]==0:
            heapq.heappop(h)
        out.append(str(-h[0]))
    print("\n".join(out))
main()
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

- 절단은 "정렬된 절단점 집합에서 x의 좌우 이웃 찾기"이므로 정렬 리스트 + bisect(TreeSet 대체)가 맞다. 자르면 조각 하나가 둘로 갈라지는데, 사라진 조각이 최댓값이었을 수 있어 최댓값을 다시 찾아야 한다 — 매번 조각 전체를 훑으면 O(Q^2)이고, 최대 힙 + 개수 dict의 지연 삭제로 O(Q log Q)에 유지한다.
- 조각 길이 값은 중복될 수 있으므로 "길이 → 개수"로 세고, 힙 top의 개수가 0이면 이미 사라진 길이라 pop한다.

(2) 코드 단계별

- `pts = [0, L]`, `cnt[L] = 1`, 최대 힙 `h = [-L]`로 시작.
- 절단 x마다 `i = bisect_left(pts, x)`로 삽입 위치를 얻고 `a = pts[i-1]`, `b = pts[i]`가 좌우 이웃. `insert(i, x)`.
- `cnt[b-a] -= 1`, 새 조각 `x-a`, `b-x`는 `cnt`를 늘리고 힙에 push.
- `cnt[-h[0]] == 0`인 동안 pop(유령 제거). top의 부호를 되돌려 출력.

(3) 스스로 다시 짤 때 생각 순서

- "이웃을 찾아 조각을 쪼갠다" → 정렬 집합. "최댓값이 사라질 수 있다" → 최대 힙 + 지연 삭제. 두 구조를 나눠 설계한다.
- 힙에는 길이만 넣고, 같은 길이가 여러 조각일 수 있으니 개수를 dict로 별도 관리해 "0개면 유령"으로 판정한다.
- 경계: 첫 절단에서 이웃이 0과 L, 정확히 절반 절단(같은 길이 두 개), 최댓값이 바뀌지 않는 절단(셋째 테스트 첫 줄). 좌표가 크지만 조각 개수만 다루므로 L 크기는 문제되지 않는다.
```

**12) 카드 지우기와 되돌리기** · Hard

- **요구사항**: 1부터 N까지 번호가 적힌 카드가 순서대로 놓여 있고 커서는 1번 카드 위에 있다. 명령은 네 가지다. `L`: 커서를 왼쪽 카드로(맨 왼쪽이면 무시). `R`: 오른쪽 카드로(맨 오른쪽이면 무시). `D`: 커서 위 카드를 지운다. 커서는 오른쪽 이웃으로 가고, 오른쪽이 없으면 왼쪽 이웃으로 간다(카드가 1장뿐일 때 `D`는 주어지지 않는다). `U`: 가장 최근에 지운 카드를 원래 자리(지울 당시의 양 이웃 사이)에 되돌리고 커서를 그 카드로 옮긴다(되돌릴 카드가 없으면 무시). 모든 명령 후 남은 카드를 순서대로 출력하고, 둘째 줄에 커서가 가리키는 카드 번호를 출력한다.
- **입력**: 첫 줄 N M(2 ≤ N ≤ 500, 1 ≤ M ≤ 500). 둘째 줄에 M개의 명령이 공백으로.
- **출력**: 첫 줄에 남은 카드 번호들을 공백으로, 둘째 줄에 커서 카드 번호.
- **예제**: `5 5 / R D D U L` → `1 3 4 5 / 1` · `3 4 / D U U D` → `2 3 / 2`
- **셀프체크**: 배열 `prv`/`nxt`(0과 N+1을 센티넬)로 지우기는 `nxt[prv[x]] = nxt[x]; prv[nxt[x]] = prv[x]`, 되돌리기는 x의 포인터를 건드리지 않고 `nxt[prv[x]] = x; prv[nxt[x]] = x`. 되돌리기는 지운 순서의 역순(스택)으로만 정확하다. 검산(첫 예제): R→커서2, D→2 삭제·커서3, D→3 삭제·커서4, U→3 복원·커서3, L→커서1.

```runner
@@SOLUTION
import sys
def main():
    data=sys.stdin.read().split()
    n=int(data[0]); m=int(data[1])
    ops=data[2:2+m]
    nxt=[i+1 for i in range(n+2)]
    prv=[i-1 for i in range(n+2)]
    cur=1
    stack=[]
    for op in ops:
        if op=="L":
            if prv[cur]!=0:
                cur=prv[cur]
        elif op=="R":
            if nxt[cur]!=n+1:
                cur=nxt[cur]
        elif op=="D":
            p=prv[cur]; q=nxt[cur]
            nxt[p]=q; prv[q]=p
            stack.append(cur)
            cur=q if q!=n+1 else p
        else:
            if stack:
                x=stack.pop()
                nxt[prv[x]]=x; prv[nxt[x]]=x
                cur=x
    res=[]
    v=nxt[0]
    while v!=n+1:
        res.append(str(v)); v=nxt[v]
    print(" ".join(res))
    print(cur)
main()
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

- 커서 이동·삭제·복원이 모두 "이웃"만으로 정의되므로 이중 연결 리스트가 자연스럽다. 카드 번호가 1..N이라 dict 대신 배열 `prv`, `nxt`로 두고 0과 N+1을 센티넬로 쓰면 끝 검사가 `prv[cur] != 0`, `nxt[cur] != n+1`로 단순해진다. 명령당 O(1), 전체 O(N + M).
- 복원의 핵심은 삭제된 노드 x의 `prv[x]`, `nxt[x]`를 지우지 않고 남겨 두는 것이다. 그 두 값이 "지울 당시의 이웃"이므로 `nxt[prv[x]] = x; prv[nxt[x]] = x`만으로 제자리에 돌아간다. 단, 이웃들이 그 사이에 바뀌지 않았어야 하므로 지운 역순(스택)으로만 복원한다.

(2) 코드 단계별

- `nxt[i] = i+1`, `prv[i] = i-1`로 0..N+1을 잇고 커서는 1.
- `L`/`R`: 이웃이 센티넬이 아니면 이동.
- `D`: 양 이웃 `p, q`를 서로 잇고 `cur`를 스택에 push. 커서는 `q`가 센티넬이 아니면 `q`, 아니면 `p`.
- `U`: 스택이 비어 있지 않으면 pop한 x를 자기 포인터로 재연결하고 커서를 x로.
- 끝나면 `nxt[0]`부터 N+1 전까지 따라가 출력하고, 커서 번호를 둘째 줄에 출력.

(3) 스스로 다시 짤 때 생각 순서

- "지운 것을 원래 자리에 되돌린다"를 보면, 삭제 시 노드의 포인터를 보존하고 스택으로 순서를 기억하는 패턴을 떠올린다.
- 삭제 후 커서 규칙(오른쪽 우선, 없으면 왼쪽)을 센티넬 비교로 정확히 옮긴다(셋째 테스트: 맨 끝 삭제).
- 경계: 되돌릴 것이 없는 `U`(무시), 연속 두 번 삭제 후 두 번 복원(넷째 테스트: 3을 먼저 되돌려야 2가 1과 3 사이로 정확히 돌아간다), 커서가 복원된 카드로 이동하는지 확인.
```
