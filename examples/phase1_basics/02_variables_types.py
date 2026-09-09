"""
Topic: Variables and Data Types
So sánh JS: dynamic typing nhưng STRONG typing.
"5" + 3 trong JS -> "53" (coercion ngầm)
"5" + 3 trong Python -> TypeError (phải cast rõ ràng)
Không có `undefined`, chỉ có None. Không có const thật (convention: UPPER_CASE).
"""


def demo_strong_typing() -> None:
    try:
        result = "5" + 3  # type: ignore
    except TypeError as e:
        print(f"TypeError như mong đợi: {e}")
    else:
        print("Không nên tới đây:", result)


def demo_basic_types() -> None:
    age: int = 30
    price: float = 9.99
    name: str = "Claude"
    is_active: bool = True
    nothing = None  # tương đương null, KHÔNG phải undefined

    print(type(age), type(price), type(name), type(is_active), type(nothing))


MAX_RETRIES = 3  # convention "const" -- không có enforcement thật


def main() -> None:
    demo_strong_typing()
    demo_basic_types()
    print("MAX_RETRIES (convention const):", MAX_RETRIES)


if __name__ == "__main__":
    main()
