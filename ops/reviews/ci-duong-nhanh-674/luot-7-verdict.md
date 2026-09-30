Reviewed commit: af1165d04977f2e3de1fa0fdbaa9a1775dd9bd30
verdict: changes_requested
reviewed_sha: af1165d04977f2e3de1fa0fdbaa9a1775dd9bd30
luot: 7 (packet #674 CI-DUONG-NHANH-HO-SO — lượt Opus effort tối đa, thay Codex hết quota)

TONG: P0=0 P1=0 P2=2 P3=1 — hai lớp P2, một lớp P3 (bảng lớp ở dưới)

## Danh tính và mức bảo đảm — đọc trước

- **Reviewer = Claude Opus 5.5, effort tối đa, KHÔNG phải Codex.** Cùng họ model với executor g3. Lượt này
  **KHÔNG** được tính là `cross_approved` của Codex. Model/effort ở trên là **yêu cầu và tự khai**; không có
  receipt runtime độc lập nên model thật chạy lượt này là `KHÔNG ĐO ĐƯỢC`.
- **Mức bảo đảm tối đa có thể kỳ vọng: `human_audited` — cần NGƯỜI.** Packet `sensitive`; protocol đòi
  `human_audited` ở cổng land. Verdict này không cấp quyền land.
- Chỉ thị gốc (chủ kho, qua lời gọi phiên này): "sử dụng opus 5.5 ở mức effort cao hơn để review có hint patch".
- **Có một verdict lượt 7 SONG SONG** đã đăng trước lượt này: `luot-7-opus-af1165d-verdict.md` (commit
  `14fa441`, subagent Opus, lưu bởi phiên Sonnet). Tệp này **không đè** tệp đó. Tôi đã đo lại các kết luận của
  nó (mục ĐỐI CHIẾU) và chỉ báo phát hiện MỚI hoặc phát hiện đã tái hiện độc lập.

## Môi trường

Linux, Python 3.11.15, actionlint 1.7.7, **shellcheck VẮNG**, ruff 0.15.15 (đúng ghim CI), PyYAML 6.0.1.
Mọi phép đo trên clone tạm trong scratchpad; `core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1` cho mọi lượt suite/đột biến.
Mỗi đột biến chạy trên một bản `cp -a` riêng của clone, xoá sau. Không chạy Actions thật, không Windows.
Ref: `ls-remote` ↔ `for-each-ref` so theo TẬP TÊN ⇒ thiếu cục bộ = ∅. Đầu nhánh (ls-remote) =
`af1165d04977f2e3de1fa0fdbaa9a1775dd9bd30`. Đặc tả `ops/specs/CI-DUONG-NHANH-HO-SO-r2.md` (chỉ có trên
`origin/ops/cap-lease-ci-duong-nhanh-ho-so`) sha256 = `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57` — khớp.
Diff `origin/master...HEAD` = đúng bốn tệp của write set g3 (`ci_dang_ky_test.py` +1/-0).

## Số đo nền (a)

| Lệnh | Kết quả |
|---|---|
| `python ops/ci_duong_nhanh_test.py` | `CA: 63/63 dat · 0 do · 0 hong` · `DOT BIEN: 151/151 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT` · rc=0 · 41,6s |
| `KIEM KE` | `hanh_vi=35 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=9 = 63 · dot bien ci_dang_ky_test.py=2 + ci.yml=65 + ci_duong_nhanh.py=44 + ci_duong_nhanh_test.py=40 = 151` |
| `python .claude/dev/ci_dang_ky_test.py` | `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 938/938 đỏ đúng` · `TỔNG: ĐẠT` · rc=0 |
| `actionlint .github/workflows/ci.yml` | rc=0 — **shellcheck vắng**, nên đây là phép đo YẾU (luật shellcheck không chạy) |
| ruff 0.15.15 `--select F` | `scripts/tl.py` 12 F821 (= nền đã ghi); ba tệp packet: 0 ⇒ delta 0 |
| `python scripts/tl.py --selftest` | `== tl selftest 1715/1715 ==` · rc=0 · 3m29s |

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Lớp | Nguồn | Đo lại ở lượt này |
|---|---|---|
| `chot-yaml-chi-do-su-hien-dien` (**nợ #694**) | lượt 6 P2: runner không gọi ca | **ĐÃ VÁ THẬT** cho biểu hiện ấy: đột biến `test_runner_khong_goi_ca` / `..._goi_ca_hai_lan` / `test_entrypoint_rc1_thanh_0` nằm trong 151, bị giết đúng ca. Tôi chạy thêm 10 đột biến của riêng mình (bảng dưới); 5 đột biến YAML đều bị giết bằng ca cấu trúc. Không có phát hiện mới trong lớp này. |
| `bang-do-thieu-neo-va-thieu-kiem-ke` (**nợ #694**) | lượt 6 P3: in thêm dòng KIEM KE sai | **ĐÃ VÁ THẬT**: `test_main_in_them_dong_kiem_ke_sai` và `..._sai_truoc` trong 151, bị giết bởi `t94`. Không có phát hiện mới. |
| `kiem-re-cua-fail-close-chua-co-ca` | lượt 7 song song, P2 | **TÁI HIỆN ĐỘC LẬP** (`kiem_yaml_bo_yml` ⇒ `CA 63/63 · 151/151 · TONG: DAT`), và tìm thêm **một cửa mà hint song song KHÔNG đóng** — xem F2. |
| `kiem-re-phu-thuoc-actor-su-kien` | lượt 7 song song, P3 | **TÁI HIỆN ĐỘC LẬP** — xem F3. |
| Hint song song `luot-7-opus-af1165d-HINT.patch` | — | Phiên Sonnet ghi "CHƯA chạy lại suite". Tôi đã chạy: áp trên `af1165d` ⇒ `CA: 69/69` · `DOT BIEN: 160/160` · `TONG: DAT`. |

## BẢNG LỚP

| Slug | Hạng | Của ai | Gốc lớp | Đường vào đã rà |
|---|---|---|---|---|
| `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` | **P2** | **lỗi MỚI của #674** | `kiem-re` bù cho các bước bị bỏ bằng cách chạy lại ĐÚNG ba ca dữ liệu (t23/t26/t27). Giả định ngầm: "bước bị bỏ chỉ đọc hồ sơ qua ba ca đó". Sai: `t82` của `lease-publish selftest` `copytree` **CẢ cây**, kể cả mọi tệp dưới allowlist, nên LOẠI TỆP (symlink) cũng là dữ liệu mà bước bị bỏ phán, và `kiem-re` không canh loại tệp. | 7 loại tệp hồ sơ "xấu" (dưới) × 8 bước bị bỏ, đo hai vế |
| `kiem-re-cua-fail-close-chua-co-ca` | **P2** | lỗi của #674 (bộ test); tái hiện lượt 7 song song + **một cửa mới** | Các cửa fail-close của helper `kiem-re` được vá theo từng đường reviewer chỉ, không ai liệt kê hết cửa rồi cho mỗi cửa một ca. | `kiem_yaml` (đuôi, tiêu thụ `safe_load_all`), `kiem_lease`, `kiem_diff_check`, `_han_lease` |
| `kiem-re-phu-thuoc-actor-su-kien` | **P3** | chính sách; tái hiện | Đường nhanh gọi validator lease có chốt `GITHUB_ACTOR`, đường đầy đủ không gọi ⇒ ai bấm quyết định màu. | actor rỗng / chủ kho / bot |

Hai lớp nợ của #694 (`chot-yaml-chi-do-su-hien-dien`, `bang-do-thieu-neo-va-thieu-kiem-ke`): **0 phát hiện mới.**

## BẢNG SĂN

### HƯỚNG 1 — Đúng đắn của bộ phân loại (lớp lỗi 6 lượt trước chưa tìm ra)

Đọc toàn bộ `ops/ci_duong_nhanh.py` và phần `ci.yml` đổi. Các đường thoát đã xét bằng lý lẽ + đo:
- `base.sha` cũ (GitHub có thể giữ base của lần mở PR): merge-base lùi về base cũ ⇒ diff **rộng hơn** ⇒ `day_du`. Hỏng về phía đóng.
- Ghi `GITHUB_OUTPUT` rồi hỏng: `main` ghi `che_do=` là thao tác cuối trước `return 0`; biểu thức output `… && steps.phan-loai.outputs.che_do || 'day_du'` ⇒ rỗng/vắng ⇒ `day_du`.
- Tiêm lệnh workflow qua tên tệp: tên ngoài allowlist được in qua `repr` và sau tiền tố `DUONG_NHANH:` nên không đứng đầu dòng; `che_do` là hằng.
- `sys.path[0]` của `python3 ops/ci_duong_nhanh.py` là `ops/`, không phải thư mục allowlist nào, nên tệp hồ sơ không che được module chuẩn.
- Checkout thiếu (`fetch-depth`): mọi job gọi `git diff base...head` đều `fetch-depth: 0` (đọc `ci.yml` dòng 67/128/521/753/817); đột biến `fetch-depth: 1` bị giết.
- **Kết luận: KHÔNG tìm được lỗi phân loại** (không có PR đụng mã nào lọt đường nhanh trong miền đo). Giới hạn đã khai của đặc tả vẫn đúng: PR sửa chính `ci.yml`/bộ phân loại tự quyết đường của mình; chốt cho việc đó là review, không phải mã.

### HƯỚNG 2 — Bước bị bỏ có phán dữ liệu hồ sơ không (đo KẾT QUẢ, không đo lượt đọc)

Lượt 7 song song đo bằng audit hook (lượt `open`/`scandir`). Tôi đo **kết quả**: dựng hai vế trong MỘT lệnh
(`exp/run.sh`), vế `nen` = `af1165d`, vế `dot` = `af1165d` + sáu tệp hồ sơ xấu, rồi chạy **mọi** bước bị bỏ ở cả hai vế.

Sáu tệp vế `dot` (commit `9ce2791`): `ops/reviews/zz-crlf.md` (CRLF) · `ops/specs/zz_hong.py` (lỗi cú pháp) ·
`ops/land/zz.json` (JSON hỏng) · `ops/reviews/zz-link.md` (symlink HỢP LỆ tới `../../CLAUDE.md`) ·
`ops/specs/zz-bin.txt` (không phải UTF-8) · `ops/reviews/tên có dấu.md`.

| Bước | nen | dot |
|---|---|---|
| phân loại | `duong_nhanh` | `duong_nhanh` |
| `kiem-re` | rc=0 | rc=0 (6 tệp, 0 lỗi) |
| release-check full · golden · determinism · release-bundle ×2 cmp | rc=0 · 0 · 0 · 0 | rc=0 · 0 · 0 · 0 |
| packet_loop_test | rc=0 | rc=0 |
| gate_lifecycle_test | 28/28 | 28/28 |
| tl selftest | 1715/1715 | 1715/1715 |
| lease_publish_test | 185/187, ĐỎ `t137` `t159` | 185/187, ĐỎ `t137` `t159` |

`t137`/`t159` đỏ **ở cả hai vế**: chúng đòi shellcheck, container này không có ⇒ đỏ sẵn của môi trường, **delta = 0**.
Sáu loại tệp trên: **không phải lỗi**. Riêng loại **symlink TREO** thì ra delta — xem F1.

### HƯỚNG 3 — Timeout `chuan-bi` 10/5/20 + `continue-on-error`

- `if:` của bước phân loại không có hàm trạng thái ⇒ GitHub thêm `success()` ngầm; checkout hỏng nhưng có `continue-on-error` ⇒ trạng thái job vẫn success ⇒ bước phân loại vẫn chạy, không có script ⇒ rc≠0 ⇒ output vắng ⇒ `day_du`. Hết giờ bước ⇒ cùng đường. Hết giờ job (20) ⇒ `chuan-bi` đỏ ⇒ ba context bắt buộc không được tạo ⇒ PR bị **chặn** (đóng, không mở). 10+5 < 20.
- Đột biến gỡ ba timeout đã được phiên `session_01Fd7YEcw3odAk7QKkydKycE` đo (comment 5894996971), và các ca `y13`/`y16` nằm trong 63/63 ở đây.
- **Không có finding.** Timeout thật trên Actions: `KHÔNG ĐO ĐƯỢC`.

### HƯỚNG 4 — Răng của bộ test: 10 đột biến của reviewer (`mut.py`, mỗi cái một bản sao)

| Đột biến | Kết quả | Ca đỏ |
|---|---|---|
| `kiemre_rc_luon_0` (`lenh_kiem_re` luôn trả 0) | GIẾT | t20b t20c t20e t20f t20g |
| `het_han_khong_exit8` (validator lease hết hạn không `SystemExit(8)`) | GIẾT | t20f t20g |
| `kiemre_chi_nhan_dong_dau_loi` (vứt lỗi của `kiem_yaml`) | GIẾT | t20b |
| `yml_kiemre_bo_doctrine` | GIẾT | y08 y14 |
| `yml_kiemre_nuot_loi` (`\|\| true`) | GIẾT | y08 y14 |
| `yml_chuanbi_env_dau_la_goc` | GIẾT | y01 y13 |
| `yml_fetch_depth_1` | GIẾT | y01 y13 |
| `yml_selftest_packet_bo` (thêm `if` theo `che_do` vào bước test của packet) | GIẾT | y04 y09 y12 y13 |
| **`kiem_yaml_bo_yml`** | **SỐNG** — `CA 63/63 · 151/151 · TONG: DAT` | — (trùng lượt 7 song song) |
| **`kiem_yaml_chi_tai_lieu_dau`** (`next(safe_load_all)`) | **SỐNG** — `CA 63/63 · 151/151 · TONG: DAT` | — ⇒ F2 |

## FINDINGS

### F1 · `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` [P2] — lỗi MỚI của #674: symlink treo dưới allowlist xanh ở đường nhanh, đỏ trên master

**Vấn đề.** `kiem-re` là bước bù duy nhất cho tám bước bị bỏ. Nó chạy lại ba ca dữ liệu vì cho rằng đó là toàn bộ dữ liệu
hồ sơ mà bước bị bỏ phán. Nhưng `lease-publish selftest` còn có `t82_A10_dot_bien_A1_A8_tren_ban_sao_CA_CAY_ten_rieng`,
và ca đó chạy `shutil.copytree(HERE.parent, …)` trên CẢ cây, mặc định đi theo symlink. Một symlink treo dưới
`ops/{land,leases,reviews,specs}/**` qua được mọi kiểm của `kiem-re`, rồi làm `t82` ném `shutil.Error`. Tức là PR hồ sơ
đó xanh cả ba required check trên PR, nhưng `gate-ops` **ĐỎ trên master** ở lượt push sau merge. Hỏng theo chiều mở:
đường nhanh cho qua đúng thứ mà đường đầy đủ từ chối. Đó là rủi ro gốc của cả packet.

**Phản chứng chạy được** (`exp2.sh`, hai vế trong MỘT lệnh; vế `dot` = `af1165d` + `ln -s khong-ton-tai ops/specs/zz-treo.md`, commit `6d2c0a0`):
```
dot HEAD=6d2c0a0ae162de0ae17670b8bac8d52f12a2295d
ops/specs/zz-treo.md
nen phan-loai rc=0 che_do=duong_nhanh
nen kiem-re rc=0 | DUONG_NHANH: kiem-re DAT (0 tep doi, 0 loi)
nen t82 rc=0 | DAT t82
dot phan-loai rc=0 che_do=duong_nhanh
dot kiem-re rc=0 | DUONG_NHANH: kiem-re DAT (1 tep doi, 0 loi)
dot t82 rc=1 | shutil.Error: [('…/dot/ops/specs/zz-treo.md', '/tmp/lp_…/repo/ops/specs/zz-treo.md', "[Errno 2] No such file or directory: …
```
Chạy trọn các bước bị bỏ trên hai vế này (`exp2b.sh`):

| Bước | nen | dot |
|---|---|---|
| release-check full · golden · determinism · release-bundle ×2 cmp | rc=0 · 0 · 0 · 0 | rc=0 · 0 · 0 · 0 |
| packet_loop_test | rc=0 | rc=0 |
| tl selftest | 1715/1715 | 1715/1715 |
| lease_publish_test | **185/187**; ĐỎ `t137` `t159` (shellcheck vắng, đỏ sẵn) | **184/187**; ĐỎ `t137` `t159` **+ `t82_A10_dot_bien_A1_A8_tren_ban_sao_CA_CAY_ten_rieng`** |

Delta = đúng **một ca**: `t82`. Mọi bước bị bỏ khác không đổi.

Symlink **hợp lệ** (`zz-link.md` ở Hướng 2) thì không có delta. Chỉ loại **treo** mới lộ ra. Hint vẫn chặn cả
hai loại, vì hồ sơ không cần symlink, và một symlink hợp lệ trỏ ra ngoài vùng hồ sơ sẽ biến thành treo ngay khi
đích bị xoá ở một PR sau.

**Mức độ: P2, không phải P1.** Hậu quả là master đỏ **nhìn thấy được**, không có mã nào lọt qua. Khả năng xảy
ra thấp. Nhưng đây là đúng lớp lỗi "đường nhanh ≠ đường đầy đủ" mà sáu lượt trước không tìm được. Nó cũng cho
thấy danh sách ba ca dữ liệu là một danh sách CẤM đoán trước: nó chặn ba thứ đã biết, không phải mọi thứ mà
bước bị bỏ phán.

**Hint (write set g3; hai tệp):** thêm `kiem_loai_tep(doi, kho)` vào `ops/ci_duong_nhanh.py` để chặn mọi tệp
hồ sơ đổi là symlink, rồi nối nó vào `lenh_kiem_re`. Kèm ca `t20n_kiem_re_symlink_ho_so_do`, gồm một đối chứng
không có symlink (phải ĐẠT), và hai đột biến: `kiem_re_bo_loai_tep` (gỡ lời gọi) và `loai_tep_cho_symlink_qua`
(gỡ vị từ). Mỗi đột biến giết đúng `t20n`. Xem `luot-7-HINT.patch`.

**Nợ còn lại (khai, không vá):** hint này đóng loại tệp *symlink*. Lối ra gốc là thay danh sách ba ca bằng một
danh sách CHO PHÉP cho các bước bị bỏ. Cụ thể: với mỗi bước bị bỏ, đo tập ca đọc cây thật, rồi đòi `kiem-re`
chạy đúng tập ấy. Việc này nằm ngoài một bản vá tối thiểu. Tôi đề xuất đưa nó vào #694 hoặc một successor, và
ghi thành nợ có tên `buoc-bi-bo-doc-ca-cay`.

### F2 · `kiem-re-cua-fail-close-chua-co-ca` [P2] — tái hiện, cộng MỘT cửa mà hint song song không đóng

- Tôi xác nhận chín cửa của lượt 7 song song bằng một đại diện, `kiem_yaml_bo_yml` (SỐNG, TONG: DAT). Tôi chưa chạy lại cả chín.
- **Cửa mới:** `kiem_yaml` phải tiêu thụ HẾT `safe_load_all`. Đột biến `list(yaml.safe_load_all(f))` →
  `next(yaml.safe_load_all(f), None)` cho kết quả `CA 63/63 · DOT BIEN 151/151 · TONG: DAT` trên `af1165d`.
  Trên cây đã áp **cả hint song song lẫn hint symlink bản đầu**, đột biến ấy cho `CA: 70/70` (không ca hành vi
  nào đỏ). Tổng vẫn ra `TONG: DO`, nhưng chỉ vì nó làm hỏng neo của đột biến song song `kiem_yaml_tep_xoa_cat_vong`
  (`HONG … neo … thay 0`). Đó là **tín dụng giả**, không phải một lần giết.
- Hệ quả: một tệp hồ sơ YAML nhiều tài liệu có tài liệu SAU bị hỏng. Ví dụ `ops/land/nhieu.yaml` chứa
  `a: 1\n---\nb: [1, 2\n` thì HEAD bắt đúng (`YAML khong parse duoc: … ParserError`). Nhưng không ca nào khoá
  hành vi ấy, nên một lần "tối ưu" về lấy tài liệu đầu sẽ lọt.
- **Hint:** ca `t20o_kiem_re_yaml_nhieu_tai_lieu_hong_o_sau_do` và đột biến `kiem_yaml_chi_tai_lieu_dau`, chỉ sửa
  tệp test. Nằm trong `luot-7-HINT.patch`.

### F3 · `kiem-re-phu-thuoc-actor-su-kien` [P3] — tái hiện độc lập; chính sách, chủ kho quyết

Chạy `kiem_lease` trên lease thật `ops/leases/ci-noi-bang-vao-gate-exec-1-claude-20260822.yaml`:
```
'' []
'ducthangho' []
'claude[bot]' ["kiem lease (het han) rc=8 cho '…': CHAN [4]: GITHUB_ACTOR='claude[bot]' không có thẩm quyền cấp lease — …"]
```
Tôi không vá: chốt actor là lớp danh tính duy nhất mà GitHub xác thực. Đề xuất giữ nguyên như lượt 7 song song:
khai hệ quả vào docstring D2, hoặc chủ kho chọn lọc `GITHUB_ACTOR` như fixture `t23`. Hint không chứa phần này.

## ĐO HINT

| Cây | Kết quả |
|---|---|
| `af1165d` + `luot-7-HINT.patch` | `git apply --check` OK · `CA: 65/65` · `DOT BIEN: 154/154 bi giet dung ly do` · `KIEM KE: … = 65 · … ops/ci_duong_nhanh.py=47 … = 154` · `TU KIEM DAT` · `TONG: DAT` · rc=0 · ruff F sạch · actionlint rc=0 |
| `af1165d` + hint song song + `luot-7-HINT.patch` (áp theo thứ tự ấy) | cả hai áp sạch · `CA: 71/71` · `DOT BIEN: 163/163` · `TONG: DAT` · rc=0 |

Hint **đã chạy trên bản sao**, chưa chạy trên cây packet thật. Executor g3 tự áp, tự đo và tự commit.

## CHƯA ĐO ĐƯỢC

Các mục dưới đây nằm ngoài tầm đo của lượt này:
- chạy thật trên Actions;
- timeout thật;
- Windows;
- actor thật của PR hồ sơ;
- `actionlint` có shellcheck (container này thiếu shellcheck, nên hai ca `t137`/`t159` của lease_publish_test đỏ sẵn ở cả hai vế);
- model và effort thực chạy của chính lượt review này.

---
Reviewer: Claude Opus 5.5, effort tối đa (tự khai). KHÔNG phải Codex. Assurance tối đa kỳ vọng: `human_audited`, tức là cần NGƯỜI.
