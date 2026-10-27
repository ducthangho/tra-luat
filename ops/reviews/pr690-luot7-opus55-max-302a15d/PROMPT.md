Bạn là REVIEWER ĐỘC LẬP (lượt 7) cho PR #690 của kho ducthangho/tra-luat — packet #671 `WINDOWS-BASH-NEN-ESCAPE`. Bạn là một phiên MỚI, READ-ONLY với kho. Bạn CÙNG PROVIDER với executor (Claude review mã do Claude viết) — lượt này là `advisory_review`, nhãn tối đa `same_provider_approved`, KHÔNG phải `cross_approved`; bạn phải TỰ đọc spec/diff và TỰ chạy lại mọi phép đo (protocol §8), không tóm tắt báo cáo executor.

## Hiện vật (mọi thứ nằm trong thư mục làm việc hiện tại `$R`)
- `kho.git` — bản sao bare của kho cục bộ. `cay-kho/` — clone làm việc, detached tại **reviewed_sha = `302a15d`** (commit ký CỤC BỘ, CHƯA đẩy lên GitHub; SHA đầy đủ: `git -C cay-kho rev-parse HEAD`). Chuỗi cục bộ: `8757a84` (merge master) → `0ce1ad3` (vá 6, review lượt 6) → `302a15d` (vá 7).
- Mốc so sánh: `0ce1ad3` (head lượt 6) và **master `fc852ff`** (merge-base; trần dòng tính so `fc852ff`). Dựng bản sao nền bằng `git clone -q kho.git tam/nen && git -C tam/nen checkout -q --detach <sha>` — hai vế trong CÙNG MỘT lệnh.
- `SPEC-WINDOWS-BASH-NEN-ESCAPE-r1.md` (sha256 phải là `18504ced1549cbe62816f067b6ed16f36c12292820c8204cb6085a9c39e80b88` — kiểm lại), `LEASE-g3.yaml` (lease hiện hành, thay g2; write set `ops/bash_nen.py` + `ops/cong_cu_test.py`; `sensitive`; trần ADR-0044 300 dòng thêm so merge-base — chủ kho đã NÂNG lên ~400 cho packet này, xem dưới; `assurance_target: human_audited`).
- Các lượt trước (READ-ONLY):
  - `luot1/VERDICT.md` — codex trên `75af95c`.
  - `luot2/VERDICT.md` + `luot2/HINT.patch` — advisory Opus trên `e46f569`.
  - `luot3/VERDICT.md` + `luot3/HINT.patch` — Opus effort max trên `e46f569`.
  - `luot4-advisory-bd6ad5d/VERDICT_comment.md` + `HINT.patch` — advisory Opus trên `bd6ad5d`.
  - `luot4/VERDICT.md` + `luot4/HINT.patch` — review lượt 4 (Opus max) trên `b137bd8`.
  - `luot5/VERDICT.md` + `luot5/HINT.patch` — review lượt 5 trên `8757a84`.
  - `luot6/VERDICT.md` + `luot6/HINT.patch` — review lượt 6 (Opus max) trên `0ce1ad3`: P2=1 P3=1 P4=6 (PR #690 comment 5922243858). Vòng vá 7 dùng HINT này.
- `bao-cao-va-luot7/BAO_CAO.md`, `DUONG_VAO.md` — lời khai executor vòng 7. **Nguồn gốc khác thường:** bộ lọc an toàn của Opus 5.5 chặn một phản hồi ở lượt 2 của agent vá, CLI tự chuyển sang `claude-opus-4-8` — 283/285 lượt của vòng vá do Opus 4.8 viết; chủ kho chọn giữ bản vá và review bằng Opus 5.5. Báo cáo dừng giữa chừng (agent thoát khi pha bán kính còn chạy). `do-manh-dieu-phoi/` — log 16 mảnh do phiên điều phối chạy trên bản vá (sha256 `cong_cu_test.py` `467248e8…`) — lời khai, đo lại.
- Diff cần review: `git -C cay-kho diff 0ce1ad3 302a15d -- ops/` (vá 7) và `git -C cay-kho diff fc852ff 302a15d` (toàn PR so master; chỉ `ops/bash_nen.py` + `ops/cong_cu_test.py`).
- Đọc trong `cay-kho/`: `CLAUDE.md` (bài học đắt giá: đột biến trên BẢN SAO TẠM, bẫy `.pyc`, "tín dụng giả", "lời khai rộng hơn phép đo", "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba"), `docs/PROTOCOL_DA_PHIEN.md` §8, §13, `.claude/skills/cross-review/SKILL.md`.

## MỚI ở lượt này — vá 7 (đo kỹ)
Vá 7 theo HINT lượt 6: kernel32 giả của `t64` thành hàm C thật qua `CFUNCTYPE` (handle > 32 bit, đọc cờ tại địa chỉ ctypes truyền); `popen` giả báo hiệu sau khi ghi thành viên job; xả đệm bỏ qua luồng `None` + chốt (k4) fd đóng; hạn chót đọc dòng đầu `t64`; bỏ số đếm trôi khỏi chú thích; giãn mã đã nén. Đo ÍT NHẤT: (i) đồ giả mới mô phỏng TRẠNG THÁI hay diễn kịch bản, và có bắt được từng lỗi ABI (quên `byref`, `argtypes`/`restype` sai, cắt HANDLE, sai kích thước struct) — đột biến sản phẩm chết đúng nhãn; (ii) chốt (k4) và hạn chót `t64` có răng (đột biến gỡ ⇒ ĐỎ đúng tín hiệu), không chập chờn dưới tải/chạy nền; (iii) không chú thích nào còn con số trôi được; (iv) giãn mã không đổi hành vi (so `0ce1ad3`); (v) vì executor là Opus 4.8 do fallback: soát kỹ hơn thường mọi lời khai trong BAO_CAO.
**Ngân sách thời gian:** 16 mảnh song song (8 env CI + 8 env ascii, mỗi mảnh `CONG_CU_TEST_TIEN_TRINH=1`, chỉ số mảnh 0–7) mất ~105 phút ở máy này — đã có log của phiên điều phối trong `do-manh-dieu-phoi/`; tự chạy lại ít nhất một env đầy đủ hoặc mẫu mảnh đủ để kiểm lời khai. ĐIỀN SNAPSHOT cuối và dòng `verdict:` NGAY khi có kết luận. Trần lượt này 6 giờ. Container có thể khởi động lại: ghi VERDICT tăng dần.
**Bộ lọc nội dung:** vòng vá 7 bị bộ lọc an toàn của nền chặn một phản hồi. Phần nào liên quan giết tiến trình/Job Object/ABI: ưu tiên CHẠY ca và ĐỘT BIẾN có sẵn trong cây; mô tả bằng lời thay vì tự soạn mã khai thác.

## Quyết định chủ kho đã có (đừng hỏi lại, nhưng ĐO)
- **2026-09-30/10-01:** vá mồ côi NGAY; trần dòng thêm nâng 300 → ~400 → **~420** so `fc852ff` (issue #671 comment 5925174103; vượt ⇒ dừng hỏi). Phiên điều phối đo: +417. Lease g3 thay g2 (comment 5922102474).
- Giữ bản vá 7 dù executor bị fallback sang Opus 4.8 (chủ kho, 2026-10-01).
- S5: BỎ cơ chế hoãn `bo_qua_va` trong `t49` — đã thi hành ở vòng 5.
- Tên ca `t60`–`t64` lệch spec (`t52`) vì #668 đã dùng `t52`–`t54` ⇒ việc khai ở PR, không đổi tên trong mã.
- Nghiệm thu Windows là KHÔNG ĐO ĐƯỢC ở đây (chủ kho: "Chỉ chạy tại máy"); phân hạng theo spec, không tự miễn, nhưng không đòi vá bằng mã.

## Luật cứng
- KHÔNG sửa `cay-kho/` hay `kho.git`. Mọi thử nghiệm/đột biến/áp vá trên BẢN SAO TẠM trong `$R/tam/`. `TMPDIR=$R/tam`, `PYTHONDONTWRITEBYTECODE=1`, xoá `__pycache__` trước mỗi lượt đo.
- KHÔNG push, KHÔNG gọi mạng GitHub, KHÔNG chạy CI, KHÔNG ghi ngoài `$R` (kể cả `~/.gitconfig`, `/tmp`).
- Python: `python3.12` cho phép đo chính; `python3.11`, `python3.13` để so. Trọn bộ `python3.12 ops/cong_cu_test.py` ~25–30 phút — chạy ngầm, làm việc khác trong lúc chờ; chạy trọn bộ trên `302a15d` (chế độ mảnh như CI) ít nhất MỘT lần ở (a) env CI và (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii`. Lưu ý: nạp module bằng importlib ở (b) thì KHÔNG phóng lại (không phải `__main__`) nên ca đỏ `Unicode*Error` — đó là tạo tác bộ chạy (đo được trên cả `8757a84`); chạy qua `__main__` hoặc `-X utf8`.
- Hướng nào cần TỰ SOẠN nội dung dạng tấn công (đường dẫn thoát cây, v.v.) thì CHỈ MÔ TẢ bằng lời; ưu tiên CHẠY phản chứng có sẵn và ĐỘT BIẾN bản vá.
- Mọi thứ riêng Windows là `KHÔNG ĐO ĐƯỢC` trừ khi mô phỏng được và nói rõ là mô phỏng.

## Việc
1. **ĐỐI CHIẾU LƯỢT TRƯỚC**: với TỪNG lớp của `luot6` (chính), rồi các lớp lượt trước chưa trùng: đo lại trên `302a15d` — đã đóng / còn mở / đóng một phần — kèm lệnh + output. Kiểm riêng lời khai executor vòng 7 và log 16 mảnh của phiên điều phối.
2. **BẢNG SĂN — ≥ 6 hướng ĐỘC LẬP**, mỗi hướng LỆNH + OUTPUT THẬT + kết luận `LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC`. Gợi ý (tự nghĩ thêm): dấu chống lặp `CONG_CU_TEST_DA_PHONG_LAI` có sót sang tiến trình con/cháu hay bị một ca nào vô tình đặt không; `__file__` không phải tệp ở các dạng gọi khác (`-m`, zipapp, symlink); `t62` có đo đúng tiến trình CHẠY BỘ CA không; mã thoát 5 của cửa tự kiểm có va chạm mã nào khác; `t61` mã con dựng bằng `encode("ascii","backslashreplace")` có đúng khi đường dẫn tệp mang chữ Việt/dấu cách; `t63` bơm lỗi có đo đúng chốt hay bị chốt khác bắt hộ; bán kính đột biến của bộ ca có bị ca mới kéo rộng (tín dụng giả) không; `t5` SIGPIPE `rc=141` (executor ghi nhận; #675 đã vá trên master) — xác định có liên quan PR không.
3. **ĐỘT BIẾN BẢN VÁ**: với mỗi chốt mới/sửa ở `t64`, `_phong_lai`, cửa `_in_tu_kiem_che_do_utf8`, và kiểm lại `t60`–`t63`: gỡ/đảo trên bản sao tạm, chạy đúng ca đích — phải ĐỎ **bằng chính tín hiệu chốt** (`TinHieuChotCa`/`bang`), không phải lỗi vô can. Bảng: đột biến → ca → kết quả → giết thật / tín dụng giả / sống sót.
4. **BẢNG ĐO**: đo lại mọi con số executor/commit khai (commit `302a15d`: +417 so `fc852ff`; 16/16 mảnh pha ca 60/60; bán kính 415/416 ok mỗi env, `t2_go_canary` KHÔNG ĐO ĐƯỢC do thiếu `jsonschema`; ruff F = nền). Ruff: `pip install --target $R/tam/ruff ruff==0.15.15`, `--select F`, so TẬP finding.
5. Mỗi finding đủ bốn phần §8 — **vá ở đâu**, **vá thế nào**, **ca test khoá nó** (và đột biến nào phải chết sau khi vá), **bản vá có thể đẻ ra gì** — kèm hunk trong **HINT.patch**:
   - MỘT tệp `$R/out/HINT.patch`, định dạng `patch -p0` từ GỐC cây làm việc (đường dẫn repo-relative, không tiền tố `a/`/`b/`), áp lên `302a15d`.
   - BẮT BUỘC tự kiểm: `git clone -q kho.git tam/ap && git -C tam/ap checkout -q --detach 302a15d && cd tam/ap && patch -p0 --fuzz=0 --dry-run < ../../out/HINT.patch` ⇒ rc=0; áp thật trên bản sao ấy, chạy lại các ca liên quan + ca khoá đề xuất, ghi kết quả; tổng dòng thêm sau áp so master `fc852ff` ≤ 420 (head đã ở +417 — HINT phải trung hoà dòng hoặc nói rõ phần vượt để chủ kho quyết).
   - HINT cho TEST/ĐỘT BIẾN được ở mức mã đầy đủ; HINT cho MÃ SẢN PHẨM là gợi ý hướng — ghi rõ.

## Đầu ra — `$R/out/VERDICT.md` (ghi TĂNG DẦN: tạo khung ngay, cập nhật SAU MỖI HƯỚNG/MỤC)
```
verdict: approve | changes_requested | blocked
reviewed_sha: <SHA đầy đủ của 302a15d>
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
