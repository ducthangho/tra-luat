# Đặc tả packet — QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG (revision 12)

- `packet_id`: **`wp523`** (ID bền theo §3.2) · `packet_slug`: **QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG**.
  **Bí danh lịch sử, đo được (21-09-2026):** chín biên nhận `ops/reviews/pr529-review-{1..9}-codex-verdict.receipt.yaml`
  (nhánh `claude/quy-trinh-lap-review-r2`) khai `packet_id: '523'` + `packet_slug: <slug>`; `packet_loop.py bien-nhan`
  so **bằng chuỗi** nên `--packet 523` ⇒ 9 · `--packet <slug>` ⇒ 9 · `--packet wp523` ⇒ **0, rc=11**. Biên nhận cũ
  **giữ nguyên byte** (`S5`); biên nhận mới phải khai `packet_id: wp523` **và** `packet_slug` để cả hai khoá cùng tra
  được. Lease gen 12 (#587) vẫn khai slug ở `packet_id` — ngoài tay executor, chủ kho neo lại cùng lúc với `spec_hash`.
  **Khoá tra ngân sách review — nói cho chật:** chừng nào `packet_loop.py bien-nhan` chưa biết bí danh (việc của
  `packet_loop.py` ⇒ `S4`, nợ **#583**), mọi phép đếm lượt/ngân sách của packet này **PHẢI** hỏi bằng `--packet 523`
  (hoặc slug) và đối chiếu = **9** tại lượt 9; hỏi bằng `wp523` mà nhận `0` là `KHÔNG ĐO ĐƯỢC` — **cấm** đọc thành
  "lịch sử bắt đầu từ 0" và cấm dùng làm bộ đếm. Phản chứng chỉ chạy được **sau** #583: hỏi cả ba khoá, khoá nào
  trả số khác nhau là ĐỎ. Đây là khai giới hạn, **không** phải đã đóng lớp.
- `packet_issue`: **523** · `mission_issue`: **499**
- `revision`: **12** · `generation`: **12** (lease hiện hành `quy-trinh-lap-review-r12-exec-12-claude-20260921`, #587;
  gen 11 cùng revision **đã hết hạn** `2026-09-21T05:00Z`) · soạn **20-09-2026**, sửa **21-09-2026**
- `thay_the_cho`: **revision 11** — nguồn **bất biến** (đo 21-09-2026, clone đầy đủ):
  commit `4a9c71a2e80b285679dd159e7a4efcb29a67a1a9` · path `ops/specs/QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG-r11.md`
  · blob `3bb25ae6169c5aeb4a1d600210c51f8794568815` · `sha256`
  `42b0f477b7db2b1cb954ee9a345c9fcc1a2fb805ec9c260461187180fdc4226b` · 474 dòng. Lấy từ checkout mới:
  `git fetch origin claude/spec-quy-trinh-r11-20260913 && git show 4a9c71a2e80b285679dd159e7a4efcb29a67a1a9:<path> | sha256sum`.
  **Thứ định danh là OID + băm, không phải tên nhánh**: r11 **không có trên `master`**; commit trên chỉ tra được chừng
  nào nhánh ấy (hoặc một tag `luu-tru/*`) còn giữ nó. **Trạng thái 21-09-2026: CHƯA có tag** ⇒ nguồn r11 là
  *đúng nhưng chưa bền*; `A2` phụ thuộc vào nó. Đường tạo tag có sẵn: `.github/workflows/ops-don-ref.yml`
  (`tao-tag`, `ref=luu-tru/spec-quy-trinh-r11`, `sha=4a9c71a2e80b285679dd159e7a4efcb29a67a1a9`, gõ `TAO`) — tag
  `luu-tru/**` **không thu hồi được** từ phiên web nên quyết định là của chủ kho; executor chỉ chạy thử khô.
  r11…r1 **giữ nguyên trên đĩa làm hồ sơ**.
- `executor`: **`claude`** · `reviewer_provider`: **`human` (chủ kho)** · `assurance_target`:
  **`human_audited`**
- `review_class`: **`sensitive`** — không đổi.
- `depends_on`: **`[]`** · `environment`: **`cloud`** · `risk`: **`sensitive`** — **chép nguyên từ r11** (dòng 42–43
  của blob `3bb25ae6…`), không đổi ⇒ không kích cò §3.2; ghi tường minh để executor mới không phải suy.

> **r12 LÀ MỘT REVIEW RESCUE CHECKPOINT (§12), KHÔNG phải một vòng vá nữa.**
> Chỉ thị chủ kho: PR #529 `issuecomment-5751125101` (`ducthangho`, OWNER, `2026-09-20T16:36:19Z`),
> đã đọc ngược qua API. Nguyên văn: *"Review Rescue Checkpoint theo §12 — đi đường (a), tách slice ổn."*

## `nguon_cap_viec`

Chỉ thị trên. §3.2 nói thẳng: *"Đổi objective, acceptance, write set, dependency, **executor** hoặc
environment tạo revision mới và làm lease cũ mất hiệu lực"*. r12 đổi **bốn** thứ trong danh sách ấy
(objective, acceptance, write set, executor), nên nó **phải** là revision mới + generation mới +
cấp lại lease (gen 11, rồi gia hạn thành gen 12 khi gen 11 hết hạn — cùng revision, cùng phạm vi). Lease gen 10 (`quy-trinh-lap-review-r11-exec-10-codex-20260913`) **mất hiệu lực**, và
nó cũng đã **hết hạn** `2026-09-14T12:00Z` từ trước.

## VÌ SAO CÓ r12 — một phép đếm, không phải một cảm giác

Chín lượt cross-review **đã đo** (`bien-nhan --packet 523` ⇒ 9 biên nhận phân biệt được) cho một thay đổi
**201 dòng, toàn tài liệu**. Verdict lượt 9: **`blocked`**, `0 P1 · 3 P2 · 1 P3 · 9 thể hiện`. Trần trục VÒNG và
số lượt còn lại **suy từ `ADR-0048` tại preflight** — ADR ấy là nhà duy nhất của con số, spec này **không chép**.

Phép đo quyết định — **không lớp mở nào là lỗi của nội dung skill**:

| lớp | chạm thật sự | trong write set r12? |
|---|---|---|
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | `LEASE:130` | **không** |
| `bien-nhan-thieu-so-ci-da-chi` | ledger + `receipt5` | **không** |
| `bien-nhan-luot-8-lan-du-lieu-luot-6` | `receipt8` | **không** |
| `phep-do-doctrine-khong-du-rang` | bộ quét `doctrine-scan` | **không** — `S4` cấm |

Ba lớp là **hồ sơ của chính packet**; lớp thứ tư là **nợ scanner có sẵn** (reviewer: *"lớp cũ còn
sống, không phải regression r10"*). Tức packet đang tiêu lượt review để sửa hồ sơ của các lượt
review trước, chứ không phải để sửa nội dung skill.

`CLAUDE.md`: *"cùng một hình dạng lặp ba lần trở lên thì câu hỏi đúng là **có nên làm việc này
không**, không phải **vá thế nào**"*. Ở đây hình dạng ấy lặp tới lượt thứ chín.

## `muc_tieu` — CHỈ nội dung skill

**M-SLICE:** đưa nội dung `M1`–`M10` của quy trình lặp review vào hai tệp skill, hợp nhất với bản
master hiện hành, **không mang theo hồ sơ review của packet**.

**Phạm vi `A2` là `M1`–`M10`, và chỉ thế.** `M11`/`M12` (r3) là nghĩa vụ về **hồ sơ review** (`ops/reviews/`,
`run_id` trong biên nhận) — nằm ngoài write set r12 theo chính mục `write_set` dưới đây; `M13`–`M16` (r4) và `M17-GO`
(r10) là nghĩa vụ **quy trình** của executor/reviewer (hoà giải, còn răng, con trỏ chứa thứ nó hứa, reviewer dựng
thước, không dựng lại cổng quét tên). Chúng **giữ hiệu lực** làm ràng buộc cách làm, nhưng **không được `A2` đo** —
khai ở `chua_do_duoc` 5. Quyết định *rút hẳn hay đưa vào acceptance* là đổi acceptance ⇒ §3.2 ⇒ **r13**, không vá
tại chỗ. r12 **không** đổi một mục tiêu nội dung nào; nó chỉ **thu hẹp phạm vi giao hàng**.

## `write_set` — ĐÚNG HAI đường

| # | đường dẫn | kiểu |
|---|---|---|
| 1 | `.claude/skills/cross-review/SKILL.md` | exact |
| 2 | `.claude/skills/work-packet/SKILL.md` | exact |

**BỎ** `ops/reviews/` (prefix) của r3–r11. Checkpoint nói rõ *"KHÔNG mang theo hồ sơ review của
packet"*.

**Hệ quả phải nói trước:** biên nhận `human_audited` của lượt này nằm ở `ops/reviews/`, tức **ngoài
write set r12**. Nó đi bằng một **PR bookkeeping riêng** — tiền lệ #567 cho #551. Đừng đọc việc ấy
thành "slice thiếu biên nhận".

**KHÔNG** đụng `docs/PROTOCOL_DA_PHIEN.md`, `.claude/hooks/**`, `packet_loop.py`, `CHANGELOG.md`,
`RELEASE_MANIFEST.json`, hay r1–r11 của chính đặc tả này.

Đo được (20-09-2026, `origin/master` `700ca8c`): `.claude/**` có **0/180** tệp trong
`RELEASE_MANIFEST.json` ⇒ slice **không** tái sinh manifest, **không** ghi lại golden.
`CHANGELOG.md` **có** trong manifest — đó là lý do nó bị loại khỏi write set.

## `assurance` — `human_audited`, và nói thẳng nó YẾU HƠN ở chỗ nào

`codex` **hết hạn token** (`access_token=-24.9h`, đo 20-09-2026) và `agy` không có CLI trong
container ⇒ `cross_approved` **không đạt được**. §8 cho class `sensitive` hai đường ngang hàng, nên
`human_audited` là đường còn lại — **không phải một lần hạ ngưỡng**.

**Nhưng nó yếu hơn r6–r11 theo một cách phải khai:** `M16` của r6 đặt *"reviewer dựng PHÉP ĐO"* làm
trụ, và chín lượt codex đã dựng thước thật. **Một lượt audit của người không dựng thước** — nó xác
nhận *"tôi đã đọc và chấp nhận"*. Chữ ký ấy **không thay được phép dò tìm**. Ai đọc `approve` của
r12 thành *"đã qua cùng mức soi như các lượt trước"* là đọc sai.

## `ngoai_pham_vi`

1. **KHÔNG vá bốn lớp mở trong slice này.** Chúng đã thành nợ có Issue: **#582** (ba lớp hồ sơ) ·
   **#583** (lớp scanner, cần packet riêng theo `S4`).
2. **KHÔNG hoàn nguyên phần master đã có.** master đã trôi **+212/−53** trên chính hai tệp ấy kể từ
   `merge-base 19de566`. Hợp nhất phải **giữ cả hai phía**; mất một mục của master là hỏng.
3. **KHÔNG tự định nghĩa `P1`/`P2`/`P3`** (kế thừa `ngoai_pham_vi` 9 của r11 — kho không có nguồn
   định nghĩa cả ba; khai nợ, đừng lấp chỗ trống).
4. **KHÔNG sửa biên nhận / `VERDICT.md` của các lượt đã giao** — chúng neo theo băm, `t26`/`t27` canh.
5. **KHÔNG dựng lại cổng quét tên.** `M17-GO` của r10 gỡ nó có căn cứ đo được: cả ba lần lớp chép
   doctrine bị bắt đều do reviewer **ĐỌC**, không lần nào do bộ quét, và bộ quét mù hai lần theo hai
   cách khác nhau.
6. **KHÔNG nới write set để "tiện tay"** — thêm đường thứ ba là `S1`, phải DỪNG và xin revision.

## `nghiem_thu`

| # | nghĩa vụ | đo thế nào |
|---|---|---|
| `A1` | Diff cuối chạm **đúng hai** tệp trong write set, không tệp nào khác | `git diff --name-only <base_sha> <head>`; **r12 không gán `base_sha`** — xem `chua_do_duoc` 6: chừng nào r13 chưa chốt baseline thì `A1` là `KHÔNG ĐO ĐƯỢC`, không phải ĐẠT |
| `A2` | Mọi mục `M1`–`M10` của r11 **có mặt** trong bản hợp nhất | đối chiếu chuỗi đặc trưng; kỷ luật đọc, **không** phải cổng |
| `A3` | **Không mục nào của master bị mất** trong hợp nhất | đối chiếu chuỗi đặc trưng của phía master |
| `A4` | Bảy cổng **`rc=0` kèm bằng chứng dương** trên exact head, **và** delta so nền master = 0 (điều kiện cần, không thay `rc=0`) | `rc` đọc TRỰC TIẾP từng tiến trình, **không qua pipe**; ca `KHÔNG ĐO ĐƯỢC` ⇒ `not_measured`; ca đỏ thật ở nền ⇒ DỪNG, không waiver ngầm |
| `A5` | `release-verify --strict` giữ `ok=true`, `expected == checked` | `180 == 180` ở nền 20-09 |
| `A6` | Chủ kho đọc **đúng diff hai tệp** trên exact `reviewed_sha` rồi ký | bản ghi bền (issue comment hoặc tệp biên nhận) mang **đủ**: `Reviewed commit: <40-hex>` đúng head, `spec_sha256` của r12, OID blob của **hai** tệp tại head ấy, và ít nhất một bằng chứng **tự đo** (lệnh + output). `author_association: OWNER` chỉ là điều kiện **cần** (nợ #566). Ca âm: comment OWNER ghi *"approve theo tóm tắt của executor"* ⇒ `S14`, không đếm. Hành vi ĐỌC của người là `KHÔNG ĐO ĐƯỢC` — không được viết thành "máy đã chứng minh" |

**Nền đã đo (21-09-2026) trên `origin/master` `714f36e6aad844f2c1a6713256f3abbdea64aec9`** — clone **đầy đủ**
`is-shallow=false`, `core.abbrev=7`, `actionlint 1.7.7` + `shellcheck 0.9.0` **đã cài**, `rc` đọc trực tiếp.
**Bảng này cố ý KHÔNG ghi SHA head**: tệp không thể chứa SHA của commit chứa nó, và bằng chứng theo cây
(tree) **không** chuyển được sang một commit khác cùng cây (`bien_nhan_v2` nhạy với tổ tiên). Bằng chứng của
**exact head** và của **merge ref** `refs/pull/<PR>/merge` (commit tổng hợp GitHub sinh lại mỗi lần, không bền)
nằm ở **comment handoff** trên PR, neo bằng OID 40 ký tự, đo **sau khi commit** và **trước khi gọi review**; hai
vế nền/head dựng trong MỘT lệnh.

| cổng | `rc` nền | bằng chứng dương (nền) |
|---|---|---|
| `doctrine-scan` | **0** | `sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `adr-song` | **0** | `50 ADR trên đĩa, 50 dòng trong §20, khớp 1–1` |
| `doc-claims-check --strict` | **0** | JSON `ok=true · schema doc_claims_check.v1 · strict=true · files_scanned 110 · flags 0 · advisory_count 381` (advisory ≠ flag) |
| `bien_nhan_v2` | **0** | `132 ĐẠT v2 · 11/11 · 42 NỢ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 185 · TỔNG: ĐẠT` — **chỉ đúng trên clone đầy đủ**; cùng cây trên clone `--depth 1` ⇒ `rc=2 · 264 KHÔNG ĐO ĐƯỢC · TỔNG: KHÔNG ĐO ĐƯỢC` (mỏ neo `canonical_ancestry` cần object) |
| `release-verify --strict --json` | **0** | `ok=true`, `expected_file_count 180 == checked_file_count 180`, `package_hash_match=true` |
| `git diff --check <base-40hex> <head-40hex> --` | — | **CÓ RANGE.** Bản không range chỉ soi worktree: kho rác commit một dòng có khoảng trắng đuôi, cây sạch ⇒ không range `rc=0`, có range `rc=2` — phép kiểm không thể đỏ không phải bằng chứng. `rc` không-range của các lượt trước **không** được dùng lại |
| `lease_publish_test` | **0** | `166/166 đạt; đã chạy=166, bỏ qua=0` với `actionlint 1.7.7` + `shellcheck 0.9.0` |

**`KHÔNG ĐO ĐƯỢC` ≠ ĐẠT, kể cả khi delta = 0.** Bản trước của bảng này nhận `lease_publish_test` `rc=1`
(`164/166`, hai ca `KHÔNG ĐO ĐƯỢC: thiếu shellcheck`) làm cổng qua vì *đỏ sẵn, delta = 0* — sai: một ca chưa tới
assertion thì **không đo gì**, và `164/166` thiếu công cụ ở lần đo này là `163/166` thiếu `actionlint` ở lần đo
sau — số trôi theo rig, không theo mã. Luật cho `A4`: cổng nào in `KHÔNG ĐO ĐƯỢC` thì ghi **`not_measured`** và
**cài công cụ rồi đo lại** (`AL_VER=1.7.7 bash ops/cai_actionlint.sh` · `bash ops/cai_cong_cu.sh shellcheck`);
không cài được thì DỪNG khai ĐẠT cho cổng ấy. **Và ĐỎ THẬT cũng không được nuốt vào delta:** `A4` đòi bảy cổng
`rc=0` với bằng chứng dương — một ca tới assertion mà fail ở **cả** nền lẫn head là **ĐỎ**, không phải *đỏ sẵn,
delta = 0*; executor DỪNG và báo chủ kho, và một waiver (nếu có) là hiện vật riêng có phạm vi và hạn, không phải
nhánh delta. "Delta = 0" chỉ còn nghĩa *head không làm nền xấu đi* — nó là điều kiện **cần**, không thay được
`rc=0`. (Ngưỡng ruff ở `CLAUDE.md` là chuyện khác: ruff **không** nằm trong bảy cổng.) Cài thêm công cụ có thể lộ
ca đỏ mới của nền: ca ấy là ĐỎ.

`bien_nhan_v2` phải đo theo **bất biến**, không theo số tuyệt đối: `vi phạm == 0` và
`KHÔNG ĐO ĐƯỢC == 0`; `miễn trừ legacy == 11/11`; `NỢ đóng băng` không tăng; `ĐẠT v2` **không giảm**
so nền đo lại **ngay trước** gate. Nền đã trôi `124 → 131 → 132` trong ba ngày — ghim số tuyệt đối
là tự báo động giả.

## `dieu_kien_dung` — DANH SÁCH ĐẦY ĐỦ, KHÔNG kế thừa qua con trỏ

Kế thừa nguyên tắc của r7: mục này **không** trỏ sang lease hay revision khác. Danh sách dưới đây là
bản có thẩm quyền DUY NHẤT, và lease **hiện hành** (gen 12; gen 11 trước đó) phải chép **đúng** nó.

- **`S1`** — cần đường dẫn thứ BA ngoài hai tệp skill. DỪNG, xin revision.
- **`S2`** — tổng dòng thêm của **HAI tệp sản phẩm**, đo từ `base_sha` tới head cuối, **> 300**
  (trần ADR-0044 cho `sensitive`). **KHÔNG cộng hai khoảng.** r12 chưa gán `base_sha` (`chua_do_duoc` 6) ⇒
  `S2` **chưa kích hoạt được**; đó là một `KHÔNG ĐO ĐƯỢC` phải khai, không phải "chưa chạm".
- **`S3`** — muốn đụng `docs/PROTOCOL_DA_PHIEN.md` hay `.claude/hooks/**`.
- **`S4`** — muốn vá `packet_loop.py` / `doctrine-scan`: KHÔNG trong write set; nợ riêng **#583**.
- **`S5`** — muốn sửa `VERDICT.md` hoặc biên nhận của một lượt đã giao (neo theo băm).
- **`S6`** — muốn đổi định nghĩa `P1`/`P2`/`P3` hay đổi slug của một lớp cũ (slug là **khoá đếm**).
- **`S7`** — hợp nhất ba chiều làm **mất** một mục của master hoặc của #529 mà không có chỗ đặt lại.
  DỪNG và báo chủ kho; KHÔNG bỏ bớt cho hết xung đột.
- **`S8` ĐÃ RÚT từ r7** — số để trống có chủ đích, KHÔNG đánh số lại.
- **`S12'`** — chuẩn bị đóng băng mà phép quét *"còn sót luật cũ"* chỉ khớp theo **TÊN**, hoặc hạ một
  luật xuống thành *"báo cáo để người đọc tự phán"*. Đó là phép dò chính tả, không phải phép đo.
- **`S13` (mới ở r12)** — muốn vá **bất kỳ lớp nào trong bốn lớp mở** để lấy `approve`. Đó là **LÁCH
  checkpoint**: chúng đã được chuyển thành nợ có Issue, và vá lẻ ở đây làm slice phình đúng thứ
  checkpoint sinh ra để cắt. DỪNG.
- **`S14` (mới ở r12)** — chủ kho **không** đọc được trọn diff hai tệp trước khi ký, hoặc muốn ký
  dựa trên tóm tắt của executor. `human_audited` §8 đòi người audit **tự đọc spec/diff**; một chữ ký
  trên bản tóm tắt là `KHÔNG ĐO ĐƯỢC`, không phải `approve`.

## `chua_do_duoc` — khai thẳng

1. **Union `findings_ids` của cả chín lượt ĐÃ ĐO (21-09-2026)**, không chỉ lượt 9. Lệnh: đọc
   `findings_ids` + `doi_chieu_luot_truoc[].phan` + `lop_da_dong_that_o_luot_nay` từ chín biên nhận trên nhánh
   `claude/quy-trinh-lap-review-r2` (PyYAML, so slug bằng chuỗi). Kết quả: **17 slug**; **4 mở** ở lượt 9
   (`dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` VÁ HỜ · `bien-nhan-thieu-so-ci-da-chi` VÁ HỜ ·
   `phep-do-doctrine-khong-du-rang` CHƯA VÁ · `bien-nhan-luot-8-lan-du-lieu-luot-6` mới); **6** có
   `ĐÃ VÁ THẬT` ngay trong **biên nhận** lượt sau (`sai-dai-luong-hoi-tu` `gop-dieu-kien-dung-review-class`
   `thieu-hop-dong-ban-va-theo-lop` `mat-dau-vet-thu-hep-pham-vi` `bien-goi-y-thanh-menh-lenh`
   `chu-giai-lease-neo-head-cu`); **7** của lượt 3–4 (`bo-doc-bang-vuot-ranh-gioi-muc`
   `bo-do-bang-chi-kiem-ten-khong-kiem-nghia` `a9-bo-sot-delta-trong-merge` `a17-whitelist-bo-roi-m8`
   `con-tro-dinh-nghia-phan-hang-sai-dich` `dem-dot-bien-khong-theo-tieu-chi-dich`
   `doi-chung-a19-khong-chi-phoi-ket-luan`) chỉ có `ĐÃ VÁ THẬT` trong **`VERDICT.md`** lượt 4–5, **không có
   dòng đối chiếu nào trong biên nhận** (biên nhận lượt 5 không có mục `doi_chieu_luot_truoc`). Tức 17/17 có
   disposition nếu đọc VERDICT, nhưng **bộ đếm máy (`bien-nhan`) mù với 7 lớp ấy** — đó là lỗ thật. Không lớp nào
   trong 13 lớp đóng là *"bỏ im lặng"*, nhưng kết luận này dựa trên **đọc**, chưa có ledger đóng băng: ledger ấy
   là tệp trong `ops/reviews/` ⇒ ngoài write set r12 ⇒ **r13**. Đột biến cần có ở đó: xoá một slug chưa đóng khỏi
   biên nhận lượt 9 phải làm checkpoint ĐỎ.
2. **Hợp nhất ba chiều có thể làm mất nội dung theo cách cổng không thấy.** `doctrine-scan` và
   `doc-claims-check` không đo *"đủ mục hay chưa"*. `A2`/`A3` là **kỷ luật đọc**, không phải cổng —
   nói ra để không ai đọc chúng thành đã có máy canh.
3. **Slice land KÈM `phep-do-doctrine-khong-du-rang` còn mở.** Scanner vẫn mù hai dạng chép sau khi
   land. Đánh đổi **có chủ đích và được khai**.
4. **Không cổng nào cưỡng chế `M1`–`M10`** — chúng là chữ, tức kỷ luật đọc. Chính skill phải khai
   điều này (`ngoai_pham_vi` 2 của r3 đòi vậy).
5. **`M11`–`M16` và `M17-GO` không được `A2` đo.** Một ứng viên bỏ `M16` khỏi hai tệp skill vẫn qua `A2`.
   Đưa chúng vào acceptance hay rút hẳn là đổi acceptance ⇒ **r13**; r12 chỉ khai lỗ.
6. **r12 KHÔNG gán `base_sha`** cho `A1`/`S2`, và ba nguồn hiện khai ba OID khác nhau: lease gen 11
   `395bc7b1be6c275d8de697f8d8541bb36a290c9e` · lease gen 12 `a1bbdc1023185a35c578ab4017990b472b5c0d6c` ·
   r13 nháp `S16` giữ `395bc7b1…`. Đo trên head slice #585 `27283d2e6ed57a6e97bf45e3179c157a59f0ff86`
   (`merge-base` với `master` = `a1bbdc10…`): từ `395bc7b1` ⇒ **3 tệp** (thêm
   `ops/specs/dang-lease-dau-truoc-kiem-sau-r1.md`, do master trôi) · từ `a1bbdc10` ⇒ **2 tệp** · cả hai đều
   +201 dòng ở hai tệp sản phẩm. Chọn baseline là quyết định **thẩm quyền** (`PROTOCOL` §3.2.1 cấm dời baseline
   bằng gia hạn lease) ⇒ **r13**, không lấp tại chỗ. Tới lúc đó `A1`/`S2` là `KHÔNG ĐO ĐƯỢC`; đột biến +301 dòng
   phải làm `S2` đỏ **sau khi** baseline được gán.
