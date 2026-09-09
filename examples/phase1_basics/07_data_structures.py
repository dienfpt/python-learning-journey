"""
Topic: Lists, Tuples, Sets, Dicts
So sánh JS:
- list ~ Array (mutable)
- tuple: KHÔNG có tương đương trong JS -- immutable, dùng cho fixed data
- set ~ Set nhưng có toán tử tập hợp | & - ^
- dict ~ Object/Map, key phải hashable (immutable)
List/dict comprehension là idiom chuẩn Python, JS không có cú pháp tương đương gọn.
"""


def demo_list() -> None:
    fruits = ["apple", "banana", "cherry"]
    fruits.append("date")        # push
    fruits.pop()                   # pop
    fruits.insert(0, "avocado")   # unshift-like

    print("fruits:", fruits)
    print("slice[1:3]:", fruits[1:3])

    squares = [x**2 for x in range(10)]
    evens = [x for x in range(20) if x % 2 == 0]
    print("squares:", squares)
    print("evens:", evens)


def demo_tuple() -> None:
    point = (10, 20)
    try:
        point[0] = 5  # type: ignore
    except TypeError as e:
        print(f"Tuple immutable, lỗi như mong đợi: {e}")

    x, y = point  # unpacking
    print(f"unpacked x={x}, y={y}")


def demo_set() -> None:
    a = {1, 2, 3}
    b = {2, 3, 4}
    print("union:", a | b)
    print("intersection:", a & b)
    print("difference (a-b):", a - b)
    print("symmetric_diff:", a ^ b)


def demo_dict() -> None:
    person = {"name": "Alice", "age": 30}
    person["email"] = "a@test.com"
    print("get with default:", person.get("phone", "N/A"))

    squares = {x: x**2 for x in range(5)}
    print("dict comprehension:", squares)


def main() -> None:
    demo_list()
    demo_tuple()
    demo_set()
    demo_dict()


if __name__ == "__main__":
    main()
