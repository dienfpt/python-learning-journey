# Phase 2 — Data Structures & Algorithms

Không nằm trong nhánh JS→Python 1:1 (DSA thì ngôn ngữ nào cũng như nhau),
nhưng roadmap.sh/python liệt kê đây là bước tiếp theo sau Core Basics, và
nắm vững sẽ giúp code Python "đúng idiom" hơn (biết khi nào dùng `list` vs
`deque` vs `dict`, độ phức tạp của các thao tác built-in, v.v.)

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
