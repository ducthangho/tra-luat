# Prompt EXECUTOR — `CI-BANG-PHU-THUOC` (#245), lượt 1

Lease `ci-bang-phu-thuoc-exec-1-claude-20260822`. Đặc tả đóng băng:
`ops/specs/CI-BANG-PHU-THUOC.md`, `sha256 = 14bd1425e89f6b304ce60f8ebd0246a7bf8020f3732647494daecc9f07bc8b7c`.

**Kiểm băm TRƯỚC khi đọc nội dung.** Lệch ⇒ dừng, không tự đoán bản nào đúng.

## Việc

Ghi **bảng phụ thuộc** giữa bước CI và nhóm đường dẫn, cộng cỗ máy **tự dựng lại bảng bằng phép
đo** để nó không trôi lệch. **KHÔNG đổi một dòng hành vi CI nào** — `.github/workflows/ci.yml`
nằm ngoài write set, cố ý.

Năm mục tiêu M1–M5 và sáu tiêu chí N1–N6 ở đặc tả. Đừng chép lại chúng vào đây; đọc từ tệp có băm.

## Thứ dễ làm sai nhất — đọc kỹ, đã trả giá trong lượt soạn spec

**Phép dò "thêm một dòng chú thích rồi xem đầu ra có đổi không" là phép dò YẾU.** Nó chỉ bắt được
bước **băm nội dung**. Bước chạy **hành vi** (`tl selftest`, `doc-claims-check`) sẽ cho `.` —
nghĩa là *"an toàn để bỏ"* — trong khi thực tế chúng đọc `docs/` **69 tệp**.

Hình dạng ấy đã đếm **BA** lần trong lượt soạn spec (B5 của đặc tả). Chạm ba là ngưỡng `CLAUDE.md`
đặt để dừng lại hỏi. **Nếu bạn thấy mình đang chứng minh "bỏ bước này an toàn" bằng bất cứ thứ gì
nhẹ hơn tập-đọc (audit hook) hoặc tập-băm (dẫn xuất từ `_RELEASE_EXCLUDE_*`), đó là lần thứ tư —
DỪNG và xuất handoff.**

Ba cái bẫy đã sập, chép ra để bạn không sập lại:

1. **Đối chứng trước, hiệu số sau.** Đầu ra JSON của `golden-test`/`determinism-audit` **tự trôi**
   mỗi lượt (`cases[12].raw_sha256`, `raw_stable` — khung golden đã tự khai `raw_stable: False`).
   Băm cả JSON rồi so là đo độ trôi, không đo phụ thuộc. Chạy **hai lượt không đột biến** trước.
2. **`core.abbrev` phải = 7.** Không ghim thì `golden-test` báo `ok: False` **giả** trên cây sạch
   (`CLAUDE.md` §Quy ước deploy mục 6).
3. **Đột biến trên BẢN SAO, không trên cây thật.** Lượt bị cắt giữa chừng để lại tệp méo và lượt
   sau đọc bản méo làm bản gốc. Đã sập đúng vậy: dùng `git worktree add --detach`.

## Môi trường — kiểm TRƯỚC khi tin bất kỳ phép đo tập-đọc nào

`tl selftest` **không chạy được** nếu `cryptography` của hệ thống hỏng
(`pyo3_runtime.PanicException` qua `pypdf`). Đo 2026-08-22: hook phiên báo *"môi trường còn khớp"*
trong khi thư viện bắt buộc panic ngay lúc import. **"Khớp requirements" không phải "chạy được".**

Chữa: `pip install --upgrade cryptography`. Kiểm bằng bằng chứng DƯƠNG:
`python3 scripts/tl.py --selftest` phải in `== tl selftest N/N ==` với **hai số bằng nhau** và
`rc=0`. Một lượt nền hỏng cho `rc=1` mà vẫn in ra vài dòng **trông như số liệu**.

## Ngân sách và điều kiện dừng

Ở lease. Vượt ⇒ DỪNG và xuất handoff, **không tự nới**.

## Thứ KHÔNG được làm

- Không đụng `.github/workflows/ci.yml`. Công tắc thuộc packet kế nhiệm.
- Không đụng `ops/specs/**`. Đặc tả đã đóng băng; cần đổi thì đi qua bản sửa đổi mới.
- Không tự cấp lease, không tự mở packet kế nhiệm.
