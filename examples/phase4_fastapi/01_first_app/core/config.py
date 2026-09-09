"""
Config tách riêng khỏi route logic -- best practice chuẩn của FastAPI
project (giống tách `config/` riêng trong NestJS/Express thay vì hardcode
port/title rải rác trong code). Ở mức đơn giản này dùng constant thường;
từ Phase 4.2 (Pydantic Models) trở đi, Settings phức tạp hơn (đọc từ
biến môi trường/.env) nên dùng `pydantic-settings` (BaseSettings) thay vì
class/constant tay như ở đây.
"""

APP_TITLE = "Bookstore API"
HOST = "127.0.0.1"
PORT = 8001
