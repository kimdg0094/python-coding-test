## L20. 정리 — 반복문 개념 지도·체크리스트·자주 하는 실수

**개념**

이 챕터에서 배운 것을 한자리에 모은다. 새 문법은 없다. `for`와 `while`, 누적 변수, `continue`/`break`, 깃발 변수가 사실은 **하나의 뼈대**를 공유한다는 것을 확인하고, 입문자가 실제로 넘어지는 지점을 미리 밟아 보는 자리다.

**개념 지도**

반복문을 고르는 갈림길은 딱 하나다. "반복을 시작하기 전에 총 횟수를 적을 수 있는가?"

```text
   ┌───────────────────────────────────────────────────────┐
   │  repeat the same work                                 │
   └───────────────────────────┬───────────────────────────┘
                               │
          can you count the passes in advance ?
                 yes │                    │ no
                     ▼                    ▼
   ┌──────────────────────────┐  ┌──────────────────────────┐
   │  for i in range(...)     │  │  while cond :            │
   │  range(n)      : n times │  │  init / check / update   │
   │  range(a, b)   : b - a   │  │  while True : + break    │
   │  range(a, b, s): step s  │  │  sentinel value          │
   └──────────────────────────┘  └──────────────────────────┘
```

둘은 같은 일을 다른 방식으로 적은 것이다. `for`가 한 줄에 뭉쳐 둔 세 정보가 `while`에서는 세 줄로 흩어진다.

```text
   for i in range(1, N + 1):      i = 1                # start
       body                       while i <= N :       # stop
                                      body
                                      i = i + 1        # step
```

반복의 껍데기가 정해지면, 남는 것은 "본문에 무엇을 두는가"뿐이다.

```text
   inside the loop body
   ────────────────────────────────────────────────────────────
   accumulate   cnt   = 0  ->  cnt += 1        # how many
                total = 0  ->  total += x      # sum
                prod  = 1  ->  prod *= x       # product
   filter       if cond :  ->  handle only the ones that pass
   jump         continue   ->  skip the rest of THIS pass
                break      ->  leave the loop right now
   decide       found  = False -> True   , 'at least one'
                all_ok = True  -> False  , 'all of them'
```

**뼈대 코드**

**1) 정해진 횟수만큼 반복**

```python
n = int(input())
for i in range(n):          # ← 문제마다 바뀜 (횟수)
    print("Hello")          # ← 문제마다 바뀜 (매번 할 일)
```

**2) 구간 훑으며 누적하기 (합·개수·곱)**

```python
n = int(input())
total = 0                   # ← 합은 0, 곱이면 1, 개수도 0 (반복 밖!)
for i in range(1, n + 1):   # ← 문제마다 바뀜 (구간, 끝은 +1)
    total = total + i       # ← 문제마다 바뀜 (+1 / +i / *i)
print(total)                # ← 반복이 끝난 뒤 한 번만
```

**3) 훑으면서 조건에 맞는 것만 고르기**

```python
n = int(input())
cnt = 0
for i in range(1, n + 1):
    if i % 5 == 0:          # ← 문제마다 바뀜 (고르는 기준)
        cnt = cnt + 1       # ← 문제마다 바뀜 (고른 것으로 할 일)
print(cnt)
```

**4) 개수를 먼저 받고, 값을 하나씩 받기**

```python
n = int(input())            # ← 몇 개가 오는지
total = 0
for i in range(n):
    x = int(input())        # ← 매 회차마다 한 줄씩 읽는다
    total = total + x       # ← 문제마다 바뀜 (읽은 값으로 할 일)
print(total)
```

**5) 언제 끝날지 모를 때 — 무한 루프와 감시 값**

```python
total = 0
while True:
    n = int(input())
    if n == 0:              # ← 문제마다 바뀜 (종료 신호)
        break               # ← 신호 값은 처리하지 않고 빠져나온다
    total = total + n       # ← 문제마다 바뀜 (신호가 아닐 때 할 일)
print(total)
```

**6) 판정하기 — "하나라도" 와 "모두"**

```python
n = int(input())

found = False               # ← '하나라도' : 없다고 가정하고 시작
for i in range(2, n):
    if n % i == 0:          # ← 문제마다 바뀜 (찾는 조건)
        found = True
        break               # ← 하나 찾으면 결론이 나므로 멈춘다

all_ok = True               # ← '모두' : 다 만족한다고 가정하고 시작
for i in range(2, n):
    if n % i == 0:          # ← 문제마다 바뀜 (어기는 조건)
        all_ok = False
        break
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
| --- | --- | --- | --- |
| 횟수를 미리 셀 수 있다 | `for` + `range` | 시작·끝·간격을 한 줄에 적을 수 있다 | 반복 n회 |
| 그냥 n번만 하면 된다 | `range(n)` | 값이 필요 없고 횟수만 필요하다 | 반복 n회 |
| a부터 b까지 값이 필요하다 | `range(a, b + 1)` | 끝값이 빠지지 않게 `+1` | 반복 (b − a + 1)회 |
| 거꾸로 내려간다 | `range(b, a - 1, -1)` | 진행 방향으로 한 칸 더 간 자리가 끝 | 반복 (b − a + 1)회 |
| 홀수·짝수만 훑는다 | `range`의 간격 2 | 판별 조건 없이 시작값이 홀짝을 정한다 | 반복 약 n/2회 |
| 끝나는 시점이 입력에 달렸다 | `while` 또는 `while True` + `break` | 횟수를 미리 적을 수 없다 | 입력 개수에 비례 |
| 한 번은 반드시 실행해야 한다 | `while True` + `break` | 종료 판단을 본문 아무 자리로 옮길 수 있다 | 상황에 따라 |
| 개수를 센다 | `cnt = 0`, `cnt += 1` | 조건이 참인 회차에만 1씩 | 반복 n회 |
| 값을 더한다 | `total = 0`, `total += x` | 덧셈의 시작은 0 | 반복 n회 |
| 값을 곱한다 | `prod = 1`, `prod *= x` | 곱셈의 시작은 1 (0이면 전부 0) | 반복 n회 |
| 특정 회차만 건너뛴다 | `continue` | 반복은 계속하고 이번 회차만 생략 | 반복 n회 |
| 찾으면 더 볼 필요가 없다 | `break` | 남은 값은 만들어지지도 않는다 | 최악 n회, 보통 더 적음 |
| "하나라도 있는가" | `found = False` + `break` | 하나만 찾으면 결론이 난다 | 최악 n회 |
| "모두 그러한가" | `all_ok = True` + `break` | 어기는 것 하나만 찾으면 결론이 난다 | 최악 n회 |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: `range(a, b)`가 `b`를 포함하지 않는데도 그 규칙이 왜 편한지(개수 = `b - a`).
- [ ] 설명할 수 있다: `range(n)`의 마지막 값과 반복 횟수가 왜 다른지.
- [ ] 설명할 수 있다: `range(b, a - 1, -1)`에서 끝값에 `-1`을 하는 이유.
- [ ] 설명할 수 있다: `for`의 `range` 세 값이 `while`의 어느 세 줄에 각각 대응되는지.
- [ ] 설명할 수 있다: `while`의 조건이 언제 검사되는지, 검사 횟수가 반복 횟수보다 왜 하나 더 많은지.
- [ ] 설명할 수 있다: 누적 변수의 초기화를 반복 밖에 두어야 하는 이유를, 반복 안에 뒀을 때의 결과와 함께.
- [ ] 설명할 수 있다: 합은 0, 곱은 1로 시작하는 이유와, 반복이 0번 돌 때 그 값이 왜 정답인지.
- [ ] 설명할 수 있다: `cnt += 1`과 `total += i`가 어떤 문제에서 각각 쓰이는지.
- [ ] 설명할 수 있다: `continue`와 `break`가 각각 어디로 점프하는지, 그림으로 그려서.
- [ ] 설명할 수 있다: `while`에서 `continue`가 무한 반복을 만드는 상황과 그 해결책.
- [ ] 설명할 수 있다: `while True:`를 안전하게 쓰는 조건("반드시 도달하는 `break`").
- [ ] 설명할 수 있다: 감시 값(센티넬)이 왜 처리 대상이 아닌지.
- [ ] 설명할 수 있다: "하나라도"와 "모두"에서 깃발의 초기값이 서로 반대인 이유.
- [ ] 설명할 수 있다: 출력 줄을 반복 안에 둘 때와 밖에 둘 때 결과가 어떻게 달라지는지.

**⚠️ 자주 하는 실수**

**1) `range(1, n)`으로 써서 마지막 값이 빠짐**

```python
# ❌ 틀린 코드
n = 5
total = 0
for i in range(1, n):       # 1, 2, 3, 4 까지만 (5가 빠진다)
    total = total + i
print(total)
# 출력: 10   (기대한 값은 15)
```

왜: `range(a, b)`는 `b` 바로 앞에서 멈춘다. "1부터 n까지"라는 말은 n을 포함하므로 끝을 `n + 1`로 둬야 한다.

```python
# ✅ 고친 코드
n = 5
total = 0
for i in range(1, n + 1):   # 1, 2, 3, 4, 5
    total = total + i
print(total)
# 출력: 15
```

**2) 누적 변수 초기화를 반복 안에 둠**

```python
# ❌ 틀린 코드
n = 10
for i in range(1, n + 1):
    cnt = 0                 # 매 회차마다 0으로 되돌아간다
    if i % 2 == 0:
        cnt = cnt + 1
print(cnt)
# 출력: 0   (기대한 값은 5)
```

왜: `cnt = 0`이 반복 안에 있으면 매 회차 출발점으로 돌아가므로, 끝났을 때 남는 값은 마지막 회차 하나의 결과뿐이다. 회차를 넘어 살아남아야 하는 변수는 반복 밖에서 만든다.

```python
# ✅ 고친 코드
n = 10
cnt = 0                     # 반복 밖(위)에서 딱 한 번
for i in range(1, n + 1):
    if i % 2 == 0:
        cnt = cnt + 1
print(cnt)
# 출력: 5
```

**3) `while`에서 값을 바꾸는 줄을 빼먹어 무한 반복**

```python
# ❌ 틀린 코드
n = 5
i = 1
while i <= n:
    print(i)
    # i를 늘리는 줄이 없다 -> 조건이 영원히 참
# 출력: 1 이 끝없이 반복된다
```

왜: `while`은 조건이 거짓이 될 때까지 돈다. 조건에 쓰인 변수(`i`)를 본문에서 바꾸지 않으면 조건이 절대 거짓이 되지 않는다.

```python
# ✅ 고친 코드
n = 5
i = 1
while i <= n:
    print(i)
    i = i + 1               # 조건을 거짓으로 만드는 줄
```

**4) 감소 반복에서 간격 `-1`을 빠뜨림**

```python
# ❌ 틀린 코드
n = 5
for i in range(n, 0):       # 간격을 생략하면 +1로 취급된다
    print(i)
# 출력: (아무것도 없음)
```

왜: 간격을 생략하면 `+1`이라 5에서 시작해 커지려 하는데 시작이 이미 끝보다 크다. 그래서 만들 값이 하나도 없다. 거꾸로 돌려면 `-1`을 반드시 적어야 한다.

```python
# ✅ 고친 코드
n = 5
for i in range(n, 0, -1):   # 5, 4, 3, 2, 1
    print(i)
```

**5) 곱을 모으는 변수를 0으로 시작함**

```python
# ❌ 틀린 코드
n = 5
prod = 0                    # 곱셈의 시작이 0이면
for i in range(1, n + 1):
    prod = prod * i         # 무엇을 곱해도 0
print(prod)
# 출력: 0   (기대한 값은 120)
```

왜: 초기값은 "그 연산에서 아무 영향을 주지 않는 값"이어야 한다. 덧셈은 0, 곱셈은 1이다. 이 실수는 오류 없이 답만 틀리므로 발견이 늦다.

```python
# ✅ 고친 코드
n = 5
prod = 1
for i in range(1, n + 1):
    prod = prod * i
print(prod)
# 출력: 120
```

**6) 결과 출력을 반복 안에 두어 여러 번 찍힘**

```python
# ❌ 틀린 코드
n = 3
total = 0
for i in range(1, n + 1):
    total = total + i
    print(total)            # 들여쓰기 = 반복 안 -> 매 회차 출력
# 출력: 1 / 3 / 6 (세 줄)
```

왜: 파이썬은 들여쓰기 깊이로 소속을 정한다. 최종 결과를 한 번만 내려면 출력 줄이 `for`와 같은 깊이(들여쓰기 밖)에 있어야 한다.

```python
# ✅ 고친 코드
n = 3
total = 0
for i in range(1, n + 1):
    total = total + i
print(total)                # 반복이 끝난 뒤 한 번
# 출력: 6
```

**7) `while`에서 `continue`가 증감 줄보다 위에 있음**

```python
# ❌ 틀린 코드
i = 0
while i < 5:
    if i == 3:
        continue            # i를 안 바꾼 채 조건 검사로 돌아간다
    print(i)
    i = i + 1
# i가 3이 되는 순간 같은 회차가 영원히 반복된다
```

왜: `continue`는 이번 회차의 남은 줄을 전부 건너뛴다. 값을 바꾸는 줄이 그 아래에 있으면 실행되지 않아 조건이 영원히 그대로다.

```python
# ✅ 고친 코드
i = 0
while i < 5:
    i = i + 1               # 값을 먼저 바꿔 두고
    if i == 3:
        continue            # 그다음 건너뛴다
    print(i)
# 출력: 1 / 2 / 4 / 5
```

**8) "모두" 판정의 깃발 초기값을 뒤집어 둠**

```python
# ❌ 틀린 코드
nums = input().split()
all_ok = False              # "모두 짝수"인데 거짓으로 시작
for s in nums:
    x = int(s)
    if x % 2 != 0:
        all_ok = True       # 방향까지 반대로 섞였다
print("YES" if all_ok else "NO")
# 2 4 6 을 넣어도 NO 가 나온다
```

왜: "모두 만족"은 "어기는 것이 하나도 없다"와 같은 말이다. 아직 아무것도 검사하지 않은 상태에서는 어긴 것이 하나도 없으므로 참에서 출발해야 한다. 어기는 값을 만났을 때 거짓으로 뒤집는다.

```python
# ✅ 고친 코드
nums = input().split()
all_ok = True               # 모두 만족한다고 가정하고 시작
for s in nums:
    x = int(s)
    if x % 2 != 0:          # 어기는 값(홀수)을 만나면
        all_ok = False
        break
print("YES" if all_ok else "NO")
```

**다음 챕터로**

여기까지가 "값을 하나씩 만들어 내며 훑는" 반복이다. 다음 단계에서는 반복 안에 반복을 넣어(중첩 반복) 격자나 표를 다루고, 값들을 변수 하나하나가 아니라 목록으로 모아 두는 방법을 배운다. 이 챕터의 누적 변수와 깃발 변수는 그대로 쓰이므로, `cnt`/`total`/`prod`의 초기값과 위치를 손에 익혀 두면 그 뒤가 훨씬 수월하다.
