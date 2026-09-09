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
- [ ] 3. Linked Lists — singly/doubly, so với `list`
- [ ] 4. Stacks — LIFO, dùng `list` làm stack
- [ ] 5. Queues — FIFO, `collections.deque`
- [ ] 6. Hash Tables — cách `dict` hoạt động bên trong (hashing, collision)
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
