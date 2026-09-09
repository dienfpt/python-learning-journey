# Phase 3 — Concurrency & Async

Quay lại nhánh JS→Python 1:1 (khác Phase 2 DSA): đây là phase có nhiều
khác biệt cốt lõi với JS nhất, vì mô hình concurrency của 2 ngôn ngữ dựa
trên nguyên lý khác hẳn nhau — Node.js single-threaded + event loop
(libuv) thao túng I/O bất đồng bộ, còn Python có sẵn threading/
multiprocessing thật (multi-threaded/multi-process) NHƯNG bị giới hạn bởi
GIL, và asyncio là mô hình bất đồng bộ riêng (event loop tương tự Node
nhưng cần khai báo tường minh bằng `async`/`await`, không "tự động" như
JS).

## Concurrency là gì, tại sao cần?

- **Concurrency** (đồng thời): cấu trúc chương trình để xử lý nhiều việc
  "cùng lúc" — không nhất thiết chạy song song thật (đó là **parallelism**),
  mà là biết cách gối các tác vụ chờ đợi (I/O) lên nhau để không lãng phí
  thời gian chờ.
- **Parallelism** (song song): thực sự chạy nhiều việc TẠI CÙNG 1 THỜI
  ĐIỂM, cần nhiều CPU core. Concurrency có thể đạt được trên 1 core (xen
  kẽ), parallelism thì không.
- **Tại sao cần**: một server xử lý nhiều request cùng lúc, một script gọi
  10 API cùng lúc thay vì tuần tự, một chương trình tính toán nặng dùng
  hết nhiều core CPU thay vì 1 — tất cả đều cần hiểu đúng mô hình
  concurrency để không lãng phí tài nguyên hoặc viết code có race
  condition (lỗi do nhiều luồng cùng sửa 1 dữ liệu chung).
- **Phân biệt bài toán I/O-bound vs CPU-bound là chìa khoá chọn đúng công
  cụ** (chi tiết ở mục 2-4):
  - **I/O-bound**: thời gian chờ chủ yếu ở việc chờ mạng/đĩa (gọi API, đọc
    file, query DB) — CPU rảnh trong lúc chờ.
  - **CPU-bound**: thời gian chủ yếu ở tính toán thực sự (xử lý ảnh, tính
    toán số học nặng) — CPU luôn bận.

## Tiến độ

- [x] 1. GIL (Global Interpreter Lock) — là gì, ảnh hưởng thế nào
- [ ] 2. Threading — I/O-bound concurrency, race condition, Lock
- [ ] 3. Multiprocessing — CPU-bound parallelism, vượt qua GIL
- [ ] 4. asyncio cơ bản — event loop, `async`/`await`, coroutine
- [ ] 5. asyncio nâng cao — `Task`, `gather`, timeout, cancellation
- [ ] 6. Chọn đúng mô hình — threading vs multiprocessing vs asyncio, so
      sánh với Node.js event loop

## 1. GIL (Global Interpreter Lock)

- **Là gì**: một lock (khoá) toàn cục trong CPython (bản Python phổ biến
  nhất — GIL là chi tiết cài đặt của CPython, không phải đặc tả ngôn ngữ
  Python) đảm bảo **tại một thời điểm chỉ 1 thread được thực thi Python
  bytecode**, kể cả khi máy có nhiều CPU core và chương trình tạo nhiều
  thread.
- **Tại sao tồn tại**: quản lý bộ nhớ của CPython (reference counting —
  đếm số reference tới mỗi object để biết khi nào giải phóng) **không
  thread-safe** theo mặc định. GIL là giải pháp đơn giản hoá: thay vì
  lock riêng cho từng object (phức tạp, chậm cho code đơn luồng), khoá
  luôn toàn bộ interpreter. Đánh đổi: code đơn luồng chạy nhanh, nhưng
  code đa luồng CPU-bound không tận dụng được nhiều core.
- **Ảnh hưởng thế nào**: GIL được **giải phóng (release)** tạm thời trong
  lúc thread đang chờ I/O (`time.sleep()`, network call, đọc file...) —
  đây là lý do threading **vẫn hữu ích cho I/O-bound**. Nhưng với công
  việc **CPU-bound thuần** (tính toán liên tục, không chờ đợi), thread
  phải giành GIL qua lại liên tục, khiến nhiều thread chạy CPU-bound
  **không nhanh hơn** (thậm chí chậm hơn do overhead) so với 1 thread —
  file `01_gil.py` đo trực tiếp cả 2 trường hợp để thấy rõ khác biệt.
- **So sánh JS**: Node.js không có GIL vì **không cần** — thiết kế đơn
  luồng ngay từ đầu (1 thread chạy JS, các thao tác I/O được libuv xử lý
  ở background threads/OS rồi callback quay lại thread chính). Python thì
  ngược lại: **có** khả năng đa luồng thật (OS thread thật), nhưng GIL
  giới hạn nó chỉ hữu dụng cho I/O-bound — về hiệu ứng cuối cùng cho
  I/O-bound code, 2 mô hình cho kết quả tương tự nhau (không block trong
  lúc chờ I/O), dù cơ chế bên dưới khác hẳn.
- **Cách "né" GIL cho CPU-bound**: dùng **multiprocessing** (mục 3) — mỗi
  process có GIL + bộ nhớ riêng, chạy thật sự song song trên nhiều core.
  Ngoài ra: các thư viện tính toán nặng (`numpy`, `pandas`) thường release
  GIL khi chạy code C bên dưới, nên vẫn tận dụng được nhiều core dù gọi từ
  Python thread.
- **Lưu ý**: Python 3.13+ có chế độ thử nghiệm **free-threaded** (bỏ GIL,
  PEP 703) — chưa phải mặc định, cần build riêng, hệ sinh thái thư viện
  chưa hỗ trợ đầy đủ. Kiến thức GIL ở trên vẫn là mô hình mặc định cần
  nắm vững.
