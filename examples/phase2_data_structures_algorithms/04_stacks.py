"""
Topic: Stacks (LIFO)
So sánh JS: Python dùng list.append()/list.pop() làm stack, y hệt JS
Array.push()/Array.pop() — cả hai đều thao tác ở CUỐI mảng nên là O(1).
Lỗi thường gặp: dùng list.pop(0)/insert(0, x) để giả lập stack — sai vị
trí (đó là đầu, không phải cuối) và tốn O(n) thay vì O(1). JS cũng có lỗi
tương tự nếu dùng shift()/unshift() thay vì push()/pop().
"""


def demo_basic_stack() -> None:
    """Dùng list làm stack: push = append(), pop = pop() — cả hai O(1)."""
    stack: list[str] = []
    stack.append("a")   # push
    stack.append("b")
    stack.append("c")
    print("stack sau 3 lần push:", stack)

    top = stack.pop()     # pop — LIFO: lấy ra phần tử thêm sau cùng
    print("pop():", top, "-> stack còn:", stack)

    print("peek (xem đỉnh không pop):", stack[-1])


def is_balanced_parentheses(expr: str) -> bool:
    """Use case kinh điển của stack: kiểm tra ngoặc cân bằng.
    Gặp ngoặc mở -> push. Gặp ngoặc đóng -> pop và so khớp."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []

    for char in expr:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack or stack.pop() != pairs[char]:
                return False

    return len(stack) == 0


def reverse_string_with_stack(s: str) -> str:
    """Stack tự nhiên đảo ngược thứ tự nhờ đặc tính LIFO."""
    stack = list(s)
    result = []
    while stack:
        result.append(stack.pop())
    return "".join(result)


def demo_call_stack_analogy() -> None:
    """Stack cũng chính là cơ chế đằng sau function call (call stack) —
    xem thêm ở topic Recursion. Ở đây minh hoạ thủ công bằng list."""
    call_stack: list[str] = []

    def enter(fn_name: str) -> None:
        call_stack.append(fn_name)
        print(f"-> gọi {fn_name}, call stack: {call_stack}")

    def leave() -> None:
        fn_name = call_stack.pop()
        print(f"<- return từ {fn_name}, call stack: {call_stack}")

    enter("main")
    enter("process_order")
    enter("charge_payment")
    leave()
    leave()
    leave()


def main() -> None:
    demo_basic_stack()

    print()
    for expr in ["(a + b) * [c - d]", "([)]", "{{[]}}"]:
        print(f"is_balanced({expr!r}):", is_balanced_parentheses(expr))

    print()
    print("reverse('hello'):", reverse_string_with_stack("hello"))

    print()
    demo_call_stack_analogy()


if __name__ == "__main__":
    main()
