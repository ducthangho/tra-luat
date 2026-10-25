# Handoff wp929 g1 — executor `claude` (phiên cloud), 25-10-2026

- Packet #929 r1 · lease `ops/leases/wp929-r1-g1-claude.yaml` @ `7ff0f27` · đặc tả `ops/specs/wp929.md`
  sha256 `79251bee45fc39003d13438d741c4e6319dc80ea6b480dc1b931c93d0c6a7ae6` (băm lại trên blob nhánh lease: khớp).
- Nhánh code `agent/wp929-g1-claude`, head **`227dcdebc62c9275f9df09056f66e2124ed5f14c`**, đẩy **một lần**. PR draft #933.
- Packet này **KHÔNG kích hoạt ADR-0054**: trên `origin/master` chỉ chính tệp ADR-0054 chứa cụm khai, nên hàm mới trả False
  (Codex đo lại độc lập ở cả hai lượt).
- Không merge/land/deploy. Không force-push, không rebase, không xoá ref.

## Lịch sử nhánh
| commit | nội dung |
|---|---|
| `393f263` | M1/M2: `_che_do_0054` quét `docs/adr/` theo cụm; bỏ `ADR0055_TEP`. M3/M4: ca (a)–(d), bốn đột biến M4 |
| `75f7a32` | neo lại đột biến cũ `r812_bo_kich_hoat` (ca `moc_dot_bien_phai_khop_DUNG_MOT_CHO` bắt: neo trỏ dòng `a55` đã bỏ) |
| `8a6d795` | merge `origin/master` `5775864` (#928, chỉ `ops/land/**`) — Q4 |
| `227dcde` | vá P2 của Codex lượt 1 (chỉ blob tệp thường) + sáu ca/đột biến phủ P3 |

Master sau đó tiến tới `7009ab9` (#931: `docs/PROTOCOL_DA_PHIEN.md`, thêm `docs/adr/0056-lease-no-progress-six-hours.md`). Không chạm
write set; ADR-0056 không chứa cụm khai (đo: quét mọi `docs/adr/*.md` trên `7009ab9` ⇒ chỉ ADR-0054). **Không merge** để head giữ
đúng commit Codex đã duyệt; CI của PR chạy trên merge ref với master hiện hành.

## Tiêu chí — đo trên đúng `227dcde` (clone thường, `.git` là thư mục, `core.abbrev 7`, không nông)
- **N1** `python .claude/dev/packet_loop_test.py`: `nền: 875/875 đạt · BỎ QUA: 1` (`luong_canonical_chay_that`, chỉ Windows — base
  cũng bỏ qua đúng ca ấy) · SỐ LIỆU máy đếm: ca **876**, đột biến **1249**, lớp lách 78, ca bắt-oan 35 · `TỔNG: ĐẠT` · rc=0 ·
  44m56s. Ca mới: **10** (`r929_*`); đột biến mới: **10** (`r929_*`), mỗi cái `ok … giết N ca đích · 3 đối chứng khác họ còn sống`.
  Base `cdc4e80` (lượt bị cắt ở 30 phút sau phần nền): `nền: 865/865 đạt · BỎ QUA: 1`.
- **N2** bốn đột biến M4 (chạy trên bản sao tạm; đọc tên ca + lớp ngoại lệ):

  | đột biến | ca đích | chết tại |
  |---|---|---|
  | `r929_bo_loai_tru_adr0054` (bỏ loại trừ ADR-0054) | (d) `r929_chi_adr0054_tu_neu_cum` | `AssertionError` khẳng định cuối: đòi False, được True |
  | `r929_mot_tro_len` (≥1 thay vì đúng 1) | (c) `r929_hai_tep_kich_hoat` | `AssertionError` khẳng định cuối: đòi False, được True |
  | `r929_hai_chuoi_roi` (hai chuỗi rời) | (b) `r929_hai_chuoi_roi_khong_tinh` | `AssertionError` khẳng định cuối: đòi False, được True |
  | `r929_duong_dan_co_dinh_0055` (đường dẫn cố định 0055) | (a) `r929_kich_hoat_so_bat_ky` | `AssertionError` khẳng định cuối: đòi True, được False |

  Ma trận đủ (12 đột biến × 12 ca kích hoạt): mỗi đột biến hẹp chỉ giết ca đích của nó. Hai đột biến rộng có chủ đích:
  `r929_duong_dan_co_dinh_0055` còn làm các ca đòi False chết ở bước nền (fixture không còn tên 0055) và `r812_bo_kich_hoat`
  (gỡ cả dòng đo) giết mọi ca đòi False. Ca (e) `r812_r7_activation_adr_name` giữ; đột biến của nó neo lại vào dòng mới.
- **N3** `ruff check --select F` hai tệp: base 3 (1 F841 + 2 F541) · head 3, cùng mã ⇒ delta 0.
- **N4** `doctrine-scan --root .` rc0 · `adr-song --root .` rc0 (54 ADR/54 dòng trên base) · `git diff --check` rc0.
- **N5** `python .claude/dev/ci_dang_ky_test.py` (không `--chay`, không sửa) ⇒ `PHẢN CHỨNG: 1070/1070 đỏ đúng` · `TỔNG: ĐẠT`.
- **N6** chờ CI trên PR #933 — đọc bằng check run, cập nhật ở comment báo cáo trên #929.
- Write set: diff PR đúng 2 tệp, `packet_loop.py` +7/−3, `packet_loop_test.py` +71/−4 (≤ 300).

## Cross-review Codex — 2/2 lời gọi (trần spec Q1 / lease M-1)
Qua `.claude/dev/launcher.py run`, `codex exec -m gpt-6-astra -c model_reasoning_effort=xhigh -s workspace-write`; header
`stderr.log` của cả hai lượt: `model: gpt-6-astra` · `reasoning effort: xhigh`. Sandbox: clone thường detached + SPEC + diff,
không mạng.

| lượt | run_id | prompt sha256 | head | thời lượng | verdict | tệp verdict (sha256) |
|---|---|---|---|---|---|---|
| 1 | `0d78fe118c6340fda716921de68a5d06` | `5104ab54…5a4af` | `8a6d795` | 1337,0 s, rc0 | request_changes | `ops/reviews/wp929-g1-codex-luot1-VERDICT.md` `8a392561…80bbf` |
| 2 | `3536a415068645adab6cfed3e3de5f03` | `35f2eb79…733f5` | `227dcde` | 594,2 s, rc0 | **approve** | `ops/reviews/wp929-g1-codex-luot2-VERDICT.md` `40d42d53…30e49` |

Finding lượt 1 và cách xử lý:
- **P2 `wp929-tree-is-not-activation-file`** (fail-open): `ls-tree --name-only` không phân biệt tree/blob — thư mục `0731-x.md`
  lọt regex, `git show` in tên con chứa cụm ⇒ True. Cùng lớp: symlink (`git show` in ĐÍCH). Vá: đọc `ls-tree -z` đầy đủ, chỉ giữ
  `100644 blob`/`100755 blob`. Ca `r929_thu_muc_ten_md`, `r929_symlink_khong_tinh`; đột biến `r929_bo_kiem_loai_doi_tuong`,
  `r929_nhan_symlink`. Lượt 2: **đóng**, kể cả gitlink.
- P3 biên tên tệp ⇒ `r929_ba_chu_so_khong_tinh`, `r929_duoi_khac_md_khong_tinh` + `r929_so_chu_so_tuy_y`, `r929_bo_duoi_md`. Đóng.
- P3 NFC ⇒ `r929_nfd_van_tinh` + `r929_bo_nfc`. Đóng.
- P3 chốt lỗi git ⇒ nhánh `show`: `r929_show_loi_la_false` (xoá blob loose sau push) + `r929_bo_rc_show`. Đóng.
  **Nhánh `ls-tree` (`ls[0] == 0`) CÒN MỞ — P3, nợ, không chặn** (Codex lượt 2 xếp hạng): bỏ chốt ấy vẫn 159/159 xanh. Mã sản phẩm
  đúng. Codex chỉ ra cách bơm được qua đường `record-lease` thật: wrapper chỉ đổi rc của đúng lệnh
  `ls-tree -z refs/remotes/origin/master docs/adr/` thành 128, giữ stdout. Không thêm vào PR này vì mọi commit mới làm verdict lượt 2
  mất neo mà trần Codex đã hết. Đề xuất: đưa vào packet kế tiếp chạm `packet_loop_test.py` (chuỗi `MAY-ADR-0054` / #834).

## Lỗi/quan sát khác (Q5 — ghi, KHÔNG vá)
- Clone của container phiên này mở ra **nông** (`is-shallow-repository = true`); phải `fetch --unshallow` trước khi đo (hàm
  `_che_do_0054` tự trả False trên kho nông; không đo xem bộ test đỏ thế nào trên checkout nông).
- Sandbox Codex có `commit.gpgsign=true` toàn cục làm fixture `ci_dang_ky_test` rc=128; reviewer cô lập bằng
  `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Không ảnh hưởng phép đo của executor.
- `packet_loop_test.py` trên master vốn đã không ở dạng NFC (trước bản vá); các dòng thêm của packet này đều NFC.
- Bộ suite đầy đủ cần ~45 phút trên container này; nền chạy nền 30 phút mặc định sẽ cắt giữa phần đột biến.

## Việc còn lại (không phải của executor)
- N6: CI PR #933 xanh trên head cuối (executor theo dõi tới xanh).
- Merge/land: chủ kho. `uy_quyen_merge: false`.

## Cập nhật 25-10-2026 ~18:35Z — head drift
- `thu-hoi` (ops-thu-hoi-admission.yml) đỏ trên `227dcde`: `CHAN [12]: S 7009ab9 không phải tổ tiên của H` — master tiến sau khi rẽ nhánh.
- Theo chỉ thị chủ kho ("Xử lý head drift đi"): merge `origin/master` `36057e8` ⇒ head **`f3b54d260bcdecf5b6d2348730a958e168bf7330`**,
  lần đẩy THỨ HAI (ngoài `push_policy` một-lần, có chỉ thị chủ kho). Hai tệp write set giống từng byte `227dcde` ↔ `f3b54d2`
  (`git diff --stat` rỗng); diff PR so master vẫn 2 tệp.
- Trên `f3b54d2`: doctrine-scan rc0 · adr-song rc0 (55/55) · diff --check rc0 · ruff F delta 0 · 160/160 ca `r812_*`/`r929_*`/`moc_dot_bien*`
  đạt; suite đầy đủ tại chỗ: `nền: 875/875 đạt · BỎ QUA: 1` (phần đột biến chạy tiếp). Vẫn chỉ ADR-0054 chứa cụm ⇒ chưa kích hoạt.
- **N6**: CI PR #933 trên `f3b54d2` — 24 check run success, 1 skipped (`launcher`); gồm `gate`, `gate-cong-cu-gop`, `gate-ops`,
  `gate-packet-loop`, `gate-registry` (CHECK_BAT_BUOC) và `thu-hoi`. Codex connector: review `227dcde` xong, không finding.
- **Chờ chủ kho**: verdict Codex lượt 2 neo `227dcde`; có tính cho head merge `f3b54d2` không (trần Codex 2/2 đã hết).
