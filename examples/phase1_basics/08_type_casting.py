"""
Topic: Type Casting
So sánh JS: Python cast lỗi -> ValueError rõ ràng, KHÔNG âm thầm trả NaN
như parseInt/parseFloat của JS.
"""


def demo_valid_casts() -> None:
    print(int("42"))
    print(float("3.14"))
    print(str(42))
    print(list("abc"))
    print(bool(0), bool(1))


def demo_invalid_cast() -> None:
    try:
        int("abc")  # JS: parseInt("abc") -> NaN (âm thầm)
    except ValueError as e:
        print(f"ValueError như mong đợi (Python KHÔNG trả NaN): {e}")


def main() -> None:
    demo_valid_casts()
    demo_invalid_cast()


if __name__ == "__main__":
    main()
