"""
Topic: Operators
So sánh JS: có // (floor division) và ** (lũy thừa, JS cũng có ** từ ES2016).
`is` so sánh IDENTITY (reference), không phải value -- bẫy phổ biến khi
nhầm với == (value comparison).
"""


def demo_arithmetic() -> None:
    print("7 // 2 =", 7 // 2)   # 3, floor division
    print("2 ** 10 =", 2 ** 10)  # 1024
    print("7 % 2 =", 7 % 2)      # 1


def demo_is_vs_equals() -> None:
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a

    print("a == b (value):", a == b)   # True -- cùng giá trị
    print("a is b (identity):", a is b)  # False -- khác object trong memory
    print("a is c (identity):", a is c)  # True -- c trỏ tới cùng object với a


def demo_logical() -> None:
    x, y = True, False
    print("x and y:", x and y)
    print("x or y:", x or y)
    print("not x:", not x)


def main() -> None:
    demo_arithmetic()
    demo_is_vs_equals()
    demo_logical()


if __name__ == "__main__":
    main()
