---
kieu: dac_ta_packet
packet: WINDOWS-BASH-NEN-ESCAPE
packet_id: WINDOWS-BASH-NEN-ESCAPE
packet_issue: 671
ban: r1
trang_thai: dong_bang_khi_dang_bam
nguon_cap_viec: >-
  Chủ kho, phiên Claude Code session_014dEtdMqShJhdQ8JfNbEeLU, 2026-09-29 ~05:37Z: "Cập nhật trạng thái và áp dụng
  các thay đổi. Tôi đồng ý cấp lease. Cho tôi prompt để thực hiện các nhiệm vụ của phiên này trong môi trường local
  có Windows". AskUserQuestion cùng phiên: thời điểm = "Cấp ngay, chấp nhận chồng" (với lease #668); phạm vi nợ
  CONG-CU-TEST-EP-UTF8 = "Gộp vào #671"; CI Windows = "Chỉ chạy tại máy".
ghi_chu_hinh_dang: Chưa cổng nào đọc tệp này. Nó là DỮ LIỆU cho lease và cho reviewer.
---

# `WINDOWS-BASH-NEN-ESCAPE` — docstring không raw trong `ops/bash_nen.py`, `t49` trên Windows, và ép UTF-8 cho `ops/cong_cu_test.py` (bản **r1**)

- `packet_id`: **`WINDOWS-BASH-NEN-ESCAPE`** · Issue **#671** · `revision`: 1 · `generation`: 1
- `review_class`: **`sensitive`** (cổng tính từ write set) · `risk`: `sensitive` · `depends_on`: `[]`
- `environment`: **`local` (Windows)** — packet đo hành vi CHỈ lộ ra trên Windows (§6: "parity Windows").
- executor: `anthropic_claude` · `claude_code` (phiên local trên máy Windows của chủ kho).
- base: `origin/master` **`1741e0a1ab7ebce4b26912aefadca56ddfcdc691`** (đo 2026-09-29T05:38Z).
- Chẩn đoán gốc (chỉ đọc, Linux): issues/671#issuecomment-5882828372.

## 1. Vấn đề đã đo

Run 36454930689, job `gate (windows-latest)`, bước 9: `cong_cu_test: 49/51 đạt`.

| ca | trạng thái trên Windows | nguyên nhân | mức chắc chắn |
|---|---|---|---|
| `t23_batch_chiu_duoc_stdout_CRLF_cua_python_windows` | ĐỎ | docstring `_tach_dinh_dang` (`ops/bash_nen.py:898`) không raw, chứa `\(` ⇒ Python ≥ 3.12 in `SyntaxWarning` kèm đường dẫn `C:\Users\runneradmin\...`; chốt `"\\r" not in p.stderr` bắt chuỗi `\r` trong `\runneradmin` | **ĐÃ ĐO** (log + tái hiện cơ chế trên Linux) |
| `t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC` | ĐỎ `(2) chiều ngược: … []` | INDEX rỗng. Giả thuyết B: Git for Windows không stage được tên mang surrogate lạc nên `git add -A` hỏng CẢ lượt; mã không đo `rc` | **GIẢ THUYẾT** — mô phỏng `add` rc=128 ra đúng nguyên văn; chưa đo trên Windows |

Giả thuyết A cho `t49` (cảnh báo làm bẩn đầu ra) đã **BỊ BÁC**: cảnh báo ra stderr, `t49` đọc stdout, JSON vẫn hợp lệ.

Nợ gộp (chủ kho: "Gộp vào #671") — `CONG-CU-TEST-EP-UTF8`, bàn giao từ phiên #570 (session_01C4h67GcQfkK937epXkvujJ),
nguồn: receipt land #581 (`5858656238`) và verdict r46 §2 (`5857766866`). Đo 27-09-2026 trên `42f2951`/`b7064f9`
(Linux, `PYTHONIOENCODING=ascii` chỉ cho tiến trình con): tự kiểm song song chốt (1) ĐỎ; `t29`, `t42`, `t45` chết bằng
lỗi VÔ CAN (`tin_dung_gia`) vì tiến trình cháu in chữ Việt ra stdout ASCII; chốt vận chuyển (3), (4a–f), (5), (6) vẫn
ĐẠT. CI che lỗi vì tự đặt `PYTHONIOENCODING=utf-8`/`PYTHONUTF8=1`; chạy tay trên Windows (cp1252/cp1258) sẽ ĐỎ oan.

## 2. Việc

**A — `t23` (bash_nen).** Đổi docstring `_tach_dinh_dang` sang `r"""`. Nội dung docstring phải KHÔNG đổi byte nào
(đo: sha256 của `ast.get_docstring(..., clean=False)` trước = sau). Ca khoá mới `t52_import_bash_nen_khong_in_gi_ra_stderr`
với HAI chốt độc lập: (1) `compile` dưới `warnings.simplefilter("error")`; (2) nạp thật trong tiến trình con `-B -W default`
từ BẢN SAO ở thư mục tạm MỚI, đòi stderr rỗng. Chốt (2) phải nạp từ bản sao — một `.pyc` cạnh nguồn thật làm nó câm (đã đo).

**B — `t49`.** Đặt ba tên byte thô (`xau_\xff`, `hong_\xff`, cặp `va_\xff`/`va_\\xff`) thẳng vào INDEX
(`hash-object -w --stdin` + `update-index --add -z --index-info`), ghi ra đĩa best-effort; tệp Unicode thường `git add`
riêng và đo `rc`. Không stage được ⇒ `BoQuaMoiTruong` (KHÔNG ĐO ĐƯỢC), không ĐỎ oan. BƯỚC ĐẦU trên Windows: ĐO giả
thuyết B TRƯỚC khi vá (chạy `t49` nguyên trạng, in `rc`/stderr của `git add -A` và `ls-files -z`). Nếu B sai thì DỪNG
phần B, ghi kết quả đo, hỏi chủ kho.

**C — ép UTF-8 (nợ gộp).** (a) `ops/cong_cu_test.py` ép stdout/stderr của CHÍNH nó sang UTF-8 trước khi in
(`reconfigure`, có `hasattr`). (b) Mọi tiến trình con/cháu nó phóng nhận `PYTHONIOENCODING=utf-8` và `PYTHONUTF8=1`
trong `env`. **Liệt kê hết điểm phóng bằng phép đo** (AST/grep mọi `subprocess.run`/`Popen`/`_chay`/`chay`/cửa
`--ban-kinh-con`), đừng vá theo danh sách đoán trước. Ca khoá mới: một ca con in chữ Việt dưới môi trường ASCII ⇒ phải
xanh; đột biến gỡ (b) ⇒ ca khoá ĐỎ. Nếu `t49` trên Windows cùng họ mã hoá (ĐO, không đoán) thì ghi rõ.

Bản vá tham chiếu cho A và B: `ops/specs/WINDOWS-BASH-NEN-ESCAPE-r1.patch`
(sha256 `59fcf3679e05cd5bd4689d5c3310ff3cf829d7b5300563734771b38375d4f011`), áp sạch lên `1741e0a` bằng `git apply`.
Đó là ĐIỂM XUẤT PHÁT đã đo trên Linux, không phải bằng chứng — executor dựng lại và đo lại trên Windows.

## 3. Write set — 2 đường

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `ops/bash_nen.py` | A: docstring raw |
| W2 | `ops/cong_cu_test.py` | A: ca `t52` · B: `t49` · C: ép UTF-8 + ca khoá |

Ba tệp khác cũng in `SyntaxWarning` (`ops/lease_publish_test.py` 2542/4500, `.claude/dev/packet_loop_test.py` 3673) —
**NGOÀI** write set; ghi thành nợ, không sửa.

## 4. Lệch có duyệt

- **Chồng write set với lease #668** (`ci-g5-cong-cu-chia-manh-r1-g1-claude`, còn hạn tới 2026-09-29T07:40:00Z, đang
  review lượt 13) trên `ops/cong_cu_test.py`. Chủ kho: "Cấp ngay, chấp nhận chồng". Hệ quả phải khai với người land:
  #668 đổi `cong_cu_test.py` (chế độ gate/mảnh/gom) và chia bán kính theo số ca; #671 THÊM ca (`t52`, ca khoá UTF-8) ⇒
  hai nhánh sẽ xung đột, và ai land sau phải merge base rồi đo lại. Executor KHÔNG đọc/chép mã từ nhánh #668.
- Gộp nợ `CONG-CU-TEST-EP-UTF8` vào packet này — chủ kho: "Gộp vào #671".
- Không `workflow_dispatch` — chủ kho: "Chỉ chạy tại máy". Nghiệm thu Windows = chạy tại máy Windows local.

## 5. Ngoài phạm vi

| thứ | lý do |
|---|---|
| `gate-registry` Windows quá trần 90' | quyết định riêng của chủ kho (Issue #671) |
| `bn_giu_bien_git_ke_thua` bán kính 2/51 · `t48` BỎ QUA trên Windows | chưa chẩn đoán; ghi quan sát nếu đo được, không vá |
| sửa `SyntaxWarning` ở tệp ngoài W1/W2 | ngoài write set |
| `.github/workflows/**` | cấm |

## 6. Tiêu chí xong (đo trên máy Windows local, và trên Linux/CI PR nếu có)

1. `python ops/cong_cu_test.py` trên Windows: `N/N đạt` với **hai số bằng nhau**; `t23`, `t49` không ĐỎ; ghi rõ số
   `bỏ qua` và lý do từng cái. Số lỗi đột biến so với NỀN `1741e0a` chạy trên CÙNG máy: **delta ≤ 0**.
2. Cùng bộ với tiến trình con ép ASCII (`PYTHONIOENCODING=ascii`, `PYTHONUTF8=0` cho con): N/N, 0 `tin_dung_gia` do
   mã hoá; tự kiểm song song ĐẠT.
3. Đột biến phản chứng, mỗi cái trên BẢN SAO TẠM: (i) `r"""` → `"""` ⇒ `t52` ĐỎ bằng tín hiệu của chính nó;
   (ii) gỡ ép UTF-8 cho tiến trình con ⇒ ca khoá UTF-8 ĐỎ, bán kính 1/N.
4. `python -m ruff check --select F` trên W1+W2: delta so nền = 0.
5. Nếu CI PR (ubuntu) chạy: xanh.

## 7. Điều kiện dừng

- S1 — chạm đường ngoài W1–W2 ⇒ DỪNG.
- S2 — giả thuyết B sai trên Windows ⇒ DỪNG phần B, báo số đo, hỏi chủ kho.
- S3 — > 300 dòng thêm hoặc > 2 tệp (trần ADR-0044 `sensitive`) ⇒ DỪNG, hỏi.
- S4 — hết hạn lease ⇒ ngừng ghi, handoff §7.
- S5 — cùng hình dạng finding ≥ 3 lần ⇒ hỏi chủ kho.

## 8. Chưa đo được lúc đóng băng

- Git for Windows có nhận tên mang surrogate lạc / mang `\` trong INDEX (`core.protectNTFS`) không.
- Bán kính `bn_doc_cay_lam_viec` trên Windows khi `va_\xff.py` không ghi ra đĩa được.
- Mô hình/effort thật của phiên executor local.
