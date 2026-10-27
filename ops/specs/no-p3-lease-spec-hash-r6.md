# Đặc tả packet `no-p3-lease-spec-hash` r6 — revision DELTA trên r5: luật `depends_on` (3) mới, dời nền, đo lại

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-lease-spec-hash` |
| `packet_issue` | #751 (`open` lúc 16:59:45Z 27-10-2026, thời điểm comment chủ kho ở hàng dưới). |
| `revision` | 6 |
| `dang_revision` | **DELTA trên r5**, r5 lại là delta trên r4. Căn cứ: hai quyết định chủ kho trên #751 — https://github.com/ducthangho/tra-luat/issues/751#issuecomment-6407123228 (`OWNER`, 2026-10-26T02:50:01Z; mục 3: revision delta) và https://github.com/ducthangho/tra-luat/issues/751#issuecomment-6448208834 (`OWNER`, 2026-10-27T16:59:45Z; luật `depends_on` (3) mới, "Áp từ r6"). Thân comment `6448208834` đọc lại bằng REST và so từng byte với bản soạn: khớp (1143 ký tự sau khi bỏ khoảng trắng đầu cuối và chuẩn hoá CRLF). |
| `thay_the_cho` | **r5**: `ops/specs/no-p3-lease-spec-hash-r5.md`, sha256 `798afca7ed7c61e65048c59a8458011ea1ea169b812918bde18141c7f1b5751d`, blob `b2eae59e9cbd92ea0c8966a28de59bae4bdb6859`, 136 dòng, commit `973e4b4` (merge vào `master` qua PR #944). r5 thay **r4**: sha256 `40c88b13806e285b1d85961ed9ff99ed89ed2108cdca94d0d8dd6177de0530fd`, blob `d0ba32d208e437e9124be6e1b97d72cfa70ac6f1`. Cả hai tìm ở `master` (đo 17:15Z 27-10-2026 tại `ef34d88`: băm khớp); thứ định danh là băm. r6 không sửa byte nào của r1–r5. Mọi closure, lease và `spec_hash` từ nay neo **r6**. |
| `review_class` | **sensitive**, như r4/r5. Hai dòng khai dưới bảng giữ nguyên OID của r5. Ba phép đo OID của mỗi dòng đo lại 17:15:49Z 27-10-2026, dưới hợp đồng môi trường đo, trên bản bare của `depends_on` (2) (`rev-parse --is-shallow-repository` ra `false`, `master` máy chủ `ef34d88`): ADR-0053 `8ab1007…` rc 0 · 128 · 0; ADR-0055 `d2e3052…` rc 0 · 128 · 0. Hai tệp ADR byte-identical giữa `f9f4a8d` và `ef34d88`. |
| `base` | `ef34d88838bc125727670f494b15213b6c6f0c8d` (merge PR #984) — `master` máy chủ lúc soạn. Từ `f9f4a8d` (nền r5): 42 merge first-parent. `git diff --numstat f9f4a8d ef34d88`: ĐỔI `.claude/dev/ci_dang_ky_test.py` +4/−1 (hai dòng `MOI` mới — `ops/codex_cloud_setup_test.py`, `ops/ci_provenance_test.py` của #899 — và một dòng chú thích của #923 r2), `docs/PROTOCOL_DA_PHIEN.md` +5/−2, `ops/reviews/README.md` +110/−19, ADR-0056 +11/−4; KHÔNG ĐỔI (blob bằng nhau) `ops/lease_publish.py`, `ops/lease_publish_test.py`, `ops/ci_duong_nhanh_test.py`, `.github/workflows/ci.yml`, `.github/workflows/ops-publish-lease.yml`, `ops/ci_duong_nhanh.py`, `ops/README.md`, `.claude/dev/chon_reviewer.py`, `.claude/skills/soan-spec/SKILL.md`, ADR-0053, ADR-0055, r4. `ops/leases/` đổi (171 → 172 tệp). |
| `write_set` | Như r4/r5, không đổi: `ops/lease_publish.py` · `ops/lease_publish_spec_hash_test.py` (MỚI) · `.claude/dev/ci_dang_ky_test.py` (+1 dòng `MOI`, Mục tiêu 6). |
| `depends_on` | **CHẶN cấp lease** cho tới khi ĐỦ năm điều kiện, đo lại lúc cấp; (3) đọc theo luật MỚI ở mục **Luật `depends_on` (3) từ r6**. Hiện trạng lúc soạn r6 (17:00Z–17:20Z 27-10-2026): **(1)** ĐÃ, như r4. **(2) ĐỎ** — xem hàng `ai-dang-giu` ở mục Đo lại: `.claude/dev/ci_dang_ky_test.py` `NGƯỜI_GIỮ 1: wp923-r3-g3-claude`, rc 11 (lease r3 của #923, nhánh `ops/wp923-r3-g3-lease` @ `13a13bc3`, commit 15:08:09Z 27-10-2026, `lease_until 2026-10-29T13:50:00Z`, `spec_path ops/specs/wp923-r3.md`, `thay_the_cho: [wp923-r2-g2-claude]`; PR #992 của lease ấy sửa đúng một fixture `_gk` trong sổ, +3/−1). Năm đường dẫn còn lại: `NGƯỜI_GIỮ 0`. Lease thực thi của #751 CHỜ `wp923-r3-g3-claude` hết hạn, bị thu hồi hoặc #923 r3 land; đo lại (2) lúc cấp. **(3)** theo luật mới: KHÔNG kích hoạt tính từ nền r5 — phép so AST ở mục Đo lại ra giống hệt trên `ef34d88` VÀ trên head của PR #992 (`agent/wp923-g3-claude`), nên #923 r3 land cũng không bắt revision mới. **(4)** #763 land qua PR #930, #899 land qua PR #945; luật như r5: không lease nào của #751 đồng thời với một lease còn hiệu lực khác giữ sổ — hiện là `wp923-r3-g3-claude`. **(5)** ĐÃ, như r5. |
| `kich_thuoc` | Như r4/r5. |

tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544

## Luật đọc delta

1. Thân đặc tả của packet này là **r4 cộng r5 cộng tệp này** (băm ở hàng `thay_the_cho`). Chỗ nào ba bản nói khác nhau, bản MỚI hơn
   thắng. Mọi mục r4 và r5 mà tệp này không nhắc thì áp nguyên văn, với ba luật thay thế của r5 mục "Luật đọc delta" (2) đọc lại
   cho r6: nền là `ef34d88`; số dòng dời theo bảng ánh xạ của r5 rồi tiếp theo bảng ánh xạ ở mục Đo lại dưới đây; số đo nền là số
   ở mục Đo lại dưới đây.
2. Thiết kế, write set, yêu cầu của Mục tiêu 1–6 và **40 ca** của r4 giữ nguyên. A7 đọc theo chữ tương đối của r4 (`N+1/N+1`, N ở
   nền lúc cấp).
3. Lease thực thi neo `spec_path` = tệp này, `spec_hash` = sha256 byte của blob tệp này. Executor đọc cả r4, r5 (lấy theo băm) và
   r6; reviewer đo băm cả ba trước khi đọc.

## Luật `depends_on` (3) từ r6

Thay chữ `depends_on` (3) của r4 và r5. Nguyên văn quyết định chủ kho, comment `6448208834`, mục 1–2:

> 1. **Revision mới CHỈ bắt buộc** khi, sau nền của revision đang hiệu lực, `master` đổi một trong các thứ sau:
>    (a) `ops/lease_publish.py` hoặc `ops/lease_publish_test.py` (bất kỳ byte nào);
>    (b) trong `.claude/dev/ci_dang_ky_test.py`: thân một trong các hàm `tim`, `kiem`, `bang_chung_xanh`, `chay_moi`, `_git_bo_qua` (so qua AST, bỏ số dòng), hoặc dạng của `MOI` / `DA_NOI` / `DANG_KY` khác với việc thêm, bớt hay sửa từng mục;
>    (c) dòng mẫu `"ops/nhanh_don_duoc_test.py"` mà Mục tiêu 6 chép nguyên.
> 2. **Mọi thay đổi khác** của ba bộ đo nền (thêm/bớt dòng `MOI`, sửa chú thích, thêm ca hay đột biến) **KHÔNG** bắt revision mới. Khi cấp lease thực thi, người cấp đo lại trên `master` lúc cấp và ghi số vào lease: ba bộ đo nền, A6, A7 (N lấy ở `master` lúc cấp, đích `N+1/N+1`), cùng phép so AST của mục 1 (b). Nền thực thi là `master` lúc cấp.

Đọc cho r6, khai thẳng chỗ chữ quyết định để ngỏ:

- "Nền của revision đang hiệu lực" là `ef34d88`. Phép so (a)–(c) chạy giữa `ef34d88` và `master` lúc cấp.
- "Phép so AST" của (b): với mỗi tên trong năm hàm, `ast.dump(node)` (mặc định, không kèm thuộc tính vị trí) của nút
  `FunctionDef` cấp mô-đun mang tên ấy phải bằng nhau ở hai nền; với `MOI`, `DA_NOI`, `DANG_KY`, kiểu nút giá trị của lệnh gán cấp
  mô-đun (đo được: `Dict`, `Set`, `BinOp`) phải bằng nhau. Thiếu tên ở một trong hai nền ⇒ coi là ĐỔI. Đây là đúng phép đã chạy ở
  mục Đo lại; tệp này không thêm phép nào khác vào chữ "so qua AST".
- (c) đo bằng đếm số dòng khớp NGUYÊN BYTE `    "ops/nhanh_don_duoc_test.py": r"^(\d+)/(\d+)$",` (bốn khoảng trắng đầu dòng) trong sổ:
  phải đúng 1 ở cả hai nền.
- "Nền thực thi là `master` lúc cấp": lease ghi `base_sha` = `master` lúc cấp; mọi chữ "nền lúc cấp" / `<nền>` trong Nghiệm thu r4
  là OID ấy. Số đo ghi vào lease thay số ở mục Đo lại dưới đây cho mọi tiêu chí.
- Điều kiện cấp lease vẫn đủ năm mục; luật mới chỉ thay (3).

## Thay đổi so với r5

- **Luật `depends_on` (3)** thay bằng luật ở mục trên (quyết định `6448208834`). Đây là thay đổi tiêu chí duy nhất của r6.
- **Nền** `f9f4a8d` → `ef34d88`.
- **`depends_on` (2)**: người giữ sổ nay là `wp923-r3-g3-claude` (r5: `wp899-r4-g5-claude`, lease ấy đã bị thay thế sau khi #899 land).
- **Số đo**: sổ `ĐĂNG KÝ` 26/26 → **28/28** (`PHẢN CHỨNG` giữ 1070/1070); A7 đích 27/27 → **29/29**; `ci_duong_nhanh_test`,
  `lease_publish_test`, ruff F giữ nguyên; quần thể lease 171 → 172 tệp, A6 giữ đúng một lease trong tập đổi rc.
- **Số dòng** dẫn vào tệp đã đổi: bảng ánh xạ `f9f4a8d` → `ef34d88` ở mục Đo lại, áp SAU bảng của r5.
- Hai dòng khai trần giữ nguyên OID của r5 (dòng khai phải nằm trong chính blob mà `spec_hash` trỏ tới, nên chép lại ở đây).

## Đo lại nền tại ef34d88

Phiên điều phối Claude đo; KHÔNG phải một lượt review. Hợp đồng môi trường đo, phiên bản công cụ (Python 3.11.17 + PyYAML 6.0.1,
git 2.43.0, actionlint 1.7.7, shellcheck 0.9.0, ruff 0.16.9) và các độ lệch (1), (2), (5) như r5. Khác r5: mọi phép đo dài chạy
thẳng trên `ef34d88`, không qua một nền trung gian. Giờ UTC, mọi mốc là 27-10-2026.

| mục (đơn vị) | r5, nền `f9f4a8d` | r6, nền `ef34d88` | lúc đo | lệnh hoặc kịch bản |
|---|---|---|---|---|
| `ops/lease_publish_test.py` (ca) | 267/267 | **267/267** (`đã chạy=267, bỏ qua=0`), rc 0 | 17:00:38Z–17:05:44Z | `do_nen.sh` |
| sổ: `ĐĂNG KÝ` · `TRẠNG THÁI` · `PHẢN CHỨNG` · `TỔNG` | 26/26 · `chan=26` · 1070/1070 · `ĐẠT` | **28/28** · `chan=28 cach_ly=0` · 1070/1070 · `ĐẠT`, rc 0 | 17:00:38Z–17:00:45Z | `do_nen.sh` |
| `ci_duong_nhanh_test`: `CA` · `DOT BIEN` · `TONG` | 104/104 · 392/392 · `DAT` | 104/104 · 392/392 · `DAT`, rc 0 | 17:00:38Z–17:03:05Z | `do_nen.sh` |
| ruff F trên `ops/lease_publish.py` | 2 F841, dòng 198–199 | như r5 | 17:00:38Z | `do_nen.sh` |
| `ops/leases/*.yaml` · có `spec_path` + băm · cả hai trường · khớp · lệch | 171 · 118 · 18 · 113 · 5 | **172 · 119 · 19 · 114 · 5** | 17:15:47Z | `m_cay.py` |
| `write_set_hash`: có scope, khớp · không scope, khớp | 6, 6/6 · 67, 4/67 | 6, 6/6 · **68, 5/68** | 17:15:47Z | `m_cay.py` |
| mang `spec_sha256` · không kèm hai tên kia | 61 · 5 | 61 · 5 | 17:15:47Z | `m_cay.py` |
| A6 nền · ứng viên (lease theo rc) | `{0: 157, 8: 9, 10: 5}` · `{0: 156, 8: 9, 10: 5, 13: 1}` | **`{0: 158, 8: 9, 10: 5}`** · **`{0: 157, 8: 9, 10: 5, 13: 1}`** | –17:14:18Z | `do_a6.py` |
| A6 tập đổi rc | {`gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906` 0 → 13} | CÙNG tập | –17:14:18Z | `do_a6.py` |
| A6 miễn bia mộ · kiểm spec khớp · kiểm write set khớp · đột biến bỏ miễn đổi rc | 46 · 66 · 4 · 5 | 46 · **67** · 4 · 5, cùng năm tên | –17:14:18Z | `do_a6.py` |
| A7 đích (tệp thế chỗ + dòng `MOI`) | 27/27 | **N = 28 ⇒ `ĐĂNG KÝ: 29/29`**, `chan=29`, `PHẢN CHỨNG: 1070/1070`, `TỔNG: ĐẠT`, rc 0; numstat sổ `1 0`; `chay_moi` trả 0, `CI_DANG_KY ops/lease_publish_spec_hash_test.py: ĐẠT rc=0`; `ci_duong_nhanh_test` 104/104 · 392/392 · `DAT` | 17:05Z–17:14Z | `do_a7.sh` |
| A7 bỏ dòng `MOI` | 27/26 · 103/104 · 391/392 | **`ĐĂNG KÝ: 29/28`**, đúng một dòng `ĐỎ: test sống chưa đăng ký: ops/lease_publish_spec_hash_test.py`, `TỔNG: ĐỎ`, rc 1 · 103/104, 391/392, `TONG: DO`, rc 1, `k01_so_dang_ky_nhan_muc_da_noi` ĐỎ | 17:05Z–17:14Z | `do_a7.sh` |
| `ai-dang-giu` ba đường dẫn write set (rc) | 0 · 0 · 11, `wp899-r4-g5-claude` | 0 (17:05:49Z) · 0 (17:06:11Z) · **11, `wp923-r3-g3-claude`** (17:06:54Z, lặp lại 17:14:33Z) | 17:05:44Z– | `adg_r5.sh` (bản bare MỚI, hợp đồng môi trường đo) |
| `ai-dang-giu` `lease_publish_test.py` · `ci_duong_nhanh_test.py` · `ci.yml` (rc) | 0 · 0 · 0 | 0 (17:07:47Z) · 0 (17:14:54Z) · 0 (17:15:17Z) | | lượt đầu cho hai đường dẫn sau ra rc 12 (17:08:39Z, 17:10:18Z; dòng `KHÔNG_XÁC_ĐỊNH` không được lưu) — máy chủ có 674 nhánh lúc fetch, 676 ở lượt lặp; lượt lặp trên bản bare MỚI fetch lại (`adg3.sh`) ra rc 0 |
| nhánh máy chủ · thiếu/thừa so `refs/remotes/origin` · so `refs/heads` | 619 · 0/0 · 0/0 | 674 · 0/0 · 0/0 (17:05:49Z); 676 · 0/0 · 0/0 (lượt lặp) | | tập tên + OID; `remote get-url origin` đúng URL |
| luật (3) mới, (b): năm hàm · dạng `MOI`/`DA_NOI`/`DANG_KY` | — | GIỐNG HỆT giữa `f9f4a8d` và `ef34d88`, và giữa `f9f4a8d` và head PR #992 (`5a05d47`); kiểu giá trị `Dict` · `Set` · `BinOp` | 17:17:09Z | `ast.dump` cấp mô-đun |
| luật (3) mới, (c): dòng mẫu nguyên byte | — | 1 · 1 · 1 (`f9f4a8d` · `ef34d88` · head PR #992 `5a05d47`) | 17:17:09Z | `grep -c` nguyên dòng |

### Bảng ánh xạ dòng `f9f4a8d` → `ef34d88` (áp sau bảng `1d7e642` → `f9f4a8d` của r5)

- `.claude/dev/ci_dang_ky_test.py` (2442 dòng cũ): 1–55 +0 · 56 +1 · 57–756 +2 · 757 ĐỔI → 759 · 758–806 +2 · 807–2442 +3.
- `docs/PROTOCOL_DA_PHIEN.md` (1567 dòng cũ): 1–242 +0 · 243 ĐỔI → 243–246 · 244–1531 +3 · 1532 ĐỔI → 1535 · 1533–1567 +3.
- `ops/reviews/README.md`: 361–565 +15 (các dòng khác: `anh_xa.py`); ba dòng r4 dẫn 414 · 445 · 484 → **429 · 460 · 499**, cùng chữ.
- `ops/ci_duong_nhanh_test.py`, `.github/workflows/ci.yml`: không dời.

Neo đã kiểm tại `ef34d88`: sổ `MOI` 38–57 → **38–59**, dòng mẫu vẫn **53**, `DANG_KY` 84 → **86**, `_git_bo_qua` 87 → **89**, `tim` 106 →
**108**, `kiem` 642 → **644**, `bang_chung_xanh` 679 → **681**, `chay_moi` 1057 → **1060**; `ci.yml` `gate-registry` **943**, `--chay`
**1015**; PROTOCOL 662–663 → **665–666**, 710 → **713**, 719–721 → **722–724**, 1480–1481 → **1483–1484**, §20 1521 → **1524**, 1529 →
**1532**; cùng chữ.

Kịch bản đo — trong scratchpad của phiên điều phối, KHÔNG có trong kho; sha256, 12 ký tự đầu: `do_nen.sh` `b37eff71e2c5…` ·
`m_cay.py` `4bc64195ec92…` · `do_a6.py` `aea18082649a…` · `do_a7.sh` `3c1190c60810…` (bản r5 với nền `ef34d88`) · `adg_r5.sh`
`6a309d4979ac…` · `adg3.sh` `77a297f113f3…` (cùng `adg_r5.sh`, ba đường dẫn, in đủ dòng) · `chay_het.sh` `1db2f8ffb562…` · `anh_xa.py`
`71e8830f9956…`.

Hệ quả cho người cấp lease: theo luật (3) mới, lúc cấp chỉ cần chạy lại các phép ở bảng trên trên `master` lúc cấp, ghi số vào lease,
và chạy phép so (a)–(c) giữa `ef34d88` và `master` lúc cấp. Nếu #923 r3 (PR #992) land trước, sổ có `ĐĂNG KÝ` không đổi (PR ấy
không thêm dòng `MOI`) và phép so (b), (c) đã đo trên head của nó ra giống.
