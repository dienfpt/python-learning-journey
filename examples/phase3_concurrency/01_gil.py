"""
Topic: GIL (Global Interpreter Lock)
So sánh JS: Node.js đơn luồng (single-threaded) theo thiết kế — không có
khái niệm "nhiều thread cùng chạy Python/JS code" để so sánh. Python
NGƯỢC LẠI: có threading module thật (multi-threaded), nhưng GIL đảm bảo
tại một thời điểm chỉ 1 thread được thực thi Python bytecode — nên nhiều
thread Python KHÔNG chạy song song cho công việc CPU-bound, dù hệ điều
hành cấp nhiều core. Đây là khác biệt quan trọng nhất cần hiểu trước khi
học threading/multiprocessing/asyncio ở các file sau.
"""

import threading
import time


def cpu_bound_task(n: int) -> int:
    """Công việc CPU-bound thuần: chỉ tính toán, không I/O, không chờ
    đợi -> CPU phải bận liên tục để hoàn thành."""
    total = 0
    for i in range(n):
        total += i * i
    return total


def run_single_threaded(n: int, times: int) -> float:
    start = time.perf_counter()
    for _ in range(times):
        cpu_bound_task(n)
    return time.perf_counter() - start


def run_multi_threaded(n: int, times: int) -> float:
    """Chạy CÙNG khối lượng công việc bằng nhiều thread -- nếu threading
    thật sự song song, thời gian phải giảm gần theo số thread. Vì GIL,
    thực tế thời gian KHÔNG giảm đáng kể (thậm chí chậm hơn vì overhead
    chuyển đổi thread)."""
    start = time.perf_counter()
    threads = [threading.Thread(target=cpu_bound_task, args=(n,)) for _ in range(times)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start


def demo_gil_blocks_cpu_bound_parallelism() -> None:
    n = 5_000_000
    times = 4

    single = run_single_threaded(n, times)
    multi = run_multi_threaded(n, times)

    print(f"CPU-bound task x{times} lần, tuần tự (1 thread):    {single:.3f}s")
    print(f"CPU-bound task x{times} lần, song song ({times} threads): {multi:.3f}s")
    print("-> GIL khiến 2 con số này GẦN BẰNG NHAU dù có nhiều thread,")
    print("   vì tại 1 thời điểm chỉ 1 thread được chạy Python bytecode.")


def io_bound_task(seconds: float) -> None:
    """time.sleep() giải phóng (release) GIL trong lúc chờ -- đây là lý do
    threading VẪN hữu ích cho I/O-bound (xem file 02_threading.py),
    dù vô dụng cho CPU-bound như trên."""
    time.sleep(seconds)


def demo_gil_releases_during_io() -> None:
    times = 4
    delay = 0.3

    start = time.perf_counter()
    for _ in range(times):
        io_bound_task(delay)
    sequential = time.perf_counter() - start

    start = time.perf_counter()
    threads = [threading.Thread(target=io_bound_task, args=(delay,)) for _ in range(times)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    concurrent = time.perf_counter() - start

    print(f"I/O-bound (sleep {delay}s) x{times} lần, tuần tự:  {sequential:.3f}s")
    print(f"I/O-bound (sleep {delay}s) x{times} lần, threading: {concurrent:.3f}s")
    print("-> Lần này threading THỰC SỰ giúp nhanh hơn ~4 lần, vì sleep()")
    print("   giải phóng GIL cho thread khác chạy trong lúc chờ.")


def main() -> None:
    print("giới hạn thread cho GIL: mỗi thời điểm CHỈ 1 thread chạy bytecode\n")

    demo_gil_blocks_cpu_bound_parallelism()
    print()
    demo_gil_releases_during_io()


if __name__ == "__main__":
    main()
