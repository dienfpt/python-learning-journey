"""
Topic: Exceptions
So sánh JS: try/except/else/finally thay try/catch/finally.
Python có exception hierarchy chi tiết (ZeroDivisionError, KeyError,
IndexError, TypeError...) -- nên bắt cụ thể, không bắt chung chung.
Quan trọng cho FastAPI error handling sau này.
"""


def demo_basic_try_except() -> None:
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    else:
        print("Không có lỗi, result =", result)
    finally:
        print("Luôn chạy (finally)")


def demo_multiple_except() -> None:
    data = {"a": 1}
    try:
        value = data["b"]
    except (TypeError, KeyError) as e:
        print(f"Bắt nhiều loại lỗi: {type(e).__name__}: {e}")


def demo_raise_custom() -> None:
    def validate_age(age: int) -> None:
        if age < 0:
            raise ValueError("Age không thể âm")

    try:
        validate_age(-5)
    except ValueError as e:
        print(f"Custom raise: {e}")


class InsufficientFundsError(Exception):
    """Custom exception -- tương tự tạo class Error riêng trong JS."""


def demo_custom_exception_class() -> None:
    def withdraw(balance: float, amount: float) -> float:
        if amount > balance:
            raise InsufficientFundsError(
                f"Không đủ tiền: có {balance}, cần {amount}"
            )
        return balance - amount

    try:
        withdraw(100, 500)
    except InsufficientFundsError as e:
        print(f"Custom exception class: {e}")


def main() -> None:
    demo_basic_try_except()
    demo_multiple_except()
    demo_raise_custom()
    demo_custom_exception_class()


if __name__ == "__main__":
    main()
