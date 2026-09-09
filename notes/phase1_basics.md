# Phase 1 — Python Core Differences (JS → Python)

## 1. Basic Syntax
- Indentation là cú pháp bắt buộc (không phải style convention như Prettier).
- Không dùng `;`, không dùng `{}` cho block.
- **Không có block scope** cho `if`/`for`/`while` — biến khai báo trong đó vẫn
  tồn tại ngoài block (khác `let`/`const` trong JS). Chỉ có function scope.

## 2. Variables & Data Types
- Dynamic typing nhưng **strong typing**: `"5" + 3` → `TypeError`, không tự
  ép kiểu ngầm như JS.
- Không có `undefined`, chỉ có `None`.
- Không có `const` thật; convention: `UPPER_CASE = value`.
- Types cơ bản: `int`, `float`, `str`, `bool`, `list`, `tuple`, `dict`, `set`.

## 3. Operators
- `//` floor division, `**` lũy thừa.
- Không có `===`; Python `==` đã strict theo type/value, không ép kiểu như
  `==` của JS.
- `is` so sánh **identity** (reference), không phải value — lỗi phổ biến khi
  người mới dùng `is` thay `==`.
- `and`/`or`/`not` thay cho `&&`/`||`/`!`.

## 4. Strings
- f-string thay template literal: `f"Hello, {name}"`.
- `"-".join(list)` — separator gọi method, **ngược** với JS `array.join("-")`.
- Slicing: `s[1:4]`, `s[::-1]` (reverse).
- Multiline: `"""..."""`.

## 5. Conditionals
- `elif` thay `else if`.
- Không có ternary `?:`, thay bằng: `x if condition else y`.
- Không có `switch` cổ điển; Python 3.10+ có `match-case`.
- Truthy/falsy: `0`, `""`, `[]`, `{}`, `None` đều falsy — **khác JS**, nơi
  `[]`/`{}` là truthy.

## 6. Loops
- `for i in range(n)` thay classic C-style for loop.
- `for item in list` giống `for...of`.
- `for k, v in dict.items()` giống `Object.entries()`.
- Loop có `else` (chạy khi không bị `break`) — Python-only, JS không có.

## 7. Lists / Tuples / Sets
- `list` ~ Array (mutable).
- `tuple` **không có tương đương trong JS** — immutable, dùng khi cần dữ liệu
  cố định hoặc return nhiều giá trị.
- `set` ~ Set nhưng có toán tử tập hợp: `|` `&` `-` `^`.
- List comprehension là idiom chuẩn, không có cú pháp tương đương gọn trong JS:
  `[x**2 for x in range(10) if x % 2 == 0]`.

## 8. Dictionaries
- `dict` ~ Object/Map. Key phải hashable (immutable).
- `.get(key, default)` tránh KeyError, giống optional chaining + default.
- Dict comprehension: `{x: x**2 for x in range(5)}`.

## 9. Type Casting
- Explicit: `int()`, `float()`, `str()`, `list()`, `bool()`.
- Cast lỗi → `ValueError` rõ ràng, không âm thầm trả `NaN` như JS.

## 10. Functions
- Default params giống JS: `def f(a, b=10)`.
- `*args` (positional) và `**kwargs` (keyword) — tách biệt rõ ràng, khác
  `...rest` gộp chung của JS.
- Lambda giới hạn 1 expression duy nhất, không như arrow function multiline.

## 11. Exceptions
- `try/except/else/finally` thay `try/catch/finally`.
- Exception hierarchy chi tiết: `ZeroDivisionError`, `KeyError`,
  `IndexError`, `TypeError`... → nên bắt cụ thể, không bắt chung chung.
- `raise ValueError("message")` thay `throw new Error()`.

## 12. Type Annotations
- Giống TypeScript về ý tưởng, nhưng **optional & không compile-time check**
  mặc định — chỉ là hint, cần `mypy`/Pydantic để enforce thật sự.
- **Cực kỳ quan trọng cho FastAPI**: Pydantic dùng type hint để validate
  request/response và generate docs tự động → phải dùng nghiêm túc như TS.

```python
def add(a: int, b: int) -> int:
    return a + b

from typing import Optional
def find_user(id: int) -> Optional[dict]:
    ...
```
