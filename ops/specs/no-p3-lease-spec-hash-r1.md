# Đặc tả packet `no-p3-lease-spec-hash` r1 — nợ P3 (b1): `lease_publish.py check` đối chiếu băm spec và write set

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-lease-spec-hash` |
| `packet_issue` | #751 |
| `revision` | 1 |
| `nguon_cap_viec` | Sổ nợ P3 mục 4: review wp685 lượt 2–5 đo `lease_publish.py check` không đọc `spec_hash`, `spec_sha256_required`, `plan_hash`, `write_set_hash`, `spec_path` (VERDICT review lượt 5 r28 sha256 `d3f1d9db4896efe8c1b62112a3d0aa479b64c5dc110da1d323b3297d7e7c45fb`, M11: đột biến D2, D3, D5, D6, D7 cho rc=0 cả năm). Ngưỡng chủ kho #698 `6094652521`. Cách tách và phạm vi do chủ kho chốt 15-10-2026 (Q7, Q8). |
| `review_class` | **sensitive** — `ops/lease_publish.py` là cổng cấp lease (authority). Trần ADR-0044: ≤ 3 tệp, ≤ 300 dòng thêm. |
| `executor` · `reviewer` | Claude (executor). Reviewer: subagent Claude Sonnet (`review_deferred`) BẮT BUỘC; thêm một lượt Codex (`cross_approved`) nếu đăng nhập Codex làm mới được trước lúc review. Chỉ P1/P2 chặn merge. |
| `base` | `origin/master` `6f121a3810045af27bf65eb723edf36b29e387f2` (đo 15-10 ~06:10Z). |
| `write_set` | `ops/lease_publish.py` · `ops/lease_publish_spec_hash_test.py` (MỚI) |
| `kich_thuoc` | 2 tệp; ước ≤ 280 dòng thêm (đơn vị: dòng thêm theo `git diff --numstat`), trong đó `lease_publish.py` ≤ 90. |

## Số đo nền (đo 15-10-2026 ~06:15Z trên cây `origin/master` `6f121a3`, đơn vị ghi rõ)

- Bảng mã thoát hiện có: `RC_OK 0`, `RC_THAM_SO 2`, `RC_TU_CAP 4`, `RC_NEO 6`, `RC_NOI_DUNG 8`, `RC_DA_DANG 9`, `RC_LOP 10`,
  `RC_DANG_GIU 11`, `RC_KHONG_XAC_DINH 12` (`ops/lease_publish.py` dòng 44–52). Mã `13` chưa dùng.
- 150 tệp `ops/leases/*.yaml`. 97 lease có cả `spec_path` và (`spec_hash` hoặc `spec_sha256_required`): 92 khớp băm tệp
  spec ĐANG Ở master, 5 lệch (spec cùng đường dẫn đã đổi sau khi cấp, hoặc lease trỏ revision khác) — đây là lý do phép so
  phải đọc spec **tại ref chứa lease**, không tại cây làm việc.
- 59 lease có `write_set` và `write_set_hash`: 5 lease khai `write_set_hash_scope: sorted NFC casefold exact …` và khớp công
  thức (a) dưới đây; **54 lease không khai scope** và KHÔNG khớp công thức (a) — chúng dùng công thức cũ khác (ví dụ "cách 1/
  cách 2" của wp685, VERDICT lượt 5 M10). Lease mẫu kiểm tay: `wp748-r9-g9-claude-windows-20261015` `3cd3f09c…` khớp (a).

## Mục tiêu

1. **[`ops/lease_publish.py`] Băm spec.** Trong `kiem(...)` (đường của lệnh `check` và `kiem-thu-hoi-github`): nếu lease có
   `spec_path` (chuỗi) VÀ ít nhất một trong `spec_hash`, `spec_sha256_required` (chuỗi 64 hex thường), đọc **blob** của
   `spec_path` tại cùng gốc/ref mà `kiem` đang đọc lease (không đọc cây làm việc), tính sha256 byte thô và so với **mọi**
   trường băm có mặt. Lệch ⇒ `Chan(RC_SPEC_LECH, …)` với `RC_SPEC_LECH = 13` mới, thông điệp nêu trường, giá trị khai, giá trị
   đo. Tệp spec vắng tại ref ⇒ `Chan(RC_SPEC_LECH, …)` (fail-close; khai băm mà không có tệp là lời khai không kiểm được).
   Hai trường băm cùng có mặt mà khác nhau ⇒ `RC_SPEC_LECH`. Thiếu `spec_path` hoặc thiếu cả hai trường băm ⇒ **không kiểm,
   không đỏ** (lease cũ); dòng kết quả của `check` phải nói rõ "spec: không khai — không kiểm".
2. **[`ops/lease_publish.py`] Băm write set.** Nếu lease có `write_set` (danh sách chuỗi), `write_set_hash` VÀ
   `write_set_hash_scope` bắt đầu bằng `sorted NFC casefold exact`: tính (a) =
   `sha256(json.dumps(sorted(unicodedata.normalize("NFC", p).casefold() for p in write_set), ensure_ascii=False, separators=(",", ":")).encode("utf-8"))`
   và so; lệch ⇒ `RC_SPEC_LECH`. Scope vắng hoặc giá trị khác ⇒ **không kiểm, không đỏ**, và `check` in "write_set_hash:
   scope không nhận ra — không kiểm" (54 lease cũ ở trên rơi vào nhánh này).
3. **[`ops/lease_publish.py`] Dòng xác nhận là bằng chứng.** Khi kiểm đạt, `check` in băm ĐO được (12 ký tự đầu) cho spec và
   write set — theo đúng nếp docstring `kiem` (dòng 1010–1016): dòng xác nhận phải đi kèm việc kiểm. Bổ sung `RC_SPEC_LECH`
   vào bảng mã thoát của `--help`.
4. **[`ops/lease_publish_spec_hash_test.py`] Phản chứng.** Bộ test MỚI, tự đứng (không import `ops/lease_publish_test.py`,
   vì tệp đó đang thuộc write set #748), dựng kho git tạm bằng `git init` trong thư mục tạm, commit spec + lease, gọi
   `lease_publish.py check` như tiến trình con và đọc rc + stdout. Chạy được bằng `python -B ops/lease_publish_spec_hash_test.py`,
   in `N/N` và trả 0 khi đạt.

## Nghiệm thu

- **A1 (băm spec khớp ⇒ qua):** lease có spec khớp ⇒ rc 0, stdout chứa 12 ký tự đầu băm đo. ĐỎ khi: đột biến gỡ dòng in ⇒
  ca kiểm chuỗi in ĐỎ.
- **A2 (lệch ⇒ 13):** sửa 1 ký tự `spec_hash` ⇒ rc 13; sửa 1 ký tự `spec_sha256_required` ⇒ rc 13; thêm 1 byte vào spec SAU
  khi tính băm ⇒ rc 13; `spec_path` trỏ tệp vắng ⇒ rc 13; hai trường băm khác nhau ⇒ rc 13. Năm ca riêng. ĐỎ khi: đột
  biến gỡ phép so trong `lease_publish.py` ⇒ ít nhất bốn ca ĐỎ (rc 0 thay vì 13) — đột biến chạy trên BẢN SAO tạm
  (CLAUDE.md: đột biến không ghi tệp thật).
- **A3 (đọc tại ref, không tại cây làm việc):** commit spec + lease, rồi sửa spec trong cây làm việc KHÔNG commit ⇒ rc 0
  (đọc blob); và ngược lại commit spec sai + cây làm việc đúng ⇒ rc 13. ĐỎ khi: đột biến đổi sang đọc tệp từ đĩa ⇒ cả hai
  ca ĐỎ.
- **A4 (write set):** scope `sorted NFC casefold exact …` + băm đúng ⇒ rc 0; sai 1 ký tự ⇒ rc 13; đổi thứ tự `write_set`
  (băm giữ) ⇒ rc 0 (vì sắp xếp); một đường dẫn viết hoa khác (casefold) ⇒ rc 0; dạng NFD của cùng tên ⇒ rc 0. ĐỎ khi: đột biến
  bỏ `casefold` ⇒ ca viết hoa ĐỎ; bỏ `normalize` ⇒ ca NFD ĐỎ; bỏ `sorted` ⇒ ca đổi thứ tự ĐỎ — ba đột biến, mỗi cái một ca.
- **A5 (lease cũ không đỏ):** lease không `spec_path` ⇒ rc 0 và stdout chứa "không khai — không kiểm"; lease có
  `write_set_hash` không scope ⇒ rc 0 và chứa "scope không nhận ra". ĐỎ khi: đột biến coi thiếu trường là lỗi ⇒ hai ca ĐỎ.
- **A6 (không hồi quy):** chạy `python -B ops/lease_publish.py check <lease>` trên cây `git archive` của base với 5 lease
  hiện hành gần nhất trên các nhánh `ops/**` (chọn và liệt kê lúc thi hành, đo lại theo L5): rc trước/sau bản vá bằng nhau,
  trừ các ca lệch băm thật — mỗi ca lệch phải liệt kê kèm lý do. Bộ test hiện có `ops/lease_publish_test.py` chạy trên
  ứng viên: số ca đạt bằng base (delta 0). ĐỎ khi: bất kỳ ca nào của `lease_publish_test.py` đổi từ đạt sang trượt.
- **A7 (cổng kho):** ruff F delta 0 (multiset) cho hai tệp; CI PR xanh (gồm `gate-ops`); kích thước ≤ trần sensitive. ĐỎ khi:
  `git diff --numstat` vượt 300 dòng thêm hoặc 3 tệp.

## Ngoài phạm vi (cố ý)

- `plan_hash`: không có quy ước chung về tệp plan (chủ kho chốt Q8).
- Sửa `ops/lease_publish_test.py`, `ci.yml` (đang thuộc write set #748); gắn test mới vào CI — ghi nợ cho packet sau #748.
- Sửa 54 lease cũ hay 5 lease lệch băm ở master — không phải việc của cổng mới; chúng không bị kiểm lại trừ khi được đăng.

## Hình dạng kế thừa

Chép từ lịch sử cổng `lease_publish.py` (CLAUDE.md, các mục "BIA MỘ", "rc=8 che rc=9", `t32`): (a) **chốt chạy trước che
chốt sau** — `kiem()` ném `rc=8` cho lease hết hạn TRƯỚC khi `rc=9` kịp chạy; chốt băm mới phải đặt ở vị trí không che và
không bị che bởi chốt hạn/đăng — executor khai vị trí và lý do; (b) **dòng xác nhận không đi kèm việc kiểm** (docstring
`kiem`) — A1 khoá. Đếm hình dạng: (a) đã gặp 1 lần (20-09-2026), (b) 1 lần. Lặp lần ba bất kỳ hình dạng nào ⇒ dừng, hỏi
chủ kho có nên tiếp không (L4).

## Chưa đo được

- Hành vi trên Windows (đường dẫn, NFC trên NTFS) — packet chỉ đo Linux; ghi `KHÔNG ĐO ĐƯỢC`.
- Lượt Codex có chạy được không phụ thuộc làm mới đăng nhập (đo 15-10: `SAP_HET_HAN`, ảnh chụp cũ ~185 h).
