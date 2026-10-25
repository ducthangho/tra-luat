# Đặc tả packet wp919 — ADR-0055: trần trục LỜI GỌI Codex mỗi PR 8 → 10 (revision 3)

- `packet_id`: **wp919** · `packet_issue`: **#919** · `mission_issue`: **#919**
- `revision`: **3** · `generation`: **3** · soạn 25-10-2026
- `executor`: **claude** (`model_family: claude`, `execution_surface: claude_code`) · `environment`: **cloud**
- `reviewer`: **codex** qua `.claude/dev/launcher.py run` (`reviewer_model_family: openai`) · `assurance_target`: `cross_approved`
- `branch`: **`agent/wp919-g1-claude`** (giữ nhánh của g1; commit cục bộ của g1 được kế thừa, chưa push)
- `risk` / `review_class`: **sensitive** (luật ngân sách review)
- `base`: `origin/master` @ `937162894e703dec9aa7c30163d913e2f83d276c`
- `depends_on`: `[]`

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

Hai dòng trên chọn trần cho CHÍNH packet này (8 lời gọi Codex; 6 tệp / 450 dòng thêm). Đã đo ba phép của
`ADR-0052`/`ADR-0053` trên clone không shallow, ref `origin/master` vừa fetch: OID chứa ADR (rc=0), cha
thứ nhất không chứa (rc≠0), nằm trên chuỗi first-parent — cả hai ADR đều land ở `8ab1007`.

## Revision này THAY THẾ TOÀN BỘ r2 (và r1)

r2: `ops/specs/wp919-adr-0055-tran-loi-goi-codex-muoi-r2.md`, sha256
`870bb1eea1def78a0b8ec35ced6cf0ded1e91253d69b6a9c6a98c0e914f573ab`, commit `2b828eb`. r3 chỉ đổi **một câu** của
Hợp đồng 2 (câu bất biến) và dòng revision; mọi mục khác chép nguyên từ r2. Lý do: cross-review Codex lượt 2 (`w919b`,
`launcher.py run` trên `0a5c5e5`, model phục vụ `gpt-6-astra`) bắt **WP919-R2-01 (P2)**: câu *"thêm một dòng khai không
bao giờ làm trần tăng"* mâu thuẫn với chính opt-in hợp lệ (không dòng nào ⇒ hai; thêm một dòng `ADR-0055` hợp lệ ⇒ mười).

## Lịch sử r1 → r2 (giữ để đọc ngược)

r1: `ops/specs/wp919-adr-0055-tran-loi-goi-codex-muoi.md`, sha256
`f5148028dbff30e31f55afc2db91543feb2c1063e148cab5de9ae93ee446b8a5`, commit `63d8c06`. r1 giữ nguyên làm hồ sơ,
không còn là nguồn thi hành. Lý do: cross-review Codex lượt 1 (`w919a`, `launcher.py run` trên `3868e92`, model
phục vụ `gpt-6-astra`) bắt **WP919-R1-02 (P2)**: Hợp đồng 4 của r1 đòi ADR khai *"0 cổng"* dựa trên tiền đề
*"`codex_review_calls_used` vẫn 0 dòng trong mã"* — tiền đề ấy **sai** từ merge `d8b15cb` (PR #779, 17-10-2026):
`packet_loop.py` có bộ đếm trong state, mặc định hai, chặn trước khi vượt. Không thể vừa thoả r1 vừa nói đúng sự
thật. Kèm theo, WP919-R1-01 (P2) chỉ ra luật phân xử của r1 §2 không đủ chặt; r2 ghi đúng luật đã thi hành.

## `nguon_cap_viec`

Chỉ thị chủ kho `ducthangho` trong phiên Claude Code ngày 25-10-2026, nguyên văn: *"Tôi duyệt trần 10, ghi vào
protocol luôn đi"*. Phạm vi chốt bằng câu hỏi trong cùng phiên, lựa chọn: **"10 lời gọi Codex / PR, mọi packet"** —
không nâng trần kích thước chung, không chỉ riêng một packet. Lease chỉ có hiệu lực khi chủ kho đăng comment cấp
quyền trên #919 neo `spec_hash` của tệp này.

Bối cảnh đo được: PR #909 (wp748 r25) dùng 5 lời gọi Codex trong khi đặc tả không có dòng khai nào ⇒ trần thực
tế là **hai** (fail-closed của `ADR-0052`); lần trước cùng lỗi là #892. Trần tám tự nó không cứu được ca ấy —
cứu là dòng khai; ADR mới phải nói thẳng điều đó.

## Write set hiệu lực

1. `docs/adr/0055-tran-loi-goi-codex-len-muoi.md` (tệp mới)
2. `docs/PROTOCOL_DA_PHIEN.md` (chỉ bảng §20)

## Hợp đồng

1. **ADR-0055 thay đúng một con số** của `ADR-0052`: trần trục LỜI GỌI Codex mỗi PR **8 → 10**. KHÔNG đổi: cách
   đếm lời gọi (lời gọi tính khi launcher có bằng chứng model đã sinh output, kể cả timeout/sai schema; lỗi
   preflight/permission/rate-limit trước output không tính); điều kiện cấp mọi lượt sau lượt đầu (còn P0/P1, còn
   finding cắt ngang, hoặc xác minh lại bản vá); mức dành sẵn **hai** lượt của `ADR-0041`; trục VÒNG
   (`ADR-0048`) và trục ATTEMPT; Review Rescue Checkpoint (`ADR-0037`) khi hết trần.
2. **Hiệu lực:** cùng luật OID land của `ADR-0052` (ba phép đo, so trên byte gốc), không hồi tố. *Dòng khai*
   `ADR-0055` là mọi dòng bắt đầu bằng `tran_loi_goi_codex: ADR-0055@`; hợp lệ khi khớp trọn
   `^tran_loi_goi_codex: ADR-0055@([0-9a-f]{40})$` và OID qua ba phép đo. Trần **mười** khi và chỉ khi có
   **đúng một** dòng khai `ADR-0055`, hợp lệ, và **không** có dòng khai `ADR-0052` nào. Có cả dòng `ADR-0052`
   hợp lệ ⇒ **tám** (trần thấp hơn). Dòng `ADR-0052` có mà không hợp lệ, hoặc dòng `ADR-0055` trùng / sai mẫu /
   sai phép đo / không đo được ⇒ **hai**. Không có dòng `ADR-0055` nào ⇒ kết quả theo `ADR-0052`, không đổi.
   Bất biến phải nói thẳng, đúng ba nghĩa: (a) thêm một dòng khai `ADR-0055` **không hợp lệ** không bao giờ làm
   trần tăng; (b) đặc tả đã chọn tám hoặc mười thì thêm bất kỳ dòng khai nào cũng không làm trần tăng; (c) không có
   dòng `ADR-0055` nào thì kết quả y hệt `ADR-0052`, kể cả cách nó so khớp nguyên văn. Trần chỉ đi lên nhờ một dòng
   opt-in hợp lệ — đó là chủ đích, không phải lỗ.
3. **Nói thẳng hệ quả trục VÒNG:** với mười, trần LỜI GỌI bằng trần VÒNG của `ADR-0048`; mục *"trần lời gọi
   chạm trước trần vòng"* của `ADR-0052` không còn đúng nguyên văn — ADR-0055 thay mục ấy bằng câu đúng cho mười.
4. **Khai đúng cổng, theo phép đo:** `packet_loop.py` có bộ đếm lời gọi trong state từ merge `d8b15cb`
   (PR #779) — `init --codex-review-calls-limit` (mặc định hai), `record-codex-call` chặn trước khi vượt,
   `nang-tran` nâng trần — nhưng **không** gì đọc dòng khai `tran_loi_goi_codex:` của đặc tả. ADR phải nói cả
   hai vế, và không khai mạnh hơn hồ sơ về việc một PR cụ thể có dùng bộ đếm hay không.
5. **Con số chỉ có một chỗ ở:** tệp ADR-0055. §20 thêm một dòng `ADR-0055` và sửa ô trạng thái dòng
   `ADR-0052` thành *"con số đã bị thay bởi `ADR-0055`"*; protocol không chép con số mười.
   Ô *"cổng"* của dòng `ADR-0052` được sửa theo phép đo của mục 4 (lời khai *"không có bộ đếm trong mã"* đã cũ).
6. **Không sửa** `ADR-0036/0037/0038/0041/0048/0052` hay đặc tả đóng băng nào.

## Chấp nhận

Chỉ thị chủ kho 25-10-2026 trong phiên: *"Thêm các lượt review tới hết P1, P2, P3. Không push, ko gate cho tới khi
đủ đk merge"* — tức review offline neo SHA cục bộ, mỗi lượt sau lượt đầu cấp vì còn finding, và nhánh code chỉ
được đẩy (kéo theo gate CI) một lần khi review đã sạch P0–P3.


- `python .claude/dev/packet_loop.py adr-song --root .` rc=0 với số ADR trên đĩa = số dòng §20 (ghi cả hai số).
- `python .claude/dev/packet_loop.py doctrine-scan --root .` rc=0.
- `git diff --numstat` so base: đúng hai tệp; trong trần `ADR-0053`.
- `git diff --check` sạch; gate CI xanh trên head cuối.
- Codex review qua `launcher.py run` trên head cuối: 0 P0/P1/P2/P3, biên nhận có `model_phuc_vu` nếu launcher của
  base đo được; chủ kho duyệt trên SHA cụ thể trước merge.

## Dừng

Dừng và báo khi: có người giữ chồng lấn; cần ghi ngoài write set (kể cả muốn sửa ADR cũ); `adr-song` hay
`doctrine-scan` đỏ vì lý do ngoài packet; hoặc chủ kho đổi phạm vi.
