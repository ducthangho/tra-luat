# Review offline MÃ — wp1236 đợt C theo đặc tả r12 — lượt 6 (CUỐI) — reviewer độc lập, theo PROTOCOL §8.3 và ADR-0060 (M2, M12: review trước push)

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của work packet `sensitive` wp1236 **đợt C** (chốt **D2b** trong `cmd_kiem_dong_wp` của `.claude/dev/packet_loop.py`). Kho: ducthangho/tra-luat. Đây là lời gọi Codex **6/6**, lượt CUỐI trong trần (khoá `nang_tran` của `LEASE.yaml`). Effort: high (chủ kho chỉ định).

## Bối cảnh lượt này
Lượt 5 (của bạn, `lich_su/VERDICT_luot5.*`; probe trong `lich_su/probe_paths.py` và `lich_su/probe_modes.py`) chấm `8aab9da` là `changes_requested`, chỉ vì **C05 P2**: danh sách cho phép chưa thực thi điều cấm "đích chứa `\`". Trên POSIX, nếu cây có một tên tệp chứa `\` thì link trỏ tên ấy đi qua với rc 0.

Chủ kho đã quyết hai lần (phiên điều phối ghi hộ):
- Luật danh sách cho phép, #1236 issuecomment-7180063460:
  > Một symlink trong thư mục provenance chỉ được cho qua khi đích của nó, chuẩn hoá trên văn bản theo dạng POSIX tương đối với thư mục chứa link, trùng chính xác từng byte với đường dẫn của một tệp thường (mode 100644 hoặc 100755) trong cây git của `oid`. Mọi trường hợp khác ⇒ `kiem_tep:not_measured:symlink` (rc 12): đích là thư mục, gốc bản bung, bí danh khác hoa/thường hay khác NFC, đích chứa `\`, đích hỏng/không tồn tại, ngoài cây, đích là một symlink khác. Symlink `*.yaml` vẫn do module bắt như cũ.

  Kèm cách đọc "cây" = danh mục cây con của thư mục provenance. Điều phối đã đồng ý cách đọc này vì nó chặt hơn luật.
- Vá C05 theo (a)+(b), #1236 issuecomment-7182681531:
  - **(a)** cấm `\` trên `join(dirname(link), readlink)` **trước** `normpath`, tức cả đích thô lẫn thư mục chứa link;
  - **(b)** đòi `posixpath.normpath(d) == d` với `d` là đích thô. Hệ quả có chủ đích: `./x`, `a//b`, `sub/../x` bị chặn;
  - **(c)** không thêm mã riêng cho mode 100644/100755; gitlink đã bị luật danh mục chặn bằng rc 8.

**M3 Windows trên `45944c7`** (điều phối đo, issuecomment-7184957862; là lời khai, bạn không đo lại được): chạy test tập trung, Python 3.12.10, base 118/118, head 135/135, `cong_d2b_c4_symlink` passed. Năm biến thể tên chứa `\` (lkf–lkj) **vắng mặt trên Windows** vì Git for Windows không nhận tên ấy; trên Windows, điều cấm `\` chỉ được đo qua lka.

Đo chẩn đoán của điều phối:
- 3.12.10: `tarfile.data_filter` giữ nguyên linkname `khong/../ci.yaml`.
- 3.13.17: `data_filter` chuẩn hoá `khong/../ci.yaml` → `ci.yaml` và đổi `/` thành `\` (`../../..` → `..\..\..`, `sub/x` → `sub\x`). Đây là nợ đo (3) đã ghi: chặn an toàn, nhưng ca sẽ đỏ trên interpreter Windows mới.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c7-6-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Tệp nháp và bản sao để đột biến: CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c7-6-codex/work/`. Đột biến chạy trên BẢN SAO. Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu vào
- Ứng viên: `repo` ở HEAD `45944c7c3f4c75beaa87f36138b2bba9fb9198a3` (tree `66a0f315…`), cha `8aab9da` (lượt 5), base `f602325574c62184caf16309631f5f680ca5cee2`. Diff của lượt này: `git diff 8aab9da HEAD`. Diff toàn đợt: `git diff f602325 HEAD`.
- `SPEC.md` (sha256 phải là `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`), `LEASE.yaml` (≤ 450 dòng thêm, Codex 6).
- Verdict và probe lượt 1–5 của bạn: `lich_su/`.
- Bằng chứng executor ở `bang_chung/`: `handoff.yaml` (sha256 `9d648b7e…`), `README.md` mục 3 (bảng đối chiếu từng mệnh đề của luật với mã, ca, đột biến; khoá `bang_doi_chieu_menh_de` trong handoff), `gate/`, `ab/`, `luat9/`. Đây là LỜI KHAI; đo lại những gì quyết định kết luận. Executor khai:
  - A/B không hồi quy: 1784 → 1801 ca, 2009 → 2077 đột biến; đỏ sẵn ở cả hai vế: `r1187_spec_packet_type`.
  - Luật 9: 235 = 232 GIET + 3 TUONG_DUONG.
  - Đột biến khai báo: 236/236.
  - Ma trận `c4_symlink`: 43 biến thể × 31 đột biến, gốc 0 lệch. `bo_cam_cheo` bị bắt bởi lkf–lkj; `cam_cheo_chi_dich_tho` chỉ bị bắt bởi lkj; `bo_chuan_tac` chỉ bị bắt bởi `nen_giu_nguyen_dich[lkl]`.
  - Probe lượt 5 của bạn chạy nguyên văn: bốn kịch bản `\` và bảy kịch bản `retained_safe_link_text` đổi từ rc 0 → 12; regular/executable/nested/nonutf_exact vẫn rc 0.
  - numstat +438 −13.

## Việc phải làm
0. **Đối chiếu lượt trước (§8.3):** gán đúng MỘT trong bốn nhãn cho từng lớp (`archive-loc-mat-du-lieu-kiem`, `symlink-tren-dia-lech-cay`, `hop-dong-dau-ra-duong-dan-tu-do`), xử lý C05. Chạy lại `lich_su/probe_paths.py` và `lich_su/probe_modes.py` trên HEAD.
1. **Mã thực thi đủ MỌI mệnh đề của luật + (a)+(b)?** Đối chiếu bảng mệnh đề của executor với mã. Mỗi mệnh đề cần có: dòng mã thực thi trực tiếp, ca, và đột biến riêng. Đặc biệt kiểm:
   - (a) áp cho cả thư mục chứa link (lkj);
   - (b) đóng được đường link hỏng mà bộ bung giữ nguyên văn bản;
   - không có đường nào làm một symlink KHÔNG trùng từng byte một tệp thường của cây con mà vẫn qua. Phải xét: Unicode, `/` thừa, `.`/`..`, đích rỗng, đích tuyệt đối, byte không UTF-8 + `surrogateescape`, 100755, gitlink, `export-ignore`, symlink lồng.
2. **Không hồi quy:** `symlink_ngoai_pham_vi_k2` (lk5) vẫn rc 0; symlink `*.yaml` vẫn do module bắt.
3. **Nợ đo (3)** và **fixture chỉ có trên POSIX**: xét đây là giới hạn đo đã khai, hay là một lỗ hành vi. Lỗ hành vi thì báo theo mức thật.
4. **Luật 9** theo quyết định chủ kho (miền DELTA + không hồi quy, #1236 issuecomment-7130670276): kiểm hiện vật `luat9/` và chạy lại một mẫu. Đột biến bạn tự dựng ngoài manifest ⇒ P3 `ngoai_bang_dong`.
5. **Tự chạy:**
   - các ca `cong_d2b_*`, qua bộ chạy nhỏ gọi `chay_suite(CANONICAL, tmp, chi_chay=...)`;
   - các đột biến `d2b_k2_*`;
   - `ruff --select F` trên hai tệp, so với base;
   - numstat (trần 450);
   - `git diff --check f602325 HEAD`.
6. **Quét độc lập theo LỚP** (§8.3).

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2+ phải có phép đo. P3 chờ miễn: ghi `chờ miễn chủ kho`; verdict `approve` chỉ khi điều kiện duy nhất còn lại là lời miễn ấy.

## Đầu ra
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c7-6-codex/work/VERDICT.json`, ghi tăng dần.
   - Kiểm bằng `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c7-6-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c7-6-codex/work/VERDICT.json --vong 6`. Phải ra HOP_LE; lưu stdout vào `work/kiem_verdict.txt`.
   - Khoá: `reviewed_sha`, `spec_sha256`, `vong`: 6, `dot`: "C", `findings` [`id` C06…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table`, `m3_windows`, `luat9`, `prior_class_status`, `hoi_tu` {`luot5_sang_6`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c7-6-codex/work/VERDICT.md`: tóm tắt. Dòng cuối: `KET_LUAN: approve | changes_requested`.
3. **Tin nhắn trả lời cuối cùng của bạn** (thứ in ra stdout) phải KẾT THÚC bằng đúng một dòng riêng, không định dạng, không ký tự nào sau nó: `KET_LUAN: approve` hoặc `KET_LUAN: changes_requested`. Dòng này phải trùng dòng cuối của VERDICT.md, vì cổng `kiem-merge` K4 đọc dòng cuối stdout.
