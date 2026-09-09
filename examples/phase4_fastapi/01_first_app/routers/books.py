"""
APIRouter tách riêng route liên quan tới "books" khỏi main.py -- giống
tách `express.Router()` riêng theo resource, hoặc Controller riêng trong
NestJS. main.py gắn router này vào app chính bằng `include_router()`.
"""

from fastapi import APIRouter

from schemas import BookListOut, BookOut

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/{book_id}")
def read_book(book_id: int) -> BookOut:
    """Path param: {book_id} khớp tên tham số `book_id` của hàm. Type
    hint `int` khiến FastAPI TỰ ĐỘNG convert string từ URL sang int, và
    trả lỗi 422 nếu không convert được (vd. /books/abc) -- không cần
    `parseInt(req.params.id)` + tự check `isNaN` như Express."""
    return {"book_id": book_id, "type": type(book_id).__name__}


@router.get("")
def list_books(skip: int = 0, limit: int = 10, genre: str | None = None) -> BookListOut:
    """Query param: tham số KHÔNG xuất hiện trong path -> FastAPI tự
    hiểu là query param (?skip=5&limit=20). Có default value -> optional,
    giống `req.query.skip || 0` của Express nhưng khai báo tường minh
    qua type hint + default, không cần parse thủ công."""
    return {"skip": skip, "limit": limit, "genre": genre}
