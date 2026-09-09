"""
Topic: asyncio nâng cao — Task, gather, timeout, cancellation
So sánh JS: `asyncio.gather()` ~ `Promise.all()`, `asyncio.create_task()`
~ gọi 1 async function mà không await ngay (JS tự "bắt đầu chạy" Promise
khi tạo, giống create_task của Python schedule coroutine chạy trong
background). `asyncio.wait_for()` ~ dùng `Promise.race()` với 1 timeout
promise. Cancellation là điểm khác biệt lớn nhất: JS Promise KHÔNG có
cách hủy chuẩn (phải tự cài AbortController), còn Python Task có
`.cancel()` built-in, throw `CancelledError` vào đúng điểm đang await.
"""

import asyncio
import time


async def fetch_data(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"data từ {name}"


async def demo_gather_runs_concurrently() -> None:
    """asyncio.gather() chạy nhiều coroutine ĐỒNG THỜI, không tuần tự như
    await thường (xem lại file 04) -- tổng thời gian ~= tác vụ chậm nhất,
    giống Promise.all() của JS."""
    start = time.perf_counter()
    results = await asyncio.gather(
        fetch_data("API_A", 0.2),
        fetch_data("API_B", 0.3),
        fetch_data("API_C", 0.1),
    )
    elapsed = time.perf_counter() - start
    print(f"gather() 3 coroutine (0.2s, 0.3s, 0.1s): {elapsed:.3f}s (~0.3s, KHÔNG cộng dồn)")
    print("kết quả:", results)


async def demo_create_task() -> None:
    """create_task() lên lịch coroutine chạy NGAY trong background (khác
    gọi thường chỉ tạo coroutine object chưa chạy) -- cho phép làm việc
    khác trong lúc nó chạy, rồi await kết quả khi cần."""
    task = asyncio.create_task(fetch_data("background_job", 0.3))

    print("task đã được schedule, làm việc khác trong lúc chờ...")
    await asyncio.sleep(0.1)
    print("vẫn đang làm việc khác... (task chạy song song ở background)")

    result = await task  # chờ tới khi task xong, lấy kết quả
    print("task hoàn thành:", result)


async def demo_timeout() -> None:
    """asyncio.timeout() (Python 3.11+) -- hủy coroutine nếu chạy quá lâu.
    Với Python < 3.11, dùng asyncio.wait_for(coro, timeout=...) tương đương."""
    try:
        async with asyncio.timeout(0.15):
            result = await fetch_data("slow_api", 0.5)
            print("kết quả:", result)
    except TimeoutError:
        print("slow_api quá 0.15s -> TimeoutError, coroutine bị hủy tự động")


async def demo_cancellation() -> None:
    """Task.cancel() ném CancelledError vào ĐÚNG điểm task đang await --
    khác JS không có cơ chế hủy Promise chuẩn (phải tự AbortController)."""
    task = asyncio.create_task(fetch_data("cancelable_job", 1.0))

    await asyncio.sleep(0.1)  # để task chạy 1 chút rồi mới hủy
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("task đã bị cancel() thành công trước khi hoàn thành")


async def demo_gather_with_exceptions() -> None:
    """Mặc định, 1 coroutine lỗi trong gather() sẽ làm cả gather() raise
    exception ngay lập tức. return_exceptions=True giữ tất cả kết quả
    (kể cả exception) thay vì dừng sớm -- hữu ích khi cần biết task nào
    lỗi mà không muốn hủy các task khác đang chạy."""
    async def maybe_fail(name: str, should_fail: bool) -> str:
        await asyncio.sleep(0.1)
        if should_fail:
            raise ValueError(f"{name} thất bại")
        return f"{name} thành công"

    results = await asyncio.gather(
        maybe_fail("task1", False),
        maybe_fail("task2", True),
        maybe_fail("task3", False),
        return_exceptions=True,
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"  lỗi: {r}")
        else:
            print(f"  ok: {r}")


async def _async_main() -> None:
    await demo_gather_runs_concurrently()
    print()
    await demo_create_task()
    print()
    await demo_timeout()
    print()
    await demo_cancellation()
    print()
    await demo_gather_with_exceptions()


def main() -> None:
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
