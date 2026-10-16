---
kieu: dac_ta_packet
packet: WP461-BE-MAT-THU-HAI-CUA-CODEX
packet_id: wp461
ban: r4
trang_thai: nhap              # NHÁP — chưa đóng băng. Chủ kho đo sha256 từ blob, đăng lên #461, rồi mới có lease từ r4.
packet_issue: 461
mission_issue: 470
ho_so_lap_luan: https://github.com/ducthangho/tra-luat/issues/461
neo_uy_quyen: https://github.com/ducthangho/tra-luat/issues/470
thay_the_ban: r3               # r3 spec_hash 7a44e0e0cb7651b980144244e828821d93af0200f7d6083b112ad3b022b2f715 (18 634 B), ĐÃ LAND (#615/#616, master 541fa6ca); giữ nguyên trên đĩa
ly_do_revision: >-
  (1) Mã sản phẩm của r3 ĐÃ LAND (#617, merge 6980e5bf, 2026-09-24T17:54:50Z). Việc còn lại của packet là
  HỒ SƠ: biên nhận lượt review 1 (GitHub App, surface codex_service) + hàng mục lục README — nhưng r3 §4
  KHÔNG có ops/reviews/** (khuyết tật A12 đã khai ở #461). Lease g4/g5 mở rộng write set bằng chỉ thị chủ kho
  (issues/461#issuecomment-5820263820, -5820541861), tức có uỷ quyền nhưng KHÔNG có hợp đồng packet nào
  băm-phủ ba đường ấy. Cross-review #624 (App, thread 4099812192, P1) nêu đúng: sửa ở TRẠNG THÁI PACKET, không
  ở trường giải thích của lease. r4 là revision bookkeeping ấy.
  (2) r4 KHÔNG đổi mục tiêu sản phẩm, KHÔNG đụng ba tệp của r3 §4, KHÔNG reset attempts/lượt review.
sinh_ra_tu: >-
  r3 (đóng băng 5817701016, land) + chỉ thị chủ kho 5820263820 (lease g4) + uỷ quyền 5820541861 (g5+, vòng
  lặp vá/cross-review) + cross-review #623/#624/#625 (review 5311622663, 5311818779 và các lượt trước).
ghi_chu_hinh_dang: >-
  Chưa cổng nào đọc tệp này. Nó là DỮ LIỆU cho lease và cho reviewer, không phải giao diện.
---

# `wp461` — bề mặt thứ hai của Codex: **hồ sơ biên nhận** (bản **r4**, bookkeeping)

> **BẢN NHÁP — CHƯA ĐÓNG BĂNG.** Soạn bởi phiên executor Claude Code sau finding P1 `4099812192` (cross-review
> #624) theo chỉ thị chủ kho `2026-09-25T00:2xZ` *"tiếp tục lặp vá, cross-review theo phân lớp…"*. Tệp này
> **không** cấp quyền gì cho tới khi chủ kho đo `sha256` từ blob, đăng băm lên #461 và cấp lease **generation 6**
> từ r4 (§3.2, §4 `docs/PROTOCOL_DA_PHIEN.md`). Lease g5 (từ r3, hết hạn `2026-09-25T01:27:45Z`) hết hạn tự nhiên.

- `packet_id`: **`wp461`** · `packet_issue`: **461** · `mission_issue`: **470**
- `revision`: **4** · `generation`: **6** *(dự kiến; g3 = run sản phẩm, land 6980e5bf; g4/g5 = bookkeeping dưới r3 + chỉ thị)*
- `executor`: **`claude`** (model khai đúng thực tế trong lease) · `environment`: **`cloud`** · `reviewer_provider`: **`openai_codex`**
  (yêu cầu gpt-6-astra, effort ≥ medium; qua GitHub App ⇒ model/effort/session `KHONG_DO_DUOC`) ·
  `assurance_target`: **`advisory_review`** cho biên nhận (connector không nâng được `cross_approved`) ·
  `risk`: **`sensitive`** · `review_class`: **`sensitive`**
- `depends_on`: **`[]`** — sản phẩm r3 đã land; không phụ thuộc wp523 (hai packet có hàng README riêng, KHÔNG được có lease sống giao nhau).
- `continuation_base`: **`601a0f18…`** (`origin/master` lúc soạn, `2026-09-25T00:3xZ`, sau khi #620 land). Chủ kho đo lại lúc đóng băng.

## 1. Phép đo nền — đo **25-09-2026 ~00:30Z** (mọi dòng chạy lại được)

| đo cái gì | lệnh | kết quả |
|---|---|---|
| hợp đồng `openai_codex` | `PROVIDER_HOP_DONG["openai_codex"]["be_mat"]` qua `ops/bien_nhan_v2.py` trên master | `['codex_cli', 'codex_desktop', 'codex_service']` (r3 đã land) |
| biên nhận wp461 hiện có trên master | `ls ops/reviews/wp461-*` | **không có** — `bien-nhan --packet wp461` ⇒ 0, rc=11 |
| ứng viên biên nhận | PR #625, nhánh `claude/wp461-g4-receipt`, head `020de5e0148808486e0530f6810e4286816969a6` | verdict = NGUYÊN BYTE comment `pull/617#issuecomment-5819108011` (609 B, sha256 `2276547ec77b74618c5e548ce3efeb3661fd90e59e847d187a3691f4c632cb8d`), receipt v2 `surface: codex_service`, hàng README |
| `bien_nhan_v2 --root .` trên ứng viên | | **134 ĐẠT · 0 vi phạm · 0 KĐĐ · tổng 187** (nền master: 133) |
| `bien-nhan --packet wp461` trên ứng viên | `python .claude/dev/packet_loop.py bien-nhan --root . --packet wp461` | **1, rc=0** |
| lượt review codex trên ứng viên | `pull/625#issuecomment-5820615576` (`78d9b74f`), `-5820906125` (`ea7711a6`), lượt App trên `020de5e0` (đang chạy lúc soạn) | 2 lượt sạch + 1 lượt App |
| lịch sử lease | g3 (sản phẩm, hết hạn 18:35:59Z) · g4 (bookkeeping, hết hạn 20:28:03Z, PR #624) · g5 (bookkeeping, hết hạn 01:27:45Z, PR #627) | `attempts_used` cộng dồn **1/3** (chỉ g3 có run sản phẩm) — r4 **giữ nguyên**, không reset |
| lớp lặp từ cross-review (để khỏi tái phạm) | thread 4097579866 · 4099651077 · 4099651082 · 4099812197 · 4099812192 | (a) hai lease sống không được có write set giao nhau; (b) scalar YAML có ` #` phải folded/quoted + assert sau parse; (c) verdict = nguyên byte; (d) lease hết hạn là lịch sử, generation mới neo chỉ thị bền; (e) write set phải nằm trong spec đã băm — chính r4 |

## 2. Mục tiêu (bookkeeping — mỗi mục một đường)

| # | đường | nội dung |
|---|---|---|
| M1 | `ops/reviews/wp461-review-1-codex-verdict.md` | NGUYÊN BYTE body UTF-8 comment `5819108011` (đọc ngược REST); không chuẩn hoá, không bỏ khoảng trắng |
| M2 | `ops/reviews/wp461-review-1-codex-verdict.receipt.yaml` | receipt v2: `role: reviewer`, `packet_id: wp461` + `packet_slug`, `reviewed_sha 5e2851881e810b39ebee6884371e5b3e229a01d7`, `surface: codex_service`, `transport: machine`, `assurance: advisory_review`, model/effort/session `KHONG_DO_DUOC`, `github_submitter_identity.actor` = actor VẬN CHUYỂN (`chatgpt-codex-connector[bot]`; người ghi tách `recorder_actor`), `anchor.cuong_do` = candidate ancestry / canonical inclusion pending tới khi land, `evidence_url` neo commit chứa đúng blob verdict, `verdict_sha256` = hash raw |
| M3 | `ops/reviews/README.md` | đúng MỘT hàng Mục lục (6 cột) cho verdict/receipt trên; không mất hàng cũ |

## 3. Write set — ĐÚNG 3 đường

```
ops/reviews/README.md
ops/reviews/wp461-review-1-codex-verdict.md
ops/reviews/wp461-review-1-codex-verdict.receipt.yaml
```
`write_set_hash` (sha256 các đường đã sắp xếp, nối LF, LF cuối): `021c0f52957836d5c7ea66de4bb3b1a5a48d3b25fcaff95c69b88eec61faaed8`.

**Ngoài phạm vi:** ba tệp sản phẩm của r3 §4; `ops/bien_nhan_v2.py`, `ops/lease_publish.py`, `.claude/dev/packet_loop.py`
(validator — nợ `lease-write-set-phai-nam-trong-spec-chua-co-cong`, `receipt-submitter-khop-delivery-author-chua-co-ca-kiem`,
`verdict-bang-byte-comment-chua-co-ca-kiem` → #583/S4); `ops/leases/**` (hồ sơ lease do lease ghi, không do packet);
109 receipt `codex_cli` + receipt r14/r15 của wp523; `CHANGELOG.md`/`RELEASE_MANIFEST.json` (nợ M4 r3, bookkeeping chủ kho).

## 4. Nghiệm thu (mỗi dòng có lệnh và giá trị làm ĐỎ)

| # | đo | ĐẠT | ĐỎ |
|---|---|---|---|
| A1 | `python ops/bien_nhan_v2.py --root .` (rc đọc trực tiếp) | rc=0 · ĐẠT ≥ nền+1 · **0 vi phạm · 0 KĐĐ** | rc≠0 hoặc receipt wp461 không ĐẠT |
| A2 | `python .claude/dev/packet_loop.py bien-nhan --root . --packet wp461` | **≥ 1**, rc=0 | 0 / rc=11 |
| A3 | `git show <evidence commit>:<verdict_path> \| sha256sum` == `verdict_sha256` == sha256 body comment `5819108011` đọc ngược REST (609 B) | bằng nhau | lệch một byte |
| A4 | parse receipt: mọi dòng có ` #` ⇒ mảnh `#…` có trong giá trị đã parse | 0 mảnh mất | ≥1 mảnh mất |
| A5 | `python ops/lease_publish_test.py` (t26/t27) | N/N | ĐỎ |
| A6 | S20 ca đỏ trên bản sao rời: `surface: codex_github_connector` | `bien_nhan_v2` **1 vi phạm** | 0 vi phạm (bộ kiểm không còn răng) |
| A7 | `evidence_url` commit là tổ tiên của head PR; sau land: tổ tiên của master (`git merge-base --is-ancestor`) | rc=0 | rc=1 (squash) |
| A8 | `ai-dang-giu` ba đường TRƯỚC khi ghi | NGƯỜI_GIỮ 0 (hoặc chỉ lease của chính generation này) | lease khác còn hiệu lực giữ đường |
| A9 | land bằng **merge commit**; `bien_nhan_v2` trên master sau land: 0 vi phạm, `bien-nhan --packet wp461` ≥ 1 | | squash / rebase |

Cổng chung: doctrine-scan · adr-song · doc-claims-check --strict · release-verify --strict (`ok`, 180==180) — rc=0. **`git diff --check`
KHÔNG là cổng của packet này**: tệp verdict raw có khoảng trắng cuối dòng là byte đã giao (khai ở lease).

## 5. Điều kiện dừng

- S1 — chạm đường ngoài 3 đường §3 ⇒ DỪNG, revision.
- S2 — tệp sản phẩm xuất hiện trong diff ⇒ DỪNG.
- S3 — sửa spec/verdict/receipt/lease ĐÃ GIAO ⇒ DỪNG.
- S4 — A1/A5 đỏ ⇒ không push (rc đọc trực tiếp, không qua ống).
- S5 — `bien_nhan_v2` đỏ vì surface ⇒ không alias, không miễn trừ; tên đúng là `codex_service`.
- S6 — write set giao với lease còn hiệu lực (kể cả lease wp523) ⇒ DỪNG; generation mới đo A8 trước khi ghi.
- S7 — codex: theo trần §12 hoặc `nang_tran` chủ kho khai bằng comment; lượt App tự bắn khi bỏ draft cũng đếm; executor không mở PR mới để reset.
- S8 — commit tổng hợp do reviewer tự dựng (không có trên server) ⇒ `KHÔNG ĐO ĐƯỢC`, không phải finding; chỉ chấm exact head.
- S9 — hết hạn lease ⇒ ngừng ghi, handoff §7, xin generation mới neo chỉ thị bền.

## 6. Chưa đo được / nợ có tên

- Model/effort/session của reviewer qua GitHub App: `KHONG_DO_DUOC` (chỉ neo được khi chủ kho chạy CLI/Desktop với `-m gpt-6-astra`).
- Ba cổng validator (mục 3, ngoài phạm vi) — #583/S4.
- Nợ M4 r3 (CHANGELOG r376 + manifest) và số Q2 r3 (109 `codex_cli`) — ghi ở #461/#616, ngoài r4.
- Lịch sử g4/g5 mang khuyết tật A12 (write set ngoài spec) — giữ nguyên làm lịch sử; r4 là hợp đồng cho generation từ g6.

## 7. Điều kiện đóng packet

#625 land bằng merge commit (A7/A9 đo trên master) ⇒ đóng nợ `receipt-r15-connector-surface-khong-co-hop-dong` phía wp461; bookkeeping trên #461;
#461 đóng khi chủ kho làm xong nợ M4 (CHANGELOG + manifest).
