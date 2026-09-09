"""
Topic: Multiprocessing
So sánh JS: tương đương gần nhất trong Node.js là `child_process` hoặc
`cluster` module (spawn nhiều process riêng biệt để tận dụng nhiều CPU
core) -- Node cũng phải dùng process (không phải thread) để đạt CPU
parallelism thật, vì lý do tương tự Python: mỗi process có interpreter/
runtime riêng, không bị giới hạn kiểu GIL của process khác. Điểm khác
Python: `multiprocessing` cho phép chia sẻ code style gần giống threading
(cùng API `Process`, `Pool`), trong khi Node child_process thường phải
tự thiết kế giao thức IPC (inter-process communication) tường minh hơn.

Lưu ý kỹ thuật: multiprocessing (chế độ "spawn", mặc định trên macOS/
Windows) cần pickle function truyền cho Process/Pool, và cần import lại
module chứa function đó trong process con bằng đúng tên module -- vì vậy
target function phải là top-level function của 1 module import được
(không phải lambda/closure/nested function).
"""

import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process, Queue


def cpu_bound_task(n: int) -> int:
    """Cùng hàm CPU-bound như ở file 01_gil.py -- lần này chạy bằng
    process thay vì thread để so sánh."""
    total = 0
    for i in range(n):
        total += i * i
    return total


def run_single_process(n: int, times: int) -> float:
    start = time.perf_counter()
    for _ in range(times):
        cpu_bound_task(n)
    return time.perf_counter() - start


def run_multi_process(n: int, times: int) -> float:
    """Mỗi Process có GIL + không gian bộ nhớ RIÊNG -- chạy thật sự song
    song trên nhiều CPU core, khác threading bị GIL chặn ở file 01_gil.py."""
    start = time.perf_counter()
    processes = [Process(target=cpu_bound_task, args=(n,)) for _ in range(times)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    return time.perf_counter() - start


def demo_multiprocessing_beats_gil() -> None:
    n = 5_000_000
    times = 4

    single = run_single_process(n, times)
    multi = run_multi_process(n, times)

    print(f"CPU-bound task x{times} lần, 1 process (tuần tự):     {single:.3f}s")
    print(f"CPU-bound task x{times} lần, {times} process song song: {multi:.3f}s")
    print("-> Khác threading (01_gil.py), lần này thời gian GIẢM RÕ RỆT")
    print("   vì mỗi process có GIL riêng, chạy thật trên nhiều CPU core.")


def demo_process_pool_executor() -> None:
    """ProcessPoolExecutor: API giống ThreadPoolExecutor (mục Threading),
    nhưng dùng process -- cách idiomatic để chạy CPU-bound song song."""
    numbers = [5_000_000, 5_000_000, 5_000_000, 5_000_000]

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, numbers))
    elapsed = time.perf_counter() - start

    print(f"ProcessPoolExecutor (4 workers): {elapsed:.3f}s, kết quả đầu: {results[0]}")


def worker_with_queue(worker_id: int, queue: Queue) -> None:
    """Process không share memory với process cha (khác threading share
    trực tiếp) -- phải dùng Queue/Pipe/Value/Array của multiprocessing để
    gửi dữ liệu qua lại, tương tự message passing của Worker Threads bên
    Node.js (xem lại mục Threading)."""
    result = cpu_bound_task(1_000_000)
    queue.put((worker_id, result))


def demo_no_shared_memory() -> None:
    """Minh hoạ: process con KHÔNG thể trực tiếp trả giá trị return như
    hàm bình thường -- phải qua Queue vì bộ nhớ tách biệt hoàn toàn."""
    queue: Queue = Queue()
    processes = [Process(target=worker_with_queue, args=(i, queue)) for i in range(3)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    results = [queue.get() for _ in processes]
    print("kết quả nhận qua Queue từ các process con:", sorted(results))


def main() -> None:
    demo_multiprocessing_beats_gil()
    print()
    demo_process_pool_executor()
    print()
    demo_no_shared_memory()


if __name__ == "__main__":
    # multiprocessing trên macOS/Windows dùng "spawn" -- yêu cầu code tạo
    # process phải nằm trong if __name__ == "__main__", nếu không sẽ lặp
    # vô hạn việc import lại module (khác Linux dùng "fork" mặc định).
    main()
