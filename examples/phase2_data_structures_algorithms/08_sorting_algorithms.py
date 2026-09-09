"""
Topic: Sorting Algorithms
So sánh JS: Array.prototype.sort() của JS (V8) dùng Timsort từ ES2019+,
GIỐNG HỆT sorted()/list.sort() của Python — cả hai đều O(n log n), stable
(giữ thứ tự tương đối của các phần tử bằng nhau). Khác biệt cần nhớ: JS
sort() mặc định so sánh theo STRING (10 đứng trước 9!) trừ khi truyền
comparator, còn Python sorted() mặc định so sánh đúng theo type của phần
tử — ít bẫy hơn.
"""

import random
import time


def bubble_sort(arr: list[int]) -> list[int]:
    """O(n^2) — so sánh từng cặp liền kề, đổi chỗ nếu sai thứ tự, lặp lại
    cho tới khi không còn đổi chỗ nào. Đơn giản nhưng chậm, chỉ nên dùng
    để học, không dùng thực tế."""
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # đã sorted, không cần lặp tiếp -> best case O(n)
            break
    return arr


def insertion_sort(arr: list[int]) -> list[int]:
    """O(n^2) trung bình, nhưng O(n) nếu list đã gần như sorted -- tốt cho
    dữ liệu nhỏ hoặc gần sorted (nhiều thư viện dùng insertion sort cho
    các đoạn nhỏ trong thuật toán hybrid, kể cả Timsort)."""
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr: list[int]) -> list[int]:
    """O(n log n) luôn luôn (best/avg/worst) — chia để trị (đệ quy, xem
    lại mục Recursion): chia đôi tới khi còn 1 phần tử, rồi merge lại
    theo thứ tự. Đánh đổi: cần O(n) bộ nhớ phụ để merge."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr: list[int]) -> list[int]:
    """O(n log n) trung bình, nhưng O(n^2) worst case (khi pivot luôn là
    phần tử nhỏ/lớn nhất, vd. list đã sorted + chọn pivot đầu tiên).
    Không cần bộ nhớ phụ nhiều như merge sort (in-place ở implementation
    thực tế; bản này dùng list mới cho dễ đọc)."""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)


def benchmark(n: int) -> None:
    data = [random.randint(0, 100_000) for _ in range(n)]

    algorithms = {
        "bubble_sort": bubble_sort,
        "insertion_sort": insertion_sort,
        "merge_sort": merge_sort,
        "quick_sort": quick_sort,
        "sorted() built-in (Timsort)": sorted,
    }

    print(f"Sort {n:,} phần tử ngẫu nhiên:")
    for name, fn in algorithms.items():
        start = time.perf_counter()
        fn(data)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  {name:<28}: {elapsed:>8.2f} ms")


def main() -> None:
    sample = [5, 2, 9, 1, 5, 6, 3]
    print("input:", sample)
    print("bubble_sort:   ", bubble_sort(sample))
    print("insertion_sort:", insertion_sort(sample))
    print("merge_sort:    ", merge_sort(sample))
    print("quick_sort:    ", quick_sort(sample))
    print("sorted() (Timsort, built-in):", sorted(sample))

    print()
    benchmark(2_000)


if __name__ == "__main__":
    main()
