"""
Topic: FastAPI cơ bản — App, Routing, Path/Query Params
So sánh JS (Express): Express dùng `app.get('/items/:id', (req, res) => {
req.params.id })` -- lấy param thủ công từ `req`, tự parse/validate. Xem
routers/books.py để thấy FastAPI lấy path/query param TRỰC TIẾP làm
THAM SỐ HÀM, dựa vào type hint để tự động parse & validate.

File này chỉ là "entry point" -- ráp app + gắn router, giống main.py/
app.js chỉ gọi `app.use('/books', booksRouter)` chứ không tự viết route
handler trực tiếp trong đó (best practice tách route logic ra router
riêng, xem routers/books.py).
"""

from fastapi import FastAPI

from core.config import APP_TITLE
from routers.books import router as books_router
from schemas import RootMessage

app = FastAPI(title=APP_TITLE)
app.include_router(books_router)


@app.get("/")
def read_root() -> RootMessage:
    return {"message": "Welcome to the Bookstore API"}
