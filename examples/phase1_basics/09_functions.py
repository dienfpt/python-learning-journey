"""
Topic: Functions, Builtin Functions
So sánh JS: default param giống JS. *args/**kwargs TÁCH RIÊNG
positional/keyword, khác ...rest gộp chung của JS. lambda giới hạn 1
expression duy nhất, không multiline như arrow function.
"""


def add(a: int, b: int = 10) -> int:
    return a + b


def show_args(*args, **kwargs) -> None:
    print("args (positional):", args)
    print("kwargs (keyword):", kwargs)


def demo_lambda() -> None:
    square = lambda x: x**2
    print("lambda square(5):", square(5))


def demo_builtins() -> None:
    fruits = ["apple", "banana", "cherry"]

    # enumerate thay cho .map((item, i) => ...)
    for i, fruit in enumerate(fruits):
        print(i, fruit)

    numbers = [4, 2, 8, 1]
    print("sorted:", sorted(numbers))
    print("sum:", sum(numbers))
    print("min/max:", min(numbers), max(numbers))
    print("map+list:", list(map(lambda n: n * 2, numbers)))
    print("filter+list:", list(filter(lambda n: n > 2, numbers)))
    print("zip:", list(zip(fruits, numbers)))


def main() -> None:
    print("add(5):", add(5))
    print("add(5, 20):", add(5, 20))
    show_args(1, 2, name="Claude")
    demo_lambda()
    demo_builtins()


if __name__ == "__main__":
    main()
