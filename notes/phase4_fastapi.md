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

## Cấu trúc mỗi topic — best-practice FastAPI project layout

Khác các phase trước (1 file .py phẳng = 1 concept), mỗi topic ở Phase 4
là **1 folder riêng** trong `examples/phase4_fastapi/`, theo cấu trúc
chuẩn của 1 FastAPI project thực tế thay vì gộp hết vào 1 file:

```
01_first_app/
├── __init__.py
├── core/
│   └── config.py       # cấu hình app (host/port/title...)
├── routers/
│   └── books.py        # APIRouter theo từng resource (giống Controller NestJS)
├── schemas.py           # Pydantic/TypedDict models cho request/response
├── dependencies.py       # dependency dùng chung qua Depends() (Phase 4.3+)
├── main.py               # entry point: tạo FastAPI(), include_router()
└── run_demo.py           # chạy demo — xem bên dưới
```

Cấu trúc này được tạo **đầy đủ ngay từ topic 1**, kể cả file gần như rỗng
(`dependencies.py` chưa dùng tới Phase 4.3) — để mọi topic sau chỉ cần
**thêm nội dung** vào đúng file có sẵn, không phải đảo lại layout giữa
chừng.

## Cách chạy example ở phase này — server thật, không phải TestClient

Khác các phase trước (script chạy xong là kết thúc), FastAPI app thường
là **long-running server**. Mỗi topic có `run_demo.py`: khởi động
**uvicorn thật** (bind cổng TCP thật trên `127.0.0.1`) trong 1 background
thread, đợi tới khi server sẵn sàng, rồi gọi bằng `httpx2.Client` **qua
network thật** (không phải `TestClient` gọi thẳng vào app qua ASGI
transport ảo trong cùng process) — gần với việc tự chạy `uvicorn` rồi
`curl` thủ công, nhưng vẫn tự động hoá được để chạy qua `run_examples.py`
(runner tự nhận diện `run_demo.py` bên trong mỗi topic folder). Server
được tắt sạch sẽ sau khi demo xong.

Muốn tự chạy server + xem `/docs` (Swagger UI) thủ công:

```bash
uvicorn main:app --reload --app-dir examples/phase4_fastapi/01_first_app --port 8001
# rồi mở http://127.0.0.1:8001/docs
```

`TestClient` (dựa trên `httpx2`) vẫn là công cụ chuẩn để viết **test**
thật sự cho FastAPI — sẽ quay lại dùng nó ở Phase 4.8 (Testing).

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
- **Tách router riêng (`routers/books.py`)**: các route liên quan tới 1
  resource (`books`) được gom vào 1 `APIRouter` riêng, `main.py` chỉ
  `include_router()` — giống tách `express.Router()` theo resource hoặc
  Controller riêng trong NestJS, thay vì định nghĩa hết route trong 1 file
  duy nhất.
- **Cách chạy example trong repo này**: `run_demo.py` khởi động **uvicorn
  thật** (không phải `TestClient`) rồi gọi bằng `httpx2.Client` qua network
  thật. Xem chi tiết ở phần "Cách chạy example ở phase này" phía trên.
