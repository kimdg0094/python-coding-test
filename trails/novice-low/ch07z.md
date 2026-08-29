## L8. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

Ch7의 핵심은 하나다. **여러 값을 이름 하나로 묶어 두면, 그다음부터는 "인덱스로 한 칸 꺼내기"와 "반복문으로 전부 훑기" 두 가지 동작만으로 거의 모든 처리가 된다.** 합·개수·최댓값·탐색·등장 횟수는 전부 "훑으면서 무언가를 갱신하는" 같은 모양의 코드다.

**개념 지도**

```text
  Ch7 core :  many values  ->  one name ( list )  ->  index  /  loop

  step 1 : GET the list
  ├─ list(map(int, input().split()))     one line of numbers      L1
  ├─ arr = []   then   arr.append(v)     build it up              L3
  └─ cnt = [0] * SIZE                    fixed size , all zeros   L4

  step 2 : REACH one value
  ├─ arr[0]                              first                    L2
  ├─ arr[len(arr) - 1]   ==   arr[-1]    last                     L2
  └─ arr[k - 1]                          k-th , counted from 1    L2

  step 3 : WALK the list
  ├─ for v in arr:                       value only               L1 L4 L6
  └─ for i in range(len(arr)):           position needed          L5 L6

  step 4 : SUMMARISE while walking
  ├─ total += v                          sum                      L1
  ├─ if v > t: count += 1                count by condition       L5
  ├─ if arr[i] == x: pos = i ; break     first position           L5
  ├─ if arr[i] == x: pos = i             last position            L5
  ├─ if v > mx: mx = v                   max  /  min              L6
  └─ cnt[v] += 1                         how many times each      L4
```

step 4의 다섯 줄은 전부 같은 자리에 들어간다. 그래서 여러 집계를 한 번의 순회로 동시에 처리할 수 있다.

```text
  one pass over  arr = [4, 9, 2, 7]      # 반복 한 바퀴로 네 가지를 동시에

    v       total   count(v>3)    mx    mn
    -----   -----   ----------   ---   ---
    start       0            0     4     4
    4           4            1     4     4
    9          13            2     9     4
    2          15            2     9     2
    7          22            3     9     2
```

`mx`와 `mn`의 시작값이 `0`이 아니라 `arr[0] = 4`인 점을 눈여겨보자. 이 한 가지가 음수만 있는 입력에서 정답과 오답을 가른다.

**뼈대 코드**

배열 문제를 만나면 아래 골격 중 하나를 꺼내 쓰고, `←` 표시된 자리만 문제에 맞춰 고친다.

① 입력 → 리스트 → 집계(합·개수)

```python
arr = list(map(int, input().split()))   # ← 문제마다 바뀜 (입력 형태)
total = 0                               # 누적 변수는 반복 '밖'에서 초기화
count = 0
for v in arr:
    total += v
    if v > 0:                           # ← 문제마다 바뀜 (세는 조건)
        count += 1
print(total, count)
```

② 최댓값·최솟값과 그 위치

```python
arr = list(map(int, input().split()))
mx = arr[0]                  # 실제 원소로 시작 (상수로 시작하지 않는다)
mn = arr[0]
for v in arr:
    if v > mx:               # ← 문제마다 바뀜 (조건과 갱신 대상)
        mx = v
    if v < mn:
        mn = v
pos = 0
for i in range(len(arr)):
    if arr[i] == mx:
        pos = i + 1          # 사람이 세는 위치 = 인덱스 + 1
        break                # ← 처음 위치면 break, 마지막 위치면 지운다
print(mx, mn, pos)
```

③ 탐색 — 있는지, 몇 번째인지

```python
arr = list(map(int, input().split()))
x = int(input())
pos = -1                     # 못 찾음 표시 (정답으로는 나올 수 없는 값)
for i in range(len(arr)):    # 위치가 필요하니 range(len(arr))
    if arr[i] == x:          # ← 문제마다 바뀜 (찾는 조건)
        pos = i + 1
        break                # ← "처음"만 필요할 때만 둔다
print(pos)
```

④ 카운트 배열 — 값별 등장 횟수

```python
arr = list(map(int, input().split()))
SIZE = 101                   # ← 문제마다 바뀜 (나올 수 있는 최댓값 + 1)
cnt = [0] * SIZE
for v in arr:
    cnt[v] += 1              # 값 자체를 인덱스로 쓴다
best = 0
for d in range(SIZE):
    if cnt[d] > cnt[best]:   # > 라서 동점이면 먼저 본 작은 값이 남는다
        best = d
print(best)
```

⑤ 새 리스트 만들기 — 생성·변환

```python
n = int(input())
arr = []                     # 빈 리스트에서 시작
for i in range(1, n + 1):    # ← 문제마다 바뀜 (범위, 방향)
    arr.append(i * i)        # ← 문제마다 바뀜 (담을 값)
print(*arr)                  # 대괄호 없이 공백으로 출력
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 훑는 횟수 |
| --- | --- | --- | --- |
| 값만 필요하다 | `for v in arr` | 인덱스를 쓸 일이 없어 짧고 안전하다 | `n` |
| 몇 번째인지가 필요하다 | `for i in range(len(arr))` | `arr[i]`와 `i`를 함께 쓸 수 있다 | `n` |
| 이웃한 두 값을 비교한다 | `for i in range(len(arr) - 1)` | 마지막 칸은 짝이 없다 | `n-1` |
| 처음 나오는 위치를 찾는다 | 찾으면 `break` | 뒤를 더 볼 필요가 없다 | 최대 `n` |
| 마지막 나오는 위치를 찾는다 | `break` 없이 계속 덮어쓴다 | 마지막으로 덮인 값이 답이다 | `n` |
| 합·개수를 구한다 | 누적 변수를 0에서 시작 | 아무것도 안 더한 상태가 0이다 | `n` |
| 최댓값·최솟값을 구한다 | `arr[0]`을 시작 기준으로 | 리스트 밖의 값이 답이 될 수 없다 | `n` |
| 값별 등장 횟수를 센다 | 카운트 배열 `[0] * (최댓값+1)` | 값을 인덱스로 쓰면 한 번에 접근된다 | `n` + 배열 크기 |
| 값을 바꿔 새 리스트를 만든다 | `result = []` + `append` | 원본을 건드리지 않아 흐름이 깔끔하다 | `n` |
| 정해진 개수를 미리 채운다 | `[0] * n` | 크기가 정해져 있고 인덱스로 바로 쓴다 | `n` |
| 원소를 걸러내야 한다 | 지우지 말고 새 리스트에 담는다 | 순회 중 삭제는 원소를 건너뛴다 | `n` |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: `input().split()`이 만든 조각이 왜 문자열이고, `map(int, ...)`와 `list(...)`가 각각 무엇을 하는지.
- [ ] 설명할 수 있다: `print(arr)`와 `print(*arr)`의 결과가 왜 다른지.
- [ ] 설명할 수 있다: 인덱스가 왜 0부터 시작하고, 마지막이 왜 `len(arr) - 1`인지.
- [ ] 설명할 수 있다: 음수 인덱스 `arr[-k]`가 어느 칸을 가리키는지와 그 이유.
- [ ] 설명할 수 있다: 사람이 세는 "K번째"와 인덱스 사이의 1칸 차이가 어디서 생기는지.
- [ ] 설명할 수 있다: 두 칸의 값을 맞바꿀 때 임시 변수가 왜 필요한지.
- [ ] 설명할 수 있다: `[0] * n`은 안전한데 `[[0] * n] * m`은 왜 위험한지.
- [ ] 설명할 수 있다: `b = a`가 왜 복사가 아닌지, 값을 진짜로 옮기려면 어떻게 하는지.
- [ ] 설명할 수 있다: 카운트 배열의 크기를 "나올 수 있는 최댓값 + 1"로 잡아야 하는 이유.
- [ ] 설명할 수 있다: 카운트 배열에서 동점일 때 작은 값이 남는 것이 왜 부등호 하나로 결정되는지.
- [ ] 설명할 수 있다: 탐색에서 `break`의 유무가 "처음"과 "마지막"을 어떻게 가르는지.
- [ ] 설명할 수 있다: 못 찾았을 때 표시로 `-1`을 쓰는 이유와, `0`이 위험할 수 있는 경우.
- [ ] 설명할 수 있다: 최댓값의 시작 기준을 `arr[0]`으로 두는 이유와, 상수로 두면 어떤 입력에서 틀리는지.
- [ ] 설명할 수 있다: 누적 변수의 초기화를 반복문 밖에 두어야 하는 이유.
- [ ] 설명할 수 있다: 리스트를 순회하면서 원소를 지우면 왜 일부가 건너뛰어지는지.

**⚠️ 자주 하는 실수**

**1) `arr[i + 1]`로 리스트 밖을 읽는다**

```python
# ❌ 틀린 코드
arr = list(map(int, input().split()))
for i in range(len(arr)):
    if arr[i] == arr[i + 1]:     # 마지막 i 에서 arr[len(arr)] 을 읽는다
        print("같음")
```

왜: `range(len(arr))`의 마지막 `i`는 `len(arr) - 1`이다. 거기서 `arr[i + 1]`은 존재하지 않는 칸이라 IndexError가 난다. "이웃끼리 비교"는 짝이 있는 칸까지만 돌아야 한다.

```python
# ✅ 고친 코드
arr = list(map(int, input().split()))
for i in range(len(arr) - 1):    # 마지막 칸은 짝이 없으므로 제외
    if arr[i] == arr[i + 1]:
        print("같음")
```

**2) "K번째"를 그대로 인덱스로 쓴다**

```python
# ❌ 틀린 코드
arr = list(map(int, input().split()))
k = int(input())
print(arr[k])                    # 1부터 세는 위치를 그대로 인덱스로
```

왜: 사람은 1부터, 인덱스는 0부터 센다. `K`번째 값은 `arr[K - 1]`이다. `arr[k]`는 한 칸 뒤 값이고, `K`가 개수와 같으면 IndexError까지 난다.

```python
# ✅ 고친 코드
arr = list(map(int, input().split()))
k = int(input())
print(arr[k - 1])
```

**3) 누적 변수 초기화를 반복문 안에 둔다**

```python
# ❌ 틀린 코드
arr = list(map(int, input().split()))
for v in arr:
    total = 0                    # 반복 '안'에서 초기화
    total += v
print(total)                     # 마지막 값 하나만 남는다
```

왜: 매 반복마다 `total`이 0으로 되돌아가므로 누적이 되지 않는다. 초기화 위치가 곧 초기화 횟수다. 전체 합이 필요하면 초기화는 반복 밖에서 한 번뿐이어야 한다.

```python
# ✅ 고친 코드
arr = list(map(int, input().split()))
total = 0                        # 반복 '밖'에서 한 번만
for v in arr:
    total += v
print(total)
```

**4) 최댓값을 상수로 시작한다**

```python
# ❌ 틀린 코드
arr = list(map(int, input().split()))
mx = 0                           # 상수로 시작
for v in arr:
    if v > mx:
        mx = v
print(mx)                        # 입력이 -3 -8 -1 이면 0 이 나온다
```

왜: 모든 값이 0보다 작으면 갱신이 한 번도 일어나지 않아, 리스트에 없던 0이 답이 되어 버린다. 시작 기준은 반드시 실제 원소여야 한다.

```python
# ✅ 고친 코드
arr = list(map(int, input().split()))
mx = arr[0]                      # 실제 원소로 시작하면 언제나 안전하다
for v in arr:
    if v > mx:
        mx = v
print(mx)
```

**5) 카운트 배열 크기를 작게 잡는다**

```python
# ❌ 틀린 코드
arr = list(map(int, input().split()))   # 값이 0 ~ 100 까지 나올 수 있다
cnt = [0] * 10
for v in arr:
    cnt[v] += 1                  # v 가 10 이상이면 IndexError
```

왜: 카운트 배열은 값 자체를 인덱스로 쓴다. 값 100을 세려면 인덱스 100이 있어야 하고, 인덱스 100이 있으려면 크기가 101이어야 한다. "최댓값 + 1"이 최소 크기다.

```python
# ✅ 고친 코드
arr = list(map(int, input().split()))
cnt = [0] * 101                  # 0 부터 100 까지 모두 담는다
for v in arr:
    cnt[v] += 1
```

**6) `b = a`를 복사로 착각한다**

```python
# ❌ 틀린 코드
a = [1, 2, 3]
b = a                            # 복사한 줄 알았지만
b[0] = 99
print(a)                         # [99, 2, 3]  <- a 까지 바뀐다
```

왜: `b = a`는 값을 복제하는 것이 아니라 같은 리스트에 이름을 하나 더 붙이는 것이다. 어느 이름으로 고쳐도 같은 리스트가 바뀐다. `[[0] * n] * m`이 위험한 것도 정확히 같은 이유다.

```python
# ✅ 고친 코드
a = [1, 2, 3]
b = []
for v in a:
    b.append(v)                  # 새 리스트에 값을 하나씩 옮긴다
b[0] = 99
print(*a)                        # 1 2 3   (원본은 그대로)
```

**7) 순회하는 도중에 원소를 지운다**

```python
# ❌ 틀린 코드
arr = [2, 2, 3]
for v in arr:
    if v == 2:
        arr.remove(v)            # remove 는 그 값을 하나 지운다
print(arr)                       # [2, 3]  <- 2 가 하나 남는다
```

왜: 원소가 빠지면 뒤 원소들이 한 칸씩 앞으로 당겨진다. 그런데 `for`는 다음 번호를 그대로 읽으므로, 당겨져 온 원소를 건너뛰어 버린다. 훑는 대상과 고치는 대상이 같은 리스트여서 생기는 문제다.

```python
# ✅ 고친 코드
arr = [2, 2, 3]
result = []                      # 원본은 그대로 두고 새 리스트에 담는다
for v in arr:
    if v != 2:
        result.append(v)
print(*result)                   # 3
```

**8) 리스트를 통째로 출력한다**

```python
# ❌ 틀린 코드
arr = list(map(int, input().split()))
print(arr)                       # [10, 20, 30]
```

왜: 리스트 한 개를 넘기면 파이썬이 대괄호와 쉼표까지 그대로 보여 준다. 채점은 보통 `10 20 30`을 기대하므로 그대로 틀린다.

```python
# ✅ 고친 코드
arr = list(map(int, input().split()))
print(*arr)                      # 10 20 30
```

**다음 챕터로**

지금은 값이 한 줄로 늘어선 리스트를 다뤘다. 여기에 "줄"이라는 축이 하나 더 붙으면 2차원 배열, 곧 격자가 된다. Ch6에서 익힌 `for i` / `for j` 구조와 이 챕터의 인덱스 감각이 만나는 지점이다. 인덱스가 0부터 시작한다는 사실과 누적 변수의 초기화 위치는 그때도 똑같이 발목을 잡으니, 지금 확실히 굳혀 두는 편이 이득이다.
