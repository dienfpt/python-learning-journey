"""
Topic: Conditionals
So sánh JS: elif thay else if. Ternary viết ngược: x if cond else y.
match-case (3.10+) thay switch. Truthy/falsy KHÁC JS: [] và {} là falsy
trong Python, nhưng là truthy trong JS -- bẫy dễ gặp khi chuyển ngôn ngữ.
"""


def classify_age(age: int) -> str:
    if age >= 18:
        status = "adult"
    elif age >= 13:
        status = "teen"
    else:
        status = "child"
    return status


def demo_ternary(age: int) -> None:
    status = "adult" if age >= 18 else "child"
    print("ternary result:", status)


def demo_match_case(status_code: int) -> None:
    match status_code:
        case 200:
            print("OK")
        case 404:
            print("Not Found")
        case _:
            print("Unknown")


def demo_falsy_trap() -> None:
    # Trong JS: [] && "truthy" -> "truthy" (array rỗng là truthy)
    # Trong Python: [] and "truthy" -> [] (list rỗng là falsy)
    empty_list = []
    print("bool([]) =", bool(empty_list))     # False
    print("bool({}) =", bool({}))               # False
    print("bool('') =", bool(""))                # False
    print("bool(0) =", bool(0))                    # False


def main() -> None:
    print(classify_age(20))
    demo_ternary(15)
    demo_match_case(404)
    demo_falsy_trap()


if __name__ == "__main__":
    main()
