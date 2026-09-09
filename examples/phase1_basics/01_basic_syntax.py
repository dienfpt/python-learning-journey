"""
Topic: Basic Syntax
So sánh JS: indentation là bắt buộc (không phải style), không dùng {} hay ;
Python KHÔNG có block scope cho if/for/while -> biến "leak" ra ngoài block,
khác hẳn let/const trong JS.
"""


def greet(name: str) -> None:
    if name:
        print(f"Hello, {name}")
    else:
        print("Hello, stranger")


def demo_no_block_scope() -> None:
    if True:
        x = 5  # khai báo trong block
    print("x sau block if:", x)  # vẫn truy cập được (5) -- khác JS let/const


def main() -> None:
    greet("Dien")
    greet("")
    demo_no_block_scope()


if __name__ == "__main__":
    main()
