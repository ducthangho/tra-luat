# Đặc tả packet `wp972` r1 — backup config không bao giờ rơi vào cây skill

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| packet | #972 `wp972`, revision 1, generation 1 |
| review_class | `sensitive` (chặn token lọt cây skill) |
| write set | `scripts/tl_core/profile_env.py`, `scripts/tl_core/profile_mgmt.py`, `scripts/tl_core/ops_misc.py`, `scripts/tl_selftest.py`, `VERSION`, `scripts/tl.py`, `SKILL.md`, `CHANGELOG.md`, `RELEASE_MANIFEST.json` |
| base | `origin/master` lúc cấp lease (đo khi soạn: `e3ea139`, VERSION `1.36.68`) |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run`, phiên mới, read-only, neo đúng head |

## 1. Vì sao
Issue #972. `_config_backup_dir()` (`scripts/tl_core/profile_env.py:607`), khi không có `TL_CONFIG_BACKUP_DIR` và không có `D:/Quốc hội/_config_backups`, chọn `($LOCALAPPDATA | Path.home())/tra-luat/_config_backups`. Trên POSIX, nếu kho clone ở `~/tra-luat`, đích ấy là `<kho>/_config_backups`, tức nằm trong cây skill.

Đo ngày 27-10-2026: `HOME=/home/user` cùng kho ở `/home/user/tra-luat` cho ra đích **trong cây**. Selftest `r202_profile_delete_backup_ngoai_cay` đỏ trên máy chủ kho dán vào (`HOME=/home/agent`).

Bản sao lưu config có chứa token, và doctrine r193/r202 cấm nó nằm trong cây skill (sự cố 23-07). Hiện có hai nơi gọi: `profile-delete --apply` (`profile_mgmt.py:548`) và `init-config` (`ops_misc.py:479`). Cả hai **nuốt mọi ngoại lệ** thành `backup = None` rồi vẫn sửa config.

## 2. Thay đổi
1. **Đích mặc định.** Thứ tự ưu tiên giữ nguyên như sau:
   1. `TL_CONFIG_BACKUP_DIR`;
   2. `D:/Quốc hội/_config_backups` (chỉ khi đã có sẵn);
   3. `%LOCALAPPDATA%/tra-luat/_config_backups` khi có `LOCALAPPDATA`;
   4. ngược lại (POSIX), `$XDG_STATE_HOME/tra-luat/_config_backups`, mặc định `~/.local/state/tra-luat/_config_backups`. Bỏ hẳn nhánh `Path.home()/tra-luat`.
2. **Chốt cứng.** Sau khi chọn đích, nếu đích (đã `resolve`) bằng gốc cây skill hoặc nằm dưới gốc cây skill, thì ném một ngoại lệ riêng, tên `BackupTrongCaySkill`. Chốt áp cho **mọi** nguồn, kể cả `TL_CONFIG_BACKUP_DIR`. Phải kiểm **trước** `mkdir`, để không dựng thư mục nào trong cây. Gốc cây skill là cách mà ca `r202` hiện dùng: thư mục cha của thư mục chứa `tl.py`.
3. **Fail-close ở hai nơi gọi.** Khi gặp `BackupTrongCaySkill`, lệnh dừng **trước** khi sửa config: không xoá profile, không ghi config, không chạm NLM hay Drive. Lệnh trả mã thoát khác 0, kèm JSON có `ok: false` và mã lỗi `CONFIG_BACKUP_TRONG_CAY_SKILL`, nêu đích bị từ chối và cách chữa (đặt `TL_CONFIG_BACKUP_DIR` ra ngoài cây). Các ngoại lệ khác giữ nguyên hành vi cũ; đó là ngoài phạm vi, xem §5.
4. **Phiên bản.** Bump `1.36.68` lên `1.36.69` ở `VERSION`, hằng `VERSION` trong `scripts/tl.py` và header `SKILL.md`. Thêm mục `★ v1.36.69` vào `CHANGELOG.md`. Tái sinh `RELEASE_MANIFEST.json`.

## 3. Tiêu chí xong
- Ca mới `r972_*` trong `scripts/tl_selftest.py` gồm:
  - (a) `HOME` là thư mục cha của một cây skill giả, không có `LOCALAPPDATA`/`TL_CONFIG_BACKUP_DIR`/`XDG_STATE_HOME`: đích mặc định nằm **ngoài** cây, dưới `~/.local/state/tra-luat/`;
  - (b) `XDG_STATE_HOME` được tôn trọng;
  - (c) `TL_CONFIG_BACKUP_DIR` trỏ vào trong cây: ném `BackupTrongCaySkill`, và không có thư mục nào được tạo;
  - (d) `profile-delete --apply` gặp đích trong cây: rc khác 0, mã lỗi `CONFIG_BACKUP_TRONG_CAY_SKILL`, config **không đổi byte**;
  - (e) như (d), cho `init-config`.
- Mỗi chốt có một đột biến riêng, bị giết đúng ca đích:
  - gỡ chốt cứng;
  - chốt chạy sau `mkdir`;
  - bỏ áp chốt cho nguồn env;
  - khôi phục nhánh `Path.home()/tra-luat`;
  - hai nơi gọi nuốt `BackupTrongCaySkill`.

  Đột biến chạy trên bản sao tạm. Một kill chỉ được tính khi ca đích **đỏ** vì đột biến, không phải vì ngoại lệ vô can.
- Ca `r202_profile_delete_backup_ngoai_cay` xanh cả khi chạy với `HOME` là thư mục cha của kho (tức đúng ca đã đỏ trên máy chủ kho).
- `python scripts/tl.py --selftest` ra N/N, hai số bằng nhau.
- `ruff --select F`: delta so với master bằng 0.
- `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ra `ok=true` và `expected == checked`.
- Guard `skill_md_version_matches_VERSION` xanh.
- Review chéo Codex qua `launcher.py run` trên đúng head, tới khi 0 P0–P3.

## 4. Trần
- Kích thước: ≤ 9 tệp / ≤ 250 dòng thêm. Mức này vượt trần 6 tệp của ADR-0053 vì có bump phiên bản và manifest, nên cần `nang_tran` trong lời duyệt của chủ kho.
- Lời gọi Codex: 10 theo dòng khai ADR-0055.

## 5. Ngoài phạm vi
- Không đổi cách hai nơi gọi xử lý các ngoại lệ **khác** khi ghi backup (hiện là nuốt rồi đi tiếp không có backup). Đây là nợ `NO-972-BACKUP-NUOT-LOI`.
- Không di chuyển hay dọn backup cũ đã lỡ nằm trong cây ở máy nào đó. Việc ấy cần chạy trên từng máy và do chủ kho quyết.
- Không deploy Package.
