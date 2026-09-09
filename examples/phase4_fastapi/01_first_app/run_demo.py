"""
Chạy server FastAPI THẬT (uvicorn, bind cổng TCP thật trên 127.0.0.1) rồi
gọi bằng httpx2.Client thật qua network -- khác `TestClient` (gọi thẳng
vào app trong cùng process qua ASGI transport ảo, không đi qua TCP/HTTP
thật). Cách này gần với việc tự chạy `uvicorn` rồi `curl` thủ công hơn,
nhưng vẫn tự động hoá được để chạy qua run_examples.py: khởi động server
trong 1 background thread, đợi tới khi bind port xong, gọi request, rồi
tắt server sạch sẽ trước khi return.
"""

import threading
import time

import httpx2
import uvicorn

from core.config import HOST, PORT
from main import app


def _start_server() -> tuple[uvicorn.Server, threading.Thread]:
    config = uvicorn.Config(app, host=HOST, port=PORT, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    while not server.started:  # chờ tới khi server thật sự bind port xong
        time.sleep(0.01)

    return server, thread


def _stop_server(server: uvicorn.Server, thread: threading.Thread) -> None:
    server.should_exit = True
    thread.join(timeout=5)


def demo_real_requests() -> None:
    with httpx2.Client(base_url=f"http://{HOST}:{PORT}") as client:
        response = client.get("/")
        print("GET /:", response.status_code, response.json())

        response = client.get("/books/42")
        print("GET /books/42:", response.status_code, response.json())

        response = client.get("/books/abc")  # không convert được sang int
        print("GET /books/abc (invalid type):", response.status_code)
        print("  detail:", response.json()["detail"])

        response = client.get("/books", params={"skip": 5, "limit": 20, "genre": "sci-fi"})
        print("GET /books?skip=5&limit=20&genre=sci-fi:", response.status_code, response.json())

        response = client.get("/books")  # dùng default values
        print("GET /books (defaults):", response.status_code, response.json())


def main() -> None:
    print(f"khởi động uvicorn thật tại http://{HOST}:{PORT} ...")
    server, thread = _start_server()
    try:
        demo_real_requests()
    finally:
        print("đóng server...")
        _stop_server(server, thread)

    print()
    print("Muốn tự chạy server + xem Swagger UI:")
    print(f"  uvicorn main:app --reload --app-dir examples/phase4_fastapi/01_first_app --port {PORT}")
    print(f"  rồi mở http://{HOST}:{PORT}/docs")


if __name__ == "__main__":
    main()
