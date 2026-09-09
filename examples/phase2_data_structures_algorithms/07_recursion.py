"""
Topic: Recursion
So sánh JS: cả Python và JS đều KHÔNG có Tail Call Optimization (TCO) —
đệ quy sâu sẽ tốn bộ nhớ theo call stack (xem lại Stacks) và có thể lỗi
("RecursionError" ở Python, "Maximum call stack size exceeded" ở JS).
Khác biệt: Python giới hạn độ sâu đệ quy MẶC ĐỊNH rất thấp
(sys.getrecursionlimit() = 1000), trong khi JS engine thường cho phép sâu
hơn nhiều (chục nghìn) trước khi stack overflow — cần lưu ý khi port thuật
toán đệ quy từ JS sang Python cho input lớn.
"""

import sys
from functools import lru_cache


def factorial(n: int) -> int:
    """Base case: n <= 1. Recursive case: n * factorial(n-1)."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def factorial_iterative(n: int) -> int:
    """Cùng bài toán, giải bằng loop — không tốn call stack, nhanh hơn
    vì không có overhead của function call."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci_naive(n: int) -> int:
    """Đệ quy "ngây thơ" — O(2^n) vì tính lại fibonacci(k) rất nhiều lần
    (fibonacci(5) gọi fibonacci(3) tới 2 lần, fibonacci(2) tới 3 lần...)."""
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    """Memoization: cache kết quả đã tính -> O(n), mỗi giá trị chỉ tính 1
    lần. lru_cache là decorator có sẵn của Python, không cần tự viết cache
    dict thủ công."""
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def demo_recursion_limit() -> None:
    """Python giới hạn độ sâu đệ quy mặc định — khác JS thường sâu hơn."""
    print("giới hạn đệ quy mặc định:", sys.getrecursionlimit())

    def count_up(n: int, limit: int) -> int:
        if n >= limit:
            return n
        return count_up(n + 1, limit)

    try:
        count_up(0, 2000)
    except RecursionError as e:
        print(f"đệ quy sâu 2000 bước -> lỗi: {e}")


def sum_nested_list(data: list) -> int:
    """Use case thực tế của đệ quy: duyệt cấu trúc lồng nhau độ sâu không
    biết trước (nested list, cây thư mục, JSON) — loop thường không đủ
    linh hoạt cho việc này."""
    total = 0
    for item in data:
        if isinstance(item, list):
            total += sum_nested_list(item)  # đệ quy vào list con
        else:
            total += item
    return total


def main() -> None:
    print("factorial(5):", factorial(5))
    print("factorial_iterative(5):", factorial_iterative(5))

    print()
    print("fibonacci_naive(20):", fibonacci_naive(20))
    print("fibonacci_memoized(50):", fibonacci_memoized(50), "(naive sẽ rất chậm ở n=50)")

    print()
    demo_recursion_limit()

    print()
    nested = [1, [2, 3, [4, 5, [6]], 7], 8]
    print(f"sum_nested_list({nested}):", sum_nested_list(nested))


if __name__ == "__main__":
    main()
