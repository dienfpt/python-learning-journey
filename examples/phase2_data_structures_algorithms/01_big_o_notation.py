"""
Topic: Big-O Notation
So sánh JS: khái niệm giống hệt nhau ở mọi ngôn ngữ (đo tốc độ tăng theo
input size, không phải thời gian chạy thực tế). Điểm cần nhớ riêng cho
Python: list.append là O(1) nhưng list.insert(0, x)/list.pop(0) là O(n)
(giống Array.unshift/shift của JS đều chậm vì phải dịch chuyển phần tử);
dict/set lookup là O(1) trung bình nhờ hash table, giống Map/Set của JS.
"""

import time


def constant_time(lst: list[int]) -> int:
    """O(1) — truy cập theo index không phụ thuộc kích thước list."""
    return lst[0]


def linear_time(lst: list[int], target: int) -> bool:
    """O(n) — trong trường hợp xấu nhất phải duyệt hết list."""
    for item in lst:
        if item == target:
            return True
    return False


def quadratic_time(lst: list[int]) -> list[tuple[int, int]]:
    """O(n²) — vòng lặp lồng nhau, tìm mọi cặp phần tử."""
    pairs = []
    for i in lst:
        for j in lst:
            pairs.append((i, j))
    return pairs


def demo_list_vs_set_lookup(n: int) -> None:
    """So sánh thực tế: tìm phần tử trong list (O(n)) vs set (O(1))."""
    data_list = list(range(n))
    data_set = set(data_list)
    target = n - 1  # worst case: phần tử cuối cùng

    start = time.perf_counter()
    target in data_list
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    target in data_set
    set_time = time.perf_counter() - start

    print(f"Tìm 1 phần tử trong {n:,} items:")
    print(f"  list (O(n)):  {list_time * 1000:.4f} ms")
    print(f"  set  (O(1)):  {set_time * 1000:.4f} ms")


def main() -> None:
    numbers = [1, 2, 3, 4, 5]

    print("O(1) — constant_time:", constant_time(numbers))
    print("O(n) — linear_time(target=5):", linear_time(numbers, 5))
    print("O(n²) — quadratic_time pairs count:", len(quadratic_time(numbers)))

    print()
    demo_list_vs_set_lookup(100_000)


if __name__ == "__main__":
    main()
