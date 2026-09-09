"""
Topic: Chọn đúng mô hình concurrency — Threading vs Multiprocessing vs
asyncio, so sánh với Node.js Event Loop
So sánh JS: Node.js CHỈ có 1 mô hình concurrency chính cho code JS
(event loop, giống asyncio) -- không phải tự chọn giữa 3 lựa chọn như
Python. Muốn CPU parallelism thật ở Node phải ra khỏi mô hình đó hoàn
toàn (Worker Threads hoặc child_process/cluster). Python "linh hoạt" hơn
vì có sẵn cả 3 (threading/multiprocessing/asyncio) nhưng đổi lại phải tự
biết chọn đúng công cụ -- đây là lý do phase này tồn tại như 1 chương
riêng, trong khi JS dev thường chỉ cần biết mỗi async/await.
"""

import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor


def choose_concurrency_model(io_bound: bool, num_tasks: int) -> str:
    """Decision guide đơn giản hoá -- xem bảng đầy đủ trong notes.
    Quy tắc cốt lõi: CPU-bound -> multiprocessing. I/O-bound số lượng
    lớn -> asyncio. I/O-bound số lượng nhỏ hoặc cần dùng thư viện chỉ hỗ
    trợ sync -> threading."""
    if not io_bound:
        return "multiprocessing (CPU-bound -> cần parallelism thật, vượt GIL)"
    if num_tasks > 50:
        return "asyncio (I/O-bound số lượng lớn -> overhead thấp hơn threading nhiều)"
    return "threading (I/O-bound số lượng nhỏ, hoặc phải gọi thư viện chỉ hỗ trợ sync)"


def demo_decision_guide() -> None:
    cases = [
        (False, 4, "resize 4 ảnh lớn"),
        (True, 5, "gọi 5 API nội bộ, dùng thư viện requests (sync)"),
        (True, 500, "gọi 500 API bên ngoài trong 1 web scraper"),
    ]
    for io_bound, n, description in cases:
        recommendation = choose_concurrency_model(io_bound, n)
        print(f"- {description}")
        print(f"  -> {recommendation}")


def blocking_io_task(seconds: float) -> None:
    time.sleep(seconds)


async def async_io_task(seconds: float) -> None:
    await asyncio.sleep(seconds)


def benchmark_threading(num_tasks: int, delay: float) -> float:
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_tasks) as executor:
        list(executor.map(lambda _: blocking_io_task(delay), range(num_tasks)))
    return time.perf_counter() - start


async def _benchmark_asyncio(num_tasks: int, delay: float) -> float:
    start = time.perf_counter()
    await asyncio.gather(*[async_io_task(delay) for _ in range(num_tasks)])
    return time.perf_counter() - start


def demo_overhead_comparison() -> None:
    """Với số lượng tác vụ I/O-bound VỪA PHẢI, threading và asyncio cho
    thời gian hoàn thành gần như nhau (cả 2 đều "song song" được việc
    chờ). Khác biệt thực sự nằm ở OVERHEAD: mỗi OS thread tốn bộ nhớ +
    chi phí context-switch của hệ điều hành, còn coroutine là object nhẹ
    do chính Python quản lý trong 1 thread -- asyncio scale tốt hơn nhiều
    khi số lượng tác vụ lên tới hàng trăm/nghìn (vd. server xử lý nhiều
    connection đồng thời), dù ở quy mô nhỏ như benchmark này sự khác biệt
    thời gian chạy chưa rõ rệt."""
    num_tasks = 30
    delay = 0.05

    threading_time = benchmark_threading(num_tasks, delay)
    asyncio_time = asyncio.run(_benchmark_asyncio(num_tasks, delay))

    print(f"{num_tasks} tác vụ I/O-bound (mỗi tác vụ chờ {delay}s):")
    print(f"  threading (ThreadPoolExecutor): {threading_time:.3f}s")
    print(f"  asyncio (gather):                {asyncio_time:.3f}s")
    print(f"  -> thời gian gần bằng nhau, nhưng threading tạo {num_tasks} OS")
    print(f"     thread thật (tốn bộ nhớ), asyncio chỉ tạo {num_tasks} coroutine")
    print("     nhẹ trong 1 thread duy nhất -- khác biệt rõ khi tăng quy mô")
    print("     lên hàng trăm/nghìn tác vụ.")


def main() -> None:
    demo_decision_guide()
    print()
    demo_overhead_comparison()


if __name__ == "__main__":
    main()
