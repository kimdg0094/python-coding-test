## L8. 정리 — 개념 지도·체크리스트·자주 하는 실수

**개념**

- 이 레슨은 Ch2(배열·연결 리스트) 전체를 한 장의 판단표로 접는다. 자료구조를 고르는 일은 취향이 아니라 **"어떤 연산을 몇 번 하는가"에 대한 산술**이다.

- C++에서는 여기에 두 가지 질문이 더 붙는다 — **"메모리를 누가 회수하는가"**(`new`/`delete`)와 **"내가 들고 있는 포인터·반복자가 아직 살아 있는가"**(무효화). 파이썬에는 없던 이 둘이 연결 리스트 구현의 난이도를 결정한다.

**개념 지도**

```text
                        sequence container
                                 |
              +------------------+-------------------+
         contiguous                            linked nodes
              |                                      |
    +---------+---------+            +---------------+---------------+
  array           vector           singly         doubly         circular
  fixed size      grow x 2         val + next     prev + next    tail->next
  a[i] O(1)       push_back O(1)*  push_front     erase(node)    = head
  insert O(n)     * amortized      search O(n)    sentinels      rotate
  shift back      size vs cap      dummy head     list / deque   josephus
  int[N]          reserve          new / delete   erase(it)      do-while
              |                                      |
              +------------------+-------------------+
                                 |
                            Iterator
              begin() / end() / ++it / *it / it != end()
              # 내부 구조를 숨기고 range-for 하나로 순회한다
```

이 챕터는 하나의 질문에서 갈라진다 — **"원소들을 붙여 놓을 것인가, 화살표로 이을 것인가."**

- 붙여 놓으면(배열·`vector`) 주소 계산으로 어디든 O(1)에 가지만, 가운데를 건드릴 때마다 뒤를 전부 밀어야 한다.
- 화살표로 이으면(연결 리스트) 링크 한두 개만 고쳐 O(1)에 끼우고 뺄 수 있지만, `i`번째를 찾으려면 처음부터 걸어가야 한다.
- `vector`는 배열 쪽 가지에서 "크기 고정"이라는 제약만 없앤 것이고(2배 확장 + 분할상환), 이중·원형 리스트는 연결 리스트 쪽 가지에서 "뒤로 못 간다·끝이 있다"는 제약을 없앤 것이다.
- Iterator는 두 갈래 위에 얹는 공통 껍데기다. 내부가 배열이든 사슬이든 `for (auto x : obj)` 한 줄로 같게 보이게 만든다. STL 알고리즘이 컨테이너를 가리지 않는 이유도 이것이다.
- 등급 표만 보면 연결 리스트가 유리해 보이지만, **실측에서는 `vector`가 이기는 경우가 훨씬 많다.** CPU가 메모리를 캐시 라인 단위로 읽어 오기 때문이다. 연결 리스트를 고를 이유는 "노드 참조를 이미 손에 쥐고 있고 그 자리를 O(1)에 떼어내야 할 때"로 좁혀진다.

**뼈대 코드**

```cpp
// 1) 단일 연결 리스트 - 노드 / 삽입 / 삭제 / 순회 골격
struct Node {
    int val;
    Node* next;
    Node(int v) : val(v), next(nullptr) {}
};

Node* build(const vector<int>& vals) {     // 뒤에 이어 붙이며 만들기
    Node dummy(0);                         // 스택에 두면 delete 가 필요 없다
    Node* tail = &dummy;
    for (int v : vals) {
        tail->next = new Node(v);
        tail = tail->next;
    }
    return dummy.next;
}

void insert_after(Node* cur, int x) {      // cur 바로 뒤에 삽입 O(1)
    Node* node = new Node(x);
    node->next = cur->next;                // 순서 고정 : 새 노드부터
    cur->next = node;
}

Node* remove_all(Node* head, int target) { // 값이 target 인 노드 모두 삭제
    Node dummy(0); dummy.next = head;
    Node* cur = &dummy;
    while (cur->next) {
        if (cur->next->val == target) {    // 문제마다 바뀜(삭제 조건)
            Node* dead = cur->next;
            cur->next = dead->next;        // 먼저 링크를 잇고
            delete dead;                   // 그다음 해제 - 순서 중요
        } else {
            cur = cur->next;               // 안 지웠을 때만 전진
        }
    }
    return dummy.next;
}

void walk(Node* head) {                    // 순회 O(n)
    for (Node* cur = head; cur; cur = cur->next)
        cout << cur->val << ' ';
    cout << '\n';
}
```

```cpp
// 2) 이중 연결 리스트 - 센티넬 두 개로 경계 분기를 없앤다
struct DNode {
    int val;
    DNode *prev, *next;
    DNode(int v = 0) : val(v), prev(nullptr), next(nullptr) {}
};

DNode H, T;                                // head / tail 센티넬 (전역)
void init_dlist() { H.next = &T; T.prev = &H; }   // 빈 상태도 정상 상태

DNode* insert_after_d(DNode* a, int x) {   // a 뒤에 x 삽입 - 링크 4개
    DNode* b = a->next;
    DNode* node = new DNode(x);
    node->prev = a; node->next = b;        // (1)(2) 새 노드 쪽 먼저
    a->next = node; b->prev = node;        // (3)(4) 이웃을 새 노드로
    return node;
}

void erase_d(DNode* node) {                // 노드 자체를 O(1)에 삭제 - 링크 2개
    node->prev->next = node->next;
    node->next->prev = node->prev;         // 두 방향을 반드시 함께
    delete node;
}

vector<int> dump_d() {                     // 센티넬 사이만 훑는다
    vector<int> out;
    for (DNode* cur = H.next; cur != &T; cur = cur->next)
        out.push_back(cur->val);
    return out;
}
```

```cpp
// 3) 원형 - 직접 구현 골격과 deque 실전 골격
void walk_circular(Node* start) {          // 종료 조건은 nullptr 이 아니라 '복귀'
    if (!start) return;
    Node* cur = start;
    do {                                   // while 이 아니라 do-while
        cout << cur->val << ' ';
        cur = cur->next;
    } while (cur != start);                // 이 줄이 없으면 무한 루프
    cout << '\n';
}

vector<int> rotate_pick(const vector<int>& vals, int k) {  // k번째마다 하나씩
    deque<int> dq(vals.begin(), vals.end());
    vector<int> order;
    while (!dq.empty()) {
        int r = (k - 1) % (int)dq.size();  // 문제마다 바뀜(간격 규칙)
        for (int t = 0; t < r; t++) {      // 왼쪽으로 r 칸 굴리기
            dq.push_back(dq.front());
            dq.pop_front();
        }
        order.push_back(dq.front());
        dq.pop_front();
    }
    return order;
}
```

```cpp
// 4) 동적 배열·반복자 실전 패턴
vector<int> buf;
buf.reserve(n);                            // 개수를 알면 재할당을 없앤다
buf.push_back(1); buf.pop_back();          // 뒤에서만 쓰면 분할상환 O(1)

deque<int> dq = {1, 2, 3};
dq.push_front(0); dq.pop_front();          // 양끝 O(1)

// 순회하며 지우기 - erase 의 반환값을 받는 것이 규칙
list<int> L = {1, 2, 3, 4, 5};
for (auto it = L.begin(); it != L.end(); ) {
    if (*it % 2 == 0) it = L.erase(it);    // 문제마다 바뀜(삭제 조건)
    else ++it;
}

// vector 에서 여러 개 지우기는 erase-remove 관용구로 한 번에 O(n)
vector<int> v = {1, 0, 2, 0, 3};
v.erase(remove(v.begin(), v.end(), 0), v.end());

// 자체 반복자 - 내부 구조를 숨긴 순회 제공
struct ListIter {
    Node* cur;
    explicit ListIter(Node* head) : cur(head) {}
    bool has_next() const { return cur != nullptr; }
    int next() { int v = cur->val; cur = cur->next; return v; }
};
```

**언제 무엇을 쓰나**

| 상황 | 고르는 것 | 이유 | 복잡도 |
|---|---|---|---|
| 인덱스로 자주 읽고 크기가 거의 안 변함 | `vector` / `array` | 주소 계산으로 바로 점프 | 접근 O(1) |
| 개수를 모른 채 뒤로만 계속 쌓음 | `vector::push_back` | 2배 확장으로 분할상환 O(1) | push_back 상환 O(1) |
| 넣을 개수를 미리 안다 | `reserve(n)` 후 `push_back` | 재할당·복사를 아예 없앤다 | 복사 0회 |
| 앞에서 넣고 빼기가 잦음 | `deque` / `queue` | 양끝이 모두 상수 시간 | 양끝 O(1) |
| 중간 삽입·삭제가 잦고 위치를 이미 쥐고 있음 | `list` 또는 직접 만든 사슬 | 링크 재배선만 하면 됨 | 삽입·삭제 O(1) |
| 노드 참조 하나로 그 자리를 즉시 삭제 | 이중 연결 리스트 | `prev`가 있어 직전 노드를 안 찾아도 됨 | 삭제 O(1) |
| 최근 사용 순서 유지 + 임의 키 접근 | `list` + `unordered_map` | 순서는 링크가, 탐색은 해시가 담당 | 갱신 평균 O(1) |
| 순회 중 조건에 맞는 원소를 지움 | `it = c.erase(it)` / erase-remove | 무효화된 반복자를 전진시키지 않기 위해 | O(n) |
| 돌면서 N번째마다 처리 | 원형 리스트 / `deque` 굴리기 | 끝이 없어 감기 처리가 필요 없음 | 굴린 칸 수에 비례 |
| 값을 인덱스로 자주 찾아야 함 | 사슬 대신 `vector`·`unordered_map` | 사슬은 임의 접근이 O(n) | O(n) vs O(1) |
| 원소가 크고 이동 비용이 큼 | 인덱스 배열을 대신 다룬다 | 실제 데이터를 옮기지 않는다 | 이동 O(n) → O(1) |
| 컨테이너를 함수에 넘김 | `const T&`(읽기) / `T&`(수정) | 값 전달은 호출마다 O(n) 복사 | O(n) → O(1) |

**✅ 마스터 체크리스트**

- [ ] 설명할 수 있다: 배열의 임의 접근이 왜 O(1)인가(주소 = base + i × `sizeof(T)`).
- [ ] 설명할 수 있다: 배열 중간 삽입이 왜 O(n)이고, 밀기를 왜 뒤에서부터 해야 하는가.
- [ ] 설명할 수 있다: `size()`와 `capacity()`의 차이, 그리고 둘이 같아지는 순간 무슨 일이 벌어지는가.
- [ ] 설명할 수 있다: `push_back`이 왜 분할상환 O(1)인가(복사 총량 1+2+4+… < 2n).
- [ ] 설명할 수 있다: 확장 배수를 2배가 아니라 +1로 하면 왜 O(n²)이 되는가.
- [ ] 설명할 수 있다: `reserve`와 `resize`의 차이와, 각각을 잘못 썼을 때 생기는 증상.
- [ ] 설명할 수 있다: 재할당이 포인터·참조·반복자를 왜 무효로 만드는가.
- [ ] 설명할 수 있다: 연결 리스트의 임의 접근이 왜 O(n)이고 삽입이 왜 O(1)인가.
- [ ] 설명할 수 있다: 삽입 시 `node->next`를 먼저 세팅해야 하는 이유와, 순서를 바꾸면 무엇이 사라지는가.
- [ ] 설명할 수 있다: 삭제에서 `delete`를 링크 재배선 뒤에 해야 하는 이유.
- [ ] 설명할 수 있다: 더미(센티넬) 헤드가 없애 주는 분기가 정확히 무엇인가.
- [ ] 설명할 수 있다: 단일 리스트에서 노드 하나를 지우려면 왜 직전 노드가 필요한가.
- [ ] 설명할 수 있다: 이중 리스트 삽입에서 바꿔야 할 링크 4개를 순서대로 댈 수 있다.
- [ ] 설명할 수 있다: LRU 캐시가 왜 해시맵 하나로도, 리스트 하나로도 안 되고 둘 다 필요한가.
- [ ] 설명할 수 있다: 원형 리스트의 순회 종료 조건이 왜 `nullptr`이 아닌가.
- [ ] 설명할 수 있다: `begin()`·`end()`·`++it`·`*it`가 range-for 안에서 각각 언제 불리는가.
- [ ] 설명할 수 있다: `end()`가 왜 "마지막 원소"가 아니라 "마지막 다음"인가.
- [ ] 설명할 수 있다: `vector`와 `list`의 반복자 무효화 규칙이 어떻게 다른가.

**⚠️ 자주 하는 실수**

**1) 링크를 바꾸는 순서를 뒤집어 노드를 통째로 잃는다**

```cpp
// ❌ 틀린 코드
void insert_after(Node* cur, int x) {
    Node* node = new Node(x);
    cur->next = node;          // 여기서 B 로 가는 마지막 포인터가 사라진다
    node->next = cur->next;    // cur->next 는 이미 node -> node->next = node
}
```

왜: `cur->next = node`를 먼저 하면 원래 뒤에 있던 노드를 가리키는 포인터가 하나도 남지 않는다. 두 번째 줄의 `cur->next`는 이미 `node`라 자기 자신을 가리키는 순환이 생기고, 뒤쪽 리스트가 통째로 유실된다(메모리 누수까지 덤이다).

```cpp
// ✅ 고친 코드
void insert_after(Node* cur, int x) {
    Node* node = new Node(x);
    node->next = cur->next;    // 새 노드가 먼저 뒤를 붙잡고
    cur->next = node;          // 그다음 앞을 갈아 끼운다
}
```

**2) 순회 중 삭제하면서 커서를 전진시킨다**

```cpp
// ❌ 틀린 코드
Node* cur = &dummy;
while (cur->next) {
    if (cur->next->val == x)
        cur->next = cur->next->next;
    cur = cur->next;           // 삭제한 뒤에도 전진 -> 연속된 x 를 건너뜀
}
```

왜: 삭제하면 `cur->next`가 이미 다음 후보로 바뀌어 있다. 여기서 또 전진하면 그 후보를 검사도 못 하고 지나친다. `{1, 2, 2, 3}`에서 2를 지우면 `{1, 2, 3}`이 남는다. `vector`에서 인덱스로 지울 때도 똑같은 함정이 생긴다.

```cpp
// ✅ 고친 코드
Node* cur = &dummy;
while (cur->next) {
    if (cur->next->val == x) {
        Node* dead = cur->next;
        cur->next = dead->next;    // 삭제했으면 제자리에서 다시 검사
        delete dead;
    } else {
        cur = cur->next;           // 안 지웠을 때만 전진
    }
}
```

**3) 이중 리스트에서 한 방향 링크만 고친다**

```cpp
// ❌ 틀린 코드
void erase_d(DNode* node) {
    node->prev->next = node->next;     // next 방향만 이었다
    delete node;
}
```

왜: 정방향 순회는 멀쩡해 보이지만 `node->next->prev`가 여전히 **해제된 노드**를 가리킨다. 역방향으로 훑는 순간 해제 후 사용(use-after-free)이 되어 값이 뒤죽박죽이거나 프로그램이 죽는다. 파이썬이라면 참조 카운트 덕에 객체가 살아 있어 "값이 되살아나는" 정도로 끝나지만, C++에서는 훨씬 위험하다.

```cpp
// ✅ 고친 코드
void erase_d(DNode* node) {
    node->prev->next = node->next;
    node->next->prev = node->prev;     // 두 방향을 반드시 함께
    delete node;                       // 이웃을 다 이은 다음에 해제
}
```

**4) `vector` 앞에서 빼는 연산을 반복한다**

```cpp
// ❌ 틀린 코드
vector<int> q = {1, 2, 3, 4, 5};
while (!q.empty()) {
    int x = q.front();
    q.erase(q.begin());        // 뺄 때마다 뒤 전체를 앞으로 당김 O(n)
    // ... x 처리 ...
}
```

왜: `erase(begin())`은 O(n)이라 n번 반복하면 O(n²)이 된다. n이 10만이면 100억 번 이동으로 시간 초과가 난다. `insert(begin(), x)`도 대칭적으로 같다.

```cpp
// ✅ 고친 코드
deque<int> q = {1, 2, 3, 4, 5};   // 또는 queue<int>
while (!q.empty()) {
    int x = q.front();
    q.pop_front();             // 양끝 O(1)
    // ... x 처리 ...
}
// 정말 vector 를 써야 한다면 인덱스 head 를 하나 두고 앞으로만 밀어도 O(1)
```

**5) 원형 리스트를 `nullptr` 기준으로 순회한다**

```cpp
// ❌ 틀린 코드
Node* cur = head;
while (cur) {                  // 원형에는 nullptr 이 없다 -> 영원히 돈다
    cout << cur->val << ' ';
    cur = cur->next;
}
```

왜: 원형 리스트에서 마지막 노드의 `next`는 `nullptr`이 아니라 다시 head다. 종료 조건이 절대 참이 되지 않아 무한 루프에 빠진다. 채점기에서는 시간 초과로만 보여 원인이 보이지 않는다.

```cpp
// ✅ 고친 코드
if (head) {
    Node* cur = head;
    do {                       // 첫 노드도 한 번은 방문해야 하므로 do-while
        cout << cur->val << ' ';
        cur = cur->next;
    } while (cur != head);     // 시작 노드로 돌아오면 한 바퀴 끝
}
```

**6) 맨 앞 노드를 지우는 경우를 빠뜨린다**

```cpp
// ❌ 틀린 코드
Node* cur = head;
while (cur->next) {            // head 가 nullptr 이면 여기서 즉사
    if (cur->next->val == x) cur->next = cur->next->next;
    else cur = cur->next;
}
// head 자체가 x 면 영영 지워지지 않는다
```

왜: 이 코드는 "직전 노드가 존재하는 노드"만 지울 수 있다. head에는 직전 노드가 없어 별도 분기가 필요하고, 그 분기를 잊으면 조용히 틀린 답이 나온다. 게다가 `head`가 `nullptr`이면 첫 줄에서 널 포인터를 역참조한다.

```cpp
// ✅ 고친 코드
Node dummy(0); dummy.next = head;      // head 앞에 가짜 노드를 하나 (스택에)
Node* cur = &dummy;
while (cur->next) {
    if (cur->next->val == x) {
        Node* dead = cur->next;
        cur->next = dead->next;
        delete dead;
    } else {
        cur = cur->next;
    }
}
head = dummy.next;                     // 새 head 를 다시 받아 온다
```

**7) 재할당으로 무효가 된 포인터·반복자를 계속 쓴다**

```cpp
// ❌ 틀린 코드
vector<int> v = {1, 2, 3};
int& first = v[0];             // 참조를 잡아 둔다
v.push_back(4);                // size == capacity 였다면 재할당이 일어난다
cout << first << '\n';         // 해제된 메모리를 읽는다 - 미정의 동작
// 반복자도 같다
for (auto it = v.begin(); it != v.end(); ++it)
    if (*it == 2) v.push_back(99);     // 루프 중 push_back -> it 과 end() 무효
```

왜: `vector`는 용량이 차면 **새 블록을 잡아 전부 복사하고 옛 블록을 해제**한다. 그 순간 옛 블록을 가리키던 포인터·참조·반복자는 전부 죽는다. 값이 우연히 맞게 나올 때도 있어 더 위험하다.

```cpp
// ✅ 고친 코드
vector<int> v = {1, 2, 3};
int idx = 0;                   // 참조 대신 인덱스를 들고 다닌다
v.push_back(4);
cout << v[idx] << '\n';        // 재할당과 무관하게 항상 올바르다
// 개수를 미리 알면 아예 재할당을 없앤다
v.reserve(1000);               // 이후 1000개까지는 반복자가 무효화되지 않는다
```

**8) `new` 한 노드를 `delete` 하지 않는다**

```cpp
// ❌ 틀린 코드
Node* head = nullptr;
for (int i = 0; i < 1000000; i++) {
    Node* node = new Node(i);
    node->next = head;
    head = node;
}
head = nullptr;                // 사슬 전체가 접근 불가능해졌지만 메모리는 그대로
```

왜: C++에는 자동 회수가 없다. `head`를 버려도 힙에 잡힌 100만 개 노드는 살아 있어 메모리 사용량이 계속 는다. 코딩 테스트 한 번 실행이면 프로세스 종료 시 운영체제가 회수해 주지만, **메모리 제한이 빡빡한 문제나 여러 번 리스트를 만들었다 버리는 코드에서는 그대로 초과**로 이어진다.

```cpp
// ✅ 고친 코드
void free_list(Node* head) {
    while (head) {
        Node* nxt = head->next;    // 다음을 먼저 저장하고
        delete head;               // 그다음 해제 (순서를 바꾸면 use-after-free)
        head = nxt;
    }
}
// 애초에 노드를 미리 배열로 잡아 두면 delete 자체가 필요 없다
// static Node pool[MAXN]; int cnt = 0;  ->  Node* node = &pool[cnt++];
```

**다음 챕터로**

- 다음 챕터의 정렬은 "배열 위에서 자리를 바꾸는 일"이다. 이 챕터에서 익힌 인덱스 밀기(삽입 정렬)와 `swap`(선택·거품 정렬)이 그대로 재료가 된다.
- 병합 정렬의 병합 단계는 L3에서 만든 "두 정렬 리스트 합치기"와 완전히 같은 투 포인터다. 연결 리스트로 짜면 추가 공간 없이도 합칠 수 있다.
- 힙 정렬에서 다시 만날 "완전 이진 트리를 배열 인덱스로 표현하기"는, 이 챕터의 "연속 메모리 + 인덱스 산술"이라는 발상의 연장이다. 포인터 없이 부모·자식을 계산한다는 점에서 `vector`의 사고방식이 그대로 이어진다.
- 반복자 감각도 계속 쓰인다. `sort(v.begin(), v.end())`, `lower_bound(v.begin(), v.end(), x)`처럼 STL은 컨테이너가 아니라 **`[first, last)` 구간**을 받는다. 이 챕터에서 익힌 "구간" 사고가 다음 두 챕터의 문법 전부를 떠받친다.
