# Python Learning Journey — JS Dev → Python/FastAPI

Project dùng xuyên suốt quá trình học Python, dựa trên roadmap.sh/python,
custom cho developer đã có 10 năm kinh nghiệm JS/Fullstack, mục tiêu cuối:
FastAPI production-ready, tối ưu performance.

## Cấu trúc project

```
python-learning-journey/
├── notes/                      # Ghi chú lý thuyết, so sánh JS <-> Python
│   ├── phase1_basics.md
│   ├── phase2_data_structures_algorithms.md
│   ├── phase3_concurrency.md
│   ├── phase4_fastapi.md
│   ├── phase5_performance.md
│   └── phase6_testing_deployment.md
│
├── examples/                   # Code chạy được, 1 file = 1 concept
│   ├── run_examples.py         # Runner: chạy toàn bộ hoặc 1 phase/1 file
│   ├── phase1_basics/
│   ├── phase2_data_structures_algorithms/
│   ├── phase3_concurrency/
│   ├── phase4_fastapi/
│   ├── phase5_performance/
│   └── phase6_testing_deployment/
│
├── pyproject.toml
└── .gitignore
```

Nguyên tắc thiết kế để **mở rộng dễ dàng**:
- Mỗi phase trong roadmap = 1 folder riêng trong `notes/` và `examples/`
- Mỗi file example độc lập, có `def main():` để chạy demo, và docstring
  giải thích + so sánh JS ở đầu file
- `run_examples.py` tự động discover và chạy mọi file trong 1 phase — thêm
  file mới vào folder là chạy được ngay, không cần sửa runner

## Cách dùng

```bash
# Cài môi trường (khuyên dùng uv, nhanh hơn pip/venv truyền thống)
cd python-learning-journey
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .

# Chạy toàn bộ example của 1 phase
python examples/run_examples.py phase1_basics

# Chạy 1 file cụ thể
python examples/run_examples.py phase1_basics 07_data_structures

# Chạy trực tiếp 1 file (mỗi file tự chạy được luôn)
python examples/phase1_basics/07_data_structures.py
```

## Roadmap tracking

- [x] **Phase 1 — Python Core Differences**: syntax, data types, operators,
      strings, conditionals, loops, list/tuple/set/dict, type casting,
      functions, exceptions, comments, type annotations
- [x] **Phase 2 — Data Structures & Algorithms**: Big-O, arrays, linked
      lists, stacks, queues, hash tables, recursion, sorting, searching,
      trees, graphs
- [x] **Phase 3 — Concurrency & Async**: GIL, threading, multiprocessing,
      asyncio, choosing the right model
- [ ] **Phase 4 — FastAPI Core**: Pydantic v2, dependency injection, async DB
- [ ] **Phase 5 — Performance Optimization**: ASGI servers, profiling,
      caching, serialization
- [ ] **Phase 6 — Testing & Deployment**: pytest, Docker, observability

## Cách thêm 1 phase/topic mới

1. Tạo note: `notes/phaseX_ten_phase.md`
2. Tạo folder: `examples/phaseX_ten_phase/`
3. Thêm file `.py` trong đó, theo template:

```python
"""
Topic: <tên concept>
So sánh JS: <điểm khác biệt chính với JS/Node>
"""

def main():
    # code demo ở đây
    pass

if __name__ == "__main__":
    main()
```

4. Chạy `python examples/run_examples.py phaseX_ten_phase` để verify.
