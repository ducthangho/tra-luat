# HANDOFF executor — wp1466 (#1466) r9 g2, lượt 3: sửa đúng một dòng ADR-0068

Handoff theo protocol §7; không phải lease, không phải approval. Executor không push, không mở PR, không gọi API ghi, không gọi reviewer.
Giờ là UTC ngày 26-11-2026, theo đồng hồ container. Lượt 3 bắt đầu 18:31:56Z (`out/l3/start.txt`). Mọi số đo ở mục 4 lấy trên commit cục bộ
`da4e876890a1ebe99bb87de9e9a3b4f63c9fd5dd`, trừ những dòng ghi rõ là đối chứng trên commit khác.

## 0. Handoff máy đọc (§7)

```yaml
schema_version: 1
packet_id: wp1466
generation: 2
spec_hash: 28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: 2a807b44-a649-43ef-ac49-0c7da3164694   # phiên CLI lượt 3 (phiên MỚI), đọc từ đường dẫn tasks của harness; phiên điều phối: session_015GtxrcdabvDuhzgezMEE89
base_sha: 695916ea3bfffdd7b2e8fcb94b0740b3c421fe70
head_sha: da4e876890a1ebe99bb87de9e9a3b4f63c9fd5dd
status: needs_followup
summary: >-
  Một commit trên d5d96e7 sửa đúng dòng 3 (dòng Trạng thái) của ADR-0068 theo quyết định Q4 "Dẫn r9": ngày, spec_hash, số revision và URL
  nay dẫn lần duyệt băm r9. Tệp giữ 14385 byte; ba tệp còn lại của write set giữ nguyên blob. N1 ĐẠT với dòng kỳ vọng dựng từ chính blob
  đặc tả (băm và số revision tự tính); doc-claims-check --strict trên clone sạch: "ok": true, flags rỗng; doctrine-scan rc 0; adr-song rc 0
  (67/67); numstat +443 −4, 4 tệp. Các phép đo nặng của lượt 2 (16 mảnh, vòng đột biến…) KHÔNG đo lại trên H mới — mục 5. Không câu hỏi mới.
changed_paths:
  - .claude/dev/packet_loop.py
  - .claude/dev/packet_loop_test.py
  - docs/PROTOCOL_DA_PHIEN.md
  - docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md
tests:
  - {name: "N1 ADR = khối adr r9, dòng Trạng thái theo 8.1", status: passed, evidence: "rc 0, `N1: ĐẠT`, ADR 14385 byte sha256 2da0db8a…45cc = bản dựng; sáu số 0·11·0·0·0·0; đối chứng: cùng script trên d5d96e7 rc 1, lệch đúng dòng 3; log l3-n1-adr, l3-n1-doi-chung-head-cu"}
  - {name: "tl.py doc-claims-check --strict --json (clone sạch của H)", status: passed, evidence: "rc 0, \"ok\": true, flags [], files_scanned 132 (nền 131), claims_flagged 392 = nền 392, mọi lớp 0, 0 advisory lệch nền; log l3-doc-claims-h, l3-doc-claims-nen, l3-doc-claims-so"}
  - {name: "doctrine-scan --root . (clone sạch của H)", status: passed, evidence: "rc 0, `doctrine-scan: sạch — đã quét 12 tệp, 0 chỗ chép doctrine`; log l3-doctrine-scan"}
  - {name: "adr-song --root . (clone sạch của H)", status: passed, evidence: "rc 0, `67 ADR trên đĩa, 67 dòng trong §20, khớp 1–1`; đối chứng: bỏ dòng Trạng thái của ADR-0068 ⇒ rc 9; log l3-adr-song, l3-adr-song-trang-thai"}
  - {name: "git diff --numstat 695916e HEAD (N12)", status: passed, evidence: "4 tệp, +443 −4 (78/1 · 170/1 · 46/2 · 149/0); log l3-numstat-nen"}
  - {name: "git diff d5d96e7 HEAD", status: passed, evidence: "1 tệp, numstat `1 1`, đúng một dòng − và một dòng +, ở dòng 3 của ADR; log l3-diff-head-cu, l3-diff-head-cu-numstat"}
  - {name: "N2 protocol, N5 tự băm (đo thêm)", status: passed, evidence: "N2 17/17, N5 7/7; log l3-n2-protocol, l3-n5-khoa"}
  - {name: "40 ca adr_song_*, 63 ca doctrine mới, r1187_doc_anchors + r1187_docs_positive (đo thêm: các ca đọc docs/adr thật)", status: passed, evidence: "40/40 · 63/63 · `nền: 2/2 đạt`, `TỔNG: ĐẠT`; log l3-adr, l3-ca-moi, l3-r1187-docs"}
  - {name: "eol-policy --all --json, git diff --check (đo thêm)", status: passed, evidence: "\"ok\": true, violations [], scanned 19025; diff --check không in gì; log l3-eol, l3-diff-check"}
  - {name: "N11 tl.py --selftest (clone sạch riêng của H)", status: passed, evidence: "rc 0, `== tl selftest 1789/1789 ==` (hai số bằng nhau), 300,9 s, clone out/ve5/h; log l3-n11-selftest"}
  - {name: "N6(e) 16 mảnh + gom, N7 vòng đột biến mới, N9 họ doctrine cũ + vòng đột biến cũ, N8, N10, các bước CI khác của mục 5b lượt 2", status: not_run, evidence: "KHÔNG đo lại trên da4e876; số của lượt 2 là trên d5d96e7. Xem mục 5"}
  - {name: "N13, N14, N15, N16; Windows", status: not_run, evidence: "cần push/PR/CI/land — ngoài quyền của lượt này; Windows được chủ kho miễn (C3, E2)"}
test_selection:
  gate_tier: T1
  selector_policy_sha: null
  tested_sha: da4e876890a1ebe99bb87de9e9a3b4f63c9fd5dd
  selected_groups: [N1, doc-claims-check, doctrine-scan, adr-song, numstat, "diff một dòng", N2, N5, adr_song_*, "doctrine_inv_* + hai ca G9 + ca kiểm mốc", "r1187_doc_anchors, r1187_docs_positive", eol-policy, tl selftest]
  full_fallback_reason: "diff của lượt là một dòng văn bản trong một tệp ADR; chọn các cổng CÓ ĐỌC tệp ấy (mục 4b). Bộ đầy đủ của packet đã chạy ở lượt 2 trên d5d96e7 và KHÔNG chạy lại (mục 5)"
remaining_work:
  - review exact-H bởi Codex trên da4e876 (phiên điều phối gọi; lease ghi trần còn 3 lời gọi)
  - chủ kho audit exact-H (E5); push + PR draft + CI (N13), ci-dot-bien-du.yml (N14), kiem-merge (N15), hồ sơ sau land (N16)
  - phiên điều phối quyết có đo lại các phép nặng trên da4e876 trước review hay để CI đo (mục 5)
next_role: reviewer
manual_next_action: "Phiên điều phối: dựng mirror ghim core.abbrev 7 tại da4e876, gọi review Codex theo .claude/skills/cross-review/SKILL.md"
copyable_prompt: null
failure: {fingerprint: null, category: null}
successors: []
```

## 1. Kiểm đầu tiên và thẩm quyền

| phép kiểm | lệnh | kết quả |
|---|---|---|
| HEAD lúc bắt đầu | `git rev-parse HEAD` | `d5d96e709e37979986d75742edf0fb9942c18b61` — khớp chỉ thị; nhánh `claude/wp1466-r9-g2`, cây sạch |
| băm đặc tả r9 | `git show 695916e:ops/specs/wp1466.md \| sha256sum` | `28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c` — khớp; blob `823e62c4f50c45425b38d2c71c04852e1dfc1543` = `spec_blob` của lease; dòng `revision:` của blob là `9` (script dựng patch đọc) |
| lease | `git show c9a7a98…:ops/leases/wp1466-r9-g2-claude.yaml` (ref đã có sẵn `origin/ops/wp1466-r9-g2-lease` = `c9a7a9838e82145ef7323ae34cac04c89f973706`) | `lease_id wp1466-r9-g2-claude`, r9 g2, `base_sha 695916e…`, nhánh `claude/wp1466-r9-g2`, write set đúng 4 tệp, hạn `2026-11-29T17:05:00Z`; `authority_url` = `…#issuecomment-7192181084` = URL ghi vào dòng mới. Lượt 3 KHÔNG fetch lại từ remote: ref là bản phiên trước đã fetch |
| mục 8.1 của đặc tả | đọc nguyên văn từ blob tại `695916e` | ngày = ngày UTC của comment duyệt băm; `<64 hex>` = sha256 của chính tệp đặc tả được duyệt; `<N>` = số ở dòng `revision:`; `<URL>` = URL comment duyệt băm |
| chỗ khác trong write set dẫn lần duyệt r8 | Grep bốn tệp write set tại `d5d96e7` với `98790505\|7058374374\|7192181084\|28de9d57\|2026-11-21\|2026-11-26` | **đúng 1 dòng khớp**: dòng 3 của ADR-0068. Không chỗ nào khác ⇒ không có câu hỏi mã E về việc này |

Ba mốc §3.2.1: **baseline nghiệm thu** = **continuation base** = `695916ea3bfffdd7b2e8fcb94b0740b3c421fe70`; **candidate đưa ra review** =
`da4e876890a1ebe99bb87de9e9a3b4f63c9fd5dd`.

**Thứ executor KHÔNG tự đo được, lấy từ chỉ thị lượt 3:** quyết định Q4 "Dẫn r9" (`issuecomment-7200558474`) và `created_at = 2026-11-26T12:34:36Z`
của comment duyệt băm r9 (`issuecomment-7192181084`). MCP github của phiên từ chối credential (401) cả lúc khởi phiên lẫn lần nối lại; executor không
gọi REST bằng đường khác. Phép đối chiếu yếu làm được tại chỗ: URL trùng `authority_url` của lease; lease commit lúc `2026-11-26T16:58:12Z` và merge
`695916e` lúc `2026-11-26T16:56:08Z` (23:56:08+07:00) đều cùng ngày 26-11 — comment 12:34:36Z đứng TRƯỚC merge #1550 hơn bốn giờ, và rơi vào ngày
26-11 ở cả UTC lẫn +07:00 (log `l3-moc-thoi-gian`). Đó là kiểm nhất quán, không phải phép đo `created_at`.

## 2. Head, tree, diff một dòng

- **HEAD = `da4e876890a1ebe99bb87de9e9a3b4f63c9fd5dd`** · **tree = `84018dbd9db5edcb1397e63d81911fc0320247aa`** · cha duy nhất `d5d96e709e37979986d75742edf0fb9942c18b61` (tree `0e20a4b8cd99f2543ee3ca2e329d502f04263967`) · nhánh `claude/wp1466-r9-g2` · chưa push (`## claude/wp1466-r9-g2...origin/master [ahead 3]`).
- Ba commit trên base: `a85db94` (cherry-pick lượt 1) → `d5d96e7` (lượt 2) → `da4e876` (lượt 3). Message của `da4e876` bằng tiếng Việt, hai dòng cuối là
  `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>` và `Claude-Session: https://claude.ai/code/session_015GtxrcdabvDuhzgezMEE89`; không có dấu bỏ qua CI. Bản message: `out/l3/COMMIT_MSG.txt`.
- Blob bốn tệp write set (`git ls-tree`, log `l3-blob-4-tep`, `l3-blob-4-tep-head-moi`):

  | tệp | `d5d96e7` | `da4e876` |
  |---|---|---|
  | `.claude/dev/packet_loop.py` | `0294d136…243b` | `0294d136…243b` (không đổi) |
  | `.claude/dev/packet_loop_test.py` | `d9232bb6…e824` | `d9232bb6…e824` (không đổi) |
  | `docs/PROTOCOL_DA_PHIEN.md` | `dcf248b9…a8ac` | `dcf248b9…a8ac` (không đổi) |
  | `docs/adr/0068-…md` | `bcd8d059…4134` (sha256 `8d5104ce…54d4`, 14385 byte) | `de5bea35…9bc1` (sha256 `2da0db8a25bbbef3eba520353e07f4ad808f0bba0db3864d724b6b4a4fb945cc`, 14385 byte) |

- Bundle: `out/l3/wp1466-r9-g2-da4e876.bundle` (ADR-0060 M12; `git bundle verify`: `is okay`, chứa `refs/heads/claude/wp1466-r9-g2` = `da4e876…`, đòi `695916e…`). Băm ở `out/l3/SHA256SUMS`.

`git diff d5d96e7 HEAD` (nguyên văn, log `l3-diff-head-cu`):

```diff
diff --git a/docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md b/docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md
index bcd8d05..de5bea3 100644
--- a/docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md
+++ b/docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md
@@ -1,6 +1,6 @@
 # ADR-0068 — Bất biến protocol có ID và ô cổng; review theo lớp là bất biến cho mọi lượt review
 
-- **Trạng thái:** Accepted (2026-11-21, chủ kho `ducthangho` duyệt `spec_hash` `98790505d927224bc5e1e42e8f9460376a911a913e2e1d1b12bdf36c5eb20834` của đặc tả `wp1466` r8 trên Issue #1466: https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7058374374)
+- **Trạng thái:** Accepted (2026-11-26, chủ kho `ducthangho` duyệt `spec_hash` `28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c` của đặc tả `wp1466` r9 trên Issue #1466: https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7192181084)
 
 ## Bối cảnh
```

Bốn trường đổi trên dòng ấy: ngày, 64 hex, `r8`→`r9`, số comment trong URL. Không byte nào khác của tệp đổi (độ dài tệp giữ 14385 byte vì bốn trường cùng độ dài).

## 3. Cách ghi

1. `out/sc/sua_l3.py` dựng TỆP PATCH ngoài kho: `out/l3/wp1466-l3-adr-trang-thai.patch` (11 dòng, sha256 `e6b28880ddfea60d2107f1155319fddee085d3fec84511c113f457830305035b`).
   Script đòi: dòng cũ đứng ở ĐÚNG dòng 3 và có đúng 1 lần trong tệp; `98790505` và `7058374374` mỗi chuỗi đúng 1 lần trong tệp; dòng mới — dựng từ
   sha256 và dòng `revision:` của blob đặc tả tại `695916e` — trùng TỪNG KÝ TỰ dòng đích ghi trong chỉ thị; patch có đúng một dòng `-` và một dòng `+`.
2. `git apply --check --verbose` rồi **`git apply --verbose`**: `Applied patch … cleanly`, không bị chặn (log `l3-apply-check`, `l3-apply`).
3. `git add <tệp ADR>` · `git commit -F out/l3/COMMIT_MSG.txt`. Không dùng `git hash-object -w`, `git update-index --cacheinfo`, `git checkout-index`; không dùng
   Edit/Write vào `kho/`. Trước commit: `git status --short --ignored` chỉ có ` M docs/adr/0068-…md` và `.claude/.packet_state/` (bị ignore, do hook phiên tạo);
   `git diff --check` không in gì. Sau commit: cây sạch.

## 4. Bảng phép đo trên `da4e876`

Mọi lệnh chạy qua `out/sc/chay.py <nhãn>` (ghi lệnh, rc, output nguyên văn vào `out/log/<nhãn>.log`); nhãn lượt 3 mang tiền tố `l3-`.
"clone H" = `out/ve4/h`, "clone nền" = `out/ve4/nen`: hai clone dựng trong một lệnh bằng `out/sc/dung_hai_ve.py` (`clone --no-checkout`, ghim
`core.autocrlf false` · `core.eol lf` · **`core.abbrev 7`**, `checkout --detach`); H: HEAD `da4e876…`, tree `84018db…`, `.git` là thư mục, bẩn 0, không shallow (log `l3-dung-ve4`).
Sau các phép đo, `git status --short --ignored` của clone H rỗng (log `l3-ve4-h-status`, `l3-ve4-h-status-cuoi`).

### 4a. Phép đo chỉ thị yêu cầu

| # | lệnh | rc | bằng chứng dương |
|---|---|---|---|
| N1 | `python3 -I -B ../out/sc/do_adr.py . da4e876890a1ebe99bb87de9e9a3b4f63c9fd5dd so` | 0 | **ĐẠT** — `N1: ĐẠT — tệp ADR bằng từng byte khối adr sau khi thay 7 chỗ trống`; ADR tại H 14385 byte sha256 `2da0db8a…45cc` = bản dựng; sáu số `0·11·0·0·0·0`; đặc tả `r9 sha256=28de9d57…6f7c`. Dòng kỳ vọng in trong log: ngày `2026-11-26`, băm = sha256 script TỰ TÍNH trên blob đặc tả, `r9` = dòng `revision:` script TỰ ĐỌC, URL `…#issuecomment-7192181084` ⇒ cả bốn trường khớp quy tắc 8.1 (ngày và URL: theo số chỉ thị khai, mục 1) |
| N1 đối chứng âm | cùng lệnh với `d5d96e7…` | 1 | `N1: KHÔNG ĐẠT`, `lệch dòng (3, …2026-11-21…, …2026-11-26…)` — script phân biệt được dòng r8 với dòng r9; chỉ dòng 3 lệch (log `l3-n1-doi-chung-head-cu`) |
| N1 trên index trước commit | cùng lệnh với `:` | 0 | `N1: ĐẠT`, cùng sha256 `2da0db8a…45cc` (log `l3-n1-index`) |
| doctrine-scan | clone H: `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 12 tệp, 0 chỗ chép doctrine` |
| adr-song | clone H: `python3 -B .claude/dev/packet_loop.py adr-song --root .` | 0 | `adr-song: sạch — 67 ADR trên đĩa, 67 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` |
| doc-claims | clone H: `python3 -B scripts/tl.py doc-claims-check --strict --json` | 0 | **`"ok": true`, `"flags": []`**, `"strict": true`, `files_scanned` 132, `claims_flagged` 392, `advisory_count` 392, `by_layer` mọi lớp L1…L9, L12 bằng 0. Clone nền cùng lệnh: rc 0, `ok` true, `files_scanned` 131, 392/392. So tập advisory (bỏ số dòng): 0 mục chỉ có ở H, 0 mục chỉ có ở nền (`out/sc/so_doc_claims.py`, log `l3-doc-claims-so`: `DOC_CLAIMS: ĐẠT`) |
| numstat so với base | `git diff --numstat 695916e HEAD` | 0 | `78 1` · `170 1` · `46 2` · `149 0` ⇒ **+443 −4, 4 tệp** — dưới trần 450 dòng thêm / 6 tệp, còn 7 dòng; không đổi so với lượt 2 |
| diff so với HEAD cũ | `git diff d5d96e7 HEAD` · `git diff --numstat d5d96e7 HEAD` | 0 · 0 | một tệp (ADR), numstat `1 1`, một hunk, đúng một dòng `-` và một dòng `+` ở dòng 3 (mục 2) |

### 4b. Phép đo thêm của executor — các cổng CÓ ĐỌC tệp ADR

Cách chọn: liệt kê theo ĐẦU VÀO — cổng hay ca nào đọc `docs/adr/0068-…md` hoặc cả thư mục `docs/adr/` của kho thật (Grep `packet_loop.py`, `packet_loop_test.py`
với `0068|Trạng thái|docs/adr`), cộng các cổng quét mọi tệp. Danh sách này lọc theo phép Grep ấy; nó KHÔNG phải trần — cổng đọc tệp ADR theo đường khác thì chưa đo (mục 5).

| phép đo | lệnh | rc | bằng chứng dương |
|---|---|---|---|
| `adr-song` có đọc dòng Trạng thái của ADR-0068 không | `python3 -I -B ../out/sc/do_adr_song_trang_thai.py ../out/ve4/h ../out/tmp/l3-adr-song-am` (cây tạm ngoài kho) | 0 | 3/3 đúng kỳ vọng: nguyên trạng ⇒ rc 0; **bỏ dòng Trạng thái ⇒ rc 9** (`ADR-0068: … không có dòng Trạng thái đọc được`); đặt lại dòng r8 ⇒ rc 0. Tức `adr-song` canh SỰ CÓ MẶT của dòng, không canh nội dung; nội dung (băm, `r9`, ngày, URL) chỉ có N1 canh |
| 40 ca `adr_song_*` | `python3 -u -B sc/chay_ca.py ve4/h ve4/nen tmp/l3-chay-ca adr` | 0 | `[adr] CHỌN 40 · CHẠY 40 · ĐẠT 40/40 · ĐỎ 0 · BỎ QUA 0` |
| N6 (d): T + ca kiểm mốc + hai ca G9 (có `doctrine_scan_repo_that_sach`) | `… sc/chay_ca.py ve4/h ve4/nen tmp/l3-chay-ca ca-moi` | 0 | `[ca-moi] CHỌN 63 · CHẠY 63 · ĐẠT 63/63 · ĐỎ 0 · BỎ QUA 0`; sổ: `CASES nền=1804 H=1864 · T=60 · MUTANTS nền=2077 H=2106` |
| hai ca chép/đọc `docs/adr/` thật | `python3 -u -B sc/chay_nen_tron.py ve4/h tmp/l3-r1187 r1187_doc_anchors,r1187_docs_positive` (qua `main()` gốc) | 0 | `nền: 2/2 đạt · BỎ QUA: 0`, `TỔNG: ĐẠT` |
| N2 | `python3 -I -B sc/do_protocol.py ../kho 695916e… da4e876…` | 0 | 17/17 dòng `ĐẠT`, `N2: ĐẠT`, numstat `46 2`, protocol H sha256 `3453ab9b…e29a` |
| N5 | `python3 -I -B sc/khoa_doc_lap.py <protocol> <đặc tả> <packet_loop.py>` của clone H | 0 | `N5: ĐẠT — 7/7 bộ bốn: tự tính = khối khoa = hằng trong mã` |
| eol-policy | clone H: `python3 -B .githooks/eol_policy.py --all --json` | 0 | `"ok": true`, `"violations": []`, `scanned` 19025, `checked` 18092 |
| `git diff --check d5d96e7 HEAD` | — | 0 | không in gì |
| N11 `tl.py --selftest` | clone sạch RIÊNG `out/ve5/h` (cùng commit, cùng tree; không lệnh nào khác chạy trong clone ấy): `python3 -u -B scripts/tl.py --selftest` | 0 | `== tl selftest 1789/1789 ==` (hai số bằng nhau; cùng số với lượt 2 trên `d5d96e7`), 18:37:04Z→18:42:05Z, 300,9 s (log `l3-n11-selftest`). Vế "trước lần đẩy" của N11: executor không đẩy |

## 5. Những gì chưa đo

- **Các phép đo nặng của lượt 2 KHÔNG đo lại trên `da4e876`.** Số của chúng trong `HANDOFF-l2.md` là trên `d5d96e7`, không phải trên candidate này:
  N6 (e) 16 mảnh + gom của `packet_loop_test` (1861 ca), N7 vòng đột biến mới (29), N9 họ doctrine cũ (133 ca) và vòng đột biến cũ (21), N8 `do-pham-vi`, N10 ruff,
  hai ca `CA_DAI`, và các bước CI của mục 5b lượt 2 (`idiom_py_test`, `ci_phamvi`, `gate_lifecycle_test`, `bien_nhan_v2_test`, `chon_reviewer_test`,
  `ci_dang_ky_test`). Cái đo được thay cho "không đổi": blob của `packet_loop.py`, `packet_loop_test.py` và protocol giống hệt giữa hai commit (mục 2), nên các phép
  đo chỉ nhận ba blob ấy làm đầu vào (N2, N5, N8, N10) có cùng đầu vào; N2 và N5 đã chạy lại, N8 và N10 thì không. Với các phép còn lại, executor KHÔNG
  khẳng định kết quả cũ còn đúng: một ca đọc cây `docs/adr/` thật theo đường mà phép Grep ở 4b không thấy thì chưa được đo trên H mới. CI trên H (N13) là nơi đo đủ.
  Protocol §10.1 nói thẳng: evidence chỉ được reuse khi tested SHA/tree khớp chính xác, "head hoặc một identity đổi thì chạy lại", và packet sensitive thì T2 là full
  trên exact head. Vậy `da4e876` CHƯA có full oracle nào; lượt 3 chỉ đạt mức T1 (nhóm bị ảnh hưởng + EOL + write set). Chỉ thị lượt 3 liệt kê đóng các phép phải đo
  và không gồm bộ đầy đủ, nên executor không tự chạy (ước ~85 phút máy cho 16 mảnh). Muốn đo trước review thì lệnh đã sẵn, chạy từ `out/`, trong một clone sạch
  KHÔNG có lệnh nào khác chạy cùng (bài học mảnh 0 của lượt 2): `python3 -u -B sc/chay_manh.py ve4/h manh-h3 tho <k> 3` với k = 0, 1, 2, rồi `… sc/chay_manh.py ve4/h manh-h3 gom`;
  vòng đột biến: `… sc/chay_ca.py ve4/h ve4/nen tmp/l3-chay-ca db-moi` và `… db-cu`; họ cũ: `… ca-cu`.
- **Ca `wp1303_target_human_chain`** vẫn chưa từng được executor đo trên H nào (như lượt 1, lượt 2).
- **`created_at` của hai comment** (`…7192181084`, `…7200558474`) và nội dung quyết định Q4: không đo được từ phiên này (mục 1) — lấy theo chỉ thị.
- **N13, N14, N15, N16**: cần push/PR/CI/land — ngoài quyền của lượt này. **Windows**: không đo (miễn theo C3). **Python**: máy đo chỉ có 3.13; `ci.yml` ghim 3.12.
- **N5 vế reviewer tự băm, mirror reviewer, `core.abbrev 7` ở clone reviewer**: việc của phiên điều phối và reviewer.
- **Lease không fetch lại từ remote ở lượt 3**: đọc từ ref `origin/ops/wp1466-r9-g2-lease` có sẵn trong clone (`c9a7a98`, khớp chỉ thị). Lease bị thay hay thu hồi sau lần fetch của lượt 2 thì phiên này không thấy.
- **Model/effort thực phục vụ**: phiên tự nhận `claude-fable-5-2`; effort `KHONG_DO_DUOC` từ bên trong.
- **Bảng "bước CI khác" của lượt 2 để ô `ci_dang_ky_test --chay` là ĐANG CHẠY**: log `out/log/l2-ci-dang-ky.log` nay có ba dòng `TỔNG: ĐẠT` nhưng KHÔNG có dòng `# rc:` ở đầu
  (đầu log chỉ có `# bat dau: 2026-11-26T17:36:55Z`), tức lượt chạy ấy không ghi được rc kết thúc. Executor lượt 3 không chạy lại và không diễn giải log ấy thành "đạt".

## 6. Sai lệch và điều phải khai

- **Script đo N1 đã bị SỬA ở lượt 3.** `out/sc/do_adr.py` của lượt 2 gõ cứng dòng Trạng thái r8 làm kỳ vọng, nên chạy nguyên bản thì N1 sẽ đỏ trên H mới.
  Executor sửa đúng phần kỳ vọng của dòng ấy: băm lấy từ sha256 script tự tính trên blob đặc tả, số revision từ dòng `revision:`, ngày và URL là hai hằng theo chỉ thị;
  thêm một dòng in dòng kỳ vọng. Bản lượt 2 giữ ở `out/l3/do_adr.luot2.py`; trên `d5d96e7` bản lượt 2 cho rc 0 (log `l3-n1-truoc-va`), bản mới cho rc 1 (log `l3-n1-doi-chung-head-cu`).
  Phần so từng byte với khối `adr` và phép đo sáu số không đổi.
- **Script mới của lượt 3** (đều ở `out/sc/`, ngoài kho): `sua_l3.py` (dựng patch), `do_adr_song_trang_thai.py` (đối chứng `adr-song`), `bam_l3.py` (ghi `SHA256SUMS`).
- **Message của commit `a85db94`** (cherry-pick lượt 1) vẫn nói "đặc tả r8, spec_hash 98790505…, lease wp1466-r8-g1-claude". Đó là message, không phải tệp của write set, và lượt 2 đã khai; lượt 3 không viết lại lịch sử.
- **Không lớp lỗi mới.** Lượt này không vá lớp nào: thay đổi là dữ liệu của một dòng theo quyết định Q4, không phải bản vá cho một finding. Phép quét cả lớp đã làm cho đúng câu hỏi "còn chỗ nào dẫn lần duyệt r8": Grep bốn tệp write set, đúng 1 chỗ (mục 1). Không `hint_provenance`. Không ghi nợ.
- **Không ghi gì ngoài tệp ADR trong `kho/`**: `git status --short --branch --ignored` sau cùng chỉ có `.claude/.packet_state/` (bị ignore; do hook phiên tạo). Tệp tạm, clone đo, log, bundle đều ở `out/`.
- **Lệnh bị chốt quyền của phiên từ chối ở lượt 3** (không ảnh hưởng kết quả; executor đổi sang lệnh đơn qua `chay.py`): hai lệnh Bash ghép nhiều thao tác (`cut`/`head`/`wc`/`xxd`/`echo`) và `cp -p`. Không lần nào `git apply` bị chặn.

## 7. Câu hỏi cho chủ kho

Không có câu hỏi mới mã E1–E5 ở lượt 3. Q4 đã được quyết và đã áp. Q3 của lượt 1 (năm dạng bản sao không đứng thành đơn vị; thẻ HTML giữa dòng) vẫn mở theo chỉ thị trước; lượt này không làm gì cho nó.

## 8. Hiện vật lượt 3 ở `out/`

- `HANDOFF-l3.md` (tệp này) · `l3/COMMIT_MSG.txt` · `l3/wp1466-l3-adr-trang-thai.patch` · `l3/wp1466-r9-g2-da4e876.bundle` · `l3/do_adr.luot2.py` · `l3/SHA256SUMS`
- `sc/sua_l3.py`, `sc/do_adr_song_trang_thai.py`, `sc/bam_l3.py` (mới) · `sc/do_adr.py` (sửa)
- `ve4/h`, `ve4/nen` — hai clone đo · `ve5/h` — clone riêng của selftest (`ve5/nen` dựng kèm, không dùng) · `log/l3-*.log`
- Hiện vật lượt 1 và lượt 2 giữ nguyên, không sửa (trừ `sc/do_adr.py`, đã khai ở mục 6).

HEAD=da4e876890a1ebe99bb87de9e9a3b4f63c9fd5dd N1=dat DOC_CLAIMS=ok DOCTRINE=0 ADR_SONG=0 NUMSTAT=+443 -4
