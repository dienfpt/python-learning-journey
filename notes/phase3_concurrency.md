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
- [x] 2. Threading — I/O-bound concurrency, race condition, Lock
- [x] 3. Multiprocessing — CPU-bound parallelism, vượt qua GIL
- [x] 4. asyncio cơ bản — event loop, `async`/`await`, coroutine
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

## 2. Threading

- **Là gì**: `threading` module tạo các **OS thread thật**, chạy trong
  cùng 1 process và **share chung bộ nhớ** (biến global, object...). Nhờ
  GIL release lúc chờ I/O (mục 1), threading là công cụ tốt cho bài toán
  **I/O-bound** (gọi API, đọc/ghi file, query DB) — nhiều thread có thể
  cùng "chờ" song song, giảm tổng thời gian chờ gần bằng thời gian của
  tác vụ chậm nhất thay vì cộng dồn.
- **Hoạt động thế nào**: `threading.Thread(target=fn, args=...)` tạo
  thread, `.start()` chạy, `.join()` chờ thread đó xong. Idiomatic hơn:
  `concurrent.futures.ThreadPoolExecutor` — tự quản lý 1 pool thread có
  sẵn, tránh chi phí tạo/huỷ thread liên tục và cung cấp `.map()`/
  `.submit()` tiện dùng hơn quản lý `Thread` thủ công.
- **Race condition — rủi ro lớn nhất của shared memory**: khi 2+ thread
  cùng đọc-sửa-ghi 1 biến chung mà không đồng bộ hoá, kết quả cuối cùng
  phụ thuộc vào **thứ tự thực thi ngẫu nhiên** giữa các thread — thường
  cho ra kết quả sai (increment bị "mất") mà không có exception nào báo
  lỗi, rất khó debug vì **không tái hiện được ổn định** (có thể đúng ở
  máy dev, sai ở production dưới tải cao). File `02_threading.py` cưỡng
  bức context switch (`time.sleep(0)`) giữa bước đọc và ghi để tái hiện
  lỗi này 1 cách xác định (deterministic) cho mục đích minh hoạ.
- **`threading.Lock` (mutex)**: `with lock: ...` đảm bảo chỉ 1 thread
  được vào đoạn code đó (critical section) tại 1 thời điểm — thread khác
  phải **chờ** tới khi lock được giải phóng. Sửa được race condition,
  đánh đổi là chậm hơn (overhead acquire/release) và có thể gây
  **deadlock** nếu nhiều lock được acquire theo thứ tự không nhất quán
  giữa các thread.
- **So sánh JS**: Node.js không có race condition kiểu này ở code JS
  thường vì luôn chạy trên 1 thread duy nhất. `Worker Threads` của Node
  (thread thật, dùng cho CPU-bound) mặc định **không share memory** —
  giao tiếp qua message passing (giống gửi tin nhắn, copy dữ liệu) trừ
  khi cố tình dùng `SharedArrayBuffer` — an toàn hơn nhưng cũng hạn chế
  hơn threading của Python (share biến trực tiếp, tiện nhưng dễ lỗi).
- **Khi nào dùng**: nhiều tác vụ I/O-bound độc lập cần chạy đồng thời
  (gọi nhiều API, đọc nhiều file) mà không muốn chuyển hẳn sang asyncio
  (mục 4-5) — đặc biệt khi làm việc với thư viện chỉ hỗ trợ blocking I/O
  (không có bản `async`). Với CPU-bound, threading **không giúp gì** — cần
  multiprocessing (mục 3).

## 3. Multiprocessing

- **Là gì**: `multiprocessing` module tạo các **process hệ điều hành hoàn
  toàn riêng biệt** (khác thread chỉ là các luồng thực thi trong CÙNG 1
  process) — mỗi process có **GIL riêng, không gian bộ nhớ riêng**. Đây
  là cách chính thống để đạt **parallelism thật** cho CPU-bound trong
  Python, vượt qua giới hạn của GIL (mục 1) mà threading (mục 2) không
  làm được.
- **Hoạt động thế nào**: API gần giống `threading` (`Process` thay
  `Thread`, cùng `.start()`/`.join()`) — idiomatic hơn là
  `concurrent.futures.ProcessPoolExecutor`, cùng interface với
  `ThreadPoolExecutor` (`.map()`, `.submit()`), chỉ đổi thread → process
  bên dưới.
- **Đánh đổi lớn nhất — không share memory**: khác threading (share biến
  global trực tiếp), mỗi process có bộ nhớ độc lập hoàn toàn. Không thể
  "return" giá trị trực tiếp từ process con như gọi hàm bình thường — cần
  cơ chế IPC (inter-process communication) tường minh: `multiprocessing.
  Queue`/`Pipe` (gửi dữ liệu qua lại), `Value`/`Array` (bộ nhớ chia sẻ có
  kiểu cố định, đồng bộ bằng lock ngầm). `ProcessPoolExecutor.map()` che
  giấu bớt việc này (tự động pickle/gửi kết quả return về), nên thường
  được ưu tiên dùng hơn `Process` thủ công.
- **Chi phí (overhead)**: tạo process **tốn kém hơn nhiều** so với tạo
  thread (cấp phát bộ nhớ mới, copy môi trường...) — vì vậy multiprocessing
  chỉ đáng dùng khi khối lượng CPU-bound đủ lớn để bù lại chi phí khởi
  tạo; với task nhỏ, chi phí tạo process có thể còn lớn hơn lợi ích song
  song hoá.
- **Ràng buộc kỹ thuật quan trọng**: chế độ mặc định trên macOS/Windows là
  **"spawn"** (tạo process con hoàn toàn mới, import lại module) — hàm
  truyền cho `Process`/`Pool` phải là **top-level function của 1 module
  import được** (không phải lambda/closure/nested function, vì không
  pickle được để gửi sang process con). Code khởi tạo process nên đặt
  trong `if __name__ == "__main__":` để tránh spawn đệ quy vô hạn (mỗi
  process con re-import module gốc, nếu code tạo process nằm ở top-level
  sẽ tạo process mới mỗi lần import). Linux mặc định dùng "fork" (copy
  trực tiếp process cha, không cần pickle function) nên ít gặp ràng buộc
  này hơn, nhưng code viết portable nên tuân theo quy tắc "spawn" để chạy
  đúng trên mọi hệ điều hành.
- **So sánh JS**: gần nhất là `child_process`/`cluster` module của
  Node.js — cũng phải dùng process riêng (không phải Worker Threads share
  memory) để đạt CPU parallelism thật, cùng lý do: mỗi process có runtime
  riêng, không bị nghẽn bởi 1 event loop/GIL chung. Khác biệt: Node
  thường phải tự thiết kế giao thức IPC, còn `multiprocessing` cung cấp
  sẵn `Queue`/`Pool.map()` tiện dùng hơn.
- **Khi nào dùng**: công việc CPU-bound nặng thực sự (xử lý ảnh/video
  hàng loạt, tính toán khoa học, nén dữ liệu lớn) mà không dùng được thư
  viện C release GIL (`numpy` thường đã đủ nhanh mà không cần
  multiprocessing). Không dùng cho I/O-bound — threading/asyncio nhẹ hơn
  nhiều cho trường hợp đó.

## 4. asyncio cơ bản — Event Loop, async/await, Coroutine

- **Là gì**: mô hình concurrency **đơn luồng** (single-threaded) dựa trên
  **event loop** — vòng lặp trung tâm luân phiên chạy nhiều coroutine,
  chuyển sang coroutine khác mỗi khi coroutine hiện tại `await` 1 việc cần
  chờ (I/O). Không dùng OS thread/process nên **không có race condition**
  kiểu threading (mục 2) — tại một thời điểm chỉ đúng 1 đoạn code Python
  đang chạy, không có 2 đoạn code cùng xen vào giữa chừng.
- **`async def`** định nghĩa 1 **coroutine function** — gọi hàm này
  **không chạy code bên trong ngay**, chỉ tạo ra 1 **coroutine object**
  (giống 1 "kế hoạch sẽ chạy", gần với Promise của JS nhưng "lazy" hơn —
  Promise JS bắt đầu chạy ngay khi tạo, coroutine Python thì không chạy gì
  cho tới khi được await/schedule).
- **`await`** mới thực sự chạy coroutine đó và lấy giá trị return, đồng
  thời là điểm mà event loop **có thể** chuyển sang chạy việc khác trong
  lúc chờ. Quên `await` là lỗi rất phổ biến — Python cảnh báo
  `RuntimeWarning: coroutine '...' was never awaited` (file
  `04_asyncio_basics.py` minh hoạ trực tiếp lỗi này).
- **Hiểu lầm phổ biến nhất — await tuần tự KHÔNG tạo ra concurrency**:
  `await a(); await b(); await c()` chạy **lần lượt**, tổng thời gian vẫn
  cộng dồn như gọi hàm sync bình thường — `async`/`await` tự nó chỉ là cú
  pháp cho phép nhường CPU tại điểm `await`, không tự động chạy song song.
  Muốn nhiều coroutine chạy **đồng thời**, cần `asyncio.gather()` hoặc
  `asyncio.create_task()` (mục 5).
- **`asyncio.run()`** là entry point bắt buộc: tạo event loop mới, chạy 1
  coroutine cho tới khi xong, rồi đóng event loop. **Khác Node.js**: JS
  runtime tự có sẵn event loop chạy ngầm ngay khi script bắt đầu (không
  cần dòng khởi động nào) — Python cần khai báo tường minh, và (ở mức cơ
  bản) không thể "vừa async vừa không" trong cùng 1 chương trình theo
  kiểu JS — code gọi coroutine phải nằm trong ngữ cảnh async (`async def`
  khác) hoặc được `asyncio.run()` khởi động.
- **`asyncio.sleep()` vs `time.sleep()`**: `asyncio.sleep()` là
  **non-blocking** — nhường quyền điều khiển lại cho event loop trong lúc
  chờ, cho phép coroutine khác chạy. `time.sleep()` là **blocking** — dừng
  toàn bộ thread (kể cả event loop) trong lúc chờ, phá vỡ hoàn toàn lợi
  ích của asyncio nếu dùng nhầm bên trong coroutine.
- **Khi nào dùng**: bài toán I/O-bound cần chạy **rất nhiều** tác vụ đồng
  thời (hàng trăm/nghìn request) — asyncio nhẹ hơn threading nhiều (không
  tốn chi phí tạo OS thread cho mỗi tác vụ), là mô hình mặc định của
  FastAPI (Phase 4). Yêu cầu: mọi thư viện I/O dùng trong coroutine phải
  có bản `async` (vd. `httpx.AsyncClient` thay vì `requests`) — dùng thư
  viện sync bên trong coroutine sẽ block event loop, mất hết lợi ích.
