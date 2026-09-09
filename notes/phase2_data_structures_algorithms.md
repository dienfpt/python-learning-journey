# Phase 2 — Data Structures & Algorithms

Không nằm trong nhánh JS→Python 1:1 (DSA thì ngôn ngữ nào cũng như nhau),
nhưng roadmap.sh/python liệt kê đây là bước tiếp theo sau Core Basics, và
nắm vững sẽ giúp code Python "đúng idiom" hơn (biết khi nào dùng `list` vs
`deque` vs `dict`, độ phức tạp của các thao tác built-in, v.v.)

## DSA là gì?

- **Data Structure (cấu trúc dữ liệu)**: cách tổ chức + lưu trữ dữ liệu
  trong bộ nhớ sao cho việc truy cập/thao tác hiệu quả cho một mục đích cụ
  thể. Không có cấu trúc nào "tốt nhất" tuyệt đối — mỗi loại đánh đổi
  (trade-off) giữa tốc độ đọc, tốc độ ghi, và bộ nhớ sử dụng khác nhau.
  Ví dụ: `list` đọc theo index nhanh (`O(1)`) nhưng chèn ở đầu chậm
  (`O(n)`); linked list thì ngược lại.
- **Algorithm (thuật toán)**: một chuỗi bước hữu hạn, rõ ràng để giải quyết
  một bài toán cụ thể (sắp xếp, tìm kiếm, duyệt đồ thị...). Cùng một bài
  toán có thể có nhiều thuật toán khác nhau, khác nhau về tốc độ và bộ nhớ
  tiêu tốn — đây là lý do cần Big-O để so sánh khách quan.
- Hai khái niệm luôn đi cùng nhau: **chọn đúng data structure** thường là
  bước quan trọng nhất để một algorithm chạy nhanh. Ví dụ: bài toán "kiểm
  tra phần tử có tồn tại không" — dùng `list` thì thuật toán tốt nhất vẫn
  là `O(n)` (phải duyệt), nhưng đổi sang `set`/`dict` thì thành `O(1)`
  ngay cả với thuật toán "ngây thơ" nhất (`in` operator).

## Tại sao cần học DSA?

- **Viết code hiệu quả hơn**: code chạy đúng với 100 dòng test data nhưng
  có thể sập (timeout, OOM) với 1 triệu dòng ở production nếu chọn sai cấu
  trúc dữ liệu/thuật toán. Hiểu độ phức tạp giúp nhận ra vấn đề ngay khi
  viết code, không cần đợi production báo lỗi.
- **Đọc hiểu source code thư viện tốt hơn**: biết `dict` là hash table,
  `deque` là doubly linked list, `sorted()` dùng Timsort... giúp đoán được
  performance characteristic của code mà không cần đọc source.
- **Interview**: hầu hết coding interview (kể cả cho vị trí không phải
  "thuật toán chuyên sâu") đều kiểm tra DSA cơ bản — đây gần như là ngôn
  ngữ chung của ngành.
- **Nền tảng cho system design**: cache (hash table), rate limiter (queue/
  sliding window), database index (B-tree — biến thể của tree), load
  balancing (heap)... đều xây trên các cấu trúc dữ liệu nền tảng ở đây.
- Với người đã có 10 năm kinh nghiệm JS: đây là kiến thức **ngôn ngữ nào
  cũng dùng chung** (khác các phase JS→Python khác), nên đầu tư ở đây có
  lợi ích lâu dài, không chỉ riêng cho Python.

## Nội dung từng mục sẽ bao gồm

Mỗi mục dưới đây trả lời 4 câu hỏi: **là gì** (định nghĩa) — **hoạt động
thế nào** (cơ chế bên trong) — **độ phức tạp** (Big-O của các thao tác
chính) — **khi nào dùng** (use case thực tế, so với lựa chọn khác).

## Tiến độ

- [x] 1. Big-O Notation — đo độ phức tạp thời gian/không gian
- [x] 2. Arrays / Python `list` — dynamic array, độ phức tạp từng thao tác
- [x] 3. Linked Lists — singly/doubly, so với `list`
- [x] 4. Stacks — LIFO, dùng `list` làm stack
- [x] 5. Queues — FIFO, `collections.deque`
- [x] 6. Hash Tables — cách `dict` hoạt động bên trong (hashing, collision)
- [ ] 7. Recursion — call stack, base case, so với loop
- [ ] 8. Sorting Algorithms — bubble/insertion/merge/quick, so với `sorted()`
- [ ] 9. Searching Algorithms — linear vs binary search
- [ ] 10. Trees — Binary Tree, Binary Search Tree
- [ ] 11. Graphs — adjacency list, BFS, DFS

## 1. Big-O Notation

- Đo độ phức tạp theo **tốc độ tăng** khi input lớn dần, không phải thời
  gian chạy thực tế (khác benchmark/profiling ở Phase 5).
- Các mốc thường gặp, từ tốt → xấu:
  `O(1)` < `O(log n)` < `O(n)` < `O(n log n)` < `O(n²)` < `O(2ⁿ)`.
- Chỉ giữ số hạng lớn nhất, bỏ hằng số: `O(2n + 100)` → `O(n)`.
- Ví dụ độ phức tạp của các thao tác `list` Python (giống `Array` JS vì
  cùng là dynamic array, dùng chung mental model):
  - `lst[i]` (index), `lst.append(x)` → `O(1)`
  - `x in lst`, `lst.insert(0, x)`, `lst.pop(0)` → `O(n)`
  - `sorted(lst)` → `O(n log n)`
- `dict`/`set` lookup (`key in d`) là `O(1)` trung bình nhờ hash table —
  khác hẳn `O(n)` của tìm trong `list`, đây là lý do nên dùng `set`/`dict`
  để check tồn tại thay vì `list`.

## 2. Arrays / Python `list`

- Python `list` là **dynamic array**, giống JS `Array` — cấp phát dư
  (over-allocate) bộ nhớ khi grow, không resize mỗi lần thêm phần tử.
  Nhờ vậy `append()` là `O(1)` amortized thay vì `O(n)` mỗi lần.
- `insert(0, x)` và `pop(0)` là `O(n)` vì phải dịch chuyển toàn bộ phần tử
  còn lại — giống `unshift()`/`shift()` chậm của JS. Cần thao tác nhiều ở
  **đầu** list → dùng `collections.deque` (`O(1)` cả hai đầu) thay vì `list`.
- Slicing (`lst[1:4]`) tạo **list mới** (shallow copy), không phải view —
  khác `numpy` array hay JS `TypedArray.subarray()`.
- Shallow copy chỉ copy 1 lớp: list lồng nhau (`list[list]`) vẫn share
  reference tới phần tử con → sửa qua bản copy vẫn ảnh hưởng bản gốc. Cần
  `copy.deepcopy()` nếu muốn tách hoàn toàn.
- Gotcha kinh điển: `[[0] * 3] * 3` tạo 3 dòng **cùng tham chiếu** tới 1
  list con (nhân list = nhân reference, không nhân giá trị) — dùng list
  comprehension `[[0] * 3 for _ in range(3)]` để tạo ma trận đúng.

## 3. Linked Lists

- **Là gì**: chuỗi các `Node`, mỗi node giữ `value` + con trỏ `next` tới
  node kế tiếp. Không có built-in trong cả Python lẫn JS — phải tự tạo
  class, hoặc dùng `collections.deque` (doubly linked list có sẵn).
- **Hoạt động thế nào**: khác `list`/`Array` lưu liền kề (contiguous) trong
  bộ nhớ, các Node của linked list nằm **rải rác**, liên kết với nhau qua
  reference. Vì vậy không thể "nhảy" tới phần tử thứ *i* — phải đi từng
  bước từ `head`.
- **Độ phức tạp**:
  - Truy cập theo index / tìm kiếm theo giá trị: `O(n)` (không có random
    access, khác hẳn `list[i]` là `O(1)`).
  - Thêm/xoá ở **đầu** (`head`), hoặc ở vị trí **đã có sẵn con trỏ tới
    node đó**: `O(1)` — chỉ cần đổi vài con trỏ, không dịch chuyển phần
    tử như array.
  - Thêm vào **cuối**: `O(n)` nếu không giữ `tail` pointer riêng (phải
    duyệt hết để tìm node cuối).
- **Doubly linked list**: mỗi node có thêm con trỏ `prev`, cho phép duyệt
  2 chiều và xoá `O(1)` nếu đã có reference tới node (không cần duyệt từ
  đầu để tìm node trước nó). `collections.deque` của Python được cài đặt
  bằng doubly linked list → `appendleft()`/`popleft()` là `O(1)`, khác
  `list.insert(0, x)`/`list.pop(0)` là `O(n)`.
- **Khi nào dùng**: cần thêm/xoá liên tục ở đầu hoặc giữa danh sách (queue,
  undo history, LRU cache) mà không muốn trả giá dịch chuyển phần tử của
  array. Nếu chỉ cần thao tác ở **cuối** hoặc random access theo index —
  `list` vẫn tốt hơn (cache-friendly hơn vì bộ nhớ liền kề).

## 4. Stacks

- **Là gì**: cấu trúc **LIFO** (Last In, First Out) — phần tử thêm vào sau
  cùng sẽ được lấy ra đầu tiên. Chỉ có 2 thao tác chính: `push` (thêm vào
  đỉnh) và `pop` (lấy ra khỏi đỉnh).
- **Hoạt động thế nào**: Python không có class `Stack` riêng — dùng thẳng
  `list`, coi **cuối list là đỉnh stack**: `push` = `list.append(x)`,
  `pop` = `list.pop()` (không tham số = lấy phần tử cuối). Giống hệt
  `Array.push()`/`Array.pop()` của JS.
- **Độ phức tạp**: `push`/`pop`/`peek` (xem đỉnh, `stack[-1]`) đều `O(1)`
  vì thao tác ở cuối list — đây là lý do **không** dùng `insert(0, x)`/
  `pop(0)` để giả lập stack (sai vị trí LIFO và tốn `O(n)`).
- **Khi nào dùng**:
  - Kiểm tra ngoặc/tag cân bằng (compiler, linter, HTML parser).
  - Undo/Redo (mỗi hành động push vào stack, undo = pop).
  - **Call stack**: cơ chế Python/JS quản lý function call chính là 1
    stack ẩn — mỗi lần gọi hàm push 1 "stack frame", return thì pop. Đây
    là lý do đệ quy sâu quá sẽ bị `RecursionError`/`Stack Overflow` (xem
    thêm ở mục Recursion).
  - DFS (Depth-First Search) trên cây/đồ thị — dùng stack (hoặc đệ quy,
    về bản chất là stack ẩn) để luôn đi sâu nhất có thể trước khi quay lui.

## 5. Queues

- **Là gì**: cấu trúc **FIFO** (First In, First Out) — phần tử thêm vào
  đầu tiên sẽ được lấy ra đầu tiên, giống hàng người xếp hàng. Thao tác
  chính: `enqueue` (thêm vào cuối) và `dequeue` (lấy ra khỏi đầu).
- **Hoạt động thế nào**: **không dùng `list` làm queue** trong Python nếu
  cần hiệu năng — `list.pop(0)` là `O(n)` vì phải dịch chuyển toàn bộ phần
  tử còn lại lên trước 1 vị trí. Dùng `collections.deque` thay thế:
  `enqueue` = `deque.append(x)`, `dequeue` = `deque.popleft()`.
- **Độ phức tạp**: `deque` được cài đặt bằng doubly linked list nội bộ nên
  `append()`/`appendleft()`/`pop()`/`popleft()` đều `O(1)` — đối xứng ở cả
  2 đầu, khác hẳn `list` chỉ nhanh ở 1 đầu (cuối).
- **Khi nào dùng**:
  - **BFS** (Breadth-First Search) trên cây/đồ thị — dùng queue để duyệt
    theo từng "lớp" (level), đảm bảo tìm được đường đi ngắn nhất theo số
    cạnh trên đồ thị không trọng số (khác DFS dùng stack, đi sâu trước).
  - Task/job queue, message queue, print queue — xử lý theo đúng thứ tự
    đến trước - phục vụ trước.
  - `queue.Queue` (khác `collections.deque`) dùng khi cần thread-safe cho
    concurrent programming (xem thêm ở Phase 3 — Concurrency).

## 6. Hash Tables

- **Là gì**: cấu trúc lưu cặp `key -> value`, cho phép lookup/insert/delete
  gần như tức thời bất kể dữ liệu lớn cỡ nào. Python `dict` (và `set`,
  vốn là dict không có value) chính là hash table — không phải cấu trúc
  "nên học riêng", mà là **hiểu cơ chế của thứ đã dùng hàng ngày**.
- **Hoạt động thế nào**: dùng hàm băm (`hash(key)`) để biến key thành 1 số
  nguyên, rồi lấy số đó modulo với kích thước bảng để ra "bucket" (vị trí)
  lưu trữ — tra cứu không cần so sánh tuần tự như `list`. **Collision**
  (2 key khác nhau băm ra cùng bucket) là không tránh khỏi; cách xử lý phổ
  biến: *separate chaining* (mỗi bucket giữ 1 list các cặp key-value —
  cách file `06_hash_tables.py` tự implement để dễ hình dung) hoặc *open
  addressing* (CPython dùng cách này thật cho `dict`: khi collision, dò
  tìm bucket trống kế tiếp theo 1 công thức xác định).
- **Điều kiện bắt buộc**: key phải **hashable** (immutable) — `str`, `int`,
  `tuple` (chỉ khi mọi phần tử bên trong cũng hashable) dùng được, `list`/
  `dict`/`set` thì **không** — vì nếu key có thể bị mutate sau khi đã lưu,
  hash của nó thay đổi và phá vỡ vị trí bucket đã tính trước đó.
- **Độ phức tạp**: `O(1)` trung bình cho get/set/delete/`in` — đây là lý
  do nên dùng `dict`/`set` thay vì `list` mỗi khi cần tra cứu tồn tại
  nhiều lần. Trường hợp xấu nhất (mọi key đều collide) là `O(n)`, nhưng
  hàm băm tốt của Python khiến trường hợp này gần như không xảy ra trong
  thực tế.
- **Khi nào dùng**: đếm tần suất (`collections.Counter`), cache/memoization
  (map input -> kết quả đã tính), loại bỏ trùng lặp (`set`), index dữ liệu
  theo 1 trường để tra cứu nhanh (map `user_id -> user object` thay vì
  duyệt `list[User]` mỗi lần cần tìm).
