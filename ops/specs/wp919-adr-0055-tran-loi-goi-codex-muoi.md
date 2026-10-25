# Đặc tả packet wp919 — ADR-0055: trần trục LỜI GỌI Codex mỗi PR 8 → 10 (revision 1)

- `packet_id`: **wp919** · `packet_issue`: **#919** · `mission_issue`: **#919**
- `revision`: **1** · `generation`: **1** · soạn 25-10-2026
- `executor`: **claude** (`model_family: claude`, `execution_surface: claude_code`) · `environment`: **cloud**
- `reviewer`: **codex** qua `.claude/dev/launcher.py run` (`reviewer_model_family: openai`) · `assurance_target`: `cross_approved`
- `branch`: **`agent/wp919-g1-claude`**
- `risk` / `review_class`: **sensitive** (luật ngân sách review)
- `base`: `origin/master` @ `937162894e703dec9aa7c30163d913e2f83d276c`
- `depends_on`: `[]`

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

Hai dòng trên chọn trần cho CHÍNH packet này (8 lời gọi Codex; 6 tệp / 450 dòng thêm). Đã đo ba phép của
`ADR-0052`/`ADR-0053` trên clone không shallow, ref `origin/master` vừa fetch: OID chứa ADR (rc=0), cha
thứ nhất không chứa (rc≠0), nằm trên chuỗi first-parent — cả hai ADR đều land ở `8ab1007`.

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
2. **Hiệu lực:** cùng luật OID land của `ADR-0052` (ba phép đo, so trên byte gốc), token riêng
   `^tran_loi_goi_codex: ADR-0055@([0-9a-f]{40})$`, **đúng một** dòng. Không hồi tố. Đặc tả có dòng khai
   `ADR-0052` hợp lệ mà không có dòng `ADR-0055` ⇒ vẫn tám. Không có dòng nào hợp lệ ⇒ hai (như cũ). Có CẢ HAI
   token, hoặc trùng ⇒ ADR phải nói rõ một kết luận fail-closed (lấy trần thấp hơn).
3. **Nói thẳng hệ quả trục VÒNG:** với mười, trần LỜI GỌI bằng trần VÒNG của `ADR-0048`; mục *"trần lời gọi
   chạm trước trần vòng"* của `ADR-0052` không còn đúng nguyên văn — ADR-0055 thay mục ấy bằng câu đúng cho mười.
4. **Không cổng nào đếm lời gọi** (`codex_review_calls_used` vẫn 0 dòng trong mã — đo lại khi viết, khớp nguyên
   từ) ⇒ ADR khai **0 cổng** và nêu bài học: thiếu dòng khai thì trần là hai, bất kể ADR mới nhất.
5. **Con số chỉ có một chỗ ở:** tệp ADR-0055. §20 thêm một dòng `ADR-0055` và sửa ô trạng thái dòng
   `ADR-0052` thành *"con số đã bị thay bởi `ADR-0055`"*; protocol không chép con số mười.
6. **Không sửa** `ADR-0036/0037/0038/0041/0048/0052` hay đặc tả đóng băng nào.

## Chấp nhận

- `python .claude/dev/packet_loop.py adr-song --root .` rc=0 với số ADR trên đĩa = số dòng §20 (ghi cả hai số).
- `python .claude/dev/packet_loop.py doctrine-scan --root .` rc=0.
- `git diff --numstat` so base: đúng hai tệp; trong trần `ADR-0053`.
- `git diff --check` sạch; gate CI xanh trên head cuối.
- Codex review qua `launcher.py run` trên head cuối: 0 P0/P1/P2, biên nhận có `model_phuc_vu` nếu launcher của
  base đo được; chủ kho duyệt trên SHA cụ thể trước merge.

## Dừng

Dừng và báo khi: có người giữ chồng lấn; cần ghi ngoài write set (kể cả muốn sửa ADR cũ); `adr-song` hay
`doctrine-scan` đỏ vì lý do ngoài packet; hoặc chủ kho đổi phạm vi.
