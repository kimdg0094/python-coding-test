## L8. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

Ch7의 핵심은 하나다. **여러 값을 이름 하나로 묶어 두면, 그다음부터는 "인덱스로 한 칸 꺼내기"와 "반복문으로 전부 훑기" 두 가지 동작만으로 거의 모든 처리가 된다.** 합·개수·최댓값·탐색·등장 횟수는 전부 "훑으면서 무언가를 갱신하는" 같은 모양의 코드다.

C++에서는 여기에 두 가지 책임이 더 붙는다. **칸을 몇 개 잡을지 스스로 정해야 하고, 그 칸 안에 머무는지도 스스로 지켜야 한다.** 파이썬처럼 `IndexError`가 대신 알려 주지 않기 때문이다.

**개념 지도**

```text
  Ch7 core :  many values  ->  one name ( vector )  ->  index  /  loop

  step 1 : GET the array
  +- while (cin >> x) arr.push_back(x);   one line of numbers     L1
  +- vector<int> arr;  then push_back     build it up             L3
  +- vector<int> v(n, 0);                 size n , all zeros      L3
  +- int cnt[SIZE] = {0};                 fixed size , all zeros  L4

  step 2 : REACH one value
  +- arr[0]                               first                L2
  +- arr[arr.size() - 1]                  last                 L2
  +- arr[k - 1]                           k-th , counted from 1  L2

  step 3 : WALK the array
  +- for (int v : arr)                    value only           L1 L4 L6
  +- for (int i = 0; i < (int)arr.size(); i++)   position needed  L5 L6

  step 4 : SUMMARISE while walking
  +- total += v;                          sum                  L1
  +- if (v > t) count++;                  count by condition   L5
  +- if (arr[i] == x) { pos = i; break; } first position       L5
  +- if (arr[i] == x) pos = i;            last position        L5
  +- if (v > mx) mx = v;                  max  /  min          L6
  +- cnt[v]++;                            how many times each  L4
```

step 4의 다섯 줄은 전부 같은 자리에 들어간다. 그래서 여러 집계를 한 번의 순회로 동시에 처리할 수 있다.

```text
  one pass over  arr = {4, 9, 2, 7}      # 반복 한 바퀴로 네 가지를 동시에

    v       total   count(v>3)    mx    mn
    -----   -----   ----------   ---   ---
    start       0            0     4     4
    4           4            1     4     4
    9          13            2     9     4
    2          15            2     9     2
    7          22            3     9     2
```

`mx`와 `mn`의 시작값이 `0`이 아니라 `arr[0] = 4`인 점을 눈여겨보자. 이 한 가지가 음수만 있는 입력에서 정답과 오답을 가른다.

C++에서만 새로 생기는 지뢰는 아래 셋이다. 셋 다 **오류 메시지 없이** 틀린다.

```text
  trap 1 : out of range        arr[n] , arr[-1]  ->  garbage , no error
  trap 2 : no initial value    int cnt[10];      ->  garbage in every box
  trap 3 : unsigned size()     arr.size() - 1    ->  huge number when empty

           empty vector :  size() = 0
                           size() - 1 = 4294967295   # -1 이 아니다
           so  for (int i = 0; i <= arr.size() - 1; i++)  never stops
```

**뼈대 코드**

배열 문제를 만나면 아래 골격 중 하나를 꺼내 쓰고, `<-` 표시된 자리만 문제에 맞춰 고친다.

① 입력 → 배열 → 집계(합·개수)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<int> arr;
    int x;
    while (cin >> x) arr.push_back(x);   // <- 문제마다 바뀜 (입력 형태)

    int total = 0;                       // 누적 변수는 반복 '밖'에서 초기화
    int count = 0;
    for (int i = 0; i < (int)arr.size(); i++) {
        total += arr[i];
        if (arr[i] > 0) {                // <- 문제마다 바뀜 (세는 조건)
            count++;
        }
    }
    cout << total << " " << count << "\n";
    return 0;
}
```

② 최댓값·최솟값과 그 위치

```cpp
vector<int> arr;
int x;
while (cin >> x) arr.push_back(x);

int mx = arr[0];              // 실제 원소로 시작 (상수로 시작하지 않는다)
int mn = arr[0];
for (int i = 0; i < (int)arr.size(); i++) {
    if (arr[i] > mx) mx = arr[i];    // <- 문제마다 바뀜 (조건과 갱신 대상)
    if (arr[i] < mn) mn = arr[i];
}
int pos = 0;
for (int i = 0; i < (int)arr.size(); i++) {
    if (arr[i] == mx) {
        pos = i + 1;          // 사람이 세는 위치 = 인덱스 + 1
        break;                // <- 처음 위치면 break, 마지막 위치면 지운다
    }
}
cout << mx << " " << mn << " " << pos << "\n";
```

③ 탐색 — 있는지, 몇 번째인지

```cpp
int n;
cin >> n;
vector<int> arr(n);
for (int i = 0; i < n; i++) cin >> arr[i];
int x;
cin >> x;

int pos = -1;                 // 못 찾음 표시 (정답으로는 나올 수 없는 값)
for (int i = 0; i < n; i++) { // 위치가 필요하니 인덱스 반복
    if (arr[i] == x) {        // <- 문제마다 바뀜 (찾는 조건)
        pos = i + 1;
        break;                // <- "처음"만 필요할 때만 둔다
    }
}
cout << pos << "\n";
```

④ 카운트 배열 — 값별 등장 횟수

```cpp
#include <bits/stdc++.h>
using namespace std;

const int SIZE = 101;         // <- 문제마다 바뀜 (나올 수 있는 최댓값 + 1)

int main() {
    int cnt[SIZE] = {0};      // = {0} 을 빼면 쓰레기 값이 남는다
    int v;
    while (cin >> v) {
        cnt[v]++;             // 값 자체를 인덱스로 쓴다
    }
    int best = 0;
    for (int d = 0; d < SIZE; d++) {
        if (cnt[d] > cnt[best]) {   // > 라서 동점이면 먼저 본 작은 값이 남는다
            best = d;
        }
    }
    cout << best << "\n";
    return 0;
}
```

⑤ 새 배열 만들기 — 생성·변환

```cpp
int n;
cin >> n;
vector<int> arr;              // 빈 배열에서 시작
for (int i = 1; i <= n; i++) {          // <- 문제마다 바뀜 (범위, 방향)
    arr.push_back(i * i);               // <- 문제마다 바뀜 (담을 값)
}
for (int i = 0; i < (int)arr.size(); i++) {
    if (i > 0) cout << " ";   // 값 '앞'에 공백 -> 끝에 군더더기가 없다
    cout << arr[i];
}
cout << "\n";
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 훑는 횟수 |
| --- | --- | --- | --- |
| 값만 필요하다 | `for (int v : arr)` | 인덱스를 쓸 일이 없어 짧고 안전하다 | `n` |
| 몇 번째인지가 필요하다 | `for (int i = 0; i < (int)arr.size(); i++)` | `arr[i]`와 `i`를 함께 쓸 수 있다 | `n` |
| 이웃한 두 값을 비교한다 | `i < (int)arr.size() - 1` | 마지막 칸은 짝이 없다 | `n-1` |
| 처음 나오는 위치를 찾는다 | 찾으면 `break` | 뒤를 더 볼 필요가 없다 | 최대 `n` |
| 마지막 나오는 위치를 찾는다 | `break` 없이 계속 덮어쓴다 | 마지막으로 덮인 값이 답이다 | `n` |
| 합·개수를 구한다 | 누적 변수를 0에서 시작 | 아무것도 안 더한 상태가 0이다 | `n` |
| 최댓값·최솟값을 구한다 | `arr[0]`을 시작 기준으로 | 배열 밖의 값이 답이 될 수 없다 | `n` |
| 값별 등장 횟수를 센다 | 카운트 배열 `int cnt[최댓값+1] = {0};` | 값을 인덱스로 쓰면 한 번에 접근된다 | `n` + 배열 크기 |
| 크기를 실행 중에 정해야 한다 | `vector<int> v(n, 0);` | 고정 크기 배열은 상수만 받는다 | `n` |
| 크기가 미리 정해져 있다 | `int a[SIZE] = {0};` | 선언 한 줄로 초기화까지 끝난다 | `n` |
| 배열을 함수에 넘긴다 | `void f(const vector<int>& v)` | `&`가 없으면 통째로 복사된다 | — |
| 원본을 남기고 걸러낸다 | 새 `vector`에 `push_back` | 순회 중 삭제는 인덱스가 어긋난다 | `n` |
| 합이 커질 수 있다 | `long long total = 0;` | `int`는 약 21억에서 넘친다 | `n` |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: `while (cin >> x)`가 왜 "남은 값이 있는 동안"이라는 뜻이 되는지.
- [ ] 설명할 수 있다: 인덱스가 왜 0부터 시작하고, 마지막이 왜 `arr.size() - 1`인지.
- [ ] 설명할 수 있다: 사람이 세는 "K번째"와 인덱스 사이의 1칸 차이가 어디서 생기는지.
- [ ] 설명할 수 있다: C++에서 `arr[n]`이나 `arr[-1]`을 읽으면 무슨 일이 일어나는지, 그리고 그것이 파이썬의 `IndexError`보다 왜 더 위험한지.
- [ ] 설명할 수 있다: `arr.size()`가 음수 없는 정수라서 생기는 함정과, `(int)`로 감싸면 왜 해결되는지.
- [ ] 설명할 수 있다: 두 칸의 값을 맞바꿀 때 임시 변수가 왜 필요한지.
- [ ] 설명할 수 있다: `vector<int> b = a;`가 파이썬의 `b = a`와 어떻게 다른지.
- [ ] 설명할 수 있다: 함수에 `vector`를 넘길 때 `&`를 붙이는 것과 안 붙이는 것의 차이.
- [ ] 설명할 수 있다: `int c[5];`와 `int c[5] = {0};`의 차이와, 초기화를 빠뜨리면 어떤 증상이 나타나는지.
- [ ] 설명할 수 있다: 고정 크기 배열의 크기가 왜 상수여야 하는지와, 그럴 수 없을 때 무엇을 쓰는지.
- [ ] 설명할 수 있다: 카운트 배열의 크기를 "나올 수 있는 최댓값 + 1"로 잡아야 하는 이유.
- [ ] 설명할 수 있다: 카운트 배열에서 동점일 때 작은 값이 남는 것이 왜 부등호 하나로 결정되는지.
- [ ] 설명할 수 있다: 탐색에서 `break`의 유무가 "처음"과 "마지막"을 어떻게 가르는지.
- [ ] 설명할 수 있다: 못 찾았을 때 표시로 `-1`을 쓰는 이유와, `0`이 위험할 수 있는 경우.
- [ ] 설명할 수 있다: 최댓값의 시작 기준을 `arr[0]`으로 두는 이유와, 상수로 두면 어떤 입력에서 틀리는지.
- [ ] 설명할 수 있다: 누적 변수의 초기화를 반복문 밖에 두어야 하는 이유.
- [ ] 설명할 수 있다: 합이 `int` 범위를 넘을 수 있는 상황을 어떻게 알아채고 무엇으로 바꾸는지.

**⚠️ 자주 하는 실수**

**1) `arr[i + 1]`로 배열 밖을 읽는다**

```cpp
// ❌ 틀린 코드
for (int i = 0; i < (int)arr.size(); i++) {
    if (arr[i] == arr[i + 1]) {   // 마지막 i 에서 arr[size()] 를 읽는다
        cout << "same\n";
    }
}
```

왜: 마지막 `i`는 `size() - 1`이다. 거기서 `arr[i + 1]`은 존재하지 않는 칸이다. 파이썬이라면 `IndexError`로 멈췄겠지만 C++은 아무 말 없이 쓰레기 값을 읽어 조용히 틀린다.

```cpp
// ✅ 고친 코드
for (int i = 0; i < (int)arr.size() - 1; i++) {   // 마지막 칸은 짝이 없다
    if (arr[i] == arr[i + 1]) {
        cout << "same\n";
    }
}
```

**2) "K번째"를 그대로 인덱스로 쓴다**

```cpp
// ❌ 틀린 코드
int k;
cin >> k;
cout << arr[k];                   // 1부터 세는 위치를 그대로 인덱스로
```

왜: 사람은 1부터, 인덱스는 0부터 센다. `K`번째 값은 `arr[K - 1]`이다. `arr[k]`는 한 칸 뒤 값이고, `K`가 개수와 같으면 배열 밖을 읽는다.

```cpp
// ✅ 고친 코드
int k;
cin >> k;
cout << arr[k - 1];
```

**3) 초기화하지 않은 배열을 쓴다**

```cpp
// ❌ 틀린 코드
int cnt[101];                     // = {0} 이 없다
for (int i = 0; i < n; i++) {
    cnt[arr[i]]++;                // 쓰레기 값에서 세기 시작한다
}
```

왜: C++은 지역 배열을 0으로 채워 주지 않는다. 각 칸에 이전에 그 메모리를 쓰던 값이 남아 있어, 실행할 때마다 결과가 달라진다. 파이썬 `[0] * 101`에는 없던 함정이다.

```cpp
// ✅ 고친 코드
int cnt[101] = {0};               // 모든 칸이 0 으로 시작한다
for (int i = 0; i < n; i++) {
    cnt[arr[i]]++;
}
```

**4) `size()`를 정수처럼 빼서 쓴다**

```cpp
// ❌ 틀린 코드
vector<int> arr;                  // 비어 있을 수 있다
for (int i = 0; i <= arr.size() - 1; i++) {
    cout << arr[i];               // 배열이 비면 반복이 끝나지 않는다
}
```

왜: `size()`는 음수가 없는 정수라 `0 - 1`이 `-1`이 아니라 아주 큰 수가 된다. 조건이 계속 참이라 반복이 멈추지 않고, 배열 밖을 계속 읽는다.

```cpp
// ✅ 고친 코드
for (int i = 0; i < (int)arr.size(); i++) {   // 빼지 말고 '<' 로 비교한다
    cout << arr[i];
}
```

**5) 누적 변수 초기화를 반복문 안에 둔다**

```cpp
// ❌ 틀린 코드
for (int i = 0; i < n; i++) {
    int total = 0;                // 반복 '안'에서 선언
    total += arr[i];
    cout << total;                // 매번 arr[i] 하나만 나온다
}
```

왜: 매 반복마다 `total`이 새로 만들어져 0으로 되돌아가므로 누적이 되지 않는다. C++에서는 블록을 벗어나면 변수 자체가 사라진다는 점까지 겹친다.

```cpp
// ✅ 고친 코드
int total = 0;                    // 반복 '밖'에서 한 번만
for (int i = 0; i < n; i++) {
    total += arr[i];
}
cout << total;
```

**6) 최댓값을 상수로 시작한다**

```cpp
// ❌ 틀린 코드
int mx = 0;                       // 상수로 시작
for (int i = 0; i < n; i++) {
    if (arr[i] > mx) mx = arr[i];
}
cout << mx;                       // 입력이 -3 -8 -1 이면 0 이 나온다
```

왜: 모든 값이 0보다 작으면 갱신이 한 번도 일어나지 않아, 배열에 없던 0이 답이 되어 버린다. 시작 기준은 반드시 실제 원소여야 한다.

```cpp
// ✅ 고친 코드
int mx = arr[0];                  // 실제 원소로 시작하면 언제나 안전하다
for (int i = 0; i < n; i++) {
    if (arr[i] > mx) mx = arr[i];
}
cout << mx;
```

**7) 카운트 배열 크기를 작게 잡는다**

```cpp
// ❌ 틀린 코드
int cnt[10] = {0};                // 값이 0 ~ 100 까지 나올 수 있다
for (int i = 0; i < n; i++) {
    cnt[arr[i]]++;                // 값이 10 이상이면 남의 메모리를 건드린다
}
```

왜: 카운트 배열은 값 자체를 인덱스로 쓴다. 값 100을 세려면 인덱스 100이 있어야 하고, 그러려면 크기가 101이어야 한다. C++은 크기를 넘어도 오류를 내지 않고 옆 변수를 조용히 망가뜨린다.

```cpp
// ✅ 고친 코드
int cnt[101] = {0};               // 0 부터 100 까지 모두 담는다
for (int i = 0; i < n; i++) {
    cnt[arr[i]]++;
}
```

**8) 큰 배열을 값으로 넘긴다**

```cpp
// ❌ 틀린 코드
int sum(vector<int> v) {          // 부를 때마다 통째로 복사된다
    int t = 0;
    for (int i = 0; i < (int)v.size(); i++) t += v[i];
    return t;
}
```

왜: `vector`는 대입과 인자 전달에서 값을 전부 복사한다(파이썬과 반대다). 원소가 수십만 개면 계산보다 복사가 더 오래 걸린다.

```cpp
// ✅ 고친 코드
int sum(const vector<int>& v) {   // & 로 원본을 그대로 가리킨다
    int t = 0;
    for (int i = 0; i < (int)v.size(); i++) t += v[i];
    return t;
}
```

**9) 합이 `int` 범위를 넘는다**

```cpp
// ❌ 틀린 코드
int total = 0;
for (int i = 0; i < n; i++) {
    total += arr[i];              // 값이 크고 개수가 많으면 넘친다
}
cout << total;                    // 음수가 튀어나오기도 한다
```

왜: `int`는 약 21억까지만 담는다. 넘으면 오류가 아니라 값이 한 바퀴 돌아 엉뚱한 수가 된다. 파이썬 정수에는 한계가 없어 겪지 않던 문제다.

```cpp
// ✅ 고친 코드
long long total = 0;              // 약 900경까지 담는다
for (int i = 0; i < n; i++) {
    total += arr[i];
}
cout << total;
```

**다음 챕터로**

지금은 값이 한 줄로 늘어선 배열을 다뤘다. 여기에 "줄"이라는 축이 하나 더 붙으면 2차원 배열, 곧 격자가 된다. Ch6에서 익힌 `for i` / `for j` 구조와 이 챕터의 인덱스 감각이 만나는 지점이다. 인덱스가 0부터 시작한다는 사실, 초기화 위치, 그리고 "칸 밖을 읽어도 아무도 말해 주지 않는다"는 C++의 성질은 그때도 똑같이 발목을 잡으니 지금 확실히 굳혀 두는 편이 이득이다.
