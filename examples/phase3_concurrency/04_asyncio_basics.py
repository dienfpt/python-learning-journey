"""
Topic: asyncio cơ bản — Event Loop, async/await, Coroutine
So sánh JS: cú pháp `async`/`await` gần như giống hệt JS -- đây là phần dễ
chuyển đổi nhất. Khác biệt quan trọng: JS luôn có sẵn 1 event loop chạy
ngầm ngay khi script bắt đầu (runtime tự quản lý), còn Python cần khởi
động event loop TƯỜNG MINH bằng `asyncio.run()` -- gọi trực tiếp 1 hàm
`async def` chỉ tạo ra 1 coroutine object (chưa chạy gì cả), phải
`await` hoặc đưa vào event loop mới thực sự thực thi. Đây là lỗi phổ biến
nhất của người mới: quên `await` và ngạc nhiên vì code "không chạy".
"""

import asyncio
import time


async def say_hello(name: str, delay: float) -> str:
    """`async def` định nghĩa 1 coroutine function -- GỌI hàm này không
    chạy code bên trong ngay, chỉ tạo ra 1 coroutine object (giống Promise
    "chưa resolve" của JS). Phải await/chạy trong event loop mới thực thi."""
    await asyncio.sleep(delay)  # non-blocking "chờ" -- khác time.sleep() blocking
    return f"Hello, {name}!"


def demo_calling_without_await() -> None:
    """Lỗi kinh điển: gọi async function mà không await -- chỉ tạo ra
    coroutine object, KHÔNG chạy code bên trong (Python sẽ cảnh báo
    "coroutine was never awaited")."""
    result = say_hello("Alice", 0.1)
    print("gọi say_hello() không await, kết quả là:", result, f"({type(result).__name__})")
    print("-> chưa in ra 'Hello, Alice!' vì coroutine chưa được chạy")


async def demo_await_runs_it() -> None:
    """await coroutine mới thực sự chạy nó và lấy giá trị return."""
    result = await say_hello("Bob", 0.1)
    print("await say_hello():", result)


async def demo_sequential_await() -> None:
    """QUAN TRỌNG: await tuần tự (1 cái xong mới tới cái tiếp theo) KHÔNG
    tạo ra concurrency -- tổng thời gian vẫn CỘNG DỒN, giống gọi hàm sync
    bình thường. Đây là hiểu lầm phổ biến: cứ dùng async/await là tự động
    nhanh hơn -- SAI, cần asyncio.gather()/Task (xem file 05) mới thực sự
    chạy đồng thời."""
    start = time.perf_counter()
    await say_hello("Alice", 0.2)
    await say_hello("Bob", 0.2)
    await say_hello("Claire", 0.2)
    elapsed = time.perf_counter() - start
    print(f"await tuần tự 3 coroutine (mỗi cái 0.2s): {elapsed:.3f}s (~0.6s, KHÔNG nhanh hơn sync)")


async def _async_main() -> None:
    demo_calling_without_await()

    print()
    await demo_await_runs_it()

    print()
    await demo_sequential_await()


def main() -> None:
    # asyncio.run() là "entry point" tường minh cần thiết -- tạo event
    # loop mới, chạy coroutine tới khi xong, rồi đóng event loop lại.
    # Khác Node.js: event loop đã chạy sẵn, không cần dòng khởi động nào.
    # main() ở đây vẫn là hàm sync để khớp quy ước run_examples.py
    # (gọi module.main() trực tiếp, không await).
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
