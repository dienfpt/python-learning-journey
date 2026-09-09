"""
Topic: Hash Tables
So sánh JS: Python dict ~ JS Map/Object — cả hai đều là hash table với
lookup O(1) trung bình. Khác biệt: Python dict yêu cầu key phải "hashable"
(immutable) — không thể dùng list làm key (giống JS không cho object literal
làm key của Map theo value, chỉ theo reference). Từ Python 3.7+, dict giữ
thứ tự insertion (giống Map của JS), khác hẳn thời trước đó (unordered).
"""

from collections import Counter


class SimpleHashTable:
    """Tự implement hash table với separate chaining để thấy cơ chế bên
    trong dict thật (CPython dùng open addressing, nhưng chaining dễ hình
    dung hơn và cùng chung nguyên lý: hash(key) -> bucket index)."""

    def __init__(self, num_buckets: int = 8) -> None:
        self.num_buckets = num_buckets
        self.buckets: list[list[tuple[str, object]]] = [[] for _ in range(num_buckets)]

    def _bucket_index(self, key: str) -> int:
        return hash(key) % self.num_buckets

    def set(self, key: str, value: object) -> None:
        bucket = self.buckets[self._bucket_index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # update
                return
        bucket.append((key, value))  # collision -> append vào cùng bucket

    def get(self, key: str) -> object | None:
        bucket = self.buckets[self._bucket_index(key)]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def show_buckets(self) -> None:
        for i, bucket in enumerate(self.buckets):
            if bucket:
                print(f"  bucket[{i}]: {bucket}")


def demo_custom_hash_table() -> None:
    table = SimpleHashTable(num_buckets=4)
    table.set("name", "Alice")
    table.set("age", 30)
    table.set("city", "Hanoi")
    table.set("job", "Engineer")  # có thể collide bucket với key khác

    print("get('name'):", table.get("name"))
    print("get('missing'):", table.get("missing"))
    print("phân bố các bucket (collision = nhiều item / bucket):")
    table.show_buckets()


def demo_hashable_requirement() -> None:
    """Key phải hashable (immutable) — list không hashable vì có thể bị
    mutate sau khi làm key, phá vỡ tính nhất quán của hash table."""
    d: dict[object, str] = {}
    d[(1, 2)] = "tuple key OK vì tuple immutable"
    d["name"] = "str key OK"

    try:
        d[[1, 2]] = "list key"  # type: ignore
    except TypeError as e:
        print(f"list làm key -> lỗi: {e}")


def demo_counter_use_case() -> None:
    """Counter (dict con) — use case cực phổ biến của hash table: đếm
    tần suất. O(n) thay vì O(n^2) nếu đếm bằng cách duyệt lồng nhau."""
    words = "the quick brown fox jumps over the lazy dog the fox runs".split()
    counts = Counter(words)
    print("tần suất từ:", dict(counts))
    print("3 từ xuất hiện nhiều nhất:", counts.most_common(3))


def has_duplicate(items: list[int]) -> bool:
    """So sánh 2 cách check trùng lặp: dùng set (hash table) là O(n),
    dùng vòng lặp lồng nhau là O(n^2)."""
    seen: set[int] = set()
    for item in items:
        if item in seen:  # O(1) trung bình nhờ hash table
            return True
        seen.add(item)
    return False


def main() -> None:
    demo_custom_hash_table()

    print()
    demo_hashable_requirement()

    print()
    demo_counter_use_case()

    print()
    print("has_duplicate([1,2,3,2]):", has_duplicate([1, 2, 3, 2]))
    print("has_duplicate([1,2,3,4]):", has_duplicate([1, 2, 3, 4]))


if __name__ == "__main__":
    main()
