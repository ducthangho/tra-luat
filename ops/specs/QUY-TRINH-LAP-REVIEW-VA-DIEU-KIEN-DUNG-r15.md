# Đặc tả packet — QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG (revision 15)

> **BẢN NHÁP — CHƯA ĐÓNG BĂNG.** Soạn bởi phiên executor Fable 5.1 theo chỉ thị chủ kho
> (`2026-09-24T01:4xZ`: *"Soạn r15 cho phần còn lại"*) để **phiên điều phối** đo `sha256` từ blob, chốt
> `executor`/`generation`, rồi neo lease. Tệp này **không** cấp quyền gì cho tới lúc đó (`S15`).

- `packet_id`: **`wp523`** · `packet_slug`: **QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG**
- `packet_issue`: **523** · `mission_issue`: **499**
- `revision`: **15** · `generation`: **16** *(dự kiến — gen 15 là lease cuối đã cấp; chủ kho/dispatcher chốt)*
- `thay_the_cho`: **revision 14** — nguồn bất biến: `codex/wp523-r14-authority`
  `80cca6f08e1c23b4738fb9467ef466860a3a24e2:ops/specs/QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG-r14.md`,
  `sha256 f36696109983d6ff607e4f20db24933f91982432f50b6ba65165da718e9bbccb`, 14 612 B. r14 **đã land**
  (PR #609, merge `d553efa51bbd659779d20edd71519e7f2d2e2765`, human audit `issuecomment-5792844363`, land
  receipt `issuecomment-5793672613`). r1–r14, nháp r13 của Claude (#605, `a36c147`) và r12 (#586, `816efab`)
  **giữ nguyên trên đĩa làm hồ sơ**; không bản nào bị sửa.
- `executor`: **`claude`** *(đề xuất; chủ kho chốt khi đóng băng)* · `environment`: **`cloud`** ·
  `reviewer_provider`: **`openai_codex`** (review kỹ thuật, khác họ model với executor) ·
  `assurance_target`: **`human_audited`** trên exact candidate (class `sensitive`, §8); nếu codex `approve`
  kèm phép đo thì ghi **thêm** `cross_approved`, không thay chữ ký người.
- `depends_on`: **`[wp610]`** — **ĐÃ THỎA** `2026-09-24T05:14:02Z`: PR #612 merge `ce25a427b87aca9a6352ce4679bb4e7dc56c8235`,
  #610 đóng; validator nhận `surface: codex_desktop` (đo ở `nguon_cap_viec`). `S18` giữ làm luật cho ca tái phát.
- `risk`: **`sensitive`** · `review_class`: **`sensitive`**.
- `immutable_acceptance_baseline`: **`395bc7b1be6c275d8de697f8d8541bb36a290c9e`** (không dời — `S16`,
  `PROTOCOL` §3.2.1). `continuation_base`: **`ce25a427b87aca9a6352ce4679bb4e7dc56c8235`** (canonical sau #612; trước
  đó `d553efa5…` sau #609 — phiên điều phối đo lại `origin/master` lúc đóng băng, không chép số này).

## `nguon_cap_viec` — phần CÒN LẠI của #523 sau khi r14 land

Land receipt r14 (`5793672613`) nói thẳng: *"Whole #523 / M11 / mission499 is NOT complete."* Bookkeeping
(`5793822403`): lease g15 (`quy-trinh-lap-review-r14-g15-codex-evidence`) **hết hạn `2026-09-23T10:52:40Z`
với M11 còn dang dở**; *"Any continuation needs fresh valid authority/generation."* r15 là continuation ấy.

Đo `2026-09-24T01:4xZ` (clone đầy đủ, `is-shallow=false`, `comm -23` rỗng):

| hiện vật | trạng thái đo được |
|---|---|
| nhánh `codex/wp523-r14-evidence` | head `46b20f1d153bb690d9df6ac6cd84c91ca666b4e2`; **4 commit** trên `15d1b10` (`e83726d` · `2462684` · `20bab04` · `46b20f1`); merge-base với master = `15d1b10`; **master KHÔNG là tổ tiên** — tức evidence chưa vào canonical |
| `ops/reviews/wp523-r14-review-1-codex-verdict.md` | blob `00d7f65937f29d2d839825e34321dabd5b1136df`, `sha256 d3078a606d9fa410042c9d02536e2d3b3a9bc52705651b0c76190c6da7bb8aec`, 13 103 B — khớp `verdict_sha256`/`verdict_bytes` trong receipt |
| `ops/reviews/wp523-r14-review-1-codex-verdict.receipt.yaml` | blob `1edff65c520f79343d23364c3ffd2b656e6f12f4`, `sha256 21e16d113b2e1b988747ed88f805b19b1ad19ee24b5c3365df8688f14d150623`, 2 702 B; `packet_id: wp523`, `verdict: approve`, `assurance: advisory_review`, `evidence_url` trỏ commit `e83726dc…` — **CÓ**, là tổ tiên của head evidence; `anchor.cuong_do: "candidate ancestry only; canonical inclusion pending"` |
| `ops/reviews/README.md` | +2 dòng (một hàng mục lục) so master |
| `bien_nhan_v2` trên cây evidence `46b20f1` (nền `d553efa`) | **`rc=1 · 1 vi phạm`**: `model_reviewer_identity.surface='codex_desktop'` không thuộc hợp đồng provider `openai_codex` (`['codex_cli']`) — lý do có `depends_on: [wp610]` |
| `bien_nhan_v2` trên **rig** `ce25a42` + `merge --no-ff 46b20f1` (scratch `ee60848`, cha `ce25a42`+`46b20f1`, đo `05:3xZ` 24-09) | **`rc=0 · 133 ĐẠT v2 · 11/11 · 42 NỢ · 0 vi phạm · 0 KĐĐ · tổng 186 · TỔNG: ĐẠT`** — receipt r14 **ĐẠT v2** sau #612; `e83726dc…` là tổ tiên của merge head; `bien-nhan --packet wp523`/`523` **vẫn 0** (thiếu `role: reviewer`, nợ khai dưới) |
| `packet_loop.py bien-nhan --packet wp523` / `523` trên cây evidence | **0 / 0, rc=11** — 9 biên nhận PR529 **không có trên master** (chỉ ở `claude/quy-trinh-lap-review-r2` `9683d500…`); receipt r14 không có `role: reviewer` nên không được đếm |

## `muc_tieu`

**M-M11:** đưa ba hiện vật M11 của r14 (raw verdict · receipt v2 · hàng mục lục) vào canonical bằng **merge giữ
nguyên commit** (`anchor.loai: canonical_ancestry` đòi `e83726dc…` là tổ tiên của master sau land), sao cho
`bien_nhan_v2` trên master **`rc=0`** với receipt ấy được **ĐẠT v2** — không sửa một byte của verdict/receipt để
qua cổng (`S5`), không alias `codex_desktop`→`codex_cli` (`S18`).

**M-ĐÓNG:** khi M-M11 xong, đăng handoff §7 khai #523 ở trạng thái **`accepted`→`integrated`** cho slice r14 +
M11, kèm bảng nợ kế nhiệm **có tên, có Issue**: #582 (ba lớp hồ sơ) · #583 (scanner, `S4`) · #566 (danh tính
người ký) · `bien-nhan-cua-PR529-khong-o-master` (mới, đo ở trên) · `receipt-r14-thieu-role-reviewer` (mới).
**Không** khai `mission 499 complete`; không khai #582/#583/#566 đóng.

`M1`–`M17`/`N1`–`N8` của r11 (`4a9c71a2e80b285679dd159e7a4efcb29a67a1a9`, `sha256 42b0f477…`) **giữ nguyên**
làm nghĩa vụ; r15 chỉ thi hành `M11`/`M12` (hồ sơ review sống trong git, `run_id` trong biên nhận) cho r14 và
cho chính lượt review của r15.

## `write_set` — chỉ hiện vật review, KHÔNG có tệp sản phẩm

| # | đường dẫn | kiểu | ghi chú |
|---|---|---|---|
| 1 | `ops/reviews/wp523-r14-review-1-codex-verdict.md` | exact | **giữ nguyên byte** từ `00d7f659…`; chỉ đi qua merge |
| 2 | `ops/reviews/wp523-r14-review-1-codex-verdict.receipt.yaml` | exact | **giữ nguyên byte** từ `1edff65c…` |
| 3 | `ops/reviews/README.md` | exact | chỉ thêm hàng mục lục; hàng cũ giữ nguyên |
| 4 | `ops/reviews/wp523-r15-review-<n>-<provider>-verdict.md` | planned | verdict thô của lượt review r15, `n` = 1, 2… |
| 5 | `ops/reviews/wp523-r15-review-<n>-<provider>-verdict.receipt.yaml` | planned | receipt v2, có `role: reviewer`, `packet_id: wp523` **và** `packet_slug` |

Theo phân biệt r11/ADR-0044: đây là **review artifact**, không phải sản phẩm ⇒ trần "≤ 3 tệp · ≤ 300 dòng thêm"
của `sensitive` áp lên tệp sản phẩm — mà r15 có **0** tệp sản phẩm. `A9` vẫn đòi liệt kê **toàn diff** từ
baseline trước khi phân loại. **KHÔNG** đụng `.claude/**`, `docs/PROTOCOL_DA_PHIEN.md`, `ops/bien_nhan_v2.py`,
`packet_loop.py`, `RELEASE_MANIFEST.json`, lease/spec/receipt cũ.

## `ngoai_pham_vi`

1. **Không vá #610 ở đây** (`launcher.py`/`bien_nhan_v2_test.py` là write set của wp610). r15 **chờ** #610 land;
   chừng nào chưa land thì M-M11 là `blocked` (`S18`), không phải "vá tạm".
2. **Không sửa receipt r14** để hợp validator, kể cả thêm `role: reviewer` — nợ `receipt-r14-thieu-role-reviewer`
   khai ra, và lượt review r15 phải tự có `role` đúng.
3. **Không đem 9 biên nhận PR529 lên master** trong r15 — đó là nợ hồ sơ (#582 mở rộng), cần quyết định riêng vì
   chúng neo `verdict_path` và băm theo cây nhánh cũ.
4. **Không vá #582/#583/#566**; không định nghĩa `P0`–`P3` (nợ `DINH-NGHIA-PHAN-HANG-KHONG-CO-NGUON`).
5. **Không tạo tag** `luu-tru/*` (chủ kho: `ops-don-ref.yml tao-tag`, không thu hồi được từ phiên web); nguồn
   r11 vẫn *đúng nhưng chưa bền* — khai, không lấp.

## `nghiem_thu`

| # | nghĩa vụ | đo thế nào (lệnh chạy được) |
|---|---|---|
| `A1` | Diff cuối so `continuation_base` chỉ chạm write set 1–5 | `git diff --name-only ce25a427… <head>`; đường ngoài tập ⇒ `S1` |
| `A2` | Hai blob M11 **byte-identical** với nguồn | `git rev-parse <head>:<path>` = `00d7f659…` / `1edff65c…`; `sha256sum` = `d3078a60…` / `21e16d11…` |
| `A3` | `e83726dc…` là tổ tiên của head ứng viên **và** của merge commit khi land | `git merge-base --is-ancestor e83726dc… <sha>` rc=0; merge **không squash** (`S17`) |
| `A4` | `bien_nhan_v2 --root .` trên exact head **`rc=0`**, receipt r14 **ĐẠT v2**, `0 vi phạm · 0 KHÔNG ĐO ĐƯỢC`, `ĐẠT v2` = nền + 1 (`133` ở nền `ce25a42`) | chạy trên clone **đầy đủ**; clone nông ⇒ `rc=2` KĐĐ, không phải bằng chứng; rig đã chứng minh đạt được (bảng trên) |
| `A5` | Bảy cổng `rc=0` kèm bằng chứng dương trên exact head, nền/head dựng trong MỘT lệnh, delta = 0 là điều kiện **cần** | `doctrine-scan` · `adr-song` · `doc-claims-check --strict` (`ok=true`, `flags 0`) · `release-verify --strict --json` (`ok=true`, `expected == checked`) · `bien_nhan_v2` · `lease_publish_test` (`N/N`, `actionlint 1.7.7` + `shellcheck`) · `git diff --check <base-40> <head-40> --` |
| `A6` | Lượt review r15 để lại verdict thô + receipt v2 (`role: reviewer`, `reviewed_sha` = exact head, `so_p0..p3`, `findings_ids` theo LỚP, `doi_chieu_luot_truoc`) + hàng README; `bien-nhan --packet wp523` ≥ 1 | `python .claude/dev/packet_loop.py bien-nhan --root . --packet wp523` rc=0 |
| `A7` | Chữ ký `human_audited`: bản ghi bền mang `Reviewed commit: <40-hex>` đúng head, `spec_sha256` r15, OID blob của **năm** đường write set tại head, ≥ 1 bằng chứng tự đo | `author_association` chỉ là điều kiện cần (#566); ký trên tóm tắt ⇒ `S14` |
| `A8` | Handoff §7 (M-ĐÓNG) đọc ngược qua API, có bảng nợ kế nhiệm 5 mục ở trên | readback byte-equal (trừ thực thể HTML của đường đọc) |

**Nền đã đo (24-09-2026 `05:4xZ`, `origin/master` `ce25a427b87aca9a6352ce4679bb4e7dc56c8235`, clone đầy đủ,
`core.abbrev=7`, `actionlint 1.7.7` + `shellcheck 0.9.0`, `rc` đọc trực tiếp; nền `d553efa` trước đó cho cùng số):** `doctrine-scan 0` (10 tệp) ·
`adr-song 0` (50↔50) · `doc-claims-check --strict 0` (`ok=true`, `files_scanned 110`, `flags 0`, `advisory 381`) ·
`bien_nhan_v2 0` (`132 ĐẠT v2 · 11/11 · 42 NỢ · 0 vi phạm · 0 KĐĐ · tổng 185`) · `lease_publish_test 167/167` ·
`release-verify` `ok=true`, `180 == 180`. Bảng này **không ghi SHA head** (tệp không thể chứa SHA của commit chứa
nó); bằng chứng head + merge ref nằm ở comment handoff, neo OID 40 ký tự. Đích review là **exact head của PR**;
reviewer dựng object tổng hợp khác thì ghi OID + cha, fetch được thì đo, không thì `KHÔNG ĐO ĐƯỢC` (luật khoá ở
r12 `816efab`, lớp lặp 3 lần trên #586).

## `dieu_kien_dung` — DANH SÁCH ĐẦY ĐỦ, không kế thừa qua con trỏ

- **`S1`** — cần đường dẫn ngoài write set 1–5. DỪNG, xin revision.
- **`S2`** — xuất hiện **tệp sản phẩm** trong diff (`.claude/**`, `docs/**`, `scripts/**`, `ops/*.py`). DỪNG.
- **`S3`** — muốn đụng `docs/PROTOCOL_DA_PHIEN.md` hay `.claude/hooks/**`.
- **`S4`** — muốn vá `packet_loop.py` / `doctrine-scan` / `bien_nhan_v2.py`: nợ #583 / packet #610.
- **`S5`** — muốn sửa `VERDICT.md`, receipt, lease của lượt **đã giao** (kể cả receipt r14 để qua validator).
- **`S6`** — muốn đổi định nghĩa `P0`–`P3` hoặc đổi slug lớp cũ (slug là khoá đếm).
- **`S7`** — merge làm **mất** hàng mục lục cũ trong `README.md` hoặc một hiện vật cũ. DỪNG, báo chủ kho.
- **`S8`** — ĐÃ RÚT từ r7; số để trống có chủ đích.
- **`S12'`** — phép quét "còn sót luật cũ" chỉ khớp theo TÊN.
- **`S13`** — vá một lớp *chỉ để lấy approve* thay vì vì nó sai.
- **`S14`** — ký `human_audited` trên tóm tắt của executor, hoặc `approve` không kèm phép đo tái hiện được.
- **`S15`** — đóng băng spec khi tập lớp/hiện vật chưa đủ (ở r15: khi #610 chưa có kết luận land).
- **`S16`** — dời `immutable_acceptance_baseline` khỏi `395bc7b1…`.
- **`S17` (mới)** — land bằng **squash** hoặc rebase làm `e83726dc…` không còn là tổ tiên của master ⇒ receipt
  r14 mất mỏ neo `canonical_ancestry`. Chỉ merge commit.
- **`S18` (mới)** — `bien_nhan_v2` đỏ vì `surface` không thuộc hợp đồng provider ⇒ `blocked`, **không** alias,
  **không** relabel `codex_cli`, không sửa receipt. (Ca `codex_desktop` **đã thỏa** từ `ce25a42`/#612; luật giữ cho
  ca tái phát, ví dụ validator đổi hợp đồng.)
- **`S19` (mới)** — trần lời gọi review §12: PR mới có bộ đếm mới (**2** lượt/PR); vượt phải có khối `nang_tran`
  của chủ kho (`ai_nang`/`can_cu`/`tran_cu`/`tran_moi`) ghi vào lease **trước** khi gọi. Không cổng nào cưỡng
  chế — kiểm tay. Tiền lệ #586: 4 lượt, không `nang_tran` ⇒ dừng.

## `chua_do_duoc` — khai thẳng

1. **Serving model của reviewer r14** (`model_da_chay: KHONG_DO_DUOC`) — r15 tích hợp receipt **đúng như nó khai**,
   không nâng lên `cross_approved`.
2. **#610 đã land** (`ce25a42`, `05:14Z`) — mục này đóng; còn lại là CI hậu merge của master (`35959038634`, đang chạy lúc soạn).
3. **Tổng lời gọi codex lịch sử của #523** — `KHONG_DO_DUOC` (r14 khai); #586 đo được **4** (`5268934360`
   `5269821633` `5270230401` `5270670271`), #585 **1**, #587 **1**, #597 **4**, #529 **9 receipt**.
4. **Danh tính người ký** (#566) — `author_association` không tách chủ kho khỏi phiên chạy bằng token chủ kho.
5. **Hành vi ĐỌC của người audit** — `KHÔNG ĐO ĐƯỢC`; chữ ký không thay phép dò tìm (bài học #585→r13).
6. **Tag bền cho r11** — chưa có; `A2` của các revision trước và nguồn `M1`–`M17` phụ thuộc nhánh còn sống.

## Lớp kế thừa từ #586 (r12, 4 lượt, 20 lớp) — disposition ở r15

Nguồn: comment tổng kết `issuecomment-5806093695` trên #586 (bảng đủ 20 lớp + id). Tóm theo LỚP:

| lớp | r15 |
|---|---|
| `packet_id`/bí danh `wp523`↔`523`↔slug (lặp ×2) | receipt mới khai **cả hai** khoá; ánh xạ chạy được ⇒ #583 (`S4`) |
| nguồn r11 chỉ tên nhánh / tag bền (lặp ×2) | OID + blob đã neo; tag ⇒ chủ kho (`ngoai_pham_vi` 5) |
| `base_sha` / baseline | `395bc7b1…` giữ (`S16`), continuation `d553efa5…` |
| phạm vi `A2` vs `M11`–`M16` | r15 thi hành `M11`/`M12`; phần còn lại giữ làm nghĩa vụ, khai ở `muc_tieu` |
| `author_association` không đủ | `A7` |
| `N8` bien_nhan rc 1 (bác) / clone nông | `A4` ghi điều kiện đo |
| `diff --check` không range · `KĐĐ ≠ ĐẠT` · đỏ thật ≠ delta 0 · bằng chứng dương doc-claims | `A5` |
| gate trên object tổng hợp (lặp ×3) | luật exact head (mục *Nền đã đo*) |
| đổi acceptance ⇒ revision mới | chính là r15 |
