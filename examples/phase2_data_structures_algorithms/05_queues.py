"""
Topic: Queues (FIFO)
So sánh JS: JS cũng không có Queue built-in hiệu quả — dùng Array.push()/
Array.shift() thì shift() là O(n) (giống Python list.pop(0)). Python giải
quyết bằng collections.deque — doubly linked list nội bộ nên cả 2 đầu đều
O(1). Đây là điểm khác biệt quan trọng: đừng dùng list làm queue trong
Python nếu cần hiệu năng, hãy dùng deque.
"""

from collections import deque


def demo_why_not_list_as_queue() -> None:
    """list.pop(0) là O(n) vì phải dịch chuyển mọi phần tử còn lại lên
    trước 1 vị trí — dùng list làm queue sẽ chậm dần khi queue lớn."""
    queue_as_list: list[str] = ["a", "b", "c"]
    first = queue_as_list.pop(0)  # O(n) -- tránh dùng cách này
    print("list.pop(0):", first, "-> còn:", queue_as_list)


def demo_deque_as_queue() -> None:
    """deque: append (enqueue) ở cuối O(1), popleft (dequeue) ở đầu O(1)."""
    queue: deque[str] = deque()
    queue.append("customer_1")   # enqueue
    queue.append("customer_2")
    queue.append("customer_3")
    print("queue sau 3 lần enqueue:", list(queue))

    served = queue.popleft()      # dequeue — FIFO: phục vụ người đến trước
    print("dequeue():", served, "-> còn:", list(queue))


def bfs_shortest_path(graph: dict[str, list[str]], start: str, goal: str) -> list[str] | None:
    """Use case kinh điển của queue: BFS tìm đường đi ngắn nhất (theo số
    cạnh) trên đồ thị không trọng số. Xem thêm ở topic Graphs."""
    queue: deque[list[str]] = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()   # luôn xử lý node được thêm vào SỚM NHẤT
        node = path[-1]

        if node == goal:
            return path

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None


def demo_task_scheduling() -> None:
    """Use case: hàng đợi xử lý task theo thứ tự đến trước - phục vụ
    trước (giống job queue, print queue, message queue)."""
    tasks: deque[str] = deque(["send_email", "resize_image", "generate_report"])

    while tasks:
        current = tasks.popleft()
        print(f"đang xử lý: {current}")


def main() -> None:
    demo_why_not_list_as_queue()

    print()
    demo_deque_as_queue()

    print()
    social_graph = {
        "you": ["alice", "bob"],
        "alice": ["you", "claire"],
        "bob": ["you", "diana"],
        "claire": ["alice", "goal_user"],
        "diana": ["bob"],
    }
    path = bfs_shortest_path(social_graph, "you", "goal_user")
    print("BFS shortest path you -> goal_user:", path)

    print()
    demo_task_scheduling()


if __name__ == "__main__":
    main()
