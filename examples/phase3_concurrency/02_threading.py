"""
Topic: Threading
So sánh JS: Node.js không có race condition kiểu này vì code JS luôn chạy
trên 1 thread duy nhất (Worker Threads của Node là process/thread riêng
biệt, giao tiếp qua message passing, KHÔNG share memory trực tiếp như
Python threads). Python threads share cùng bộ nhớ tiến trình -- tiện lợi
(truy cập biến chung dễ dàng) nhưng nguy hiểm (race condition nếu không
đồng bộ hoá đúng cách) theo kiểu mà lập trình viên JS thường không phải
lo, trừ khi họ đã từng làm việc với Worker Threads chia sẻ SharedArrayBuffer.
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor


def download_file(name: str, seconds: float) -> str:
    """Giả lập I/O-bound: tải file mất thời gian chờ mạng, không tốn CPU
    trong lúc chờ -- ứng viên lý tưởng cho threading (xem lại mục GIL)."""
    time.sleep(seconds)
    return f"{name} downloaded"


def demo_concurrent_downloads() -> None:
    files = [("file1.zip", 0.3), ("file2.zip", 0.2), ("file3.zip", 0.4)]

    start = time.perf_counter()
    for name, delay in files:
        download_file(name, delay)
    sequential = time.perf_counter() - start

    start = time.perf_counter()
    threads = [threading.Thread(target=download_file, args=(name, delay)) for name, delay in files]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    concurrent = time.perf_counter() - start

    print(f"tải {len(files)} file tuần tự:  {sequential:.3f}s (tổng thời gian chờ cộng dồn)")
    print(f"tải {len(files)} file bằng thread: {concurrent:.3f}s (~bằng file chậm nhất)")


counter = 0


def increment_unsafe(times: int) -> None:
    """counter += 1 KHÔNG phải 1 thao tác nguyên tử (atomic) -- thực chất
    là đọc giá trị, cộng 1, ghi lại (3 bước riêng biệt). Nếu 2 thread cùng
    đọc trước khi thread kia kịp ghi, 1 lần increment sẽ bị MẤT -- đây là
    race condition. `time.sleep(0)` ở giữa đọc và ghi CƯỠNG BỨC context
    switch ngay tại khe hở đó để lỗi này luôn tái hiện được (bình thường
    GIL chuyển đổi thread không thường xuyên/đúng lúc để lộ race trong 1
    vòng lặp ngắn -- thử bỏ dòng sleep(0) sẽ thấy kết quả thường vẫn đúng
    "may mắn", nhưng lỗi vẫn tồn tại và có thể xảy ra bất kỳ lúc nào)."""
    global counter
    for _ in range(times):
        current = counter   # đọc
        time.sleep(0)         # nhường CPU cho thread khác ngay tại đây
        counter = current + 1  # ghi -- có thể ghi đè lên update của thread khác


def demo_race_condition() -> None:
    global counter
    counter = 0
    times_per_thread = 500
    num_threads = 4

    threads = [threading.Thread(target=increment_unsafe, args=(times_per_thread,)) for _ in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    expected = times_per_thread * num_threads
    print(f"kỳ vọng counter = {expected}, thực tế counter = {counter}")
    print("-> lệch nhau do race condition (nhiều lần increment bị MẤT vì")
    print("   2 thread cùng đọc giá trị cũ trước khi kịp ghi giá trị mới)")


counter_safe = 0
lock = threading.Lock()


def increment_safe(times: int) -> None:
    """Lock đảm bảo chỉ 1 thread được vào 'critical section' (đoạn code
    đọc-sửa-ghi biến chung) tại 1 thời điểm -- giống mutex trong các ngôn
    ngữ khác. `with lock:` tự động acquire/release, kể cả khi có exception.
    Cố ý giữ nguyên sleep(0) ở giữa đọc/ghi (giống increment_unsafe) để
    chứng minh: dù bị "nhường CPU" ngay giữa critical section, thread khác
    vẫn phải CHỜ vì không giành được lock -> kết quả luôn đúng."""
    global counter_safe
    for _ in range(times):
        with lock:
            current = counter_safe
            time.sleep(0)
            counter_safe = current + 1


def demo_lock_fixes_race_condition() -> None:
    global counter_safe
    counter_safe = 0
    times_per_thread = 500
    num_threads = 4

    threads = [threading.Thread(target=increment_safe, args=(times_per_thread,)) for _ in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    expected = times_per_thread * num_threads
    print(f"kỳ vọng counter_safe = {expected}, thực tế = {counter_safe}")
    print("-> với Lock, kết quả LUÔN đúng, đổi lại chậm hơn (mỗi increment phải acquire/release lock)")


def demo_thread_pool_executor() -> None:
    """ThreadPoolExecutor: cách idiomatic hơn để chạy nhiều thread -- tự
    quản lý số lượng thread (pool), không cần tự tạo/join từng Thread
    thủ công như các demo trên."""
    files = [("a.zip", 0.2), ("b.zip", 0.2), ("c.zip", 0.2), ("d.zip", 0.2)]

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda args: download_file(*args), files))
    elapsed = time.perf_counter() - start

    print(f"ThreadPoolExecutor (4 workers): {elapsed:.3f}s")
    for r in results:
        print(" ", r)


def main() -> None:
    demo_concurrent_downloads()

    print()
    demo_race_condition()

    print()
    demo_lock_fixes_race_condition()

    print()
    demo_thread_pool_executor()


if __name__ == "__main__":
    main()
