"""
Topic: Trees (Binary Tree, Binary Search Tree)
So sánh JS: giống Linked List, cây không có built-in ở cả Python lẫn JS —
tự cài đặt bằng class + reference (node.left/node.right thay vì node.next).
Khái niệm giống hệt nhau ở mọi ngôn ngữ; điểm khác biệt thực tế là Python
đệ quy bị giới hạn bởi sys.getrecursionlimit() = 1000 (xem lại mục
Recursion) — cây quá sâu (vd. BST bị lệch hẳn 1 bên) có thể gây
RecursionError khi duyệt đệ quy, cần chuyển sang duyệt bằng loop + stack/
queue tường minh nếu cần xử lý cây rất sâu.
"""

from __future__ import annotations

from collections import deque


class TreeNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


class BinarySearchTree:
    """BST: quy ước left < node < right tại MỌI node — quy ước này là thứ
    giúp search/insert nhanh hơn duyệt tuyến tính, khác binary tree
    thường (không có thứ tự, chỉ có tối đa 2 con)."""

    def __init__(self) -> None:
        self.root: TreeNode | None = None

    def insert(self, value: int) -> None:
        """O(log n) trung bình nếu cây cân bằng, O(n) worst case nếu cây
        bị lệch hẳn 1 bên (vd. insert dữ liệu đã sorted sẵn -> thành
        linked list trá hình)."""
        if self.root is None:
            self.root = TreeNode(value)
            return
        self._insert_recursive(self.root, value)

    def _insert_recursive(self, node: TreeNode, value: int) -> None:
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value: int) -> bool:
        """O(log n) trung bình — mỗi bước loại bỏ 1 nhánh, giống binary
        search trên list đã sorted (xem lại mục Searching Algorithms)."""
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node: TreeNode | None, value: int) -> bool:
        if node is None:
            return False
        if node.value == value:
            return True
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

    def inorder(self) -> list[int]:
        """Inorder (left -> node -> right) trên BST luôn cho ra dãy ĐÃ
        SORTED — đây là tính chất đặc trưng của BST."""
        result: list[int] = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: TreeNode | None, result: list[int]) -> None:
        if node is None:
            return
        self._inorder_recursive(node.left, result)
        result.append(node.value)
        self._inorder_recursive(node.right, result)

    def preorder(self) -> list[int]:
        """Preorder (node -> left -> right) — dùng khi cần copy/serialize
        cây theo đúng cấu trúc (root trước, dễ tái tạo lại cây)."""
        result: list[int] = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node: TreeNode | None, result: list[int]) -> None:
        if node is None:
            return
        result.append(node.value)
        self._preorder_recursive(node.left, result)
        self._preorder_recursive(node.right, result)

    def level_order(self) -> list[int]:
        """Level-order (BFS, xem lại mục Queues) — duyệt theo từng tầng
        từ trên xuống, dùng queue thay vì đệ quy."""
        if self.root is None:
            return []

        result: list[int] = []
        queue: deque[TreeNode] = deque([self.root])
        while queue:
            node = queue.popleft()
            result.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def height(self) -> int:
        """Chiều cao cây — ảnh hưởng trực tiếp tới độ phức tạp thực tế
        (O(height) cho search/insert, height = log n nếu cân bằng, = n
        nếu bị lệch hẳn)."""
        return self._height_recursive(self.root)

    def _height_recursive(self, node: TreeNode | None) -> int:
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left), self._height_recursive(node.right))


def demo_bst() -> None:
    bst = BinarySearchTree()
    for value in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(value)

    print("inorder (luôn sorted trên BST):", bst.inorder())
    print("preorder:", bst.preorder())
    print("level_order (BFS):", bst.level_order())
    print("height:", bst.height())

    print("search(40):", bst.search(40))
    print("search(99):", bst.search(99))


def demo_unbalanced_tree() -> None:
    """Insert dữ liệu ĐÃ SORTED vào BST -> cây bị lệch hẳn 1 bên, thành
    linked list trá hình -> search/insert từ O(log n) tụt xuống O(n)."""
    bst = BinarySearchTree()
    for value in [1, 2, 3, 4, 5]:  # đã sorted -> worst case cho BST
        bst.insert(value)

    print(f"insert [1,2,3,4,5] (đã sorted) -> height = {bst.height()} (thay vì ~3 nếu cân bằng)")
    print("đây là lý do các thư viện thực tế dùng self-balancing tree (AVL, Red-Black)")


def main() -> None:
    demo_bst()
    print()
    demo_unbalanced_tree()


if __name__ == "__main__":
    main()
