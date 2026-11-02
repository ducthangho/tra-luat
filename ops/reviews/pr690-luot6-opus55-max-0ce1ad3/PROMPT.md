Bạn là REVIEWER ĐỘC LẬP (lượt 6) cho PR #690 của kho ducthangho/tra-luat — packet #671 `WINDOWS-BASH-NEN-ESCAPE`. Bạn là một phiên MỚI, READ-ONLY với kho. Bạn CÙNG PROVIDER với executor (Claude review mã do Claude viết) — lượt này là `advisory_review`, nhãn tối đa `same_provider_approved`, KHÔNG phải `cross_approved`; bạn phải TỰ đọc spec/diff và TỰ chạy lại mọi phép đo (protocol §8), không tóm tắt báo cáo executor.

## Hiện vật (mọi thứ nằm trong thư mục làm việc hiện tại `$R`)
- `kho.git` — bản sao bare của kho cục bộ (dựng `git clone --bare --no-local`). `cay-kho/` — clone làm việc, detached tại **reviewed_sha = `0ce1ad3`** (commit ký CỤC BỘ, CHƯA đẩy lên GitHub — không tìm nó trên mạng; lấy SHA đầy đủ bằng `git -C cay-kho rev-parse HEAD`). Chuỗi cục bộ: `8757a84` (merge master, đã review lượt 5) → `0ce1ad3` (vá 6).
- Mốc so sánh: `8757a84` (head lượt 5) và **master `fc852ff`** (merge-base của PR — mọi đo 'delta so nền' và trần dòng tính so `fc852ff`). Dựng bản sao nền bằng `git clone -q kho.git tam/nen && git -C tam/nen checkout -q --detach <sha>` — hai vế dựng trong CÙNG MỘT lệnh.
- `SPEC-WINDOWS-BASH-NEN-ESCAPE-r1.md` (sha256 phải là `18504ced1549cbe62816f067b6ed16f36c12292820c8204cb6085a9c39e80b88` — kiểm lại), `LEASE-g2.yaml` (write set `ops/bash_nen.py` + `ops/cong_cu_test.py`; `sensitive`; trần ADR-0044 300 dòng thêm so merge-base — chủ kho đã NÂNG lên ~400 cho packet này, xem dưới; `assurance_target: human_audited`).
- Các lượt trước (READ-ONLY):
  - `luot1/VERDICT.md` — codex trên `75af95c`.
  - `luot2/VERDICT.md` + `luot2/HINT.patch` — advisory Opus trên `e46f569`.
  - `luot3/VERDICT.md` + `luot3/HINT.patch` — Opus effort max trên `e46f569`.
  - `luot4-advisory-bd6ad5d/VERDICT_comment.md` + `HINT.patch` — advisory Opus trên `bd6ad5d`.
  - `luot4/VERDICT.md` + `luot4/HINT.patch` — review lượt 4 (Opus max) trên `b137bd8`.
  - `luot5/VERDICT.md` + `luot5/HINT.patch` — review lượt 5 (Opus max) trên `8757a84`: P1=1 P2=1 P3=1 P4=2 (đăng PR #690 comment 5918603629). Vòng vá 6 dùng HINT này.
- `bao-cao-va-luot6/BAO_CAO.md`, `DUONG_VAO.md` — lời khai của executor vòng 6 (va-spec-opus; agent bị `timeout` 4 giờ cắt khi trọn bộ lần 2 đang chạy — báo cáo dừng ở mục 7). Sau agent, phiên điều phối tự áp `luot5/HINT.patch` (P1 + P4) và nén hai chú thích để vừa trần (xem `git show 0ce1ad3`). Chỉ dùng để biết họ KHAI gì; mọi con số phải đo lại.
- Diff cần review: `git -C cay-kho diff 8757a84 0ce1ad3 -- ops/` (vá 6) và `git -C cay-kho diff fc852ff 0ce1ad3` (toàn PR so master; phải chỉ có `ops/bash_nen.py` + `ops/cong_cu_test.py`).
- Đọc trong `cay-kho/`: `CLAUDE.md` (bài học đắt giá: đột biến trên BẢN SAO TẠM, bẫy `.pyc`, "tín dụng giả", "lời khai rộng hơn phép đo", "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba"), `docs/PROTOCOL_DA_PHIEN.md` §8, §13, `.claude/skills/cross-review/SKILL.md`.

## MỚI ở lượt này — vá mồ côi (đo kỹ)
Vá 6 thay `subprocess.run`-rồi-chờ của khối tự phóng lại bằng `_phong_lai`: POSIX `os.execve` (cùng PID); Windows tự gán tiến trình vào Job Object `KILL_ON_JOB_CLOSE` qua `ctypes` TRƯỚC khi phóng, hỏng thì in `CANH_BAO_MO_COI` và vẫn chạy. Ca khoá `t64` (k1)(k2)(k3) chạy thật + (w0)(w1)(w2) trên kernel32 GIẢ. Đo ÍT NHẤT: (i) execve có làm mất gì mà đường cũ giữ: cờ trình thông dịch, `-B`, dấu chống lặp, mã thoát, stdout/stderr đã đệm, fd/stdin, cwd, `sys.orig_argv` khi gọi qua `-m`/symlink/đường dẫn có dấu cách; (ii) chế độ mảnh/gom #668 như CI gọi (`.github/workflows/ci.yml`) đi qua execve đúng không; (iii) đồ giả kernel32 mô phỏng TRẠNG THÁI hay diễn kịch bản (bài học CLAUDE.md) — đột biến sản phẩm Windows có bị đồ giả che không; bố cục cấu trúc `JOBOBJECT_EXTENDED_LIMIT_INFORMATION` (x64 144 B / x86 112 B, cờ offset 16) so tài liệu; (iv) `t64` có chập chờn dưới tải/chạy nền (`&`), có để lại tiến trình sót, có kéo rộng bán kính đột biến (tín dụng giả) không; (v) P1 lượt 5: `f25_cua_moi_vi_tri` và các đột biến #668 có về `ok … 1/61`; (vi) ảnh hưởng tới `t62`/`t61` (executor khai `t62` không đổi dòng nào).
**Ngân sách thời gian:** lượt 5 bị `timeout` 4 giờ cắt trước khi điền SNAPSHOT cuối. Trọn bộ nối tiếp nay có pha bán kính 416 đột biến (> 90 phút ở máy này). Dùng chế độ MẢNH như CI (8 mảnh, env CI trong `ci.yml`, chạy song song trên các clone riêng) thay cho một lượt nối tiếp; ĐIỀN SNAPSHOT cuối và dòng `verdict:` NGAY khi đã có kết luận, rồi mới làm thêm. Trần lượt này 6 giờ.

## Quyết định chủ kho đã có (đừng hỏi lại, nhưng ĐO)
- **2026-09-30:** vá mồ côi NGAY (vòng 6 thi hành) và **nâng trần dòng thêm của packet từ 300 lên ~400** so `fc852ff` (lệch có duyệt so ADR-0044; vượt 400 ⇒ dừng hỏi). Phiên điều phối đo: +400.
- S5: BỎ cơ chế hoãn `bo_qua_va` trong `t49` — đã thi hành ở vòng 5.
- Tên ca `t60`–`t64` lệch spec (`t52`) vì #668 đã dùng `t52`–`t54` ⇒ việc khai ở PR, không đổi tên trong mã.
- Nghiệm thu Windows là KHÔNG ĐO ĐƯỢC ở đây (chủ kho: "Chỉ chạy tại máy"); phân hạng theo spec, không tự miễn, nhưng không đòi vá bằng mã.

## Luật cứng
- KHÔNG sửa `cay-kho/` hay `kho.git`. Mọi thử nghiệm/đột biến/áp vá trên BẢN SAO TẠM trong `$R/tam/`. `TMPDIR=$R/tam`, `PYTHONDONTWRITEBYTECODE=1`, xoá `__pycache__` trước mỗi lượt đo.
- KHÔNG push, KHÔNG gọi mạng GitHub, KHÔNG chạy CI, KHÔNG ghi ngoài `$R` (kể cả `~/.gitconfig`, `/tmp`).
- Python: `python3.12` cho phép đo chính; `python3.11`, `python3.13` để so. Trọn bộ `python3.12 ops/cong_cu_test.py` ~25–30 phút — chạy ngầm, làm việc khác trong lúc chờ; chạy trọn bộ trên `0ce1ad3` (chế độ mảnh như CI) ít nhất MỘT lần ở (a) env CI và (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii`. Lưu ý: nạp module bằng importlib ở (b) thì KHÔNG phóng lại (không phải `__main__`) nên ca đỏ `Unicode*Error` — đó là tạo tác bộ chạy (đo được trên cả `8757a84`); chạy qua `__main__` hoặc `-X utf8`.
- Hướng nào cần TỰ SOẠN nội dung dạng tấn công (đường dẫn thoát cây, v.v.) thì CHỈ MÔ TẢ bằng lời; ưu tiên CHẠY phản chứng có sẵn và ĐỘT BIẾN bản vá.
- Mọi thứ riêng Windows là `KHÔNG ĐO ĐƯỢC` trừ khi mô phỏng được và nói rõ là mô phỏng.

## Việc
1. **ĐỐI CHIẾU LƯỢT TRƯỚC**: với TỪNG lớp của `luot5` (chính), rồi các lớp lượt trước chưa trùng: đo lại trên `0ce1ad3` — đã đóng / còn mở / đóng một phần — kèm lệnh + output. Kiểm riêng lời khai của executor vòng 6 (BAO_CAO: 37/37 đột biến giết đúng nhãn, 3 tương đương; bảng mồ côi nền/vá; (k3) 45/45 xanh chạy nền).
2. **BẢNG SĂN — ≥ 6 hướng ĐỘC LẬP**, mỗi hướng LỆNH + OUTPUT THẬT + kết luận `LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC`. Gợi ý (tự nghĩ thêm): dấu chống lặp `CONG_CU_TEST_DA_PHONG_LAI` có sót sang tiến trình con/cháu hay bị một ca nào vô tình đặt không; `__file__` không phải tệp ở các dạng gọi khác (`-m`, zipapp, symlink); `t62` có đo đúng tiến trình CHẠY BỘ CA không; mã thoát 5 của cửa tự kiểm có va chạm mã nào khác; `t61` mã con dựng bằng `encode("ascii","backslashreplace")` có đúng khi đường dẫn tệp mang chữ Việt/dấu cách; `t63` bơm lỗi có đo đúng chốt hay bị chốt khác bắt hộ; bán kính đột biến của bộ ca có bị ca mới kéo rộng (tín dụng giả) không; `t5` SIGPIPE `rc=141` (executor ghi nhận; #675 đã vá trên master) — xác định có liên quan PR không.
3. **ĐỘT BIẾN BẢN VÁ**: với mỗi chốt mới/sửa ở `t64`, `_phong_lai`, cửa `_in_tu_kiem_che_do_utf8`, và kiểm lại `t60`–`t63`: gỡ/đảo trên bản sao tạm, chạy đúng ca đích — phải ĐỎ **bằng chính tín hiệu chốt** (`TinHieuChotCa`/`bang`), không phải lỗi vô can. Bảng: đột biến → ca → kết quả → giết thật / tín dụng giả / sống sót.
4. **BẢNG ĐO**: đo lại mọi con số executor/commit khai (commit `0ce1ad3`: +400 dòng so `fc852ff`, 37/37 đột biến, `f25`… `1/61`, pha ca 60/60; ruff F = nền; các số mồ côi). Ruff: `pip install --target $R/tam/ruff ruff==0.15.15`, `--select F` trên hai tệp ở nền và head, so TẬP finding.
5. Mỗi finding đủ bốn phần §8 — **vá ở đâu**, **vá thế nào**, **ca test khoá nó** (và đột biến nào phải chết sau khi vá), **bản vá có thể đẻ ra gì** — kèm hunk trong **HINT.patch**:
   - MỘT tệp `$R/out/HINT.patch`, định dạng `patch -p0` từ GỐC cây làm việc (đường dẫn repo-relative, không tiền tố `a/`/`b/`), áp lên `0ce1ad3`.
   - BẮT BUỘC tự kiểm: `git clone -q kho.git tam/ap && git -C tam/ap checkout -q --detach 0ce1ad3 && cd tam/ap && patch -p0 --fuzz=0 --dry-run < ../../out/HINT.patch` ⇒ rc=0; áp thật trên bản sao ấy, chạy lại các ca liên quan + ca khoá đề xuất, ghi kết quả; tổng dòng thêm sau áp so master `fc852ff` ≤ 400 (head đã ở +400 — HINT phải trung hoà dòng hoặc nói rõ phần vượt để chủ kho quyết).
   - HINT cho TEST/ĐỘT BIẾN được ở mức mã đầy đủ; HINT cho MÃ SẢN PHẨM là gợi ý hướng — ghi rõ.

## Đầu ra — `$R/out/VERDICT.md` (ghi TĂNG DẦN: tạo khung ngay, cập nhật SAU MỖI HƯỚNG/MỤC)
```
verdict: approve | changes_requested | blocked
reviewed_sha: <SHA đầy đủ của 0ce1ad3>
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
