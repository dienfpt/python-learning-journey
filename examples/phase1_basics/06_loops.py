"""
Topic: Loops
So sánh JS: for i in range(n) thay classic C-style for. for item in list
~ for...of. for k, v in dict.items() ~ Object.entries().
Loop có else (chạy khi KHÔNG bị break) -- Python-only, JS không có.
"""


def demo_range_loop() -> None:
    for i in range(5):
        print("range:", i)


def demo_iterate_list() -> None:
    fruits = ["apple", "banana", "cherry"]
    for fruit in fruits:
        print("fruit:", fruit)


def demo_iterate_dict() -> None:
    person = {"name": "Alice", "age": 30}
    for key, value in person.items():
        print(f"{key} = {value}")


def demo_while_loop() -> None:
    count = 0
    while count < 3:
        print("while count:", count)
        count += 1  # Python KHÔNG có ++ / --


def demo_loop_else() -> None:
    for i in range(5):
        if i == 10:  # điều kiện không bao giờ đúng ở đây
            break
    else:
        print("Loop hoàn thành, không bị break")

    for i in range(5):
        if i == 3:
            break
    else:
        print("Câu này KHÔNG in ra vì loop bị break")


def main() -> None:
    demo_range_loop()
    demo_iterate_list()
    demo_iterate_dict()
    demo_while_loop()
    demo_loop_else()


if __name__ == "__main__":
    main()
