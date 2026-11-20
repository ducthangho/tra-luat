# wp1434 r1 — Đo nền mutation testing, chỉ đọc (DO-NEN-DOT-BIEN)
packet_id: wp1434
revision: 1

Trạng thái: đặc tả cho Packet #1434 thuộc Mission #1172. Packet chỉ đo: không sửa workflow, test hay runtime; không chạy lượt CI đột biến mới. Kết quả là đầu vào cho **kế hoạch nguồn r3**, bản thay thế cho kế hoạch nguồn r2 (sha256 `f4611b0f0c79f33d56b293f5fcb854eeeae2fcbb6acbdfd59d6134dcbfbdcb8f`) mà nguyên bản không còn tìm được. Packet này KHÔNG soạn r3 và KHÔNG đề xuất tối ưu.

## Vấn đề

Mission #1172 cam kết tối ưu mutation testing PR0–PR8, nhưng mục tiêu và acceptance chi tiết của PR1–PR8 nằm trong kế hoạch r2 đã mất. Viết lại kế hoạch mà không có số nền thì PR1–PR8 sẽ không có tiêu chí kiểm được. Các con số đang ghi trong kho lại có dấu hiệu đã trôi: chú thích đầu `.github/workflows/ci-dot-bien-du.yml` ghi "~73 800 s nối tiếp ⇒ 8 mảnh ≈ 2,6 h/mảnh", trong khi lượt 43990524880 (17/11/2026) có các job `dot-bien-manh` chạy khoảng 25–29 phút mỗi job.

## Hợp đồng

1. **Nguồn dữ liệu cho phép — chỉ đọc:**
   - GitHub REST GET (`actions/workflows/*/runs`, `actions/runs/<id>`, `.../jobs`, `.../artifacts`, tải artifact còn hạn) trên kho `ducthangho/tra-luat`.
   - Đọc tệp trong cây `origin/master` tại SHA ghi trong đầu ra.
   - Lệnh cục bộ chỉ được: `--help`, import để liệt kê bảng (không gọi hàm chạy ca hay chạy đột biến), `git log`/`git show`/`git rev-parse`.
   Cấm: `workflow_dispatch`, rerun, chạy `ops/nhanh_don_duoc_test.py`/`.claude/dev/ci_dang_ky_test.py --chay` hay bất kỳ bộ đột biến nào, mọi lệnh GHI GitHub ngoài push nhánh packet và PR.
2. **Phép đo bắt buộc:**
   - **M1 — full audit** (`ci-dot-bien-du.yml`): MỌI lượt mà API còn trả (ghi rõ cửa sổ thời gian thật có dữ liệu). Mỗi lượt: run id, sự kiện, SHA, kết luận, mỗi job (`dot-bien-du`, `dot-bien-manh (0..7)`, `dot-bien-gop`) với thời gian chờ (created→started), thời gian chạy (started→completed), runner label; mỗi bước của job mảnh với thời lượng. Nếu artifact mảnh còn hạn: số liệu bên trong (số mục, rc, mọi trường thời gian có sẵn) — tải về, băm sha256, không sửa.
   - **M2 — gate CI** (`ci.yml`): các lượt `push` master và `pull_request` trong 30 ngày gần nhất mà API còn trả. Mỗi lượt: thời lượng toàn lượt; mỗi job thuộc nhóm `gate*` thời lượng chạy; với job `gate-cong-cu*`, `gate-nhanh-*`, `gate-registry`, `gate-packet-loop*`: thời lượng từng bước. Tách theo nền (nhãn `labels` của job). Lượt huỷ/đỏ vẫn ghi, có cờ.
   - **M3 — kiểm kê tĩnh:** liệt kê các bộ test có đột biến (theo bảng đăng ký trong `.claude/dev/ci_dang_ky_test.py` và `ops/nhanh_don_duoc_test.py`), mỗi bộ: số ca, số mutant tự đột biến, số mutant sản phẩm, đường dẫn tệp:dòng của bảng nguồn. Số lấy bằng đọc/import bảng, không chạy.
   - **M4 — đối chiếu lời khai:** mọi con số thời gian/số lượng về đột biến đang ghi trong chú thích workflow, `CLAUDE.md`, `docs/` và `ops/specs/wp1166*` (tìm bằng `rg`, ghi lệnh tìm), mỗi lời khai kèm số đo tương ứng và kết luận `khớp | lệch | không đo được`.
3. **Đầu ra** (trong write set):
   - `ops/do/wp1434/thu_thap.py`: script thu thập một lần, chạy lại được (`python ops/do/wp1434/thu_thap.py --ra <thư mục>`), không ghi ngoài thư mục ra, không nối vào CI hay registry.
   - `ops/do/wp1434/BASELINE.json`: mọi số đo. Mỗi giá trị có `trang_thai ∈ {do_duoc, khong_do_duoc, khong_ap_dung}`, `nguon` (URL API hoặc `tệp:dòng@SHA` hoặc lệnh), và `ly_do` khi không phải `do_duoc`. Có khối `meta`: SHA master, thời điểm thu, cửa sổ thời gian, số lượt mỗi workflow, sha256 của từng bản thô đã tải.
   - `ops/do/wp1434/BAO_CAO.md`: tối đa ~200 dòng — bảng tổng hợp M1–M4; 5 điểm tốn thời gian nhất (theo số đo, kèm nguồn); mục **"Không đo được"** liệt kê đủ; mục **"Lời khai lệch"** từ M4. Không có mục khuyến nghị tối ưu.
   - Bản thô API: KHÔNG commit; chỉ commit sha256 + kích thước trong `meta`.
4. **Ba trạng thái, không hai:** thiếu dữ liệu (log hết hạn, artifact hết hạn, API lỗi) ⇒ `khong_do_duoc` kèm lý do; cấm điền 0 hay ước lượng vào ô đo. Mọi phép tính dẫn xuất (trung vị, p90, tổng) ghi công thức và tập đầu vào.
5. **Kiểm được lại:** reviewer chạy `thu_thap.py` vào thư mục tạm và so với `BASELINE.json`: các trường thuộc lượt đã hoàn tất trước `meta.thoi_diem_thu` phải bằng nhau (lượt mới phát sinh sau đó được phép thêm, không được làm đổi lượt cũ). Script có ca tự kiểm nhỏ `ops/do/wp1434/thu_thap_test.py` (không mạng, fixture JSON tối thiểu trong cùng thư mục) kiểm: phân loại ba trạng thái, phép trừ thời gian, xử lý job thiếu `started_at`/`completed_at` ⇒ `khong_do_duoc`.

## Write set

- `ops/specs/wp1434-r1/SPEC.md`
- `ops/leases/wp1434-r1-g1-claude.yaml`
- `ops/do/wp1434/thu_thap.py`
- `ops/do/wp1434/thu_thap_test.py`
- `ops/do/wp1434/fixtures/` (tệp JSON fixture của ca tự kiểm)
- `ops/do/wp1434/BASELINE.json`
- `ops/do/wp1434/BAO_CAO.md`

## Quy trình và quyền

- Executor: Claude Code (Fable 5.2). Reviewer: Codex service (gpt-6-astra), phiên độc lập, chỉ đọc, chạy lại `thu_thap.py` và ca tự kiểm. Trần: attempts 2, review 2, lời gọi Codex 2 (+1 lời gọi review spec trước lease).
- Rủi ro thấp (không đụng runtime/cổng), nhưng chủ kho duyệt băm đặc tả này trước khi cấp lease, và audit exact-H trước merge vì kết quả là căn cứ của kế hoạch r3. Điều phối không ký thay. Merge do chủ kho bấm. Không Windows CI, không full M9 mới.
- Ngoài phạm vi: soạn kế hoạch nguồn r3, đề xuất hay thử tối ưu, sửa workflow/test/chú thích đang lệch (chỉ ghi vào "Lời khai lệch"), PR1–PR8, installation, LIVE.
