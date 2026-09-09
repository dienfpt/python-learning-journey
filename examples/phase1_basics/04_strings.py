"""
Topic: Working with Strings
So sánh JS: f-string ~ template literal.
`.join()` gọi NGƯỢC so với JS: "-".join(list) thay vì array.join("-").
"""


def demo_fstring() -> None:
    name = "World"
    print(f"Hello, {name}!")  # thay cho `Hello, ${name}!`


def demo_join_reversed() -> None:
    parts = ["a", "b", "c"]
    joined = "-".join(parts)  # separator gọi method, KHÔNG phải array
    print("joined:", joined)


def demo_slicing() -> None:
    s = "Hello, Python"
    print("s[7:13] =", s[7:13])   # "Python"
    print("reversed =", s[::-1])  # reverse toàn bộ string


def demo_multiline() -> None:
    text = """Dòng 1
Dòng 2
Dòng 3"""
    print(text)


def main() -> None:
    demo_fstring()
    demo_join_reversed()
    demo_slicing()
    demo_multiline()


if __name__ == "__main__":
    main()
