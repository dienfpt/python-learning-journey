"""
Topic: Searching Algorithms
So sánh JS: Array.prototype.indexOf()/includes() của JS đều là linear
search O(n), giống Python `in`/`.index()` trên list — không có binary
search built-in ở cả 2 ngôn ngữ cho array thường. Python có sẵn module
`bisect` để làm binary search trên list đã sorted, JS phải tự viết hoặc
dùng thư viện ngoài.
"""

import bisect
import random
import time


def linear_search(arr: list[int], target: int) -> int:
    """O(n) — duyệt tuần tự, không yêu cầu dữ liệu đã sorted. Đây là cách
    `in`/`list.index()` hoạt động bên trong."""
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1


def binary_search(arr: list[int], target: int) -> int:
    """O(log n) — YÊU CẦU list đã sorted. Mỗi bước loại bỏ một nửa không
    gian tìm kiếm bằng cách so sánh với phần tử giữa."""
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1   # target ở nửa phải
        else:
            high = mid - 1  # target ở nửa trái

    return -1


def binary_search_recursive(arr: list[int], target: int, low: int = 0, high: int | None = None) -> int:
    """Cùng logic binary search nhưng viết bằng đệ quy (xem lại mục
    Recursion) — chia để trị: mỗi lần gọi thu hẹp không gian tìm kiếm."""
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1

    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)


def demo_bisect_module() -> None:
    """bisect: binary search built-in của Python cho list đã sorted.
    bisect_left trả về vị trí để CHÈN target mà vẫn giữ sorted (không
    phải index của phần tử tìm thấy như binary_search ở trên)."""
    sorted_data = [1, 3, 5, 7, 9, 11, 13]

    pos = bisect.bisect_left(sorted_data, 7)
    print(f"bisect_left(data, 7) = {pos} (vị trí của 7 trong list)")

    insert_pos = bisect.bisect_left(sorted_data, 8)
    print(f"bisect_left(data, 8) = {insert_pos} (8 không có, nhưng đây là vị trí nên chèn)")

    bisect.insort(sorted_data, 8)  # chèn giữ nguyên thứ tự sorted, O(n) do shift
    print("sau insort(8):", sorted_data)


def benchmark(n: int) -> None:
    data = sorted(random.sample(range(n * 10), n))
    target = data[-1]  # worst case cho linear search: phần tử cuối cùng

    start = time.perf_counter()
    linear_search(data, target)
    linear_time = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    binary_search(data, target)
    binary_time = (time.perf_counter() - start) * 1000

    print(f"Tìm 1 phần tử (worst case) trong {n:,} phần tử đã sorted:")
    print(f"  linear_search O(n):     {linear_time:.4f} ms")
    print(f"  binary_search O(log n): {binary_time:.4f} ms")


def main() -> None:
    data = [1, 3, 5, 7, 9, 11, 13, 15]

    print("linear_search(data, 11):", linear_search(data, 11))
    print("binary_search(data, 11):", binary_search(data, 11))
    print("binary_search_recursive(data, 11):", binary_search_recursive(data, 11))
    print("binary_search(data, 99) (không tồn tại):", binary_search(data, 99))

    print()
    demo_bisect_module()

    print()
    benchmark(100_000)


if __name__ == "__main__":
    main()
