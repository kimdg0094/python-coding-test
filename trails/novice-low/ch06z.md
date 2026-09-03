## L18. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

Ch6에서 배운 것은 결국 한 문장으로 줄어든다. **바깥 `for`가 줄을 만들고, 안쪽 `for`가 그 줄의 칸을 만든다.** 그 위에서 "한 줄에 몇 칸인가"와 "그 칸에 무엇을 찍는가"를 따로 정하기만 하면, 이 챕터의 모든 문제가 같은 틀로 풀린다.

**개념 지도**

```text
  Ch6 core :  for i ( row )  ->  for j ( column )  ->  print(c, end="")
                                                  ->  print()    # row end

  decide 1 : HOW MANY cells in this row      ( inner loop range )
  +- fixed w                -> rectangle                   L1
  +- i + 1   /   n - i      -> right triangle              L2  L3
  +- 2*i + 1  ( + spaces )  -> centered pyramid , diamond  L4  L5
  +- always n , use if      -> border , diagonal , checker L5  L6  L7

  decide 2 : WHAT to put in each cell        ( the printed value )
  +- "*"                    -> star patterns               L1..L7
  +- j    or    i           -> column / row number         L8  L11
  +- cnt  ( cnt += 1 )      -> running number              L10
  +- i + j   ,   i * j      -> formula table , times table L9  L12
  +- f"{v:3d}"              -> aligned columns             L14
  +- chr(ord("A") + k)      -> alphabet                    L15

  decide 3 : REPEAT the whole drawing        ( test cases )
  +- for t in range(T)      -> read , draw , blank line    L16
```

세 결정은 서로 독립이다. 모양(decide 1)을 그대로 두고 값(decide 2)만 바꾸면 별 삼각형이 숫자 삼각형이 되고, 알파벳 삼각형이 된다.

정렬이 필요한 도형은 한 줄을 두 덩어리로 쪼개는 것이 전부다.

```text
  one line  =  [ spaces ]  +  [ content ]     # 두 덩어리의 합이 그 줄의 폭

    right aligned ( n = 4 )         centered ( n = 3 )
      i=1     . . . *                 i=0     . . *
      i=2     . . * *                 i=1     . * * *
      i=3     . * * *                 i=2     * * * * *
      i=4     * * * *
    spaces = n - i                  spaces = n - 1 - i
    stars  = i                      stars  = 2*i + 1
    sum    = n   ( constant )       center = column n-1   ( constant )
```

`.`은 실제로는 공백이다. 오른쪽 맞춤은 두 덩어리의 **합**이 일정하고, 가운데 정렬은 별 덩어리의 **한가운데 열**이 일정하다. 무엇이 고정되는지만 알면 식이 저절로 나온다.

**뼈대 코드**

이 챕터 유형을 만나면 아래 골격 중 하나를 그대로 꺼내 쓰고, `←` 표시된 자리만 문제에 맞춰 고친다.

① 기본 틀 — 모든 줄의 칸 수가 같은 도형

```python
n = int(input())              # ← 문제마다 바뀜 (입력 형태)
for i in range(n):            # 바깥: 줄
    for j in range(n):        # ← 문제마다 바뀜 (한 줄의 칸 수)
        print("*", end="")    # ← 문제마다 바뀜 (찍을 것)
    print()                   # 줄바꿈은 항상 안쪽 for '밖'
```

② 줄마다 칸 수가 달라지는 도형

```python
n = int(input())
for i in range(n):                 # i = 0 .. n-1
    cells = i + 1                  # ← 문제마다 바뀜: i+1 / n-i / 2*i / 2*i+1
    for j in range(cells):
        print("*", end="")
    print()
```

③ 정렬이 있는 도형 — 공백 덩어리 + 내용 덩어리

```python
n = int(input())
for i in range(n):
    spaces = n - 1 - i             # ← 문제마다 바뀜 (앞 공백 개수)
    stars = 2 * i + 1              # ← 문제마다 바뀜 (내용 개수)
    for j in range(spaces):
        print(" ", end="")
    for j in range(stars):
        print("*", end="")
    print()
```

④ 조건으로 칸을 채우기 — 테두리·대각선·무늬

```python
n = int(input())
for i in range(n):
    for j in range(n):             # 범위는 항상 0..n-1 로 고정한다
        if i == 0 or i == n - 1 or j == 0 or j == n - 1:   # ← 문제마다 바뀜
            print("*", end="")
        else:
            print(" ", end="")     # 두 가지 모두 한 글자씩 (폭 유지)
    print()
```

⑤ 숫자 채우기 — 카운터·공식·폭 정렬

```python
n = int(input())
cnt = 1                            # 이어지는 번호면 반복문 '밖'에서 초기화
for i in range(1, n + 1):
    for j in range(1, n + 1):
        value = cnt                # ← 문제마다 바뀜: cnt / i+j / i*j / i / j
        print(f"{value:4d}", end="")   # ← 문제마다 바뀜 (폭, 구분자)
        cnt += 1
    print()
```

⑥ 테스트 케이스 반복

```python
T = int(input())
for t in range(T):
    n = int(input())               # ← 케이스마다 새로 읽는다
    cnt = 1                        # ← 케이스마다 초기화할 것은 여기에
    for i in range(n):
        for j in range(n):
            print("*", end="")
        print()
    print()                        # ← 케이스 구분 빈 줄 (형식에 따라)
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 총 출력 칸 |
| --- | --- | --- | --- |
| 모든 줄의 칸 수가 같다 | 안쪽 `range(w)` 고정 | 줄 번호와 무관하게 개수가 정해진다 | `h × w` |
| 줄마다 칸 수가 늘거나 줄어든다 | 안쪽 `range(i+1)` 또는 `range(n-i)` | 안쪽 횟수를 바깥 변수에 연동한다 | `n(n+1)/2` |
| 도형을 가운데·오른쪽에 맞춘다 | [공백 `for`] + [내용 `for`] | 한 줄이 두 덩어리로 쪼개진다 | `n²` 안팎 |
| 위아래로 대칭이다 | 반복문 두 개, 아래쪽은 `range(n-1)` | 가운데 줄이 두 번 나오는 것을 막는다 | `2n-1`줄 |
| 칸마다 찍을지가 규칙으로 갈린다 | 안쪽 `range(n)` 고정 + `if`/`else` | 칸 수를 유지해야 열이 밀리지 않는다 | `n²` |
| 번호가 줄을 넘어 이어진다 | `cnt`를 반복문 밖에서 초기화 | 초기화 위치가 곧 초기화 횟수다 | `n²` |
| 칸의 값이 위치만으로 정해진다 | `i`·`j` 공식 (`i+j`, `i*j`, `j*h+i+1`) | 카운터 없이 바로 계산된다 | `n²` |
| 자릿수가 달라도 세로줄을 맞춰야 한다 | `f"{v:{w}d}"` | 모든 칸이 같은 폭을 차지한다 | `n²` |
| 문자를 규칙적으로 찍는다 | `chr(ord('A') + k % 26)` | 코드값이 연속이라 덧셈이 통한다 | `n²` |
| 같은 처리를 여러 케이스에 반복한다 | 맨 바깥에 `for t in range(T)` | 안쪽 코드를 그대로 재사용한다 | `T × n²` |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 바깥 `for`와 안쪽 `for`가 각각 무엇을 담당하는지, 그리고 줄바꿈 `print()`가 왜 안쪽 `for` 밖에 있어야 하는지.
- [ ] 설명할 수 있다: `end=""`를 쓰면 왜 출력이 옆으로 이어지는지, 빼면 어떤 모양이 되는지.
- [ ] 설명할 수 있다: "안쪽 반복 횟수를 바깥 변수에 연동한다"는 말의 뜻과, `i+1`·`n-i`·`2*i+1`이 각각 어떤 모양을 만드는지.
- [ ] 설명할 수 있다: 안쪽 반복이 `i`에 매달릴 때 총 실행 횟수가 왜 `1+2+…+n = n(n+1)/2`가 되는지.
- [ ] 설명할 수 있다: 가운데 정렬에서 앞 공백 `n-1-i`와 별 `2*i+1`을 쓰면 왜 한가운데가 항상 같은 열에 오는지.
- [ ] 설명할 수 있다: 가운데 정렬 도형의 별 개수가 왜 홀수여야 하는지.
- [ ] 설명할 수 있다: 위아래 대칭 도형에서 아래쪽 반복이 왜 `range(n-1)`이어야 하는지.
- [ ] 설명할 수 있다: 조건으로 칸을 채울 때 안쪽 반복 범위를 왜 건드리면 안 되는지, `if`의 두 가지에서 왜 각각 한 글자씩 찍어야 하는지.
- [ ] 설명할 수 있다: `i == j`, `j == n-1-i`, `(i+j) % 2`가 각각 어떤 무늬를 만드는지와 그 이유.
- [ ] 설명할 수 있다: `cnt`를 반복문 밖·바깥 `for` 안·안쪽 `for` 안에 두었을 때 결과가 어떻게 달라지는지.
- [ ] 설명할 수 있다: 세로 우선 번호 공식 `value = j*h + i + 1`이 어떻게 유도되는지.
- [ ] 설명할 수 있다: 구구단에서 두 `for`의 순서를 바꾸면 왜 출력이 세로에서 가로로 바뀌는지.
- [ ] 설명할 수 있다: `f"{v:3d}"`가 세로줄을 맞추는 원리와, 폭을 "자릿수 + 1"로 잡는 이유.
- [ ] 설명할 수 있다: `chr(ord('A') + k)`가 성립하는 조건과 `% 26`이 필요한 이유.
- [ ] 설명할 수 있다: 케이스 반복이 붙었을 때 입력 읽기와 변수 초기화를 각각 어디에 두어야 하는지.

**⚠️ 자주 하는 실수**

**1) 줄바꿈을 안쪽 `for` 안에 넣는다**

```python
# ❌ 틀린 코드
for i in range(3):
    for j in range(4):
        print("*", end="")
        print()          # 안쪽 for '안'
```

왜: 별 하나를 찍을 때마다 줄이 바뀐다. 3×4 사각형이 아니라 별 한 개짜리 줄이 12개 나온다. 줄바꿈은 "한 줄이 끝났을 때" 한 번이어야 한다.

```python
# ✅ 고친 코드
for i in range(3):
    for j in range(4):
        print("*", end="")
    print()              # 안쪽 for '밖', 바깥 for '안'
```

**2) `end=""`를 빠뜨린다**

```python
# ❌ 틀린 코드
for i in range(3):
    for j in range(4):
        print("*")
    print()
```

왜: `print`는 기본으로 뒤에 줄바꿈을 붙인다. 별이 옆으로 이어지지 않고 세로로 늘어서며, 바깥의 `print()`까지 더해져 빈 줄이 섞인다.

```python
# ✅ 고친 코드
for i in range(3):
    for j in range(4):
        print("*", end="")
    print()
```

**3) 안쪽 반복 범위를 바깥 변수에 연동하지 않는다**

```python
# ❌ 틀린 코드
n = 4
for i in range(n):
    for j in range(n):       # 항상 n 개
        print("*", end="")
    print()
```

왜: 삼각형을 원했는데 모든 줄이 `n`개라 사각형이 나온다. "줄마다 개수가 다르다"는 조건이 코드에 전혀 반영되지 않았다.

```python
# ✅ 고친 코드
n = 4
for i in range(n):
    for j in range(i + 1):   # 1, 2, 3, 4 개
        print("*", end="")
    print()
```

**4) `range(n)`과 `range(1, n+1)`을 혼동한다**

```python
# ❌ 틀린 코드
n = 3
for i in range(n):           # i = 0, 1, 2
    for j in range(2 * i):   # 0, 2, 4 개 -> 첫 줄이 비어 버린다
        print("*", end="")
    print()
```

왜: 문제는 "`i`번째 줄에 `2*i`개"이고 줄 번호를 1부터 센다. 그런데 `range(n)`의 `i`는 0부터라 첫 줄이 0개가 된다. 공식이 1-기준이면 반복도 1-기준으로 맞춰야 한다.

```python
# ✅ 고친 코드
n = 3
for i in range(1, n + 1):    # i = 1, 2, 3
    for j in range(2 * i):   # 2, 4, 6 개
        print("*", end="")
    print()
```

**5) 카운터 초기화를 반복문 안에 둔다**

```python
# ❌ 틀린 코드
n = 3
for i in range(n):
    cnt = 1                  # 줄마다 초기화
    for j in range(n):
        print(cnt, end=' ')
        cnt += 1
    print()
```

왜: 매 줄 `cnt`가 1로 돌아가 `1 2 3` / `1 2 3` / `1 2 3`이 나온다. "전체에 걸쳐 이어지는 번호"가 되려면 초기화가 딱 한 번이어야 한다.

```python
# ✅ 고친 코드
n = 3
cnt = 1                      # 반복문 '밖'에서 한 번만
for i in range(n):
    for j in range(n):
        print(cnt, end=' ')
        cnt += 1
    print()
```

**6) 대칭 도형에서 가운데 줄을 두 번 출력한다**

```python
# ❌ 틀린 코드
n = 3
for i in range(n):           # 별 1, 2, 3 개
    print("*" * (i + 1))
for i in range(n):           # 별 3, 2, 1 개 -> 3 이 또 나온다
    print("*" * (n - i))
```

왜: 위쪽 반복이 이미 별 `n`개짜리 줄을 찍었는데 아래쪽이 다시 `n`개부터 시작한다. 가장 넓은 줄이 두 번 나와 대칭이 깨지고, 줄 수도 `2n-1`이 아니라 `2n`이 된다.

```python
# ✅ 고친 코드
n = 3
for i in range(n):           # 별 1, 2, 3 개
    print("*" * (i + 1))
for i in range(n - 1):       # 별 2, 1 개
    print("*" * (n - 1 - i))
```

**7) 조건으로 칸을 채울 때 `else`를 빠뜨린다**

```python
# ❌ 틀린 코드
n = 4
for i in range(n):
    for j in range(n):
        if i == j:
            print("*", end="")
    print()
```

왜: 조건이 거짓인 칸에서 아무것도 찍히지 않아 그 칸이 통째로 사라진다. 뒤 칸이 왼쪽으로 밀려 모든 줄이 `*` 하나짜리가 되고, 대각선이 세로줄처럼 보인다.

```python
# ✅ 고친 코드
n = 4
for i in range(n):
    for j in range(n):
        if i == j:
            print("*", end="")
        else:
            print(" ", end="")   # 거짓일 때도 한 글자 (폭 유지)
    print()
```

**8) 케이스마다 입력을 다시 읽지 않는다**

```python
# ❌ 틀린 코드
T = int(input())
n = int(input())             # 한 번만 읽음
for t in range(T):
    for i in range(n):
        print("*" * n)
    print()
```

왜: 두 번째 케이스부터 첫 케이스의 `n`을 그대로 쓴다. 케이스마다 값이 달라지는 입력은 반드시 케이스 반복 **안**에서 읽어야 한다.

```python
# ✅ 고친 코드
T = int(input())
for t in range(T):
    n = int(input())         # 케이스마다 새로 읽는다
    for i in range(n):
        print("*" * n)
    print()
```

**다음 챕터로**

여기서 익힌 "바깥은 행, 안쪽은 열"이라는 감각은 그대로 2차원 격자 문제의 기초가 된다. 지금은 계산한 값을 바로 화면에 찍었지만, 다음 단계에서는 그 값을 배열에 **저장해 두고** 나중에 꺼내 쓴다. 값을 담을 자리가 필요해지는 셈이고, 그 준비가 바로 이어지는 1차원 배열 챕터다.
