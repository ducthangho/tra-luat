# Cross-review packet #1525 LLM-KHOAN-DOCX r35 (PR #1517, ducthangho/tra-luat) — lượt 35, reviewer Codex

Lời gọi Codex thứ 36 (lease `ops/leases/llm-khoan-docx-r35-g1-claude.yaml`, `review_calls_limit: 36`, `review_calls_used_truoc: 35` — lượt 34 dùng 2 lời gọi vì chạy lại theo lớp). Chủ kho đã trao quyền ĐỨNG cho executor tự nâng trần và vá theo LỚP lỗi tới khi hết P1/P2 — đánh giá xem bản vá có ĐÓNG LỚP hay chỉ vá biểu hiện; chặn oan nguồn mang ký tự ngoài danh sách cho phép là cái giá đã khai, không phải finding. Với đường `<số hiệu>`, chủ kho đã QUYẾT giữ đường và khai giới hạn — finding về đường ấy chỉ tính khi nằm ngoài các giới hạn §2.21 U2 / §2.22 V3 / §2.23 (W1, W3, phần `<số hiệu>` của W2): hành vi của bộ đọc dùng chung `tl extract`/`docx_markup` là giới hạn đã khai của đường này. Các giới hạn mới khai ở §2.37 (ranh giới nhìn thấy giữa nhãn và thân, nhãn ghép khác kiểu chữ, ngân sách đọc) là quyết định của executor theo câu khai reviewer lượt 34 đề xuất — đánh giá xem chúng có hợp lý và có đủ hẹp không.
Bề mặt reviewer: `codex_cli` (`codex exec` qua `.claude/dev/launcher.py run`).

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần review:

- reviewed_sha: `8b6782620a6a365d7e5c890481d19a0077609f2e`
- base_sha: `64b7f2c14776d5d0e1d34a6be4725490956f5bec` (master)
- Đặc tả đóng băng HIỆN HÀNH: `ops/specs/llm-khoan-docx-r35.md` (thay r34; §2.4 (r2) … §2.37 (r35) THAY các điểm tương ứng trước đó) —
  kiểm sha256 khớp `spec_hash` trong lease r35. Lượt 34 chấm `a3ef89a`: verdict `ops/acceptance/llm-khoan-docx/r1/review-34-codex/VERDICT.md`
  (APPROVE, 0 P1, 3 lớp P2: ranh-gioi-khoan, can-tai-nguyen-doc-nguon, ranh-gioi-ky-tu). Nhánh đã đẩy tới `8b67826` = ứng viên này (đẩy trước review theo quyền đứng của chủ kho; ghi ở đầu đặc tả r35). Nhánh đã được đẩy tới `fce28fd` trước approve (ngoại lệ M5 do chủ kho duyệt, ghi ở đầu đặc tả r12). r7 ĐỔI HỢP ĐỒNG theo quyết định chủ kho: tệp .docx chỉ chứa ĐÚNG Điều cần đọc (§2.9) — không còn
  đoán điểm kết thúc Điều; finding về "tệp nhiều Điều bị chặn" là giới hạn đã khai. Diff bản vá: `git diff 5bc6abd 8b6782620a6a365d7e5c890481d19a0077609f2e`.
- Bối cảnh: nhánh này mang packet #1514 (dừng ở r9 `fcb12b3`, verdict lượt 10 `ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md`:
  APPROVE, còn K1 P2). Packet #1525 làm tiếp trên cùng nhánh: thêm đường ranh giới từ CẤU TRÚC .docx và đóng K1 bằng cách cho đường
  văn bản thô chỉ nhận khoản đúng một dòng. Lease #1525 thay lease r9 của #1514 (bia mộ hai chiều).
  Diff packet này: `git diff fcb12b3 8b6782620a6a365d7e5c890481d19a0077609f2e` (bỏ qua các tệp hồ sơ `ops/acceptance/llm-ranh-gioi-khoan/`). Diff toàn PR: `git diff 64b7f2c 8b6782620a6a365d7e5c890481d19a0077609f2e`.
- Điều kiện merge theo ADR-0060 M1 (mặc định qua ADR-0062): 0 finding P0, P1, P2 mở.

Đọc `CLAUDE.md` ở gốc kho trước.

## PHẠM VI — lượt KIỂM CHỨNG

Các lượt review của mảng này từng bị nền từ chối phản hồi khi reviewer tự dựng nội dung thử nghiệm mới. Lượt này chỉ:
1. **Đối chiếu** ba lớp P2 của lượt 34 — `ranh-gioi-khoan`, `can-tai-nguyen-doc-nguon`, `ranh-gioi-ky-tu` — từng lớp ĐÓNG TOÀN MIỀN hay chỉ đóng các biểu hiện đã nêu, đối chiếu với hint patch của lượt 34 (và mọi finding các lượt trước) (ĐÃ VÁ THẬT / VÁ MỘT PHẦN / CHƯA VÁ / VÁ SINH LỖI MỚI / HẾT ĐỐI TƯỢNG do hợp đồng r7)
   và đặc tả r35 (§1, §2.1–§2.37, §3); write set đúng lease r35; bia mộ hai chiều r9 (#1514) ↔ r1 ↔ … ↔ r35 đúng; K1 (nợ #1514) vẫn đóng.
2. **Chạy** các bộ test có sẵn (mục "Cách đo") và báo số đạt/tổng.
3. **Đột biến bản vá** trên BẢN SAO TẠM: bảng `DOT_BIEN` có sẵn (bộ test tự chạy; đột biến `wp1525_*`) và, nếu muốn, sửa vài dòng của
   `doc_dieu_docx` / `_phan_tich_doan` / `_doan_trong` / `_doc_danh_so` / `doc_dieu_cau_truc` để xác nhận ca đích đỏ đúng lý do.
4. **Đọc mã** `scripts/tl_core/llm_route.py` (`doc_dieu_docx`, `_doan_trong`, `_phan_tich_doan`, `_doc_danh_so`, `_doc_kieu`, `_theo_kieu`, `_nhan`, `doc_dieu_cau_truc`, `tach_khoan`, `lech_nguyen_van`)
   và `scripts/tl_core/ops_misc.py` (`cmd_llm_khai_niem`), mô tả nghi vấn **bằng lời**. KHÔNG viết thêm tệp thử nghiệm, tệp .docx,
   chuỗi thử nghiệm hay script dò mới; điều chỉ kiểm được bằng thử nghiệm mới thì ghi vào "Không đo được".

## CÁCH REVIEW — THEO LỚP LỖI, KÈM HINT PATCH (chỉ thị chủ kho, 26-11-2026)
Chủ kho yêu cầu: **vá và review theo LỚP lỗi, không theo từng lỗi riêng lẻ, có hint patch.** 33 lượt trước mỗi lượt báo 1–5 biểu hiện
mới của CÙNG vài lớp (`ranh-gioi-khoan`, `docx-markup-du-thao`, `docx-so-hien-thi`, `docx-khoa-bang-style`…), executor vá từng biểu hiện và
lượt sau lộ biểu hiện kế. Lượt này phải phá vòng ấy:
- Với MỖI lớp còn mở, phát biểu **BẤT BIẾN** mà mã phải giữ (một câu tổng quát, kiểm được), rồi **liệt kê ĐỦ các hình dạng / đường vào**
  của lớp theo đọc mã (không dừng ở một ví dụ) — đó là "miền" bản vá phải phủ.
- Kèm **HINT PATCH**: phác thảo diff (unified diff, hoặc mã giả sát tên hàm/biến thật) đóng **CẢ LỚP tại MỘT chỗ** (một bộ quét/ngữ pháp/bảng
  dùng chung, một điểm phân giải duy nhất…), và giải thích vì sao nó phủ mọi hình dạng đã liệt kê. Nếu lớp không đóng được bằng hình dạng
  (vùng giao nhập nhằng thật), nói rõ và đề xuất ranh giới miền + câu khai giới hạn cho đặc tả.
- Kèm **HINT TEST**: nhóm ca âm/dương và đột biến để KHOÁ lớp (đột biến gỡ chốt chung phải làm đỏ ca đích).
- KHÔNG tách các biểu hiện của cùng một lớp thành nhiều finding. Mỗi lớp = MỘT finding. Hạng của finding = hạng cao nhất trong lớp.
- Hint patch là VĂN BẢN trong verdict — không áp vào cây, không tạo tệp mới (ràng buộc dưới vẫn giữ).

## Câu hỏi cần trả lời
- Còn đường nào để một kết quả SAI (bỏ/gộp/cắt/tráo khoản, hoặc chữ đã bỏ của dự thảo) được nhận là nguyên văn — ở đường cấu trúc
  hay đường thô — theo đọc mã? Đặc biệt: bộ đếm số Word (`start`, `startOverride`, đặt lại cấp con, nhiều numId), định vị vùng Điều,
  điểm gõ tay, câu dẫn, `KhongCauTruc` lùi về đường thô.
- K1 (nhánh điểm và tiếp dòng "là" ở nguồn có số) đã đóng ở đường thô chưa? Lớp `ranh-gioi-khoan` còn biểu hiện nào trên đường thô?
- Có dạng .docx văn bản luật THƯỜNG GẶP (Word/Google Doc) bị chặn oan mà đặc tả không khai không? Danh sách cho phép của §2.5 có
  thiếu phần tử phổ biến của bản export Google Doc / Word (ghi P2 kèm lý do; chặn oan không phải nhận sai)?

Phân hạng finding theo bảng severity của `docs/PROTOCOL_DA_PHIEN.md` và ADR-0060, nêu lý do hạng. Giới hạn đã khai (không phải finding):
`can_nguoi_duyet: true` giữ nguyên; mọi giới hạn liệt kê trong đặc tả r35 và `docs/GOI_AGENT_DA_NEN.md` mục script gọi Claude.
VERDICT: APPROVE nếu không còn P0/P1; ghi riêng số P2 còn mở (điều kiện merge).

**Ghi dòng `VERDICT:` SỚM** (tạm), cập nhật nếu kết luận đổi.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r35-g1-claude.yaml
python scripts/tl.py --selftest        # ~6 phút
```

Lưu ý môi trường: thư mục RỖNG `/tmp/.git` (sandbox để lại) làm 14 ca selftest `r973_bootstrap_*`, `wp433_*`,
`wp727_tl_gws_refresh` đỏ trên CẢ base lẫn head — đỏ sẵn, không phải hồi quy.

## Ràng buộc
- KHÔNG gọi Claude/Anthropic API thật, KHÔNG chạy `claude -p` thật, KHÔNG chạy `tl llm-khai-niem` với model thật. Không đọc/in bí mật.
- KHÔNG push, KHÔNG gọi GitHub, KHÔNG sửa tệp đã theo dõi trong cây.

## Đầu ra
Ghi TĂNG DẦN vào `.review/VERDICT.md`:

```
# Verdict packet #1525 r35 lượt 35 — Codex
reviewed_sha: 8b6782620a6a365d7e5c890481d19a0077609f2e
## Đối chiếu lượt 34 và đặc tả r35
| Mục | Trạng thái | Bằng chứng |
## Findings THEO LỚP
### Lớp `<slug>` [P?] — <tệp:dòng chính>
- Bất biến:
- Miền (mọi hình dạng / đường vào đã biết; biểu hiện cụ thể làm bằng chứng):
- Hint patch (diff phác thảo đóng cả lớp tại một chỗ) + vì sao phủ đủ miền:
- Hint test (ca âm/dương + đột biến khoá lớp):
- Phần không đóng được bằng hình dạng (nếu có) + câu khai giới hạn đề xuất:
## Kết quả test và đột biến
## Không đo được
P2_mo: <số>
VERDICT: APPROVE | REQUEST_CHANGES
```
