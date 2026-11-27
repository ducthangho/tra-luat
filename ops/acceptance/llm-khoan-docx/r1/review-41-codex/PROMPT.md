# Cross-review packet #1525 LLM-KHOAN-DOCX r41 (PR #1517, ducthangho/tra-luat) — lượt 41, reviewer Codex

Lời gọi Codex thứ 42 (lease `ops/leases/llm-khoan-docx-r41-g1-claude.yaml`, `review_calls_limit: 45`, `review_calls_used_truoc: 41` — r34 dùng 2; lượt 35 bị ngắt vẫn tính 1). Chủ kho đã trao quyền ĐỨNG cho executor tự nâng trần và vá theo LỚP lỗi tới khi hết P1/P2 — đánh giá xem bản vá có ĐÓNG LỚP hay chỉ vá biểu hiện; chặn oan nguồn mang ký tự ngoài danh sách cho phép là cái giá đã khai, không phải finding. Với đường `<số hiệu>`, chủ kho đã QUYẾT giữ đường và khai giới hạn — finding về đường ấy chỉ tính khi nằm ngoài các giới hạn §2.21 U2 / §2.22 V3 / §2.23 (W1, W3, phần `<số hiệu>` của W2). **Bối cảnh:** r36 là Review Rescue Checkpoint §12 — lớp `ranh-gioi-khoan` dùng DANH SÁCH CHO PHÉP đầu dòng (`dau_dong_cho_phep`, §2.38). Lượt 36 APPROVE, còn biểu hiện nhãn điểm số `N.`/`N)`/`(N)` trùng số khoản; **chủ kho đã QUYẾT khai giới hạn** (§2.39) và khoá vào `pham_vi_kiem` — biểu hiện ấy KHÔNG còn là finding, trừ khi việc khai/khoá sai hoặc thiếu. Kiểm: lớp có còn biểu hiện NGOÀI ba giới hạn đã khai (nhãn dính thân; nhãn chỉ ngăn bằng khoảng trắng; nhãn số trùng số khoản) không. Các dạng bị chặn oan có chủ đích (`Tp.`, `e-mail`, `A1`, `1. A là`, `ASEAN (`) là quyết định chủ kho, KHÔNG phải finding. Lượt 37 APPROVE còn nhãn gõ tay chữ tiếng Việt (`đ)`) — r38 đòi từ đầu là TỪ TRỌN (§2.40). Lượt 38 APPROVE còn nhãn nhiều vế — **chủ kho QUYẾT THU HẸP MIỀN** (§2.41, chép nguyên văn ba quyết định): phần mở đầu có hình dạng nhãn điểm nhiều vế ⇒ đường thô từ chối cả Điều; kiểm định nghĩa hình dạng ấy (`_mo_dau_nhieu_ve`) có phủ đúng câu khai lượt 38 và hai phía miền có khoá trong `pham_vi_kiem` không. Lượt 39 (offline, `9e2f419`) APPROVE còn 2 P2 + 2 P3 — r40 (§2.42) thực thi trọn thu hẹp miền (mọi số vế, gạch dài, `là` trong ngoặc không thoát), locator ZIP64 tuyệt đối, hạn chót một nguồn, sửa hai P3. Lượt 40 (offline, `f63028a`) APPROVE còn 2 P2 + 1 P3 — r41 (§2.43) quét TOÀN phần đầu thân tới từ nối (nháy/ngoặc cân), chuẩn hoá lỗi zipfile, thu hồi cả nhóm tiến trình, P3 kết tệp. Ngân sách §2.37–§2.43 thuộc lớp `can-tai-nguyen-doc-nguon`: đối chiếu hint patch lượt 40. **ỨNG VIÊN LÀ COMMIT CỤC BỘ CHƯA PUSH** (ADR-0060 M5/M12: push chỉ sau review offline approve VÀ đủ điều kiện merge). **Điều kiện merge chủ kho đòi: 0 P1, 0 P2, 0 P3** — báo đủ P3 (mỗi P3 một lớp, kèm hint), không bỏ qua P3.
Bề mặt reviewer: `codex_cli` (`codex exec` qua `.claude/dev/launcher.py run`).

Bạn là reviewer độc lập. Thư mục làm việc là bản sao RỜI của kho, checkout detached đúng commit cần review:

- reviewed_sha: `4d6495bacd8922a841ddabce50686bca54bca9cf`
- base_sha: `64b7f2c14776d5d0e1d34a6be4725490956f5bec` (master)
- Đặc tả đóng băng HIỆN HÀNH: `ops/specs/llm-khoan-docx-r41.md` (thay r40; §2.4 (r2) … §2.43 (r41) THAY các điểm tương ứng trước đó) —
  kiểm sha256 khớp `spec_hash` trong lease r41. Lượt 40 chấm `f63028a` (offline): verdict `ops/acceptance/llm-khoan-docx/r1/review-40-codex/VERDICT.md`
  (APPROVE, 0 P1, 2 lớp P2: ranh-gioi-khoan, can-tai-nguyen-doc-nguon; 1 lớp P3: ve-sinh-diff-ho-so-review). Trước r39 nhánh đã MERGE `origin/master` (`695916e`; xung đột duy nhất `RELEASE_MANIFEST.json`, sinh lại ở `b5f8195`). Origin đang ở `c671163`; ứng viên `4d6495b` CHƯA push = ứng viên này (review offline TRƯỚC push — ADR-0060 M5/M12; chỉ push khi đủ điều kiện merge). Nhánh đã được đẩy tới `fce28fd` trước approve (ngoại lệ M5 do chủ kho duyệt, ghi ở đầu đặc tả r12). r7 ĐỔI HỢP ĐỒNG theo quyết định chủ kho: tệp .docx chỉ chứa ĐÚNG Điều cần đọc (§2.9) — không còn
  đoán điểm kết thúc Điều; finding về "tệp nhiều Điều bị chặn" là giới hạn đã khai. Diff bản vá: `git diff f63028a 4d6495bacd8922a841ddabce50686bca54bca9cf`.
- Bối cảnh: nhánh này mang packet #1514 (dừng ở r9 `fcb12b3`, verdict lượt 10 `ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md`:
  APPROVE, còn K1 P2). Packet #1525 làm tiếp trên cùng nhánh: thêm đường ranh giới từ CẤU TRÚC .docx và đóng K1 bằng cách cho đường
  văn bản thô chỉ nhận khoản đúng một dòng. Lease #1525 thay lease r9 của #1514 (bia mộ hai chiều).
  Diff packet này (lưu ý: từ r39 diff này gồm cả 148 commit master đã merge — phần của PR tách bằng `git diff 695916e <ứng viên>`): `git diff fcb12b3 4d6495bacd8922a841ddabce50686bca54bca9cf` (bỏ qua các tệp hồ sơ `ops/acceptance/llm-ranh-gioi-khoan/`). Diff toàn PR: `git diff 695916e 4d6495bacd8922a841ddabce50686bca54bca9cf`.
- Điều kiện merge theo ADR-0060 M1 (mặc định qua ADR-0062): 0 finding P0, P1, P2 mở.

Đọc `CLAUDE.md` ở gốc kho trước.

## PHẠM VI — lượt KIỂM CHỨNG

Các lượt review của mảng này từng bị nền từ chối phản hồi khi reviewer tự dựng nội dung thử nghiệm mới. Lượt này chỉ:
1. **Đối chiếu** hai lớp P2 và một lớp P3 của lượt 40 (`ranh-gioi-khoan`, `can-tai-nguyen-doc-nguon`) — từng lớp ĐÓNG TOÀN MIỀN (kể cả bằng giới hạn đã khai) hay chỉ đóng biểu hiện, đối chiếu hint patch lượt 40 (và mọi finding các lượt trước) (ĐÃ VÁ THẬT / VÁ MỘT PHẦN / CHƯA VÁ / VÁ SINH LỖI MỚI / HẾT ĐỐI TƯỢNG do hợp đồng r7)
   và đặc tả r41 (§1, §2.1–§2.43, §3); write set đúng lease r41; bia mộ hai chiều r9 (#1514) ↔ r1 ↔ … ↔ r41 đúng; K1 (nợ #1514) vẫn đóng.
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
`can_nguoi_duyet: true` giữ nguyên; mọi giới hạn liệt kê trong đặc tả r41 và `docs/GOI_AGENT_DA_NEN.md` mục script gọi Claude.
VERDICT: APPROVE nếu không còn P0/P1; ghi riêng số P2 còn mở (điều kiện merge).

**Ghi dòng `VERDICT:` SỚM** (tạm), cập nhật nếu kết luận đổi.

## Cách đo (không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r41-g1-claude.yaml
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
# Verdict packet #1525 r41 lượt 41 — Codex
reviewed_sha: 4d6495bacd8922a841ddabce50686bca54bca9cf
## Đối chiếu lượt 40 và đặc tả r41
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
P3_mo: <số>
VERDICT: APPROVE | REQUEST_CHANGES
```
