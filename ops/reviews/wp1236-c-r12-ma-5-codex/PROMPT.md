# Review offline MÃ — wp1236 đợt C theo đặc tả r12 — lượt 5 — reviewer độc lập, theo PROTOCOL §8.3 và ADR-0060 (M2, M12: review trước push)

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của work packet `sensitive` wp1236 **đợt C** (chốt **D2b** trong `cmd_kiem_dong_wp` của `.claude/dev/packet_loop.py`). Kho: ducthangho/tra-luat. Đây là lời gọi Codex **5/6** của đợt C (trần 6, khai ở khoá `nang_tran` của `LEASE.yaml`). Effort: high (chủ kho chỉ định).

## Bối cảnh lượt này
Lượt 4 (của bạn, `lich_su/VERDICT_luot4.*`; probe `lich_su/probe_models.py`) trên `d5a7d85` kết luận `changes_requested` với hai finding:
- **C03 P1:** so đích bằng chuỗi chính xác nên bỏ sót bí danh thư mục (khác hoa/thường, dấu `\`).
- **C04 P2:** `normpath` chặn thừa symlink hỏng.

Đây là lần thứ tư lớp `archive-loc-mat-du-lieu-kiem` lặp lại. **Chủ kho quyết định ĐỔI KIẾN TRÚC sang DANH SÁCH CHO PHÉP** (#1236 issuecomment-7180063460, phiên điều phối ghi hộ). Nguyên văn luật:

> Một symlink trong thư mục provenance chỉ được cho qua khi đích của nó, chuẩn hoá trên văn bản theo dạng POSIX tương đối với thư mục chứa link, trùng **chính xác từng byte** với đường dẫn của một **tệp thường** (mode 100644 hoặc 100755) trong cây git của `oid`. Mọi trường hợp khác ⇒ `kiem_tep:not_measured:symlink` (rc 12): đích là thư mục, gốc bản bung, bí danh khác hoa/thường hay khác NFC, đích chứa `\`, đích hỏng/không tồn tại, ngoài cây, đích là một symlink khác. Symlink `*.yaml` vẫn do module bắt như cũ. … Đây là siết một phần K2 so với đặc tả r12. Phần K2 được giữ: symlink tệp không phải yaml trỏ đúng một tệp thường trong cây vẫn qua (ca `symlink_ngoai_pham_vi_k2` vẫn rc 0).

Điều phối đồng ý cách đọc chặt hơn của executor: "cây" = **danh mục cây con của thư mục provenance**, tức đúng phần được bung, chứ không phải cả cây của `oid`.

**M3 Windows trên `8aab9da`** (điều phối đo, issuecomment-7180853548; đây là lời khai, bạn không đo lại được): chạy tập trung, base 118/118, head 135/135. Ca `cong_d2b_c4_symlink` đạt trên Windows thật cho mọi biến thể:
- lk4, lk6, lk7: đích là thư mục;
- lk8 `SUB`, bí danh mà NTFS phân giải được;
- lk9 `CI.YAML`;
- lka: đích có `\`;
- lkb: hỏng;
- lkc: ngoài thư mục provenance;
- lkd: trỏ một symlink khác;
- lke: NFD;
- lk5: đối chứng rc 0.

Điều phối còn đo trên Windows: tên NFC đi qua ls-tree/archive/tarfile/os.walk không đổi byte; symlink trỏ tên NFD là link hỏng (NTFS không chuẩn hoá).

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c6-5-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Nháp và bản sao để đột biến: CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c6-5-codex/work/`. Đột biến chạy trên BẢN SAO. Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu vào
- Ứng viên: `repo` ở HEAD `8aab9dabb6f3f150e4ab1872e37757c2620912c3` (tree `5474259b…`), cha `d5a7d85` (lượt 4), base `f602325574c62184caf16309631f5f680ca5cee2`. Diff lượt này: `git diff d5a7d85 HEAD`. Toàn đợt: `git diff f602325 HEAD`.
- `SPEC.md` (sha256 phải là `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`), `LEASE.yaml` (≤ 450 dòng thêm, Codex 6).
- Verdict và probe lượt 1–4 của bạn: `lich_su/`.
- Bằng chứng executor: `bang_chung/` (`handoff.yaml` sha256 `422d4ab7…`, `gate/`, `ab/`, `luat9/`, …). Đó là LỜI KHAI: đo lại những gì quyết định kết luận. Executor khai:
  - A/B không hồi quy: ca nền 1784 → 1801, đột biến 2009 → 2075. Đỏ sẵn ở cả hai vế: `r1187_spec_packet_type`.
  - Luật 9: 228 = 225 GIET + 3 TUONG_DUONG.
  - Đột biến khai báo 234/234.
  - Ma trận `c4_symlink`: 36 biến thể × 29 đột biến; mỗi `cho_ten_<lk>` bị đúng một biến thể bắt.
  - `probe_models.py` của bạn chạy nguyên văn: case/nfc/backslash trên `d5a7d85` rc 0 → trên `8aab9da` rc 12.
  - numstat +429 −13.
- Bốn chỗ executor tự chọn cách đọc, nhờ bạn soi (khoá `quyet_dinh_thiet_ke_can_reviewer_soi`):
  1. "cây" = danh mục cây con của thư mục provenance;
  2. chuẩn hoá văn bản: đích không chuẩn tắc vẫn qua nếu chuẩn hoá ra đúng tệp thường, kèm lập luận "không thành thư mục"; không có ca dương trên Python 3.13;
  3. "kiểu tệp" = mode khác 040000/120000; gitlink dựa vào luật danh mục của lượt 3;
  4. K2 siết hơn chữ r12.

## Việc phải làm
0. **Đối chiếu lượt trước (§8.3).** Gán đúng MỘT trong bốn nhãn, đo trên HEAD, cho từng lớp: `archive-loc-mat-du-lieu-kiem`, `symlink-tren-dia-lech-cay`, `hop-dong-dau-ra-duong-dan-tu-do`. Xử lý riêng C03 và C04. Chạy lại `lich_su/probe_models.py` cùng các probe lượt 4. Cập nhật `lop_lap_lan_ba`.
1. **Đúng luật đã quyết?** Đối chiếu từng mệnh đề của luật nguyên văn ở trên với mã và ca.
   - Kiểm riêng: cách đọc "cây con" có chặt hơn luật không, và có chặn oan ca hợp lệ nào trong `repo/ops/land` không (executor khai có 0 mục 120000).
   - Kiểm điểm (2): một đích không chuẩn tắc chuẩn hoá ra tệp thường có thể dẫn tới đường nào lọt qua thư mục/symlink thật trên nền nào không. Tự dựng phản chứng trên bản sao nếu được; không dựng được thì nói rõ là chưa đo.
2. **Danh sách cho phép có thật là danh sách cho phép không?** Tìm mọi đường làm một symlink KHÔNG trùng từng byte một tệp thường của cây con mà vẫn qua. Các hướng phải xét:
   - Unicode: casefold, NFC/NFD, ký tự đồng dạng;
   - dấu `/` thừa, `./`, `..` đặt giữa;
   - đích rỗng, đích tuyệt đối;
   - byte không UTF-8 và `surrogateescape`;
   - đích trỏ tệp mode 100755, gitlink, tệp trong `.gitattributes export-ignore`;
   - symlink lồng trong thư mục con.
   Đột biến "nới danh sách cho đúng một tên tấn công" phải làm ca đích đỏ. Kiểm 7 đột biến `cho_ten_<lk>`.
3. **Không hồi quy:** ca `symlink_ngoai_pham_vi_k2` vẫn rc 0; symlink `*.yaml` vẫn do module bắt; thứ tự báo lỗi của D2b.
4. **Luật 9** theo quyết định của chủ kho (miền DELTA + không hồi quy, #1236 issuecomment-7130670276): kiểm hiện vật `luat9/` và chạy lại một mẫu. Đột biến tự dựng ngoài manifest ⇒ P3 `ngoai_bang_dong`.
5. **Tự chạy:**
   - các ca `cong_d2b_*`, qua bộ chạy nhỏ gọi `chay_suite(CANONICAL, tmp, chi_chay=...)`;
   - đột biến `d2b_k2_*`;
   - `ruff --select F` trên hai tệp, so với base;
   - numstat (trần 450);
   - `git diff --check f602325 HEAD`.
6. **Quét độc lập theo LỚP** (§8.3): khái quát mỗi biểu hiện thành lớp, rồi quét mọi biểu hiện cùng lớp trước khi báo.

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2+ phải có phép đo. P3 chờ miễn: ghi `chờ miễn chủ kho`; verdict `approve` chỉ khi điều kiện duy nhất còn lại là lời miễn ấy.

## Đầu ra
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c6-5-codex/work/VERDICT.json`, ghi tăng dần.
   - Kiểm bằng `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c6-5-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c6-5-codex/work/VERDICT.json --vong 5` (phải HOP_LE; lưu stdout vào `work/kiem_verdict.txt`).
   - Khoá: `reviewed_sha`, `spec_sha256`, `vong`: 5, `dot`: "C", `findings` [`id` C05…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table`, `m3_windows`, `luat9`, `prior_class_status`, `hoi_tu` {`luot4_sang_5`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c6-5-codex/work/VERDICT.md`: tóm tắt cho executor. Dòng cuối: `KET_LUAN: approve | changes_requested`.
3. **Tin nhắn trả lời cuối cùng của bạn** (thứ in ra stdout) phải KẾT THÚC bằng đúng một dòng riêng, không định dạng, không ký tự nào sau nó: `KET_LUAN: approve` hoặc `KET_LUAN: changes_requested`. Dòng này phải trùng dòng cuối của VERDICT.md, vì cổng `kiem-merge` K4 đọc dòng cuối stdout.
