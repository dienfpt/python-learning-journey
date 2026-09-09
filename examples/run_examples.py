"""
Runner tự động cho các example trong project.

Thiết kế để MỞ RỘNG không cần sửa file này: thêm 1 file .py mới vào
examples/phaseX_xxx/ (có def main()) là runner tự động nhận diện và chạy
được. Từ Phase 4 (FastAPI) trở đi, mỗi topic là 1 FOLDER riêng
(examples/phase4_fastapi/01_first_app/, theo best-practice structure của
1 FastAPI project) thay vì 1 file .py phẳng -- runner nhận diện topic
dạng này qua file `run_demo.py` bên trong folder đó.

Cách dùng:
    python examples/run_examples.py                          # list tất cả phase
    python examples/run_examples.py phase1_basics             # chạy cả phase, dừng chờ Enter giữa từng file
    python examples/run_examples.py phase1_basics 07_data_structures  # chạy 1 file
    python examples/run_examples.py phase4_fastapi 01_first_app        # chạy 1 topic folder (run_demo.py)
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).parent


def discover_phases() -> list[Path]:
    return sorted(
        p for p in EXAMPLES_DIR.iterdir()
        if p.is_dir() and p.name.startswith("phase")
    )


def _sort_key(f: Path) -> str:
    # File phẳng (01_x.py) sort theo tên file; topic dạng folder
    # (01_x/run_demo.py) sort theo tên FOLDER để giữ đúng thứ tự topic.
    return f.parent.name if f.name == "run_demo.py" else f.stem


def discover_examples(phase_dir: Path) -> list[Path]:
    flat_files = [
        f for f in phase_dir.glob("*.py")
        if f.name != "__init__.py"
    ]
    nested_demos = list(phase_dir.glob("*/run_demo.py"))
    return sorted(flat_files + nested_demos, key=_sort_key)


def run_file(file_path: Path) -> None:
    """Load 1 file .py bằng đường dẫn (import bình thường không chạy được
    vì tên file bắt đầu bằng số, VD 01_basic_syntax.py không phải identifier
    hợp lệ để `import`)."""
    spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None

    # Đăng ký vào sys.modules + thêm thư mục chứa file vào sys.path: cần
    # thiết để (1) multiprocessing (spawn) re-import được module này trong
    # process con (xem phase3_concurrency/03_multiprocessing.py), và (2)
    # để 1 topic dạng folder (phase4_fastapi/01_first_app/run_demo.py) có
    # thể `import main`/`from routers.books import router` bằng tên module
    # phẳng thay vì package import thật (vì "01_first_app" bắt đầu bằng
    # số, không phải identifier hợp lệ để làm tên package). Phải giữ
    # nguyên cho tới hết module.main(), không chỉ lúc exec_module.
    parent_dir = str(file_path.parent)
    sys.modules[file_path.stem] = module
    sys.path.insert(0, parent_dir)
    modules_before = set(sys.modules)
    try:
        spec.loader.exec_module(module)

        if hasattr(module, "main"):
            print(f"\n{'=' * 60}")
            print(f"▶ {file_path.relative_to(EXAMPLES_DIR)}")
            print("=" * 60)
            module.main()
    finally:
        sys.path.remove(parent_dir)

        # Dọn sys.modules: CHỈ xoá module được load TỪ TRONG folder này
        # (vd. "main", "routers.books", "schemas" của topic hiện tại) --
        # không đụng tới thư viện thứ 3 (fastapi, uvicorn...) lỡ được
        # import lần đầu trong lúc chạy. Cần thiết vì các topic khác nhau
        # dùng chung tên module phẳng ("main.py", "schemas.py"...) -- nếu
        # không dọn, topic sau sẽ nhận nhầm module đã cache của topic
        # trước khi chạy cả phase liên tiếp qua run_files_one_by_one().
        for name in set(sys.modules) - modules_before:
            origin = getattr(getattr(sys.modules[name], "__spec__", None), "origin", None)
            if origin and origin.startswith(parent_dir):
                del sys.modules[name]
        sys.modules.pop(file_path.stem, None)


def run_files_one_by_one(files: list[Path]) -> None:
    """Chạy từng file, dừng lại chờ Enter trước khi qua file kế tiếp — để
    đọc kỹ output từng phần thay vì bị trôi hết ra màn hình cùng lúc."""
    for i, f in enumerate(files):
        run_file(f)
        if i < len(files) - 1:
            choice = input("\n... Nhấn Enter để chạy tiếp ('q' để dừng) ...")
            if choice.strip().lower() == "q":
                break


def _matches(f: Path, file_stem: str) -> bool:
    if f.name == "run_demo.py":
        return f.parent.name == file_stem or f.parent.name.endswith(file_stem)
    return f.stem == file_stem or f.stem.endswith(file_stem)


def main() -> None:
    args = sys.argv[1:]
    phases = discover_phases()

    if not args:
        print("Các phase hiện có:")
        for p in phases:
            n_files = len(discover_examples(p))
            print(f"  - {p.name} ({n_files} example files)")
        print("\nDùng: python examples/run_examples.py <phase_name> [file_stem]")
        return

    phase_name = args[0]
    phase_dir = EXAMPLES_DIR / phase_name

    if not phase_dir.exists():
        print(f"Không tìm thấy phase '{phase_name}'. Có: {[p.name for p in phases]}")
        return

    examples = discover_examples(phase_dir)

    if len(args) >= 2:
        file_stem = args[1]
        matched = [f for f in examples if _matches(f, file_stem)]
        if not matched:
            print(f"Không tìm thấy file '{file_stem}' trong {phase_name}")
            return
        run_files_one_by_one(matched)
    else:
        run_files_one_by_one(examples)


if __name__ == "__main__":
    main()
