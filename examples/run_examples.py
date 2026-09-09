"""
Runner tự động cho các example trong project.

Thiết kế để MỞ RỘNG không cần sửa file này: thêm 1 file .py mới vào
examples/phaseX_xxx/ (có def main()) là runner tự động nhận diện và chạy được.

Cách dùng:
    python examples/run_examples.py                          # list tất cả phase
    python examples/run_examples.py phase1_basics             # chạy cả phase, dừng chờ Enter giữa từng file
    python examples/run_examples.py phase1_basics 07_data_structures  # chạy 1 file
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


def discover_examples(phase_dir: Path) -> list[Path]:
    return sorted(
        f for f in phase_dir.glob("*.py")
        if f.name != "__init__.py"
    )


def run_file(file_path: Path) -> None:
    """Load 1 file .py bằng đường dẫn (import bình thường không chạy được
    vì tên file bắt đầu bằng số, VD 01_basic_syntax.py không phải identifier
    hợp lệ để `import`)."""
    spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None

    # Đăng ký vào sys.modules + thêm thư mục chứa file vào sys.path: cần
    # thiết để multiprocessing (spawn) re-import được module này trong
    # process con bằng đúng tên file_path.stem (xem phase3_concurrency/
    # 03_multiprocessing.py) -- nếu không, pickle function bên trong module
    # sẽ báo lỗi "import of module '<tên file>' failed". Phải giữ nguyên
    # cho tới hết module.main() (không chỉ lúc exec_module) vì spawn có
    # thể xảy ra bất cứ lúc nào trong quá trình chạy main().
    sys.modules[file_path.stem] = module
    sys.path.insert(0, str(file_path.parent))
    try:
        spec.loader.exec_module(module)

        if hasattr(module, "main"):
            print(f"\n{'=' * 60}")
            print(f"▶ {file_path.relative_to(EXAMPLES_DIR)}")
            print("=" * 60)
            module.main()
    finally:
        sys.path.remove(str(file_path.parent))
        del sys.modules[file_path.stem]


def run_files_one_by_one(files: list[Path]) -> None:
    """Chạy từng file, dừng lại chờ Enter trước khi qua file kế tiếp — để
    đọc kỹ output từng phần thay vì bị trôi hết ra màn hình cùng lúc."""
    for i, f in enumerate(files):
        run_file(f)
        if i < len(files) - 1:
            choice = input("\n... Nhấn Enter để chạy tiếp ('q' để dừng) ...")
            if choice.strip().lower() == "q":
                break


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
        matched = [f for f in examples if f.stem == file_stem or f.stem.endswith(file_stem)]
        if not matched:
            print(f"Không tìm thấy file '{file_stem}' trong {phase_name}")
            return
        run_files_one_by_one(matched)
    else:
        run_files_one_by_one(examples)


if __name__ == "__main__":
    main()
