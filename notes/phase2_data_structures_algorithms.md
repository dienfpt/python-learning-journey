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
- [x] 7. Recursion — call stack, base case, so với loop
- [x] 8. Sorting Algorithms — bubble/insertion/merge/quick, so với `sorted()`
- [x] 9. Searching Algorithms — linear vs binary search
- [x] 10. Trees — Binary Tree, Binary Search Tree
- [x] 11. Graphs — adjacency list, BFS, DFS

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

## 7. Recursion

- **Là gì**: một hàm tự gọi lại chính nó để giải bài toán nhỏ hơn, cho
  đến khi chạm **base case** (điều kiện dừng) thì trả kết quả ngược lên.
  Thiếu base case (hoặc base case không bao giờ đạt tới) sẽ gây đệ quy
  vô hạn.
- **Hoạt động thế nào**: mỗi lần gọi hàm tạo 1 "stack frame" mới (giữ biến
  cục bộ + vị trí cần quay lại) và push vào call stack (xem lại mục
  Stacks); khi hàm return, frame đó pop ra. Vì vậy đệ quy về bản chất là
  dùng stack ẩn — bất kỳ đệ quy nào cũng có thể viết lại bằng loop + stack
  tường minh.
- **Độ phức tạp — dễ nhầm nhất là đệ quy không có memoization**: ví dụ
  `fibonacci_naive(n)` là `O(2^n)` vì tính lại cùng 1 giá trị con rất
  nhiều lần (fibonacci(3) bị gọi lại nhiều lần khi tính fibonacci(5)).
  Thêm memoization (cache kết quả đã tính, dùng `@functools.lru_cache` có
  sẵn của Python) hạ xuống `O(n)`.
- **Giới hạn quan trọng của Python**: `sys.getrecursionlimit()` mặc định
  chỉ 1000 — thấp hơn nhiều so với JS engine (thường cho phép sâu hơn
  trước khi stack overflow). Port thuật toán đệ quy từ JS sang Python cho
  input lớn (duyệt cây sâu, chia để trị trên n lớn) dễ gặp
  `RecursionError` dù cùng logic chạy tốt bên JS — cần chuyển sang loop
  hoặc tăng limit bằng `sys.setrecursionlimit()` (cẩn thận, không giải
  quyết tận gốc vấn đề bộ nhớ).
- Không có TCO (Tail Call Optimization) ở cả Python lẫn JS (khác một số
  ngôn ngữ như Scheme/Elixir) — viết đệ quy dạng "tail call" không giúp
  tiết kiệm stack như các ngôn ngữ đó.
- **Khi nào dùng**: bài toán có cấu trúc chia để trị (merge sort, quick
  sort — xem mục Sorting) hoặc dữ liệu lồng nhau độ sâu không biết trước
  (duyệt cây, đồ thị, JSON/nested list, cây thư mục) — đệ quy diễn tả tự
  nhiên và ngắn gọn hơn loop trong các trường hợp này.

## 8. Sorting Algorithms

- **Là gì**: nhóm thuật toán sắp xếp lại thứ tự phần tử trong 1 collection
  theo 1 tiêu chí (tăng dần, giảm dần...). Trong thực tế **hầu như không
  bao giờ tự viết** — dùng `sorted()`/`list.sort()` built-in — nhưng hiểu
  cơ chế các thuật toán kinh điển giúp nắm vững đánh đổi giữa tốc độ, bộ
  nhớ, và tính ổn định (stable sort).
- **Bubble Sort** — `O(n^2)`: so sánh từng cặp phần tử liền kề, đổi chỗ
  nếu sai thứ tự, lặp lại nhiều vòng. Đơn giản nhất nhưng chậm nhất, chỉ
  có giá trị học thuật.
- **Insertion Sort** — `O(n^2)` trung bình, nhưng `O(n)` nếu dữ liệu **gần
  như đã sorted**: chèn từng phần tử vào đúng vị trí trong phần đã sorted
  phía trước. Nhiều thuật toán hybrid thực tế (kể cả Timsort) dùng
  insertion sort cho các đoạn dữ liệu nhỏ vì overhead thấp.
- **Merge Sort** — `O(n log n)` **luôn luôn** (best/avg/worst case, không
  có trường hợp xấu): chia để trị bằng đệ quy (xem lại mục Recursion) —
  chia đôi liên tục tới khi còn 1 phần tử, rồi merge lại theo đúng thứ
  tự. Đánh đổi: cần `O(n)` bộ nhớ phụ. **Stable** (giữ thứ tự tương đối
  của phần tử bằng nhau).
- **Quick Sort** — `O(n log n)` trung bình nhưng `O(n^2)` **worst case**
  (khi pivot luôn rơi vào phần tử nhỏ/lớn nhất, vd. chọn pivot đầu tiên
  trên list đã sorted sẵn). Đổi lại thường nhanh hơn merge sort trong
  thực tế vì ít cần bộ nhớ phụ (in-place). Không stable theo cách cài đặt
  thông thường.
- **`sorted()`/`list.sort()` của Python dùng Timsort**: lai giữa merge
  sort và insertion sort, `O(n log n)` worst case, **stable**, tối ưu đặc
  biệt tốt cho dữ liệu đã sorted 1 phần (best case gần `O(n)`). JS
  `Array.prototype.sort()` (V8, từ ES2019) cũng dùng Timsort — cùng độ
  phức tạp, nhưng JS mặc định so sánh theo **string** (`10` đứng trước
  `9` nếu không truyền comparator) — Python `sorted()` so sánh đúng theo
  type của phần tử, an toàn hơn.
- **Khi nào dùng thuật toán nào**: thực tế luôn dùng `sorted()` trừ khi có
  lý do đặc biệt (bộ nhớ cực hạn chế → cân nhắc in-place quick sort; cần
  đảm bảo `O(n log n)` worst case tuyệt đối → merge sort thay vì quick
  sort).

## 9. Searching Algorithms

- **Là gì**: tìm vị trí (hoặc xác nhận sự tồn tại) của 1 phần tử trong
  collection. Đây chính là bài toán mà mục Hash Tables đã giải rất nhanh
  (`O(1)`) cho `dict`/`set` — mục này bàn về tìm kiếm trên **list**, nơi
  không có sẵn cơ chế hash.
- **Linear Search** — `O(n)`: duyệt tuần tự từng phần tử, không yêu cầu
  dữ liệu đã sorted. Đây là cách `in`/`list.index()` của Python và
  `indexOf()`/`includes()` của JS hoạt động bên trong.
- **Binary Search** — `O(log n)`: **yêu cầu bắt buộc dữ liệu đã sorted**.
  Mỗi bước so sánh với phần tử ở giữa rồi loại bỏ hẳn 1 nửa không gian tìm
  kiếm — vì vậy nhanh hơn linear search rất nhiều với dữ liệu lớn (100,000
  phần tử: ~17 bước so với tối đa 100,000 bước).
- **Đánh đổi cần nhớ**: binary search nhanh hơn nhưng **cần dữ liệu đã
  sorted trước** — nếu dữ liệu thay đổi liên tục (insert/delete nhiều),
  chi phí giữ list luôn sorted (`O(n)` mỗi lần insert đúng vị trí) có thể
  làm mất lợi thế so với việc chỉ linear search khi cần.
- **Module `bisect`**: Python có sẵn binary search cho list đã sorted —
  `bisect_left`/`bisect_right` tìm vị trí chèn giữ nguyên thứ tự sorted,
  `insort` chèn trực tiếp vào đúng vị trí. JS không có tương đương built-in,
  phải tự viết hoặc dùng thư viện ngoài.
- **Khi nào dùng**: dữ liệu **tĩnh hoặc ít thay đổi, cần tra cứu nhiều
  lần** → sort 1 lần rồi binary search (hoặc dùng `bisect`). Dữ liệu thay
  đổi liên tục và không cần tra cứu quá thường xuyên → `dict`/`set` (nếu
  chỉ cần biết tồn tại) vẫn là lựa chọn tốt nhất, `O(1)` mà không cần giữ
  thứ tự sorted.

## 10. Trees

- **Là gì**: cấu trúc phân cấp gồm các `node`, mỗi node có 1 node cha
  (trừ `root`) và 0+ node con. **Binary Tree**: mỗi node tối đa 2 con
  (`left`/`right`), không có ràng buộc thứ tự. **Binary Search Tree
  (BST)**: binary tree có thêm quy ước tại **mọi** node: mọi giá trị bên
  nhánh trái nhỏ hơn node, mọi giá trị bên nhánh phải lớn hơn — quy ước
  này chính là thứ giúp search/insert nhanh hơn duyệt tuyến tính.
- **Hoạt động thế nào**: giống Linked List, cài đặt bằng class (`TreeNode`
  với `left`/`right` thay vì `next`), không có built-in ở Python/JS.
  Search/insert trên BST tận dụng quy ước thứ tự: so sánh với node hiện
  tại rồi rẽ trái/phải, loại bỏ hẳn 1 nhánh mỗi bước — cùng nguyên lý với
  binary search trên list đã sorted (mục 9).
- **4 cách duyệt cây (traversal)**:
  - **Inorder** (trái → node → phải): trên BST luôn cho ra dãy **đã
    sorted** — tính chất đặc trưng, dùng để lấy dữ liệu ra theo thứ tự.
  - **Preorder** (node → trái → phải): root luôn đứng đầu — dùng để copy/
    serialize cây (dễ tái tạo lại đúng cấu trúc từ danh sách preorder).
  - **Postorder** (trái → phải → node): con luôn xử lý trước cha — dùng
    khi cần giải phóng/xoá node con trước khi xoá node cha.
  - **Level-order** (BFS theo từng tầng, xem lại mục Queues): dùng `queue`
    thay vì đệ quy, hữu ích khi cần xử lý cây theo "độ sâu" (vd. tìm node
    gần root nhất thoả điều kiện).
- **Độ phức tạp**: search/insert/delete là `O(height)` — nếu cây **cân
  bằng** (balanced), `height ≈ log n` nên các thao tác là `O(log n)`.
  **Nhưng nếu insert dữ liệu đã sorted sẵn**, BST cơ bản (không tự cân
  bằng) sẽ bị lệch hẳn 1 bên, trở thành **linked list trá hình** với
  `height = n` → mọi thao tác tụt xuống `O(n)`. Đây là lý do thư viện
  thực tế dùng **self-balancing tree** (AVL, Red-Black Tree — tự động
  xoay cây để giữ cân bằng sau mỗi insert/delete); B-Tree (biến thể nhiều
  nhánh) là nền tảng của hầu hết database index.
- **Giới hạn của Python cần nhớ**: duyệt cây bằng đệ quy có thể gặp
  `RecursionError` nếu cây quá sâu (`sys.getrecursionlimit()` mặc định
  1000 — xem lại mục Recursion) — cây bị lệch hẳn 1 bên với hàng nghìn
  node là ví dụ thực tế dễ gặp lỗi này; cần chuyển sang duyệt bằng loop +
  stack/queue tường minh nếu dữ liệu có thể tạo cây rất sâu.
- **Khi nào dùng**: dữ liệu có quan hệ phân cấp tự nhiên (cây thư mục,
  DOM, tổ chức công ty), cần tra cứu/insert nhanh mà vẫn giữ thứ tự
  (BST/self-balancing tree thay vì sort lại `list` mỗi lần), hoặc làm nền
  cho cấu trúc phức tạp hơn (heap, trie, database index).

## 11. Graphs

- **Là gì**: cấu trúc tổng quát gồm các **node** (đỉnh) nối với nhau bằng
  **edge** (cạnh) — không ràng buộc phân cấp cha/con như Tree. Thực chất
  **Tree là 1 dạng đặc biệt của Graph**: không có chu trình (cycle), và
  giữa 2 node bất kỳ chỉ có đúng 1 đường đi. Có thể **vô hướng**
  (undirected — cạnh đi được 2 chiều, vd. bạn bè Facebook) hoặc **có
  hướng** (directed — cạnh chỉ đi được 1 chiều, vd. follow trên Twitter/X)
  và **có trọng số** (weighted, vd. khoảng cách giữa 2 thành phố) hoặc
  không.
- **Hoạt động thế nào — 2 cách biểu diễn phổ biến**:
  - **Adjacency List** (dùng trong `11_graphs.py`): `dict[node, list[neighbor]]`.
    Tốn `O(V + E)` bộ nhớ (V = số đỉnh, E = số cạnh) — hiệu quả cho đồ
    thị **thưa** (sparse, ít cạnh so với số đỉnh), là lựa chọn mặc định
    trong thực tế.
  - **Adjacency Matrix**: ma trận `V x V`, ô `[i][j] = 1` nếu có cạnh nối
    i-j. Tốn `O(V^2)` bộ nhớ bất kể số cạnh thực tế, nhưng tra cứu "có
    cạnh giữa i và j không" là `O(1)` (so với `O(V)` của adjacency list).
    Chỉ nên dùng khi đồ thị **dày đặc** (dense, gần như mọi cặp đỉnh đều
    có cạnh).
- **BFS (Breadth-First Search)** — dùng **queue** (xem lại mục Queues):
  duyệt theo từng "lớp" khoảng cách tăng dần từ điểm bắt đầu. Đảm bảo tìm
  ra đường đi **ngắn nhất theo số cạnh** trên đồ thị không trọng số — đây
  là ứng dụng quan trọng nhất của BFS (tìm bạn chung gần nhất, số bước di
  chuyển tối thiểu...).
- **DFS (Depth-First Search)** — dùng **stack** (xem lại mục Stacks, có
  thể viết tường minh hoặc bằng đệ quy vì call stack chính là stack ẩn):
  đi sâu nhất có thể theo 1 nhánh trước khi quay lui thử nhánh khác. Dùng
  khi cần duyệt **toàn bộ** đồ thị (không quan tâm đường ngắn nhất), phát
  hiện chu trình, topological sort, tìm connected components.
- **Độ phức tạp**: cả BFS và DFS đều `O(V + E)` — mỗi đỉnh và mỗi cạnh chỉ
  được xử lý đúng 1 lần nhờ tập `visited` đánh dấu đã ghé qua (thiếu bước
  này sẽ lặp vô hạn nếu đồ thị có chu trình).
- **Khi nào dùng**: mạng xã hội (bạn bè, follow), bản đồ/định tuyến
  (đường đi ngắn nhất — thực tế dùng Dijkstra/A* cho đồ thị có trọng số,
  nâng cao hơn BFS), dependency graph (thứ tự build/install package),
  web crawler (BFS/DFS theo link), phát hiện deadlock (chu trình trong
  directed graph).
