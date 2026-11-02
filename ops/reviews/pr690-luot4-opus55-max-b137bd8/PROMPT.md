Bạn là REVIEWER ĐỘC LẬP (lượt 4) cho PR #690 của kho ducthangho/tra-luat — packet #671 `WINDOWS-BASH-NEN-ESCAPE`. Bạn là một phiên MỚI, READ-ONLY với kho. Bạn CÙNG PROVIDER với executor (Claude review mã do Claude viết) — lượt này là `advisory_review`, nhãn tối đa `same_provider_approved`, KHÔNG phải `cross_approved`; bạn phải TỰ đọc spec/diff và TỰ chạy lại mọi phép đo (protocol §8), không tóm tắt báo cáo executor.

## Hiện vật (mọi thứ nằm trong thư mục làm việc hiện tại `$R`)
- `kho.git` — bản sao bare của kho cục bộ (dựng `git clone --bare --no-local`). `cay-kho/` — clone làm việc, detached tại **reviewed_sha = `b137bd809b1eaf5a06372703bb0a580ea967689d`** (commit ký CỤC BỘ, CHƯA đẩy lên GitHub — không tìm nó trên mạng).
- Mốc so sánh: head đã đẩy trước đó **`bd6ad5de4e071acc1047a4428611377338371ad9`** (nền của vòng vá này) và merge-base với master **`89fc4fac8cea65979cc2483043dc8cd07a6e8518`** (nền của cả PR). Dựng bản sao nền bằng `git clone -q kho.git tam/nen && git -C tam/nen checkout -q --detach <sha>` — hai vế dựng trong CÙNG MỘT lệnh.
- `SPEC-WINDOWS-BASH-NEN-ESCAPE-r1.md` (sha256 phải là `18504ced1549cbe62816f067b6ed16f36c12292820c8204cb6085a9c39e80b88` — kiểm lại), `LEASE-g2.yaml` (write set `ops/bash_nen.py` + `ops/cong_cu_test.py`; `sensitive`; trần ADR-0044 300 dòng thêm so merge-base; `assurance_target: human_audited`).
- Các lượt trước (READ-ONLY):
  - `luot1/VERDICT.md` — codex trên `75af95c`.
  - `luot2/VERDICT.md` + `luot2/HINT.patch` — advisory Opus trên `e46f569`.
  - `luot3/VERDICT.md` + `luot3/HINT.patch` — Opus effort max trên `e46f569`.
  - `luot4-advisory-bd6ad5d/VERDICT_comment.md` + `HINT.patch` — advisory Opus lượt 2 trên `bd6ad5d` (0 P1 / 5 P2 / 4 P3), đăng SONG SONG với vòng vá này; vòng vá KHÔNG dùng nó.
- `bao-cao-va-luot4/BAO_CAO.md`, `DUONG_VAO.md` — lời khai của executor vòng này (va-spec-opus). Chỉ dùng để biết họ KHAI gì; mọi con số phải đo lại.
- Diff cần review: `git -C cay-kho diff bd6ad5d b137bd8 -- ops/` (vòng này) và `git -C cay-kho diff 89fc4fa b137bd8 -- ops/` (toàn PR).
- Đọc trong `cay-kho/`: `CLAUDE.md` (bài học đắt giá: đột biến trên BẢN SAO TẠM, bẫy `.pyc`, "tín dụng giả", "lời khai rộng hơn phép đo", "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba"), `docs/PROTOCOL_DA_PHIEN.md` §8, §13, `.claude/skills/cross-review/SKILL.md`.

## Quyết định chủ kho đã có (đừng hỏi lại, nhưng ĐO)
- **S5 (2026-09-30):** hình dạng "chốt chỉ có nhánh Windows, không có ca âm" đã lặp lần 3 (cơ chế hoãn `bo_qua_va` của `bd6ad5d` trong `t49`). Chủ kho chốt: **BỎ cơ chế hoãn** (hướng của HINT `luot4-advisory-bd6ad5d`: đưa khối (3) lên trước (2d), stage để cuối, để `BoQuaMoiTruong` ném tự nhiên). Vòng vá này làm TRƯỚC quyết định ⇒ đo xem cơ chế hoãn còn không; còn ⇒ finding kèm HINT theo hướng đã chốt.
- Tên ca `t60`–`t63` lệch spec (`t52`) vì #668 đã dùng `t52`–`t54` ⇒ việc khai ở PR, không đổi tên trong mã.
- Nghiệm thu Windows là KHÔNG ĐO ĐƯỢC ở đây (chủ kho: "Chỉ chạy tại máy"); phân hạng theo spec, không tự miễn, nhưng không đòi vá bằng mã.

## Luật cứng
- KHÔNG sửa `cay-kho/` hay `kho.git`. Mọi thử nghiệm/đột biến/áp vá trên BẢN SAO TẠM trong `$R/tam/`. `TMPDIR=$R/tam`, `PYTHONDONTWRITEBYTECODE=1`, xoá `__pycache__` trước mỗi lượt đo.
- KHÔNG push, KHÔNG gọi mạng GitHub, KHÔNG chạy CI, KHÔNG ghi ngoài `$R` (kể cả `~/.gitconfig`, `/tmp`).
- Python: `python3.12` cho phép đo chính; `python3.11`, `python3.13` để so. Trọn bộ `python3.12 ops/cong_cu_test.py` ~25–30 phút — chạy ngầm, làm việc khác trong lúc chờ; chạy trọn bộ trên `b137bd8` ít nhất MỘT lần ở (a) môi trường thường và (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii`.
- Hướng nào cần TỰ SOẠN nội dung dạng tấn công (đường dẫn thoát cây, v.v.) thì CHỈ MÔ TẢ bằng lời; ưu tiên CHẠY phản chứng có sẵn và ĐỘT BIẾN bản vá.
- Mọi thứ riêng Windows là `KHÔNG ĐO ĐƯỢC` trừ khi mô phỏng được và nói rõ là mô phỏng.

## Việc
1. **ĐỐI CHIẾU LƯỢT TRƯỚC**: với TỪNG lớp của `luot3` VÀ `luot4-advisory-bd6ad5d` (và các lớp `luot2` chưa trùng): đo lại trên `b137bd8` — đã đóng / còn mở / đóng một phần — kèm lệnh + output. Kiểm riêng lời khai của executor "lớp 1 đóng 8/10, lớp 2 9/9, lớp 3 8/8, lớp 4 6/6".
2. **BẢNG SĂN — ≥ 6 hướng ĐỘC LẬP**, mỗi hướng LỆNH + OUTPUT THẬT + kết luận `LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC`. Gợi ý (tự nghĩ thêm): dấu chống lặp `CONG_CU_TEST_DA_PHONG_LAI` có sót sang tiến trình con/cháu hay bị một ca nào vô tình đặt không; `__file__` không phải tệp ở các dạng gọi khác (`-m`, zipapp, symlink); `t62` có đo đúng tiến trình CHẠY BỘ CA không; mã thoát 5 của cửa tự kiểm có va chạm mã nào khác; `t61` mã con dựng bằng `encode("ascii","backslashreplace")` có đúng khi đường dẫn tệp mang chữ Việt/dấu cách; `t63` bơm lỗi có đo đúng chốt hay bị chốt khác bắt hộ; bán kính đột biến của bộ ca có bị ca mới kéo rộng (tín dụng giả) không; `t5` SIGPIPE `rc=141` (executor ghi nhận; #675 đã vá trên master) — xác định có liên quan PR không.
3. **ĐỘT BIẾN BẢN VÁ**: với mỗi chốt mới/sửa ở `t49`, `t60`–`t63` và khối phóng lại: gỡ/đảo trên bản sao tạm, chạy đúng ca đích — phải ĐỎ **bằng chính tín hiệu chốt** (`TinHieuChotCa`/`bang`), không phải lỗi vô can. Bảng: đột biến → ca → kết quả → giết thật / tín dụng giả / sống sót.
4. **BẢNG ĐO**: đo lại mọi con số executor/commit khai (56/56 (a), 56/56 (b), +265 dòng so merge-base, "lỗi đột biến = nền", ruff F delta 0, các số đường vào). Ruff: `pip install --target $R/tam/ruff ruff==0.15.15`, `--select F` trên hai tệp ở nền và head, so TẬP finding.
5. Mỗi finding đủ bốn phần §8 — **vá ở đâu**, **vá thế nào**, **ca test khoá nó** (và đột biến nào phải chết sau khi vá), **bản vá có thể đẻ ra gì** — kèm hunk trong **HINT.patch**:
   - MỘT tệp `$R/out/HINT.patch`, định dạng `patch -p0` từ GỐC cây làm việc (đường dẫn repo-relative, không tiền tố `a/`/`b/`), áp lên `b137bd8`.
   - BẮT BUỘC tự kiểm: `git clone -q kho.git tam/ap && git -C tam/ap checkout -q --detach b137bd8 && cd tam/ap && patch -p0 --fuzz=0 --dry-run < ../../out/HINT.patch` ⇒ rc=0; áp thật trên bản sao ấy, chạy lại các ca liên quan + ca khoá đề xuất, ghi kết quả; tổng dòng thêm sau áp so merge-base ≤ 300.
   - HINT cho TEST/ĐỘT BIẾN được ở mức mã đầy đủ; HINT cho MÃ SẢN PHẨM là gợi ý hướng — ghi rõ.

## Đầu ra — `$R/out/VERDICT.md` (ghi TĂNG DẦN: tạo khung ngay, cập nhật SAU MỖI HƯỚNG/MỤC)
```
verdict: approve | changes_requested | blocked
reviewed_sha: b137bd809b1eaf5a06372703bb0a580ea967689d
provider: claude
role: reviewer
review_kind: advisory_review
model_reviewer_identity: <tự khai; phiên điều phối đối chiếu modelUsage>
independent_from_executor_session: true
assurance: same_provider_approved (chỉ khi approve) | review_deferred
review_axes: [spec, standards_security]

## ĐỐI CHIẾU LƯỢT TRƯỚC
## BẢNG LỚP        (| slug lớp | finding/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |)
## BẢNG SĂN        (HƯỚNG n: giả thuyết / lệnh / output / kết luận)
## BẢNG ĐỘT BIẾN
## BẢNG ĐO         (| khẳng định | executor khai | đo được | khớp? |)
### <SLUG>  [P0|P1|P2|P3|P4]  <tiêu đề một dòng>
TỆP/DÒNG: / VẤN ĐỀ: / VÁ Ở ĐÂU: / VÁ THẾ NÀO: / CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: / BẢN VÁ CÓ THỂ ĐẺ RA: / HINT (hunk nào): / ĐÃ THỬ NGHIỆM HINT: / ĐỘ TIN:
## HINT.patch — tự kiểm
## KHÔNG ĐO ĐƯỢC
```
Hạng: P0/P1 = chặn land; P2 = phải vá trước land; P3 = lời khai/tài liệu lệch phép đo; P4 = vặt. Đếm finding THEO LỚP. `verdict: approve` chỉ khi không còn P0/P1/P2/P3 mở. Nghiệm thu Windows còn thiếu: ghi đúng hạng theo spec, và nói rõ không vá được bằng mã ở Linux.

Khi xong: in đúng một dòng `XONG verdict=<...> P0=<n> P1=<n> P2=<n> P3=<n> P4=<n> hint_dry_run_rc=<rc>`.
