---
kieu: dac_ta_packet
packet: WP461-BE-MAT-THU-HAI-CUA-CODEX
packet_id: wp461
ban: r3
trang_thai: nhap              # NHÁP — chưa đóng băng. Chủ kho đo sha256 từ blob, đăng lên #461, rồi mới có lease.
packet_issue: 461
mission_issue: 470
ho_so_lap_luan: https://github.com/ducthangho/tra-luat/issues/461
neo_uy_quyen: https://github.com/ducthangho/tra-luat/issues/470
thay_the_ban: r2               # r2 spec_hash db4980e3c5e12b3f9ffaac63e20d7f5d2316551f0b04a05449d2a87e85969b03 (9 789 B, 144 dòng), giữ nguyên trên đĩa làm hồ sơ
ly_do_revision: >-
  (1) WP610 (#610, PR #612, merge ce25a427b87aca9a6352ce4679bb4e7dc56c8235, 2026-09-24T05:14Z) đã sửa
  CÙNG BA TỆP của write set: thêm hàng codex_desktop vào _PROVIDER_NGOAI_CLI, viết lại chú thích
  "không bao giờ chứa", bỏ ngoại lệ Codex trong c44 tầng (b) (nay đòi ĐÚNG MỘT token/hàng §2),
  tách §2 thành "Codex CLI"/"Codex Desktop" và ghi chú nợ #461. Ba mục của r2 vì thế lỗi thời:
  §1 (phép đo nền), §3bis đoạn "vật cản còn lại là một câu chú thích", §5 mục 2 (c44).
  (2) wp523 r15 (bookkeeping issues/523#issuecomment-5815274276) mở nợ có tên
  receipt-r15-connector-surface-khong-co-hop-dong: lượt review codex qua GitHub App
  chatgpt-codex-connector[bot] KHÔNG có bề mặt hợp lệ để khai — đúng lớp của packet này, đo lại
  ngày 24-09 (mục 1). r3 trả nợ ấy ở tầng hợp đồng dữ liệu; receipt r15 tự nó là việc của một
  lease wp523 sau khi r3 land (mục 8).
sinh_ra_tu: >-
  r2 (#470, bốn quyết định Q1–Q4 đã chốt, GIỮ NGUYÊN) + bookkeeping đóng M-ĐÓNG wp523 r15
  (issues/523#issuecomment-5815274276) + spec r15 S18 (blob 9f4625dd152cb47be8d8cee69650fd47be8e704c,
  sha256 f333152f5f44cdb65a354d4eb9fc44fe69a718a5d9b61e47926309105da93f53).
ghi_chu_hinh_dang: >-
  Chưa cổng nào đọc tệp này. Nó là DỮ LIỆU cho lease và cho reviewer, không phải giao diện.
---

# `wp461` — bề mặt thứ hai của Codex chưa có tên trong hợp đồng dữ liệu (bản **r3**)

> **BẢN NHÁP — CHƯA ĐÓNG BĂNG.** Soạn bởi phiên executor Claude Code theo chỉ thị chủ kho
> (`2026-09-24T13:5xZ`: *"Soạn spec packet trả nợ receipt-r15-connector-surface"*) và bốn câu trả lời
> biên giới của chủ kho trong cùng phiên (mục 2). Tệp này **không** cấp quyền gì cho tới khi chủ kho đo
> `sha256` từ blob, đăng băm lên #461 và cấp lease **generation 3** (§3.2, §4 `docs/PROTOCOL_DA_PHIEN.md`).

- `packet_id`: **`wp461`** · `packet_issue`: **461** · `mission_issue`: **470**
- `revision`: **3** · `generation`: **3** *(dự kiến; gen 1 = r1/r2 `2026-09-07T05:27Z`, gen 2 = `2026-09-07T09:52Z`
  hết hạn `2026-09-08T09:52Z`, cả hai **không có mã land** — đo: `origin/master 515d16a` chưa có hàng `codex_service`,
  không còn ref `agent/wp461*`)*
- `executor`: **`claude`** · `environment`: **`cloud`** · `reviewer_provider`: **`openai_codex`** ·
  `assurance_target`: **`cross_approved`** (như r2) · `risk`: **`sensitive`** · `review_class`: **`sensitive`**
- `depends_on`: **`[wp610]`** — **ĐÃ THỎA** (`ce25a427…`, #612 merged `2026-09-24T05:14:02Z`). Không phụ thuộc wp523.
- `continuation_base`: **`515d16a1776dd6bb030790e207c98e3beefaabba`** (`origin/master` lúc soạn, `2026-09-24T13:52Z`,
  sau khi #613 và #614 land). Chủ kho đo lại lúc đóng băng; con số này chỉ để đối chiếu (L5).

## 1. Phép đo nền — đo lại **24-09-2026 ~14:00Z** trên `515d16a` (mọi dòng chạy lại được)

| đo cái gì | lệnh | kết quả |
|---|---|---|
| hợp đồng `openai_codex` hiện có mấy bề mặt | `PROVIDER_HOP_DONG["openai_codex"]["be_mat"]` (qua `ops/bien_nhan_v2.py`) | **`['codex_cli', 'codex_desktop']`** — hai (r2 đo: một) |
| `_PROVIDER_NGOAI_CLI` | `.claude/dev/launcher.py` | 4 hàng: `google_antigravity/antigravity`, `openai_chatgpt/chatgpt_web`, `openai_codex/codex_desktop`, `human/manual_audit` — **chưa có `codex_service`** |
| §2 `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` | đọc bảng | 6 hàng, mỗi hàng **một** token surface; đoạn văn dưới bảng: *"Tên lịch sử 'Codex service' chưa có tên máy trong hợp đồng dữ liệu; nợ này để riêng tại #461"* |
| `c44` tầng (b) | `ops/bien_nhan_v2_test.py` | **không còn** nhánh `bang(prov == "openai_codex", …)`; đòi `o[-2] == f"\`{be_mat_s2}\`"` — tức đúng một token/hàng ⇒ tiêu chí 2 của r2 **đã được WP610 thoả**, không còn là việc của wp461 |
| oracle `BO_BA_PROVIDER_DONG_BANG` | `ops/bien_nhan_v2_test.py` | 6 bộ ba, có `("openai_codex","codex_desktop","machine")`, **chưa có `codex_service`** |
| lượt review codex **thật** qua GitHub App | PR #613, comment `5812074543` + review `5304344210`, actor `chatgpt-codex-connector[bot]` | không CLI, không Desktop, không `session_run_id`, không model/effort xuất ra |
| receipt thử khai TRUNG THỰC bề mặt ấy (`surface: codex_github_connector`, rig tạm, không commit) | `python ops/bien_nhan_v2.py --root .` | **rc=1 · 1 vi phạm**, lỗi duy nhất: *"không phải bề mặt của provider `openai_codex` — hợp đồng của kho cho ['codex_cli', 'codex_desktop']"* |
| cùng receipt, khai SAI `surface: codex_desktop` | như trên | **0 vi phạm** — tức bộ kiểm NHẬN lời khai sai, TỪ CHỐI lời khai thật (cùng chiều đảo với `R8-05`) |
| `bien_nhan_v2 --root .` toàn kho | | rc=0 · **133 ĐẠT v2 · 11/11 miễn trừ · 42 NỢ · 0 vi phạm · 0 KĐĐ · tổng 186** |
| `lease_publish_test` | actionlint 1.7.7 + shellcheck 0.9.0 | **167/167** |
| `_TRANSPORT_CONTRACTS` | `.claude/dev/launcher.py` | 3 hàng (`anthropic_claude`, `openai_codex/codex_cli`, `openai_api`), **không đổi** so r2 |

**Hệ quả một câu (không đổi so r2, nay có ca thật):** một reviewer chạy trên bề mặt thứ ba của Codex
(dịch vụ, qua GitHub App) **không có giá trị hợp lệ nào để khai trung thực**; muốn qua cổng chỉ có
cách khai sai. Spec r15 `S18` đã chặn đúng: *blocked, không alias, không sửa receipt*.

## 2. Bốn quyết định của #470 — GIỮ NGUYÊN, và bốn câu biên giới của r3 (chủ kho trả lời `2026-09-24T14:0xZ`)

| | quyết định | r3 |
|---|---|---|
| **Q1** | tên máy bề mặt thứ hai = **`codex_service`** | **giữ**. r3 **định nghĩa**: `codex_service` = mọi đường chạy Codex **không** qua lệnh `codex` (CLI) và **không** qua Codex Desktop — gồm GitHub App `chatgpt-codex-connector[bot]` (review trên PR) và Codex cloud/service nói chung. Không mọc tên `codex_github_connector`. |
| **Q2** | 12 receipt lịch sử `codex_cli` **ĐÚNG**, không sửa, không caveat | **giữ**; nay là **14** receipt `codex_cli` + 1 `codex_desktop` (đếm lại lúc thi công, ghi số vào PR) — tiêu chí "0 vi phạm" vẫn phải thoả tự nhiên |
| **Q3** | cột surface **vô hướng**, không đổi arity | **giữ** |
| **Q4** | §2 giữ prose, chỉ thêm hàng đối chiếu được | **giữ**; hàng mới: `| Codex service (GitHub App / cloud) | \`openai_codex\` | \`codex_service\` | machine |`, đoạn văn "Tên lịch sử 'Codex service'…" sửa thành đã có tên máy |
| **B1** (r3) | hình thức | **wp461 r3**, không mở packet mới chồng write set |
| **B2** (r3) | bề mặt GitHub App | **`codex_service`** (Q1), không tên riêng |
| **B3** (r3) | receipt r15 (`ops/reviews/wp523-r15-review-1-codex-verdict.{md,receipt.yaml}` + hàng README) | **ngoài write set r3**; ghi bằng lease wp523 riêng SAU khi r3 land (mục 8) |
| **B4** (r3) | vai | executor `claude`, reviewer `openai_codex`, `cross_approved`, trần **2 lượt codex/PR** (§12) |

## 3. Hình dạng bản vá — chép từ r2 §3bis, cập nhật sau WP610

Hàng mới đi vào **`_PROVIDER_NGOAI_CLI`** (không vào `_TRANSPORT_CONTRACTS` — `_dinh_danh_van_chuyen` ném
`RuntimeError: provider co nhieu transport` khi một provider có hai contract, đo ở r2 và vẫn đúng: WP610
cũng đặt `codex_desktop` ở bảng ngoài CLI):

```python
    # wp461 r3: Codex chạy như DỊCH VỤ — GitHub App chatgpt-codex-connector[bot] (review trên PR) và
    # Codex cloud nói chung. Không CLI, không Desktop; không chứng minh model/effort/độc lập phiên.
    ("openai_codex", "codex_service", "machine"),
```

Căn cứ: `ops/bien_nhan_v2.py` gộp hai bảng thành TẬP (`setdefault` + `.add`) — đo được ở r2 và **đã có tiền
lệ chạy thật**: `codex_desktop` (WP610) sống chung với `codex_cli` trên `515d16a`, `133 ĐẠT · 0 vi phạm`.

Câu chú thích *"không bao giờ chứa provider đi qua CLI"* mà r2 coi là vật cản **đã được WP610 viết lại**
(*"Một provider có thể có cả hàng CLI và ngoài CLI với hai bề mặt khác nhau (Codex)"*) — r3 **không** sửa lại
đoạn ấy, chỉ thêm hàng + chú thích riêng của hàng.

**Executor KHÔNG được đổi hình dạng này.** Đổi ⇒ verdict `blocked` + revision mới.

## 4. Write set — 4 đường, KHÔNG đổi so r2 (mỗi đường một mục tiêu, L2)

```
.claude/dev/launcher.py                      # M1: một hàng trong _PROVIDER_NGOAI_CLI + chú thích của hàng
ops/KE_HOACH_THI_CONG_DA_PROVIDER.md         # M2: §2 thêm một hàng "Codex service"; sửa đoạn nợ #461 thành đã có tên máy
ops/bien_nhan_v2_test.py                     # M3: BO_BA_PROVIDER_DONG_BANG + 2 ca mới + đột biến rút hàng
CHANGELOG.md                                 # M4: một mục r-mới, ghi số đo hai vế
```

**Cố ý KHÔNG có:** `ops/bien_nhan_v2.py` (không cần, đã chứng minh bằng `codex_desktop`), `ops/lease_publish.py`
(nợ `PLAT-DISPATCHER-TRUONG-PHAI-SINH`, #470 mục 1), `AGENTS.md` (khối máy đọc được ở đó chỉ khai `openai_chatgpt`;
`c28`/`_provider_chinh_tac` đối chiếu khối ấy với bảng — thêm hàng Codex **không** làm nó lệch, đo trước khi push),
`ops/reviews/**` (mục 8), 14 receipt lịch sử.

Kích thước dự kiến: **4 tệp, ≤ +120 dòng** (tham chiếu WP610: 3 tệp, +90/−22). Ngưỡng ADR-0044 cho `sensitive`
chạm authority là 3 tệp/300 dòng — r2 đã khai 4 tệp với lý do CHANGELOG là bookkeeping bắt buộc (ADR-0034); r3 giữ
lý do ấy, và **nếu `numstat` vượt 300 dòng thêm thì DỪNG trước review** (S6).

## 5. Mục tiêu

1. **M1** — `.claude/dev/launcher.py`: `_PROVIDER_NGOAI_CLI` có đúng **một** hàng `("openai_codex", "codex_service", "machine")`;
   `_TRANSPORT_CONTRACTS` **không đổi một byte**.
2. **M2** — `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` §2: thêm hàng `Codex service (GitHub App / cloud)` với ô surface
   **đúng một token** `` `codex_service` ``, transport `machine`; đoạn *"Tên lịch sử 'Codex service' chưa có tên máy…"*
   sửa thành: đã có tên máy từ wp461 r3, 14 receipt lịch sử `codex_cli` giữ nguyên (Q2), #461 đóng khi r3 land.
3. **M3** — `ops/bien_nhan_v2_test.py`: (a) `BO_BA_PROVIDER_DONG_BANG` thêm bộ ba `codex_service`; (b) hai ca mới đánh số
   tiếp sau ca cuối hiện có (`c66` tại `515d16a`), theo mẫu `c64`/`c65` của WP610: ca dương (receipt `advisory_review`
   khai `codex_service`/`machine` ⇒ `_thieu` rỗng) và ca âm (khai `codex_api`, `codex_github_connector`, `Codex service`
   ⇒ đúng **một** lỗi, đúng **cột surface**; `codex_service` **không** vào `_TRANSPORT_CONTRACTS`; `human_audited` +
   `codex_service` bị chặn bởi phân vùng người/mô hình); (c) **đột biến rút hàng `codex_service` khỏi `launcher.py`
   phải làm ca dương ĐỎ**, đọc nguyên văn thông báo giết.
4. **M4** — `CHANGELOG.md`: một mục theo mẫu r375 (phạm vi nguồn a/b/c), ghi: hàng mới, số receipt lịch sử đếm được,
   `bien_nhan_v2` hai vế, `launcher_test` hai vế, nợ nào đóng (#461) và nợ nào **không** (receipt r15 — mục 8).

## 6. Nghiệm thu — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | ĐỎ khi |
|---|---|---|
| A1 | receipt thật khai `surface: codex_service`, `transport: machine`, `assurance: advisory_review` ⇒ `bnv2._thieu(d) == []` | danh sách lỗi ≠ rỗng |
| A2 | khai `codex_api` · `codex_github_connector` · `Codex service` ⇒ **đúng 1** lỗi, thông báo chứa *"không phải bề mặt của provider `openai_codex`"* | 0 lỗi (nới quá), hoặc lỗi ở cột khác |
| A3 | `PROVIDER_HOP_DONG["openai_codex"]["be_mat"] == {'codex_cli','codex_desktop','codex_service'}` | thiếu/thừa phần tử |
| A4 | `_TRANSPORT_CONTRACTS`: `git diff <base> <head> -- .claude/dev/launcher.py` **không** có dòng `+/-` trong khối ấy (so KHỐI, không grep tên) | có dòng đổi trong khối |
| A5 | `c44` (a)+(b) xanh với hàng mới: launcher ↔ oracle ↔ §2 khớp cả ba cột, §2 tìm được **đúng 1** hàng cho `(openai_codex, codex_service)` | c44 đỏ |
| A6 | đột biến "xoá hàng `codex_service`" trên bản sao tạm ⇒ ca dương ĐỎ với thông báo nêu `codex_service` | ca dương vẫn xanh |
| A7 | `python ops/bien_nhan_v2.py --root .` head: rc=0 · ĐẠT ≥ 133 · **0 vi phạm · 0 KĐĐ**; **0 miễn trừ mới**; 14 receipt `codex_cli` không đổi byte (Q2) | rc≠0, vi phạm>0, miễn trừ mới, hoặc receipt lịch sử đổi |
| A8 | `python ops/lease_publish_test.py` head = nền (**167/167** lúc soạn) | thêm ca đỏ so nền |
| A9 | `python .claude/dev/launcher_test.py` **hai vế cùng lệnh** (nền/head): delta = 0 (nền `155` ca lúc soạn, đếm `^def t`; số đạt ghi lúc đo) | delta ≠ 0 |
| A10 | `doctrine-scan`, `adr-song`, `doc-claims-check --strict` (`ok=true`), `release-verify --strict --json` (`ok=true`, 180==180), `git diff --check <base40> <head40> --` — rc đọc trực tiếp | bất kỳ rc≠0 |
| A11 | ADR-0044: `git diff --numstat <base> <head>` ≤ 4 tệp, ≤ 300 dòng thêm | vượt |
| A12 | review: codex ≤ **2** lượt/PR, verdict `approve` với `Reviewed commit:` = exact head 40-hex; receipt v2 `role: reviewer`, `packet_id: wp461` | lượt 3 không có `nang_tran`; verdict neo commit tổng hợp không có trên server ⇒ KĐĐ, không phải ĐẠT |

## 7. Hình dạng kế thừa (L4) — chép từ hồ sơ r1/r2, đo `24-09`

| nguồn | lượt | kết quả | lớp lặp |
|---|---|---|---|
| PR #469 (r1 lease) | cross-review 1 | `blocked`, 4 P1 + 2 P2 + 2 P3 | `uy-quyen-khong-co-neo-ben` ①, `spec-chua-chot-hop-dong` |
| PR #471 (r2 spec+lease) | cross-review 2 (`5565839022`) | `blocked`, 2 P1 + 2 P2 + 1 P3 | `uy-quyen-khong-co-neo-ben` **②**, `lease-thieu-truong-dieu-phoi` (miễn trừ có phạm vi, #470 mục 1) |
| nhánh `ops/lease-wp461-g2` | cross-review 3, 4 (commit `3c4c587`, `ddb3200`) | vá "merge không tự làm hết hai người giữ", "có BA ref" | `bo-loc-va-cham-thieu-ref` **②** |
| PR #471 | connector `@codex review` `5568509940` | treo `Running` vì merge 68 giây sau khi bắt đầu | bài học CLAUDE.md "gate xanh ≠ đã review" |

Bộ đếm mang sang r3: `uy-quyen-khong-co-neo-ben` = **2**, `bo-loc-va-cham-thieu-ref` = **2**. Lặp lần 3 ⇒ dừng, hỏi chủ kho
(§12). Cách tránh đã biết: lease r3 neo `mission_issue: 470` + comment chủ kho có URL; quét va chạm theo **ref**, không
chỉ theo lease (mục 9).

## 8. Điều kiện đóng nợ `receipt-r15-connector-surface-khong-co-hop-dong` (NGOÀI write set r3)

Sau khi r3 land (hàng `codex_service` ở master): một lease **wp523** riêng (generation mới, cùng spec r15 đã đóng băng
hoặc revision kế) ghi `ops/reviews/wp523-r15-review-1-codex-verdict.md` + `.receipt.yaml` (v2, `role: reviewer`,
`packet_id: wp523`, `packet_slug`, `reviewed_sha: 92adc7112155a6711ec2c86d59ce60293b342314`, `verdict: approve`,
0 P0–P3, `model_reviewer_identity.surface: codex_service`, `transport: machine`, `KHONG_do_duoc` khai không có
`session_run_id`/model) + hàng README, rồi đo `bien_nhan_v2` ⇒ ĐẠT +1 và `bien-nhan --packet wp523` ≥ 1. r3 **không**
làm việc đó và **không** khai nợ ấy đã đóng.

## 9. Va chạm & điều kiện dừng

**Ref đang chạm write set (đo `24-09 ~14:00Z`, PR mở):** #509 `codex/wp484-g6-integration`, #447 `codex/wp433-r13-runtime-closure`,
#435, #394 (`launcher.py`); #485 (`launcher.py` + `CHANGELOG.md`); #459 (`CHANGELOG.md`). Không PR nào sửa
`_PROVIDER_NGOAI_CLI`/§2 (kiểm lại bằng `git diff origin/master...<ref> -- .claude/dev/launcher.py` trước khi push).
`ai-dang-giu` cho 4 đường phải rc=0 lúc bắt đầu.

- **S1** — cần đường ngoài 4 đường ⇒ DỪNG, revision.
- **S2** — phải sửa `ops/bien_nhan_v2.py` để A1–A3 xanh ⇒ spec **thiếu** ⇒ DỪNG, revision (r2 §4).
- **S3** — bất kỳ receipt lịch sử nào cần sửa/miễn trừ mới để A7 xanh ⇒ bản vá SAI, DỪNG (Q2).
- **S4** — c44 đòi đổi §2 sang khối máy đọc được ⇒ DỪNG (Q4).
- **S5** — `_TRANSPORT_CONTRACTS` phải đổi ⇒ DỪNG (hình dạng 3).
- **S6** — `numstat` > 4 tệp hoặc > 300 dòng thêm ⇒ DỪNG trước review (ADR-0044).
- **S7** — lớp `uy-quyen-khong-co-neo-ben` hoặc `bo-loc-va-cham-thieu-ref` lặp lần **3** ⇒ DỪNG, hỏi chủ kho.
- **S8** — trần 2 lượt codex/PR chạm ⇒ Review Rescue Checkpoint (§12), không gọi lách.
- **S9** — lease hết hạn ⇒ handoff §7, không tự gia hạn.

## 10. Chưa đo được từ phiên soạn

- Bề mặt **thật** của `chatgpt-codex-connector[bot]` (cloud nào, model nào): không có telemetry; `codex_service` là
  **tên hợp đồng**, không phải bằng chứng model/effort — receipt phải khai `KHONG_do_duoc`.
- `launcher_test` 155 ca **chưa chạy** trong phiên soạn (cần mạng + venv theo r2 §5.6); số nền đo lúc thi công.
- Lease g2 branch `ops/lease-wp461-g2` (`ddb3200`) chưa merge: r3 KHÔNG tái dùng; chủ kho quyết đóng hay giữ làm hồ sơ.
- Danh tính người ký các comment `ducthangho` (#566) — như mọi packet, không đo được từ trong tài khoản.
