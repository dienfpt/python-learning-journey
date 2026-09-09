"""
Topic: Linked Lists
So sánh JS: JS không có linked list built-in (cũng như Python) — cả hai
đều phải tự implement bằng class + reference. Điểm khác biệt quan trọng
với Python `list`/JS `Array` (dynamic array, bộ nhớ liền kề - contiguous):
linked list lưu các Node RẢI RÁC trong bộ nhớ, mỗi Node giữ con trỏ
(reference) tới Node kế tiếp. Đánh đổi: mất khả năng truy cập theo index
O(1) (phải đi từng bước O(n)), đổi lại insert/delete ở one đầu đã biết vị
trí là O(1) (không cần dịch chuyển phần tử như array).
"""

from __future__ import annotations

from collections import deque


class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.next: Node | None = None


class SinglyLinkedList:
    """Linked list tự implement để thấy rõ cơ chế bên trong."""

    def __init__(self) -> None:
        self.head: Node | None = None

    def prepend(self, value: int) -> None:
        """Thêm vào đầu — O(1), KHÔNG cần dịch chuyển phần tử như
        list.insert(0, x) (O(n))."""
        node = Node(value)
        node.next = self.head
        self.head = node

    def append(self, value: int) -> None:
        """Thêm vào cuối — O(n) vì phải duyệt hết để tìm node cuối (không
        giữ tail pointer ở implementation đơn giản này)."""
        node = Node(value)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = node

    def find(self, value: int) -> Node | None:
        """Tìm kiếm — O(n), không có random access như array."""
        current = self.head
        while current is not None:
            if current.value == value:
                return current
            current = current.next
        return None

    def delete(self, value: int) -> bool:
        """Xoá theo value — O(n) để tìm, nhưng việc xoá thực sự chỉ là
        đổi 1 con trỏ (O(1)) một khi đã tìm thấy node cần xoá."""
        if self.head is None:
            return False
        if self.head.value == value:
            self.head = self.head.next
            return True
        current = self.head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                return True
            current = current.next
        return False

    def to_list(self) -> list[int]:
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result


def demo_singly_linked_list() -> None:
    ll = SinglyLinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.prepend(0)
    print("list sau append(1,2,3) + prepend(0):", ll.to_list())

    found = ll.find(2)
    print("find(2):", found.value if found else None)

    ll.delete(2)
    print("sau delete(2):", ll.to_list())


def demo_deque_as_doubly_linked_list() -> None:
    """collections.deque là doubly linked list built sẵn của Python —
    O(1) thêm/xoá ở CẢ HAI đầu, khác list chỉ nhanh ở đầu cuối."""
    dq = deque([1, 2, 3])
    dq.appendleft(0)   # O(1) — list.insert(0, x) sẽ là O(n)
    dq.append(4)        # O(1), giống list.append
    print("deque sau appendleft(0) + append(4):", list(dq))

    dq.popleft()         # O(1) — list.pop(0) sẽ là O(n)
    print("sau popleft():", list(dq))


def main() -> None:
    demo_singly_linked_list()
    print()
    demo_deque_as_doubly_linked_list()


if __name__ == "__main__":
    main()
