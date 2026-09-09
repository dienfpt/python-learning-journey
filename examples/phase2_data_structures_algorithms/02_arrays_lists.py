"""
Topic: Arrays / Python `list`
So sánh JS: Python list và JS Array đều là "dynamic array" — cấp phát dư
(over-allocate) bộ nhớ nên append() là O(1) amortized (giống push()).
Khác biệt cần nhớ: insert(0, x)/pop(0) là O(n) vì phải dịch chuyển toàn bộ
phần tử (giống unshift()/shift() chậm của JS) — dùng collections.deque nếu
cần thao tác nhiều ở đầu list. Gotcha kinh điển: [[0] * 3] * 3 tạo 3 dòng
CÙNG THAM CHIẾU tới 1 list con — sửa 1 dòng thì cả 3 dòng đổi theo, khác kỳ
vọng của dev quen Array.from trong JS.
"""

import sys
import time


def demo_over_allocation() -> None:
    """List Python cấp phát dư capacity, không resize mỗi lần append —
    đây là lý do append() là O(1) amortized thay vì O(n)."""
    lst: list[int] = []
    prev_size = sys.getsizeof(lst)
    print("size tăng khi append (bytes) — không tăng đều mỗi lần:")
    for i in range(10):
        lst.append(i)
        size = sys.getsizeof(lst)
        if size != prev_size:
            print(f"  len={len(lst):>2} -> size={size} bytes (nhảy capacity)")
            prev_size = size


def demo_append_vs_insert_front(n: int) -> None:
    """append (cuối) O(1) amortized vs insert(0, x) (đầu) O(n)."""
    start = time.perf_counter()
    lst = []
    for i in range(n):
        lst.append(i)
    append_time = time.perf_counter() - start

    start = time.perf_counter()
    lst2 = []
    for i in range(n):
        lst2.insert(0, i)
    insert_front_time = time.perf_counter() - start

    print(f"Thêm {n:,} phần tử:")
    print(f"  append (cuối, O(1)):        {append_time * 1000:.2f} ms")
    print(f"  insert(0, x) (đầu, O(n)):   {insert_front_time * 1000:.2f} ms")


def demo_slicing_copies() -> None:
    """Slicing tạo list MỚI (shallow copy), không phải view như numpy."""
    original = [1, 2, 3, 4, 5]
    sliced = original[1:4]
    sliced.append(999)

    print("original:", original, "(không đổi)")
    print("sliced:", sliced, "(list mới, độc lập)")

    # Shallow copy: các phần tử lồng nhau (list con) vẫn share reference
    nested = [[1, 2], [3, 4]]
    shallow = nested[:]
    shallow[0].append("mutated")
    print("nested sau khi sửa qua shallow copy:", nested, "<- bị ảnh hưởng!")


def demo_matrix_reference_gotcha() -> None:
    """Gotcha kinh điển: [[0]*3]*3 tạo 3 tham chiếu tới CÙNG 1 list con."""
    wrong = [[0] * 3] * 3
    wrong[0][0] = 1
    print("wrong (nhân list, share reference):", wrong, "<- cả 3 dòng đổi!")

    correct = [[0] * 3 for _ in range(3)]
    correct[0][0] = 1
    print("correct (list comprehension, độc lập):", correct)


def main() -> None:
    demo_over_allocation()
    print()
    demo_append_vs_insert_front(20_000)
    print()
    demo_slicing_copies()
    print()
    demo_matrix_reference_gotcha()


if __name__ == "__main__":
    main()
