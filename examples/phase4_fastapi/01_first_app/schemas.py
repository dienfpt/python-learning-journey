"""
Response shapes cho topic này -- dùng `TypedDict` thay vì Pydantic
`BaseModel` vì BaseModel mới được giới thiệu ở Phase 4.2. TypedDict là
bước đệm hữu ích để so sánh trực tiếp: TypedDict khai báo shape bằng type
hint (giống Pydantic) nhưng KHÔNG có runtime validation -- return sai
type vẫn chạy được, không raise lỗi như Pydantic sẽ làm ở Phase 4.2.
"""

from typing import TypedDict


class RootMessage(TypedDict):
    message: str


class BookOut(TypedDict):
    book_id: int
    type: str


class BookListOut(TypedDict):
    skip: int
    limit: int
    genre: str | None
