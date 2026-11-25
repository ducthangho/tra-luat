# Review offline MÃ — wp1236 đợt C theo đặc tả r12 — lượt 4 — reviewer độc lập, theo PROTOCOL §8.3 và ADR-0060 (M2, M12: review trước push)

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của work packet `sensitive` wp1236 **đợt C** (chốt **D2b** trong `cmd_kiem_dong_wp` của `.claude/dev/packet_loop.py`). Kho: ducthangho/tra-luat. Đây là lời gọi Codex **4/6** của đợt C (chủ kho nâng trần 4 → 6 ở #1236 issuecomment-7170968907; lease `LEASE.yaml` khoá `nang_tran`). Effort: high (chủ kho chỉ định).

## Vì sao có lượt này
Lượt 3 (của bạn, `lich_su/VERDICT_luot3.*`) đã approve `dbe650d`. Sau đó M3 Windows local, chạy tập trung trên DESKTOP-T9R33P2 bằng Python 3.12.10 (#1236 issuecomment-7170894289), ĐỎ ở `cong_d2b_c4_symlink[yaml_thuong_kem_thu_muc_symlink]`: cổng trả rc 0 "D2b ĐẠT" thay vì rc 12 `kiem_tep:not_measured:symlink`. Điều phối đã đo gốc lỗi trên máy ấy:
- `git archive` xếp symlink `d` (trỏ `sub`) trước `sub`;
- `tarfile.extractall(filter="data")` vì thế tạo `d` thành symlink LOẠI TỆP;
- `os.walk` xếp `d` vào danh sách tệp, và `chon_provenance` của module đợt A bỏ sót nó.

Điều phối đo thêm (18:41Z): trên Windows, symlink có đích chứa "/" KHÔNG phân giải được (`os.path.isdir` False dù đích là thư mục có thật), nhưng `os.readlink` vẫn trả nguyên chuỗi.

Bạn chính là reviewer đã nêu rủi ro này trong `m3_windows` của lượt 3 và ghi là chưa đo.

**Quyết định chủ kho cho lượt này:**
1. "Vá + nâng trần Codex C lên 6" (issuecomment-7170968907). Lớp mới, slug đề xuất `symlink-tren-dia-lech-cay`. Đây là lần thứ ba lớp `archive-loc-mat-du-lieu-kiem` (C01) lặp lại dưới dạng khác; chủ kho đã quyết đi tiếp, không phải executor tự quyết.
2. "Giữ phạm vi K2" (hỏi đáp trong phiên điều phối, ghi trong `handoff.yaml` khoá `doi_chieu_mau_co_san`). D2b KHÔNG siết thành "mọi symlink ⇒ not_measured". Symlink tệp không phải `*.yaml` vẫn ngoài phạm vi K2 (ca `symlink_ngoai_pham_vi_k2` rc 0). Chốt mới tính đích symlink trên DANH MỤC CÂY git (120000 → 040000 hoặc gốc bản bung), không hỏi đĩa về loại link.
3. Chủ kho chỉ thị đối chiếu với mẫu sẵn có: `repo/.claude/dev/launcher.py` `_chup_workspace` (islink/lstat trên mọi mục ở cả hai danh sách của os.walk) và `repo/.claude/skills/work-packet/SKILL.md` mục "Ca symlink Windows native".

**M3 Windows trên ứng viên mới** (điều phối đo, issuecomment-7172185200; lời khai, bạn không đo lại được): tập trung, base `f602325` 118/118, head `d5a7d85` 135/135. `cong_d2b_c4_symlink` đạt. Máy tạo được symlink, nên các biến thể lk4/lk6/lk7 đo chốt thật.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c5-4-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Tệp nháp, bản sao để đột biến: CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c5-4-codex/work/`. Đột biến luôn chạy trên BẢN SAO. Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu vào
- Ứng viên: `repo` ở HEAD `d5a7d8510af03e0d08545f677ad5de687e0264f4` (tree `241bd084…`), cha `dbe650d` (ứng viên lượt 3 bạn đã approve), base `f602325574c62184caf16309631f5f680ca5cee2`. Diff lượt này: `git diff dbe650d HEAD`. Diff toàn đợt: `git diff f602325 HEAD`.
- `SPEC.md` (sha256 phải là `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`), `LEASE.yaml` (trần ≤ 6 tệp / ≤ 450 dòng thêm; Codex 6).
- Verdict và probe lượt 1–3 của bạn: `lich_su/`.
- Bằng chứng executor: `bang_chung/` — `handoff.yaml` (sha256 `a695c91f…`), `gate/` (gồm `m3_mo_hinh.log`), `ab/`, `luat9/`, `cong_cu/`. Đây là LỜI KHAI: đo lại những gì quyết định kết luận. Executor khai:
  - A/B không hồi quy: ca nền 1784 → 1801, đột biến 2009 → 2062; đỏ sẵn ở cả hai vế: `r1187_spec_packet_type`.
  - Luật 9 khối D2b: 229 = 226 GIET + 3 TUONG_DUONG (ba tương đương cũ).
  - Ma trận `c4_symlink`: 29 biến thể × 16 đột biến.
  - numstat +420 −13.
- Tám điểm executor tự đề nghị bạn soi (khai trong handoff.yaml):
  1. Chốt chỉ ở nhánh passed, chỉ xét symlink TRỎ THƯ MỤC.
  2. Chuẩn hoá đích bằng `posixpath.normpath` trên VĂN BẢN. Lập luận không bỏ sót dựa vào "symlink trong cùng của chuỗi". Hướng lệch còn lại là chặn thừa (đích có `..` sau một symlink, hoặc tên không tồn tại).
  3. Chuỗi symlink không có đột biến riêng.
  4. Đổi thứ tự báo: `symlink` đứng trước lỗi K1.
  5. Mô hình `git_loi="tep"` thay os.walk trong tiến trình.
  6. Dòng `import posixpath` nằm ngoài khối của bộ quét luật 9.
  7. Gate không chạy lại trên bản ghép với master mới.
  8. `doi_chieu_mau_co_san` và hai mục `no_ngoai_write_set`.

## Việc phải làm
0. **Đối chiếu lượt trước (§8.3).**
   - Hai lớp cũ: `archive-loc-mat-du-lieu-kiem` (C01), `hop-dong-dau-ra-duong-dan-tu-do` (C02).
   - Lớp mới: `symlink-tren-dia-lech-cay`.
   - Gán MỘT trong bốn nhãn cho mỗi lớp, đo trên HEAD. Xét lớp mới có thật là một lớp riêng, hay chỉ là biểu hiện thứ ba của C01. Ghi `lop_lap_lan_ba`.
1. **Bản vá có đóng ĐÚNG cơ chế đã đo trên Windows không**, trên mọi đường vào. Tự liệt kê các đường, đừng lấy danh sách của executor làm trần. Gợi ý cần xét:
   - symlink tạo trước đích;
   - đích chứa "/";
   - đích `..`, gốc bản bung, ngoài bản bung;
   - chuỗi symlink, chuỗi vòng;
   - symlink trỏ symlink trỏ thư mục;
   - symlink trong thư mục con của provenance;
   - phân biệt hoa/thường hoặc NFC của tên đích so với danh mục cây;
   - junction (mô tả bằng lời).
   Mỗi đường: ca nào đo, đột biến nào giết. Chỗ chỉ dựa vào mô hình `git_loi="tep"` thì ghi rõ là mô hình.
2. **Chặn thừa**: hướng lệch "đích có `..` sau symlink" hoặc tên không tồn tại có làm D2b chặn oan một hồ sơ hợp lệ thật không? Đối chiếu dữ liệu thật trong `repo/ops/land/` (executor khai 0 symlink).
3. **Giữ phạm vi K2**: `symlink_ngoai_pham_vi_k2` vẫn rc 0; symlink `*.yaml` vẫn do module bắt; không có đường nào làm symlink trỏ thư mục lọt qua vì bị xếp như "tệp không phải yaml".
4. **Đối chiếu mẫu** `_chup_workspace` và skill. Phần khác có chủ đích (không coi mọi symlink như nhau) có đúng là chỉ khác ở phạm vi K2 không, hay còn đường mẫu bắt được mà D2b bỏ sót?
5. **Luật 9 theo quyết định chủ kho** (miền DELTA + không hồi quy, #1236 issuecomment-7130670276): kiểm hiện vật `luat9/`, chạy lại mẫu. Đột biến tự dựng ngoài manifest ⇒ P3 `ngoai_bang_dong`.
6. Tự chạy:
   - `python3 -B .claude/dev/packet_loop_test.py` giới hạn vào ca `cong_d2b_*` (dựng bộ chạy nhỏ trong `work/` gọi `chay_suite(CANONICAL, tmp, chi_chay=...)`);
   - đột biến `d2b_*` mới;
   - `python3 -m ruff check --select F` hai tệp, so với base;
   - numstat `git diff --numstat f602325 HEAD` (trần 450);
   - `git diff --check f602325 HEAD`.
7. **Quét độc lập theo LỚP** (§8.3, ADR-0060 M2): khái quát mỗi biểu hiện thành lớp, quét mọi biểu hiện cùng lớp trước khi báo.

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2+ phải có phép đo. P3 chờ miễn: ghi `chờ miễn chủ kho`; verdict `approve` chỉ khi điều kiện duy nhất còn lại là lời miễn ấy.

## Đầu ra
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c5-4-codex/work/VERDICT.json`, ghi tăng dần.
   - Kiểm bằng `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c5-4-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c5-4-codex/work/VERDICT.json --vong 4`. Phải ra HOP_LE; lưu stdout vào `work/kiem_verdict.txt`.
   - Khoá:
     - `reviewed_sha`, `spec_sha256`, `vong`: 4, `dot`: "C";
     - `findings` [`id` C03…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`];
     - `class_table` [`slug`, `manifestations`, `highest_open_severity`, `common_fix`, `closing_check`];
     - `m3_windows` {`ket_luan`, `can_cu`};
     - `luat9` {`delta`, `ke_thua_hoi_quy`, `tuong_duong_da_kiem`};
     - `prior_class_status` [`slug`, `finding_cu`, `luot_xuat_hien`, `status`, `evidence`, `chua_do_duoc`];
     - `hoi_tu` {`luot3_sang_4`: "|F|/|U|", `lop_lap_lan_ba`: [...]};
     - `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/c5-4-codex/work/VERDICT.md`: tóm tắt cho executor, gồm bảng lớp và từng finding kèm phép đo tái lập. Dòng cuối: `KET_LUAN: approve | changes_requested`.
3. **Tin nhắn trả lời cuối cùng của bạn** (thứ in ra stdout) phải KẾT THÚC bằng đúng một dòng riêng, không định dạng, không ký tự nào sau nó: `KET_LUAN: approve` hoặc `KET_LUAN: changes_requested`. Dòng này phải trùng với dòng cuối của VERDICT.md, vì cổng `kiem-merge` K4 đọc dòng cuối của stdout.
