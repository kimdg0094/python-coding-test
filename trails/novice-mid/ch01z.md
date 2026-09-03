## L6. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

**개념 지도**

Ch1은 "함수 하나를 어떻게 만드는가"에서 출발해, "값이 어떻게 오가는가"와 "이름이 어디까지 살아 있는가"로 갈라진다. 이 세 갈래가 한 장에 들어가면 챕터가 끝난 것이다.

```text
                        +-------------+
                        |  function   |
                        +------+------+
                 +-------------+-------------+
                 |                           |
          no return value              returns a value
          (side effect only)           (a reusable part)
                 |                           |
          print / draw / log           return x  |  return a, b
                 |                           |
                 +-------------+-------------+
                               |
                    +----------+----------+
                    |                     |
            argument passing         name scope
                    |                     |
        immutable -> rebind only    local  : dies at return
        mutable   -> in-place edit  global : 'global' to assign
```

왼쪽 갈래(L1·L2)는 "무엇을 돌려줄까", 오른쪽 아래 갈래(L3·L4)는 "무엇이 바깥에 남을까"의 문제다. 실전에서 함수를 설계할 때 던지는 질문은 사실상 아래 한 장으로 압축된다.

```text
   want the function to change the caller's data?
        |
        +-- it is int / str / tuple  --> impossible : return a new value
        |
        +-- it is list / dict / set  --> edit in place (no return needed)
                                         or copy first to protect it
```

**뼈대 코드**

문제를 만나면 아래 골격 중 하나를 골라 빈칸만 채운다.

```python
# 1) 함수 분해 골격 — 판정/계산 부품을 위에, 조립은 아래에
def check(x):                      # ← 문제마다 바뀜: 판정 규칙
    if x < 0:
        return False               # 안 되는 경우를 조기 반환으로 먼저 걸러냄
    return True

def transform(x):                  # ← 문제마다 바뀜: 값 변환 규칙
    return x * 2

def main():
    n = int(input())
    vals = list(map(int, input().split()))
    answer = 0
    for v in vals:
        if check(v):               # ← 문제마다 바뀜: 무엇을 세고 무엇을 모을지
            answer += transform(v)
    print(answer)

main()
```

```python
# 2) 반환 없는 출력 함수 — 함수가 함수를 부른다
def show_row(row):                 # ← 문제마다 바뀜: 한 줄의 출력 형식
    print(' '.join(map(str, row)))

def show_all(grid):
    for row in grid:
        show_row(row)              # 반환값을 쓰지 않는다
```

```python
# 3) 여러 값 한 번에 돌려주기
def min_max(arr):
    return min(arr), max(arr)      # ← 문제마다 바뀜: 돌려줄 값들(쉼표가 튜플을 만든다)

lo, hi = min_max([3, 1, 4])        # 튜플 언패킹으로 받기
```

```python
# 4) 원본 보존 vs 원본 갱신 — 둘을 절대 섞지 않는다
def apply_copy(arr):               # 보존형: 새 리스트를 만들어 반환
    new = arr[:]                   # 2차원이면 [r[:] for r in grid]
    new[0] += 1                    # ← 문제마다 바뀜: 연산
    return new

def apply_inplace(arr):            # 갱신형: 반환 없음, 호출자가 바뀐다
    arr[0] += 1                    # ← 문제마다 바뀜: 연산
```

```python
# 5) 여러 함수가 상태를 공유할 때
count = 0
visited = []

def mark(v):
    global count                   # 정수를 '대입'하려면 반드시 필요
    if not visited[v]:
        visited[v] = True          # 리스트 제자리 수정은 global 없이도 공유됨
        count += 1

def reset(m):
    global count, visited
    count = 0                      # ← 질의마다 초기화하는 것을 잊기 쉽다
    visited = [False] * (m + 1)
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 결과를 출력하고 끝난다 | 반환 없는 함수 | 위로 올릴 값이 없다 | 호출 O(1) + 내부 작업 |
| 그 값을 나중에 또 쓴다 | `return` 있는 함수 | 부품으로 조립할 수 있다 | 호출 O(1) + 내부 작업 |
| 안 되는 경우를 먼저 쳐낸다 | 조기 반환 | 중첩 `if`가 사라진다 | 평균 실행량이 줄어듦 |
| 값 두 개 이상을 돌려준다 | `return a, b` + 언패킹 | 쉼표가 튜플 하나로 묶는다 | O(1) |
| 큰 배열을 함수가 갱신한다 | 리스트를 넘겨 제자리 수정 | 복사가 없다 | 전달 O(1) |
| 호출자의 원본을 지켜야 한다 | 복사본을 만들어 반환 | 부작용 차단 | 복사 O(n) |
| 2차원 격자를 복사한다 | `[r[:] for r in grid]` | `grid[:]`는 행을 공유한다 | O(R·C) |
| 여러 함수가 정수 카운터를 공유 | 전역 + `global` | 정수는 재대입뿐이라 선언 필요 | O(1) |
| 여러 함수가 배열·딕셔너리를 공유 | 전역 가변 객체 제자리 수정 | 이름 대입이 아니라 `global` 불필요 | O(1) |
| 함수마다 값이 독립이어야 한다 | 지역 변수(인자로 받고 반환) | 간섭이 원천 차단된다 | O(1) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 함수를 부를 때 스택 프레임이 쌓였다가 반환과 함께 사라지는 과정.
- [ ] 설명할 수 있다: `return`이 없는 함수가 왜 `None`을 돌려주는지, 그리고 `return` 없음·`return`만 있음·`return None`이 왜 같은 뜻인지.
- [ ] 설명할 수 있다: 조기 반환이 코드를 왜 짧고 안전하게 만드는지, 그리고 왜 정답을 바꾸지 않는지.
- [ ] 설명할 수 있다: `return a, b`가 실제로는 값 하나(튜플)를 돌려준다는 것과, `x, y = f()`가 그것을 푸는 과정.
- [ ] 설명할 수 있다: 파이썬이 "객체 참조를 값처럼 넘긴다"는 한 문장에서 왜 값 전달·참조 전달 두 현상이 모두 나오는지.
- [ ] 설명할 수 있다: `n = n + 1`과 `lst.append(x)`가 호출자에게 다르게 보이는 이유를 이름표와 객체 그림으로.
- [ ] 설명할 수 있다: 함수 안에서 `lst = [...]`로 재대입하면 왜 바깥이 안 바뀌는지.
- [ ] 설명할 수 있다: 2차원에서 `grid[:]`가 왜 위험하고 `[r[:] for r in grid]`가 왜 안전한지.
- [ ] 설명할 수 있다: 방어적 복사의 비용이 O(n)이라는 것과, 그것을 반복문 안에 두면 왜 위험한지.
- [ ] 설명할 수 있다: 함수 안에 대입이 한 번이라도 있으면 왜 그 이름이 함수 전체에서 지역이 되는지.
- [ ] 설명할 수 있다: `global`이 정수에는 필요한데 리스트 제자리 수정에는 필요 없는 이유.
- [ ] 설명할 수 있다: LEGB 탐색 순서와, 지역에 없는 이름이 전역에서 발견되는 과정.
- [ ] 설명할 수 있다: 함수로 잘게 나눈다고 시간 복잡도가 나빠지지 않는 이유.

**⚠️ 자주 하는 실수**

**1) 반환 없는 함수의 결과를 값처럼 쓴다**

```python
# ❌ 틀린 코드
def total(arr):
    print(sum(arr))          # 출력만 하고 return이 없다

s = total([1, 2, 3])
print(s + 1)                 # TypeError: NoneType + int
```

왜: 출력은 화면에 글자를 찍는 부수 효과일 뿐이고, 호출자에게 올라가는 값은 여전히 `None`이다. "보인다"와 "돌려받는다"는 다른 일이다.

```python
# ✅ 고친 코드
def total(arr):
    return sum(arr)          # 값을 돌려준다

s = total([1, 2, 3])
print(s + 1)
```

**2) 기본 인자로 가변 객체를 쓴다**

```python
# ❌ 틀린 코드
def push(x, box=[]):         # 기본값 리스트는 함수를 정의할 때 딱 한 번 만들어진다
    box.append(x)
    return box

print(push(1))               # [1]
print(push(2))               # [1, 2]  ← 이전 호출의 흔적이 남아 있다
```

왜: 기본값은 호출할 때마다 새로 만들어지지 않는다. 함수 객체에 한 번 붙어 계속 재사용되므로, 가변 객체를 기본값으로 두면 호출 사이에 상태가 새어 나간다.

```python
# ✅ 고친 코드
def push(x, box=None):
    if box is None:
        box = []             # 호출할 때마다 새 리스트
    box.append(x)
    return box
```

**3) 리스트 인자를 정렬해 호출자의 원본을 뭉갠다**

```python
# ❌ 틀린 코드
def median(arr):
    arr.sort()               # 호출자가 넘긴 바로 그 리스트가 정렬된다
    return arr[len(arr) // 2]

data = [3, 1, 2]
m = median(data)
print(data)                  # [1, 2, 3] ← 입력 순서가 사라졌다
```

왜: 리스트는 가변 객체라 함수 안팎이 같은 객체를 가리킨다. `.sort()`는 그 객체를 제자리에서 바꾸므로 호출자에게 그대로 보인다.

```python
# ✅ 고친 코드
def median(arr):
    s = sorted(arr)          # 새 리스트를 만들어 그것만 정렬
    return s[len(s) // 2]
```

**4) 함수 안 재대입으로 바깥을 바꾸려 한다**

```python
# ❌ 틀린 코드
def reset(pos):
    pos = [0, 0]             # 지역 이름표만 새 리스트로 옮겨 붙었다

p = [3, 4]
reset(p)
print(p)                     # [3, 4] ← 바뀌지 않는다
```

왜: `=`는 객체를 고치는 연산이 아니라 이름표를 옮기는 연산이다. 호출자의 이름표는 원래 객체에 그대로 남는다.

```python
# ✅ 고친 코드
def reset(pos):
    pos[0] = 0               # 같은 객체의 내용을 고친다
    pos[1] = 0
```

**5) 전역을 바꾸면서 `global`을 빠뜨린다**

```python
# ❌ 틀린 코드
count = 0

def tick():
    count += 1               # UnboundLocalError: 대입이 있어 count는 지역으로 확정됨

tick()
```

왜: 함수 안에 대입이 한 줄이라도 있으면 그 이름은 함수 전체에서 지역이 된다. `count += 1`은 아직 값이 없는 지역 `count`를 읽으려다 터진다.

```python
# ✅ 고친 코드
count = 0

def tick():
    global count             # 전역 상자를 쓰겠다고 선언
    count += 1
```

**6) 2차원 격자를 얕은 복사로 지킨다고 착각한다**

```python
# ❌ 틀린 코드
def bump(grid):
    new = grid[:]            # 바깥 리스트만 새로 만들어졌다
    new[0][0] += 1           # 안쪽 행은 원본과 같은 객체
    return new
```

왜: 슬라이싱은 "행을 가리키는 참조들"을 복사할 뿐 행 자체를 복사하지 않는다. 그래서 복사본을 고치면 원본도 함께 바뀐다.

```python
# ✅ 고친 코드
def bump(grid):
    new = [row[:] for row in grid]   # 각 행까지 새로 만든다
    new[0][0] += 1
    return new
```

**7) 여러 질의를 처리하며 전역을 초기화하지 않는다**

```python
# ❌ 틀린 코드
count = 0

def run(vals):
    global count
    for v in vals:
        count += 1
    return count

print(run([1, 2]))           # 2
print(run([1, 2, 3]))        # 5 ← 앞 질의의 2가 그대로 남아 있다
```

왜: 전역은 프로그램이 끝날 때까지 살아 있다. 함수가 끝나도 값이 사라지지 않으므로, 질의마다 새로 세려면 명시적으로 되돌려야 한다.

```python
# ✅ 고친 코드
count = 0

def run(vals):
    global count
    count = 0                # 질의 시작마다 초기화
    for v in vals:
        count += 1
    return count
```

**다음 챕터로**

- Ch2에서는 함수가 **자기 자신**을 부른다. 그러면 L1에서 본 스택 프레임이 한 겹이 아니라 깊이만큼 여러 겹으로 쌓이고, "언제 멈추는가"가 곧 생사를 가르는 문제가 된다.
- L2의 "값을 돌려주는 부품" 감각은 재귀의 반환값 조합으로, L4의 "전역 공유" 감각은 재귀 도중 누적하는 카운터로 그대로 이어진다.
