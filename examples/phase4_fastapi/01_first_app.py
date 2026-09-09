"""
Topic: FastAPI cơ bản — App đầu tiên, Routing, Path/Query Params
So sánh JS (Express): Express dùng `app.get('/items/:id', (req, res) => {
req.params.id })` -- lấy param thủ công từ `req`, tự parse/validate. FastAPI
lấy path/query param TRỰC TIẾP làm THAM SỐ HÀM, dựa vào TÊN THAM SỐ khớp
với `{placeholder}` trong route + TYPE HINT để tự động parse & validate
(vd. `item_id: int` tự convert string "42" -> int 42, tự trả 422 nếu
không convert được) -- không cần đọc `req.params`/`req.query` thủ công.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(title="Bookstore API")


@app.get("/")
def read_root() -> dict:
    """Route đơn giản nhất -- không param, trả về dict (FastAPI tự
    serialize thành JSON, tương đương res.json({...}) của Express)."""
    return {"message": "Welcome to the Bookstore API"}


@app.get("/books/{book_id}")
def read_book(book_id: int) -> dict:
    """Path param: {book_id} trong route khớp với tên tham số `book_id`
    của hàm. Type hint `int` khiến FastAPI TỰ ĐỘNG convert string từ URL
    sang int, và trả lỗi 422 nếu không convert được (vd. /books/abc) --
    không cần `parseInt(req.params.id)` + tự check `isNaN` như Express."""
    return {"book_id": book_id, "type": type(book_id).__name__}


@app.get("/books")
def list_books(skip: int = 0, limit: int = 10, genre: str | None = None) -> dict:
    """Query param: tham số KHÔNG xuất hiện trong path -> FastAPI tự hiểu
    là query param (?skip=5&limit=20). Có default value -> optional,
    giống `req.query.skip || 0` của Express nhưng khai báo tường minh qua
    type hint + default, không cần parse thủ công."""
    return {"skip": skip, "limit": limit, "genre": genre}


def demo_routes() -> None:
    """TestClient gọi thẳng vào `app` trong cùng process -- không cần
    server thật đang chạy. Đây cũng là cách viết test cho FastAPI (Phase
    4.8) -- dùng ngay từ đầu ở đây để example chạy được qua run_examples.py."""
    client = TestClient(app)

    response = client.get("/")
    print("GET /:", response.status_code, response.json())

    response = client.get("/books/42")
    print("GET /books/42:", response.status_code, response.json())

    response = client.get("/books/abc")  # không convert được sang int
    print("GET /books/abc (invalid type):", response.status_code)
    print("  detail:", response.json()["detail"])

    response = client.get("/books?skip=5&limit=20&genre=sci-fi")
    print("GET /books?skip=5&limit=20&genre=sci-fi:", response.status_code, response.json())

    response = client.get("/books")  # dùng default values
    print("GET /books (defaults):", response.status_code, response.json())


def main() -> None:
    demo_routes()
    print()
    print("Chạy server thật để xem Swagger UI tự sinh:")
    print("  uvicorn examples.phase4_fastapi.01_first_app:app --reload")
    print("  rồi mở http://127.0.0.1:8000/docs")


if __name__ == "__main__":
    main()

    # Bỏ comment để chạy server thật thay vì chỉ demo qua TestClient:
    # import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8000)
