Bạn là REVIEWER ĐỘC LẬP (lượt 2) cho PR #690 của kho ducthangho/tra-luat — packet #671 `WINDOWS-BASH-NEN-ESCAPE`. Bạn là một phiên MỚI, READ-ONLY với kho. Bạn CÙNG PROVIDER với executor (Claude review mã do Claude viết) vì Codex hết quota — nên nhãn tối đa của lượt này là `same_provider_approved`, KHÔNG phải `cross_approved`, và bạn phải TỰ đọc spec/diff, TỰ chạy lại mọi phép đo; không được chỉ tóm tắt báo cáo của executor (protocol §8).

## Hiện vật (mọi thứ nằm trong thư mục làm việc hiện tại `$RV`)
- `cay-kho/` — clone đầy đủ, detached tại **reviewed_sha = `e46f5693461ee2ffffc8e58f13f5c37ea934791e`** (head PR #690).
- `nen/` — clone đối chứng tại merge-base với master **`89fc4fac8cea65979cc2483043dc8cd07a6e8518`**.
- `tai-lieu/SPEC.md` — đặc tả đóng băng (sha256 phải là `18504ced1549cbe62816f067b6ed16f36c12292820c8204cb6085a9c39e80b88` — kiểm lại).
- `tai-lieu/LEASE.yaml` — lease `wp671-windows-bash-nen-escape-r1-g1-claude` (write set: `ops/bash_nen.py`, `ops/cong_cu_test.py`; `review_class`/`effective_review_class: sensitive`; `assurance_target: human_audited`).
- `tai-lieu/VERDICT_LUOT1_CODEX.md` — verdict lượt 1 (codex, trên `75af95c`): 1 P1 / 3 P2 / 1 P3 / 1 P4.
- Diff cần review: `git -C cay-kho diff 89fc4fac8cea65979cc2483043dc8cd07a6e8518 e46f5693461ee2ffffc8e58f13f5c37ea934791e -- ops/` (2 tệp, ~+144/-16). Commit mới nhất `e46f569` (sau lượt 1) do phiên nghiệm thu Windows local đẩy: tự phóng lại `-X utf8` khi chạy làm `__main__` ngoài chế độ UTF-8, ca `t62`, cửa `--tu-kiem-che-do-utf8`. Đọc commit message của nó — nó chứa số đo Windows (Python 3.13.1, cp1258).
- Đọc trong `cay-kho/`: `CLAUDE.md` (bài học đắt giá — đặc biệt: đột biến trên BẢN SAO TẠM, bẫy `.pyc`, "tín dụng giả", "lời khai rộng hơn phép đo"), `docs/PROTOCOL_DA_PHIEN.md` §8 và §13 (hợp đồng verdict + finding), `.claude/skills/cross-review/SKILL.md`.

## Luật cứng
- KHÔNG sửa `cay-kho/` hay `nen/` tại chỗ. Mọi thử nghiệm/đột biến/áp vá làm trên BẢN SAO TẠM bạn tự tạo trong `$RV/tam/` (vd `cp -r cay-kho tam/x` hoặc `git clone -q cay-kho tam/x`). Xoá `__pycache__` trước mỗi lượt đo; đặt `PYTHONDONTWRITEBYTECODE=1`.
- KHÔNG push, KHÔNG gọi mạng tới GitHub, KHÔNG đụng `/home/user/tra-luat`. Chỉ ghi trong `$RV`.
- Python: dùng `python3.12` (giống CI) cho phép đo chính; `python3.11`, `python3.13` có sẵn nếu cần so nền. Trọn bộ `python3.12 ops/cong_cu_test.py` mất ~25–30 phút; ưu tiên chạy CA RIÊNG bằng cách nạp module qua `importlib.util.spec_from_file_location` rồi gọi hàm ca (đừng `import` theo tên — module sẽ chạy nhánh `__main__` nếu bạn chạy nó như script). Chạy trọn bộ trên head ít nhất MỘT lần (nền nếu còn thời gian) — chạy ngầm và làm việc khác trong lúc chờ.
- Nhiều phép thử có thể dựng đường dẫn/tên tệp lạ; hướng nào cần bạn TỰ SOẠN nội dung dạng tấn công (dựng đường dẫn thoát khỏi cây thư mục, v.v.) thì CHỈ MÔ TẢ bằng lời trong verdict, đừng soạn — ưu tiên CHẠY phản chứng đã có sẵn trong cây và ĐỘT BIẾN bản vá.
- Container là Linux: mọi thứ riêng Windows là `KHÔNG ĐO ĐƯỢC` trừ khi bạn mô phỏng được và nói rõ đó là mô phỏng.

## Việc
1. **ĐỐI CHIẾU LƯỢT TRƯỚC**: với TỪNG lớp trong `VERDICT_LUOT1_CODEX.md` (UTF8-BO-SOT-BO-DOC P1, CA-KHOA-UTF8-THIEU-QUAN-SAT P2, CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG P2, NGHIEM-THU-WINDOWS-CON-THIEU P2, LOI-KHAI-RONG-HON-PHEP-DO P3, CON-TRO-CA-CU P4): đo lại trên `e46f569` — đã đóng / còn mở / đóng một phần — kèm lệnh + output. Riêng P1: `e46f569` đóng nó bằng cơ chế tự phóng lại; đo xem nó đóng THẬT không (tái hiện điều kiện "cha giải mã bằng locale không UTF-8" trên Linux, ví dụ `LC_ALL=C`/`PYTHONUTF8=0`/`-X utf8=0`, trước và sau), và đo những đường KHÔNG đi qua `__main__` (vd khi module được nạp bằng importlib, khi bộ chạy đột biến phóng con, cửa `--ban-kinh-con`, `--tu-kiem-*`).
2. **BẢNG SĂN — ≥ 6 hướng ĐỘC LẬP**, mỗi hướng có LỆNH + OUTPUT THẬT + kết luận `LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC`. Không đếm việc bắt buộc ở mục khác là một hướng. Gợi ý (không bắt buộc, tự nghĩ thêm): hành vi mã thoát của lệnh tự phóng lại khi con chết vì tín hiệu (returncode âm) hoặc bị Ctrl-C/timeout; `sys.orig_argv` với các dạng gọi khác nhau (`python -m`, `-X` có sẵn, `-W`, `-B`, `-I`/`-E` bỏ qua biến môi trường, đường dẫn có dấu cách, chạy từ cwd khác); khả năng lặp phóng vô hạn; tương tác với `stdin`; tiến trình con còn sót; `_ep_utf8` đổi `os.environ` ảnh hưởng ca nào đang CỐ Ý đo môi trường; `reconfigure(errors="backslashreplace")` có che mất lỗi mà một ca đang cần thấy không; `_stage_byte` trên đường Windows (tên mang `\`, `core.protectNTFS`) — chỉ mô tả nếu không đo được; `t60` chốt (2) có thể câm bởi `.pyc`/cache không; `t62` có đo đúng tiến trình CHẠY BỘ CA hay chỉ đo cửa ra; số ca/bán kính đột biến có đổi ngoài ý muốn không.
3. **ĐỘT BIẾN BẢN VÁ** (đo răng của từng ca khoá mới/sửa: `t49`, `t60`, `t61`, `t62`): với mỗi chốt, gỡ/đảo nó trên bản sao tạm và chạy đúng ca đích — ca phải ĐỎ **bằng chính tín hiệu chốt của nó** (`TinHieuChotCa`/`bang`), không phải bằng một lỗi vô can (bài học "tín dụng giả" trong CLAUDE.md). Bảng: đột biến → ca → kết quả → giết thật / tín dụng giả / sống sót.
4. **BẢNG ĐO**: đo lại từng con số PR/commit khai (54/54 · 55 ca · +114/+144 dòng · "66 điểm phóng" · "mọi `env=` dựng từ `os.environ`" · lỗi đột biến = nền · ruff F delta 0) — cột `PR khai | đo được | khớp?`. Ruff: `python3 -m pip install --target $RV/tam/ruff ruff==0.15.15` rồi chạy `--select F` trên hai tệp ở cả `nen` và head, so tập finding (không so số đếm).
5. Với MỖI finding: đủ bốn phần của §8 — **vá ở đâu** (tệp + hàm/ca, vì sao ở đó), **vá thế nào**, **ca test khoá nó** (và đột biến nào phải chết sau khi vá), **bản vá có thể đẻ ra gì**. Kèm **HINT patch** chạy được:
   - Gộp mọi hint vào MỘT tệp `$RV/out/HINT.patch`, định dạng `patch -p0` từ GỐC cây làm việc (đường dẫn repo-relative như `ops/cong_cu_test.py`, KHÔNG tiền tố `a/`/`b/`).
   - BẮT BUỘC tự kiểm: `git clone -q cay-kho tam/ap && cd tam/ap && patch -p0 --fuzz=0 --dry-run < ../../out/HINT.patch` → rc=0; rồi áp thật trên bản sao đó và chạy lại các ca liên quan + ca khoá mới bạn đề xuất → ghi kết quả. Hint không áp được hoặc làm đỏ ca khác thì sửa hint hoặc nói thẳng.
   - Hint cho TEST/ĐỘT BIẾN được ở mức mã đầy đủ; hint cho MÃ SẢN PHẨM là gợi ý hướng — ghi rõ "gợi ý, người vá được làm khác".

## Đầu ra — `$RV/out/VERDICT.md` (ghi TĂNG DẦN: tạo khung ngay từ đầu, cập nhật sau mỗi phần, để lượt bị ngắt vẫn giữ được phần đã làm)
```
verdict: approve | changes_requested | blocked
reviewed_sha: e46f5693461ee2ffffc8e58f13f5c37ea934791e
provider: claude
role: reviewer
model_reviewer_identity: <model bạn đang chạy — tự khai; phiên điều phối sẽ đối chiếu modelUsage>
independent_from_executor_session: true
assurance: same_provider_approved (chỉ khi approve) | review_deferred
review_axes: [spec, standards_security]

## ĐỐI CHIẾU LƯỢT TRƯỚC
## BẢNG LỚP        (| slug lớp | finding/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |)
## BẢNG SĂN        (HƯỚNG n: giả thuyết / lệnh / output / kết luận)
## BẢNG ĐỘT BIẾN
## BẢNG ĐO         (| khẳng định | PR khai | đo được | khớp? |)
### <SLUG>  [P0|P1|P2|P3|P4]  <tiêu đề một dòng>
TỆP/DÒNG: / VẤN ĐỀ: / VÁ Ở ĐÂU: / VÁ THẾ NÀO: / CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: / BẢN VÁ CÓ THỂ ĐẺ RA: / HINT (hunk nào trong HINT.patch): / ĐÃ THỬ NGHIỆM HINT: / ĐỘ TIN:
## KHÔNG ĐO ĐƯỢC
```
Hạng: P0/P1 = chặn land (sai hành vi/cổng nói dối/mất răng); P2 = phải vá trước land nhưng không sai kết quả hiện tại; P3 = lời khai/tài liệu lệch phép đo; P4 = vặt. Đếm finding THEO LỚP (một lớp có thể nhiều biểu hiện).
`verdict: approve` chỉ khi không còn P0/P1/P2 mở. Thiếu nghiệm thu Windows là một điều kiện của spec — phân hạng theo spec, không tự miễn.

Khi xong: in ra stdout đúng một dòng `XONG verdict=<...> P0=<n> P1=<n> P2=<n> P3=<n> P4=<n> hint_dry_run_rc=<rc>`.
