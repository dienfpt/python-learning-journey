# Phase 4 — FastAPI Core

Đây là mục tiêu chính của cả journey: build API production-ready bằng
FastAPI. Các phase trước (Core Python, DSA, Concurrency) đều là nền tảng
dẫn tới đây — đặc biệt Phase 3 (asyncio) gần như là điều kiện bắt buộc,
vì FastAPI dùng `async def` làm mô hình xử lý request mặc định.

## Vì sao FastAPI (so với Express/NestJS đã quen)?

- **Gần NestJS hơn Express**: FastAPI có DI (Dependency Injection) built-in
  qua `Depends`, tách route/schema/business logic rõ ràng — tư duy giống
  NestJS's decorator + DI hơn là Express's middleware chain tự do.
- **Validation là công dân hạng nhất**: Pydantic model định nghĩa
  request/response schema bằng type hint thuần Python — tương đương Zod/
  class-validator của Node, nhưng **tích hợp sẵn vào framework**, không
  cần cấu hình thêm middleware validation.
- **OpenAPI/Swagger tự sinh miễn phí**: route + Pydantic model tự động
  sinh ra `/docs` (Swagger UI) — không cần viết YAML/decorator riêng như
  `@nestjs/swagger`.
- **Type hint là spec, không chỉ là hint**: khác Phase 1 (nơi type
  annotation chỉ là gợi ý, không enforce runtime), ở FastAPI, Pydantic
  **enforce type hint thật sự tại runtime** để validate request — đây là
  lý do Phase 1 nhấn mạnh phải dùng type annotation nghiêm túc.

## Tiến độ

- [x] 1. FastAPI cơ bản — app đầu tiên, routing, path/query params
- [ ] 2. Pydantic Models — request/response validation & serialization
- [ ] 3. Dependency Injection (`Depends`) — so sánh NestJS DI
- [ ] 4. Error Handling — `HTTPException`, custom exception handler, status code
- [ ] 5. Middleware — CORS, custom middleware, request lifecycle
- [ ] 6. Async DB — SQLAlchemy 2.0 async, CRUD API hoàn chỉnh
- [ ] 7. Background Tasks & WebSocket
- [ ] 8. Testing FastAPI — `TestClient`, pytest-asyncio

## Cách chạy example ở phase này

Khác các phase trước (script chạy xong là kết thúc), FastAPI app thường
là **long-running server**. Để giữ đúng quy ước `def main()` chạy được
qua `run_examples.py` (không cần mở terminal thứ 2 để gõ `curl`), phần
lớn example ở đây dùng `fastapi.testclient.TestClient` — gọi thẳng vào
app trong cùng process, in ra kết quả, không cần khởi động server thật.
Đây cũng chính là cách viết **test** cho FastAPI trong thực tế (Phase
4.8). Mỗi file vẫn có `if __name__ == "__main__": uvicorn.run(...)` được
comment sẵn để chạy server thật + xem `/docs` khi muốn.

## 1. FastAPI cơ bản — App, Routing, Path/Query Params

- **Tạo app**: `app = FastAPI()` — tương đương `const app = express()`.
  Đăng ký route bằng decorator: `@app.get("/path")`, `@app.post(...)` —
  giống `app.get("/path", handler)` của Express nhưng dùng decorator thay
  vì truyền callback.
- **Path params — khác biệt lớn nhất với Express**: FastAPI lấy giá trị
  từ `{placeholder}` trong route và truyền **trực tiếp vào tham số hàm
  cùng tên**, dựa trên **type hint** để tự động convert + validate. Vd.
  `@app.get("/books/{book_id}")` + `def read_book(book_id: int)` — string
  `"42"` từ URL tự convert thành `int 42`; nếu không convert được (vd.
  `/books/abc`), FastAPI tự trả **422 Unprocessable Entity** kèm chi tiết
  lỗi — không cần code `parseInt()` + check `isNaN()` thủ công như
  `req.params.id` của Express.
- **Query params**: tham số hàm **không** xuất hiện trong path string được
  FastAPI tự hiểu là query param (`?key=value`). Có giá trị default (vd.
  `skip: int = 0`) → optional; không có default → **bắt buộc**, thiếu thì
  trả 422. Tương đương `req.query.skip` của Express nhưng khai báo tường
  minh qua type hint thay vì đọc object `req.query` không có type.
- **Response tự serialize**: return 1 `dict` (hoặc Pydantic model — mục 2)
  từ route handler, FastAPI tự động serialize thành JSON + set
  `Content-Type: application/json` — tương đương `res.json({...})` nhưng
  không cần gọi tường minh.
- **`/docs` tự sinh miễn phí**: chỉ cần chạy `uvicorn app:app --reload`
  rồi mở `http://127.0.0.1:8000/docs` — Swagger UI tương tác được sinh ra
  hoàn toàn từ route + type hint, không cần viết OpenAPI spec riêng.
- **Cách chạy example trong repo này**: dùng `TestClient` (dựa trên
  `httpx2` — bản mới của `httpx`, package cũ đã deprecated cho việc này)
  để gọi thẳng vào `app` trong cùng process, không cần mở server thật.
  Xem chi tiết ở phần "Cách chạy example ở phase này" phía trên.
