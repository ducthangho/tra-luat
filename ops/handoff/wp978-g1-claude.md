# Handoff wp978-g1-claude — nợ F13 của #899 (`git_cuc_bo` đọc metadata commit bằng bytes)

- packet #978 · lease `wp978-r1-g1-claude` (`ops/leases/wp978-r1-g1-claude.yaml`, nhánh `ops/wp978-r1-g1-lease`)
- spec `ops/specs/wp978.md` sha256 `eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638` (commit `5f438b4`)
- base `c8d92ba05c3ea875d8f84d94195430302690286d` · head ứng viên `bef1403` trên `agent/wp978-g1-claude` (CHƯA đẩy)
- executor phiên `session_015GtxrZYA5uRwjhUvsG1i8A`

## Thứ tự (khai thẳng)
Bản vá được viết THĂM DÒ trước khi có lease, để đo kích thước cho đặc tả (đo được 2 tệp, 9 + 29 dòng thêm). Nó không được
commit hay đẩy trước lease. Mốc thời gian (UTC, 27-10-2026):
1. ~09:30 bản thăm dò trong cây làm việc (chưa commit);
2. 09:36 spec commit `5f438b4`; 09:37 lease `check` rc 0, commit `83de8bc`, push;
3. 09:38 commit cục bộ `bef1403` (cha = base_sha của lease); 09:39 chạy full suite lượt 1 (head + base);
4. 09:44 run `ops-publish-lease.yml` 40482277284 `success` trên `83de8bc`;
5. sau mốc 4: chạy lại full suite trên `bef1403` (lượt 2) — đây là bằng chứng tính cho N3.
Phiên điều phối `session_01B8U8TTEwfMS1u4u4E1VmRW` nhắc thứ tự này; code không đổi giữa thăm dò và `bef1403`.

## Thay đổi
- `ops/ci_provenance.py`: `git_cuc_bo` chạy `cat-file -p` không `text=True`; tách phần đầu trên bytes; chỉ giải mã dòng
  `tree`/`parent` và chỉ khi khớp `RE_OID_B` (40 hoặc 64 hex). Không đúng một `tree` hoặc giá trị không phải OID ⇒ `None`.
- `ops/ci_provenance_test.py`: ca `c53_git_commit_khong_utf8` + 3 đột biến `F13_*` trong `DOT_BIEN`.

## Nghiệm thu
| | lệnh | kết quả |
|---|---|---|
| N1 | `--mot-ca c53_git_commit_khong_utf8` trên head | rc 0 |
| N1 | cùng ca, `CI_PROVENANCE_MA=<ci_provenance.py tại c8d92ba>` | `DO:c53_…: … UnicodeDecodeError … 0xe9` (rc 3) |
| N2 | `chay_dot_bien` cho 3 đột biến F13 | `F13_doc_text_true` GIET · `F13_giai_ma_ca_phan_dau` GIET · `F13_bo_kiem_oid` GIET |
| N3 | full suite base `c8d92ba` (clone riêng) | `CA: 52/52` · `DOT BIEN: 292/292` · `TONG: DAT` rc 0 |
| N3 | full suite head `bef1403` lượt 1 | `CA: 53/53` · `DOT BIEN: 295/295` · `TONG: DAT` rc 0 |
| N3 | full suite head `bef1403` lượt 2 (sau lease xanh) | `CA: 53/53` · `DOT BIEN: 295/295` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT` rc 0 (10:18:49Z → 10:57:31Z) |
| N4 | `ruff check --select F` (ruff 0.17.3) hai tệp, base và head | `All checks passed!` cả hai ⇒ delta 0; `git diff --check` rc 0 |
| N5 | `doctrine-scan` · `adr-song` | rc 0 · rc 0 (55/55) |
| N6 | `ci.yml` lượt PR | chưa đẩy ⇒ chưa đo |
| N7 | `--dot-bien-dong` | KHÔNG chạy: `git_cuc_bo` không thuộc `HAM_DONG`; không khai đạt |

## Review chéo
Codex CHƯA gọi được: `CODEX_AUTH_JSON` có mặt (5860 ký tự) nhưng refresh token đã bị thu hồi; `codex exec` thử
(09:39Z) trả `workspace routing discovery unauthorized (401)`, không chạm model ⇒ không tính vào trần (0/2 đã dùng).
Chờ chủ kho cấp lại `CODEX_AUTH_JSON` hoặc cho `codex login --device-auth`.

## Chưa đo được
Windows native; `ci_dang_ky_test.py --chay`; băm byte lời chủ kho.
