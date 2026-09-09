"""
Topic: Type Annotations
So sánh JS/TS: giống TypeScript về Y TUONG, nhưng optional & KHÔNG
compile-time check mặc định -- chỉ là hint, cần mypy/Pydantic để enforce.

QUAN TRỌNG NHẤT trong toàn bộ Phase 1 cho mục tiêu FastAPI: Pydantic dùng
type hint để validate request/response và tự generate docs (OpenAPI).
Dù Python "cho phép" bỏ type hint, với FastAPI phải dùng nghiêm túc như TS.
"""

from typing import Optional, Union


def add(a: int, b: int) -> int:
    return a + b


def find_user(user_id: int) -> Optional[dict]:
    """Optional[dict] ~ dict | None -- hàm có thể trả None."""
    fake_db = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    return fake_db.get(user_id)


def parse_id(value: Union[int, str]) -> int:
    """Union[int, str] ~ TS union type `number | string`."""
    return int(value)


def demo_collection_hints() -> None:
    scores: list[int] = [90, 85, 70]
    user: dict[str, str] = {"name": "Alice", "role": "admin"}
    print("scores:", scores)
    print("user:", user)


def demo_type_hint_is_not_enforced() -> None:
    """
    Python KHÔNG chặn runtime nếu truyền sai type -- khác TS compile-time.
    Đây là lý do FastAPI/Pydantic tồn tại: enforce validation THẬT SỰ tại
    runtime dựa trên type hint.
    """
    result = add("5", "10")  # type: ignore -- Python vẫn chạy được (string concat)
    print("add('5', '10') chạy được (không lỗi type):", result)


def main() -> None:
    print("add(2, 3):", add(2, 3))
    print("find_user(1):", find_user(1))
    print("find_user(99):", find_user(99))
    print("parse_id('42'):", parse_id("42"))
    demo_collection_hints()
    demo_type_hint_is_not_enforced()


if __name__ == "__main__":
    main()
