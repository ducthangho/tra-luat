# HANDOFF executor — wp1466 (#1466) r9 g2, lượt 2

**TRẠNG THÁI TỆP: BẢN GẦN CUỐI (18:06Z) — chỉ còn `ci_dang_ky_test` đang chạy.** Ô ghi `ĐANG CHẠY` là phép đo đã khởi nhưng chưa có kết quả lúc ghi; nếu phiên bị cắt trước lần cập nhật kế thì
đọc ô ấy là `KHÔNG ĐO ĐƯỢC` và xem log ở `out/log/l2-*.log`, `out/manh-h2/`.

Handoff theo protocol §7; không phải lease, không phải approval. Executor không push, không mở PR, không gọi API ghi, không gọi reviewer.
Giờ là UTC ngày 26-11-2026, theo đồng hồ container. Lượt 2 bắt đầu 17:11:18Z. Mọi số đo trên commit cục bộ `d5d96e709e37979986d75742edf0fb9942c18b61`.

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
session_id: 53b08a72-9e60-41a9-abde-905241a3d60a   # phiên CLI lượt 1 được resume; phiên điều phối: session_015GtxrcdabvDuhzgezMEE89
base_sha: 695916ea3bfffdd7b2e8fcb94b0740b3c421fe70
head_sha: d5d96e709e37979986d75742edf0fb9942c18b61
status: needs_followup
summary: >-
  Cherry-pick commit lượt 1 (96e4472) lên base mới 695916e (sạch, không xung đột), rồi một commit sửa cho khớp đặc tả r9: bảng §1.1 của protocol
  bằng từng byte khối p2-moi của r9 (18 con trỏ ca không backtick + một câu luật), băm K01 trong INV_KHOA_PROTOCOL theo khối khoa của r9.
  doc-claims-check --strict trên clone sạch của H: "ok": true, flags rỗng. N1–N12 ĐẠT ở phần đo được tại chỗ (packet_loop_test: 16 mảnh + gom, nền 1823/1823; selftest 1789/1789; 29/29 đột biến mới; 21/21 đột biến cũ); N13–N16 KHÔNG ĐO ĐƯỢC (cần CI/sau land). Không lớp lỗi mới. Một câu hỏi E5 (Q4, dòng Trạng thái của ADR).
changed_paths:
  - .claude/dev/packet_loop.py
  - .claude/dev/packet_loop_test.py
  - docs/PROTOCOL_DA_PHIEN.md
  - docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md
tests:
  - {name: "tl.py doc-claims-check --strict --json (clone sạch của H)", status: passed, evidence: "rc 0, \"ok\": true, flags [], claims_flagged 392 = nền 392, 0 advisory lệch nền; log l2-doc-claims-h, l2-doc-claims-nen, l2-doc-claims-so"}
  - {name: "doctrine-scan --root . (N4)", status: passed, evidence: "rc 0, `doctrine-scan: sạch — đã quét 12 tệp, 0 chỗ chép doctrine`"}
  - {name: "adr-song --root . (N3)", status: passed, evidence: "rc 0, `67 ADR trên đĩa, 67 dòng` (nền 66/66); bỏ dòng ADR-0068 của §20 ⇒ rc 9"}
  - {name: "N1 ADR = khối adr r9", status: passed, evidence: "bằng từng byte, 14385 byte, sáu số 0·11·0·0·0·0"}
  - {name: "N2 protocol = nền + sáu khối r9", status: passed, evidence: "17/17 phép, numstat 46 2, 18 con trỏ ca không backtick"}
  - {name: "N5 tự băm độc lập", status: passed, evidence: "7/7 bộ bốn; K01 = 987f9527…81c5"}
  - {name: "N6(a)(b)(c)(d)(f), so-dang-ky", status: passed, evidence: "57/57 ca bắt buộc; T = 60; 63/63 đạt, 0 bỏ qua; `SỔ ĐĂNG KÝ: ĐẠT`"}
  - {name: "N6(e) packet_loop_test mọi ca: 16 mảnh + gom", status: passed, evidence: "16/16 bản ghi mảnh rc 0, mỗi mảnh `TỔNG: ĐẠT`; cộng 16 dòng: `nền: 1823/1823 đạt · BỎ QUA: 38`; `GOM: mọi mảnh khớp phân hoạch` · `GOM: ĐẠT · 16 mảnh · 1861 ca bắt buộc`; carrier WP1174 ở đúng mảnh 0. Mảnh 0 chạy HAI lần (lần đầu rc 1 do giàn đo của executor — mục 8); log l2-manh-tho-0/1/2, l2-manh-0-chay-lai, l2-manh-gom, l2-manh-cong"}
  - {name: "hai ca CA_DAI (ngoài 16 mảnh)", status: not_run, evidence: "1/2: `wp1303_target_supported_pairs` passed (`nền: 1/1 đạt`, `TỔNG: ĐẠT`, rc 0, 1200 s; log l2-ca-dai-2); `wp1303_target_human_chain` KHÔNG ĐO ĐƯỢC — khởi 17:14:32Z, executor dừng 17:28Z chưa có kết quả để nhường nhân cho phép đo bắt buộc; xem mục 8"}
  - {name: "N7 vòng đột biến mới (29)", status: passed, evidence: "`nền: 63/63 đạt · BỎ QUA: 0`; 29/29 dòng `ok … 3 đối chứng khác họ còn sống`; 0 dòng ĐỎ; `TỔNG: ĐẠT`; rc 0; log l2-db-moi"}
  - {name: "N8 do-pham-vi ma/test", status: passed, evidence: "`PHẠM VI [ma]: ĐẠT` · `PHẠM VI [test]: ĐẠT`, so với blob nền 695916e"}
  - {name: "N9 hành vi cũ", status: passed, evidence: "40/40 adr_song_*; 133/133 (132 ca họ doctrine cũ + ca kiểm mốc), 0 bỏ qua; vòng đột biến cũ `nền: 132/132 đạt`, 21/21 dòng `ok … 3 đối chứng khác họ còn sống`, `TỔNG: ĐẠT`"}
  - {name: "N10 ruff --select F", status: passed, evidence: "delta 0: nền 3+13, H 3+13, mới 0, mất 0 (ruff 0.15.15)"}
  - {name: "N11 tl.py --selftest", status: passed, evidence: "`== tl selftest 1789/1789 ==`, rc 0, 431,6 s; log l2-n11-selftest"}
  - {name: "N12 numstat", status: passed, evidence: "4 tệp, +443 −4 so với 695916e"}
  - {name: "bảng đột biến đầy đủ 2106 (N14/K7), CI PR (N13), kiem-merge (N15), sau land (N16)", status: not_run, evidence: "cần push/PR/CI/land — ngoài quyền của lượt này"}
  - {name: "Windows", status: not_run, evidence: "chủ kho miễn (C3, E2)"}
test_selection:
  gate_tier: T2
  selector_policy_sha: null
  tested_sha: d5d96e709e37979986d75742edf0fb9942c18b61
  selected_groups: [doc-claims-check, doctrine_inv_*, họ doctrine cũ, adr_song_*, "packet_loop_test: 16 mảnh + gom (1861 ca) + 1 trong 2 ca CA_DAI", tl selftest]
  full_fallback_reason: "packet sensitive ⇒ chạy bộ ca của packet_loop_test theo cách của CI: 1862/1863 ca đã chạy, thiếu wp1303_target_human_chain; bảng đột biến đầy đủ để CI (K7)"
remaining_work:
  - review exact-H bởi Codex trên d5d96e7 (phiên điều phối gọi; lease ghi trần còn 3 lời gọi)
  - chủ kho audit exact-H (E5); push + PR draft + CI (N13), ci-dot-bien-du.yml (N14), kiem-merge (N15), hồ sơ sau land (N16)
  - câu Q4 ở mục 9 (dòng Trạng thái của ADR-0068 dẫn lần duyệt băm r8)
next_role: reviewer
manual_next_action: "Phiên điều phối: quyết Q4 (hoặc nhận khuyến nghị), dựng mirror ghim core.abbrev 7 tại d5d96e7, gọi review Codex theo .claude/skills/cross-review/SKILL.md"
copyable_prompt: null
failure: {fingerprint: null, category: null}
successors: []
```

## 1. Kiểm đầu tiên và thẩm quyền

| phép kiểm | lệnh | kết quả |
|---|---|---|
| `origin/master` chứa `695916e` | `git fetch origin master` · `git rev-parse origin/master` · `git merge-base --is-ancestor 695916e… origin/master` | `origin/master` = `695916ea3bfffdd7b2e8fcb94b0740b3c421fe70` (fetch in `1fac6ce..695916e`); là tổ tiên: rc 0 |
| băm đặc tả r9 | `git show 695916e:ops/specs/wp1466.md \| sha256sum` | `28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c` — khớp; blob `823e62c4f50c45425b38d2c71c04852e1dfc1543` = `spec_blob` của lease |
| bốn tệp write set giữa `1fac6ce` và `695916e` | `git diff --quiet 1fac6ce 695916e -- <bốn tệp>` | rc 0, `--stat` rỗng (ADR-0068 chưa có ở cả hai) |
| lease | `git fetch origin ops/wp1466-r9-g2-lease` · `git show FETCH_HEAD:ops/leases/wp1466-r9-g2-claude.yaml` | commit `c9a7a9838e82145ef7323ae34cac04c89f973706`; `lease_id wp1466-r9-g2-claude`, r9 g2, `thay_the_cho: [wp1466-r8-g1-claude]`, `base_sha 695916e…`, nhánh `claude/wp1466-r9-g2`, write set đúng 4 tệp, hạn `2026-11-29T17:05:00Z` |
| tài liệu phải đọc nguyên văn | `git diff --quiet 1fac6ce 695916e -- .claude/skills/work-packet/SKILL.md docs/adr/0060-…md docs/PROTOCOL_DA_PHIEN.md CLAUDE.md` | rc 0: bốn tệp này KHÔNG đổi so với bản executor đã đọc nguyên văn ở lượt 1 của chính phiên này (nội dung còn trong ngữ cảnh phiên, không tóm tắt); lượt 2 không đọc lại chúng. ADR-0062 và ADR-0063: đọc nguyên văn ở lượt 2. Đặc tả r9: đọc trọn diff r8→r9 (mọi đoạn chữ đổi), phần không đổi đã đọc ở lượt 1 |

Trên `master` giữa hai base, ngoài `ops/**` chỉ có `.claude/dev/ci_dang_ky_test.py` và năm tệp `.agents/skills/proxima-control/**` đổi (`git diff --name-status 1fac6ce 695916e`).

Ba mốc §3.2.1: **baseline nghiệm thu** = **continuation base** = `695916ea3bfffdd7b2e8fcb94b0740b3c421fe70`; **candidate đưa ra review** =
`d5d96e709e37979986d75742edf0fb9942c18b61`, tree `0e20a4b8cd99f2543ee3ca2e329d502f04263967`.

## 2. Head, tree, numstat

- HEAD = `d5d96e709e37979986d75742edf0fb9942c18b61` · tree = `0e20a4b8cd99f2543ee3ca2e329d502f04263967` · nhánh `claude/wp1466-r9-g2` · chưa push.
- Hai commit trên base (executor chọn KHÔNG gộp, để commit lượt 1 còn đối chiếu được từng byte):
  1. `a85db94dc56603b2a71df51af01b45af94dc3698` (tree `e8584d1fc714cf9a16424a551f18f2cfcde45554`) — cherry-pick của `96e4472`; message giữ nguyên của lượt 1 (nói về r8 g1).
  2. `d5d96e709e37979986d75742edf0fb9942c18b61` — commit sửa theo r9. Hai dòng cuối của message đúng yêu cầu; không có dấu bỏ qua CI.
- Bundle: `out/l2/wp1466-r9-g2-d5d96e7.bundle` (ADR-0060 M12), băm ở `out/l2/SHA256SUMS`.

`git diff --numstat 695916e d5d96e7`:

```
78	1	.claude/dev/packet_loop.py
170	1	.claude/dev/packet_loop_test.py
46	2	docs/PROTOCOL_DA_PHIEN.md
149	0	docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md
```

Tổng **+443 −4, 4 tệp** — dưới trần ADR-0053 (450 dòng thêm / 6 tệp), còn 7 dòng.

## 3. Cách đưa lượt 1 lên base mới, và cách sửa theo r9

1. `git checkout -b claude/wp1466-r9-g2 origin/master` (tại `695916e`), rồi `git cherry-pick 96e4472`: **sạch, không xung đột** (`4 files changed, 443 insertions(+), 4 deletions(-)`).
   `git diff --stat 96e4472 a85db94 -- <bốn tệp>` rỗng: nội dung bốn tệp sau cherry-pick trùng commit lượt 1.
2. Bản vá r9 dựng thành TỆP PATCH ngoài kho bằng `out/sc/sua_r9.py` → `out/l2/wp1466-r9.patch` (63 dòng, sha256 `0424d0fe123194ec701dc423bc96ad3accbb3a98a57eb58184f4a0f0171f1159`;
   dựng lại lần hai từ `a85db94` cho đúng băm ấy), rồi `git apply --check` và **`git apply`** — không bị chặn. Không dùng `git hash-object -w`,
   `git update-index --cacheinfo` hay `git checkout-index`; không dùng Edit/Write vào `kho/`.
3. Nội dung bản vá (`git diff --stat 96e4472 d5d96e7`: `packet_loop.py` 1 dòng đổi, protocol 16 dòng đổi; `packet_loop_test.py` và ADR không đổi):
   - `docs/PROTOCOL_DA_PHIEN.md`: thay nguyên khối `p2-moi` r8 đang ở §1.1 bằng khối `p2-moi` r9 (script đòi khối cũ có đúng 1 lần): dòng dẫn thêm câu luật, 15 dòng bảng bỏ backtick quanh 18 con trỏ `ca:`.
   - `.claude/dev/packet_loop.py`: băm đơn vị của `K01` `607431f2…0531` → `987f952747e26847a5a8e39dd82bf09da72d508dd3e03cef3bfdd42db4e381c5` (script lấy từ khối `khoa` r9, và đòi r9 chỉ khác r8 ở đúng trường ấy).
   - Fixture hay ca ghi cứng băm/nội dung cũ của `K01`: **không có** — `_proto_co_khoa` dựng từ protocol thật và từ hằng của mã cổng; các ca `K01` tìm dòng theo tiền tố ``| `INV-07` `` và tiêu đề `### 1.1 `. Bằng chứng: 63/63 ca mới đạt, và vòng đột biến (mục 5, N7).

## 4. `doc-claims-check`

Lệnh: `python3 -B scripts/tl.py doc-claims-check --strict --json`, chạy trong clone SẠCH của H (`out/ve2/h`) và của nền (`out/ve2/nen`), hai clone dựng trong một
lệnh (`out/sc/dung_hai_ve.py`: `clone --no-checkout`, ghim `core.autocrlf false` · `core.eol lf` · `core.abbrev 7`, `checkout --detach`; cả hai sạch, `.git` là thư mục, không shallow).

| vế | rc | `"ok"` | `flags` | `files_scanned` | `claims_flagged` | `advisory_count` |
|---|---|---|---|---|---|---|
| nền `695916e` | 0 | `true` | `[]` | 131 | 392 | 392 |
| H `d5d96e7` | 0 | `true` | `[]` | 132 | 392 | 392 |

`by_layer` của cả hai: mọi lớp L1…L9, L12 bằng 0. So tập advisory (bỏ số dòng): 0 mục chỉ có ở H, 0 mục chỉ có ở nền (log `l2-doc-claims-so`).
Đối chiếu: H lượt 1 (`96e4472`) cho rc 2 với 3 cờ L12 (log `h-doc-claims` của lượt 1).

## 5. Bảng N1–N16

Mọi lệnh chạy qua `out/sc/chay.py <nhãn>` (ghi lệnh, rc, output nguyên văn vào `out/log/<nhãn>.log`); nhãn lượt 2 mang tiền tố `l2-`. "clone H" = `out/ve2/h`, "clone nền" = `out/ve2/nen`.

| # | lệnh (rút gọn) | rc | kết quả |
|---|---|---|---|
| N1 | `python3 -I -B sc/do_adr.py ../kho d5d96e7… so` | 0 | **ĐẠT** — ADR bằng từng byte khối `adr` của r9 sau khi thay 7 chỗ trống (14385 byte, sha256 `8d5104ce…54d4`, không đổi so với lượt 1); sáu số đo trên H mới: `0·11·0·0·0·0`. Dòng Trạng thái: câu Q4 |
| N2 | `python3 -I -B sc/do_protocol.py ../kho 695916e… d5d96e7…` | 0 | **ĐẠT** — 17/17 phép: H = nền + đúng sáu khối của r9, từng byte; mỗi `p*-moi` 1 lần đúng vị trí; `p4-cu` 0; dòng `p5-cu` 0; numstat `46 2`; 28 dòng `INV-01`…`INV-28`; 18 con trỏ `ca:` không backtick, 0 con trỏ có backtick |
| N3 | `packet_loop.py adr-song --root .` (clone H · clone nền · cây tạm bỏ dòng p6) | 0 · 0 · 9 | **ĐẠT** — H `67 ADR trên đĩa, 67 dòng trong §20`; nền 66/66; bỏ dòng `ADR-0068` ⇒ rc 9 |
| N4 | `packet_loop.py doctrine-scan --root .` (clone H) | 0 | **ĐẠT** — `doctrine-scan: sạch — đã quét 12 tệp, 0 chỗ chép doctrine`. Phép làm nó đỏ: các ca đòi rc 9 trong T đạt ở N6 (d); bộ dò thử `sc/do_tham.py` 25/25 đúng kỳ vọng |
| N5 | `python3 -I -B sc/khoa_doc_lap.py <protocol H> <đặc tả r9> <packet_loop.py H>` | 0 | **ĐẠT** — 7/7: tự băm = khối `khoa` r9 = hằng trong mã; `K01` = `987f952747e26847…` ở dòng 49–82; mỗi đơn vị 1 bản hiển thị. Vế "reviewer tự băm": KHÔNG ĐO ĐƯỢC ở lượt executor (việc của reviewer) |
| N6 | (a) `sc/do_tap_bat_buoc.py`; (b)(c)(f) `khoi-r9/so_dang_ky.py ve2/nen ve2/h`; (d) `sc/chay_ca.py … ca-moi`; (e) `sc/chay_manh.py ve2/h manh-h2 tho k 3` ×3 + `… gom` | 0 | (a) **ĐẠT** 57/57 ⊆ T · (b) **ĐẠT** 60/60 tên mang tiền tố `doctrine_inv_` · (c) **ĐẠT** \|T\| = 60 = 1864−1804 = 1863−1803 (T như lượt 1, liệt kê ở HANDOFF lượt 1 mục 11) · (d) **ĐẠT** 63/63 (T + ca kiểm mốc + hai ca G9), 0 bỏ qua — gồm ba ca "phần đầu tệp" · (e) **ĐẠT** — 16/16 mảnh rc 0 và `TỔNG: ĐẠT`; cộng 16 dòng: **`nền: 1823/1823 đạt`** · `BỎ QUA: 38` (37 ca `wp1342_native_*` và `luong_canonical_chay_that` của nền; 0 ca thuộc T); `GOM: mọi mảnh khớp phân hoạch` · `GOM: ĐẠT · 16 mảnh · 1861 ca bắt buộc (sổ 1863 − CA_DAI)`; carrier WP1174 chạy ở đúng mảnh 0. Cùng số với lượt 1. Mảnh 0 phải chạy hai lần: lần đầu rc 1 vì giàn đo của executor (mục 8), lần hai trong clone sạch riêng rc 0. Hai ca `CA_DAI` ngoài 16 mảnh: `wp1303_target_supported_pairs` **ĐẠT** (`nền: 1/1 đạt · BỎ QUA: 0`, `TỔNG: ĐẠT`, rc 0, 1200 s, qua `main()` gốc bằng `sc/chay_nen_tron.py`; log `l2-ca-dai-2`). `wp1303_target_human_chain` **KHÔNG ĐO ĐƯỢC**: khởi lúc 17:14:32Z, executor chủ động DỪNG lúc 17:28Z khi nó chưa in kết quả nào — máy 4 nhân đang chạy 7 tiến trình, và ca này một mình ước ~85 phút (1820 s trong `packet_loop_test_manh.py` × hệ số chậm ~2,8 đo được ở ca kia), không kịp trong quỹ ~100 phút. Ở lượt 1 nó cũng bị cắt khi phiên kết thúc. Vậy ca ấy chưa từng được executor đo trên H nào; trên CI nó chạy ở `packet-loop-dot-bien.yml`, không thuộc cổng bắt buộc `gate-packet-loop`. · (f) **ĐẠT** `SỔ ĐĂNG KÝ: ĐẠT`, CASES 1804→1864, MUTANTS 2077→2106, 0 bộ ba cũ đổi |
| N7 | `sc/chay_ca.py ve2/h ve2/nen … db-moi` (`packet_loop_test_manh.chay`: nền = T + hai ca G9 + ca kiểm mốc; pha đột biến = MỌI đột biến có ở H mà không có ở nền = 26 bắt buộc + 3 "phần đầu tệp") | 0 | **ĐẠT** — `nền: 63/63 đạt · BỎ QUA: 0`; 29/29 dòng `ok <tên> → giết N ca đích · 3 đối chứng khác họ còn sống`; 0 dòng `ĐỎ`; `TỔNG: ĐẠT`. Ba đột biến "phần đầu tệp": `inv_bo_dem_truoc_tieu_de_dau` giết 2, `inv_truoc_tieu_de_chi_khoi_dau` giết 1, `inv_truoc_tieu_de_bo_bien_tieu_de` giết 1. `inv_bo_khoa_K01` (băm mới) giết 8. Log nguyên văn: `out/log/l2-db-moi.log` |
| N8 | `python3 -I -B khoi-r9/do_pham_vi.py ma\|test <blob nền 695916e> <blob H>` (khối chép nguyên byte từ r9, sha256 `24b890e0…b836`, không đổi so với r8) | 0 · 0 | **ĐẠT** — `PHẠM VI [ma]: ĐẠT` · `PHẠM VI [test]: ĐẠT` |
| N9 | `sc/chay_ca.py … ca-cu` · `… adr` · `… db-cu` | 0 · 0 · 0 | **ĐẠT** — 133/133 (132 ca họ doctrine cũ + `moc_dot_bien_phai_khop_DUNG_MOT_CHO`), 0 bỏ qua · 40/40 `adr_song_*` · vòng đột biến cũ (`packet_loop_test_manh.chay`, nền = 132 ca, pha đột biến = 21 đột biến của nền có ca đích trong họ): `nền: 132/132 đạt · BỎ QUA: 0`, 21/21 dòng `ok … 3 đối chứng khác họ còn sống`, 0 dòng `ĐỎ`, `TỔNG: ĐẠT` |
| N10 | `python3 -I -B sc/do_ruff_ky_tu.py ../kho 695916e… d5d96e7… tmp/l2-ruff` | 0 | **ĐẠT** — delta 0 (mục 6) |
| N11 | `python3 -u -B scripts/tl.py --selftest` (clone H); `git diff --check` trước commit | 0 · 0 | **ĐẠT** — `== tl selftest 1789/1789 ==` (hai số bằng nhau); `git diff --check` không in gì. Vế "trước lần đẩy": executor không đẩy |
| N12 | `git diff --numstat 695916e d5d96e7` | 0 | **ĐẠT** — đúng 4 tệp, +443 ≤ 450 |
| N13 | CI PR trên H | — | **KHÔNG ĐO ĐƯỢC** — cần push và PR (bị cấm ở lượt này). Bước `doc-claims-check strict` của job `gate`, thứ làm lượt 1 bị chặn, nay đo tại chỗ `"ok": true`. Các bước CI khác đã thử tại chỗ: mục 5b |
| N14 | `ci-dot-bien-du.yml` trên H (K7) | — | **KHÔNG ĐO ĐƯỢC** — cần CI trên H đã đẩy; không `workflow_dispatch`. Tại chỗ chỉ có 29 đột biến mới + 21 đột biến cũ của họ doctrine trên 2106 |
| N15 | `kiem-merge` bằng mã `master` trên H | — | **KHÔNG ĐO ĐƯỢC** — cần PR, CI, verdict review và comment `windows: <H> mien` neo đúng H |
| N16 | sau land | — | **KHÔNG ĐO ĐƯỢC** — chỉ đo được sau land |

### 5b. Các bước khác của `ci.yml` đã thử tại chỗ trên clone H

Đây là phép thử thêm của executor để dự báo N13, không thay CI. Bảng này lọc theo các bước executor kịp chạy trong quỹ thời gian — nó KHÔNG phải trần; bước không có trong bảng là chưa đo (mục 8).

| bước của `ci.yml` | lệnh (clone H `ve2/h`, trừ khi ghi khác) | rc | bằng chứng dương |
|---|---|---|---|
| job `gate`: `doc-claims-check strict` | `python3 -B scripts/tl.py doc-claims-check --strict --json` | 0 | `"ok": true`, `flags: []` (mục 4) |
| job `gate`: selftest | `python3 -u -B scripts/tl.py --selftest` | 0 | `== tl selftest 1789/1789 ==` |
| job `gate`: `idiom_py_test` | `python3 -B .claude/dev/idiom_py_test.py` | 0 | `TỔNG: ĐẠT` (7 ca, 9 đột biến) |
| job `gate`: `eol-policy survey` | `python3 -B .githooks/eol_policy.py --all --json` | 0 | `"ok": true`, `violations: []`, `scanned` 19025 |
| job `gate`: `ci_phamvi` | `python3 -B .github/checks/ci_phamvi.py --kiem-bam` · `ci_phamvi_test.py` | 0 · 0 | `OK ci_phamvi (ve BAM)` · `== ci_phamvi_test 7/7 ==` |
| job `gate-ops`: `doctrine-scan` | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 12 tệp` |
| job `gate-ops`: `gate_lifecycle_test` | `python3 -u -B .claude/dev/gate_lifecycle_test.py` | 0 | `gate lifecycle tests: 28/28 ca QUA (bo qua 0, hong 0)` |
| job `gate-ops`: `bien_nhan_v2_test` (neo câu luật trong protocol §8) | `python3 -u -B ops/bien_nhan_v2_test.py` | 0 | `bien_nhan_v2_test: 98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT` (394 s) |
| `chon_reviewer_test` (không thấy trong `ci.yml` theo phép grep `run:`; chạy vì nó phân loại `docs/PROTOCOL_DA_PHIEN.md`) | `python3 -u -B .claude/dev/chon_reviewer_test.py` | 0 | `TỔNG: ĐẠT` (28 ca, 45 đột biến) |
| job `gate-packet-loop-manh` + `gate-packet-loop` | 16 mảnh + gom (N6 (e)) | 0 | `nền: 1823/1823`, `GOM: ĐẠT · 16 mảnh · 1861 ca bắt buộc` |
| job `gate-registry`: `ci_dang_ky_test --chay` | `python3 -u -B .claude/dev/ci_dang_ky_test.py --chay` (clone sạch `ve3/h`) | ĐANG CHẠY | ĐANG CHẠY |

## 6. Ruff delta (N10) và ký tự lạ

`ruff 0.15.15`, `--select F --no-cache --isolated`, hai vế từ `git show <rev>:<tệp>` trong một lệnh:

| tệp | nền `695916e` | H `d5d96e7` | mới | mất |
|---|---|---|---|---|
| `packet_loop.py` | 3 (F841 ×3) | 3 (F841 ×3) | 0 | 0 |
| `packet_loop_test.py` | 13 (F401 ×8, F811 ×3, F541 ×2) | 13 (như nền) | 0 | 0 |

**Delta = 0.** Ký tự lạ (Cc trừ LF, Cf, Zl, Zp, Zs khác dấu cách): `packet_loop.py` 0 và 0; `packet_loop_test.py` 12 và 12.

## 7. Lớp lỗi

**Không lớp mới nào được executor phát hiện ở lượt 2.** Hai lớp đã có, trạng thái trên H mới:

| slug | nguồn | trạng thái trên `d5d96e7` | phép đo đóng lớp | phần chưa đo |
|---|---|---|---|---|
| `con-tro-trong-backtick-bi-cong-khac-doc` | đặc tả r9 mục 19 (executor đo ở lượt 1, chủ kho quyết Q0) | bản vá của r9 đã áp nguyên byte. Đường vào của lớp = mọi chuỗi trong backtick mà packet này THÊM vào tệp `doc-claims-check` quét (sáu khối protocol và ADR-0068), trên mọi lớp có cờ của cổng (L1…L9, L12) | chính cổng ấy trên clone sạch của H: `"ok": true`, `flags: []`, mọi lớp 0, tập advisory trùng nền | CI thật chưa chạy (N13). Executor KHÔNG tự xếp lớp này là "đã vá thật": nhãn do reviewer đặt |
| `phep-dem-ban-sao-khong-phu-ca-tep` | executor lượt 1; nay là hợp đồng (r9 mục 8.3, *Phần đầu tệp*; Q2) | mã và test của lượt 1 giữ nguyên byte | ba ca và ba đột biến "phần đầu tệp": ca đạt ở N6 (d); đột biến ở N7; `sc/do_tham.py` 25/25 | như lượt 1: năm dạng "bản sao không đứng thành đơn vị" là Q3, CHƯA quyết — lượt này không làm gì cho Q3 |

Không `hint_provenance`: không hunk nào bắt nguồn từ hint của reviewer. Không lớp nào lặp tới lần thứ ba ở phía executor.

## 8. Những gì chưa đo, và sai lệch môi trường

- **Mảnh 0/16 phải chạy HAI lần — lỗi giàn đo của executor, khai đủ.** Lần đầu (trong `ve2/h`, 17:14–17:26Z) ra `nền: 109/109 đạt` nhưng rc 1, `TỔNG: 1 lỗi`: carrier WP1174 chụp cây làm việc lúc đầu và lúc cuối (`snapshot_before.file_count` 20514, `snapshot_after.file_count` 20538, hai `content_sha256` khác nhau; `status` rỗng, `index_sha256` giống nhau) và thấy lệch. Nguyên nhân đo được: cùng lúc ấy executor chạy `tl --selftest` (17:18–17:25Z) NGAY TRONG clone `ve2/h`; lệnh ấy sinh tệp bị ignore (`scripts/.tl_state/`, `references/golden/fixtures/` — `git status --short --ignored` của `ve2/h` liệt kê đúng hai thư mục ấy). Không ca nào đỏ. Hiện vật lần đầu giữ ở `out/manh-h2/manh-0.luot-dau-rc1.log` và `.json`. Lần hai chạy trong clone sạch RIÊNG `out/ve3/h` (cùng commit, cùng tree, dựng bằng cùng script), không lệnh nào khác chạy trong clone ấy: rc 0, `nền: 109/109 đạt · BỎ QUA: 0`, `TỔNG: ĐẠT`, `carrier=có`, 512 s (log `l2-manh-0-chay-lai`, `manh-h2/log/manh-0.log`); sau lượt chạy `git status --short --ignored` của `ve3/h` rỗng. Mười lăm mảnh còn lại chạy trong `ve2/h`; chúng không chạy carrier (dòng log `WP1174 carrier: KHÔNG chạy ở mảnh này`), nên không đọc ảnh chụp cây. Ở lượt 1 lỗi này không xảy ra vì selftest đã xong trước khi các mảnh bắt đầu.
- **Lệnh nguyên văn `python .claude/dev/packet_loop_test.py` một tiến trình với đủ bảng 2106 đột biến: KHÔNG chạy** — như lượt 1 (ước nhiều giờ; tác vụ nền bị cắt ở 2 giờ). Thay bằng 16 mảnh + gom theo đúng lệnh của `ci.yml`, và hai vòng đột biến của N7, N9. 2056 đột biến còn lại thuộc N14 (K7) trên CI.
- **Hai ca `CA_DAI`** (`wp1303_target_human_chain`, `wp1303_target_supported_pairs`) không nằm trong 16 mảnh (CI chạy chúng ở `packet-loop-dot-bien.yml`): `wp1303_target_supported_pairs` **ĐẠT** (`nền: 1/1 đạt · BỎ QUA: 0`, `TỔNG: ĐẠT`, rc 0, 1200 s, qua `main()` gốc bằng `sc/chay_nen_tron.py`; log `l2-ca-dai-2`). `wp1303_target_human_chain` **KHÔNG ĐO ĐƯỢC**: khởi lúc 17:14:32Z, executor chủ động DỪNG lúc 17:28Z khi nó chưa in kết quả nào — máy 4 nhân đang chạy 7 tiến trình, và ca này một mình ước ~85 phút (1820 s trong `packet_loop_test_manh.py` × hệ số chậm ~2,8 đo được ở ca kia), không kịp trong quỹ ~100 phút. Ở lượt 1 nó cũng bị cắt khi phiên kết thúc. Vậy ca ấy chưa từng được executor đo trên H nào; trên CI nó chạy ở `packet-loop-dot-bien.yml`, không thuộc cổng bắt buộc `gate-packet-loop`.
- **`.claude/dev/ci_dang_ky_test.py --chay`** (job `gate-registry`): ĐANG CHẠY
- **Các bước CI không thử tại chỗ**: `ops/chay_lease_publish_test.sh`, `ops/ci_duong_nhanh_test.py`, `ops/cong_cu.py kiem-tra` + `ops/cong_cu_test.py`, `ops/nhanh_don_duoc_test.py`, `.githooks/pre_push_test.py`, `.claude/dev/codex_cred_test.py`, `scripts/tl.py workflow-audit` / `golden-test` / `determinism-audit` / `release-*`, `scripts/gen_instructions.py --selftest`, `scripts/tl_core/command_registry_test.py` — `KHÔNG ĐO ĐƯỢC` trong quỹ ~100 phút của lượt này; diff của packet không chạm tệp nào chúng lấy làm đầu vào theo phép `grep` tên `PROTOCOL_DA_PHIEN|docs/adr` ở lượt 1, nhưng đó là lọc theo TÊN TỆP, không phải phép đo hành vi.
- **Python**: máy đo chỉ có 3.13.18; `ci.yml` ghim 3.12. **Windows**: không đo (miễn theo C3).
- **N5 vế reviewer, mirror reviewer, `core.abbrev 7` ở clone reviewer**: việc của phiên điều phối và reviewer.
- **Ngày và URL của comment duyệt băm r9** (`issuecomment-7192181084`): executor chỉ đọc được qua tệp lease; không đo bằng REST (MCP github không kết nối, `curl`/`gh` bị chốt quyền từ chối ở lượt 1; lượt 2 không thử lại).
- **Model/effort thực phục vụ**: phiên tự nhận `claude-fable-5-2`; effort `KHONG_DO_DUOC` từ bên trong.
- **Cách ghi vào `.claude/dev/`**: lượt 2 chỉ dùng `git checkout -b`, `git cherry-pick`, `git apply`, `git add`, `git commit`. Không plumbing, không Edit/Write vào `kho/`. `git status --short --ignored` của `kho/` sau commit: chỉ có `.claude/.packet_state/` (bị ignore; chứa `session-start.ran` do hook phiên tạo, không phải do executor).
- **`SyntaxWarning: invalid escape sequence '\\d'`** ở `packet_loop_test.py:3811` trong mọi log: dòng của nền (dòng 3786 ở base), không thuộc diff.
- **Hai tác vụ nền của lượt 1 bị cắt khi phiên trước kết thúc** (`wp1303_target_human_chain` và `ci_dang_ky_test --chay` trên H lượt 1): không có kết quả; HANDOFF lượt 1 vì vậy còn ô chờ ở N6 (e) — lượt 2 đo lại trên H mới.

## 9. Câu hỏi cho chủ kho

| # | mã E | câu hỏi | khuyến nghị của executor |
|---|---|---|---|
| Q4 | E5 | Dòng Trạng thái của ADR-0068 trên H dẫn lần duyệt băm **r8**: ngày `2026-11-21`, `spec_hash` `98790505…0834`, `r8`, `issuecomment-7058374374`. Mục 8.1 của r9 (không đổi so với r8) định nghĩa `<64 hex>` là "sha256 của chính tệp đặc tả được duyệt" và `<N>` là revision của tệp ấy; đặc tả đang hiệu lực của lease g2 là **r9** (`28de9d57…6f7c`, duyệt ở `issuecomment-7192181084` theo lease). Executor GIỮ dòng r8 vì: (i) chỉ thị lượt 2 khai ngày `2026-11-21` là đúng và không liệt kê ADR trong việc phải sửa; (ii) r9 khai khối `adr` không đổi; (iii) hồ sơ dựng r9 của phiên điều phối đo trên H lượt 1 với ADR nguyên trạng; (iv) N1 chỉ đòi dòng khớp DẠNG, và dòng hiện tại khớp. Nhưng một reviewer có thể đọc 8.1 thành "phải dẫn r9". Chủ kho muốn dòng ấy dẫn lần duyệt nào? | giữ dòng r8 (ADR được chấp nhận ở lần duyệt ấy; văn bản ADR không đổi ở r9). Nếu chủ kho chọn r9 thì sửa đúng một dòng — hash, `r9`, URL, và ngày UTC của comment duyệt r9 phải ĐO bằng REST (executor không đọc được REST) — sinh SHA mới, nên quyết TRƯỚC khi gọi review |

Q3 của lượt 1 (năm dạng bản sao không đứng thành đơn vị; thẻ HTML giữa dòng) vẫn mở theo chỉ thị; lượt này không làm gì cho nó. Không có câu hỏi mã E1, E2, E3, E4.

## 10. Hiện vật lượt 2 ở `out/`

- `HANDOFF-l2.md` (tệp này) · `l2/COMMIT_MSG.txt` · `l2/wp1466-r9.patch` · `l2/spec-r8.md`, `l2/spec-r9.md` (hai blob đặc tả) · `l2/SHA256SUMS` · `l2/wp1466-r9-g2-d5d96e7.bundle`
- script mới hay sửa ở lượt 2: `sc/sua_r9.py` (dựng patch), `sc/so_doc_claims.py`; `sc/do_adr.py` và `sc/do_protocol.py` đổi băm đặc tả kỳ vọng sang r9 (và `do_protocol.py` thêm phép đếm 18 con trỏ không backtick); `sc/chay.py`, `sc/chay_nen_tron.py` như cuối lượt 1
- `khoi-r9/` — khối `do-pham-vi`, `so-dang-ky`, `adr`, `khoa`, `p2-moi` chép nguyên byte từ r9 · `ve2/h`, `ve2/nen` — hai clone đo · `manh-h2/` — bản ghi và log 16 mảnh · `log/l2-*.log`
- Hiện vật lượt 1 (`HANDOFF.md`, `log/h-*.log`, `ve/`, `manh-h/`, `lam/`…) giữ nguyên, không sửa.

HEAD=d5d96e709e37979986d75742edf0fb9942c18b61 TEST=1823/1823 NUMSTAT=+443 -4 TRAN=dat DOC_CLAIMS=ok
