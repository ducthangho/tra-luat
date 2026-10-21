# Cross-review độc lập — Packet #856 (`KG-RANG-TEST-2`) revision 1, lượt 3, OFFLINE trên SHA cục bộ

Bạn là reviewer Codex, khác họ với executor (Claude). Bạn chỉ ĐỌC kho: KHÔNG sửa tệp nào trong `KHO`. Chỉ ghi vào thư mục ra
(thư mục làm việc hiện tại) hoặc /tmp. Kết quả bắt buộc là tệp `VERDICT.md` trong thư mục ra. Nếu có finding thì kèm
`HINT.patch` cho các lớp phức tạp: một diff gợi ý, áp được bằng `git apply` trên exact head, và CHỈ chạm
`.claude/dev/packet_loop_test.py`. Ghi `VERDICT.md` TĂNG DẦN trong lúc làm, để lượt bị ngắt vẫn giữ được phần đã ghi.

## Định danh (băm là định danh, không phải tên nhánh)

- Kho `ducthangho/tra-luat`, bản sao đầy đủ (không shallow) tại `KHO=/home/user/rv856`, detached ở exact head.
- Exact head: `bf671b0524a8472eb0b0fcd1d75ea3a89d1f6973`. Kiểm bằng `git -C KHO rev-parse HEAD`. Dòng 1 của VERDICT phải là `Reviewed commit: <sha40 đó>`.
- Base: `94220547cd155c73392e95726e8daf353888b3aa`. Diff cần review: `git -C KHO diff 9422054 HEAD`, đúng 1 tệp
  `.claude/dev/packet_loop_test.py`. Nhánh chưa đẩy, chưa có PR.
- Đặc tả: `ops/specs/wp856.md`, sha256 `d50065e79fcb92c223fc1799418e266579e339b4033cc509ef22a083e6e8dd34`; phụ lục
  `ops/specs/wp856-dot-bien-r6.json`, sha256 `6b1c41958fb36eaeef35d32bd03c424ef7a90e5ab2d8a32cc7d67bc8bea9e85d`. Cả hai ở ref
  `origin/ops/wp856-spec` trong KHO: `git -C KHO show origin/ops/wp856-spec:ops/specs/wp856.md | sha256sum`. Đọc TRỌN `tap_toan_tu`
  T1–T6, `muc_tieu` M1–M4, `nghiem_thu` A1–A8, `dieu_kien_dung`.
- Lease: `git -C KHO show origin/ops/wp856-spec:ops/leases/wp856-r1-g1-claude.yaml`. Write set chỉ gồm
  `.claude/dev/packet_loop_test.py`; mã sản phẩm `.claude/dev/packet_loop.py` KHÔNG được đổi.
- Bối cảnh: packet #822 land ở PR #851 với 6 lớp P2 còn mở (VERDICT lượt 6 ở `git -C KHO show
  origin/ops/wp822-g1-reviews:ops/reviews/wp822-r1-g1-exec-review-6-codex/VERDICT.md`). Packet này đóng chúng bằng một TẬP TOÁN TỬ CỐ ĐỊNH.
- Ngân sách: đây là lời gọi Codex **3/8** của packet (gồm cả một lượt connector sau khi đẩy).
- **Lượt 1** (trên `7302ea3`): bị cắt khi container khởi động lại; VERDICT tăng dần ghi `P2=4`: `so-khop-tuyet-doi-chua-du`,
  `so-khop-so-nguyen-chua-chinh-xac`, `chuan-hoa-doi-so-chi-trong-phep-kiem`, `fixture-vi-pham-nhieu-chot`. Hiện vật: `/tmp/claude-0/-home-user-tra-luat/3aad6106-b796-579e-a532-bf98ecdf8fe7/scratchpad/rv1_hienvat_ro`.
- **Lượt 2** (trên `19fdfa6`): `changes_requested — P0=0 P1=0 P2=3 P3=0`: `kiem-kieu-chi-do-mot-loai-sai` (18 hiện thực ép kiểu sống),
  `so-khop-tuyet-doi-chua-du` (77 chỉ số giữa + 11 hiện thực `x == y or …` sống), `so-khop-so-nguyen-chua-chinh-xac` (2 ô `id_max`
  tiền tố khai `khong_ap_dung` sai). Hiện vật (gồm evidence và HINT): `/tmp/claude-0/-home-user-tra-luat/3aad6106-b796-579e-a532-bf98ecdf8fe7/scratchpad/rv2_hienvat_ro` (chỉ đọc).
  Executor đóng theo lớp ở `bf671b0`: T1 thêm 13 miền giá trị ÉP ĐƯỢC × mọi vị trí đặt + 26 đột biến; T2 họ biến thể phủ MỌI chỉ số,
  ảnh f(t), đích đã sắp xếp/không chuẩn, hiện thực `hoặc` cho mọi ô trái/phải (2 ô hằng chưa sắp khai tương đương), và ca
  `kg_t2_phu` tính bằng hàm cùng nghĩa rằng mọi toán tử × mọi chỉ số giữa × phía × (thuần | hoặc) có mục giết; T3 `id_max` tiền tố
  qua `cmp_to_key`. Executor phát lại 110 hiện thực từng sống của lượt 2 trên head này (đã trừ các ô đang khai tương đương):
  ≥107 GIẾT, các mục còn lại đang chạy. Thay đổi kể từ lượt 2: `git -C KHO diff 19fdfa6 HEAD`.
- **ĐIỀU KIỆN DỪNG của đặc tả:** một lớp xuất hiện ở lượt thứ 3 ⇒ executor dừng và hỏi chủ kho. Vì vậy hãy đặc biệt xác minh hai lớp
  so khớp (đã có ở lượt 1 và 2) bằng PHÉP ĐO; chỉ báo khi có hiện thực không sập, không tương đương, thật sự sống trong tập.
  Mục bắt buộc trong VERDICT: **ĐỐI CHIẾU LƯỢT TRƯỚC** — mỗi lớp lượt 1–2 một nhãn: đã vá thật / vá hờ / vá sinh lỗi mới.

## PHẠM VI CHẤM = `tap_toan_tu` của đặc tả — luật của packet này

Qua 6 lượt của #822, mỗi lượt reviewer mở thêm một chiều quét mới nên số lớp không giảm. Chủ kho đã chốt (#856): **reviewer
CHỈ chấm trong `tap_toan_tu` (T1–T6)**. Một ô "vị trí × toán tử" của bảng T1–T5 là một biểu thức trong `_doc_check_runs` hoặc
`cmd_kiem_gate` trên base, kèm một toán tử của đúng hàng ấy. Ô đạt khi có một trong hai: (i) đột biến SINH BẰNG VÒNG trong
`MUTANTS`, có dòng trong `_KG_KIEM_KE`, bị giết KHÔNG SẬP (chuẩn M6 của #822) bởi fixture chỉ vi phạm đúng chốt ấy; hoặc
(ii) dòng `tuong_duong` mà lập luận đứng vững: với MỌI đầu vào, CLI dưới đột biến cho cùng rc, stdout, stderr.

- Đột biến hay finding NGOÀI tập toán tử: ghi ở mục "Ngoài phạm vi" của VERDICT, KHÔNG tính hạng. Nếu bạn thấy một chiều
  ngoài tập đáng đưa vào tập, nói rõ ở mục ấy (đưa vào hay không là quyết định của chủ kho).
- Executor ghi ma trận ô vào `_KG_MA_TRAN` trong tệp test: khoá `(họ, vị trí, toán tử)`, giá trị là tên đột biến hoặc
  `("tuong_duong" | "khong_ap_dung", lập luận)`. Đọc nó như LỜI KHAI cần kiểm, không phải bằng chứng. Executor có thể đã hiểu sai
  một hàng của bảng (cách chọn vị trí, cách hiện thực một toán tử). Khi thấy hiểu sai, báo theo lớp.

## Cách review — chuẩn connector, KHÔNG lọc

Review như connector review PR: tìm MỌI lỗi thật trong phạm vi chấm. Phạm vi gồm tính đúng đắn, test không đo gì, tín dụng
giết giả, ca đích bị chốt khác chặn hộ, lệch đặc tả, và hồi quy (ca nào của base vắng mặt hoặc đổi màu). Không lọc theo
"mô hình tin cậy".

**Tìm theo LỚP, không theo lỗi riêng lẻ.** Khái quát mỗi biểu hiện thành một lớp, rồi quét MỌI biểu hiện cùng lớp trước
khi báo. VERDICT có bảng lớp gồm các cột: `slug` · hạng (`P0`–`P3`) · biểu hiện (file:dòng) · phép đo đã chạy · hướng vá.
Lớp phức tạp thì kèm HINT.

## Nhiệm vụ — ĐO, đừng chỉ đọc

1. **A4 (trọng tâm).** Tự dựng ma trận vị trí × toán tử của `tap_toan_tu` trên base, ĐỘC LẬP với `_KG_MA_TRAN`, rồi đối chiếu.
   - Ô áp dụng được mà không có gì ⇒ finding.
   - Ô mà đột biến của executor không hiện thực đúng toán tử ⇒ finding. Ví dụ: hiện thực yếu hơn toán tử, hoặc chỉ một chiều trong khi bảng đòi "cả hai phía và từng phía".
   - Ô `tuong_duong`: thử dựng fixture phân biệt. Ca `kg_t_bo_de` đo các bổ đề Unicode mà lập luận dựa vào; kiểm cả bổ đề lẫn bước suy từ bổ đề ra kết luận.
   - Với mỗi ô: dựng **hiện thực KHÁC** của cùng toán tử (dạng `cho qua` hay `bỏ qua`, dạng ép kiểu hay nới kiểu), không sập, rồi chạy MỌI ca `kg_*` dưới nó. Nếu không ca nào đỏ thì đó là finding trong tập.
2. **A1/A3 — ca đích đo đúng chốt.**
   - Với từng đột biến của tập: chạy CLI `kiem-gate` dưới đột biến (bản sao tạm `packet_loop.py`) trên fixture của ca đích.
   - Ca đích phải đỏ vì CHÍNH chốt ấy. Ca chết vì một chốt khác chặn hộ, hoặc vì sập, là finding.
   - T6: `kg_t6_ban_sua` (bản sửa của mọi fixture từ chối được sinh, cộng 18 ca đối số cũ của #822, phải ra rc 0) và `kg_t6_co_rang`. Gỡ phép tự kiểm thì ca phải ĐỎ. Nếu một fixture từ chối được sinh mà không có bản sửa, hoặc bản sửa khác fixture ở hơn một chốt, thì đó là finding.
3. **A2 — phát lại phụ lục.** Phát lại 75 đột biến của `wp856-dot-bien-r6.json` trên head.
   - Mỗi đột biến chạy trên bản sao tạm, qua `chay_suite` + `_phan_loai_giet` trên mọi ca `kg_*`.
   - Đòi 75/75 GIẾT, 0 tín dụng giả. Ghi tên từng đột biến kèm ca giết nó.
4. **M4 — M5/M6 của #822 giữ nguyên.** `kg_m5_kiem_ke` và `kg_m6_tin_dung_giet` vẫn có răng. `_kg_ho` (bộ chạy mới) không được rửa cú sập thành GIẾT: một mục sập rồi mục sau đỏ sạch là GIẾT, chỉ-sập là TIN_DUNG_GIA. Có `kg_t_ho_sap` và các đột biến `t856_*` để đo.
5. **Gate.** Chạy suite trong BẢN SAO TẠM: `cp -a KHO /tmp/x && python3 -B /tmp/x/.claude/dev/packet_loop_test.py`.
   - Đòi `nền: N/N` với hai số bằng nhau, mọi đột biến bị giết, và `TỔNG: ĐẠT`.
   - A6: mọi tên ca của base có mặt ở head với cùng màu.
   - A7: `doctrine-scan`/`adr-song` có rc như base; ruff F delta 0 (executor đo base 2 F541, head 2 F541).
   - A8: `git -C KHO diff --numstat 9422054 HEAD` ra đúng 1 tệp. Số dòng thêm KHÔNG có trần và không tính là finding.
   - Executor chạy gate đầy đủ trên chính SHA này SONG SONG với lượt review này (chưa có số). Lượt trước, trên `19fdfa6`:
     `nền: 863/863 · BỎ QUA: 1 · TỔNG: ĐẠT`. Hãy tự chạy gate trên bản sao của bạn; đừng nhận lời khai.

## Phân công — KHÔNG tự soạn nội dung nhạy cảm (lượt 2 của #822 chết đúng vì việc này. Lượt 1 của packet này bị cắt do container khởi động lại — GHI VERDICT TĂNG DẦN)

1. Mọi phản chứng M6 về traceback/sập **đã nằm sẵn trong cây**: `kg_m6_tin_dung_giet`, `kg_t_ho_sap`, các đột biến `t822_m6_*` và
   `t856_*`. **CHẠY** chúng, và **ĐỘT BIẾN BẢN VÁ** (trên bản sao tạm) để đo răng của từng chốt.
2. **KHÔNG tự viết mã in, giả hay bọc traceback, và không soạn payload gây sập.** Hướng thử nào cần thứ đó thì MÔ TẢ BẰNG
   LỜI trong VERDICT (đầu vào, kỳ vọng); executor sẽ tự viết ca. Tương tự với đường dẫn thoát cây, byte thô bất thường, symlink.
3. Mọi phép thử khác (logic, kiểu, thứ tự, phân trang, độ phủ đột biến trên `_doc_check_runs`/`cmd_kiem_gate`) cứ dựng bình thường.

## Định dạng verdict

- Dòng 2 của VERDICT: `Verdict: <approve|changes_requested> — P0=a P1=b P2=c P3=d`, đếm theo LỚP, CHỈ trong tập.
- **NGƯỠNG:** chỉ `approve` khi P0=P1=P2=P3=0 trong tập.
- Mỗi lớp kèm **phép đo đã chạy** (lệnh, rc, đầu ra). Lớp không có phép đo không được tính.
- Mục "Ngoài phạm vi": đột biến/finding ngoài tập, sửa `packet_loop.py`, chứng minh nguồn gốc JSON, ca ngoài họ `kg_*`.
