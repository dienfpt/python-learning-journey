"""
Topic: Graphs
So sánh JS: khái niệm giống hệt nhau ở mọi ngôn ngữ — không có built-in
Graph class ở cả Python lẫn JS, cách phổ biến nhất là dùng dict/Map làm
adjacency list (`{node: [neighbors]}`). Cây (mục 10) thực chất là 1 dạng
đặc biệt của đồ thị (không có chu trình - cycle, có đúng 1 đường đi giữa
2 node bất kỳ) — nên BFS/DFS ở đây tổng quát hoá level_order/traversal đã
làm với cây.
"""

from collections import deque


class Graph:
    """Adjacency list — mỗi node map tới list các node kề (neighbor).
    Ưu điểm so với adjacency matrix (ma trận n x n): tiết kiệm bộ nhớ
    O(V + E) thay vì O(V^2) cho đồ thị thưa (sparse, ít cạnh)."""

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self.adjacency: dict[str, list[str]] = {}

    def add_node(self, node: str) -> None:
        self.adjacency.setdefault(node, [])

    def add_edge(self, a: str, b: str) -> None:
        self.add_node(a)
        self.add_node(b)
        self.adjacency[a].append(b)
        if not self.directed:  # đồ thị vô hướng: cạnh đi được cả 2 chiều
            self.adjacency[b].append(a)

    def bfs(self, start: str) -> list[str]:
        """Breadth-First Search — dùng QUEUE (xem lại mục Queues), duyệt
        theo từng "lớp" node gần start nhất trước. Tìm được đường đi
        NGẮN NHẤT theo số cạnh trên đồ thị không trọng số."""
        visited = {start}
        order = []
        queue: deque[str] = deque([start])

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in self.adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order

    def dfs(self, start: str) -> list[str]:
        """Depth-First Search — dùng STACK (xem lại mục Stacks), đi sâu
        nhất có thể trước khi quay lui. Thường viết bằng đệ quy (call
        stack = stack ẩn) hoặc stack tường minh như dưới đây."""
        visited = {start}
        order = []
        stack: list[str] = [start]

        while stack:
            node = stack.pop()
            order.append(node)
            for neighbor in reversed(self.adjacency[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)

        return order

    def dfs_recursive(self, start: str, visited: set[str] | None = None) -> list[str]:
        """DFS bằng đệ quy — ngắn gọn hơn, nhưng có thể RecursionError
        nếu đồ thị quá lớn/sâu (xem lại mục Recursion)."""
        if visited is None:
            visited = set()
        visited.add(start)
        order = [start]

        for neighbor in self.adjacency[start]:
            if neighbor not in visited:
                order.extend(self.dfs_recursive(neighbor, visited))

        return order

    def has_path(self, start: str, end: str) -> bool:
        return end in self.bfs(start)


def demo_undirected_graph() -> None:
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")
    g.add_edge("D", "E")

    print("adjacency list:", g.adjacency)
    print("BFS từ A:", g.bfs("A"))
    print("DFS từ A (stack tường minh):", g.dfs("A"))
    print("DFS từ A (đệ quy):", g.dfs_recursive("A"))
    print("has_path(A, E):", g.has_path("A", "E"))
    print("has_path(A, Z) (không tồn tại node Z):", "Z" in g.adjacency and g.has_path("A", "Z"))


def demo_directed_graph() -> None:
    """Đồ thị có hướng — cạnh chỉ đi được 1 chiều, vd. mô hình "follow"
    trên mạng xã hội (A follow B không có nghĩa B follow A)."""
    g = Graph(directed=True)
    g.add_edge("alice", "bob")     # alice follows bob
    g.add_edge("bob", "claire")    # bob follows claire

    print("alice's following:", g.adjacency["alice"])
    print("bob's followers tính bằng cách nào? -> phải build reverse graph")
    print("  (adjacency list có hướng KHÔNG cho biết ai trỏ VÀO 1 node,")
    print("   chỉ biết node đó trỏ ĐẾN ai)")


def main() -> None:
    demo_undirected_graph()
    print()
    demo_directed_graph()


if __name__ == "__main__":
    main()
